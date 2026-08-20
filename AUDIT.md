# Repository Audit

Audit date: 2026-08-20  
Branch: `agent/initial-research-disclosure`

## Overall assessment

The repository is **technically mature enough to stop exploratory modeling and move to release preparation** for the present computational/public technical record.

It contains:

- an integrated technical disclosure;
- an explicit embodiment matrix;
- a canonical current-results record;
- **43 indexed executable screening/sensitivity/audit/virtual-prototype models** plus the reference-output generator;
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

## Corrections intentionally preserved

The repository must continue to show the following corrections rather than silently erase them:

- an earlier claim that aligned sparse high-`k` traces exceeded an equal-material homogenized field was wrong and was withdrawn;
- passive corridor flow direction was initially treated too simply; thermo-solutal buoyancy can reverse or neutralize it;
- sensible and vapor transfer were separated after the earlier common-multiplier simplification;
- the terminal-route `d95*r^-4` proxy was initially given too much hydraulic significance; explicit branched networks supersede that interpretation;
- water and nonvolatile-solute balances were separated so `J_salt,vapor = 0`.

## Reproducibility and CI

The pre-cleanup 43-model integration head was:

`529fc573f2a24a0d4d3db8464c3c1409a38b34ec`

All five defined pull-request workflows completed successfully on that head:

| workflow | run | conclusion |
|---|---:|---|
| `model-tests` | #722 | PASS |
| `topology-tests` | #278 | PASS |
| `pressure-tests` | #112 | PASS |
| `liquid-tests` | #91 | PASS |
| `garment-tests` | #46 | PASS |

The release-candidate documentation cleanup creates later commits, so the **final release commit must be checked again** before tagging. The cleanup phase is documentation/metadata oriented and does not intentionally expand the 43-model stack.

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
| 43-model executable stack | PASS | Indexed in `simulations/README.md`. |
| Regression/CI structure | PASS | Five dedicated workflows. |
| Pre-cleanup 43-model CI | PASS | All five workflows successful on `529fc573...`. |
| Physical data | NOT AVAILABLE | Not represented as completed. |
| Authoritative patent-family/claim verification | OPEN | Publication/family identifiers and dates still need authoritative confirmation before stable release notes rely on them. |
| Exact release commit CI | OPEN | Must be rerun/confirmed after documentation cleanup. |
| Stable tag/release | OPEN | Not yet created. |
| Frozen release hash manifest | OPEN | Regenerate at exact release commit. |
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
- [x] freeze `simulations/README.md` at 43 indexed models;
- [x] synchronize roadmap, release checklist, changelog, and citation metadata with the freeze decision;
- [x] record successful five-workflow integration on the pre-cleanup 43-model head;
- [ ] confirm all five workflows on the final documentation-cleanup head;
- [ ] final cross-document proofreading pass.

### P1 — publication integrity

- [ ] verify patent publication/family identifiers and dates from authoritative sources;
- [ ] freeze one exact release commit;
- [ ] regenerate reference artifacts and SHA-256 manifest from that commit;
- [ ] finalize `CITATION.cff` version/date and release notes;
- [ ] create versioned GitHub tag/release;
- [ ] optionally archive the exact release persistently and record the archive identifier/DOI.

## Final stop rule

No new numerical model should be added to the current release candidate solely because another sensitivity could be explored. New technical work is justified only to correct a contradiction or a release-critical error. Otherwise it belongs to a later version.
