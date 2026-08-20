from simulations.spatial_pressure_layout import run_pressure_layout_screen


def test_pressure_aware_layout_beats_center_panel_under_backpack_load():
    table = run_pressure_layout_screen(
        n=12,
        pressure_names=["backpack_plus_straps"],
    ).set_index("wet_layout")
    assert table.loc["pressure_aware", "converged"]
    assert table.loc["center_panel", "converged"]
    assert table.loc["pressure_aware", "body_W_m2"] > table.loc["center_panel", "body_W_m2"]
    assert table.loc["pressure_aware", "evap_capacity_g_m2_h"] > table.loc["center_panel", "evap_capacity_g_m2_h"]
    assert table.loc["pressure_aware", "mean_local_compression"] < table.loc["center_panel", "mean_local_compression"]


def test_unpressurized_reference_does_not_reward_pressure_avoidance():
    table = run_pressure_layout_screen(
        n=12,
        pressure_names=["none"],
    ).set_index("wet_layout")
    assert table.loc["four_islands", "converged"]
    assert table.loc["pressure_aware", "converged"]
    assert table.loc["four_islands", "body_W_m2"] > table.loc["pressure_aware", "body_W_m2"]
