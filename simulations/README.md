# Simulations

## Executable model / audit hierarchy

1. **`passive_rib_screen.py`** — historical low-order exterior heat/mass model; one `M`, multiple-root audit.
2. **`split_heat_mass_screen.py`** — separate sensible `M_h`, vapor `M_m`, and radiation.
3. **`split_transfer_sensitivity.py`** — deterministic model-form sensitivity grid; grid fractions are not probabilities.
4. **`rib_diffusion_screen.py`** — periodic 2-D wet-rib vapor diffusion under an idealized renewal plane; pure diffusion, not CFD.
5. **`corridor_buoyancy_screen.py`** — prescribed-state thermo-solutal corridor flow sign/scaling.
6. **`self_consistent_corridor_1d.py`** — covered/end-renewed corridor velocity, T/RH, evaporation and body-side heat-flow screen.
7. **`open_valley_exchange_target.py`** — local open-valley `R=G_a/G_w` and `F=R/(1+R)` target/measurement inversion.
8. **`open_valley_distributed_1d.py`** — axial diffusion/advection plus distributed lateral vapor renewal; reports exchange length, `F`, and `k_eff`.
9. **`open_valley_thermal_1d.py`** — coupled valley-air T, vapor density, surface T, evaporation and body-side heat flow; optional homogenized `wet_fraction`.
10. **`open_valley_feed_limited.py`** — solves the homogenized wet fraction `beta` required to satisfy imposed feed when fully-wet transfer capacity is too high; reports latent heat-source partition.
11. **`wet_dry_two_node.py`** — separate wet/dry temperatures at fixed feed, coupled through a lateral heat-spreader mixing conductance under symmetric external coefficients.
12. **`asymmetric_wet_dry_spreader.py`** — bounded/continuation wet-dry mechanism screen with a shielded or weakly exposed dry region; tests when heat routing changes total body heat removal.
13. **`spreader_material_mapping.py`** — maps abstract `g_mix` to `k*t/pitch²`, mass, bending-strain screening and a two-contact thermal-resistance burden.
14. **`open_valley_heat_mass_coupling_audit.py`** — heat/mass coupling audit using `Xi=delta_vapor/delta_heat`, Lewis number, a Chilton–Colburn-style comparison, and the hot-ambient zero-body-flux threshold.
15. **`passive_environment_boundary.py`** — analytic same-path environmental sign boundary and skin-temperature sensitivity.
16. **`supply_limit_audit.py`** — conservative capacity/feed classification retained separately from the explicit partial-wetness solution.
17. **`heat_spreader_2d.py`** — anisotropic 2-D lateral heat-routing model.
18. **`water_salt_1d.py`** — normalized water/nonvolatile-salt mass-balance screen.

All are screening or analytic models. None is a validated CFD replacement or physical garment-performance measurement.

## Key current findings

### Rib area and ambient access

Tighter ribs do not provide proportional benefit when they share a stagnant humidity layer. Geometric area is not accessible evaporative area.

### Covered corridors

Long wet covered/end-renewed corridors can contain nonzero natural flow while remaining nearly saturated. Upward velocity and axial Péclet number are not success metrics by themselves.

### Open-valley segmentation

For the representative 6 × 3 mm distributed screen, the exchange length is roughly 0.7–1.1 mm. Thus 20–50 mm interruption alone does not rescue a weakly laterally renewed interior. Continuous lateral opening is the primary hypothesis; 1–3 mm segmentation is retained as an extreme mechanism test.

### Renewal quality versus absolute transfer

Local renewal quality is

\[
F=\frac{R}{1+R}.
\]

Absolute local series conductance is

\[
k_{eff}=\frac{k_wk_a}{k_w+k_a}=k_wF.
\]

High `F` alone can select a low-transfer design. Pair it with evaporation flux / `k_eff` and signed body-side heat flow.

### Positive evaporation versus body cooling

