import pytest

from simulations.supply_limit_audit import audit_capacity, run_screen


def test_capacity_below_feed_is_not_supply_limited():
    result = audit_capacity(700.0, feed_g_h=150.0, wet_area_m2=0.195)
    assert result["evap_capacity_g_h"] == pytest.approx(136.5)
    assert not result["supply_limited"]
    assert result["thermal_capacity_state_valid_at_fixed_feed"]


def test_capacity_above_feed_is_supply_limited_without_fake_thermal_solution():
    result = audit_capacity(1273.0, feed_g_h=150.0, wet_area_m2=0.195)
    assert result["evap_capacity_g_h"] > 150.0
    assert result["supply_limited"]
    assert result["achievable_evap_upper_bound_g_h"] == pytest.approx(150.0)
    assert not result["thermal_capacity_state_valid_at_fixed_feed"]


def test_primary_150gph_linked_cases_remain_below_feed_capacity():
    df = run_screen()
    linked = df[
        (df["ambient_C"] == 35.0)
        & (df["ambient_RH"] == 0.70)
        & (df["feed_g_h"] == 150.0)
        & (df["delta_vapor_mm"] == df["delta_heat_mm"])
    ]
    assert len(linked) >= 3
    assert not linked["supply_limited"].any()


def test_dry_150gph_screen_contains_supply_limited_linked_cases():
    df = run_screen()
    linked = df[
        (df["ambient_C"] == 35.0)
        & (df["ambient_RH"] == 0.50)
        & (df["feed_g_h"] == 150.0)
        & (df["delta_vapor_mm"] == df["delta_heat_mm"])
    ]
    assert linked["supply_limited"].any()
