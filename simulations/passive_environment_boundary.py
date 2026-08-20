"""Analytic environmental boundary for the same-path heat/vapor baseline.

At zero body-side heat flux the wet surface equals the controlled skin-side
setpoint.  With the same characteristic exchange length and the same screening
Nu/Sh for heat and vapor, the transfer factor cancels:

    (k_air / D_v) * (T_inf - T_skin)
      = L_v * [rho_v,sat(T_skin) - RH_inf * rho_v,sat(T_inf)].

The resulting curve is a model sign boundary, not a human safety threshold or a
measured garment limit.  Skin/artificial-skin temperature is explicit because
the boundary moves materially with that setpoint.
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


def run_skin_sensitivity() -> pd.DataFrame:
    rows = []
    for skin_c in (32.0, 33.0, 34.0, 35.0, 36.0):
        for rh in (0.50, 0.70, 0.85, 0.90):
            rows.append(
                {
                    "classification": "ANALYTIC_MODEL_BOUNDARY_SENSITIVITY",
                    "skin_C": skin_c,
                    "RH_percent": rh * 100.0,
                    "zero_body_flux_ambient_C": zero_body_flux_ambient_temperature(
                        rh, skin_c=skin_c
                    ),
                }
            )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print("Default skin-temperature boundary:")
    print(run_screen().to_string(index=False))
    print("\nSkin-temperature sensitivity:")
    print(run_skin_sensitivity().to_string(index=False))
