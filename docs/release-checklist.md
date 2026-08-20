# Stable Release Checklist

Status date: 2026-08-20

This checklist tracks the **release candidate**, not further exploratory model development.

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
- [ ] Final exact-head pass confirms no documentation/count drift after the last reproducibility edits.

## 3. Prior art and source integrity

- [x] Close literature is identified with stable bibliographic identifiers in the working prior-art map.
- [x] Close integrated heat-conduction + sweat-transport prior art is explicitly acknowledged.
- [x] Patent working notes separate public-index bibliographic/technical cross-checks from authoritative patent-office verification.
- [x] Claim-scope caveats are retained where specification embodiments could be mistaken for independent-claim limitations.
- [x] Repository does not claim novelty, patentability, invalidity, or freedom to operate as a legal conclusion.
- [ ] For any patent family/claim fact the stable release chooses to label **authoritatively verified**, verify that exact fact from an authoritative patent-office record; otherwise leave it explicitly as a working-map/public-index statement.

## 4. Models, tests, data, and release artifact

- [x] Simulation index contains **45 executable models** plus the reference-output generator.
- [x] Regression tests exist for the current model families.
- [x] Multiple/multi-stable equilibrium behavior is reported rather than hidden by root selection.
- [x] Uncertainty/sensitivity analysis is present.
- [x] Dense and sparse liquid-network corrections are reflected in canonical documentation.
- [x] Collector-fouling/radius-loss is identified as an imposed failure sensitivity rather than measured deposition kinetics.
- [x] Transient terminal buffering is identified as a mass-conserving low-order model rather than a measured response constant.
- [x] Documentation-cleanup checkpoint `14fa2ab6fb289ad8db568ef6425009f84c684855` passed all five workflows:
  - `model-tests` #752;
  - `topology-tests` #308;
  - `pressure-tests` #127;
  - `liquid-tests` #106;
  - `garment-tests` #61.
- [x] `model-tests` now uploads the generated reference package as an exact-head Actions artifact.
- [ ] Confirm all five workflows pass on the **final release-candidate commit** after the count/artifact corrections.
- [ ] Confirm the reference artifact exists and contains generated data, figures, `metadata.json`, and `sha256.txt`.

## 5. Physical experiments

Physical measurements are **not required for closure of this computational disclosure**, and no specimen exists.

If measurements are ever added in a later version:

- [ ] retain raw data;
- [ ] include calibration metadata;
- [ ] document exclusion criteria;
- [ ] report water balance;
- [ ] report sample count;
- [ ] retain negative/null results;
- [ ] report measurement uncertainty with appropriate precision.

No unchecked physical-experiment item blocks the present computational release.

## 6. Version and public record

- [ ] Choose final version identifier (`v1.0.0` is the natural stable candidate unless intentionally choosing another version).
- [ ] Update `CITATION.cff` version/date to match the actual release.
- [ ] Finalize release notes for the exact final commit.
- [ ] Record the final release commit SHA.
- [ ] Create public GitHub tag/release without rewriting earlier public history.
- [ ] Attach or reference the exact-head reference artifact / SHA-256 manifest.
- [ ] Optionally create a persistent archival copy/DOI and link it to the exact GitHub tag/commit.

## 7. Final audit questions

Before tagging stable, all answers should be **yes**:

1. Can a technically skilled reader identify one complete passive working architecture rather than only a menu of concepts?
2. Can a reader identify equations, assumptions, boundary conditions, and known failure regimes?
3. Can the numerical results be reproduced from the exact release commit?
4. Are major corrections and superseded interpretations traceable?
5. Are close prior technologies acknowledged accurately at the confidence level actually verified?
6. Is every remaining unchecked item a publication/source-integrity task rather than an invitation to resume open-ended modeling?
7. Does the repository clearly distinguish computational evidence from physical measurement?

## Release rule

Do **not** add a new numerical model to the release candidate merely because another sensitivity could be explored. New research should normally be deferred to a later version unless it corrects a contradiction or a release-critical technical error.
