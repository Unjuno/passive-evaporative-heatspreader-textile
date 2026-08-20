"""Apparel-constraint robustness screen for the 2-D heat network.

This module asks two narrower questions after the equal-material topology screen:

1. how sensitive is the routed-heat mechanism to a first-order uniaxial stretch
   penalty on in-plane conductance?;
2. how sensitive is it to spatial loss of spreader-to-outer thermal contact?

The stretch modes are deliberately low-order:

- ``straight_geometry_only``: x conduction factor = 1/(1+strain)^2;
- ``straight_volume_preserving``: adds one more 1/(1+strain) factor;
- ``serpentine_screen``: uses the previously documented geometric retention
  points for a compliant serpentine path.

These are not constitutive textile models.  The contact-loss maps are likewise
mechanism screens, not measured contact coefficients.

No physical specimen exists.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import factorized

try:
    from simulations.heat_network_topology_2d import (
        DEFAULT_AMBIENT_C,
        DEFAULT_AMBIENT_RH,
        DEFAULT_BACKGROUND_SHEET_W_K,
        DEFAULT_H_CONTACT,
        DEFAULT_H_DRY,
        DEFAULT_HIGH_SHEET_W_K,
        DEFAULT_MATERIAL_FRACTION,
        _harmonic,
        topology_mask,
        wet_mask,
    )
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
    from heat_network_topology_2d import (
        DEFAULT_AMBIENT_C,
        DEFAULT_AMBIENT_RH,
        DEFAULT_BACKGROUND_SHEET_W_K,
        DEFAULT_H_CONTACT,
        DEFAULT_H_DRY,
        DEFAULT_HIGH_SHEET_W_K,
        DEFAULT_MATERIAL_FRACTION,
        _harmonic,
        topology_mask,
        wet_mask,
    )
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

SERPENTINE_POINTS = np.array(
    [
        (0.00, 1.000),
        (0.05, 0.952),
        (0.10, 0.908),
        (0.15, 0.869),
        (0.20, 0.833),
        (0.30, 0.769),
    ],
    dtype=float,
)


def stretch_conduction_factor(strain: float, mode: str) -> float:
    if not 0.0 <= strain <= 0.30:
        raise ValueError("screen supports strain in [0,0.30]")
    ratio = 1.0 + strain
    if mode == "straight_geometry_only":
        return 1.0 / ratio**2
    if mode == "straight_volume_preserving":
        return 1.0 / ratio**3
    if mode == "serpentine_screen":
        return float(np.interp(strain, SERPENTINE_POINTS[:, 0], SERPENTINE_POINTS[:, 1]))
    raise ValueError(f"unknown stretch mode: {mode}")


def contact_field(case: str, n: int, low_contact_W_m2K: float = 100.0, seed: int = 20260820) -> np.ndarray:
    """Return a spatial spreader-to-outer contact map."""
    field = np.full((n, n), DEFAULT_H_CONTACT, dtype=float)
    jj, ii = np.mgrid[0:n, 0:n]
    x = (ii + 0.5) / n
    y = (jj + 0.5) / n

    if case == "uniform":
        return field
    if case == "localized_wet_island":
        region = (x - 0.25) ** 2 + (y - 0.25) ** 2 <= 0.18**2
        field[region] = low_contact_W_m2K
        return field
    if case == "center_seam":
        field[np.abs(x - 0.5) < 0.05] = low_contact_W_m2K
        return field
    if case == "distributed_10pct":
        rng = np.random.default_rng(seed)
        selected = rng.choice(n * n, int(round(0.10 * n * n)), replace=False)
        field.ravel()[selected] = low_contact_W_m2K
        return field
    raise ValueError(f"unknown contact case: {case}")


class RobustHeatNetworkTile:
    def __init__(
        self,
        conductor_mask: np.ndarray,
        wet_field: np.ndarray,
        h_contact_field: np.ndarray | None = None,
        x_conduction_factor: float = 1.0,
        y_conduction_factor: float = 1.0,
        domain_mm: float = DEFAULT_DOMAIN_MM,
        high_sheet_W_K: float = DEFAULT_HIGH_SHEET_W_K,
        background_sheet_W_K: float = DEFAULT_BACKGROUND_SHEET_W_K,
        h_dry_W_m2K: float = DEFAULT_H_DRY,
        ambient_c: float = DEFAULT_AMBIENT_C,
        ambient_rh: float = DEFAULT_AMBIENT_RH,
    ) -> None:
        conductor = np.asarray(conductor_mask, dtype=bool)
        wet = np.asarray(wet_field, dtype=bool)
        if conductor.shape != wet.shape or conductor.ndim != 2 or conductor.shape[0] != conductor.shape[1]:
            raise ValueError("conductor and wet fields must be equal square arrays")
        if x_conduction_factor <= 0.0 or y_conduction_factor <= 0.0:
            raise ValueError("conduction factors must be positive")

        self.n = conductor.shape[0]
        self.wet = wet
        self.sheet = np.where(conductor, high_sheet_W_K, background_sheet_W_K)
        self.dx = domain_mm * 1e-3 / self.n
        self.h_dry = float(h_dry_W_m2K)
        self.ambient_c = float(ambient_c)
        self.c_inf = float(ambient_rh * saturated_vapor_density(ambient_c))
        self.fx = float(x_conduction_factor)
        self.fy = float(y_conduction_factor)

        if h_contact_field is None:
            self.h_contact = np.full((self.n, self.n), DEFAULT_H_CONTACT, dtype=float)
        else:
            contact = np.asarray(h_contact_field, dtype=float)
            if contact.shape != conductor.shape or np.any(contact <= 0.0):
                raise ValueError("contact map must be positive and match topology shape")
            self.h_contact = contact

        rows: list[int] = []
        cols: list[int] = []
        values: list[float] = []

        def index(j: int, i: int) -> int:
            return j * self.n + i

        for j in range(self.n):
            for i in range(self.n):
                p = index(j, i)
                diagonal = -U_BODY - float(self.h_contact[j, i])
                for dj, di, factor in (
                    (0, 1, self.fx),
                    (0, -1, self.fx),
                    (1, 0, self.fy),
                    (-1, 0, self.fy),
                ):
                    jj = (j + dj) % self.n
                    ii = (i + di) % self.n
                    face = (
                        factor
                        * _harmonic(float(self.sheet[j, i]), float(self.sheet[jj, ii]))
                        / self.dx**2
                    )
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
        tolerance_C: float = 2e-6,
        max_iterations: int = 600,
        relaxation: float = 0.42,
    ) -> dict[str, float | bool | int]:
        spreader = np.full((self.n, self.n), 32.0)
        outer = np.full_like(spreader, 32.0)
        change = np.inf

        for iteration in range(max_iterations):
            h_local = np.where(self.wet, H_WET, self.h_dry)
            outer_new = (
                self.h_contact * spreader + h_local * self.ambient_c
            ) / (self.h_contact + h_local)

            for _ in range(12):
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
                if float(np.max(np.abs(step))) < 1e-10:
                    break

            rhs = -U_BODY * T_SKIN * np.ones(spreader.size) - self.h_contact.ravel() * outer_new.ravel()
            spreader_new = self._solve(rhs).reshape(spreader.shape)
            change = max(
                float(np.max(np.abs(spreader_new - spreader))),
                float(np.max(np.abs(outer_new - outer))),
            )
            spreader = (1.0 - relaxation) * spreader + relaxation * spreader_new
            outer = (1.0 - relaxation) * outer + relaxation * outer_new
            if change < tolerance_C:
                break

        return {
            "body_heat_flux_W_m2": float(np.mean(U_BODY * (T_SKIN - spreader))),
            "temperature_std_C": float(np.std(spreader)),
            "iterations": iteration + 1,
            "converged": bool(change < tolerance_C),
        }


def _gain(
    conductor: np.ndarray,
    wet: np.ndarray,
    contact: np.ndarray,
    fx: float = 1.0,
    fy: float = 1.0,
) -> tuple[float, bool]:
    background = RobustHeatNetworkTile(
        np.zeros_like(conductor), wet, contact, fx, fy
    ).solve()
    routed = RobustHeatNetworkTile(conductor, wet, contact, fx, fy).solve()
    gain = (
        float(routed["body_heat_flux_W_m2"])
        - float(background["body_heat_flux_W_m2"])
    ) * STRUCTURED_AREA_M2
    return gain, bool(background["converged"] and routed["converged"])


def run_stretch_screen(n: int = 24) -> pd.DataFrame:
    wet = wet_mask("four_islands", n)
    rows = []
    for name, mesh_weight in (("directed_mesh_blend", 0.125), ("directed_mesh_blend", 0.375), ("redundant_mesh", None)):
        conductor = topology_mask(name, n, DEFAULT_MATERIAL_FRACTION, mesh_weight)
        label = name if mesh_weight is None else f"blend_{mesh_weight:.3f}"
        contact = contact_field("uniform", n)
        for strain in (0.0, 0.10, 0.20, 0.30):
            for mode in (
                "straight_geometry_only",
                "straight_volume_preserving",
                "serpentine_screen",
            ):
                fx = stretch_conduction_factor(strain, mode)
                gain, converged = _gain(conductor, wet, contact, fx=fx, fy=1.0)
                rows.append(
                    {
                        "topology": label,
                        "strain": strain,
                        "mode": mode,
                        "x_conduction_factor": fx,
                        "gain_W": gain,
                        "converged": converged,
                    }
                )
    return pd.DataFrame(rows)


def run_contact_screen(n: int = 24) -> pd.DataFrame:
    wet = wet_mask("four_islands", n)
    rows = []
    for name, mesh_weight in (("directed_mesh_blend", 0.125), ("directed_mesh_blend", 0.375), ("redundant_mesh", None)):
        conductor = topology_mask(name, n, DEFAULT_MATERIAL_FRACTION, mesh_weight)
        label = name if mesh_weight is None else f"blend_{mesh_weight:.3f}"
        for case in ("uniform", "localized_wet_island", "center_seam", "distributed_10pct"):
            contact = contact_field(case, n)
            gain, converged = _gain(conductor, wet, contact)
            rows.append(
                {
                    "topology": label,
                    "contact_case": case,
                    "low_contact_fraction": float(np.mean(contact < DEFAULT_H_CONTACT)),
                    "gain_W": gain,
                    "converged": converged,
                }
            )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print("STRETCH")
    print(run_stretch_screen().to_string(index=False))
    print("\nCONTACT")
    print(run_contact_screen().to_string(index=False))
