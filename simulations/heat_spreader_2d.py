"""2D anisotropic heat-spreader screening model.

This model isolates lateral heat routing. It does NOT calculate evaporation mass
transfer. Evaporative regions are represented by a prescribed effective thermal
sink to make the spatial heat-spreading problem explicit and reproducible.

Steady finite-volume equation for each cell:

    div(t * K_parallel * grad(T))
    + g_body * (T_skin - T)
    - g_sink(x,y) * (T - T_sink) = 0

No-flux conditions are applied at the outer boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve


@dataclass(frozen=True)
class SpreaderResult:
    temperature_C: np.ndarray
    body_cooling_W: float
    temperature_std_C: float
    temperature_min_C: float
    temperature_max_C: float


def vertical_band_mask(nx: int, ny: int, fraction: float = 0.25) -> np.ndarray:
    """Evaporator band occupying the right-most fraction of the domain."""
    if not (0.0 < fraction <= 1.0):
        raise ValueError("fraction must be in (0, 1]")
    mask = np.zeros((ny, nx), dtype=bool)
    start = max(0, nx - int(np.ceil(nx * fraction)))
    mask[:, start:] = True
    return mask


def solve_spreader(
    *,
    width_m: float = 0.50,
    height_m: float = 0.60,
    nx: int = 40,
    ny: int = 48,
    thickness_m: float = 0.00010,
    kx_W_mK: float = 200.0,
    ky_W_mK: float = 15.0,
    g_body_W_m2K: float = 25.0,
    g_sink_W_m2K: float = 80.0,
    skin_temp_C: float = 34.0,
    sink_temp_C: float = 30.0,
    sink_mask: np.ndarray | None = None,
) -> SpreaderResult:
    """Solve steady anisotropic lateral conduction with a patchy thermal sink.

    Parameters `g_body` and `g_sink` are effective areal conductances. `sink_temp`
    is a prescribed proxy temperature for active evaporative zones; it is not a
    prediction of wet-surface temperature.
    """
    if nx < 2 or ny < 2:
        raise ValueError("nx and ny must be >=2")
    if width_m <= 0 or height_m <= 0 or thickness_m <= 0:
        raise ValueError("geometry must be positive")
    if min(kx_W_mK, ky_W_mK, g_body_W_m2K, g_sink_W_m2K) < 0:
        raise ValueError("conductivities/conductances must be nonnegative")

    if sink_mask is None:
        sink_mask = vertical_band_mask(nx, ny, 0.25)
    sink_mask = np.asarray(sink_mask, dtype=bool)
    if sink_mask.shape != (ny, nx):
        raise ValueError(f"sink_mask must have shape {(ny, nx)}")

    dx = width_m / nx
    dy = height_m / ny
    cell_area = dx * dy

    # Finite-volume conductance between neighboring cells [W/K].
    gx = kx_W_mK * thickness_m * dy / dx
    gy = ky_W_mK * thickness_m * dx / dy
    gb = g_body_W_m2K * cell_area
    ge = g_sink_W_m2K * cell_area

    n = nx * ny
    mat = lil_matrix((n, n), dtype=float)
    rhs = np.zeros(n, dtype=float)

    def idx(ix: int, iy: int) -> int:
        return iy * nx + ix

    for iy in range(ny):
        for ix in range(nx):
            row = idx(ix, iy)
            diag = gb
            rhs[row] = gb * skin_temp_C

            if ix > 0:
                mat[row, idx(ix - 1, iy)] = -gx
                diag += gx
            if ix < nx - 1:
                mat[row, idx(ix + 1, iy)] = -gx
                diag += gx
            if iy > 0:
                mat[row, idx(ix, iy - 1)] = -gy
                diag += gy
            if iy < ny - 1:
                mat[row, idx(ix, iy + 1)] = -gy
                diag += gy

            if sink_mask[iy, ix]:
                diag += ge
                rhs[row] += ge * sink_temp_C

            mat[row, row] = diag

    temp = spsolve(mat.tocsr(), rhs).reshape((ny, nx))
    q_body = float(np.sum(gb * (skin_temp_C - temp)))

    return SpreaderResult(
        temperature_C=temp,
        body_cooling_W=q_body,
        temperature_std_C=float(np.std(temp)),
        temperature_min_C=float(np.min(temp)),
        temperature_max_C=float(np.max(temp)),
    )


def orientation_demo() -> dict[str, SpreaderResult]:
    """Compare anisotropy aligned vs transverse to a vertical evaporator band."""
    common = dict(
        width_m=0.50,
        height_m=0.60,
        nx=40,
        ny=48,
        thickness_m=0.00010,
        g_body_W_m2K=25.0,
        g_sink_W_m2K=80.0,
        skin_temp_C=34.0,
        sink_temp_C=30.0,
    )
    return {
        "aligned_x": solve_spreader(kx_W_mK=200.0, ky_W_mK=15.0, **common),
        "reversed_y": solve_spreader(kx_W_mK=15.0, ky_W_mK=200.0, **common),
        "isotropic_100": solve_spreader(kx_W_mK=100.0, ky_W_mK=100.0, **common),
    }


if __name__ == "__main__":
    for name, result in orientation_demo().items():
        print(
            f"{name:>14s}  body_cooling={result.body_cooling_W:8.4f} W  "
            f"Tstd={result.temperature_std_C:7.4f} C  "
            f"Tmin={result.temperature_min_C:7.4f} C  "
            f"Tmax={result.temperature_max_C:7.4f} C"
        )
