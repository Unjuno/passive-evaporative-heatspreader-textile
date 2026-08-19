# Passive Evaporative Heat-Spreader Textile

Open research on a passive personal-cooling garment combining directional liquid transport, capillary delivery, routed heat spreading, and exterior evaporation.

> **Current state: virtual/computational prototype only. No physical garment or bench specimen currently exists, and no physical performance claim is made.**

## Primary architecture

The current fanless hypothesis is:

1. directional sweat transport away from skin;
2. capillary delivery to selected wet exterior fields;
3. low-profile micro-rib / 3D-knit / short-fin evaporative texture;
4. continuously ambient-connected open valleys, gaps or islands rather than long covered wet ducts;
5. short-range in-plane heat routing between thermally different dry/wet regions;
6. explicit wet/dry thermal contact;
7. dry-side shielding / selective exposure where hot ambient sensible heat would otherwise be harmful.

The objective is **body-coupled useful evaporation**, not maximum geometric surface area or evaporation mass alone.

## Current numerical conclusions

- Dense ribs can share one humid boundary layer; geometric area is not useful area without ambient access.
- Long covered wet passive corridors can remain nearly saturated despite nonzero natural flow, and flow can reverse.
- Sensible heat transfer and water-vapor transfer are treated separately.
- Positive evaporation can coexist with negative body-side heat flow in hot ambient conditions.
- Water supply can become limiting; a computational sub-grid wet fraction `beta` is solved explicitly in the feed-limited screen.
- The same evaporated water mass can draw materially different fractions of latent heat from the body versus warm ambient air.
- A heat spreader produces little area-integrated benefit under deliberately symmetric wet/dry boundary conditions; its system value appears when it connects genuinely different local wetting/exposure/shielding conditions.
- Infinite heat-spreader conductivity is not the target; current asymmetric screens show diminishing returns in the few-hundred-W/(m² K) effective `g_mix` range.

## Exterior vapor-renewal metrics

Local renewal quality:

\[
R=G_a/G_w,
\qquad
F=\frac{R}{1+R}.
\]

`F=0.8` requires `R=4`; `F=0.9` requires `R=9`.

But `F` is not absolute capacity. The local series conductance is

\[
k_{eff}=\frac{k_wk_a}{k_w+k_a}=k_wF.
\]

Every virtual design therefore tracks both renewal quality and absolute transfer.

## Hot/humid sign boundary

For the repository's same-path heat/vapor baseline, zero body-side heat flow satisfies

\[
\frac{k_{air}}{D_v}(T_\infty-T_{skin})
=
L_v\left[\rho_{v,sat}(T_{skin})-\phi_\infty\rho_{v,sat}(T_\infty)\right].
\]

At a 34 °C artificial-skin setpoint, representative low-order boundaries are approximately:

- 45.25 °C at 50% RH;
- 39.73 °C at 70% RH;
- 37.57 °C at 80% RH;
- 36.59 °C at 85% RH;
- 35.68 °C at 90% RH.

This is a **model sign boundary**, not a human-safety, medical, or measured garment threshold.

## Heat-spreader material mapping

The asymmetric wet/dry mechanism model uses an effective lateral conductance `g_mix`. A first-order periodic-stripe mapping is now explicit:

\[
g_{sheet}\approx\Gamma\frac{k_{\parallel}tc}{P^2},
\qquad \Gamma=4.
\]

This is a topology screen, not a validated textile correlation. Its main implication is the quadratic routing-distance penalty: required `k*t` grows as `P²`.

Thermal contacts are included with

\[
\frac{1}{g_{eff}}=\frac{1}{g_{sheet}}+\frac{2}{h_c}.
\]

For the representative 100 g/h asymmetric mechanism target (`g_mix≈330 W/(m² K)` for ~90% of high-mixing gain):

- abstract `k=100 W/(m K)`, `rho=1600 kg/m³`: about 83 µm / 40 g over 0.30 m² at 10 mm routing pitch, versus about 330 µm / 159 g at 20 mm;
- even an ideal sheet would require each-side contact conductance above roughly 660 W/(m² K) in the lumped contact screen.

These are computational design burdens, not measured material values.

## Virtual prototypes v0.1

Four explicit computational anchors are committed:

