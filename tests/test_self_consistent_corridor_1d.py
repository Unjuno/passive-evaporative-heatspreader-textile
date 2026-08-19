import math

from simulations.self_consistent_corridor_1d import (
    rectangular_poiseuille_number,
    solve_corridor,
)


def one_solution(**kwargs):
    roots = solve_corridor(**kwargs)
    assert len(roots) == 1
    return roots[0]


def test_rectangular_poiseuille_limits_are_reasonable():
    square = rectangular_poiseuille_number(0.003, 0.003)
    shallow = rectangular_poiseuille_number(0.030, 0.001)
    assert math.isclose(square, 56.9, rel_tol=0.01)
    assert 90.0 < shallow < 96.0


def test_primary_shallow_corridor_is_diffusion_dominated():
    sol = one_solution(
        width_mm=3.0,
        depth_mm=2.0,
        length_mm=100.0,
        ambient_c=35.0,
        ambient_rh=0.70,
    )
    assert sol.velocity_m_s > 0.0
    assert sol.Pe_mass_length < 1.0
    assert sol.transport_regime == "diffusion-dominated"


def test_large_open_corridor_becomes_advection_relevant_in_drier_air():
    sol = one_solution(
        width_mm=10.0,
        depth_mm=5.0,
        length_mm=100.0,
        ambient_c=35.0,
        ambient_rh=0.50,
    )
    assert sol.velocity_m_s > 0.0
    assert sol.Pe_mass_length >= 10.0
    assert sol.transport_regime == "advection-relevant"


def test_flow_can_reverse_at_high_humidity():
    sol = one_solution(
        width_mm=10.0,
        depth_mm=5.0,
        length_mm=100.0,
        ambient_c=35.0,
        ambient_rh=0.85,
    )
    assert sol.velocity_m_s < 0.0


def test_hot_ambient_case_can_drive_downward_flow_and_inward_body_heat():
    sol = one_solution(
        width_mm=10.0,
        depth_mm=5.0,
        length_mm=100.0,
        ambient_c=40.0,
        ambient_rh=0.70,
    )
    assert sol.velocity_m_s < 0.0
    assert sol.Pe_mass_length >= 10.0
    assert sol.body_heat_flux_W_m2_wet < 0.0


def test_shorter_segments_reduce_saturation_penalty_in_primary_environment():
    short = one_solution(
        width_mm=10.0,
        depth_mm=5.0,
        length_mm=20.0,
        ambient_c=35.0,
        ambient_rh=0.70,
    )
    long = one_solution(
        width_mm=10.0,
        depth_mm=5.0,
        length_mm=200.0,
        ambient_c=35.0,
        ambient_rh=0.70,
    )
    assert short.body_heat_flux_W_m2_wet > long.body_heat_flux_W_m2_wet
    assert short.mean_air_RH < long.mean_air_RH


def test_horizontal_channel_has_no_buoyancy_root_in_this_model():
    roots = solve_corridor(
        width_mm=10.0,
        depth_mm=5.0,
        length_mm=100.0,
        ambient_c=35.0,
        ambient_rh=0.70,
        vertical_projection=0.0,
    )
    assert roots == []
