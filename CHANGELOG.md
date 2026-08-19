# Changelog

All notable research-record changes are documented here.

## Unreleased

### Added

- integrated README, citation metadata, architecture, embodiment matrix, design history, roadmap, current-results record, prior-art notes, and repository audit;
- nonlinear passive heat/mass model with explicit multi-equilibrium reporting;
- split sensible/vapor transfer model (`M_h`, `M_m`) and deterministic sensitivity grid;
- periodic 2-D E3 rib vapor-diffusion model and grid-convergence checks;
- thermo-solutal corridor buoyancy and self-consistent covered/end-renewed corridor models;
- local open-valley `R/F` target plus distributed lateral-renewal vapor model;
- coupled open-valley thermal/vapor/wet-wall model;
- explicit feed-limited partial-wetness model and latent heat-source partition;
- symmetric wet/dry two-temperature screen;
- asymmetric wet/dry heat-spreader mechanism screen;
- bounded least-squares + continuation solver for dense asymmetric `g_mix` sweeps;
- Lewis-number / Chilton–Colburn-style heat/mass coupling audit;
- analytic hot/humid environmental body-heat-flow sign boundary;
- low-order heat-spreader material mapping `g_sheet ~ Gamma*k*t*c/P^2`;
- spreader mass/thickness/bending-strain and `k/rho` figure-of-merit screening;
- two-contact thermal-resistance audit `1/g_eff = 1/g_sheet + 2/h_contact`;
- explicit virtual prototypes v0.1: VP-A short-pitch, VP-B 20 mm comparison, VP-C lightweight/high-`k/rho`, VP-D shielded short-pitch;
- deterministic topology/contact robustness screen for VP-A through VP-D;
- **distributed direct-material 1-D spreader model** replacing scalar `g_mix` with periodic `k*t` conduction, local contact, dry shielding, wet evaporation and feed-solved continuous wet width;
- grid/feed/energy-residual regressions for the distributed spreader bridge;
- anisotropic 2-D heat spreading and normalized nonvolatile water/salt models;
- future E3b/E3c/E4a/E4/E6 validation protocols and measurement/uncertainty templates;
- regression tests and GitHub Actions CI;
- reproducible CSV/PNG/metadata/SHA-256 reference package including material/contact, virtual-prototype and distributed-spreader outputs.

### Corrected

- project status explicitly states **virtual/computational prototype only; no physical specimen exists**;
- salt is nonvolatile under garment operating conditions; water evaporates, salt does not;
- nonlinear equilibrium branch selection is explicit rather than silently selecting one root;
- historical single-value `M` thresholds are not treated as validated design criteria;
- vapor-transfer enhancement is not automatically copied into sensible heat transfer;
- geometric exterior area is not treated as accessible evaporative area;
- vertical wet corridors are not assumed to produce useful upward chimney flow;
- nonzero corridor velocity / Péclet number is not proof of vapor renewal;
- 20–50 mm segmentation is not assumed sufficient when lateral renewal is weak;
- high `F` is not treated as proof of high absolute vapor transfer;
- positive evaporation is not treated as proof of positive body cooling;
- fully-wet transfer-capacity states are not reused after liquid feed becomes limiting;
- stronger linked external exchange is not assumed always beneficial at fixed feed;
- identical evaporation mass is not assumed to imply identical body heat removal;
- arbitrary `Xi<1` heat/vapor decoupling is not assumed physically available without a mechanism;
- symmetric heat spreading is not credited with global cooling when wet/dry external conditions are identical;
- dense asymmetric `g_mix` sweeps no longer rely on an unconstrained nonlinear root that could jump to a nonphysical high-beta branch;
- infinite heat-spreader conductivity is not treated as a design goal; corrected screens show finite diminishing-return targets;
- sparse conductive coverage is not assumed to reduce mass under the linear `t*c` conductance model;
- sheet conductivity is not treated as sufficient without explicit routing pitch/topology/contact resistance;
- virtual-prototype spreader-only mechanism gain is not reported as total garment-vs-control performance;
- VP-C sparse coverage in the distributed bridge is explicitly identified as a homogenized effective-thickness approximation rather than resolved trace geometry.

### Virtual prototype v0.1 — scalar anchors

At 100 g/h:

| prototype | nominal spreader mass over 0.30 m² | nominal `g_eff` | scalar spreader-only gain over 0.195 m² |
|---|---:|---:|---:|
| VP-A | ~48 g | ~286 W/(m² K) | ~5.3 W |
| VP-B | ~96 g | ~167 | ~4.9 W |
| VP-C | ~27 g | ~197 | ~5.0 W |
| VP-D | ~48 g | ~286 | ~6.1 W |

### Distributed direct-material bridge

At 100 g/h, equal-feed no-lateral baseline comparison gives:

| prototype | distributed wet fraction | distributed spreader-only gain over 0.195 m² |
|---|---:|---:|
| VP-A | ~0.444 | ~5.48 W |
| VP-B | ~0.448 | ~5.32 W |
| VP-C | ~0.451 | ~5.30 W |
| VP-D | ~0.447 | ~6.29 W |

Numerical checks show feed closure better than ~0.001 g/h, outer energy residual numerically near zero, spreader-equation residual ~0.004 W/m² or below, and small grid sensitivity. Distributed gains remain within roughly 0.8 W of the scalar virtual anchors. This is hierarchy consistency, not physical validation.

### Current research direction

The preferred virtual architecture is:

- directional liquid transport and capillary delivery;
- wet micro-rib / 3D-knit / short-fin exterior fields;
- continuously ambient-connected open valleys/gaps/islands;
- short-range heat routing, initially concentrated around 10–20 mm pitch;
- high `k/rho` paths with explicit `k*t/P²` accounting;
- explicit wet/dry thermal contacts;
- explicit liquid-supply/wetness state;
- dry-side hot-ambient shielding / selective exposure.

Next model step: move from periodic 1-D to a 2-D geometry-resolved wet/dry heat-routing field containing direct `k_x/k_y`, thickness, explicit routed traces, contact maps, wet islands, dry shielding and curvature/compression sensitivity. VP-A–D remain regression anchors.

## Verification

- `model-tests` #370 passed at `a01eeafc8ae6814349a3a0937251efd048823dae`, covering the pre-material-mapping expanded stack.
- The current 20-module + distributed-spreader head requires a newer passing CI run before being recorded as the next verified integration point.

## Release policy

Stable releases should be tagged and archived without overwriting earlier public records. A stable release should include the frozen technical disclosure, virtual-prototype specifications, source, reference data, metadata, SHA-256 manifest, version/citation metadata, and release notes.
