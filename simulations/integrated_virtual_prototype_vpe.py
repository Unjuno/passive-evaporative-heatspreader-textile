"""Integrated virtual prototype VP-E.

VP-E is a fixed computational design anchor, not a physical garment:
- lightly cross-linked directed heat-route topology;
- regularized pressure-aware wet-terminal geography;
- 8 local liquid cells with short 200 um-class trunks;
- pressure-resistant liquid escape margin represented by retained radius;
- ideal endpoint wet-terminal open/shield state selected by signed body heat flow;
- nominal pressure-relocation garment BOM.

The module combines existing low-order assumptions into one auditable design
sheet. It does not constitute independent validation of those assumptions.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import factorized

from simulations.capillary_liquid_network import required_parallel_channels
from simulations.spatial_pressure_layout import (
    CONTACT_GAIN,
    H_CONTACT_0,
    H_DRY_0,
    H_WET_0,
    KM_WET_0,
    K_BACKGROUND_SHEET,
    K_HIGH_SHEET,
    L_V,
    T_SKIN_C,
    U_BODY,
    _exact_coverage,
    _gaussian,
    _geometry,
    _harmonic,
    build_pressure_maps,
    build_route_mask,
    drho_v_sat,
    rho_v_sat,
)
from simulations.terminal_route_coddesign import regularized_wet_mask
from simulations.virtual_garment_bom import evaluate_design

VP_E = {
    "heat_network": "directed + limited cross-link",
    "route_blend": 0.125,
    "wet_layout": "regularized pressure-aware",
    "terminal_template_weight": 0.125,
    "terminal_route_weight": 0.35,
    "wet_fraction": 0.23,
    "liquid_cells": 8,
    "total_reference_flow_g_h": 150.0,
    "flow_per_cell_g_h": 18.75,
    "trunk_radius_um": 200.0,
    "trunk_path_mm": 30.0,
    "trunk_rise_mm": 15.0,
    "blockage_design_fraction": 0.30,
    "bom_assumption": "nominal",
    "bom_architecture": "pressure_relocation",
}


def _build_solver(k_sheet, h_contact, domain_m=0.060):
    k_sheet = np.asarray(k_sheet, dtype=float)
    n = k_sheet.shape[0]
    dx = domain_m / n
    rows, cols, vals = [], [], []
    def idx(j, i): return j*n+i
    for j in range(n):
        for i in range(n):
            p = idx(j, i)
            diag = -U_BODY - h_contact[j,i]
            for dj, di in ((0,1),(0,-1),(1,0),(-1,0)):
                jj, ii = (j+dj)%n, (i+di)%n
                c = _harmonic(k_sheet[j,i], k_sheet[jj,ii]) / dx**2
                rows.append(p); cols.append(idx(jj,ii)); vals.append(c)
                diag -= c
            rows.append(p); cols.append(p); vals.append(diag)
    return factorized(coo_matrix((vals,(rows,cols)), shape=(n*n,n*n)).tocsc())


def _vpe_geometry(n=12):
    pressure = build_pressure_maps(n)["backpack_plus_straps"]
    route = build_route_mask(n)
    wet = regularized_wet_mask(
        pressure,
        route,
        VP_E["terminal_template_weight"],
        VP_E["terminal_route_weight"],
    )
    compression = np.clip(0.5*pressure, 0, 0.95)
    air_scale = np.maximum((1-compression)**2, 1e-6)
    h_contact = H_CONTACT_0*(1+CONTACT_GAIN*compression)
    h_dry = H_DRY_0*air_scale
    k_route = np.where(route, K_HIGH_SHEET, K_BACKGROUND_SHEET)
    return pressure, route, wet, air_scale, h_contact, h_dry, k_route


def run_vpe_thermal_state(ambient_c=35.0, ambient_rh=0.70,
                          exposure_fraction=1.0, n=12):
    _, _, wet, air_scale, h_contact, h_dry, k_route = _vpe_geometry(n)
    h_wet = H_WET_0*air_scale*float(exposure_fraction)
    km_wet = KM_WET_0*air_scale*float(exposure_fraction)
    c_inf = float(ambient_rh*rho_v_sat(ambient_c))
    linear = _build_solver(k_route, h_contact)

    ts = np.full((n,n), 32.0)
    to = ts.copy()
    relaxation = 0.40
    change = np.inf
    for it in range(480):
        h_ext = np.where(wet, h_wet, h_dry)
        outer = (h_contact*ts + h_ext*ambient_c)/(h_contact+h_ext+1e-30)
        for _ in range(12):
            evap = np.zeros_like(outer)
            evap[wet] = km_wet[wet]*np.maximum(rho_v_sat(outer[wet])-c_inf,0.0)
            active = np.zeros_like(wet)
            active[wet] = rho_v_sat(outer[wet]) > c_inf
            residual = h_contact*(ts-outer) + h_ext*(ambient_c-outer) - L_V*evap
            derivative = -h_contact-h_ext-L_V*km_wet*drho_v_sat(outer)*active
            step = residual/derivative
            outer = np.clip(outer-step, 5, 60)
            if np.max(np.abs(step)) < 1e-10:
                break
        rhs = -U_BODY*T_SKIN_C*np.ones(n*n)-h_contact.ravel()*outer.ravel()
        ts_new = linear(rhs).reshape((n,n))
        change = max(float(np.max(np.abs(ts_new-ts))), float(np.max(np.abs(outer-to))))
        ts = (1-relaxation)*ts+relaxation*ts_new
        to = (1-relaxation)*to+relaxation*outer
        if change < 3e-6:
            break

    evap = np.zeros_like(to)
    evap[wet] = km_wet[wet]*np.maximum(rho_v_sat(to[wet])-c_inf,0.0)
    return {
        "ambient_C": ambient_c,
        "RH_percent": 100*ambient_rh,
        "exposure_fraction": exposure_fraction,
        "body_W_m2": float(np.mean(U_BODY*(T_SKIN_C-ts))),
        "evap_capacity_g_m2_h": float(np.mean(evap)*3.6e6),
        "converged": bool(change < 3e-6),
    }


def run_vpe_environment_map(n=12, environments=None):
    if environments is None:
        environments = [
            (35.0,.50),(35.0,.70),(35.0,.85),
            (40.0,.50),(40.0,.70),(40.0,.85),
            (45.0,.30),(45.0,.50),
        ]
    rows = []
    for t, rh in environments:
        opened = run_vpe_thermal_state(t, rh, 1.0, n)
        shielded = run_vpe_thermal_state(t, rh, 0.0, n)
        if opened["body_W_m2"] >= shielded["body_W_m2"]:
            selected = opened
            state = "open"
        else:
            selected = shielded
            state = "shield"
        rows.append({
            "ambient_C": t,
            "RH_percent": 100*rh,
            "open_body_W_m2": opened["body_W_m2"],
            "shield_body_W_m2": shielded["body_W_m2"],
            "selected_terminal_state": state,
            "selected_body_W_m2": selected["body_W_m2"],
            "open_evap_capacity_g_m2_h": opened["evap_capacity_g_m2_h"],
            "selected_evap_capacity_g_m2_h": selected["evap_capacity_g_m2_h"],
            "converged": opened["converged"] and shielded["converged"],
        })
    return pd.DataFrame(rows)


def vpe_liquid_margin(radius_retentions=(1.0,.90,.80,.70)):
    rows = []
    blockage = VP_E["blockage_design_fraction"]
    for retention in radius_retentions:
        live = required_parallel_channels(
            VP_E["flow_per_cell_g_h"],
            VP_E["trunk_path_mm"],
            VP_E["trunk_radius_um"]*retention,
            VP_E["trunk_rise_mm"],
        )
        installed = float(np.ceil(live/(1-blockage)))
        rows.append({
            "radius_retention": retention,
            "live_channels_per_cell": live,
            "installed_per_cell_for_30pct_blockage": installed,
            "installed_total_8cells": VP_E["liquid_cells"]*installed,
        })
    return pd.DataFrame(rows)


def vpe_bom():
    result = evaluate_design(VP_E["bom_assumption"], VP_E["bom_architecture"])
    result.pop("component_masses_g")
    return result


if __name__ == "__main__":
    print(run_vpe_environment_map(n=20).to_csv(index=False))
    print(vpe_liquid_margin().to_csv(index=False))
    print(vpe_bom())
