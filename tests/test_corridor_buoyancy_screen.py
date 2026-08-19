import math

from simulations.corridor_buoyancy_screen import (
    corridor_case,
    neutral_rh,
    slot_velocity,
)


def test_neutral_rh_near_34C_is_about_90_percent():
    rh = neutral_rh(34.0, ambient_c=35.0, ambient_rh=0.70)
    assert rh is not None
    assert math.isclose(rh, 0.901, rel_tol=0.0, abs_tol=0.003)


def test_cool_saturated_channel_can_be_heavier_than_ambient():
    u = slot_velocity(2.0, 35.0, 0.70, 32.0, 1.00)
    assert u < 0.0


def test_warm_saturated_channel_can_be_lighter_than_ambient():
    u = slot_velocity(2.0, 35.0, 0.70, 34.0, 1.00)
    assert u > 0.0


def test_wider_slot_increases_laminar_screen_velocity_quadratically():
    u1 = slot_velocity(1.0, 35.0, 0.70, 34.0, 1.00)
    u2 = slot_velocity(2.0, 35.0, 0.70, 34.0, 1.00)
    assert math.isclose(u2 / u1, 4.0, rel_tol=1e-12)


def test_case_reports_direction_and_dimensionless_groups():
    case = corridor_case(2.0, 50.0, 35.0, 0.70, 34.0, 1.00)
    assert case["direction"] == "up"
    assert case["Re_Dh"] >= 0.0
    assert case["Pe_mass_height"] >= 0.0
    assert case["idealized_residence_s"] > 0.0
