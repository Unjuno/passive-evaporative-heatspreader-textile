# Passive Evaporative Heat-Spreader Textile

Open research on a passive personal-cooling garment that combines whole-garment heat spreading, directional moisture transport, capillary liquid delivery, and high-surface-area exterior evaporation.

## Concept

The primary architecture is fully passive: no onboard fan is required.

1. A skin-side layer transports liquid sweat outward.
2. A lightweight in-plane heat spreader redistributes body heat over the garment.
3. Capillary transport routes liquid toward exterior evaporation zones.
4. Exterior micro-ribs, short fins, 3D-knit relief, pile-like structures, lamellae, pleats, or related high-area textures evaporate water to ambient air.
5. Macro-scale open valleys, ventilation corridors, spacer paths, cross-openings, or discontinuous rib fields may keep wet microstructures connected to refreshed ambient air.
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

This is **pure-diffusion screening, not CFD and not a measured garment result**. Its main design consequence is that the preferred exterior is hierarchical: wet microstructures for surface area plus larger open paths for passive or motion-assisted air renewal.

See `docs/e3-boundary-layer-screen.md` and `experiments/e3b_hierarchical_air_renewal.md`.

### 3. Sensible heat transfer and vapor transfer are now separated

Earlier thermal screens used one exterior multiplier for both convective sensible heat transfer and water-vapor mass transfer. That is now treated as a special case rather than the default physical assumption.

The split model introduces:

- `M_h` — multiplier for sensible convective heat transfer;
- `M_m` — multiplier for water-vapor mass transfer.

E3 constrains only the **mass-transfer side** and must not automatically be copied into `M_h`. This matters especially in hot ambient air, where stronger sensible convection can increase inward heat pickup while stronger vapor transfer can still improve evaporation.

See `docs/split-transfer-model.md` and `simulations/split_heat_mass_screen.py`.

### 4. A vertical wet corridor does not guarantee upward chimney flow

The first explicit macro-corridor model evaluates moist-air density and a laminar vertical-slot pressure/friction balance. Evaporative cooling tends to make channel air denser, while humidification tends to make it lighter.

For the common 35 °C / 70% RH ambient screen, the model places a neutral-density condition near 34 °C at roughly 90% RH. Depending on channel temperature and humidity, a vertical corridor can therefore have upward, downward, or near-neutral buoyancy tendency.

This is a **prescribed-state screening model**, not CFD. See `docs/corridor-buoyancy-screen.md` and `simulations/corridor_buoyancy_screen.py`.

### 5. End-renewed covered corridors saturate too easily in the primary condition

`simulations/self_consistent_corridor_1d.py` replaces the prescribed channel state with a coupled low-order calculation of signed buoyancy flow, wet-wall temperature, channel temperature/RH, evaporation, and body-side heat flow for a rectangular end-renewed duct limit.

Selected 35 °C / 70% RH, 100 mm cases:

- 3 × 2 mm: about +0.23 mm/s, `Pe_m ~ 0.81`, mean RH ~100%;
- 6 × 3 mm: about +0.59 mm/s, `Pe_m ~ 2.1`, mean RH ~100%;
- 10 × 5 mm: about +1.60 mm/s, `Pe_m ~ 5.7`, mean RH ~99.9%.

A larger Péclet number does not by itself mean good vapor renewal: a longer duct can have `Pe_m > 10` while the internal air is even closer to saturation.

At 35 °C / 85% RH the screened flow can reverse downward. At 40 °C / 70% RH a 10 × 5 × 100 mm case produces stronger downward flow but slightly **negative body-side heat flux** in the local wet-wall model, showing that more airflow can also increase hot-air sensible heat pickup.

This model is intentionally a covered/end-renewed limiting case. It does **not** model a valley that is continuously open to ambient air along its length. The current design preference is therefore:

