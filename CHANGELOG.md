# Changelog

This changelog records major changes to the public computational research record. Detailed intermediate history remains available in Git history and `docs/design-history.md`.

## Unreleased — release-candidate consolidation (2026-08-20)

### Project-state change

- Declared the exploratory numerical phase sufficiently complete for the present public technical record.
- Moved the repository into **research-freeze / release-preparation mode**.
- Added `docs/research-freeze.md` to distinguish frozen technical content, release blockers, and optional future research.
- Replaced the placeholder `docs/README.md` with a structured documentation index.
- Refocused the root README, audit, roadmap, and release checklist on canonical conclusions and exact-release preparation rather than continued model expansion.

### Current reproducible stack

- 43 indexed executable screening/sensitivity/audit/virtual-prototype models.
- One reference-output generator.
- Dedicated `model-tests`, `topology-tests`, `pressure-tests`, `liquid-tests`, and `garment-tests` workflows.
- Pre-cleanup integration head `529fc573f2a24a0d4d3db8464c3c1409a38b34ec` passed all five workflows:
  - `model-tests` #722;
  - `topology-tests` #278;
  - `pressure-tests` #112;
  - `liquid-tests` #91;
  - `garment-tests` #46.

### Retained architecture

The current passive design family combines:

- directional local sweat collection;
- short distributed two-scale capillary liquid routing;
- pressure/ambient-aware exterior wet terminals;
- continuously ambient-connected evaporative microtexture/open valleys/gaps/islands;
- short high-`k/rho` heat routing with limited cross-link redundancy;
- terminal contact/load management;
- dry-side hot-ambient protection;
- separate water/nonvolatile-solute balances with zero salt-vapor flux.

### Major corrections retained

- Geometric exterior area is not treated as accessible evaporative area without ambient renewal.
- Vertical/passive corridor flow is not assumed to be upward or useful; thermo-solutal effects can reverse/neutralize buoyancy.
- Sensible and vapor transfer are separated rather than forced through one multiplier.
- Positive evaporation is not treated as proof of positive body-side cooling.
- Fully-wet transfer capacity is not reused after water/feed limitation becomes active.
- Symmetric heat spreading is not credited with integrated cooling when local boundary conditions are identical.
- The earlier claim that aligned sparse high-`k` traces beat an equal-material homogenized field was withdrawn; the retained ordering is `uniform homogenized > x-aligned / mesh >> y-transverse`.
- The `d95*r^-4` terminal-route proxy is retained as a geometric burden metric only. Explicit dense/sparse branched liquid networks supersede it for hydraulic-pressure conclusions.
- Salt vapor flux is zero; small upstream water leakage does not by itself prove bulk salt crystallization.

### Release-policy change

New numerical models are no longer added to the current release candidate merely to explore additional sensitivities. Further technical research should normally enter a later version unless it corrects a contradiction or a release-critical error.

## Development record before research freeze

The repository accumulated the following major model families before freeze:

- nonlinear passive heat/mass and multi-root screening;
- separate sensible/vapor transfer and model-form sensitivity;
- periodic rib diffusion and corridor buoyancy/self-consistent corridor models;
- open-valley exchange, thermal, feed-limited, and hot/humid sign-boundary screens;
- direct-material 1-D and anisotropic/explicit 2-D heat-routing models;
- heat-network topology, stretch, fracture, contact, and combined-failure screens;
- compression and synthetic backpack/strap/seat pressure maps;
- protected under-load vapor-path and support-area tradeoffs;
- fixed/adaptive terminal-layout schedule screens;
- ideal capillary architecture, radius/lift optimum, blockage and collapse screens;
- explicit dense branched and sparse two-scale liquid-network pressure models;
- corrected nonvolatile water/salt balance;
- collector-fouling sensitivity;
- transient terminal water-buffer model;
- integrated VP-E environmental anchor and virtual garment BOM.

See `docs/current-results.md`, `simulations/README.md`, `docs/design-history.md`, and `AUDIT.md` for the detailed technical record.

## Stable release policy

A stable release should identify one exact public commit/tag, confirm CI on that commit, regenerate reference artifacts and hashes, update citation/version metadata, and preserve earlier public history. A persistent archive/DOI is optional but useful for durable version/date evidence.
