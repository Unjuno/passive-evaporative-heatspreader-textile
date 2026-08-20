# Repository Audit — v1.0.0

Audit date: 2026-08-20  
Release-candidate branch: `agent/initial-research-disclosure`

## Overall assessment

The repository is **technically mature enough to stop exploratory modeling and publish v1.0.0 as a computational/public technical record**.

It contains an integrated technical disclosure, embodiment matrix, canonical current-results record, **45 indexed executable screening/sensitivity/audit/virtual-prototype models** plus one reference-output generator, regression tests, five domain/test PR CI workflows, a release-validation/publication workflow, prior-art notes with explicit confidence boundaries, future physical-validation protocols, and a research-freeze/change-control policy.

The project remains a **virtual/computational prototype only**. No physical garment or bench specimen exists and no measured garment-performance claim is made.

## Frozen technical core

> directional local sweat collection + short distributed two-scale capillary liquid routes + pressure/ambient-aware exterior wet terminals + continuously ambient-connected evaporative microtexture/open valleys/gaps/islands + short high-`k/rho` heat routes with limited cross-link redundancy + terminal contact/load management + dry-side hot-ambient protection.

The primary embodiment is passive/fanless. Fan, sorbent, adaptive, detachable, and assisted-flow variants are optional alternatives.

## Canonical retained findings

1. Geometric evaporator area is not automatically accessible evaporative area.
2. Long covered passive wet corridors can remain nearly saturated; nonzero natural flow does not prove useful renewal.
3. Thermo-solutal corridor-flow tendency can be upward, downward, or near neutral.
4. Sensible heat transfer and vapor transfer must be treated separately.
5. Positive evaporation is not equivalent to positive body-side cooling in hot ambient conditions.
6. Feed limitation can change the optimum external-exchange condition.
7. Heat spreading creates integrated value only across genuinely different local boundary conditions.
8. Routing pitch and terminal contact are first-order heat-spreader burdens.
9. Corrected equal-material ordering is `uniform homogenized > x-aligned / mesh >> y-transverse` for the tested geometry.
10. The current combined stretch/contact/fracture robustness anchor is a lightly cross-linked directed heat network (`lambda≈0.125`).
11. Synthetic load maps favor moving active wet terminals away from persistent high-pressure regions unless vapor access is mechanically protected with little support-area occupation.
12. Active load-state wet-layout switching is not justified as a baseline by the current quasisteady screens.
13. Short distributed liquid routing is strongly favored over one long upward centralized route in the ideal capillary screens.
14. The `d95*r^-4` route proxy is a geometric burden metric, not a substitute for explicit hydraulic-network pressure solves.
15. Sparse liquid-network feasibility is jointly controlled by collector radius, trunk pitch, route phase/placement, source localization, and collapse assumptions.
16. Salt vapor flux is zero; small upstream water leakage does not by itself imply bulk crystallization.
17. Collector fouling is an imposed hydraulic-radius-loss sensitivity, not measured deposition kinetics or lifetime.
18. Transient liquid delivery/storage is a mass-conserving low-order buffer model, not measured textile response constants.

## Corrections intentionally preserved

- An earlier claim that aligned sparse high-`k` traces exceeded an equal-material homogenized field was withdrawn.
- Passive corridor flow was initially treated too simply; thermo-solutal buoyancy can reverse or neutralize it.
- Sensible and vapor transfer were separated after the earlier common-multiplier simplification.
- The terminal-route `d95*r^-4` proxy was initially given too much hydraulic significance; explicit branched networks supersede that interpretation.
- Water and nonvolatile-solute balances were separated so `J_salt,vapor = 0`.

## Release-integrity corrections

Two automated-review P2 findings were fixed and promoted into regression coverage:

1. `simulations/branched_liquid_resistor_network.py` inserts the repository root before `simulations.*` imports, and `liquid-tests` directly executes the indexed script.
2. `simulations/generate_reference_outputs.py` resolves Git metadata with `cwd=REPO_ROOT`, and `model-tests` invokes the generator from outside the checkout working directory.

`model-tests` also distinguishes merge-candidate testing from exact-source-head artifact provenance: before generating the reference artifact, it checks out the exact PR head and verifies `git rev-parse HEAD == expected head == metadata.json git_commit`.

Both review conversations have been resolved after the fixes passed CI.

## Verified v1.0.0 pre-publication checkpoint

The code/release-workflow-bearing head

`568d637f09f039366465544099d8a28d803391c8`

passed all six PR workflows:

| workflow | run | result |
|---|---:|---|
| `model-tests` | #796 | PASS |
| `topology-tests` | #352 | PASS |
| `pressure-tests` | #149 | PASS |
| `liquid-tests` | #128 | PASS |
| `garment-tests` | #83 | PASS |
| `publish-v1` validation | #2 | PASS |

Its exact-head reference artifact is:

- name: `reference-output-568d637f09f039366465544099d8a28d803391c8`;
- artifact id: `9409854675`;
- GitHub ZIP digest: `sha256:9830c9b16c6c4a4b2a7b195e7243b341bb3bec3d4c070dcaefdf97dd6828031f`.

This audit/checklist synchronization changes documentation only. GitHub PR CI is rerun on the resulting final branch head before merge; the PR check state is the authoritative final pre-merge status.

## Patent/prior-art confidence boundary

The stable-release decision is conservative:

- the six-item patent map is retained as a **public-index bibliographic/technical map**;
- v1.0.0 does **not** label patent family, legal-status, or claim-scope facts as authoritatively patent-office verified when that verification was not completed;
- exact family/legal status is not required for the technical conclusions retained in this release;
- no novelty, patentability, invalidity, infringement, or freedom-to-operate conclusion is asserted.

Public official deep links were identified where available, but several office interfaces were not reliably machine-readable from the release-preparation environment. The repository therefore records the lower confidence level rather than converting incomplete access into a false verification claim.

## v1.0.0 publication mechanism

- `CITATION.cff` specifies version `1.0.0` and release date `2026-08-20`.
- `docs/release-notes-v1.0.0.md` is the release-note source.
- `.github/workflows/publish-v1.yml` is PR-validated without write permission.
- On a push to `main`, its publication job uses `contents: write`, verifies the exact merge commit, reruns the full regression suite, directly executes the indexed branched-network script, regenerates the reference package from outside the checkout, checks the recorded commit SHA, builds a ZIP and SHA-256 file, and creates GitHub release/tag `v1.0.0` if it does not already exist.
- An existing `v1.0.0` release is left unchanged on later `main` pushes.

## Public-record readiness

| item | status |
|---|---|
| Public GitHub repository | PASS |
| Apache-2.0 license | PASS |
| Integrated disclosure / embodiment matrix | PASS |
| Canonical results / correction history | PASS |
| 45-model executable index | PASS |
| Regression/CI structure | PASS |
| Exact-head artifact provenance | PASS |
| P2 review fixes / thread resolution | PASS |
| v1.0.0 release notes / citation metadata | PASS |
| Patent confidence policy | PASS |
| `publish-v1` PR validation | PASS |
| Physical measurements | NOT AVAILABLE; not claimed |
| Merge + `v1.0.0` GitHub Release | POST-MERGE OPERATION; automated and verified after merge |
| Persistent DOI/archive | OPTIONAL; no connected archive integration available in this workspace |

## Stop rule

No new numerical model should be added to v1.0.0 solely because another sensitivity could be explored. New technical work belongs to a later version unless it corrects a contradiction or a release-critical error.
