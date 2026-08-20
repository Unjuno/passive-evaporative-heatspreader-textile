"""Pressure-aware wet-terminal placement vs heat/liquid routing distance.

Virtual/computational screen only. The model reuses the static spatial-pressure
thermal screen, then adds geometry-only nearest-terminal distance metrics for
liquid collection and load-weighted heat routing. A regularized placement rule
trades pure pressure avoidance against distributed four-island coverage.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.ndimage import distance_transform_edt

from simulations.spatial_pressure_layout import (
    K_BACKGROUND_SHEET,
    K_HIGH_SHEET,
    WET_FRACTION,
    _exact_coverage,
    _gaussian,
    _geometry,
    build_pressure_maps,
    build_route_mask,
    PressureTile,
)


def four_island_template(n=12):
    x, y = _geometry(n)
    g = lambda cx, cy, sx, sy: _gaussian(x, y, cx, cy, sx, sy)
    score = np.maximum.reduce([
        g(.25,.25,.10,.10), g(.75,.25,.10,.10),
        g(.25,.75,.10,.10), g(.75,.75,.10,.10),
    ])
    return (score - score.min()) / (score.max() - score.min() + 1e-30)


def regularized_wet_mask(pressure, route_mask, template_weight=0.125,
                         route_weight=0.35):
    n = pressure.shape[0]
    template = four_island_template(n)
    score = (
        1.0 - np.asarray(pressure, dtype=float)
        + float(template_weight) * template
        + float(route_weight) * np.asarray(route_mask, dtype=float)
    )
    return _exact_coverage(score, WET_FRACTION)


def route_distance_metrics(wet, pressure, domain_mm=60.0):
    wet = np.asarray(wet, dtype=bool)
    pressure = np.asarray(pressure, dtype=float)
    cell_mm = float(domain_mm) / wet.shape[0]
    distance_mm = distance_transform_edt(~wet) * cell_mm
    weights = pressure * (~wet)
    if weights.sum() <= 1e-12:
        weights = np.ones_like(weights) * (~wet)
    heat_rms = np.sqrt(np.sum(weights * distance_mm**2) / (weights.sum() + 1e-30))
    return {
        "liquid_mean_mm": float(distance_mm.mean()),
        "liquid_p95_mm": float(np.quantile(distance_mm, 0.95)),
        "liquid_max_mm": float(distance_mm.max()),
        "load_weighted_heat_rms_mm": float(heat_rms),
    }


def evaluate_regularized_candidate(n=12, template_weight=0.125, route_weight=0.35):
    pressure = build_pressure_maps(n)["backpack_plus_straps"]
    route = build_route_mask(n)
    wet = regularized_wet_mask(pressure, route, template_weight, route_weight)
    k_route = np.where(route, K_HIGH_SHEET, K_BACKGROUND_SHEET)
    routed = PressureTile(k_route, pressure, cmax=0.5, air_exponent=2.0)
    background = PressureTile(np.full((n,n), K_BACKGROUND_SHEET), pressure, cmax=0.5, air_exponent=2.0)
    r = routed.run(wet)
    b = background.run(wet)
    return {
        "template_weight": template_weight,
        "route_weight": route_weight,
        "body_W_m2": r["body_W_m2"],
        "heat_routing_gain_W": (r["body_W_m2"] - b["body_W_m2"]) * 0.195,
        "evap_capacity_g_m2_h": r["evap_capacity_g_m2_h"],
        "mean_pressure_on_wet": float(np.mean(pressure[wet])),
        **route_distance_metrics(wet, pressure),
        "converged": r["converged"] and b["converged"],
    }


def sweep_regularization(n=12, template_weights=None, route_weights=None):
    if template_weights is None:
        template_weights = np.linspace(0.0, 2.0, 17)
    if route_weights is None:
        route_weights = np.array([0.0, 0.10, 0.20, 0.35])
    rows = []
    for beta in template_weights:
        for route_weight in route_weights:
            rows.append(evaluate_regularized_candidate(n, beta, route_weight))
    table = pd.DataFrame(rows)
    pareto = []
    for _, row in table.iterrows():
        dominated = (
            (table["body_W_m2"] >= row["body_W_m2"])
            & (table["liquid_p95_mm"] <= row["liquid_p95_mm"])
            & (table["load_weighted_heat_rms_mm"] <= row["load_weighted_heat_rms_mm"])
            & (
                (table["body_W_m2"] > row["body_W_m2"])
                | (table["liquid_p95_mm"] < row["liquid_p95_mm"])
                | (table["load_weighted_heat_rms_mm"] < row["load_weighted_heat_rms_mm"])
            )
        ).any()
        pareto.append(not dominated)
    table["pareto"] = pareto
    return table


if __name__ == "__main__":
    print(sweep_regularization(n=24).to_csv(index=False))
