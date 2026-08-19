# Repository Audit

Audit date: 2026-08-19  
Branch audited: `agent/initial-research-disclosure`

## Overall assessment

The branch contains a coherent technical disclosure, explicit implementation variants, **seven executable screening/sensitivity modules**, regression tests, a reproducible output generator, prior-art working notes, and staged physical experiment protocols.

It is still a development branch, not a frozen stable release, and it contains **no physical garment-performance measurements yet**.

Four numerical audit findings currently dominate the research plan:

1. the low-order nonlinear passive heat/mass model can contain multiple stable equilibria, so earlier single-value `M` cooling thresholds are not treated as validated criteria;
2. the E3 periodic 2-D diffusion screen shows that dense wet micro-ribs can share one stagnant humidity layer, making near-surface air renewal at least as important as geometric rib area;
3. sensible convective heat transfer and vapor mass transfer are now modeled with independent multipliers (`M_h`, `M_m`) rather than automatically assigning one multiplier to both mechanisms;
4. the first moist-air corridor buoyancy screen shows that a vertical wet channel does **not** guarantee beneficial upward chimney flow: evaporative cooling increases air density while humidification reduces it, so the flow tendency can reverse or become near-neutral.

The current preferred exterior is therefore hierarchical: wet microstructures for local evaporation area plus larger open corridors/valleys/spacer paths for passive or motion-assisted air renewal. The thermal and flow consequences of those corridors must be solved together rather than assumed.

## A. Technical coherence

| Item | Status | Audit note |
|---|---|---|
| Core passive architecture | PASS | Directional liquid transport + heat spreading + capillary delivery + exterior evaporation remains consistent. |
| Whole-body/routed heat spreading | PASS | Continuous, anisotropic, mesh, serpentine, island-bridge and redundant paths documented. |
| Exterior geometry families | PASS | Ribs, fins, 3D knit, pile, lamellae, pleats and related structures explicit. |
| Hierarchical air-renewal exterior | PASS | E17 and E3b make microstructure + macro corridor combinations explicit. |
| Sensible/vapor exchange separation | PASS | `M_h` and `M_m` separated in executable model; E3 maps only to vapor side. |
| Corridor buoyancy direction | PASS/SCREEN | Up/down/near-neutral tendency now screened from moist-air density; channel state is still prescribed. |
| Hot-ambient dry-side risk | PASS | Stronger sensible exchange may increase inward heat pickup; dry conductive regions may require shielding/thermal isolation. |
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
| Moist-air corridor buoyancy model | PASS/SCREEN | `simulations/corridor_buoyancy_screen.py`; prescribed channel T/RH, laminar slot-friction screen. |
| 2-D heat-spreader model | PASS | `simulations/heat_spreader_2d.py`. |
| Water/salt mass-balance model | PASS | `simulations/water_salt_1d.py`. |
| Regression tests | PASS | Split-model, sensitivity-grid, E3, heat-spreader, salt, and corridor tests exist. |
| Grid convergence | PASS/SCREEN | E3 reference case differs by about 0.62% between 24 nodes/pitch and the 48-node screened result. |
| Reference generator | PASS | Split-transfer, sensitivity, E3, corridor, heat-spreader and salt outputs are included with metadata/SHA generation. |
| CI definition | PASS | CI runs all current model demos/tests and checks generated reference artifacts. |
| Flow-model integration CI | PASS | GitHub Actions `model-tests` run #137 completed successfully at computational head `0ff7bad704f61ba45d0897ae5dbcc6c6e98882da`. |
| Post-audit documentation head | INFO | This audit update itself creates a newer documentation commit and may trigger a new CI run; run #137 is the verified computational integration point. |

## C. Numerical-model audit

### C1 — nonlinear equilibrium branches

- Earlier single-value thresholds such as `M ~ 2.5–3.5` for +10 W are retained only as historical screening references.
- The current passive models expose all stable roots.
- Any future single-number comparison must state root-selection policy.
- Whether the multi-equilibrium behavior is physical or a low-order natural-convection artifact remains open.

### C2 — E3 boundary-layer interference

E3 fixes one idealized refreshed-air plane above periodic wet ribs and solves steady vapor diffusion.

For `h=2.5 mm`, structured-panel coverage `f=0.65`:

