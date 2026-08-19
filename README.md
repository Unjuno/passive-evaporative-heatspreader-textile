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

This repository currently represents a **virtual / computational prototype only**. No physical garment or bench specimen exists yet, and no physical garment-performance measurements have been published.

The repository contains screening models, reproducibility infrastructure, prior-art notes, concrete implementation variants, uncertainty requirements, and future physical-test protocols. The experiment files are specifications for later validation, not records of completed hardware tests.

Nominal future benchmark condition used to normalize the simulation/validation plan:

- active-area normalization: 0.30 m²;
- artificial skin: 34 °C;
- ambient: 35 °C / 70% RH;
- liquid input: 150 g/h equivalent;
- nominal still air;
- flat fast-dry textile control at the same water input.

Project screening rules for a future B0-vs-B4 physical comparison:

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

Current virtual-prototype candidates are:

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

### 9. Ordinary same-boundary heat/mass analogies do not supply the hot-ambient selectivity the sensitivity model requires

Define

\[
\Xi=\delta_{vapor}/\delta_{heat}.
\]

`Xi=1` is the same-exchange-length baseline. At 40 °C / 70% RH, zero body-side heat flux in the current low-order model requires critical `Xi` values of roughly 0.31–0.65 across the screened vapor-side range.

For ordinary same-boundary air/water-vapor transport, the screening Lewis number is near one. A Chilton–Colburn-style equal-j-factor comparison gives an equivalent `Xi` also near one, not near 0.3–0.6.

**Current interpretation:** simply opening the same air path more strongly is unlikely to provide the modeled hot-ambient selectivity. Dry-side shielding, radiation control, anisotropic heat routing, selective wet exposure, or another genuinely different heat/vapor pathway must be physically tested.

This is still a low-order comparison, not a validated textile correlation.

### 10. Water supply can become the limit, and an explicit first partial-wetness state now exists

The fully-wet thermal model reports transfer capacity. `simulations/open_valley_feed_limited.py` now solves a homogenized sub-grid wet fraction `beta` when available liquid feed is below that capacity.

For the nominal structured area `0.30 × 0.65 = 0.195 m²`, a 150 g/h feed corresponds to about 769 g/(m² h).

At 35 °C / 50% RH with linked heat/vapor exchange:

- strong exchange can be supply-limited with `beta < 1`;
- the same 150 g/h evaporation can remove different amounts of heat from the body because ambient air supplies part of the latent heat;
- the current linked-exchange sweep gives a finite body-cooling optimum near the point where evaporation capacity approximately matches available feed;
- making exchange still stronger after feed saturation can **reduce body-coupled cooling**.

At 35 °C / 70% RH and 85% RH, the primary 150 g/h linked cases in the current screen remain transfer-limited over the tested range.

The model `beta` is not a measured visible wet fraction.

### 11. Same evaporation does not imply the same body cooling

For the 35 °C / 50% RH / 150 g/h feed-limited screen, the latent heat can be partitioned into body-side and ambient sensible contributions.

Representative linked-exchange cases that all evaporate approximately the same 150 g/h total feed show body fractions of latent heat ranging from roughly 62% at very strong exchange to roughly 78% near the modeled transition region.

This reinforces the primary metric choice: **signed body-side heat flow / heater power**, not evaporation mass alone.

### 12. Heat spreading only creates system-level value under spatial asymmetry

The symmetric wet/dry two-node screen shows that lateral heat spreading can collapse a large local wet/dry temperature difference without materially changing area-integrated cooling when wet and dry patches have identical external sensible boundary conditions.

The asymmetric screen gives the dry region a lower ambient sensible coefficient. Under that condition, heat spreading routes body heat from the dry region into the active wet evaporator and increases total body-side heat removal.

The nonlinear asymmetric solver is now bounded and continuation-capable after a dense sweep exposed nonphysical branch jumps in the earlier unconstrained root formulation.

For the representative `h_dry=5 W/(m² K)` screen, the approximate `g_mix` needed to reach 90% of the high-mixing gain is:

- 30 g/h: ~117 W/(m² K);
- 50 g/h: ~192 W/(m² K);
- 75 g/h: ~285 W/(m² K);
- 100 g/h: ~330 W/(m² K);
- 150 g/h: ~258 W/(m² K).

