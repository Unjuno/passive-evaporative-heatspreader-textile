import pytest

from simulations.open_valley_distributed_1d import solve_open_valley


def test_long_valley_center_matches_local_analytic_balance():
    result = solve_open_valley(
        width_mm=6.0,
        depth_mm=3.0,
        length_mm=50.0,
        velocity_mm_s=0.0,
        effective_open_exchange_distance_mm=0.5,
        nx=801,
    )
    assert result.center_retention_F == pytest.approx(
        result.local_long_valley_retention_F,
        rel=5e-4,
    )


def test_short_end_open_segment_retains_more_driving_force():
    short = solve_open_valley(6.0, 3.0, 1.0, 0.0, 0.5, nx=401)
    long = solve_open_valley(6.0, 3.0, 50.0, 0.0, 0.5, nx=801)
    assert short.center_retention_F > 0.90
    assert short.center_retention_F > long.center_retention_F
    assert long.center_retention_F == pytest.approx(0.515, abs=0.005)


def test_centimeter_scale_segmentation_does_not_rescue_weak_lateral_exchange():
    twenty = solve_open_valley(6.0, 3.0, 20.0, 0.0, 1.0, nx=801)
    fifty = solve_open_valley(6.0, 3.0, 50.0, 0.0, 1.0, nx=801)
    assert twenty.center_retention_F == pytest.approx(fifty.center_retention_F, abs=0.002)
    assert fifty.center_retention_F < 0.40


def test_small_axial_flow_has_little_effect_on_long_valley_center():
    still = solve_open_valley(6.0, 3.0, 50.0, 0.0, 0.5, nx=801)
    slow = solve_open_valley(6.0, 3.0, 50.0, 5.0, 0.5, nx=801)
    assert slow.center_retention_F == pytest.approx(still.center_retention_F, abs=0.002)


def test_high_retention_cannot_be_used_as_only_optimization_metric():
    shallow = solve_open_valley(6.0, 0.5, 50.0, 0.0, 0.1, nx=801)
    deep = solve_open_valley(6.0, 8.0, 50.0, 0.0, 0.1, nx=801)

    # In this screening mapping the deeper valley weakens wet-wall transfer,
    # so F rises while the actual series vapor conductance falls.
    assert deep.local_long_valley_retention_F > shallow.local_long_valley_retention_F
    assert (
        deep.effective_series_vapor_conductance_m_s
        < shallow.effective_series_vapor_conductance_m_s
    )


def test_series_conductance_identity():
    result = solve_open_valley(6.0, 3.0, 50.0, 0.0, 0.5, nx=401)
    expected = (
        result.wet_surface_transfer_coefficient_m_s
        * result.lateral_renewal_coefficient_m_s
        / (
            result.wet_surface_transfer_coefficient_m_s
            + result.lateral_renewal_coefficient_m_s
        )
    )
    assert result.effective_series_vapor_conductance_m_s == pytest.approx(expected)


def test_grid_convergence_for_center_retention():
    coarse = solve_open_valley(6.0, 3.0, 50.0, 1.0, 0.5, nx=101)
    fine = solve_open_valley(6.0, 3.0, 50.0, 1.0, 0.5, nx=801)
    assert coarse.center_retention_F == pytest.approx(fine.center_retention_F, rel=1e-5)
