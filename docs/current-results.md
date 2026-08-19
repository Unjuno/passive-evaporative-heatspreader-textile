# Current Numerical Results

Status: **SIMULATION / SCREENING ONLY — NO PHYSICAL GARMENT PERFORMANCE DATA YET**  
Compiled: 2026-08-19

This document consolidates principal quantitative results from earlier exploratory models. Values are approximate and are retained as a research record. Stable-release results must be regenerated from repository code.

## 1. Water/latent-heat scale

Using a representative latent heat of vaporization near `2.4–2.42 MJ/kg`, 50 W of latent heat corresponds to roughly 74–75 g/h of water evaporation.

Important: latent heat at the evaporating exterior is not necessarily equal to heat removed from the wearer; ambient convection/radiation can supply part of the evaporation energy.

## 2. Whole-body lateral heat spreading under patchy evaporation

A prior 2D screening model used spatially nonuniform evaporation over approximately 25% of the modeled area.

| In-plane conductivity (W/mK) | Body-side cooling (W) | Spatial temperature SD (°C) |
|---:|---:|---:|
| 0.2 | ~16.1 | ~1.46 |
| 2 | ~16.9 | ~1.40 |
| 20 | ~20.3 | ~1.13 |
| 200 | ~27.3 | ~0.44 |

Interpretation: lateral heat spreading produced the largest benefit when evaporation was spatially uneven. In a uniform-equivalent evaporation case, increasing in-plane conductivity had much less effect.

## 3. Mass/performance tradeoff for continuous heat spreaders

An abstract 0.30 m² screen found that continuous high-conductivity sheets can become too heavy for clothing.

Representative exploratory outputs included:

- baseline: ~10.3 W body-side cooling;
- maximum screened: ~21.4 W;
- carbon-like case around `k = 150 W/mK`, thickness `0.8 mm`, mass ~432 g: ~20.5 W.

This motivated thin, anisotropic, patterned, and discontinuous heat-spreader architectures.

## 4. Thin anisotropic heat-spreader screening

Representative aligned anisotropic case: `kx = 200 W/mK`, `ky = 15 W/mK`.

| Thickness (mm) | Approx. mass (g) | Body-side cooling (W) |
|---:|---:|---:|
| 0.05 | 24.0 | 16.04 |
| 0.08 | 38.4 | 17.19 |
| 0.10 | 48.0 | 17.78 |
| 0.15 | 72.0 | 18.92 |
| 0.20 | 96.0 | 19.74 |

At `0.10 mm` in the same abstract geometry:

- aligned `kx=200, ky=15`: ~17.78 W;
- reversed `kx=15, ky=200`: ~13.09 W;
- isotropic `k=100`: ~16.04 W;
- isotropic `k=200`: ~17.78 W.

Interpretation: orientation can matter strongly when wet/evaporative regions are spatially organized.

## 5. Dry-side shielding in hot ambient air

A prior screen near 40 °C ambient showed approximately +9 W body-side advantage for shielding dry exterior regions versus leaving them exposed in the top screened designs.

Interpretation: a dry high-conductivity exterior can become a parasitic inward heat collector when ambient temperature exceeds skin/garment temperature.

## 6. Stretchable serpentine heat paths

A geometric serpentine screen estimated retained single-path thermal conductance as extension increases:

| Target extension | Approx. retained conductance |
|---:|---:|
| 5% | ~95% |
| 10% | ~91% |
| 15% | ~87% |
| 20% | ~83% |
| 30% | ~77% |

This is a path-length/geometric screen, not a fatigue measurement.

## 7. Exterior exchange model and equilibrium-branch audit

The original low-order passive model describes exterior performance with an effective exchange multiplier `M` relative to a flat wet textile.

Earlier v1.3/v1.4 exploratory summaries reported single threshold values such as `M ~ 2.5–3.5` for a modeled +10 W advantage at 35 °C / 70% RH. **Those threshold values are no longer accepted as robust design criteria.**

Repository audit found that the nonlinear heat/mass balance can contain multiple stable surface-temperature equilibria. Earlier code selected the stable root with the greatest body-side cooling, which can produce an optimistic jump.

Under the current frozen screening parameters at `35 °C / 70% RH / 150 g/h`:

- the flat control (`M=1`, `U=60 W/(m²K)`) has a modeled body-side cooling near 4.84 W;
- around `M=3.5`, the advanced `U=100 W/(m²K)` case can exhibit **two stable branches**;
- one branch gives only about +7.9 W over the flat control;
- the colder branch gives roughly +14.7 W over the flat control;
- the warm stable branch persists in the present low-order model until roughly `M ~ 9.77`, after which the model jumps to the colder branch.

These values are a numerical-model audit result, not a physical prediction of hysteresis in a garment. They show that a single `M` threshold is not defensible until the natural-convection model and branch-selection physics are validated.

