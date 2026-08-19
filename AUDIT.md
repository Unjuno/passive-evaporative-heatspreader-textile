# Repository Audit

Audit date: 2026-08-20  
Branch: `agent/initial-research-disclosure`

## Overall assessment

The branch contains a coherent technical disclosure, explicit implementation variants, **18 executable screening/sensitivity/audit modules**, regression tests, reproducible reference-output generation, prior-art working notes, and future physical-test protocols.

It remains a development branch and a **virtual/computational prototype only**. No physical garment or bench specimen currently exists, and no physical garment-performance measurements have been published.

The present numerical record supports a narrower and more falsifiable design direction:

> wet microstructures + spatially purposeful short-range heat routing + continuously ambient-connected exterior valleys/islands + explicit liquid-supply/wetness state + explicit thermal-contact burden + hot-ambient sensible-heat protection.

Long covered passive chimneys, geometric area alone, centimeter-scale interruption alone, high local vapor-retention `F` alone, positive evaporation alone, fully-wet capacity above available feed, heat spreading without spatially heterogeneous boundary conditions, and high sheet conductivity without routing/contact constraints are no longer accepted as sufficient design criteria.

## A. Technical coherence

| Item | Status | Audit note |
|---|---|---|
| Directional sweat transport | PASS | Core layer retained. |
| Flexible whole-garment/routed heat spreader | PASS/REFINED | Value is tied to spatially nonuniform wetting/exposure/coupling, not internal mixing alone. |
| Heat-spreader material mapping | PASS/SCREEN | `g_mix` now maps to `k*t/pitch²`, mass and contact burden under an explicit topology assumption. |
| Capillary liquid delivery | PASS | Distributed liquid path retained. |
| Exterior micro-ribs / 3D knit / fins / lamellae | PASS | Multiple concrete families documented. |
| Hierarchical ambient-access exterior | PASS | Open valleys, cross-openings, short interruptions, islands and covered comparison channels explicit. |
| Sensible/vapor separation | PASS | Heat and vapor exchange are not forced to share one multiplier. |
| Ordinary heat/mass analogy baseline | PASS/SCREEN | Lewis and Chilton–Colburn-style comparison added; not a validated textile correlation. |
| Explicit feed-limited state | PASS/SCREEN | Homogenized sub-grid wet fraction `beta` is solved when feed is below fully-wet capacity. |
| Separate wet/dry temperatures | PASS/SCREEN | Symmetric and asymmetric two-node screens test when heat spreading changes local and global results. |
| Hot-ambient dry-side protection | PASS/HYPOTHESIS | Required by several screens; no physical validation yet. |
| Fan | OPTIONAL | Not required by primary architecture. |
| Sorbent/MOF | OPTIONAL | Secondary embodiment only. |
| Salt | PASS | Water evaporates; salt vapor flux is zero. |
| Apparel integration | PASS | Low-profile texture/pattern implementations documented. |

## B. Executable model / audit stack

1. `simulations/passive_rib_screen.py` — historical coupled exterior heat/mass screen and multi-root audit.
2. `simulations/split_heat_mass_screen.py` — independent `M_h` and `M_m` lumped screen.
3. `simulations/split_transfer_sensitivity.py` — deterministic model-form sensitivity grid.
4. `simulations/rib_diffusion_screen.py` — periodic 2-D rib vapor-diffusion screen.
5. `simulations/corridor_buoyancy_screen.py` — prescribed-state thermo-solutal corridor buoyancy.
6. `simulations/self_consistent_corridor_1d.py` — covered/end-renewed corridor T/RH/flow coupling.
7. `simulations/open_valley_exchange_target.py` — local open-valley `R/F` target and measurement inversion.
8. `simulations/open_valley_distributed_1d.py` — axial diffusion/advection plus distributed lateral vapor renewal.
9. `simulations/open_valley_thermal_1d.py` — distributed open-valley heat/vapor/wet-wall energy coupling with optional homogenized wet fraction.
10. `simulations/open_valley_feed_limited.py` — explicit feed-limited partial-wetness closure and latent heat-source partition.
11. `simulations/wet_dry_two_node.py` — separate wet/dry temperatures linked by lateral heat-spreader mixing under symmetric external coefficients.
12. `simulations/asymmetric_wet_dry_spreader.py` — bounded/continuation partial-wetness screen with unequal wet/dry ambient sensible coefficients.
13. `simulations/spreader_material_mapping.py` — maps `g_mix` to sheet `k*t/pitch²`, mass, simple bending strain and two-contact resistance burden.
14. `simulations/open_valley_heat_mass_coupling_audit.py` — required heat/vapor selectivity plus same-length and Chilton–Colburn-style baselines.
15. `simulations/passive_environment_boundary.py` — analytic hot/humid body-heat-flow sign boundary and skin-setpoint sensitivity.
16. `simulations/supply_limit_audit.py` — conservative capacity/feed classification retained as a non-dryout upper-bound audit.
17. `simulations/heat_spreader_2d.py` — anisotropic lateral heat-routing screen.
18. `simulations/water_salt_1d.py` — nonvolatile salt/water mass-balance screen.

