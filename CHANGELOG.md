# Changelog

All notable research-record changes will be documented here.

## Unreleased

### Added

- integrated project README and citation metadata;
- technical disclosure with primary and optional embodiments;
- research roadmap and staged experiment plan;
- prior-art map with close adjacent literature explicitly acknowledged;
- governing equations and variable/unit definitions;
- passive exterior rib screening model;
- explicit multi-equilibrium detection and conservative/optimistic branch reporting;
- periodic 2-D E3 rib vapor-diffusion model with grid-convergence checks;
- hierarchical microstructure + macro air-renewal embodiment and E3b experiment protocol;
- split sensible-heat / vapor-transfer model using independent `M_h` and `M_m` multipliers;
- regression test proving the split model reduces to the older coupled model when `M_h = M_m`;
- deterministic model-form sensitivity sweep over RH, `U_body`, radiation, `M_h`, and `M_m`;
- model-form uncertainty framework distinguishing screening-grid fractions from probabilities;
- low-order moist-air vertical-corridor buoyancy screen with neutral-density analysis and regression tests;
- corridor buoyancy outputs in the reproducible reference package;
- regression tests and GitHub Actions workflow;
- experiment, data, and figure conventions;
- embodiment matrix and design-history record;
- consolidated numerical-results summary;
- reference equilibrium branch CSV;
- reproducible reference-output generator with CSV/PNG/metadata/SHA-256 artifacts;
- repository audit checklist with P0/P1/P2/P3 queues.

### Corrected

- clarified that sweat salts are nonvolatile under garment operating conditions;
- removed any interpretation that salt is removed by evaporation;
- corrected earlier screening practice that silently selected the most-cooling stable equilibrium when multiple stable roots coexist;
- downgraded earlier single-value `M` cooling thresholds from design conclusions to exploratory model artifacts pending validation;
- corrected the assumption that a vapor-transfer enhancement must produce the same multiplier in sensible convective heat transfer;
- clarified that E3 outputs are vapor mass-transfer multipliers, not cooling wattages or measured effective-area factors;
- clarified that deterministic sensitivity-grid fractions are not reliability estimates or statistical confidence levels;
- corrected the design intuition that a vertical wet corridor must generate upward chimney flow: evaporative cooling and humidification can oppose each other, so the buoyancy direction can reverse or become near-neutral.

### Current research direction

The exterior architecture has shifted from a single-scale dense rib field toward a hierarchical structure combining wet micro-ribs / 3D-knit features with larger open corridors, valleys, spacer paths, or discontinuous fields for air renewal.

The first explicit corridor model now screens moist-air buoyancy direction and laminar slot-flow scaling with prescribed channel temperature/RH. The next major numerical task is a self-consistent channel model that solves flow, heat, and water-vapor conservation together and thereby constrains both `M_h` and `M_m`.

## Release policy

Stable releases should be tagged, archived without overwriting earlier releases, and accompanied by a frozen technical disclosure, reproducible code/data, release notes, and checksums where practical.
