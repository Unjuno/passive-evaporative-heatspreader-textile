# Research Roadmap

Date: 2026-08-20

## Objective

Develop and publicly document a reproducible passive cooling garment architecture based on local sweat collection, short liquid transport, exterior evaporation, pressure-aware heat routing and explicit hot/humid failure boundaries.

**Current project mode: virtual/computational prototype only. No physical specimen currently exists.**

The immediate objective is to make the architecture sufficiently concrete that a third party could reproduce the calculations and later build/test representative embodiments. Physical protocols are retained as implementation specifications, not completed experiments.

## Gate 0 — scope and architecture

Status: **substantially complete**

- [x] fanless/passive baseline;
- [x] core versus optional components separated;
- [x] layer/architecture vocabulary;
- [x] apparel-like exterior design families;
- [x] nonvolatile-salt correction;
- [x] virtual-prototype status separated from future physical validation.

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

## Gate 2 — reproducible model stack

Status: **advanced low-order stack with direct geometry/material bridges**

Completed:

- [x] nonlinear heat/mass balances and multi-root audit;
- [x] separate sensible/vapor transfer;
- [x] periodic rib diffusion and corridor buoyancy screens;
- [x] open-valley ambient-renewal target and distributed 1-D model;
- [x] feed-limited/partial-wetness state;
- [x] latent heat-source partition;
- [x] hot/humid signed body-heat-flow boundary;
- [x] symmetric/asymmetric heat-spreader screens;
- [x] direct `k*t` distributed 1-D heat routing;
- [x] explicit 2-D heat-network topology;
- [x] material/mass/contact mapping;
- [x] compression/contact/ambient-path regime screen;
- [x] spatial pressure maps;
- [x] capillary transport, lift/radius optimum and blockage/radius-collapse screens;
- [x] nonvolatile water/salt mass balance;
- [x] regression tests, CI and reference CSVs.

Still open:

1. geometry-resolved 3-D exterior natural convection/cross-flow;
2. branched liquid-network solve coupled directly to terminal placement;
3. local wall-film salt deposition and progressive radius loss;
4. measured or independently validated constitutive laws if hardware is ever built.

## Gate 3 — explicit virtual prototypes

Status: **advanced**

VP-A through VP-D remain mechanism anchors for routing pitch, mass/contact burden and hot-ambient shielding.

### VP-E — current integrated design anchor

VP-E combines:

- directed heat routing with limited cross-link redundancy (`lambda`-like heat-route blend near 0.125);
- distributed local liquid cells rather than a garment-scale central wick;
- pressure-aware exterior terminals;
- fixed passive terminal placement rather than active switching as baseline;
- dry-side shielding in hot ambient conditions;
- explicit nonvolatile-salt handling;
- mass/thickness BOM screen.

The terminal-placement rule is now a **thermal/liquid co-design**, not a pure thermal optimum.

At the converged 24 x 24 backpack+straps reference:

- thermal-only optimum: `beta=0`, route weight `0.20`, `q_body≈112.84 W/m²`, liquid `d95≈20.16 mm`;
- co-design anchor: `beta=0.125`, route weight `0.35`, `q_body≈110.83 W/m²`, liquid `d95≈16.77 mm`.

The co-design anchor retains ~98.21% of modeled thermal performance while reducing the same protected-trunk hydraulic proxy by ~16.79%.

Gate-3 completion criterion:

- [x] at least three explicit virtual prototypes;
- [x] integrated VP-E heat/liquid/terminal architecture;
- [x] screening mass/thickness budget;
- [x] hot/humid state maps at low-order resolution;
- [ ] freeze one reproducible VP-E input manifest for release.

## Gate 4 — virtual robustness / apparel constraints

Status: **advanced; no longer merely planned**

Completed screens:

