# Passive Evaporative Heat-Spreader Textile

Open research on a passive personal-cooling garment that combines whole-garment heat spreading, directional moisture transport, capillary liquid delivery, and high-surface-area exterior evaporation.

## Concept

The primary architecture is fully passive: no onboard fan is required.

1. A skin-side layer transports liquid sweat outward.
2. A lightweight in-plane heat spreader redistributes body heat over the garment.
3. Capillary transport routes liquid toward exterior evaporation zones.
4. Exterior micro-ribs, short fins, 3D-knit relief, pile-like structures, lamellae, pleats, or related high-area textures evaporate water to ambient air.
5. Dry exterior regions may be thermally shielded from hot ambient air to reduce parasitic inward heat flow.

The design goal is not simply to evaporate more water. It is to increase body-coupled evaporative cooling while remaining wearable, washable, flexible, and visually acceptable as normal apparel.

## Current status

This repository currently contains numerical screening models and experimental protocols. **Physical garment performance has not yet been validated.**

The primary planned benchmark uses a 0.30 m² active-area equivalent at 35 °C, 70% RH, 150 g/h liquid-water input, nominal still air, and an artificial-skin setpoint of 34 °C.

Project decision rules for that future physical test are:

- compare against a flat fast-dry textile at the same liquid-water input;
- use artificial-skin heater-power difference as the primary cooling metric;
- approximately +10 W over control: provisional PASS;
- approximately +20 W: provisional STRONG PASS;
- less than +5 W: provisional FAIL.

These are experimental decision rules, not measured product claims.

### Model audit note

The current nonlinear heat/mass screening model can produce **multiple stable surface-temperature equilibria**. Earlier exploratory work sometimes selected the most-cooling stable branch and therefore produced overly simple single-value exchange thresholds. The repository model now exposes all detected stable roots and reports conservative/warm and optimistic/cool branches separately.

Accordingly, no single value of exterior exchange multiplier `M` is currently accepted as a validated cooling threshold.

## Key model variables

For a rectangular-rib screening geometry:

\[
G_{panel} \approx 1 + \frac{2h}{p}
\]

\[
M \approx 1 + \alpha f (G_{panel}-1)
\]

where:

- `h` = rib height;
- `p` = rib pitch;
- `f` = fraction of active projected garment area covered by structured evaporative panels;
- `alpha` = fraction of added geometric area effectively accessible for independent heat and mass exchange;
- `M` = effective exterior exchange multiplier relative to a flat wet textile.

The principal unresolved exterior parameter is `alpha`, because dense structures may share a humid boundary layer and fail to use all geometric surface area.

## Repository map

### Technical record

- `docs/technical-disclosure.md` — integrated technical description
- `docs/architecture.md` — numbered functional architecture diagrams
- `docs/embodiment-matrix.md` — concrete complete implementation combinations
- `docs/design-history.md` — retained, optional, and deprecated design branches
- `docs/current-results.md` — consolidated numerical findings and corrections
- `docs/roadmap.md` — research and publication roadmap
- `docs/experiment-plan.md` — staged physical validation plan
- `docs/accessibility-identification.md` — method for estimating effective exterior area
- `docs/prior-art.md` — literature/prior-art overview
- `docs/patent-notes.md` — close patent-family working notes
- `docs/release-checklist.md` — stable-release audit gate

### Models and reproducibility

- `models/governing-equations.md` — equations, assumptions, variables, and checks
- `models/water-salt-transport.md` — water/salt conservation model and zero salt-vapor rule
- `simulations/passive_rib_screen.py` — nonlinear passive exterior heat/mass-transfer screen
- `simulations/heat_spreader_2d.py` — 2D anisotropic lateral heat-routing model
- `simulations/water_salt_1d.py` — normalized nonvolatile-salt mass-balance screen
- `simulations/generate_reference_outputs.py` — reproducible CSV/PNG/metadata/SHA generator
- `simulations/README.md` — model hierarchy and run instructions
- `tests/` — numerical regression tests
- `.github/workflows/model-tests.yml` — CI for tests, models, and reference generation

### Data and release controls

- `data/reference_branch_map_35C_70RH_150gph.csv` — retained multi-equilibrium audit table
- `experiments/README.md` — experiment structure and data requirements
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

This project therefore does **not** treat capillary transport, exterior ribs, 3D knit, heat-conductive textiles, or evaporation individually as unique premises. The research emphasis is on the specific integrated architecture, heat-routing strategy, effective-area/boundary-layer analysis, hot-ambient protection, stretchability, apparel integration, and falsifiable comparison methods. See `docs/prior-art.md` and `docs/patent-notes.md`.

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
