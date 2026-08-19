# Passive Evaporative Heat-Spreader Textile

Open research on a passive personal-cooling garment combining whole-garment heat spreading, directional liquid transport, capillary delivery, and high-surface-area exterior evaporation.

## Concept

The primary architecture is fanless:

1. skin-side directional sweat transport;
2. flexible in-plane heat spreading over a substantial garment area;
3. distributed capillary delivery to wet exterior zones;
4. low-profile micro-ribs, short fins, 3D-knit relief, lamellae, pile, pleats, or related evaporative textures;
5. **continuous lateral ambient access** through open valleys, cross-openings, gaps, or discontinuous wet islands;
6. thermal shielding/routing of dry conductive regions where hot ambient air would otherwise add inward sensible heat.

The design goal is not maximum geometric area or maximum evaporation alone. It is **body-coupled useful evaporation** in a wearable, washable, flexible, visually acceptable garment.

## Current status

This repository contains screening models, reproducibility infrastructure, prior-art notes, concrete implementation variants, uncertainty requirements, and staged physical experiment protocols. **Physical garment performance has not yet been validated.**

Primary planned benchmark:

- active-area normalization: 0.30 m²;
- artificial skin: 34 °C;
- ambient: 35 °C / 70% RH;
- liquid input: 150 g/h equivalent;
- nominal still air;
- flat fast-dry textile control at the same water input.

Project screening rules for the future physical B0-vs-B4 comparison:

- approximately +10 W heater-power difference: provisional PASS;
- approximately +20 W: provisional STRONG PASS;
- less than +5 W: provisional FAIL.

These are project decision rules, not measured claims or external standards.

## Current audit findings

### 1. No validated single `M` cooling threshold

The low-order nonlinear lumped model can contain multiple stable equilibria. Earlier single-value exchange thresholds are retained only as exploratory history. Current code exposes all detected stable roots.

### 2. Geometric rib area can disappear inside one humid boundary layer

The E3 2-D vapor-diffusion screen shows that dense wet microstructures gain little when they share a several-millimeter stagnant humidity layer. Exterior area must be paired with explicit ambient-air/vapor access.

### 3. Sensible heat and vapor transfer are not interchangeable

The thermal models separate heat and vapor exchange. Better vapor renewal can improve evaporation while stronger sensible exchange can bring environmental heat inward.

### 4. Long covered wet “chimneys” are not preferred

The self-consistent covered/end-renewed corridor model produces nonzero natural flow but near-saturated channel air at 35 °C / 70% RH for shallow 100 mm corridors. Flow can reverse at high humidity, and stronger flow at 40 °C can coincide with inward body-side heat flux.

### 5. Centimeter-scale interruption alone is too coarse in the current open-valley screen

For the representative 6 × 3 mm distributed open-valley screen, the exchange length is roughly 0.7–1.1 mm. Therefore 20–50 mm interruption is retained as a **negative/control condition**, not an assumed renewal solution.

Current physical candidates are:

- continuously laterally open valleys;
- frequent cross-openings;
- discontinuous ambient-connected wet islands;
- 1–3 mm interrupted segments only as an extreme mechanism test.

### 6. High vapor-driving-force retention is not enough

Define local renewal quality

\[
F=\frac{R}{1+R}, \qquad R=G_a/G_w.
\]

`F=0.8` requires `R=4`; `F=0.9` requires `R=9`.

But a high `F` can result from weak wet-surface transfer. The repository also tracks

\[
k_{eff}=\frac{k_wk_a}{k_w+k_a}=k_wF.
\]

Every design must pair renewal quality with absolute evaporation transfer and body-side heat flow.

### 7. Positive evaporation is not necessarily body cooling

The coupled open-valley thermal/vapor screen solves valley-air temperature, vapor density, wet-surface temperature, evaporation, and body-side heat flow.

At 35 °C / 70% RH, stronger vapor renewal generally increases modeled body-side heat removal. At 40 °C / 70% RH, a same-exchange-length heat/vapor baseline still evaporates water while producing **negative body-side heat flux**.

Therefore evaporation rate alone is never the cooling endpoint.

### 8. Hot/humid operation has a model sign boundary

For the repository's same-path heat/vapor baseline, zero body-side heat flow reduces to

\[
\frac{k_{air}}{D_v}(T_\infty-T_{skin})
=
L_v\left[\rho_{v,sat}(T_{skin})-\phi_\infty\rho_{v,sat}(T_\infty)\right].
\]

With a 34 °C artificial-skin setpoint, representative model boundaries are about:

- 45.25 °C at 50% RH;
- 39.73 °C at 70% RH;
- 37.57 °C at 80% RH;
- 36.59 °C at 85% RH;
- 35.68 °C at 90% RH.

This is a **low-order model sign boundary**, not a human heat-safety limit or measured garment threshold. It changes materially with skin/artificial-skin temperature; at 70% RH the modeled boundary moves from about 37.54 °C for a 32 °C skin setpoint to about 41.91 °C for a 36 °C setpoint.

### 9. Same-path heat/mass coupling is restrictive above the boundary

Define the coupling audit quantity

\[
\Xi=\delta_{vapor}/\delta_{heat}.
\]

