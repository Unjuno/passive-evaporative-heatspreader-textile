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
- separate-temperature wet/dry two-node model with lateral heat-spreader mixing conductance;
- asymmetric wet/dry spreader screen with dry-side shielding/exposure as an explicit spatial heterogeneity;
- bounded least-squares + continuation support for the asymmetric partial-wetness solver;
- low-order heat-spreader material/geometry mapping `g_sheet ~ Gamma*k*t*c/P^2`;
- heat-spreader mass/thickness/bending-strain screening and `k/rho` mass figure of merit;
- two-contact thermal-resistance audit `1/g_eff = 1/g_sheet + 2/h_contact`;
- Lewis-number and Chilton–Colburn-style ordinary heat/mass coupling baselines;
- wet-wall energy-closure, feed-balance, latent-partition, wet/dry, asymmetric-branch, material/contact-mapping, and heat/mass-selectivity regression tests;
- conservative liquid-supply capacity audit retained separately from the explicit partial-wetness state;
- E3b hierarchical air-renewal and E3c open-vs-covered future physical protocols;
- E4a feed-limit / wetness-transition future physical protocol;
- E18–E21 open-valley / segmented / island / covered-channel implementation variants;
- 2-D anisotropic heat-spreader and normalized nonvolatile water/salt models;
- regression tests and GitHub Actions CI;
- reproducible CSV/PNG/metadata/SHA-256 output package including feed-limited, wet/dry, asymmetric and spreader material/contact screens.

### Corrected

- repository status now explicitly states that the current project is a **virtual/computational prototype only** and no physical specimen exists;
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
- arbitrary `Xi<1` heat/vapor decoupling is no longer treated as freely available: ordinary same-boundary Lewis/Chilton–Colburn-style comparisons remain near `Xi≈1` for the current air/water-vapor screen;
- lateral heat spreading is no longer credited with a global cooling gain in a spatially symmetric fixed-feed system;
- dense asymmetric `g_mix` sweeps no longer rely on an unconstrained nonlinear root that could jump to a nonphysical high-beta branch;
- infinite heat-spreader conductivity is no longer treated as a useful target: corrected asymmetric sweeps show finite few-hundred-W/(m² K) diminishing-return bands;
- sparse conductive coverage is no longer assumed to reduce mass under the linear `t*c` conductance model;
- sheet conductivity is no longer treated as sufficient without explicit wet/dry thermal-contact conductance;
- heat-spreader performance is no longer stated without routing pitch/topology/material/contact assumptions.

### Current research direction

The preferred virtual architecture has narrowed to:

- wet micro-ribs / 3D-knit / short-fin texture for local area;
- open valleys, cross-openings and ambient-connected gaps;
- discontinuous evaporator islands;
- millimeter-scale interruptions only as an extreme mechanism test rather than a required apparel dimension;
- short-range routed/anisotropic heat spreading toward **spatially nonuniform** wet/exposed regions;
- initial virtual-prototype heat-routing pitch around 10–20 mm rather than long-range uniform spreading;
- high `k/rho` pathways with explicit `k*t/P²` accounting;
- explicit wet/dry thermal-contact resistance;
- explicit water-supply/wetness-state accounting;
- hot-ambient shielding or thermal routing that limits harmful sensible heat pickup.

The current numerical objective is simultaneous validation of:

1. vapor-renewal quality (`F`);
2. absolute evaporation transfer (`k_eff` / mass flux);
3. signed body-side heat removal;
4. available water supply and wetness state;
5. latent heat-source partition;
6. sensible heat pickup from ambient air;
7. whether heat spreading connects genuinely different local boundary conditions;
8. whether any claimed heat/vapor selectivity has an actual physical mechanism;
9. whether a proposed spreader has sufficient `k*t/P²` and thermal contact at acceptable added mass.

Next model-strengthening tasks are a distributed wet/dry field with direct material `k`, thickness, anisotropy and contact terms, then geometry-resolved external natural-convection/cross-flow followed by re-testing the older lumped multi-equilibrium behavior.

## Verification

- `model-tests` #370 passed at `a01eeafc8ae6814349a3a0937251efd048823dae`, covering the expanded feed-limited / wet-dry / asymmetric stack before the latest material-mapping commits.
- The current material/contact-mapping integration requires a newer passing CI before being recorded as the next verified integration point.

## Release policy

Stable releases should be tagged and archived without overwriting earlier public records. A stable release should include the frozen technical disclosure, source, reference data, metadata, SHA-256 manifest, version/citation metadata, and release notes.
