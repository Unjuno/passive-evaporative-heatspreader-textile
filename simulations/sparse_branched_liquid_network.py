"""Sparse two-scale liquid-network screen with trunk-grid phase sensitivity.

Virtual/computational model only. A coarse 200 um-class trunk lattice is embedded
in a finer collector mesh. Distributed or localized liquid sources drain to
wet-terminal nodes. The model screens when collector hydraulic radius and trunk
pitch become binding under pressure-linked radius collapse.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

from simulations.branched_liquid_resistor_network import (
    GAMMA,
    GRAVITY,
    MU,
    RHO,
    CONTACT_ANGLE_DEG,
    DEFAULT_DOMAIN_M,
    DEFAULT_LIFT_MM,
    DEFAULT_MIN_RADIUS_RETENTION,
    GARMENT_ACTIVE_AREA_M2,
    GARMENT_FEED_G_H,
    terminal_masks,
)
from simulations.spatial_pressure_layout import _gaussian, _geometry, build_pressure_maps

DEFAULT_TRUNK_RADIUS_UM = 200.0


def collector_drive_pa(collector_radius_um: float, lift_mm: float = DEFAULT_LIFT_MM) -> float:
    radius = float(collector_radius_um) * 1e-6
    theta = np.deg2rad(CONTACT_ANGLE_DEG)
    return float(
        2.0 * GAMMA * np.cos(theta) / radius
        - RHO * GRAVITY * float(lift_mm) * 1e-3
    )


def source_weights(n: int, kind: str, terminal: np.ndarray) -> np.ndarray:
    x, y = _geometry(n)
    if kind == "uniform":
        weights = np.ones((n, n), dtype=float)
    elif kind == "center_hotspot":
        weights = 0.15 + _gaussian(x, y, 0.50, 0.52, 0.16, 0.18)
    elif kind == "strap_hotspots":
        weights = (
            0.15
            + _gaussian(x, y, 0.30, 0.30, 0.08, 0.28)
            + _gaussian(x, y, 0.70, 0.30, 0.08, 0.28)
        )
    else:
        raise ValueError(f"unknown source kind: {kind}")
    weights = np.asarray(weights, dtype=float)
    weights[np.asarray(terminal, dtype=bool)] = 0.0
    total = float(weights.sum())
    if total <= 0.0:
        raise ValueError("source weights vanish outside terminal mask")
    return weights / total


def _is_trunk_edge(
    j: int,
    i: int,
    jj: int,
    ii: int,
    spacing_cells: int,
    offset_y: int,
    offset_x: int,
) -> bool:
    spacing = int(spacing_cells)
    if spacing <= 1:
        return True
    if j == jj:
        return ((j - int(offset_y)) % spacing) == 0
    return ((i - int(offset_x)) % spacing) == 0


def solve_sparse_network(
    terminal_mask: np.ndarray,
    pressure: np.ndarray,
    trunk_spacing_cells: int,
    collector_radius_um: float,
    trunk_radius_um: float = DEFAULT_TRUNK_RADIUS_UM,
    source_kind: str = "center_hotspot",
    offset_y: int = 0,
    offset_x: int = 0,
    collapse_severity: float = 1.0,
    min_radius_retention: float = DEFAULT_MIN_RADIUS_RETENTION,
    domain_m: float = DEFAULT_DOMAIN_M,
) -> dict[str, float]:
    terminal = np.asarray(terminal_mask, dtype=bool)
    pressure = np.asarray(pressure, dtype=float)
    if terminal.shape != pressure.shape or terminal.ndim != 2:
        raise ValueError("terminal and pressure must be same-shape 2-D arrays")
    n_y, n_x = terminal.shape
    if n_x != n_y:
        raise ValueError("reference implementation expects a square grid")
    n = n_x
    spacing = int(trunk_spacing_cells)
    if spacing < 1:
        raise ValueError("trunk_spacing_cells must be >= 1")

    dx = float(domain_m) / n
    compression = 0.5 * pressure
    retention = np.clip(
        1.0 - float(collapse_severity) * compression,
        float(min_radius_retention),
        1.0,
    )

    weights = source_weights(n, source_kind, terminal)
    is_terminal = terminal.ravel()
    internal_ids = np.flatnonzero(~is_terminal)
    internal_map = {node: k for k, node in enumerate(internal_ids)}

    tile_area = float(domain_m) ** 2
    tile_feed_g_h = GARMENT_FEED_G_H * tile_area / GARMENT_ACTIVE_AREA_M2
    total_q = (tile_feed_g_h / 1000.0 / 3600.0) / RHO
    rhs = weights.ravel()[internal_ids] * total_q

    rows: list[int] = []
    cols: list[int] = []
    vals: list[float] = []

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
                trunk = _is_trunk_edge(
                    j, i, jj, ii, spacing, offset_y, offset_x
                )
                base_radius_um = float(trunk_radius_um if trunk else collector_radius_um)
                r1 = base_radius_um * 1e-6 * retention[j, i]
                r2 = base_radius_um * 1e-6 * retention[jj, ii]
                r4_eff = 2.0 * r1**4 * r2**4 / (r1**4 + r2**4 + 1e-60)
                conductance = np.pi * r4_eff / (8.0 * MU * dx)
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
    p = spsolve(matrix, rhs)
    if not np.all(np.isfinite(p)):
        raise RuntimeError("sparse liquid network produced non-finite pressure")

    drive = collector_drive_pa(collector_radius_um)
    max_pressure = float(np.max(p))

    unique_edges = 2 * n * (n - 1)
    trunk_edges = 0
    for j in range(n):
        for i in range(n):
            for dj, di in ((1, 0), (0, 1)):
                jj, ii = j + dj, i + di
                if 0 <= jj < n and 0 <= ii < n:
                    trunk_edges += int(
                        _is_trunk_edge(
                            j, i, jj, ii, spacing, offset_y, offset_x
                        )
                    )

    return {
        "tile_feed_g_h": tile_feed_g_h,
        "collector_radius_um": float(collector_radius_um),
        "trunk_radius_um": float(trunk_radius_um),
        "trunk_spacing_cells": spacing,
        "trunk_pitch_mm": spacing * dx * 1000.0,
        "trunk_edge_fraction": trunk_edges / unique_edges,
        "max_pressure_Pa": max_pressure,
        "p95_pressure_Pa": float(np.quantile(p, 0.95)),
        "collector_drive_Pa": drive,
        "margin_ratio": drive / max_pressure,
        "passes_SF3": bool(drive / max_pressure >= 3.0),
    }


def sampled_offset_robust_screen(
    n: int = 12,
    collector_radii_um=(20.0, 25.0, 30.0, 35.0, 40.0, 50.0),
    spacings_cells=(2, 3, 4, 6, 12),
) -> pd.DataFrame:
    pressure = build_pressure_maps(n)["backpack_plus_straps"]
    terminal = terminal_masks(n)["thermal_only"]
    rows = []
    for radius in collector_radii_um:
        for spacing in spacings_cells:
            offsets = {
                (0, 0),
                (spacing // 2, 0),
                (0, spacing // 2),
                (spacing // 2, spacing // 2),
                (1 % spacing, 1 % spacing),
            }
            results = [
                solve_sparse_network(
                    terminal,
                    pressure,
                    spacing,
                    radius,
                    source_kind="center_hotspot",
                    offset_y=oy,
                    offset_x=ox,
                )
                for oy, ox in offsets
            ]
            margins = np.array([r["margin_ratio"] for r in results])
            rows.append(
                {
                    "collector_radius_um": float(radius),
                    "trunk_spacing_cells": int(spacing),
                    "trunk_pitch_mm": results[0]["trunk_pitch_mm"],
                    "worst_margin_ratio": float(np.min(margins)),
                    "median_margin_ratio": float(np.median(margins)),
                    "best_margin_ratio": float(np.max(margins)),
                    "all_offsets_pass_SF3": bool(np.all(margins >= 3.0)),
                }
            )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(sampled_offset_robust_screen(n=24).to_csv(index=False))
