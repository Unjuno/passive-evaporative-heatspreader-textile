# Repository Audit

Audit date: 2026-08-20  
Branch: `agent/initial-research-disclosure`

## Overall assessment

The branch contains a coherent technical disclosure, explicit implementation variants, **19 executable screening/sensitivity/audit/virtual-prototype modules**, regression tests, reproducible reference-output generation, prior-art working notes, and future physical-test protocols.

It remains a development branch and a **virtual/computational prototype only**. No physical garment or bench specimen currently exists, and no physical garment-performance measurements have been published.

The numerical record now supports a narrower design hypothesis:

> directional liquid transport + capillary-fed wet microtexture + continuously ambient-connected exterior valleys/islands + short-range high-`k/rho` heat routing between thermally asymmetric wet/dry regions + explicit thermal contacts + explicit liquid-supply state + hot-ambient sensible-heat protection.

The repository no longer accepts the following as sufficient design criteria: geometric area alone, long passive wet chimneys, axial Péclet number alone, centimeter-scale segmentation alone, high local `F` alone, positive evaporation alone, fully-wet capacity above feed, heat spreading under symmetric boundary conditions, infinite sheet conductivity, sparse coverage as automatic mass reduction, or high sheet `k` without routing/contact constraints.

## A. Technical coherence

| Item | Status | Audit note |
|---|---|---|
| Directional sweat transport | PASS | Core layer retained. |
| Capillary liquid delivery | PASS | Distributed liquid path retained. |
| Exterior micro-ribs / 3D knit / fins / lamellae | PASS | Multiple concrete families documented. |
| Hierarchical ambient access | PASS | Open valleys, cross-openings, short interruptions, islands and covered comparison channels explicit. |
| Sensible/vapor separation | PASS | Heat and vapor transfer are not forced to share one multiplier. |
| Explicit feed-limited state | PASS/SCREEN | Homogenized `beta` solves imposed feed when fully-wet capacity is too high. |
| Separate wet/dry temperatures | PASS/SCREEN | Symmetric and asymmetric two-node models exist. |
| Asymmetric heat-routing value | PASS/SCREEN | System-level spreader gain appears only when local boundary conditions differ. |
| Spreader material mapping | PASS/SCREEN | `g_mix` maps to `k*t/P²`, mass and bend-strain screening under an explicit topology factor. |
| Spreader contact mapping | PASS/SCREEN | Two-contact series burden is explicit. |
| Virtual prototypes | PASS/DEV | VP-A through VP-D are reproducible computational anchors. |
| Hot-ambient protection | PASS/HYPOTHESIS | Required by several screens; no physical validation. |
| Salt handling | PASS | Water evaporates; salt vapor flux is zero. |
| Apparel integration | PASS/CONCEPT | Low-profile patterns, panels, valleys/islands and routed paths documented. |
| Fan / MOF | OPTIONAL | Not required by primary architecture. |

## B. Executable model / audit stack

1. `simulations/passive_rib_screen.py`
2. `simulations/split_heat_mass_screen.py`
3. `simulations/split_transfer_sensitivity.py`
4. `simulations/rib_diffusion_screen.py`
5. `simulations/corridor_buoyancy_screen.py`
6. `simulations/self_consistent_corridor_1d.py`
7. `simulations/open_valley_exchange_target.py`
8. `simulations/open_valley_distributed_1d.py`
9. `simulations/open_valley_thermal_1d.py`
10. `simulations/open_valley_feed_limited.py`
11. `simulations/wet_dry_two_node.py`
12. `simulations/asymmetric_wet_dry_spreader.py`
13. `simulations/spreader_material_mapping.py`
14. `simulations/virtual_prototype_v01.py`
15. `simulations/open_valley_heat_mass_coupling_audit.py`
16. `simulations/passive_environment_boundary.py`
17. `simulations/supply_limit_audit.py`
18. `simulations/heat_spreader_2d.py`
19. `simulations/water_salt_1d.py`

`simulations/generate_reference_outputs.py` is the reproducibility generator rather than a physical model.

All models are screening/analytic/virtual-prototype models. None is validated CFD or measured garment performance.

## C. Reproducibility / verification

