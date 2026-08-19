import pytest

from simulations.spreader_topology_2d import (
    evaluate_topology,
    topology_fraction_field,
)


def test_all_topologies_preserve_exact_half_high_k_material_fraction():
    for n in (24, 30, 36):
        for name in (
            "uniform_homogenized",
            "x_aligned_traces",
            "y_aligned_traces",
            "connected_mesh",
        ):
            field = topology_fraction_field(name, n)
            assert field.mean() == pytest.approx(0.5, abs=1e-12)


def test_2d_topology_states_close_feed_and_energy_residuals():
    for name in (
        "uniform_homogenized",
        "x_aligned_traces",
        "y_aligned_traces",
        "connected_mesh",
    ):
        result = evaluate_topology(name, n=30, feed_total_g_h=100.0)
        assert result.converged
        assert result.evap_total_g_h == pytest.approx(100.0, abs=0.03)
        assert result.max_outer_energy_residual_W_m2 < 1e-5
        assert result.max_spreader_energy_residual_W_m2 < 0.02


def test_alignment_changes_value_at_equal_material_fraction():
    uniform = evaluate_topology("uniform_homogenized", n=30)
    aligned = evaluate_topology("x_aligned_traces", n=30)
    transverse = evaluate_topology("y_aligned_traces", n=30)
    mesh = evaluate_topology("connected_mesh", n=30)

    assert aligned.high_k_material_fraction == pytest.approx(uniform.high_k_material_fraction)
    assert transverse.high_k_material_fraction == pytest.approx(uniform.high_k_material_fraction)
    assert mesh.high_k_material_fraction == pytest.approx(uniform.high_k_material_fraction)

    assert aligned.gain_vs_no_lateral_W > uniform.gain_vs_no_lateral_W + 0.5
    assert transverse.gain_vs_no_lateral_W < uniform.gain_vs_no_lateral_W - 2.0
    assert mesh.gain_vs_no_lateral_W > transverse.gain_vs_no_lateral_W + 2.0


def test_topology_result_is_grid_stable_for_uniform_and_aligned_cases():
    for name in ("uniform_homogenized", "x_aligned_traces"):
        coarse = evaluate_topology(name, n=24)
        fine = evaluate_topology(name, n=36)
        assert coarse.gain_vs_no_lateral_W == pytest.approx(
            fine.gain_vs_no_lateral_W,
            abs=0.25,
        )
        assert coarse.wet_fraction == pytest.approx(fine.wet_fraction, abs=0.002)
