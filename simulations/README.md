# Simulations

Status: **screening / analytic / virtual-prototype models only**. No physical garment or bench specimen exists.

The current release-candidate stack is frozen at **45 executable models**, plus `generate_reference_outputs.py` as a reproducibility generator. New exploratory models should normally be deferred to a later version unless needed to correct a release-critical contradiction.

## Executable model hierarchy

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
15. `asymmetric_wet_dry_spreader.py` — wet/dry mechanism screen with unequal exposure.
16. `spreader_material_mapping.py` — maps routing conductance to `k*t/pitch^2`, mass and contact burden.
17. `virtual_prototype_v01.py` — VP-A/B/C/D computational anchors.
18. `distributed_spreader_1d.py` — direct periodic `k*t` conduction with feed-solved wet width.
19. `heat_spreader_2d.py` — anisotropic 2-D lateral heat-routing screen.
20. `spreader_topology_2d.py` — equal-material explicit trace/topology screen and corrected orientation result.
21. `heat_network_topology_2d.py` — four wet-island routing motifs and directed/mesh blends.
22. `heat_network_apparel_robustness.py` — stretch, wet-field relocation and spatial-contact sensitivity.
23. `heat_network_combined_failure.py` — simultaneous stretch/contact/fracture screen.
24. `compression_contact_air_access.py` — contact improvement vs vapor-path collapse and regime transition.
25. `integrated_virtual_prototype_vpe.py` — integrated VP-E heat/terminal/liquid-class environmental anchor.
26. `virtual_garment_bom.py` — garment dry/operating mass and thickness budget screen.
27. `vpe_dry_shield_control.py` — independent wet-terminal exposure / dry-side shielding hot-ambient screen.

### Spatial load / terminal / environment architecture

28. `spatial_pressure_layout.py` — synthetic backpack/strap/seat pressure maps and equal-area evaporator placement.
29. `protected_air_channel_tradeoff.py` — relocation vs mechanically protected vapor path under load.
30. `load_schedule_policy.py` — quasisteady fixed vs ideal state-adaptive wet-layout policy.
31. `protected_support_skeleton.py` — protected-gap air access vs load-bearing support-area penalty.
32. `terminal_route_coddesign.py` — pressure avoidance vs liquid/heat nearest-terminal distance Pareto screen.
33. `pressure_weighted_liquid_routes.py` — pressure/collapse-weighted route cost and protected escape trunks.
34. `environment_exposure_control.py` — hot/humid wet-terminal open/shield screen under load.
35. `pressure_liquid_codesign.py` — relative pressure-aware thermal/geometric route co-design proxy.

### Liquid transport / nonvolatile solute / transient water state

36. `water_salt_1d.py` — normalized water/nonvolatile-solute balance screen.
37. `capillary_liquid_network.py` — ideal cylindrical capillary pressure/flow burden and local-routing screen.
38. `capillary_architecture_tradeoff.py` — analytic optimum radius and centralized-vs-distributed comparison.
39. `capillary_practical_constraints.py` — radius caps, two-scale micro-wick/trunk split and blockage redundancy.
40. `capillary_radius_collapse.py` — equivalent hydraulic-radius collapse plus blockage sensitivity.
41. `salt_leakage_budget.py` — corrected bulk nonvolatile-solute concentration under upstream water-only leakage.
42. `branched_liquid_resistor_network.py` — explicit distributed-source branched-flow pressure solve to multiple terminals.
43. `sparse_branched_liquid_network.py` — trunk-pitch / collector-radius / grid-phase robustness screen.
44. `collector_fouling_margin.py` — imposed nonvolatile-residue / hydraulic-radius-loss failure screen; does not predict deposition chemistry or rate.
45. `transient_terminal_buffer.py` — mass-conserving transport/terminal water-buffer and response-time screen.

`generate_reference_outputs.py` is a reproducibility generator rather than a model and is excluded from the count.

## Retained interpretation

The model hierarchy supports the following architecture-level conclusions:

- geometric evaporator area requires ambient-access verification;
- covered passive wet corridors can remain humid/saturated despite nonzero flow;
- sensible and vapor transfer are distinct;
- positive evaporation is not equivalent to positive body-side cooling;
- feed limitation changes the optimum;
- heat routing requires asymmetric local boundary conditions to create integrated value;
- routing pitch/contact burden must accompany any high-`k` claim;
- sparse high-`k` traces do not automatically beat an equal-material homogenized field;
- local load changes terminal placement and can collapse vapor paths;
- short distributed capillary routing is favored over long centralized lift;
- explicit branched-network pressure solves supersede route-distance proxies for hydraulic claims;
- collector radius, trunk pitch, phase/placement, and source localization jointly control sparse-network feasibility;
- salt vapor flux is zero and bulk concentration is distinct from local deposition;
- imposed collector fouling/radius loss is a failure sensitivity, not a measured salt-deposition lifetime;
- transient water storage trades startup/decay response against operating wet mass.

## Reproducibility

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Five dedicated workflows separate the broad stack and domain-specific checks:

- `model-tests`;
- `topology-tests`;
- `pressure-tests`;
- `liquid-tests`;
- `garment-tests`.

The final release candidate should preserve the exact-head reference package produced by `model-tests` as an Actions artifact containing generated data, figures, `metadata.json`, and `sha256.txt`.

## Interpretation rules

Do not use any one of the following as proof of real-garment performance or hydraulic viability:

- geometric area;
- one lumped exchange multiplier;
- corridor velocity or Péclet number;
- evaporation mass alone;
- fully-wet capacity above feed;
- scalar heat-spreader conductance under symmetric boundaries;
- high sheet `k` without route length/contact burden;
- sparse material coverage without topology;
- synthetic pressure/compression percentages as measured garment limits;
- ideal cylindrical-capillary counts as measured textile permeability;
- pressure-weighted shortest-path or `d95*r^-4` cost as a full hydraulic network;
- one favorable trunk-grid phase as a robust sparse-network boundary;
- bulk salt balance as proof of local crystallization;
- imposed fouling thickness as a measured deposition rate or service life;
- transient time constants as measured textile response constants;
- virtual BOM values as measured garment mass.

## Freeze rule

Further simulations are optional future research. The current release candidate should change only for corrections, clarifications, reproducibility fixes, or release metadata. See `../docs/research-freeze.md` and `../AUDIT.md`.
