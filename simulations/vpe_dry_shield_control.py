"""VP-E2: independently control wet-terminal and dry-side ambient exposure.

Virtual/computational screen only. This model tests whether hostile hot/humid
performance can be improved by keeping wet terminals exposed for evaporation
while separately shielding dry garment regions from sensible ambient heat.

Wet exposure scales wet sensible and vapor exchange together; no physically
unsupported heat/mass selectivity is assumed.
"""
from __future__ import annotations

import numpy as np
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
    _harmonic,
    build_pressure_maps,
    build_route_mask,
    drho_v_sat,
    rho_v_sat,
)
from simulations.terminal_route_coddesign import regularized_wet_mask


def _solver_geometry(n=12, domain_m=0.060):
    pressure = build_pressure_maps(n)["backpack_plus_straps"]
    route = build_route_mask(n)
    wet = regularized_wet_mask(pressure, route, 0.125, 0.35)
    compression = np.clip(0.5*pressure, 0, 0.95)
    air_scale = np.maximum((1-compression)**2, 1e-6)
    h_contact = H_CONTACT_0*(1+CONTACT_GAIN*compression)
    k_sheet = np.where(route, K_HIGH_SHEET, K_BACKGROUND_SHEET)
    dx = domain_m/n
    rows, cols, vals = [], [], []
    def idx(j, i): return j*n+i
    for j in range(n):
        for i in range(n):
            p = idx(j,i)
            diag = -U_BODY-h_contact[j,i]
            for dj, di in ((0,1),(0,-1),(1,0),(-1,0)):
                jj, ii = (j+dj)%n, (i+di)%n
                c = _harmonic(k_sheet[j,i], k_sheet[jj,ii])/dx**2
                rows.append(p); cols.append(idx(jj,ii)); vals.append(c)
                diag -= c
            rows.append(p); cols.append(p); vals.append(diag)
    linear = factorized(coo_matrix((vals,(rows,cols)), shape=(n*n,n*n)).tocsc())
    return wet, air_scale, h_contact, linear


def run_vpe2_state(ambient_c=40.0, ambient_rh=0.70,
                   wet_exposure=1.0, dry_exposure=1.0, n=12):
    wet, air_scale, h_contact, linear = _solver_geometry(n)
    h_wet = H_WET_0*air_scale*float(wet_exposure)
    km_wet = KM_WET_0*air_scale*float(wet_exposure)
    h_dry = H_DRY_0*air_scale*float(dry_exposure)
    c_inf = float(ambient_rh*rho_v_sat(ambient_c))

    ts = np.full((n,n),32.0)
    to = ts.copy()
    relaxation = 0.45
    change = np.inf
    for it in range(420):
        h_ext = np.where(wet,h_wet,h_dry)
        outer = (h_contact*ts+h_ext*ambient_c)/(h_contact+h_ext+1e-30)
        for _ in range(10):
            evap = np.zeros_like(outer)
            evap[wet] = km_wet[wet]*np.maximum(rho_v_sat(outer[wet])-c_inf,0.0)
            active = np.zeros_like(wet)
            active[wet] = rho_v_sat(outer[wet]) > c_inf
            residual = h_contact*(ts-outer)+h_ext*(ambient_c-outer)-L_V*evap
            derivative = -h_contact-h_ext-L_V*km_wet*drho_v_sat(outer)*active
            step = residual/derivative
            outer = np.clip(outer-step,5,60)
            if np.max(np.abs(step)) < 1e-10:
                break
        rhs = -U_BODY*T_SKIN_C*np.ones(n*n)-h_contact.ravel()*outer.ravel()
        ts_new = linear(rhs).reshape((n,n))
        change = max(float(np.max(np.abs(ts_new-ts))), float(np.max(np.abs(outer-to))))
        ts = (1-relaxation)*ts+relaxation*ts_new
        to = (1-relaxation)*to+relaxation*outer
        if change < 4e-6:
            break

    evap = np.zeros_like(to)
    evap[wet] = km_wet[wet]*np.maximum(rho_v_sat(to[wet])-c_inf,0.0)
    return {
        "ambient_C": ambient_c,
        "RH_percent": 100*ambient_rh,
        "wet_exposure": wet_exposure,
        "dry_exposure": dry_exposure,
        "body_W_m2": float(np.mean(U_BODY*(T_SKIN_C-ts))),
        "evap_capacity_g_m2_h": float(np.mean(evap)*3.6e6),
        "converged": bool(change < 4e-6),
    }


if __name__ == "__main__":
    for state in (
        run_vpe2_state(35,.70,1,0),
        run_vpe2_state(40,.70,1,1),
        run_vpe2_state(40,.70,1,0),
        run_vpe2_state(40,.70,0,0),
    ):
        print(state)
