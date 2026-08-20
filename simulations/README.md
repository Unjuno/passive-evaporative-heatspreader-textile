# Simulations

Status: **screening / analytic / virtual-prototype models only**. No physical garment or bench specimen currently exists.

## Executable model / audit hierarchy

### Exterior heat / vapor physics

1. `passive_rib_screen.py` — historical low-order exterior heat/mass screen and multi-root audit.
2. `split_heat_mass_screen.py` — separates sensible `M_h`, vapor `M_m`, and radiation.
3. `split_transfer_sensitivity.py` — deterministic model-form sensitivity grid.
4. `rib_diffusion_screen.py` — periodic 2-D wet-rib vapor diffusion under an idealized renewal plane.
5. `corridor_buoyancy_screen.py` — prescribed-state thermo-solutal corridor-flow sign/scaling.
6. `self_consistent_corridor_1d.py` — covered/end-renewed corridor T/RH/flow/evaporation coupling.
7. `open_valley_exchange_target.py` — local `R=G_a/G_w`, `F=R/(1+R)` target and measurement inversion.
8. `open_valley_distributed_1d.py` — axial diffusion/advection plus distributed lateral vapor renewal.
9. `open_valley_thermal_1d.py` — coupled valley-air T, vapor density, wet-surface T, evaporation and body-side heat flow.
10. `open_valley_feed_limited.py` — explicit feed-limited partial-wetness closure and latent heat-source partition.
11. `open_valley_heat_mass_coupling_audit.py` — heat/mass selectivity, Lewis number and analogy baselines.
12. `passive_environment_boundary.py` — analytic same-path hot/humid body-heat-flow sign boundary.
13. `supply_limit_audit.py` — conservative fully-wet capacity/feed classification.

### Heat routing / virtual prototypes

14. `wet_dry_two_node.py` — separate wet/dry temperatures under symmetric sensible boundaries.
15. `asymmetric_wet_dry_spreader.py` — bounded/continuation wet/dry mechanism screen with unequal exposure.
16. `spreader_material_mapping.py` — maps abstract routing conductance to `k*t/pitch^2`, mass and contact burden.
17. `virtual_prototype_v01.py` — VP-A/B/C/D computational anchors.
18. `distributed_spreader_1d.py` — direct periodic `k*t` conduction with feed-solved wet width.
19. `heat_spreader_2d.py` — anisotropic 2-D lateral heat-routing screen.
20. `spreader_topology_2d.py` — equal-material explicit trace/topology screen and corrected orientation result.
21. `heat_network_topology_2d.py` — four wet-island routing motifs and directed/mesh blends.
22. `heat_network_apparel_robustness.py` — stretch, wet-field relocation and spatial-contact sensitivity.
23. `heat_network_combined_failure.py` — simultaneous stretch/contact/fracture screen.
24. `compression_contact_air_access.py` — contact improvement vs vapor-path collapse and regime transition.

### Spatial load / apparel architecture

25. `spatial_pressure_layout.py` — synthetic backpack/strap/seat pressure maps and equal-area evaporator placement.
26. `protected_air_channel_tradeoff.py` — relocation vs mechanically protected vapor path under load.
27. `load_schedule_policy.py` — quasisteady fixed vs ideal state-adaptive wet-layout policy.
28. `protected_support_skeleton.py` — protected-gap air access vs load-bearing support-area penalty.

### Liquid transport / nonvolatile solute

29. `water_salt_1d.py` — earlier normalized water/nonvolatile-salt balance screen.
30. `capillary_liquid_network.py` — ideal cylindrical capillary pressure/flow burden and local-routing screen.
31. `capillary_architecture_tradeoff.py` — analytic optimum radius and centralized-vs-distributed architecture comparison.
32. `capillary_practical_constraints.py` — radius caps, two-scale micro-wick/trunk split and blockage redundancy.
33. `salt_leakage_budget.py` — corrected bulk nonvolatile-salt concentration under upstream water-only leakage.

`generate_reference_outputs.py` is a reproducibility generator rather than a physical model.

## Current integrated architecture