| Item | Status | Audit note |
|---|---|---|
| Regression tests | PASS/UPDATED | Include multi-root, split transfer, E3, corridor, open-valley, feed-limited, wet/dry, asymmetric continuation, material/contact and virtual-prototype checks. |
| E3 grid convergence | PASS/SCREEN | 24 nodes/pitch within ~0.62% of 48-node reference for the screened case. |
| Distributed open-valley convergence | PASS/SCREEN | Center `F` stable over tested grids. |
| Wall-energy closure | PASS | Coupled open-valley energy balance regression exists. |
| Feed balance closure | PASS | Feed-limited solver matches imposed feed numerically. |
| Latent-source partition | PASS | Body + ambient latent fractions close to one in the low-order model. |
| Symmetric wet/dry global closure | PASS | Internal mixing cancels globally when local boundary conditions are symmetric. |
| Asymmetric branch acceptance | PASS | Bounded least squares + residual threshold + continuation regression prevents the earlier high-beta branch jump. |
| Material mapping identities | PASS | Round trip, quadratic pitch penalty, coverage/mass identity and contact ceiling are tested. |
| Virtual prototype regression | PASS/DEFINED | VP-A/B/C/D nominal convergence and relative design expectations are tested. |
| Reference generator | PASS/UPDATED | Material/contact and VP-A–D outputs are included. |
| CI definition | PASS/UPDATED | Current workflow explicitly runs the virtual prototype module and checks generated VP CSVs. |
| Previously verified integration | PASS | `model-tests` #370 succeeded at SHA `a01eeafc8ae6814349a3a0937251efd048823dae` before the latest material/VP updates. |
| Current 19-module head | CHECK | Record a newer successful Actions run before marking the current head verified. |

## D. Major numerical findings

### D1 — exterior geometric area is not accessible area

Dense wet ribs can share one humidity boundary layer. In the E3 screen (`h=2.5 mm`, structured fraction `0.65`), whole-area vapor multipliers fall from roughly 3–4 at a 0.5 mm idealized renewal gap to roughly 1.3 at a 5 mm gap.

### D2 — long passive wet corridors are weak renewal mechanisms

The self-consistent 100 mm covered/end-renewed corridor model can give nonzero natural flow while mean RH approaches saturation. Flow direction can reverse with thermo-solutal conditions. Corridor velocity and axial Péclet number are not accepted as success metrics by themselves.

### D3 — open-valley renewal must be reported with absolute transfer

\[
R=G_a/G_w,
\qquad
F=\frac{R}{1+R},
\qquad
k_{eff}=\frac{k_wk_a}{k_w+k_a}=k_wF.
\]

`F=0.8` requires `R=4`; `F=0.9` requires `R=9`. High `F` can coexist with low `k_eff`, so both must be reported.

The distributed 6 × 3 mm open-valley screen gives an exchange length around 0.7–1.1 mm. Twenty-to-fifty-millimeter interruption alone is therefore retained as a negative/control case rather than a preferred renewal mechanism.

### D4 — positive evaporation is not equivalent to wearer cooling

At 40 °C / 70% RH, linked heat/vapor low-order cases can continue evaporating while body-side heat flux is negative. Signed body-side heat flow remains the integrated metric.

### D5 — hot/humid same-path sign boundary

For

\[
\frac{k_{air}}{D_v}(T_\infty-T_{skin})
=
L_v[\rho_{v,sat}(T_{skin})-\phi_\infty\rho_{v,sat}(T_\infty)],
\]

with artificial skin 34 °C, representative zero-body-flux boundaries are approximately 45.25 °C at 50% RH, 39.73 °C at 70%, 37.57 °C at 80%, 36.59 °C at 85%, and 35.68 °C at 90%.

This is a model sign boundary, not a human-safety or measured garment threshold.

### D6 — ordinary heat/mass analogy does not supply arbitrary hot-ambient selectivity

The audit variable is

\[
\Xi=\delta_{vapor}/\delta_{heat}.
\]

At 40 °C / 70% RH, current low-order zero-body-flux critical `Xi` is roughly 0.31–0.65. Same-path and ordinary Lewis/Chilton–Colburn-style baselines remain near `Xi≈1`. A distinct physical mechanism is therefore required for stronger heat/vapor selectivity.

### D7 — explicit feed limitation changes the optimum

For 0.195 m² structured area, 150 g/h corresponds to ~769 g/(m²h). At 35 °C / 50% RH, strong linked exchange can be supply-limited. Once the available feed is already evaporated, making linked external exchange still stronger can reduce body-coupled cooling because a larger share of latent heat comes from warm ambient air.

### D8 — same evaporation mass can remove different amounts of body heat

At 35 °C / 50% RH / 150 g/h, modeled body share of latent heat ranges from roughly 62–64% under very strong linked exchange to roughly 78% near the modeled feed/transfer transition.

