# Simulations

## Executable models

### `passive_rib_screen.py`

Consolidated low-order passive exterior heat/mass-transfer model. It compares a structured evaporative textile against a flat wet reference at equal liquid-water input and explicitly reports multiple stable surface-temperature equilibria when detected.

This legacy/consolidated screen uses one exterior multiplier `M` for both sensible convection and vapor transfer. It remains useful as a historical/reference special case.

### `split_heat_mass_screen.py`

Refined low-order thermal model with independent external multipliers:

- `M_h` for sensible convective heat transfer;
- `M_m` for water-vapor mass transfer.

Radiation is parameterized separately. Setting `M_h = M_m = M` reproduces the older coupled-multiplier formulation at the same conditions; a regression test enforces that equivalence.

Use this model when connecting E3 vapor-transfer results to the thermal balance. **E3 constrains `M_m`, not `M_h`.**

### `split_transfer_sensitivity.py`

Deterministic sensitivity grid over RH, body-to-evaporator coupling, radiative exchange, `M_h`, and `M_m`.

The reported fractions are fractions of a predeclared screening grid. They are **not probabilities, reliability estimates, or confidence intervals**.

### `rib_diffusion_screen.py`

Periodic 2-D steady vapor-diffusion model for wet exterior ribs under an idealized refreshed-air plane. It isolates boundary-layer sharing and reports a whole-area vapor mass-transfer multiplier.

This is pure diffusion, not CFD. The air-renewal boundary is currently the dominant model-form assumption.

### `corridor_buoyancy_screen.py`

Low-order moist-air buoyancy screen for vertical macro air-renewal corridors. It balances hydrostatic density head against laminar parallel-plate slot friction and reports signed flow tendency, Reynolds number, vapor Peclet number, and a neutral-density humidity curve.

The channel temperature and RH are prescribed inputs; they are **not solved self-consistently**. This model is intended to test whether evaporative cooling and humidification can reinforce or oppose each other and can reverse the expected chimney-flow direction.

### `heat_spreader_2d.py`

Steady 2D finite-volume model that isolates lateral heat routing in an isotropic or anisotropic flexible spreader. Evaporation is represented only by a prescribed effective sink; this model does **not** predict evaporation mass transfer. Its purpose is to test whether heat-spreader topology and orientation can move heat from a larger body area toward spatially localized cooling zones.

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

The recommended low-order external balance is now conceptually:

`body heat + M_h * sensible convection + radiation - latent evaporation(M_m) = 0`

This matters when ambient air is hotter than the wet exterior. A larger `M_h` can increase inward sensible heat pickup, while a larger `M_m` can increase evaporation capacity if vapor-pressure driving force remains positive.

The two multipliers may still be physically coupled by buoyancy and boundary-layer flow; independence is an uncertainty tool, not a claim that the mechanisms are unrelated.

## Corridor-buoyancy interpretation

A vertical macro corridor does not automatically create a beneficial upward chimney flow. Evaporation tends to cool the air, increasing density, while humidification lowers density at fixed temperature. Under hot/humid conditions the two effects can oppose each other strongly.

The current screen therefore evaluates the sign of

`rho_ambient - rho_channel`

before assigning an idealized upward/downward slot-flow tendency. The next step is to solve channel temperature and humidity along the flow direction rather than prescribe them.

## 2D heat-spreader interpretation

The 2D model solves a steady equation of the form:

`div(t K_parallel grad(T)) + g_body (T_skin - T) - g_sink(x,y)(T - T_sink) = 0`

with no-flux outer boundaries.

For the included demonstration geometry, the cooling sink is a vertical band on the right side. The regression tests therefore require the high-conductivity axis directed toward that band to route more body-side heat than the same anisotropy rotated by 90 degrees.

This is a topology/heat-routing result, not a prediction of wet-surface temperature or garment cooling power.

## Modeling hierarchy

Keep models separate rather than hiding assumptions inside one opaque solver:

1. **Coupled exterior lumped model** — historical/reference `M` formulation and multi-root audit.
2. **Split exterior lumped model** — separate `M_h`, `M_m`, radiation, liquid-supply limit, and multi-root behavior.
3. **Periodic vapor-diffusion model** — geometric rib/boundary-layer sharing and candidate constraints on `M_m`.
4. **Moist-air corridor buoyancy screen** — sign/scaling of macro-channel air-renewal tendency with prescribed channel state.
5. **2D heat-spreader model** — lateral conduction and spatially patchy cooling sinks.
6. **Water/salt transport model** — liquid water, water vapor phase change, nonvolatile salt advection/precipitation.
7. **Future coupled corridor model / CFD** — solve channel heat + vapor conservation and flow together, replacing the prescribed E3 renewal plane and prescribed corridor state.

Each higher-fidelity model should be compared against lower-order models and physical measurements rather than silently replacing them.

See also:

- `docs/split-transfer-model.md`
- `docs/model-form-uncertainty.md`
- `docs/e3-boundary-layer-screen.md`
- `docs/corridor-buoyancy-screen.md`
