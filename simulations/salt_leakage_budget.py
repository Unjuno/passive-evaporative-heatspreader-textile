"""Normalized nonvolatile-salt mass balance for upstream water leakage.

Salt vapor flux is identically zero. Upstream evaporation removes water only,
so a conserved dissolved-salt flux becomes more concentrated. The model tracks
bulk concentration relative to an arbitrary saturation concentration and does
not model local wall-film dryout or nucleation.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

SALT_VAPOR_FLUX = 0.0


def concentration_multiplier(water_leak_fraction: float) -> float:
    f = float(water_leak_fraction)
    if not 0.0 <= f < 1.0:
        raise ValueError("water_leak_fraction must be in [0,1)")
    return 1.0 / (1.0 - f)


def outlet_saturation_ratio(inlet_saturation_ratio: float, water_leak_fraction: float) -> float:
    return float(inlet_saturation_ratio) * concentration_multiplier(water_leak_fraction)


def critical_leak_fraction_to_bulk_saturation(inlet_saturation_ratio: float) -> float:
    sigma0 = float(inlet_saturation_ratio)
    if not 0.0 < sigma0 <= 1.0:
        raise ValueError("inlet_saturation_ratio must be in (0,1]")
    return 1.0 - sigma0


def run_salt_leakage_screen(
    inlet_saturation_ratios=(0.005, 0.01, 0.02, 0.05, 0.10, 0.20, 0.50),
    leak_fractions=None,
):
    if leak_fractions is None:
        leak_fractions = np.linspace(0.0, 0.99, 200)
    rows = []
    for sigma0 in inlet_saturation_ratios:
        for leak in leak_fractions:
            sigma = outlet_saturation_ratio(sigma0, leak)
            rows.append({
                "inlet_saturation_ratio_sigma0": sigma0,
                "water_leak_fraction": leak,
                "water_remaining_fraction": 1.0 - leak,
                "bulk_salt_saturation_ratio": sigma,
                "bulk_precipitation_expected": sigma >= 1.0,
                "salt_vapor_flux": SALT_VAPOR_FLUX,
            })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(run_salt_leakage_screen().to_csv(index=False))
