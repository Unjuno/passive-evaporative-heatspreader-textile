# Repository Audit

Audit date: 2026-08-20  
Branch: `agent/initial-research-disclosure`

## Overall assessment

The branch contains a coherent technical disclosure, explicit implementation variants, **20 executable screening/sensitivity/audit/virtual-prototype modules**, regression tests, reproducible reference-output generation, prior-art working notes, and future physical-test protocols.

It remains a development branch and a **virtual/computational prototype only**. No physical garment or bench specimen currently exists, and no physical garment-performance measurements have been published.

The numerical record now supports a narrower design hypothesis:

> directional liquid transport + capillary-fed wet microtexture + continuously ambient-connected exterior valleys/islands + short-range high-`k/rho` heat routing between thermally asymmetric wet/dry regions + explicit thermal contacts + explicit liquid-supply state + hot-ambient sensible-heat protection.

The repository no longer accepts geometric area alone, long passive wet chimneys, axial Péclet number alone, centimeter-scale segmentation alone, high local `F` alone, positive evaporation alone, fully-wet capacity above feed, heat spreading under symmetric boundary conditions, infinite sheet conductivity, sparse coverage as automatic mass reduction, or high sheet `k` without routing/contact constraints as sufficient design criteria.

## A. Technical coherence

| Item | Status | Audit note |
|---|---|---|
| Directional sweat transport | PASS | Core layer retained. |
| Capillary liquid delivery | PASS | Distributed liquid path retained. |
| Exterior micro-ribs / 3D knit / fins / lamellae | PASS | Multiple concrete families documented. |
| Hierarchical ambient access | PASS | Open valleys, cross-openings, short interruptions, islands and covered comparisons explicit. |
| Sensible/vapor separation | PASS | Heat and vapor transfer are not forced to share one multiplier. |
| Explicit feed-limited state | PASS/SCREEN | Homogenized wet fraction solves imposed feed when fully-wet capacity is too high. |
| Separate wet/dry temperatures | PASS/SCREEN | Symmetric and asymmetric two-node models exist. |
| Asymmetric heat-routing value | PASS/SCREEN | System-level spreader gain appears only when local boundary conditions differ. |
| Material/pitch mapping | PASS/SCREEN | `g_mix` maps to `k*t/P²`, mass and bend-strain screening under an explicit topology factor. |
| Thermal-contact mapping | PASS/SCREEN | Two-contact series burden is explicit. |
| Virtual prototypes v0.1 | PASS/DEV | VP-A through VP-D are reproducible computational anchors. |
| Direct-material distributed bridge | PASS/DEV | Scalar `g_mix` is replaced by periodic 1-D direct `k*t` conduction for VP regression. |
| Hot-ambient protection | PASS/HYPOTHESIS | Required by several screens; no physical validation. |
| Salt handling | PASS | Water evaporates; salt vapor flux is zero. |
| Apparel integration | PASS/CONCEPT | Low-profile patterns, valleys/islands and routed paths documented. |

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
15. `simulations/distributed_spreader_1d.py`
16. `simulations/open_valley_heat_mass_coupling_audit.py`
17. `simulations/passive_environment_boundary.py`
18. `simulations/supply_limit_audit.py`
19. `simulations/heat_spreader_2d.py`
20. `simulations/water_salt_1d.py`

`simulations/generate_reference_outputs.py` is the reproducibility generator rather than a physical model.

All models are screening/analytic/virtual-prototype models. None is validated CFD or measured garment performance.

## C. Reproducibility / verification

| Item | Status | Audit note |
|---|---|---|
| Regression tests | PASS/UPDATED | Include multi-root, split transfer, E3, corridor, open-valley, feed-limited, wet/dry, asymmetric continuation, material/contact, virtual-prototype and distributed-spreader checks. |
| E3 grid convergence | PASS/SCREEN | 24 nodes/pitch within ~0.62% of 48-node reference for the screened case. |
| Distributed open-valley convergence | PASS/SCREEN | Center `F` stable over tested grids. |
| Coupled wall-energy closure | PASS | Open-valley regression exists. |
| Feed balance closure | PASS | Feed-limited model matches imposed feed numerically. |
| Asymmetric branch acceptance | PASS | Bounded least squares + residual threshold + continuation replaced the earlier branch-jumping solver. |
| Material mapping identities | PASS | Round trip, quadratic pitch penalty, coverage/mass identity and contact ceiling are tested. |
| Virtual prototype regression | PASS | VP-A/B/C/D nominal and relative design expectations are tested. |
| Distributed feed closure | PASS/SCREEN | Development screen closes 100 g/h feed to better than ~0.001 g/h. |
| Distributed outer-energy residual | PASS/SCREEN | Numerically near zero in checked VP cases. |
| Distributed spreader residual | PASS/SCREEN | ~0.004 W/m² or lower in checked VP cases. |
| Distributed grid convergence | PASS/SCREEN | VP-A 32→96-node body-flux change is ~0.01 W/m². |
| Scalar/distributed hierarchy continuity | PASS/SCREEN | VP-A–D distributed gains remain within ~0.8 W of scalar-anchor gains. |
| Reference generator | PASS/UPDATED | Material/contact, VP and distributed-spreader CSVs included. |
| CI definition | PASS/UPDATED | Current workflow runs all current executable models and checks generated distributed output. |
| Previously verified integration | PASS | `model-tests` #370 succeeded at SHA `a01eeafc8ae6814349a3a0937251efd048823dae` before the latest material/VP/distributed updates. |
| Current 20-module head | CHECK | Record a newer successful Actions run before marking the current head verified. |

