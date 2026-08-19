# Stable Release Checklist

Use this checklist before creating the first versioned public technical release.

## Technical disclosure

- [ ] Core architecture is stated consistently in README and technical disclosure.
- [ ] Primary passive embodiment is separated from optional fan/MOF/adaptive variants.
- [ ] Concrete embodiment matrix is reviewed for operability and internal consistency.
- [ ] All dimensional ranges are labeled as examples, test ranges, or measurements.
- [ ] No simulated number is presented as measured product performance.
- [ ] Salt mass balance contains zero salt-vapor flux.
- [ ] Known failure modes are preserved rather than deleted.

## Prior art

- [ ] Every cited literature item has verified authors/title/year/DOI.
- [ ] Close i-Cool heat-conduction + sweat-transport prior art is explicitly acknowledged.
- [ ] Patent publication numbers and earliest priority dates are verified from authoritative records.
- [ ] Independent-claim overlap is summarized for the closest patent families.
- [ ] No legal conclusion of novelty is asserted without separate professional review.

## Models and data

- [ ] CI passes on the release commit.
- [ ] Multi-stable equilibrium behavior is reported rather than hidden by root selection.
- [ ] Reference output CSV is regenerated from the release commit.
- [ ] Generated data record input parameters and commit SHA.
- [ ] Numerical sensitivity to grid/root detection has been checked.
- [ ] At least one uncertainty/sensitivity report is included.

## Physical experiments

Physical measurements are desirable but not mandatory for an early technical disclosure if the architecture is otherwise enabling. If measurements are included:

- [ ] raw data are retained;
- [ ] calibration metadata are included;
- [ ] exclusion criteria are documented;
- [ ] water balance is reported;
- [ ] sample count is reported;
- [ ] negative/null results are not removed;
- [ ] measurement uncertainty is reported with appropriate precision.

## Public record

- [ ] `CITATION.cff` version and date match the release.
- [ ] `CHANGELOG.md` is updated.
- [ ] repository commit/tag is public.
- [ ] release files are immutable or versioned rather than overwritten.
- [ ] SHA-256 manifest is generated for bundled release artifacts.
- [ ] persistent archival copy/DOI is created when ready.
- [ ] archive links back to the exact repository release/tag.

## Final audit questions

1. Can a technically skilled reader understand a complete working stack rather than only a list of concepts?
2. Can a reader identify the equations, assumptions, boundary conditions, and known failure regimes?
3. Can the numerical results be reproduced from the exact release?
4. Are close prior technologies distinguished accurately rather than ignored?
5. Are all corrections and deprecated design branches traceable?

Do not mark the release stable if any answer is materially unclear.
