# Stable Release Checklist

Status date: 2026-08-20

This checklist records the completed `v1.0.0` publication and the remaining optional archival work. It is not an open-ended research queue.

## 1. Technical record

- [x] Core passive architecture is stated consistently in the root README and technical disclosure.
- [x] Primary passive embodiment is separated from optional fan/sorbent/adaptive variants.
- [x] Concrete embodiment matrix records complete implementation combinations.
- [x] Numerical values are described as simulations, analytic screens, or research ranges rather than measurements.
- [x] No simulated watt value is presented as measured garment performance.
- [x] Salt mass balance contains zero salt-vapor flux: `J_salt,vapor = 0`.
- [x] Major negative results and corrections are retained rather than removed.
- [x] Research-freeze / change-control policy is documented.
- [x] Optional future research is separated from stable-release blockers.

## 2. Canonical documentation

- [x] Root `README.md` is the project summary and navigation entry point.
- [x] `docs/README.md` is the documentation index.
- [x] `docs/technical-disclosure.md` is the integrated architecture disclosure.
- [x] `docs/embodiment-matrix.md` records concrete implementation families.
- [x] `docs/current-results.md` is the canonical numerical-results record for v1.0.0.
- [x] `docs/research-freeze.md` states what is frozen and what is deferred.
- [x] `AUDIT.md` records release integrity and known corrections.
- [x] `docs/release-notes-v1.0.0.md` records stable release scope and evidence boundary.
- [x] Actual executable-model count was reconciled against `simulations/`: **45 models + 1 reference-output generator**.

## 3. Prior art and source integrity

- [x] Close literature is identified with stable bibliographic identifiers in the working prior-art map.
- [x] Close integrated heat-conduction + sweat-transport prior art is explicitly acknowledged.
- [x] Patent working notes separate public-index bibliographic/technical cross-checks from authoritative patent-office verification.
- [x] Claim-scope caveats are retained where specification embodiments could be mistaken for independent-claim limitations.
- [x] Repository does not claim novelty, patentability, invalidity, infringement, or freedom to operate as a legal conclusion.
- [x] `v1.0.0` labels no patent family/legal-status/claim-scope fact as authoritatively office-verified unless such verification is actually recorded.

## 4. Models, tests, and pre-release reference artifact

- [x] Simulation index contains **45 executable models** plus the reference-output generator.
- [x] Regression tests exist for the current model families.
- [x] Multiple/multi-stable equilibrium behavior is reported rather than hidden by root selection.
- [x] Uncertainty/sensitivity analysis is present.
- [x] Dense and sparse liquid-network corrections are reflected in canonical documentation.
- [x] Collector-fouling/radius-loss is identified as an imposed failure sensitivity rather than measured deposition kinetics.
- [x] Transient terminal buffering is identified as a mass-conserving low-order model rather than a measured response constant.
- [x] `branched_liquid_resistor_network.py` direct execution is covered by CI.
- [x] `generate_reference_outputs.py` resolves Git metadata from `REPO_ROOT`, and CI invokes it from outside the checkout working directory.
- [x] Final release-candidate head `0a885e41f8a1ebef1152066d2cea79fe156b5dad` passed all six PR workflows.
- [x] Exact-head reference artifact existed for that head: artifact id `9410060502`, GitHub ZIP digest `sha256:a2dbba8d70d5453bd445afa035dbf62857f6c14b71157ddcb933917b5d08b6fc`.

## 5. Stable version and public record

- [x] Final version identifier: `v1.0.0`.
- [x] `CITATION.cff` contains `version: 1.0.0` and `date-released: 2026-08-20`.
- [x] PR #1 was merged to `main` without squashing the research history.
- [x] Stable merge commit: `e544f64630119c88425b49cc3e5a00e06d15ad84`.
- [x] Public tag `v1.0.0` resolves to that exact merge commit.
- [x] Publication workflow was PR-validated before merge.
- [x] Publication workflow was designed to regenerate the exact-commit package, verify its metadata, create a ZIP and SHA-256 file, and create `v1.0.0` if absent.
- [ ] Independently re-download the GitHub Release assets and verify the published ZIP against its published SHA-256. **Not completed in this workspace because the connected GitHub interface does not expose Release-asset download endpoints.**
- [ ] Persistent archival copy/DOI. **Optional; no Zenodo/DOI integration is currently connected to this workspace.**

The two unchecked items do not change the technical content of `v1.0.0`. The first is an independent post-publication distribution check; the second is an optional second archive.

## 6. Post-release maintenance

- [x] `v1.0.0` is treated as immutable project history.
- [x] Automatic `v1.0.0` publication on every later `main` push is removed in post-release maintenance.
- [x] The former publication workflow is converted into a read-only/manual verifier that checks out tag `v1.0.0`, verifies exact SHA/metadata, reruns regressions, regenerates the reference package, and uploads a temporary verification artifact.
- [x] Post-release maintenance does not move or rewrite the stable tag.

## 7. Physical experiments

Physical measurements are **not required for closure of this computational disclosure**, and no specimen exists.

If measurements are ever added in a later version, retain raw data, calibration metadata, exclusion criteria, water balance, sample count, negative/null results, and measurement uncertainty with appropriate precision.

No physical-experiment item blocks `v1.0.0`.

## Final audit questions

1. Can a technically skilled reader identify one complete passive working architecture rather than only a menu of concepts? **Yes.**
2. Can a reader identify equations, assumptions, boundary conditions, and known failure regimes? **Yes.**
3. Can the numerical results be regenerated from the exact release tag? **Yes; the post-release verifier is explicitly bound to the immutable v1.0.0 SHA.**
4. Are major corrections and superseded interpretations traceable? **Yes.**
5. Are close prior technologies acknowledged at the confidence level actually verified? **Yes.**
6. Does the repository clearly distinguish computational evidence from physical measurement? **Yes.**
7. Is further numerical exploration required to keep v1.0.0 valid as the published computational record? **No.**

## Release rule

Do **not** add a new numerical model to `v1.0.0`. New research belongs to a later version unless it corrects a contradiction in the published record. Never rewrite or move the `v1.0.0` tag.
