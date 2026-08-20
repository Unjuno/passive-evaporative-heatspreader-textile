from simulations.pressure_weighted_liquid_routes import evaluate_layouts


def test_pressure_collapse_increases_weighted_liquid_route_cost():
    uncollapsed = evaluate_layouts(n=12, collapse_severity=0.0).set_index("layout")
    collapsed = evaluate_layouts(n=12, collapse_severity=0.5).set_index("layout")
    assert collapsed.loc["regularized", "p95_path_cost_mm_equivalent"] > uncollapsed.loc["regularized", "p95_path_cost_mm_equivalent"]


def test_protected_escape_trunk_reduces_pressure_weighted_route_cost():
    unprotected = evaluate_layouts(n=12, collapse_severity=0.5).set_index("layout")
    protected = evaluate_layouts(n=12, collapse_severity=0.5, protected_radius_floor=0.90).set_index("layout")
    assert protected.loc["regularized", "p95_path_cost_mm_equivalent"] < unprotected.loc["regularized", "p95_path_cost_mm_equivalent"]
