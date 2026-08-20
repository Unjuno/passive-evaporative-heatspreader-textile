from simulations.terminal_route_coddesign import evaluate_regularized_candidate


def test_route_regularization_shortens_terminal_distances_with_small_thermal_tradeoff():
    pressure_focused = evaluate_regularized_candidate(
        n=12, template_weight=0.0, route_weight=0.20
    )
    regularized = evaluate_regularized_candidate(
        n=12, template_weight=0.125, route_weight=0.35
    )
    assert pressure_focused["converged"]
    assert regularized["converged"]
    assert regularized["liquid_p95_mm"] < pressure_focused["liquid_p95_mm"]
    assert regularized["load_weighted_heat_rms_mm"] < pressure_focused["load_weighted_heat_rms_mm"]
    assert regularized["body_W_m2"] > 0.95 * pressure_focused["body_W_m2"]