`simulations/generate_reference_outputs.py` is the reproducibility generator rather than a physical model.

All models remain screening models. None is a validated CFD replacement or physical garment-performance measurement.

## C. Reproducibility / verification

| Item | Status | Audit note |
|---|---|---|
| Regression tests | PASS/UPDATED | Include multi-root, split transfer, E3, corridor, open-valley, feed-limited, wet/dry, asymmetric continuation, material/contact mapping, coupling, heat-spreader and salt checks. |
| E3 grid convergence | PASS/SCREEN | 24 nodes/pitch within ~0.62% of 48-node reference for the screened case. |
| Distributed open-valley convergence | PASS/SCREEN | Center `F` stable over tested grids. |
| Wall-energy closure | PASS | Thermal open-valley tests enforce `q_body + q_air = L_v m_evap` numerically. |
| Feed balance closure | PASS | Supply-limited solver regression requires evaporation to match imposed feed within numerical tolerance. |
| Latent-source partition | PASS | Feed-limited test requires body + ambient latent fractions to close to approximately one. |
| Wet/dry two-node global energy closure | PASS | Separate wet/dry temperatures conserve feed and energy in the symmetric screen. |
| Asymmetric branch acceptance | PASS/NEW | Solver uses bounded least squares; dense continuation regression rejects high-beta/nonphysical branch jumps. |
| Material mapping round trip | PASS/NEW | `g_mix -> thickness -> g_mix`, quadratic pitch penalty, coverage/mass identity and contact ceiling are regression-tested. |
| Reference generator | PASS/UPDATED | Asymmetric and spreader material/contact CSVs are included. |
| CI definition | PASS/UPDATED | Current model stack and generated artifacts are exercised. |
| Previously verified computational integration | PASS | GitHub Actions `model-tests` #370 succeeded at SHA `a01eeafc8ae6814349a3a0937251efd048823dae` before the latest material-mapping commits. |
| Current material-mapping integration | CHECK | Record a newer passing run after the latest solver/mapping/docs changes before calling the current head verified. |

## D. Major numerical findings

### D1 — nonlinear equilibrium branches

The original lumped passive heat/mass model can contain multiple stable equilibria. Historical single-value `M` thresholds are exploratory references only.

### D2 — rib boundary-layer sharing

For the E3 screen (`h=2.5 mm`, structured fraction `f=0.65`), whole-area vapor multipliers fall from roughly 3–4 at a 0.5 mm idealized renewal gap to roughly 1.3 at a 5 mm gap. Tight pitch alone cannot overcome a shared stagnant humidity layer.

### D3 — sensible and vapor exchange differ

`M_h` and `M_m` are distinct. In hot ambient air, improved vapor transfer can help evaporation while improved sensible transfer can increase inward environmental heat pickup.

### D4 — passive corridor flow can reverse

Thermo-solutal buoyancy can produce upward, downward or near-neutral flow. A vertical groove is not a guaranteed chimney.

### D5 — covered/end-renewed corridors saturate

The self-consistent 100 mm corridor screen at 35 °C / 70% RH gives nonzero natural flow but mean RH near saturation for 3×2, 6×3 and 10×5 mm channels. High axial Péclet number is not proof that useful vapor driving force remains.

### D6 — open-valley renewal requirement

For local conductance ratio

\[
R=G_a/G_w,\qquad F=\frac{R}{1+R},
\]

`F=0.8` requires `R=4`; `F=0.9` requires `R=9`. Exact high inferred `R` is measurement-ill-conditioned, so `F` is the preferred mechanism metric.

### D7 — centimeter-scale segmentation correction

