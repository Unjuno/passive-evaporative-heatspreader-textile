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

The current low-order passive model describes exterior performance with an effective exchange multiplier `M` relative to a flat wet textile.

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

1. full stable-equilibrium branch maps versus `M`, RH, water input, and `U`;
2. rib geometry/accessibility design space with branch count;
3. anisotropic heat-spreader orientation comparison;
4. hot-ambient dry-side shielding comparison;
5. uncertainty/sensitivity bounds;
6. reference CSVs with code commit SHA and parameter metadata.

The primary physical experiment should determine which, if any, low-order equilibrium behavior corresponds to real textile operation.
