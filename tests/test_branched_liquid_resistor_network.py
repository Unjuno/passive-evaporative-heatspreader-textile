import pytest

from simulations.branched_liquid_resistor_network import (
    collector_capillary_drive_pa,
    critical_radius_um,
    reference_screen,
    solve_network,
    terminal_masks,
)
from simulations.spatial_pressure_layout import build_pressure_maps


def test_reference_network_has_large_capillary_margin_at_200um():
    table = reference_screen(n=12)
    severe = table[table["collapse_severity"] == 1.0]
    assert not severe.empty
    assert severe["passes_SF3"].all()
    assert (severe["margin_ratio"] > 100.0).all()


def test_pressure_scales_with_inverse_fourth_power_of_radius():
    pressure = build_pressure_maps(12)["backpack_plus_straps"]
    mask = terminal_masks(12)["thermal_only"]
    p200 = solve_network(mask, pressure, trunk_radius_um=200.0)["max_pressure_Pa"]
    p100 = solve_network(mask, pressure, trunk_radius_um=100.0)["max_pressure_Pa"]
    assert p100 / p200 == pytest.approx(16.0, rel=2e-3)


def test_critical_radius_is_well_below_50um_for_local_dense_network():
    pressure = build_pressure_maps(12)["backpack_plus_straps"]
    mask = terminal_masks(12)["thermal_only"]
    p200 = solve_network(mask, pressure, trunk_radius_um=200.0)["max_pressure_Pa"]
    rcrit = critical_radius_um(p200, 200.0, safety_factor=3.0)
    assert collector_capillary_drive_pa() > 0
    assert rcrit < 50.0
