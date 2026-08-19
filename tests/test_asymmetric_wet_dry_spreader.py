import pytest

from simulations.asymmetric_wet_dry_spreader import DEFAULT_AREA_M2, solve_asymmetric
from simulations.wet_dry_two_node import solve_two_node


def test_asymmetric_screen_closes_feed_and_energy_balance():
    result = solve_asymmetric(100.0, 5.0, feed_total_g_h=100.0)
    assert result.converged
    assert result.evap_total_g_h == pytest.approx(100.0, rel=3e-4)
    assert abs(result.energy_error_W_m2) < 1e-3


def test_equal_dry_and_wet_sensible_coefficients_recover_symmetric_global_flux():
    symmetric = solve_two_node(100.0)
    asymmetric = solve_asymmetric(
        100.0,
        26.200772200772203,
        feed_total_g_h=150.0,
    )
    assert asymmetric.body_heat_flux_W_m2 == pytest.approx(symmetric.body_heat_flux_W_m2, rel=2e-3)


def test_dry_side_shielding_allows_spreader_to_increase_global_body_heat_removal():
    no_mix = solve_asymmetric(0.0, 5.0, feed_total_g_h=100.0)
    high_mix = solve_asymmetric(5000.0, 5.0, feed_total_g_h=100.0)
    assert high_mix.body_heat_flux_W_m2 > no_mix.body_heat_flux_W_m2 + 20.0
    assert (high_mix.body_heat_flux_W_m2 - no_mix.body_heat_flux_W_m2) * DEFAULT_AREA_M2 > 4.0


def test_spreader_gain_collapses_when_dry_side_exposure_matches_wet_side():
    reference = solve_asymmetric(0.0, 5.0, feed_total_g_h=150.0)
    h_wet = reference.h_wet_W_m2K
    no_mix = solve_asymmetric(0.0, h_wet, feed_total_g_h=150.0)
    high_mix = solve_asymmetric(5000.0, h_wet, feed_total_g_h=150.0)
    assert high_mix.body_heat_flux_W_m2 == pytest.approx(no_mix.body_heat_flux_W_m2, rel=5e-4)


def test_intermediate_feed_can_show_more_spreader_value_than_higher_partial_wet_feed():
    mid_no = solve_asymmetric(0.0, 5.0, feed_total_g_h=100.0)
    mid_hi = solve_asymmetric(5000.0, 5.0, feed_total_g_h=100.0)
    high_no = solve_asymmetric(0.0, 5.0, feed_total_g_h=150.0)
    high_hi = solve_asymmetric(5000.0, 5.0, feed_total_g_h=150.0)
    mid_gain = mid_hi.body_heat_flux_W_m2 - mid_no.body_heat_flux_W_m2
    high_gain = high_hi.body_heat_flux_W_m2 - high_no.body_heat_flux_W_m2
    assert mid_gain > 20.0
    assert mid_gain > high_gain + 10.0