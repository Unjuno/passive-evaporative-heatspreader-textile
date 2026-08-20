# Release-preparation roadmap

Date: 2026-08-20

## Project mode

The project has moved from exploratory computational research to **research freeze / release preparation**.

The present public technical record is considered sufficiently developed to stop adding models for completeness alone. The remaining required work is repository consistency, authoritative source verification, exact-commit reproducibility, versioning, and archival publication.

No physical garment or bench specimen exists. Future physical validation remains optional and must not be described as completed work.

## Gate A — technical architecture

Status: **COMPLETE FOR CURRENT COMPUTATIONAL DISCLOSURE**

- [x] fanless/passive baseline defined;
- [x] core and optional components separated;
- [x] heat, liquid, vapor, pressure/load, and hot-ambient subsystems coupled conceptually;
- [x] multiple concrete embodiments documented;
- [x] nonvolatile-salt correction retained;
- [x] failure modes and negative/corrected results retained.

Current retained family:

> directional local sweat collection -> short distributed two-scale capillary routing -> pressure/ambient-aware exterior wet terminals -> ambient-connected microtexture/open valleys -> short routed heat spreading with limited redundancy -> contact/load management -> dry-side hot-ambient protection.

## Gate B — reproducible model stack

Status: **COMPLETE FOR CURRENT RELEASE CANDIDATE**

The branch contains 43 indexed executable screening/sensitivity/audit/virtual-prototype models plus a reference-output generator.

The stack covers:

- exterior heat/vapor physics;
- feed-limited states and environmental sign boundaries;
- direct-material and 2-D heat routing;
- topology/failure/pressure/contact screens;
- synthetic garment load maps;
- protected vapor-gap alternatives;
- capillary architecture, collapse, dense branched flow, and sparse two-scale networks;
- nonvolatile-solute balance;
- transient terminal buffering;
- virtual garment mass/thickness.

The pre-cleanup integration head `529fc573...` passed all five defined workflows (`model-tests`, `topology-tests`, `pressure-tests`, `liquid-tests`, `garment-tests`). The final cleanup head must be checked again before release.

## Gate C — canonical documentation

Status: **IN FINAL CONSOLIDATION**

Canonical documents:

- `technical-disclosure.md` — disclosed architecture and embodiments;
- `current-results.md` — detailed numerical findings and limitations;
- `architecture.md` — system structure;
- `embodiment-matrix.md` — concrete implementation combinations;
- `research-freeze.md` — frozen core, optional backlog, and change-control rule;
- `../AUDIT.md` — release-readiness audit;
- `release-checklist.md` — exact release checklist.

The root README and documentation index are now navigation/summary documents rather than competing technical summaries.

## Gate D — prior-art/publication integrity

Status: **OPEN**

Required before stable release notes rely on patent/publication metadata:

- [ ] verify literature bibliographic identifiers used in the prior-art notes;
- [ ] verify patent publication/family identifiers and earliest dates from authoritative patent-office records;
- [ ] ensure close integrated heat-conduction + sweat-transport work is acknowledged accurately;
- [ ] avoid legal conclusions of novelty, patentability, invalidity, or freedom to operate.

This gate is a source-verification task, not a reason to resume open-ended thermal/fluid modeling.

## Gate E — exact release commit

Status: **OPEN**

- [ ] finish documentation synchronization;
- [ ] confirm all five workflows pass on the exact candidate commit;
- [ ] regenerate release reference outputs from that commit;
- [ ] record commit SHA in release metadata;
- [ ] generate/freeze SHA-256 manifest for bundled release artifacts;
- [ ] update `CITATION.cff` version/date;
- [ ] finalize changelog and release notes.

## Gate F — versioned public release

Status: **OPEN**

- [ ] merge/freeze the selected commit into the release branch/default branch as appropriate;
- [ ] create a versioned GitHub tag/release;
- [ ] keep earlier public commits/history accessible rather than overwriting them;
- [ ] optionally create a persistent archival copy/DOI linked to the exact tag/commit.

## Optional future research — not release blockers

The following remain technically interesting but are deferred to a later version unless they reveal a contradiction in the frozen record:

- geometry-resolved 3-D exterior natural convection/cross-flow;
- garment-scale curvature and seam placement;
- time-varying sweat-source migration;
- explicit spacer/gap deformation under load;
- measured local wall-film precipitation/dissolution and fouling kinetics;
- physical prototype construction and controlled bench validation;
- human-subject work, subject to appropriate ethics/safety processes if ever pursued.

## Change-control policy

After research freeze, every new branch change should be classified as:

1. **correction** — fixes an error;
2. **clarification** — improves wording/traceability without expanding architecture;
3. **release metadata** — CI, hashes, citation, version, archive information;
4. **new research** — normally deferred to a later version.

The default action for category 4 is **defer**, not expand the current release candidate.

## Stop condition

The current project can stop after a stable version is frozen and the exact public record is identifiable by commit/tag (and optionally archive identifier). Further modeling is not required for closure of this computational research phase.
