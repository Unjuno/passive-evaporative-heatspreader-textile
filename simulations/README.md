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

The model reports both axial mass Péclet number and vapor-driving-force retention. A large axial Péclet number does not imply useful renewal if the air nearly equilibrates with the wet wall.

### `open_valley_exchange_target.py`

Local analytic target and measurement-inversion model for a laterally open valley.

It defines:

- `R = G_a/G_w`, lateral ambient-renewal conductance divided by wet-surface vapor conductance;
- `F = R/(1+R)`, retained wet-wall vapor driving-force fraction.

It does not predict `R` from geometry. Its role is to state a falsifiable renewal target and to identify `F/R` from measured T/RH where the inverse problem is well-conditioned.

### `open_valley_distributed_1d.py`

Distributed one-dimensional vapor model for an open valley. It includes:

- axial molecular diffusion;
- optional signed axial advection;
- distributed wet-surface vapor input;
- distributed lateral exchange with ambient;
- ambient vapor loading at both ends.

The current geometry mapping uses an effective lateral diffusion thickness `delta_open`, which is a **model parameter**, not a literal garment dimension.

Key audit findings:

- for the screened 6 × 3 mm valley, the exchange length is roughly 0.7–1.1 mm across the tested lateral-exchange range;
- therefore 20–50 mm interruptions are too coarse to materially alter the long-valley center state when lateral exchange is weak;
- 1–3 mm end-connected segments can materially improve retained vapor driving force;
- few-mm/s axial flow does not rescue a 50 mm weakly renewed valley center;
- `F` cannot be optimized alone.

The module also reports

`k_eff = k_w * k_a / (k_w + k_a) = k_w * F`

because high `F` can be produced by lowering the wet-wall transfer coefficient, which may reduce absolute evaporation capacity.

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
python simulations/open_valley_exchange_target.py
python simulations/open_valley_distributed_1d.py
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

A larger `M_h` can increase inward sensible heat pickup in hot ambient air while a larger `M_m` can improve evaporation. The two mechanisms must not be collapsed into one score.

## Open-valley interpretation

The current air-renewal hierarchy is:

1. local conductance requirement/measurement inversion (`open_valley_exchange_target.py`);
2. distributed 1-D axial diffusion/advection plus lateral renewal (`open_valley_distributed_1d.py`);
3. future thermal/vapor coupling and 2-D/3-D external-flow treatment.

The distributed model corrects two earlier design shortcuts:

- centimeter-scale segmentation is not automatically enough;
- high local driving-force retention `F` is not automatically high evaporation capacity.

Every laterally open design should therefore be evaluated with both:

- renewal quality (`F`, local vapor loading);
- absolute transfer or cooling (`k_eff`, evaporation mass flux, and ultimately heater-power difference).

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
6. local open-valley renewal target — measurable conductance-ratio requirement;
7. distributed open-valley vapor model — axial diffusion/advection plus distributed lateral renewal;
8. 2D heat-spreader model — lateral conduction and patchy cooling sinks;
9. water/salt model — liquid water, phase change, nonvolatile salt transport;
10. next coupled open-valley thermal model / CFD — relate lateral vapor renewal to sensible heat transfer and body-side cooling without assuming `M_h=M_m`.

Each higher-fidelity model should be compared against lower-order models and physical measurements rather than silently replacing them.

See also:

- `docs/split-transfer-model.md`
- `docs/model-form-uncertainty.md`
- `docs/e3-boundary-layer-screen.md`
- `docs/corridor-buoyancy-screen.md`
- `docs/self-consistent-corridor-model.md`
- `docs/open-valley-renewal-target.md`
- `docs/open-valley-distributed-model.md`
- `docs/open-valley-metric-audit.md`
- `experiments/e3c_open_vs_covered_corridors.md`
