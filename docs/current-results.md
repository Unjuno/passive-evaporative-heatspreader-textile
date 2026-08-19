# Current Numerical Results

Status: **SIMULATION / ANALYTIC SCREENING / VIRTUAL PROTOTYPE ONLY — NO PHYSICAL SPECIMEN**  
Compiled: 2026-08-20

This file summarizes results that currently change design decisions. Values are model outputs under stated assumptions, not measured garment claims.

## 1. Current design direction

The working virtual architecture is:

> directional liquid transport + capillary-fed wet microtexture + continuously ambient-connected open valleys/gaps/islands + short-range high-`k/rho` heat routing between thermally asymmetric wet/dry regions + explicit thermal contact + explicit water-supply state + dry-side hot-ambient protection.

No physical garment or bench specimen currently exists.

## 2. Exterior geometric area is not accessible evaporative area

The E3 periodic 2-D vapor-diffusion screen shows strong boundary-layer sharing.

For `h=2.5 mm`, structured fraction `f=0.65`:

| idealized renewal gap | p=0.8 mm | p=1.0 mm | p=1.5 mm |
|---:|---:|---:|---:|
| 0.5 mm | 3.785 | 3.548 | 3.098 |
| 1.0 mm | 2.481 | 2.400 | 2.229 |
| 5.0 mm | 1.312 | 1.304 | 1.286 |

These are vapor-transfer multipliers, not cooling watts.

**Conclusion:** tighter ribs do not overcome a thick shared humidity layer.

## 3. Long covered passive wet corridors are not preferred

The self-consistent 100 mm covered/end-renewed corridor screen at 35 °C / 70% RH gives nonzero natural flow but near-saturated interior air for representative shallow channels. Thermo-solutal conditions can reverse the flow direction.

**Conclusion:** corridor velocity and axial Péclet number are not accepted as proof of useful renewal.

## 4. Open-valley renewal requires both quality and capacity

Define

\[
R=G_a/G_w,
\qquad
F=\frac{R}{1+R}.
\]

`F=0.8` requires `R=4`; `F=0.9` requires `R=9`.

Absolute series vapor conductance is

\[
k_{eff}=\frac{k_wk_a}{k_w+k_a}=k_wF.
\]

A high `F` can coexist with low absolute transfer, so both must be reported.

For a representative 6 × 3 mm distributed open valley, the screened exchange length is roughly 0.7–1.1 mm. Twenty-to-fifty-millimeter interruption alone is therefore too coarse when distributed lateral access is weak.

Current exterior roles:

- O1 continuously laterally open: principal hypothesis;
- O2a 20–50 mm segmentation: negative/control;
- O2b 1–3 mm segmentation: extreme end-access test;
- O3 ambient-connected wet islands: apparel-relevant implementation.

## 5. Sensible heat and vapor transfer are distinct

The current stack does not reuse vapor-transfer enhancement as sensible heat-transfer enhancement. This matters because warm ambient air can supply latent heat to evaporation while simultaneously reducing or reversing body-side cooling.

## 6. Positive evaporation is not equivalent to body cooling

Representative coupled open-valley screen, 6 × 3 × 50 mm, skin 34 °C, `U_body=100 W/(m² K)`:

At 35 °C / 70% RH:

| vapor / heat parameter | evaporation | body heat flux | ambient sensible heat to wet wall |
|---|---:|---:|---:|
| 0.1 / 0.1 mm | ~700 g/m²h | +299 W/m² | +172 W/m² |
| 0.5 / 0.5 mm | ~522 g/m²h | +254 W/m² | +97 W/m² |
| 1.0 / 1.0 mm | ~414 g/m²h | +216 W/m² | +63 W/m² |

At 40 °C / 70% RH, linked same-path cases still evaporate while body-side heat flux becomes negative; a representative 0.5/0.5 mm case is about −16 W/m².

**Conclusion:** signed body-side heat flow, not evaporation mass, is the integrated endpoint.

## 7. Hot/humid same-path sign boundary

For zero body-side heat flow:

\[
\frac{k_{air}}{D_v}(T_\infty-T_{skin})
=
L_v[\rho_{v,sat}(T_{skin})-\phi_\infty\rho_{v,sat}(T_\infty)].
\]