### D9 — symmetric heat spreading does not create global cooling by itself

The symmetric wet/dry screen can reduce a local temperature split from ~4.9 °C toward zero as `g_mix` increases, while area-integrated body heat flow remains essentially invariant because internal heat transfer cancels globally.

### D10 — asymmetric heat spreading creates finite mechanism value

With lower dry-side ambient sensible exposure than the wet evaporator, lateral routing moves body heat from dry regions into the active wet sink.

A dense sweep exposed a nonphysical branch jump in the old unconstrained root solver. The current solver uses bounded least squares in `(T_wet,T_dry,beta)`, explicit residual acceptance, and continuation support.

For `h_dry=5 W/(m² K)`, approximate `g_mix` for 90% of high-mixing gain:

| feed | `g_mix` | asymptotic gain over 0.195 m² |
|---:|---:|---:|
| 30 g/h | ~117 W/(m² K) | ~3.0 W |
| 50 g/h | ~192 | ~4.5 W |
| 75 g/h | ~285 | ~5.7 W |
| 100 g/h | ~330 | ~6.0 W |
| 150 g/h | ~258 | ~3.5 W |

Infinite conductivity is not the target; the mechanism shows finite diminishing returns.

### D11 — routing distance dominates material burden

The ideal periodic-stripe mapping is

\[
g_{sheet}\approx \Gamma\frac{k_{\parallel}tc}{P^2},\qquad \Gamma=4.
\]

Hence

\[
k t \propto g_{mix}P^2.
\]

For a representative `g_mix≈330 W/(m² K)` target:

- abstract `k=100 W/(m K)`, `rho=1600 kg/m³`: ~83 µm / ~40 g over 0.30 m² at `P=10 mm`, ~330 µm / ~159 g at `P=20 mm`, ~743 µm / ~357 g at `P=30 mm`;
- abstract `k=300 W/(m K)`, `rho=1800 kg/m³`: ~28 µm / ~15 g at 10 mm, ~110 µm / ~59 g at 20 mm, ~248 µm / ~134 g at 30 mm.

These are abstract property inputs, not measurements of named materials.

### D12 — sparse coverage is not automatically lighter

Under linear coverage scaling, holding `g_sheet` fixed gives

\[
m=A\rho\frac{g_{sheet}P^2}{\Gamma k},
\]

so coverage cancels. Sparse routing only saves mass if it also changes topology/path length/material/inactive-area behavior.

### D13 — thermal contacts can cap useful spreader conductance

\[
\frac{1}{g_{eff}}=\frac{1}{g_{sheet}}+\frac{2}{h_c}.
\]

Even an ideal sheet has `g_eff<h_c/2`. For a `g_target≈330 W/(m² K)` case, each-side contact must exceed ~660 W/(m² K) even for an ideal sheet; if `g_sheet≈660`, each contact must be ~1320 W/(m² K) in the lumped model.

### D14 — virtual prototypes v0.1

At 100 g/h:

| prototype | nominal concept | mass over 0.30 m² | `g_eff` | modeled spreader-only gain over 0.195 m² |
|---|---|---:|---:|---:|
| VP-A | 10 mm / `k=100` / 100 µm | ~48 g | ~286 W/(m² K) | ~5.3 W |
| VP-B | 20 mm / same class / 200 µm | ~96 g | ~167 | ~4.9 W |
| VP-C | 15 mm / 50% routed / higher `k/rho` class | ~27 g | ~197 | ~5.0 W |
| VP-D | VP-A path + stronger dry-side shielding | ~48 g | ~286 | ~6.1 W |

The gains are spreader mechanism increments versus the same local case with `g_mix=0`; they are **not total garment-vs-control performance**.

Deterministic `Gamma=2–4`, each-side contact 500–5000 W/(m² K) sensitivity at 100 g/h gives approximate gain ranges:

- VP-A: 4.4–5.4 W;
- VP-B: 3.9–5.0 W;
- VP-C: 4.1–5.2 W;
- VP-D: 5.1–6.2 W.

Current roles: VP-D performance anchor, VP-C lightweight anchor, VP-A short-pitch baseline, VP-B routing-distance/manufacturability comparison.

## E. Future physical-validation readiness

No specimen exists. All experiment files are future specifications only.

| Item | Status |
|---|---|
| Physical specimen | **NOT BUILT** |
| Physical performance data | **NOT EXECUTED** |
| B0/B2/B3/B4 definitions | PLANNED |
| E3/E3b/E3c | PLANNED |
| E4a feed transition | PLANNED |
| E4/E6 hot/humidity validation | PLANNED |
| Signed heat-flow / water-balance / T-RH requirements | SPECIFIED |
| Exact future hardware/calibration | PARTIAL |

