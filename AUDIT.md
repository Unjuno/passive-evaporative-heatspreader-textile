# Repository Audit

Audit date: 2026-08-20  
Branch: `agent/initial-research-disclosure`

## Overall assessment

The branch contains a coherent technical disclosure, explicit implementation variants, **15 executable screening/sensitivity/audit modules**, regression tests, reproducible reference-output generation, prior-art working notes, and staged physical protocols.

It remains a development branch. **No physical garment-performance measurements have been published yet.**

The present numerical record supports a narrower and more falsifiable exterior design direction:

> wet microstructures + strong lateral heat routing + continuously ambient-connected exterior valleys/islands + explicit liquid-supply state + hot-ambient sensible-heat protection.

Long covered passive chimneys, geometric area alone, centimeter-scale interruption alone, high local vapor-retention `F` alone, positive evaporation alone, and fully-wet capacity above available feed are no longer accepted as sufficient design criteria.

## A. Technical coherence

| Item | Status | Audit note |
|---|---|---|
| Directional sweat transport | PASS | Core layer retained. |
| Flexible whole-garment/routed heat spreader | PASS | Continuous, anisotropic, mesh, serpentine, island-bridge variants documented. |
| Capillary liquid delivery | PASS | Distributed liquid path retained. |
| Exterior micro-ribs / 3D knit / fins / lamellae | PASS | Multiple concrete families documented. |
| Hierarchical ambient-access exterior | PASS | Open valleys, cross-openings, short interruptions, islands and covered comparison channels explicit. |
| Sensible/vapor separation | PASS | Heat and vapor exchange are not forced to share one multiplier. |
| Ordinary heat/mass analogy baseline | PASS/SCREEN | Lewis and Chilton–Colburn-style comparison added; not a validated textile correlation. |
| Explicit feed-limited state | PASS/SCREEN | Homogenized sub-grid wet fraction `beta` now solved when feed is below fully-wet capacity. |
| Hot-ambient dry-side protection | PASS/HYPOTHESIS | Required by several screens; physical validation still open. |
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
9. `simulations/open_valley_thermal_1d.py` — distributed open-valley heat/vapor/wet-wall energy coupling, now with optional homogenized wet fraction.
10. `simulations/open_valley_feed_limited.py` — explicit feed-limited partial-wetness closure and latent heat-source partition.
11. `simulations/open_valley_heat_mass_coupling_audit.py` — required heat/vapor selectivity plus same-length and Chilton–Colburn-style baselines.
12. `simulations/passive_environment_boundary.py` — analytic hot/humid body-heat-flow sign boundary and skin-setpoint sensitivity.
13. `simulations/supply_limit_audit.py` — conservative capacity/feed classification retained as a non-dryout upper-bound audit.
14. `simulations/heat_spreader_2d.py` — anisotropic lateral heat-routing screen.
15. `simulations/water_salt_1d.py` — nonvolatile salt/water mass-balance screen.

`simulations/generate_reference_outputs.py` is the reproducibility generator rather than a physical model.

All models remain screening models. None is a validated CFD replacement or physical garment-performance measurement.

## C. Reproducibility / verification

| Item | Status | Audit note |
|---|---|---|
| Regression tests | PASS/UPDATED | Include multi-root, split transfer, E3, corridor, open-valley, feed-limited, coupling, heat-spreader and salt checks. |
| E3 grid convergence | PASS/SCREEN | 24 nodes/pitch within ~0.62% of 48-node reference for the screened case. |
| Distributed open-valley convergence | PASS/SCREEN | Center `F` stable over tested grids. |
| Wall-energy closure | PASS | Thermal open-valley tests enforce `q_body + q_air = L_v m_evap` numerically. |
| Feed balance closure | PASS/NEW | Supply-limited solver regression requires evaporation to match imposed feed within numerical tolerance. |
| Latent-source partition | PASS/NEW | Feed-limited test requires body + ambient latent fractions to close to approximately one. |
| Reference generator | PASS/UPDATED | Explicit feed-limited CSV added to generated package. |
| CI definition | PASS/UPDATED | New feed-limited model and generated artifact are exercised. |
| Previously verified computational integration | PASS | `model-tests` #231 succeeded at SHA `7f015b8e1b0278f29b545f41d24674b5a394ee79`. |
| Current feed-limited integration | CHECK | New code/tests/generator/CI are committed; record the new passing run before declaring this integration verified. |

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

Current E3c roles:

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

## E. Experimental readiness

| Item | Status | Audit note |
|---|---|---|
| B0/B2/B3/B4 controls | PASS | Defined. |
| Primary environment | PASS | 35 °C / 70% RH / 150 g/h / nominal still air / 34 °C artificial skin. |
| Primary endpoint | PASS | Heater-power difference. |
| Water balance | PASS | >=95% target. |
| E3/E3b | PASS/PLANNED | Pitch/boundary-layer and hierarchical access tests defined. |
| E3c | PASS/UPDATED | D1/O1/O2a/O2b/O3 defined with `F` plus absolute-transfer metrics. |
| E4a feed transition | PASS/NEW | Feed sweep plus visible/derived wetness comparison defined. |
| E4 humidity | PASS/PLANNED | Supply-limit classification included. |
| E6 hot ambient | PASS/UPDATED | Positive evaporation with negative body cooling is an explicit failure mode. |
| Physical data | **MISSING** | No bench experiment executed yet. |
| Exact hardware/calibration budget | PARTIAL | Still required before a PASS-quality physical run. |

## F. Public-release readiness

| Item | Status |
|---|---|
| Public GitHub repository | PASS |
| Apache-2.0 | PASS |
| Integrated technical disclosure | PASS / development |
| Concrete embodiment matrix | PASS / development |
| Reproducible model stack | PASS / screening |
| Experimental protocols | PASS / planned |
| Authoritative patent-office claim mapping | OPEN |
| Physical evidence | MISSING |
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
- [x] regression energy/feed closure and hot-ambient sign tests;
- [x] reference-generator / CI definition integration;
- [x] E4a physical feed-transition protocol;
- [x] synchronize README/current-results with the new model;
- [ ] confirm new feed-limited integration CI passes at a recorded SHA;
- [ ] synchronize roadmap/changelog/master experiment plan/PR narrative.

### P1 — model strengthening

- [x] axial diffusion + distributed lateral vapor renewal;
- [x] low-order open-valley heat/vapor/wet-wall coupling;
- [x] explicit liquid-feed-limited homogenized solution;
- [x] ordinary Lewis/Chilton–Colburn-style coupling comparison;
- [ ] resolve wet and dry patches spatially rather than through one homogenized `beta`;
- [ ] predict lateral exchange from geometry-resolved 2-D/3-D natural convection/cross-flow;
- [ ] re-test lumped-model multi-equilibrium behavior under improved external-flow treatment;
- [ ] sensitivity to Nu/Sh, compression, opening losses, radiation and external drift.

### P2 — physical evidence

- [ ] E1 B0 vs B4;
- [ ] E2 ablation;
- [ ] E3/E3b;
- [ ] E3c D1/O1/O2a/O2b/O3;
- [ ] E4a feed-limit / wetness transition;
- [ ] E4 humidity boundary;
- [ ] E6 hot-ambient shielding / sensible-heat penalty;
- [ ] publish raw data, calibration metadata, uncertainty and negative results.

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
5. are nonlinear branch choices explicit?
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
17. is any large inferred `R` reported more precisely than T/RH uncertainty supports?

If any answer is unclear, keep the item open.