`Xi=1` is the model's same-exchange-length baseline. At 40 °C / 70% RH, zero body-side heat flux in the current low-order model requires `Xi<1`; the screened critical values rise from about 0.31 to 0.65 as the vapor-side exchange parameter increases from 0.1 to 2 mm.

This does **not** prove a passive textile can arbitrarily decouple heat from vapor transfer. It quantifies what the sensitivity model would require and therefore defines a falsifiable design burden.

### 10. Water supply can become the limit

The thermal model is a fully-wet transfer-capacity screen. At 35 °C / 70% RH, the linked screened cases remain below the planned 150 g/h supply when scaled to 65% of 0.30 m². At 35 °C / 50% RH, stronger-transfer cases can exceed the available feed and must be classified as supply-limited.

Supply-limited cases are **not** assigned a fabricated dryout temperature field; only the capacity/feed upper bound is reported until a wetting/dryout model exists.

### 11. Physical measurement resolution is part of the experiment

The E3c mechanism target can be only a few watts and local `F` differences can be small. A pre-bench uncertainty screen shows that, for a representative true `F=0.8`:

- 1σ temperature uncertainty 0.10 °C and RH uncertainty 0.5 percentage point gives an approximate 5–95% `F` range of 0.75–0.85;
- 0.20 °C and 1.0 percentage point broadens it to roughly 0.70–0.91.

Near the hot/humid sign boundary, a heater-only plate cannot measure inward environmental heat. E4/E6 therefore requires **bidirectional temperature control or calibrated signed heat-flux measurement**.

## Current exterior hypothesis

> directional sweat transport + routed whole-garment heat spreading + capillary-fed wet microtexture + continuously ambient-connected open valleys/gaps/islands + hot-ambient sensible-heat protection.

This is a research hypothesis, not a validated product architecture.

## Repository map

### Technical record

- `docs/technical-disclosure.md` — integrated disclosure
- `docs/architecture.md` — functional architecture
- `docs/embodiment-matrix.md` — concrete implementation combinations
- `docs/design-history.md` — retained/deprecated branches
- `docs/current-results.md` — current numerical conclusions and corrections
- `docs/e3-boundary-layer-screen.md` — micro-rib boundary-layer sharing
- `docs/split-transfer-model.md` — separate sensible/vapor transfer
- `docs/model-form-uncertainty.md` — uncertainty framework
- `docs/corridor-buoyancy-screen.md` — thermo-solutal flow sign
- `docs/self-consistent-corridor-model.md` — covered/end-renewed coupled corridor
- `docs/open-valley-renewal-target.md` — local `R/F` target and measurement inversion
- `docs/open-valley-distributed-model.md` — distributed open-valley vapor model
- `docs/open-valley-metric-audit.md` — `F` versus absolute `k_eff`
- `docs/open-valley-thermal-model.md` — coupled open-valley heat/vapor result
- `docs/passive-environment-boundary.md` — analytic hot/humid body-heat-flow sign boundary
- `docs/measurement-uncertainty-budget.md` — pre-bench resolution and uncertainty requirements
- `docs/roadmap.md` — research/publication roadmap
- `docs/experiment-plan.md` — master validation plan
- `docs/prior-art.md` / `docs/patent-notes.md` — adjacent work and patent-family notes
- `AUDIT.md` — current repository audit and remaining queue

### Physical protocols

- `experiments/e3b_hierarchical_air_renewal.md`
- `experiments/e3c_open_vs_covered_corridors.md`
- `experiments/e4_e6_environment_boundary.md`
- `experiments/README.md`

### Executable model / audit modules

```text
simulations/passive_rib_screen.py
simulations/split_heat_mass_screen.py
simulations/split_transfer_sensitivity.py
simulations/rib_diffusion_screen.py
simulations/corridor_buoyancy_screen.py
simulations/self_consistent_corridor_1d.py
simulations/open_valley_exchange_target.py
simulations/open_valley_distributed_1d.py
simulations/open_valley_thermal_1d.py
simulations/open_valley_heat_mass_coupling_audit.py
simulations/passive_environment_boundary.py
simulations/supply_limit_audit.py
simulations/heat_spreader_2d.py
simulations/water_salt_1d.py
```

## Reproducibility

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python simulations/open_valley_thermal_1d.py
python simulations/passive_environment_boundary.py
python simulations/generate_reference_outputs.py --output-root generated-reference
```

Generated reference artifacts include classification, git commit metadata, and SHA-256 hashes. The latest fully verified integration SHA/run is recorded in `AUDIT.md`; documentation commits may trigger newer CI runs.

## Physical clarification: sweat salts

At garment temperatures, sweat salts are treated as nonvolatile. Water evaporates; dissolved salts remain in liquid/solid phases. Any salt removal must physically remove salt-containing liquid or solids.

## Prior-art position

Many building blocks are already known: directional sweat transport, evaporative textiles, conductive cooling textiles, external ribs/walls, spacer knits, fan-assisted garments, and sorbent garments. This project does not treat those components individually as unique. The research record focuses on integrated heat routing, liquid routing, effective exterior accessibility, ambient-access topology, hot-ambient protection, apparel integration, and falsifiable comparison methods.

## License

Apache License 2.0. See `LICENSE`.

## Citation

See `CITATION.cff`. Version/date will be frozen for a stable release.
