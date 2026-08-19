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
- homogenized partial-wetness parameter in the open-valley thermal model;
- explicit feed-limited solver that determines sub-grid wet fraction `beta` from imposed liquid feed;
- latent heat-source partition between body-side heat and ambient sensible heat;
- Lewis-number and Chilton–Colburn-style ordinary heat/mass coupling baselines;
- wet-wall energy-closure, feed-balance, latent-partition, and heat/mass-selectivity regression tests;
- conservative liquid-supply capacity audit retained separately from the explicit partial-wetness state;
- E3b hierarchical air-renewal and E3c open-vs-covered physical protocols;
- E4a feed-limit / wetness-transition physical protocol;
- E18–E21 open-valley / segmented / island / covered-channel implementation variants;
- 2-D anisotropic heat-spreader and normalized nonvolatile water/salt models;
- regression tests and GitHub Actions CI;
- reproducible CSV/PNG/metadata/SHA-256 output package including explicit feed-limited states.

### Corrected

- salt is nonvolatile under garment operating conditions; water evaporates, salt does not;
- earlier most-cooling-root selection is no longer silently used when multiple stable equilibria exist;
- earlier single-value `M` cooling thresholds are historical screening artifacts, not validated design criteria;
- vapor-transfer enhancement is not automatically assigned to sensible heat transfer;
- geometric exterior area is not treated as accessible evaporative area;
- vertical wet corridors are not assumed to produce upward chimney flow;
- nonzero corridor velocity and axial Péclet number are not treated as proof of useful vapor renewal;
- covered/end-renewed corridor results are not generalized directly to laterally open garment valleys;
- 20–50 mm interruption is no longer assumed to provide adequate air renewal when interior lateral exchange remains weak;
- high local vapor-driving-force retention `F` is no longer treated as proof of high evaporation capacity; `k_eff`/evaporation/heater power must also be considered;
- positive evaporation is no longer treated as proof of positive wearer cooling: hot ambient sensible heat can make body-side heat flow negative;
- fully-wet transfer-capacity states are no longer reused after liquid feed becomes limiting;
- supply-limited operation now has a first explicit homogenized partial-wetness state rather than only a capacity/feed flag;
- stronger linked external exchange is no longer assumed always beneficial at fixed feed: once available water is fully consumed, additional ambient sensible heat can reduce body-coupled cooling;
- identical evaporation mass is no longer assumed to imply identical body heat removal;
- arbitrary `Xi<1` heat/vapor decoupling is no longer treated as freely available: ordinary same-boundary Lewis/Chilton–Colburn-style comparisons remain near `Xi≈1` for the current air/water-vapor screen.

### Current research direction

The preferred exterior has narrowed to a hierarchical, continuously/largely laterally open architecture:

- wet micro-ribs / 3D-knit / short-fin texture for local area;
- open valleys, cross-openings and ambient-connected gaps;
- discontinuous evaporator islands;
- millimeter-scale interruptions only as an extreme mechanism test rather than a required apparel dimension;
- routed/anisotropic heat spreading toward wet fields;
- explicit water-supply/wetness-state accounting;
- hot-ambient shielding or thermal routing that limits harmful sensible heat pickup.

The current numerical objective is simultaneous validation of:

1. vapor-renewal quality (`F`);
2. absolute evaporation transfer (`k_eff` / mass flux);
3. signed body-side heat removal;
4. available water supply and wetness state;
5. latent heat-source partition;
6. sensible heat pickup from ambient air;
7. whether any claimed heat/vapor selectivity has an actual physical mechanism.

Next model-strengthening tasks are spatially resolved wet/dry patches and geometry-resolved external natural-convection/cross-flow, followed by re-testing the older lumped multi-equilibrium behavior against that improved external-flow model.

## Verification

- `model-tests` #231 passed at `7f015b8e1b0278f29b545f41d24674b5a394ee79`, covering the coupled open-valley thermal model and preceding stack.
- The feed-limited / analogy integration requires a newer passing CI before being recorded as the next verified integration point.

## Release policy

Stable releases should be tagged and archived without overwriting earlier public records. A stable release should include the frozen technical disclosure, source, reference data, metadata, SHA-256 manifest, version/citation metadata, and release notes.