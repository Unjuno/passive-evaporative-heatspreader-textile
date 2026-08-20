import numpy as np

from simulations.heat_network_topology_2d import (
    distributed_dropout,
    evaluate,
    localized_damage,
    topology_mask,
)


def test_equal_material_count_across_network_topologies():
    n = 24
    names = (
        "parallel_stripes",
        "herringbone",
        "radial_spokes",
        "leaf_venation",
        "redundant_mesh",
    )
    counts = [int(topology_mask(name, n).sum()) for name in names]
    counts.append(int(topology_mask("directed_mesh_blend", n, mesh_weight=0.125).sum()))
    assert len(set(counts)) == 1


def test_damage_operators_remove_conductor_without_adding_material():
    mask = topology_mask("parallel_stripes", 24)
    localized = localized_damage(mask, 0.5, 0.5, 0.05)
    random_a = distributed_dropout(mask, 0.05, seed=123)
    random_b = distributed_dropout(mask, 0.05, seed=123)

    assert localized.sum() < mask.sum()
    assert random_a.sum() < mask.sum()
    assert np.array_equal(random_a, random_b)
    assert np.all(~localized | mask)
    assert np.all(~random_a | mask)


def test_small_grid_network_screens_are_positive_and_converged():
    directed = evaluate("parallel_stripes", n=16)
    radial = evaluate("radial_spokes", n=16)
    blend = evaluate("directed_mesh_blend", n=16, mesh_weight=0.125)

    assert directed.converged
    assert radial.converged
    assert blend.converged
    assert directed.gain_vs_background_W > 0.0
    assert radial.gain_vs_background_W > 0.0
    assert blend.gain_vs_background_W > 0.0
    assert 0.30 < directed.material_fraction < 0.40