The distributed vapor model gives a representative exchange length of roughly 0.7–1.1 mm for a 6×3 mm valley across the screened lateral-exchange range. Therefore 20–50 mm interruption alone does not materially rescue a weakly renewed interior.

Virtual/protocol roles:

- O1 — continuously laterally open: principal hypothesis;
- O2a — 20–50 mm interruption: negative/control;
- O2b — 1–3 mm segments: extreme end-access test;
- O3 — discontinuous ambient-connected wet islands: apparel-relevant implementation.

### D8 — `F` is not absolute evaporation capacity

For local resistances in series:

\[
k_{eff}=\frac{k_wk_a}{k_w+k_a}=k_wF.
\]

Deeper valleys can increase `F` while decreasing `k_eff`. Every design must report both renewal quality and absolute transfer.

### D9 — coupled open-valley thermal result

At 35 °C / 70% RH, stronger vapor renewal improves body heat removal in the current screen. At 40 °C / 70% RH, linked heat/vapor exchange still evaporates water while body-side heat flux is negative.

**Audit conclusion:** positive evaporation is not equivalent to wearer cooling.

### D10 — ordinary heat/mass analogy does not meet the modeled 40 °C / 70% RH selectivity burden

The sensitivity parameter is

\[
\Xi=\delta_{vapor}/\delta_{heat}.
\]

At 40 °C / 70% RH, the low-order zero-body-flux critical `Xi` is approximately 0.31–0.65 across the screened vapor-side range.

The screening Lewis number is near one. A same-exchange-length baseline has `Xi=1`, and a Chilton–Colburn-style equal-j-factor comparison gives `Xi_CC=Le^{-1/3}`, also near one.

Neither ordinary baseline reaches the required selectivity in the current audit.

**Interpretation:** hot-ambient protection must invoke a distinct physical mechanism; arbitrary passive heat/mass decoupling is not assumed.

### D11 — explicit feed-limited partial wetness

For a structured area of `0.30 × 0.65 = 0.195 m²`, a 150 g/h total feed corresponds to about 769 g/(m²h).

At 35 °C / 50% RH with linked heat/vapor exchange:

| linked parameter | regime | solved `beta` | total evaporation | body heat flux |
|---:|---|---:|---:|---:|
| 0.10 mm | supply-limited | ~0.37 | ~150 g/h | ~331 W/m² |
| 0.25 mm | supply-limited | ~0.43 | ~150 g/h | ~356 W/m² |
| 0.50 mm | supply-limited | ~0.55 | ~150 g/h | ~383 W/m² |
| ~0.95–1.0 mm | transition | ~1 | ~147–150 g/h | ~400–411 W/m² |
| 2.0 mm | transfer-limited | 1 | ~109 g/h | ~317 W/m² |

**Audit correction:** under fixed feed, making linked external exchange stronger after supply limitation can reduce body-coupled cooling.

### D12 — latent heat can come substantially from ambient air

At 35 °C / 50% RH / 150 g/h, several supply-limited cases evaporate the same total feed but differ in body contribution to latent heat:

- very strong linked exchange: body share ~62–64%;
- 0.5 mm linked case: body share ~74%;
- near 0.75 mm: body share ~78%.

Therefore evaporation mass and body heat removal must remain separate reported quantities.

### D13 — symmetric two-temperature wet/dry screen

At 35 °C / 50% RH / 150 g/h with symmetric wet/dry external and body-side sensible coefficients:

- `g_mix=0`: wet/dry temperature split ~4.9 °C;
- around 50 W/(m²-total K): split ~1.6 °C;
- around 100 W/(m²-total K): split ~1.0 °C;
- around 500 W/(m²-total K): split ~0.3 °C;
- very high mixing approaches one temperature.

The global body heat flux is essentially invariant because the boundary conditions are deliberately symmetric.

**Audit interpretation:** a heat spreader does not create total cooling merely by equalizing otherwise identical patches.

### D14 — asymmetric heat-spreader synergy and solver correction

When the dry region has lower ambient sensible exposure than the wet evaporator, lateral heat spreading can route body heat from the dry region into the wet sink and increase total modeled body heat removal.

A dense `g_mix` sweep exposed nonphysical branch jumps in the earlier unconstrained nonlinear solver. The asymmetric solver now uses bounded least squares in `(T_wet, T_dry, beta)`, explicit residual acceptance, and continuation support.

For `h_dry=5 W/(m² K)`, corrected approximate `g_mix` values needed to capture 90% of the high-mixing gain are:

