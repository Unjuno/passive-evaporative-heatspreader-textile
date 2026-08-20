"""Quasisteady load-schedule screen for fixed vs state-adaptive wet layouts.

This model composes static spatial-pressure states. It does not model transient
wicking, valve dynamics or wearer behavior. Schedule fractions are explicit
hypothetical scenarios used only to decide whether dynamic wet-layout switching
has enough modeled upside to justify added mechanism complexity.
"""
from __future__ import annotations

import pandas as pd

from simulations.spatial_pressure_layout import run_pressure_layout_screen

DEFAULT_SCHEDULES = {
    "commuter_backpack": {
        "none": 0.20,
        "shoulder_straps": 0.15,
        "backpack_plus_straps": 0.65,
    },
    "seated_office": {
        "none": 0.45,
        "seat_back": 0.55,
    },
    "mixed_day": {
        "none": 0.25,
        "backpack_panel": 0.20,
        "shoulder_straps": 0.15,
        "seat_back": 0.20,
        "backpack_plus_straps": 0.20,
    },
}


def evaluate_load_schedules(n=12, schedules=None):
    schedules = DEFAULT_SCHEDULES if schedules is None else schedules
    states = sorted({state for weights in schedules.values() for state in weights})
    table = run_pressure_layout_screen(n=n, pressure_names=states)
    rows = []

    for schedule_name, weights in schedules.items():
        for layout in sorted(table["wet_layout"].unique()):
            q = 0.0
            evap = 0.0
            for state, fraction in weights.items():
                row = table[(table["pressure_map"] == state) & (table["wet_layout"] == layout)].iloc[0]
                q += fraction * row["body_W_m2"]
                evap += fraction * row["evap_capacity_g_m2_h"]
            rows.append({
                "schedule": schedule_name,
                "policy": "fixed",
                "layout": layout,
                "mean_body_W_m2": q,
                "mean_evap_capacity_g_m2_h": evap,
            })

        q = 0.0
        evap = 0.0
        choices = []
        for state, fraction in weights.items():
            group = table[table["pressure_map"] == state]
            best = group.loc[group["body_W_m2"].idxmax()]
            q += fraction * best["body_W_m2"]
            evap += fraction * best["evap_capacity_g_m2_h"]
            choices.append(f"{state}:{best['wet_layout']}")
        rows.append({
            "schedule": schedule_name,
            "policy": "ideal_adaptive",
            "layout": "statewise_best",
            "mean_body_W_m2": q,
            "mean_evap_capacity_g_m2_h": evap,
            "state_choices": ";".join(choices),
        })

    result = pd.DataFrame(rows)
    summaries = []
    for schedule_name, group in result.groupby("schedule"):
        fixed = group[group["policy"] == "fixed"]
        best_fixed = fixed.loc[fixed["mean_body_W_m2"].idxmax()]
        adaptive = group[group["policy"] == "ideal_adaptive"].iloc[0]
        summaries.append({
            "schedule": schedule_name,
            "best_fixed_layout": best_fixed["layout"],
            "best_fixed_body_W_m2": best_fixed["mean_body_W_m2"],
            "adaptive_body_W_m2": adaptive["mean_body_W_m2"],
            "adaptive_uplift_W_m2": adaptive["mean_body_W_m2"] - best_fixed["mean_body_W_m2"],
            "adaptive_uplift_W_over_0p195m2": (adaptive["mean_body_W_m2"] - best_fixed["mean_body_W_m2"]) * 0.195,
            "adaptive_relative_percent": 100 * (adaptive["mean_body_W_m2"] / best_fixed["mean_body_W_m2"] - 1),
            "break_even_control_penalty_percent_of_adaptive_flux": 100 * (
                (adaptive["mean_body_W_m2"] - best_fixed["mean_body_W_m2"]) / adaptive["mean_body_W_m2"]
            ),
            "adaptive_state_choices": adaptive.get("state_choices", ""),
        })
    return result, pd.DataFrame(summaries)


if __name__ == "__main__":
    _, summary = evaluate_load_schedules(n=24)
    print(summary.to_csv(index=False))
