"""Periodic 2-D diffusion screen for wet exterior ribs.

Purpose
-------
Estimate how strongly neighboring wet ribs share a stagnant humidity boundary
layer.  This is a deliberately low-order model: it solves steady vapor diffusion
in one periodic 2-D rib cell with a prescribed bulk-air renewal plane.

It does NOT model natural convection, forced convection, turbulence, fabric
porosity, temperature-dependent properties, or coupled heat transfer.  The
output is therefore a mass-transfer screening multiplier, not a garment cooling
prediction.

Boundary conditions
-------------------
Normalized vapor concentration u:
  u = 1 on all wet textile/rib surfaces
  u = 0 at an idealized bulk-air renewal plane above the ribs
  periodic boundary condition in x

The computed integrated vapor flux is divided by the corresponding flat wet
surface flux at the same projected pitch and renewal-plane height.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import cg


def solve_periodic_rib_diffusion(
    pitch_mm: float,
    rib_height_mm: float,
    rib_width_mm: float,
    renewal_height_mm: float,
    nx: int = 24,
) -> tuple[float, float]:
    """Return (panel mass-transfer multiplier, actual renewal height [mm])."""
    if renewal_height_mm <= rib_height_mm:
        raise ValueError("renewal_height_mm must exceed rib_height_mm")

    dx = pitch_mm / nx
    ny = int(round(renewal_height_mm / dx)) + 1
    y = np.arange(ny) * dx
    x = (np.arange(nx) + 0.5) * dx

    center = pitch_mm / 2.0
    rib_x = (
        np.abs(((x - center + pitch_mm / 2.0) % pitch_mm) - pitch_mm / 2.0)
        <= rib_width_mm / 2.0
    )

    wet_solid = np.zeros((ny, nx), dtype=bool)
    wet_solid[0, :] = True
    yi = np.where(y <= rib_height_mm)[0]
    xi = np.where(rib_x)[0]
    wet_solid[np.ix_(yi, xi)] = True

    bulk = np.zeros_like(wet_solid)
    bulk[-1, :] = True
    fixed = wet_solid | bulk
    unknown = ~fixed

    index = -np.ones((ny, nx), dtype=int)
    coords = np.argwhere(unknown)
    index[unknown] = np.arange(len(coords))

    rows: list[int] = []
    cols: list[int] = []
    data: list[float] = []
    rhs = np.zeros(len(coords))

    for k, (j, i) in enumerate(coords):
        rows.append(k)
        cols.append(k)
        data.append(4.0)

        for jj, ii in ((j, i - 1), (j, i + 1), (j - 1, i), (j + 1, i)):
            ii %= nx
            if fixed[jj, ii]:
                if wet_solid[jj, ii]:
                    rhs[k] += 1.0
            else:
                rows.append(k)
                cols.append(int(index[jj, ii]))
                data.append(-1.0)

    matrix = coo_matrix(
        (data, (rows, cols)), shape=(len(coords), len(coords))
    ).tocsr()
    solution, info = cg(matrix, rhs, rtol=1e-9, maxiter=5000)
    if info != 0:
        raise RuntimeError(f"CG did not converge: info={info}")

    u = np.zeros((ny, nx))
    u[wet_solid] = 1.0
    u[bulk] = 0.0
    u[unknown] = solution

    # Since dx == dy, the integrated dimensionless top flux reduces to this sum.
    rib_flux = float(np.sum(u[-2, :]))
    flat_flux = pitch_mm / y[-1]
    return rib_flux / flat_flux, float(y[-1])


def run_screen() -> pd.DataFrame:
    """Run the E3 boundary-layer sensitivity screen."""
    rib_height_mm = 2.5
    panel_fraction = 0.65
    pitches = (0.8, 1.0, 1.5)
    gaps_mm = (0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0, 7.5, 10.0, 15.0)

    rows: list[dict[str, float]] = []
    for pitch_mm in pitches:
        rib_width_mm = min(0.25, 0.30 * pitch_mm)
        for gap_mm in gaps_mm:
            panel_multiplier, actual_height_mm = solve_periodic_rib_diffusion(
                pitch_mm=pitch_mm,
                rib_height_mm=rib_height_mm,
                rib_width_mm=rib_width_mm,
                renewal_height_mm=rib_height_mm + gap_mm,
            )
            whole_multiplier = 1.0 + panel_fraction * (panel_multiplier - 1.0)
            rows.append(
                {
                    "rib_height_mm": rib_height_mm,
                    "pitch_mm": pitch_mm,
                    "rib_width_mm": rib_width_mm,
                    "panel_fraction": panel_fraction,
                    "renewal_gap_above_tip_mm": gap_mm,
                    "renewal_height_from_base_mm": actual_height_mm,
                    "panel_mass_transfer_multiplier": panel_multiplier,
                    "whole_garment_mass_transfer_multiplier": whole_multiplier,
                }
            )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    result = run_screen()
    print(result.to_string(index=False))