For artificial skin 34 °C:

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

This is a low-order model sign boundary, not a human-safety or measured garment limit.

## 8. Ordinary heat/mass analogy does not provide arbitrary selectivity

Define

\[
\Xi=\delta_{vapor}/\delta_{heat}.
\]

At 40 °C / 70% RH, the low-order model requires critical `Xi≈0.31–0.65` to reach zero body-side heat flux over the screened vapor-side range. Same-exchange-length and ordinary Lewis/Chilton–Colburn-style baselines remain near `Xi≈1`.

**Conclusion:** hot-ambient protection requires a distinct physical mechanism such as dry-side shielding, radiation control, selective exposure, anisotropic solid routing, contact engineering, or genuinely separated pathways.

## 9. Explicit feed limitation and partial wetness

`open_valley_feed_limited.py` solves a computational sub-grid wet fraction `beta`:

\[
\dot m''=\beta k_{m,w}[\rho_{v,sat}(T_s)-\rho_v].
\]

For 0.195 m² structured area, 150 g/h corresponds to ~769 g/(m²h).

At 35 °C / 50% RH with linked heat/vapor exchange:

| linked parameter | regime | `beta` | total evaporation | body heat flux |
|---:|---|---:|---:|---:|
| 0.10 mm | supply-limited | ~0.37 | ~150 g/h | ~331 W/m² |
| 0.25 mm | supply-limited | ~0.43 | ~150 g/h | ~356 W/m² |
| 0.50 mm | supply-limited | ~0.55 | ~150 g/h | ~383 W/m² |
| ~0.95–1.0 mm | transition | ~1 | ~147–150 g/h | ~400–411 W/m² |
| 2.0 mm | transfer-limited | 1 | ~109 g/h | ~317 W/m² |

**Correction:** once water supply is saturated, stronger linked external exchange can reduce body-coupled cooling because additional latent heat comes from ambient air.

## 10. Same evaporation mass can remove different body heat

At 35 °C / 50% RH / 150 g/h, modeled body share of latent heat is approximately:

- very strong linked exchange: 62–64%;
- linked 0.5 mm: ~74%;
- near linked 0.75 mm: ~78%.

Thus identical evaporation mass does not imply identical body cooling.

## 11. Symmetric heat spreading does not create global cooling by itself

The symmetric wet/dry two-node model reduces the local wet/dry temperature split from roughly 4.9 °C at no mixing toward zero at high `g_mix`, but area-integrated body heat flow remains essentially invariant when wet/dry sensible boundary conditions are identical.

**Conclusion:** heat spreading only creates system-level value when it connects spatially different wetting/exposure/body-coupling conditions.

## 12. Asymmetric heat-spreader mechanism and solver correction

The asymmetric model gives the dry region lower ambient sensible exposure than the wet evaporator. Under that asymmetry, heat routing increases total modeled body heat removal.

A dense `g_mix` sweep exposed nonphysical high-beta branch jumps in the old unconstrained solver. The current solver uses bounded least squares, explicit original-equation residual acceptance, and continuation support.

For `h_dry=5 W/(m² K)`, corrected approximate `g_mix` needed for 90% of the high-mixing asymptotic gain:

| feed | target `g_mix` | asymptotic mechanism gain over 0.195 m² |
|---:|---:|---:|
| 30 g/h | ~117 W/(m² K) | ~3.0 W |
| 50 g/h | ~192 | ~4.5 W |
| 75 g/h | ~285 | ~5.7 W |
| 100 g/h | ~330 | ~6.0 W |
| 150 g/h | ~258 | ~3.5 W |

**Conclusion:** infinite spreader conductivity is not useful as a design objective; the low-order mechanism reaches diminishing returns at finite conductance.

## 13. Material / routing-pitch mapping

The first sheet mapping is

\[
g_{sheet}\approx\Gamma\frac{k_{\parallel}tc}{P^2},\qquad\Gamma=4.
\]

This is an ideal periodic-stripe topology screen, not a validated textile correlation.

The key scaling is

\[
k t\propto g_{mix}P^2.
\]

For representative `g_mix≈330 W/(m² K)`:

### Abstract `k=100 W/(m K)`, `rho=1600 kg/m³`

