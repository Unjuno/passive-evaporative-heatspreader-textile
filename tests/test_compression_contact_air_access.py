from simulations.compression_contact_air_access import solve_compression


def test_uncompressed_reference_is_supply_limited_and_converged():
    result = solve_compression(0.0, air_exponent=2.0)
    assert result.converged
    assert result.regime == "supply-limited-partial-wet"
    assert 0.0 < result.wet_fraction < 1.0
    assert abs(result.evaporation_g_h - 100.0) < 0.05


def test_strong_compression_can_become_transfer_limited():
    result = solve_compression(0.60, air_exponent=2.0)
    assert result.converged
    assert result.regime == "transfer-limited-full-wet"
    assert result.wet_fraction == 1.0
    assert result.evaporation_g_h < 100.0


def test_moderate_compression_can_improve_contact_before_air_closure_dominates():
    nominal = solve_compression(0.0, air_exponent=2.0)
    moderate = solve_compression(0.25, air_exponent=2.0)
    severe = solve_compression(0.70, air_exponent=2.0)

    assert moderate.body_heat_W > nominal.body_heat_W
    assert severe.body_heat_W < nominal.body_heat_W
