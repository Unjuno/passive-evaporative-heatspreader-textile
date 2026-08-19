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
- **explicit virtual prototypes v0.1**: VP-A short-pitch, VP-B 20 mm comparison, VP-C lightweight/high-`k/rho`, VP-D shielded short-pitch;
- deterministic topology/contact robustness screen for VP-A through VP-D;
- anisotropic 2-D heat spreading and normalized nonvolatile water/salt models;
- future E3b/E3c/E4a/E4/E6 validation protocols and measurement/uncertainty templates;
- regression tests and GitHub Actions CI;
- reproducible CSV/PNG/metadata/SHA-256 reference package including material/contact and virtual-prototype outputs.

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
- a dense asymmetric `g_mix` sweep exposed a nonphysical branch jump in the old unconstrained root solver; the solver is now bounded, continuation-capable, and residual-checked;
- infinite heat-spreader conductivity is not treated as a design goal; corrected screens show finite diminishing-return targets;
- sparse conductive coverage is not assumed to reduce mass under the linear `t*c` conductance model;
- sheet conductivity is not treated as sufficient without explicit routing pitch/topology/contact resistance;
- virtual-prototype spreader-only mechanism gain is not reported as total garment-vs-control performance.

### Virtual prototype v0.1

At 100 g/h in the current asymmetric mechanism screen:

| prototype | nominal spreader mass over 0.30 m² | nominal `g_eff` | modeled spreader-only gain over 0.195 m² |
|---|---:|---:|---:|
| VP-A | ~48 g | ~286 W/(m² K) | ~5.3 W |
| VP-B | ~96 g | ~167 W/(m² K) | ~4.9 W |
| VP-C | ~27 g | ~197 W/(m² K) | ~5.0 W |
| VP-D | ~48 g | ~286 W/(m² K) | ~6.1 W |

Current roles: VP-D performance anchor, VP-C lightweight anchor, VP-A short-pitch baseline, VP-B routing-distance/manufacturability comparison.

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

Next model step: replace scalar `g_mix` with a distributed 1-D/2-D wet/dry heat-routing field containing direct material `k`, thickness, anisotropy, patch pitch, contacts, dry shielding and evaporative sink strength. VP-A–D remain regression anchors.

## Verification

- `model-tests` #370 passed at `a01eeafc8ae6814349a3a0937251efd048823dae`, covering the pre-material-mapping expanded stack.
- The current 19-module + virtual-prototype head requires a newer passing CI run before being recorded as the next verified integration point.

## Release policy

Stable releases should be tagged and archived without overwriting earlier public records. A stable release should include the frozen technical disclosure, virtual-prototype specifications, source, reference data, metadata, SHA-256 manifest, version/citation metadata, and release notes.
