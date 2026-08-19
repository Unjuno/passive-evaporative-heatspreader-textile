# Passive Evaporative Heat-Spreader Textile

Open research on a passive personal-cooling garment that combines whole-garment heat spreading, directional moisture transport, capillary liquid delivery, and high-surface-area exterior evaporation.

## Concept

The primary architecture is fully passive: no onboard fan is required.

1. A skin-side layer transports liquid sweat outward.
2. A lightweight in-plane heat spreader redistributes body heat over the garment.
3. Capillary transport routes liquid toward exterior evaporation zones.
4. Exterior micro-ribs, short fins, 3D-knit relief, pile-like structures, lamellae, pleats, or related high-area textures evaporate water to ambient air.
5. Macro-scale ventilation corridors, valleys, spacer channels, or discontinuous rib fields may be used to keep wet microstructures connected to refreshed ambient air.
6. Dry exterior regions may be thermally shielded from hot ambient air to reduce parasitic inward heat flow.

The design goal is not simply to maximize geometric surface area or evaporate more water. It is to increase **body-coupled useful evaporation** while remaining wearable, washable, flexible, and visually acceptable as normal apparel.

## Current status

This repository contains numerical screening models, reproducibility infrastructure, prior-art notes, and staged experimental protocols. **Physical garment performance has not yet been validated.**

The primary planned benchmark uses a 0.30 m² active-area equivalent at 35 °C, 70% RH, 150 g/h liquid-water input, nominal still air, and an artificial-skin setpoint of 34 °C.

Project decision rules for that future physical test are:

- compare against a flat fast-dry textile at the same liquid-water input;
- use artificial-skin heater-power difference as the primary cooling metric;
- approximately +10 W over control: provisional PASS;
- approximately +20 W: provisional STRONG PASS;
- less than +5 W: provisional FAIL.

These are project decision rules, not measured product claims or external standards.

## Important model audit findings

### 1. Nonlinear heat/mass model can have multiple stable equilibria

The current low-order passive heat/mass screening model can produce multiple stable surface-temperature equilibria. Earlier exploratory work sometimes selected the most-cooling stable branch and therefore produced overly simple single-value exchange thresholds.

The repository model now exposes all detected stable roots and reports conservative/warm and optimistic/cool branches separately. **No single exterior multiplier `M` is currently accepted as a validated cooling threshold.**

### 2. Geometric rib area can be hidden inside one humid boundary layer

E3 adds a periodic 2-D steady-diffusion screen for wet exterior ribs. It replaces the idea that a single empirical accessibility number `alpha` is sufficient with a more explicit boundary-layer question: how close is refreshed ambient air to the rib tips?

For one screened geometry (`h = 2.5 mm`, 65% structured-panel coverage):

- with an idealized refreshed-air plane only about 0.5 mm above the rib tips, modeled whole-area vapor-transfer multipliers can be around 3–4;
- with the renewal plane about 5 mm above the tips, the same screen falls to roughly 1.3;
- pitch changes between 0.8 and 1.5 mm become secondary when the entire field is buried in a thicker stagnant humidity layer.

This is **pure-diffusion screening, not CFD and not a measured garment result**. Its main design consequence is that the preferred exterior is now hierarchical: wet microstructures for surface area plus larger open paths for passive or motion-assisted air renewal.

See `docs/e3-boundary-layer-screen.md` and `experiments/e3b_hierarchical_air_renewal.md`.

## Key model variables

For a rectangular-rib geometric screen:

\[
G_{panel} \approx 1 + \frac{2h}{p}
\]

A phenomenological whole-garment exchange mapping used in earlier screens is:

\[
M \approx 1 + \alpha f (G_{panel}-1)
\]

where:

- `h` = rib height;
- `p` = rib pitch;
- `f` = fraction of active projected garment area covered by structured evaporative panels;
- `alpha` = phenomenological effective-area factor;
- `M` = effective exterior exchange multiplier relative to a flat wet textile.

E3 shows why `alpha` must not be treated as a geometry-only material constant: boundary-layer renewal can dominate it. The newer diffusion model therefore reports a mass-transfer multiplier directly as a function of rib geometry and an idealized air-renewal boundary.

## Repository map

### Technical record

