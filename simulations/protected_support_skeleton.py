"""Support-area penalty screen for protected under-load evaporators.

A protected air gap requires load-bearing ribs/spacers. Those supports preserve
ambient access but consume active wet area. This module sweeps support fraction
and protected wet-side air-access floor under the synthetic backpack+strap load.

Virtual/computational screen only.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from simulations.spatial_pressure_layout import (
    K_BACKGROUND_SHEET,
    K_HIGH_SHEET,
    WET_FRACTION,
    build_pressure_maps,
    build_route_mask,
    build_wet_layouts,
    PressureTile,
)
from simulations.protected_air_channel_tradeoff import _run_with_wet_air_floor


def _support_mask(footprint, fraction):
    n = footprint.shape[0]
    jj, ii = np.mgrid[0:n, 0:n]
    x = (ii + 0.5) / n
    y = (jj + 0.5) / n
    score = np.maximum(np.cos(2*np.pi*4*x)**12, np.cos(2*np.pi*4*y)**12)
    ids = np.flatnonzero(footprint.ravel())
    count = int(round(float(fraction) * len(ids)))
    support = np.zeros_like(footprint, dtype=bool)
    if count <= 0:
        return support
    vals = score.ravel()[ids]
    chosen = ids[np.argpartition(vals, -count)[-count:]]
    support.ravel()[chosen] = True
    return support


def run_support_frontier(n=12, air_floors=None, support_fractions=None):
    if air_floors is None:
        air_floors = np.array([0.80, 0.85, 0.90, 0.95, 1.00])
    if support_fractions is None:
        support_fractions = np.linspace(0.0, 0.30, 13)

    pressure = build_pressure_maps(n)["backpack_plus_straps"]
    route = build_route_mask(n)
    layouts = build_wet_layouts(n, pressure, route)
    center = layouts["center_panel"]
    aware = layouts["pressure_aware"]

    k_route = np.where(route, K_HIGH_SHEET, K_BACKGROUND_SHEET)
    routed = PressureTile(k_route, pressure, cmax=0.5, air_exponent=2.0)
    background = PressureTile(np.full((n, n), K_BACKGROUND_SHEET), pressure, cmax=0.5, air_exponent=2.0)
    aware_state = routed.run(aware)

    rows = []
    for air_floor in air_floors:
        for support_fraction in support_fractions:
            support = _support_mask(center, support_fraction)
            active_wet = center & ~support
            r = _run_with_wet_air_floor(routed, active_wet, air_floor)
            b = _run_with_wet_air_floor(background, active_wet, air_floor)
            rows.append({
                "protected_air_floor": float(air_floor),
                "support_fraction_of_center_footprint": float(support_fraction),
                "active_wet_fraction_of_center_footprint": float(active_wet.sum()/center.sum()),
                "body_W_m2": r["body_W_m2"],
                "body_vs_pressure_aware_W_m2": r["body_W_m2"] - aware_state["body_W_m2"],
                "heat_routing_gain_W": (r["body_W_m2"] - b["body_W_m2"]) * 0.195,
                "evap_capacity_g_m2_h": r["evap_capacity_g_m2_h"],
                "converged": r["converged"] and b["converged"] and aware_state["converged"],
            })
    return pd.DataFrame(rows)


def summarize_frontier(table):
    rows = []
    for air_floor, group in table.groupby("protected_air_floor"):
        passing = group[group["body_vs_pressure_aware_W_m2"] >= 0]
        rows.append({
            "protected_air_floor": air_floor,
            "max_support_fraction_matching_relocation": (
                float(passing["support_fraction_of_center_footprint"].max())
                if not passing.empty else np.nan
            ),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    table = run_support_frontier(n=24)
    print(summarize_frontier(table).to_csv(index=False))
