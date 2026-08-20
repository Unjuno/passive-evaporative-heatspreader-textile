# Documentation index

This repository is in **research-freeze / release-preparation mode**. The computational exploration phase is considered sufficient for the present public technical record. No physical garment or bench specimen exists, and no measured garment-performance claim is made.

## Start here

1. [`technical-disclosure.md`](technical-disclosure.md) — integrated technical disclosure and implementation families.
2. [`current-results.md`](current-results.md) — canonical numerical findings, corrections, failure boundaries, and limitations.
3. [`architecture.md`](architecture.md) — system architecture and subsystem interfaces.
4. [`embodiment-matrix.md`](embodiment-matrix.md) — concrete implementation combinations.
5. [`../AUDIT.md`](../AUDIT.md) — repository consistency, verification status, and remaining release blockers.
6. [`research-freeze.md`](research-freeze.md) — what is frozen, what is optional future work, and what remains before a stable release.

## Reproducibility

- [`../simulations/README.md`](../simulations/README.md) — indexed executable model stack.
- [`../data/README.md`](../data/README.md) — reference datasets and interpretation rules.
- [`experiment-plan.md`](experiment-plan.md) — future physical validation specification only; no physical experiment is represented as completed.
- [`measurement-uncertainty-budget.md`](measurement-uncertainty-budget.md) — measurement framework for any future bench work.

## Design and engineering notes

### Exterior heat / vapor transfer

- [`e3-boundary-layer-screen.md`](e3-boundary-layer-screen.md)
- [`corridor-buoyancy-screen.md`](corridor-buoyancy-screen.md)
- [`self-consistent-corridor-model.md`](self-consistent-corridor-model.md)
- [`open-valley-thermal-model.md`](open-valley-thermal-model.md)
- [`feed-limited-open-valley.md`](feed-limited-open-valley.md)
- [`passive-environment-boundary.md`](passive-environment-boundary.md)

### Heat routing and apparel robustness

- [`distributed-spreader-1d.md`](distributed-spreader-1d.md)
- [`spreader-topology-2d.md`](spreader-topology-2d.md)
- [`heat-network-topology-2d.md`](heat-network-topology-2d.md)
- [`heat-network-apparel-robustness.md`](heat-network-apparel-robustness.md)
- [`heat-network-combined-failure.md`](heat-network-combined-failure.md)
- [`audit-heat-network-topology.md`](audit-heat-network-topology.md)

### Pressure, terminals, and garment loading

- [`spatial-pressure-layout.md`](spatial-pressure-layout.md)
- [`protected-air-channel-tradeoff.md`](protected-air-channel-tradeoff.md)
- [`protected-support-skeleton.md`](protected-support-skeleton.md)
- [`terminal-route-codesign.md`](terminal-route-codesign.md)
- [`environment-exposure-control.md`](environment-exposure-control.md)

### Liquid routing and nonvolatile solute

- [`capillary-liquid-network.md`](capillary-liquid-network.md)
- [`capillary-architecture-tradeoff.md`](capillary-architecture-tradeoff.md)
- [`capillary-practical-constraints.md`](capillary-practical-constraints.md)
- [`branched-liquid-resistor-network.md`](branched-liquid-resistor-network.md)
- [`sparse-branched-liquid-network.md`](sparse-branched-liquid-network.md)
- [`collector-fouling-margin.md`](collector-fouling-margin.md)
- [`salt-leakage-budget.md`](salt-leakage-budget.md)
- [`transient-terminal-buffer.md`](transient-terminal-buffer.md)

## Publication and history

- [`design-history.md`](design-history.md) — design evolution and superseded branches.
- [`prior-art.md`](prior-art.md) — literature/prior-art working map.
- [`patent-notes.md`](patent-notes.md) — patent working notes; not a legal opinion.
- [`release-checklist.md`](release-checklist.md) — stable-release checklist.
- [`roadmap.md`](roadmap.md) — release-preparation roadmap; further modeling is optional rather than required.

## Interpretation rule

The repository should be read as a **computational technical disclosure**, not as product validation. Simulated watt values, synthetic pressure maps, idealized capillary dimensions, and virtual BOM values are design-space outputs under stated assumptions. They are not measurements of a manufactured garment.
