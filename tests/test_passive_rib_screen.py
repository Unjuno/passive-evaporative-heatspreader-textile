import math

from simulations.passive_rib_screen import (
    U_FLAT,
    effective_exchange_multiplier,
    panel_geometric_multiplier,
    p_sat,
    select_equilibrium,
    stable_equilibria,
)


def test_saturation_pressure_reference_points():
    assert math.isclose(float(p_sat(0.0)), 611.21, rel_tol=1e-6)
    assert math.isclose(float(p_sat(35.0)), 5626.75, rel_tol=2e-4)


def test_rectangular_rib_geometry_is_dimensionless_ratio():
    g_panel = panel_geometric_multiplier(2.0, 1.5)
    assert math.isclose(g_panel, 3.6666666667, rel_tol=1e-9)


def test_effective_exchange_multiplier_reference_case():
    # f=0.45, h=2 mm, p=1.5 mm, alpha=0.55
    m_eff = effective_exchange_multiplier(0.45, 2.0, 1.5, 0.55)
    assert math.isclose(m_eff, 1.66, rel_tol=1e-12)


def test_primary_flat_control_has_stable_equilibrium():
    roots = stable_equilibria(35.0, 0.70, 150.0, 1.0, U_FLAT)
    assert len(roots) >= 1
    warm = select_equilibrium(roots, "warm")
    assert warm is not None
    assert 33.0 < warm.surface_temp_C < 34.0
    assert warm.body_cooling_W > 0.0


def test_model_exposes_multiple_stable_branches_near_transition():
    # This regression test exists because earlier exploratory code selected the
    # most-cooling stable root without reporting that another stable branch
    # coexisted. The exact transition is model-dependent, but M=3.5 under the
    # frozen screening parameters should expose at least two stable roots.
    roots = stable_equilibria(35.0, 0.70, 150.0, 3.5, 100.0, grid_points=2000)
    assert len(roots) >= 2

    warm = select_equilibrium(roots, "warm")
    cool = select_equilibrium(roots, "cool")
    assert warm is not None and cool is not None
    assert warm.surface_temp_C > cool.surface_temp_C
    assert warm.body_cooling_W < cool.body_cooling_W
