# Equal-material 2-D heat-spreader topology screen

Status: **SIMULATION / 2-D PERIODIC SCREEN — NO PHYSICAL SPECIMEN**

## Question

The earlier material mapping showed that, **for a fixed topology factor**, reducing conductive coverage does not automatically reduce mass because the required product `t × coverage` stays fixed.

The next question is different:

> If the same amount of high-conductivity material is placed in different 2-D routing topologies, can orientation/topology change the effective routing factor enough to matter?

This screen answers yes under the current periodic wet/dry geometry.

## Equal-material construction

All four cases use exactly 50% high-k material fraction over a 15 mm × 15 mm periodic cell:

1. `uniform_homogenized` — local 50/50 effective sheet;
2. `x_aligned_traces` — high-k traces run along the dominant wet/dry heat-routing direction;
3. `y_aligned_traces` — same material amount placed perpendicular to that direction;
4. `connected_mesh` — orthogonal connected lines with union coverage exactly 50%.

Fractional boundary-cell coverage is integrated analytically so mean high-k material fraction remains exactly 0.5 as grid resolution changes.

The high-k screening property is the same VP-C-like sheet budget used in the preceding virtual work. Background textile conductance remains explicit.

## Governing sheet equation

The local 2-D sheet balance is

\[
\nabla\cdot(K_s(x,y)\nabla T_s)
+U_b(T_{skin}-T_s)
+h_c(T_o-T_s)=0,
\]

where

\[
K_s(x,y)=k(x,y)t(x,y)
\]

has units W/K per metre transverse width in each in-plane direction for the thin-sheet discretization.

Face conductance uses the harmonic mean between neighboring cells. Periodic boundaries are applied in both in-plane directions.

Wet/dry state varies primarily along `x`, so `x` is the principal dry-to-wet heat-routing direction in this test.

## Variables

| symbol | meaning | SI unit | current assumption |
|---|---|---:|---|
| `K_s` | local sheet conductance `k*t` | W/K | scalar cell value |
| `T_s` | spreader temperature | °C | 2-D periodic field |
| `T_o` | outer-layer temperature | °C | local wet/dry field |
| `U_b` | body-to-spreader coupling | W/(m² K) | low-order constant |
| `h_c` | spreader-to-outer contact | W/(m² K) | low-order constant |
| `w(x)` | local wet-area fraction | 1 | continuous boundary-cell weighting |

Dimensional check:

\[
\nabla\cdot(K_s\nabla T)
\sim
\frac{\mathrm{W/K}\;\mathrm{K/m}}{\mathrm m}
=
\mathrm{W/m^2},
\]

matching the body/contact areal heat-flux terms.

## Result

At 35 °C / 50% RH / 100 g/h with equal 50% high-k material fraction, the current 2-D screen gives approximate heat-routing gains over the 0.195 m² structured area:

| topology | approximate gain vs no lateral routing | interpretation |
|---|---:|---|
| x-aligned traces | ~7.2 W | best use of material in the dominant routing direction |
| uniform homogenized | ~6.0 W | isotropic reference |
| connected mesh | ~6.0 W | cross-links consume material but preserve connectivity |
| y-aligned traces | ~2.0 W | most high-k material is poorly oriented for dry-to-wet routing |

All cases use the same total high-k material fraction. Therefore the difference is a topology/orientation effect, not a material-mass difference.

The qualitative ordering is stable across the checked grids:

\[
\text{x-aligned} > \text{uniform} \approx \text{mesh} \gg \text{y-aligned}.
\]

## Refinement of the earlier “coverage does not save mass” result

The earlier relation

\[
g_{sheet}\approx \Gamma\frac{k t c}{P^2}
\]

showed that coverage `c` cancels from mass **when `Gamma` is held fixed**.

This 2-D result identifies the missing qualifier:

> sparse/routed coverage can improve mass efficiency only if its topology/orientation changes the effective routing factor `Gamma` or effective path length.

So both statements can be true:

- simply deleting conductive area and compensating with thickness gives no mass benefit in the fixed-topology model;
- deliberately aligning a sparse network with the dominant heat-flow direction can use the same material more effectively than an isotropically distributed network.

## VP-C consequence

VP-C's lightweight concept is no longer represented only by a homogenized effective thickness. The 2-D screen suggests a plausible route for its lightweight advantage to survive explicit geometry:

- use directional traces that bridge dry/body-coupled regions to wet evaporative regions;
- minimize high-k material placed perpendicular to the dominant thermal gradient unless cross-links are required for robustness;
- treat mesh cross-links as a reliability/manufacturability cost, not automatically useful thermal area.

This is still a virtual-screening result. It does not establish that a real garment has one fixed global heat-flow direction; a garment contains multiple wet islands, seams, curved surfaces and changing sweat patterns.

## Numerical checks

The repository regression requires:

- exact mean high-k material fraction = 0.5 for every topology;
- feed closure near the nominal 100 g/h state;
- local outer-energy residual below numerical tolerance;
- 2-D spreader residual below the screening threshold;
- x-aligned topology outperforming the uniform case at equal material amount;
- y-aligned topology underperforming strongly;
- grid-stable gain for the uniform and x-aligned reference cases.

## Next step

Use this topology solver to build geometry-resolved VP-C variants with:

1. multiple wet islands rather than one stripe;
2. trace redundancy / broken-trace faults;
3. anisotropic trace orientation fields;
4. seam interruptions;
5. contact degradation;
6. curvature / compression;
7. mass-normalized gain and reliability metrics.

The current result should not be extrapolated to “all aligned traces are better.” It establishes only that topology orientation is a first-class design variable under a specified thermal field.
