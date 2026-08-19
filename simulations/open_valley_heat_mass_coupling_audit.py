"""Audit heat/mass coupling in the open-valley thermal model.

The thermal screen allows independent effective lateral exchange lengths
``delta_vapor`` and ``delta_heat``.  This module quantifies departure from
ordinary same-boundary heat/mass coupling and solves the hot-ambient body-heat
flow sign boundary.

For

    h_a  = k_air / delta_heat
    k_ma = D_v   / delta_vapor

we define

    Le  = k_air / (rho cp D_v)
    chi = h_a / (rho cp k_ma)
        = Le * delta_vapor / delta_heat
    Xi  = chi / Le
        = delta_vapor / delta_heat.

``Xi=1`` is the same-exchange-length conduction/diffusion baseline.

For an equal-j-factor Chilton-Colburn-style comparison,

    h/(rho cp k_m) ~ Le^(2/3),

so the equivalent exchange-length ratio in this parameterization is

    Xi_CC = Le^(-1/3).

These are comparison baselines, not validated textile correlations.  They are
used to show whether a required hot-ambient heat/mass selectivity is close to
ordinary same-boundary transport or would require a distinct physical
mechanism such as thermal shielding, geometry-dependent contact, radiation
control, or separated heat/vapor pathways.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import brentq

try:
    from simulations.open_valley_thermal_1d import CP_AIR, solve_open_valley_thermal
    from simulations.passive_rib_screen import D_V, K_AIR, P_ATM, R_D, R_V, p_sat
except ModuleNotFoundError:
    from open_valley_thermal_1d import CP_AIR, solve_open_valley_thermal
    from passive_rib_screen import D_V, K_AIR, P_ATM, R_D, R_V, p_sat


def ambient_density(temp_c: float, rh: float) -> float:
    pv = rh * float(p_sat(temp_c))
    pd = P_ATM - pv
    tk = temp_c + 273.15
    return float(pd / (R_D * tk) + pv / (R_V * tk))


def lewis_number(temp_c: float, rh: float) -> float:
    rho = ambient_density(temp_c, rh)
    alpha = K_AIR / (rho * CP_AIR)
    return float(alpha / D_V)


def chilton_colburn_xi(temp_c: float, rh: float) -> float:
    """Equivalent Xi for an equal-j-factor heat/mass analogy comparison."""
    le = lewis_number(temp_c, rh)
    return float(le ** (-1.0 / 3.0))


def coupling_metrics(
    delta_vapor_mm: float,
    delta_heat_mm: float,
    ambient_c: float = 35.0,
    ambient_rh: float = 0.70,
) -> dict[str, float]:
    if delta_vapor_mm <= 0.0 or delta_heat_mm <= 0.0:
        raise ValueError("exchange distances must be positive")
    le = lewis_number(ambient_c, ambient_rh)
    xi = delta_vapor_mm / delta_heat_mm
    return {
        "Lewis_number": le,
        "Xi_delta_vapor_over_delta_heat": xi,
        "chi_h_over_rhocp_km": le * xi,
        "same_length_Xi": 1.0,
        "same_length_chi": le,
        "chilton_colburn_Xi": le ** (-1.0 / 3.0),
        "chilton_colburn_chi": le ** (2.0 / 3.0),
    }


def zero_body_flux_threshold(
    delta_vapor_mm: float,
    ambient_c: float = 40.0,
    ambient_rh: float = 0.70,
    min_delta_heat_mm: float = 0.05,
    max_delta_heat_mm: float = 10.0,
) -> dict[str, float | bool]:
    """Solve the effective heat-exchange distance at zero mean body heat flux."""
    if delta_vapor_mm <= 0.0:
        raise ValueError("delta_vapor must be positive")

    def body_flux(log_delta_heat: float) -> float:
        delta_heat = 10.0 ** log_delta_heat
        return solve_open_valley_thermal(
            ambient_c=ambient_c,
            ambient_rh=ambient_rh,
            delta_vapor_mm=delta_vapor_mm,
            delta_heat_mm=delta_heat,
        ).mean_body_heat_flux_W_m2

    lo = np.log10(min_delta_heat_mm)
    hi = np.log10(max_delta_heat_mm)
    flo = body_flux(lo)
    fhi = body_flux(hi)

    bracket: tuple[float, float] | None = None
    if flo * fhi <= 0.0:
        bracket = (lo, hi)
    else:
        scan = np.linspace(lo, hi, 16)
        values = np.array([body_flux(x) for x in scan])
        indices = np.where(values[:-1] * values[1:] <= 0.0)[0]
        if len(indices):
            idx = int(indices[0])
            bracket = (float(scan[idx]), float(scan[idx + 1]))

    if bracket is None:
        return {
            "found_zero_crossing": False,
            "delta_vapor_mm": delta_vapor_mm,
            "critical_delta_heat_mm": np.nan,
            "critical_Xi": np.nan,
            "evap_at_zero_body_flux_g_m2_h": np.nan,
        }

    root = brentq(body_flux, bracket[0], bracket[1], maxiter=60)
    critical_delta_heat = 10.0 ** root
    result = solve_open_valley_thermal(
        ambient_c=ambient_c,
        ambient_rh=ambient_rh,
        delta_vapor_mm=delta_vapor_mm,
        delta_heat_mm=critical_delta_heat,
    )
    return {
        "found_zero_crossing": True,
        "delta_vapor_mm": delta_vapor_mm,
        "critical_delta_heat_mm": critical_delta_heat,
        "critical_Xi": delta_vapor_mm / critical_delta_heat,
        "evap_at_zero_body_flux_g_m2_h": result.mean_evap_flux_g_m2_h,
    }


def run_screen() -> pd.DataFrame:
    rows = []
    ambient_c = 40.0
    ambient_rh = 0.70
    cc_xi = chilton_colburn_xi(ambient_c, ambient_rh)

    for delta_vapor in (0.10, 0.25, 0.50, 1.0, 2.0):
        threshold = zero_body_flux_threshold(
            delta_vapor,
            ambient_c=ambient_c,
            ambient_rh=ambient_rh,
        )
        if threshold["found_zero_crossing"]:
            metrics = coupling_metrics(
                delta_vapor,
                float(threshold["critical_delta_heat_mm"]),
                ambient_c=ambient_c,
                ambient_rh=ambient_rh,
            )
            critical_xi = float(threshold["critical_Xi"])
            same_length_meets = 1.0 <= critical_xi
            cc_meets = cc_xi <= critical_xi
        else:
            le = lewis_number(ambient_c, ambient_rh)
            metrics = {
                "Lewis_number": le,
                "Xi_delta_vapor_over_delta_heat": np.nan,
                "chi_h_over_rhocp_km": np.nan,
                "same_length_Xi": 1.0,
                "same_length_chi": le,
                "chilton_colburn_Xi": cc_xi,
                "chilton_colburn_chi": le ** (2.0 / 3.0),
            }
            critical_xi = np.nan
            same_length_meets = False
            cc_meets = False

        rows.append(
            {
                "classification": "SIMULATION/COUPLING_AUDIT",
                "ambient_C": ambient_c,
                "ambient_RH": ambient_rh,
                **threshold,
                **metrics,
                "same_length_meets_required_selectivity": same_length_meets,
                "chilton_colburn_meets_required_selectivity": cc_meets,
                "critical_Xi_over_chilton_colburn_Xi": (
                    critical_xi / cc_xi if np.isfinite(critical_xi) else np.nan
                ),
            }
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(run_screen().to_string(index=False))