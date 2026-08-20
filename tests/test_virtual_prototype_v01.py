import pytest

from simulations.virtual_prototype_v01 import PROTOTYPES, evaluate_prototype, run_robustness_screen


def prototype(name):
    return next(p for p in PROTOTYPES if p.name == name)


def test_nominal_virtual_prototypes_converge():
    for item in PROTOTYPES:
        result = evaluate_prototype(item, feed_total_g_h=100.0)
        assert result["solver_converged"]
        assert result["spreader_mass_g_over_0p30m2"] > 0.0
        assert result["g_eff_W_m2K"] > 0.0


def test_shielded_short_pitch_outperforms_same_spreader_with_weaker_shielding():
    a = evaluate_prototype(prototype("VP-A_short_pitch"), 100.0)
    d = evaluate_prototype(prototype("VP-D_shielded_short"), 100.0)
    assert d["g_eff_W_m2K"] == pytest.approx(a["g_eff_W_m2K"])
    assert d["spreader_gain_W_over_0p195m2"] > a["spreader_gain_W_over_0p195m2"] + 0.5


def test_sparse_high_k_rho_case_is_lightweight_but_not_claimed_free_mass_saving():
    a = evaluate_prototype(prototype("VP-A_short_pitch"), 100.0)
    c = evaluate_prototype(prototype("VP-C_sparse_highkrho"), 100.0)
    assert c["spreader_mass_g_over_0p30m2"] < a["spreader_mass_g_over_0p30m2"]
    assert c["spreader_gain_W_over_0p195m2"] > 4.0
    # The lower mass comes with a different k/rho class and pitch, not coverage alone.
    assert c["k_parallel_W_mK"] > a["k_parallel_W_mK"]


def test_20mm_same_material_case_carries_quadratic_pitch_penalty():
    a = evaluate_prototype(prototype("VP-A_short_pitch"), 100.0)
    b = evaluate_prototype(prototype("VP-B_20mm_simple"), 100.0)
    assert b["routing_pitch_mm"] == pytest.approx(2.0 * a["routing_pitch_mm"])
    assert b["spreader_mass_g_over_0p30m2"] > a["spreader_mass_g_over_0p30m2"]
    assert b["g_eff_W_m2K"] < a["g_eff_W_m2K"]


def test_topology_contact_robustness_screen_remains_positive_gain_for_vp_a():
    table = run_robustness_screen()
    a = table[table["prototype"] == "VP-A_short_pitch"]
    assert a["solver_converged"].all()
    assert a["spreader_gain_W_over_0p195m2"].min() > 4.0
