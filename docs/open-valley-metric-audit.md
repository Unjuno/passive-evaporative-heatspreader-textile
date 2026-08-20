# Open-Valley Metric Audit — Retention Is Not Evaporation Capacity

Date: 2026-08-20  
Classification: **SIMULATION / ANALYTIC AUDIT**

## Problem

The local mechanism metric

\[
F=\frac{R}{1+R}
\]

measures how much of the bulk-ambient-to-saturated-wall vapor-density difference remains available at the wet surface.

A high `F` is useful, but it is **not sufficient** as an optimization objective.

If wet-surface transfer is deliberately weakened, local valley air becomes less humid and `F` rises even though total evaporation capacity may fall.

## Series conductance

For wet-surface coefficient `k_w` and lateral ambient-renewal coefficient `k_a`, the long-valley local balance is equivalent to two mass-transfer resistances in series:

\[
k_{eff}=\frac{k_w k_a}{k_w+k_a}.
\]

Because

\[
F=\frac{k_a}{k_w+k_a},
\]

then

\[
k_{eff}=k_w F.
\]

### Variable table

| symbol | meaning | SI unit | definition |
|---|---|---:|---|
| `k_w` | wet surface → valley vapor-transfer coefficient | m/s | current screen: `Sh D_v / D_h` |
| `k_a` | valley → ambient lateral-renewal coefficient | m/s | current screen: `D_v/delta_open` |
| `F` | retained wet-wall vapor driving-force fraction | 1 | `k_a/(k_w+k_a)` |
| `k_eff` | net saturated-wall → ambient series conductance | m/s | `k_w k_a/(k_w+k_a)` |

### Unit check

\[
[k_{eff}]=\frac{[m/s][m/s]}{[m/s]}=m/s.
\]

## Numerical tradeoff

For a 6 mm-wide valley under the current diffusion-only lateral mapping (`delta_open=0.1 mm`):

| depth | `F` | `k_eff` |
|---:|---:|---:|
| 0.5 mm | 0.550 | 0.126 m/s |
| 1.0 mm | 0.695 | 0.0855 m/s |
| 2.0 mm | 0.799 | 0.0562 m/s |
| 3.0 mm | 0.841 | 0.0444 m/s |
| 5.0 mm | 0.879 | 0.0340 m/s |
| 8.0 mm | 0.901 | 0.0277 m/s |

Thus deeper geometry appears better if only `F` is inspected, while its modeled absolute series vapor conductance decreases strongly.

This is not evidence that a 0.5 mm-deep valley is optimal. The assumed `Sh`, external exchange mapping, wetting geometry, heat transfer, and manufacturing constraints remain uncertain. It is evidence that **retention alone can select the wrong direction**.

## Updated evaluation rule

Every open-valley numerical or physical result should report at least two distinct quantities:

1. **renewal quality** — `F` or normalized valley vapor loading;
2. **absolute useful transfer** — evaporation mass flux, inferred effective conductance, or body-side heater-power gain.

Do not accept an architecture as improved solely because valley RH is lower or `F` is higher.

## Physical experiment consequence

E3c should retain `F` as the mechanism metric, but the integrated decision remains heater power and water balance. If possible, also estimate an experimental effective vapor conductance:

\[
k_{eff,exp}=\frac{\dot m''_{evap}}
{\rho_{v,sat}(T_s)-\rho_{v,\infty}}.
\]

This estimate should be reported only where evaporated mass can be assigned to the tested wet projected area with adequate water-balance closure.

## Design implication

The goal is not:

> maximize `F`.

It is closer to:

> maintain adequate `F` **without sacrificing absolute evaporation conductance**, while also preventing excessive inward sensible heat gain.

That requires the next thermal coupling step to consider `F`, `k_eff`, and body-side heat flow together.
