"""Passive evaporative rib-screening model.

Low-order research model for comparing a structured passive evaporative textile
against a flat fast-dry control at the same liquid-water input.

This is not CFD and not a validated garment-performance predictor.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import brentq

# Geometry / environment
A = 0.30  # m^2 projected active area
T_SKIN = 34.0  # degC
L_CHAR = 0.50  # m
P_ATM = 101325.0  # Pa
G = 9.80665  # m/s^2
R_D = 287.058  # J/(kg K)
R_V = 461.5  # J/(kg K)
NU = 1.66e-5  # m^2/s
ALPHA_AIR = 2.35e-5  # m^2/s
D_V = 2.80e-5  # m^2/s
K_AIR = 0.027  # W/(m K)
PR = NU / ALPHA_AIR
SC = NU / D_V
L_V = 2.42e6  # J/kg
H_RAD = 6.0  # W/(m^2 K), linearized screening value

# Effective body-to-evaporator coupling values used in the current screen.
# These are model parameters, not measurements.
U_FLAT = 60.0  # W/(m^2 K)
U_PREVIEW = 100.0  # W/(m^2 K)


def p_sat(temp_c: float | np.ndarray) -> float | np.ndarray:
    """Approximate saturation vapor pressure of water [Pa]."""
    temp_c = np.asarray(temp_c)
    return 611.21 * np.exp((18.678 - temp_c / 234.5) * (temp_c / (257.14 + temp_c)))


def rho_v_sat(temp_c: float) -> float:
    """Saturated water-vapor density [kg/m^3]."""
    return float(p_sat(temp_c) / (R_V * (temp_c + 273.15)))


def rho_moist(temp_c: float, rh: float) -> float:
    """Moist-air density [kg/m^3] using ideal dry-air + vapor mixture."""
    pv = rh * float(p_sat(temp_c))
    pd = P_ATM - pv
    tk = temp_c + 273.15
    return pd / (R_D * tk) + pv / (R_V * tk)


def churchill_chu(rayleigh: float, x: float) -> float:
    """Vertical-plate screening correlation used for heat/mass analogies."""
    rayleigh = max(float(rayleigh), 0.0)
    return (
        0.825
        + 0.387 * rayleigh ** (1.0 / 6.0)
        / (1.0 + (0.492 / x) ** (9.0 / 16.0)) ** (8.0 / 27.0)
    ) ** 2


def passive_coeffs(surface_c: float, ambient_c: float, rh: float) -> tuple[float, float]:
    """Return low-order natural-convection heat and mass coefficients."""
    rho_inf = rho_moist(ambient_c, rh)
    rho_s = rho_moist(surface_c, 1.0)
    beta_eff = abs(rho_s - rho_inf) / rho_inf
    gr = G * beta_eff * L_CHAR**3 / NU**2
    h = churchill_chu(gr * PR, PR) * K_AIR / L_CHAR
    km = churchill_chu(gr * SC, SC) * D_V / L_CHAR
    return h, km


def equilibrium(
    ambient_c: float,
    rh: float,
    water_gph: float,
    exchange_multiplier: float,
    u_body: float,
) -> dict[str, float] | None:
    """Solve a stable surface-temperature equilibrium.

    Positive body_cooling_W means heat is drawn from the artificial skin toward
    the evaporating surface in this model.
    """
    water_flux_cap = (water_gph / 1000.0 / 3600.0) / A

    def residual(surface_c: float) -> float:
        h, km = passive_coeffs(surface_c, ambient_c, rh)
        q_body = u_body * (T_SKIN - surface_c)
        q_conv = exchange_multiplier * h * (ambient_c - surface_c)
        q_rad = H_RAD * (ambient_c - surface_c)
        vapor_drive = max(
            rho_v_sat(surface_c) - rh * rho_v_sat(ambient_c),
            0.0,
        )
        m_capacity = exchange_multiplier * km * vapor_drive
        m_evap = min(m_capacity, water_flux_cap)
        q_lat = L_V * m_evap
        return q_body + q_conv + q_rad - q_lat

    grid = np.linspace(18.0, 39.5, 120)
    vals = np.array([residual(t) for t in grid])
    roots: list[tuple[float, float, float]] = []

    for idx in np.where(vals[:-1] * vals[1:] <= 0.0)[0]:
        try:
            root = brentq(residual, grid[idx], grid[idx + 1], maxiter=80)
        except ValueError:
            continue

        eps = 1e-3
        derivative = (residual(root + eps) - residual(root - eps)) / (2.0 * eps)
        if derivative >= 0.0:
            continue

        _, km = passive_coeffs(root, ambient_c, rh)
        vapor_drive = max(rho_v_sat(root) - rh * rho_v_sat(ambient_c), 0.0)
        m_capacity = exchange_multiplier * km * vapor_drive
        m_evap = min(m_capacity, water_flux_cap)
        q_body_w = u_body * (T_SKIN - root) * A
        evap_gph = m_evap * A * 3600.0 * 1000.0
        roots.append((root, q_body_w, evap_gph))

    if not roots:
        return None

    surface_c, body_cooling_w, evap_gph = max(roots, key=lambda item: item[1])
    return {
        "surface_temp_C": surface_c,
        "body_cooling_W": body_cooling_w,
        "evaporation_g_h": evap_gph,
    }


def panel_geometric_multiplier(rib_height_mm: float, pitch_mm: float) -> float:
    """Rectangular-rib geometric multiplier, local to the structured panel."""
    return 1.0 + 2.0 * rib_height_mm / pitch_mm


def effective_exchange_multiplier(
    panel_fraction: float,
    rib_height_mm: float,
    pitch_mm: float,
    accessibility: float,
) -> float:
    """Whole-garment effective exchange multiplier M."""
    g_panel = panel_geometric_multiplier(rib_height_mm, pitch_mm)
    return 1.0 + accessibility * panel_fraction * (g_panel - 1.0)


def run_screen() -> pd.DataFrame:
    """Generate a compact design screen for the current primary condition."""
    ambient_c = 35.0
    rh = 0.70
    water_gph = 150.0

    control = equilibrium(ambient_c, rh, water_gph, 1.0, U_FLAT)
    if control is None:
        raise RuntimeError("Control equilibrium not found")

    rows: list[dict[str, float]] = []
    for panel_fraction in (0.45, 0.55, 0.65, 0.70):
        for rib_height_mm in (2.0, 2.5, 3.0):
            for pitch_mm in (0.8, 1.0, 1.5):
                for accessibility in (0.40, 0.55, 0.70, 0.85):
                    m_eff = effective_exchange_multiplier(
                        panel_fraction,
                        rib_height_mm,
                        pitch_mm,
                        accessibility,
                    )
                    result = equilibrium(ambient_c, rh, water_gph, m_eff, U_PREVIEW)
                    if result is None:
                        continue
                    rows.append(
                        {
                            "panel_fraction": panel_fraction,
                            "rib_height_mm": rib_height_mm,
                            "pitch_mm": pitch_mm,
                            "accessibility_alpha": accessibility,
                            "G_panel": panel_geometric_multiplier(rib_height_mm, pitch_mm),
                            "M": m_eff,
                            "body_cooling_W": result["body_cooling_W"],
                            "gain_over_flat_W": result["body_cooling_W"]
                            - control["body_cooling_W"],
                            "evaporation_g_h": result["evaporation_g_h"],
                            "surface_temp_C": result["surface_temp_C"],
                        }
                    )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = run_screen()
    print(df.sort_values("gain_over_flat_W", ascending=False).head(20).to_string(index=False))
