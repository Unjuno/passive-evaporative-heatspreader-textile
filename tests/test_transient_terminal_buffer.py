import numpy as np

from simulations.transient_terminal_buffer import (
    lucas_washburn_time_s,
    simulate_terminal_buffer,
    storage_capacity_screen,
)


def test_lucas_washburn_time_falls_with_radius():
    small = lucas_washburn_time_s(30.0, 35.0)
    large = lucas_washburn_time_s(30.0, 100.0)
    assert small > large > 0.0


def test_transient_water_mass_balance_closes():
    table = simulate_terminal_buffer(
        tau_liquid_min=2.0,
        tau_thermal_min=2.0,
        terminal_storage_g=4.0,
        total_min=60.0,
        dt_s=5.0,
    )
    assert np.max(np.abs(table["mass_balance_error_g"])) < 1e-8
    assert (table["terminal_inventory_g"] >= -1e-12).all()
    assert (table["terminal_inventory_g"] <= 4.0 + 1e-9).all()


def test_more_terminal_storage_extends_post_pulse_response():
    table = storage_capacity_screen(capacities_g=(0.0, 4.0, 8.0))
    times = table["time_after_stop_to_half_body_flux_min"].to_numpy()
    assert np.all(np.diff(times) > 0.0)