## D. Major findings retained

### D1 — exterior area requires ambient access

Dense wet ribs can share one humidity boundary layer. In the E3 screen, whole-area vapor multipliers fall from roughly 3–4 at a 0.5 mm idealized renewal gap to roughly 1.3 at a 5 mm gap.

### D2 — long wet covered corridors are weak

Covered/end-renewed channels can sustain nonzero natural flow while remaining nearly saturated, and flow direction can reverse. Velocity and axial Péclet number are not accepted as success metrics alone.

### D3 — open-valley renewal requires both `F` and absolute conductance

\[
R=G_a/G_w,
\quad F=\frac{R}{1+R},
\quad k_{eff}=\frac{k_wk_a}{k_w+k_a}=k_wF.
\]

`F=0.8` requires `R=4`; `F=0.9` requires `R=9`. The representative distributed open-valley exchange length is ~0.7–1.1 mm, making 20–50 mm interruption a negative/control case rather than the preferred mechanism.

### D4 — positive evaporation can coexist with inward body heat flow

At 40 °C / 70% RH, linked heat/vapor low-order cases can still evaporate while body-side heat flow is negative.

### D5 — hot/humid same-path sign boundary

For a 34 °C artificial skin, representative zero-body-flux boundaries are ~45.25 °C at 50% RH, ~39.73 °C at 70%, ~37.57 °C at 80%, ~36.59 °C at 85%, and ~35.68 °C at 90%. This is a model sign boundary, not a safety/medical threshold.

### D6 — arbitrary heat/vapor selectivity is not assumed

At 40 °C / 70% RH, current low-order critical `Xi=delta_vapor/delta_heat` is roughly 0.31–0.65. Ordinary same-path / Lewis / Chilton–Colburn-style baselines remain near one. A distinct physical mechanism is required to claim stronger selectivity.

### D7 — feed limitation changes the optimum

Once all available feed is already evaporated, stronger linked ambient exchange can reduce body-coupled cooling because more latent heat comes from warm ambient air.

### D8 — identical evaporation mass does not imply identical body heat removal

At 35 °C / 50% RH / 150 g/h, modeled body share of latent heat varies from roughly 62–64% under very strong linked exchange to roughly 78% near the feed/transfer transition.

### D9 — symmetric heat spreading does not create global cooling

Internal equalization under identical wet/dry external boundary conditions changes local temperatures but leaves area-integrated body heat flow essentially unchanged.

### D10 — asymmetric heat spreading creates finite value

With a shielded/weaker-exposed dry region and an active wet sink, lateral routing increases total modeled body heat removal. Corrected `h_dry=5 W/(m² K)` scalar targets for ~90% of high-mixing gain are ~117, 192, 285, 330 and 258 W/(m² K) at 30, 50, 75, 100 and 150 g/h respectively. High-mixing gains over 0.195 m² are finite, roughly 3–6 W.

### D11 — routing pitch has a quadratic burden

\[
g_{sheet}\approx\Gamma\frac{k_{\parallel}tc}{P^2},\qquad\Gamma=4.
\]

For a representative `g_mix≈330 W/(m² K)` target, abstract `k=100 W/(m K)`, `rho=1600 kg/m³` maps to ~83 µm / 40 g over 0.30 m² at 10 mm pitch, ~330 µm / 159 g at 20 mm, and ~743 µm / 357 g at 30 mm.

### D12 — sparse coverage is not automatically lighter

Under linear `t*c` scaling, coverage cancels from idealized mass at fixed target conductance. Sparse routing only helps if topology/path/material/inactive-area behavior also changes.

### D13 — contact can dominate sheet conductivity

\[
1/g_{eff}=1/g_{sheet}+2/h_c.
\]

For `g_target≈330 W/(m² K)`, even an ideal sheet requires each-side `h_c>~660 W/(m² K)` in the lumped contact screen.

### D14 — virtual prototypes v0.1 scalar anchors

At 100 g/h:

