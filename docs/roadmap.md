# Release-preparation roadmap

Date: 2026-08-20

## Project mode

The project has moved from exploratory computational research to **research freeze / release preparation**.

The present public technical record is considered sufficiently developed to stop adding models for completeness alone. The remaining required work is repository consistency, exact-commit reproducibility, versioning, and archival publication. Patent/publication facts are kept at the confidence level actually verified.

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

The branch contains **45 indexed executable screening/sensitivity/audit/virtual-prototype models** plus a reference-output generator. The count has been reconciled against the actual `simulations/` directory, including the later-added collector-fouling and transient-terminal-buffer screens.

The stack covers:

- exterior heat/vapor physics;
- feed-limited states and environmental sign boundaries;
- direct-material and 2-D heat routing;
- topology/failure/pressure/contact screens;
- synthetic garment load maps;
- protected vapor-gap alternatives;
- capillary architecture, collapse, dense branched flow, sparse two-scale networks, and imposed fouling/radius loss;
- nonvolatile-solute balance;
- transient terminal water buffering;
- virtual garment mass/thickness.

A documentation-cleanup checkpoint head `14fa2ab6...` passed all five defined workflows. A later release-reproducibility commit adds exact-head reference-package artifact upload, so the final head is being checked again.

## Gate C — canonical documentation

Status: **COMPLETE SUBJECT TO FINAL EXACT-HEAD CHECK**

Canonical documents:

- `technical-disclosure.md` — disclosed architecture and embodiments;
- `current-results.md` — canonical numerical findings and limitations;
- `architecture.md` — system structure;
- `embodiment-matrix.md` — concrete implementation combinations;
- `research-freeze.md` — frozen core, optional backlog, and change-control rule;
- `../AUDIT.md` — release-readiness audit;
- `release-checklist.md` — exact release checklist.

The root README and documentation index are navigation/summary documents rather than competing technical summaries.

## Gate D — prior-art/publication integrity

Status: **SCOPED / PARTIALLY VERIFIED**

Completed:

- [x] close literature is acknowledged, including integrated heat-conduction + sweat-transport work;
- [x] patent working notes distinguish public-index bibliographic/technical cross-checks from authoritative patent-office/family/claim verification;
- [x] claim-scope caveats are recorded where specification embodiments could otherwise be mistaken for independent-claim limitations;
- [x] no legal conclusion of novelty, patentability, invalidity, or freedom to operate is asserted.

Before a stable release labels any patent-family/claim fact as authoritative:

- [ ] verify only those exact facts from authoritative patent-office records;
- [ ] otherwise retain them explicitly as public-index working-map information.

This gate is a source-integrity task, not a reason to resume open-ended thermal/fluid modeling.

## Gate E — exact release commit

Status: **IN FINAL CI / ARTIFACT CHECK**

- [x] finish main documentation synchronization;
- [x] reconcile actual executable model count;
- [x] add Actions artifact preservation for the generated reference package;
- [ ] confirm all five workflows pass on the exact candidate commit;
- [ ] confirm the exact-head reference artifact exists and contains generated data, figures, `metadata.json`, and `sha256.txt`;
- [ ] record the selected release commit SHA in release metadata;
- [ ] update `CITATION.cff` version/date;
- [ ] finalize release notes.

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
3. **release metadata/reproducibility** — CI, artifacts, hashes, citation, version, archive information;
4. **new research** — normally deferred to a later version.

The default action for category 4 is **defer**, not expand the current release candidate.

## Stop condition

The current project can stop after a stable version is frozen and the exact public record is identifiable by commit/tag (and optionally archive identifier). Further modeling is not required for closure of this computational research phase.
