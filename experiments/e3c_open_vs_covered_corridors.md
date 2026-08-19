# E3c — Open Valley vs Covered Corridor Validation

Date: 2026-08-19  
Status: planned physical experiment

## Objective

Test the central limitation identified by the self-consistent 1-D corridor
screen:

> a long end-renewed covered channel can carry some buoyancy flow while still
> becoming nearly saturated and losing most of its vapor driving force.

The experiment therefore compares an exterior path that is open to ambient air
along its length against a geometrically similar covered/end-renewed path.

## Samples

### C0 — flat control

Flat fast-dry exterior at the same water input.

### D1 — covered/end-renewed duct

A rectangular channel with a wet floor, sidewalls/cover, and ambient connection
primarily at the two ends.

Suggested starting geometry:

- width: 6–10 mm;
- depth: 3–5 mm;
- length: 100 mm.

This sample approximates the limiting case represented by
`simulations/self_consistent_corridor_1d.py`.

### O1 — laterally open valley

Same or closely matched wet floor width/depth/length, but with the path exposed
to ambient air continuously along its length rather than covered.

### O2 — segmented open valley

Same local valley cross-section as O1, divided by openings/cross-cuts so no
continuous wet segment exceeds approximately 20–50 mm.

### O3 — discontinuous evaporator islands

Wet microstructured fields separated by open ambient-connected gaps.  Total wet
area should be matched to O1/O2 as closely as practical.

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
- vertical, horizontal, and inverted orientation where mechanically possible.

## Required measurements

1. heater power required to hold artificial skin at 34 °C;
2. actual liquid feed and runoff;
3. sample mass change / evaporation balance;
4. wet-surface temperature;
5. ambient T/RH and far-field air speed;
6. channel/valley T and RH at inlet, 25%, 50%, 75%, and outlet positions;
7. local RH approximately 1–5 mm above an open valley;
8. signed local air velocity or tracer-flow direction where measurable;
9. actual wet area and geometry after wetting/compression.

## Derived metrics

### Useful cooling difference

\[
\Delta Q_{O-D}=P_{heater,O}-P_{heater,D1}.
\]

Positive values favor the laterally open geometry.

### Humidity saturation penalty

For each axial position `x`, report

\[
S(x)=RH(x)-RH_{ambient}.
\]

Also report the fraction of the channel/valley length with `RH > 95%`.

The 95% threshold is only a reporting marker, not a universal physical cutoff.

### Water balance

Require

\[
\frac{|m_{feed}-(m_{evap}+m_{runoff}+\Delta m_{sample})|}{m_{feed}} \le 0.05
\]

for a primary PASS-quality run.

## Hypotheses

**H3c-1:** O1 maintains lower mean local RH than D1 under equal water input.

**H3c-2:** O2 reduces the saturated-length fraction relative to O1 while
retaining or improving heater-power benefit.

**H3c-3:** at 40 °C / 70% RH, greater air renewal can increase sensible heat
input; therefore the geometry with the largest velocity need not produce the
largest useful body cooling.

## Decision rules

These are project screening rules, not external standards.

### PASS open-valley premise

At 35 °C / 70% RH, at least one open configuration must satisfy all of:

- lower mean local RH than D1 by >=5 percentage points over at least half of the
  sampled positions;
- heater-power advantage over D1 >=3 W over the tested active area after area
  normalization;
- equal liquid input within measurement uncertainty;
- water-balance closure >=95%.

### STRONG PASS

In addition to PASS:

- open configuration also exceeds the flat control by >=10 W over 0.30 m²
  equivalent;
- result repeats with CV <=10%;
- the advantage remains after controlling for wet area.

### FAIL

- open geometry does not reduce humidity accumulation relative to D1; or
- RH improves but heater power does not, indicating another bottleneck; or
- any apparent gain is explained by unequal water input, different wet area,
  or uncontrolled external airflow.

### UNCERTAIN

- repeatable RH reduction without a clear heater-power gain;
- large run-to-run variation;
- local velocity too small for reliable sign measurement.

## H / T / D / C / U

**H:** continuous lateral ambient access and/or segmentation provides more
useful vapor renewal than an end-renewed covered corridor.

**T:** C0/D1/O1/O2/O3 at the primary environment, n>=3, equal liquid input,
with spatial RH/T and heater power.

**D:** use PASS/STRONG PASS/FAIL/UNCERTAIN above.

**C:** open geometry may simply reduce wet area, probe intrusion may alter the
small flow, external room currents may dominate buoyancy, or heat-spreader
coupling may be the true limit.

**U:** dominant uncertainties are low-speed velocimetry, RH probe size and
position, wet-area determination, local compression, thermal contact, and
far-field air-speed stability.  Report calibration and placement uncertainty.
