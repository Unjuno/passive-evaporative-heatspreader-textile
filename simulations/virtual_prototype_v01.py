"""Explicit virtual prototype v0.1 comparison.

No physical specimen exists. These prototypes are reproducible combinations of
abstract material/geometry/contact inputs used to connect the mechanism models
to concrete garment-scale design budgets.

The screen evaluates spreader-only mechanism gain relative to the same local
wet/dry boundary conditions with ``g_mix=0``. It is not a full garment cooling
prediction and must not be compared directly with the future B0/B4 physical
benchmark.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

try:
    from simulations.asymmetric_wet_dry_spreader import DEFAULT_AREA_M2, solve_asymmetric
    from simulations.spreader_material_mapping import (
        effective_g_with_contacts,
        sheet_g_mix,
        spreader_mass_g,
    )
except ModuleNotFoundError:
    from asymmetric_wet_dry_spreader import DEFAULT_AREA_M2, solve_asymmetric
    from spreader_material_mapping import effective_g_with_contacts, sheet_g_mix, spreader_mass_g

GARMENT_AREA_M2 = 0.30


@dataclass(frozen=True)
class VirtualPrototype:
    name: str
    description: str
    k_parallel_W_mK: float
    density_kg_m3: float
    thickness_um: float
    coverage: float
    routing_pitch_mm: float
    h_contact_W_m2K: float
    h_dry_W_m2K: float


PROTOTYPES = (
    VirtualPrototype(
        name="VP-A_short_pitch",
        description="10 mm pitch, high-k lightweight property class, strong nominal contact",
        k_parallel_W_mK=100.0,
        density_kg_m3=1600.0,
        thickness_um=100.0,
        coverage=1.0,
        routing_pitch_mm=10.0,
        h_contact_W_m2K=2000.0,
        h_dry_W_m2K=5.0,
    ),
    VirtualPrototype(
        name="VP-B_20mm_simple",
        description="20 mm pitch, same property class, thicker but simpler routing",
        k_parallel_W_mK=100.0,
        density_kg_m3=1600.0,
        thickness_um=200.0,
        coverage=1.0,
        routing_pitch_mm=20.0,
        h_contact_W_m2K=2000.0,
        h_dry_W_m2K=5.0,
    ),
    VirtualPrototype(
        name="VP-C_sparse_highkrho",
        description="15 mm routed half-coverage using a higher k/rho screening property class",
        k_parallel_W_mK=300.0,
        density_kg_m3=1800.0,
        thickness_um=100.0,
        coverage=0.50,
        routing_pitch_mm=15.0,
        h_contact_W_m2K=1500.0,
        h_dry_W_m2K=5.0,
    ),
    VirtualPrototype(
        name="VP-D_shielded_short",
        description="VP-A heat path with stronger dry-side sensible shielding",
        k_parallel_W_mK=100.0,
        density_kg_m3=1600.0,
        thickness_um=100.0,
        coverage=1.0,
        routing_pitch_mm=10.0,
        h_contact_W_m2K=2000.0,
        h_dry_W_m2K=2.0,
    ),
)


def evaluate_prototype(
    prototype: VirtualPrototype,
    feed_total_g_h: float = 100.0,
    gamma: float = 4.0,
    h_contact_override_W_m2K: float | None = None,
) -> dict[str, float | str | bool]:
    h_contact = (
        prototype.h_contact_W_m2K
        if h_contact_override_W_m2K is None
        else h_contact_override_W_m2K
    )
    g_sheet = sheet_g_mix(
        prototype.k_parallel_W_mK,
        prototype.thickness_um,
        prototype.routing_pitch_mm,
        coverage=prototype.coverage,
        gamma=gamma,
    )
    g_eff = effective_g_with_contacts(g_sheet, h_contact)
    base = solve_asymmetric(
        0.0,
        prototype.h_dry_W_m2K,
        feed_total_g_h=feed_total_g_h,
    )
    advanced = solve_asymmetric(
        g_eff,
        prototype.h_dry_W_m2K,
        feed_total_g_h=feed_total_g_h,
    )
    mass_g = spreader_mass_g(
        GARMENT_AREA_M2,
        prototype.density_kg_m3,
        prototype.thickness_um,
        coverage=prototype.coverage,
    )
    gain_W_m2 = advanced.body_heat_flux_W_m2 - base.body_heat_flux_W_m2
    return {
        "classification": "SIMULATION/VIRTUAL_PROTOTYPE_V01",
        "prototype": prototype.name,
        "description": prototype.description,
        "feed_total_g_h": feed_total_g_h,
        "gamma": gamma,
        "k_parallel_W_mK": prototype.k_parallel_W_mK,
        "density_kg_m3": prototype.density_kg_m3,
        "thickness_um": prototype.thickness_um,
        "coverage": prototype.coverage,
        "routing_pitch_mm": prototype.routing_pitch_mm,
        "h_contact_W_m2K": h_contact,
        "h_dry_W_m2K": prototype.h_dry_W_m2K,
        "g_sheet_W_m2K": g_sheet,
        "g_eff_W_m2K": g_eff,
        "spreader_mass_g_over_0p30m2": mass_g,
        "bend_strain_R10mm_percent": prototype.thickness_um * 1e-6 / (2.0 * 0.010) * 100.0,
        "baseline_body_flux_W_m2": base.body_heat_flux_W_m2,
        "prototype_body_flux_W_m2": advanced.body_heat_flux_W_m2,
        "spreader_gain_W_m2": gain_W_m2,
        "spreader_gain_W_over_0p195m2": gain_W_m2 * DEFAULT_AREA_M2,
        "wet_fraction_beta": advanced.wet_fraction_beta,
        "evap_total_g_h": advanced.evap_total_g_h,
        "solver_converged": bool(base.converged and advanced.converged),
    }


def run_screen() -> pd.DataFrame:
    rows = []
    for prototype in PROTOTYPES:
        for feed in (50.0, 75.0, 100.0, 150.0):
            rows.append(evaluate_prototype(prototype, feed_total_g_h=feed))
    return pd.DataFrame(rows)


def run_robustness_screen() -> pd.DataFrame:
    rows = []
    for prototype in PROTOTYPES:
        for gamma in (2.0, 3.0, 4.0):
            for h_contact in (500.0, 1000.0, 2000.0, 5000.0):
                rows.append(
                    evaluate_prototype(
                        prototype,
                        feed_total_g_h=100.0,
                        gamma=gamma,
                        h_contact_override_W_m2K=h_contact,
                    )
                )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(run_screen().to_string(index=False))
    print("\nTopology/contact robustness at 100 g/h:")
    print(run_robustness_screen().to_string(index=False))
