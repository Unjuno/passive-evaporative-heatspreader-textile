# Simulations

Status: **screening / analytic / virtual-prototype models only**. No physical garment or bench specimen currently exists.

## Executable model / audit hierarchy

1. `passive_rib_screen.py` — historical low-order exterior heat/mass model and multi-root audit.
2. `split_heat_mass_screen.py` — separate sensible `M_h`, vapor `M_m`, and radiation.
3. `split_transfer_sensitivity.py` — deterministic model-form sensitivity grid.
4. `rib_diffusion_screen.py` — periodic 2-D wet-rib vapor diffusion under an idealized renewal plane.
5. `corridor_buoyancy_screen.py` — prescribed-state thermo-solutal corridor flow sign/scaling.
6. `self_consistent_corridor_1d.py` — covered/end-renewed corridor T/RH/flow/evaporation coupling.
7. `open_valley_exchange_target.py` — local `R=G_a/G_w`, `F=R/(1+R)` target and measurement inversion.
8. `open_valley_distributed_1d.py` — axial diffusion/advection plus distributed lateral vapor renewal.
9. `open_valley_thermal_1d.py` — coupled valley-air T, vapor density, wet-surface T, evaporation and body-side heat flow.
10. `open_valley_feed_limited.py` — explicit homogenized feed-limited partial-wetness closure and latent heat-source partition.
11. `wet_dry_two_node.py` — separate wet/dry temperatures under symmetric local sensible boundary conditions.
12. `asymmetric_wet_dry_spreader.py` — bounded/continuation wet/dry mechanism screen with unequal dry/wet exposure.
13. `spreader_material_mapping.py` — maps abstract `g_mix` to `k*t/pitch^2`, mass, bend-strain screening and contact resistance.
14. `virtual_prototype_v01.py` — explicit VP-A/VP-B/VP-C/VP-D computational design anchors and topology/contact sensitivity.
15. `open_valley_heat_mass_coupling_audit.py` — heat/mass selectivity, Lewis number and Chilton–Colburn-style baselines.
16. `passive_environment_boundary.py` — analytic same-path hot/humid body-heat-flow sign boundary.
17. `supply_limit_audit.py` — conservative fully-wet capacity/feed classification.
18. `heat_spreader_2d.py` — anisotropic 2-D lateral heat-routing screen.
19. `water_salt_1d.py` — normalized water/nonvolatile-salt mass-balance screen.

`generate_reference_outputs.py` is the reproducibility generator rather than a physical model.

## Current design conclusions

### Ambient access dominates geometric area

Dense wet ribs can share one stagnant humidity layer. Increasing geometric area alone is not accepted as evidence of increased useful evaporation.

### Long covered wet corridors are not preferred

They can sustain nonzero natural flow while remaining nearly saturated, and thermo-solutal buoyancy can reverse flow direction. Current exterior preference is continuously laterally ambient-connected valleys, gaps or islands.

### `F` is not absolute transfer

Local renewal quality

\[
F=\frac{R}{1+R}
\]

must be paired with absolute conductance

\[
k_{eff}=\frac{k_wk_a}{k_w+k_a}=k_wF.
\]

### Positive evaporation is not equivalent to body cooling

At hot ambient conditions, latent heat can be supplied partly or predominantly by ambient sensible heat. Signed body-side heat flow remains the integrated endpoint.

### Water supply is explicit

`open_valley_feed_limited.py` solves a computational sub-grid wet fraction `beta` when fully-wet capacity exceeds available feed. `beta` is not a measured visible wet area.

### Heat spreading requires spatial heterogeneity

The symmetric wet/dry screen shows that internal equalization alone does not create area-integrated cooling. The asymmetric screen produces finite benefit when the dry and wet regions have genuinely different exposure/shielding.

The asymmetric nonlinear solver uses bounded least squares, explicit equation-residual acceptance and continuation support. This replaced an earlier unconstrained solve after dense sweeps exposed nonphysical branch jumps.