- `docs/technical-disclosure.md` — integrated technical description
- `docs/architecture.md` — numbered functional architecture diagrams
- `docs/embodiment-matrix.md` — concrete complete implementation combinations
- `docs/design-history.md` — retained, optional, and deprecated design branches
- `docs/current-results.md` — consolidated numerical findings and corrections
- `docs/e3-boundary-layer-screen.md` — periodic rib diffusion/boundary-layer interference result
- `docs/roadmap.md` — research and publication roadmap
- `docs/experiment-plan.md` — staged physical validation plan
- `docs/accessibility-identification.md` — method for estimating effective exterior exchange
- `docs/prior-art.md` — literature/prior-art overview
- `docs/patent-notes.md` — close patent-family working notes
- `docs/release-checklist.md` — stable-release audit gate

### Experiments

- `experiments/e3b_hierarchical_air_renewal.md` — next physical test for micro-ribs + macro air-renewal paths
- `experiments/README.md` — experiment structure and data requirements

### Models and reproducibility

- `models/governing-equations.md` — equations, assumptions, variables, and checks
- `models/water-salt-transport.md` — water/salt conservation model and zero salt-vapor rule
- `simulations/passive_rib_screen.py` — nonlinear passive exterior heat/mass-transfer screen
- `simulations/rib_diffusion_screen.py` — periodic 2-D vapor-diffusion / boundary-layer-sharing screen
- `simulations/heat_spreader_2d.py` — 2D anisotropic lateral heat-routing model
- `simulations/water_salt_1d.py` — normalized nonvolatile-salt mass-balance screen
- `simulations/generate_reference_outputs.py` — reproducible CSV/PNG/metadata/SHA generator
- `simulations/README.md` — model hierarchy and run instructions
- `tests/` — numerical regression tests
- `.github/workflows/model-tests.yml` — CI for tests, model demos, and reference generation

### Data and release controls

- `data/e3_boundary_layer_screen.csv` — E3 diffusion-screen outputs
- `data/e3_grid_convergence.csv` — E3 numerical convergence check
- `data/e3_M3p5_thresholds.csv` — cross-model legacy-reference threshold screen
- `data/reference_branch_map_35C_70RH_150gph.csv` — retained multi-equilibrium audit table
- `data/README.md` — data conventions
- `figures/README.md` — figure conventions
- `AUDIT.md` — repository completeness and uncertainty audit
- `CHANGELOG.md` — corrections and research-record changes

## Important physical clarification: sweat salts

At garment temperatures, sweat salts are treated as nonvolatile. Water evaporates; dissolved salts remain in liquid/solid phases. Any salt-removal mechanism discussed in this project must involve physical removal of salt-containing liquid or solids, not evaporation of salt.

## Prior-art position

Several important building blocks are already known. Current audit has identified prior disclosures covering, among other things:

- directional sweat transport;
- integrated heat-conductive and sweat-transport textiles;
- textile ribs/walls that wick sweat away from skin toward an exterior evaporation surface;
- wicking evaporative cooling garments supplied with liquid;
- 3D spacer-knit outward moisture transport and evaporation-area enlargement;
- fan-assisted sweat evaporation;
- sorbent cooling garments and exterior fins.

This project therefore does **not** treat capillary transport, exterior ribs, 3D knit, heat-conductive textiles, or evaporation individually as unique premises. The research emphasis is on the specific integrated architecture, heat-routing strategy, boundary-layer/accessibility analysis, hierarchical air-renewal structures, hot-ambient protection, stretchability, apparel integration, and falsifiable comparison methods. See `docs/prior-art.md` and `docs/patent-notes.md`.

## Scope

The core research focus is the passive architecture. Optional variants may include external airflow, auxiliary fans, humidity-responsive vents, different heat-spreader topologies, or gas-phase moisture-capture layers, but those are secondary embodiments unless explicitly stated otherwise.

## Reproducibility

Install development dependencies and run:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python simulations/generate_reference_outputs.py --output-root generated-reference
```

Generated reference artifacts are marked as simulation outputs and include metadata and SHA-256 hashes.

## License

Apache License 2.0. See `LICENSE`.

## Citation

See `CITATION.cff`. Update citation version/date when a stable release is tagged.