| feed | `g_mix` for 90% gain |
|---:|---:|
| 30 g/h | ~117 W/(m² K) |
| 50 g/h | ~192 W/(m² K) |
| 75 g/h | ~285 W/(m² K) |
| 100 g/h | ~330 W/(m² K) |
| 150 g/h | ~258 W/(m² K) |

High-mixing gains over the 0.195 m² structured area are finite, roughly 3.0, 4.5, 5.7, 6.0 and 3.5 W respectively.

**Audit interpretation:** infinite conductivity is not the target; a finite useful-conductance band exists in this low-order mechanism screen.

### D15 — material/pitch/mass mapping

For an ideal periodic alternating wet/dry stripe topology:

\[
g_{sheet}\approx \Gamma\frac{k_{\parallel}tc}{P^2},\qquad \Gamma=4.
\]

The main scaling is

\[
k t \propto g_{mix}P^2.
\]

The quadratic routing-pitch penalty is large. For the representative 100 g/h / 90%-gain target (`g_mix≈330 W/(m² K)`):

- abstract `k=100 W/(m K)`, `rho=1600 kg/m³`: ~83 µm / ~40 g over 0.30 m² at `P=10 mm`; ~330 µm / ~159 g at `P=20 mm`; ~743 µm / ~357 g at `P=30 mm`;
- abstract `k=300 W/(m K)`, `rho=1800 kg/m³`: ~28 µm / ~15 g at `P=10 mm`; ~110 µm / ~59 g at `P=20 mm`; ~248 µm / ~134 g at `P=30 mm`.

These property classes are explicit screening inputs, not named-material measurements.

Under linear coverage scaling, lowering conductive coverage and increasing thickness to preserve `g_sheet` leaves mass unchanged. Sparse routing is therefore not automatically lighter. The simple mass figure of merit is `k/rho`.

### D16 — thermal contact can dominate sheet conductivity

A two-contact series screen is

\[
\frac{1}{g_{eff}}=\frac{1}{g_{sheet}}+\frac{2}{h_c}.
\]

Even an infinitely conductive sheet has

\[
g_{eff}<h_c/2.
\]

For the representative `g_target≈330 W/(m² K)` case, the absolute minimum each-side contact conductance is about 660 W/(m² K). If `g_sheet` is only twice the target, the model requires each contact to be about 1320 W/(m² K).

**Audit interpretation:** sheet `k` alone is not a sufficient implementation metric. Routing pitch, topology, thickness and integrated wet/dry thermal contact must be explicit.

## E. Future physical-validation readiness

No specimen exists yet; this section records protocol readiness only.

| Item | Status | Audit note |
|---|---|---|
| B0/B2/B3/B4 controls | PASS/PLANNED | Defined for a future bench implementation. |
| Primary environment | PASS/PLANNED | 35 °C / 70% RH / 150 g/h / nominal still air / 34 °C artificial skin. |
| Primary endpoint | PASS/PLANNED | Signed heater/cooler power or signed heat flux. |
| Water balance | PASS/PLANNED | >=95% target. |
| E3/E3b | PASS/PLANNED | Pitch/boundary-layer and hierarchical access tests defined. |
| E3c | PASS/PLANNED | D1/O1/O2a/O2b/O3 defined with `F` plus absolute-transfer metrics. |
| E4a feed transition | PASS/PLANNED | Feed sweep plus visible/derived wetness comparison defined. |
| E4 humidity | PASS/PLANNED | Supply-limit classification included. |
| E6 hot ambient | PASS/PLANNED | Positive evaporation with negative body cooling is an explicit failure mode. |
| Physical specimen | **MISSING / NOT YET BUILT** | Current work is virtual/computational only. |
| Physical data | **MISSING / NOT EXECUTED** | No bench experiment executed. |
| Exact hardware/calibration budget | PARTIAL | Retained only for future implementation. |

## F. Public-release readiness

| Item | Status |
|---|---|
| Public GitHub repository | PASS |
| Apache-2.0 | PASS |
| Integrated technical disclosure | PASS / development |
| Concrete embodiment matrix | PASS / development |
| Reproducible model stack | PASS / screening |
| Future validation protocols | PASS / planned |
| Authoritative patent-office claim mapping | OPEN |
| Physical evidence | NOT AVAILABLE |
| Stable release tag | MISSING |
| Persistent archive / DOI | MISSING |
| Frozen release SHA-256 manifest | MISSING |

