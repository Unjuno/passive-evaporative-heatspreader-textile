"""Virtual garment bill-of-materials and thickness budget.

Computational design-budget model only. All component areal masses, densities,
thicknesses and water hold-up values are explicit design assumptions, not
measured materials or finished-garment specifications.

The thermal/liquid screens elsewhere use ~0.30 m² functional active area; this
BOM allows the base shirt shell area to be larger than the active functional
area.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

ACTIVE_AREA_M2 = 0.30
WET_FRACTION = 0.23
WET_AREA_M2 = ACTIVE_AREA_M2 * WET_FRACTION
HIGH_K_COVERAGE = 0.35
DRY_FRACTION = 1.0 - WET_FRACTION

ASSUMPTION_SETS = {
    "lean": {
        "garment_area_m2": 0.65,
        "base_textile_g_m2": 115.0,
        "directional_layer_g_m2": 25.0,
        "heat_density_kg_m3": 1500.0,
        "heat_thickness_um": 60.0,
        "capillary_structure_g_m2_active": 15.0,
        "terminal_microtexture_g_m2_local": 70.0,
        "encapsulation_g_m2_route": 15.0,
        "dry_shield_g_m2_dry_active": 20.0,
        "water_equivalent_mm": 0.08,
        "base_thickness_mm": 0.55,
        "directional_thickness_mm": 0.20,
        "capillary_plane_thickness_mm": 0.25,
        "encapsulation_thickness_mm": 0.05,
        "shield_thickness_mm": 0.15,
        "terminal_height_mm": 2.0,
    },
    "nominal": {
        "garment_area_m2": 0.75,
        "base_textile_g_m2": 145.0,
        "directional_layer_g_m2": 45.0,
        "heat_density_kg_m3": 1600.0,
        "heat_thickness_um": 100.0,
        "capillary_structure_g_m2_active": 30.0,
        "terminal_microtexture_g_m2_local": 120.0,
        "encapsulation_g_m2_route": 30.0,
        "dry_shield_g_m2_dry_active": 40.0,
        "water_equivalent_mm": 0.18,
        "base_thickness_mm": 0.75,
        "directional_thickness_mm": 0.30,
        "capillary_plane_thickness_mm": 0.40,
        "encapsulation_thickness_mm": 0.08,
        "shield_thickness_mm": 0.25,
        "terminal_height_mm": 2.5,
    },
    "conservative": {
        "garment_area_m2": 0.90,
        "base_textile_g_m2": 185.0,
        "directional_layer_g_m2": 70.0,
        "heat_density_kg_m3": 1800.0,
        "heat_thickness_um": 160.0,
        "capillary_structure_g_m2_active": 60.0,
        "terminal_microtexture_g_m2_local": 220.0,
        "encapsulation_g_m2_route": 55.0,
        "dry_shield_g_m2_dry_active": 70.0,
        "water_equivalent_mm": 0.35,
        "base_thickness_mm": 1.00,
        "directional_thickness_mm": 0.45,
        "capillary_plane_thickness_mm": 0.70,
        "encapsulation_thickness_mm": 0.12,
        "shield_thickness_mm": 0.40,
        "terminal_height_mm": 3.0,
    },
}

ARCHITECTURES = {
    "pressure_relocation": {
        "support_fraction": 0.0,
        "support_height_mm": 0.0,
        "support_fill": 0.0,
        "support_density_kg_m3": 1200.0,
        "protected_gap_mm": 0.0,
    },
    "protected_under_load": {
        "support_fraction": 0.05,
        "support_height_mm": 2.5,
        "support_fill": 0.30,
        "support_density_kg_m3": 1200.0,
        "protected_gap_mm": 2.5,
    },
}


def heat_route_mass_g(density_kg_m3, thickness_um, coverage=HIGH_K_COVERAGE,
                      active_area_m2=ACTIVE_AREA_M2):
    return active_area_m2 * density_kg_m3 * thickness_um * 1e-6 * coverage * 1000.0


def support_mass_g(support_fraction, height_mm, fill_fraction, density_kg_m3,
                   wet_area_m2=WET_AREA_M2):
    volume_m3 = wet_area_m2 * support_fraction * height_mm * 1e-3 * fill_fraction
    return volume_m3 * density_kg_m3 * 1000.0


def water_hold_up_g(equivalent_water_mm, wet_area_m2=WET_AREA_M2):
    return wet_area_m2 * equivalent_water_mm * 1e-3 * 1000.0 * 1000.0


def evaluate_design(assumption="nominal", architecture="pressure_relocation"):
    a = ASSUMPTION_SETS[assumption]
    arch = ARCHITECTURES[architecture]
    masses = {
        "base_textile": a["garment_area_m2"] * a["base_textile_g_m2"],
        "directional_collection": ACTIVE_AREA_M2 * a["directional_layer_g_m2"],
        "heat_routes": heat_route_mass_g(a["heat_density_kg_m3"], a["heat_thickness_um"]),
        "capillary_structure": ACTIVE_AREA_M2 * a["capillary_structure_g_m2_active"],
        "terminal_microtexture": WET_AREA_M2 * a["terminal_microtexture_g_m2_local"],
        "heat_route_encapsulation": ACTIVE_AREA_M2 * HIGH_K_COVERAGE * a["encapsulation_g_m2_route"],
        "dry_side_shield": ACTIVE_AREA_M2 * DRY_FRACTION * a["dry_shield_g_m2_dry_active"],
        "support_skeleton": support_mass_g(
            arch["support_fraction"], arch["support_height_mm"],
            arch["support_fill"], arch["support_density_kg_m3"]
        ),
        "operating_water_hold_up": water_hold_up_g(a["water_equivalent_mm"]),
    }
    dry_mass = sum(v for k,v in masses.items() if k != "operating_water_hold_up")
    operating_mass = sum(masses.values())
    base_mass = masses["base_textile"]
    heat_route_thickness_mm = a["heat_thickness_um"] / 1000.0
    dry_stack = (
        a["base_thickness_mm"] + a["directional_thickness_mm"]
        + a["capillary_plane_thickness_mm"] + heat_route_thickness_mm
        + a["encapsulation_thickness_mm"] + a["shield_thickness_mm"]
    )
    wet_stack = (
        a["base_thickness_mm"] + a["directional_thickness_mm"]
        + a["capillary_plane_thickness_mm"] + heat_route_thickness_mm
        + a["encapsulation_thickness_mm"] + a["terminal_height_mm"]
        + arch["protected_gap_mm"]
    )
    return {
        "assumption_set": assumption,
        "architecture": architecture,
        "garment_area_m2": a["garment_area_m2"],
        "functional_active_area_m2": ACTIVE_AREA_M2,
        "wet_area_m2": WET_AREA_M2,
        "dry_mass_g": dry_mass,
        "operating_water_hold_up_g": masses["operating_water_hold_up"],
        "operating_mass_g": operating_mass,
        "base_textile_mass_g": base_mass,
        "added_functional_dry_mass_g": dry_mass - base_mass,
        "added_functional_dry_mass_g_m2_active": (dry_mass-base_mass)/ACTIVE_AREA_M2,
        "dry_zone_peak_stack_mm": dry_stack,
        "wet_terminal_peak_stack_mm": wet_stack,
        "support_fraction_of_wet_footprint": arch["support_fraction"],
        "component_masses_g": masses,
    }


def run_bom_summary():
    rows = []
    for assumption in ASSUMPTION_SETS:
        for architecture in ARCHITECTURES:
            result = evaluate_design(assumption, architecture).copy()
            result.pop("component_masses_g")
            rows.append(result)
    return pd.DataFrame(rows)


def heat_route_mass_for_target_gmix(target_gmix_W_m2K, routing_pitch_mm,
                                    k_W_mK, density_kg_m3,
                                    gamma_topology=4.0,
                                    active_area_m2=ACTIVE_AREA_M2):
    """Ideal route mass implied by g ~= Gamma*k*t*c/P^2.

    Coverage cancels from mass when effective conductivity scales linearly with
    coverage: m=A*rho*(t*c)=A*rho*g*P^2/(Gamma*k).
    """
    pitch_m = float(routing_pitch_mm) * 1e-3
    return (
        active_area_m2 * density_kg_m3 * target_gmix_W_m2K * pitch_m**2
        / (gamma_topology * k_W_mK) * 1000.0
    )


if __name__ == "__main__":
    print(run_bom_summary().to_csv(index=False))
