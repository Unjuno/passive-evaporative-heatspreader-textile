"""Passive evaporative rib-screening model.

Low-order research model for comparing a structured passive evaporative textile
against a flat fast-dry control at the same liquid-water input.

Important numerical note
------------------------
The nonlinear heat/mass balance can have more than one stable equilibrium.
Earlier exploratory screens selected the stable root with the largest modeled
body-side cooling, which can create an optimistic discontinuous jump. This
version exposes all stable roots and defaults to the warmer/conservative stable
branch when a single design value is requested.

This is not CFD and not a validated garment-performance predictor.
"""

from __future__ import annotations

from dataclasses import dataclass

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


@dataclass(frozen=True)
class Equilibrium:
    surface_temp_C: float
    body_cooling_W: float
    evaporation_g_h: float
    residual_slope: float


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


def stable_equilibria(
    ambient_c: float,
    rh: float,
    water_gph: float,
    exchange_multiplier: float,
    u_body: float,
    grid_points: int = 1200,
) -> list[Equilibrium]:
    """Return all numerically detected stable equilibria.

    Stability criterion follows C dT/dt = residual(T): a negative local slope
    of residual versus surface temperature is treated as stable.
    """
    water_flux_cap = (water_gph / 1000.0 / 3600.0) / A

    def terms(surface_c: float) -> tuple[float, float, float]:
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
        residual = q_body + q_conv + q_rad - q_lat
        return residual, q_body, m_evap

    grid = np.linspace(18.0, 39.5, grid_points)
    vals = np.array([terms(t)[0] for t in grid])
    roots: list[Equilibrium] = []

    for idx in np.where(vals[:-1] * vals[1:] <= 0.0)[0]:
        try:
            root = brentq(lambda x: terms(x)[0], grid[idx], grid[idx + 1], maxiter=100)
        except ValueError:
            continue

        eps = 1e-4
        slope = (terms(root + eps)[0] - terms(root - eps)[0]) / (2.0 * eps)
        if slope >= 0.0:
            continue

        _, q_body, m_evap = terms(root)
        roots.append(
            Equilibrium(
                surface_temp_C=float(root),
                body_cooling_W=float(q_body * A),
                evaporation_g_h=float(m_evap * A * 3600.0 * 1000.0),
                residual_slope=float(slope),
            )
        )

    # Deduplicate roots that may be bracketed twice by a near-zero grid point.
    unique: list[Equilibrium] = []
    for root in sorted(roots, key=lambda r: r.surface_temp_C):
        if not unique or abs(root.surface_temp_C - unique[-1].surface_temp_C) > 1e-5:
            unique.append(root)
    return unique


def select_equilibrium(roots: list[Equilibrium], policy: str = "warm") -> Equilibrium | None:
    """Select one stable root with an explicit policy.

    warm: highest surface temperature / lowest-cooling stable branch; conservative.
    cool: lowest surface temperature / highest-cooling stable branch; optimistic.
    """
    if not roots:
        return None
    if policy == "warm":
        return max(roots, key=lambda r: r.surface_temp_C)
    if policy == "cool":
        return min(roots, key=lambda r: r.surface_temp_C)
    raise ValueError("policy must be 'warm' or 'cool'")


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
    """Generate a design screen reporting conservative and optimistic branches."""
    ambient_c = 35.0
    rh = 0.70
    water_gph = 150.0

    control_roots = stable_equilibria(ambient_c, rh, water_gph, 1.0, U_FLAT)
    control = select_equilibrium(control_roots, "warm")
    if control is None:
        raise RuntimeError("Control equilibrium not found")

    rows: list[dict[str, float | int]] = []
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
                    roots = stable_equilibria(ambient_c, rh, water_gph, m_eff, U_PREVIEW)
                    warm = select_equilibrium(roots, "warm")
                    cool = select_equilibrium(roots, "cool")
                    if warm is None or cool is None:
                        continue
                    rows.append(
                        {
                            "panel_fraction": panel_fraction,
                            "rib_height_mm": rib_height_mm,
                            "pitch_mm": pitch_mm,
                            "accessibility_alpha": accessibility,
                            "G_panel": panel_geometric_multiplier(rib_height_mm, pitch_mm),
                            "M": m_eff,
                            "n_stable_roots": len(roots),
                            "warm_body_cooling_W": warm.body_cooling_W,
                            "warm_gain_over_flat_W": warm.body_cooling_W - control.body_cooling_W,
                            "cool_body_cooling_W": cool.body_cooling_W,
                            "cool_gain_over_flat_W": cool.body_cooling_W - control.body_cooling_W,
                            "warm_surface_temp_C": warm.surface_temp_C,
                            "cool_surface_temp_C": cool.surface_temp_C,
                        }
                    )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = run_screen()
    cols = [
        "panel_fraction",
        "rib_height_mm",
        "pitch_mm",
        "accessibility_alpha",
        "M",
        "n_stable_roots",
        "warm_gain_over_flat_W",
        "cool_gain_over_flat_W",
    ]
    print(df.sort_values("warm_gain_over_flat_W", ascending=False)[cols].head(20).to_string(index=False))
