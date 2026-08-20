import numpy as np

from simulations.protected_support_skeleton import run_support_frontier


def test_support_area_reduces_protected_center_panel_performance():
    table = run_support_frontier(
        n=12,
        air_floors=np.array([1.0]),
        support_fractions=np.array([0.0, 0.20]),
    ).sort_values("support_fraction_of_center_footprint")
    assert table["converged"].all()
    assert table.iloc[0]["body_W_m2"] > table.iloc[-1]["body_W_m2"]
    assert table.iloc[0]["evap_capacity_g_m2_h"] > table.iloc[-1]["evap_capacity_g_m2_h"]


def test_protected_channel_has_a_support_area_budget():
    table = run_support_frontier(
        n=12,
        air_floors=np.array([1.0]),
        support_fractions=np.array([0.0, 0.30]),
    ).sort_values("support_fraction_of_center_footprint")
    assert table.iloc[0]["body_vs_pressure_aware_W_m2"] > 0.0
    assert table.iloc[-1]["body_vs_pressure_aware_W_m2"] < 0.0