The high-mixing gain itself is finite, roughly 3–6 W over the 0.195 m² structured area in this screen. Infinite thermal conductivity is not the design target.

### 13. Heat-spreader performance is now mapped to material geometry and contact burden

For an ideal periodic alternating wet/dry stripe topology,

\[
g_{sheet}\approx \Gamma\frac{k_{\parallel}tc}{P^2},\qquad \Gamma=4.
\]

This is a low-order mapping, not a validated textile correlation. Its key implication is robust: **routing burden grows with the square of wet/dry pitch**.

For a representative 100 g/h / 90%-gain target (`g_mix≈330 W/(m² K)`):

- abstract `k=100 W/(m K)`, `rho=1600 kg/m³`: about 83 µm / 40 g over 0.30 m² at `P=10 mm`, but about 330 µm / 159 g at `P=20 mm`;
- abstract `k=300 W/(m K)`, `rho=1800 kg/m³`: about 28 µm / 15 g at `P=10 mm`, about 110 µm / 59 g at `P=20 mm`.

Under the simple linear-coverage assumption, a sparse network is not automatically lighter because reduced coverage must be offset by increased thickness to preserve the same conductance. The simple mass figure of merit is `k/rho`.

A separate two-contact series screen gives

\[
\frac{1}{g_{eff}}=\frac{1}{g_{sheet}}+\frac{2}{h_c}.
\]

For the representative `g_target≈330 W/(m² K)` case, even an infinitely conductive sheet needs each-side contact conductance above roughly 660 W/(m² K). Sheet conductivity alone is therefore insufficient; integrated thermal contact is a first-class design parameter.

**Current virtual-prototype implication:** keep heat-routing distances short, initially around the 10–20 mm scale, and integrate wet/dry thermal contacts rather than relying on a thick continuous high-conductivity sheet.

### 14. Measurement resolution is already specified for future validation

The E3c mechanism target can be only a few watts and local `F` differences can be small. A pre-bench uncertainty screen shows that, for a representative true `F=0.8`:

- 1σ temperature uncertainty 0.10 °C and RH uncertainty 0.5 percentage point gives an approximate 5–95% `F` range of 0.75–0.85;
- 0.20 °C and 1.0 percentage point broadens it to roughly 0.70–0.91.

Near the hot/humid sign boundary, a heater-only plate cannot measure inward environmental heat. Any future E4/E6 bench implementation therefore requires **bidirectional temperature control or calibrated signed heat-flux measurement**.

## Current exterior / spreader hypothesis

> directional sweat transport + capillary-fed wet microtexture + continuously ambient-connected open valleys/gaps/islands + short-range high-`k/rho` heat routing between thermally asymmetric wet/dry regions + explicit thermal contact + hot-ambient sensible-heat protection.

This is a virtual-prototype research hypothesis, not a validated product architecture.

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
- `docs/feed-limited-open-valley.md` — explicit homogenized partial-wetness/feed-limit model
- `docs/spreader-material-mapping.md` — `g_mix` to material/thickness/pitch/mass/contact mapping
- `docs/passive-environment-boundary.md` — analytic hot/humid body-heat-flow sign boundary
- `docs/measurement-uncertainty-budget.md` — pre-bench resolution and uncertainty requirements
- `docs/roadmap.md` — research/publication roadmap
- `docs/experiment-plan.md` — future validation plan
- `docs/prior-art.md` / `docs/patent-notes.md` — adjacent work and patent-family notes
- `AUDIT.md` — current repository audit and remaining queue

### Future physical-test specifications

No physical specimen currently exists. These files are future validation protocols:

- `experiments/e3b_hierarchical_air_renewal.md`
- `experiments/e3c_open_vs_covered_corridors.md`
- `experiments/e4a_feed_limit_transition.md`
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
simulations/open_valley_feed_limited.py
simulations/wet_dry_two_node.py
simulations/asymmetric_wet_dry_spreader.py
simulations/spreader_material_mapping.py
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
python simulations/open_valley_feed_limited.py
python simulations/asymmetric_wet_dry_spreader.py
python simulations/spreader_material_mapping.py
python simulations/open_valley_heat_mass_coupling_audit.py
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
