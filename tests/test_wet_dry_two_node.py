import pytest

from simulations.wet_dry_two_node import solve_two_node


def test_two_node_model_closes_feed_and_energy_balance():
    result = solve_two_node(100.0)
    assert result.converged
    assert result.evap_total_g_h == pytest.approx(150.0, rel=2e-4)
    assert abs(result.energy_error_W_m2) < 1e-3


def test_lateral_spreading_reduces_wet_dry_temperature_split():
    weak = solve_two_node(1.0)
    strong = solve_two_node(500.0)
    assert strong.wet_dry_deltaT_C < weak.wet_dry_deltaT_C
    assert strong.wet_dry_deltaT_C < 0.5


def test_symmetric_global_body_flux_is_nearly_invariant_to_internal_mixing():
    weak = solve_two_node(0.0)
    strong = solve_two_node(1000.0)
    assert weak.body_heat_flux_W_m2 == pytest.approx(strong.body_heat_flux_W_m2, rel=5e-4)
    assert weak.body_fraction_of_latent == pytest.approx(strong.body_fraction_of_latent, rel=5e-4)


def test_model_wet_fraction_changes_with_mixing_even_when_total_heat_does_not():
    weak = solve_two_node(0.0)
    strong = solve_two_node(1000.0)
    assert abs(weak.wet_fraction_beta - strong.wet_fraction_beta) > 0.05


def test_no_mixing_allows_large_local_temperature_split():
    result = solve_two_node(0.0)
    assert result.wet_dry_deltaT_C > 4.0