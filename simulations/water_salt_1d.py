"""Normalized 1D water/salt transport screen.

Purpose
-------
Estimate whether distributed water evaporation along an internal liquid path is
large enough to concentrate a nonvolatile salt surrogate to saturation before
the intended terminal evaporator.

This intentionally avoids choosing a specific salt solubility. Concentration is
normalized by the relevant saturation concentration:

    c = C / C_sat

Assumptions
-----------
- steady through-flow;
- inlet water flow W0 is normalized to 1;
- inlet dissolved-salt inventory S0 = c0 in the same normalized basis;
- water can evaporate along the internal path;
- salt vapor flux is exactly zero;
- salt precipitates locally once dissolved concentration would exceed c=1;
- no redissolution kinetics, dispersion, pore blockage, or activity correction;
- remaining liquid reaches a terminal evaporator where its dissolved salt can
  ultimately deposit/be washed out.

This is a conservative bookkeeping model, not a crystallization-kinetics model.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class SaltPathResult:
    x_fraction: np.ndarray
    water_flow_fraction: np.ndarray
    dissolved_salt_flow_norm: np.ndarray
    solid_salt_deposited_norm: np.ndarray
    concentration_over_csat: np.ndarray
    inlet_concentration_over_csat: float
    internal_evaporation_fraction: float
    precipitation_onset_x_fraction: float | None
    upstream_salt_deposition_fraction: float
    terminal_salt_fraction: float


def solve_normalized_path(
    inlet_concentration_over_csat: float,
    internal_evaporation_fraction: float,
    n_points: int = 501,
) -> SaltPathResult:
    """Solve a uniform distributed-leak path in normalized mass coordinates.

    `internal_evaporation_fraction` is the fraction of inlet liquid water lost
    by evaporation before the terminal evaporator. It must be in [0, 1).
    """
    c0 = float(inlet_concentration_over_csat)
    leak = float(internal_evaporation_fraction)
    if not (0.0 < c0 <= 1.0):
        raise ValueError("inlet concentration ratio must be in (0, 1]")
    if not (0.0 <= leak < 1.0):
        raise ValueError("internal evaporation fraction must be in [0, 1)")
    if n_points < 2:
        raise ValueError("n_points must be >= 2")

    x = np.linspace(0.0, 1.0, n_points)
    water = 1.0 - leak * x
    salt_total = c0

    # Dissolved salt cannot exceed the normalized solubility capacity of the
    # remaining liquid: S_dissolved <= C_sat * W. With C_sat normalized to 1,
    # the capacity equals the remaining normalized water flow W.
    dissolved = np.minimum(salt_total, water)
    solid = salt_total - dissolved
    concentration = dissolved / water

    precip_indices = np.where(solid > 1e-12)[0]
    onset = None if precip_indices.size == 0 else float(x[precip_indices[0]])

    upstream_solid = float(solid[-1])
    upstream_fraction = upstream_solid / salt_total
    terminal_fraction = float(dissolved[-1] / salt_total)

    # Conservation check: all inlet salt is either upstream solid or reaches
    # the terminal in dissolved form.
    if not np.isclose(upstream_fraction + terminal_fraction, 1.0, atol=1e-10):
        raise RuntimeError("salt mass balance failed")

    return SaltPathResult(
        x_fraction=x,
        water_flow_fraction=water,
        dissolved_salt_flow_norm=dissolved,
        solid_salt_deposited_norm=solid,
        concentration_over_csat=concentration,
        inlet_concentration_over_csat=c0,
        internal_evaporation_fraction=leak,
        precipitation_onset_x_fraction=onset,
        upstream_salt_deposition_fraction=upstream_fraction,
        terminal_salt_fraction=terminal_fraction,
    )


def analytic_precipitation_leak_threshold(inlet_concentration_over_csat: float) -> float:
    """Minimum total internal water-loss fraction that reaches saturation.

    For W0=1 and conserved dissolved salt S0=c0, saturation first becomes
    possible when remaining water W <= c0, so leak >= 1-c0.
    """
    c0 = float(inlet_concentration_over_csat)
    if not (0.0 < c0 <= 1.0):
        raise ValueError("inlet concentration ratio must be in (0, 1]")
    return 1.0 - c0


def run_parameter_screen() -> pd.DataFrame:
    rows: list[dict[str, float | None]] = []
    for c0 in (0.05, 0.10, 0.20, 0.40, 0.60, 0.80):
        threshold = analytic_precipitation_leak_threshold(c0)
        for leak in (0.01, 0.05, 0.10, 0.20, 0.40, 0.60, 0.80, 0.90, 0.95):
            result = solve_normalized_path(c0, leak)
            rows.append(
                {
                    "inlet_C_over_Csat": c0,
                    "internal_evap_fraction": leak,
                    "analytic_onset_leak_fraction": threshold,
                    "precipitation_onset_x_fraction": result.precipitation_onset_x_fraction,
                    "upstream_salt_deposition_fraction": result.upstream_salt_deposition_fraction,
                    "terminal_salt_fraction": result.terminal_salt_fraction,
                    "outlet_C_over_Csat": float(result.concentration_over_csat[-1]),
                }
            )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    screen = run_parameter_screen()
    print(screen.to_string(index=False))
