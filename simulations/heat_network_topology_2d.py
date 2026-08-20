"""2-D heat-network topology, wet-pattern, and damage screening.

This model extends the equal-material sheet comparison in
``spreader_topology_2d.py`` from simple stripes/mesh to explicit garment-like
routing motifs:

- directed parallel routes;
- herringbone;
- radial spokes;
- leaf/venation routing;
- redundant mesh;
- directed/mesh blends.

The initial high-conductivity material fraction is held equal across binary
network designs.  Four wet evaporator islands are the nominal field, and
alternate wet patterns can be supplied to test whether a design is over-fit to
one sweat distribution.

Two damage classes are intentionally distinguished:

1. localized damage: remove a fixed fraction of high-k cells nearest a chosen
   tear center;
2. distributed dropout: remove a fixed fraction of high-k cells using a fixed
   random seed, representing dispersed microcrack/contact loss.

Outputs are low-order numerical screens, not measured garment performance.
No physical specimen exists.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import factorized

try:
    from simulations.distributed_spreader_1d import (
        H_WET,
        KM_WET,
        L_V,
        STRUCTURED_AREA_M2,
        T_SKIN,
        U_BODY,
        saturated_vapor_density,
        saturated_vapor_density_derivative,
    )
except ModuleNotFoundError:
    from distributed_spreader_1d import (
        H_WET,
        KM_WET,
        L_V,
        STRUCTURED_AREA_M2,
        T_SKIN,
        U_BODY,
        saturated_vapor_density,
        saturated_vapor_density_derivative,
    )

DEFAULT_DOMAIN_MM = 60.0
DEFAULT_MATERIAL_FRACTION = 0.35
DEFAULT_HIGH_SHEET_W_K = 300.0 * 100e-6
DEFAULT_BACKGROUND_SHEET_W_K = 0.2 * 500e-6
DEFAULT_H_CONTACT = 1500.0
DEFAULT_H_DRY = 5.0
DEFAULT_AMBIENT_C = 35.0
DEFAULT_AMBIENT_RH = 0.50


@dataclass(frozen=True)
class NetworkResult:
    topology: str
    material_fraction: float
    wet_fraction: float
    body_heat_flux_W_m2: float
    gain_vs_background_W: float
    temperature_std_C: float
    temperature_range_C: float
    iterations: int
    converged: bool


def _harmonic(a: float, b: float) -> float:
    return 2.0 * a * b / (a + b + 1e-30)


def _coordinates(n: int) -> tuple[np.ndarray, np.ndarray]:
    jj, ii = np.mgrid[0:n, 0:n]
    return (ii + 0.5) / n, (jj + 0.5) / n


def _distance_to_segment(
    x: np.ndarray,
    y: np.ndarray,
    a: tuple[float, float],
    b: tuple[float, float],
) -> np.ndarray:
    ax, ay = a
    bx, by = b
    vx = bx - ax
    vy = by - ay
    t = np.clip(((x - ax) * vx + (y - ay) * vy) / (vx * vx + vy * vy + 1e-30), 0.0, 1.0)
    return np.sqrt((x - (ax + t * vx)) ** 2 + (y - (ay + t * vy)) ** 2)


def _line_score(
    n: int,
    segments: list[tuple[tuple[float, float], tuple[float, float]]],
    sigma: float,
) -> np.ndarray:
    x, y = _coordinates(n)
    score = np.zeros((n, n), dtype=float)
    for a, b in segments:
        distance = _distance_to_segment(x, y, a, b)
        score = np.maximum(score, np.exp(-((distance / sigma) ** 2)))
    return score


def _normalize(score: np.ndarray) -> np.ndarray:
    score = np.asarray(score, dtype=float)
    return (score - score.min()) / (score.max() - score.min() + 1e-30)


def exact_coverage_mask(score: np.ndarray, fraction: float = DEFAULT_MATERIAL_FRACTION) -> np.ndarray:
    """Select the highest-score cells while preserving the material count."""
    score = np.asarray(score, dtype=float)
    if score.ndim != 2 or score.shape[0] != score.shape[1]:
        raise ValueError("score must be a square 2-D field")
    if not 0.0 < fraction < 1.0:
        raise ValueError("fraction must be in (0,1)")
    count = int(round(fraction * score.size))
    selected = np.argpartition(score.ravel(), -count)[-count:]
    mask = np.zeros(score.size, dtype=bool)
    mask[selected] = True
    return mask.reshape(score.shape)


def topology_scores(n: int) -> dict[str, np.ndarray]:
    """Return unthresholded routing-priority fields."""
    centers = np.array(((0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)))

    directed_segments = [
        ((0.0, 0.25), (1.0, 0.25)),
        ((0.0, 0.75), (1.0, 0.75)),
        ((0.25, 0.0), (0.25, 1.0)),
        ((0.75, 0.0), (0.75, 1.0)),
    ]

    herringbone = [((0.5, 0.0), (0.5, 1.0))]
    for center in centers:
        c = tuple(center)
        herringbone.extend((((0.5, c[1]), c), ((0.5, 0.5), c)))

    radial: list[tuple[tuple[float, float], tuple[float, float]]] = []
    for center in centers:
        radial.append(((0.5, 0.5), tuple(center)))
    for edge in ((0.5, 0.0), (1.0, 0.5), (0.5, 1.0), (0.0, 0.5)):
        radial.append((edge, (0.5, 0.5)))

    leaf = [
        ((0.0, 0.5), (1.0, 0.5)),
        ((0.5, 0.0), (0.5, 1.0)),
        ((0.0, 0.0), (1.0, 1.0)),
        ((1.0, 0.0), (0.0, 1.0)),
    ]
    for center in centers:
        c = tuple(center)
        leaf.extend((((0.5, c[1]), c), ((c[0], 0.5), c)))

    x, y = _coordinates(n)
    mesh = np.maximum(np.cos(2.0 * np.pi * 4.0 * x) ** 10, np.cos(2.0 * np.pi * 4.0 * y) ** 10)

    return {
        "parallel_stripes": _line_score(n, directed_segments, 0.024),
        "herringbone": _line_score(n, herringbone, 0.020),
        "radial_spokes": _line_score(n, radial, 0.019),
        "leaf_venation": _line_score(n, leaf, 0.016),
        "redundant_mesh": mesh,
    }


def topology_mask(
    topology: str,
    n: int,
    material_fraction: float = DEFAULT_MATERIAL_FRACTION,
    mesh_weight: float | None = None,
) -> np.ndarray:
    scores = topology_scores(n)
    if topology == "directed_mesh_blend":
        if mesh_weight is None or not 0.0 <= mesh_weight <= 1.0:
            raise ValueError("mesh_weight must be in [0,1] for blend")
        directed = _normalize(scores["parallel_stripes"])
        mesh = _normalize(scores["redundant_mesh"])
        score = (1.0 - mesh_weight) * directed + mesh_weight * mesh
    else:
        if topology not in scores:
            raise ValueError(f"unknown topology: {topology}")
        score = scores[topology]
    return exact_coverage_mask(score, material_fraction)


def wet_mask(pattern: str, n: int) -> np.ndarray:
    """Return equal-purpose wet patterns for robustness checks."""
    x, y = _coordinates(n)
    mask = np.zeros((n, n), dtype=bool)

    if pattern == "four_islands":
        centers = ((0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75))
        radius = 0.138
    elif pattern == "top_pair":
        centers = ((0.25, 0.25), (0.75, 0.25))
        radius = 0.195
    elif pattern == "diagonal_pair":
        centers = ((0.25, 0.25), (0.75, 0.75))
        radius = 0.195
    elif pattern == "single_center":
        centers = ((0.5, 0.5),)
        radius = np.sqrt(0.229 / np.pi)
    elif pattern == "shifted_four":
        centers = ((0.20, 0.30), (0.70, 0.20), (0.30, 0.78), (0.80, 0.68))
        radius = 0.138
    else:
        raise ValueError(f"unknown wet pattern: {pattern}")

    for cx, cy in centers:
        mask |= (x - cx) ** 2 + (y - cy) ** 2 <= radius**2
    return mask


def localized_damage(
    mask: np.ndarray,
    center_x: float,
    center_y: float,
    remove_fraction_of_high_k: float = 0.05,
) -> np.ndarray:
    """Remove a fixed amount of conductor nearest one tear center."""
    mask = np.asarray(mask, dtype=bool)
    x, y = _coordinates(mask.shape[0])
    conductor = np.flatnonzero(mask.ravel())
    n_remove = max(1, int(round(remove_fraction_of_high_k * len(conductor))))
    distance2 = (x.ravel()[conductor] - center_x) ** 2 + (y.ravel()[conductor] - center_y) ** 2
    local = np.argpartition(distance2, n_remove - 1)[:n_remove]
    damaged = mask.ravel().copy()
    damaged[conductor[local]] = False
    return damaged.reshape(mask.shape)


def distributed_dropout(
    mask: np.ndarray,
    remove_fraction_of_high_k: float = 0.05,
    seed: int = 20260820,
) -> np.ndarray:
    """Remove a fixed random subset of conductor cells."""
    mask = np.asarray(mask, dtype=bool)
    conductor = np.flatnonzero(mask.ravel())
    n_remove = max(1, int(round(remove_fraction_of_high_k * len(conductor))))
    rng = np.random.default_rng(seed)
    removed = rng.choice(conductor, n_remove, replace=False)
    damaged = mask.ravel().copy()
    damaged[removed] = False
    return damaged.reshape(mask.shape)


class HeatNetworkTile:
    def __init__(
        self,
        conductor_mask: np.ndarray,
        wet_field: np.ndarray,
        domain_mm: float = DEFAULT_DOMAIN_MM,
        high_sheet_W_K: float = DEFAULT_HIGH_SHEET_W_K,
        background_sheet_W_K: float = DEFAULT_BACKGROUND_SHEET_W_K,
        h_contact_W_m2K: float = DEFAULT_H_CONTACT,
        h_dry_W_m2K: float = DEFAULT_H_DRY,
        ambient_c: float = DEFAULT_AMBIENT_C,
        ambient_rh: float = DEFAULT_AMBIENT_RH,
    ) -> None:
        conductor = np.asarray(conductor_mask, dtype=bool)
        wet = np.asarray(wet_field, dtype=bool)
        if conductor.shape != wet.shape or conductor.ndim != 2 or conductor.shape[0] != conductor.shape[1]:
            raise ValueError("conductor and wet fields must be equal square arrays")

        self.conductor = conductor
        self.wet = wet
        self.n = conductor.shape[0]
        self.length_m = domain_mm * 1e-3
        self.dx = self.length_m / self.n
        self.sheet = np.where(conductor, high_sheet_W_K, background_sheet_W_K)
        self.h_contact = float(h_contact_W_m2K)
        self.h_dry = float(h_dry_W_m2K)
        self.ambient_c = float(ambient_c)
        self.c_inf = float(ambient_rh * saturated_vapor_density(ambient_c))

        rows: list[int] = []
        cols: list[int] = []
        values: list[float] = []

        def index(j: int, i: int) -> int:
            return j * self.n + i

        for j in range(self.n):
            for i in range(self.n):
                p = index(j, i)
                diagonal = -U_BODY - self.h_contact
                for dj, di in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    jj = (j + dj) % self.n
                    ii = (i + di) % self.n
                    face = _harmonic(float(self.sheet[j, i]), float(self.sheet[jj, ii])) / self.dx**2
                    rows.append(p)
                    cols.append(index(jj, ii))
                    values.append(face)
                    diagonal -= face
                rows.append(p)
                cols.append(p)
                values.append(diagonal)

        matrix = coo_matrix((values, (rows, cols)), shape=(self.n * self.n, self.n * self.n)).tocsc()
        self._solve = factorized(matrix)

    def solve(
        self,
        tolerance_C: float = 1e-6,
        max_iterations: int = 700,
        relaxation: float = 0.40,
    ) -> dict[str, object]:
        spreader = np.full((self.n, self.n), 32.0)
        outer = np.full_like(spreader, 32.0)
        change = np.inf

        for iteration in range(max_iterations):
            h_local = np.where(self.wet, H_WET, self.h_dry)
            outer_new = (self.h_contact * spreader + h_local * self.ambient_c) / (self.h_contact + h_local)

            for _ in range(15):
                evap = np.zeros_like(outer_new)
                evap[self.wet] = KM_WET * np.maximum(
                    saturated_vapor_density(outer_new[self.wet]) - self.c_inf,
                    0.0,
                )
                active = np.zeros_like(self.wet)
                active[self.wet] = saturated_vapor_density(outer_new[self.wet]) > self.c_inf
                residual = (
                    self.h_contact * (spreader - outer_new)
                    + h_local * (self.ambient_c - outer_new)
                    - L_V * evap
                )
                derivative = (
                    -self.h_contact
                    - h_local
                    - L_V
                    * KM_WET
                    * saturated_vapor_density_derivative(outer_new)
                    * active
                )
                step = residual / derivative
                outer_new = np.clip(outer_new - step, 5.0, 55.0)
                if float(np.max(np.abs(step))) < 1e-11:
                    break

            rhs = np.full(spreader.size, -U_BODY * T_SKIN) - self.h_contact * outer_new.ravel()
            spreader_new = self._solve(rhs).reshape(spreader.shape)
            change = max(
                float(np.max(np.abs(spreader_new - spreader))),
                float(np.max(np.abs(outer_new - outer))),
            )
            spreader = (1.0 - relaxation) * spreader + relaxation * spreader_new
            outer = (1.0 - relaxation) * outer + relaxation * outer_new
            if change < tolerance_C:
                break

        evap = np.zeros_like(outer)
        evap[self.wet] = KM_WET * np.maximum(
            saturated_vapor_density(outer[self.wet]) - self.c_inf,
            0.0,
        )
        body_flux = U_BODY * (T_SKIN - spreader)
        return {
            "material_fraction": float(np.mean(self.conductor)),
            "wet_fraction": float(np.mean(self.wet)),
            "body_heat_flux_W_m2": float(np.mean(body_flux)),
            "evaporation_capacity_g_m2_h": float(np.mean(evap) * 3.6e6),
            "temperature_std_C": float(np.std(spreader)),
            "temperature_range_C": float(np.ptp(spreader)),
            "iterations": iteration + 1,
            "converged": bool(change < tolerance_C),
        }


def evaluate(
    topology: str,
    n: int = 30,
    wet_pattern: str = "four_islands",
    material_fraction: float = DEFAULT_MATERIAL_FRACTION,
    mesh_weight: float | None = None,
) -> NetworkResult:
    wet_field = wet_mask(wet_pattern, n)
    conductor = topology_mask(topology, n, material_fraction, mesh_weight)
    background = HeatNetworkTile(np.zeros_like(conductor), wet_field).solve()
    result = HeatNetworkTile(conductor, wet_field).solve()
    gain_W = (
        float(result["body_heat_flux_W_m2"])
        - float(background["body_heat_flux_W_m2"])
    ) * STRUCTURED_AREA_M2
    label = topology if mesh_weight is None else f"{topology}:{mesh_weight:.3f}"
    return NetworkResult(
        topology=label,
        material_fraction=float(result["material_fraction"]),
        wet_fraction=float(result["wet_fraction"]),
        body_heat_flux_W_m2=float(result["body_heat_flux_W_m2"]),
        gain_vs_background_W=float(gain_W),
        temperature_std_C=float(result["temperature_std_C"]),
        temperature_range_C=float(result["temperature_range_C"]),
        iterations=int(result["iterations"]),
        converged=bool(result["converged"]),
    )


def run_nominal_screen(n: int = 30) -> pd.DataFrame:
    rows = []
    for topology in (
        "parallel_stripes",
        "herringbone",
        "radial_spokes",
        "leaf_venation",
        "redundant_mesh",
    ):
        rows.append(evaluate(topology, n=n).__dict__)
    for mesh_weight in (0.125, 0.375):
        rows.append(
            evaluate(
                "directed_mesh_blend",
                n=n,
                mesh_weight=mesh_weight,
            ).__dict__
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    table = run_nominal_screen()
    print(table.to_string(index=False))
