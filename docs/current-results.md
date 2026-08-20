# Current Numerical Results

Status: **SIMULATION / ANALYTIC SCREENING / VIRTUAL PROTOTYPE ONLY — NO PHYSICAL SPECIMEN**  
Compiled: 2026-08-20

This file is the current integrated numerical summary. Values are outputs of low-order screening models under explicit assumptions, not measured garment claims.

## 1. Current design direction

The working virtual architecture is:

> directional local sweat collection + distributed short capillary liquid routes + nearby pressure-aware or mechanically protected wet terminals + continuously ambient-connected evaporative microtexture/open valleys + short high-`k/rho` heat routes with limited cross-link redundancy + robust terminal contact + dry-side hot-ambient protection.

The project no longer prefers one garment-scale centralized wick, long covered wet chimneys, indiscriminate whole-area high-`k` exposure, geometric area alone, or active wet-layout switching as baseline mechanisms.

## 2. Exterior geometric area is not accessible evaporative area

The E3 periodic 2-D vapor-diffusion screen shows strong boundary-layer sharing.

For `h=2.5 mm`, structured fraction `f=0.65`, whole-area vapor multipliers were approximately:

| renewal gap above rib tips | pitch 0.8 mm | pitch 1.0 mm | pitch 1.5 mm |
|---:|---:|---:|---:|
| 0.5 mm | 3.79 | 3.55 | 3.10 |
| 1.0 mm | 2.48 | 2.40 | 2.23 |
| 2.0 mm | ~1.77 | ~1.74 | ~1.67 |
| 5.0 mm | ~1.31 | ~1.30 | ~1.29 |

Result: adding rib area without renewing the humid boundary layer produces little useful exchange.

## 3. Long covered passive wet corridors are not preferred

Self-consistent covered-corridor screens showed that nonzero buoyant flow does not guarantee useful evaporation. Long wet channels can become nearly saturated, and thermo-solutal buoyancy can reverse flow direction.

Current exterior preference is continuously laterally ambient-connected valleys, gaps or islands rather than a long covered "chimney."

## 4. Open-valley renewal requires both retention and absolute conductance

Define

\[
R=G_a/G_w,
\qquad
F=\frac{R}{1+R}.
\]

`F` is the fraction of the ideal wet-wall vapor driving force retained after local ambient renewal. Examples:

- `F=0.8` requires `R=4`;
- `F=0.9` requires `R=9`;
- `F=0.95` requires `R=19`.

However

\[
k_{eff}=\frac{k_wk_a}{k_w+k_a}=k_wF,
\]

so high `F` can also occur because the wet-wall transfer itself is weak. `F` is therefore not sufficient as a performance metric.

## 5. Positive evaporation is not equivalent to body cooling

The coupled heat/vapor model can sustain evaporation while signed body-side heat flow becomes negative in hot ambient air.

For a 34 °C skin boundary and ordinary same-path heat/vapor coupling, representative zero-body-flux ambient-temperature boundaries are approximately:

| RH | ambient temperature at zero body heat flux |
|---:|---:|
| 50% | 45.25 °C |
| 70% | 39.73 °C |
| 80% | 37.57 °C |
| 85% | 36.59 °C |
| 90% | 35.68 °C |

These are model sign boundaries, not medical/safety limits.

## 6. Water supply changes the optimum

The feed-limited open-valley model solves a computational wet fraction `beta` when fully-wet evaporation capacity exceeds available water.

At 35 °C / 50% RH with 150 g/h over a 0.195 m² structured region, progressively stronger linked ambient exchange can first increase body heat removal, then reduce it after all available feed is already evaporated because a larger fraction of latent heat comes from ambient air.

Therefore maximum transfer coefficient is not automatically the body-cooling optimum.

## 7. Heat spreading requires spatially different boundary conditions

A symmetric wet/dry screen showed that lateral temperature equalization alone does not create area-integrated cooling when both regions have identical local external boundaries.

Finite heat-routing value appears when wet and dry regions differ in exposure, shielding, pressure/contact or evaporation state.

For a representative asymmetric `h_dry=5 W/(m² K)` scalar screen, the `g_mix` needed for ~90% of the high-mixing gain was approximately:

