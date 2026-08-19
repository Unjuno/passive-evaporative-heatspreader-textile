# Repository Audit

Audit date: 2026-08-19  
Branch audited: `agent/initial-research-disclosure`

## Overall assessment

The branch contains a coherent technical disclosure, explicit implementation variants, **six executable screening/sensitivity modules**, regression tests, a reproducible output generator, prior-art working notes, and staged physical experiment protocols.

It is still a development branch, not a frozen stable release, and it contains **no physical garment-performance measurements yet**.

Three numerical audit findings currently dominate the research plan:

1. the low-order nonlinear passive heat/mass model can contain multiple stable equilibria, so earlier single-value `M` cooling thresholds are not treated as validated criteria;
2. the E3 periodic 2-D diffusion screen shows that dense wet micro-ribs can share one stagnant humidity layer, making near-surface air renewal at least as important as geometric rib area;
3. sensible convective heat transfer and vapor mass transfer are now modeled with independent multipliers (`M_h`, `M_m`) rather than automatically assigning one multiplier to both mechanisms.

The current preferred exterior is therefore hierarchical: wet microstructures for local evaporation area plus larger open corridors/valleys/spacer paths for passive or motion-assisted air renewal. The thermal consequence of those corridors must be evaluated separately for sensible heat and vapor transfer.

## A. Technical coherence

| Item | Status | Audit note |
|---|---|---|
| Core passive architecture | PASS | Directional liquid transport + heat spreading + capillary delivery + exterior evaporation remains consistent. |
| Whole-body/routed heat spreading | PASS | Continuous, anisotropic, mesh, serpentine, island-bridge and redundant paths documented. |
| Exterior geometry families | PASS | Ribs, fins, 3D knit, pile, lamellae, pleats and related structures explicit. |
| Hierarchical air-renewal exterior | PASS | E17 and E3b make microstructure + macro corridor combinations explicit. |
| Sensible/vapor exchange separation | PASS/NEW | `M_h` and `M_m` separated in executable model; E3 maps only to vapor side. |
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
| Split heat/vapor model | PASS/NEW | `simulations/split_heat_mass_screen.py`. |
| Deterministic uncertainty sweep | PASS/NEW | `simulations/split_transfer_sensitivity.py`. |
| Periodic rib diffusion model | PASS | `simulations/rib_diffusion_screen.py`. |
| 2-D heat-spreader model | PASS | `simulations/heat_spreader_2d.py`. |
| Water/salt mass-balance model | PASS | `simulations/water_salt_1d.py`. |
| Regression tests | PASS/UPDATED | Split-model equivalence and sensitivity-grid tests added. |
| Grid convergence | PASS/SCREEN | E3 reference case differs by about 0.62% between 24 nodes/pitch and the 48-node screened result. |
| Reference generator | PASS/UPDATED | Split-transfer and deterministic sensitivity CSVs added. |
| CI definition | PASS/UPDATED | CI runs split-transfer/sensitivity demos and checks generated split-transfer artifacts. |
| Last confirmed complete CI before current P1 commits | PASS | PR-triggered `model-tests` run #83 completed successfully at head `468aad136e2e80e588de443920617daf376eb8b7`. |
| Current P1-integrated CI | CHECK AFTER HEAD SETTLES | New commits trigger CI; do not infer success until the run completes. |

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

The new split model uses:

- `M_h`: sensible convective heat-transfer multiplier;
- `M_m`: vapor mass-transfer multiplier;
- `h_rad`: independent linearized radiative exchange coefficient.

Regression rule: when `M_h = M_m = M` and all other parameters match, the split solver must reproduce the older coupled-multiplier model. This preserves the older model as a special case while avoiding the assumption that an E3 vapor multiplier must also multiply sensible convection.

This is especially important when ambient air is hotter than the wet exterior: increasing `M_h` can increase inward sensible heat pickup while increasing `M_m` may still increase latent evaporation.

### C4 — deterministic model-form sensitivity

`simulations/split_transfer_sensitivity.py` sweeps predeclared ranges in:

- RH;
- `U_body`;
- `h_rad`;
- `M_h`;
- `M_m`.

Fractions reported by the script are **fractions of the deterministic screening grid**, not probabilities, reliabilities, or confidence intervals.

Current classification of absolute garment cooling wattage: **FORM-UNCERTAIN** until external-flow/boundary-layer treatment and bench data improve.

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
| Split heat/vapor identification | PARTIAL/NEW | Experiment should measure surface/air temperature with RH so improved vapor renewal is not mistaken for uniformly improved heat transfer. |
| Physical data | MISSING | No bench experiment has yet been executed. |
| Exact instrument/calibration list | PARTIAL | Measurement categories exist; hardware-specific uncertainty budget remains open. |

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
| README | PASS/UPDATED | Split transfer and model-form uncertainty reflected. |
| Citation metadata | PASS/PARTIAL | Update at stable version/tag. |
| Reproducible generator + SHA | PASS/UPDATED | Split-transfer data included; final release must regenerate at exact release commit. |
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
- [x] Confirm E3-integrated CI passes (#83 and prior runs).
- [x] Re-audit generated reference package path/CI existence checks.
- [x] Separate sensible heat and vapor-transfer multipliers.
- [x] Add split-model regression equivalence test.
- [x] Add deterministic model-form sensitivity framework and executable sweep.
- [ ] Confirm current P1-integrated CI after the latest commits settle.

### P1 — model strengthening

- [ ] Couple a better natural-convection / boundary-layer model to E3 rather than prescribing a renewal plane.
- [x] Separate mass-transfer and sensible-heat multipliers explicitly in the thermal model.
- [ ] Investigate whether passive macro corridors can create/maintain near-tip air renewal in 2-D/3-D flow models.
- [x] Add systematic model-form uncertainty ranges and deterministic sensitivity code.
- [ ] Re-test nonlinear multi-equilibrium behavior with the improved boundary-layer treatment.
- [ ] Use improved external-flow physics to constrain a plausible relationship between `M_h` and `M_m` rather than assuming either equality or total independence.

### P2 — physical evidence

- [ ] Execute E1 direct B0 vs B4 comparison.
- [ ] Execute E2 ablation.
- [ ] Execute E3/E3b rib/accessibility/hierarchical-air-renewal comparison.
- [ ] Execute humidity boundary test.
- [ ] Measure enough temperature/RH information to estimate vapor and sensible-transfer effects separately.
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

If any answer is unclear, keep the item open rather than silently marking it complete.
