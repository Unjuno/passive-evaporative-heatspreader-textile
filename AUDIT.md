# Repository Audit

Audit date: 2026-08-20  
Branch: `agent/initial-research-disclosure`

## Overall assessment

The repository is **technically mature enough to stop exploratory modeling and move to release preparation** for the present computational/public technical record.

It contains:

- an integrated technical disclosure;
- an explicit embodiment matrix;
- a canonical current-results record;
- **45 indexed executable screening/sensitivity/audit/virtual-prototype models** plus the reference-output generator;
- regression tests and committed reference CSVs;
- five dedicated GitHub Actions workflows;
- prior-art/patent working notes;
- future physical-validation protocols;
- a research-freeze/change-control policy.

The project remains a **virtual/computational prototype only**. No physical garment or bench specimen exists and no measured garment-performance claim is made.

## Frozen technical core

The retained architecture is:

> directional local sweat collection + short distributed two-scale capillary liquid routes + pressure/ambient-aware exterior wet terminals + continuously ambient-connected evaporative microtexture/open valleys + short high-`k/rho` heat routes with limited cross-link redundancy + terminal contact management + dry-side hot-ambient protection.

The primary embodiment is passive/fanless. Optional fan, sorbent, adaptive, detachable, and assisted-flow variants remain disclosed alternatives.

## Canonical findings retained

1. Geometric evaporator area is not automatically accessible evaporative area.
2. Long covered passive wet corridors can remain nearly saturated; nonzero natural flow is not sufficient evidence of useful renewal.
3. Sensible heat and vapor transfer must be treated separately.
4. Positive evaporation is not equivalent to positive body-side cooling in hot ambient conditions.
5. Feed limitation can change the optimum external-exchange condition.
6. Heat spreading creates integrated value only across genuinely different local boundary conditions.
7. Routing pitch and terminal contact are first-order heat-spreader burdens.
8. Corrected equal-material ordering is `uniform homogenized > x-aligned / mesh >> y-transverse`.
9. The current combined stretch/contact/fracture robustness anchor is a lightly cross-linked directed heat network (`lambda≈0.125`).
10. Synthetic load maps favor moving active wet terminals away from persistent high-pressure regions unless vapor access is mechanically protected with little support-area occupation.
11. Active load-state wet-layout switching is not justified as a baseline by the current quasisteady screens.
12. Short distributed liquid routing is strongly favored over one long upward centralized route in the ideal capillary screens.
13. The `d95*r^-4` route proxy is a geometric burden metric, not a substitute for explicit hydraulic-network pressure solves.
14. Sparse liquid-network feasibility is jointly controlled by collector radius, trunk pitch, route phase/placement, source localization, and collapse assumptions.
15. Salt vapor flux is zero; small upstream water leakage does not by itself imply bulk crystallization.
16. Collector fouling is represented only as an imposed hydraulic-radius-loss sensitivity, not as measured deposition kinetics or lifetime.
17. Transient liquid delivery/storage is represented by a mass-conserving low-order buffer model, not measured textile response constants.

## Corrections intentionally preserved

The repository must continue to show the following corrections rather than silently erase them:

- an earlier claim that aligned sparse high-`k` traces exceeded an equal-material homogenized field was wrong and was withdrawn;
- passive corridor flow direction was initially treated too simply; thermo-solutal buoyancy can reverse or neutralize it;
- sensible and vapor transfer were separated after the earlier common-multiplier simplification;
- the terminal-route `d95*r^-4` proxy was initially given too much hydraulic significance; explicit branched networks supersede that interpretation;
- water and nonvolatile-solute balances were separated so `J_salt,vapor = 0`.

## Reproducibility and CI

A documentation-cleanup checkpoint head

`14fa2ab6fb289ad8db568ef6425009f84c684855`

passed all five defined pull-request workflows:

| workflow | run | conclusion |
|---|---:|---|
| `model-tests` | #752 | PASS |
| `topology-tests` | #308 | PASS |
| `pressure-tests` | #127 | PASS |
| `liquid-tests` | #106 | PASS |
| `garment-tests` | #61 | PASS |

A subsequent release-reproducibility change adds Actions artifact upload for the generated reference package. Therefore the final release-candidate head must pass again. The artifact is designed to preserve generated data, figures, `metadata.json`, and `sha256.txt` for the exact commit.

## Public-record readiness

| Item | Status | Note |
|---|---|---|
| Public GitHub repository | PASS | Repository is public. |
| Apache-2.0 | PASS | License present. |
| Integrated technical disclosure | PASS | `docs/technical-disclosure.md`. |
| Concrete embodiment matrix | PASS | `docs/embodiment-matrix.md`. |
| Canonical numerical summary | PASS | `docs/current-results.md`. |
| Documentation index | PASS | `docs/README.md`. |
| Research-freeze policy | PASS | `docs/research-freeze.md`. |
| 45-model executable stack | PASS | Indexed in `simulations/README.md`; count reconciled against the actual directory. |
| Regression/CI structure | PASS | Five dedicated workflows. |
| Cleanup checkpoint CI | PASS | All five workflows successful on `14fa2ab6...`. |
| Exact-head reference artifact | IN PROGRESS | Workflow now uploads the generated reference package. |
| Physical data | NOT AVAILABLE | Not represented as completed. |
| Authoritative patent-family/claim verification | OPEN / SCOPED | Public-index working map is separated from authoritative office verification. |
| Stable tag/release | OPEN | Not yet created. |
| Persistent archive/DOI | OPTIONAL/OPEN | Useful for durable version/date evidence. |

## What is no longer a release blocker

The following are useful future research but are **not required to continue delaying publication** of the present computational record:

- geometry-resolved 3-D natural convection / cross-flow;
- garment-scale curvature and seam models;
- time-varying sweat-source migration;
- detailed spacer/gap deformation mechanics;
- measured precipitation/fouling kinetics;
- a manufactured specimen or physical bench test.

If these are pursued later, they should normally enter a later version rather than expand the current release candidate indefinitely.

## Remaining queue

### P0 — release consistency

- [x] replace placeholder documentation index;
- [x] establish research-freeze/change-control policy;
- [x] simplify root README around canonical conclusions and release state;
- [x] consolidate `docs/current-results.md` as the canonical numerical summary;
- [x] reconcile and freeze `simulations/README.md` at 45 actual executable models;
- [x] synchronize roadmap, release checklist, changelog, citation metadata, prior-art map, and PR description with the freeze decision;
- [x] record a successful five-workflow cleanup checkpoint;
- [x] add exact-head reference-package artifact upload to CI;
- [ ] confirm all five workflows and artifact creation on the final release-candidate head;

### P1 — publication integrity

- [ ] decide which patent family/claim facts, if any, will be labeled authoritatively verified in the stable release;
- [ ] freeze one exact release commit;
- [ ] use the exact-head generated reference artifact / SHA-256 manifest as the release reproducibility package;
- [ ] finalize `CITATION.cff` version/date and release notes;
- [ ] create versioned GitHub tag/release;
- [ ] optionally archive the exact release persistently and record the archive identifier/DOI.

## Final stop rule

No new numerical model should be added to the current release candidate solely because another sensitivity could be explored. New technical work is justified only to correct a contradiction or a release-critical error. Otherwise it belongs to a later version.
