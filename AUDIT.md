# Repository Audit

Audit date: 2026-08-19  
Branch audited: `agent/initial-research-disclosure`

## Overall assessment

The repository now has a coherent technical disclosure, explicit design variants, reproducible low-order model source, regression tests, reference numerical data, and a staged physical experiment plan. It is **not yet a finished stable release**.

The most important audit finding was numerical: the nonlinear passive heat/mass model can have multiple stable equilibria. Earlier exploratory calculations sometimes selected the most-cooling root, creating an overly optimistic single-value exchange threshold. The repository model has been corrected to expose all stable roots and distinguish warm/conservative and cool/optimistic branches.

Remaining high-priority gaps are verified patent mapping, CI execution on the PR, higher-fidelity/sensitivity models, and physical bench data.

## A. Technical coherence

| Item | Status | Audit note |
|---|---|---|
| Core architecture defined | PASS | Passive directional-liquid transport + heat spreading + capillary delivery + exterior evaporation is consistent. |
| Numbered architecture | PASS | `docs/architecture.md` defines functional layers and transport paths. |
| Concrete complete embodiments | PASS | `docs/embodiment-matrix.md` records 16 implementation stacks and cross-combinations. |
| Design-history consistency | PASS | `docs/design-history.md` separates retained, optional, and deprecated branches. |
| Fan requirement | PASS | Fan is optional, not part of the primary architecture. |
| MOF/sorbent role | PASS | Optional secondary embodiment only. |
| Salt physics | PASS | Water evaporation and nonvolatile salt transport are separated; salt evaporation is explicitly rejected. |
| Water/salt model specification | PASS/PARTIAL | Governing two-species/phase specification exists; numerical implementation still pending. |
| Hot-ambient reversal risk | PASS | Dry high-conductivity exterior heat pickup and shielding embodiments are included. |
| Apparel/exterior design | PASS | Low-profile ribs, 3D knit, lamellae, pleats, pile, and pattern-as-function embodiments are explicit. |
| Simulation vs measurement labels | PASS | No physical garment result is currently claimed. |

## B. Reproducibility

| Item | Status | Audit note |
|---|---|---|
| Governing equations | PASS | Current low-order heat/mass model documented. |
| Variable definitions and units | PASS | Included in `models/governing-equations.md` and water/salt model. |
| Runnable source file present | PASS | `simulations/passive_rib_screen.py`. |
| Dependencies | PASS | `requirements.txt` and `requirements-dev.txt`. |
| Multi-equilibrium handling | PASS | All stable roots exposed; explicit selection policy required. |
| Unit/regression tests | PASS/PENDING CI | Tests include vapor-pressure, geometry, control equilibrium, and multi-root regression. |
| CI workflow | PASS/PENDING RUN | GitHub Actions workflow is defined; verify on PR. |
| Reference output CSV | PASS | `data/reference_branch_map_35C_70RH_150gph.csv`. |
| Consolidated numerical-results record | PASS | `docs/current-results.md`. |
| Figure regeneration | MISSING | Add plotting script after branch-map output is generated directly by repository code. |
| 2D heat-spreader source | MISSING | Earlier results are recorded, consolidated source still needed. |

## C. Numerical-model audit

| Item | Status | Audit note |
|---|---|---|
| Single `M` threshold accepted? | NO | Earlier `M ~2.5–3.5` +10 W values are not treated as robust thresholds. |
| Multiple stable roots detected? | YES | Present model exhibits coexisting stable branches near the transition. |
| Root selection visible? | YES | Warm and cool policies are explicit. |
| Physical hysteresis established? | NO | Multi-root behavior may be a low-order-model artifact and requires experiment/higher-fidelity analysis. |
| Conservative interpretation | PASS | README/current-results no longer present a single `M` as validated design criterion. |

## D. Experimental readiness