`open_valley_thermal_1d.py` shows that positive evaporation can coexist with negative body-side heat flow in hot ambient conditions. Heater power/signed body heat flux remains the integrated endpoint.

### Feed-limited partial wetness

`open_valley_feed_limited.py` introduces a homogenized sub-grid wet fraction `beta`.

If fully-wet evaporation capacity is below the available feed, `beta=1` and the state is transfer-limited. If fully-wet capacity exceeds feed, the solver finds `0<beta<1` such that predicted evaporation equals feed.

At 35 °C / 50% RH with 150 g/h over 0.195 m² of structured area, strong linked-exchange cases become supply-limited. The model predicts that making linked exchange stronger beyond water-supply saturation can **reduce body-coupled cooling** even while the same water mass is evaporated.

This occurs because a larger fraction of latent heat is supplied by warm ambient air. `beta` is not a measured visible wet-area fraction.

### Wet/dry two-temperature audit

`wet_dry_two_node.py` tests the one-temperature `beta` approximation by assigning distinct wet and dry temperatures at fixed feed.

For the deliberately symmetric 35 °C / 50% RH reference:

- no lateral mixing permits a wet/dry temperature split near 4.9 °C;
- increasing heat-spreader mixing progressively collapses the local temperature difference;
- the required wet fraction changes with mixing;
- **the area-integrated body heat flux remains nearly invariant** because the wet and dry patches have identical body and ambient sensible coefficients and internal lateral heat transfer cancels globally.

This establishes a sharper condition: heat spreading changes total cooling only when there is spatial heterogeneity in evaporation, ambient exposure, body coupling, shielding, sink placement, or other boundary conditions.

### Asymmetric wet/dry spreader result

`asymmetric_wet_dry_spreader.py` deliberately gives the dry region a lower ambient sensible coefficient than the wet evaporator. Under that asymmetry, heat spreading routes heat from the dry/body-coupled region into the active wet evaporator and increases total modeled body heat removal.

The nonlinear solve now uses bounded least squares plus an equation-residual acceptance test and supports continuation in `g_mix`. This change was made after a dense sweep exposed nonphysical branch jumps from the earlier unconstrained root formulation.

For the representative `h_dry=5 W/(m² K)` screen, the approximate `g_mix` needed to reach 90% of the high-mixing asymptotic gain is about 117, 192, 285, 330 and 258 W/(m² K) at 30, 50, 75, 100 and 150 g/h feed respectively.

The corresponding asymptotic high-mixing gains over 0.195 m² are finite: roughly 3.0, 4.5, 5.7, 6.0 and 3.5 W. Infinite conductivity is therefore not the objective.

### Material / geometry mapping of `g_mix`

For an ideal periodic alternating wet/dry stripe topology,

\[
g_{sheet}\approx \Gamma\frac{k_{\parallel}tc}{P^2},\qquad \Gamma=4.
\]

This is a low-order geometry mapping, not a validated textile correlation.

The main result is the quadratic pitch penalty: required `k*t` grows as `P²`. For a representative 100 g/h / 90%-gain target (`g_mix≈330 W/(m² K)`):

- abstract `k=100 W/(m K)`, `rho=1600 kg/m³`, full coverage: about 83 µm / 40 g over 0.30 m² at `P=10 mm`, but about 330 µm / 159 g at `P=20 mm`;
- abstract `k=300 W/(m K)`, `rho=1800 kg/m³`: about 28 µm / 15 g at `P=10 mm`, about 110 µm / 59 g at `P=20 mm`.

Under the simple linear coverage assumption, reducing conductive coverage and increasing thickness to preserve `g_sheet` leaves mass unchanged. A sparse network is not automatically lighter unless it changes path topology, material choice, inactive area, or another non-linear factor.

The corresponding simple mass figure of merit is `k/rho`.

### Thermal-contact burden

A two-contact screen gives

\[
\frac{1}{g_{eff}}=\frac{1}{g_{sheet}}+\frac{2}{h_c}.
\]

