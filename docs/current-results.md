# Current Numerical Results

Status: **SIMULATION / ANALYTIC SCREENING / VIRTUAL PROTOTYPE ONLY — NO PHYSICAL SPECIMEN**  
Canonical summary date: 2026-08-20

This file is the canonical numerical summary for the research-freeze state. Specialized documents and committed CSVs contain the detailed sweeps. Values below are model outputs under explicit assumptions, not measured garment claims.

## 1. Frozen design direction

The retained passive architecture is:

> directional local sweat collection + short distributed two-scale capillary liquid routes + pressure/ambient-aware exterior wet terminals + continuously ambient-connected evaporative microtexture/open valleys/gaps/islands + short high-`k/rho` heat routes with limited cross-link redundancy + robust terminal contact + dry-side hot-ambient protection.

The project does not use one garment-scale centralized wick, one long passive wet chimney, indiscriminate whole-area high-`k` exposure, geometric area alone, or active load-state switching as baseline mechanisms.

## 2. Exterior evaporation: area is not automatically accessible area

The periodic 2-D rib vapor-diffusion screen shows strong boundary-layer sharing. For `h=2.5 mm`, structured fraction `f=0.65`:

| renewal gap above rib tips | pitch 0.8 mm | pitch 1.0 mm | pitch 1.5 mm |
|---:|---:|---:|---:|
| 0.5 mm | 3.79 | 3.55 | 3.10 |
| 1.0 mm | 2.48 | 2.40 | 2.23 |
| 2.0 mm | ~1.77 | ~1.74 | ~1.67 |
| 5.0 mm | ~1.31 | ~1.30 | ~1.29 |

Result: adding rib/fin area without renewing the local humid air gives diminishing benefit.

Covered/end-renewed corridors can remain nearly saturated despite nonzero natural flow. Thermo-solutal buoyancy can also reverse or neutralize the flow direction. The preferred passive family therefore uses continuously laterally ambient-connected valleys, gaps, islands, or short open segments.

## 3. Heat and vapor transfer are separate

Sensible heat transfer and vapor transfer are not forced to share one empirical multiplier. Positive water evaporation is also not sufficient to establish positive body-side cooling.

For a 34 °C skin boundary in the same-path low-order screen, representative ambient temperatures at zero body-side heat flow are approximately:

| RH | zero-body-flux ambient temperature |
|---:|---:|
| 50% | 45.25 °C |
| 70% | 39.73 °C |
| 80% | 37.57 °C |
| 85% | 36.59 °C |
| 90% | 35.68 °C |

These are model sign boundaries, not medical or measured garment limits.

## 4. Water/feed limitation changes the optimum

If fully-wet evaporation capacity exceeds available sweat/water supply, the model switches to a partial-wet/feed-limited state. Under fixed feed, stronger linked ambient exchange can eventually reduce body-coupled cooling because more latent heat is supplied from ambient air after all available water is already evaporated.

Therefore maximum exchange coefficient is not automatically the cooling optimum.

## 5. Heat spreading requires asymmetric local boundary conditions

Lateral heat spreading produces little integrated value in a deliberately symmetric wet/dry boundary condition. Finite value appears when heat is routed between regions that differ in wetting, shielding, exposure, pressure, or contact state.

A direct-material 1-D bridge replacing scalar mixing with explicit periodic `k*t` conduction gives, at 100 g/h, spreader-only mechanism gains over 0.195 m² of approximately:

| virtual anchor | modeled gain |
|---|---:|
| VP-A | 5.48 W |
| VP-B | 5.32 W |
| VP-C | 5.30 W |
| VP-D | 6.29 W |

Agreement with earlier scalar screens is model-hierarchy continuity, not physical validation.

## 6. Corrected equal-material topology result

An earlier draft conclusion that aligned sparse traces beat an equal-material homogenized field was wrong and is withdrawn.

The retained ordering is:

\[
\boxed{\text{uniform homogenized} > \text{x-aligned / mesh} \gg \text{y-transverse}}
\]

Representative 30-cell gains:

- uniform homogenized: ~5.31 W;
- connected mesh: ~4.76 W;
- x-aligned traces: ~4.71 W;
- y-transverse traces: ~1.82 W.

Orientation matters strongly, but sparse coverage is not automatically superior or lighter.

## 7. Heat-network robustness

With four wet islands and ~35% binary high-`k` material, nominal routing gains include:

