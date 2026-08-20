# Stable Release Checklist

Status date: 2026-08-20

This checklist now tracks the **release candidate**, not further exploratory model development.

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
- [x] `docs/current-results.md` is the detailed numerical-results record.
- [x] `docs/research-freeze.md` states what is frozen and what is deferred.
- [x] `AUDIT.md` records release-readiness and known corrections.
- [x] `docs/roadmap.md` is release-oriented rather than an open-ended research queue.
- [ ] Final proofreading pass confirms these documents do not contradict one another after the cleanup commits.

## 3. Prior art and source integrity

- [ ] Verify every cited literature item used in the final prior-art summary for authors/title/year/DOI or other stable identifier.
- [ ] Explicitly retain acknowledgement of close integrated heat-conduction + sweat-transport prior art.
- [ ] Verify patent publication numbers, family relationships, and earliest relevant dates from authoritative patent-office sources.
- [ ] Where independent-claim overlap is discussed, ensure the wording is descriptive rather than a legal conclusion.
- [x] Repository does not claim novelty, patentability, invalidity, or freedom to operate as a legal conclusion.

## 4. Models, tests, and data

- [x] Simulation index contains 43 executable models plus the reference-output generator.
- [x] Regression tests exist for the current model families.
- [x] Multiple/multi-stable equilibrium behavior is reported rather than hidden by root selection.
- [x] Uncertainty/sensitivity analysis is present.
- [x] Dense and sparse liquid-network corrections are reflected in canonical documentation.
- [x] Pre-cleanup integration head `529fc573f2a24a0d4d3db8464c3c1409a38b34ec` passed all five workflows:
  - `model-tests` #722;
  - `topology-tests` #278;
  - `pressure-tests` #112;
  - `liquid-tests` #91;
  - `garment-tests` #46.
- [ ] Confirm all five workflows pass on the **exact final cleanup/release commit**.
- [ ] Regenerate release reference outputs from that exact commit.
- [ ] Confirm generated data/metadata record the release commit SHA where intended.
- [ ] Generate/freeze SHA-256 manifest for bundled release artifacts.

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

- [ ] Choose final version identifier (`v1.0.0` or another explicit stable version).
- [ ] Update `CITATION.cff` version/date to match the actual release.
- [ ] Update `CHANGELOG.md` and release notes to the exact final commit.
- [ ] Record the final release commit SHA.
- [ ] Create public GitHub tag/release without rewriting earlier public history.
- [ ] Attach or reference the frozen hash/reference package.
- [ ] Optionally create a persistent archival copy/DOI and link it to the exact GitHub tag/commit.

## 7. Final audit questions

Before tagging stable, all answers should be **yes**:

1. Can a technically skilled reader identify one complete passive working architecture rather than only a menu of concepts?
2. Can a reader identify equations, assumptions, boundary conditions, and known failure regimes?
3. Can the numerical results be reproduced from the exact release commit?
4. Are major corrections and superseded interpretations traceable?
5. Are close prior technologies acknowledged accurately?
6. Is every remaining unchecked item a publication/source-integrity task rather than an invitation to resume open-ended modeling?
7. Does the repository clearly distinguish computational evidence from physical measurement?

## Release rule

Do **not** add a new numerical model to the release candidate merely because another sensitivity could be explored. New research should normally be deferred to a later version unless it corrects a contradiction or a release-critical technical error.
