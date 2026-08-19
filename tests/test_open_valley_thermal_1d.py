import pytest

from simulations.open_valley_thermal_1d import L_V, solve_open_valley_thermal


def test_primary_case_converges_and_closes_wall_energy_balance():
    result = solve_open_valley_thermal(
        ambient_c=35.0,
        ambient_rh=0.70,
        delta_vapor_mm=0.5,
        delta_heat_mm=0.5,
    )
    assert result.converged

    latent = L_V * (result.mean_evap_flux_g_m2_h / 3.6e6)
    supplied = result.mean_body_heat_flux_W_m2 + result.mean_air_to_wall_W_m2
    assert supplied == pytest.approx(latent, rel=2e-3)


def test_stronger_vapor_renewal_increases_body_heat_removal_at_primary_condition():
    strong = solve_open_valley_thermal(35.0, 0.70, delta_vapor_mm=0.1, delta_heat_mm=0.5)
    weak = solve_open_valley_thermal(35.0, 0.70, delta_vapor_mm=1.0, delta_heat_mm=0.5)
    assert strong.mean_evap_flux_g_m2_h > weak.mean_evap_flux_g_m2_h
    assert strong.mean_body_heat_flux_W_m2 > weak.mean_body_heat_flux_W_m2


def test_reducing_hot_air_sensible_access_can_increase_body_coupled_fraction():
    strong_heat_access = solve_open_valley_thermal(35.0, 0.70, delta_vapor_mm=0.5, delta_heat_mm=0.1)
    weaker_heat_access = solve_open_valley_thermal(35.0, 0.70, delta_vapor_mm=0.5, delta_heat_mm=1.0)
    assert weaker_heat_access.mean_air_to_wall_W_m2 < strong_heat_access.mean_air_to_wall_W_m2
    assert weaker_heat_access.mean_body_heat_flux_W_m2 > strong_heat_access.mean_body_heat_flux_W_m2


def test_linked_air_exchange_can_be_body_heating_at_40C_70RH():
    result = solve_open_valley_thermal(
        ambient_c=40.0,
        ambient_rh=0.70,
        delta_vapor_mm=0.5,
        delta_heat_mm=0.5,
    )
    assert result.converged
    assert result.mean_evap_flux_g_m2_h > 0.0
    assert result.mean_body_heat_flux_W_m2 < 0.0


def test_primary_linked_case_is_below_150gph_feed_for_65pct_of_0p30m2():
    result = solve_open_valley_thermal(
        ambient_c=35.0,
        ambient_rh=0.70,
        delta_vapor_mm=0.1,
        delta_heat_mm=0.1,
    )
    total_g_h = result.mean_evap_flux_g_m2_h * (0.30 * 0.65)
    assert total_g_h < 150.0


def test_drier_secondary_case_can_exceed_same_feed_and_must_be_labeled_supply_limited():
    result = solve_open_valley_thermal(
        ambient_c=35.0,
        ambient_rh=0.50,
        delta_vapor_mm=0.1,
        delta_heat_mm=0.1,
    )
    total_g_h = result.mean_evap_flux_g_m2_h * (0.30 * 0.65)
    assert total_g_h > 150.0
