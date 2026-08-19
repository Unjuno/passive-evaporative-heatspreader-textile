# Research Roadmap

Date: 2026-08-20

## Objective

Develop and publicly document a reproducible passive cooling garment architecture based on heat routing, liquid transport, exterior evaporation, and ambient-air access.

**Current project mode: virtual/computational prototype only. No physical specimen currently exists.**

The immediate objective is therefore to make the design sufficiently concrete that a third party could reproduce the calculations and build/test representative embodiments later. Future physical protocols are retained as implementation specifications, not as active experiments.

## Gate 0 — scope and architecture

Status: **substantially complete**

- [x] primary architecture is fanless/passive;
- [x] core versus optional components separated;
- [x] numbered architecture/layer vocabulary;
- [x] apparel-like exterior design families;
- [x] nonvolatile-salt correction;
- [x] hierarchical/open-valley/island/covered comparison embodiments explicit;
- [x] virtual-prototype status explicitly separated from future physical validation.

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

## Gate 2 — reproducible screening / virtual-prototype model stack

Status: **advanced low-order stack; direct material/contact mapping added; distributed geometry-resolved physics still open**

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
- [x] conservative liquid-supply capacity classification;
- [x] explicit homogenized partial-wetness/feed-limited solution;
- [x] latent heat-source partition between body and ambient air;
- [x] Lewis / Chilton–Colburn-style ordinary heat/mass coupling comparison;
- [x] analytic hot/humid body-heat-flow sign boundary;
- [x] symmetric and asymmetric wet/dry heat-spreader mechanism screens;
- [x] bounded continuation solver for asymmetric `g_mix` sweeps;
- [x] mapping from `g_mix` to `k*t/pitch²`, thickness, mass, simple bending strain and contact burden;
- [x] anisotropic 2-D heat spreading;
- [x] nonvolatile water/salt transport;
- [x] regression tests, CI, reproducible CSV/PNG/metadata/SHA generation.

Next strengthening tasks:

1. resolve wet and dry patches in a distributed 1-D/2-D field with direct `k`, thickness, anisotropy, contact conductance and patch pitch;
2. sweep topology/path factor rather than fixing the ideal periodic-stripe `Gamma=4` mapping;
3. predict lateral external exchange from geometry-resolved 2-D/3-D natural convection/cross-flow;
4. use the improved geometry-resolved flow to constrain heat/vapor transfer rather than only comparing low-order analogies;
5. re-test lumped-model multi-equilibrium behavior against improved external-flow physics;
6. sensitivity to Nu/Sh, compression, contact degradation, openings, external drift, radiative properties, and garment curvature.

## Gate 3 — explicit virtual prototype specifications

Status: **now the primary active gate**

Create several complete computational embodiments rather than one abstract concept.

Each virtual prototype must specify:

- projected active area;
- wet/dry field topology and routing pitch;
- micro-rib / 3D-knit / fin geometry;
- lateral ambient-access geometry;
- water-feed regime and wetness model;
- heat-spreader `k_parallel`, thickness, density, coverage, anisotropy and topology factor;
- wet/dry thermal-contact conductance;
- dry-side ambient sensible coefficient / shielding assumption;
- total added mass and approximate thickness budget;
- all model assumptions and failure conditions.

Initial target families:

### VP-A — short-pitch lightweight spreader

- wet/dry thermal routing pitch: 10 mm class;
- continuously laterally open evaporative valleys/islands;
- high `k/rho` spreader class;
- explicit contact-conductance requirement;
- intended to minimize mass while retaining most modeled spreader gain.

### VP-B — moderate-pitch manufacturability screen

- routing pitch: 20 mm class;
- compare additional thickness/mass burden against VP-A;
- test whether simpler panelization is worth the quadratic `P²` penalty.

### VP-C — sparse/routed-network challenge case

- reduced conductive coverage;
- thickness increased to hold `k*t*c` constant;
- test whether topology actually changes effective path length enough to beat the ideal mass-invariance result.

### VP-D — hot-ambient protected configuration

- dry-side sensible shielding / selective exposure explicit;
- heat/vapor pathway asymmetry explicit;
- tested against the same-path environmental sign boundary.

Gate-3 completion criterion:

- at least 3 virtual prototypes have reproducible input files/tables and are comparable on body-side heat flow, evaporation, water use, mass, thickness, routing/contact burden and hot/humid failure boundary.

## Gate 4 — virtual robustness / apparel constraints

Status: **planned**

Before any hardware exists, screen:

- compression reducing valley opening and thermal contact;
- bending strain and fold radius;
- stretch/serpentine path penalty;
- contact degradation;
- wet/dry cycling and changing wet fraction;
- weak external drift / walking air;
- garment curvature;
- mass and visual thickness;
- topology sensitivity.