- directed: ~5.63 W;
- leaf/venation: ~5.17 W;
- mesh: ~5.35 W;
- directed/mesh blend `lambda=0.125`: ~5.86 W;
- blend `lambda=0.375`: ~5.93 W.

Under simultaneous 20% compliant-path stretch, localized wet-terminal contact loss, and localized 5% conductor fracture:

| topology | nominal | combined-failure gain | retained |
|---|---:|---:|---:|
| blend `lambda=0.125` | ~5.86 W | **~4.96 W** | **~84.6%** |
| blend `lambda=0.375` | ~5.93 | ~4.70 | ~79.2% |
| directed | ~5.63 | ~4.68 | ~83.1% |
| leaf | ~5.17 | ~4.23 | ~81.9% |
| mesh | ~5.35 | ~4.20 | ~78.4% |

The nominal-gain maximum is not the current failure-robustness maximum.

## 8. Compression and terminal contact compete with vapor-path closure

A hypothetical compression screen uses

\[
h_c(c)=h_{c,0}(1+ac),\qquad s_{air}(c)=(1-c)^n.
\]

At 35 °C / 50% RH / 100 g/h with `n=2`, modeled body-side heat removal rises slightly from ~55.9 W at zero compression to ~58.3 W near 30% compression because contact improves while vapor access remains adequate. Beyond the transfer-limited transition, stronger compression reduces evaporation and body heat removal.

The transition depends strongly on the assumed closure law and is not a garment pressure limit.

## 9. Spatial load changes wet-terminal placement

For the converged 24 x 24 synthetic backpack + shoulder-strap map (`cmax=0.5`, `n=2`):

| equal-area wet layout | body-side heat flux | vapor-capacity index | mean local compression |
|---|---:|---:|---:|
| pressure-aware | **~112.8 W/m²** | **~211 g/(m² h)** | **~0.061** |
| peripheral islands | ~106.4 | ~194 | ~0.129 |
| side columns | ~103.9 | ~191 | ~0.130 |
| four islands | ~84.3 | ~147 | ~0.303 |
| center panel | ~60.9 | ~105 | ~0.421 |

With no load, ordinary four-island placement can rank above the pressure-aware rule. The retained conclusion is **load-aware placement where persistent load exists**, not universal peripheral evaporation.

A loaded center-panel evaporator can compete only if wet-side ambient access is strongly protected. In the current effective screen the crossover is near an air-access floor of ~0.83–0.85. Support structures consume active evaporator area: at an air floor of 0.90 only ~2.5% support footprint still matches relocation, rising to ~10% only at an idealized air floor of 1.00.

## 10. Active load-state switching is not the baseline

Quasisteady ideal statewise switching improves the best fixed layout by only about 0.10–0.23 W over 0.195 m² in the current commuter/mixed/seated schedules, below ~1% relative uplift. A small control or redistribution penalty can erase that benefit.

## 11. Short distributed capillary routing is strongly preferred

Ideal cylindrical-capillary screen:

\[
\Delta P_f=\frac{8\mu LQ}{\pi r^4N},\qquad
\Delta P_c=\frac{2\gamma\cos\theta}{r},\qquad
\Delta P_h=\rho g\Delta z.
\]

For positive lift, total ideal capillary cross-section is minimized at

\[
\boxed{r_* = \frac{\gamma\cos\theta}{\rho g\Delta z}}.
\]

One equal-total-flow illustration at 150 g/h gives:

| architecture | path / rise | ideal total capillary area | ideal liquid inventory |
|---|---|---:|---:|
| central | 200 / 100 mm | ~48.0 mm² | ~9.61 mL |
| 4 local cells | 50 / 25 mm | ~3.01 mm² | ~0.15 mL |
| 8 local cells | 30 / 15 mm | ~1.34 mm² | ~0.04 mL |
| 12 local cells | 25 / 10 mm | ~1.21 mm² | ~0.03 mL |

This is geometry-dependent screening evidence, not a universal ratio.

The preferred liquid architecture is:

> local collector -> fine collector mesh / short micro-wick -> spaced larger liquid-filled trunks -> nearby exterior wet terminal.

## 12. Route-distance proxy corrected by explicit hydraulic networks

A pressure-aware route proxy initially favored a mildly regularized terminal layout because it retained ~98.2% of thermal output while shortening a common `d95*r^-4` burden by ~16.8%.

