# Current Numerical Results

Status: **SIMULATION / ANALYTIC SCREENING ONLY — NO PHYSICAL GARMENT PERFORMANCE DATA YET**  
Compiled: 2026-08-20

This file lists results that currently change design or validation decisions. Values are model outputs under stated assumptions, not measured garment claims.

## 1. Heat-spreader findings retained

- Lateral heat spreading is most useful when evaporation/wetting is spatially nonuniform.
- Anisotropic spreader orientation can materially change heat routed toward a localized cooling band.
- Dry high-conductivity exterior regions can collect hot ambient heat and require shielding, segmentation, or anisotropic routing.

## 2. Exterior area / boundary-layer finding

The E3 periodic 2-D vapor-diffusion screen shows that dense wet ribs can share one humid boundary layer.

For `h=2.5 mm`, structured fraction `f=0.65`:

| idealized renewal gap | p=0.8 mm | p=1.0 mm | p=1.5 mm |
|---:|---:|---:|---:|
| 0.5 mm | 3.785 | 3.548 | 3.098 |
| 1.0 mm | 2.481 | 2.400 | 2.229 |
| 5.0 mm | 1.312 | 1.304 | 1.286 |

These are vapor mass-transfer multipliers, not cooling wattages.

**Current conclusion:** geometric area is not useful area unless the ambient-access mechanism is explicit.

## 3. Lumped-model corrections

- The original nonlinear passive heat/mass model can contain multiple stable roots. Historical single-value `M≈2.5–3.5` thresholds are not validated design criteria.
- Sensible transfer and vapor transfer are modeled separately (`M_h`, `M_m`). A vapor-transfer result must not be copied into sensible heat transfer.

## 4. Covered/end-renewed corridor

At 35 °C / 70% RH, 100 mm length:

| width × depth | signed velocity | axial Pe | mean RH | body-side heat flux |
|---|---:|---:|---:|---:|
| 3 × 2 mm | +0.228 mm/s | 0.81 | ~100% | +0.10 W/m² |
| 6 × 3 mm | +0.594 mm/s | 2.12 | ~100% | +0.40 W/m² |
| 10 × 5 mm | +1.60 mm/s | 5.70 | ~99.9% | +1.81 W/m² |

At 35 °C / 85% RH the 10 × 5 mm case reverses flow. At 40 °C / 70% RH it gives stronger downward flow and slightly negative body-side heat flux.

**Current conclusion:** long covered wet passive chimneys are not preferred. Nonzero velocity and axial Péclet number do not prove useful vapor renewal.

## 5. Local open-valley renewal metric

Define

\[
R=G_a/G_w,
\qquad
F=\frac{R}{1+R}.
\]

| `F` | required `R` |
|---:|---:|
| 0.50 | 1 |
| 0.80 | 4 |
| 0.90 | 9 |
| 0.95 | 19 |

Measured T/RH plus wet-surface temperature can identify `F`. Exact high `R` is secondary because inversion becomes poorly conditioned near ambient vapor loading.

## 6. Distributed open-valley result

The distributed vapor model solves

\[
D_vA\theta''-uA\theta'+G'_w(1-\theta)-G'_a\theta=0.
\]

For a representative 6 × 3 mm valley, the screened exchange length is approximately 0.7–1.1 mm.

Selected zero-axial-flow center `F` values:

| effective lateral parameter | segment length | center `F` |
|---:|---:|---:|
| 0.25 mm | 1 mm | 0.935 |
| 0.25 mm | 20 mm | 0.680 |
| 0.50 mm | 1 mm | 0.931 |
| 0.50 mm | 2 mm | 0.797 |
| 0.50 mm | 20 mm | 0.515 |
| 1.00 mm | 1 mm | 0.929 |
| 1.00 mm | 20 mm | 0.347 |

For 6 × 3 × 50 mm, few-mm/s axial flow changes the center state negligibly in the current screen.

**Correction:** 20–50 mm interruption alone is too coarse when distributed lateral exchange remains weak. Continuous lateral opening is the principal hypothesis; 1–3 mm segmentation is retained as an extreme mechanism test.

## 7. Renewal quality is not absolute evaporation capacity

For local resistances in series:

\[
k_{eff}=\frac{k_wk_a}{k_w+k_a}=k_wF.
\]

