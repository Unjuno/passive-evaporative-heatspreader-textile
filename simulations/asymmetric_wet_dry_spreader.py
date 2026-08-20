"""Asymmetric wet/dry two-node screen for heat-spreader synergy.

The symmetric ``wet_dry_two_node.py`` model shows that internal heat spreading
does not change area-integrated body heat flux when wet and dry patches have
identical body and ambient sensible coefficients and total evaporation is fixed.

This module deliberately breaks that symmetry: the wet evaporator remains
exposed to a representative open-valley sensible coefficient, while the dry
patch can have a lower ambient sensible coefficient ``h_dry`` representing
insulation, shielding, reduced exposure, or another dry-side thermal barrier.

The lateral mixing conductance ``g_mix`` then routes heat from the dry patch
into the active wet evaporator. This is a low-order mechanism screen, not a
mapping from a textile conductivity to ``g_mix``.

The partial-wetness solve uses bounded least squares in ``(T_wet, T_dry, beta)``
rather than an unconstrained root in logit(beta). This avoids accepting
nonphysical branch jumps during dense ``g_mix`` sweeps. A solution is marked
converged only when the bounded optimizer succeeds and the original balance
residuals are small.

The deterministic screen is intentionally limited to feed values for which a
partial-wetness solution is well behaved. Transfer-limited/full-wet operation
belongs in ``open_valley_feed_limited.py`` rather than forcing ``beta -> 1`` in
this two-node mechanism model.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.optimize import least_squares

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
DEFAULT_AREA_M2 = 0.30 * 0.65
MAX_PARTIAL_WET_BETA = 0.979


@dataclass(frozen=True)
class AsymmetricWetDryResult:
    feed_total_g_h: float
    g_mix_W_m2K: float
    h_dry_W_m2K: float
    h_wet_W_m2K: float
    wet_fraction_beta: float
    wet_temp_C: float
    dry_temp_C: float
    wet_dry_deltaT_C: float
    lateral_heat_dry_to_wet_W_m2_total: float
    evap_total_g_h: float
    body_heat_flux_W_m2: float
    ambient_heat_flux_W_m2: float
    latent_flux_W_m2: float
    body_fraction_of_latent: float
    energy_error_W_m2: float
    max_equation_residual_W_m2: float
    converged: bool


def saturated_vapor_density(temp_c: float) -> float:
    return float(p_sat(temp_c) / (R_V * (temp_c + 273.15)))


def solve_asymmetric(
    g_mix_W_m2K: float,
    h_dry_W_m2K: float,
    feed_total_g_h: float = 150.0,
    wet_panel_area_m2: float = DEFAULT_AREA_M2,
    ambient_c: float = 35.0,
    ambient_rh: float = 0.50,
    skin_c: float = DEFAULT_SKIN_C,
    u_body_W_m2K: float = DEFAULT_U_BODY,
    width_mm: float = 6.0,
    depth_mm: float = 3.0,
    delta_vapor_mm: float = 0.5,
    delta_heat_wet_mm: float = 0.5,
    initial_state: tuple[float, float, float] | None = None,
) -> AsymmetricWetDryResult:
    """Solve a bounded partial-wetness asymmetric wet/dry state.

    ``initial_state`` may be supplied as ``(T_wet_C, T_dry_C, beta)`` for
    continuation sweeps. The returned ``converged`` flag requires both optimizer
    success and a small residual in the unscaled governing equations.
    """
    if g_mix_W_m2K < 0.0 or h_dry_W_m2K < 0.0:
        raise ValueError("conductances must be nonnegative")
    if feed_total_g_h <= 0.0 or wet_panel_area_m2 <= 0.0:
        raise ValueError("feed and area must be positive")

    width = width_mm * 1e-3
    depth = depth_mm * 1e-3
    dh = hydraulic_diameter(width, depth)

    h_wall = NU_SCREEN * K_AIR / dh
    h_lateral_wet = K_AIR / (delta_heat_wet_mm * 1e-3)
    h_wet = h_wall * h_lateral_wet / (h_wall + h_lateral_wet)

    km_wall = SH_SCREEN * D_V / dh
    km_lateral = D_V / (delta_vapor_mm * 1e-3)
    km_eff = km_wall * km_lateral / (km_wall + km_lateral)

    c_inf = ambient_rh * saturated_vapor_density(ambient_c)
    feed_flux = (feed_total_g_h / 1000.0 / 3600.0) / wet_panel_area_m2

    def raw_equations(x: np.ndarray) -> np.ndarray:
        wet_c, dry_c, beta = x
        evap_wet = km_eff * max(saturated_vapor_density(float(wet_c)) - c_inf, 0.0)
        q_mix_total = g_mix_W_m2K * (dry_c - wet_c)

        wet_balance = (
            u_body_W_m2K * (skin_c - wet_c)
            + h_wet * (ambient_c - wet_c)
            + q_mix_total / max(beta, 1e-9)
            - L_V * evap_wet
        )
        dry_balance = (
            u_body_W_m2K * (skin_c - dry_c)
            + h_dry_W_m2K * (ambient_c - dry_c)
            - q_mix_total / max(1.0 - beta, 1e-9)
        )
        water_balance_W_m2 = L_V * (beta * evap_wet - feed_flux)
        return np.array((wet_balance, dry_balance, water_balance_W_m2))

    if initial_state is None:
        beta_guess = min(max(feed_total_g_h / 180.0, 0.05), 0.90)
        x0 = np.array((30.0, 34.0, beta_guess))
    else:
        x0 = np.array(initial_state, dtype=float)
        x0[2] = np.clip(x0[2], 1e-4, MAX_PARTIAL_WET_BETA - 1e-4)

    solution = least_squares(
        lambda x: raw_equations(x) / 100.0,
        x0,
        bounds=(
            np.array((5.0, 5.0, 1e-6)),
            np.array((55.0, 55.0, MAX_PARTIAL_WET_BETA)),
        ),
        xtol=1e-12,
        ftol=1e-12,
        gtol=1e-12,
        max_nfev=5000,
    )

    wet_c, dry_c, beta = solution.x
    evap_wet = km_eff * max(saturated_vapor_density(float(wet_c)) - c_inf, 0.0)
    q_mix_total = g_mix_W_m2K * (dry_c - wet_c)

    body_flux = (
        beta * u_body_W_m2K * (skin_c - wet_c)
        + (1.0 - beta) * u_body_W_m2K * (skin_c - dry_c)
    )
    ambient_flux = (
        beta * h_wet * (ambient_c - wet_c)
        + (1.0 - beta) * h_dry_W_m2K * (ambient_c - dry_c)
    )
    latent_flux = beta * L_V * evap_wet
    evap_total_g_h = beta * evap_wet * wet_panel_area_m2 * 3.6e6
    max_residual = float(np.max(np.abs(raw_equations(solution.x))))

    return AsymmetricWetDryResult(
        feed_total_g_h=feed_total_g_h,
        g_mix_W_m2K=g_mix_W_m2K,
        h_dry_W_m2K=h_dry_W_m2K,
        h_wet_W_m2K=h_wet,
        wet_fraction_beta=float(beta),
        wet_temp_C=float(wet_c),
        dry_temp_C=float(dry_c),
        wet_dry_deltaT_C=float(dry_c - wet_c),
        lateral_heat_dry_to_wet_W_m2_total=float(q_mix_total),
        evap_total_g_h=float(evap_total_g_h),
        body_heat_flux_W_m2=float(body_flux),
        ambient_heat_flux_W_m2=float(ambient_flux),
        latent_flux_W_m2=float(latent_flux),
        body_fraction_of_latent=float(body_flux / latent_flux),
        energy_error_W_m2=float(body_flux + ambient_flux - latent_flux),
        max_equation_residual_W_m2=max_residual,
        converged=bool(solution.success and max_residual < 1e-5),
    )


def continuation_screen(
    feed_total_g_h: float,
    h_dry_W_m2K: float,
    g_mix_values: np.ndarray,
) -> pd.DataFrame:
    """Follow the bounded partial-wetness branch over increasing ``g_mix``."""
    rows = []
    state: tuple[float, float, float] | None = None
    for g_mix in np.asarray(g_mix_values, dtype=float):
        result = solve_asymmetric(
            float(g_mix),
            h_dry_W_m2K,
            feed_total_g_h=feed_total_g_h,
            initial_state=state,
        )
        if result.converged:
            state = (result.wet_temp_C, result.dry_temp_C, result.wet_fraction_beta)
        rows.append({"classification": "SIMULATION/ASYMMETRIC_CONTINUATION", **result.__dict__})
    return pd.DataFrame(rows)


def run_screen() -> pd.DataFrame:
    rows = []
    for feed in (30.0, 50.0, 75.0, 100.0, 150.0):
        for h_dry in (0.0, 5.0, 10.0, 20.0):
            table = continuation_screen(
                feed,
                h_dry,
                np.array((0.0, 10.0, 50.0, 100.0, 500.0, 5000.0)),
            )
            rows.extend(table.to_dict(orient="records"))
    return pd.DataFrame(rows)


def gain_summary(table: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (feed, h_dry), group in table.groupby(["feed_total_g_h", "h_dry_W_m2K"]):
        valid = group[group["converged"]].sort_values("g_mix_W_m2K")
        if valid.empty:
            continue
        no_mix = valid.iloc[0]
        high_mix = valid.iloc[-1]
        gain = high_mix["body_heat_flux_W_m2"] - no_mix["body_heat_flux_W_m2"]
        rows.append(
            {
                "classification": "SIMULATION/ASYMMETRIC_SPREADING_GAIN",
                "feed_total_g_h": float(feed),
                "h_dry_W_m2K": float(h_dry),
                "beta_no_mix": float(no_mix["wet_fraction_beta"]),
                "beta_high_mix": float(high_mix["wet_fraction_beta"]),
                "body_flux_no_mix_W_m2": float(no_mix["body_heat_flux_W_m2"]),
                "body_flux_high_mix_W_m2": float(high_mix["body_heat_flux_W_m2"]),
                "gain_high_mix_W_m2": float(gain),
                "gain_over_0p195m2_W": float(gain * DEFAULT_AREA_M2),
            }
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    screen = run_screen()
    print(screen.to_string(index=False))
    print("\nGain summary:")
    print(gain_summary(screen).to_string(index=False))
