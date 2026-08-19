# Repository Audit

Audit date: 2026-08-19  
Branch audited: `agent/initial-research-disclosure`

## Overall assessment

The branch contains a coherent technical disclosure, explicit implementation variants, **nine executable screening/sensitivity/identification modules**, regression tests, a reproducible output generator, prior-art working notes, and staged physical experiment protocols.

It remains a development branch, not a frozen stable release, and it contains **no physical garment-performance measurements yet**.

Six numerical/analytic audit findings currently dominate the research plan:

1. the low-order nonlinear passive heat/mass model can contain multiple stable equilibria, so earlier single-value `M` cooling thresholds are not treated as validated criteria;
2. the E3 periodic 2-D diffusion screen shows that dense wet micro-ribs can share one stagnant humidity layer, making near-surface air renewal at least as important as geometric rib area;
3. sensible convective heat transfer and vapor mass transfer are modeled with independent multipliers (`M_h`, `M_m`) rather than assigning one multiplier to both mechanisms;
4. moist-air buoyancy can reverse corridor flow direction because evaporative cooling increases air density while humidification lowers it;
5. the self-consistent 1-D end-renewed corridor model shows that nonzero buoyancy flow and even large axial Péclet number do not guarantee useful vapor renewal: long covered channels can remain nearly saturated;
6. the open-valley conductance target shows that preserving a large fraction of wet-wall vapor driving force requires ambient-renewal conductance comparable to or larger than wet-surface vapor conductance, and that exact large inferred `R` values become measurement-ill-conditioned.

The current preferred exterior is therefore hierarchical and laterally open: wet microstructures for local evaporation area plus open valleys, cross-openings, short segments, spacer paths, or discontinuous fields that remain exposed to ambient air along more than just two channel ends.

## A. Technical coherence

| Item | Status | Audit note |
|---|---|---|
| Core passive architecture | PASS | Directional liquid transport + heat spreading + capillary delivery + exterior evaporation remains consistent. |
| Whole-body/routed heat spreading | PASS | Continuous, anisotropic, mesh, serpentine, island-bridge and redundant paths documented. |
| Exterior geometry families | PASS | Ribs, fins, 3D knit, pile, lamellae, pleats and related structures explicit. |
| Hierarchical air-renewal exterior | PASS | E17 plus E18–E21 cover broad hierarchy, open valleys, segmentation/islands, and covered/end-renewed comparison channels. |
| Sensible/vapor exchange separation | PASS | `M_h` and `M_m` separated; E3 maps only to vapor side. |
| Corridor buoyancy direction | PASS/SCREEN | Up/down/near-neutral tendency derived rather than assumed. |
| Self-consistent covered corridor | PASS/SCREEN | Signed velocity + wet-wall T + channel T/RH solved for an end-renewed rectangular-duct limit. |
| Open-valley renewal target | PASS/ANALYTIC | Required/inferred conductance ratio `R` and retained driving-force `F` explicit; geometry-specific `k_a` remains unknown. |
| Laterally open valley transport physics | OPEN | Distributed lateral ambient exchange and axial diffusion/advection-diffusion are not yet solved from geometry. |
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
| Coupled passive heat/mass model | PASS | `simulations/passive_rib_screen.py`. |
| Split heat/vapor model | PASS | `simulations/split_heat_mass_screen.py`. |
| Deterministic uncertainty sweep | PASS | `simulations/split_transfer_sensitivity.py`. |
| Periodic rib diffusion model | PASS | `simulations/rib_diffusion_screen.py`. |
| Prescribed-state corridor buoyancy | PASS/SCREEN | `simulations/corridor_buoyancy_screen.py`. |
| Self-consistent corridor model | PASS | `simulations/self_consistent_corridor_1d.py`. |
| Open-valley renewal target/identification | PASS | `simulations/open_valley_exchange_target.py`. |
| 2-D heat-spreader model | PASS | `simulations/heat_spreader_2d.py`. |
| Water/salt model | PASS | `simulations/water_salt_1d.py`. |
| Regression tests | PASS | Includes multi-root, split-transfer, E3, corridor, open-valley inversion, heat-spreader and salt checks. |
| E3 grid convergence | PASS/SCREEN | 24 nodes/pitch differs by ~0.62% from the 48-node screened reference. |
| Reference generator | PASS | Includes self-consistent corridor and open-valley renewal-target CSVs plus metadata/SHA-256. |
| CI definition | PASS | Current models/tests/reference outputs are exercised by GitHub Actions. |
| Current verified code integration | **PASS** | GitHub Actions `model-tests` **#183** passed at SHA `1b052ecc2b31f9719a80852eefc58204e533e5a9`. |
| Documentation commits after code integration | INFO | Later protocol/audit/docs commits do not change the verified numerical core; they can trigger additional CI runs. |

