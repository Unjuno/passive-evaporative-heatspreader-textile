"""Map abstract wet/dry heat-spreader conductance to sheet geometry and contacts.

The asymmetric wet/dry screen uses an areal lateral mixing conductance
``g_mix`` [W/(m² K)]. This module translates that mechanism parameter into a
low-order periodic-stripe sheet requirement.

For a repeating wet/dry stripe pair with two parallel center-to-center heat
paths, the screening relation is

    g_sheet ~= gamma * k_parallel * t * coverage / pitch**2

with ``gamma=4`` for the ideal periodic stripe topology used here.

This is not a universal textile correlation. ``gamma`` depends on topology,
contact area, routing geometry, and whether the local wet/dry regions are close
to isothermal. The purpose is to expose the required ``k*t/pitch²`` scaling and
mass burden explicitly.

A separate two-contact series screen is provided:

    1/g_eff = 1/g_sheet + 2/h_contact

which shows that sheet conductivity alone cannot deliver a large effective
wet-to-dry conductance when interfaces are weak.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

DEFAULT_GAMMA = 4.0
DEFAULT_AREA_M2 = 0.30

# Explicit screening property classes. These are model inputs, not claims for
# named commercial materials.
PROPERTY_CLASSES = (
    ("moderate", 10.0, 1500.0),
    ("high-k lightweight", 100.0, 1600.0),
    ("very-high-k lightweight", 300.0, 1800.0),
    ("high-k dense", 200.0, 2700.0),
)


def sheet_g_mix(
    k_parallel_W_mK: float,
    thickness_um: float,
    pitch_mm: float,
    coverage: float = 1.0,
    gamma: float = DEFAULT_GAMMA,
) -> float:
    """Return idealized sheet-only ``g_mix`` [W/(m² K)]."""
    if k_parallel_W_mK <= 0 or thickness_um <= 0 or pitch_mm <= 0 or gamma <= 0:
        raise ValueError("k, thickness, pitch and gamma must be positive")
    if not 0.0 < coverage <= 1.0:
        raise ValueError("coverage must be in (0,1]")
    thickness_m = thickness_um * 1e-6
    pitch_m = pitch_mm * 1e-3
    return float(gamma * k_parallel_W_mK * thickness_m * coverage / pitch_m**2)


def required_k_times_t_W_K(
    target_g_mix_W_m2K: float,
    pitch_mm: float,
    coverage: float = 1.0,
    gamma: float = DEFAULT_GAMMA,
) -> float:
    """Return required ``k*t`` [W/K] for the screening stripe topology."""
    if target_g_mix_W_m2K <= 0 or pitch_mm <= 0 or gamma <= 0:
        raise ValueError("target, pitch and gamma must be positive")
    if not 0.0 < coverage <= 1.0:
        raise ValueError("coverage must be in (0,1]")
    pitch_m = pitch_mm * 1e-3
    return float(target_g_mix_W_m2K * pitch_m**2 / (gamma * coverage))


def required_thickness_um(
    target_g_mix_W_m2K: float,
    k_parallel_W_mK: float,
    pitch_mm: float,
    coverage: float = 1.0,
    gamma: float = DEFAULT_GAMMA,
) -> float:
    if k_parallel_W_mK <= 0:
        raise ValueError("k must be positive")
    return float(
        1e6
        * required_k_times_t_W_K(
            target_g_mix_W_m2K,
            pitch_mm,
            coverage=coverage,
            gamma=gamma,
        )
        / k_parallel_W_mK
    )


def spreader_mass_g(
    area_m2: float,
    density_kg_m3: float,
    thickness_um: float,
    coverage: float = 1.0,
) -> float:
    if area_m2 <= 0 or density_kg_m3 <= 0 or thickness_um <= 0:
        raise ValueError("area, density and thickness must be positive")
    if not 0.0 < coverage <= 1.0:
        raise ValueError("coverage must be in (0,1]")
    return float(area_m2 * density_kg_m3 * thickness_um * 1e-6 * coverage * 1000.0)


def effective_g_with_contacts(g_sheet_W_m2K: float, h_contact_W_m2K: float) -> float:
    """Two identical interface contacts in series with the lateral sheet path."""
    if g_sheet_W_m2K <= 0 or h_contact_W_m2K <= 0:
        raise ValueError("conductances must be positive")
    return float(1.0 / (1.0 / g_sheet_W_m2K + 2.0 / h_contact_W_m2K))


def required_contact_h_W_m2K(target_g_eff_W_m2K: float, g_sheet_W_m2K: float) -> float:
    """Required each-side contact conductance for a target effective ``g_mix``.

    Returns infinity when the sheet-only conductance is not greater than the
    requested effective target.
    """
    if target_g_eff_W_m2K <= 0 or g_sheet_W_m2K <= 0:
        raise ValueError("conductances must be positive")
    denominator = 1.0 / target_g_eff_W_m2K - 1.0 / g_sheet_W_m2K
    if denominator <= 0.0:
        return float("inf")
    return float(2.0 / denominator)


def run_screen(target_g_mix_W_m2K: float = 300.0) -> pd.DataFrame:
    rows = []
    for name, k_parallel, density in PROPERTY_CLASSES:
        for pitch_mm in (10.0, 20.0, 30.0, 50.0):
            for coverage in (0.25, 0.50, 1.0):
                thickness_um = required_thickness_um(
                    target_g_mix_W_m2K,
                    k_parallel,
                    pitch_mm,
                    coverage=coverage,
                )
                mass_g = spreader_mass_g(
                    DEFAULT_AREA_M2,
                    density,
                    thickness_um,
                    coverage=coverage,
                )
                rows.append(
                    {
                        "classification": "SIMULATION/SPREADER_GEOMETRY_MAPPING",
                        "target_g_mix_W_m2K": target_g_mix_W_m2K,
                        "property_class": name,
                        "k_parallel_W_mK": k_parallel,
                        "density_kg_m3": density,
                        "pitch_mm": pitch_mm,
                        "coverage": coverage,
                        "required_thickness_um": thickness_um,
                        "mass_over_0p30m2_g": mass_g,
                        "outer_fiber_strain_at_R10mm_percent": thickness_um * 1e-6 / (2.0 * 0.010) * 100.0,
                        "k_over_rho": k_parallel / density,
                    }
                )
    return pd.DataFrame(rows)


def run_contact_screen(target_g_eff_W_m2K: float = 300.0) -> pd.DataFrame:
    rows = []
    for multiplier in (1.05, 1.25, 1.5, 2.0, 3.0, 5.0, 10.0):
        g_sheet = target_g_eff_W_m2K * multiplier
        rows.append(
            {
                "classification": "SIMULATION/SPREADER_CONTACT_AUDIT",
                "target_g_eff_W_m2K": target_g_eff_W_m2K,
                "g_sheet_W_m2K": g_sheet,
                "sheet_to_target_ratio": multiplier,
                "required_h_contact_each_side_W_m2K": required_contact_h_W_m2K(
                    target_g_eff_W_m2K,
                    g_sheet,
                ),
                "absolute_contact_ceiling_min_h_W_m2K": 2.0 * target_g_eff_W_m2K,
            }
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(run_screen().to_string(index=False))
    print("\nContact audit:")
    print(run_contact_screen().to_string(index=False))
