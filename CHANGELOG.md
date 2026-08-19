# Changelog

All notable research-record changes are documented here.

## Unreleased

### Added

- integrated README, citation metadata, architecture, embodiment matrix, design history, roadmap, experiment plan, prior-art notes, and repository audit;
- nonlinear passive heat/mass model with explicit multi-equilibrium reporting;
- split sensible/vapor transfer model (`M_h`, `M_m`) and deterministic sensitivity grid;
- periodic 2-D E3 rib vapor-diffusion model and grid-convergence checks;
- prescribed-state thermo-solutal corridor buoyancy model;
- self-consistent covered/end-renewed 1-D corridor T/RH/flow/evaporation model;
- local open-valley renewal target and T/RH measurement inversion using `R` and `F`;
- distributed open-valley vapor model with axial diffusion/advection and distributed lateral renewal;
- exchange-length calculation and centimeter-scale segmentation audit;
- absolute series vapor-conductance metric `k_eff = k_w k_a/(k_w+k_a)`;
- coupled open-valley thermal/vapor model solving valley T, vapor density, wet-surface T, evaporation and body-side heat flow;
- wet-wall energy-closure regression test;
- explicit liquid-supply capacity audit separating fully-wet transfer capacity from available feed without inventing a dryout temperature field;
- E3b hierarchical air-renewal and E3c open-vs-covered physical protocols;
- E18–E21 open-valley / segmented / island / covered-channel implementation variants;
- 2-D anisotropic heat-spreader and normalized nonvolatile water/salt models;
- regression tests and GitHub Actions CI;
- reproducible CSV/PNG/metadata/SHA-256 output package.

### Corrected

- salt is nonvolatile under garment operating conditions; water evaporates, salt does not;
- earlier most-cooling-root selection is no longer silently used when multiple stable equilibria exist;
- earlier single-value `M` cooling thresholds are historical screening artifacts, not validated design criteria;
- vapor-transfer enhancement is not automatically assigned to sensible heat transfer;
- geometric exterior area is not treated as accessible evaporative area;
- vertical wet corridors are not assumed to produce upward chimney flow;
- nonzero corridor velocity and axial Péclet number are not treated as proof of useful vapor renewal;
- covered/end-renewed corridor results are not generalized directly to laterally open garment valleys;
- 20–50 mm interruption is no longer assumed to provide adequate air renewal when the interior lateral exchange remains weak;
- high local vapor-driving-force retention `F` is no longer treated as proof of high evaporation capacity; `k_eff`/evaporation/heater power must also be considered;
- positive evaporation is no longer treated as proof of positive wearer cooling: hot ambient sensible heat can make body-side heat flow negative;
- transfer-capacity evaporation above the available liquid feed is explicitly classified as supply-limited and the fully-wet thermal state is not reused as a feed-limited prediction.

### Current research direction

The preferred exterior has narrowed to a hierarchical, continuously/largely laterally open architecture:

- wet micro-ribs / 3D-knit / short-fin texture for local area;
- open valleys, cross-openings and ambient-connected gaps;
- discontinuous evaporator islands;
- millimeter-scale interruptions only as an extreme mechanism test rather than a required apparel dimension;
- routed/anisotropic heat spreading toward wet fields;
- hot-ambient shielding or thermal routing that limits harmful sensible heat pickup.

The current numerical objective is no longer just air renewal. It is simultaneous optimization/validation of:

1. vapor-renewal quality (`F`);
2. absolute evaporation transfer (`k_eff` / mass flux);
3. body-side heat removal;
4. available water supply;
5. sensible heat pickup from ambient air.

Next model-strengthening tasks are a physically constrained heat/mass coupling baseline, an explicit wetting/dryout treatment for supply-limited cases, and geometry-resolved external natural-convection/cross-flow.

## Verification

- `model-tests` #231 passed at `7f015b8e1b0278f29b545f41d24674b5a394ee79`, covering the coupled open-valley thermal model and preceding stack.
- Later supply-audit and documentation commits require a newer passing CI before being recorded as the next verified integration point.

## Release policy

Stable releases should be tagged and archived without overwriting earlier public records. A stable release should include the frozen technical disclosure, source, reference data, metadata, SHA-256 manifest, version/citation metadata, and release notes.
