# Stable Release Checklist

Status date: 2026-08-20

This checklist tracks **v1.0.0 publication**, not further exploratory model development.

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

- [x] Root `README.md` is a concise project summary and navigation entry point.
- [x] `docs/README.md` is a usable documentation index.
- [x] `docs/technical-disclosure.md` is the integrated architecture disclosure.
- [x] `docs/embodiment-matrix.md` records concrete implementation families.
- [x] `docs/current-results.md` is the canonical numerical-results record.
- [x] `docs/research-freeze.md` states what is frozen and what is deferred.
- [x] `AUDIT.md` records release-readiness and known corrections.
- [x] `docs/roadmap.md` is release-oriented rather than an open-ended research queue.
- [x] Actual executable-model count was reconciled against `simulations/`: **45 models + 1 reference-output generator**.
- [x] v1.0.0 release notes are present at `docs/release-notes-v1.0.0.md`.
- [ ] Final exact-head CI pass after the v1.0.0 metadata/publication-workflow edits.

## 3. Prior art and source integrity

- [x] Close literature is identified with stable bibliographic identifiers in the working prior-art map.
- [x] Close integrated heat-conduction + sweat-transport prior art is explicitly acknowledged.
- [x] Patent working notes separate public-index bibliographic/technical cross-checks from authoritative patent-office verification.
- [x] Claim-scope caveats are retained where specification embodiments could be mistaken for independent-claim limitations.
- [x] Repository does not claim novelty, patentability, invalidity, infringement, or freedom to operate as a legal conclusion.
- [x] Stable-release confidence policy is decided: **v1.0.0 labels no patent family/legal-status/claim-scope fact as authoritatively office-verified unless such verification is actually recorded.** The current six-item patent map remains explicitly a public-index technical map.

## 4. Models, tests, data, and release artifact

- [x] Simulation index contains **45 executable models** plus the reference-output generator.
- [x] Regression tests exist for the current model families.
- [x] Multiple/multi-stable equilibrium behavior is reported rather than hidden by root selection.
- [x] Uncertainty/sensitivity analysis is present.
- [x] Dense and sparse liquid-network corrections are reflected in canonical documentation.
- [x] Collector-fouling/radius-loss is identified as an imposed failure sensitivity rather than measured deposition kinetics.
- [x] Transient terminal buffering is identified as a mass-conserving low-order model rather than a measured response constant.
- [x] Exact-PR-head artifact provenance was corrected and independently checked.
- [x] `branched_liquid_resistor_network.py` direct execution is covered by CI.
- [x] `generate_reference_outputs.py` resolves Git metadata from `REPO_ROOT`, and CI invokes it from outside the checkout working directory.
- [x] Exact-head reference artifacts contain generated data, figures, `metadata.json`, and `sha256.txt`.
- [ ] Confirm all five PR workflows pass on the final v1.0.0 release-candidate head.

## 5. Physical experiments

Physical measurements are **not required for closure of this computational disclosure**, and no specimen exists.

If measurements are ever added in a later version, retain raw data, calibration metadata, exclusion criteria, water balance, sample count, negative/null results, and measurement uncertainty with appropriate precision.

No physical-experiment item blocks v1.0.0.

## 6. Version and public record

- [x] Final version identifier chosen: `v1.0.0`.
- [x] `CITATION.cff` contains `version: 1.0.0` and `date-released: 2026-08-20`.
- [x] Release notes finalized at `docs/release-notes-v1.0.0.md`.
- [x] `.github/workflows/publish-v1.yml` is configured to publish `v1.0.0` from the exact stable `main` commit after running regressions and regenerating the reference package.
- [ ] Merge the verified release-candidate PR to `main`.
- [ ] Confirm `publish-v1` creates tag/release `v1.0.0` at the merge commit.
- [ ] Confirm the GitHub Release contains `reference-output-v1.0.0.zip` and its SHA-256 file.
- [ ] Persistent archival copy/DOI: optional; no Zenodo/DOI integration is currently connected to this workspace.

## 7. Final audit questions

Before merge/tag, all answers should be **yes**:

1. Can a technically skilled reader identify one complete passive working architecture rather than only a menu of concepts?
2. Can a reader identify equations, assumptions, boundary conditions, and known failure regimes?
3. Can the numerical results be reproduced from the exact release commit?
4. Are major corrections and superseded interpretations traceable?
5. Are close prior technologies acknowledged accurately at the confidence level actually verified?
6. Is every remaining unchecked item a publication operation rather than an invitation to resume open-ended modeling?
7. Does the repository clearly distinguish computational evidence from physical measurement?

## Release rule

Do **not** add a new numerical model to v1.0.0 merely because another sensitivity could be explored. New research should normally be deferred to a later version unless it corrects a contradiction or a release-critical technical error.
