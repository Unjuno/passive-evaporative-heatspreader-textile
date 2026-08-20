import numpy as np

from simulations.capillary_architecture_tradeoff import (
    area_optimal_radius_um,
    compare_architectures,
    minimum_continuous_cross_section_mm2,
)
from simulations.capillary_liquid_network import (
    DENSITY_KG_M3,
    G_M_S2,
    SURFACE_TENSION_N_M,
    CONTACT_ANGLE_DEG,
)


def test_area_optimum_is_half_static_radius_limit():
    rise_mm = 50.0
    theta = np.deg2rad(CONTACT_ANGLE_DEG)
    static_max_radius_m = (
        2.0 * SURFACE_TENSION_N_M * np.cos(theta)
        / (DENSITY_KG_M3 * G_M_S2 * rise_mm * 1e-3)
    )
    assert np.isclose(area_optimal_radius_um(rise_mm), static_max_radius_m * 1e6 / 2.0)


def test_minimum_area_scales_linearly_with_flow_and_path():
    base = minimum_continuous_cross_section_mm2(75.0, 50.0, 50.0)
    double_flow = minimum_continuous_cross_section_mm2(150.0, 50.0, 50.0)
    double_path = minimum_continuous_cross_section_mm2(75.0, 100.0, 50.0)
    assert np.isclose(double_flow / base, 2.0)
    assert np.isclose(double_path / base, 2.0)


def test_distributed_example_uses_less_total_channel_area_than_centralized_example():
    table = compare_architectures().set_index("architecture")
    assert table.loc["4_local", "total_cross_section_mm2"] < table.loc["central", "total_cross_section_mm2"]
    assert table.loc["8_local", "total_liquid_inventory_ml"] < table.loc["central", "total_liquid_inventory_ml"]