Thus even an infinitely conductive sheet has `g_eff < h_c/2`. For the representative `g_target≈330 W/(m² K)` case, the absolute minimum each-side contact conductance is about 660 W/(m² K). If the sheet-only conductance is only twice the target, each contact must be about 1320 W/(m² K) in this lumped model.

This is a validation burden, not a measured textile contact coefficient.

### Heat/mass coupling audit

The thermal sensitivity model defines

\[
\Xi=\delta_{vapor}/\delta_{heat}.
\]

At 40 °C / 70% RH, current zero-body-flux critical `Xi` values are roughly 0.31–0.65 across the screened vapor-side range.

The same-boundary baselines are much less selective:

- same exchange length: `Xi=1`;
- Chilton–Colburn-style equal-j-factor comparison: `Xi_CC=Le^{-1/3}`, also near one for the current air/water-vapor screen.

This does **not** establish an exact textile correlation. It shows that the hot-ambient sensitivity result requires a distinct physical mechanism rather than merely assuming arbitrary heat/vapor decoupling.

### Environmental sign boundary

For the same-path heat/vapor baseline, zero body-side heat flow satisfies

\[
\frac{k_{air}}{D_v}(T_\infty-T_{skin})
=
L_v[\rho_{v,sat}(T_{skin})-\phi_\infty\rho_{v,sat}(T_\infty)].
\]

At a 34 °C artificial-skin setpoint, the model boundary is about 39.73 °C at 70% RH. It changes materially with skin setpoint.

This is a model sign boundary, not a human safety/medical threshold.

## Run

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python simulations/open_valley_thermal_1d.py
python simulations/open_valley_feed_limited.py
python simulations/wet_dry_two_node.py
python simulations/asymmetric_wet_dry_spreader.py
python simulations/spreader_material_mapping.py
python simulations/open_valley_heat_mass_coupling_audit.py
python simulations/passive_environment_boundary.py
python simulations/supply_limit_audit.py
python simulations/generate_reference_outputs.py --output-root generated-reference
```

## Interpretation rules

Do not use any one of these as proof of garment cooling:

- geometric surface area;
- a single lumped `M`;
- corridor velocity;
- axial Péclet number;
- local `F`;
- evaporation mass flux;
- fully-wet transfer capacity;
- model wet fraction `beta`;
- internal heat-spreader conductance in a spatially symmetric model;
- a high sheet `k` without routing pitch/contact constraints;
- a `g_mix` mapping that ignores topology/contact resistance.

Integrated interpretation requires:

1. local vapor renewal (`F` / T-RH field);
2. absolute vapor transfer (`k_eff` / evaporation mass);
3. signed body-side heat flow / heater power;
4. available water supply, wetness state, retention and runoff;
5. ambient sensible heat pickup / latent heat-source partition;
6. explicit artificial-skin temperature;
7. spatial boundary-condition heterogeneity when claiming a heat-spreader benefit;
8. an identified physical mechanism for any claimed heat/vapor selectivity;
9. explicit heat-spreader routing length, `k*t`, topology and thermal-contact burden.

## Current next model tasks

1. distributed wet/dry field with unequal local body/ambient boundary conditions and direct material `k`, thickness and contact terms;
2. geometry-resolved 2-D/3-D external natural-convection/cross-flow;
3. use that flow field to constrain heat/mass transfer and re-test low-order coupling assumptions;
4. re-test lumped-model multi-equilibrium behavior against improved external-flow physics;
5. sensitivity to Nu/Sh, compression, opening losses, radiation and weak external drift.

See `docs/current-results.md`, `docs/spreader-material-mapping.md`, `docs/open-valley-thermal-model.md`, `docs/feed-limited-open-valley.md`, `docs/passive-environment-boundary.md`, `docs/measurement-uncertainty-budget.md`, and the E3c/E4a/E4/E6 experiment protocols.
