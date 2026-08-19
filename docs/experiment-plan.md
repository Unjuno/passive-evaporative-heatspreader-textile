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
- hot-ambient shielding comparison near 40 °C.

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

10. RH and temperature at approximately 2, 5, 10, 20, and 40 mm outside the exterior structure;
11. infrared surface-temperature map;
12. rib wetting fraction;
13. compression state / rib height during operation.

## 8. Experiment E1 — direct value test

Compare B0 and B4 at the primary condition.

Hypothesis H1: B4 increases body-side heat removal by >=10 W over 0.30 m² equivalent.

Alternative explanations if H1 fails:

- insufficient effective exterior area;
- insufficient wetting;
- high thermal contact resistance;
- humid boundary-layer overlap;
- runoff instead of evaporation;
- natural-convection cancellation under hot/humid conditions.

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

Use heater-power gain plus near-surface RH profiles to infer whether tighter geometry increases effective exchange or merely geometric area.

Hypothesis H3: an intermediate spacing maximizes effective exchange before boundary-layer overlap dominates.

## 11. Experiment E4 — humidity boundary

Test the best current B4 sample at 50%, 70%, and 85% RH.

Hypothesis H4: passive advantage decreases strongly as ambient vapor-pressure driving force decreases.

Record the condition where B4 no longer exceeds B0 by a practically useful margin.

## 12. Experiment E5 — heat-spreader orientation

For an anisotropic heat spreader, compare its high-conductivity axis aligned toward the evaporative panel versus rotated approximately 90°.

Hypothesis H5: alignment toward the evaporation zone improves body-side heat removal under spatially nonuniform wetting.

## 13. Experiment E6 — hot-ambient shielding

At elevated ambient temperature, compare dry conductive exterior regions exposed versus thermally shielded.

Hypothesis H6: shielding dry regions reduces parasitic inward heat pickup while preserving wet-zone evaporation.

## 14. Experiment E7 — mechanical durability

After a baseline measurement, apply controlled bending, stretch, compression, washing, and wet/dry cycling.

Track:

- in-plane thermal conductance;
- capillary delivery rate;
- cooling gain;
- exterior geometry recovery.

Provisional durability target: retain >=80% of baseline functional performance after the defined cycle protocol.

## 15. Uncertainty

For each primary result, report:

- instrument calibration uncertainty;
- run-to-run standard deviation;
- uncertainty in active area;
- uncertainty in actual water feed;
- humidity and temperature stability;
- estimated combined standard uncertainty where practical;
- coverage factor if expanded uncertainty is reported.

Do not report more numerical precision than measurement uncertainty supports.

## 16. Salt/contamination protocol

Salt deposition is not unique to this architecture. Compare degradation against the same synthetic-sweat exposure in B0.

Only add dedicated salt-management hardware if the proposed architecture exhibits materially faster functional degradation than the conventional control.

No experiment or model should assume that salt evaporates.
