# Repository Audit — v1.0.0

Audit date: 2026-08-20  
Release-candidate branch: `agent/initial-research-disclosure`

## Overall assessment

The repository is **technically mature enough to stop exploratory modeling and publish v1.0.0 as a computational/public technical record**.

It contains:

- an integrated technical disclosure;
- an explicit embodiment matrix;
- a canonical current-results record;
- **45 indexed executable screening/sensitivity/audit/virtual-prototype models** plus one reference-output generator;
- regression tests and five dedicated PR CI workflows;
- prior-art/patent technical notes with explicit confidence boundaries;
- future physical-validation protocols;
- a research-freeze/change-control policy;
- v1.0.0 citation metadata, release notes, and an automated exact-commit release workflow.

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

The repository explicitly retains these corrections:

- an earlier claim that aligned sparse high-`k` traces exceeded an equal-material homogenized field was withdrawn;
- passive corridor flow was initially treated too simply; thermo-solutal buoyancy can reverse or neutralize it;
- sensible and vapor transfer were separated after the earlier common-multiplier simplification;
- the terminal-route `d95*r^-4` proxy was initially given too much hydraulic significance; explicit branched networks supersede that interpretation;
- water and nonvolatile-solute balances were separated so `J_salt,vapor = 0`.

## Release-integrity corrections

Two automated-review P2 findings were fixed and promoted into regression coverage:

1. `simulations/branched_liquid_resistor_network.py` now inserts the repository root before `simulations.*` imports, and `liquid-tests` directly executes the indexed script.
2. `simulations/generate_reference_outputs.py` resolves Git metadata with `cwd=REPO_ROOT`, and `model-tests` invokes the generator from outside the checkout working directory.

The PR workflow also distinguishes merge-candidate testing from exact-source-head artifact provenance: before generating the reference artifact, `model-tests` checks out the exact PR head and verifies `git rev-parse HEAD == expected head == metadata.json git_commit`.

## Verified pre-publication checkpoint

Head `a4bba3fc93c5197ced42f30d836237afae6ac699` passed all five PR workflows after the P2 fixes:

| workflow | run | result |
|---|---:|---|
| `model-tests` | #778 | PASS |
| `topology-tests` | #334 | PASS |
| `pressure-tests` | #140 | PASS |
| `liquid-tests` | #119 | PASS |
| `garment-tests` | #74 | PASS |

Its exact-head artifact was `reference-output-a4bba3fc93c5197ced42f30d836237afae6ac699`, artifact id `9408966551`, GitHub ZIP digest `sha256:17e98cca6aff31994283dda33ad3a489a1a935e5cc623beef6cd1bd624ef1d50`. Independent inspection found 33 files and zero mismatches across the 32 entries in the package-level `sha256.txt` manifest.

The final metadata/publication-workflow head must pass again before merge.

## Patent/prior-art confidence boundary

The stable-release decision is conservative:

- the six-item patent map is retained as a **public-index bibliographic/technical map**;
- v1.0.0 does **not** label patent family, legal-status, or claim-scope facts as authoritatively patent-office verified when that verification was not completed;
- exact family/legal status is not required for the technical conclusions retained in this release;
- no novelty, patentability, invalidity, infringement, or freedom-to-operate conclusion is asserted.

This resolves the publication blocker without turning incomplete office-record access into a false verification claim.

## v1.0.0 publication mechanism

- `CITATION.cff` specifies version `1.0.0` and release date `2026-08-20`.
- `docs/release-notes-v1.0.0.md` is the release-note source.
- `.github/workflows/publish-v1.yml` runs on the first relevant `main` push, verifies the exact merge commit, runs the full regression suite, directly executes the indexed branched-network script, regenerates the reference package from outside the checkout, checks the recorded commit SHA, builds a ZIP and SHA-256 file, and creates GitHub release/tag `v1.0.0` if it does not already exist.
- Existing `v1.0.0` releases are left unchanged on later `main` pushes.

## Public-record readiness

| item | status |
|---|---|
| Public repository | PASS |
| Apache-2.0 license | PASS |
| Integrated disclosure / embodiment matrix | PASS |
| Canonical results / correction history | PASS |
| 45-model executable index | PASS |
| Regression/CI structure | PASS |
| Exact-head artifact provenance | PASS |
| Release notes / citation metadata | PASS |
| Patent confidence policy | PASS |
| Physical measurements | NOT AVAILABLE; not claimed |
| Final metadata-head CI | PENDING before merge |
| `v1.0.0` tag/release | AUTOMATED on verified merge to `main` |
| Persistent DOI/archive | OPTIONAL; no connected archive integration available in this workspace |

## Stop rule

No new numerical model should be added to v1.0.0 solely because another sensitivity could be explored. New technical work belongs to a later version unless it corrects a contradiction or a release-critical error.