| feed | required `g_mix` |
|---:|---:|
| 30 g/h | ~117 W/(m² K) |
| 50 | ~192 |
| 75 | ~285 |
| 100 | ~330 |
| 150 | ~258 |

The associated mechanism gains over 0.195 m² were only several watts, not unlimited.

## 8. Routing pitch and contact are first-order burdens

Ideal periodic routing screen:

\[
g_{sheet}\approx\Gamma\frac{k_{\parallel}tc}{P^2}.
\]

Thus required `k*t` grows with routing pitch squared.

Lumped two-contact burden:

\[
\frac{1}{g_{eff}}=\frac{1}{g_{sheet}}+\frac{2}{h_c}.
\]

High sheet conductivity alone does not guarantee useful routing if terminal contacts are weak.

## 9. Direct-material 1-D bridge preserves the finite heat-routing value

Replacing scalar `g_mix` with direct periodic `k*t` conduction, local contact, wet evaporation and feed-solved wet width gives, at 100 g/h:

| virtual anchor | direct-material spreader-only gain over 0.195 m² |
|---|---:|
| VP-A | ~5.48 W |
| VP-B | ~5.32 W |
| VP-C | ~5.30 W |
| VP-D | ~6.29 W |

Feed closure and equation residuals were numerically checked. Agreement with the scalar model is hierarchy continuity, not independent validation.

## 10. Corrected equal-material 2-D topology result

An earlier draft conclusion that aligned sparse traces beat the homogenized equal-material field was wrong and has been withdrawn.

Current corrected periodic ordering:

\[
\boxed{\text{uniform homogenized} > \text{x-aligned / mesh} \gg \text{y-transverse}}
\]

Representative 30-cell gains:

- uniform homogenized: ~5.31 W;
- connected mesh: ~4.76 W;
- x-aligned traces: ~4.71 W;
- y-transverse traces: ~1.82 W.

Orientation matters strongly, but the tested sparse traces do not exceed the ideal homogenized field.

## 11. Multi-island heat-network motifs

With four wet islands and ~35% binary high-`k` material:

| routing motif | nominal heat-routing gain |
|---|---:|
| parallel directed | ~5.63 W |
| herringbone | ~4.66 W |
| radial spokes | ~3.31 W |
| leaf/venation | ~5.17 W |
| redundant mesh | ~5.35 W |

A directed/mesh score blend gives:

- `lambda=0.125`: ~5.86 W;
- `lambda=0.375`: ~5.93 W;
- pure mesh: ~5.35 W.

## 12. Failure morphology changes the best heat network

Distributed 5% conductor dropout and localized 5% tears rank topologies differently.

For the current localized-tear screen, `lambda=0.125` retained about 94% of nominal gain at the worst of nine tested tear centers.

For simultaneous 20% compliant-path stretch + localized wet-terminal contact loss + localized 5% conductor fracture:

| topology | nominal | combined-failure gain | retained |
|---|---:|---:|---:|
| blend `lambda=0.125` | ~5.86 W | **~4.96 W** | **~84.6%** |
| blend `lambda=0.375` | ~5.93 | ~4.70 | ~79.2% |
| directed | ~5.63 | ~4.68 | ~83.1% |
| leaf | ~5.17 | ~4.23 | ~81.9% |
| mesh | ~5.35 | ~4.20 | ~78.4% |

The nominal maximum is not the current robustness maximum.

## 13. Stretch alone is less important than contact loss in the present model

If the conductive path remains intact, 20% uniaxial stretch in the compliant-serpentine screen retained roughly 97–99% of nominal routing gain.

This is not a durability claim because cracking, delamination and contact loss are excluded.

Localized low contact around an active wet island was more damaging, retaining only roughly 83–87% of routing gain in the current spatial-contact screen.

## 14. Compression has two competing effects

Hypothetical compression laws:

\[
h_c(c)=h_{c,0}(1+ac),
\qquad
s_{air}(c)=(1-c)^n.
\]

At 35 °C / 50% RH / 100 g/h with `n=2`, body-side heat removal increased slightly from ~55.9 W at zero compression to ~58.3 W near 30% compression because contact improved while vapor access was still adequate.

