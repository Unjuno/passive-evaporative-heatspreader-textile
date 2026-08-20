"""Pressure-weighted liquid-route cost and protected escape-trunk screen.

Virtual/computational screen only. Local garment pressure is mapped to an
assumed equivalent hydraulic-radius retention, then a grid shortest-path cost
uses the circular-channel r^-4 resistance scaling. The pressure-to-radius law
is hypothetical and swept through a severity coefficient.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra

from simulations.spatial_pressure_layout import (
    WET_FRACTION,
    _exact_coverage,
    _gaussian,
    _geometry,
    build_pressure_maps,
    build_route_mask,
    build_wet_layouts,
)
from simulations.terminal_route_coddesign import regularized_wet_mask


def _graph(resistance_multiplier, domain_mm=60.0):
    resistance_multiplier = np.asarray(resistance_multiplier, dtype=float)
    n = resistance_multiplier.shape[0]
    dx = domain_mm / n
    rows, cols, data = [], [], []
    def idx(j, i): return j*n + i
    for j in range(n):
        for i in range(n):
            a = idx(j, i)
            for dj, di in ((1,0),(-1,0),(0,1),(0,-1)):
                jj, ii = j+dj, i+di
                if 0 <= jj < n and 0 <= ii < n:
                    b = idx(jj, ii)
                    cost = dx * 0.5 * (
                        resistance_multiplier[j,i] + resistance_multiplier[jj,ii]
                    )
                    rows.append(a); cols.append(b); data.append(cost)
    return coo_matrix((data,(rows,cols)), shape=(n*n,n*n)).tocsr()


def shortest_weighted_distance_to_wet(wet, resistance_multiplier, domain_mm=60.0):
    wet = np.asarray(wet, dtype=bool)
    graph = _graph(resistance_multiplier, domain_mm)
    wet_indices = np.flatnonzero(wet.ravel())
    distances = dijkstra(graph, directed=False, indices=wet_indices)
    return np.min(distances, axis=0).reshape(wet.shape)


def resistance_field(pressure, collapse_severity=0.5, cmax=0.5,
                     minimum_radius_retention=0.35,
                     protected_radius_floor=None):
    compression = np.clip(cmax * np.asarray(pressure, dtype=float), 0, 0.95)
    retention = np.clip(1.0 - float(collapse_severity)*compression,
                        minimum_radius_retention, 1.0)
    if protected_radius_floor is not None:
        retention = np.maximum(retention, float(protected_radius_floor))
    return retention**-4


def evaluate_layouts(n=12, collapse_severity=0.5, protected_radius_floor=None):
    pressure = build_pressure_maps(n)["backpack_plus_straps"]
    route = build_route_mask(n)
    layouts = build_wet_layouts(n, pressure, route)
    layouts = {
        "four_islands": layouts["four_islands"],
        "pressure_focused": _exact_coverage((1-pressure)+0.20*route.astype(float), WET_FRACTION),
        "regularized": regularized_wet_mask(pressure, route, 0.125, 0.35),
    }
    resistance = resistance_field(
        pressure,
        collapse_severity=collapse_severity,
        protected_radius_floor=protected_radius_floor,
    )
    rows = []
    for name, wet in layouts.items():
        distance = shortest_weighted_distance_to_wet(wet, resistance)
        rows.append({
            "layout": name,
            "collapse_severity": collapse_severity,
            "protected_radius_floor": protected_radius_floor,
            "mean_path_cost_mm_equivalent": float(distance.mean()),
            "p95_path_cost_mm_equivalent": float(np.quantile(distance, 0.95)),
            "max_path_cost_mm_equivalent": float(distance.max()),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    frames = []
    for severity in (0.25, 0.50, 0.75):
        for floor in (None, 0.90, 1.00):
            frames.append(evaluate_layouts(24, severity, floor))
    print(pd.concat(frames, ignore_index=True).to_csv(index=False))