In the current geometry mapping, increasing valley depth can raise `F` while lowering `k_eff`.

**Correction:** do not optimize `F` alone. Pair `F` with evaporation mass flux / `k_eff` and signed body-side heat flow.

## 8. Coupled open-valley thermal / vapor result

Representative 6 × 3 × 50 mm, zero prescribed axial flow, `U_body=100 W/(m² K)`, skin 34 °C.

At 35 °C / 70% RH:

| vapor parameter | heat parameter | evaporation | body heat flux | ambient sensible heat to wet wall |
|---:|---:|---:|---:|---:|
| 0.1 mm | 0.1 mm | ~700 g/m²h | +299 W/m² | +172 W/m² |
| 0.1 mm | 0.5 mm | ~645 g/m²h | +319 W/m² | +115 W/m² |
| 0.5 mm | 0.5 mm | ~522 g/m²h | +254 W/m² | +97 W/m² |
| 1.0 mm | 1.0 mm | ~414 g/m²h | +216 W/m² | +63 W/m² |

At 40 °C / 70% RH, same-exchange-length cases still evaporate but body-side heat flux is negative. Example `0.5/0.5 mm`: evaporation ~215 g/m²h and body heat flux ~−16 W/m².

**Current conclusion:** positive evaporation is not equivalent to wearer cooling.

## 9. Heat/mass coupling audit now has ordinary-transport baselines

The sensitivity model defines

\[
\Xi=\delta_{vapor}/\delta_{heat}.
\]

`Xi=1` is the same-exchange-length baseline. At 40 °C / 70% RH, the low-order model requires critical `Xi` values approximately in the 0.31–0.65 range to reach zero body-side heat flux across the screened vapor-side parameters.

For the same air/water-vapor screening state, the Lewis number is near one. A Chilton–Colburn-style equal-j-factor comparison gives

\[
\Xi_{CC}=Le^{-1/3},
\]

which is also near one.

**Current conclusion:** the required hot-ambient selectivity is substantially stronger than ordinary same-boundary heat/mass analogy suggests. This is a design burden, not evidence that arbitrary passive decoupling is available.

Candidate physical mechanisms that could change the ratio include dry-side insulation, reflective/radiative control, selective wet exposure, anisotropic solid heat routing, contact resistance engineering, and genuinely separated air/vapor pathways.

## 10. Analytic environmental body-heat-flow sign boundary

For the same-path heat/vapor baseline, zero body-side heat flow satisfies

\[
\frac{k_{air}}{D_v}(T_\infty-T_{skin})
=
L_v\left[\rho_{v,sat}(T_{skin})-\phi_\infty\rho_{v,sat}(T_\infty)\right].
\]

With skin/artificial skin = 34 °C:

| RH | zero-body-flux ambient T |
|---:|---:|
| 30% | 53.85 °C |
| 50% | 45.25 °C |
| 60% | 42.24 °C |
| 70% | 39.73 °C |
| 80% | 37.57 °C |
| 85% | 36.59 °C |
| 90% | 35.68 °C |
| 95% | 34.81 °C |

This is **not a human safety, survivability, or medical threshold**. It is a model sign boundary.

At RH70%, changing the artificial-skin setpoint from 32 °C to 36 °C moves the modeled boundary from about 37.54 °C to about 41.91 °C.

## 11. Heat-spreader coupling does not automatically rescue above-boundary operation

An exploratory linked-exchange sweep at 40 °C / 70% RH found that increasing body-to-wet-surface coupling does not restore positive body heat flow when the wet surface is already hotter than skin. Stronger coupling can instead transmit more environmental heat inward.

## 12. Explicit feed-limited partial-wetness model

The prior `supply_limit_audit.py` only flagged when fully-wet capacity exceeded available feed. The new `open_valley_feed_limited.py` now solves a homogenized sub-grid wet fraction `beta`.

The vapor source is

\[
\dot m''=\beta k_{m,w}[\rho_{v,sat}(T_s)-\rho_v],
\]

with `0 <= beta <= 1`. The whole floor remains sensibly coupled to the body/heat spreader and air. This is a strong-heat-spreader, fine-scale wet/dry homogenization, not a resolved dry-patch model.

For 65% of a 0.30 m² active area, 150 g/h corresponds to approximately 769 g/(m²h).

At 35 °C / 50% RH with linked heat/vapor exchange:

