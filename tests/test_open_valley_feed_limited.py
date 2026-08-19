import pytest

from simulations.open_valley_feed_limited import solve_feed_limited
from simulations.open_valley_thermal_1d import solve_open_valley_thermal


WET_AREA_M2 = 0.30 * 0.65


def test_beta_one_reproduces_full_wet_solver_when_feed_is_abundant():
    feed_flux = 300.0 / WET_AREA_M2
    limited = solve_feed_limited(
        feed_g_m2_h=feed_flux,
        ambient_c=35.0,
        ambient_rh=0.70,
        delta_vapor_mm=0.5,
        delta_heat_mm=0.5,
    )
    full = solve_open_valley_thermal(
        ambient_c=35.0,
        ambient_rh=0.70,
        delta_vapor_mm=0.5,
        delta_heat_mm=0.5,
    )
    assert limited.regime == "transfer-limited"
    assert limited.wet_fraction_beta == pytest.approx(1.0)
    assert limited.mean_evap_flux_g_m2_h == pytest.approx(full.mean_evap_flux_g_m2_h, rel=2e-4)
    assert limited.mean_body_heat_flux_W_m2 == pytest.approx(full.mean_body_heat_flux_W_m2, rel=2e-4)


def test_dry_ambient_case_solves_partial_wetness_and_closes_feed_balance():
    feed_flux = 150.0 / WET_AREA_M2
    result = solve_feed_limited(
        feed_g_m2_h=feed_flux,
        ambient_c=35.0,
        ambient_rh=0.50,
        delta_vapor_mm=0.5,
        delta_heat_mm=0.5,
    )
    assert result.regime == "supply-limited-partial-wetness"
    assert 0.0 < result.wet_fraction_beta < 1.0
    assert result.mean_evap_flux_g_m2_h == pytest.approx(feed_flux, rel=2e-4)
    assert abs(result.feed_balance_error_percent) < 0.05
    assert result.thermal_solver_converged


def test_feed_limited_state_does_not_reuse_fully_wet_body_flux():
    feed_flux = 150.0 / WET_AREA_M2
    limited = solve_feed_limited(
        feed_g_m2_h=feed_flux,
        ambient_c=35.0,
        ambient_rh=0.50,
        delta_vapor_mm=0.5,
        delta_heat_mm=0.5,
    )
    full = solve_open_valley_thermal(
        ambient_c=35.0,
        ambient_rh=0.50,
        delta_vapor_mm=0.5,
        delta_heat_mm=0.5,
    )
    assert limited.mean_body_heat_flux_W_m2 < full.mean_body_heat_flux_W_m2


def test_latent_heat_partition_closes_for_positive_evaporation():
    result = solve_feed_limited(
        feed_g_m2_h=150.0 / WET_AREA_M2,
        ambient_c=35.0,
        ambient_rh=0.50,
        delta_vapor_mm=0.5,
        delta_heat_mm=0.5,
    )
    assert result.latent_flux_W_m2 > 0.0
    assert result.body_fraction_of_latent + result.ambient_fraction_of_latent == pytest.approx(1.0, abs=3e-3)
    assert 0.0 < result.body_fraction_of_latent < 1.0
    assert 0.0 < result.ambient_fraction_of_latent < 1.0


def test_stronger_linked_exchange_can_reduce_body_cooling_after_feed_saturates():
    feed_flux = 150.0 / WET_AREA_M2
    very_strong = solve_feed_limited(
        feed_g_m2_h=feed_flux,
        ambient_c=35.0,
        ambient_rh=0.50,
        delta_vapor_mm=0.10,
        delta_heat_mm=0.10,
    )
    moderate = solve_feed_limited(
        feed_g_m2_h=feed_flux,
        ambient_c=35.0,
        ambient_rh=0.50,
        delta_vapor_mm=0.50,
        delta_heat_mm=0.50,
    )
    assert very_strong.mean_evap_flux_g_m2_h == pytest.approx(feed_flux, rel=2e-4)
    assert moderate.mean_evap_flux_g_m2_h == pytest.approx(feed_flux, rel=2e-4)
    assert moderate.mean_body_heat_flux_W_m2 > very_strong.mean_body_heat_flux_W_m2
    assert moderate.body_fraction_of_latent > very_strong.body_fraction_of_latent


def test_primary_70pct_case_remains_transfer_limited_at_150gph():
    feed_flux = 150.0 / WET_AREA_M2
    result = solve_feed_limited(
        feed_g_m2_h=feed_flux,
        ambient_c=35.0,
        ambient_rh=0.70,
        delta_vapor_mm=0.5,
        delta_heat_mm=0.5,
    )
    assert result.regime == "transfer-limited"
    assert result.wet_fraction_beta == pytest.approx(1.0)
    assert result.mean_evap_flux_g_m2_h < feed_flux