| renewal gap above tips | p=0.8 mm | p=1.0 mm | p=1.5 mm |
|---:|---:|---:|---:|
| 0.5 mm | 3.785 | 3.548 | 3.098 |
| 1.0 mm | 2.481 | 2.400 | 2.229 |
| 5.0 mm | 1.312 | 1.304 | 1.286 |

Values are whole-area **vapor mass-transfer multipliers**, not cooling wattages.

Audit interpretation:

- geometric area alone is insufficient;
- pitch refinement has weak benefit once the whole field lies under a several-millimeter stagnant humidity layer;
- the idealized air-renewal boundary dominates numerical grid error;
- a hierarchical micro+macro exterior should be physically tested.

### C3 — split sensible/vapor transfer

The split model uses:

- `M_h`: sensible convective heat-transfer multiplier;
- `M_m`: vapor mass-transfer multiplier;
- `h_rad`: independent linearized radiative exchange coefficient.

Regression rule: when `M_h = M_m = M` and all other parameters match, the split solver must reproduce the older coupled-multiplier model. This preserves the older model as a special case while avoiding the assumption that an E3 vapor multiplier must also multiply sensible convection.

This is especially important when ambient air is hotter than the wet exterior: increasing `M_h` can increase inward sensible heat pickup while increasing `M_m` may still increase latent evaporation.

### C4 — deterministic model-form sensitivity

`simulations/split_transfer_sensitivity.py` sweeps predeclared ranges in RH, `U_body`, `h_rad`, `M_h`, and `M_m`.

Fractions reported by the script are **fractions of the deterministic screening grid**, not probabilities, reliabilities, or confidence intervals.

Current classification of absolute garment cooling wattage: **FORM-UNCERTAIN** until external-flow/boundary-layer treatment and bench data improve.

### C5 — thermo-solutal corridor buoyancy

`simulations/corridor_buoyancy_screen.py` is the first explicit air-renewal mechanism model. It balances a moist-air density head against fully developed laminar wide-slot friction using a prescribed mean channel temperature and RH.

For the common 35 °C / 70% RH ambient screen, the model places the neutral-density state near 34 °C at roughly 90% RH. This is a screening result, not an experimental threshold.

Audit interpretation:

- a cooler saturated channel can remain denser than hot ambient air and tend downward;
- a sufficiently warm/humid channel can become lighter and tend upward;
- vertical grooves therefore cannot be assumed to produce one-way beneficial chimney flow;
- corridor orientation and openings should tolerate weak, reversed, externally driven, and motion-assisted flow;
- the next model must solve channel temperature, humidity, and flow self-consistently.

## D. Experimental readiness

| Item | Status | Audit note |
|---|---|---|
| B0 flat control | PASS | Defined. |
| B2/B3/B4 ablation | PASS | Defined. |
| Primary condition | PASS | 35 °C / 70% RH / 150 g/h / nominal still air / 34 °C artificial skin. |
| Primary endpoint | PASS | Heater-power difference at equal liquid feed. |
| Water balance | PASS | >=95% closure target. |
| E3 micro-rib pitch plan | PASS | Original accessibility experiment defined. |
| E3b hierarchical air-renewal plan | PASS | Micro-rib-only versus micro+macro corridor architectures defined. |
| Near-surface RH profile | PASS | E3b includes 0.5/1/2/5/10/20 mm sampling heights. |
| Split heat/vapor identification | PLANNED/PARTIAL | Master plan now requires surface/air temperature with RH so vapor renewal is not conflated with sensible exchange. Exact inverse-identification method remains open. |
| Corridor flow-direction measurement | PLANNED | E3b now requires signed upward/downward/reversing/below-resolution classification, plus vertical/horizontal/inverted controls where practical. |
| Corridor T/RH profile | PLANNED | E3b includes inlet/mid-height/outlet temperature and RH where sensor intrusion is acceptable. |
| Physical data | MISSING | No bench experiment has yet been executed. |
| Exact instrument/calibration list | PARTIAL | Measurement categories exist; hardware-specific instrument list and uncertainty budget remain open. |

## E. Prior-art readiness