## F. Public-release readiness

| Item | Status |
|---|---|
| Public GitHub repository | PASS |
| Apache-2.0 | PASS |
| Integrated technical disclosure | PASS / development |
| Concrete embodiment matrix | PASS / development |
| Reproducible model stack | PASS / screening |
| Explicit virtual prototypes | PASS / v0.1 development anchors |
| Future validation protocols | PASS / planned |
| Authoritative patent-office claim mapping | OPEN |
| Stable release tag | MISSING |
| Persistent archive / DOI | MISSING |
| Frozen release SHA-256 manifest | MISSING |

## G. Remaining queue

### P0 — repository / virtual-prototype quality

- [x] distributed open-valley vapor model;
- [x] feed-limited partial-wetness model;
- [x] symmetric and asymmetric wet/dry heat-spreader screens;
- [x] bounded continuation solver and branch-jump regression;
- [x] `g_mix -> k*t/P² -> thickness/mass` mapping;
- [x] two-contact thermal-resistance audit;
- [x] explicit VP-A/B/C/D v0.1 anchors;
- [x] VP tests and reference-output generator integration;
- [x] CI definition includes virtual prototype module and generated VP CSVs;
- [x] README / simulations README / roadmap / PR narrative state that no physical specimen exists;
- [ ] record a passing current-head CI run and update this audit with the verified SHA/run;
- [ ] synchronize `docs/current-results.md` and changelog with VP-A–D if any final drift remains.

### P1 — model strengthening

- [x] low-order external vapor/thermal/feed/wetness stack;
- [x] first direct material/pitch/mass/contact mapping;
- [ ] replace scalar `g_mix` with a distributed 1-D/2-D wet/dry field using direct `k`, thickness, anisotropy, contacts and patch geometry;
- [ ] predict lateral ambient exchange from geometry-resolved 2-D/3-D natural convection/cross-flow;
- [ ] re-test lumped-model multi-equilibrium behavior under improved external-flow physics;
- [ ] sensitivity to topology factor `Gamma`, compression, contact degradation, Nu/Sh, radiation, curvature and external drift.

### P2 — explicit virtual prototypes

- [x] VP-A short-pitch baseline;
- [x] VP-B 20 mm routing-distance comparison;
- [x] VP-C lightweight/high-`k/rho` routed case;
- [x] VP-D shielded short-pitch performance anchor;
- [ ] create distributed-model versions of VP-A–D without using scalar `g_mix`;
- [ ] add full architecture mass/thickness budgets beyond spreader mass alone;
- [ ] include exterior microtexture/capillary layer mass and thickness assumptions;
- [ ] add hot/humid virtual performance map for each VP.

### P3 — stable publication

- [ ] authoritative patent-family/claim verification;
- [ ] freeze exact technical-disclosure + virtual-prototype commit;
- [ ] regenerate reference artifacts and SHA-256 at that commit;
- [ ] update `CITATION.cff` / version / release notes;
- [ ] create stable tag/release;
- [ ] create persistent public archive/DOI without overwriting earlier records.

## H. Audit rules

Every significant result must answer:

1. measurement, simulation, analytic screen, inference, or hypothesis?
2. reproducible from code/data?
3. does it supersede an earlier conclusion?
4. are nonlinear branch choices explicit and residual-checked?
5. is geometric area being confused with accessible area?
6. is vapor transfer being reused as sensible heat transfer?
7. is axial Péclet number being confused with vapor renewal?
8. is a covered-channel result being generalized to an open valley?
9. is centimeter-scale segmentation assumed useful without comparison to exchange length?
10. is high `F` being confused with high evaporation capacity?
11. is positive evaporation being confused with positive body cooling?
12. does predicted evaporation exceed available liquid feed?
13. is a fully-wet state being reused after supply limitation?
14. is model `beta` being reported as measured wet area?
15. is ordinary heat/mass analogy being violated without a physical mechanism?
16. is symmetric heat spreading being generalized to asymmetric systems without stating the heterogeneity?
17. is `g_mix` quoted without routing pitch/topology/material/contact assumptions?
18. is sparse conductive coverage being assumed to reduce mass when the model says `t*c` controls conductance?
19. is a virtual-prototype spreader-only gain being confused with total garment cooling?
20. is any planned physical protocol being described as executed when no specimen exists?

If any answer is unclear, keep the item open.