Near 35% compression the screen became fully wet / transfer limited. Stronger compression then reduced evaporation and body heat removal rapidly.

The transition is highly model-form dependent:

- `n=1`: first transfer-limited point around 58%;
- `n=2`: around 35%;
- `n=3`: around 25%.

These are not garment pressure limits.

## 15. Spatial pressure maps favor moving active wet terminals out of persistent load zones

Synthetic pressure maps were created for a backpack panel, shoulder straps, seat back and combined backpack+straps.

All wet layouts use approximately equal wet area and the same routed high-`k` material fraction.

At the converged 24 x 24 primary screen (`cmax=0.5`, `n=2`) for backpack+straps:

| wet layout | body-side heat flux | vapor-capacity index | mean local compression |
|---|---:|---:|---:|
| pressure-aware | **112.8 W/m²** | **211 g/(m² h)** | **0.061** |
| peripheral islands | 106.4 | 194 | 0.129 |
| side columns | 103.9 | 191 | 0.130 |
| upper/lower bands | 86.1 | 152 | 0.270 |
| four islands | 84.3 | 147 | 0.303 |
| center panel | 60.9 | 105 | 0.421 |

Pressure-aware placement ranked first under each primary load map. With no load, ordinary four-island placement ranked above the pressure-aware rule.

Supported conclusion: avoid persistent load zones **where they occur**; do not universally move evaporation to the garment perimeter.

## 16. Protected under-load evaporation is an alternative, but air access must be preserved strongly

Keeping the loaded center panel active while imposing a minimum wet-side ambient-access floor gives:

| protected air floor | body-side heat flux |
|---:|---:|
| 0.50 | ~81.3 W/m² |
| 0.60 | ~91.9 |
| 0.70 | ~101.5 |
| 0.80 | ~110.0 |
| 0.85 | ~114.0 |
| 0.90 | ~117.8 |
| 1.00 | ~125.0 |

The pressure-aware relocation reference is ~112.8 W/m². The model crossover is near an effective air-access floor of ~0.83–0.85.

This is an effective model parameter, not a measured channel-height requirement.

## 17. Load-bearing support consumes active evaporator area

After support footprint is removed from the loaded center wet panel, the protected-gap design space narrows:

| protected air floor | maximum screened support fraction still matching relocation |
|---:|---:|
| 0.80 | none |
| 0.85 | ~0% |
| 0.90 | ~2.5% |
| 0.95 | ~7.5% |
| 1.00 | ~10% |

This favors narrow ribs, point/perimeter supports or arches over coarse load-bearing lattices.

## 18. Ideal active wet-layout switching has small value in current schedules

Quasisteady hypothetical schedules compare one fixed wet layout with an ideal statewise-best layout.

| schedule | best fixed | ideal adaptive uplift over 0.195 m² |
|---|---|---:|
| commuter backpack | pressure-aware | ~0.10 W |
| mixed day | pressure-aware | ~0.13 W |
| seated office | pressure-aware | ~0.23 W |

The relative uplift is below ~1%. A small control/redistribution penalty can erase it, so active switching is not the current baseline direction.

## 19. Passive capillary delivery favors short distributed routes

Ideal cylindrical capillary screen:

\[
\Delta P_f=\frac{8\mu LQ}{\pi r^4N},
\quad
\Delta P_c=\frac{2\gamma\cos\theta}{r},
\quad
\Delta P_h=\rho g\Delta z.
\]

With safety factor 3 and the current screening liquid properties, a 150 g/h, 100 mm route requires many small channels if significant vertical rise is present.

Example at 100 mm route / 50 mm rise:

- 50 µm radius: ~2370 channels;
- 100 µm: ~397;
- 150 µm: ~178;
- 200 µm: ~155;
- 300 µm: no positive capillary-head margin.

Short local routes are much more favorable.

## 20. Ideal capillary radius has a lift/resistance optimum

For positive vertical rise, total ideal capillary cross-section is minimized at

\[
\boxed{r_* = \frac{\gamma\cos\theta}{\rho g\Delta z}}.
\]

This is exactly half the largest equivalent radius capable of statically supporting the same rise.

