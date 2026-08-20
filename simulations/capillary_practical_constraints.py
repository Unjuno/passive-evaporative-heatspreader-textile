"""Practical-radius, hierarchical liquid-network and blockage screens.

Virtual/computational mechanism screen only. Extends the ideal capillary model
with maximum equivalent trunk radius, a short micro-wick + larger trunk split,
and installed-channel redundancy for partial blockage.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from simulations.capillary_liquid_network import (
    required_parallel_channels,
    liquid_inventory_ml,
)


def channel_cross_section_mm2(n_channels: float, radius_um: float) -> float:
    if not np.isfinite(n_channels):
        return np.inf
    radius_mm = float(radius_um) * 1e-3
    return float(n_channels) * np.pi * radius_mm**2


def best_under_radius_cap(flow_g_h: float, path_mm: float, rise_mm: float,
                          radius_cap_um: float, points: int = 1600):
    radii = np.geomspace(5.0, float(radius_cap_um), points)
    best = None
    for radius in radii:
        n = required_parallel_channels(flow_g_h, path_mm, radius, rise_mm)
        if not np.isfinite(n):
            continue
        area = channel_cross_section_mm2(n, radius)
        candidate = (area, radius, n, liquid_inventory_ml(path_mm, radius, n))
        if best is None or candidate[0] < best[0]:
            best = candidate
    if best is None:
        return {
            "selected_radius_um": np.nan,
            "channels": np.inf,
            "cross_section_mm2": np.inf,
            "inventory_ml": np.inf,
        }
    return {
        "selected_radius_um": best[1],
        "channels": best[2],
        "cross_section_mm2": best[0],
        "inventory_ml": best[3],
    }


def radius_cap_screen():
    architectures = [
        ("4_local_cell", 37.5, 50.0, 25.0),
        ("8_local_cell", 18.75, 30.0, 15.0),
        ("12_local_cell", 12.5, 25.0, 10.0),
        ("central", 150.0, 200.0, 100.0),
    ]
    rows = []
    for name, flow, path, rise in architectures:
        unconstrained = best_under_radius_cap(flow, path, rise, 600.0)
        for cap in (75.0, 100.0, 150.0, 200.0, 300.0, 600.0):
            result = best_under_radius_cap(flow, path, rise, cap)
            rows.append({
                "architecture": name,
                "flow_per_cell_g_h": flow,
                "path_mm": path,
                "rise_mm": rise,
                "radius_cap_um": cap,
                "selected_radius_um": result["selected_radius_um"],
                "channels_per_cell": result["channels"],
                "cross_section_per_cell_mm2": result["cross_section_mm2"],
                "area_penalty_vs_unconstrained": result["cross_section_mm2"] / unconstrained["cross_section_mm2"],
                "inventory_per_cell_ml": result["inventory_ml"],
            })
    return pd.DataFrame(rows)


def hierarchical_network_screen():
    rows = []
    for cells in (4, 8, 12):
        flow = 150.0 / cells
        if cells == 4:
            trunk_path, trunk_rise = 50.0, 25.0
        elif cells == 8:
            trunk_path, trunk_rise = 30.0, 15.0
        else:
            trunk_path, trunk_rise = 25.0, 10.0
        for micro_radius in (20.0, 30.0, 50.0):
            for micro_length in (2.0, 5.0, 10.0):
                micro_n = required_parallel_channels(flow, micro_length, micro_radius, 0.0)
                micro_area = channel_cross_section_mm2(micro_n, micro_radius)
                micro_inventory = liquid_inventory_ml(micro_length, micro_radius, micro_n)
                for trunk_radius in (100.0, 150.0, 200.0, 250.0, 300.0):
                    trunk_n = required_parallel_channels(flow, trunk_path, trunk_radius, trunk_rise)
                    if not np.isfinite(trunk_n):
                        continue
                    trunk_area = channel_cross_section_mm2(trunk_n, trunk_radius)
                    trunk_inventory = liquid_inventory_ml(trunk_path, trunk_radius, trunk_n)
                    rows.append({
                        "cells": cells,
                        "flow_per_cell_g_h": flow,
                        "micro_radius_um": micro_radius,
                        "micro_length_mm": micro_length,
                        "micro_channels_per_cell": micro_n,
                        "micro_area_per_cell_mm2": micro_area,
                        "trunk_radius_um": trunk_radius,
                        "trunk_length_mm": trunk_path,
                        "trunk_rise_mm": trunk_rise,
                        "trunk_channels_per_cell": trunk_n,
                        "trunk_area_per_cell_mm2": trunk_area,
                        "total_cross_section_proxy_mm2": cells * (micro_area + trunk_area),
                        "total_liquid_inventory_ml": cells * (micro_inventory + trunk_inventory),
                    })
    return pd.DataFrame(rows)


def installed_channels_for_blockage(live_channels_required: float, blocked_fraction: float) -> float:
    if blocked_fraction >= 1.0:
        return np.inf
    return float(np.ceil(float(live_channels_required) / (1.0 - float(blocked_fraction))))


if __name__ == "__main__":
    print(radius_cap_screen().to_csv(index=False))
