"""Explicit distributed liquid-resistor network for pressure-aware terminals.

Virtual/computational screen only. This model replaces a route-distance-only
hydraulic proxy with a 2-D resistor network carrying distributed source flow to
multiple zero-pressure wet-terminal nodes. It is still an idealized network:
all grid edges are available trunks, channels are circular-equivalent, and
capillary drive is represented by a collector pressure margin.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

from simulations.spatial_pressure_layout import (
    WET_FRACTION,
    _exact_coverage,
    build_pressure_maps,
    build_route_mask,
)
from simulations.terminal_route_coddesign import four_island_template, regularized_wet_mask

MU = 0.9e-3
GAMMA = 0.070
RHO = 1000.0
GRAVITY = 9.80665
CONTACT_ANGLE_DEG = 30.0
GARMENT_ACTIVE_AREA_M2 = 0.30
GARMENT_FEED_G_H = 150.0
DEFAULT_DOMAIN_M = 0.060
DEFAULT_TRUNK_RADIUS_UM = 200.0
DEFAULT_COLLECTOR_RADIUS_UM = 50.0
DEFAULT_LIFT_MM = 15.0
DEFAULT_MIN_RADIUS_RETENTION = 0.70


def collector_capillary_drive_pa(
    collector_radius_um: float = DEFAULT_COLLECTOR_RADIUS_UM,
    lift_mm: float = DEFAULT_LIFT_MM,
) -> float:
    radius = float(collector_radius_um) * 1e-6
    theta = np.deg2rad(CONTACT_ANGLE_DEG)
    capillary = 2.0 * GAMMA * np.cos(theta) / radius
    hydrostatic = RHO * GRAVITY * float(lift_mm) * 1e-3
    return float(capillary - hydrostatic)


def terminal_masks(n: int = 12) -> dict[str, np.ndarray]:
    pressure = build_pressure_maps(n)["backpack_plus_straps"]
    route = build_route_mask(n)
    four = four_island_template(n)
    thermal_only = _exact_coverage((1.0 - pressure) + 0.20 * route, WET_FRACTION)
    codesign = regularized_wet_mask(
        pressure,
        route,
        template_weight=0.125,
        route_weight=0.35,
    )
    four_islands = _exact_coverage(four, WET_FRACTION)
    return {
        "thermal_only": thermal_only,
        "regularized": codesign,
        "four_islands": four_islands,
    }


def _edge_conductance(radius_m: float, edge_length_m: float) -> float:
    return np.pi * radius_m**4 / (8.0 * MU * edge_length_m)


def solve_network(
    terminal_mask: np.ndarray,
    pressure: np.ndarray,
    trunk_radius_um: float = DEFAULT_TRUNK_RADIUS_UM,
    collapse_severity: float = 1.0,
    min_radius_retention: float = DEFAULT_MIN_RADIUS_RETENTION,
    domain_m: float = DEFAULT_DOMAIN_M,
    garment_feed_g_h: float = GARMENT_FEED_G_H,
    garment_active_area_m2: float = GARMENT_ACTIVE_AREA_M2,
) -> dict[str, float]:
    """Solve nodal pressures for distributed source injection to wet terminals."""
    terminal = np.asarray(terminal_mask, dtype=bool)
    pressure = np.asarray(pressure, dtype=float)
    if terminal.shape != pressure.shape or terminal.ndim != 2:
        raise ValueError("terminal_mask and pressure must be same-shape 2-D arrays")

    n_y, n_x = terminal.shape
    if n_y != n_x:
        raise ValueError("reference implementation expects a square grid")
    n = n_x
    dx = float(domain_m) / n

    compression = 0.5 * pressure
    retention = np.clip(
        1.0 - float(collapse_severity) * compression,
        float(min_radius_retention),
        1.0,
    )
    radius = float(trunk_radius_um) * 1e-6 * retention

    is_terminal = terminal.ravel()
    internal_ids = np.flatnonzero(~is_terminal)
    internal_map = {node: k for k, node in enumerate(internal_ids)}

    tile_area = float(domain_m) ** 2
    tile_feed_g_h = float(garment_feed_g_h) * tile_area / float(garment_active_area_m2)
    total_q_m3_s = (tile_feed_g_h / 1000.0 / 3600.0) / RHO
    source_q = total_q_m3_s / len(internal_ids)

    rows: list[int] = []
    cols: list[int] = []
    vals: list[float] = []
    rhs = np.full(len(internal_ids), source_q, dtype=float)

    def node(j: int, i: int) -> int:
        return j * n + i

    for j in range(n):
        for i in range(n):
            a = node(j, i)
            if is_terminal[a]:
                continue
            ia = internal_map[a]
            diagonal = 0.0
            for dj, di in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                jj, ii = j + dj, i + di
                if not (0 <= jj < n and 0 <= ii < n):
                    continue
                other = node(jj, ii)
                r1 = radius[j, i]
                r2 = radius[jj, ii]
                r4_eff = 2.0 * r1**4 * r2**4 / (r1**4 + r2**4 + 1e-60)
                conductance = _edge_conductance(r4_eff**0.25, dx)
                diagonal += conductance
                if not is_terminal[other]:
                    rows.append(ia)
                    cols.append(internal_map[other])
                    vals.append(-conductance)
            rows.append(ia)
            cols.append(ia)
            vals.append(diagonal)

    matrix = coo_matrix(
        (vals, (rows, cols)),
        shape=(len(internal_ids), len(internal_ids)),
    ).tocsc()
    p_internal = spsolve(matrix, rhs)
    p = np.zeros(n * n, dtype=float)
    p[internal_ids] = p_internal
    p_nonterminal = p[internal_ids]

    return {
        "tile_feed_g_h": tile_feed_g_h,
        "max_pressure_Pa": float(np.max(p_nonterminal)),
        "p95_pressure_Pa": float(np.quantile(p_nonterminal, 0.95)),
        "mean_pressure_Pa": float(np.mean(p_nonterminal)),
        "trunk_radius_um": float(trunk_radius_um),
        "collapse_severity": float(collapse_severity),
    }


def critical_radius_um(
    reference_pressure_pa: float,
    reference_radius_um: float = DEFAULT_TRUNK_RADIUS_UM,
    safety_factor: float = 3.0,
    capillary_drive_pa: float | None = None,
) -> float:
    """Radius where r^-4-scaled max pressure reaches the capillary safety limit."""
    drive = collector_capillary_drive_pa() if capillary_drive_pa is None else float(capillary_drive_pa)
    return float(
        float(reference_radius_um)
        * (float(safety_factor) * float(reference_pressure_pa) / drive) ** 0.25
    )


def reference_screen(n: int = 12) -> pd.DataFrame:
    pressure = build_pressure_maps(n)["backpack_plus_straps"]
    rows = []
    for severity in (0.0, 0.5, 1.0):
        for name, mask in terminal_masks(n).items():
            result = solve_network(mask, pressure, collapse_severity=severity)
            rows.append({"layout": name, **result})
    table = pd.DataFrame(rows)
    drive = collector_capillary_drive_pa()
    table["capillary_drive_Pa"] = drive
    table["margin_ratio"] = drive / table["max_pressure_Pa"]
    table["passes_SF3"] = table["margin_ratio"] >= 3.0
    return table


if __name__ == "__main__":
    print(reference_screen(n=24).to_csv(index=False))
