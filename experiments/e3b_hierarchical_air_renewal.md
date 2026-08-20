# E3b — Hierarchical Air-Renewal Exterior Bench Protocol

Date: 2026-08-19  
Status: planned physical experiment

## Objective

Test the E3 numerical finding that micro-scale evaporative ribs require a second, larger length scale that renews ambient air close to the wet surface.

The comparison is not “more geometric area versus less area.” It is:

> the same or similar wet micro-rib field with and without macro-scale ventilation paths.

A second objective is now explicit: determine whether the macro paths produce **upward, downward, reversing, or negligible** still-air flow. The low-order corridor-buoyancy screen shows that evaporative cooling and humidification can oppose each other, so beneficial upward chimney flow must not be assumed.

## Primary environment

- artificial skin: 34 °C setpoint;
- ambient: 35 °C;
- RH: 70%;
- nominal still-air speed: <0.05 m/s;
- equal commanded liquid feed: 150 g/h equivalent over 0.30 m² projected active area;
- minimum independent repeats: n = 3.

Secondary conditions:

- RH 50% and 85%;
- orientation vertical versus horizontal relative to gravity;
- vertical sample inverted top-to-bottom where the geometry permits;
- low walking-equivalent external air speed as a separate follow-up, not mixed with the still-air primary result.

## Sample matrix

### C0 — flat control

Flat fast-dry exterior, no added rib geometry.

### R0 — micro-rib-only control

Representative current rib field:

- rib height approximately 2.5 mm;
- pitch approximately 0.8–1.0 mm;
- no deliberate macro ventilation corridor.

### H1 — narrow-corridor hierarchy

Same micro-rib family with periodic open corridors. Starting screen:

- corridor width: 1–3 mm;
- rib-field width between corridors: 5–15 mm.

### H2 — wide-corridor hierarchy

Same micro-rib family with larger open corridors. Starting screen:

- corridor width: 3–6 mm;
- rib-field width between corridors: 10–25 mm.

### H3 — raised spacer / channel architecture

Micro-rib evaporation zones combined with 3-D spacer-knit, pleated, grooved, or equivalent passages that preserve an open air path above or between wet structures.

### H4 — orientation control

Best hierarchical geometry rotated approximately 90° to test whether buoyant or motion-induced air renewal is orientation-sensitive.

### H5 — gravity-direction control

Best vertical-channel geometry inverted top-to-bottom where mechanically possible. Compare flow direction and cooling while preserving the same wet-area layout and liquid feed.

## Controlled quantities

Hold as constant as practical across R0/H1/H2/H3:

- wettable material family;
- projected active area;
- liquid feed;
- rib height and local pitch inside the rib field;
- skin-side thermal interface;
- heat-spreader architecture;
- sample preconditioning.

Record any reduction in wet structured area caused by adding corridors. A hierarchical sample must not be credited for improved RH profiles if it simply receives less water or contains substantially less wet area without that fact being reported.

## Measurements

Primary:

1. heater electrical power required to hold the artificial skin at 34 °C;
2. actual liquid feed by mass;
3. evaporated mass and runoff;
4. ambient temperature/RH and air speed.

Boundary-layer measurements:

5. RH and temperature approximately 0.5, 1, 2, 5, 10, and 20 mm above representative rib fields;
6. the same measurements above macro corridors;
7. local corridor air temperature/RH near inlet, mid-height, and outlet where sensor intrusion is acceptable.

Flow-direction measurements:

8. determine whether corridor flow is upward, downward, reversing/intermittent, or below resolution;
9. preferred methods: low-disturbance tracer visualization, micro-PIV, bidirectional thermal anemometry, or another calibrated low-speed method;
10. record flow sign before reporting flow magnitude; if the method cannot resolve sign, report that limitation explicitly;
11. compare vertical, horizontal, and inverted orientation so a gravity-driven component can be separated from leakage, room drift, or instrumentation bias.

Structure measurements:

12. actual rib height under wet operation;
13. corridor width and open fraction;
14. wetting fraction of ribs and corridor surfaces;
15. compression after garment-like contact or bending.

## Derived quantities

Integrated cooling advantage relative to flat control:

\[
\Delta Q_{B4} = P_{heater,sample} - P_{heater,C0}
\]

Incremental hierarchy benefit relative to the micro-rib-only control:

\[
\Delta Q_{hier} = P_{heater,Hx} - P_{heater,R0}
\]

Near-surface humidity reduction at height `z`:

\[
\Delta RH(z) = RH_{R0}(z) - RH_{Hx}(z)
\]

Positive `Delta RH` means the hierarchical sample keeps the local air drier at the same measurement height.

For directional flow, define a signed channel velocity convention before data collection:

- positive = upward along gravity-opposing vertical channel direction;
- negative = downward;
- zero/indeterminate = below validated instrument resolution or strongly reversing.

Do not average signed flow to a misleading near-zero value without also reporting reversal/intermittency.

## Provisional decision rules

These are project screening criteria, not external standards.

**PASS E3b:** at the primary condition, at least one hierarchical sample:

- exceeds R0 by >=5 W in heater-power requirement, **and**
- shows a consistently lower near-surface RH profile over at least two measurement heights, **and**
- does not achieve the result through substantially greater liquid feed.

**STRONG PASS:** hierarchical sample also exceeds the flat control by >=10 W and retains the advantage across n >= 3 repeats with CV <=10%.

**FLOW-MECHANISM SUPPORT:** a repeatable signed corridor flow changes predictably with vertical/horizontal/inverted orientation and is associated with a repeatable RH/temperature profile along the corridor.

**FAIL:** hierarchical channels do not improve heater power or near-surface RH relative to R0, or any gain is explained by unequal water input / reduced wetting rather than better air renewal.

**UNCERTAIN:** heater-power advantage is <5 W but boundary-layer RH changes are repeatable, or corridor flow exists but does not correlate with improved vapor renewal. This would suggest heat-transfer coupling, reduced wet area, or a competing sensible-heat effect may be limiting.

## H / T / D / C / U

**H:** a two-scale exterior combining wet microstructures with macro air-renewal paths outperforms a dense micro-rib field alone under equal water input; a gravity-dependent flow component may exist but its sign is not assumed in advance.

**T:** C0/R0/H1/H2/H3, n >= 3 at 35 °C / 70% RH / 150 g/h equivalent, followed by orientation controls H4/H5.

**D:** use the PASS/FAIL/UNCERTAIN and FLOW-MECHANISM SUPPORT rules above.

**C:** macro corridors may reduce wet area too much; heat-spreader contact may dominate; natural convection may already renew R0 sufficiently; corridor flow may reverse because cooling and humidification have opposite density effects; compression may close the intended passages; room drift may overwhelm weak buoyancy.

**U:** major uncertainties are low-speed bidirectional flow measurement, sensor intrusion, ambient room drift, RH sensor disturbance, actual wet area, rib collapse, thermal contact resistance, and liquid-feed uniformity. Report run-to-run variation, calibration uncertainty, and minimum resolvable signed velocity.

## Design implication if supported

A supported result would move the preferred exterior from a single-scale “dense micro-rib surface” toward a hierarchical structure comprising:

- wet micro-ribs / short fins / 3-D knit for local evaporation area;
- larger open corridors, valleys, spacer channels, or discontinuous rib islands for passive or motion-assisted air renewal;
- multiple openings/orientations that do not depend on one assumed chimney-flow direction;
- heat-spreader routing that thermally feeds wet fields without unnecessarily exposing dry conductive regions to hot ambient air.
