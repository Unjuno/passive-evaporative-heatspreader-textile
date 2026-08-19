# Research Roadmap

Date: 2026-08-20

## Objective

Develop and publicly document a reproducible passive cooling garment architecture based on heat routing, liquid transport, exterior evaporation, and ambient-air access. Falsification of the cooling premise takes priority over optimization for durability, appearance, or manufacturing.

## Gate 0 — scope and architecture

Status: **substantially complete**

- [x] primary architecture is fanless/passive;
- [x] core versus optional components separated;
- [x] numbered architecture/layer vocabulary;
- [x] apparel-like exterior design families;
- [x] nonvolatile-salt correction;
- [x] hierarchical/open-valley/island/covered comparison embodiments explicit.

## Gate 1 — prior-art map

Status: **in progress**

- [x] directional liquid transport;
- [x] evaporative textiles;
- [x] humidity-responsive ventilation;
- [x] heat-conductive/cooling textiles;
- [x] fan/sorbent garment families at working-note level;
- [x] 3D-knit/pile/fin adjacent structures;
- [x] close integrated heat-conductive + sweat-transport work acknowledged;
- [ ] authoritative patent-office family/claim mapping;
- [ ] final source-by-source difference table.

## Gate 2 — reproducible screening model stack

Status: **advanced low-order stack complete; higher-fidelity external flow open**

Completed:

- [x] nonlinear lumped heat/mass balance and multi-root audit;
- [x] separate sensible/vapor transfer (`M_h`, `M_m`);
- [x] deterministic model-form sensitivity;
- [x] periodic E3 rib vapor diffusion;
- [x] prescribed thermo-solutal corridor buoyancy;
- [x] self-consistent covered/end-renewed corridor T/RH/flow;
- [x] local open-valley `R/F` target and measurement inversion;
- [x] distributed open-valley axial diffusion/advection + lateral vapor renewal;
- [x] exchange-length / centimeter-segmentation audit;
- [x] `F` versus absolute `k_eff` audit;
- [x] coupled open-valley wet-wall / air heat / vapor model;
- [x] explicit liquid-supply capacity classification;
- [x] anisotropic 2-D heat spreading;
- [x] nonvolatile water/salt transport;
- [x] regression tests, CI, reproducible CSV/PNG/metadata/SHA generation.

Next strengthening tasks:

1. physically constrain heat/mass exchange coupling instead of freely varying `delta_heat` and `delta_vapor`;
2. add a wetting/dryout state model for supply-limited cases rather than only a capacity flag;
3. predict lateral exchange from geometry-resolved 2-D/3-D natural convection/cross-flow;
4. re-test lumped-model multi-equilibrium behavior against improved external-flow physics;
5. sensitivity to Nu/Sh, compression, openings, external drift, and garment curvature.

## Gate 3 — minimum bench validation

Status: **not started physically; protocols prepared**

Priority:

1. **E1** — B0 flat fast-dry vs B4 integrated architecture.
2. **E2** — B0/B2/B3/B4 ablation.
3. **E3/E3b** — microstructure pitch and ambient-access hierarchy.
4. **E3c** — D1 covered vs O1 continuously open vs O2a centimeter-control vs O2b millimeter segments vs O3 islands.
5. **E4** — 50/70/85% RH with supply-limit classification.
6. **E5** — heat-spreader orientation.
7. **E6** — hot-ambient sensible-heat penalty and shielding.

Minimum measurement package:

- heater power at fixed artificial-skin temperature;
- actual liquid feed and >=95% water-balance target;
- wet-surface temperature;
- ambient and local T/RH;
- far-field and local flow where resolvable;
- actual wet area and compressed geometry;
- local renewal `F`;
- evaporation mass flux / inferred `k_eff` where valid.

## Gate 4 — textile/mechanical validation

Status: **not started**

Compression recovery, stretch, bending, laundering, wet/dry cycling, abrasion, snagging, contamination, salt exposure, silhouette, and wearer-contact safety.

## Gate 5 — apparel design optimization

Status: **concept stage, narrowed**

Current preferred family:

- low-profile micro-rib / 3D-knit wet fields;
- continuously ambient-connected valleys or gaps;
- cross-openings and discontinuous islands;
- millimeter-scale interruption only where practical, not as a universal requirement;
- heat-routing patterns integrated into seams/stripes/panels;
- dry-side shielding in hot ambient conditions.

Do **not** rank designs by geometric area, local `F`, airflow, or evaporation alone. Compare at matched water input/wet area using:

1. renewal quality `F`;
2. absolute vapor transfer / evaporation;
3. heater-power body cooling;
4. ambient sensible heat pickup;
5. mass/compression/wearability.

## Gate 6 — stable public release

Status: **public development repository active; stable v1.0 not frozen**

Before stable v1.0:

- [ ] authoritative patent-office verification;
- [ ] freeze disclosure/embodiments at one exact commit;
- [ ] regenerate all reference outputs at that commit;
- [ ] freeze SHA-256 manifest;
- [ ] update `CITATION.cff`, version/date, changelog, release notes;
- [ ] create GitHub tag/release;
- [ ] archive exact release in a persistent public DOI repository;
- [ ] preserve earlier public records without overwrite.

## Current research priorities

### P0 — product premise

Does B4 remove measurably more body heat than B0 at equal water input?

### P1 — passive exterior physics

Current rejected shortcuts:

- geometric area alone is enough;
- long wet vertical channels guarantee useful chimney renewal;
- high axial Péclet number proves renewal;
- 20–50 mm segmentation is sufficient;
- high `F` proves high evaporation capacity;
- positive evaporation proves body cooling;
- modeled transfer capacity above water feed is achievable at fixed feed.

Current hypothesis:

> continuously ambient-connected wet microtexture with sufficient vapor conductance, controlled sensible heat pickup, and strong body-to-wet-zone heat routing.

### P2 — integration

Use ablation and heat-spreader orientation to determine whether the gain is truly integrated rather than dominated by one component.

### P3 — failure boundaries

Map high humidity, hot ambient air, supply limitation, inward sensible heat, flow reversal, stagnant humidity layers, and compression-closing of ambient paths.

### P4 — garment viability

Mechanical durability, washability, snag resistance, visual bulk, mass, and textile manufacturability.

## Stop / redesign conditions

Substantial redesign is required if controlled tests show the integrated architecture gives <5 W over B0 at the primary condition and neither ambient-access topology nor heat routing provides a reproducible mechanism benefit.

Retire a specific exterior geometry if it:

- improves vapor renewal but not heater-power cooling;
- increases evaporation while net body heat flow becomes adverse;
- gets high `F` by reducing absolute transfer;
- depends on unavailable liquid supply;
- depends on a flow direction that reverses;
- loses its ambient paths under ordinary compression/wear.

Negative results remain part of the public technical record.
