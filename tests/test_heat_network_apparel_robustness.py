from simulations.heat_network_apparel_robustness import (
    contact_field,
    run_contact_screen,
    stretch_conduction_factor,
)


def test_serpentine_screen_retains_more_conduction_at_twenty_percent_stretch():
    serpentine = stretch_conduction_factor(0.20, "serpentine_screen")
    straight = stretch_conduction_factor(0.20, "straight_volume_preserving")
    assert 0.0 < straight < serpentine < 1.0


def test_contact_maps_have_expected_degraded_fraction():
    uniform = contact_field("uniform", 20)
    distributed = contact_field("distributed_10pct", 20, seed=7)
    assert (uniform == uniform.max()).all()
    assert (distributed < uniform).sum() == 40


def test_local_wet_contact_degradation_reduces_gain():
    table = run_contact_screen(n=12)
    blend = table[table["topology"] == "blend_0.125"].set_index("contact_case")
    assert blend.loc["uniform", "converged"]
    assert blend.loc["localized_wet_island", "converged"]
    assert blend.loc["localized_wet_island", "gain_W"] < blend.loc["uniform", "gain_W"]
