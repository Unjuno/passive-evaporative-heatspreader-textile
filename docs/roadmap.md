# Research Roadmap

Date: 2026-08-19

## Objective

Develop and publicly document a reproducible passive cooling garment architecture based on coupled heat spreading, liquid transport, exterior evaporation, and ambient-air access. The roadmap prioritizes falsification of the core cooling premise before durability, aesthetic, or manufacturing optimization.

## Gate 0 — Scope freeze

Status: **substantially complete**

- [x] Primary architecture is passive and does not require an onboard fan.
- [x] Core elements separated from optional embodiments.
- [x] Numbered architecture/layer vocabulary documented.
- [x] Exterior design treated as apparel texture rather than exposed machine hardware.
- [x] Salt transport corrected: water evaporates; nonvolatile salts do not.
- [x] Hierarchical exterior family recorded.
- [x] Laterally open valleys, segmented valleys, discontinuous islands, and covered/end-renewed corridors made explicit as distinct embodiments.

## Gate 1 — Prior-art map

Status: **in progress**

- [x] directional sweat/liquid transport;
- [x] evaporative cooling textiles;
- [x] humidity-responsive garment ventilation;
- [x] heat-conductive/cooling textiles;
- [x] broad fan/sorbent garment families recorded at working-note level;
- [x] 3D-knit/pile/fin adjacent structures recorded at working-note level;
- [x] close integrated heat-conductive + sweat-transport work acknowledged;
- [ ] authoritative patent-office claim mapping of closest families;
- [ ] final source-by-source difference table for stable release.

Deliverables: `docs/prior-art.md`, `docs/patent-notes.md`, and stable-release claim-oriented verification.

## Gate 2 — Reproducible screening model stack

Status: **substantially complete at low-order/screening level**

Completed:

- [x] nonlinear passive heat/mass balance with multi-equilibrium audit;
- [x] separate sensible and vapor multipliers `M_h` / `M_m`;
- [x] deterministic model-form sensitivity ranges;
- [x] periodic 2-D rib vapor-diffusion / boundary-layer-sharing model;
- [x] anisotropic 2-D heat-spreader model;
- [x] nonvolatile water/salt transport screen;
- [x] prescribed-state moist-air corridor buoyancy screen;
- [x] self-consistent 1-D covered/end-renewed corridor screen;
- [x] regression tests;
- [x] GitHub Actions CI;
- [x] reproducible CSV/PNG/metadata/SHA generator.

Open model-strengthening tasks:

- [ ] distributed lateral ambient exchange for an open exterior valley;
- [ ] axial diffusion / 2-D advection-diffusion for low-Pe corridors;
- [ ] geometry-specific Nu/Sh and entrance/opening-loss sensitivity;
- [ ] constrain the physical relationship between `M_h` and `M_m` from improved external-flow physics;
- [ ] re-test nonlinear equilibrium behavior after improved boundary-layer coupling.

## Gate 3 — Minimum bench validation

Status: **not started physically; protocols prepared**

Priority sequence:

1. **E1:** B0 flat fast-dry control vs B4 integrated architecture.
2. **E2:** B0/B2/B3/B4 ablation.
3. **E3/E3b:** micro-rib pitch and hierarchical air-renewal comparison.
4. **E3c:** covered/end-renewed duct vs laterally open valley vs segmented valley/islands.
5. **E4:** humidity limit at 50/70/85% RH.
6. **E5:** heat-spreader orientation.
7. **E6:** hot-ambient dry-side shielding and sensible-heat penalty.

The first physical objective is a controlled artificial-skin experiment, not a wearable human trial.

### Minimum measurement package

- heater power at fixed artificial-skin temperature;
- actual liquid feed and water balance;
- surface temperature;
- ambient T/RH and far-field air speed;
- near-surface and corridor/valley T/RH;
- signed local flow direction/magnitude where resolvable;
- actual wet area and compressed geometry.

## Gate 4 — Mechanical and textile validation

Status: **not started**

- compression recovery;
- bending and stretch;
- wash durability;
- wetting recovery after drying;
- contamination and salt exposure;
- snagging and abrasion;
- visual thickness/silhouette;
- wearer-contact safety.

## Gate 5 — Apparel design optimization

Status: **concept stage with narrowed direction**

Current preferred visual/functional family:

- low-profile micro-rib or 3D-knit wet fields;
- laterally open valleys integrated as stripes/seams/panel boundaries;
- short segmented valleys and cross-openings;
- discontinuous evaporator islands;
- anisotropic or patterned heat-routing paths aligned to wet fields;
- shielding of dry conductive regions in hot ambient conditions.

Compare alternatives at similar projected area, wet area, mass, and compression state rather than by geometric surface area alone.

## Gate 6 — Stable public release

Status: **public development repository active; stable release not frozen**

Before stable v1.0:

- [ ] complete authoritative prior-art/patent-office verification;
- [ ] freeze technical disclosure and embodiment matrix at one exact commit;
- [ ] freeze source code and reference inputs;
- [ ] regenerate all reference outputs at the exact release commit;
- [ ] generate/freeze SHA-256 manifest;
- [ ] update `CITATION.cff`, version/date, changelog, and release notes;
- [ ] create GitHub release/tag;
- [ ] archive the exact release in a persistent public repository/DOI service;
- [ ] never overwrite older public release records.

## Current research priorities

### P0 — Does the integrated architecture beat a normal fast-dry textile?

Primary physical metric: artificial-skin heater-power difference at equal water input.

### P1 — Can the exterior maintain vapor driving force without a fan?

The numerical record now rejects two overly simple assumptions:

- geometric area alone is sufficient;
- a long vertical wet corridor automatically produces useful chimney renewal.

The current hypothesis is a laterally open/segmented ambient-access topology. E3c is the direct physical discriminator.

### P2 — Is the gain due to integration rather than one component?

Use B2/B3/B4 ablation and heat-spreader orientation tests.

### P3 — Where does passive operation fail or reverse?

Map:

- high humidity;
- hot ambient air;
- inward sensible heat pickup;
- weak/reversed buoyancy flow;
- compression closing open paths.

### P4 — Can the architecture survive clothing mechanics and remain visually acceptable?

Stretch, compression, washing, abrasion, repeated wet/dry cycles, snag resistance, and normal apparel silhouette.

## Stop / redesign conditions

Substantial redesign is required if controlled tests show all of the following:

- integrated B4 gains <5 W over flat B0 under the primary condition;
- open/segmented ambient-access geometries do not measurably reduce local humidity or improve useful cooling;
- heat spreading adds mass/stiffness without measurable body-side benefit;
- passive high-humidity operation provides no useful advantage within wearable geometry.

A specific exterior concept should be retired even if the whole project continues when:

- it increases airflow but increases net inward sensible heat;
- it relies on a flow direction that reverses under relevant conditions;
- its apparent benefit is explained by unequal water input or wet area;
- compression or normal clothing contact closes its intended air paths.

Negative results remain part of the technical record.
