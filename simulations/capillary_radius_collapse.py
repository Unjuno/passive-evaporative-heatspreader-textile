"""Equivalent-radius collapse and blockage sensitivity for capillary trunks.

Virtual/computational screen only. This module does not predict pressure-to-
collapse mechanics. It directly sweeps retained hydraulic radius so the severe
r^-4 Poiseuille sensitivity is explicit while retaining the simultaneous
increase in capillary pressure at smaller radius.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from simulations.capillary_liquid_network import required_parallel_channels
from simulations.capillary_practical_constraints import installed_channels_for_blockage


DEFAULT_CASES = [
    ("4local_r200", 37.5, 50.0, 25.0, 200.0),
    ("4local_r150", 37.5, 50.0, 25.0, 150.0),
    ("8local_r200", 18.75, 30.0, 15.0, 200.0),
    ("12local_r150", 12.5, 25.0, 10.0, 150.0),
]


def run_radius_collapse_screen(cases=DEFAULT_CASES,
                               radius_retentions=(1.0,.95,.90,.85,.80,.75,.70,.60,.50)):
    rows = []
    for name, flow, path, rise, nominal_radius in cases:
        nominal_n = required_parallel_channels(flow, path, nominal_radius, rise)
        for retention in radius_retentions:
            effective_radius = nominal_radius * float(retention)
            required_n = required_parallel_channels(flow, path, effective_radius, rise)
            rows.append({
                "case": name,
                "radius_retention": retention,
                "effective_radius_um": effective_radius,
                "nominal_required_channels": nominal_n,
                "required_channels": required_n,
                "channel_count_multiplier": required_n / nominal_n,
                "resistance_only_multiplier": float(retention) ** -4,
            })
    return pd.DataFrame(rows)


def collapse_blockage_design(flow_g_h=37.5, path_mm=50.0, rise_mm=25.0,
                              nominal_radius_um=200.0,
                              radius_retentions=(.90,.80,.70),
                              blocked_fractions=(0,.1,.2,.3,.5)):
    rows = []
    for retention in radius_retentions:
        live = required_parallel_channels(
            flow_g_h, path_mm, nominal_radius_um * retention, rise_mm
        )
        for blocked in blocked_fractions:
            installed = installed_channels_for_blockage(live, blocked)
            rows.append({
                "radius_retention": retention,
                "blocked_fraction": blocked,
                "live_channels_needed_per_cell": live,
                "installed_channels_per_cell": installed,
                "installed_total_4cells": 4 * installed,
            })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(run_radius_collapse_screen().to_csv(index=False))
