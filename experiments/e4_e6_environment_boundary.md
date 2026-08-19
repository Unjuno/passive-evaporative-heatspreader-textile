# E4/E6 — Environmental Sign-Boundary and Hot-Ambient Validation

Date: 2026-08-20  
Status: planned physical experiment

## Objective

Test the analytic/model prediction that a passive same-path wet exterior can continue evaporating water while net heat flow at the artificial-skin interface changes sign as ambient temperature and humidity increase.

This is an engineering heat-flow experiment. It is **not** a human safety or heat-stress experiment.

## Why the apparatus must be bidirectional

The normal B0/B4 experiment uses heater power required to hold an artificial skin at 34 °C. That works while the specimen removes heat from the plate.

Above the predicted environmental sign boundary, the specimen may instead deliver heat **into** the plate. A heater-only controller can fall to zero power but cannot measure the magnitude of inward heat flow.

Therefore E4/E6 requires at least one of:

1. a bidirectional Peltier/thermoelectric plate with calibrated electrical/thermal balance;
2. a thermostatic liquid plate capable of both supplying and removing heat, with calibrated heat-flow measurement;
3. a calibrated heat-flux sensor between the controlled plate and specimen plus independent plate temperature control.

Report signed heat flux using a declared convention. Recommended:

- positive = heat leaving artificial skin into garment;
- negative = heat entering artificial skin from garment/environment.

## Model boundary used only to choose test points

For the current same-path linked heat/vapor screen with `T_skin=34 °C`:

\[
\frac{k_{air}}{D_v}(T_\infty-T_{skin})
=
L_v\left[\rho_{v,sat}(T_{skin})-\phi_\infty\rho_{v,sat}(T_\infty)\right].
\]

Representative model zero-flux points:

| ambient temperature | model critical RH |
|---:|---:|
| 35 °C | 93.9% |
| 36 °C | 88.2% |
| 37 °C | 82.9% |
| 38 °C | 77.9% |
| 39 °C | 73.2% |
| 40 °C | 68.8% |
| 42 °C | 60.9% |
| 45 °C | 50.8% |

These values are test-placement hypotheses, not measured thresholds.

## Samples

At minimum:

- **B0:** flat fast-dry control;
- **B4-open:** current integrated heat-spreader + capillary-fed continuously open wet exterior;
- **B4-shield:** same wet architecture with intended dry-side/hot-ambient thermal shielding or routing modification;
- optional **wet-reference plate/textile** without whole-garment heat spreader for mechanism separation.

## Test sequence

### Phase A — fixed 35 °C, humidity approach to the boundary

Suggested RH levels:

- 70%;
- 85%;
- 90%;
- 92%;
- 94%;
- 96% where chamber capability/condensation control permits.

Purpose: verify whether signed body-side heat flow approaches zero near the predicted ~93.9% RH boundary.

### Phase B — fixed 40 °C, humidity approach to the boundary

Suggested RH levels:

- 50%;
- 60%;
- 65%;
- 69%;
- 75%.

Purpose: straddle the predicted ~68.8% RH boundary.

### Phase C — temperature sweep at 70% RH

Suggested dry-bulb levels:

- 35 °C;
- 37 °C;
- 38.5 °C;
- 39.5 °C;
- 40.5 °C;
- 42 °C.

The current model predicts zero body-side heat flow near 39.73 °C at 70% RH.

## Water-input rule

Use the same commanded feed for compared samples at each environmental point.

However, classify the run as supply-limited when the exterior cannot remain wet at that feed. Do not interpret a drying specimen as a fully wet transfer-capacity test.

For boundary identification, a secondary controlled-wetness protocol may deliberately provide enough water to maintain a visibly/gravimetrically wet reference surface. Such a test must be reported separately from the fixed-150-g/h garment benchmark.

## Required measurements

1. signed body-side heat flux or bidirectional heat-control power;
2. artificial-skin temperature;
3. wet-surface temperature;
4. ambient dry-bulb and RH;
5. local near-surface/valley T and RH;
6. water feed;
7. evaporation mass / sample mass change / runoff;
8. wet-area fraction;
9. dry-region surface temperature;
10. local/far-field air speed;
11. visible/IR condensation where relevant.

## Primary derived quantities

### Signed body heat flux

\[
q''_{body}>0
\]
means useful heat removal from the artificial skin.

\[
q''_{body}<0
\]
means environmental/garment heat enters the artificial skin.

### Evaporation/body-cooling decoupling

Report both

\[
\dot m''_{evap}
\]

and

\[
q''_{body}.
\]

A state with positive evaporation but negative `q_body` is classified as **evaporating / body-heating**, not cooling.

## Hypotheses

**H4a:** at fixed 34 °C artificial-skin temperature, the sign of body-side heat flow crosses zero as ambient T/RH crosses a reproducible environmental boundary.

**H4b:** the measured boundary follows the qualitative model trend: increasing RH lowers the dry-bulb temperature at which the sign reversal occurs.

**H6a:** dry-side shielding/routing can reduce parasitic inward heat through dry conductive regions.

**H6b:** shielding dry regions does not necessarily eliminate sensible heat entering the actively wet surface itself; this must be measured rather than assumed.

## Decision rules

### SUPPORT for environmental-boundary hypothesis

- signed body heat flux changes sign reproducibly across the test matrix; and
- the zero crossing moves to lower ambient temperature as RH increases; and
- positive evaporation is observed on at least one point with zero/negative body-side heat flow.

Exact agreement with the analytic boundary is not required.

### FAIL / model rejection signal

- no sign reversal appears over a sufficiently broad fully wet test range where the model predicts one; or
- the measured trend with RH is opposite to the model; or
- sign changes are fully explained by uncontrolled water supply, condensation, or apparatus drift.

### UNCERTAIN

- apparatus cannot resolve signed heat flux near zero;
- wet area changes strongly across conditions;
- condensation on chamber/sensors corrupts water balance;
- plate cannot maintain 34 °C bidirectionally.

## H / T / D / C / U

**H:** the passive same-path wet exterior has a T/RH-dependent body-heat-flow sign boundary.

**T:** B0/B4-open/B4-shield around the predicted boundary, n>=3 near critical points, with signed heat flow, wet-surface T, water balance, local T/RH and wet area.

**D:** SUPPORT/FAIL/UNCERTAIN as above.

**C:** real heat/mass analogy differs from model; radiation matters; wetting becomes patchy; chamber flow changes; heat spreader changes surface temperature field; condensation occurs.

**U:** dominant sources are signed heat-flux calibration, plate control error, RH/T uncertainty, probe position, wet area, water balance, radiation, and chamber flow. Report combined uncertainty near the zero crossing and avoid quoting a critical temperature/RH more precisely than the uncertainty supports.