The repository model now reports all stable roots and defaults to a warmer/conservative branch when a single value is required.

## 8. Preview-like exterior rib geometry

For a visual concept interpreted approximately as:

- structured-panel coverage `f = 0.45`;
- rib height `h = 2.0 mm`;
- pitch `p = 1.5 mm`;

`G_panel ~ 3.67`.

For `alpha = 0.55`, the geometric mapping gives `M ~ 1.66`; for `alpha = 1.0`, `M ~ 2.2`.

These are geometric/exchange mappings only. Because of the equilibrium-branch issue above, they should not currently be converted into a single claimed cooling gain without reporting branch behavior.

## 9. Exterior candidate region remains an experimental hypothesis

Aesthetic/performance exploration currently prioritizes roughly:

- structured-panel coverage: 55–70%;
- rib height: 2–3 mm;
- rib pitch: 0.8–1.0 mm;
- rounded/flexible textile-like ribs;
- large-area heat spreading retained.

This is **not yet an optimized design**. Tight pitch increases geometric area but may reduce effective accessibility because neighboring wet structures share a humid boundary layer.

## 10. Salt mass-balance correction

No current result assumes salt evaporation.

A previous conservative NaCl-equivalent mass balance at 150 g/h water throughput for 8 h gave retained-salt scales of approximately:

- ~1.4 g at 20 mmol/L;
- ~2.8 g at 40 mmol/L;
- ~4.2 g at 60 mmol/L;
- ~5.6 g at 80 mmol/L.

These values only illustrate mass scale. Ordinary garments also retain nonvolatile sweat residues. Dedicated salt-management hardware should be justified only by comparative degradation data.

## 11. Stable-release re-run requirements

Before a stable versioned release, regenerate and archive:

1. full stable-equilibrium branch maps versus exterior exchange, RH, water input, and `U`;
2. split `M_h` / `M_m` sensitivity tables;
3. rib geometry/accessibility design space and E3 boundary-layer tables;
4. prescribed-state and self-consistent corridor-flow screens;
5. anisotropic heat-spreader orientation comparison;
6. hot-ambient dry-side shielding comparison;
7. uncertainty/sensitivity bounds;
8. reference CSVs with code commit SHA and parameter metadata.

The primary physical experiments must determine which low-order branch/boundary-layer/corridor behavior corresponds to real textile operation.

## 12. E3 periodic rib-diffusion / boundary-layer screen

A 2-D periodic steady-diffusion model isolates humidity-boundary-layer sharing between neighboring wet ribs. It solves normalized vapor diffusion with wet textile surfaces at `u=1`, a prescribed refreshed-air plane at `u=0`, and periodic lateral boundaries.

This model reports a **mass-transfer multiplier only**. It is not CFD, does not include buoyancy or walking airflow, and must not be interpreted as a measured `alpha` or a garment cooling wattage.

Screened geometry:

- rib height `h = 2.5 mm`;
- structured-panel coverage `f = 0.65`;
- pitch `p = 0.8, 1.0, 1.5 mm`;
- rib width approximately `0.24–0.25 mm`.

Selected whole-garment vapor-transfer multipliers `M_m`:

| renewal gap above rib tip | p=0.8 mm | p=1.0 mm | p=1.5 mm |
|---:|---:|---:|---:|
| 0.5 mm | 3.785 | 3.548 | 3.098 |
| 1.0 mm | 2.481 | 2.400 | 2.229 |
| 2.0 mm | 1.765 | 1.736 | 1.673 |
| 5.0 mm | 1.312 | 1.304 | 1.286 |
| 7.5 mm | 1.209 | 1.204 | 1.193 |

Using the older `M≈3.5` value only as a cross-model screening reference, the idealized refreshed-air plane must be within roughly 0.4–0.5 mm of the rib tips for this geometry. At a several-millimeter stagnant renewal gap, pitch refinement by itself provides little additional effective transfer.

A grid-convergence check for `p=1.0 mm`, `h=2.5 mm`, and renewal height 3.0 mm gave whole-area multiplier values from 3.528 at 16 nodes/pitch to 3.570 at 48 nodes/pitch; the 24-node result differs from the finest screened value by about -0.62%.

**Design consequence:** the preferred exterior should be treated as hierarchical rather than single-scale. Wet micro-ribs/3-D-knit relief supply local area, while larger open paths are needed to connect those wet surfaces to refreshed ambient air.

## 13. Split sensible-heat / vapor-transfer model

The thermal model now separates:

- `M_h`: multiplier applied to sensible convective heat transfer;
- `M_m`: multiplier applied to water-vapor mass transfer;
- `h_rad`: independent linearized radiative exchange.

