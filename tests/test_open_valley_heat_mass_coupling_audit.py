import pytest

from simulations.open_valley_heat_mass_coupling_audit import (
    chilton_colburn_xi,
    coupling_metrics,
    lewis_number,
    run_screen,
    zero_body_flux_threshold,
)
from simulations.open_valley_thermal_1d import solve_open_valley_thermal


def test_same_exchange_length_has_xi_one():
    metrics = coupling_metrics(0.5, 0.5, 35.0, 0.70)
    assert metrics["Xi_delta_vapor_over_delta_heat"] == pytest.approx(1.0)
    assert metrics["chi_h_over_rhocp_km"] == pytest.approx(metrics["Lewis_number"])


def test_screening_lewis_number_is_order_one():
    le = lewis_number(35.0, 0.70)
    assert 0.7 < le < 1.1


def test_chilton_colburn_equivalent_xi_is_near_unity_for_air_water_vapor_screen():
    xi = chilton_colburn_xi(40.0, 0.70)
    assert 0.9 < xi < 1.2


def test_hot_ambient_same_length_baseline_has_negative_body_flux():
    result = solve_open_valley_thermal(
        40.0,
        0.70,
        delta_vapor_mm=0.5,
        delta_heat_mm=0.5,
    )
    assert result.mean_evap_flux_g_m2_h > 0.0
    assert result.mean_body_heat_flux_W_m2 < 0.0


def test_hot_ambient_zero_flux_requires_xi_below_same_length_baseline():
    threshold = zero_body_flux_threshold(0.5)
    assert threshold["found_zero_crossing"]
    assert 0.0 < threshold["critical_Xi"] < 1.0
    assert threshold["critical_Xi"] == pytest.approx(0.56, abs=0.08)


def test_standard_same_boundary_analogies_do_not_meet_40C70RH_selectivity_burden():
    table = run_screen()
    assert not table["same_length_meets_required_selectivity"].any()
    assert not table["chilton_colburn_meets_required_selectivity"].any()
    assert (table["critical_Xi_over_chilton_colburn_Xi"] < 1.0).all()


def test_primary_same_length_baseline_remains_positive():
    result = solve_open_valley_thermal(
        35.0,
        0.70,
        delta_vapor_mm=0.5,
        delta_heat_mm=0.5,
    )
    assert result.mean_body_heat_flux_W_m2 > 0.0