| prototype | key design | mass over 0.30 m² | nominal `g_eff` | spreader-only mechanism gain at 100 g/h |
|---|---|---:|---:|---:|
| VP-A | 10 mm, `k=100`, 100 µm | ~48 g | ~286 W/(m² K) | ~5.3 W |
| VP-B | 20 mm, same class, 200 µm | ~96 g | ~167 W/(m² K) | ~4.9 W |
| VP-C | 15 mm, 50% routed, higher `k/rho` class | ~27 g | ~197 W/(m² K) | ~5.0 W |
| VP-D | VP-A path + stronger dry-side shielding | ~48 g | ~286 W/(m² K) | ~6.1 W |

The gains above are **only the modeled heat-spreader mechanism increment relative to the same local wet/dry case with `g_mix=0`**. They are not total garment-vs-control cooling predictions.

A deterministic topology/contact sensitivity screen at 100 g/h gives approximate gain ranges:

- VP-A: 4.4–5.4 W;
- VP-B: 3.9–5.0 W;
- VP-C: 4.1–5.2 W;
- VP-D: 5.1–6.2 W.

These are model-form sensitivity ranges, not probabilities.

Current anchors:

- **performance:** VP-D;
- **lightweight:** VP-C;
- **short-pitch baseline:** VP-A;
- **routing-distance/manufacturability comparison:** VP-B.

## Repository map

### Main technical record

- `docs/technical-disclosure.md` — integrated disclosure
- `docs/architecture.md` — functional architecture
- `docs/embodiment-matrix.md` — implementation combinations
- `docs/design-history.md` — retained/deprecated branches
- `docs/current-results.md` — current numerical conclusions and corrections
- `docs/spreader-material-mapping.md` — `g_mix` to material/pitch/mass/contact mapping
- `docs/virtual-prototypes-v0.1.md` — VP-A through VP-D specifications
- `docs/roadmap.md` — virtual-prototype-first roadmap
- `docs/prior-art.md` / `docs/patent-notes.md` — adjacent work / working patent notes
- `AUDIT.md` — current repository audit

### Future physical-validation specifications

No specimen currently exists. These are future protocols only:

- `experiments/e3b_hierarchical_air_renewal.md`
- `experiments/e3c_open_vs_covered_corridors.md`
- `experiments/e4a_feed_limit_transition.md`
- `experiments/e4_e6_environment_boundary.md`

### Executable stack

The branch currently contains **19** executable screening/sensitivity/audit/virtual-prototype modules, including:

```text
simulations/passive_rib_screen.py
simulations/split_heat_mass_screen.py
simulations/rib_diffusion_screen.py
simulations/self_consistent_corridor_1d.py
simulations/open_valley_distributed_1d.py
simulations/open_valley_thermal_1d.py
simulations/open_valley_feed_limited.py
simulations/wet_dry_two_node.py
simulations/asymmetric_wet_dry_spreader.py
simulations/spreader_material_mapping.py
simulations/virtual_prototype_v01.py
simulations/open_valley_heat_mass_coupling_audit.py
simulations/passive_environment_boundary.py
simulations/heat_spreader_2d.py
simulations/water_salt_1d.py
```

See `simulations/README.md` for the full indexed list.

## Reproducibility

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python simulations/asymmetric_wet_dry_spreader.py
python simulations/spreader_material_mapping.py
python simulations/virtual_prototype_v01.py
python simulations/generate_reference_outputs.py --output-root generated-reference
```

Generated reference artifacts carry classification, git-commit metadata and SHA-256 hashes. GitHub Actions exercises the model/test/generator stack.

## Current next model task

Replace the single two-node `g_mix` abstraction with a distributed 1-D/2-D wet/dry heat-routing field using direct:

- `k_parallel` / anisotropy;
- thickness;
- patch/routing pitch;
- wet/dry thermal contacts;
- dry-side shielding;
- distributed body coupling;
- distributed evaporative sink strength.

VP-A through VP-D will remain regression anchors for that transition.

## Physical clarification: sweat salts

At garment temperatures, sweat salts are nonvolatile in these models. Water evaporates; dissolved salts remain in liquid/solid phases. Salt vapor flux is zero.

## Prior-art position

Many individual building blocks are already known. This repository does not treat directional sweat transport, evaporative textiles, conductive cooling textiles, external ribs/walls, spacer knits, fan garments or sorbent garments individually as unique. The technical record focuses on integrated routing, ambient-access topology, hot-ambient protection, explicit supply state, apparel integration, and reproducible falsifiable modeling.

## License

Apache License 2.0. See `LICENSE`.

## Citation / release state

See `CITATION.cff`. Stable v1.0 has not yet been frozen or persistently archived with a DOI.
