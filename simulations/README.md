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
15. `distributed_spreader_1d.py` — replaces scalar `g_mix` with direct periodic `k*t` conduction, local contact, dry shielding, wet evaporation and feed-solved wet width.
16. `open_valley_heat_mass_coupling_audit.py` — heat/mass selectivity, Lewis number and Chilton–Colburn-style baselines.
17. `passive_environment_boundary.py` — analytic same-path hot/humid body-heat-flow sign boundary.
18. `supply_limit_audit.py` — conservative fully-wet capacity/feed classification.
19. `heat_spreader_2d.py` — anisotropic 2-D lateral heat-routing screen.
20. `water_salt_1d.py` — normalized water/nonvolatile-salt mass-balance screen.

`generate_reference_outputs.py` is the reproducibility generator rather than a physical model.

## Current design conclusions

### Ambient access dominates geometric area

Dense wet ribs can share one stagnant humidity layer. Increasing geometric area alone is not accepted as evidence of increased useful evaporation.

### Long covered wet corridors are not preferred

They can sustain nonzero natural flow while remaining nearly saturated, and thermo-solutal buoyancy can reverse flow direction. Current exterior preference is continuously laterally ambient-connected valleys, gaps or islands.

### `F` is not absolute transfer

\[
F=\frac{R}{1+R},
\qquad
k_{eff}=\frac{k_wk_a}{k_w+k_a}=k_wF.
\]

Both renewal quality and absolute conductance must be reported.

### Positive evaporation is not equivalent to body cooling

At hot ambient conditions, latent heat can be supplied partly or predominantly by ambient sensible heat. Signed body-side heat flow remains the integrated endpoint.

### Water supply is explicit

`open_valley_feed_limited.py` solves a computational sub-grid wet fraction `beta` when fully-wet capacity exceeds available feed. `beta` is not a measured visible wet area.

### Heat spreading requires spatial heterogeneity

The symmetric wet/dry screen shows that internal equalization alone does not create area-integrated cooling. The asymmetric screen produces finite benefit when the dry and wet regions have genuinely different exposure/shielding.

The asymmetric nonlinear solver uses bounded least squares, explicit equation-residual acceptance and continuation support after dense sweeps exposed nonphysical branch jumps in the earlier unconstrained formulation.

For the representative `h_dry=5 W/(m² K)` screen, approximate scalar-`g_mix` targets for 90% of high-mixing gain are 117, 192, 285, 330 and 258 W/(m² K) at 30, 50, 75, 100 and 150 g/h respectively. The corresponding mechanism gains over 0.195 m² are finite, roughly 3–6 W.

## Heat-spreader geometry / contact mapping

The ideal periodic-stripe mapping is

\[
g_{sheet}\approx \Gamma\frac{k_{\parallel}tc}{P^2},\qquad \Gamma=4.
\]

This is a low-order topology screen, not a validated textile correlation. Required `k*t` grows as routing pitch squared.

Thermal contacts are screened by

\[
\frac{1}{g_{eff}}=\frac{1}{g_{sheet}}+\frac{2}{h_c}.
\]

A high-`k` sheet therefore cannot deliver the target routing conductance if wet/dry contacts are weak.

## Virtual prototypes v0.1 — scalar anchor model

At 100 g/h:

| prototype | mass over 0.30 m² | nominal `g_eff` | scalar spreader-only gain over 0.195 m² |
|---|---:|---:|---:|
| VP-A | ~48 g | ~286 W/(m² K) | ~5.3 W |
| VP-B | ~96 g | ~167 | ~4.9 W |
| VP-C | ~27 g | ~197 | ~5.0 W |
| VP-D | ~48 g | ~286 | ~6.1 W |

The gains are relative to the same local wet/dry model with `g_mix=0`; they are not total garment-vs-control cooling predictions.

## Direct-material distributed bridge model

`distributed_spreader_1d.py` replaces `g_mix` with

\[
\frac{d}{dx}\left(k_{\parallel}t\frac{dT_s}{dx}\right)
+U_b(T_{skin}-T_s)+h_c(T_o-T_s)=0.
\]

The outer layer locally exchanges sensible heat with ambient air and latent heat over the wet fraction. Wet-stripe width is solved continuously so integrated evaporation matches feed when capacity permits.

At 100 g/h, equal-feed no-lateral baseline comparison gives:

| prototype | solved wet fraction | distributed spreader-only gain over 0.195 m² |
|---|---:|---:|
| VP-A | ~0.444 | ~5.48 W |
| VP-B | ~0.448 | ~5.32 W |
| VP-C | ~0.451 | ~5.30 W |
| VP-D | ~0.447 | ~6.29 W |

Numerical checks in the development screen:

- feed closure better than ~0.001 g/h;
- outer energy residual numerically near zero;
- spreader equation residual ~0.004 W/m² or below;
- VP-A 32→96 node body-flux change ~0.01 W/m²;
- distributed gains remain within roughly 0.8 W of the scalar virtual-anchor gains.

The latter is model-hierarchy continuity, not independent validation, because both models share exterior/body assumptions.

VP-C's 50% routed coverage is still homogenized as effective thickness `t_eff=t*coverage`; actual sparse traces are not yet geometry-resolved.

## Run

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python simulations/asymmetric_wet_dry_spreader.py
python simulations/spreader_material_mapping.py
python simulations/virtual_prototype_v01.py
python simulations/distributed_spreader_1d.py
python simulations/generate_reference_outputs.py --output-root generated-reference
```

## Interpretation rules

Do not use any one of the following as proof of garment cooling:

- geometric surface area;
- one lumped exchange multiplier;
- corridor velocity or axial Péclet number;
- local `F`;
- evaporation mass alone;
- fully-wet capacity above feed;
- model wet fraction `beta`;
- scalar `g_mix` under symmetric boundary conditions;
- high sheet `k` without routing/contact constraints;
- homogenized sparse coverage as proof of trace-level performance;
- virtual-prototype spreader-only gain as total garment performance.

Integrated interpretation requires vapor renewal, absolute vapor transfer, signed body heat flow, water supply/wetness state, ambient sensible pickup, spatially heterogeneous wet/dry boundary conditions, material `k*t/P²`, contacts, added mass and explicit hot-ambient protection.

## Next model task

Move from the periodic 1-D bridge to a **2-D geometry-resolved spreader** with anisotropic `k_x/k_y`, explicit routed traces/sparse coverage, spatially varying contact, wet islands, dry shielding and garment curvature/compression. VP-A through VP-D remain regression anchors.

See `docs/distributed-spreader-1d.md`, `docs/virtual-prototypes-v0.1.md`, `docs/current-results.md`, and `AUDIT.md`.
