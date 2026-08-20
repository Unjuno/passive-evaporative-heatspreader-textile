# Repository Audit

Audit date: 2026-08-20  
Branch: `agent/initial-research-disclosure`

## Overall assessment

The branch now contains a coherent technical disclosure, explicit implementation variants, **43 executable screening/sensitivity/audit/virtual-prototype models**, regression tests, reference CSVs, multiple CI workflows, prior-art working notes, and future physical-validation specifications.

It remains a **virtual/computational prototype only**. No physical garment or bench specimen exists and no measured garment-performance claim is made.

The current integrated design hypothesis is:

> directional local sweat collection + distributed two-scale capillary liquid routes + pressure-aware wet terminals + continuously ambient-connected evaporative microtexture/open valleys + short high-`k/rho` heat routes with limited redundancy + terminal contact management + dry-side hot-ambient protection.

The design has moved away from garment-scale centralized liquid lift, long covered wet chimneys, indiscriminate full-area high-`k` spreading, geometric surface area alone, and active layout switching as baseline mechanisms.

## A. Technical coherence

| Item | Status | Audit note |
|---|---|---|
| Directional sweat collection | PASS/CONCEPT | Retained as skin-side source layer. |
| Distributed capillary delivery | PASS/SCREEN | Local short routes explicitly favored over centralized lift. |
| Hierarchical liquid pore scale | PASS/SCREEN | Fine collector + larger transport trunk now screened as a two-scale network. |
| Exterior micro-ribs / 3D knit / fins | PASS/CONCEPT | Multiple exterior families retained. |
| Ambient-open valleys/islands | PASS/SCREEN | Preferred to long covered wet corridors. |
| Sensible/vapor separation | PASS | Heat and vapor transfer are not forced to share one multiplier. |
| Feed-limited state | PASS/SCREEN | Water supply is explicit in the open-valley stack. |
| Wet/dry thermal asymmetry | PASS/SCREEN | Required for integrated heat-spreader value. |
| Direct heat-routing topology | PASS/DEV | 1-D direct `k*t` and 2-D explicit topology models exist. |
| Damage/stretch/contact robustness | PASS/SCREEN | Separate and combined failure maps exist. |
| Compression regime transition | PASS/SCREEN | Contact benefit vs vapor-path closure is explicit. |
| Spatial pressure maps | PASS/SCREEN | Backpack/strap/seat synthetic maps and equal-area terminal layouts exist. |
| Protected under-load vapor path | PASS/HYPOTHESIS | Effective air-access floor and support-area penalty are explicit. |
| Relative terminal route proxy | PASS/CORRECTED | Useful as a geometric tradeoff, not proof of a binding hydraulic-pressure benefit. |
| Explicit branched liquid network | PASS/SCREEN | Distributed source flow to many terminals solved with pressure-dependent radii. |
| Sparse two-scale liquid network | PASS/SCREEN | Collector radius, trunk pitch and lattice phase now screened jointly. |
| Load-schedule adaptation | PASS/SCREEN | Ideal switching adds little in current quasisteady scenarios; fixed passive layout remains baseline. |
| Virtual garment mass/thickness budget | PASS/SCREEN | Lean/nominal/conservative BOM envelopes exist; values are design variables, not measured materials. |
| Integrated VP-E anchor | PASS/DEV | Heat, liquid class, terminal and environment models are combined, but final terminal geometry remains open. |
| Hot-ambient protection | PASS/HYPOTHESIS | Required by signed heat-flow screens. |
| Salt nonvolatility | PASS | Salt vapor flux is exactly zero. |
| Bulk salt leakage correction | PASS/CORRECTION | Small upstream water loss does not by itself imply bulk saturation. |
| Physical validation | NOT EXECUTED | No specimen exists. |

## B. Executable model / audit stack

See `simulations/README.md` for the indexed list. Current count: **43** executable models, plus `generate_reference_outputs.py` as a reproducibility generator.

Major groups:

- exterior heat/vapor physics;
- heat routing / virtual prototypes;
- spatial load / terminal / environment architecture;
- liquid transport / nonvolatile solute;
- dense and sparse branched liquid-network screens.

## C. Reproducibility / verification

