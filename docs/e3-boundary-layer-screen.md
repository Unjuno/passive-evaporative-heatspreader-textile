# E3 — Boundary-Layer Interference Screen

Date: 2026-08-19  
Status: numerical experiment; not a physical measurement

## 1. Question

The earlier rib model used a phenomenological accessibility parameter `alpha` to represent the fraction of added rib area that actually participates in useful exchange. E3 asks a more direct question:

> If multiple wet ribs share a stagnant humidity boundary layer, how much vapor-transfer enhancement survives as a function of rib pitch and the distance to refreshed bulk air?

This experiment does not attempt to predict the complete garment. It isolates one failure mechanism: diffusion shielding between neighboring wet structures.

## 2. Model

One periodic 2-D rib cell is solved using steady diffusion in the air domain:

\[
\nabla^2 u = 0
\]

where `u` is normalized water-vapor concentration.

Boundary conditions:

- `u = 1` on the wet substrate and wet rib surfaces;
- `u = 0` at an idealized bulk-air renewal plane above the rib tips;
- periodic boundary conditions in the lateral direction.

The panel mass-transfer multiplier is

\[
M_{panel} = \frac{J_{rib}}{J_{flat}}
\]

where both fluxes use the same projected pitch and the same renewal-plane height.

For structured panels occupying fraction `f` of the active projected garment area, the screening whole-garment mass-transfer multiplier is

\[
M_m = 1 + f(M_{panel}-1).
\]

This `M_m` is a mass-transfer quantity only. It must not automatically be interpreted as the same multiplier for convective heat transfer.

## 3. Variables

| Symbol | Meaning | SI unit | Definition / assumption | Type |
|---|---|---:|---|---|
| `u` | normalized vapor concentration | 1 | 1 at wet surfaces, 0 at renewal plane | field |
| `p` | rib pitch | m | periodic cell width | scalar |
| `h` | rib height | m | substrate to rib tip | scalar |
| `w` | rib width | m | rectangular screening cross-section | scalar |
| `delta` | renewal-plane height from substrate | m | idealized refreshed-air boundary | scalar |
| `g` | renewal gap above rib tip | m | `g = delta - h` | scalar |
| `f` | structured-panel projected coverage | 1 | current screen: 0.65 | scalar |
| `M_panel` | structured-panel vapor-flux multiplier | 1 | `J_rib/J_flat` | scalar |
| `M_m` | whole-garment mass-transfer multiplier | 1 | `1 + f(M_panel-1)` | scalar |

Dimensional check: `M_panel` and `M_m` are ratios of equal-dimension vapor fluxes and are dimensionless. `g = delta - h` has dimensions of length.

## 4. Screened geometry

Fixed values:

- rib height `h = 2.5 mm`;
- structured-panel coverage `f = 0.65`;
- pitch `p = 0.8, 1.0, 1.5 mm`;
- rib width approximately `0.24–0.25 mm`;
- renewal gap above rib tips `g = 0.25–15 mm`.

The previous low-order thermal screen used approximately `M ~ 3.5` as a design target associated with a +10 W body-cooling advantage under its primary assumed condition. The current experiment uses that value only as a cross-model screening reference; it is not a measured requirement.

## 5. Results

Selected whole-garment mass-transfer multipliers:

| renewal gap above tip | p = 0.8 mm | p = 1.0 mm | p = 1.5 mm |
|---:|---:|---:|---:|
| 0.5 mm | 3.785 | 3.548 | 3.098 |
| 1.0 mm | 2.481 | 2.400 | 2.229 |
| 2.0 mm | 1.765 | 1.736 | 1.673 |
| 5.0 mm | 1.312 | 1.304 | 1.286 |
| 7.5 mm | 1.209 | 1.204 | 1.193 |

Within this pure-diffusion screen, the largest renewal gap that still reaches `M_m >= 3.5` is approximately:

