"""Two-temperature wet/dry patch screen for feed-limited operation.

Purpose
-------
Test the strongest assumption in the homogenized ``beta`` model: that wet and
dry sub-grid patches are nearly isothermal because of lateral heat spreading.

This model assigns separate temperatures to a wet patch and a dry patch and
couples them through a lateral mixing conductance ``g_mix``.  The total liquid
feed is fixed.  The model uses one effective series sensible coefficient and
one effective series vapor coefficient for both patches.

Important result of this deliberately symmetric model:

- ``g_mix`` changes wet/dry temperature split and the wet fraction required to
  evaporate a fixed feed;
- but when body-side and ambient sensible coefficients are identical on wet and
  dry patches, total body heat flux is nearly invariant to ``g_mix`` because
  internal lateral heat transfer cancels from the global energy balance.

Therefore heat spreading changes total cooling only when there is spatial
heterogeneity in evaporation, body coupling, ambient exposure, dry shielding,
or other boundary conditions.  This is consistent with the separate 2-D heat
spreader screens and is not evidence that heat spreading is generally useless.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.optimize import root

try:
    from simulations.open_valley_thermal_1d import (
        D_V,
        K_AIR,
        L_V,
        NU_SCREEN,
        R_V,
        SH_SCREEN,
        hydraulic_diameter,
    )
    from simulations.passive_rib_screen import p_sat
except ModuleNotFoundError:
    from open_valley_thermal_1d import D_V, K_AIR, L_V, NU_SCREEN, R_V, SH_SCREEN, hydraulic_diameter
    from passive_rib_screen import p_sat

DEFAULT_U_BODY = 100.0
DEFAULT_SKIN_C = 34.0


@dataclass(frozen=True)
class WetDryTwoNodeResult:
    g_mix_W_m2K: float
    wet_fraction_beta: float
    wet_temp_C: float
    dry_temp_C: float
    wet_dry_deltaT_C: float
    evap_total_g_h: float
    body_heat_flux_W_m2: float
    ambient_heat_flux_W_m2: float
    latent_flux_W_m2: float
    body_fraction_of_latent: float
    energy_error_W_m2: float
    converged: bool


def saturated_vapor_density(temp_c: float) -> float:
    return float(p_sat(temp_c) / (R_V * (temp_c + 273.15)))


def solve_two_node(
    g_mix_W_m2K: float,
    feed_total_g_h: float = 150.0,
    wet_panel_area_m2: float = 0.30 * 0.65,
    ambient_c: float = 35.0,
    ambient_rh: float = 0.50,
    skin_c: float = DEFAULT_SKIN_C,
    u_body_W_m2K: float = DEFAULT_U_BODY,
    width_mm: float = 6.0,
    depth_mm: float = 3.0,
    delta_vapor_mm: float = 0.5,
    delta_heat_mm: float = 0.5,
) -> WetDryTwoNodeResult:
    """Solve wet temperature, dry temperature, and wet fraction at fixed feed."""
    if g_mix_W_m2K < 0.0:
        raise ValueError("g_mix must be nonnegative")
    if feed_total_g_h <= 0.0 or wet_panel_area_m2 <= 0.0:
        raise ValueError("feed and area must be positive")

    width = width_mm * 1e-3
    depth = depth_mm * 1e-3
    dh = hydraulic_diameter(width, depth)

    h_wall = NU_SCREEN * K_AIR / dh
    h_lateral = K_AIR / (delta_heat_mm * 1e-3)
    h_eff = h_wall * h_lateral / (h_wall + h_lateral)

    km_wall = SH_SCREEN * D_V / dh
    km_lateral = D_V / (delta_vapor_mm * 1e-3)
    km_eff = km_wall * km_lateral / (km_wall + km_lateral)

    c_inf = ambient_rh * saturated_vapor_density(ambient_c)
    feed_flux = (feed_total_g_h / 1000.0 / 3600.0) / wet_panel_area_m2

    def equations(x: np.ndarray) -> np.ndarray:
        wet_c, dry_c, logit_beta = x
        beta = 1.0 / (1.0 + np.exp(-logit_beta))
        evap_wet = km_eff * max(saturated_vapor_density(wet_c) - c_inf, 0.0)
        q_mix_total = g_mix_W_m2K * (dry_c - wet_c)

        wet_balance = (
            u_body_W_m2K * (skin_c - wet_c)
            + h_eff * (ambient_c - wet_c)
            + q_mix_total / max(beta, 1e-9)
            - L_V * evap_wet
        )
        dry_balance = (
            u_body_W_m2K * (skin_c - dry_c)
            + h_eff * (ambient_c - dry_c)
            - q_mix_total / max(1.0 - beta, 1e-9)
        )
        water_balance_W_m2 = L_V * (beta * evap_wet - feed_flux)
        return np.array((wet_balance, dry_balance, water_balance_W_m2))

    solution = root(equations, np.array((29.5, 34.0, 0.0)))
    wet_c, dry_c, logit_beta = solution.x
    beta = float(1.0 / (1.0 + np.exp(-logit_beta)))
    evap_wet = km_eff * max(saturated_vapor_density(float(wet_c)) - c_inf, 0.0)

    body_flux = (
        beta * u_body_W_m2K * (skin_c - wet_c)
        + (1.0 - beta) * u_body_W_m2K * (skin_c - dry_c)
    )
    ambient_flux = (
        beta * h_eff * (ambient_c - wet_c)
        + (1.0 - beta) * h_eff * (ambient_c - dry_c)
    )
    latent_flux = beta * L_V * evap_wet
    evap_total_g_h = beta * evap_wet * wet_panel_area_m2 * 3.6e6

    return WetDryTwoNodeResult(
        g_mix_W_m2K=g_mix_W_m2K,
        wet_fraction_beta=beta,
        wet_temp_C=float(wet_c),
        dry_temp_C=float(dry_c),
        wet_dry_deltaT_C=float(dry_c - wet_c),
        evap_total_g_h=float(evap_total_g_h),
        body_heat_flux_W_m2=float(body_flux),
        ambient_heat_flux_W_m2=float(ambient_flux),
        latent_flux_W_m2=float(latent_flux),
        body_fraction_of_latent=float(body_flux / latent_flux),
        energy_error_W_m2=float(body_flux + ambient_flux - latent_flux),
        converged=bool(solution.success),
    )


def run_screen() -> pd.DataFrame:
    rows = []
    for g_mix in (0.0, 1.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, 1000.0, 5000.0):
        result = solve_two_node(g_mix)
        rows.append({"classification": "SIMULATION/TWO_NODE_WET_DRY", **result.__dict__})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(run_screen().to_string(index=False))