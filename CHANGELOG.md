# Changelog

This changelog records major changes to the public computational research record. Detailed intermediate history remains available in Git history and `docs/design-history.md`.

## v1.0.0 — stable computational technical record (2026-08-20)

### Project-state change

- Declared the exploratory numerical phase sufficiently complete for the present public technical record.
- Moved the repository into **research freeze / stable-release mode**.
- Added `docs/research-freeze.md` to distinguish frozen technical content, release blockers, and optional future research.
- Replaced the placeholder `docs/README.md` with a structured documentation index.
- Refocused the root README, audit, roadmap, and release checklist on canonical conclusions and exact-release preparation rather than continued model expansion.
- Reconciled the simulation index against the actual directory: **45 executable models + one reference-output generator**. The previously stated count of 43 omitted the already-added collector-fouling and transient-terminal-buffer models.
- Added Actions artifact preservation for exact-head generated reference packages (`metadata.json`, `sha256.txt`, generated data and figures).
- Added `docs/release-notes-v1.0.0.md` and automated exact-commit publication on the first merge to `main` carrying v1.0.0 metadata.

### Reproducibility and release integrity

- Dedicated `model-tests`, `topology-tests`, `pressure-tests`, `liquid-tests`, and `garment-tests` workflows.
- Corrected PR-workflow provenance so the release reference package is generated from the exact PR head rather than GitHub's temporary merge ref.
- Added an explicit direct-execution regression for `simulations/branched_liquid_resistor_network.py`.
- Corrected `generate_reference_outputs.py` so Git metadata is resolved with the repository root as `cwd`, including when invoked from outside the checkout.
- Added an outside-checkout generator regression to `model-tests`.
- Added `publish-v1`, which on the stable `main` commit runs the regression suite, regenerates the reference package from outside the checkout, verifies `metadata.json` against the exact commit SHA, builds a ZIP plus SHA-256 file, and creates GitHub release `v1.0.0` if it does not already exist.

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
- Collector fouling/radius-loss screens are failure sensitivities, not measured deposition kinetics or lifetime predictions.
- Transient terminal-buffer time constants are model inputs, not measured textile response constants.

### Prior-art confidence policy

- The stable release retains a technical prior-art map and public-index bibliographic cross-checks.
- v1.0.0 does **not** label patent family, legal-status, or claim-scope facts as authoritatively patent-office verified when that verification was not completed.
- No legal conclusion of novelty, patentability, invalidity, infringement, or freedom to operate is asserted.

### Release-policy change

New numerical models are no longer added to v1.0.0 merely to explore additional sensitivities. Further technical research should normally enter a later version unless it corrects a contradiction or a release-critical error.

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

See `docs/current-results.md`, `simulations/README.md`, `docs/design-history.md`, `docs/release-notes-v1.0.0.md`, and `AUDIT.md` for the detailed technical record.
