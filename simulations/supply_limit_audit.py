"""Liquid-supply audit for transfer-capacity model outputs.

This module deliberately does **not** invent the spatial drying pattern that
would occur when a fully-wet transfer-capacity solution demands more water than
is supplied.

Instead it separates:

- fully-wet evaporation capacity from `open_valley_thermal_1d.py`;
- available liquid feed;
- the upper bound on achievable evaporation = min(capacity, feed).

When capacity exceeds feed, the fully-wet surface temperature and body-side heat
flux from the capacity solver must not be reported as a feed-limited physical
prediction. A later wetting/dryout model is required for that state.
"""

from __future__ import annotations

import pandas as pd

try:
    from simulations.open_valley_thermal_1d import run_screen as run_thermal_screen
except ModuleNotFoundError:  # direct execution
    from open_valley_thermal_1d import run_screen as run_thermal_screen


DEFAULT_PROJECTED_AREA_M2 = 0.30
DEFAULT_WET_FRACTION = 0.65


def audit_capacity(
    capacity_flux_g_m2_h: float,
    feed_g_h: float,
    wet_area_m2: float,
) -> dict[str, float | bool | str]:
    if capacity_flux_g_m2_h < 0.0:
        raise ValueError("capacity flux must be nonnegative for supply audit")
    if feed_g_h <= 0.0 or wet_area_m2 <= 0.0:
        raise ValueError("feed and wet area must be positive")

    capacity_g_h = capacity_flux_g_m2_h * wet_area_m2
    ratio = capacity_g_h / feed_g_h
    supply_limited = capacity_g_h > feed_g_h

    return {
        "wet_area_m2": wet_area_m2,
        "feed_g_h": feed_g_h,
        "evap_capacity_g_h": capacity_g_h,
        "capacity_to_feed_ratio": ratio,
        "supply_limited": supply_limited,
        "achievable_evap_upper_bound_g_h": min(capacity_g_h, feed_g_h),
        "thermal_capacity_state_valid_at_fixed_feed": not supply_limited,
        "interpretation": (
            "SUPPLY-LIMITED: evaporation upper bound may be capped by feed, but "
            "capacity-model surface temperature/body heat flux are not a dryout solution"
            if supply_limited
            else "TRANSFER-LIMITED/BELOW-FEED-CAPACITY within this screening comparison"
        ),
    }


def run_screen(
    projected_area_m2: float = DEFAULT_PROJECTED_AREA_M2,
    wet_fraction: float = DEFAULT_WET_FRACTION,
) -> pd.DataFrame:
    if not 0.0 < wet_fraction <= 1.0:
        raise ValueError("wet_fraction must be in (0,1]")
    wet_area = projected_area_m2 * wet_fraction
    thermal = run_thermal_screen()
    rows = []

    for feed_g_h in (75.0, 150.0, 300.0):
        for _, source in thermal.iterrows():
            audited = audit_capacity(
                capacity_flux_g_m2_h=float(source["mean_evap_flux_g_m2_h"]),
                feed_g_h=feed_g_h,
                wet_area_m2=wet_area,
            )
            rows.append(
                {
                    "classification": "SIMULATION/CAPACITY_AUDIT",
                    "ambient_C": source["ambient_C"],
                    "ambient_RH": source["ambient_RH"],
                    "delta_vapor_mm": source["delta_vapor_mm"],
                    "delta_heat_mm": source["delta_heat_mm"],
                    "capacity_body_heat_flux_W_m2": source["mean_body_heat_flux_W_m2"],
                    **audited,
                }
            )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(run_screen().to_string(index=False))
