from simulations.integrated_virtual_prototype_vpe import (
    run_vpe_environment_map,
    vpe_bom,
    vpe_liquid_margin,
)


def test_vpe_is_open_and_body_cooling_positive_at_35c_70rh():
    row = run_vpe_environment_map(n=12, environments=[(35.0,0.70)]).iloc[0]
    assert row["converged"]
    assert row["selected_terminal_state"] == "open"
    assert row["selected_body_W_m2"] > 0.0


def test_vpe_shields_terminal_at_40c_70rh_but_remains_body_heating_in_screen():
    row = run_vpe_environment_map(n=12, environments=[(40.0,0.70)]).iloc[0]
    assert row["converged"]
    assert row["selected_terminal_state"] == "shield"
    assert row["selected_body_W_m2"] < 0.0
    assert row["shield_body_W_m2"] > row["open_body_W_m2"]


def test_vpe_liquid_margin_and_bom():
    liquid = vpe_liquid_margin(radius_retentions=(0.80,)).iloc[0]
    assert liquid["installed_per_cell_for_30pct_blockage"] >= 5
    bom = vpe_bom()
    assert 175 < bom["operating_mass_g"] < 190
    assert bom["wet_terminal_peak_stack_mm"] < 5.0
