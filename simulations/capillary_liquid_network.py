"""Passive capillary liquid-routing screen.

Virtual/computational mechanism model only. The model treats sweat-like liquid
as an incompressible Newtonian fluid moving through N parallel cylindrical
capillaries. Capillary pressure must overcome hydrostatic head and a chosen
safety factor on viscous pressure drop.

This is a design-burden screen, not a claim that a real knitted/woven textile
contains ideal cylindrical tubes or has the default material properties below.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

MU_PA_S = 0.9e-3
SURFACE_TENSION_N_M = 0.070
DENSITY_KG_M3 = 1000.0
G_M_S2 = 9.80665
CONTACT_ANGLE_DEG = 30.0
DEFAULT_SAFETY_FACTOR = 3.0


def flow_m3_s_from_g_h(flow_g_h: float, density_kg_m3: float = DENSITY_KG_M3) -> float:
    return (float(flow_g_h) / 1000.0 / 3600.0) / density_kg_m3


def capillary_pressure_pa(radius_um: float, surface_tension_n_m: float = SURFACE_TENSION_N_M,
                          contact_angle_deg: float = CONTACT_ANGLE_DEG) -> float:
    r = float(radius_um) * 1e-6
    return 2.0 * surface_tension_n_m * np.cos(np.deg2rad(contact_angle_deg)) / r


def hydrostatic_pressure_pa(vertical_rise_mm: float, density_kg_m3: float = DENSITY_KG_M3) -> float:
    return density_kg_m3 * G_M_S2 * float(vertical_rise_mm) * 1e-3


def viscous_pressure_drop_pa(flow_g_h: float, path_mm: float, radius_um: float,
                             n_channels: float, viscosity_pa_s: float = MU_PA_S) -> float:
    q = flow_m3_s_from_g_h(flow_g_h)
    length = float(path_mm) * 1e-3
    radius = float(radius_um) * 1e-6
    return 8.0 * viscosity_pa_s * length * q / (np.pi * radius**4 * float(n_channels))


def available_capillary_pressure_pa(radius_um: float, vertical_rise_mm: float) -> float:
    return capillary_pressure_pa(radius_um) - hydrostatic_pressure_pa(vertical_rise_mm)


def required_parallel_channels(flow_g_h: float, path_mm: float, radius_um: float,
                               vertical_rise_mm: float = 0.0,
                               safety_factor: float = DEFAULT_SAFETY_FACTOR) -> float:
    available = available_capillary_pressure_pa(radius_um, vertical_rise_mm)
    if available <= 0:
        return np.inf
    q = flow_m3_s_from_g_h(flow_g_h)
    length = float(path_mm) * 1e-3
    radius = float(radius_um) * 1e-6
    continuous = (
        safety_factor * 8.0 * MU_PA_S * length * q
        / (np.pi * radius**4 * available)
    )
    return float(np.ceil(continuous))


def liquid_inventory_ml(path_mm: float, radius_um: float, n_channels: float) -> float:
    if not np.isfinite(n_channels):
        return np.inf
    length = float(path_mm) * 1e-3
    radius = float(radius_um) * 1e-6
    return float(n_channels) * np.pi * radius**2 * length * 1e6


def static_capillary_rise_limit_mm(radius_um: float) -> float:
    return capillary_pressure_pa(radius_um) / (DENSITY_KG_M3 * G_M_S2) * 1000.0


def run_capillary_screen(
    flows_g_h=(75.0, 150.0, 300.0),
    paths_mm=(20.0, 50.0, 100.0, 200.0),
    rises_mm=(0.0, 25.0, 50.0, 100.0, 200.0, 500.0),
    radii_um=(20.0, 30.0, 50.0, 75.0, 100.0, 150.0, 200.0, 300.0),
    safety_factor: float = DEFAULT_SAFETY_FACTOR,
) -> pd.DataFrame:
    rows = []
    for flow in flows_g_h:
        for path in paths_mm:
            for rise in rises_mm:
                for radius in radii_um:
                    n = required_parallel_channels(flow, path, radius, rise, safety_factor)
                    rows.append({
                        "flow_g_h": flow,
                        "path_mm": path,
                        "vertical_rise_mm": rise,
                        "radius_um": radius,
                        "capillary_pressure_Pa": capillary_pressure_pa(radius),
                        "hydrostatic_pressure_Pa": hydrostatic_pressure_pa(rise),
                        "available_pressure_Pa": available_capillary_pressure_pa(radius, rise),
                        "required_channels": n,
                        "liquid_inventory_ml": liquid_inventory_ml(path, radius, n),
                        "static_capillary_rise_limit_mm": static_capillary_rise_limit_mm(radius),
                        "safety_factor": safety_factor,
                    })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(run_capillary_screen().to_csv(index=False))
