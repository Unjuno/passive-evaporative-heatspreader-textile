"""Distributed 1-D vapor-renewal screen for a laterally open evaporative valley.

Purpose
-------
Extend the local analytic open-valley target in ``open_valley_exchange_target.py``
into a spatial model with:

- axial molecular diffusion;
- optional signed axial advection;
- distributed vapor addition from a wet valley surface;
- distributed lateral exchange with ambient air;
- ambient concentration at both axial ends.

The normalized vapor loading is

    theta = (C - C_inf) / (C_sat - C_inf)

and the retained wet-wall vapor driving-force fraction is

    F = 1 - theta.

The steady equation is

    D A theta'' - u A theta' + G_w' (1-theta) - G_a' theta = 0,

where G_w' is wet-surface-to-valley vapor conductance per unit axial length and
G_a' is valley-to-ambient lateral renewal conductance per unit axial length.

For the included geometry mapping:

    k_w = Sh * D / D_h
    k_a = D / delta_open
    G_w' = k_w P_w
    G_a' = k_a P_a

with a floor-only wet surface and an open top, so P_w=P_a=valley width.  The
parameter ``delta_open`` is therefore an **effective stagnant exchange
thickness**, not a directly measured geometric opening height.  Natural
convection, cross-flow, wearer motion, and turbulence can make the real lateral
exchange stronger or weaker than this diffusion-only mapping.

Important audit rule: high retention ``F`` is not by itself proof of high
absolute vapor transfer.  The local long-valley series conductance is also
reported:

    k_eff = k_w k_a / (k_w + k_a) = k_w F.

A design can obtain higher F simply by reducing k_w; that would make the local
air less loaded while also reducing evaporation capacity.

This is a SCREENING model, not CFD and not a garment cooling prediction.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

try:
    from simulations.passive_rib_screen import D_V
except ModuleNotFoundError:  # direct execution
    from passive_rib_screen import D_V

SH_SCREEN = 7.54


@dataclass(frozen=True)
class OpenValleyResult:
    width_mm: float
    depth_mm: float
    length_mm: float
    velocity_mm_s: float
    effective_open_exchange_distance_mm: float
    hydraulic_diameter_mm: float
    wet_surface_transfer_coefficient_m_s: float
    lateral_renewal_coefficient_m_s: float
    effective_series_vapor_conductance_m_s: float
    renewal_to_wet_ratio_R: float
    local_long_valley_retention_F: float
    exchange_length_mm: float
    axial_Pe: float
    center_retention_F: float
    mean_retention_F: float
    minimum_retention_F: float


def hydraulic_diameter(width_m: float, depth_m: float) -> float:
    if width_m <= 0.0 or depth_m <= 0.0:
        raise ValueError("valley dimensions must be positive")
    return 4.0 * width_m * depth_m / (2.0 * (width_m + depth_m))


def solve_open_valley(
    width_mm: float,
    depth_mm: float,
    length_mm: float,
    velocity_mm_s: float = 0.0,
    effective_open_exchange_distance_mm: float = 0.5,
    nx: int = 401,
) -> OpenValleyResult:
    """Solve the normalized distributed vapor balance.

    Boundary conditions are ambient vapor loading at both ends: theta=0.
    First-order upwinding is used for axial advection so the screen remains
    numerically stable across the parameter sweep.
    """
    if width_mm <= 0.0 or depth_mm <= 0.0 or length_mm <= 0.0:
        raise ValueError("width, depth and length must be positive")
    if effective_open_exchange_distance_mm <= 0.0:
        raise ValueError("effective exchange distance must be positive")
    if nx < 5:
        raise ValueError("nx must be at least 5")

    width = width_mm * 1e-3
    depth = depth_mm * 1e-3
    length = length_mm * 1e-3
    velocity = velocity_mm_s * 1e-3
    delta_open = effective_open_exchange_distance_mm * 1e-3

    area = width * depth
    dh = hydraulic_diameter(width, depth)

    k_w = SH_SCREEN * D_V / dh
    k_a = D_V / delta_open
    p_wet = width
    p_open = width
    g_w = k_w * p_wet
    g_a = k_a * p_open

    ratio = g_a / g_w
    local_retention = ratio / (1.0 + ratio)
    k_eff = k_w * k_a / (k_w + k_a)
    source_rate = g_w / area
    total_relaxation_rate = (g_w + g_a) / area
    exchange_length = np.sqrt(D_V / total_relaxation_rate)

    z = np.linspace(0.0, length, nx)
    dz = z[1] - z[0]
    n = nx - 2

    lower = np.full(n - 1, D_V / dz**2)
    diagonal = np.full(n, -2.0 * D_V / dz**2 - total_relaxation_rate)
    upper = np.full(n - 1, D_V / dz**2)

    if velocity >= 0.0:
        diagonal += -velocity / dz
        lower += velocity / dz
    else:
        diagonal += velocity / dz
        upper += -velocity / dz

    rhs = np.full(n, -source_rate)
    matrix = diags((lower, diagonal, upper), offsets=(-1, 0, 1), format="csr")
    interior = spsolve(matrix, rhs)

    theta = np.zeros(nx)
    theta[1:-1] = interior
    retention = 1.0 - theta

    return OpenValleyResult(
        width_mm=width_mm,
        depth_mm=depth_mm,
        length_mm=length_mm,
        velocity_mm_s=velocity_mm_s,
        effective_open_exchange_distance_mm=effective_open_exchange_distance_mm,
        hydraulic_diameter_mm=dh * 1e3,
        wet_surface_transfer_coefficient_m_s=k_w,
        lateral_renewal_coefficient_m_s=k_a,
        effective_series_vapor_conductance_m_s=k_eff,
        renewal_to_wet_ratio_R=ratio,
        local_long_valley_retention_F=local_retention,
        exchange_length_mm=exchange_length * 1e3,
        axial_Pe=abs(velocity) * length / D_V,
        center_retention_F=float(retention[nx // 2]),
        mean_retention_F=float(np.mean(retention)),
        minimum_retention_F=float(np.min(retention)),
    )


def run_screen() -> pd.DataFrame:
    """Return a compact deterministic screen used by CI/reference generation."""
    rows = []
    for length_mm in (1.0, 2.0, 5.0, 20.0, 50.0):
        for delta_mm in (0.10, 0.25, 0.50, 1.0, 2.0):
            for velocity_mm_s in (0.0, 5.0, 100.0):
                r = solve_open_valley(
                    width_mm=6.0,
                    depth_mm=3.0,
                    length_mm=length_mm,
                    velocity_mm_s=velocity_mm_s,
                    effective_open_exchange_distance_mm=delta_mm,
                )
                rows.append(
                    {
                        "classification": "SIMULATION/SCREEN",
                        **r.__dict__,
                    }
                )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(run_screen().to_string(index=False))
