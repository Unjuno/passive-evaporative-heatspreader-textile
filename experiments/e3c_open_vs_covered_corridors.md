# E3c — Open Valley vs Covered Corridor Validation

Date: 2026-08-20  
Status: planned physical experiment

## Objective

Test two numerical limitations now present in the repository:

1. a long end-renewed covered channel can carry some buoyancy flow while still becoming nearly saturated;
2. centimeter-scale end segmentation does not materially rescue vapor renewal when the interior lateral exchange is weak.

The physical question is therefore:

> does **continuous lateral ambient access** preserve vapor driving force better than an end-renewed or sparsely interrupted path at the same water input and wet area?

## Samples

### C0 — flat control

Flat fast-dry exterior at the same water input.

### D1 — covered/end-renewed duct

A rectangular channel with a wet floor, sidewalls/cover, and ambient connection primarily at the two ends.

Starting geometry:

- width: 6–10 mm;
- depth: 3–5 mm;
- length: 50–100 mm.

This approximates the limiting case represented by `simulations/self_consistent_corridor_1d.py`.

### O1 — continuously laterally open valley

Same or closely matched wet floor width/depth/length as D1, but exposed to ambient air continuously along its length.

This is the principal design candidate.

### O2a — centimeter-scale interrupted valley negative/control case

Same local cross-section as O1, with end/cross openings approximately every 20–50 mm.

The distributed 1-D screen predicts that this spacing is too coarse to materially change the interior vapor state when lateral exchange remains weak. O2a is retained as a falsification/control condition rather than a preferred design.

### O2b — millimeter-scale short segments

Same local cross-section but with wet path lengths around:

- 1 mm;
- 2 mm;
- 3 mm;

where manufacturable and measurable.

The current 6 × 3 mm numerical screen gives an exchange length of roughly 0.7–1.1 mm for the tested lateral-exchange range, so millimeter-scale end access can change the interior state whereas 20–50 mm segmentation usually does not.

O2b may be implemented as short wet bars, interrupted ribs, transverse cuts, or small evaporator islands rather than literal covered ducts.

### O3 — discontinuous evaporator islands

Wet microstructured fields separated by open ambient-connected gaps. Total wet area should be matched to O1/O2 as closely as practical.

This is the most apparel-relevant implementation of frequent ambient access if 1–3 mm literal segments are impractical.

## Primary environment

- artificial skin: 34 °C setpoint;
- ambient: 35 °C;
- RH: 70%;
- nominal far-field air speed: <0.05 m/s;
- equal commanded liquid feed across samples;
- n >= 3 independent repeats.

Secondary conditions:

- 35 °C / 50% RH;
- 35 °C / 85% RH;
- 40 °C / 70% RH;
- vertical, horizontal, and inverted orientation where mechanically possible;
- optional controlled external airflow after the passive still-air condition is complete.

## Required measurements

1. heater power required to hold artificial skin at 34 °C;
2. actual liquid feed and runoff;
3. sample mass change / evaporation balance;
4. wet-surface temperature;
5. ambient T/RH and far-field air speed;
6. channel/valley T and RH at multiple axial positions;
7. local T/RH approximately 0.5–5 mm above continuously open regions;
8. signed local air velocity or tracer-flow direction where measurable;
9. actual wet area and geometry after wetting/compression;
10. exact spacing between ambient-connected interruptions or islands.

Wet-surface temperature and local dry-bulb temperature are required with RH because RH alone is not a vapor-density driving-force measure when temperatures differ.

## Derived metrics

### Useful cooling difference

\[
\Delta Q_{O-D}=P_{heater,O}-P_{heater,D1}.
\]

Positive values favor the laterally open geometry.

### Vapor-driving-force retention

For each measurement position `x`, calculate

\[
\theta(x)=
\frac{\rho_{v,valley}(x)-\rho_{v,\infty}}
{\rho_{v,sat}(T_s(x))-\rho_{v,\infty}},
\qquad
F(x)=1-\theta(x).
\]

When `0 < theta < 1`, the local renewal-to-wet vapor-conductance ratio may be inferred as

