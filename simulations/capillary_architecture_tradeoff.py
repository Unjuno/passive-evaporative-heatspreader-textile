"""Analytic capillary-radius optimum and centralized-vs-local routing screen.

Virtual/computational screen only. Uses the ideal cylindrical-channel model in
`capillary_liquid_network.py` and minimizes total ideal channel cross-section.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from simulations.capillary_liquid_network import (
    CONTACT_ANGLE_DEG,
    DENSITY_KG_M3,
    G_M_S2,
    MU_PA_S,
    SURFACE_TENSION_N_M,
    DEFAULT_SAFETY_FACTOR,
    flow_m3_s_from_g_h,
    required_parallel_channels,
    liquid_inventory_ml,
)


def area_optimal_radius_um(vertical_rise_mm: float) -> float:
    """Continuous optimum radius for minimum total channel cross-sectional area.

    For positive vertical rise, with C=2*gamma*cos(theta) and H=rho*g*z,
    total area is proportional to 1/[r(C-Hr)]. The optimum is C/(2H).
    At zero rise this ideal objective decreases monotonically with radius, so
    no finite optimum exists without another physical constraint.
    """
    z = float(vertical_rise_mm) * 1e-3
    if z <= 0:
        return np.nan
    theta = np.deg2rad(CONTACT_ANGLE_DEG)
    return (
        SURFACE_TENSION_N_M * np.cos(theta)
        / (DENSITY_KG_M3 * G_M_S2 * z)
        * 1e6
    )


def minimum_continuous_cross_section_mm2(flow_g_h: float, path_mm: float,
                                         vertical_rise_mm: float,
                                         safety_factor: float = DEFAULT_SAFETY_FACTOR) -> float:
    """Analytic minimum ideal total capillary area for positive vertical rise."""
    z = float(vertical_rise_mm) * 1e-3
    if z <= 0:
        return np.nan
    q = flow_m3_s_from_g_h(flow_g_h)
    length = float(path_mm) * 1e-3
    theta = np.deg2rad(CONTACT_ANGLE_DEG)
    gamma_cos = SURFACE_TENSION_N_M * np.cos(theta)
    area_m2 = (
        8.0 * safety_factor * MU_PA_S * length * q
        * DENSITY_KG_M3 * G_M_S2 * z
        / gamma_cos**2
    )
    return area_m2 * 1e6


def scan_discrete_optimum(flow_g_h: float, path_mm: float, vertical_rise_mm: float,
                          radius_min_um: float = 5.0, radius_max_um: float = 600.0,
                          points: int = 1500):
    radii = np.geomspace(radius_min_um, radius_max_um, points)
    best = None
    for radius in radii:
        n = required_parallel_channels(flow_g_h, path_mm, radius, vertical_rise_mm)
        if not np.isfinite(n):
            continue
        r_m = radius * 1e-6
        area_mm2 = n * np.pi * r_m**2 * 1e6
        inventory = liquid_inventory_ml(path_mm, radius, n)
        candidate = (area_mm2, radius, n, inventory)
        if best is None or candidate[0] < best[0]:
            best = candidate
    if best is None:
        return {
            "best_radius_um": np.nan,
            "required_channels": np.inf,
            "total_cross_section_mm2": np.inf,
            "liquid_inventory_ml": np.inf,
        }
    return {
        "best_radius_um": best[1],
        "required_channels": best[2],
        "total_cross_section_mm2": best[0],
        "liquid_inventory_ml": best[3],
    }


def compare_architectures(architectures=None):
    if architectures is None:
        architectures = [
            ("central", 1, 150.0, 200.0, 100.0),
            ("4_local", 4, 37.5, 50.0, 25.0),
            ("8_local", 8, 18.75, 30.0, 15.0),
            ("12_local", 12, 12.5, 25.0, 10.0),
        ]
    rows = []
    for name, cells, flow_per_cell, path_mm, rise_mm in architectures:
        optimum = scan_discrete_optimum(flow_per_cell, path_mm, rise_mm)
        rows.append({
            "architecture": name,
            "cells": cells,
            "total_flow_g_h": cells * flow_per_cell,
            "flow_per_cell_g_h": flow_per_cell,
            "path_mm": path_mm,
            "vertical_rise_mm": rise_mm,
            "best_radius_um": optimum["best_radius_um"],
            "channels_per_cell": optimum["required_channels"],
            "total_channels": cells * optimum["required_channels"],
            "total_cross_section_mm2": cells * optimum["total_cross_section_mm2"],
            "total_liquid_inventory_ml": cells * optimum["liquid_inventory_ml"],
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(compare_architectures().to_csv(index=False))
