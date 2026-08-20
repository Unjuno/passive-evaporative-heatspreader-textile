"""Compare pressure-aware evaporator relocation with a protected vapor path.

Virtual/computational screen only. The model asks how much wet-side ambient
access must be mechanically preserved under a synthetic backpack+strap load
for a central wet panel to match a pressure-aware relocated wet layout.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from simulations.spatial_pressure_layout import (
    C_INF,
    CONTACT_GAIN,
    H_CONTACT_0,
    H_DRY_0,
    H_WET_0,
    KM_WET_0,
    K_BACKGROUND_SHEET,
    K_HIGH_SHEET,
    L_V,
    T_AMBIENT_C,
    T_SKIN_C,
    U_BODY,
    WET_FRACTION,
    _exact_coverage,
    build_pressure_maps,
    build_route_mask,
    build_wet_layouts,
    drho_v_sat,
    rho_v_sat,
    PressureTile,
)


def _run_with_wet_air_floor(model: PressureTile, wet, air_floor, max_iterations=520,
                            tolerance=3e-6, relaxation=0.38):
    wet = np.asarray(wet, dtype=bool)
    n = model.n
    protected_air = np.maximum(model.air_scale, float(air_floor))
    h_wet = H_WET_0 * protected_air
    km_wet = KM_WET_0 * protected_air

    ts = np.full((n, n), 32.0)
    to = ts.copy()
    change = np.inf
    for it in range(max_iterations):
        h_ext = np.where(wet, h_wet, model.h_dry)
        outer = (model.h_contact*ts + h_ext*T_AMBIENT_C) / (model.h_contact + h_ext)
        for _ in range(12):
            evap = np.zeros_like(outer)
            evap[wet] = km_wet[wet] * np.maximum(rho_v_sat(outer[wet]) - C_INF, 0)
            active = np.zeros_like(wet)
            active[wet] = rho_v_sat(outer[wet]) > C_INF
            residual = model.h_contact*(ts-outer) + h_ext*(T_AMBIENT_C-outer) - L_V*evap
            derivative = -model.h_contact - h_ext - L_V*km_wet*drho_v_sat(outer)*active
            step = residual / derivative
            outer = np.clip(outer-step, 5, 55)
            if np.max(np.abs(step)) < 1e-10:
                break
        rhs = -U_BODY*T_SKIN_C*np.ones(n*n) - model.h_contact.ravel()*outer.ravel()
        ts_new = model.linear(rhs).reshape((n, n))
        change = max(float(np.max(np.abs(ts_new-ts))), float(np.max(np.abs(outer-to))))
        ts = (1-relaxation)*ts + relaxation*ts_new
        to = (1-relaxation)*to + relaxation*outer
        if change < tolerance:
            break

    evap = np.zeros_like(to)
    evap[wet] = km_wet[wet] * np.maximum(rho_v_sat(to[wet]) - C_INF, 0)
    return {
        "body_W_m2": float(np.mean(U_BODY*(T_SKIN_C-ts))),
        "evap_capacity_g_m2_h": float(np.mean(evap)*3.6e6),
        "mean_wet_air_scale": float(np.mean(protected_air[wet])),
        "converged": bool(change < tolerance),
    }


def run_protected_air_tradeoff(n=12, floors=None):
    if floors is None:
        floors = np.linspace(0.0, 1.0, 21)
    pressure = build_pressure_maps(n)["backpack_plus_straps"]
    route = build_route_mask(n)
    layouts = build_wet_layouts(n, pressure, route)
    center = layouts["center_panel"]
    aware = layouts["pressure_aware"]
    k_route = np.where(route, K_HIGH_SHEET, K_BACKGROUND_SHEET)
    model = PressureTile(k_route, pressure, cmax=0.5, air_exponent=2.0)
    background = PressureTile(np.full((n,n), K_BACKGROUND_SHEET), pressure, cmax=0.5, air_exponent=2.0)

    aware_state = model.run(aware)
    rows = []
    for floor in floors:
        routed = _run_with_wet_air_floor(model, center, floor)
        base = _run_with_wet_air_floor(background, center, floor)
        rows.append({
            "protected_air_floor": float(floor),
            "mean_wet_air_scale": routed["mean_wet_air_scale"],
            "center_body_W_m2": routed["body_W_m2"],
            "center_heat_routing_gain_W": (routed["body_W_m2"] - base["body_W_m2"]) * 0.195,
            "center_evap_capacity_g_m2_h": routed["evap_capacity_g_m2_h"],
            "pressure_aware_body_W_m2": aware_state["body_W_m2"],
            "body_difference_vs_relocation_W_m2": routed["body_W_m2"] - aware_state["body_W_m2"],
            "converged": routed["converged"] and base["converged"] and aware_state["converged"],
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(run_protected_air_tradeoff(n=24).to_csv(index=False))
