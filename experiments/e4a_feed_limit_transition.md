# E4a — Feed-Limit / Partial-Wetness Transition

Status: planned physical falsification test  
Date: 2026-08-20

## Objective

Test the new homogenized partial-wetness model under a condition where the numerical fully-wet transfer capacity can exceed the imposed liquid feed.

The experiment asks whether increasing feed produces a transition from:

1. **supply-limited / partially wet operation**, where evaporation follows feed;
2. to **transfer-limited / nearly fully wet operation**, where additional feed no longer produces proportional evaporation and instead increases retained liquid or runoff.

## Primary environment

- ambient temperature: 35 °C;
- RH: 50%;
- artificial-skin setpoint: 34 °C;
- nominal still air: <0.05 m/s;
- fixed exterior geometry for all feed points;
- same orientation and compression state at every point.

The 50% RH condition is selected because current screening predicts a supply-limited regime for strong linked exchange at the nominal 150 g/h whole-garment-equivalent feed.

## Sample

Use the best manufacturable O1/O3 open-valley or discontinuous-field specimen available after E3c geometry selection.

Run a flat fast-dry B0 control with the same feed schedule where practical.

## Feed sweep

Recommended whole-garment-equivalent sequence over the 0.30 m² normalization:

- 20 g/h;
- 40 g/h;
- 60 g/h;
- 80 g/h;
- 100 g/h;
- 120 g/h;
- 150 g/h;
- 180 g/h;
- 220 g/h;
- 300 g/h.

If specimen area differs from 0.30 m², scale the commanded mass flow by the declared active projected area and structured/wet-panel fraction. Record the actual delivered mass independently.

## Required measurements

1. signed heater/cooler power or calibrated signed heat flux;
2. artificial-skin temperature;
3. ambient T/RH;
4. actual liquid feed mass rate;
5. evaporated mass by closed water balance;
6. runoff/retained liquid;
7. wet-surface temperature;
8. time-resolved wetness image or equivalent spatial wetness indicator;
9. near-surface T/RH at fixed probe positions;
10. specimen compression and open-valley dimensions.

## Wetness metric

Define an image-derived visible wet fraction

\[
\beta_{img}=A_{visibly\ wet}/A_{declared\ evaporator}.
\]

This is **not assumed equal** to the model's homogenized `beta`. It is an experimental comparison quantity.

If optical contrast is insufficient, use a validated alternative such as calibrated infrared wetness contrast, electrical impedance mapping, or tracer-compatible imaging.

## Hypotheses

### H4a-1 — low-feed mass balance

At sufficiently low feed, evaporation approximately follows delivered liquid mass:

\[
\frac{d\dot m_{evap}}{d\dot m_{feed}}\approx1.
\]

### H4a-2 — increasing wetness

In the supply-limited region, `beta_img` increases with feed.

### H4a-3 — transfer-limit transition

A feed exists above which evaporation grows substantially more slowly than feed and retained liquid/runoff increases.

### H4a-4 — thermal slope change

Heater power/body-side heat flow changes slope near the mass-transfer transition. The model does **not** require a sharp discontinuity.

## Model-specific prediction to falsify

For the current 6 × 3 × 50 mm low-order reference with linked heat/vapor exchange around 0.5 mm, the model predicts a partial-wetness regime at 150 g/h and a transition to full-wet transfer limitation at a higher feed.

This numeric location is not a product specification and should not be used to tune the experiment outcome. The experimental feed sweep must be executed independently.

## PASS / FAIL / UNCERTAIN for the model mechanism

**SUPPORTS PARTIAL-WETNESS MECHANISM** if all are observed:

- low-feed evaporation tracks feed within the combined mass-balance uncertainty;
- wetness indicator increases systematically with feed;
- a reproducible transition to transfer/runoff limitation appears;
- heater-power/body-flux slope changes consistently with the water-balance transition.

**FAILS HOMOGENIZED PARTIAL-WETNESS MECHANISM** if, after ruling out feed/calibration errors:

- evaporation is essentially feed-independent in the supposed low-feed region;
- wetness does not change with feed while mass balance does;
- the inferred transition differs qualitatively between repeat runs without a measured geometric/wetting cause;
- body heat flow changes in the opposite direction to the closed energy balance.

**UNCERTAIN** if wetness cannot be measured reliably or water-balance closure is below 95%.

## Minimum repeats

- n >= 3 independent runs at the low-feed, transition-region, and high-feed points;
- at least one randomized feed-order repeat to detect hysteresis/memory;
- report both ramp-up and ramp-down if time permits.

## Important limitation

The model `beta` is a homogenized sub-grid state under strong thermal spreading. A mismatch between `beta_img` and modeled `beta` does not by itself falsify conservation. It does falsify a literal interpretation of `beta` as visible wet area and may require a spatial two-temperature / wet-dry patch model.