- P=10 mm: ~83 µm, ~40 g over 0.30 m²;
- P=20 mm: ~330 µm, ~159 g;
- P=30 mm: ~743 µm, ~357 g.

### Abstract `k=300 W/(m K)`, `rho=1800 kg/m³`

- P=10 mm: ~28 µm, ~15 g;
- P=20 mm: ~110 µm, ~59 g;
- P=30 mm: ~248 µm, ~134 g.

The property values are model inputs, not measurements of named materials.

## 14. Sparse conductive coverage is not automatically lighter

Under linear coverage scaling,

\[
m=A\rho\frac{g_{sheet}P^2}{\Gamma k},
\]

so coverage cancels. A sparse network only saves mass if it also changes path topology/effective pitch, permits a better material, removes inactive regions, or provides another non-linear advantage.

The simple mass figure of merit is `k/rho`.

## 15. Thermal contact can dominate sheet conductivity

A two-contact screen uses

\[
\frac{1}{g_{eff}}=\frac{1}{g_{sheet}}+\frac{2}{h_c}.
\]

For a representative `g_target≈330 W/(m² K)`:

- even an ideal sheet needs each-side `h_c>~660 W/(m² K)`;
- if `g_sheet≈660 W/(m² K)`, each contact must be ~1320 W/(m² K) in the lumped model.

These are validation burdens, not measured contact coefficients.

## 16. Explicit virtual prototypes v0.1

At 100 g/h:

| prototype | design anchor | spreader mass over 0.30 m² | nominal `g_eff` | spreader-only mechanism gain over 0.195 m² |
|---|---|---:|---:|---:|
| VP-A | 10 mm / `k=100` / 100 µm | ~48 g | ~286 W/(m² K) | ~5.3 W |
| VP-B | 20 mm / same class / 200 µm | ~96 g | ~167 | ~4.9 W |
| VP-C | 15 mm / 50% routed / higher `k/rho` class | ~27 g | ~197 | ~5.0 W |
| VP-D | VP-A spreader + stronger dry-side shielding | ~48 g | ~286 | ~6.1 W |

Gain versus feed:

| feed | VP-A | VP-B | VP-C | VP-D |
|---:|---:|---:|---:|---:|
| 50 g/h | ~4.2 W | ~4.0 W | ~4.1 W | ~4.9 W |
| 75 g/h | ~5.1 W | ~4.8 W | ~4.9 W | ~5.9 W |
| 100 g/h | ~5.3 W | ~4.9 W | ~5.0 W | ~6.1 W |
| 150 g/h | ~3.2 W | ~3.0 W | ~3.1 W | ~3.6 W |

The gains are relative to the same local wet/dry model with `g_mix=0`. They are **not total garment-vs-control cooling predictions**.

Deterministic topology/contact sensitivity at 100 g/h (`Gamma=2–4`, each-side contact 500–5000 W/(m² K)) gives:

- VP-A: ~4.4–5.4 W;
- VP-B: ~3.9–5.0 W;
- VP-C: ~4.1–5.2 W;
- VP-D: ~5.1–6.2 W.

Current roles:

- VP-D: performance anchor;
- VP-C: lightweight anchor;
- VP-A: short-pitch baseline;
- VP-B: routing-distance/manufacturability comparison.

## 17. Current virtual-prototype implication

The current calculations favor:

- short dry-to-wet routing distances, initially 10–20 mm;
- high `k/rho` paths instead of indiscriminate thickness;
- explicit wet/dry contact design;
- dry-side shielding as a complementary mechanism;
- continuously ambient-connected wet exterior structures;
- explicit water supply and wetness state.

## 18. Next numerical work

1. Replace scalar `g_mix` with a distributed 1-D/2-D wet/dry field using direct material `k`, thickness, anisotropy, contacts and patch geometry.
2. Preserve VP-A–D as regression anchors for that distributed model.
3. Add full virtual garment mass/thickness budgets including capillary and exterior microtexture layers.
4. Add hot/humid virtual performance maps for each VP.
5. Move exterior transfer toward geometry-resolved 2-D/3-D natural convection/cross-flow.
6. Re-test old nonlinear lumped equilibria under the improved external-flow treatment.

Future physical protocols remain specifications only; no physical experiment has been executed.
