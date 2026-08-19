# Repository Audit

Audit date: 2026-08-19  
Branch audited: `agent/initial-research-disclosure`

## Overall assessment

The branch now contains a coherent technical disclosure, explicit implementation variants, **eight executable screening/sensitivity modules**, regression tests, a reproducible output generator, prior-art working notes, and staged physical experiment protocols.

It remains a development branch, not a frozen stable release, and it contains **no physical garment-performance measurements yet**.

Five numerical audit findings currently dominate the research plan:

1. the low-order nonlinear passive heat/mass model can contain multiple stable equilibria, so earlier single-value `M` cooling thresholds are not treated as validated criteria;
2. the E3 periodic 2-D diffusion screen shows that dense wet micro-ribs can share one stagnant humidity layer, making near-surface air renewal at least as important as geometric rib area;
3. sensible convective heat transfer and vapor mass transfer are modeled with independent multipliers (`M_h`, `M_m`) rather than automatically assigning one multiplier to both mechanisms;
4. moist-air buoyancy can reverse corridor flow direction because evaporative cooling increases air density while humidification lowers it;
5. the new self-consistent 1-D end-renewed corridor model shows that **nonzero buoyancy flow and even a moderate/large axial Péclet number do not guarantee useful vapor renewal**: long covered channels can still approach saturation and lose most of their evaporation driving force.

The current preferred exterior is therefore hierarchical and laterally open: wet microstructures for local evaporation area plus open valleys, cross-openings, short segments, spacer paths, or discontinuous fields that remain exposed to ambient air along more than just two channel ends.

## A. Technical coherence

| Item | Status | Audit note |
|---|---|---|
| Core passive architecture | PASS | Directional liquid transport + heat spreading + capillary delivery + exterior evaporation remains consistent. |
| Whole-body/routed heat spreading | PASS | Continuous, anisotropic, mesh, serpentine, island-bridge and redundant paths documented. |
| Exterior geometry families | PASS | Ribs, fins, 3D knit, pile, lamellae, pleats and related structures explicit. |
| Hierarchical air-renewal exterior | PASS/UPDATED | E17/E3b/E3c now distinguish micro-area enhancement from macro/lateral air renewal. |
| Sensible/vapor exchange separation | PASS | `M_h` and `M_m` separated; E3 maps only to vapor side. |
| Corridor buoyancy direction | PASS/SCREEN | Up/down/near-neutral tendency derived from moist-air density rather than assumed. |
| Self-consistent corridor state | PASS/SCREEN | `self_consistent_corridor_1d.py` solves signed velocity + wet-wall T + channel T/RH for a covered/end-renewed rectangular-duct limit. |
| Laterally open valley physics | OPEN | Distributed lateral ambient exchange is not yet solved. E3c is the direct physical test. |
| Hot-ambient dry-side risk | PASS | Stronger air exchange can increase inward sensible heat pickup; shielding/routing remains required. |
| Fan requirement | PASS | Fan remains optional; primary architecture is fanless. |
| MOF/sorbent role | PASS | Secondary optional embodiment only. |
| Salt physics | PASS | Water evaporates; salt vapor flux is zero in garment-temperature models. |
| Apparel integration | PASS | Low-profile textile-like textures and pattern-as-function variants recorded. |
| Simulation vs measurement labeling | PASS | Physical performance is not claimed. |

## B. Reproducibility

