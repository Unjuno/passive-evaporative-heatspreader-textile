from simulations.load_schedule_policy import evaluate_load_schedules


def test_pressure_aware_is_best_fixed_layout_in_load_heavy_scenarios():
    _, summary = evaluate_load_schedules(n=12)
    lookup = summary.set_index("schedule")
    assert lookup.loc["commuter_backpack", "best_fixed_layout"] == "pressure_aware"
    assert lookup.loc["seated_office", "best_fixed_layout"] == "pressure_aware"


def test_ideal_adaptation_has_positive_but_small_screened_uplift():
    _, summary = evaluate_load_schedules(n=12)
    assert (summary["adaptive_uplift_W_m2"] > 0).all()
    assert (summary["adaptive_relative_percent"] < 3.0).all()