| Item | Status | Audit note |
|---|---|---|
| Broad regression suite | PASS/DEV | Existing model/topology tests retained. |
| Dedicated pressure CI | PASS/DEFINED | Includes terminal-route proxy regression. |
| Dedicated liquid CI | PASS/DEFINED | Includes capillary, salt, dense branched and sparse branched tests. |
| Pressure reference tables | PASS/SCREEN | Converged 24 x 24 references committed. |
| Capillary reference tables | PASS/SCREEN | Central/local, radius-cap, collapse and salt references committed. |
| Dense branched-flow reference | PASS/SCREEN | Absolute liquid-network pressure reference committed. |
| Sparse phase-robust reference | PASS/SCREEN | Collector-radius / trunk-pitch boundaries committed. |
| Current full-head CI | CHECK | Do not call the current 43-model head verified until latest workflows complete successfully. |

## D. Major findings retained

### D1 — exterior area requires ambient access

Dense wet ribs can share one humidity boundary layer. Geometric area alone is not accepted as proof of useful evaporation.

### D2 — long covered wet corridors are weak

Covered/end-renewed channels can remain nearly saturated despite nonzero buoyant flow; flow direction can reverse.

### D3 — positive evaporation is not equivalent to body cooling

Warm ambient air can supply a substantial fraction of latent heat. Signed body-side heat flow remains the integrated thermal endpoint.

### D4 — feed limitation changes the optimum

Once available water is fully evaporated, stronger linked ambient exchange can lower body-coupled cooling by supplying more latent heat from ambient air.

### D5 — heat spreading requires spatially different boundary conditions

Symmetric wet/dry exposure produces little integrated gain. Shielding, pressure, wetting and exposure heterogeneity create finite routing value.

### D6 — heat-routing distance/contact are first-order burdens

Ideal routing burden grows approximately as `P^2`; two terminal contacts can cap useful sheet conductivity.

### D7 — corrected equal-material topology result

The retained ordering is:

`uniform homogenized > x-aligned / mesh >> y-transverse`.

The earlier opposite claim is withdrawn in the repository record.

### D8 — robust heat topology is failure-map dependent

For the current combined stretch/contact/fracture map, the lightly cross-linked directed network (`lambda≈0.125`) is the strongest screened robustness anchor, not the nominal-gain maximum.

### D9 — spatial load changes evaporator placement

Under synthetic backpack/strap/seat maps, low-pressure wet-terminal placement ranks highest in the primary pressure-closure screen. Under no load, ordinary four-island placement can be better.

Therefore the conclusion is pressure-aware placement in load-prone regions, not universal peripheral evaporation.

### D10 — under-load evaporation requires strong vapor-path protection

For the primary backpack+strap screen, a loaded center wet panel needs an effective wet-side air-access floor near ~0.83–0.85 to match the relocated pressure-aware terminal.

This is a model parameter, not a measured porosity/velocity requirement.

### D11 — support structures consume evaporator area

At an air-access floor of 0.90 only about 2.5% support footprint still matches relocation; at 0.95 about 7.5%; at 1.00 about 10%.

This favors narrow ribs, point/perimeter supports or arches rather than coarse lattices.

### D12 — active wet-layout switching is not currently justified

Ideal statewise switching improves the best fixed layout by only about 0.10–0.23 W over 0.195 m² in the current quasisteady schedules.

### D13 — distributed liquid delivery beats long centralized lift in the ideal capillary model

For 150 g/h total flow, an illustrative 200 mm / 100 mm-rise centralized route requires roughly 48 mm² ideal total capillary cross-section, while four 50 mm / 25 mm-rise local cells require about 3 mm².

### D14 — capillary radius has a lift/resistance optimum

For positive lift,

\[
r_* = \frac{\gamma\cos\theta}{\rho g\Delta z},
\]

which is half the largest radius capable of statically supporting the same rise.

### D15 — liquid capture and transport should use different hydraulic scales

Short fine-pore collection can provide capillary pressure while larger liquid-filled trunks carry longer-distance flow. The exterior evaporator remains a separate terminal phase-change zone.

### D16 — salt leakage wording is corrected

Salt vapor flux is zero. If upstream evaporation removes water fraction `f_leak`,

\[
\sigma_{out}=\sigma_0/(1-f_{leak}).
\]

Thus 10% water leakage raises bulk concentration only ~1.11x. Small leakage does not mathematically guarantee bulk crystallization.

### D17 — geometric terminal-route regularization is real, but its hydraulic interpretation was too strong

The 24 x 24 route proxy found:

- pure thermal pressure-aware layout: ~112.84 W/m², `d95≈20.16 mm`;
- regularized candidate: ~110.83 W/m², `d95≈16.77 mm`.

