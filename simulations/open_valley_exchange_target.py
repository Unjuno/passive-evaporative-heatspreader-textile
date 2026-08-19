"""Dimensionless lateral ambient-renewal target for an open evaporative valley.

This module does NOT predict an open-valley exchange coefficient from geometry.
Instead it states and inverts a local steady vapor-balance requirement.

Let

    G_w = k_w P_w

be the effective vapor conductance from wet surface to local valley air, and

    G_a = k_a P_a

be the effective conductance from local valley air to refreshed ambient air.
Define

    R = G_a / G_w.

For local steady balance

    G_w (C_sat - C) = G_a (C - C_inf),

the fraction of the full ambient-to-saturated-wall vapor driving force retained
at the wet wall is

    F = (C_sat - C)/(C_sat - C_inf) = R/(1+R).

The normalized valley vapor loading is

    theta = (C - C_inf)/(C_sat - C_inf) = 1/(1+R).

Therefore

    R = F/(1-F) = (1-theta)/theta.

This is a threshold/identification model, not CFD and not a garment cooling
prediction.  Its main use is to translate measured local T/RH into an inferred
renewal-to-wet conductance ratio and to state how large that ratio must be to
retain a chosen fraction of the vapor driving force.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

try:
    from simulations.passive_rib_screen import R_V, p_sat
except ModuleNotFoundError:  # direct execution
    from passive_rib_screen import R_V, p_sat


def retention_from_ratio(ratio: float) -> float:
    """Return F = R/(1+R)."""
    if ratio < 0.0:
        raise ValueError("ratio must be nonnegative")
    return float(ratio / (1.0 + ratio))


def loading_from_ratio(ratio: float) -> float:
    """Return theta = 1/(1+R)."""
    if ratio < 0.0:
        raise ValueError("ratio must be nonnegative")
    return float(1.0 / (1.0 + ratio))


def required_ratio(retention: float) -> float:
    """Return R required for a target 0<=F<1."""
    if not 0.0 <= retention < 1.0:
        raise ValueError("retention must satisfy 0 <= F < 1")
    if retention == 1.0:
        return np.inf
    return float(retention / (1.0 - retention))


def vapor_density(temp_c: float, rh: float) -> float:
    """Water-vapor density [kg/m^3] from dry-bulb T and RH."""
    if not 0.0 <= rh <= 1.0:
        raise ValueError("RH must be between 0 and 1")
    return float(rh * p_sat(temp_c) / (R_V * (temp_c + 273.15)))


def saturated_vapor_density(temp_c: float) -> float:
    return vapor_density(temp_c, 1.0)


def infer_from_measurement(
    ambient_c: float,
    ambient_rh: float,
    surface_c: float,
    valley_c: float,
    valley_rh: float,
) -> dict[str, float | str]:
    """Infer normalized loading, retained driving force, and R from measured T/RH.

    The identification is valid only when the measured valley vapor density lies
    between ambient vapor density and saturated vapor density at the wet-surface
    temperature.  Values outside that interval are returned with status
    ``outside-local-balance-range`` rather than silently clipped.
    """
    c_inf = vapor_density(ambient_c, ambient_rh)
    c_sat = saturated_vapor_density(surface_c)
    c_valley = vapor_density(valley_c, valley_rh)
    denominator = c_sat - c_inf
    if denominator <= 0.0:
        return {
            "status": "no-positive-vapor-driving-force",
            "theta": np.nan,
            "retention_F": np.nan,
            "R": np.nan,
            "ambient_vapor_density_kg_m3": c_inf,
            "surface_saturated_vapor_density_kg_m3": c_sat,
            "valley_vapor_density_kg_m3": c_valley,
        }

    theta = (c_valley - c_inf) / denominator
    if not 0.0 < theta < 1.0:
        return {
            "status": "outside-local-balance-range",
            "theta": float(theta),
            "retention_F": float(1.0 - theta),
            "R": np.nan,
            "ambient_vapor_density_kg_m3": c_inf,
            "surface_saturated_vapor_density_kg_m3": c_sat,
            "valley_vapor_density_kg_m3": c_valley,
        }

    return {
        "status": "identified",
        "theta": float(theta),
        "retention_F": float(1.0 - theta),
        "R": float((1.0 - theta) / theta),
        "ambient_vapor_density_kg_m3": c_inf,
        "surface_saturated_vapor_density_kg_m3": c_sat,
        "valley_vapor_density_kg_m3": c_valley,
    }


def target_table() -> pd.DataFrame:
    rows = []
    for retention in (0.50, 0.67, 0.80, 0.90, 0.95):
        rows.append(
            {
                "classification": "SIMULATION/ANALYTIC_TARGET",
                "target_driving_force_retention_F": retention,
                "required_renewal_to_wet_conductance_ratio_R": required_ratio(retention),
                "normalized_valley_vapor_loading_theta": 1.0 - retention,
            }
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(target_table().to_string(index=False))