| Item | Status | Audit note |
|---|---|---|
| Governing equations | PASS | Heat/mass and water/salt assumptions documented. |
| Coupled passive heat/mass model | PASS | `simulations/passive_rib_screen.py`; retained as reference/special case. |
| Split heat/vapor model | PASS | `simulations/split_heat_mass_screen.py`. |
| Deterministic uncertainty sweep | PASS | `simulations/split_transfer_sensitivity.py`. |
| Periodic rib diffusion model | PASS | `simulations/rib_diffusion_screen.py`. |
| Prescribed-state corridor buoyancy model | PASS/SCREEN | `simulations/corridor_buoyancy_screen.py`. |
| Self-consistent corridor model | PASS/NEW | `simulations/self_consistent_corridor_1d.py`. |
| 2-D heat-spreader model | PASS | `simulations/heat_spreader_2d.py`. |
| Water/salt mass-balance model | PASS | `simulations/water_salt_1d.py`. |
| Regression tests | PASS/UPDATED | New self-consistent corridor tests include Poiseuille resistance, flow reversal, hot-ambient inward heat, low-Pe classification, and segment-length behavior. |
| E3 grid convergence | PASS/SCREEN | 24 nodes/pitch differs by about 0.62% from the 48-node screened result in the reference case. |
| Reference generator | PASS/UPDATED | Self-consistent corridor CSV added to generated reference package. |
| CI definition | PASS/UPDATED | CI runs all current model demos/tests and checks self-consistent corridor output. |
| Previously verified computational integration | PASS | `model-tests` #137 passed at `0ff7bad704f61ba45d0897ae5dbcc6c6e98882da`. |
| Current self-consistent-corridor integration | CHECK | New model/tests/generator are committed; record the new passing run before declaring this integration verified. |

## C. Numerical-model audit

### C1 — nonlinear equilibrium branches

- Earlier single-value thresholds such as `M ~ 2.5–3.5` for +10 W are historical screening references only.
- Current passive models expose all stable roots.
- Any future single-number comparison must state root-selection policy.
- Whether multi-equilibrium behavior is physical or an artifact remains open.

### C2 — E3 boundary-layer interference

For `h=2.5 mm`, structured-panel coverage `f=0.65`:

| renewal gap above tips | p=0.8 mm | p=1.0 mm | p=1.5 mm |
|---:|---:|---:|---:|
| 0.5 mm | 3.785 | 3.548 | 3.098 |
| 1.0 mm | 2.481 | 2.400 | 2.229 |
| 5.0 mm | 1.312 | 1.304 | 1.286 |

Values are whole-area **vapor mass-transfer multipliers**, not cooling wattages.

Audit interpretation:

- geometric area alone is insufficient;
- pitch refinement has weak benefit once the field lies under a several-millimeter stagnant humidity layer;
- the prescribed refreshed-air boundary dominates numerical grid error;
- a hierarchical micro+macro exterior is justified as a testable hypothesis.

### C3 — split sensible/vapor transfer

The split model uses:

- `M_h`: sensible convective heat-transfer multiplier;
- `M_m`: vapor mass-transfer multiplier;
- `h_rad`: independent radiative exchange.

When `M_h = M_m = M`, the split model reproduces the older coupled model as a regression-tested special case.

In hot ambient air, increasing `M_h` can increase inward sensible heat pickup while increasing `M_m` may still improve latent evaporation. Therefore airflow or area enhancement cannot be scored with one exchange multiplier.

### C4 — deterministic model-form sensitivity

`simulations/split_transfer_sensitivity.py` sweeps RH, `U_body`, `h_rad`, `M_h`, and `M_m`.

Reported fractions are deterministic screening-grid fractions, not probabilities or confidence intervals.

Absolute garment cooling wattage remains **FORM-UNCERTAIN** until external-flow physics and bench data improve.

### C5 — prescribed-state thermo-solutal corridor buoyancy

`simulations/corridor_buoyancy_screen.py` balances a moist-air density head against laminar slot friction for prescribed channel T/RH.

For 35 °C / 70% RH ambient, a neutral-density state lies near 34 °C / ~90% RH in the screen.

Therefore a wet vertical corridor can tend upward, downward, or near-neutral; one-way chimney action must not be assumed.

### C6 — self-consistent end-renewed rectangular corridor

`simulations/self_consistent_corridor_1d.py` solves signed velocity, wet-wall temperature, mean/outlet channel T/RH, evaporation, and body-side heat flux for a rectangular covered/end-renewed limit.

