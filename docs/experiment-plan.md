# Experiment Plan

Date: 2026-08-20

## 1. Primary question

At the same liquid-water input and ambient conditions, does the integrated passive architecture remove more heat from an artificial skin than a conventional flat fast-dry textile?

## 2. Sample matrix

- **B0 — flat fast-dry control:** conventional-like polyester moisture-management textile.
- **B1 — directional transport only:** directional liquid transport, flat exterior.
- **B2 — exterior structure only:** capillary-fed rib/fin exterior without whole-area heat spreader.
- **B3 — heat spreader only:** whole-area heat spreader with flat exterior.
- **B4 — integrated architecture:** directional transport + heat spreader + capillary delivery + exterior ribs/fins.
- **B5 — intentionally dense exterior:** boundary-layer-overlap/failure control.

For E3b/E3c, B4/B5 exterior structures are further split into micro-rib-only, hierarchical microstructure + macro air-renewal, covered-corridor, continuously open-valley, centimeter-interruption control, millimeter-scale interruption, and discontinuous-island variants.

## 3. Primary environment

- artificial-skin setpoint: 34 °C;
- ambient temperature: 35 °C;
- relative humidity: 70% for the primary test;
- nominal air speed: <0.05 m/s;
- projected active-area normalization: 0.30 m²;
- liquid-water/synthetic-sweat feed: 150 g/h equivalent;
- minimum independent repeats: n = 3.

Secondary conditions:

- RH: 50% and 85%;
- water feed: 75 and 300 g/h equivalent;
- hot-ambient comparison near 40 °C;
- vertical, horizontal, and inverted orientation where relevant;
- controlled external airflow only after the passive still-air condition is complete.

## 4. Fair-comparison and supply-limit rules

All compared samples must receive the same commanded liquid feed in a given test cell. Record actual feed mass independently and close the water balance.

Do not credit a numerical transfer-capacity case for evaporation exceeding the physical liquid supply. For each experiment report whether the exterior is:

- transfer-limited;
- supply-limited;
- runoff-limited;
- uncertain.

## 5. Primary measurement

Measure electrical heater power required to maintain the artificial skin at 34 °C.

For the integrated sample relative to the flat control:

\[
\Delta Q=P_{heater,B4}-P_{heater,B0}.
\]

A larger positive value indicates greater heat removal from the artificial skin.

## 6. Provisional project decision rules

At 35 °C / 70% RH / 150 g/h equivalent / still air:

- **PASS:** `Delta Q >= 10 W`, n >= 3, CV <=10%, water-balance closure >=95%.
- **STRONG PASS:** `Delta Q >= 20 W`.
- **FAIL:** `Delta Q < 5 W`.
- **UNCERTAIN:** 5–10 W, CV >10%, or inadequate water-balance closure.

These are internal screening thresholds, not external standards.

## 7. Measurements

Required:

1. heater electrical power;
2. artificial-skin temperature;
3. ambient temperature and RH;
4. far-field air speed;
5. commanded and measured liquid feed;
6. sample mass before/after;
7. runoff/drip collection;
8. evaporated mass by water balance;
9. wet exterior surface temperature.

Strongly recommended:

10. local T/RH at approximately 0.5, 1, 2, 5, 10, 20, and 40 mm where probe size permits;
11. infrared surface-temperature map;
12. rib/wet-field wetting fraction;
13. compression state and actual rib/valley geometry;
14. macro-path dimensions and open fraction;
15. signed local flow direction/magnitude where resolvable;
16. axial and transverse valley T/RH profiles;
17. exact wet projected area used for evaporation-flux normalization.

Heater power, surface T, local air T/RH, evaporation mass and flow must be interpreted together. Do not infer `M_h=M_m` from one integrated measurement.

## 8. E1 — direct value test

Compare B0 and B4 at the primary condition.

**H1:** B4 increases body-side heat removal by >=10 W over 0.30 m² equivalent.

Failure alternatives include insufficient wetting, thermal contact resistance, humidity-layer overlap, runoff, weak vapor renewal, or inward sensible heat offsetting latent benefit.

## 9. E2 — ablation

Compare B0/B2/B3/B4.

**H2:** B4 exceeds both B2 and B3, demonstrating complementarity of heat routing and exterior evaporation enhancement.

## 10. E3 — exterior pitch / boundary-layer access

Hold exterior material family and approximate height constant; compare pitch near 0.8, 1.0, and 1.5 mm.

Use heater power plus temperature-corrected local vapor loading rather than geometric area alone.

`docs/e3-boundary-layer-screen.md` shows that a several-millimeter stagnant humidity layer can dominate pitch refinement. E3 remains a physical falsification experiment, not a confirmation exercise.

## 11. E3b — hierarchical air renewal

Compare a micro-rib-only exterior against similar wet microstructure combined with larger ambient-access paths such as open valleys, cross-openings, spacer passages, grooves, pleats, or discontinuous fields.

Starting research ranges remain broad:

- microstructure height: about 2–3 mm;
- local pitch: about 0.8–1.5 mm;
- macro/open path width: about 1–10 mm;
- depth: about 1–5 mm;
- wet-field widths: about 5–25 mm.

Do not assume upward chimney flow. Record upward, downward, reversing/intermittent, or below-resolution behavior.

