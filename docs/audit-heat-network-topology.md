# Heat-Network Topology Audit Addendum

Date: 2026-08-20  
Status: **SIMULATION / VIRTUAL DESIGN ONLY — NO PHYSICAL SPECIMEN**

## Audit scope

This addendum closes part of the earlier P1 item:

> move from periodic 1-D heat routing toward geometry-resolved 2-D traces, wet islands, damage and changing wet fields.

It does **not** close the larger external-flow/contact/curvature problem.

## What is now resolved numerically

- explicit 2-D binary high-k networks at equal initial material fraction;
- four-island nominal evaporator field;
- parallel, herringbone, radial, leaf/venation, mesh and directed/mesh blends;
- equal-material nominal comparison;
- convergence audit to about `1e-6 C` iteration change for the 42 x 42 reference screen;
- localized conductor loss at equal removed material amount;
- deterministic distributed dropout at equal removed material amount;
- alternate static wet patterns to test topology over-fitting.

## Main corrections

### 1. Sparse routing is useful only through topology

The earlier mass identity remains valid when topology/path factor is held fixed. The new result shows that spatial placement changes the effective path factor: equal conductor quantity can produce materially different body-side heat flow.

### 2. A mesh is not automatically the most damage-tolerant pattern

Damage morphology matters.

- A connected mesh tolerates some single branch cuts well.
- Distributed micro-dropout can damage many thin links simultaneously.
- Thick directed routes can retain more gain under the current dispersed-dropout model.
- A small amount of cross-link redundancy can improve localized-tear robustness without giving up all directed-routing benefit.

Therefore robustness must always state the damage model.

### 3. The best network depends on wet-field mobility

For a fixed four-island field, a lightly cross-linked directed network is strong. When wet islands move or disappear, a more redundant blend/mesh becomes comparatively stronger. A central single wet island favors leaf/branch routing in the current screen.

No one decorative network is accepted as universally optimal.

## Reference findings

At equal ~35% binary high-k material and the fixed four-island field:

| topology | nominal gain over background |
|---|---:|
| parallel routes | ~5.63 W |
| herringbone | ~4.66 W |
| radial spokes | ~3.31 W |
| leaf/venation | ~5.17 W |
| redundant mesh | ~5.35 W |

Directed/mesh score blending gave:

- `lambda=0.125`: nominal ~5.86 W;
- `lambda=0.375`: nominal ~5.93 W;
- full mesh: nominal ~5.35 W.

Under localized removal of exactly 5% of conductor cells, the current worst-case retained gain for `lambda=0.125` is ~94% across nine tear centers.

Across five alternate wet distributions, `lambda=0.375` gives the highest current mean-minus-standard-deviation score; the result is not universal and is explicitly tied to the tested patterns.

## P1 status update

### Now PASS/SCREEN

- geometry-resolved 2-D conductor placement;
- equal-material topology comparison;
- wet-island field support;
- first localized/distributed damage screens;
- first wet-field relocation screen.

### Still OPEN

- explicit contact maps rather than uniform `h_contact`;
- stretch/serpentine deformation applied to the network geometry;
- curvature/compression;
- time-dependent moving wet fields;
- coupled liquid routing and thermal network co-design;
- geometry-resolved external natural convection/cross-flow;
- 3-D textile thickness/topology;
- full garment mass/manufacturing constraints.

## Audit rule added

Any future topology result must state:

1. initial conductor material fraction;
2. wet-field geometry;
3. damage morphology and removed conductor fraction, if damaged;
4. whether a topology is optimized for nominal gain, worst-case gain, average wet-field robustness or another objective;
5. whether a result uses homogenized material or explicit traces.

This prevents nominal performance, redundancy and material efficiency from being collapsed into one unsupported ranking.
