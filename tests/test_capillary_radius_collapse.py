from simulations.capillary_radius_collapse import (
    collapse_blockage_design,
    run_radius_collapse_screen,
)


def test_radius_loss_increases_required_live_channels():
    table = run_radius_collapse_screen(
        cases=[("local", 37.5, 50.0, 25.0, 200.0)],
        radius_retentions=(1.0, 0.8, 0.7),
    ).set_index("radius_retention")
    assert table.loc[0.8, "required_channels"] > table.loc[1.0, "required_channels"]
    assert table.loc[0.7, "required_channels"] > table.loc[0.8, "required_channels"]


def test_blockage_and_radius_loss_require_additional_installed_channels():
    table = collapse_blockage_design(
        radius_retentions=(0.8,), blocked_fractions=(0.0, 0.3)
    ).set_index("blocked_fraction")
    assert table.loc[0.3, "installed_channels_per_cell"] > table.loc[0.0, "installed_channels_per_cell"]