Reference optima with current screening properties:

- 25 mm rise: ~247 µm;
- 50 mm: ~124 µm;
- 100 mm: ~61.8 µm;
- 200 mm: ~30.9 µm.

At zero rise this ideal area objective has no finite optimum without another radius/thickness constraint.

## 21. Centralized liquid lift is a poor current architecture

One explicit equal-total-flow illustration (150 g/h):

| architecture | path / rise | ideal total capillary cross-section | ideal liquid inventory |
|---|---|---:|---:|
| central | 200 / 100 mm | ~48.0 mm² | ~9.61 mL |
| 4 local cells | 50 / 25 mm | ~3.01 mm² | ~0.15 mL |
| 8 local cells | 30 / 15 mm | ~1.34 mm² | ~0.04 mL |
| 12 local cells | 25 / 10 mm | ~1.21 mm² | ~0.03 mL |

This is a geometry-dependent screening comparison. The benefit comes from shortening route length and lift.

## 22. Practical trunk-radius caps still favor local cells

For the 4-local-cell reference (37.5 g/h/cell, 50 mm path, 25 mm rise), the unconstrained ideal discrete optimum is near 244 µm equivalent radius.

| max radius | area penalty vs unconstrained |
|---:|---:|
| 75 µm | ~1.95x |
| 100 µm | ~1.56x |
| 150 µm | ~1.19x |
| 200 µm | ~1.06x |
| 300 µm | ~1.00x |

Thus a 150–200 µm-class transport trunk remains close to the ideal hydraulic burden in this specific local geometry.

## 23. Liquid capture and transport should use different pore scales

Current preferred liquid architecture:

> local collector -> short 20–50 µm-class micro-wick -> larger 100–300 µm-class liquid-filled trunk -> accessible exterior terminal.

Fine pores are used for local capillary capture rather than garment-scale hydraulic transport.

Blockage redundancy can be added by installing more trunks/channels than the minimum live count. This remains a simple independent-channel screen; correlated blockage is unresolved.

## 24. Salt is nonvolatile; bulk leakage wording is corrected

Salt vapor flux is exactly zero:

\[
J_{salt,vapor}=0.
\]

If an upstream water fraction `f_leak` evaporates while dissolved salt flux is conserved, normalized bulk concentration follows

\[
\sigma_{out}=\frac{\sigma_0}{1-f_{leak}}.
\]

Thus:

- 10% water leak -> 1.11x bulk concentration;
- 20% -> 1.25x;
- 30% -> 1.43x.

Small upstream leakage therefore does not mathematically prove bulk saturation or crystallization.

Internal phase change is still discouraged because it wastes water delivery to the selected terminal and can create local thin-film dryout/deposition that this bulk balance does not resolve.

## 25. Current virtual product direction

The current baseline architecture is passive and fixed rather than actively switched:

1. partition the garment into local liquid/thermal cells;
2. collect sweat locally;
3. move liquid a short distance with a two-scale capillary network;
4. route heat from nearby dry/compressed zones toward the same terminal;
5. place the terminal in a low-pressure ambient-open zone when possible;
6. if terminal relocation is impossible, mechanically protect the vapor gap with very low support-area occupation;
7. keep buried liquid trunks protected from evaporation;
8. keep dry exterior zones shielded when hot ambient sensible gain is harmful.

## 26. What is not established

- no physical cooling measurement;
- no human trial;
- no validated CFD;
- no measured textile permeability/contact/pressure constitutive laws;
- no measured salt deposition threshold;
- no proven manufacturing process;
- no full-garment weight/thickness optimization;
- no claim that the listed numerical watt values will be achieved by a garment.

## 27. Next numerical priorities

1. co-optimize heat-route length and liquid-route length to common pressure-aware terminals;
2. add channel collapse/curvature under local pressure;
3. resolve protected vapor-gap geometry instead of using an effective air-access floor;
4. model local wall-film salt deposition and progressive hydraulic-radius loss;
5. complete integrated virtual-prototype mass/thickness budgets;
6. add hot/humid maps for the integrated virtual prototype;
7. continue repository/publication audit and freeze a stable release only after all references and CI are synchronized.