## G. Remaining queue

### P0 — repository quality

- [x] distributed open-valley vapor model;
- [x] `F`/`k_eff` metric audit;
- [x] coupled open-valley thermal/vapor model;
- [x] explicit homogenized feed-limited partial-wetness model;
- [x] latent heat-source partition output;
- [x] Lewis / Chilton–Colburn-style heat/mass analogy comparison;
- [x] symmetric two-temperature wet/dry patch screen;
- [x] asymmetric wet/dry spreader mechanism screen;
- [x] bounded continuation solver and branch-jump regression;
- [x] `g_mix -> k*t/pitch² -> thickness/mass` mapping;
- [x] two-contact thermal-resistance audit;
- [x] reference-generator / CI definition integration for material/contact mapping;
- [x] README and simulations README virtual-prototype/material-mapping synchronization;
- [ ] confirm current expanded integration CI passes at a recorded SHA;
- [ ] synchronize `docs/current-results.md`, roadmap/changelog and PR narrative after the passing run.

### P1 — model strengthening

- [x] axial diffusion + distributed lateral vapor renewal;
- [x] low-order open-valley heat/vapor/wet-wall coupling;
- [x] explicit liquid-feed-limited homogenized solution;
- [x] ordinary Lewis/Chilton–Colburn-style coupling comparison;
- [x] separate-temperature wet/dry mechanism screens;
- [x] first material/pitch/mass/contact mapping of the abstract heat-spreader conductance;
- [ ] resolve wet/dry patches in a distributed 1-D/2-D field with unequal local boundary conditions and direct `k`, thickness and contact terms;
- [ ] predict lateral exchange from geometry-resolved 2-D/3-D natural convection/cross-flow;
- [ ] re-test lumped-model multi-equilibrium behavior under improved external-flow treatment;
- [ ] sensitivity to topology factor `Gamma`, Nu/Sh, compression, contact degradation, opening losses, radiation and external drift.

### P2 — future physical evidence

No physical specimen currently exists. These remain future tasks, not active measurements:

- [ ] build a representative B0/B2/B3/B4 bench specimen set;
- [ ] E1 B0 vs B4;
- [ ] E2 ablation;
- [ ] E3/E3b;
- [ ] E3c D1/O1/O2a/O2b/O3;
- [ ] E4a feed-limit / wetness transition;
- [ ] E4 humidity boundary;
- [ ] E6 hot-ambient shielding / sensible-heat penalty;
- [ ] publish raw data, calibration metadata, uncertainty and negative results if/when these tests are executed.

### P3 — stable publication

- [ ] authoritative patent-family/claim verification;
- [ ] freeze one exact technical-disclosure commit;
- [ ] regenerate reference artifacts and SHA-256 at that commit;
- [ ] update `CITATION.cff` / version / release notes;
- [ ] create stable tag/release;
- [ ] create persistent public archive/DOI without overwriting earlier records.

## H. Audit rules

Every significant result must answer:

1. measurement, simulation, analytic screen, inference, or hypothesis?
2. reproducible from code/data?
3. does it supersede an earlier conclusion?
4. is the broad mechanism already prior art?
5. are nonlinear branch choices explicit and residual-checked?
6. is geometric area being confused with accessible area?
7. is vapor transfer being reused as sensible heat transfer?
8. is axial Péclet number being confused with vapor renewal?
9. is a covered-channel result being generalized to an open valley?
10. is centimeter-scale segmentation assumed useful without comparison to exchange length?
11. is high `F` being confused with high evaporation capacity?
12. is positive evaporation being confused with positive body cooling?
13. does predicted evaporation exceed available liquid feed?
14. is a fully-wet body-flux state being reused after supply limitation?
15. is model `beta` being misreported as measured visible wet fraction?
16. is ordinary heat/mass analogy being violated without a physical mechanism?
17. is a symmetric internal heat-spreading result being generalized to spatially heterogeneous boundary conditions?
18. is a `g_mix` benefit being quoted without routing pitch/topology/material/contact assumptions?
19. is sparse conductive coverage being assumed to reduce mass under a model where `t*c` is the controlling product?
20. is any large inferred `R` reported more precisely than T/RH uncertainty supports?
21. is any planned physical protocol being described as an executed experiment when no specimen exists?

If any answer is unclear, keep the item open.