## C. Numerical / analytic model audit

### C1 — nonlinear equilibrium branches

- Historical single-value `M` thresholds are screening references only.
- Current passive models expose all stable roots.
- Any future single-number comparison must state root-selection policy.
- Physical reality of multi-equilibrium behavior remains open.

### C2 — E3 boundary-layer interference

For `h=2.5 mm`, structured-panel coverage `f=0.65`:

| renewal gap above tips | p=0.8 mm | p=1.0 mm | p=1.5 mm |
|---:|---:|---:|---:|
| 0.5 mm | 3.785 | 3.548 | 3.098 |
| 1.0 mm | 2.481 | 2.400 | 2.229 |
| 5.0 mm | 1.312 | 1.304 | 1.286 |

Values are whole-area vapor mass-transfer multipliers, not cooling wattages.

Conclusion: geometric area alone is insufficient; a hierarchical micro+macro exterior is a testable hypothesis, not yet a measured result.

### C3 — split sensible/vapor transfer

The split model uses:

- `M_h`: sensible convective heat-transfer multiplier;
- `M_m`: vapor mass-transfer multiplier;
- `h_rad`: independent radiative exchange.

When `M_h=M_m=M`, the split model reproduces the older coupled model as a regression-tested special case.

Hot ambient air can make larger `M_h` adverse even when larger `M_m` helps evaporation.

### C4 — deterministic model-form sensitivity

`simulations/split_transfer_sensitivity.py` sweeps RH, `U_body`, `h_rad`, `M_h`, and `M_m`.

Grid fractions are not probabilities or confidence intervals. Absolute garment cooling wattage remains **FORM-UNCERTAIN**.

### C5 — thermo-solutal corridor buoyancy

The prescribed-state model shows that a wet vertical corridor can tend upward, downward, or near-neutral. At 35 °C / 70% RH ambient, a screened neutral-density state lies near 34 °C / ~90% RH.

### C6 — self-consistent end-renewed rectangular corridor

Selected 35 °C / 70% RH / 100 mm results:

| width × depth | velocity | Pe_m | mean RH | wet-wall body heat flux |
|---|---:|---:|---:|---:|
| 3 × 2 mm | +0.228 mm/s | 0.81 | ~100.0% | +0.10 W/m² |
| 6 × 3 mm | +0.594 mm/s | 2.12 | ~99.99% | +0.40 W/m² |
| 10 × 5 mm | +1.60 mm/s | 5.70 | ~99.92% | +1.81 W/m² |

For 10 × 5 × 100 mm:

- 35 °C / 50% RH: +4.82 mm/s, `Pe_m≈17.2`, ~+9.94 W/m²;
- 35 °C / 85% RH: -1.01 mm/s, flow reversal;
- 40 °C / 70% RH: -14.94 mm/s, **~−1.67 W/m²** wet-wall body heat flux.

The code reports mass-transfer NTU and

\[
\Phi(NTU_m)=\frac{1-e^{-NTU_m}}{NTU_m}
\]

