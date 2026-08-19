from simulations.rib_diffusion_screen import solve_periodic_rib_diffusion


def test_rib_increases_flux_over_flat_reference():
    multiplier, _ = solve_periodic_rib_diffusion(
        pitch_mm=1.0,
        rib_height_mm=2.5,
        rib_width_mm=0.25,
        renewal_height_mm=5.0,
        nx=16,
    )
    assert multiplier > 1.0


def test_closer_air_renewal_increases_effective_transfer():
    near, _ = solve_periodic_rib_diffusion(
        pitch_mm=1.0,
        rib_height_mm=2.5,
        rib_width_mm=0.25,
        renewal_height_mm=3.0,
        nx=16,
    )
    far, _ = solve_periodic_rib_diffusion(
        pitch_mm=1.0,
        rib_height_mm=2.5,
        rib_width_mm=0.25,
        renewal_height_mm=7.5,
        nx=16,
    )
    assert near > far


def test_reference_case_regression_band():
    multiplier, actual_height = solve_periodic_rib_diffusion(
        pitch_mm=1.0,
        rib_height_mm=2.5,
        rib_width_mm=0.25,
        renewal_height_mm=3.0,
        nx=24,
    )
    assert abs(actual_height - 3.0) < 1e-12
    assert 4.85 < multiplier < 5.00
