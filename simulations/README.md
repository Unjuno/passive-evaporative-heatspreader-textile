# Simulations

## Executable models

### `passive_rib_screen.py`

Consolidated low-order passive exterior heat/mass-transfer model. It compares a structured evaporative textile against a flat wet reference at equal liquid-water input and explicitly reports multiple stable surface-temperature equilibria when detected.

### `heat_spreader_2d.py`

Steady 2D finite-volume model that isolates lateral heat routing in an isotropic or anisotropic flexible spreader. Evaporation is represented only by a prescribed effective sink; this model does **not** predict evaporation mass transfer. Its purpose is to test whether heat-spreader topology and orientation can move heat from a larger body area toward spatially localized cooling zones.

Install:

```bash
python -m pip install -r requirements.txt
```

Run both current model demos:

```bash
python simulations/passive_rib_screen.py
python simulations/heat_spreader_2d.py
```

Test:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## Important: multiple stable equilibria

The nonlinear surface energy/mass balance in `passive_rib_screen.py` can contain more than one stable equilibrium under the frozen screening assumptions.

The model therefore exposes:

- `stable_equilibria(...)` — all detected stable roots;
- `select_equilibrium(..., policy="warm")` — conservative high-temperature branch;
- `select_equilibrium(..., policy="cool")` — low-temperature/high-cooling branch.

Do not publish a single cooling threshold without stating the root-selection policy and number of stable roots.

## 2D heat-spreader interpretation

The 2D model solves a steady equation of the form:

`div(t K_parallel grad(T)) + g_body (T_skin - T) - g_sink(x,y)(T - T_sink) = 0`

with no-flux outer boundaries.

For the included demonstration geometry, the cooling sink is a vertical band on the right side. The regression tests therefore require the high-conductivity axis directed toward that band to route more body-side heat than the same anisotropy rotated by 90 degrees.

This is a topology/heat-routing result, not a prediction of wet-surface temperature or garment cooling power.

## Modeling hierarchy

Keep models separate rather than hiding assumptions inside one opaque solver:

1. **Exterior lumped model** — heat/mass exchange, liquid-supply limit, rib accessibility, multiple equilibria.
2. **2D heat-spreader model** — lateral conduction and spatially patchy cooling sinks.
3. **Water/salt transport model** — liquid water, water vapor phase change, nonvolatile salt advection/precipitation; governing specification exists, numerical solver pending.
4. **Boundary-layer model/CFD** — if justified by experiment, replace or constrain the empirical effective-accessibility parameter.

Each higher-fidelity model should be compared against lower-order models and physical measurements rather than silently replacing them.