as vapor-driving-force retention. This prevents large axial `Pe_m` from being misread as proof of useful renewal.

Conclusion: do not depend on long covered/end-renewed passive chimneys.

### C7 — open-valley renewal target and measurement identification

Define

\[
R=G_a/G_w
\]

where `G_a` is local valley-to-ambient renewal conductance and `G_w` is wet-surface-to-valley vapor conductance.

The retained wet-wall driving-force fraction is

\[
F=\frac{R}{1+R}.
\]

Required ratios:

| `F` | required `R` |
|---:|---:|
| 0.50 | 1 |
| 0.80 | 4 |
| 0.90 | 9 |
| 0.95 | 19 |

The model also identifies

\[
\theta=\frac{\rho_{v,valley}-\rho_{v,\infty}}{\rho_{v,sat}(T_s)-\rho_{v,\infty}},
\quad F=1-\theta,
\quad R=\frac{1-\theta}{\theta}
\]

from measured local T/RH and wet-surface temperature.

A hypothetical uncertainty screen using 1σ values of 0.2 °C for temperatures and 1 RH percentage point found that exact large `R` becomes poorly conditioned: for true `R=9`, the simulated 5th–95th percentile identified range was roughly 3.8–50. Therefore **`F`/`theta` is the primary mechanism metric and `R` is secondary**.

This analytic model states a target and an identification method; it does not predict `G_a` from valley geometry.

## D. Experimental readiness

| Item | Status | Audit note |
|---|---|---|
| B0 flat control | PASS | Defined. |
| B2/B3/B4 ablation | PASS | Defined. |
| Primary condition | PASS | 35 °C / 70% RH / 150 g/h / nominal still air / 34 °C artificial skin. |
| Primary endpoint | PASS | Heater-power difference at equal liquid feed. |
| Water balance | PASS | >=95% closure target. |
| E3 micro-rib pitch plan | PASS | Defined. |
| E3b hierarchical air-renewal plan | PASS | Signed flow and orientation controls defined. |
| E3c open-vs-covered validation | PASS | D1/O1/O2/O3 defined. |
| T/RH-based renewal identification | PASS/NEW | E3c now calculates `theta`, primary `F`, and conditional `R`. |
| Measurement-uncertainty policy | PASS/NEW | High `R` point estimates are not over-interpreted; `F` is primary. |
| Split heat/vapor identification | PLANNED/PARTIAL | Exact inverse identification of `M_h`/`M_m` remains open. |
| Corridor flow-direction measurement | PLANNED | Signed flow classification required. |
| Physical data | MISSING | No bench experiment has yet been executed. |
| Exact instrument/calibration list | PARTIAL | Hardware-specific uncertainty budget remains open. |

## E. Prior-art readiness

| Item | Status | Audit note |
|---|---|---|
| Directional sweat transport | PASS | Acknowledged. |
| Heat-conductive + sweat-transport textiles | PASS | Close adjacent work acknowledged. |
| Capillary exterior ribs/walls | PASS/PARTIAL | Close patent family identified; authoritative claim mapping still needed. |
| 3-D spacer-knit moisture/evaporation | PASS/PARTIAL | Relevant families recorded. |
| Fan/sorbent cooling garments | PASS/PARTIAL | Relevant families recorded. |
| Concrete implementation combinations | PASS | E18 open valleys, E19 segmentation, E20 islands, E21 covered channels explicit. |
| Authoritative patent-office verification | OPEN | Highest-priority legal-strengthening item before stable release. |

## F. Public-release readiness

