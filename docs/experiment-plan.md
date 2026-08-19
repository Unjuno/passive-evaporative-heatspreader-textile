# Experiment Plan

Date: 2026-08-19

## 1. Primary question

At the same liquid-water input and ambient conditions, does the integrated passive architecture remove more heat from an artificial skin than a conventional flat fast-dry textile?

## 2. Sample matrix

- **B0 — flat fast-dry control:** conventional-like polyester moisture-management textile.
- **B1 — directional transport only:** directional liquid transport, flat exterior.
- **B2 — exterior structure only:** capillary-fed rib/fin exterior without whole-area heat spreader.
- **B3 — heat spreader only:** whole-area heat spreader with flat exterior.
- **B4 — integrated architecture:** directional transport + heat spreader + capillary delivery + exterior ribs/fins.
- **B5 — intentionally dense exterior:** boundary-layer-overlap/failure control.

For E3b/E3c, B4/B5 exterior structures are further split into micro-rib-only, hierarchical microstructure + macro air-renewal, covered-corridor, open-valley, and segmented-open variants.

## 3. Primary environment

- artificial-skin setpoint: 34 °C;
- ambient temperature: 35 °C;
- relative humidity: 70% for the primary test;
- nominal air speed: <0.05 m/s;
- projected active-area normalization: 0.30 m²;
- liquid-water/synthetic-sweat feed: 150 g/h equivalent;
- minimum independent repeats: n = 3.

Secondary conditions:

- relative humidity: 50%, 85%;
- water feed: 75, 300 g/h equivalent;
- hot-ambient shielding comparison near 40 °C;
- vertical, horizontal, and inverted channel orientation for hierarchical exteriors.

## 4. Fair-comparison rule

All compared samples must receive the same commanded liquid feed in a given test cell. Do not create an apparent advantage by feeding the advanced sample more water than the control.

Record feed mass independently and close the water balance.

## 5. Primary measurement

Measure electrical heater power required to maintain the artificial skin at 34 °C.

For the integrated sample relative to the flat control:

\[
\Delta Q = P_{heater,B4} - P_{heater,B0}
\]

A larger positive value indicates greater heat removal from the artificial skin.

## 6. Provisional decision rules

At 35 °C / 70% RH / 150 g/h equivalent / still air:

- **PASS:** `Delta Q >= 10 W`, n >= 3, coefficient of variation <=10%, water-balance closure >=95%.
- **STRONG PASS:** `Delta Q >= 20 W` under the same comparison.
- **FAIL:** `Delta Q < 5 W`.
- **UNCERTAIN:** 5–10 W, or CV >10%, or inadequate water-balance closure.

These are project decision thresholds, not external standards.

## 7. Measurements

Required:

1. heater electrical power;
2. artificial-skin temperature;
3. ambient temperature and RH;
4. air speed;
5. commanded and measured liquid feed;
6. sample mass before/after;
7. runoff/drip collection;
8. evaporated mass by balance;
9. textile/rib surface temperature.

Strongly recommended:

10. RH and temperature at approximately 0.5, 1, 2, 5, 10, 20, and 40 mm outside the exterior structure where sensor size permits;
11. infrared surface-temperature map;
12. rib wetting fraction;
13. compression state / rib height during operation;
14. macro-corridor dimensions/open fraction for hierarchical samples;
15. signed local corridor flow direction and, where resolvable, magnitude;
16. corridor temperature/RH at inlet, intermediate positions, and outlet.

The combination of heater power, surface temperature, near-surface RH, and signed local air flow is intended to help distinguish vapor-transfer improvement from sensible-heat-transfer change. Do not infer `M_h = M_m` from a single integrated cooling measurement.

## 8. Experiment E1 — direct value test

Compare B0 and B4 at the primary condition.

Hypothesis H1: B4 increases body-side heat removal by >=10 W over 0.30 m² equivalent.

Alternative explanations if H1 fails:

- insufficient effective exterior area;
- insufficient wetting;
- high thermal contact resistance;
- humid boundary-layer overlap;
- runoff instead of evaporation;
- natural-convection cancellation under hot/humid conditions;
- increased inward sensible heat transfer offsetting latent benefit.

## 9. Experiment E2 — ablation

Compare B0/B2/B3/B4.

Hypothesis H2: B4 exceeds both B2 and B3, showing that heat spreading and exterior evaporation enhancement are complementary.

If B4 ~= B2, the heat spreader may be unnecessary under the tested sweat distribution.

If B4 ~= B3, the exterior structured area may not be providing useful mass-transfer enhancement.

## 10. Experiment E3 — exterior pitch/accessibility

Hold exterior material family and approximate height constant; compare pitch around:

- 0.8 mm;
- 1.0 mm;
- 1.5 mm.

Use heater-power gain plus near-surface RH profiles to determine whether tighter geometry increases effective vapor exchange or merely geometric area.

Original hypothesis H3: an intermediate spacing maximizes effective exchange before boundary-layer overlap dominates.

### E3 numerical pre-screen

`docs/e3-boundary-layer-screen.md` provides a periodic 2-D pure-diffusion pre-screen. For the screened 2.5 mm-high, 65%-coverage geometry, it indicates that the idealized distance from rib tips to refreshed ambient air can dominate pitch refinement. At several-millimeter renewal gaps, the predicted benefit of changing pitch from 1.5 mm to 0.8 mm is small.

This is a simulation result only. It motivates E3b rather than replacing physical E3.

## 11. Experiment E3b — hierarchical air renewal