For the representative `h_dry=5 W/(m² K)` screen, approximate `g_mix` for 90% of high-mixing gain is:

| feed | target `g_mix` |
|---:|---:|
| 30 g/h | ~117 W/(m² K) |
| 50 g/h | ~192 W/(m² K) |
| 75 g/h | ~285 W/(m² K) |
| 100 g/h | ~330 W/(m² K) |
| 150 g/h | ~258 W/(m² K) |

The corresponding asymptotic mechanism gains over 0.195 m² are finite, roughly 3–6 W.

### Heat-spreader geometry is now explicit

The ideal periodic-stripe mapping is

\[
g_{sheet}\approx \Gamma\frac{k_{\parallel}tc}{P^2},\qquad \Gamma=4.
\]

This is a low-order topology screen, not a validated textile correlation. The key implication is the quadratic routing-distance penalty: required `k*t` grows as `P²`.

A contact audit uses

\[
\frac{1}{g_{eff}}=\frac{1}{g_{sheet}}+\frac{2}{h_c}.
\]

Thus a high-`k` sheet cannot provide the target effective routing conductance if wet/dry contacts are weak.

## Virtual prototypes v0.1

At 100 g/h in the current asymmetric mechanism model:

| prototype | routing / property concept | spreader mass over 0.30 m² | nominal `g_eff` | modeled spreader-only gain over 0.195 m² |
|---|---|---:|---:|---:|
| VP-A | 10 mm, `k=100`, 100 µm, strong contact | ~48 g | ~286 W/(m² K) | ~5.3 W |
| VP-B | 20 mm, same class, 200 µm | ~96 g | ~167 W/(m² K) | ~4.9 W |
| VP-C | 15 mm, 50% routed, higher `k/rho` class | ~27 g | ~197 W/(m² K) | ~5.0 W |
| VP-D | VP-A path + stronger dry-side shielding | ~48 g | ~286 W/(m² K) | ~6.1 W |

These gains are relative to the same local wet/dry model with `g_mix=0`; they are **not** total garment-vs-control cooling predictions.

Deterministic `Gamma=2–4` and each-side contact `500–5000 W/(m² K)` sensitivity gives approximate 100 g/h gain ranges:

- VP-A: 4.4–5.4 W;
- VP-B: 3.9–5.0 W;
- VP-C: 4.1–5.2 W;
- VP-D: 5.1–6.2 W.

The ranges are model-form sensitivity, not probabilities.

## Run

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python simulations/open_valley_thermal_1d.py
python simulations/open_valley_feed_limited.py
python simulations/asymmetric_wet_dry_spreader.py
python simulations/spreader_material_mapping.py
python simulations/virtual_prototype_v01.py
python simulations/open_valley_heat_mass_coupling_audit.py
python simulations/passive_environment_boundary.py
python simulations/generate_reference_outputs.py --output-root generated-reference
```

## Interpretation rules

Do not use any one of the following as proof of garment cooling:

- geometric surface area;
- a single lumped exchange multiplier;
- corridor velocity or axial Péclet number;
- local `F`;
- evaporation mass alone;
- fully-wet transfer capacity above available feed;
- model `beta`;
- internal `g_mix` in a spatially symmetric model;
- high sheet `k` without routing pitch/topology/contact constraints;
- virtual-prototype spreader-only gain as total garment performance.

Integrated interpretation requires vapor renewal, absolute vapor transfer, signed body heat flow, water supply/wetness state, ambient sensible pickup, spatially heterogeneous wet/dry boundary conditions, material `k*t/P²`, thermal contacts, added mass and explicit hot-ambient protection.

## Next model task

Replace the two-node `g_mix` abstraction with a distributed 1-D/2-D wet/dry heat-routing model containing direct material `k`, thickness, anisotropy, thermal contacts, patch pitch, dry shielding and evaporative sink strength. VP-A through VP-D should remain regression anchors for that transition.

See `docs/current-results.md`, `docs/spreader-material-mapping.md`, `docs/virtual-prototypes-v0.1.md`, and `AUDIT.md`.
