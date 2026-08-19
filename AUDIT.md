# Repository Audit

Audit date: 2026-08-19  
Branch audited: `agent/initial-research-disclosure`

## Overall assessment

The repository now has a coherent technical disclosure, explicit design variants, three executable screening models, regression tests, a reproducible table/figure generation pipeline, prior-art working notes, and a staged physical experiment plan. It is **not yet a finished stable release**.

The most important numerical audit finding remains that the nonlinear passive heat/mass model can have multiple stable equilibria. Earlier exploratory calculations sometimes selected the most-cooling root, creating an overly optimistic single-value exchange threshold. The repository model now exposes all stable roots and distinguishes warm/conservative and cool/optimistic branches.

GitHub Actions has successfully executed the test suite, all three current model demos, and the reproducible reference-output generator. Remaining high-priority gaps are authoritative patent-family/claim verification, final-release artifact freezing/provenance, higher-fidelity boundary-layer/model-uncertainty work, and physical bench data.

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
| Water/salt model | PASS/PARTIAL | Governing multi-phase specification plus normalized 1D mass-balance screen implemented; pore-scale/kinetic model still open. |
| Hot-ambient reversal risk | PASS | Dry high-conductivity exterior heat pickup and shielding embodiments are included. |
| Apparel/exterior design | PASS | Low-profile ribs, 3D knit, lamellae, pleats, pile, and pattern-as-function embodiments are explicit. |
| Simulation vs measurement labels | PASS | No physical garment result is currently claimed. |

## B. Reproducibility

| Item | Status | Audit note |
|---|---|---|
| Governing equations | PASS | Current low-order heat/mass model documented. |
| Variable definitions and units | PASS | Included in governing and water/salt documents. |
| Passive exterior source | PASS | `simulations/passive_rib_screen.py`. |
| 2D anisotropic heat-spreader source | PASS | `simulations/heat_spreader_2d.py`. |
| Normalized water/salt source | PASS | `simulations/water_salt_1d.py`. |
| Dependencies | PASS | `requirements.txt` and `requirements-dev.txt`. |
| Multi-equilibrium handling | PASS | All stable roots exposed; explicit selection policy required. |
| Unit/regression tests | PASS | Includes vapor-pressure, geometry, equilibrium, multi-root, 2D orientation, and salt-conservation tests. |
| CI workflow | PASS | GitHub Actions completes tests and current model demos. |
| Reproducible output generator | PASS | `simulations/generate_reference_outputs.py` creates CSVs, PNGs, metadata with git commit, and SHA-256 manifest. |
| Reference output CSV | PASS/PARTIAL | Existing branch-map record plus generator; stable-release outputs must be regenerated at the final tag/commit. |
| Consolidated numerical-results record | PASS | `docs/current-results.md`. |
| Figure regeneration | PASS | Plotting/generation pipeline is CI-validated; stable-release figures still need freezing from the release commit. |

## C. Numerical-model audit

| Item | Status | Audit note |
|---|---|---|
| Single `M` threshold accepted? | NO | Earlier `M ~2.5–3.5` +10 W values are not treated as robust thresholds. |
| Multiple stable roots detected? | YES | Present low-order model exhibits coexisting stable branches near the transition. |
| Root selection visible? | YES | Warm and cool policies are explicit. |
| Physical hysteresis established? | NO | Multi-root behavior may be a low-order-model artifact and requires experiment/higher-fidelity analysis. |
| Conservative interpretation | PASS | README/current-results no longer present a single `M` as validated design criterion. |
| 2D anisotropy direction | PASS/MODEL | In the current right-side sink geometry, x-aligned high conductivity routes more body-side heat than the 90°-rotated anisotropy; regression-tested. |
| Salt conservation | PASS/MODEL | Normalized model conserves salt between upstream solids and terminal liquid; no salt vapor flux exists. |
| RH branch sweep | PASS/PARTIAL | Reproducible output generator maps stable branches at 50/70/85% RH; broader coefficient/model-form uncertainty remains open. |

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
| Early sorbent cooling garment + exterior fins | PASS/PARTIAL | JPH04209808A recorded from a public patent index; authoritative office/family verification remains. |
| Fan garment family | PASS/PARTIAL | WO2005/063065 family identified; detailed authoritative claim/family mapping still needed. |
| Ribbed capillary exterior evaporation | PASS/PARTIAL | EP1978836 family identified as highly relevant: capillary textile ribs/walls transport sweat away from skin toward an exterior evaporation web. |
| Wicking evaporative cooling garment | PASS/PARTIAL | US8443463 / US20110283722 family identified: liquid supply + wicking garment + exterior evaporation. |
| 3D spacer-knit outward moisture/evaporation | PASS/PARTIAL | US12209335 / US20240125016 family identified; 3D-knit evaporation media also found outside clothing. |
| Patent working notes | PASS | `docs/patent-notes.md` records close families and design consequences. |
| Selection/combination escape routes | PASS/PARTIAL | Concrete embodiment matrix added; still needs claim-oriented professional review. |

## F. Public-release readiness

| Item | Status | Audit note |
|---|---|---|
| Public GitHub repository | PASS | Public repository. |
| Apache-2.0 | PASS | Existing `LICENSE`. |
| README | PASS | Updated after numerical audit. |
| Citation metadata | PASS/PARTIAL | Update version/date at stable tag. |
| Changelog | PASS | `CHANGELOG.md`. |
| Stable-release checklist | PASS | `docs/release-checklist.md`. |
| Artifact SHA-256 capability | PASS | Reference generator creates a manifest; stable release still needs the frozen final manifest. |
| Stable release tag | MISSING | Current work remains a development branch/draft PR. |
| Persistent archive/DOI | MISSING | Do after stable release audit. |

## G. Remaining queue

### P0 — before stable release

- [x] Concrete embodiment matrix.
- [x] Current quantitative-results summary.
- [x] Reference branch-map CSV.
- [x] Automated model tests/CI definition.
- [x] CI passes for current models and reference-output generator.
- [x] Stable-release checklist and changelog.
- [x] Numbered architecture schematic.
- [x] Correct simulation/measurement labeling.
- [x] Reproducible CSV/figure/SHA generation pipeline.
- [ ] Verify closest patent families/claims from authoritative patent-office records.
- [ ] Regenerate/freeze reference artifacts from the final release commit and record that exact SHA.
- [ ] Update `CITATION.cff`, changelog, and version metadata for the stable tag.

### P1 — technical strengthening

- [x] Add consolidated 2D anisotropic heat-spreader source model.
- [x] Add normalized water/salt mass-balance numerical model with zero salt vapor flux.
- [ ] Add higher-fidelity water/salt pore-scale or cyclic model if experiments justify it.
- [x] Add RH 50/70/85 stable-branch sensitivity generation.
- [ ] Add systematic parameter/model-form uncertainty study.
- [x] Add exterior boundary-layer/accessibility identification method.
- [ ] Investigate whether multi-equilibrium behavior survives a better natural-convection/boundary-layer model.
- [x] Add plotting/regeneration pipeline for quantitative figures.

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
