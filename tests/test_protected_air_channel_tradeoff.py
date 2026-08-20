import numpy as np

from simulations.protected_air_channel_tradeoff import run_protected_air_tradeoff


def test_protected_air_path_improves_loaded_center_panel():
    table = run_protected_air_tradeoff(n=12, floors=np.array([0.0, 0.5, 1.0]))
    assert table["converged"].all()
    assert table.iloc[-1]["center_body_W_m2"] > table.iloc[0]["center_body_W_m2"]
    assert table.iloc[-1]["center_evap_capacity_g_m2_h"] > table.iloc[0]["center_evap_capacity_g_m2_h"]


def test_strong_protected_air_path_can_beat_relocation_in_this_screen():
    table = run_protected_air_tradeoff(n=12, floors=np.array([0.0, 1.0]))
    assert table.iloc[0]["body_difference_vs_relocation_W_m2"] < 0.0
    assert table.iloc[-1]["body_difference_vs_relocation_W_m2"] > 0.0
