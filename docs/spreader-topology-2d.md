# Equal-material 2-D heat-spreader topology screen

Status: **SIMULATION / 2-D PERIODIC SCREEN — NO PHYSICAL SPECIMEN**

## Question

The earlier material mapping showed that, **for a fixed topology factor**, reducing conductive coverage does not automatically reduce mass because the required product `t × coverage` stays fixed.

The next question is different:

> If the same amount of high-conductivity material is placed in different 2-D routing topologies, does orientation/topology materially change useful heat routing?

The current screen answers **yes**, but it does **not** show that sparse aligned traces outperform an ideal homogenized field.

## Equal-material construction

All four cases use exactly 50% high-k material fraction over a 15 mm × 15 mm periodic cell:

1. `uniform_homogenized` — local 50/50 effective sheet;
2. `x_aligned_traces` — high-k traces run along the dominant wet/dry heat-routing direction;
3. `y_aligned_traces` — same material amount placed perpendicular to that direction;
4. `connected_mesh` — orthogonal connected lines with union coverage exactly 50%.

Fractional boundary-cell coverage is integrated analytically so mean high-k material fraction remains exactly 0.5 as grid resolution changes.

## Governing sheet equation

\[
\nabla\cdot(K_s(x,y)\nabla T_s)
+U_b(T_{skin}-T_s)
+h_c(T_o-T_s)=0,
\]

where

\[
K_s(x,y)=k(x,y)t(x,y).
\]

Dimensional check:

\[
\nabla\cdot(K_s\nabla T)
\sim
\frac{\mathrm{W/K}\;\mathrm{K/m}}{\mathrm m}
=
\mathrm{W/m^2},
\]

matching the body/contact areal heat-flux terms.

## Corrected result

At 35 °C / 50% RH / 100 g/h with equal 50% high-k material fraction, the reproducible 30-cell reference gives approximately:

| topology | gain vs no lateral routing |
|---|---:|
| uniform homogenized | ~5.31 W |
| connected mesh | ~4.76 W |
| x-aligned traces | ~4.71 W |
| y-aligned traces | ~1.82 W |

The qualitative ordering over the checked grids is therefore:

\[
\text{uniform homogenized}
>
\text{x-aligned / mesh}
\gg
\text{y-aligned}.
\]

The exact order between x-aligned and mesh is grid/topology-detail sensitive; the robust conclusion is that transverse routing is strongly worse, while the ideal homogenized conductivity field remains the upper/reference case in this model.

## Correction of an earlier interpretation

An earlier draft incorrectly stated that the x-aligned trace case beat the uniform homogenized reference. The regression test encoded that incorrect assumption and failed when rerun in CI.

That statement is withdrawn.

The supported conclusion is narrower:

> Orientation and topology matter strongly at equal material amount, but the explicit sparse traces tested so far do not beat the ideal homogenized 50% field.

This is physically plausible: a homogenized field distributes conductivity everywhere, whereas binary traces incur path gaps, local bottlenecks and contact with low-conductivity background regions.

## Refinement of the coverage/mass result

The relation

\[
g_{sheet}\approx \Gamma\frac{k t c}{P^2}
\]

still shows that coverage `c` cancels from mass **when `Gamma` is fixed**.

The 2-D result adds two constraints:

1. topology/orientation can substantially reduce or preserve routing effectiveness relative to a homogenized field;
2. a sparse network only creates a real mass advantage if it changes effective path length, permits a better material class, removes truly inactive area, or provides another non-linear benefit.

Therefore the project no longer uses "aligned sparse traces can beat uniform material at the same mass" as a design conclusion.

## VP-C consequence

VP-C remains a lightweight challenge case, not a validated sparse-network advantage.

Its explicit geometry must demonstrate that:

- useful dry-to-wet paths remain short;
- conductor bottlenecks do not dominate;
- contact resistance stays acceptable;
- any material removed from the homogenized field is genuinely thermally inactive or compensated by better `k/rho`, path length, topology, or integration.

The newer multi-island network model in `heat_network_topology_2d.py` is the next step because real garments have multiple moving wet zones rather than one fixed stripe.

## Numerical checks

The repository regression now requires:

- exact mean high-k material fraction = 0.5 for every topology;
- feed closure near the nominal 100 g/h state;
- local outer-energy residual below numerical tolerance;
- 2-D spreader residual below the screening threshold;
- the homogenized reference to remain above the tested discrete aligned trace at the current reference state;
- aligned and mesh topologies to outperform transverse routing materially;
- grid-stable gain for uniform and aligned reference cases.

## Next step

The project now tests:

1. multiple wet islands;
2. directed/mesh blends;
3. localized tears versus distributed micro-dropout;
4. wet-zone relocation;
5. contact degradation;
6. stretch/serpentine deformation;
7. curvature/compression;
8. mass-normalized gain and reliability metrics.

The key current statement is simply that **topology is a first-class design variable, while the homogenized field remains the ideal reference to beat or approximate**.