The working virtual architecture is:

> directional skin-side liquid collection -> distributed short capillary routes -> low-pressure or mechanically protected wet terminals -> continuously ambient-connected microtexture/open valleys -> short high-`k/rho` heat routes with limited cross-link redundancy -> dry-side shielding where hot ambient sensible pickup is harmful.

The current project does **not** treat one garment-scale central wick, one long wet chimney, one global heat sink or geometric surface area alone as the preferred architecture.

## High-value conclusions currently retained

- Added geometric evaporator area can be lost to one shared humid boundary layer.
- Covered passive wet corridors can remain near saturation despite nonzero buoyant flow.
- Sensible heat transfer and vapor transfer must be tracked separately.
- Positive evaporation is not equivalent to positive body-side heat removal.
- Feed limitation changes the optimum; evaporation capacity above available water is not achievable fixed-feed performance.
- Heat spreading creates system value only when it routes heat between genuinely different local boundary conditions.
- Short routing pitch matters because ideal sheet burden scales approximately with `P^2`.
- Contact resistance can cap useful high-`k` routing.
- Equal-material sparse traces tested so far do not beat the homogenized ideal field; orientation still matters strongly.
- A lightly cross-linked directed heat network is the current combined-failure robustness anchor for the tested failure map.
- Under persistent local load, active evaporation is better placed in nearby low-pressure regions unless a protected vapor path retains near-uncompressed ambient access with little support-area occupation.
- Ideal active switching between load states adds little over the best fixed pressure-aware layout in the current quasisteady schedules.
- Passive liquid transport strongly favors distributed local collection over long upward centralized transport in the ideal capillary screen.
- Micro-wicking and longer-range liquid transport should use different hydraulic scales.
- Salt vapor flux is zero. Small upstream water leakage modestly raises **bulk** concentration; local wall-film crystallization remains a separate unresolved mechanism.

## Liquid-routing equations

Ideal capillary burden:

\[
\Delta P_f=\frac{8\mu LQ}{\pi r^4N},\qquad
\Delta P_c=\frac{2\gamma\cos\theta}{r},\qquad
\Delta P_h=\rho g\Delta z.
\]

For positive lift, the ideal radius minimizing total capillary cross-sectional area is

\[
r_* = \frac{\gamma\cos\theta}{\rho g\Delta z},
\]

half the largest radius that can statically sustain the same rise.

Bulk nonvolatile-solute leakage balance:

\[
\sigma_{out}=\frac{\sigma_0}{1-f_{leak}},\qquad J_{salt,vapor}=0.
\]

This bulk equation does not prove that small upstream evaporation causes crystallization.

## Reproducibility

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Dedicated workflows currently separate the broad model stack, topology/apparel screens, spatial-pressure screens and liquid-routing screens.

## Interpretation rules

Do not use any one of the following as proof of garment cooling:

- geometric area;
- a single lumped exchange multiplier;
- corridor velocity or Péclet number;
- local `F` alone;
- evaporation mass alone;
- fully-wet capacity above feed;
- a scalar heat-spreader conductance under symmetric boundaries;
- high sheet `k` without route length and contact;
- sparse material coverage without topology;
- synthetic pressure percentages as real garment pressure limits;
- ideal cylindrical-capillary counts as measured textile permeability;
- bulk salt balance as proof of local crystallization.

Integrated interpretation requires signed body heat flow, vapor renewal, absolute vapor conductance, water supply, wet/dry spatial state, ambient sensible pickup, heat-route/contact burden, liquid hydraulic burden, pressure/load maps, added mass/thickness and explicit uncertainty.

## Next model tasks

1. couple heat-route and capillary-route cost to the same pressure-aware terminal geography;
2. add explicit channel collapse/curvature under pressure;
3. resolve protected vapor-gap geometry rather than use an effective air-access floor;
4. add time-varying wet/load maps only if the static robust architecture leaves meaningful performance on the table;
5. complete full virtual-garment mass/thickness budgets and hot/humid maps.

See `docs/current-results.md`, the pressure/liquid design notes under `docs/`, and `AUDIT.md`.
