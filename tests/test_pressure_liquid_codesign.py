import pytest

from simulations.pressure_liquid_codesign import (
    add_hydraulic_proxy,
    select_codesign_anchor,
)
from simulations.terminal_route_coddesign import sweep_regularization


def test_codesign_anchor_preserves_thermal_performance_and_shortens_route():
    summary, table = select_codesign_anchor(
        n=12,
        minimum_thermal_retention=0.98,
        radius_retention_floor=0.90,
    )
    thermal = summary[summary["candidate"] == "thermal_only_best"].iloc[0]
    anchor = summary[summary["candidate"] == "codesign_anchor"].iloc[0]

    assert not table.empty
    assert anchor["thermal_retention_percent"] >= 98.0
    assert (
        anchor["hydraulic_p95_proxy_mm_eq"]
        <= thermal["hydraulic_p95_proxy_mm_eq"]
    )
    assert table["pareto_thermal_hydraulic"].any()


def test_hydraulic_proxy_uses_r_to_minus_four_scaling():
    base = sweep_regularization(
        n=12,
        template_weights=[0.0],
        route_weights=[0.20],
    )
    proxied = add_hydraulic_proxy(base, radius_retention_floor=0.90)
    expected = 0.90 ** -4
    assert proxied.iloc[0]["hydraulic_resistance_multiplier"] == pytest.approx(
        expected
    )
    assert proxied.iloc[0]["hydraulic_p95_proxy_mm_eq"] == pytest.approx(
        proxied.iloc[0]["liquid_p95_mm"] * expected
    )
