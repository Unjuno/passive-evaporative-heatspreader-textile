"""Low-order moist-air buoyancy screen for vertical macro corridors.

Purpose
-------
Investigate whether a vertical open corridor in the hierarchical exterior could
support passive air renewal, and whether thermo-solutal effects can reverse the
flow direction.

The model treats a wide slot of gap ``b`` with a prescribed mean channel-air
state. Hydrostatic density head is balanced by fully developed laminar
parallel-plate friction:

    dp/dz ~= g (rho_inf - rho_ch)
    u_bar ~= b^2 / (12 mu) * dp/dz

This is a screening relation, not CFD. It ignores entrance losses, open-end
mixing, garment curvature, wind, body motion, turbulence, and self-consistent
coupling between evaporation and the channel-air state.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

try:
    from simulations.passive_rib_screen import (
        D_V,
        G,
        P_ATM,
        R_D,
        R_V,
        p_sat,
    )
except ModuleNotFoundError:  # direct execution
    from passive_rib_screen import D_V, G, P_ATM, R_D, R_V, p_sat

MU_AIR = 1.90e-5  # Pa s, fixed screening value


def moist_air_density(temp_c: float, rh: float) -> float:
    """Ideal-mixture moist-air density [kg/m^3]."""
    if not 0.0 <= rh <= 1.0:
        raise ValueError("RH must be between 0 and 1")
    pv = rh * float(p_sat(temp_c))
    pd = P_ATM - pv
    tk = temp_c + 273.15
    return pd / (R_D * tk) + pv / (R_V * tk)


def slot_velocity(
    gap_mm: float,
    ambient_c: float,
    ambient_rh: float,
    channel_c: float,
    channel_rh: float,
    mu: float = MU_AIR,
) -> float:
    """Signed mean slot velocity [m/s].

    Positive means the prescribed channel air is lighter than ambient and the
    idealized vertical channel tends upward. Negative means downward tendency.
    """
    if gap_mm <= 0.0:
        raise ValueError("gap must be positive")
    b = gap_mm * 1e-3
    rho_inf = moist_air_density(ambient_c, ambient_rh)
    rho_ch = moist_air_density(channel_c, channel_rh)
    pressure_gradient = G * (rho_inf - rho_ch)  # Pa/m
    return b * b * pressure_gradient / (12.0 * mu)


def corridor_case(
    gap_mm: float,
    height_mm: float,
    ambient_c: float,
    ambient_rh: float,
    channel_c: float,
    channel_rh: float,
) -> dict[str, float | str]:
    """Return velocity and screening dimensionless groups for one corridor."""
    if height_mm <= 0.0:
        raise ValueError("height must be positive")

    u = slot_velocity(gap_mm, ambient_c, ambient_rh, channel_c, channel_rh)
    rho_ch = moist_air_density(channel_c, channel_rh)
    gap_m = gap_mm * 1e-3
    height_m = height_mm * 1e-3
    hydraulic_diameter = 2.0 * gap_m
    re = rho_ch * abs(u) * hydraulic_diameter / MU_AIR
    pe_height = abs(u) * height_m / D_V
    residence = np.inf if abs(u) < 1e-12 else height_m / abs(u)

    if u > 1e-6:
        direction = "up"
    elif u < -1e-6:
        direction = "down"
    else:
        direction = "near-neutral"

    return {
        "gap_mm": gap_mm,
        "height_mm": height_mm,
        "ambient_C": ambient_c,
        "ambient_RH": ambient_rh,
        "channel_C": channel_c,
        "channel_RH": channel_rh,
        "rho_ambient_kg_m3": moist_air_density(ambient_c, ambient_rh),
        "rho_channel_kg_m3": rho_ch,
        "velocity_m_s": u,
        "direction": direction,
        "Re_Dh": re,
        "Pe_mass_height": pe_height,
        "idealized_residence_s": residence,
    }


def neutral_rh(
    channel_c: float,
    ambient_c: float = 35.0,
    ambient_rh: float = 0.70,
) -> float | None:
    """RH at which prescribed channel air has the same density as ambient.

    Returns None when equality is outside RH=[0,1].
    """
    target = moist_air_density(ambient_c, ambient_rh)
    rho0 = moist_air_density(channel_c, 0.0)
    rho1 = moist_air_density(channel_c, 1.0)
    if not (min(rho0, rho1) <= target <= max(rho0, rho1)):
        return None

    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        rho_mid = moist_air_density(channel_c, mid)
        # Increasing RH lowers moist-air density at fixed T.
        if rho_mid > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def run_screen() -> pd.DataFrame:
    """Generate a small corridor design/state matrix."""
    rows = []
    for gap_mm in (0.5, 1.0, 2.0, 3.0, 5.0):
        for height_mm in (20.0, 50.0, 100.0):
            for channel_c, channel_rh in (
                (32.0, 1.00),
                (33.5, 1.00),
                (34.0, 0.80),
                (34.0, 0.90),
                (34.0, 1.00),
            ):
                rows.append(
                    corridor_case(
                        gap_mm,
                        height_mm,
                        ambient_c=35.0,
                        ambient_rh=0.70,
                        channel_c=channel_c,
                        channel_rh=channel_rh,
                    )
                )
    return pd.DataFrame(rows)


def neutral_curve() -> pd.DataFrame:
    rows = []
    for temp_c in np.arange(30.0, 35.01, 0.25):
        rh = neutral_rh(float(temp_c))
        rows.append({"channel_C": temp_c, "neutral_RH": rh})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print("Corridor cases:")
    print(run_screen().to_string(index=False))
    print("\nNeutral-density curve (35 C / 70% RH ambient):")
    print(neutral_curve().dropna().to_string(index=False))
