from simulations.sparse_branched_liquid_network import (
    sampled_offset_robust_screen,
    solve_sparse_network,
)
from simulations.branched_liquid_resistor_network import terminal_masks
from simulations.spatial_pressure_layout import build_pressure_maps


def test_sparse_trunks_raise_pressure_relative_to_full_trunk_grid():
    pressure = build_pressure_maps(12)["backpack_plus_straps"]
    terminal = terminal_masks(12)["thermal_only"]
    dense = solve_sparse_network(
        terminal,
        pressure,
        trunk_spacing_cells=1,
        collector_radius_um=20.0,
        source_kind="center_hotspot",
    )
    sparse = solve_sparse_network(
        terminal,
        pressure,
        trunk_spacing_cells=6,
        collector_radius_um=20.0,
        source_kind="center_hotspot",
    )
    assert dense["max_pressure_Pa"] > 0
    assert sparse["max_pressure_Pa"] > dense["max_pressure_Pa"]


def test_larger_collector_radius_reduces_sparse_network_pressure():
    pressure = build_pressure_maps(12)["backpack_plus_straps"]
    terminal = terminal_masks(12)["thermal_only"]
    small = solve_sparse_network(
        terminal,
        pressure,
        trunk_spacing_cells=6,
        collector_radius_um=20.0,
        source_kind="center_hotspot",
        offset_y=3,
        offset_x=3,
    )
    large = solve_sparse_network(
        terminal,
        pressure,
        trunk_spacing_cells=6,
        collector_radius_um=50.0,
        source_kind="center_hotspot",
        offset_y=3,
        offset_x=3,
    )
    assert large["max_pressure_Pa"] < small["max_pressure_Pa"]
    assert large["margin_ratio"] > small["margin_ratio"]


def test_offset_robust_screen_is_finite_and_reports_boolean_pass_state():
    table = sampled_offset_robust_screen(
        n=12,
        collector_radii_um=(20.0, 50.0),
        spacings_cells=(2, 4, 6),
    )
    assert len(table) == 6
    assert (table["worst_margin_ratio"] > 0).all()
    assert table["all_offsets_pass_SF3"].dtype == bool
