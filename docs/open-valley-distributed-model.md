# Distributed Open-Valley Vapor Model

Date: 2026-08-20  
Classification: **SIMULATION / SCREENING — NOT PHYSICAL GARMENT DATA**

## Purpose

The earlier open-valley target model defined the local conductance ratio

\[
R=G_a/G_w
\]

and the retained wet-wall vapor driving-force fraction

\[
F=R/(1+R).
\]

That local model did not include axial diffusion, axial flow, or finite segment length. `simulations/open_valley_distributed_1d.py` adds those effects explicitly.

## Governing equation

Define normalized valley vapor loading

\[
\theta(z)=\frac{C(z)-C_\infty}{C_{sat}-C_\infty},
\qquad F(z)=1-\theta(z).
\]

The steady one-dimensional balance is

\[
D_v A\frac{d^2\theta}{dz^2}
-uA\frac{d\theta}{dz}
+G'_w(1-\theta)
-G'_a\theta=0.
\]

Both axial ends are set to ambient vapor loading:

\[
\theta(0)=\theta(L)=0.
\]

### Variable table

| symbol | meaning | SI unit | definition / assumption |
|---|---|---:|---|
| `D_v` | water-vapor diffusivity in air | m²/s | fixed screening value used across repository models |
| `A` | valley cross-sectional area | m² | width × depth |
| `u` | signed axial mean velocity | m/s | prescribed in this vapor-only model |
| `G'_w` | wet-surface vapor conductance per axial length | m²/s | `k_w P_w` |
| `G'_a` | distributed lateral ambient-renewal conductance per axial length | m²/s | `k_a P_a` |
| `R` | lateral-renewal / wet-source conductance ratio | 1 | `G'_a/G'_w` |
| `theta` | normalized local vapor loading | 1 | 0=ambient, 1=saturated-wall vapor density |
| `F` | retained wet-wall vapor driving force | 1 | `1-theta` |
| `L` | axial segment length | m | end-to-end ambient-connected length |

### Unit check

Each term has units of vapor-density rate integrated over cross section:

\[
[D_v A\theta'']=[m^2/s][m^2][1/m^2]=m^2/s,
\]

\[
[uA\theta']=[m/s][m^2][1/m]=m^2/s,
\]

and `G'_w`, `G'_a` also have units `m²/s`.

## Geometry mapping used only for screening

For a rectangular valley with a wet floor and open top:

\[
k_w=Sh\,D_v/D_h,
\qquad k_a=D_v/\delta_{open}.
\]

Therefore `delta_open` is an **effective stagnant lateral exchange thickness**, not a literal opening height. The mapping is intentionally conservative/simple; natural convection, cross-flow, wearer motion, geometry, and turbulence are not predicted by it.

## Main result 1 — the long-valley interior returns to the local analytic balance

For a sufficiently long valley, axial end effects disappear and

\[
F_{interior}\rightarrow\frac{R}{1+R}.
\]

The numerical solver is regression-tested against this limit.

## Main result 2 — centimeter-scale segmentation is too coarse in the screened geometry

Representative geometry: 6 mm wide × 3 mm deep.

For effective lateral exchange distances from 0.25 to 2 mm, the computed exchange length

\[
\ell=\sqrt{\frac{D_v A}{G'_w+G'_a}}
\]

is approximately 0.7–1.1 mm.

Consequently, segments of 20, 50, or 100 mm all develop essentially the same interior vapor loading. End openings matter only within a few exchange lengths.

Selected still-air axial results:

| `delta_open` | `R` | segment | center `F` |
|---:|---:|---:|---:|
| 0.25 mm | 2.12 | 1 mm | 0.935 |
| 0.25 mm | 2.12 | 20 mm | 0.680 |
| 0.50 mm | 1.06 | 1 mm | 0.931 |
| 0.50 mm | 1.06 | 2 mm | 0.797 |
| 0.50 mm | 1.06 | 20 mm | 0.515 |
| 1.00 mm | 0.53 | 1 mm | 0.929 |
| 1.00 mm | 0.53 | 20 mm | 0.347 |

**Correction:** the earlier idea that macro fields could simply be interrupted every 20–50 mm is not supported by this model if lateral exchange remains weak between interruptions.

## Main result 3 — small axial flow does not rescue a long valley interior

For the 6 × 3 × 50 mm, `delta_open=0.5 mm` screen:

- 0 mm/s axial flow: center `F≈0.515`;
- 5 mm/s: center `F≈0.515`;
- 100 mm/s: center `F≈0.515`;
- 500 mm/s: center `F≈0.595`;
- 1000 mm/s: center `F≈0.711`.

Thus the few-mm/s flow scales produced by the passive covered-corridor screen are far too small to keep the middle of a long valley near ambient vapor loading in this model.

This does **not** say walking airflow is useless. It says the architecture should not rely on weak axial chimney flow as a substitute for distributed ambient access.

## Main result 4 — diffusion-only geometry mapping gives a stringent lateral-renewal requirement

For the representative 6 × 3 mm valley:

- center `F>=0.8` in a long valley requires approximately `R>=4`;
- under the diffusion-only mapping this corresponds to effective `delta_open≈0.13 mm`;
- center `F>=0.9` requires approximately `R>=9`, or `delta_open≈0.058 mm`.

These `delta_open` values are **not product dimensions**. They indicate that a thick stagnant layer above the valley is incompatible with high retained vapor driving force when the wet-surface conductance is as large as assumed by the current Sherwood-number screen.

## Design consequence

The current preferred exterior is further narrowed to:

1. wet microstructure for area;
2. a top and/or sides that remain continuously exposed to ambient air;
3. frequent cross-openings rather than a long roofed duct;
4. shallow open valleys or discontinuous islands that minimize a stagnant external humidity layer;
5. optional motion/wind assistance as a secondary benefit, not a required passive mechanism.

A centimeter-scale decorative groove that is open only at its ends is no longer treated as sufficient air-renewal architecture.

## Physical falsification

E3c should compare:

- covered/end-renewed channel;
- continuously laterally open valley;
- very short 1–3 mm interrupted wet segments where manufacturable;
- discontinuous wet islands with ambient-connected gaps.

Measure local `F` from T/RH rather than inferring success from geometric opening alone.

## Uncertainty / limitations

Major model-form uncertainties:

- `Sh=7.54` is a screening transfer coefficient, not a measured open-valley value;
- `delta_open` is an effective exchange distance, not direct geometry;
- thermal coupling and sensible heat transfer are omitted here;
- natural convection and transverse cross-flow are represented only through the unknown/effective lateral renewal conductance;
- the 1-D model cannot resolve 2-D/3-D plume structure above a real textile.

The model is therefore best used to identify **necessary air-access behavior and falsifiable measurements**, not final garment dimensions.
