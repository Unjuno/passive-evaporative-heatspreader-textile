"""Explicit liquid-feed-limited open-valley screening model.

The fully-wet thermal solver reports a transfer capacity.  When that capacity
exceeds available liquid feed, this module solves a homogenized sub-grid wet
fraction ``beta`` so that predicted evaporation equals the imposed feed.

Interpretation
--------------
``beta`` is the fraction of the thermally connected floor that is effectively
wet at scales smaller than the 1-D axial model.  The entire floor remains
sensibly coupled to the body/heat spreader and valley air, while the vapor
source and latent sink are scaled by ``beta``.

This is appropriate only as a strong-heat-spreader / fine-scale partial-wetness
screen.  It does not resolve individual dry patches, advancing wetting fronts,
liquid redistribution transients, contact-angle hysteresis, or capillary
failure.  Those remain physical-test / higher-fidelity-model questions.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.optimize import brentq

try:
    from simulations.open_valley_thermal_1d import solve_open_valley_thermal
except ModuleNotFoundError:
    from open_valley_thermal_1d import solve_open_valley_thermal

DEFAULT_PROJECTED_AREA_M2 = 0.30
DEFAULT_STRUCTURED_FRACTION = 0.65


@dataclass(frozen=True)
class FeedLimitedResult:
    ambient_C: float
    ambient_RH: float
    feed_g_m2_h: float
    delta_vapor_mm: float
    delta_heat_mm: float
    regime: str
    wet_fraction_beta: float
    mean_evap_flux_g_m2_h: float
    mean_body_heat_flux_W_m2: float
    mean_surface_C: float
    mean_air_RH: float
    full_wet_capacity_g_m2_h: float
    feed_balance_error_percent: float
    thermal_solver_converged: bool


def solve_feed_limited(
    feed_g_m2_h: float,
    ambient_c: float,
    ambient_rh: float,
    width_mm: float = 6.0,
    depth_mm: float = 3.0,
    length_mm: float = 50.0,
    velocity_mm_s: float = 0.0,
    delta_vapor_mm: float = 0.5,
    delta_heat_mm: float = 0.5,
    u_body_W_m2K: float = 100.0,
    skin_c: float = 34.0,
    nx: int = 81,
) -> FeedLimitedResult:
    """Solve transfer-limited or homogenized partial-wetness operation."""
    if feed_g_m2_h <= 0.0:
        raise ValueError("feed_g_m2_h must be positive")

    def solve_beta(beta: float):
        return solve_open_valley_thermal(
            ambient_c=ambient_c,
            ambient_rh=ambient_rh,
            width_mm=width_mm,
            depth_mm=depth_mm,
            length_mm=length_mm,
            velocity_mm_s=velocity_mm_s,
            delta_vapor_mm=delta_vapor_mm,
            delta_heat_mm=delta_heat_mm,
            u_body_W_m2K=u_body_W_m2K,
            skin_c=skin_c,
            wet_fraction=beta,
            nx=nx,
        )

    full = solve_beta(1.0)
    capacity = full.mean_evap_flux_g_m2_h

    if capacity <= feed_g_m2_h:
        result = full
        beta = 1.0
        regime = "transfer-limited"
        target_evap = capacity
    else:
        def residual(beta: float) -> float:
            return solve_beta(beta).mean_evap_flux_g_m2_h - feed_g_m2_h

        beta = brentq(residual, 1e-8, 1.0, xtol=1e-8, maxiter=80)
        result = solve_beta(beta)
        regime = "supply-limited-partial-wetness"
        target_evap = feed_g_m2_h

    balance_error = 100.0 * (
        result.mean_evap_flux_g_m2_h - target_evap
    ) / max(target_evap, 1e-12)

    return FeedLimitedResult(
        ambient_C=ambient_c,
        ambient_RH=ambient_rh,
        feed_g_m2_h=feed_g_m2_h,
        delta_vapor_mm=delta_vapor_mm,
        delta_heat_mm=delta_heat_mm,
        regime=regime,
        wet_fraction_beta=beta,
        mean_evap_flux_g_m2_h=result.mean_evap_flux_g_m2_h,
        mean_body_heat_flux_W_m2=result.mean_body_heat_flux_W_m2,
        mean_surface_C=result.mean_surface_C,
        mean_air_RH=result.mean_air_RH,
        full_wet_capacity_g_m2_h=capacity,
        feed_balance_error_percent=balance_error,
        thermal_solver_converged=result.converged,
    )


def linked_exchange_optimization(
    feed_total_g_h: float = 150.0,
    projected_area_m2: float = DEFAULT_PROJECTED_AREA_M2,
    structured_fraction: float = DEFAULT_STRUCTURED_FRACTION,
) -> pd.DataFrame:
    """Sweep linked heat/vapor exchange at equal total liquid feed."""
    if projected_area_m2 <= 0.0:
        raise ValueError("projected_area_m2 must be positive")
    if not 0.0 < structured_fraction <= 1.0:
        raise ValueError("structured_fraction must be in (0,1]")
    wet_area = projected_area_m2 * structured_fraction
    feed_flux = feed_total_g_h / wet_area

    rows = []
    for ambient_rh in (0.50, 0.70, 0.85):
        for delta in np.geomspace(0.03, 10.0, 48):
            result = solve_feed_limited(
                feed_g_m2_h=feed_flux,
                ambient_c=35.0,
                ambient_rh=ambient_rh,
                delta_vapor_mm=float(delta),
                delta_heat_mm=float(delta),
                nx=61,
            )
            rows.append(
                {
                    "classification": "SIMULATION/FEED_LIMITED_SCREEN",
                    "feed_total_g_h": feed_total_g_h,
                    "projected_area_m2": projected_area_m2,
                    "structured_fraction": structured_fraction,
                    "wet_panel_area_m2": wet_area,
                    "linked_delta_mm": float(delta),
                    **result.__dict__,
                    "evap_total_g_h": result.mean_evap_flux_g_m2_h * wet_area,
                }
            )
    return pd.DataFrame(rows)


def summarize_optima(table: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for rh, group in table.groupby("ambient_RH"):
        best = group.loc[group["mean_body_heat_flux_W_m2"].idxmax()]
        rows.append(
            {
                "classification": "SIMULATION/FEED_LIMITED_OPTIMUM",
                "ambient_C": float(best["ambient_C"]),
                "ambient_RH": float(rh),
                "feed_total_g_h": float(best["feed_total_g_h"]),
                "best_linked_delta_mm": float(best["linked_delta_mm"]),
                "best_body_heat_flux_W_m2": float(best["mean_body_heat_flux_W_m2"]),
                "wet_fraction_beta_at_best": float(best["wet_fraction_beta"]),
                "evap_total_g_h_at_best": float(best["evap_total_g_h"]),
                "regime_at_best": str(best["regime"]),
            }
        )
    return pd.DataFrame(rows)


def run_screen() -> pd.DataFrame:
    rows = []
    wet_area = DEFAULT_PROJECTED_AREA_M2 * DEFAULT_STRUCTURED_FRACTION
    for feed_total in (75.0, 150.0, 300.0):
        feed_flux = feed_total / wet_area
        for ambient_c, ambient_rh in ((35.0, 0.50), (35.0, 0.70), (35.0, 0.85), (40.0, 0.70)):
            for delta in (0.10, 0.25, 0.50, 1.0, 2.0):
                result = solve_feed_limited(
                    feed_g_m2_h=feed_flux,
                    ambient_c=ambient_c,
                    ambient_rh=ambient_rh,
                    delta_vapor_mm=delta,
                    delta_heat_mm=delta,
                    nx=61,
                )
                rows.append(
                    {
                        "classification": "SIMULATION/FEED_LIMITED_SCREEN",
                        "feed_total_g_h": feed_total,
                        "wet_panel_area_m2": wet_area,
                        **result.__dict__,
                        "evap_total_g_h": result.mean_evap_flux_g_m2_h * wet_area,
                    }
                )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    screen = run_screen()
    print(screen.to_string(index=False))
    print("\nLinked-exchange optima at 150 g/h:")
    print(summarize_optima(linked_exchange_optimization()).to_string(index=False))