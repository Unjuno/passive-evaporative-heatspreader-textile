"""Distributed 1-D wet/dry heat-spreader bridge model.

This module replaces the scalar two-node ``g_mix`` coupling with a periodic
one-dimensional sheet that uses direct in-plane material conductivity and
thickness:

    d/dx(k_parallel * t * dT_spreader/dx)
      + U_body (T_skin - T_spreader)
      + h_contact (T_outer - T_spreader) = 0

The outer surface is coupled locally to the spreader. Wet sub-area additionally
loses latent heat through the same low-order open-valley vapor conductance used
elsewhere in the repository. Dry sub-area uses ``h_dry`` to represent shielding
or reduced ambient sensible exposure.

A continuous wet-stripe width is solved so total evaporation matches imposed
feed when capacity permits. Boundary cells can be fractionally wet, avoiding a
wet-width grid-quantization artifact.

This remains a bridge/screening model:

- one repeating 1-D stripe period;
- isotropic scalar ``k_parallel`` within the period;
- one lumped spreader-to-outer contact coefficient;
- low-order effective exterior heat/vapor transfer rather than CFD;
- VP-C sparse coverage is represented by homogenized effective ``k*t`` rather
  than resolved conductive traces.

No physical specimen exists and no result is a measured garment claim.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.sparse import diags
from scipy.sparse.linalg import factorized

try:
    from simulations.open_valley_thermal_1d import D_V, K_AIR, L_V, NU_SCREEN, R_V, SH_SCREEN
    from simulations.passive_rib_screen import p_sat
    from simulations.virtual_prototype_v01 import PROTOTYPES
except ModuleNotFoundError:
    from open_valley_thermal_1d import D_V, K_AIR, L_V, NU_SCREEN, R_V, SH_SCREEN
    from passive_rib_screen import p_sat
    from virtual_prototype_v01 import PROTOTYPES

U_BODY = 100.0
T_SKIN = 34.0
STRUCTURED_AREA_M2 = 0.30 * 0.65
DEFAULT_AMBIENT_C = 35.0
DEFAULT_AMBIENT_RH = 0.50

# Representative open-valley wet-side coefficients retained from the current
# low-order exterior screen: 6 x 3 mm hydraulic geometry, 0.5 mm effective
# heat/vapor lateral exchange distances.
_WIDTH_M = 6e-3
_DEPTH_M = 3e-3
_DH_M = 4.0 * _WIDTH_M * _DEPTH_M / (2.0 * (_WIDTH_M + _DEPTH_M))
_H_WALL = NU_SCREEN * K_AIR / _DH_M
_H_LATERAL = K_AIR / 0.5e-3
H_WET = _H_WALL * _H_LATERAL / (_H_WALL + _H_LATERAL)
_KM_WALL = SH_SCREEN * D_V / _DH_M
_KM_LATERAL = D_V / 0.5e-3
KM_WET = _KM_WALL * _KM_LATERAL / (_KM_WALL + _KM_LATERAL)


@dataclass(frozen=True)
class DistributedSpreaderResult:
    feed_total_g_h: float
    wet_fraction: float
    evap_total_g_h: float
    mean_body_heat_flux_W_m2: float
    spreader_temperature_range_C: float
    outer_temperature_range_C: float
    max_outer_energy_residual_W_m2: float
    max_spreader_energy_residual_W_m2: float
    iterations: int
    converged: bool
    regime: str


def saturated_vapor_density(temp_c: np.ndarray | float) -> np.ndarray:
    temp = np.asarray(temp_c, dtype=float)
    return p_sat(temp) / (R_V * (temp + 273.15))


def saturated_vapor_density_derivative(temp_c: np.ndarray | float) -> np.ndarray:
    temp = np.asarray(temp_c, dtype=float)
    eps = 1e-3
    return (saturated_vapor_density(temp + eps) - saturated_vapor_density(temp - eps)) / (2.0 * eps)


def _wet_weights(beta: float, period_m: float, n: int) -> np.ndarray:
    if not 0.0 <= beta <= 1.0:
        raise ValueError("beta must be in [0,1]")
    dx = period_m / n
    centers = (np.arange(n) + 0.5) * dx
    cell_left = centers - dx / 2.0
    cell_right = centers + dx / 2.0
    wet_left = period_m / 2.0 - beta * period_m / 2.0
    wet_right = period_m / 2.0 + beta * period_m / 2.0
    overlap = np.maximum(
        0.0,
        np.minimum(cell_right, wet_right) - np.maximum(cell_left, wet_left),
    )
    return overlap / dx


class DistributedSpreader1D:
    def __init__(
        self,
        k_parallel_W_mK: float,
        effective_thickness_um: float,
        pitch_mm: float,
        h_contact_W_m2K: float,
        h_dry_W_m2K: float,
        ambient_c: float = DEFAULT_AMBIENT_C,
        ambient_rh: float = DEFAULT_AMBIENT_RH,
        n: int = 64,
    ) -> None:
        if k_parallel_W_mK <= 0 or effective_thickness_um <= 0 or pitch_mm <= 0:
            raise ValueError("k, thickness and pitch must be positive")
        if h_contact_W_m2K <= 0 or h_dry_W_m2K < 0:
            raise ValueError("contact must be positive and h_dry nonnegative")
        if not 0.0 <= ambient_rh <= 1.0:
            raise ValueError("ambient RH must be in [0,1]")
        if n < 16:
            raise ValueError("n must be at least 16")

        self.k_parallel = float(k_parallel_W_mK)
        self.thickness_m = float(effective_thickness_um) * 1e-6
        self.pitch_m = float(pitch_mm) * 1e-3
        self.h_contact = float(h_contact_W_m2K)
        self.h_dry = float(h_dry_W_m2K)
        self.ambient_c = float(ambient_c)
        self.ambient_rh = float(ambient_rh)
        self.n = int(n)
        self.dx = self.pitch_m / self.n
        self.sheet_conductance_W_K = self.k_parallel * self.thickness_m
        self.c_inf = float(self.ambient_rh * saturated_vapor_density(self.ambient_c))

        a = self.sheet_conductance_W_K / self.dx**2
        main = np.full(self.n, -2.0 * a - U_BODY - self.h_contact)
        off = np.full(self.n - 1, a)
        matrix = diags((off, main, off), offsets=(-1, 0, 1), shape=(self.n, self.n), format="lil")
        matrix[0, self.n - 1] = a
        matrix[self.n - 1, 0] = a
        self._solve_spreader = factorized(matrix.tocsc())

    def solve_wet_fraction(
        self,
        wet_fraction: float,
        tolerance_C: float = 2e-6,
        max_iterations: int = 260,
    ) -> dict[str, object]:
        wet = _wet_weights(wet_fraction, self.pitch_m, self.n)
        spreader = np.full(self.n, 32.0)
        outer = np.full(self.n, 32.0)
        relax = 0.65
        change = np.inf

        for iteration in range(max_iterations):
            h_local = wet * H_WET + (1.0 - wet) * self.h_dry
            outer_new = (
                self.h_contact * spreader + h_local * self.ambient_c
            ) / (self.h_contact + h_local)

            for _ in range(15):
                vapor_excess = np.maximum(saturated_vapor_density(outer_new) - self.c_inf, 0.0)
                active = saturated_vapor_density(outer_new) > self.c_inf
                evap_flux = wet * KM_WET * vapor_excess
                residual = (
                    self.h_contact * (spreader - outer_new)
                    + h_local * (self.ambient_c - outer_new)
                    - L_V * evap_flux
                )
                derivative = (
                    -self.h_contact
                    - h_local
                    - L_V * wet * KM_WET * saturated_vapor_density_derivative(outer_new) * active
                )
                step = residual / derivative
                outer_new = np.clip(outer_new - step, 5.0, 55.0)
                if float(np.max(np.abs(step))) < 1e-10:
                    break

            rhs = np.full(self.n, -U_BODY * T_SKIN) - self.h_contact * outer_new
            spreader_new = self._solve_spreader(rhs)
            change = max(
                float(np.max(np.abs(spreader_new - spreader))),
                float(np.max(np.abs(outer_new - outer))),
            )
            spreader = (1.0 - relax) * spreader + relax * spreader_new
            outer = (1.0 - relax) * outer + relax * outer_new
            if change < tolerance_C:
                break

        # Final local outer solve at the converged spreader state.
        h_local = wet * H_WET + (1.0 - wet) * self.h_dry
        outer = (self.h_contact * spreader + h_local * self.ambient_c) / (self.h_contact + h_local)
        for _ in range(20):
            vapor_excess = np.maximum(saturated_vapor_density(outer) - self.c_inf, 0.0)
            active = saturated_vapor_density(outer) > self.c_inf
            evap_flux = wet * KM_WET * vapor_excess
            residual = (
                self.h_contact * (spreader - outer)
                + h_local * (self.ambient_c - outer)
                - L_V * evap_flux
            )
            derivative = (
                -self.h_contact
                - h_local
                - L_V * wet * KM_WET * saturated_vapor_density_derivative(outer) * active
            )
            step = residual / derivative
            outer = np.clip(outer - step, 5.0, 55.0)
            if float(np.max(np.abs(step))) < 1e-11:
                break

        evap_flux = wet * KM_WET * np.maximum(saturated_vapor_density(outer) - self.c_inf, 0.0)
        body_flux = U_BODY * (T_SKIN - spreader)
        laplacian = (
            np.roll(spreader, 1) - 2.0 * spreader + np.roll(spreader, -1)
        ) / self.dx**2
        outer_energy_residual = (
            self.h_contact * (spreader - outer)
            + h_local * (self.ambient_c - outer)
            - L_V * evap_flux
        )
        spreader_energy_residual = (
            self.sheet_conductance_W_K * laplacian
            + U_BODY * (T_SKIN - spreader)
            + self.h_contact * (outer - spreader)
        )

        return {
            "wet_fraction": float(wet_fraction),
            "evap_total_g_h": float(np.mean(evap_flux) * 3.6e6 * STRUCTURED_AREA_M2),
            "mean_body_heat_flux_W_m2": float(np.mean(body_flux)),
            "spreader_temperature_range_C": float(np.ptp(spreader)),
            "outer_temperature_range_C": float(np.ptp(outer)),
            "max_outer_energy_residual_W_m2": float(np.max(np.abs(outer_energy_residual))),
            "max_spreader_energy_residual_W_m2": float(np.max(np.abs(spreader_energy_residual))),
            "iterations": iteration + 1,
            "converged": bool(change < tolerance_C),
            "spreader_temperature_C": spreader,
            "outer_temperature_C": outer,
            "wet_weights": wet,
        }

    def solve_feed(
        self,
        feed_total_g_h: float,
        max_wet_fraction: float = 0.95,
    ) -> DistributedSpreaderResult:
        if feed_total_g_h <= 0:
            raise ValueError("feed must be positive")
        if not 0.0 < max_wet_fraction <= 1.0:
            raise ValueError("max wet fraction must be in (0,1]")

        full = self.solve_wet_fraction(max_wet_fraction)
        if full["evap_total_g_h"] <= feed_total_g_h:
            state = full
            regime = "transfer-limited"
        else:
            def mismatch(beta: float) -> float:
                return float(self.solve_wet_fraction(beta)["evap_total_g_h"]) - feed_total_g_h

            beta = brentq(mismatch, 0.001, max_wet_fraction, xtol=2e-5, maxiter=30)
            state = self.solve_wet_fraction(beta)
            regime = "supply-limited-continuous-wet-width"

        return DistributedSpreaderResult(
            feed_total_g_h=feed_total_g_h,
            wet_fraction=float(state["wet_fraction"]),
            evap_total_g_h=float(state["evap_total_g_h"]),
            mean_body_heat_flux_W_m2=float(state["mean_body_heat_flux_W_m2"]),
            spreader_temperature_range_C=float(state["spreader_temperature_range_C"]),
            outer_temperature_range_C=float(state["outer_temperature_range_C"]),
            max_outer_energy_residual_W_m2=float(state["max_outer_energy_residual_W_m2"]),
            max_spreader_energy_residual_W_m2=float(state["max_spreader_energy_residual_W_m2"]),
            iterations=int(state["iterations"]),
            converged=bool(state["converged"]),
            regime=regime,
        )


def no_lateral_equal_feed_baseline(
    h_contact_W_m2K: float,
    h_dry_W_m2K: float,
    feed_total_g_h: float,
    ambient_c: float = DEFAULT_AMBIENT_C,
    ambient_rh: float = DEFAULT_AMBIENT_RH,
) -> dict[str, float]:
    """Analytic equal-feed baseline with no lateral conduction between patches."""
    c_inf = float(ambient_rh * saturated_vapor_density(ambient_c))

    def spreader_from_outer(outer_c: float) -> float:
        return float((U_BODY * T_SKIN + h_contact_W_m2K * outer_c) / (U_BODY + h_contact_W_m2K))

    def wet_balance(outer_c: float) -> float:
        spreader_c = spreader_from_outer(outer_c)
        evap = KM_WET * max(float(saturated_vapor_density(outer_c) - c_inf), 0.0)
        return (
            h_contact_W_m2K * (spreader_c - outer_c)
            + H_WET * (ambient_c - outer_c)
            - L_V * evap
        )

    wet_outer = brentq(wet_balance, 15.0, 40.0)
    wet_spreader = spreader_from_outer(wet_outer)
    wet_evap = KM_WET * max(float(saturated_vapor_density(wet_outer) - c_inf), 0.0)

    def dry_balance(outer_c: float) -> float:
        spreader_c = spreader_from_outer(outer_c)
        return (
            h_contact_W_m2K * (spreader_c - outer_c)
            + h_dry_W_m2K * (ambient_c - outer_c)
        )

    dry_outer = brentq(dry_balance, 15.0, 45.0)
    dry_spreader = spreader_from_outer(dry_outer)
    feed_flux = (feed_total_g_h / 1000.0 / 3600.0) / STRUCTURED_AREA_M2
    beta = min(feed_flux / wet_evap, 1.0)
    mean_body_flux = (
        beta * U_BODY * (T_SKIN - wet_spreader)
        + (1.0 - beta) * U_BODY * (T_SKIN - dry_spreader)
    )
    return {
        "wet_fraction": float(beta),
        "mean_body_heat_flux_W_m2": float(mean_body_flux),
        "evap_total_g_h": float(min(beta * wet_evap, feed_flux) * STRUCTURED_AREA_M2 * 3.6e6),
    }


def evaluate_virtual_prototype_distributed(
    prototype_name: str,
    feed_total_g_h: float = 100.0,
    n: int = 64,
) -> dict[str, float | str | bool]:
    prototype = next(item for item in PROTOTYPES if item.name == prototype_name)
    # Coverage is homogenized into effective sheet thickness in this bridge model.
    effective_thickness_um = prototype.thickness_um * prototype.coverage
    model = DistributedSpreader1D(
        k_parallel_W_mK=prototype.k_parallel_W_mK,
        effective_thickness_um=effective_thickness_um,
        pitch_mm=prototype.routing_pitch_mm,
        h_contact_W_m2K=prototype.h_contact_W_m2K,
        h_dry_W_m2K=prototype.h_dry_W_m2K,
        n=n,
    )
    result = model.solve_feed(feed_total_g_h)
    baseline = no_lateral_equal_feed_baseline(
        prototype.h_contact_W_m2K,
        prototype.h_dry_W_m2K,
        feed_total_g_h,
    )
    gain_W_m2 = result.mean_body_heat_flux_W_m2 - baseline["mean_body_heat_flux_W_m2"]
    return {
        "classification": "SIMULATION/DISTRIBUTED_SPREADER_1D",
        "prototype": prototype.name,
        "feed_total_g_h": feed_total_g_h,
        "k_parallel_W_mK": prototype.k_parallel_W_mK,
        "effective_sheet_thickness_um": effective_thickness_um,
        "routing_pitch_mm": prototype.routing_pitch_mm,
        "h_contact_W_m2K": prototype.h_contact_W_m2K,
        "h_dry_W_m2K": prototype.h_dry_W_m2K,
        "wet_fraction": result.wet_fraction,
        "evap_total_g_h": result.evap_total_g_h,
        "mean_body_heat_flux_W_m2": result.mean_body_heat_flux_W_m2,
        "no_lateral_body_heat_flux_W_m2": baseline["mean_body_heat_flux_W_m2"],
        "distributed_spreader_gain_W_over_0p195m2": gain_W_m2 * STRUCTURED_AREA_M2,
        "spreader_temperature_range_C": result.spreader_temperature_range_C,
        "outer_temperature_range_C": result.outer_temperature_range_C,
        "max_outer_energy_residual_W_m2": result.max_outer_energy_residual_W_m2,
        "max_spreader_energy_residual_W_m2": result.max_spreader_energy_residual_W_m2,
        "iterations": result.iterations,
        "converged": result.converged,
        "regime": result.regime,
    }


def run_screen(n: int = 64) -> pd.DataFrame:
    return pd.DataFrame(
        [
            evaluate_virtual_prototype_distributed(prototype.name, feed_total_g_h=100.0, n=n)
            for prototype in PROTOTYPES
        ]
    )


if __name__ == "__main__":
    print(run_screen().to_string(index=False))
