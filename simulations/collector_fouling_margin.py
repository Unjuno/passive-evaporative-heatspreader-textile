"""Collector fouling / hydraulic-radius-loss failure screen.

Virtual/computational model only. Dissolved salt and other nonvolatile residues are
not allowed to evaporate. Instead this module treats an inward collector-radius
loss ``delta`` as a failure-state variable and re-solves the sparse branched liquid
network.

The module intentionally does not claim a deposition rate or chemistry. It asks a
narrow question: if collector hydraulic radius is lost, when does the sampled
capillary safety margin fall below 3?
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
from simulations.sparse_branched_liquid_network import (
    DEFAULT_TRUNK_RADIUS_UM,
    _is_trunk_edge,
    source_weights,
)
from simulations.spatial_pressure_layout import build_pressure_maps

SALT_VAPOR_FLUX = 0.0
DEFAULT_TRUNK_SPACING_CELLS = 24


def collector_drive_pa(radius_um: float, lift_mm: float = DEFAULT_LIFT_MM) -> float:
    radius = float(radius_um) * 1e-6
    theta = np.deg2rad(CONTACT_ANGLE_DEG)
    return float(
        2.0 * GAMMA * np.cos(theta) / radius
        - RHO * GRAVITY * float(lift_mm) * 1e-3
    )


def uniform_deposit_field(n: int, deposit_um: float) -> np.ndarray:
    return np.full((n, n), float(deposit_um), dtype=float)


def localized_deposit_field(
    n: int,
    mean_deposit_um: float,
    occupied_fraction: float = 0.20,
    seed: int = 0,
) -> np.ndarray:
    """Concentrate the same mean deposit into a subset of collector cells."""
    if not 0.0 < occupied_fraction <= 1.0:
        raise ValueError("occupied_fraction must be in (0, 1]")
    field = np.zeros((n, n), dtype=float)
    count = max(1, int(round(occupied_fraction * n * n)))
    rng = np.random.default_rng(20260820 + int(seed))
    chosen = rng.choice(n*n, count, replace=False)
    field.ravel()[chosen] = float(mean_deposit_um) / occupied_fraction
    return field


def solve_fouled_sparse_network(
    terminal_mask: np.ndarray,
    pressure: np.ndarray,
    collector_radius_um: float,
    deposit_um: np.ndarray,
    trunk_spacing_cells: int = DEFAULT_TRUNK_SPACING_CELLS,
    trunk_radius_um: float = DEFAULT_TRUNK_RADIUS_UM,
    source_kind: str = "center_hotspot",
    offset_y: int = 0,
    offset_x: int = 0,
    collapse_severity: float = 1.0,
    min_radius_retention: float = DEFAULT_MIN_RADIUS_RETENTION,
    domain_m: float = DEFAULT_DOMAIN_M,
    minimum_open_radius_um: float = 2.0,
    drive_radius_um: float | None = None,
) -> dict[str, float]:
    terminal = np.asarray(terminal_mask, dtype=bool)
    pressure = np.asarray(pressure, dtype=float)
    deposit = np.asarray(deposit_um, dtype=float)
    if terminal.shape != pressure.shape or deposit.shape != terminal.shape:
        raise ValueError("terminal, pressure and deposit arrays must have equal shape")
    if terminal.ndim != 2 or terminal.shape[0] != terminal.shape[1]:
        raise ValueError("reference implementation expects a square 2-D grid")

    n = terminal.shape[0]
    dx = float(domain_m) / n
    spacing = int(trunk_spacing_cells)
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
        return j*n+i

    for j in range(n):
        for i in range(n):
            a = node(j, i)
            if is_terminal[a]:
                continue
            ia = internal_map[a]
            diagonal = 0.0
            for dj, di in ((1,0),(-1,0),(0,1),(0,-1)):
                jj, ii = j+dj, i+di
                if not (0 <= jj < n and 0 <= ii < n):
                    continue
                other = node(jj, ii)
                trunk = _is_trunk_edge(
                    j, i, jj, ii, spacing, offset_y, offset_x
                )
                if trunk:
                    r1_um = float(trunk_radius_um) * retention[j, i]
                    r2_um = float(trunk_radius_um) * retention[jj, ii]
                else:
                    r1_um = max(
                        float(minimum_open_radius_um),
                        float(collector_radius_um) - deposit[j, i],
                    ) * retention[j, i]
                    r2_um = max(
                        float(minimum_open_radius_um),
                        float(collector_radius_um) - deposit[jj, ii],
                    ) * retention[jj, ii]
                r1 = r1_um * 1e-6
                r2 = r2_um * 1e-6
                r4_eff = 2.0*r1**4*r2**4/(r1**4+r2**4+1e-60)
                conductance = np.pi*r4_eff/(8.0*MU*dx)
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
        raise RuntimeError("fouled sparse network produced non-finite pressure")

    drive_r = float(collector_radius_um if drive_radius_um is None else drive_radius_um)
    drive = collector_drive_pa(drive_r)
    max_pressure = float(np.max(p))
    return {
        "tile_feed_g_h": tile_feed_g_h,
        "collector_radius_um": float(collector_radius_um),
        "drive_radius_um": drive_r,
        "max_pressure_Pa": max_pressure,
        "p95_pressure_Pa": float(np.quantile(p, 0.95)),
        "collector_drive_Pa": drive,
        "margin_ratio": drive/max_pressure,
        "passes_SF3": bool(drive/max_pressure >= 3.0),
        "salt_vapor_flux": SALT_VAPOR_FLUX,
    }


def uniform_fouling_thresholds(
    n: int = 24,
    collector_radii_um=(35.0, 40.0, 50.0),
    deposits_um=range(0, 26),
) -> pd.DataFrame:
    pressure = build_pressure_maps(n)["backpack_plus_straps"]
    terminal = terminal_masks(n)["thermal_only"]
    rows = []
    for radius in collector_radii_um:
        results = []
        for deposit in deposits_um:
            if deposit >= radius-2.0:
                continue
            field = uniform_deposit_field(n, float(deposit))
            margins = []
            spacing = DEFAULT_TRUNK_SPACING_CELLS if n == 24 else n
            offsets = {(0,0),(spacing//2,0),(0,spacing//2),(spacing//2,spacing//2),(1 % spacing,1 % spacing)}
            for oy, ox in offsets:
                result = solve_fouled_sparse_network(
                    terminal,
                    pressure,
                    radius,
                    field,
                    trunk_spacing_cells=spacing,
                    source_kind="center_hotspot",
                    offset_y=oy,
                    offset_x=ox,
                    drive_radius_um=max(2.0, radius-float(deposit)),
                )
                margins.append(result["margin_ratio"])
            worst = float(np.min(margins))
            results.append((float(deposit), worst, worst >= 3.0))
        passing = [r for r in results if r[2]]
        failing = [r for r in results if not r[2]]
        rows.append({
            "collector_radius_um": float(radius),
            "largest_tested_uniform_deposit_passing_um": max((r[0] for r in passing), default=np.nan),
            "first_tested_uniform_deposit_failing_um": min((r[0] for r in failing), default=np.nan),
            "initial_worst_margin": results[0][1],
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(uniform_fouling_thresholds().to_csv(index=False))