- [x] compression vs terminal contact / ambient access;
- [x] bending/serpentine stretch burden;
- [x] local heat-route fracture;
- [x] contact degradation;
- [x] changing wet-terminal maps;
- [x] synthetic backpack/strap/seat pressure maps;
- [x] protected under-load vapor-gap floor;
- [x] support-footprint penalty;
- [x] pressure-linked liquid-channel radius-collapse sensitivity;
- [x] localized and distributed damage comparisons;
- [x] virtual garment BOM range screen;
- [x] pressure-aware heat/liquid terminal co-design.

Remaining:

- [ ] garment curvature and seam placement;
- [ ] regional full-garment load map instead of one repeating tile;
- [ ] time-dependent wet-source migration rather than quasisteady snapshots;
- [ ] explicit branched liquid network with shared trunks and local collectors;
- [ ] resolved protected-gap geometry instead of an effective air-access factor.

## Gate 5 — future physical validation specification

Status: **protocols prepared; not active because no specimen exists**

If a specimen is eventually built, planned order remains:

1. E1 — flat fast-dry baseline vs integrated architecture;
2. E2 — layer ablation;
3. E3/E3b — microstructure pitch and ambient-access hierarchy;
4. E3c — covered vs continuously open vs segmented/island exterior;
5. E4a — feed-limit / partial-wetness transition;
6. E4 — humidity mapping with water-balance classification;
7. E5 — heat-route orientation/material/contact validation;
8. E6 — hot-ambient sensible-heat penalty and shielding;
9. new pressure validation — loaded terminal air-access/contact mapping;
10. new hydraulic validation — local collector/trunk pressure drop and collapse.

Minimum future measurement package:

- signed heat flux or calibrated heater/cooler power;
- actual liquid feed and >=95% water-balance target;
- wet-surface temperature;
- ambient/local T/RH;
- local/far-field flow where resolvable;
- compressed geometry and terminal gap;
- actual wet area;
- heat-route/contact properties;
- liquid pressure drop / trunk geometry;
- salt concentration/deposition where relevant.

## Gate 6 — stable public release

Status: **public development repository active; stable v1.0 not frozen**

Before stable v1.0:

- [ ] authoritative patent-office verification;
- [ ] freeze technical disclosure and VP-E input manifest at one exact commit;
- [ ] regenerate all reference outputs at that commit;
- [ ] obtain successful current-head model/topology/pressure/liquid workflows;
- [ ] freeze SHA-256 manifest;
- [ ] update `CITATION.cff`, version/date, changelog and release notes;
- [ ] create GitHub tag/release;
- [ ] archive exact release in a persistent public DOI repository;
- [ ] preserve earlier public records without overwrite.

## Current research priorities

### P0 — replace the co-design proxy with an explicit liquid network

Current pressure/liquid co-design uses

\[
J_h=d_{95}\hat r^{-4}
\]

as a first-order common metric. Next step is a graph/network solve where collector, trunk and terminal topology are explicit and pressure-dependent.

### P1 — exterior vapor-gap geometry

Replace the effective protected-air-access floor with gap height, width, support spacing, orientation and deformation.

### P2 — salt / local-film failure

Keep salt vapor flux at zero and model water evaporation, dissolved-salt advection, local concentration, precipitation/dissolution and hydraulic-radius loss separately.

### P3 — garment regionalization

Map backpack straps, back panels, waistbands, seams and seat contact onto a garment-scale regional model, then assign pressure-aware terminals and local liquid cells.

### P4 — release consistency

Keep README, simulation index, audit, current-results, workflow counts, references and PR description synchronized before freezing a stable release.

## Stop / redesign conditions

A virtual architecture should be downgraded if it:

- improves evaporation but not signed body-side cooling;
- depends on unavailable water supply;
- requires long central liquid lift when local routing is feasible;
- moves terminals so far from liquid sources that hydraulic burden offsets pressure benefit;
- requires vapor-gap preservation incompatible with expected compression;
- depends on heat/vapor selectivity without a physical mechanism;
- maps required heat routing to impractical mass/thickness/contact burden;
- assumes sparse conductive coverage automatically saves mass;
- assumes salt evaporates;
- loses ambient paths or liquid radius under expected load without redundancy/protection.
