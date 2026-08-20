from simulations.heat_network_combined_failure import run_combined_screen


def test_combined_failure_reduces_gain_for_each_candidate():
    table = run_combined_screen(n=12)
    for topology, group in table.groupby("topology"):
        states = group.set_index("condition")
        assert states.loc["nominal", "converged"]
        assert states.loc["all_three", "converged"]
        assert states.loc["all_three", "gain_W"] < states.loc["nominal", "gain_W"]
        assert states.loc["all_three", "gain_W"] > 0.0


def test_contact_plus_fracture_is_worse_than_fracture_alone_for_blend():
    table = run_combined_screen(n=12)
    blend = table[table["topology"] == "blend_0p125"].set_index("condition")
    assert blend.loc["contact_plus_fracture", "gain_W"] < blend.loc["local_5pct_fracture", "gain_W"]