Selected 35 °C / 70% RH / 100 mm results:

| width × depth | velocity | Pe_m | mean RH | wet-wall body heat flux |
|---|---:|---:|---:|---:|
| 3 × 2 mm | +0.228 mm/s | 0.81 | ~100.0% | +0.10 W/m² |
| 6 × 3 mm | +0.594 mm/s | 2.12 | ~99.99% | +0.40 W/m² |
| 10 × 5 mm | +1.60 mm/s | 5.70 | ~99.92% | +1.81 W/m² |

For 10 × 5 × 100 mm:

- 35 °C / 50% RH: +4.82 mm/s, `Pe_m≈17.2`, ~+9.94 W/m² wet-wall body heat flux;
- 35 °C / 85% RH: -1.01 mm/s, `Pe_m≈3.59`, flow reversal;
- 40 °C / 70% RH: -14.94 mm/s, `Pe_m≈53.4`, **~−1.67 W/m²** wet-wall body heat flux.

Audit interpretation:

- nonzero velocity is not sufficient;
- axial Péclet number is not sufficient;
- long covered channels can have high `Pe_m` while remaining nearly saturated because mass-transfer NTU is also high;
- a stronger hot-ambient flow can be thermally adverse;
- the design should not depend on long covered/end-renewed chimneys;
- laterally open valleys/cross-openings/segmentation are now the preferred hypothesis.

Important limitation: this model omits distributed lateral ambient exchange and axial diffusion. It is intentionally a covered/end-renewed limiting case, not a prediction for an open garment groove.

## D. Experimental readiness

| Item | Status | Audit note |
|---|---|---|
| B0 flat control | PASS | Defined. |
| B2/B3/B4 ablation | PASS | Defined. |
| Primary condition | PASS | 35 °C / 70% RH / 150 g/h / nominal still air / 34 °C artificial skin. |
| Primary endpoint | PASS | Heater-power difference at equal liquid feed. |
| Water balance | PASS | >=95% closure target. |
| E3 micro-rib pitch plan | PASS | Defined. |
| E3b hierarchical air-renewal plan | PASS | Defined with signed flow and orientation controls. |
| E3c open-vs-covered validation | PASS/NEW | Covered duct, open valley, segmented valley, and discontinuous island variants defined. |
| Near-surface RH profile | PASS | Spatial RH/T measurements required. |
| Split heat/vapor identification | PLANNED/PARTIAL | Surface/air T and RH required; exact inverse-identification method remains open. |
| Corridor flow-direction measurement | PLANNED | Signed flow classification required. |
| Covered-vs-open axial RH profile | PLANNED/NEW | E3c samples inlet/intermediate/outlet positions and open-valley near field. |
| Physical data | MISSING | No bench experiment has yet been executed. |
| Exact instrument/calibration list | PARTIAL | Hardware-specific uncertainty budget remains open. |

## E. Prior-art readiness

| Item | Status | Audit note |
|---|---|---|
| Directional sweat transport | PASS | Acknowledged. |
| Heat-conductive + sweat-transport textiles | PASS | i-Cool and related work acknowledged as close prior art. |
| Capillary exterior ribs/walls | PASS/PARTIAL | Close patent family identified; authoritative claim mapping still needed. |
| 3-D spacer-knit moisture/evaporation | PASS/PARTIAL | Relevant families recorded. |
| Fan/sorbent cooling garments | PASS/PARTIAL | Relevant prior families recorded. |
| Concrete implementation combinations | PASS | `docs/embodiment-matrix.md`, including hierarchical E17. |
| Authoritative patent-office verification | OPEN | Highest-priority legal-strengthening item before stable release. |

## F. Public-release readiness

