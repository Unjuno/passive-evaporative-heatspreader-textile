# Simulations

## Current executable model

`passive_rib_screen.py` is the consolidated low-order passive exterior model.

Install:

```bash
python -m pip install -r requirements.txt
```

Run:

```bash
python simulations/passive_rib_screen.py
```

Test:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## Important: multiple stable equilibria

The nonlinear surface energy/mass balance can contain more than one stable equilibrium under the frozen screening assumptions.

The model therefore exposes:

- `stable_equilibria(...)` — all detected stable roots;
- `select_equilibrium(..., policy="warm")` — conservative high-temperature branch;
- `select_equilibrium(..., policy="cool")` — low-temperature/high-cooling branch.

Do not publish a single cooling threshold without stating the root-selection policy and number of stable roots.

## Modeling hierarchy

Planned models should remain separate rather than being hidden inside one opaque script:

1. **Exterior lumped model** — current file; heat/mass exchange and rib accessibility.
2. **2D heat-spreader model** — lateral conduction and spatially patchy evaporation.
3. **Water/salt transport model** — liquid water, water vapor phase change, nonvolatile salt advection/precipitation.
4. **Boundary-layer model/CFD** — if justified by experimental data, to replace the simple effective accessibility parameter.

Each higher-fidelity model should be compared against the lower-order model and physical measurements rather than silently replacing them.
