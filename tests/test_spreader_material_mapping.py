import math

import pytest

from simulations.spreader_material_mapping import (
    effective_g_with_contacts,
    required_contact_h_W_m2K,
    required_thickness_um,
    sheet_g_mix,
    spreader_mass_g,
)


def test_sheet_mapping_round_trip():
    target = 300.0
    thickness_um = required_thickness_um(target, 100.0, 20.0)
    assert thickness_um == pytest.approx(300.0)
    assert sheet_g_mix(100.0, thickness_um, 20.0) == pytest.approx(target)


def test_required_mass_is_coverage_invariant_under_linear_coverage_model():
    target = 300.0
    masses = []
    for coverage in (0.25, 0.50, 1.0):
        thickness_um = required_thickness_um(
            target,
            100.0,
            20.0,
            coverage=coverage,
        )
        masses.append(spreader_mass_g(0.30, 1600.0, thickness_um, coverage=coverage))
    assert masses[0] == pytest.approx(masses[1])
    assert masses[1] == pytest.approx(masses[2])


def test_pitch_penalty_is_quadratic():
    g10 = sheet_g_mix(100.0, 100.0, 10.0)
    g20 = sheet_g_mix(100.0, 100.0, 20.0)
    assert g10 / g20 == pytest.approx(4.0)


def test_two_contact_ceiling():
    h_contact = 600.0
    very_large_sheet = 1e12
    effective = effective_g_with_contacts(very_large_sheet, h_contact)
    assert effective == pytest.approx(h_contact / 2.0, rel=1e-8)


def test_contact_requirement_is_infinite_if_sheet_does_not_exceed_target():
    assert math.isinf(required_contact_h_W_m2K(300.0, 300.0))
    assert math.isinf(required_contact_h_W_m2K(300.0, 250.0))


def test_contact_requirement_round_trip():
    target = 300.0
    sheet = 900.0
    h_contact = required_contact_h_W_m2K(target, sheet)
    assert h_contact == pytest.approx(900.0)
    assert effective_g_with_contacts(sheet, h_contact) == pytest.approx(target)
