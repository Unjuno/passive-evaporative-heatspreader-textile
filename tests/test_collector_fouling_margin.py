import numpy as np

from simulations.collector_fouling_margin import (
    SALT_VAPOR_FLUX,
    localized_deposit_field,
    solve_fouled_sparse_network,
    uniform_deposit_field,
)
from simulations.branched_liquid_resistor_network import terminal_masks
from simulations.spatial_pressure_layout import build_pressure_maps


def test_salt_vapor_flux_is_zero():
    assert SALT_VAPOR_FLUX == 0.0


def test_uniform_collector_radius_loss_reduces_capillary_margin():
    n = 12
    pressure = build_pressure_maps(n)["backpack_plus_straps"]
    terminal = terminal_masks(n)["thermal_only"]
    clean = solve_fouled_sparse_network(
        terminal,
        pressure,
        collector_radius_um=40.0,
        deposit_um=uniform_deposit_field(n, 0.0),
        trunk_spacing_cells=n,
        drive_radius_um=40.0,
    )
    fouled = solve_fouled_sparse_network(
        terminal,
        pressure,
        collector_radius_um=40.0,
        deposit_um=uniform_deposit_field(n, 5.0),
        trunk_spacing_cells=n,
        drive_radius_um=35.0,
    )
    assert fouled["max_pressure_Pa"] > clean["max_pressure_Pa"]
    assert fouled["margin_ratio"] < clean["margin_ratio"]


def test_localized_deposit_preserves_requested_mean_thickness():
    field = localized_deposit_field(20, mean_deposit_um=3.0, occupied_fraction=0.20, seed=1)
    assert np.isclose(field.mean(), 3.0, rtol=0.05)
    assert np.count_nonzero(field) == round(0.20 * 20 * 20)
