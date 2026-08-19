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
- Water supply can become limiting; a computational sub-grid wet fraction is solved explicitly in the feed-limited screen.
- The same evaporated water mass can draw materially different fractions of latent heat from the body versus warm ambient air.
- A heat spreader produces little area-integrated benefit under deliberately symmetric wet/dry boundary conditions; system value appears when it connects genuinely different local wetting/exposure/shielding conditions.
- Infinite heat-spreader conductivity is not the target; current asymmetric screens show finite diminishing returns.

## Exterior vapor-renewal metrics

\[
R=G_a/G_w,
\qquad
F=\frac{R}{1+R},
\qquad
k_{eff}=\frac{k_wk_a}{k_w+k_a}=k_wF.
\]

`F=0.8` requires `R=4`; `F=0.9` requires `R=9`. But `F` is not absolute transfer capacity; `k_eff`, evaporation mass and signed body heat flow are tracked separately.

## Hot/humid sign boundary

For the repository's same-path heat/vapor baseline, zero body-side heat flow satisfies

\[
\frac{k_{air}}{D_v}(T_\infty-T_{skin})
=
L_v\left[\rho_{v,sat}(T_{skin})-\phi_\infty\rho_{v,sat}(T_\infty)\right].
\]

At a 34 °C artificial-skin setpoint, representative low-order boundaries are approximately 45.25 °C at 50% RH, 39.73 °C at 70%, 37.57 °C at 80%, 36.59 °C at 85%, and 35.68 °C at 90%.

This is a **model sign boundary**, not a human-safety, medical, or measured garment threshold.

## Heat-spreader material mapping

The first periodic-stripe mapping is

\[
g_{sheet}\approx\Gamma\frac{k_{\parallel}tc}{P^2},
\qquad \Gamma=4,
\]

with contact burden

\[
\frac{1}{g_{eff}}=\frac{1}{g_{sheet}}+\frac{2}{h_c}.
\]

This is a topology screen, not a validated textile correlation. Its key implication is the quadratic routing-distance penalty: required `k*t` grows as `P²`.

For a representative 100 g/h asymmetric mechanism target (`g_mix≈330 W/(m² K)` for ~90% of high-mixing gain):

- abstract `k=100 W/(m K)`, `rho=1600 kg/m³`: ~83 µm / 40 g over 0.30 m² at 10 mm routing pitch, versus ~330 µm / 159 g at 20 mm;
- even an ideal sheet would require each-side contact conductance above ~660 W/(m² K) in the lumped contact screen.

These are computational burdens, not measured material values.

## Virtual prototypes v0.1

Four explicit scalar-anchor cases are committed:

| prototype | key design | mass over 0.30 m² | nominal `g_eff` | scalar spreader-only mechanism gain at 100 g/h |
|---|---|---:|---:|---:|
| VP-A | 10 mm, `k=100`, 100 µm | ~48 g | ~286 W/(m² K) | ~5.3 W |
| VP-B | 20 mm, same class, 200 µm | ~96 g | ~167 | ~4.9 W |
| VP-C | 15 mm, 50% routed, higher `k/rho` class | ~27 g | ~197 | ~5.0 W |
| VP-D | VP-A path + stronger dry-side shielding | ~48 g | ~286 | ~6.1 W |

The gains are **only heat-spreader mechanism increments relative to the same local wet/dry model with no lateral routing**. They are not total garment-vs-control cooling predictions.

Current anchors: VP-D performance, VP-C lightweight, VP-A short-pitch baseline, VP-B routing-distance/manufacturability comparison.

## Direct-material distributed bridge

`simulations/distributed_spreader_1d.py` removes the scalar `g_mix` coupling and solves a periodic sheet directly:

\[
\frac{d}{dx}\left(k_{\parallel}t\frac{dT_s}{dx}\right)
+U_b(T_{skin}-T_s)+h_c(T_o-T_s)=0.
\]

The outer layer exchanges sensible heat with ambient air and latent heat over a continuously solved wet stripe. Wet width is adjusted to match imposed feed when capacity permits.

At 100 g/h, equal-feed no-lateral baseline comparison gives:

| prototype | wet fraction | distributed spreader-only gain over 0.195 m² |
|---|---:|---:|
| VP-A | ~0.444 | ~5.48 W |
| VP-B | ~0.448 | ~5.32 W |
| VP-C | ~0.451 | ~5.30 W |
| VP-D | ~0.447 | ~6.29 W |

Numerical checks show feed closure better than ~0.001 g/h, outer energy residual numerically near zero, spreader-equation residual ~0.004 W/m² or lower, and small 32→96-node grid sensitivity.

The direct-material gains remain within roughly 0.8 W of the scalar-anchor gains. This is model-hierarchy continuity, **not independent validation**, because the models share exterior/body assumptions.

VP-C's sparse 50% coverage is still homogenized as effective `k*t`; actual traces are not yet resolved.

## Repository map

### Technical record

- `docs/technical-disclosure.md` — integrated disclosure
- `docs/architecture.md` — functional architecture
- `docs/embodiment-matrix.md` — implementation combinations
- `docs/current-results.md` — current numerical conclusions
- `docs/spreader-material-mapping.md` — material/pitch/mass/contact mapping
- `docs/virtual-prototypes-v0.1.md` — VP-A through VP-D
- `docs/distributed-spreader-1d.md` — direct-material 1-D bridge model
- `docs/roadmap.md` — virtual-prototype-first roadmap
- `docs/prior-art.md` / `docs/patent-notes.md` — adjacent work / working patent notes
- `AUDIT.md` — repository audit

### Future physical-validation specifications

No specimen currently exists. Experiment files are future protocols only.

### Executable stack

The branch currently contains **20 executable screening/sensitivity/audit/virtual-prototype modules**. See `simulations/README.md` for the complete indexed list.

## Reproducibility

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python simulations/asymmetric_wet_dry_spreader.py
python simulations/spreader_material_mapping.py
python simulations/virtual_prototype_v01.py
python simulations/distributed_spreader_1d.py
python simulations/generate_reference_outputs.py --output-root generated-reference
```

Generated reference artifacts carry classification, git-commit metadata and SHA-256 hashes. GitHub Actions exercises the model/test/generator stack.

## Next model task

Move from periodic 1-D to a **2-D geometry-resolved virtual spreader** containing:

- anisotropic `k_x/k_y`;
- explicit routed traces / sparse coverage;
- spatially varying thermal contact;
- wet islands and dry shielding maps;
- garment curvature / compression sensitivity.

VP-A through VP-D remain regression anchors.

## Physical clarification: sweat salts

At garment temperatures, sweat salts are nonvolatile in these models. Water evaporates; dissolved salts remain in liquid/solid phases. Salt vapor flux is zero.

## Prior-art position

Many individual building blocks are already known. This repository focuses on the integrated routing, ambient-access topology, explicit supply state, hot-ambient protection, material/contact burdens, apparel integration and reproducible falsifiable modeling rather than claiming known components individually.

## License

Apache License 2.0. See `LICENSE`.

## Citation / release state

See `CITATION.cff`. Stable v1.0 has not yet been frozen or persistently archived with a DOI.
