# Repository Audit — v1.0.0

Audit date: 2026-08-20  
Stable tag: `v1.0.0`  
Stable commit: `e544f64630119c88425b49cc3e5a00e06d15ad84`

## Overall assessment

`v1.0.0` is the published stable computational/public technical record for this project. The exploratory numerical phase is frozen for that version.

The stable record contains an integrated technical disclosure, embodiment matrix, canonical current-results record, **45 indexed executable screening/sensitivity/audit/virtual-prototype models** plus one reference-output generator, regression tests, five domain/test CI workflows, prior-art notes with explicit confidence boundaries, future physical-validation protocols, and a research-freeze/change-control policy.

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
10. The combined stretch/contact/fracture robustness anchor is a lightly cross-linked directed heat network (`lambda≈0.125`).
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

Two automated-review P2 findings were fixed before release and promoted into regression coverage:

1. `simulations/branched_liquid_resistor_network.py` inserts the repository root before `simulations.*` imports, and CI directly executes the indexed script.
2. `simulations/generate_reference_outputs.py` resolves Git metadata with `cwd=REPO_ROOT`, and CI invokes the generator from outside the checkout working directory.

Both review conversations were resolved before merge.

## Final pre-merge verification

Final release-candidate head:

`0a885e41f8a1ebef1152066d2cea79fe156b5dad`

All six PR workflows passed:

| workflow | run | result |
|---|---:|---|
| `model-tests` | #800 | PASS |
| `topology-tests` | #356 | PASS |
| `pressure-tests` | #151 | PASS |
| `liquid-tests` | #130 | PASS |
| `garment-tests` | #85 | PASS |
| `publish-v1` validation | #4 | PASS |

The exact-head reference artifact was:

- name: `reference-output-0a885e41f8a1ebef1152066d2cea79fe156b5dad`;
- artifact id: `9410060502`;
- GitHub ZIP digest: `sha256:a2dbba8d70d5453bd445afa035dbf62857f6c14b71157ddcb933917b5d08b6fc`.

## Published stable state

PR #1 was merged normally into `main`. The resulting merge commit is:

`e544f64630119c88425b49cc3e5a00e06d15ad84`

The public tag `v1.0.0` resolves to that exact commit. `CITATION.cff` in the tag records `version: 1.0.0` and `date-released: 2026-08-20`.

The release publication workflow was designed to rerun the full regression suite at the exact merge commit, directly execute the branched liquid model, regenerate the reference package outside the checkout, verify `metadata.json` commit provenance, create a ZIP and SHA-256 file, and create the GitHub `v1.0.0` release/tag if absent.

The current workspace can verify the public tag and exact commit but does not expose a GitHub Release-asset download endpoint. Therefore **asset contents are not claimed here as independently re-downloaded after publication**. Pre-release exact-head artifact provenance and the publication workflow itself were separately verified before merge. This confidence boundary is intentional.

## Post-release workflow policy

After `v1.0.0` exists, automatic publication on every future `main` push is unnecessary. The post-release maintenance branch converts `.github/workflows/publish-v1.yml` into a read-only/manual release verifier that checks out immutable tag `v1.0.0`, verifies its exact SHA and metadata, reruns regressions, regenerates the reference package, and uploads a temporary verification artifact. It does not modify or republish the stable release.

## Patent/prior-art confidence boundary

- The six-item patent map is retained as a **public-index bibliographic/technical map**.
- `v1.0.0` does **not** label patent family, legal-status, or claim-scope facts as authoritatively patent-office verified when that verification was not completed.
- Exact family/legal status is not required for the technical conclusions retained in this release.
- No novelty, patentability, invalidity, infringement, or freedom-to-operate conclusion is asserted.

## Public-record status

| item | status |
|---|---|
| Public GitHub repository | PASS |
| Apache-2.0 license | PASS |
| Integrated disclosure / embodiment matrix | PASS |
| Canonical results / correction history | PASS |
| 45-model executable index | PASS |
| Regression/CI structure | PASS |
| Exact-head pre-release artifact provenance | PASS |
| P2 review fixes / thread resolution | PASS |
| v1.0.0 release notes / citation metadata | PASS |
| PR merge to `main` | PASS |
| `v1.0.0` tag -> exact merge commit | PASS |
| Post-publication release-asset re-download | NOT INDEPENDENTLY VERIFIED IN THIS WORKSPACE |
| Physical measurements | NOT AVAILABLE; not claimed |
| Persistent DOI/archive | OPTIONAL; no connected archive integration available in this workspace |

## Stop rule

No new numerical model should be added to `v1.0.0`. New technical work belongs to a later version unless it corrects a contradiction in the published record. Post-release `main` maintenance must not rewrite or move the `v1.0.0` tag.
