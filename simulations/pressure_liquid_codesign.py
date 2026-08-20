"""Pressure-aware wet-terminal thermal/liquid co-design screen.

Virtual/computational screen only. This module combines the converged terminal
regularization sweep with a first-order protected-trunk hydraulic burden proxy.
It does not claim measured garment performance or a geometry-resolved liquid
network solution.

The hydraulic proxy uses the laminar r^-4 sensitivity as a deliberately simple
penalty on the geometric p95 terminal distance. A radius-retention floor models
a mechanically protected escape trunk. The purpose is to prevent a pure
thermal optimum from silently creating unnecessarily long liquid routes.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from simulations.terminal_route_coddesign import sweep_regularization


def add_hydraulic_proxy(
    table: pd.DataFrame,
    radius_retention_floor: float = 0.90,
) -> pd.DataFrame:
    """Add first-order protected-trunk hydraulic burden columns.

    Parameters
    ----------
    table:
        Output from ``sweep_regularization``. Must contain ``liquid_p95_mm``
        and ``load_weighted_heat_rms_mm``.
    radius_retention_floor:
        Minimum equivalent liquid-channel radius divided by the uncompressed
        radius. The proxy scales resistance with ``radius_retention_floor**-4``.
    """
    retention = float(radius_retention_floor)
    if not (0.0 < retention <= 1.0):
        raise ValueError("radius_retention_floor must satisfy 0 < r_hat <= 1")

    out = table.copy()
    multiplier = retention ** -4
    out["radius_retention_floor"] = retention
    out["hydraulic_resistance_multiplier"] = multiplier
    out["hydraulic_p95_proxy_mm_eq"] = out["liquid_p95_mm"] * multiplier
    out["hydraulic_rms_proxy_mm_eq"] = (
        out["load_weighted_heat_rms_mm"] * multiplier
    )
    return out


def mark_thermal_hydraulic_pareto(table: pd.DataFrame) -> pd.DataFrame:
    """Mark non-dominated rows: maximize body heat flux, minimize hydraulic p95."""
    out = table.copy()
    flags = []
    for _, row in out.iterrows():
        dominated = (
            (out["body_W_m2"] >= row["body_W_m2"])
            & (
                out["hydraulic_p95_proxy_mm_eq"]
                <= row["hydraulic_p95_proxy_mm_eq"]
            )
            & (
                (out["body_W_m2"] > row["body_W_m2"])
                | (
                    out["hydraulic_p95_proxy_mm_eq"]
                    < row["hydraulic_p95_proxy_mm_eq"]
                )
            )
        ).any()
        flags.append(not dominated)
    out["pareto_thermal_hydraulic"] = flags
    return out


def select_codesign_anchor(
    n: int = 12,
    minimum_thermal_retention: float = 0.98,
    radius_retention_floor: float = 0.90,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Select a short-route candidate while retaining a fraction of thermal best.

    The returned summary contains a pure-thermal optimum and a co-design anchor.
    The anchor is the row with minimum hydraulic p95 among all converged rows
    whose body-side heat flux is at least ``minimum_thermal_retention`` times
    the thermal optimum.
    """
    keep = float(minimum_thermal_retention)
    if not (0.0 < keep <= 1.0):
        raise ValueError("minimum_thermal_retention must satisfy 0 < f <= 1")

    table = sweep_regularization(n=n)
    table = table[table["converged"]].copy()
    if table.empty:
        raise RuntimeError("regularization sweep returned no converged rows")

    table = add_hydraulic_proxy(table, radius_retention_floor)
    table = mark_thermal_hydraulic_pareto(table)

    thermal_index = table["body_W_m2"].idxmax()
    thermal_best = table.loc[thermal_index]
    q_best = float(thermal_best["body_W_m2"])

    near = table[table["body_W_m2"] >= keep * q_best].copy()
    anchor_index = near.sort_values(
        [
            "hydraulic_p95_proxy_mm_eq",
            "load_weighted_heat_rms_mm",
            "mean_pressure_on_wet",
        ]
    ).index[0]
    anchor = table.loc[anchor_index]

    summary = pd.DataFrame(
        [
            {
                "candidate": "thermal_only_best",
                "template_weight_beta": thermal_best["template_weight"],
                "route_weight": thermal_best["route_weight"],
                "body_W_m2": thermal_best["body_W_m2"],
                "liquid_p95_mm": thermal_best["liquid_p95_mm"],
                "hydraulic_p95_proxy_mm_eq": thermal_best[
                    "hydraulic_p95_proxy_mm_eq"
                ],
                "mean_pressure_wet": thermal_best["mean_pressure_on_wet"],
            },
            {
                "candidate": "codesign_anchor",
                "template_weight_beta": anchor["template_weight"],
                "route_weight": anchor["route_weight"],
                "body_W_m2": anchor["body_W_m2"],
                "liquid_p95_mm": anchor["liquid_p95_mm"],
                "hydraulic_p95_proxy_mm_eq": anchor[
                    "hydraulic_p95_proxy_mm_eq"
                ],
                "mean_pressure_wet": anchor["mean_pressure_on_wet"],
            },
        ]
    )
    summary["thermal_retention_percent"] = (
        100.0 * summary["body_W_m2"] / q_best
    )
    h_best = float(thermal_best["hydraulic_p95_proxy_mm_eq"])
    summary["hydraulic_reduction_percent_vs_thermal_best"] = 100.0 * (
        1.0 - summary["hydraulic_p95_proxy_mm_eq"] / h_best
    )
    return summary, table


def weighted_codesign_selection(
    table: pd.DataFrame,
    thermal_weight: float,
) -> pd.Series:
    """Select one row using normalized thermal-loss / hydraulic-penalty weights."""
    alpha = float(thermal_weight)
    if not (0.0 <= alpha <= 1.0):
        raise ValueError("thermal_weight must satisfy 0 <= alpha <= 1")

    q_best = float(table["body_W_m2"].max())
    h_best = float(table["hydraulic_p95_proxy_mm_eq"].min())
    thermal_loss = (q_best - table["body_W_m2"]) / q_best
    hydraulic_penalty = table["hydraulic_p95_proxy_mm_eq"] / h_best - 1.0
    objective = alpha * thermal_loss + (1.0 - alpha) * hydraulic_penalty
    return table.loc[objective.idxmin()]


if __name__ == "__main__":
    summary, table = select_codesign_anchor(n=24)
    print(summary.to_csv(index=False))
    print(
        table[table["pareto_thermal_hydraulic"]]
        .sort_values("body_W_m2", ascending=False)
        .to_csv(index=False)
    )
