"""Mass-conserving transient water-delivery / terminal-buffer screen.

Virtual/computational model only. This model adds time dependence to the current
VP-E steady-state anchors. Water is explicitly conserved between a transport-line
inventory, terminal storage, evaporation and overflow/drain.

The transport and thermal time constants are screening variables, not measured
textile properties.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from simulations.integrated_virtual_prototype_vpe import (
    run_vpe_thermal_state,
    vpe_bom,
)

DEFAULT_STRUCTURED_AREA_M2 = 0.195


def lucas_washburn_time_s(
    length_mm: float,
    radius_um: float,
    mu_pa_s: float = 0.9e-3,
    gamma_n_m: float = 0.070,
    contact_angle_deg: float = 30.0,
) -> float:
    """Ideal horizontal Lucas-Washburn lower-bound filling time."""
    length = float(length_mm) * 1e-3
    radius = float(radius_um) * 1e-6
    theta = np.deg2rad(contact_angle_deg)
    return float(2.0*mu_pa_s*length**2/(gamma_n_m*radius*np.cos(theta)))


def default_sweat_schedule_g_h(time_min: float) -> float:
    """Reference pulse: 10 min baseline, 30 min high feed, then stop."""
    if time_min < 10.0:
        return 10.0
    if time_min < 40.0:
        return 100.0
    return 0.0


def simulate_terminal_buffer(
    tau_liquid_min: float = 2.0,
    tau_thermal_min: float = 2.0,
    terminal_storage_g: float | None = None,
    ambient_c: float = 35.0,
    ambient_rh: float = 0.70,
    structured_area_m2: float = DEFAULT_STRUCTURED_AREA_M2,
    dt_s: float = 2.0,
    total_min: float = 120.0,
    sweat_schedule=default_sweat_schedule_g_h,
) -> pd.DataFrame:
    opened = run_vpe_thermal_state(ambient_c, ambient_rh, 1.0, n=12)
    dry = run_vpe_thermal_state(ambient_c, ambient_rh, 0.0, n=12)
    q_open = float(opened["body_W_m2"])
    q_dry = float(dry["body_W_m2"])
    evap_capacity_g_h = float(opened["evap_capacity_g_m2_h"])*float(structured_area_m2)

    if terminal_storage_g is None:
        terminal_storage_g = float(vpe_bom()["operating_water_hold_up_g"])
    terminal_storage_g = max(0.0, float(terminal_storage_g))

    dt_h = float(dt_s)/3600.0
    tau_h = float(tau_liquid_min)/60.0
    line_inventory = 0.0
    terminal_inventory = 0.0
    q_body = q_dry
    cumulative_source = 0.0
    cumulative_evap = 0.0
    cumulative_overflow = 0.0
    rows = []

    steps = int(float(total_min)*60.0/float(dt_s)) + 1
    for k in range(steps):
        time_min = k*float(dt_s)/60.0
        source = max(0.0, float(sweat_schedule(time_min)))

        if tau_h <= 0.0:
            delivered = source
        else:
            delivered = line_inventory/tau_h
            line_inventory = max(
                0.0,
                line_inventory + (source-delivered)*dt_h,
            )

        if terminal_inventory > 1e-12:
            evap = evap_capacity_g_h
        else:
            evap = min(delivered, evap_capacity_g_h)

        next_terminal = terminal_inventory + (delivered-evap)*dt_h
        overflow = 0.0
        if next_terminal > terminal_storage_g:
            overflow = (next_terminal-terminal_storage_g)/dt_h
            next_terminal = terminal_storage_g
        if next_terminal < 0.0:
            evap = min(evap_capacity_g_h, delivered+terminal_inventory/dt_h)
            next_terminal = 0.0
        terminal_inventory = next_terminal

        wet_fraction = (
            float(np.clip(evap/evap_capacity_g_h, 0.0, 1.0))
            if evap_capacity_g_h > 0.0 else 0.0
        )
        target = q_dry + wet_fraction*(q_open-q_dry)
        if tau_thermal_min <= 0.0:
            q_body = target
        else:
            q_body += (target-q_body)*float(dt_s)/(float(tau_thermal_min)*60.0)

        cumulative_source += source*dt_h
        cumulative_evap += evap*dt_h
        cumulative_overflow += overflow*dt_h
        mass_error = (
            cumulative_source
            - cumulative_evap
            - cumulative_overflow
            - line_inventory
            - terminal_inventory
        )
        rows.append({
            "time_min": time_min,
            "source_g_h": source,
            "delivered_g_h": delivered,
            "line_inventory_g": line_inventory,
            "terminal_inventory_g": terminal_inventory,
            "evap_g_h": evap,
            "overflow_g_h": overflow,
            "wet_fraction_proxy": wet_fraction,
            "body_W_m2": q_body,
            "cumulative_source_g": cumulative_source,
            "cumulative_evap_g": cumulative_evap,
            "cumulative_overflow_g": cumulative_overflow,
            "mass_balance_error_g": mass_error,
        })
    return pd.DataFrame(rows)


def storage_capacity_screen(
    capacities_g=(0.0, 2.0, 4.0, 8.0, 12.42, 20.0),
    tau_liquid_min: float = 2.0,
    tau_thermal_min: float = 2.0,
) -> pd.DataFrame:
    dry = run_vpe_thermal_state(35.0, 0.70, 0.0, n=12)["body_W_m2"]
    wet = run_vpe_thermal_state(35.0, 0.70, 1.0, n=12)["body_W_m2"]
    half = dry + 0.5*(wet-dry)
    rows = []
    for capacity in capacities_g:
        table = simulate_terminal_buffer(
            tau_liquid_min=tau_liquid_min,
            tau_thermal_min=tau_thermal_min,
            terminal_storage_g=float(capacity),
            total_min=150.0,
        )
        after = table[table["time_min"] >= 40.0]
        below = after[after["body_W_m2"] <= half]
        half_time = np.nan if below.empty else float(below["time_min"].iloc[0]-40.0)
        rows.append({
            "terminal_storage_capacity_g": float(capacity),
            "time_after_stop_to_half_body_flux_min": half_time,
            "total_evaporated_g": float(table["cumulative_evap_g"].iloc[-1]),
            "total_overflow_g": float(table["cumulative_overflow_g"].iloc[-1]),
            "max_mass_balance_error_g": float(np.max(np.abs(table["mass_balance_error_g"]))),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(storage_capacity_screen().to_csv(index=False))