- `0.5 mm` for `p = 0.8 mm`;
- `0.5 mm` for `p = 1.0 mm`;
- `0.4 mm` for `p = 1.5 mm`.

The dominant variable is therefore not pitch alone. It is whether humid air near the rib field is replaced close to the rib tips.

## 6. Numerical convergence check

Reference case: `p = 1.0 mm`, `h = 2.5 mm`, `w = 0.25 mm`, renewal plane at 3.0 mm from the substrate.

| nodes per pitch | `M_panel` | `M_m` | difference from 48-node result |
|---:|---:|---:|---:|
| 16 | 4.889 | 3.528 | -1.19% |
| 24 | 4.920 | 3.548 | -0.62% |
| 32 | 4.937 | 3.559 | -0.32% |
| 48 | 4.955 | 3.570 | reference |

This is adequate for the present screening purpose. Boundary-condition uncertainty is much larger than grid error.

## 7. Interpretation

### Finding A — geometric area is not sufficient

Sub-millimeter rib pitch produces large geometric surface area, but most of that area can become diffusion-shielded when the entire rib field sits inside a several-millimeter stagnant humidity layer.

### Finding B — pitch refinement alone is not the main solution

At a 5 mm renewal gap, changing pitch from 1.5 mm to 0.8 mm changes the whole-garment multiplier only from approximately 1.286 to 1.312 in this model. Making the micro-ribs still denser would therefore be a weak strategy if the near-surface humid air is not renewed.

### Finding C — the architecture should be hierarchical

A stronger implementation is a two-scale exterior:

1. **micro-scale wet ribs / 3-D knit / short fins** for wetted surface area;
2. **macro-scale air-renewal paths** that allow ambient air to reach or sweep close to the evaporating structure.

Examples include open longitudinal corridors, spacer-knit channels, discontinuous rib islands, raised pleats, alternating rib fields and ventilation valleys, or other structures that prevent the entire evaporator from being buried in one stagnant humid layer.

The primary concept can remain fanless. The purpose of the macro structure is to reduce diffusion shielding and promote passive or motion-assisted air renewal.

## 8. H / T / D / C / U

**H — falsifiable hypothesis**  
Dense micro-ribs by themselves do not provide a large effective vapor-transfer multiplier when the rib field is covered by a stagnant humidity layer several millimeters thick; useful enhancement requires air renewal near the rib tips or an equivalent transport mechanism.

**T — minimum validation**  
Numerical: periodic 2-D diffusion sweep with grid-convergence check.  
Physical follow-up: compare 0.8/1.0/1.5 mm rib pitch with and without macro ventilation corridors while measuring heater power and RH at approximately 0.5, 1, 2, 5, 10 and 20 mm above the structure.

**D — decision rule**  
If measured structured samples do not materially increase vapor removal or heater power over the flat control despite large geometric area, the micro-rib-only premise fails. If adding macro air-renewal channels restores a substantial advantage, the hierarchical architecture is supported.

**C — competing explanations**  
Natural convection may renew air more effectively than the present pure-diffusion boundary condition; walking/body motion may dominate; real 3-D ribs may induce flow not represented in 2-D; incomplete wetting may reduce performance independently of boundary-layer overlap.

**U — uncertainty**  
The dominant uncertainty is the idealized renewal-plane boundary condition, not numerical grid spacing. This model omits coupled heat transfer and fluid motion and therefore cannot establish a physical `alpha` value or a garment cooling wattage by itself.

## 9. Next experiment

E3b should test a hierarchical exterior in which micro-rib fields are separated by macro-scale ventilation corridors. The variables should be:

- micro-rib pitch and height;
- corridor width and spacing;
- rib-field width between corridors;
- channel orientation relative to gravity and expected walking airflow;
- wet versus intentionally dry corridor surfaces;
- near-surface RH profile and artificial-skin heater power.

The objective is to move the project from “maximize geometric area” to “maximize wetted area that remains connected to refreshed ambient air.”
