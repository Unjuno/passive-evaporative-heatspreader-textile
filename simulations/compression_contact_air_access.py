"""Compression competition between thermal contact and evaporative air access.

Compression can have opposite effects in the garment concept:

- improve spreader-to-outer thermal contact;
- close open valleys/gaps and reduce both vapor and sensible ambient exchange.

This low-order screen uses a dimensionless compression fraction ``c`` and
explicit hypothetical constitutive laws.  It is intended to reveal the regime
transition, not to claim measured textile compression properties.

Contact screen:
    h_contact(c) = h_contact_0 * (1 + a*c)

Ambient-access screen:
    s_air(c) = (1-c)^n

The wet sensible and vapor coefficients are multiplied by ``s_air``.  The dry
ambient coefficient is scaled by the same factor.  Three exponents ``n`` are
used as model-form sensitivity rather than a probability distribution.

The solver explicitly switches between:

- supply-limited partial wetness when fully-wet transfer capacity exceeds feed;
- transfer-limited full wetness when capacity falls below feed.

No physical specimen exists and the compression thresholds are not measured
product limits.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.optimize import brentq, least_squares

try:
    from simulations.distributed_spreader_1d import (
        H_WET,
        KM_WET,
        L_V,
        STRUCTURED_AREA_M2,
        T_SKIN,
        U_BODY,
        saturated_vapor_density,
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
    )

DEFAULT_AMBIENT_C = 35.0
DEFAULT_AMBIENT_RH = 0.50
DEFAULT_FEED_G_H = 100.0
DEFAULT_H_CONTACT = 800.0
DEFAULT_H_DRY = 5.0
DEFAULT_G_MIX = 200.0


@dataclass(frozen=True)
class CompressionResult:
    compression: float
    air_exponent: float
    air_scale: float
    h_contact_W_m2K: float
    regime: str
    wet_fraction: float
    evaporation_g_h: float
    body_heat_W: float
    wet_temp_C: float
    dry_temp_C: float | None
    converged: bool


def _series_conductance(a: float, b: float) -> float:
    return 1.0 / (1.0 / a + 1.0 / b)


def solve_compression(
    compression: float,
    air_exponent: float = 2.0,
    contact_gain: float = 2.0,
    feed_g_h: float = DEFAULT_FEED_G_H,
    ambient_c: float = DEFAULT_AMBIENT_C,
    ambient_rh: float = DEFAULT_AMBIENT_RH,
    improve_contact: bool = True,
    close_air: bool = True,
) -> CompressionResult:
    if not 0.0 <= compression < 1.0:
        raise ValueError("compression must be in [0,1)")
    if air_exponent <= 0.0:
        raise ValueError("air exponent must be positive")
    if feed_g_h <= 0.0:
        raise ValueError("feed must be positive")

    c = float(compression)
    air_scale = (1.0 - c) ** air_exponent if close_air else 1.0
    h_contact = (
        DEFAULT_H_CONTACT * (1.0 + contact_gain * c)
        if improve_contact
        else DEFAULT_H_CONTACT
    )
    h_external_wet = H_WET * air_scale
    km = KM_WET * air_scale
    h_wet = _series_conductance(h_contact, max(h_external_wet, 1e-12))
    h_dry = DEFAULT_H_DRY * air_scale
    c_inf = ambient_rh * saturated_vapor_density(ambient_c)
    feed_flux = (feed_g_h / 1000.0 / 3600.0) / STRUCTURED_AREA_M2

    def full_wet_balance(temp_c: float) -> float:
        evap = km * max(saturated_vapor_density(temp_c) - c_inf, 0.0)
        return (
            U_BODY * (T_SKIN - temp_c)
            + h_wet * (ambient_c - temp_c)
            - L_V * evap
        )

    grid = np.linspace(15.0, 40.0, 160)
    values = np.array([full_wet_balance(value) for value in grid])
    roots = np.where(values[:-1] * values[1:] <= 0.0)[0]
    if len(roots) == 0:
        raise RuntimeError("no full-wet energy root")
    wet_full = brentq(full_wet_balance, grid[roots[0]], grid[roots[0] + 1])
    evap_full_flux = km * max(saturated_vapor_density(wet_full) - c_inf, 0.0)
    full_capacity_g_h = evap_full_flux * STRUCTURED_AREA_M2 * 3.6e6

    if full_capacity_g_h < feed_g_h:
        return CompressionResult(
            compression=c,
            air_exponent=float(air_exponent),
            air_scale=float(air_scale),
            h_contact_W_m2K=float(h_contact),
            regime="transfer-limited-full-wet",
            wet_fraction=1.0,
            evaporation_g_h=float(full_capacity_g_h),
            body_heat_W=float(U_BODY * (T_SKIN - wet_full) * STRUCTURED_AREA_M2),
            wet_temp_C=float(wet_full),
            dry_temp_C=None,
            converged=True,
        )

    def residual(state: np.ndarray) -> np.ndarray:
        wet_c, dry_c, beta = state
        evap = km * max(saturated_vapor_density(wet_c) - c_inf, 0.0)
        q_mix = DEFAULT_G_MIX * (dry_c - wet_c)
        return np.array(
            (
                U_BODY * (T_SKIN - wet_c)
                + h_wet * (ambient_c - wet_c)
                + q_mix / beta
                - L_V * evap,
                U_BODY * (T_SKIN - dry_c)
                + h_dry * (ambient_c - dry_c)
                - q_mix / (1.0 - beta),
                L_V * (beta * evap - feed_flux),
            )
        ) / 100.0

    solution = least_squares(
        residual,
        np.array((30.5, 34.0, 0.55)),
        bounds=(np.array((10.0, 10.0, 1e-5)), np.array((45.0, 45.0, 0.999))),
        xtol=1e-12,
        ftol=1e-12,
        gtol=1e-12,
        max_nfev=5000,
    )
    wet_c, dry_c, beta = solution.x
    evap_flux = km * max(saturated_vapor_density(float(wet_c)) - c_inf, 0.0)
    body_heat = (
        beta * U_BODY * (T_SKIN - wet_c)
        + (1.0 - beta) * U_BODY * (T_SKIN - dry_c)
    ) * STRUCTURED_AREA_M2
    max_residual = float(np.max(np.abs(residual(solution.x))) * 100.0)

    return CompressionResult(
        compression=c,
        air_exponent=float(air_exponent),
        air_scale=float(air_scale),
        h_contact_W_m2K=float(h_contact),
        regime="supply-limited-partial-wet",
        wet_fraction=float(beta),
        evaporation_g_h=float(beta * evap_flux * STRUCTURED_AREA_M2 * 3.6e6),
        body_heat_W=float(body_heat),
        wet_temp_C=float(wet_c),
        dry_temp_C=float(dry_c),
        converged=bool(solution.success and max_residual < 1e-5),
    )


def run_screen() -> pd.DataFrame:
    rows = []
    for exponent in (1.0, 2.0, 3.0):
        for compression in np.linspace(0.0, 0.80, 17):
            result = solve_compression(float(compression), exponent)
            rows.append(result.__dict__)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(run_screen().to_string(index=False))