| Item | Status | Audit note |
|---|---|---|
| Public GitHub repository | PASS | Repository is public. |
| Apache-2.0 | PASS | `LICENSE`. |
| README / technical disclosure / embodiment matrix | PASS | Current design family and alternatives are explicit. |
| Current-results / roadmap / experiment plan | PASS | Synced through self-consistent corridor direction. |
| Open-valley renewal target document | PASS/NEW | `docs/open-valley-renewal-target.md`. |
| E3c protocol | PASS | Uses vapor-density-corrected `F/R` identification. |
| Draft PR narrative | PASS | PR #1 includes current model/design/verification state. |
| Citation metadata | PASS/PARTIAL | Update at stable version/tag. |
| Reproducible generator + SHA | PASS | Open-valley targets included. |
| Stable tag | MISSING | Development branch only. |
| Persistent archive / DOI | MISSING | Do after stable-release audit. |
| Frozen release artifact manifest | MISSING | Generate from exact final commit. |

## G. Remaining queue

### P0 — current development-branch quality

- [x] E3 diffusion/convergence.
- [x] E3b hierarchy protocol.
- [x] split sensible/vapor model.
- [x] deterministic model-form sensitivity.
- [x] prescribed-state corridor buoyancy.
- [x] self-consistent covered/end-renewed corridor model + tests.
- [x] E3c open-vs-covered protocol.
- [x] E18–E21 explicit ambient-access embodiments.
- [x] open-valley renewal target + measurement inversion + tests.
- [x] reference generator/CI integration for the open-valley target.
- [x] CI verification: `model-tests` #183 PASS at `1b052ecc2b31f9719a80852eefc58204e533e5a9`.
- [x] PR narrative synchronized.

**P0 status: complete for the current development stage.**

### P1 — model strengthening

- [x] Solve covered/end-renewed corridor T/RH and buoyancy/friction self-consistently.
- [x] State measurable lateral-renewal conductance requirements without inventing a geometry-specific coefficient.
- [ ] Predict distributed lateral ambient exchange for an open exterior valley from geometry/flow.
- [ ] Add axial diffusion for low-Pe corridors or solve 2-D advection-diffusion.
- [ ] Constrain physical `M_h`/`M_m` coupling from improved external-flow physics.
- [ ] Re-test nonlinear multi-equilibrium behavior with improved boundary-layer treatment.
- [ ] Add sensitivity to Nu/Sh, entrance losses, opening losses, compression, and external drift.

### P2 — physical evidence

- [ ] E1 B0 vs B4.
- [ ] E2 ablation.
- [ ] E3/E3b rib/accessibility/hierarchical comparison.
- [ ] E3c covered vs open/segmented/island validation.
- [ ] E4 humidity boundary.
- [ ] Measure T/RH/flow with enough accuracy to separate vapor renewal from sensible heat effects.
- [ ] Publish raw data, calibration metadata, analysis, and negative results.

### P3 — stable publication

- [ ] Verify closest patent families/claims from authoritative patent-office sources.
- [ ] Freeze technical disclosure at one exact commit.
- [ ] Regenerate all reference outputs and SHA-256 manifest at that commit.
- [ ] Update `CITATION.cff`, version/date and changelog.
- [ ] Tag stable release.
- [ ] Create persistent public archive/DOI without replacing the original record.

## H. Audit rule going forward

Every significant update must answer:

1. Is the statement a **measurement**, **simulation**, **analytic screen**, **inference**, or **hypothesis**?
2. Can another person reproduce it from repository code/data?
3. Does it contradict or supersede an earlier result?
4. Does known prior art already disclose the broad mechanism?
5. If a nonlinear model has multiple solutions, is branch selection explicit?
6. If added geometric area is claimed to help, is the air/vapor access mechanism explicit?
7. Is a vapor-transfer result being incorrectly reused as a sensible-heat-transfer result?
8. Is an uncertainty-grid fraction being mislabeled as a probability?
9. Is passive corridor flow direction assumed instead of derived or measured?
10. Is axial Péclet number being mistaken for proof that useful vapor driving force remains?
11. Is a covered/end-renewed corridor model being generalized incorrectly to a laterally open valley?
12. Is a large inferred `R` being reported more precisely than the T/RH uncertainty supports?

If any answer is unclear, keep the item open rather than silently marking it complete.
