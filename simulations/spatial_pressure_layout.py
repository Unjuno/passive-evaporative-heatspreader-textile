"""Spatial pressure-map screen for passive evaporative heat-spreader textiles.

Virtual/computational mechanism model only. Normalized pressure produces two
competing local effects: improved solid thermal contact and reduced ambient
heat/vapor access. Equal-area wet layouts are compared under synthetic
backpack, shoulder-strap and seat-back pressure maps.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import factorized

D_V = 2.80e-5
K_AIR = 0.027
L_V = 2.42e6
R_V = 461.5
NU_SCREEN = SH_SCREEN = 7.54
U_BODY = 100.0
T_SKIN_C = 34.0
T_AMBIENT_C = 35.0
RH_AMBIENT = 0.50
K_HIGH_SHEET = 300.0 * 100e-6
K_BACKGROUND_SHEET = 0.2 * 500e-6
H_CONTACT_0 = 800.0
H_DRY_0 = 5.0
CONTACT_GAIN = 2.0
HIGH_K_FRACTION = 0.35
WET_FRACTION = 0.23


def p_sat(t_c):
    t_c = np.asarray(t_c, dtype=float)
    return 611.21 * np.exp((18.678 - t_c / 234.5) * (t_c / (257.14 + t_c)))


def rho_v_sat(t_c):
    t_c = np.asarray(t_c, dtype=float)
    return p_sat(t_c) / (R_V * (t_c + 273.15))


def drho_v_sat(t_c):
    eps = 1e-3
    t_c = np.asarray(t_c, dtype=float)
    return (rho_v_sat(t_c + eps) - rho_v_sat(t_c - eps)) / (2 * eps)


_WIDTH = 6e-3
_DEPTH = 3e-3
_DH = 4 * _WIDTH * _DEPTH / (2 * (_WIDTH + _DEPTH))
_H_WALL = NU_SCREEN * K_AIR / _DH
_H_LATERAL = K_AIR / 0.5e-3
H_WET_0 = _H_WALL * _H_LATERAL / (_H_WALL + _H_LATERAL)
_KM_WALL = SH_SCREEN * D_V / _DH
_KM_LATERAL = D_V / 0.5e-3
KM_WET_0 = _KM_WALL * _KM_LATERAL / (_KM_WALL + _KM_LATERAL)
C_INF = RH_AMBIENT * float(rho_v_sat(T_AMBIENT_C))


def _exact_coverage(score, fraction):
    count = int(round(fraction * score.size))
    idx = np.argpartition(score.ravel(), -count)[-count:]
    out = np.zeros(score.size, dtype=bool)
    out[idx] = True
    return out.reshape(score.shape)


def _harmonic(a, b):
    return 2 * a * b / (a + b + 1e-30)


def _geometry(n):
    jj, ii = np.mgrid[0:n, 0:n]
    return (ii + 0.5) / n, (jj + 0.5) / n


def _gaussian(x, y, cx, cy, sx, sy):
    return np.exp(-0.5 * (((x - cx) / sx) ** 2 + ((y - cy) / sy) ** 2))


def build_pressure_maps(n=12):
    x, y = _geometry(n)
    g = lambda cx, cy, sx, sy: _gaussian(x, y, cx, cy, sx, sy)
    maps = {
        "none": np.zeros((n, n)),
        "backpack_panel": np.clip(g(0.50, 0.52, 0.25, 0.32), 0, 1),
        "shoulder_straps": np.clip(g(0.30, 0.30, 0.07, 0.34) + g(0.70, 0.30, 0.07, 0.34), 0, 1),
        "seat_back": np.clip(g(0.50, 0.72, 0.28, 0.18), 0, 1),
    }
    maps["backpack_plus_straps"] = np.clip(
        0.75 * maps["backpack_panel"] + 0.65 * maps["shoulder_straps"], 0, 1
    )
    return maps


def _distance_to_segment(x, y, a, b):
    ax, ay = a
    bx, by = b
    vx, vy = bx - ax, by - ay
    t = np.clip(((x - ax) * vx + (y - ay) * vy) / (vx * vx + vy * vy + 1e-30), 0, 1)
    return np.sqrt((x - (ax + t * vx)) ** 2 + (y - (ay + t * vy)) ** 2)


def build_route_mask(n=12):
    x, y = _geometry(n)
    segments = [
        ((0.0, 0.25), (1.0, 0.25)), ((0.0, 0.75), (1.0, 0.75)),
        ((0.25, 0.0), (0.25, 1.0)), ((0.75, 0.0), (0.75, 1.0)),
    ]
    directed = np.zeros((n, n))
    for a, b in segments:
        d = _distance_to_segment(x, y, a, b)
        directed = np.maximum(directed, np.exp(-(d / 0.028) ** 2))
    mesh = np.maximum(np.cos(2 * np.pi * 4 * x) ** 10, np.cos(2 * np.pi * 4 * y) ** 10)
    directed = (directed - directed.min()) / (directed.max() - directed.min() + 1e-30)
    mesh = (mesh - mesh.min()) / (mesh.max() - mesh.min() + 1e-30)
    return _exact_coverage(0.875 * directed + 0.125 * mesh, HIGH_K_FRACTION)


def build_wet_layouts(n=12, pressure=None, route_mask=None):
    x, y = _geometry(n)
    g = lambda cx, cy, sx, sy: _gaussian(x, y, cx, cy, sx, sy)
    four = np.maximum.reduce([g(.25,.25,.10,.10), g(.75,.25,.10,.10), g(.25,.75,.10,.10), g(.75,.75,.10,.10)])
    peripheral = np.maximum.reduce([g(.13,.25,.10,.13), g(.87,.25,.10,.13), g(.13,.75,.10,.13), g(.87,.75,.10,.13)])
    layouts = {
        "four_islands": _exact_coverage(four, WET_FRACTION),
        "peripheral_islands": _exact_coverage(peripheral, WET_FRACTION),
        "center_panel": _exact_coverage(g(.5,.5,.20,.20), WET_FRACTION),
        "upper_lower_bands": _exact_coverage(np.maximum(g(.5,.16,.23,.08), g(.5,.84,.23,.08)), WET_FRACTION),
        "side_columns": _exact_coverage(np.maximum(g(.12,.5,.09,.28), g(.88,.5,.09,.28)), WET_FRACTION),
    }
    if pressure is not None:
        if route_mask is None:
            route_mask = build_route_mask(n)
        layouts["pressure_aware"] = _exact_coverage(
            (1.0 - pressure) + 0.18 * route_mask.astype(float), WET_FRACTION
        )
    return layouts


class PressureTile:
    def __init__(self, k_sheet, pressure, cmax=0.5, air_exponent=2.0, domain_m=0.060):
        self.k_sheet = np.asarray(k_sheet, dtype=float)
        self.n = self.k_sheet.shape[0]
        self.dx = domain_m / self.n
        self.compression = np.clip(cmax * np.asarray(pressure, dtype=float), 0, 0.95)
        self.air_scale = np.maximum((1 - self.compression) ** air_exponent, 1e-6)
        self.h_contact = H_CONTACT_0 * (1 + CONTACT_GAIN * self.compression)
        self.h_wet = H_WET_0 * self.air_scale
        self.km_wet = KM_WET_0 * self.air_scale
        self.h_dry = H_DRY_0 * self.air_scale
        self.linear = self._build_solver()

    def _build_solver(self):
        n = self.n
        rows, cols, vals = [], [], []
        def idx(j, i): return j * n + i
        for j in range(n):
            for i in range(n):
                p = idx(j, i)
                diag = -U_BODY - self.h_contact[j, i]
                for dj, di in ((0,1),(0,-1),(1,0),(-1,0)):
                    jj, ii = (j + dj) % n, (i + di) % n
                    c = _harmonic(self.k_sheet[j,i], self.k_sheet[jj,ii]) / self.dx**2
                    rows.append(p); cols.append(idx(jj,ii)); vals.append(c)
                    diag -= c
                rows.append(p); cols.append(p); vals.append(diag)
        return factorized(coo_matrix((vals, (rows, cols)), shape=(n*n, n*n)).tocsc())

    def run(self, wet, max_iterations=520, tolerance=3e-6, relaxation=0.38):
        n = self.n
        wet = np.asarray(wet, dtype=bool)
        ts = np.full((n, n), 32.0)
        to = ts.copy()
        change = np.inf
        for it in range(max_iterations):
            h_ext = np.where(wet, self.h_wet, self.h_dry)
            outer = (self.h_contact * ts + h_ext * T_AMBIENT_C) / (self.h_contact + h_ext)
            for _ in range(12):
                evap = np.zeros_like(outer)
                evap[wet] = self.km_wet[wet] * np.maximum(rho_v_sat(outer[wet]) - C_INF, 0)
                active = np.zeros_like(wet)
                active[wet] = rho_v_sat(outer[wet]) > C_INF
                residual = self.h_contact*(ts-outer) + h_ext*(T_AMBIENT_C-outer) - L_V*evap
                derivative = -self.h_contact - h_ext - L_V*self.km_wet*drho_v_sat(outer)*active
                step = residual / derivative
                outer = np.clip(outer - step, 5, 55)
                if np.max(np.abs(step)) < 1e-10:
                    break
            rhs = -U_BODY*T_SKIN_C*np.ones(n*n) - self.h_contact.ravel()*outer.ravel()
            ts_new = self.linear(rhs).reshape((n, n))
            change = max(float(np.max(np.abs(ts_new-ts))), float(np.max(np.abs(outer-to))))
            ts = (1-relaxation)*ts + relaxation*ts_new
            to = (1-relaxation)*to + relaxation*outer
            if change < tolerance:
                break
        evap = np.zeros_like(to)
        evap[wet] = self.km_wet[wet] * np.maximum(rho_v_sat(to[wet]) - C_INF, 0)
        return {
            "body_W_m2": float(np.mean(U_BODY*(T_SKIN_C-ts))),
            "evap_capacity_g_m2_h": float(np.mean(evap)*3.6e6),
            "mean_local_compression": float(np.mean(self.compression[wet])),
            "mean_wet_air_scale": float(np.mean(self.air_scale[wet])),
            "final_change_C": float(change),
            "iterations": it + 1,
            "converged": bool(change < tolerance),
        }


def run_pressure_layout_screen(n=12, cmax=0.5, air_exponent=2.0, pressure_names=None):
    pressure_maps = build_pressure_maps(n)
    if pressure_names is not None:
        pressure_maps = {k: pressure_maps[k] for k in pressure_names}
    route_mask = build_route_mask(n)
    k_route = np.where(route_mask, K_HIGH_SHEET, K_BACKGROUND_SHEET)
    k_background = np.full((n, n), K_BACKGROUND_SHEET)
    rows = []
    for pressure_name, pressure in pressure_maps.items():
        layouts = build_wet_layouts(n, pressure, route_mask)
        route_model = PressureTile(k_route, pressure, cmax, air_exponent)
        background_model = PressureTile(k_background, pressure, cmax, air_exponent)
        for layout_name, wet in layouts.items():
            routed = route_model.run(wet)
            background = background_model.run(wet)
            rows.append({
                "pressure_map": pressure_name,
                "wet_layout": layout_name,
                "wet_fraction": float(np.mean(wet)),
                "body_W_m2": routed["body_W_m2"],
                "heat_routing_gain_W": (routed["body_W_m2"] - background["body_W_m2"]) * 0.195,
                "evap_capacity_g_m2_h": routed["evap_capacity_g_m2_h"],
                "mean_local_compression": routed["mean_local_compression"],
                "mean_wet_air_scale": routed["mean_wet_air_scale"],
                "converged": routed["converged"] and background["converged"],
            })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(run_pressure_layout_screen(n=24).to_csv(index=False))
