"""Deterministic sensitivity sweep for the split external-transfer model.

The grid is intentionally not assigned probabilities. Fractions reported by this
script are fractions of a predeclared screening grid, not reliability or
confidence probabilities.
"""

from __future__ import annotations

import pandas as pd

try:
    from simulations.split_heat_mass_screen import (
        select_warm,
        stable_equilibria_split,
    )
except ModuleNotFoundError:  # direct execution
    from split_heat_mass_screen import select_warm, stable_equilibria_split


def run_sensitivity() -> pd.DataFrame:
    ambient_c = 35.0
    water_gph = 150.0

    rows: list[dict[str, float | int]] = []
    for rh in (0.50, 0.70, 0.85):
        for u_body in (60.0, 100.0, 140.0):
            for h_rad in (4.0, 6.0, 8.0):
                reference_roots = stable_equilibria_split(
                    ambient_c,
                    rh,
                    water_gph,
                    heat_multiplier=1.0,
                    mass_multiplier=1.0,
                    u_body=u_body,
                    h_rad=h_rad,
                )
                reference = select_warm(reference_roots)
                if reference is None:
                    continue

                for m_h in (1.0, 1.25, 1.5, 2.0):
                    for m_m in (1.3, 2.0, 3.0, 4.0):
                        roots = stable_equilibria_split(
                            ambient_c,
                            rh,
                            water_gph,
                            heat_multiplier=m_h,
                            mass_multiplier=m_m,
                            u_body=u_body,
                            h_rad=h_rad,
                        )
                        warm = select_warm(roots)
                        if warm is None:
                            continue
                        rows.append(
                            {
                                "ambient_C": ambient_c,
                                "RH": rh,
                                "water_g_h": water_gph,
                                "U_body_W_m2K": u_body,
                                "h_rad_W_m2K": h_rad,
                                "M_h": m_h,
                                "M_m": m_m,
                                "n_stable_roots": len(roots),
                                "surface_temp_C": warm.surface_temp_C,
                                "body_cooling_W": warm.body_cooling_W,
                                "gain_vs_sameU_flat_W": warm.body_cooling_W
                                - reference.body_cooling_W,
                                "evaporation_g_h": warm.evaporation_g_h,
                            }
                        )
    return pd.DataFrame(rows)


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    """Return deterministic grid fractions by RH; not probabilities."""
    groups = []
    for rh, group in df.groupby("RH"):
        groups.append(
            {
                "RH": rh,
                "n_grid_cases": len(group),
                "fraction_gain_positive": float(
                    (group["gain_vs_sameU_flat_W"] > 0.0).mean()
                ),
                "fraction_gain_ge_5W": float(
                    (group["gain_vs_sameU_flat_W"] >= 5.0).mean()
                ),
                "min_gain_W": float(group["gain_vs_sameU_flat_W"].min()),
                "median_gain_W": float(group["gain_vs_sameU_flat_W"].median()),
                "max_gain_W": float(group["gain_vs_sameU_flat_W"].max()),
            }
        )
    return pd.DataFrame(groups)


if __name__ == "__main__":
    frame = run_sensitivity()
    print("Deterministic screening-grid summary (not probabilities):")
    print(summarize(frame).to_string(index=False))
