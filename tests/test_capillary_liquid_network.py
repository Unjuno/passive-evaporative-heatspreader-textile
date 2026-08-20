import numpy as np

from simulations.capillary_liquid_network import (
    required_parallel_channels,
    static_capillary_rise_limit_mm,
)


def test_longer_route_requires_more_parallel_channels():
    short = required_parallel_channels(150.0, 20.0, 200.0, 0.0)
    long = required_parallel_channels(150.0, 100.0, 200.0, 0.0)
    assert np.isfinite(short)
    assert np.isfinite(long)
    assert long > short


def test_large_capillary_loses_vertical_head():
    assert static_capillary_rise_limit_mm(100.0) > static_capillary_rise_limit_mm(300.0)
    assert np.isfinite(required_parallel_channels(150.0, 100.0, 200.0, 50.0))
    assert np.isinf(required_parallel_channels(150.0, 100.0, 300.0, 50.0))


def test_local_short_route_can_use_modest_channel_count():
    n = required_parallel_channels(150.0, 20.0, 200.0, 25.0)
    assert n <= 20
