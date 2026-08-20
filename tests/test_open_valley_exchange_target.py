import math

import pytest

from simulations.open_valley_exchange_target import (
    infer_from_measurement,
    loading_from_ratio,
    required_ratio,
    retention_from_ratio,
    vapor_density,
)


def test_ratio_retention_inverse():
    for f in (0.5, 0.67, 0.8, 0.9, 0.95):
        r = required_ratio(f)
        assert math.isclose(retention_from_ratio(r), f, rel_tol=1e-12)
        assert math.isclose(loading_from_ratio(r), 1.0 - f, rel_tol=1e-12)


def test_key_design_targets():
    assert required_ratio(0.5) == pytest.approx(1.0)
    assert required_ratio(0.8) == pytest.approx(4.0)
    assert required_ratio(0.9) == pytest.approx(9.0)
    assert required_ratio(0.95) == pytest.approx(19.0)


def test_measurement_identification_recovers_constructed_ratio():
    # Construct a valley vapor density from the analytic normalized balance,
    # then convert it to RH at the measurement temperature and recover R.
    ambient_c = 35.0
    ambient_rh = 0.70
    surface_c = 34.0
    valley_c = 34.0
    target_r = 4.0

    c_inf = vapor_density(ambient_c, ambient_rh)
    c_sat = vapor_density(surface_c, 1.0)
    theta = 1.0 / (1.0 + target_r)
    c_valley = c_inf + theta * (c_sat - c_inf)

    # At fixed valley temperature, vapor density is linear in RH.
    c_valley_sat = vapor_density(valley_c, 1.0)
    valley_rh = c_valley / c_valley_sat

    result = infer_from_measurement(
        ambient_c=ambient_c,
        ambient_rh=ambient_rh,
        surface_c=surface_c,
        valley_c=valley_c,
        valley_rh=valley_rh,
    )
    assert result["status"] == "identified"
    assert result["R"] == pytest.approx(target_r, rel=1e-10)
    assert result["retention_F"] == pytest.approx(0.8, rel=1e-10)


def test_invalid_measurement_is_not_silently_clipped():
    result = infer_from_measurement(
        ambient_c=35.0,
        ambient_rh=0.70,
        surface_c=34.0,
        valley_c=35.0,
        valley_rh=0.60,
    )
    assert result["status"] == "outside-local-balance-range"
    assert math.isnan(result["R"])
