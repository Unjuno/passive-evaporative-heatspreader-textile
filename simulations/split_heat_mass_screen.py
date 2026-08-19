"""Split sensible-heat and vapor-transfer screening model.

This module removes one deliberate simplification from ``passive_rib_screen``:
the exterior heat-transfer multiplier and vapor mass-transfer multiplier are
independent parameters.

Use ``M_h`` for sensible convective heat transfer and ``M_m`` for water-vapor
mass transfer.  Radiation is not multiplied by either value.

This is a low-order screening model, not CFD and not a validated garment
performance predictor.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.optimize import brentq

try:
    from simulations.passive_rib_screen import (
        A,
        H_RAD,
        L_V,
        T_SKIN,
        passive_coeffs,
        rho_v_sat,
    )
except ModuleNotFoundError:  # direct execution: python simulations/...
    from passive_rib_screen import (
        A,
        H_RAD,
        L_V,
        T_SKIN,
        passive_coeffs,
        rho_v_sat,
    )


@dataclass(frozen=True)
class SplitEquilibrium:
    surface_temp_C: float
    body_cooling_W: float
    evaporation_g_h: float
    residual_slope: float


def stable_equilibria_split(
    ambient_c: float,
    rh: float,
    water_gph: float,
    heat_multiplier: float,
    mass_multiplier: float,
    u_body: float,
    grid_points: int = 1200,
) -> list[SplitEquilibrium]:
    """Return all stable equilibria using independent external multipliers.

    Parameters
    ----------
    heat_multiplier:
        ``M_h`` multiplying only sensible convective heat transfer.
    mass_multiplier:
        ``M_m`` multiplying only vapor mass transfer.
    """
    if heat_multiplier <= 0.0 or mass_multiplier <= 0.0:
        raise ValueError("transfer multipliers must be positive")

    water_flux_cap = (water_gph / 1000.0 / 3600.0) / A

    def terms(surface_c: float) -> tuple[float, float, float]:
        h, km = passive_coeffs(surface_c, ambient_c, rh)
        q_body = u_body * (T_SKIN - surface_c)
        q_conv = heat_multiplier * h * (ambient_c - surface_c)
        q_rad = H_RAD * (ambient_c - surface_c)
        vapor_drive = max(
            rho_v_sat(surface_c) - rh * rho_v_sat(ambient_c),
            0.0,
        )
        m_capacity = mass_multiplier * km * vapor_drive
        m_evap = min(m_capacity, water_flux_cap)
        residual = q_body + q_conv + q_rad - L_V * m_evap
        return residual, q_body, m_evap

    grid = np.linspace(18.0, 39.5, grid_points)
    vals = np.array([terms(t)[0] for t in grid])
    roots: list[SplitEquilibrium] = []

    for idx in np.where(vals[:-1] * vals[1:] <= 0.0)[0]:
        try:
            root = brentq(lambda x: terms(x)[0], grid[idx], grid[idx + 1], maxiter=100)
        except ValueError:
            continue

        eps = 1e-4
        slope = (terms(root + eps)[0] - terms(root - eps)[0]) / (2.0 * eps)
        if slope >= 0.0:
            continue

        _, q_body, m_evap = terms(root)
        roots.append(
            SplitEquilibrium(
                surface_temp_C=float(root),
                body_cooling_W=float(q_body * A),
                evaporation_g_h=float(m_evap * A * 3600.0 * 1000.0),
                residual_slope=float(slope),
            )
        )

    unique: list[SplitEquilibrium] = []
    for root in sorted(roots, key=lambda r: r.surface_temp_C):
        if not unique or abs(root.surface_temp_C - unique[-1].surface_temp_C) > 1e-5:
            unique.append(root)
    return unique


def select_warm(roots: list[SplitEquilibrium]) -> SplitEquilibrium | None:
    """Select the warmer / lower-cooling stable branch explicitly."""
    if not roots:
        return None
    return max(roots, key=lambda r: r.surface_temp_C)


def run_split_screen() -> pd.DataFrame:
    """Screen independent M_h and M_m at the primary environment.

    ``u_body`` is intentionally held fixed so this table isolates external
    transfer assumptions rather than heat-spreader coupling.
    """
    ambient_c = 35.0
    rh = 0.70
    water_gph = 150.0
    u_body = 100.0

    reference = select_warm(
        stable_equilibria_split(ambient_c, rh, water_gph, 1.0, 1.0, u_body)
    )
    if reference is None:
        raise RuntimeError("reference equilibrium not found")

    rows: list[dict[str, float | int]] = []
    for m_h in (1.0, 1.25, 1.5, 2.0):
        for m_m in (1.0, 1.5, 2.0, 3.0, 4.0):
            roots = stable_equilibria_split(
                ambient_c, rh, water_gph, m_h, m_m, u_body
            )
            warm = select_warm(roots)
            if warm is None:
                continue
            rows.append(
                {
                    "M_h": m_h,
                    "M_m": m_m,
                    "n_stable_roots": len(roots),
                    "surface_temp_C": warm.surface_temp_C,
                    "body_cooling_W": warm.body_cooling_W,
                    "gain_vs_Mh1_Mm1_W": warm.body_cooling_W
                    - reference.body_cooling_W,
                    "evaporation_g_h": warm.evaporation_g_h,
                }
            )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = run_split_screen()
    print(df.to_string(index=False))
