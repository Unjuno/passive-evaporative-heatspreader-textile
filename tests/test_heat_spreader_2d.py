import numpy as np

from simulations.heat_spreader_2d import orientation_demo, solve_spreader, vertical_band_mask


def test_vertical_band_mask_places_sink_on_right_side():
    mask = vertical_band_mask(20, 10, 0.25)
    assert mask.shape == (10, 20)
    assert np.all(mask[:, -5:])
    assert not np.any(mask[:, :-5])


def test_spreader_temperature_stays_between_sink_and_skin():
    result = solve_spreader(nx=24, ny=24, skin_temp_C=34.0, sink_temp_C=30.0)
    assert result.temperature_min_C >= 30.0 - 1e-8
    assert result.temperature_max_C <= 34.0 + 1e-8
    assert result.body_cooling_W > 0.0
    assert result.temperature_std_C > 0.0


def test_anisotropy_aligned_toward_vertical_sink_band_improves_heat_routing():
    results = orientation_demo()
    aligned = results["aligned_x"]
    reversed_case = results["reversed_y"]

    # The evaporator is a vertical band at the right edge. Higher conductivity
    # in x should therefore move more heat laterally toward the sink than the
    # same anisotropy rotated by 90 degrees.
    assert aligned.body_cooling_W > reversed_case.body_cooling_W
    assert aligned.temperature_std_C < reversed_case.temperature_std_C
