import math

from simulations.water_salt_1d import (
    analytic_precipitation_leak_threshold,
    solve_normalized_path,
)


def test_precipitation_threshold_is_one_minus_inlet_ratio():
    assert math.isclose(analytic_precipitation_leak_threshold(0.10), 0.90)
    assert math.isclose(analytic_precipitation_leak_threshold(0.40), 0.60)


def test_low_internal_evaporation_does_not_precipitate_dilute_feed():
    result = solve_normalized_path(0.10, 0.20)
    assert result.precipitation_onset_x_fraction is None
    assert math.isclose(result.upstream_salt_deposition_fraction, 0.0, abs_tol=1e-12)
    assert math.isclose(result.terminal_salt_fraction, 1.0, abs_tol=1e-12)
    assert result.concentration_over_csat[-1] < 1.0


def test_large_internal_evaporation_can_precipitate_without_salt_vapor_loss():
    result = solve_normalized_path(0.40, 0.80)
    assert result.precipitation_onset_x_fraction is not None
    assert result.upstream_salt_deposition_fraction > 0.0
    assert result.terminal_salt_fraction < 1.0
    assert math.isclose(
        result.upstream_salt_deposition_fraction + result.terminal_salt_fraction,
        1.0,
        abs_tol=1e-10,
    )
    assert math.isclose(result.concentration_over_csat[-1], 1.0, abs_tol=1e-12)