| VP | mass over 0.30 m² | scalar spreader-only gain over 0.195 m² |
|---|---:|---:|
| A | ~48 g | ~5.3 W |
| B | ~96 g | ~4.9 W |
| C | ~27 g | ~5.0 W |
| D | ~48 g | ~6.1 W |

These are spreader mechanism increments, not total garment-vs-control performance.

### D15 — direct-material distributed bridge retains the design direction

The 1-D bridge solves

\[
\frac{d}{dx}\left(k_{\parallel}t\frac{dT_s}{dx}\right)
+U_b(T_{skin}-T_s)+h_c(T_o-T_s)=0
\]

with local wet evaporation, dry shielding, periodic routing and feed-solved continuous wet width.

At 100 g/h, equal-feed no-lateral baseline comparison gives:

| VP | wet fraction | distributed spreader-only gain over 0.195 m² |
|---|---:|---:|
| A | ~0.444 | ~5.48 W |
| B | ~0.448 | ~5.32 W |
| C | ~0.451 | ~5.30 W |
| D | ~0.447 | ~6.29 W |

This preserves the short-pitch and shielding conclusions without using scalar `g_mix`. Distributed/scalar gains agree within ~0.8 W, which is hierarchy continuity rather than independent validation.

**Important limitation:** VP-C's 50% coverage is still homogenized as effective thickness. Actual sparse trace geometry, tortuosity and local contact loss are not yet resolved.

## E. Future physical-validation readiness

No specimen exists. Experiment files are future specifications only.

| Item | Status |
|---|---|
| Physical specimen | **NOT BUILT** |
| Physical performance data | **NOT EXECUTED** |
| B0/B2/B3/B4 definitions | PLANNED |
| E3/E3b/E3c | PLANNED |
| E4a feed transition | PLANNED |
| E4/E6 hot/humidity validation | PLANNED |
| Signed heat-flow / water-balance / T-RH requirements | SPECIFIED |

## F. Public-release readiness

| Item | Status |
|---|---|
| Public GitHub repository | PASS |
| Apache-2.0 | PASS |
| Integrated technical disclosure | PASS / development |
| Reproducible model stack | PASS / screening |
| Explicit virtual prototypes | PASS / v0.1 anchors |
| Direct-material distributed bridge | PASS / development |
| Future validation protocols | PASS / planned |
| Authoritative patent-office claim mapping | OPEN |
| Stable release tag | MISSING |
| Persistent archive / DOI | MISSING |
| Frozen release SHA-256 manifest | MISSING |

## G. Remaining queue

### P0 — repository / virtual-prototype quality

- [x] feed-limited / wet-dry / asymmetric model stack;
- [x] bounded continuation solver and branch-jump regression;
- [x] material/pitch/mass/contact mapping;
- [x] VP-A/B/C/D scalar anchors;
- [x] direct-material distributed 1-D bridge;
- [x] distributed grid/feed/energy regression;
- [x] reference-generator / CI integration;
- [ ] record a successful current-head CI run and update this audit with exact SHA/run;
- [ ] ensure README/current-results/changelog/PR all show 20-model state.

### P1 — model strengthening

- [ ] move from periodic 1-D to geometry-resolved 2-D heat routing with direct `k_x/k_y`, explicit traces, contact maps, wet islands and dry shielding;
- [ ] predict exterior lateral exchange from geometry-resolved 2-D/3-D natural convection/cross-flow;
- [ ] re-test lumped multi-equilibrium behavior under improved external-flow physics;
- [ ] sensitivity to topology factor, compression, contact degradation, Nu/Sh, radiation, curvature and external drift.

### P2 — virtual-prototype completion

- [x] VP-A short-pitch baseline;
- [x] VP-B routing-distance comparison;
- [x] VP-C lightweight/high-`k/rho` anchor;
- [x] VP-D shielded performance anchor;
- [x] direct-material 1-D versions of VP-A–D;
- [ ] resolve VP-C sparse trace topology explicitly in 2-D;
- [ ] add full garment mass/thickness budget beyond spreader layer;
- [ ] add hot/humid performance map for each VP.

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
8. is high `F` being confused with high evaporation capacity?
9. is positive evaporation being confused with body cooling?
10. does predicted evaporation exceed available feed?
11. is model wet fraction being reported as measured wet area?
12. is ordinary heat/mass analogy being violated without a mechanism?
13. is symmetric heat spreading being generalized to asymmetric systems without stating the heterogeneity?
14. is `g_mix` quoted without routing/material/contact assumptions?
15. is sparse conductive coverage being assumed to reduce mass automatically?
16. is scalar-to-distributed agreement being misrepresented as independent validation?
17. is VP-C homogenized coverage being misrepresented as resolved sparse-trace behavior?
18. is a virtual-prototype spreader-only gain being confused with total garment cooling?
19. is any planned physical protocol being described as executed when no specimen exists?

If any answer is unclear, keep the item open.
