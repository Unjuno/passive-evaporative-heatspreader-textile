# Simulations

## Executable model hierarchy

### 1. `passive_rib_screen.py`

Historical low-order exterior heat/mass model. It uses one multiplier `M` for both sensible and vapor transfer and exposes multiple stable equilibria when present. Retained as a reference/special case.

### 2. `split_heat_mass_screen.py`

Lumped thermal model with separate:

- `M_h` — sensible convective transfer;
- `M_m` — vapor mass transfer;
- radiation.

`M_h=M_m=M` reproduces the historical coupled model as a regression-tested special case.

### 3. `split_transfer_sensitivity.py`

Deterministic model-form sensitivity over RH, body coupling, radiation, `M_h`, and `M_m`. Grid fractions are not probabilities or confidence intervals.

### 4. `rib_diffusion_screen.py`

Periodic 2-D steady vapor diffusion around wet ribs under an idealized refreshed-air plane. It isolates boundary-layer sharing. Pure diffusion; not CFD.

### 5. `corridor_buoyancy_screen.py`

Prescribed-state moist-air buoyancy / laminar corridor screen. Tests flow sign and scaling; channel T/RH are inputs.

### 6. `self_consistent_corridor_1d.py`

Covered/end-renewed rectangular-corridor limit. Couples signed buoyancy/friction velocity, wet-wall temperature, channel T/RH, evaporation, and body-side heat flow.

Main audit result: nonzero flow or high axial Péclet number does not guarantee vapor renewal; long wet covered channels can remain nearly saturated.

### 7. `open_valley_exchange_target.py`

Local analytic open-valley target and measurement inversion:

\[
R=G_a/G_w,
\qquad F=R/(1+R).
\]

`F` is the preferred local renewal-quality metric; exact high `R` is secondary because the inverse measurement becomes ill-conditioned.

### 8. `open_valley_distributed_1d.py`

Distributed vapor model with axial molecular diffusion, optional axial advection, wet-surface vapor input, and distributed lateral ambient renewal.

Key corrections:

- representative exchange length is roughly 0.7–1.1 mm for the 6×3 mm screened valley;
- 20–50 mm interruption does not rescue a weakly laterally renewed interior;
- few-mm/s axial flow is insufficient to rescue a 50 mm valley center in the current screen;
- `F` must be paired with absolute series conductance
  `k_eff = k_w k_a/(k_w+k_a)`.

### 9. `open_valley_thermal_1d.py`

Coupled open-valley thermal/vapor screen. Solves iteratively for:

- valley-air dry-bulb temperature;
- valley water-vapor density;
- wet-surface temperature;
- evaporation mass flux;
- body-to-wet-surface heat flux;
- ambient-air sensible heat supplied to the wet surface.

Lateral heat and vapor exchange are parameterized separately through effective `delta_heat` and `delta_vapor`. Equality is a Lewis-like screening baseline, not a validated law for the textile.

Important findings:

- stronger vapor renewal increases body-side cooling in the primary 35 °C / 70% RH screen;
- positive evaporation can coexist with **negative body-side heat flux** at 40 °C / 70% RH;
- the solver is currently a transfer-capacity model without an explicit liquid-feed cap, so dry/high-renewal cases must be labeled supply-limited when predicted capacity exceeds available feed.

Regression tests enforce wet-wall energy closure:

`q_body + q_air = L_v * m_evap`.

### 10. `heat_spreader_2d.py`

Steady 2-D finite-volume lateral heat-routing model. Evaporation is represented only by a prescribed sink. Used for topology/orientation studies.

### 11. `water_salt_1d.py`

Normalized water/salt mass-balance screen. Salt is nonvolatile; water can evaporate while salt remains in liquid/solid phases.

## Install and run

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python simulations/open_valley_distributed_1d.py
python simulations/open_valley_thermal_1d.py
python simulations/generate_reference_outputs.py --output-root generated-reference
```

## Audit rules for model interpretation

Do not use any one of the following as proof of garment cooling:

- geometric exterior area;
- a single lumped `M` threshold;
- upward corridor velocity;
- axial Péclet number;
- local `F` alone;
- evaporation mass flux alone.

Integrated interpretation requires at minimum:

1. local vapor renewal (`F` / T/RH field);
2. absolute evaporation transfer (`k_eff` or mass flux);
3. body-side heat flow / heater power;
4. available liquid supply and runoff;
5. hot-ambient sensible heat pickup.

## Current next model tasks

1. explicit feed-limited coupled open-valley solution;
2. physically constrain heat/mass coupling with Lewis/Chilton-Colburn-style treatment instead of arbitrary independent exchange distances;
3. geometry-resolved 2-D/3-D external natural-convection/cross-flow treatment;
4. re-test lumped-model multi-equilibrium behavior against the improved external-flow physics.

See:

- `docs/current-results.md`
- `docs/open-valley-renewal-target.md`
- `docs/open-valley-distributed-model.md`
- `docs/open-valley-metric-audit.md`
- `docs/open-valley-thermal-model.md`
- `experiments/e3c_open_vs_covered_corridors.md`
