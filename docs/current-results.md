# Current Numerical Results

Status: **SIMULATION / SCREENING ONLY — NO PHYSICAL GARMENT PERFORMANCE DATA YET**  
Compiled: 2026-08-19

This document consolidates the principal quantitative results from earlier exploratory model versions so they are not lost across disconnected files. Values are approximate outputs from simplified models and should be re-generated from consolidated repository code before a stable release.

## 1. Water/latent-heat scale

Using a representative latent heat of vaporization near `2.4–2.42 MJ/kg`:

- 50 W of latent heat corresponds to roughly 74–75 g/h of water evaporation.

Important: latent heat at the evaporating exterior is not necessarily equal to heat removed from the wearer; ambient convection/radiation can supply part of the evaporation energy.

## 2. Whole-body lateral heat spreading under patchy evaporation

A prior 2D screening model used spatially nonuniform evaporation over approximately 25% of the modeled area.

Representative outputs:

| In-plane conductivity (W/mK) | Body-side cooling (W) | Spatial temperature SD (°C) |
|---:|---:|---:|
| 0.2 | ~16.1 | ~1.46 |
| 2 | ~16.9 | ~1.40 |
| 20 | ~20.3 | ~1.13 |
| 200 | ~27.3 | ~0.44 |

Interpretation: lateral heat spreading produced the largest benefit when evaporation was spatially uneven. In a uniform-equivalent evaporation case, increasing in-plane conductivity had much less effect.

## 3. Mass/performance tradeoff for continuous heat spreaders

An abstract 0.30 m² screen found that continuous high-conductivity sheets can become too heavy for clothing.

One screened family produced approximately:

- baseline: ~10.3 W body-side cooling;
- maximum screened: ~21.4 W;
- a carbon-like case around `k = 150 W/mK`, thickness `0.8 mm`, mass ~432 g: ~20.5 W.

This motivated thinner, anisotropic, patterned, and discontinuous heat-spreader architectures rather than simply maximizing bulk conductivity.

## 4. Thin anisotropic heat-spreader screening

For a representative anisotropic case with `kx = 200 W/mK`, `ky = 15 W/mK` in a geometry where the high-conductivity direction was aligned toward evaporative bands:

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

Interpretation: a dry high-conductivity exterior can become a parasitic inward heat collector when ambient temperature exceeds skin/garment temperature. High in-plane conductivity should not automatically imply high through-thickness exposure to ambient heat.

## 6. Stretchable serpentine heat paths

A geometric serpentine screen estimated retained single-path thermal conductance as extension increases:

| Target extension | Approx. retained conductance |
|---:|---:|
| 5% | ~95% |
| 10% | ~91% |
| 15% | ~87% |
| 20% | ~83% |
| 30% | ~77% |

This is a geometric/electrical-thermal path-length screen, not a fatigue measurement.

## 7. Passive exterior exchange target

The current low-order model describes exterior performance through an effective exchange multiplier `M` relative to a flat wet textile.

For the current `35 °C / 70% RH / 150 g/h / 0.30 m²` screening case, a later v1.4 model indicated approximately:

- `M ~ 3.5` for a +10 W modeled advantage over the flat fast-dry baseline;
- `M ~ 3.9` for a +20 W modeled advantage.

These values depend on assumed body-to-evaporator thermal coupling and the natural-convection model and should not be treated as measured thresholds.

## 8. Preview-like exterior rib geometry

For a visual concept interpreted approximately as:

- structured-panel coverage `f = 0.45`;
- rib height `h = 2.0 mm`;
- pitch `p = 1.5 mm`;

local geometric multiplier:

`G_panel ~ 3.67`.

With the current model, even `alpha = 1.0` only gives whole-garment `M ~ 2.2`, which was insufficient for the +10 W target at 35 °C / 70% RH.

This negative result led to denser but still low-profile candidate textures.

## 9. Current exterior candidate region

Aesthetic/performance screening currently prioritizes approximately:

- structured-panel coverage: 55–70%;
- rib height: 2–3 mm;
- rib pitch: 0.8–1.0 mm;
- rounded/flexible textile-like ribs;
- whole-garment or large-area heat spreading retained.

The critical unresolved variable is the effective accessibility `alpha`. Tight pitch increases geometric area, but may reduce `alpha` because adjacent wet structures share a humid boundary layer.

## 10. Salt mass-balance correction

No current result assumes salt evaporation.

For reference, a previous conservative NaCl-equivalent mass balance at 150 g/h water throughput for 8 h gave total retained salt on the order of:

- ~1.4 g at 20 mmol/L NaCl-equivalent;
- ~2.8 g at 40 mmol/L;
- ~4.2 g at 60 mmol/L;
- ~5.6 g at 80 mmol/L.

These numbers only illustrate mass scale. Actual sweat contains multiple ions and organics, and ordinary garments also retain nonvolatile sweat residues. Dedicated salt-management hardware should only be added if comparative testing shows abnormal degradation relative to normal textile controls.

## 11. What must be re-run before stable release

Before a versioned stable release, the repository should regenerate at least:

1. the passive `M` threshold table;
2. the rib geometry/accessibility design space;
3. the anisotropic heat-spreader orientation comparison;
4. the hot-ambient dry-side shielding comparison;
5. uncertainty/sensitivity bounds for all of the above.

The re-generated outputs should include code commit SHA and parameter metadata.