- laterally open valleys rather than long covered ducts;
- frequent cross-openings or short segments;
- discontinuous evaporator islands;
- geometry that tolerates either buoyancy-flow direction;
- hot-ambient shielding/routing where sensible heat pickup becomes adverse.

See `docs/self-consistent-corridor-model.md` and `experiments/e3c_open_vs_covered_corridors.md`.

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

E3 shows why `alpha` must not be treated as a geometry-only material constant: boundary-layer renewal can dominate it. The newer diffusion model reports a vapor mass-transfer multiplier as a function of rib geometry and an idealized air-renewal boundary. The split thermal model then keeps vapor and sensible exchange distinct as `M_m` and `M_h`.

## Repository map

### Technical record

- `docs/technical-disclosure.md` — integrated technical description
- `docs/architecture.md` — numbered functional architecture diagrams
- `docs/embodiment-matrix.md` — concrete complete implementation combinations
- `docs/design-history.md` — retained, optional, and deprecated design branches
- `docs/current-results.md` — consolidated numerical findings and corrections
- `docs/e3-boundary-layer-screen.md` — periodic rib diffusion/boundary-layer interference result
- `docs/split-transfer-model.md` — independent sensible-heat and vapor-transfer multipliers
- `docs/model-form-uncertainty.md` — parameter/model-form uncertainty framework
- `docs/corridor-buoyancy-screen.md` — prescribed-state thermo-solutal corridor screen
- `docs/self-consistent-corridor-model.md` — coupled 1-D end-renewed corridor screen
- `docs/roadmap.md` — research and publication roadmap
- `docs/experiment-plan.md` — staged physical validation plan
- `docs/accessibility-identification.md` — method for estimating effective exterior exchange
- `docs/prior-art.md` — literature/prior-art overview
- `docs/patent-notes.md` — close patent-family working notes
- `docs/release-checklist.md` — stable-release audit gate

### Experiments

- `experiments/e3b_hierarchical_air_renewal.md` — micro-ribs + macro air-renewal comparison
- `experiments/e3c_open_vs_covered_corridors.md` — open valley vs covered/end-renewed corridor validation
- `experiments/README.md` — experiment structure and data requirements

### Models and reproducibility

- `models/governing-equations.md` — equations, assumptions, variables, and checks
- `models/water-salt-transport.md` — water/salt conservation model and zero salt-vapor rule
- `simulations/passive_rib_screen.py` — nonlinear passive exterior heat/mass-transfer screen
- `simulations/split_heat_mass_screen.py` — split sensible/vapor external-transfer screen
- `simulations/split_transfer_sensitivity.py` — deterministic model-form sensitivity grid
- `simulations/rib_diffusion_screen.py` — periodic 2-D vapor-diffusion / boundary-layer-sharing screen
- `simulations/corridor_buoyancy_screen.py` — prescribed-state moist-air corridor buoyancy screen
- `simulations/self_consistent_corridor_1d.py` — self-consistent end-renewed rectangular-corridor screen
- `simulations/heat_spreader_2d.py` — 2D anisotropic lateral heat-routing model
- `simulations/water_salt_1d.py` — normalized nonvolatile-salt mass-balance screen
- `simulations/generate_reference_outputs.py` — reproducible CSV/PNG/metadata/SHA generator
- `simulations/README.md` — model hierarchy and run instructions
- `tests/` — numerical regression tests
- `.github/workflows/model-tests.yml` — CI for tests, model demos, and reference generation

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
python simulations/passive_rib_screen.py
python simulations/split_heat_mass_screen.py
python simulations/split_transfer_sensitivity.py
python simulations/rib_diffusion_screen.py
python simulations/corridor_buoyancy_screen.py
python simulations/self_consistent_corridor_1d.py
python simulations/generate_reference_outputs.py --output-root generated-reference
```

Generated reference artifacts are marked as simulation outputs and include metadata and SHA-256 hashes.

## License

Apache License 2.0. See `LICENSE`.

## Citation

See `CITATION.cff`. Update citation version/date when a stable release is tagged.
