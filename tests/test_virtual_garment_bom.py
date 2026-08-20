import numpy as np

from simulations.virtual_garment_bom import (
    evaluate_design,
    heat_route_mass_for_target_gmix,
)


def test_nominal_pressure_relocation_budget_matches_reference_order():
    result = evaluate_design("nominal", "pressure_relocation")
    assert 160 < result["dry_mass_g"] < 180
    assert 175 < result["operating_mass_g"] < 190
    assert 55 < result["added_functional_dry_mass_g"] < 65
    assert 4.0 < result["wet_terminal_peak_stack_mm"] < 4.3


def test_protected_under_load_costs_more_thickness_than_mass():
    relocation = evaluate_design("nominal", "pressure_relocation")
    protected = evaluate_design("nominal", "protected_under_load")
    assert protected["dry_mass_g"] > relocation["dry_mass_g"]
    assert protected["dry_mass_g"] - relocation["dry_mass_g"] < 5.0
    assert protected["wet_terminal_peak_stack_mm"] - relocation["wet_terminal_peak_stack_mm"] >= 2.0


def test_heat_route_mass_has_pitch_squared_scaling():
    m10 = heat_route_mass_for_target_gmix(100.0, 10.0, 100.0, 1600.0)
    m20 = heat_route_mass_for_target_gmix(100.0, 20.0, 100.0, 1600.0)
    assert np.isclose(m20 / m10, 4.0)
