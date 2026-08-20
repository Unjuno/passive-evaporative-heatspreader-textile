from simulations.capillary_practical_constraints import (
    best_under_radius_cap,
    installed_channels_for_blockage,
)


def test_local_cell_tolerates_200um_radius_cap_with_small_area_penalty():
    unconstrained = best_under_radius_cap(37.5, 50.0, 25.0, 600.0)
    capped = best_under_radius_cap(37.5, 50.0, 25.0, 200.0)
    penalty = capped["cross_section_mm2"] / unconstrained["cross_section_mm2"]
    assert penalty < 1.15


def test_tighter_radius_cap_increases_hydraulic_area_burden():
    cap100 = best_under_radius_cap(37.5, 50.0, 25.0, 100.0)
    cap200 = best_under_radius_cap(37.5, 50.0, 25.0, 200.0)
    assert cap100["cross_section_mm2"] > cap200["cross_section_mm2"]


def test_blockage_requires_installed_redundancy():
    assert installed_channels_for_blockage(7, 0.0) == 7
    assert installed_channels_for_blockage(7, 0.3) == 10
    assert installed_channels_for_blockage(7, 0.5) == 14
