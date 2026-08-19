from simulations.split_transfer_sensitivity import run_sensitivity, summarize


def test_sensitivity_grid_has_expected_axes():
    df = run_sensitivity()
    assert not df.empty
    assert set(df["RH"].unique()) == {0.50, 0.70, 0.85}
    assert set(df["U_body_W_m2K"].unique()) == {60.0, 100.0, 140.0}
    assert set(df["h_rad_W_m2K"].unique()) == {4.0, 6.0, 8.0}
    assert set(df["M_h"].unique()) == {1.0, 1.25, 1.5, 2.0}
    assert set(df["M_m"].unique()) == {1.3, 2.0, 3.0, 4.0}


def test_summary_is_grid_fraction_not_out_of_bounds():
    summary = summarize(run_sensitivity())
    assert not summary.empty
    assert ((summary["fraction_gain_positive"] >= 0.0) & (summary["fraction_gain_positive"] <= 1.0)).all()
    assert ((summary["fraction_gain_ge_5W"] >= 0.0) & (summary["fraction_gain_ge_5W"] <= 1.0)).all()
