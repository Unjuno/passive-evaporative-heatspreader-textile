"""Coupled 1-D thermal/vapor screen for a laterally open wet valley.

Solves valley-air temperature, water-vapor density, wet-surface temperature,
evaporation, body-side heat flux, and ambient sensible heat supplied to the wet
surface. Heat and vapor lateral exchange remain separately parameterized for
model-form sensitivity.

This is a fully-wet transfer-capacity screen, not CFD.  Liquid-feed limits are
audited separately.  ``skin_c`` is explicit because the environmental heat-flow
sign boundary depends strongly on the controlled skin/artificial-skin
setpoint; 34 °C is only the repository's primary bench condition.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

try:
    from simulations.passive_rib_screen import (
        D_V,
        K_AIR,
        L_V,
        P_ATM,
        R_D,
        R_V,
        T_SKIN,
        p_sat,
    )
except ModuleNotFoundError:
    from passive_rib_screen import D_V, K_AIR, L_V, P_ATM, R_D, R_V, T_SKIN, p_sat

CP_AIR = 1006.0
NU_SCREEN = 7.54
SH_SCREEN = 7.54
U_BODY_DEFAULT = 100.0


@dataclass(frozen=True)
class OpenValleyThermalResult:
    ambient_C: float
    ambient_RH: float
    skin_C: float
    width_mm: float
    depth_mm: float
    length_mm: float
    velocity_mm_s: float
    delta_vapor_mm: float
    delta_heat_mm: float
    converged: bool
    iterations: int
    mean_surface_C: float
    center_surface_C: float
    mean_air_C: float
    mean_air_RH: float
    mean_evap_flux_g_m2_h: float
    mean_body_heat_flux_W_m2: float
    center_body_heat_flux_W_m2: float
    mean_air_to_wall_W_m2: float
    condensation_fraction: float
    k_m_wall_m_s: float
    k_m_lateral_m_s: float
    h_wall_W_m2K: float
    h_lateral_W_m2K: float


def saturated_vapor_density(temp_c: np.ndarray | float) -> np.ndarray:
    temp = np.asarray(temp_c, dtype=float)
    return p_sat(temp) / (R_V * (temp + 273.15))


def saturated_vapor_density_derivative(temp_c: np.ndarray | float) -> np.ndarray:
    temp = np.asarray(temp_c, dtype=float)
    eps = 1e-3
    return (saturated_vapor_density(temp + eps) - saturated_vapor_density(temp - eps)) / (2.0 * eps)


def vapor_density(temp_c: float, rh: float) -> float:
    if not 0.0 <= rh <= 1.0:
        raise ValueError("RH must be between 0 and 1")
    return float(rh * saturated_vapor_density(temp_c))


def moist_air_density(temp_c: float, vapor_density_kg_m3: float) -> float:
    tk = temp_c + 273.15
    pv = vapor_density_kg_m3 * R_V * tk
    pd = P_ATM - pv
    return float(pd / (R_D * tk) + vapor_density_kg_m3)


def hydraulic_diameter(width_m: float, depth_m: float) -> float:
    if width_m <= 0.0 or depth_m <= 0.0:
        raise ValueError("dimensions must be positive")
    return 4.0 * width_m * depth_m / (2.0 * (width_m + depth_m))


def _solve_linear_field(
    source_target: np.ndarray,
    source_conductance_per_length: float,
    ambient_conductance_per_length: float,
    ambient_value: float,
    axial_diffusive_conductance: float,
    axial_advective_conductance: float,
    length_m: float,
    nx: int,
) -> np.ndarray:
    dz = length_m / (nx - 1)
    n = nx - 2

    lower = np.full(n - 1, axial_diffusive_conductance / dz**2)
    diagonal = np.full(
        n,
        -2.0 * axial_diffusive_conductance / dz**2
        - source_conductance_per_length
        - ambient_conductance_per_length,
    )
    upper = np.full(n - 1, axial_diffusive_conductance / dz**2)

    if axial_advective_conductance >= 0.0:
        diagonal += -axial_advective_conductance / dz
        lower += axial_advective_conductance / dz
    else:
        diagonal += axial_advective_conductance / dz
        upper += -axial_advective_conductance / dz

    rhs = -(
        source_conductance_per_length * source_target[1:-1]
        + ambient_conductance_per_length * ambient_value
    )
    rhs[0] -= lower[0] * ambient_value
    rhs[-1] -= upper[-1] * ambient_value

    solution = np.empty(nx)
    solution[0] = ambient_value
    solution[-1] = ambient_value
    matrix = diags((lower, diagonal, upper), offsets=(-1, 0, 1), format="csr")
    solution[1:-1] = spsolve(matrix, rhs)
    return solution


def solve_open_valley_thermal(
    ambient_c: float,
    ambient_rh: float,
    width_mm: float = 6.0,
    depth_mm: float = 3.0,
    length_mm: float = 50.0,
    velocity_mm_s: float = 0.0,
    delta_vapor_mm: float = 0.5,
    delta_heat_mm: float = 0.5,
    u_body_W_m2K: float = U_BODY_DEFAULT,
    skin_c: float = T_SKIN,
    nx: int = 81,
    max_iterations: int = 120,
    tolerance: float = 2e-7,
) -> OpenValleyThermalResult:
    """Solve coupled wet-wall / valley-air heat and vapor balances."""
    if width_mm <= 0 or depth_mm <= 0 or length_mm <= 0:
        raise ValueError("geometry must be positive")
    if delta_vapor_mm <= 0 or delta_heat_mm <= 0:
        raise ValueError("effective exchange distances must be positive")
    if u_body_W_m2K <= 0:
        raise ValueError("u_body must be positive")
    if nx < 5:
        raise ValueError("nx must be at least 5")

    width = width_mm * 1e-3
    depth = depth_mm * 1e-3
    length = length_mm * 1e-3
    velocity = velocity_mm_s * 1e-3
    area = width * depth
    dh = hydraulic_diameter(width, depth)
    p_wet = width
    p_open = width

    k_m_wall = SH_SCREEN * D_V / dh
    h_wall = NU_SCREEN * K_AIR / dh
    k_m_lateral = D_V / (delta_vapor_mm * 1e-3)
    h_lateral = K_AIR / (delta_heat_mm * 1e-3)

    c_inf = vapor_density(ambient_c, ambient_rh)
    rho_inf = moist_air_density(ambient_c, c_inf)

    surface = np.full(nx, skin_c - 0.5)
    air_temp = np.full(nx, ambient_c)
    vapor = np.full(nx, c_inf)
    relax = 0.45
    error = np.inf

    for iteration in range(max_iterations):
        air_new = _solve_linear_field(
            source_target=surface,
            source_conductance_per_length=h_wall * p_wet,
            ambient_conductance_per_length=h_lateral * p_open,
            ambient_value=ambient_c,
            axial_diffusive_conductance=K_AIR * area,
            axial_advective_conductance=rho_inf * CP_AIR * velocity * area,
            length_m=length,
            nx=nx,
        )

        vapor_new = _solve_linear_field(
            source_target=saturated_vapor_density(surface),
            source_conductance_per_length=k_m_wall * p_wet,
            ambient_conductance_per_length=k_m_lateral * p_open,
            ambient_value=c_inf,
            axial_diffusive_conductance=D_V * area,
            axial_advective_conductance=velocity * area,
            length_m=length,
            nx=nx,
        )

        surface_new = surface.copy()
        for _ in range(20):
            evap_flux = k_m_wall * (saturated_vapor_density(surface_new) - vapor_new)
            residual = (
                u_body_W_m2K * (skin_c - surface_new)
                + h_wall * (air_new - surface_new)
                - L_V * evap_flux
            )
            derivative = (
                -u_body_W_m2K
                - h_wall
                - L_V * k_m_wall * saturated_vapor_density_derivative(surface_new)
            )
            step = residual / derivative
            surface_new = np.clip(surface_new - step, 5.0, 55.0)
            if np.max(np.abs(step)) < 1e-9:
                break

        error = max(
            float(np.max(np.abs(air_new - air_temp))),
            float(np.max(np.abs(vapor_new - vapor))) * 1e4,
            float(np.max(np.abs(surface_new - surface))),
        )
        air_temp = (1.0 - relax) * air_temp + relax * air_new
        vapor = (1.0 - relax) * vapor + relax * vapor_new
        surface = (1.0 - relax) * surface + relax * surface_new

        if error < tolerance:
            break

    evap_flux = k_m_wall * (saturated_vapor_density(surface) - vapor)
    body_flux = u_body_W_m2K * (skin_c - surface)
    air_to_wall = h_wall * (air_temp - surface)
    local_rh = vapor / saturated_vapor_density(air_temp)

    return OpenValleyThermalResult(
        ambient_C=ambient_c,
        ambient_RH=ambient_rh,
        skin_C=skin_c,
        width_mm=width_mm,
        depth_mm=depth_mm,
        length_mm=length_mm,
        velocity_mm_s=velocity_mm_s,
        delta_vapor_mm=delta_vapor_mm,
        delta_heat_mm=delta_heat_mm,
        converged=bool(error < tolerance),
        iterations=iteration + 1,
        mean_surface_C=float(np.mean(surface)),
        center_surface_C=float(surface[nx // 2]),
        mean_air_C=float(np.mean(air_temp)),
        mean_air_RH=float(np.mean(local_rh)),
        mean_evap_flux_g_m2_h=float(np.mean(evap_flux) * 3.6e6),
        mean_body_heat_flux_W_m2=float(np.mean(body_flux)),
        center_body_heat_flux_W_m2=float(body_flux[nx // 2]),
        mean_air_to_wall_W_m2=float(np.mean(air_to_wall)),
        condensation_fraction=float(np.mean(evap_flux < 0.0)),
        k_m_wall_m_s=k_m_wall,
        k_m_lateral_m_s=k_m_lateral,
        h_wall_W_m2K=h_wall,
        h_lateral_W_m2K=h_lateral,
    )


def run_screen() -> pd.DataFrame:
    rows = []
    exchange_pairs = (
        (0.10, 0.10),
        (0.50, 0.50),
        (1.00, 1.00),
        (0.10, 0.50),
        (0.10, 1.00),
        (0.50, 1.00),
    )
    environments = (
        (35.0, 0.50),
        (35.0, 0.70),
        (35.0, 0.85),
        (40.0, 0.70),
    )
    for delta_vapor, delta_heat in exchange_pairs:
        for ambient_c, ambient_rh in environments:
            result = solve_open_valley_thermal(
                ambient_c=ambient_c,
                ambient_rh=ambient_rh,
                delta_vapor_mm=delta_vapor,
                delta_heat_mm=delta_heat,
            )
            rows.append({"classification": "SIMULATION/SCREEN", **result.__dict__})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(run_screen().to_string(index=False))
