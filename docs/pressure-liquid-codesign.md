# Pressure-aware terminal / liquid-route co-design

Status: virtual/computational screening only. No physical garment or bench specimen exists and no measured cooling claim is made.

## Purpose

The pressure-aware thermal screen favors moving wet evaporator terminals away from compressed regions because compression closes ambient vapor-renewal paths. That creates a second design burden: moving terminals away from the pressure field can lengthen liquid collection routes.

This screen therefore treats terminal placement as a two-objective problem:

1. maximize body-side heat removal in the low-order pressure/evaporation model;
2. minimize a first-order hydraulic route burden.

The result is not a full fluid-network solution. It is a design-selection layer on top of the converged terminal regularization sweep.

## Hydraulic proxy

For a laminar circular-equivalent channel, Poiseuille scaling gives

\[
\Delta p_f \propto \frac{L\dot V}{r^4}.
\]

The co-design screen therefore defines

\[
J_h = d_{95}\,\hat r^{-4},
\]

where `d95` is the 95th-percentile geometric distance to the nearest wet terminal and `r_hat` is the retained equivalent radius of a mechanically protected liquid trunk. The current reference uses `r_hat = 0.90`.

This proxy is intentionally conservative and simple. It does **not** replace the explicit capillary-network, radius-collapse, or pressure-weighted-route models elsewhere in the repository.

## Variable table

| Symbol | Meaning | SI unit | Definition / assumption | Type |
|---|---|---:|---|---|
| `d95` | 95th-percentile source-to-terminal distance | m | geometric terminal-distance statistic | model output |
| `r_hat` | retained channel radius ratio | 1 | compressed radius / nominal radius, `0 < r_hat <= 1` | design assumption |
| `J_h` | hydraulic route burden proxy | m-equivalent | `d95 r_hat^-4` | derived metric |
| `q_b` | body-side heat flux | W/m² | output of the pressure-aware thermal model | model output |
| `beta` | four-island regularization weight | 1 | terminal-placement score weight | design variable |
| `w_r` | heat-route overlap weight | 1 | terminal-placement score weight | design variable |

Dimensional check:

\[
[J_h] = [d_{95}] [\hat r]^{-4} = \mathrm{m}.
\]

The numerical value is an equivalent path-burden metric, not a physical pressure drop unless channel geometry, flow and viscosity are supplied.

## 24 x 24 reference result

The pure thermal optimum in the current backpack-plus-straps pressure map is:

- `beta = 0.0`;
- route weight `0.20`;
- body-side heat flux `112.84 W/m²`;
- liquid-route `d95 = 20.16 mm`;
- protected-trunk hydraulic proxy `30.72 mm-equivalent`.

If terminal placement is constrained to retain at least 98% of the thermal optimum and then chosen to minimize hydraulic burden, the selected co-design anchor is:

- `beta = 0.125`;
- route weight `0.35`;
- body-side heat flux `110.83 W/m²`;
- thermal retention `98.21%`;
- liquid-route `d95 = 16.77 mm`;
- hydraulic proxy `25.56 mm-equivalent`;
- hydraulic-proxy reduction versus the pure thermal optimum: `16.79%`.

Therefore the current VP-E terminal-placement anchor is **not** the pure pressure-avoidance optimum. A small amount of distributed four-island regularization is retained because it materially shortens liquid routes at a small thermal penalty.

## Interpretation

The result supports a distributed-cell architecture:

> local sweat collection -> short protected liquid trunk -> pressure-aware wet terminal -> open evaporative microtexture.

It does not support long centralized liquid transport across the garment. Separate capillary screens already show that vertical rise and long path length can dominate passive liquid-transport area.

## H / T / D / C / U

### H — falsifiable hypothesis

For a fixed pressure field and equal wet-terminal area, a mildly regularized pressure-aware layout can reduce hydraulic route burden by at least 10% while retaining at least 98% of the body-side heat flux of the pure thermal optimum.

### T — minimum validation

- synthetic backpack-plus-straps pressure field;
- equal wet-terminal area;
- equal heat-route material fraction;
- converged pressure/thermal solver;
- regularization sweep over terminal-template and route-overlap weights;
- hydraulic burden evaluated with the same radius-retention assumption for every candidate.

### D — decision rule

PASS if a candidate simultaneously satisfies:

- `q_b >= 0.98 q_b,max`;
- `J_h <= 0.90 J_h,thermal-best`.

The 24 x 24 reference passes this rule.

### C — failure modes / alternatives

- nearest-terminal distance may not equal the actual routed liquid path;
- protected trunks may not maintain the assumed radius floor;
- pressure fields and sweat-source fields are time-varying;
- manufacturing may force terminal shapes different from the score-field masks;
- a hierarchy of micro-collectors and larger trunks may change the optimum.

### U — uncertainty

The largest uncertainties are model form, pressure-to-radius coupling, terminal contact, and the effective ambient mass-transfer coefficient. The hydraulic proxy is not assigned a statistical uncertainty because it is a deterministic screening index; the dominant uncertainty is structural/model-form uncertainty rather than numerical convergence.

## Salt conservation

This co-design model moves salt only with the liquid phase. Salt vapor flux is zero. Water may evaporate at the exterior terminal; nonvolatile dissolved salts remain in the liquid and can concentrate or precipitate. No salt evaporation mechanism is assumed.

## Reproducibility

- `simulations/pressure_liquid_codesign.py`
- `tests/test_pressure_liquid_codesign.py`
- `data/pressure_liquid_codesign_reference.csv`