Compare a micro-rib-only exterior against the same/similar wet microstructure combined with larger open air-renewal paths.

Candidate macro structures include:

- open corridors between rib fields;
- valleys between discontinuous evaporator islands;
- spacer-knit channels;
- grooves or corrugations;
- pleat gaps;
- raised stand-off structures preserving an air passage.

Starting research ranges:

- microstructure height: about 2–3 mm;
- local microstructure pitch: about 0.8–1.5 mm;
- macro corridor width: about 1–10 mm;
- corridor/open-valley depth: about 1–5 mm;
- evaporator-field width between corridors: about 5–25 mm.

Measure heater power, RH/T approximately 0.5, 1, 2, 5, 10, and 20 mm above both rib fields and corridors, and signed corridor flow direction where possible.

### Corridor-flow correction

`simulations/corridor_buoyancy_screen.py` shows that a wet vertical channel need not generate upward chimney flow. Evaporative cooling increases air density while humidification reduces it.

`simulations/self_consistent_corridor_1d.py` then couples signed buoyancy flow to wet-wall temperature and channel heat/vapor state for an end-renewed covered rectangular-duct limit. At 35 °C / 70% RH, shallow 100 mm channels become nearly saturated internally and natural buoyancy flow is weak. At 40 °C / 70% RH the same model can predict stronger downward flow while local sensible heat input makes body-side heat flux inward.

Therefore E3b must classify corridor flow as upward, downward, reversing/intermittent, or below measurement resolution before interpreting the mechanism. Vertical, horizontal, and inverted controls are required where practical.

Hypothesis H3b: a two-scale exterior combining wet microstructures with macro air-renewal paths outperforms a dense micro-rib field alone under equal water input. The sign of any buoyancy-driven corridor flow is not assumed in advance.

Provisional hierarchy-specific PASS condition:

- hierarchical sample exceeds micro-rib-only control by >=5 W; and
- shows consistently lower near-surface RH over at least two measurement heights; and
- the result is not explained by greater water input.

Additional **FLOW-MECHANISM SUPPORT** requires a repeatable signed flow response to orientation together with a consistent corridor RH/T profile.

See `experiments/e3b_hierarchical_air_renewal.md` for the detailed protocol.

## 12. Experiment E3c — open valley vs covered corridor

The self-consistent 1-D model is intentionally a covered/end-renewed limit. It predicts that a channel can have nonzero flow and even `Pe_m > 10` while still becoming nearly saturated and losing most of its vapor driving force.

E3c therefore compares:

- **D1:** covered/end-renewed rectangular duct;
- **O1:** same or matched wet floor in a laterally open valley;
- **O2:** segmented open valley with 20–50 mm maximum uninterrupted wet length;
- **O3:** discontinuous evaporator islands separated by ambient-connected gaps.

Primary hypothesis H3c: continuous lateral ambient access and/or segmentation maintains lower local RH and more useful heater-power cooling than an end-renewed covered duct at equal water input and wet area.

Provisional PASS for the open-valley premise at 35 °C / 70% RH:

- mean local RH lower than D1 by >=5 percentage points over at least half of sampled positions;
- heater-power advantage over D1 >=3 W after active-area normalization;
- equal water input within measurement uncertainty;
- water-balance closure >=95%.

See `experiments/e3c_open_vs_covered_corridors.md` for the complete protocol.

## 13. Experiment E4 — humidity boundary

Test the best current B4 sample at 50%, 70%, and 85% RH.

Hypothesis H4: passive advantage decreases strongly as ambient vapor-pressure driving force decreases.

Record the condition where B4 no longer exceeds B0 by a practically useful margin.

## 14. Experiment E5 — heat-spreader orientation

For an anisotropic heat spreader, compare its high-conductivity axis aligned toward the evaporative panel versus rotated approximately 90°.

Hypothesis H5: alignment toward the evaporation zone improves body-side heat removal under spatially nonuniform wetting.

## 15. Experiment E6 — hot-ambient shielding

At elevated ambient temperature, compare dry conductive exterior regions exposed versus thermally shielded.

Hypothesis H6: shielding dry regions reduces parasitic inward heat pickup while preserving wet-zone evaporation.

Also record exterior/ambient temperature gradients so increased sensible exchange is not mistaken for latent-cooling benefit.

## 16. Experiment E7 — mechanical durability

After a baseline measurement, apply controlled bending, stretch, compression, washing, and wet/dry cycling.

Track:

- in-plane thermal conductance;
- capillary delivery rate;
- cooling gain;
- exterior geometry recovery;
- macro-channel open fraction where applicable.

Provisional durability target: retain >=80% of baseline functional performance after the defined cycle protocol.

## 17. Uncertainty

For each primary result, report:

- instrument calibration uncertainty;
- run-to-run standard deviation;
- uncertainty in active area;
- uncertainty in actual water feed;
- humidity and temperature stability;
- RH probe position uncertainty near structured surfaces;
- signed low-speed flow measurement resolution and directional uncertainty;
- estimated combined standard uncertainty where practical;
- coverage factor if expanded uncertainty is reported.

Do not report more numerical precision than measurement uncertainty supports.

Model-screen sensitivity fractions in `simulations/split_transfer_sensitivity.py` are deterministic grid fractions, not statistical probabilities.

## 18. Salt/contamination protocol

Salt deposition is not unique to this architecture. Compare degradation against the same synthetic-sweat exposure in B0.

Only add dedicated salt-management hardware if the proposed architecture exhibits materially faster functional degradation than the conventional control.

No experiment or model should assume that salt evaporates.
