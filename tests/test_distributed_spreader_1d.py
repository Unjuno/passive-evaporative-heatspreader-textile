import pytest

from simulations.distributed_spreader_1d import evaluate_virtual_prototype_distributed
from simulations.virtual_prototype_v01 import PROTOTYPES, evaluate_prototype


def _prototype(name):
    return next(item for item in PROTOTYPES if item.name == name)


def test_distributed_vp_states_close_feed_and_energy_residuals():
    for name in (
        "VP-A_short_pitch",
        "VP-B_20mm_simple",
        "VP-C_sparse_highkrho",
        "VP-D_shielded_short",
    ):
        result = evaluate_virtual_prototype_distributed(name, 100.0, n=64)
        assert result["converged"]
        assert result["evap_total_g_h"] == pytest.approx(100.0, abs=0.02)
        assert result["max_outer_energy_residual_W_m2"] < 1e-5
        assert result["max_spreader_energy_residual_W_m2"] < 0.01
        assert result["distributed_spreader_gain_W_over_0p195m2"] > 4.0


def test_distributed_grid_convergence_is_small_for_vp_a():
    coarse = evaluate_virtual_prototype_distributed("VP-A_short_pitch", 100.0, n=32)
    fine = evaluate_virtual_prototype_distributed("VP-A_short_pitch", 100.0, n=64)
    assert coarse["mean_body_heat_flux_W_m2"] == pytest.approx(
        fine["mean_body_heat_flux_W_m2"], abs=0.08
    )
    assert coarse["wet_fraction"] == pytest.approx(fine["wet_fraction"], abs=5e-4)


def test_distributed_short_pitch_beats_20mm_same_material_family():
    a = evaluate_virtual_prototype_distributed("VP-A_short_pitch", 100.0, n=64)
    b = evaluate_virtual_prototype_distributed("VP-B_20mm_simple", 100.0, n=64)
    assert a["distributed_spreader_gain_W_over_0p195m2"] > b["distributed_spreader_gain_W_over_0p195m2"]


def test_distributed_dry_shielding_improves_short_pitch_case():
    a = evaluate_virtual_prototype_distributed("VP-A_short_pitch", 100.0, n=64)
    d = evaluate_virtual_prototype_distributed("VP-D_shielded_short", 100.0, n=64)
    assert d["distributed_spreader_gain_W_over_0p195m2"] > a["distributed_spreader_gain_W_over_0p195m2"] + 0.5


def test_distributed_bridge_remains_close_to_two_node_virtual_anchor():
    for name in (
        "VP-A_short_pitch",
        "VP-B_20mm_simple",
        "VP-C_sparse_highkrho",
        "VP-D_shielded_short",
    ):
        distributed = evaluate_virtual_prototype_distributed(name, 100.0, n=64)
        scalar = evaluate_prototype(_prototype(name), 100.0)
        assert distributed["distributed_spreader_gain_W_over_0p195m2"] == pytest.approx(
            scalar["spreader_gain_W_over_0p195m2"], abs=0.8
        )