| Item | Status | Audit note |
|---|---|---|
| Directional sweat transport | PASS | Acknowledged. |
| Heat-conductive + sweat-transport textiles | PASS | i-Cool and related work acknowledged as close prior art. |
| Capillary exterior ribs/walls | PASS/PARTIAL | Close patent family identified; authoritative claim mapping still needed. |
| 3-D spacer-knit moisture/evaporation | PASS/PARTIAL | Relevant families recorded. |
| Fan/sorbent cooling garments | PASS/PARTIAL | Relevant prior families recorded. |
| Concrete implementation combinations | PASS | `docs/embodiment-matrix.md`, including hierarchical E17. |
| Authoritative patent-office verification | OPEN | Highest-priority release/legal-strengthening item. |

## F. Public-release readiness

| Item | Status | Audit note |
|---|---|---|
| Public GitHub repository | PASS | Repository is public. |
| Apache-2.0 | PASS | `LICENSE`. |
| README | PASS | Synced with multiple-root, E3, split-transfer, model-form uncertainty, and corridor-flow findings. |
| Current-results summary | PASS | Synced through E3, split transfer, deterministic uncertainty, and corridor-buoyancy findings. |
| Master experiment plan | PASS | Synced with signed corridor-flow and separate sensible/vapor measurement requirements. |
| E3b protocol | PASS | Signed flow, orientation/inversion controls, and flow-mechanism support criterion included. |
| Citation metadata | PASS/PARTIAL | Update at stable version/tag. |
| Reproducible generator + SHA | PASS | Split-transfer, E3, corridor, heat-spreader and salt data included; final release must regenerate at exact release commit. |
| Stable tag | MISSING | Development branch only. |
| Persistent archive / DOI | MISSING | Do after stable release audit. |
| Frozen release artifact manifest | MISSING | Generate from exact final commit. |

## G. Remaining queue

### P0 — current branch / PR quality

- [x] Add E3 periodic diffusion model.
- [x] Add E3 raw screening CSVs.
- [x] Add E3 grid-convergence record.
- [x] Add E3 interpretation document.
- [x] Add E3b physical protocol.
- [x] Add E17 hierarchical exterior embodiment.
- [x] Add E3 regression tests.
- [x] Extend reference generator and CI definition for E3.
- [x] Confirm E3-integrated CI passes.
- [x] Re-audit generated reference package path/CI existence checks.
- [x] Separate sensible heat and vapor-transfer multipliers.
- [x] Add split-model regression equivalence test.
- [x] Add deterministic model-form sensitivity framework and executable sweep.
- [x] Add first moist-air corridor buoyancy screen and regression tests.
- [x] Add corridor outputs to reproducible reference generator and CI artifact checks.
- [x] Confirm flow-model integration CI: run #137 PASS at `0ff7bad704f61ba45d0897ae5dbcc6c6e98882da`.
- [x] Sync top-level README with corridor model/result.
- [x] Sync `docs/current-results.md` with split-transfer and corridor findings.
- [x] Sync master experiment plan with signed-flow and split-transfer measurements.
- [x] Extend E3b with signed-flow, orientation, and inversion controls.

### P1 — model strengthening

- [ ] Couple a better natural-convection / boundary-layer model to E3 rather than prescribing a renewal plane.
- [x] Separate mass-transfer and sensible-heat multipliers explicitly in the thermal model.
- [ ] Investigate whether passive macro corridors can create/maintain near-tip air renewal in a self-consistent flow model. **Initial prescribed-state buoyancy screen complete.**
- [x] Add systematic model-form uncertainty ranges and deterministic sensitivity code.
- [ ] Re-test nonlinear multi-equilibrium behavior with the improved boundary-layer treatment.
- [ ] Use improved external-flow physics to constrain a plausible relationship between `M_h` and `M_m` rather than assuming either equality or total independence.
- [ ] Couple channel heat and water-vapor conservation to buoyancy/friction so channel T/RH are solved rather than prescribed.

### P2 — physical evidence

- [ ] Execute E1 direct B0 vs B4 comparison.
- [ ] Execute E2 ablation.
- [ ] Execute E3/E3b rib/accessibility/hierarchical-air-renewal comparison.
- [ ] Execute humidity boundary test.
- [ ] Measure enough temperature/RH information to estimate vapor and sensible-transfer effects separately.
- [ ] Measure or visualize corridor flow direction under still-air conditions.
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
9. Is a passive corridor flow direction being assumed instead of derived or measured?

If any answer is unclear, keep the item open rather than silently marking it complete.
