import math

from simulations.passive_rib_screen import stable_equilibria
from simulations.split_heat_mass_screen import (
    run_split_screen,
    stable_equilibria_split,
)


def test_split_model_matches_legacy_when_multipliers_are_equal():
    legacy = stable_equilibria(35.0, 0.70, 150.0, 1.5, 100.0)
    split = stable_equilibria_split(35.0, 0.70, 150.0, 1.5, 1.5, 100.0)

    assert len(split) == len(legacy)
    for a, b in zip(split, legacy):
        assert math.isclose(a.surface_temp_C, b.surface_temp_C, rel_tol=0.0, abs_tol=1e-8)
        assert math.isclose(a.body_cooling_W, b.body_cooling_W, rel_tol=0.0, abs_tol=1e-8)
        assert math.isclose(a.evaporation_g_h, b.evaporation_g_h, rel_tol=0.0, abs_tol=1e-8)


def test_mass_multiplier_can_change_without_heat_multiplier():
    base = stable_equilibria_split(35.0, 0.70, 150.0, 1.0, 1.0, 100.0)
    mass_enhanced = stable_equilibria_split(35.0, 0.70, 150.0, 1.0, 2.0, 100.0)

    assert base
    assert mass_enhanced
    assert any(
        abs(a.body_cooling_W - b.body_cooling_W) > 1e-6
        for a in base
        for b in mass_enhanced
    )


def test_screen_contains_independent_multiplier_columns():
    df = run_split_screen()
    assert not df.empty
    assert {"M_h", "M_m", "gain_vs_Mh1_Mm1_W"}.issubset(df.columns)
    assert df["M_h"].nunique() > 1
    assert df["M_m"].nunique() > 1