Explicit branched liquid-resistor networks show that this proxy was given too much hydraulic significance for the current short dense routes. For a 60 mm tile carrying 1.8 g/h, 200 µm nominal trunks, 50 µm collector radius, 15 mm lift, and severe pressure-linked radius reduction:

| terminal layout | max network pressure drop | capillary-drive / pressure margin |
|---|---:|---:|
| thermal pressure-aware | ~0.526 Pa | ~4330 |
| regularized | ~0.470 Pa | ~4850 |
| four islands | ~0.205 Pa | ~11100 |

Collector capillary drive is ~2278 Pa. The proxy remains useful as a geometric/material/seam route metric, but not as proof of binding hydraulic pressure loss.

## 13. Sparse two-scale liquid-network boundary

After sparsifying 200 µm trunks inside a finer collector mesh and shifting the trunk lattice through sampled phase offsets under a localized sweat-source field, the largest tested pitch retaining capillary safety factor >=3 at every sampled phase is:

| collector radius | largest robust tested 200 µm trunk pitch |
|---:|---:|
| 20 µm | ~15 mm |
| 25 µm | ~20 mm |
| 30 µm | ~30 mm |
| 35–50 µm | >=60 mm |

This is now the more useful hydraulic design boundary: collector radius × trunk pitch × route phase × source localization × collapse assumptions.

## 14. Salt is nonvolatile; bulk concentration and local deposition are distinct

Salt vapor flux is exactly zero:

\[
J_{salt,vapor}=0.
\]

If upstream evaporation removes water fraction `f_leak` while dissolved nonvolatile-solute flux is conserved:

\[
\sigma_{out}=\frac{\sigma_0}{1-f_{leak}}.
\]

Thus 10% upstream water loss raises bulk concentration only ~1.11x. This does not prove bulk saturation or crystallization.

Local wall-film drying, deposition, re-dissolution, and hydraulic-radius loss are separate mechanisms. The repository contains screening models for fouling sensitivity, but no measured fouling lifetime.

## 15. Transient water buffering

The transient terminal-buffer model preserves water mass explicitly between a transport buffer, terminal buffer, evaporation, and overflow/drain terms. It is a low-order response screen rather than a measured textile dynamic model.

The main retained conclusion is qualitative: transport lag penalizes startup response, while terminal water storage extends post-sweat cooling at the cost of operating wet mass. No universal optimal storage mass is established.

## 16. Virtual garment mass

The nominal VP-E pressure-relocation BOM screen gives approximately:

- dry mass: ~169 g;
- operating mass including modeled water hold-up: ~181 g;
- base textile contribution: ~109 g;
- added functional dry mass: ~60 g.

These are virtual design-variable calculations, not measured garment masses.

## 17. Current product-level hypothesis

At equal liquid input and ambient conditions below the relevant passive sign boundary, a garment combining routed heat spreading, capillary-fed exterior wet structures, and sufficient ambient access can in principle remove more heat from an artificial skin than a conventional flat fast-dry textile.

This remains a testable hypothesis. It is not represented as physically validated.

## 18. What is not established

- no physical cooling measurement;
- no manufactured garment;
- no human trial;
- no validated CFD;
- no measured textile permeability/contact/pressure constitutive laws;
- no measured salt/fouling lifetime;
- no proven manufacturing process;
- no claim that the listed watt values will be achieved by a real garment;
- no legal conclusion of novelty, patentability, invalidity, or freedom to operate.

## 19. Verification state

The pre-cleanup 43-model integration head

`529fc573f2a24a0d4d3db8464c3c1409a38b34ec`

passed all five defined pull-request workflows:

- `model-tests` #722 — success;
- `topology-tests` #278 — success;
- `pressure-tests` #112 — success;
- `liquid-tests` #91 — success;
- `garment-tests` #46 — success.

The final documentation-cleanup/release commit must be checked again before tagging.

## 20. Research freeze

The exploratory numerical phase is considered sufficient for the present computational disclosure. Additional 3-D flow modeling, garment-scale curvature, detailed spacer mechanics, time-varying sweat migration, measured fouling kinetics, and physical prototypes are **optional future research**, not blockers for closing this phase.

Remaining stable-release work is publication/repository work:

1. final cross-document consistency check;
2. authoritative source/patent identifier verification;
3. CI confirmation on the exact release commit;
4. regeneration of release reference artifacts/hashes;
5. citation/version metadata;
6. versioned GitHub release/tag;
7. optional persistent archive/DOI.

See `research-freeze.md`, `release-checklist.md`, and `../AUDIT.md`.
