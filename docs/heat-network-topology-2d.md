# Equal-Material Heat-Network Topology Screen

Status: **SIMULATION / DESIGN SCREEN ONLY — NO PHYSICAL SPECIMEN**  
Date: 2026-08-20

## Objective

Test whether the same amount of high-conductivity material performs differently when arranged as a garment-scale heat-routing network rather than as a uniform sheet.

The nominal screen uses:

- 60 mm periodic design tile;
- four wet evaporator islands occupying about 23% of tile area;
- 35% high-conductivity material fraction for every binary network topology;
- high-k sheet conductance input `k*t = 300 W/(m K) * 100 um`;
- background textile sheet conductance input `0.2 W/(m K) * 500 um`;
- artificial-skin temperature 34 C;
- ambient 35 C / 50% RH;
- wet-region vapor/sensible transfer coefficients inherited from the existing open-valley bridge model;
- structured-area reporting scale 0.195 m2.

These are explicit screening inputs, not measured commercial-material properties or garment performance.

## Topologies

The model compares:

1. parallel directed routes;
2. herringbone;
3. radial spokes;
4. leaf/venation routing;
5. redundant mesh;
6. directed/mesh blends.

The binary network masks are thresholded so the initial high-k cell count is equal.

## Nominal equal-material result

At 42 x 42 cells, converged to approximately `1e-6 C` iteration change:

| topology | nominal heat-routing gain over background |
|---|---:|
| parallel routes | ~5.63 W |
| herringbone | ~4.66 W |
| radial spokes | ~3.31 W |
| leaf/venation | ~5.17 W |
| redundant mesh | ~5.35 W |

The homogenized 35% high-k reference is higher (~10.1 W) and remains an idealized distributed-conductivity reference rather than a trace-manufacturing claim.

**Interpretation:** equal material mass is not equal thermal usefulness. Placement relative to the dry-to-wet routing field matters.

## Directed/mesh Pareto sweep

Define `lambda` as the mesh weight in a score-field blend:

- `lambda=0`: directed routes;
- `lambda=1`: redundant mesh.

At equal 35% material fraction:

| mesh weight | nominal gain | worst gain after 5% deterministic random conductor dropout |
|---:|---:|---:|
| 0.000 | ~5.63 W | ~5.39 W |
| 0.125 | ~5.86 W | ~5.34 W |
| 0.375 | ~5.93 W | ~5.24 W |
| 1.000 | ~5.35 W | ~4.55 W |

The nominal optimum in this discrete sweep is near `lambda=0.375`, while the best retained gain under the current distributed-dropout test is the pure directed case. Therefore no single scalar optimum is asserted.

## Damage-mode correction

Two different failure modes behave differently and must not be conflated.

### Localized 5% tear

Exactly 5% of the high-k cells are removed nearest each of nine possible tear centers. Worst-case retained nominal gain:

| topology | worst retained gain |
|---|---:|
| blend `lambda=0.125` | ~94% |
| directed routes | ~93% |
| leaf/venation | ~92% |
| herringbone | ~92% |
| radial spokes | ~87% |
| redundant mesh | ~85% |

In this particular grid, the `lambda=0.125` blend is the strongest localized-damage compromise.

### Distributed 5% dropout

Randomly distributed micro-loss removes the same total conductor amount but creates many small discontinuities. Thin mesh lines are more sensitive to this damage mode in the current binary model.

**Correction:** `mesh = robust` is not a general rule. Robustness depends on whether the failure is localized tearing, distributed microcracking, contact loss, or complete branch severance.

## Wet-pattern robustness

The same fixed networks were tested against five wet distributions:

- four islands;
- top pair;
- diagonal pair;
- one center island;
- shifted four islands.

Mean/minimum heat-routing gains over the five patterns:

| topology | mean gain | minimum gain |
|---|---:|---:|
| blend `lambda=0.375` | ~5.12 W | ~3.75 W |
| mesh | ~4.78 W | ~3.73 W |
| directed | ~4.73 W | ~3.82 W |
| blend `lambda=0.125` | ~4.85 W | ~3.49 W |
| leaf | ~4.47 W | ~3.50 W |

The `lambda=0.375` blend performs best on the current mean-minus-standard-deviation robustness score. A single center wet island favors the leaf network instead.

## Current design conclusion

The current exterior/heat-routing hypothesis should not specify one decorative network as universally optimal.

Instead, the disclosed design family should include:

- strongly directed routes when evaporator locations are stable;
- light cross-link redundancy for expected localized damage;
- denser redundant connectivity when wet-zone location is expected to move;
- leaf/branch routing for centrally concentrated or strongly migrating wet zones;
- explicit orientation of major heat paths toward expected evaporator fields.

A practical textile design can express these networks as stripes, ribs, seams, printed conductive paths, woven/knitted high-k yarn groups, leaf-like graphics, or hidden internal routing while keeping the external visual language conventional.

## H / T / D / C / U

**H**: At fixed high-k material fraction, topology and orientation materially change heat routed from dry regions to wet evaporator regions, and moderate directed/mesh blending can improve the nominal/robustness tradeoff.

**T**: Equal-material 2-D finite-volume/finite-difference screen, fixed wet field plus alternate wet-pattern and damage screens.

**D**: Hypothesis supported numerically if equal-material patterns produce materially different body-side heat flow and ranking changes under controlled damage/wet-pattern perturbations.

**C**: The network can be over-fit to the chosen wet field; binary conductor breaks exaggerate some microcrack failure modes; periodic boundaries and low-order external transfer remain idealizations.

**U**: Major uncertainties are contact conductance, actual trace/yarn anisotropy, deformation, crack morphology, local wetting, curvature, external flow and the effective high-k/background sheet conductances.

## Next numerical work

1. optimize branch width and redundancy with mass held fixed;
2. include stretch/serpentine penalties directly in the 2-D network;
3. introduce spatial contact-resistance loss separately from conductor fracture;
4. test moving wet fields rather than only static snapshots;
5. couple this network layer to the open-valley exterior geometry rather than using the current transfer bridge.