| Item | Status | Audit note |
|---|---|---|
| Control sample defined | PASS | B0 flat fast-dry textile. |
| Integrated sample defined | PASS | B4. |
| Ablation controls | PASS | B2/B3/B4. |
| Primary condition | PASS | 35 °C / 70% RH / 150 g/h / nominal still air / 34 °C artificial skin. |
| Primary endpoint | PASS | Heater-power difference at equal water input. |
| PASS/FAIL rule | PASS | >=10 W provisional PASS; <5 W FAIL for future physical test. |
| Water balance | PASS | >=95% closure target. |
| Exterior `alpha` identification | PASS/PROTOCOL | `docs/accessibility-identification.md` defines geometry/RH profiling method. |
| Uncertainty plan | PARTIAL | Categories defined; exact instruments/calibration and propagation pending. |
| Physical data | MISSING | No bench measurements yet. |

## E. Prior-art readiness

| Item | Status | Audit note |
|---|---|---|
| i-Cool heat conduction + sweat transport | PASS | Explicitly acknowledged as close prior art. |
| Directional liquid transport | PASS | 2020 Science Advances work recorded. |
| Humidity-responsive ventilation | PASS | 2021 Science Advances work recorded. |
| 2026 sweat-pumping cooling fabric | PASS | Recorded. |
| Patent landscape | MISSING | Verify publication numbers, priority dates, independent claims, and family members. |
| 3D rib/fin textile search | MISSING | Dedicated literature/patent search needed. |
| Selection/combination escape routes | PASS/PARTIAL | Concrete embodiment matrix added; still needs patent-claim-oriented review. |

## F. Public-release readiness

| Item | Status | Audit note |
|---|---|---|
| Public GitHub repository | PASS | Public repository. |
| Apache-2.0 | PASS | Existing `LICENSE`. |
| README | PASS | Updated after numerical audit. |
| Citation metadata | PASS/PARTIAL | Update version/date at stable tag. |
| Changelog | PASS | `CHANGELOG.md`. |
| Stable-release checklist | PASS | `docs/release-checklist.md`. |
| Stable release tag | MISSING | Current work remains a development branch/PR. |
| Persistent archive/DOI | MISSING | Do after stable release audit. |
| SHA-256 release manifest | MISSING | Generate for frozen release bundle. |

## G. Remaining queue

### P0 — before stable release

- [x] Concrete embodiment matrix.
- [x] Current quantitative-results summary.
- [x] Reference branch-map CSV.
- [x] Automated model tests/CI definition.
- [x] Stable-release checklist and changelog.
- [x] Numbered architecture schematic.
- [x] Correct simulation/measurement labeling.
- [ ] Verify patent landscape entries from authoritative patent records.
- [ ] Confirm CI passes on the exact release candidate.
- [ ] Generate reference CSV/figures directly from the release commit and record commit SHA.

### P1 — technical strengthening

- [ ] Add consolidated 2D anisotropic heat-spreader source model.
- [ ] Implement the water/salt transport numerical model specified in `models/water-salt-transport.md`.
- [ ] Add high-humidity sensitivity/uncertainty study.
- [x] Add exterior boundary-layer/accessibility identification method.
- [ ] Investigate whether multi-equilibrium behavior survives a better natural-convection/boundary-layer model.

### P2 — physical evidence

- [ ] Execute E1 direct comparison.
- [ ] Execute E2 ablation.
- [ ] Execute E3 rib-pitch/accessibility test.
- [ ] Publish raw data, calibration metadata, analysis, and negative results.

## H. Audit rule going forward

Every significant update should answer:

1. Is this statement a **measurement**, **simulation**, **inference**, or **hypothesis**?
2. Can another person reproduce it from the repository?
3. Does it conflict with an earlier statement or deprecated branch?
4. Does known prior art already disclose the broad idea?
5. If a nonlinear model has multiple solutions, is branch selection explicit?

If an answer is unclear, keep the item open rather than silently treating it as complete.
