# Simulations

## Executable models

### `passive_rib_screen.py`

Consolidated low-order passive exterior heat/mass-transfer model. It compares a structured evaporative textile against a flat wet reference at equal liquid-water input and explicitly reports multiple stable surface-temperature equilibria when detected.

This legacy/consolidated screen uses one exterior multiplier `M` for both sensible convection and vapor transfer. It remains useful as a historical/reference special case.

### `split_heat_mass_screen.py`

Refined low-order thermal model with independent external multipliers:

- `M_h` for sensible convective heat transfer;
- `M_m` for water-vapor mass transfer.

Radiation is parameterized separately. Setting `M_h = M_m = M` reproduces the older coupled formulation and is regression-tested.

### `split_transfer_sensitivity.py`

Deterministic sensitivity grid over RH, body-to-evaporator coupling, radiative exchange, `M_h`, and `M_m`. Reported fractions are deterministic grid fractions, **not probabilities or confidence intervals**.

### `rib_diffusion_screen.py`

Periodic 2-D steady vapor-diffusion model for wet exterior ribs under an idealized refreshed-air plane. It isolates boundary-layer sharing and reports a whole-area vapor mass-transfer multiplier.

This is pure diffusion, not CFD. The prescribed air-renewal boundary is the dominant model-form assumption.

### `corridor_buoyancy_screen.py`

Low-order moist-air buoyancy screen for vertical macro corridors. It balances hydrostatic density head against laminar slot friction. Channel temperature and RH are prescribed inputs, so this model is a sign/scaling precursor rather than a self-consistent channel solution.

### `self_consistent_corridor_1d.py`

Low-order self-consistent rectangular-corridor model. It solves together:

- signed buoyancy/friction velocity;
- wet-wall temperature;
- mean/outlet channel temperature and RH;
- evaporation flux;
- body-side wet-wall heat flux.

The geometry is a **covered/end-renewed limiting case**. It does not include distributed lateral ambient exchange, so it must not be generalized directly to an open exterior valley.

The model reports both:

- axial mass Péclet number `Pe_m = |u| L / D_v`;
- mean vapor-driving-force retention `Phi(NTU_m) = (1-exp(-NTU_m))/NTU_m`.

This distinction is important: a long channel can have `Pe_m > 10` while retaining almost none of the inlet vapor driving force because the air has nearly equilibrated with the wet wall.

### `heat_spreader_2d.py`

Steady 2D finite-volume model that isolates lateral heat routing in an isotropic or anisotropic flexible spreader. Evaporation is represented by a prescribed effective sink; this model does **not** predict evaporation mass transfer.

### `water_salt_1d.py`

Normalized one-dimensional water/salt mass-balance screen. Salt is nonvolatile: water can evaporate, while salt remains in liquid/solid phases.

## Install

```bash
python -m pip install -r requirements.txt
```

## Run current model demos

```bash
python simulations/passive_rib_screen.py
python simulations/split_heat_mass_screen.py
python simulations/split_transfer_sensitivity.py
python simulations/rib_diffusion_screen.py
python simulations/corridor_buoyancy_screen.py
python simulations/self_consistent_corridor_1d.py
python simulations/heat_spreader_2d.py
python simulations/water_salt_1d.py
```

## Test

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## Important: multiple stable equilibria

The nonlinear surface energy/mass balance can contain more than one stable equilibrium under the frozen screening assumptions.

The models therefore expose all stable roots or use an explicit warm/conservative branch-selection policy. Do not publish a single cooling threshold without stating the root-selection policy and number of stable roots.

## Split-transfer interpretation

The recommended low-order external balance is conceptually:

`body heat + M_h * sensible convection + radiation - latent evaporation(M_m) = 0`

This matters when ambient air is hotter than the wet exterior. A larger `M_h` can increase inward sensible heat pickup, while a larger `M_m` can increase evaporation capacity if vapor-pressure driving force remains positive.

The two multipliers may still be physically coupled by flow; independence is an uncertainty tool, not a claim that the mechanisms are unrelated.

## Corridor interpretation

The corridor models now form a hierarchy:

1. **Prescribed-state buoyancy screen** — asks whether a given T/RH channel state tends upward or downward.
2. **Self-consistent end-renewed 1-D corridor** — solves velocity, wall T, and channel T/RH together for a covered rectangular-duct limit.
3. **Next model: laterally open valley** — must add distributed lateral ambient exchange and low-Pe axial diffusion/advection-diffusion.

The self-consistent screen indicates that natural buoyancy in shallow end-renewed channels can be too weak to prevent near-saturation at 35 °C / 70% RH. It also shows that stronger downward flow in hot ambient air can coincide with inward sensible heat flow. Therefore the current garment direction favors laterally open valleys, short/segmented paths, cross-openings, and discontinuous evaporator fields rather than long covered chimneys.

## 2D heat-spreader interpretation

The 2D model solves a steady equation of the form:

`div(t K_parallel grad(T)) + g_body (T_skin - T) - g_sink(x,y)(T - T_sink) = 0`

with no-flux outer boundaries.

For the included demonstration geometry, the cooling sink is a vertical band on the right side. Regression tests require the high-conductivity axis directed toward that band to route more body-side heat than the same anisotropy rotated by 90 degrees.

## Modeling hierarchy

Keep models separate rather than hiding assumptions inside one opaque solver:

1. coupled exterior lumped model — historical/reference `M` formulation and multi-root audit;
2. split exterior lumped model — separate `M_h`, `M_m`, radiation, liquid-supply limit, and multi-root behavior;
3. periodic vapor-diffusion model — rib geometry/boundary-layer sharing and candidate constraints on `M_m`;
4. prescribed-state corridor buoyancy screen — thermo-solutal flow sign/scaling;
5. self-consistent end-renewed corridor model — coupled T/RH/flow limit for covered channels;
6. 2D heat-spreader model — lateral conduction and patchy cooling sinks;
7. water/salt model — liquid water, phase change, nonvolatile salt transport;
8. future open-valley advection-diffusion/CFD — distributed lateral exchange, entrance/opening effects, and physical coupling of `M_h`/`M_m`.

Each higher-fidelity model should be compared against lower-order models and physical measurements rather than silently replacing them.

See also:

- `docs/split-transfer-model.md`
- `docs/model-form-uncertainty.md`
- `docs/e3-boundary-layer-screen.md`
- `docs/corridor-buoyancy-screen.md`
- `docs/self-consistent-corridor-model.md`
- `experiments/e3c_open_vs_covered_corridors.md`
