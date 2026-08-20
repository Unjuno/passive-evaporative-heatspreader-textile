"""Self-consistent 1-D moist-air corridor screening model.

Purpose
-------
Replace the prescribed channel temperature/RH state used in
``corridor_buoyancy_screen.py`` with a low-order coupled calculation of:

- signed buoyancy-driven corridor velocity;
- channel dry-bulb temperature;
- channel water-vapor concentration;
- wet-wall temperature;
- evaporation and body-side heat flow.

The model treats a straight rectangular duct with ambient renewal primarily at
its ends. For a trial speed, heat and vapor exchange approach a wet-wall state
exponentially along the duct. The wet-wall temperature is solved from a mean
energy balance. The resulting mean moist-air density determines a new
buoyancy-driven velocity through laminar rectangular-duct friction. Signed
velocity roots are then found self-consistently.

This remains a SCREENING model, not CFD. Important omissions include axial
molecular diffusion, distributed lateral ambient exchange, entrance/exit
mixing, turbulence, garment curvature, walking/wind forcing, spatially varying
wall wetness, exact rectangular-duct Nusselt/Sherwood boundary-condition
dependence, radiation inside the channel, and coupling to a full 2-D/3-D heat
spreader.

The model reports both axial mass Péclet number and a mean vapor-driving-force
retention factor. A large Pe alone does not establish useful renewal if the
channel also has a very large mass-transfer NTU and approaches saturation.

Project Pe labels are heuristics, not external standards:

    Pe < 1          diffusion-dominated
    1 <= Pe < 10   mixed / weak advection
    Pe >= 10       advection-relevant
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.optimize import brentq

try:
    from simulations.passive_rib_screen import (
        D_V,
        G,
        K_AIR,
        L_V,
        P_ATM,
        R_D,
        R_V,
        T_SKIN,
        p_sat,
    )
except ModuleNotFoundError:  # direct execution
    from passive_rib_screen import D_V, G, K_AIR, L_V, P_ATM, R_D, R_V, T_SKIN, p_sat

MU_AIR = 1.90e-5  # Pa s, fixed screening value
CP_AIR = 1006.0  # J/(kg K), fixed screening value
NU_SCREEN = 7.54  # fixed fully-developed laminar transfer screen
SH_SCREEN = 7.54  # heat/mass analogue used only for screening


@dataclass(frozen=True)
class CorridorSolution:
    velocity_m_s: float
    direction: str
    transport_regime: str
    surface_temp_C: float
    mean_air_temp_C: float
    mean_air_RH: float
    outlet_air_temp_C: float
    outlet_air_RH: float
    mean_density_kg_m3: float
    ambient_density_kg_m3: float
    Pe_mass_length: float
    NTU_heat: float
    NTU_mass: float
    vapor_driving_force_retention: float
    body_heat_flux_W_m2_wet: float
    evaporation_flux_kg_m2_s_wet: float
    hydraulic_diameter_mm: float
    poiseuille_number: float
    supersaturation_flag: bool


def saturated_vapor_density(temp_c: float) -> float:
    return float(p_sat(temp_c) / (R_V * (temp_c + 273.15)))


def ambient_vapor_density(temp_c: float, rh: float) -> float:
    if not 0.0 <= rh <= 1.0:
        raise ValueError("RH must be between 0 and 1")
    return float(rh * p_sat(temp_c) / (R_V * (temp_c + 273.15)))


def moist_air_density_from_vapor_density(temp_c: float, rho_v: float) -> float:
    """Ideal-mixture moist-air density from dry-bulb T and vapor density."""
    tk = temp_c + 273.15
    pv = rho_v * R_V * tk
    if pv >= P_ATM:
        raise ValueError("vapor partial pressure exceeds total pressure")
    pd = P_ATM - pv
    return float(pd / (R_D * tk) + rho_v)


def relative_humidity_from_vapor_density(temp_c: float, rho_v: float) -> float:
    tk = temp_c + 273.15
    pv = rho_v * R_V * tk
    return float(pv / p_sat(temp_c))


def rectangular_poiseuille_number(width_m: float, depth_m: float) -> float:
    """Darcy Poiseuille number f_D*Re for a rectangular duct."""
    if width_m <= 0.0 or depth_m <= 0.0:
        raise ValueError("duct dimensions must be positive")
    alpha = min(width_m, depth_m) / max(width_m, depth_m)
    return float(
        96.0
        * (
            1.0
            - 1.3553 * alpha
            + 1.9467 * alpha**2
            - 1.7012 * alpha**3
            + 0.9564 * alpha**4
            - 0.2537 * alpha**5
        )
    )


def mean_approach_factor(ntu: float) -> float:
    """Mean of exp(-NTU*z/L) over 0<=z<=L."""
    if ntu < 0.0:
        raise ValueError("NTU must be nonnegative")
    if ntu < 1e-8:
        return 1.0 - 0.5 * ntu
    if ntu > 700.0:
        return 1.0 / ntu
    return float(-np.expm1(-ntu) / ntu)


def transport_regime(pe: float) -> str:
    if pe < 1.0:
        return "diffusion-dominated"
    if pe < 10.0:
        return "mixed-weak-advection"
    return "advection-relevant"


def _state_for_speed(
    speed_m_s: float,
    width_mm: float,
    depth_mm: float,
    length_mm: float,
    ambient_c: float,
    ambient_rh: float,
    u_body_W_m2K: float,
    wet_sidewalls: bool,
) -> dict[str, float | bool]:
    """Solve mean thermodynamic state for a positive trial speed magnitude."""
    if speed_m_s <= 0.0:
        raise ValueError("trial speed must be positive")
    if width_mm <= 0.0 or depth_mm <= 0.0 or length_mm <= 0.0:
        raise ValueError("corridor dimensions must be positive")
    if u_body_W_m2K <= 0.0:
        raise ValueError("u_body must be positive")

    width = width_mm * 1e-3
    depth = depth_mm * 1e-3
    length = length_mm * 1e-3
    area = width * depth
    flow_perimeter = 2.0 * (width + depth)
    hydraulic_diameter = 4.0 * area / flow_perimeter
    wet_perimeter = width + 2.0 * depth if wet_sidewalls else width

    h_c = NU_SCREEN * K_AIR / hydraulic_diameter
    k_m = SH_SCREEN * D_V / hydraulic_diameter

    rho_v_in = ambient_vapor_density(ambient_c, ambient_rh)
    rho_in = moist_air_density_from_vapor_density(ambient_c, rho_v_in)
    mass_flow = rho_in * speed_m_s * area

    ntu_heat = h_c * wet_perimeter * length / (mass_flow * CP_AIR)
    ntu_mass = k_m * wet_perimeter * length / (speed_m_s * area)
    phi_h = mean_approach_factor(ntu_heat)
    phi_m = mean_approach_factor(ntu_mass)

    def wall_balance(surface_c: float) -> float:
        rho_v_surface = saturated_vapor_density(surface_c)
        mean_air_c = surface_c + (ambient_c - surface_c) * phi_h
        mean_rho_v = rho_v_surface - (rho_v_surface - rho_v_in) * phi_m
        evaporation_flux = max(k_m * (rho_v_surface - mean_rho_v), 0.0)
        body_to_wall = u_body_W_m2K * (T_SKIN - surface_c)
        air_to_wall = h_c * (mean_air_c - surface_c)
        return body_to_wall + air_to_wall - L_V * evaporation_flux

    low, high = 10.0, 45.0
    f_low = wall_balance(low)
    f_high = wall_balance(high)
    roots: list[float] = []
    if f_low == 0.0:
        roots = [low]
    elif f_high == 0.0:
        roots = [high]
    elif f_low * f_high < 0.0:
        roots = [brentq(wall_balance, low, high, maxiter=100)]
    else:
        grid = np.linspace(low, high, 81)
        vals = np.array([wall_balance(t) for t in grid])
        for idx in np.where(vals[:-1] * vals[1:] <= 0.0)[0]:
            try:
                roots.append(brentq(wall_balance, grid[idx], grid[idx + 1], maxiter=100))
            except ValueError:
                continue
    if not roots:
        raise RuntimeError("wet-wall temperature root not found")

    surface_c = max(roots)
    rho_v_surface = saturated_vapor_density(surface_c)
    mean_air_c = surface_c + (ambient_c - surface_c) * phi_h
    mean_rho_v = rho_v_surface - (rho_v_surface - rho_v_in) * phi_m

    exp_h = 0.0 if ntu_heat > 700.0 else float(np.exp(-ntu_heat))
    exp_m = 0.0 if ntu_mass > 700.0 else float(np.exp(-ntu_mass))
    outlet_air_c = surface_c + (ambient_c - surface_c) * exp_h
    outlet_rho_v = rho_v_surface - (rho_v_surface - rho_v_in) * exp_m

    mean_density = moist_air_density_from_vapor_density(mean_air_c, mean_rho_v)
    po = rectangular_poiseuille_number(width, depth)
    velocity_coefficient = 2.0 * hydraulic_diameter**2 / (po * MU_AIR)
    evaporation_flux = max(k_m * (rho_v_surface - mean_rho_v), 0.0)

    return {
        "surface_temp_C": surface_c,
        "mean_air_temp_C": mean_air_c,
        "mean_air_RH": relative_humidity_from_vapor_density(mean_air_c, mean_rho_v),
        "outlet_air_temp_C": outlet_air_c,
        "outlet_air_RH": relative_humidity_from_vapor_density(outlet_air_c, outlet_rho_v),
        "mean_density_kg_m3": mean_density,
        "ambient_density_kg_m3": rho_in,
        "velocity_coefficient": velocity_coefficient,
        "Pe_mass_length": speed_m_s * length / D_V,
        "NTU_heat": ntu_heat,
        "NTU_mass": ntu_mass,
        "vapor_driving_force_retention": phi_m,
        "body_heat_flux_W_m2_wet": u_body_W_m2K * (T_SKIN - surface_c),
        "evaporation_flux_kg_m2_s_wet": evaporation_flux,
        "hydraulic_diameter_mm": hydraulic_diameter * 1e3,
        "poiseuille_number": po,
        "supersaturation_flag": relative_humidity_from_vapor_density(outlet_air_c, outlet_rho_v) > 1.001,
    }


def solve_corridor(
    width_mm: float,
    depth_mm: float,
    length_mm: float,
    ambient_c: float = 35.0,
    ambient_rh: float = 0.70,
    u_body_W_m2K: float = 100.0,
    wet_sidewalls: bool = False,
    vertical_projection: float = 1.0,
    velocity_scan_max_m_s: float = 0.10,
) -> list[CorridorSolution]:
    """Return all signed self-consistent buoyancy/friction roots."""
    if not -1.0 <= vertical_projection <= 1.0:
        raise ValueError("vertical_projection must be between -1 and 1")
    if abs(vertical_projection) < 1e-12:
        return []

    def residual(velocity: float) -> float:
        state = _state_for_speed(
            max(abs(velocity), 1e-8),
            width_mm,
            depth_mm,
            length_mm,
            ambient_c,
            ambient_rh,
            u_body_W_m2K,
            wet_sidewalls,
        )
        pressure_gradient = (
            G
            * vertical_projection
            * (state["ambient_density_kg_m3"] - state["mean_density_kg_m3"])
        )
        predicted = state["velocity_coefficient"] * pressure_gradient
        return float(velocity - predicted)

    magnitudes = np.logspace(-7, np.log10(velocity_scan_max_m_s), 140)
    scan = np.concatenate((-magnitudes[::-1], magnitudes))
    vals = np.array([residual(v) for v in scan])
    roots: list[float] = []

    for idx in np.where(vals[:-1] * vals[1:] < 0.0)[0]:
        try:
            root = brentq(residual, scan[idx], scan[idx + 1], maxiter=120)
        except ValueError:
            continue
        if not roots or all(abs(root - existing) > 1e-7 for existing in roots):
            roots.append(float(root))

    solutions: list[CorridorSolution] = []
    for velocity in roots:
        state = _state_for_speed(
            max(abs(velocity), 1e-8),
            width_mm,
            depth_mm,
            length_mm,
            ambient_c,
            ambient_rh,
            u_body_W_m2K,
            wet_sidewalls,
        )
        if velocity > 1e-6:
            direction = "positive-axis"
        elif velocity < -1e-6:
            direction = "negative-axis"
        else:
            direction = "near-neutral"
        solutions.append(
            CorridorSolution(
                velocity_m_s=velocity,
                direction=direction,
                transport_regime=transport_regime(float(state["Pe_mass_length"])),
                surface_temp_C=float(state["surface_temp_C"]),
                mean_air_temp_C=float(state["mean_air_temp_C"]),
                mean_air_RH=float(state["mean_air_RH"]),
                outlet_air_temp_C=float(state["outlet_air_temp_C"]),
                outlet_air_RH=float(state["outlet_air_RH"]),
                mean_density_kg_m3=float(state["mean_density_kg_m3"]),
                ambient_density_kg_m3=float(state["ambient_density_kg_m3"]),
                Pe_mass_length=float(state["Pe_mass_length"]),
                NTU_heat=float(state["NTU_heat"]),
                NTU_mass=float(state["NTU_mass"]),
                vapor_driving_force_retention=float(state["vapor_driving_force_retention"]),
                body_heat_flux_W_m2_wet=float(state["body_heat_flux_W_m2_wet"]),
                evaporation_flux_kg_m2_s_wet=float(state["evaporation_flux_kg_m2_s_wet"]),
                hydraulic_diameter_mm=float(state["hydraulic_diameter_mm"]),
                poiseuille_number=float(state["poiseuille_number"]),
                supersaturation_flag=bool(state["supersaturation_flag"]),
            )
        )
    return solutions


def run_screen() -> pd.DataFrame:
    """Generate the deterministic self-consistent corridor screen."""
    rows: list[dict[str, float | str | bool | int]] = []
    environments = (
        (35.0, 0.50),
        (35.0, 0.70),
        (35.0, 0.85),
        (40.0, 0.70),
    )
    for ambient_c, ambient_rh in environments:
        for width_mm, depth_mm in ((3.0, 2.0), (6.0, 3.0), (10.0, 5.0)):
            for length_mm in (20.0, 50.0, 100.0, 200.0):
                solutions = solve_corridor(
                    width_mm=width_mm,
                    depth_mm=depth_mm,
                    length_mm=length_mm,
                    ambient_c=ambient_c,
                    ambient_rh=ambient_rh,
                )
                for root_index, sol in enumerate(solutions):
                    rows.append(
                        {
                            "classification": "SIMULATION/SCREENING",
                            "ambient_C": ambient_c,
                            "ambient_RH_percent": ambient_rh * 100.0,
                            "width_mm": width_mm,
                            "depth_mm": depth_mm,
                            "length_mm": length_mm,
                            "root_index": root_index,
                            **sol.__dict__,
                        }
                    )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = run_screen()
    selected = df[
        (df["length_mm"] == 100.0)
        & (df["ambient_RH_percent"].isin([50.0, 70.0, 85.0]))
        & (df["ambient_C"] == 35.0)
    ]
    print("Selected 35 C / 100 mm corridor cases:")
    print(
        selected[
            [
                "ambient_RH_percent",
                "width_mm",
                "depth_mm",
                "velocity_m_s",
                "transport_regime",
                "Pe_mass_length",
                "NTU_mass",
                "vapor_driving_force_retention",
                "surface_temp_C",
                "mean_air_RH",
                "body_heat_flux_W_m2_wet",
            ]
        ].to_string(index=False)
    )
