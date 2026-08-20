from simulations.environment_exposure_control import run_loaded_exposure_case


def test_open_terminal_is_better_at_35c_70rh():
    closed = run_loaded_exposure_case(n=12, ambient_c=35.0, ambient_rh=0.70, exposure_fraction=0.0)
    opened = run_loaded_exposure_case(n=12, ambient_c=35.0, ambient_rh=0.70, exposure_fraction=1.0)
    assert closed["converged"] and opened["converged"]
    assert opened["body_W_m2"] > closed["body_W_m2"]
    assert opened["evap_capacity_g_m2_h"] > closed["evap_capacity_g_m2_h"]


def test_closing_wet_terminal_reduces_harm_at_40c_70rh():
    closed = run_loaded_exposure_case(n=12, ambient_c=40.0, ambient_rh=0.70, exposure_fraction=0.0)
    opened = run_loaded_exposure_case(n=12, ambient_c=40.0, ambient_rh=0.70, exposure_fraction=1.0)
    assert closed["converged"] and opened["converged"]
    assert closed["body_W_m2"] > opened["body_W_m2"]


def test_closing_is_even_more_valuable_at_40c_85rh():
    closed = run_loaded_exposure_case(n=12, ambient_c=40.0, ambient_rh=0.85, exposure_fraction=0.0)
    opened = run_loaded_exposure_case(n=12, ambient_c=40.0, ambient_rh=0.85, exposure_fraction=1.0)
    assert closed["body_W_m2"] > opened["body_W_m2"]