\[
R(x)=\frac{1-\theta(x)}{\theta(x)}.
\]

`F` is the primary mechanism metric. Exact large `R` values are secondary because the inverse problem becomes ill-conditioned as valley air approaches ambient conditions.

Interpretation targets:

- `F >= 0.50` corresponds to `R >= 1`;
- `F >= 0.80` corresponds to `R >= 4`;
- `F >= 0.90` corresponds to `R >= 9`.

These are mechanism targets, not garment PASS thresholds.

### Segment-length normalization

For each interrupted sample report

\[
\Lambda=L_{segment}/\ell_{exchange},
\]

where the numerical screening exchange length is

\[
\ell_{exchange}=\sqrt{\frac{D_v A}{G'_w+G'_a}}.
\]

The current model predicts that end openings become weakly relevant once `Lambda` is much larger than one. This dimensionless ratio should be compared with physical RH/T profiles rather than treated as a validated material constant.

### Water balance

Require

\[
\frac{|m_{feed}-(m_{evap}+m_{runoff}+\Delta m_{sample})|}{m_{feed}} \le 0.05
\]

for a primary PASS-quality run.

## Hypotheses

**H3c-1:** O1 maintains lower local vapor loading `theta` and higher `F` than D1 under equal water input.

**H3c-2:** O2a (20–50 mm interruptions) gives little or no improvement over a long weakly renewed path when its interior remains laterally stagnant.

**H3c-3:** O2b/O3 with millimeter-scale or continuously distributed ambient access produces higher `F` than O2a at matched wet area.

**H3c-4:** at 40 °C / 70% RH, greater air exchange can increase sensible heat input; the geometry with the largest velocity or vapor renewal need not produce the largest useful body cooling.

## Decision rules

These are project screening rules, not external standards.

### PASS open-valley premise

At 35 °C / 70% RH, at least one of O1/O2b/O3 must satisfy all of:

- clearly higher temperature-corrected vapor-driving-force retention `F` than D1;
- heater-power advantage over D1 >=3 W over the tested active area after area normalization;
- equal liquid input within measurement uncertainty;
- water-balance closure >=95%.

### SUPPORT for the distributed-renewal model

The numerical interpretation is supported if the physical ordering is broadly:

`O1 or O2b/O3 > O2a > or ~= D1`

in median `F`, with centimeter-scale interruption showing materially less benefit than continuous/millimeter-scale ambient access.

Exact agreement with a numerical `delta_open` value is **not** required because `delta_open` is an effective exchange thickness, not direct geometry.

### STRONG PASS

In addition to PASS:

- open configuration also exceeds flat control by >=10 W over 0.30 m² equivalent;
- result repeats with CV <=10%;
- the advantage remains after controlling for wet area.

### FAIL

- continuous lateral opening does not improve `F` relative to D1; or
- `F` improves but heater power does not, indicating another bottleneck; or
- apparent gain is explained by unequal water input, wet area, or uncontrolled airflow.

### UNCERTAIN

- repeatable vapor-renewal improvement without clear heater-power gain;
- large run-to-run variation;
- local probes materially disturb the small flow;
- inferred `F` is dominated by T/RH position uncertainty.

## H / T / D / C / U

**H:** continuous or millimeter-scale ambient access provides more useful vapor renewal than long end-renewed or centimeter-scale interrupted paths.

**T:** C0/D1/O1/O2a/O2b/O3 at the primary environment, n>=3, equal liquid input, spatial T/RH, wet-surface T, heater power, water balance, and signed flow where measurable.

**D:** use PASS/STRONG PASS/FAIL/UNCERTAIN above and separately report the `F` mechanism classification.

**C:** open geometry may reduce wet area; probe intrusion may alter the local field; the screened Sherwood number may overestimate wet-wall transfer; external room currents may dominate; heat-spreader coupling may be limiting.

**U:** dominant uncertainties are low-speed flow measurement, RH/T probe size and position, wet-surface temperature, wet-area determination, local compression, thermal contact, and far-field stability. Propagate T/RH uncertainty into vapor density, `theta`, and `F`. Avoid over-interpreting exact large `R` values.