This corrects a strong earlier simplification in which one exterior multiplier scaled both sensible and vapor exchange. The old model remains a regression-tested special case when `M_h = M_m = M`.

E3 outputs are candidates for `M_m` only. They must not be copied directly into `M_h`.

**Design consequence:** in hot ambient air, increasing air access can have competing effects. Better vapor exchange can improve evaporation while stronger sensible convection can bring more ambient heat toward the cooler wet surface. The net body-cooling result therefore requires separate treatment.

A deterministic sensitivity script sweeps RH, `U_body`, radiation, `M_h`, and `M_m`. Fractions reported by that script are fractions of a predeclared screening grid, **not statistical probabilities or confidence intervals**.

Absolute garment cooling wattage remains classified as model-form uncertain.

## 14. Prescribed-state moist-air macro-corridor buoyancy screen

The first explicit macro-channel model uses a prescribed mean channel temperature/RH and balances moist-air hydrostatic density head against fully developed laminar slot friction.

For ambient `35 °C / 70% RH`, the model finds a neutral-density condition near `34 °C / 90% RH`.

Interpretation:

- sufficiently cool channel air can remain denser than ambient even when very humid and can tend downward;
- sufficiently warm/humid channel air can become lighter and tend upward;
- near the neutral-density state, weak room drift, wearer motion, or external airflow may dominate;
- therefore a vertical corridor should not be designed on the assumption of guaranteed upward chimney flow.

## 15. Self-consistent 1-D covered/end-renewed corridor screen

`simulations/self_consistent_corridor_1d.py` replaces prescribed channel T/RH with a coupled screen for:

- signed buoyancy/friction velocity;
- wet-wall temperature;
- mean/outlet channel temperature and RH;
- evaporation flux;
- body-side heat flux.

The geometry is a rectangular corridor that exchanges with ambient primarily at its ends. It is intentionally a **covered/end-renewed limiting case**, not a laterally open exterior groove.

### 15.1 Primary environment, 100 mm length

At 35 °C / 70% RH and `U_body=100 W/(m² K)`:

| width × depth | signed velocity | Pe_m | mean RH | wet-wall body heat flux |
|---|---:|---:|---:|---:|
| 3 × 2 mm | +0.228 mm/s | 0.81 | ~100.0% | +0.10 W/m² |
| 6 × 3 mm | +0.594 mm/s | 2.12 | ~99.99% | +0.40 W/m² |
| 10 × 5 mm | +1.60 mm/s | 5.70 | ~99.92% | +1.81 W/m² |

These channels have nonzero flow but the internal air approaches saturation. The small/medium cases are diffusion-dominated or mixed according to axial `Pe_m`.

### 15.2 Humidity and hot-ambient reversal

For 10 × 5 × 100 mm:

| environment | signed velocity | Pe_m | mean RH | wet-wall body heat flux |
|---|---:|---:|---:|---:|
| 35 °C / 50% RH | +4.82 mm/s | 17.2 | ~99.6% | +9.94 W/m² |
| 35 °C / 70% RH | +1.60 mm/s | 5.70 | ~99.9% | +1.81 W/m² |
| 35 °C / 85% RH | -1.01 mm/s | 3.59 | ~99.97% | +0.42 W/m² |
| 40 °C / 70% RH | -14.94 mm/s | 53.4 | ~99.0% | **-1.67 W/m²** |

The 40 °C result is important: greater passive flow magnitude does not imply useful body cooling. Hot-air sensible input can offset or reverse local body-side heat removal.

### 15.3 Segment-length effect

For a 10 × 5 mm corridor at 35 °C / 70% RH:

| length | signed velocity | Pe_m | mean RH | wet-wall body heat flux |
|---:|---:|---:|---:|---:|
| 20 mm | +1.38 mm/s | 0.98 | 99.65% | +7.67 W/m² |
| 100 mm | +1.60 mm/s | 5.70 | 99.92% | +1.81 W/m² |
| 200 mm | +1.63 mm/s | 11.65 | 99.96% | +0.92 W/m² |

This demonstrates why axial Péclet number cannot be used alone as a renewal metric. The 200 mm case has `Pe_m > 10` but a smaller useful vapor driving force because its air is more equilibrated with the wet wall.

### 15.4 Current design consequence

The current preferred macro exterior is **not** a long covered chimney. It is a falsifiable hypothesis consisting of:

- laterally open valleys;
- short/segmented wet paths;
- cross-openings;
- discontinuous evaporator islands;
- bidirectional flow tolerance;
- hot-ambient thermal shielding/routing.

The next physical discriminator is E3c: `experiments/e3c_open_vs_covered_corridors.md`.

The next numerical model should add distributed lateral ambient exchange and axial diffusion so that an open exterior valley, rather than a covered duct, is represented directly.
