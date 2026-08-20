import numpy as np

from simulations.salt_leakage_budget import (
    SALT_VAPOR_FLUX,
    concentration_multiplier,
    critical_leak_fraction_to_bulk_saturation,
    outlet_saturation_ratio,
)


def test_salt_vapor_flux_is_zero():
    assert SALT_VAPOR_FLUX == 0.0


def test_ten_percent_water_leak_only_concentrates_bulk_by_one_over_point_nine():
    assert np.isclose(concentration_multiplier(0.10), 1.0 / 0.90)
    assert np.isclose(outlet_saturation_ratio(0.10, 0.10), 0.10 / 0.90)


def test_bulk_saturation_threshold_follows_mass_balance():
    assert np.isclose(critical_leak_fraction_to_bulk_saturation(0.10), 0.90)
    assert outlet_saturation_ratio(0.10, 0.89) < 1.0
    assert outlet_saturation_ratio(0.10, 0.90) >= 1.0