The regularized candidate retained ~98.21% of thermal output while reducing the common `d95 r^-4` proxy by ~16.79%.

This remains a valid **geometric Pareto result**. It no longer establishes that the regularized layout is hydraulically necessary.

### D18 — explicit branched flow shows dense local 50–200 µm trunks have enormous capillary margin

For a 60 mm, 24 x 24 tile carrying 1.8 g/h, with 200 µm nominal trunks, 50 µm collector radius, 15 mm lift and radius retention down to 0.70:

- thermal pressure-aware terminal layout: max network drop ~0.526 Pa;
- regularized layout: ~0.470 Pa;
- four-island layout: ~0.205 Pa.

Collector capillary drive is ~2278 Pa. The safety-factor-3 single-network critical nominal radius is only ~26–32 µm depending on terminal layout.

Therefore the earlier route proxy cannot justify sacrificing thermal performance for the current dense 50–200 µm local network.

### D19 — after sparsification, collector radius and trunk pitch become binding

A 200 µm trunk lattice was embedded in a 20–50 µm collector mesh and shifted through multiple grid phases under a localized sweat source.

Largest tested trunk pitch for which **all sampled phases** retain capillary margin >=3:

| collector radius | largest robust tested pitch |
|---:|---:|
| 20 µm | ~15 mm |
| 25 µm | ~20 mm |
| 30 µm | ~30 mm |
| 35 µm | >=60 mm |
| 40 µm | >=60 mm |
| 50 µm | >=60 mm |

This is now the more useful hydraulic design boundary. A single favorable trunk-grid phase is not accepted as a robust result.

### D20 — current BOM screens do not make mass the dominant blocker

The nominal pressure-relocation BOM screen gives roughly 169 g dry / 181 g operating mass, including a ~109 g base textile. Broad deterministic parameter sampling puts the median added functional dry mass near 71 g. These are design-range calculations only.

## E. Public-release readiness

| Item | Status |
|---|---|
| Public GitHub repository | PASS |
| Apache-2.0 | PASS |
| Integrated technical disclosure | PASS / development |
| 43-model executable screening stack | PASS / development |
| Regression tests / dedicated workflows | PASS / development |
| Explicit pressure/load architecture | PASS / development |
| Explicit dense/sparse liquid routing | PASS / development |
| Salt nonvolatility / corrected leakage balance | PASS |
| Physical data | NOT AVAILABLE / not required for current computational record |
| Authoritative patent-family/claim verification | OPEN |
| Root `docs/current-results.md` consolidated to newest state | OPEN |
| Stable release tag | MISSING |
| Persistent archive / DOI | MISSING |
| Frozen release SHA-256 manifest | MISSING |

## F. Remaining queue

### P0 — repository consistency

- [x] synchronize simulation index to 43 executable models;
- [x] document dense-network correction;
- [x] document sparse collector-radius / trunk-pitch boundary;
- [x] include dense and sparse network regressions in liquid CI;
- [ ] update root README and PR summary to the 43-model state;
- [ ] obtain successful current-head runs for model/topology/pressure/liquid/garment workflows;
- [ ] consolidate newest corrections into `docs/current-results.md`;
- [ ] update changelog after CI success.

### P1 — model strengthening

- [x] replace the route-distance-only pressure argument with an explicit dense branched-flow solve;
- [x] sparsify the network and test collector-radius / trunk-pitch / phase sensitivity;
- [ ] jointly optimize thermal terminal placement, collector radius, trunk pitch and liquid-network material burden;
- [ ] add broader localized/time-varying sweat-source maps;
- [ ] map protected gap height/width/support spacing to vapor exchange;
- [ ] model local wall-film evaporation/deposition and progressive hydraulic-radius loss;
- [ ] geometry-resolved exterior natural convection/cross-flow.

### P2 — virtual garment completion

- [x] screening mass/thickness budget;
- [x] integrated VP-E computational stack;
- [ ] freeze final terminal-placement rule after sparse-network/material optimization;
- [ ] garment-scale regional layout rather than one repeating tile;
- [ ] curvature and seam placement;
- [ ] explicit full-garment liquid/heat network material budget.

### P3 — stable publication

- [ ] authoritative patent-office family/claim verification;
- [ ] freeze exact technical-disclosure + integrated virtual-prototype commit;
- [ ] regenerate reference artifacts and SHA-256 at that commit;
- [ ] update `CITATION.cff`, version and release notes;
- [ ] create stable tag/release;
- [ ] archive persistently after internal consistency review.