| Item | Status | Audit note |
|---|---|---|
| Public GitHub repository | PASS | Repository is public. |
| Apache-2.0 | PASS | `LICENSE`. |
| README | PASS/UPDATED | Includes self-consistent corridor findings and open-valley direction. |
| Self-consistent model documentation | PASS/NEW | `docs/self-consistent-corridor-model.md`. |
| Master experiment plan | PASS/UPDATED | E3c added. |
| E3c protocol | PASS/NEW | `experiments/e3c_open_vs_covered_corridors.md`. |
| Citation metadata | PASS/PARTIAL | Update at stable version/tag. |
| Reproducible generator + SHA | PASS/UPDATED | Self-consistent corridor CSV included. |
| Stable tag | MISSING | Development branch only. |
| Persistent archive / DOI | MISSING | Do after stable-release audit. |
| Frozen release artifact manifest | MISSING | Generate from exact final commit. |

## G. Remaining queue

### P0 — current branch / PR quality

- [x] Add E3 periodic diffusion model and convergence record.
- [x] Add E3b hierarchical physical protocol.
- [x] Separate sensible and vapor transfer.
- [x] Add deterministic model-form sensitivity.
- [x] Add prescribed-state moist-air corridor buoyancy screen.
- [x] Add self-consistent 1-D end-renewed corridor model.
- [x] Add self-consistent corridor regression tests.
- [x] Add self-consistent corridor outputs to reference generator and CI definition.
- [x] Add E3c open-vs-covered physical validation protocol.
- [x] Sync README and master experiment plan.
- [ ] Confirm self-consistent-corridor CI passes at a recorded computational SHA.
- [ ] Sync `docs/current-results.md`, simulations README, changelog, and PR body with the new model.

### P1 — model strengthening

- [x] Solve channel T/RH and buoyancy/friction self-consistently for the end-renewed covered-duct limit.
- [ ] Add distributed lateral ambient exchange to represent an open exterior valley.
- [ ] Add axial diffusion for low-Pe corridors or solve the 2-D advection-diffusion problem.
- [ ] Constrain `M_h` and `M_m` from the improved external-flow model rather than assuming equality or complete independence.
- [ ] Re-test nonlinear multi-equilibrium behavior with improved boundary-layer treatment.
- [ ] Add geometry/model-form sensitivity for Nu/Sh and entrance/opening losses.

### P2 — physical evidence

- [ ] Execute E1 direct B0 vs B4 comparison.
- [ ] Execute E2 ablation.
- [ ] Execute E3/E3b rib/accessibility/hierarchical-air-renewal comparison.
- [ ] Execute E3c open-vs-covered/segmented validation.
- [ ] Execute humidity boundary test.
- [ ] Measure enough T/RH and flow information to separate vapor renewal from sensible heat transfer.
- [ ] Publish raw data, calibration metadata, analysis, and negative results.

### P3 — stable publication

- [ ] Verify closest patent families and claims from authoritative patent-office sources.
- [ ] Freeze a consistent technical disclosure at one exact commit.
- [ ] Regenerate all reference outputs and SHA-256 manifest at that commit.
- [ ] Update `CITATION.cff`, version/date and changelog.
- [ ] Tag the stable release.
- [ ] Create a persistent public archive/DOI without replacing the original release record.

## H. Audit rule going forward

Every significant update must answer:

1. Is the statement a **measurement**, **simulation**, **inference**, or **hypothesis**?
2. Can another person reproduce it from repository code/data?
3. Does it contradict or supersede an earlier result?
4. Does known prior art already disclose the broad mechanism?
5. If a nonlinear model has multiple solutions, is branch selection explicit?
6. If added geometric area is claimed to help, is the **air/vapor access mechanism** explicit?
7. Is a vapor-transfer result being incorrectly reused as a sensible-heat-transfer result?
8. Is an uncertainty-grid fraction being mislabeled as a probability?
9. Is passive corridor flow direction assumed instead of derived or measured?
10. Is axial Péclet number being mistaken for proof that the channel retains useful vapor driving force?
11. Is a covered/end-renewed corridor model being incorrectly generalized to a laterally open garment valley?

If any answer is unclear, keep the item open rather than silently marking it complete.