| linked exchange parameter | regime | solved `beta` | total evaporation | body heat flux |
|---:|---|---:|---:|---:|
| 0.10 mm | supply-limited | ~0.37 | ~150 g/h | ~331 W/m² |
| 0.25 mm | supply-limited | ~0.43 | ~150 g/h | ~356 W/m² |
| 0.50 mm | supply-limited | ~0.55 | ~150 g/h | ~383 W/m² |
| ~0.95–1.0 mm | near transition | ~1 | ~147–150 g/h | ~400–411 W/m² |
| 2.0 mm | transfer-limited | 1 | ~109 g/h | ~317 W/m² |

**New correction:** once water supply is saturated, stronger linked external exchange can reduce body-coupled cooling because additional ambient sensible heat contributes to evaporation without increasing total evaporated water.

At 35 °C / 70% RH and 85% RH, the nominal 150 g/h linked cases remain transfer-limited over the screened range.

## 13. Latent-heat source partition

For the 35 °C / 50% RH / 150 g/h supply-limited cases, all of the following can evaporate approximately the same total 150 g/h while drawing different fractions of latent heat from the body:

| linked exchange parameter | body share of latent heat | ambient-air share |
|---:|---:|---:|
| 0.05 mm | ~62% | ~38% |
| 0.10 mm | ~64% | ~36% |
| 0.25 mm | ~69% | ~31% |
| 0.50 mm | ~74% | ~26% |
| 0.75 mm | ~78% | ~22% |

The fractions are model outputs from the local energy balance and sum to approximately one.

**Current conclusion:** identical evaporation mass does not imply identical body cooling.

## 14. Measurement-resolution audit

A fixed-seed sensitivity screen for true `F=0.8` at representative 35 °C / 70% RH gave approximate 5–95% ranges:

| 1σ temperature | 1σ RH | `F` 5–95% |
|---:|---:|---:|
| 0.05 °C | 0.25 pp | 0.774–0.827 |
| 0.10 °C | 0.50 pp | 0.748–0.854 |
| 0.10 °C | 1.00 pp | 0.715–0.892 |
| 0.20 °C | 1.00 pp | 0.699–0.910 |

This is a hypothetical sensor-uncertainty screen, not a calibration result.

Above the modeled environmental sign boundary, a heater-only artificial skin cannot quantify inward heat. E4/E6 therefore requires bidirectional plate control or calibrated signed heat-flux measurement.

## 15. Current design hypothesis

1. directional liquid transport from skin;
2. flexible routed/whole-area in-plane heat spreading;
3. capillary delivery to wet exterior fields;
4. low-profile micro-rib / 3D-knit / short-fin evaporative texture;
5. continuous lateral ambient access through open valleys/gaps/islands rather than long covered ducts;
6. hot-ambient shielding/routing that limits harmful sensible heat pickup;
7. design evaluation using `F`, absolute vapor transfer, signed body heat flow, available water supply, and wetness state.

## 16. Results explicitly downgraded or rejected as standalone criteria

The following are not current design conclusions:

- a single `M≈2.5–3.5` validated cooling threshold;
- geometric rib area as useful evaporative area;
- guaranteed upward chimney flow;
- axial Péclet number as proof of renewal;
- 20–50 mm segmentation as a sufficient renewal mechanism;
- high `F` as proof of high evaporation capacity;
- positive evaporation as proof of body cooling;
- fully-wet transfer capacity above available feed as achievable fixed-feed performance;
- a model `beta` value as a measured visible wet-area fraction;
- arbitrary `Xi<1` heat/vapor decoupling as physically available without a mechanism;
- 39.73 °C at 70% RH as a universal garment or human limit.

## 17. Next work

Numerical:

- resolve wet/dry patches spatially instead of only homogenized `beta`;
- connect lateral heat/mass exchange to geometry-resolved 2-D/3-D natural convection/cross-flow;
- re-test multi-equilibrium behavior under improved external-flow treatment;
- sensitivity to Nu/Sh, compression, opening losses, radiative properties and weak external drift.

Physical:

- E1 B0 vs B4;
- E2 ablation;
- E3/E3b boundary-layer access;
- E3c D1/O1/O2a/O2b/O3;
- E4a feed-limit / wetness transition;
- E4/E6 signed environmental-boundary and hot-ambient validation.