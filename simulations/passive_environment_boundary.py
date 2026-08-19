"""Analytic environmental boundary for the same-path heat/vapor baseline.

Under the open-valley screening assumptions, take the same characteristic
external exchange length for sensible heat and water-vapor transfer and the
same screening Nusselt/Sherwood number.  At the point where body-side heat flux
is zero, the wet surface equals the skin-side setpoint:

    T_s = T_skin.

The wet-wall energy balance then reduces to

    (k_air / D_v) * (T_inf - T_skin)
      = L_v * [rho_v,sat(T_skin) - RH_inf * rho_v,sat(T_inf)].

The geometry/transfer multiplier cancels.  The resulting temperature-RH curve
is therefore an **environmental sign boundary inside this low-order linked
heat/mass model**.

Below the boundary the linked model predicts positive body-to-wet-surface heat
flow; above it, ambient sensible heat can dominate and body-side heat flow is
negative even while evaporation remains positive.

This is not a human heat-stress limit, medical threshold, or measured garment
limit.  It is a model boundary for the fixed skin-side temperature and transfer
analogy stated above.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import brentq

try:
    from simulations.passive_rib_screen import D_V, K_AIR, L_V, R_V, T_SKIN, p_sat
except ModuleNotFoundError:
    from passive_rib_screen import D_V, K_AIR, L_V, R_V, T_SKIN, p_sat


def saturated_vapor_density(temp_c: float) -> float:
    return float(p_sat(temp_c) / (R_V * (temp_c + 273.15)))


def boundary_residual(
    ambient_c: float,
    ambient_rh: float,
    skin_c: float = T_SKIN,
) -> float:
    if not 0.0 <= ambient_rh <= 1.0:
        raise ValueError("RH must be between 0 and 1")
    sensible_energy_density = (K_AIR / D_V) * (ambient_c - skin_c)
    latent_energy_density = L_V * (
        saturated_vapor_density(skin_c)
        - ambient_rh * saturated_vapor_density(ambient_c)
    )
    return sensible_energy_density - latent_energy_density


def zero_body_flux_ambient_temperature(
    ambient_rh: float,
    skin_c: float = T_SKIN,
    upper_c: float = 80.0,
) -> float:
    """Ambient dry-bulb temperature at the linked-model zero-body-flux boundary."""
    lower = skin_c
    f_lower = boundary_residual(lower, ambient_rh, skin_c)
    f_upper = boundary_residual(upper_c, ambient_rh, skin_c)
    if f_lower == 0.0:
        return lower
    if f_lower * f_upper > 0.0:
        raise RuntimeError("zero-body-flux boundary not bracketed")
    return float(
        brentq(
            lambda temp: boundary_residual(temp, ambient_rh, skin_c),
            lower,
            upper_c,
            maxiter=100,
        )
    )


def run_screen(skin_c: float = T_SKIN) -> pd.DataFrame:
    rows = []
    for rh in np.arange(0.30, 0.951, 0.05):
        boundary_c = zero_body_flux_ambient_temperature(float(rh), skin_c=skin_c)
        rows.append(
            {
                "classification": "ANALYTIC_MODEL_BOUNDARY",
                "skin_C": skin_c,
                "RH_percent": float(rh * 100.0),
                "zero_body_flux_ambient_C": boundary_c,
                "vapor_density_sat_at_skin_kg_m3": saturated_vapor_density(skin_c),
            }
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(run_screen().to_string(index=False))