## Gate 5 — future physical validation specification

Status: **protocols prepared; not active because no specimen exists**

If a specimen is eventually built, planned order remains:

1. **E1** — B0 flat fast-dry vs B4 integrated architecture.
2. **E2** — B0/B2/B3/B4 ablation.
3. **E3/E3b** — microstructure pitch and ambient-access hierarchy.
4. **E3c** — D1 covered vs O1 continuously open vs O2a centimeter-control vs O2b millimeter segments vs O3 islands.
5. **E4a** — feed-limit / partial-wetness transition at 35 °C / 50% RH.
6. **E4** — 50/70/85% RH environmental mapping with transfer/supply/runoff classification.
7. **E5** — heat-spreader orientation/material/contact validation.
8. **E6** — hot-ambient sensible-heat penalty and shielding.

Minimum future measurement package:

- signed heater/cooler power or calibrated signed heat flux;
- actual liquid feed and >=95% water-balance target;
- wet-surface temperature;
- ambient and local T/RH;
- far-field and local flow where resolvable;
- actual wet area and compressed geometry;
- local renewal `F`;
- evaporation mass flux / inferred `k_eff` where valid;
- measured heat-spreader/contact properties;
- visible or otherwise validated wetness indicator for E4a.

## Gate 6 — stable public release

Status: **public development repository active; stable v1.0 not frozen**

Before stable v1.0:

- [ ] authoritative patent-office verification;
- [ ] freeze disclosure/embodiments at one exact commit;
- [ ] freeze at least 3 explicit virtual prototype input specifications;
- [ ] regenerate all reference outputs at that commit;
- [ ] freeze SHA-256 manifest;
- [ ] update `CITATION.cff`, version/date, changelog, release notes;
- [ ] create GitHub tag/release;
- [ ] archive exact release in a persistent public DOI repository;
- [ ] preserve earlier public records without overwrite.

## Current research priorities

### P0 — concrete virtual prototypes

Replace abstract mechanism parameters with reproducible geometry/property inputs.

Current most important conversion:

\[
g_{sheet}\approx \Gamma\frac{k_{\parallel}tc}{P^2}
\]

plus

\[
\frac{1}{g_{eff}}=\frac{1}{g_{sheet}}+\frac{2}{h_c}.
\]

The next virtual prototypes should therefore prioritize short routing pitch, high `k/rho`, explicit contact and dry-side shielding.

### P1 — passive exterior physics

Current rejected shortcuts:

- geometric area alone is enough;
- long wet vertical channels guarantee useful chimney renewal;
- high axial Péclet number proves renewal;
- 20–50 mm segmentation is sufficient;
- high `F` proves high evaporation capacity;
- positive evaporation proves body cooling;
- modeled fully-wet transfer capacity above water feed is achievable at fixed feed;
- stronger external exchange is always better at fixed feed;
- arbitrary heat/vapor decoupling is physically available without a separate mechanism.

Current hypothesis:

> continuously ambient-connected wet microtexture with enough vapor conductance to use available sweat, limited harmful sensible heat pickup, explicit liquid-supply state, and short-range body-to-wet-zone heat routing through a quantified material/contact path.

### P2 — heat-routing integration

Current findings:

- symmetric wet/dry boundary conditions produce little or no global heat-spreader gain even if local temperatures equalize;
- asymmetric wet/dry exposure creates a finite spreader benefit;
- corrected low-order screens show diminishing returns in the few-hundred-W/(m² K) `g_mix` range;
- required `k*t` grows as routing pitch squared;
- sparse coverage alone does not reduce idealized mass when `t*c` controls conductance;
- contact resistance can dominate a high-conductivity sheet.

### P3 — failure boundaries

Map high humidity, hot ambient air, supply limitation, partial wetness, inward sensible heat, flow reversal, stagnant humidity layers, compression-closing of ambient paths, contact degradation and long routing distances.

### P4 — apparel viability in silico

Weight, thickness, bending strain, routing density, panel dimensions, visual bulk and compatibility with seams/3D-knit patterns.

## Stop / redesign conditions

A virtual architecture should be downgraded if it:

- improves vapor renewal but not signed body-side cooling in the integrated model;
- increases evaporation while net body heat flow becomes adverse;
- gets high `F` by reducing absolute transfer;
- depends on unavailable liquid supply;
- loses body-coupled cooling after feed saturation because ambient sensible heat dominates;
- requires heat/vapor selectivity far beyond ordinary transport without an identified mechanism;
- requires `g_mix` that maps to impractical thickness/mass at the chosen routing pitch;
- requires thermal contact far above the stated integration assumption;
- assumes sparse conductive coverage automatically reduces mass;
- depends on a flow direction that reverses;
- loses ambient paths under expected compression/curvature.

Negative numerical results remain part of the public technical record.
