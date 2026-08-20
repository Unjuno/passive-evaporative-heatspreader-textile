import numpy as np
import pytest

from experiments.analysis.derived_metrics import (
    effective_vapor_conductance_m_s,
    evaporation_heat_classification,
    heat_flow_classification,
    renewal_metrics,
    water_balance_with_independent_evaporation,
)


def test_renewal_metric_recovers_constructed_F():
    # Construct local state halfway between ambient vapor density and saturated
    # surface vapor density by solving it through the public function inputs.
    # For this regression, 34 C local/surface makes RH conversion direct.
    ambient_t = 35.0
    ambient_rh = 0.70
    surface_t = 34.0

    # First get the endpoint vapor densities using a fully ambient-like local
    # state and then construct target vapor density through RH at 34 C.
    from experiments.analysis.derived_metrics import (
        saturated_vapor_density_kg_m3,
        vapor_density_kg_m3,
    )

    c_inf = float(vapor_density_kg_m3(ambient_t, ambient_rh))
    c_sat = float(saturated_vapor_density_kg_m3(surface_t))
    target_F = 0.8
    c_local = c_inf + (1.0 - target_F) * (c_sat - c_inf)
    local_rh = c_local / float(saturated_vapor_density_kg_m3(surface_t))

    result = renewal_metrics(ambient_t, ambient_rh, surface_t, local_rh, surface_t)
    assert float(result["F"]) == pytest.approx(target_F, abs=1e-10)


def test_renewal_metric_does_not_clip_out_of_range_values():
    result = renewal_metrics(35.0, 0.70, 34.0, 0.60, 34.0)
    assert not np.isnan(float(result["F"]))
    # Drier-than-ambient-equivalent local vapor can yield F > 1; retain it as
    # a diagnostic instead of silently clipping.
    assert float(result["F"]) > 1.0


def test_renewal_metric_rejects_nonpositive_bulk_driving_force():
    with pytest.raises(ValueError):
        renewal_metrics(40.0, 1.0, 40.0, 1.0, 34.0)


def test_effective_vapor_conductance_positive_for_positive_flux():
    k = effective_vapor_conductance_m_s(
        1e-4,
        ambient_temp_c=35.0,
        ambient_rh_fraction=0.70,
        wet_surface_temp_c=34.0,
    )
    assert float(k) > 0.0


def test_heat_sign_classification_preserves_negative_body_heat():
    assert heat_flow_classification(-2.0) == "body-heating-direction"
    assert evaporation_heat_classification(-2.0, 1e-5) == "evaporating/body-heating"


def test_water_balance_requires_independent_evaporation_and_reports_failure():
    result = water_balance_with_independent_evaporation(
        feed_g=150.0,
        runoff_g=5.0,
        sample_mass_change_g=10.0,
        independently_measured_evap_g=120.0,
    )
    assert result.unaccounted_g == pytest.approx(15.0)
    assert result.closure_fraction == pytest.approx(0.90)


def test_water_balance_can_meet_95pct_target():
    result = water_balance_with_independent_evaporation(
        feed_g=150.0,
        runoff_g=5.0,
        sample_mass_change_g=10.0,
        independently_measured_evap_g=130.0,
    )
    assert result.closure_fraction == pytest.approx(0.9666666667)