## 12. E3c — covered versus continuously open / interrupted exterior

Latest numerical work changes the sample matrix.

### D1 — covered/end-renewed control

Wet-floor duct, ambient connection primarily at ends; approximately 6–10 mm wide, 3–5 mm deep, 50–100 mm long.

### O1 — continuously laterally open valley

Matched wet floor, continuously exposed to ambient along the path. **This is the principal hypothesis.**

### O2a — centimeter-interruption negative/control

Cross/end openings every approximately 20–50 mm.

The distributed 1-D vapor screen predicts this spacing is generally too coarse when lateral renewal between openings is weak. O2a is therefore a negative/control condition, not the preferred design.

### O2b — millimeter-scale short segments

Approximate wet segment lengths: 1, 2, and 3 mm where manufacturable. This tests the numerical result that axial end effects decay over an exchange length of roughly 0.7–1.1 mm in the representative 6 × 3 mm screen.

### O3 — discontinuous wet islands

Small wet fields separated by ambient-connected gaps; preferred apparel implementation if literal 1–3 mm channels are impractical.

### E3c mechanism metrics

Convert measured ambient, wet-surface, and local-valley states to vapor density:

\[
\theta(x)=\frac{\rho_{v,valley}(x)-\rho_{v,\infty}}
{\rho_{v,sat}(T_s(x))-\rho_{v,\infty}},
\qquad
F(x)=1-\theta(x).
\]

When the inversion is well-conditioned:

\[
R(x)=\frac{1-\theta(x)}{\theta(x)}.
\]

Use `F` as the primary renewal-quality metric. Exact high `R` is secondary because measurement inversion becomes ill-conditioned near ambient vapor loading.

**Do not optimize `F` alone.** Pair it with absolute transfer:

\[
k_{eff,exp}=\frac{\dot m''_{evap}}
{\rho_{v,sat}(T_s)-\rho_{v,\infty}}
\]

where water balance and wet-area assignment support the calculation, and always retain heater power as the integrated cooling metric.

### E3c hypotheses

- **H3c-1:** O1 maintains higher `F` than D1 at equal water input.
- **H3c-2:** O2a gives little improvement when its interior remains laterally stagnant.
- **H3c-3:** O2b/O3 improve `F` more strongly than O2a at matched wet area.
- **H3c-4:** an architecture with higher `F` but lower evaporation flux / `k_eff` is not an improvement.

### E3c PASS

At 35 °C / 70% RH, at least one of O1/O2b/O3 must show:

- clearly higher temperature-corrected `F` than D1;
- heater-power advantage over D1 >=3 W after active-area normalization;
- equal liquid input within uncertainty;
- water-balance closure >=95%.

Support for the distributed-renewal interpretation is strengthened if the ordering is broadly:

`O1 or O2b/O3 > O2a >= or ~= D1`

in median `F`, without loss of absolute evaporation conductance.

See `experiments/e3c_open_vs_covered_corridors.md`.

## 13. E4 — humidity boundary

Test the best current B4 sample at 50%, 70%, and 85% RH.

**H4:** passive advantage decreases strongly as ambient vapor-pressure driving force decreases.

At the dry 50% condition, explicitly check whether evaporation becomes **liquid-supply-limited** before interpreting a transfer-capacity advantage.

## 14. E5 — heat-spreader orientation

For an anisotropic heat spreader, compare the high-conductivity axis aligned toward wet evaporation zones versus rotated approximately 90°.

**H5:** alignment improves body-side heat removal under spatially nonuniform wetting.

## 15. E6 — hot-ambient sensible-heat penalty and shielding

At approximately 40 °C, compare exposed versus thermally protected/routed structures while retaining the same wet-area and water-input controls.

**H6:** shielding/routing reduces parasitic inward sensible heat while retaining useful vapor exchange.

The coupled open-valley thermal screen explicitly shows a failure mode in which evaporation remains positive while body-side heat flux becomes negative. Therefore E6 must never use evaporation rate alone as the cooling endpoint.

Required comparison variables:

- heater power;
- evaporation mass;
- wet-surface T;
- valley/ambient T/RH;
- dry-region surface T;
- local flow if measurable.

## 16. E7 — mechanical durability

After baseline measurement, apply controlled bending, stretch, compression, washing, and wet/dry cycling.

Track in-plane thermal conductance, capillary delivery rate, cooling gain, exterior geometry recovery, and open-path fraction.

Provisional durability target: retain >=80% of baseline functional performance after the defined cycle protocol.

## 17. Uncertainty

For each primary result report:

- instrument calibration uncertainty;
- run-to-run standard deviation;
- active-area uncertainty;
- actual water-feed uncertainty;
- humidity and temperature stability;
- probe position/size uncertainty near structured surfaces;
- low-speed flow measurement resolution;
- wet-area and compression uncertainty;
- propagated uncertainty in vapor density, `theta`, `F`, and where reported `R`/`k_eff`;
- combined standard uncertainty and coverage factor where practical.

Do not report more numerical precision than measurement uncertainty supports.

## 18. Salt / contamination protocol

Salt deposition is not unique to this architecture. Compare degradation against the same synthetic-sweat exposure in B0.

Only add dedicated salt-management hardware if the proposed architecture exhibits materially faster functional degradation than the conventional control.

No experiment or model should assume that salt evaporates.
