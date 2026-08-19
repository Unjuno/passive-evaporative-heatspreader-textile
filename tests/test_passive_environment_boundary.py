import pytest

from simulations.open_valley_thermal_1d import solve_open_valley_thermal
from simulations.passive_environment_boundary import (
    boundary_residual,
    zero_body_flux_ambient_temperature,
)


def test_70pct_boundary_matches_reference_value():
    temp = zero_body_flux_ambient_temperature(0.70)
    assert temp == pytest.approx(39.726, abs=0.01)
    assert boundary_residual(temp, 0.70) == pytest.approx(0.0, abs=1e-5)


def test_boundary_decreases_with_humidity():
    t50 = zero_body_flux_ambient_temperature(0.50)
    t70 = zero_body_flux_ambient_temperature(0.70)
    t90 = zero_body_flux_ambient_temperature(0.90)
    assert t50 > t70 > t90


def test_analytic_boundary_matches_coupled_linked_model():
    for rh in (0.60, 0.70, 0.85):
        ambient_c = zero_body_flux_ambient_temperature(rh)
        result = solve_open_valley_thermal(
            ambient_c=ambient_c,
            ambient_rh=rh,
            delta_vapor_mm=0.5,
            delta_heat_mm=0.5,
        )
        assert result.mean_body_heat_flux_W_m2 == pytest.approx(0.0, abs=0.02)


def test_above_boundary_is_body_heating_in_linked_model():
    boundary = zero_body_flux_ambient_temperature(0.70)
    result = solve_open_valley_thermal(
        ambient_c=boundary + 0.5,
        ambient_rh=0.70,
        delta_vapor_mm=0.5,
        delta_heat_mm=0.5,
    )
    assert result.mean_evap_flux_g_m2_h > 0.0
    assert result.mean_body_heat_flux_W_m2 < 0.0
