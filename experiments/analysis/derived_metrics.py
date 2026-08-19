"""Derived metrics for future physical experiment data.

This module contains only deterministic transformations of measured quantities.
It does not fabricate missing measurements or convert model capacity into
physical performance.

Sign convention used by the experiment schema:
    q_body > 0  heat leaves artificial skin (cooling direction)
    q_body < 0  heat enters artificial skin (body-heating direction)
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

R_V = 461.5  # J/(kg K), consistent with repository screening models


def saturation_pressure_pa(temp_c: float | np.ndarray) -> float | np.ndarray:
    temp = np.asarray(temp_c, dtype=float)
    return 611.21 * np.exp((18.678 - temp / 234.5) * (temp / (257.14 + temp)))


def vapor_density_kg_m3(temp_c: float | np.ndarray, rh_fraction: float | np.ndarray) -> np.ndarray:
    temp = np.asarray(temp_c, dtype=float)
    rh = np.asarray(rh_fraction, dtype=float)
    if np.any((rh < 0.0) | (rh > 1.0)):
        raise ValueError("RH fraction must lie within [0,1]")
    return rh * saturation_pressure_pa(temp) / (R_V * (temp + 273.15))


def saturated_vapor_density_kg_m3(temp_c: float | np.ndarray) -> np.ndarray:
    temp = np.asarray(temp_c, dtype=float)
    return saturation_pressure_pa(temp) / (R_V * (temp + 273.15))


def renewal_metrics(
    ambient_temp_c: float | np.ndarray,
    ambient_rh_fraction: float | np.ndarray,
    local_temp_c: float | np.ndarray,
    local_rh_fraction: float | np.ndarray,
    wet_surface_temp_c: float | np.ndarray,
) -> dict[str, np.ndarray]:
    """Calculate temperature-corrected local vapor loading and F.

    theta = (rho_v,local - rho_v,ambient) /
            (rho_v,sat(T_surface) - rho_v,ambient)
    F = 1 - theta

    Values outside [0,1] are retained rather than silently clipped because they
    may reveal condensation, measurement error, non-saturated wet surfaces, or
    violation of the assumed local model.
    """
    c_inf = vapor_density_kg_m3(ambient_temp_c, ambient_rh_fraction)
    c_local = vapor_density_kg_m3(local_temp_c, local_rh_fraction)
    c_sat = saturated_vapor_density_kg_m3(wet_surface_temp_c)
    denominator = c_sat - c_inf
    if np.any(denominator <= 0.0):
        raise ValueError(
            "non-positive saturated-wall minus ambient vapor-density driving force"
        )
    theta = (c_local - c_inf) / denominator
    f = 1.0 - theta
    with np.errstate(divide="ignore", invalid="ignore"):
        r = f / (1.0 - f)
    return {
        "rho_v_ambient_kg_m3": c_inf,
        "rho_v_local_kg_m3": c_local,
        "rho_v_sat_surface_kg_m3": c_sat,
        "theta": theta,
        "F": f,
        "R_inferred": r,
    }


def effective_vapor_conductance_m_s(
    evaporation_flux_kg_m2_s: float | np.ndarray,
    ambient_temp_c: float | np.ndarray,
    ambient_rh_fraction: float | np.ndarray,
    wet_surface_temp_c: float | np.ndarray,
) -> np.ndarray:
    """Infer k_eff from measured evaporation flux and bulk vapor driving force."""
    flux = np.asarray(evaporation_flux_kg_m2_s, dtype=float)
    c_inf = vapor_density_kg_m3(ambient_temp_c, ambient_rh_fraction)
    c_sat = saturated_vapor_density_kg_m3(wet_surface_temp_c)
    driving = c_sat - c_inf
    if np.any(driving <= 0.0):
        raise ValueError("non-positive bulk vapor-density driving force")
    return flux / driving


def heat_flow_classification(body_heat_flux_w_m2: float) -> str:
    if body_heat_flux_w_m2 > 0.0:
        return "body-cooling-direction"
    if body_heat_flux_w_m2 < 0.0:
        return "body-heating-direction"
    return "zero-within-numeric-input"


def evaporation_heat_classification(
    body_heat_flux_w_m2: float,
    evaporation_flux_kg_m2_s: float,
) -> str:
    if evaporation_flux_kg_m2_s > 0.0 and body_heat_flux_w_m2 < 0.0:
        return "evaporating/body-heating"
    if evaporation_flux_kg_m2_s > 0.0 and body_heat_flux_w_m2 > 0.0:
        return "evaporating/body-cooling"
    if evaporation_flux_kg_m2_s <= 0.0 and body_heat_flux_w_m2 < 0.0:
        return "non-evaporating/body-heating"
    return "non-evaporating-or-zero/body-cooling-or-zero"


@dataclass(frozen=True)
class WaterBalanceResult:
    feed_g: float
    runoff_g: float
    sample_mass_change_g: float
    independently_measured_evap_g: float
    unaccounted_g: float
    closure_fraction: float


def water_balance_with_independent_evaporation(
    feed_g: float,
    runoff_g: float,
    sample_mass_change_g: float,
    independently_measured_evap_g: float,
) -> WaterBalanceResult:
    """Close a water balance only when evaporation is independently measured.

    This function intentionally does not set evaporation equal to the residual;
    doing that would make closure tautological and hide measurement error.
    """
    if feed_g <= 0.0:
        raise ValueError("feed mass must be positive")
    unaccounted = (
        feed_g - runoff_g - sample_mass_change_g - independently_measured_evap_g
    )
    closure = 1.0 - abs(unaccounted) / feed_g
    return WaterBalanceResult(
        feed_g=feed_g,
        runoff_g=runoff_g,
        sample_mass_change_g=sample_mass_change_g,
        independently_measured_evap_g=independently_measured_evap_g,
        unaccounted_g=unaccounted,
        closure_fraction=closure,
    )
