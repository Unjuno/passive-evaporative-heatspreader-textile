"""Environment-dependent wet-terminal exposure screen under a loaded tile.

Virtual/computational screen only. Uses the same synthetic backpack+strap
pressure field and routed high-k sheet as the pressure-layout model, but allows
ambient temperature/RH and a global wet-terminal exposure fraction to vary.

Exposure scales wet-side sensible and vapor exchange together; it does not
represent a selective membrane. Dry-side exposure remains unchanged, so a
closed wet terminal can still have negative body heat flow in hostile ambient
conditions.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import factorized

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
    _harmonic,
    build_pressure_maps,
    build_route_mask,
    drho_v_sat,
    rho_v_sat,
)


def _build_solver(k_sheet, h_contact, domain_m=0.060):
    k_sheet = np.asarray(k_sheet, dtype=float)
    n = k_sheet.shape[0]
    dx = domain_m / n
    rows, cols, vals = [], [], []
    def idx(j, i): return j*n + i
    for j in range(n):
        for i in range(n):
            p = idx(j, i)
            diag = -U_BODY - h_contact[j, i]
            for dj, di in ((0,1),(0,-1),(1,0),(-1,0)):
                jj, ii = (j+dj)%n, (i+di)%n
                c = _harmonic(k_sheet[j,i], k_sheet[jj,ii]) / dx**2
                rows.append(p); cols.append(idx(jj,ii)); vals.append(c)
                diag -= c
            rows.append(p); cols.append(p); vals.append(diag)
    return factorized(coo_matrix((vals,(rows,cols)), shape=(n*n,n*n)).tocsc())


def pressure_focused_mask(n=12):
    pressure = build_pressure_maps(n)["backpack_plus_straps"]
    route = build_route_mask(n)
    return _exact_coverage((1.0-pressure)+0.20*route.astype(float), 0.23)


def run_loaded_exposure_case(n=12, ambient_c=35.0, ambient_rh=0.70,
                             exposure_fraction=1.0):
    pressure = build_pressure_maps(n)["backpack_plus_straps"]
    route = build_route_mask(n)
    wet = pressure_focused_mask(n)
    compression = np.clip(0.5*pressure, 0, 0.95)
    air_scale = np.maximum((1.0-compression)**2, 1e-6)
    h_contact = H_CONTACT_0*(1.0+CONTACT_GAIN*compression)
    h_dry = H_DRY_0*air_scale
    h_wet = H_WET_0*air_scale*float(exposure_fraction)
    km_wet = KM_WET_0*air_scale*float(exposure_fraction)
    c_inf = float(ambient_rh*rho_v_sat(ambient_c))

    k_route = np.where(route, K_HIGH_SHEET, K_BACKGROUND_SHEET)
    linear = _build_solver(k_route, h_contact)
    ts = np.full((n,n), 32.0)
    to = ts.copy()
    relaxation = 0.40
    change = np.inf

    for it in range(480):
        h_ext = np.where(wet, h_wet, h_dry)
        outer = (h_contact*ts+h_ext*ambient_c)/(h_contact+h_ext+1e-30)
        for _ in range(12):
            evap = np.zeros_like(outer)
            evap[wet] = km_wet[wet]*np.maximum(rho_v_sat(outer[wet])-c_inf, 0.0)
            active = np.zeros_like(wet)
            active[wet] = rho_v_sat(outer[wet]) > c_inf
            residual = h_contact*(ts-outer)+h_ext*(ambient_c-outer)-L_V*evap
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
    evap[wet] = km_wet[wet]*np.maximum(rho_v_sat(to[wet])-c_inf, 0.0)
    return {
        "ambient_C": ambient_c,
        "RH_percent": 100*ambient_rh,
        "exposure_fraction": exposure_fraction,
        "body_W_m2": float(np.mean(U_BODY*(T_SKIN_C-ts))),
        "evap_capacity_g_m2_h": float(np.mean(evap)*3.6e6),
        "converged": bool(change < 3e-6),
    }


def run_environment_sweep(n=12, environments=None, exposures=None):
    if environments is None:
        environments = [
            (35.0,.50),(35.0,.70),(35.0,.85),
            (40.0,.50),(40.0,.70),(40.0,.85),
            (45.0,.30),(45.0,.50),
        ]
    if exposures is None:
        exposures = np.concatenate(([0.0], np.geomspace(0.01,1.0,25)))
    rows = []
    for t, rh in environments:
        for exposure in exposures:
            rows.append(run_loaded_exposure_case(n, t, rh, float(exposure)))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(run_environment_sweep(n=20).to_csv(index=False))
