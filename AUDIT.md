# Repository Audit

Audit date: 2026-08-20  
Branch: `agent/initial-research-disclosure`

## Overall assessment

The branch now contains a coherent technical disclosure, explicit implementation variants, **34 executable screening/sensitivity/audit/virtual-prototype modules**, regression tests, reference CSVs, multiple CI workflows, prior-art working notes, and future physical-validation specifications.

It remains a **virtual/computational prototype only**. No physical garment or bench specimen exists and no measured garment-performance claim is made.

The current integrated design hypothesis is:

> directional local sweat collection + distributed short capillary liquid routes + pressure-aware wet terminals regularized against excessive liquid-route length + continuously ambient-connected evaporative microtexture/open valleys + short high-`k/rho` heat routes with limited redundancy + terminal contact management + dry-side hot-ambient protection.

The design has moved away from garment-scale centralized liquid lift, long covered wet chimneys, indiscriminate full-area high-`k` spreading, geometric surface area alone, and active layout switching as baseline mechanisms.

## A. Technical coherence

| Item | Status | Audit note |
|---|---|---|
| Directional sweat collection | PASS/CONCEPT | Retained as skin-side source layer. |
| Distributed capillary delivery | PASS/SCREEN | Local short routes explicitly favored over centralized lift. |
| Hierarchical liquid pore scale | PASS/HYPOTHESIS | Short fine collector + larger transport trunk is explicit. |
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
| Pressure/liquid terminal co-design | PASS/SCREEN | Thermal-only pressure avoidance is regularized against excessive liquid-route burden. |
| Load-schedule adaptation | PASS/SCREEN | Ideal switching adds little in current quasisteady scenarios; fixed robust layout remains baseline. |
| Virtual garment mass/thickness budget | PASS/SCREEN | Lean/nominal/conservative BOM envelopes exist; values are design variables, not measured materials. |
| Integrated VP-E anchor | PASS/SCREEN | Heat network, liquid network, wet-terminal rule and environment state are combined computationally. |
| Hot-ambient protection | PASS/HYPOTHESIS | Required by signed heat-flow screens. |
| Salt nonvolatility | PASS | Salt vapor flux is exactly zero. |
| Bulk salt leakage correction | PASS/CORRECTION | Small upstream water loss does not by itself imply bulk saturation. |
| Physical validation | NOT EXECUTED | No specimen exists. |

## B. Executable model / audit stack

See `simulations/README.md` for the indexed list. Current count: **34**.

Major groups include:

- exterior heat/vapor physics;
- heat routing / virtual prototypes;
- spatial load / apparel architecture;
- liquid transport / nonvolatile solute;
- integrated pressure/terminal/liquid co-design.

`generate_reference_outputs.py` remains a reproducibility generator rather than a physical model.

## C. Reproducibility / verification

| Item | Status | Audit note |
|---|---|---|
| Broad regression suite | PASS/DEV | Existing model/topology tests retained. |
| Dedicated pressure CI | PASS/DEFINED | `pressure-tests.yml` now includes pressure/liquid co-design regression. |
| Dedicated liquid CI | PASS/DEFINED | `liquid-tests.yml` covers capillary architecture/practical/salt regression tests. |
| 24 x 24 pressure reference | PASS/SCREEN | Converged reference CSV committed. |
| Protected-air reference | PASS/SCREEN | 24 x 24 floor sweep committed. |
| Support-skeleton frontier | PASS/SCREEN | Reference frontier committed. |
| Load-schedule reference | PASS/SCREEN | Quasisteady 24 x 24 scenario summary committed. |
| Capillary reference tables | PASS/SCREEN | Central/local, radius-cap and salt-leakage references committed. |
| Pressure/liquid co-design reference | PASS/SCREEN | 24 x 24 anchor comparison committed. |
| Current full-head CI | CHECK | Do not call the current 34-module head verified until current workflow runs complete successfully. |

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

### D7 — explicit sparse traces do not beat the homogenized ideal reference in the corrected equal-material screen

The corrected ordering is:

`uniform homogenized > x-aligned / mesh >> y-transverse`.

The earlier opposite claim is withdrawn in the repository record.

### D8 — robust heat topology is failure-map dependent

For the current combined stretch/contact/fracture map, the lightly cross-linked directed network (`lambda≈0.125`) is the strongest screened robustness anchor, not the nominal-gain maximum.

### D9 — spatial load changes evaporator placement

Under synthetic backpack/strap/seat maps, low-pressure wet-terminal placement ranks highest in the primary pressure-closure screen. Under no load, ordinary four-island placement can be better.

Therefore the conclusion is pressure-aware placement in load-prone garment regions, not universal peripheral evaporation.

### D10 — under-load evaporation can work only if vapor access is protected strongly enough

For the primary backpack+strap screen, a loaded center wet panel needs an effective wet-side air-access floor near ~0.83–0.85 to match the relocated pressure-aware terminal.

This is a model parameter, not a measured porosity/velocity requirement.

### D11 — support structures consume evaporator area

After charging support footprint against the loaded wet panel, the screened feasible region is narrow:

- air floor 0.90: only about 2.5% support footprint still matches relocation;
- 0.95: about 7.5%;
- 1.00: about 10%.

This favors narrow ribs, point/perimeter supports or arches rather than coarse lattices.

### D12 — active wet-layout switching is not currently justified

Ideal statewise switching improves the best fixed layout by only about 0.10–0.23 W over 0.195 m² in the current quasisteady commuter/office/mixed schedules. A sub-percent switching/control penalty can erase this benefit.

### D13 — distributed capillary delivery is strongly favored in the ideal liquid model

For 150 g/h total flow, an illustrative 200 mm / 100 mm-rise centralized route requires roughly 48 mm² ideal total capillary cross-section, while four 50 mm / 25 mm-rise local cells require about 3 mm².

This is geometry-dependent, not a universal performance ratio.

### D14 — capillary radius has a lift/resistance optimum

For positive lift,

\[
r_* = \frac{\gamma\cos\theta}{\rho g\Delta z},
\]

which is half the largest radius capable of statically supporting the same rise.

A 4-local-cell reference remains near its unconstrained ideal burden with a ~200 µm maximum radius; a 75–100 µm cap imposes a much larger hydraulic area penalty.

### D15 — liquid capture and transport should use different hydraulic scales

Short fine-pore collection can provide capillary pressure while larger liquid-filled trunks carry longer-distance flow. The exterior evaporator remains a separate terminal phase-change zone.

### D16 — salt leakage wording is corrected

Salt vapor flux is zero. If upstream evaporation removes water fraction `f_leak`, the bulk normalized concentration is

\[
\sigma_{out}=\sigma_0/(1-f_{leak}).
\]

Thus 10% water leakage raises bulk concentration only ~1.11x. Small leakage does not mathematically guarantee bulk crystallization. Local wall-film drying/nucleation remains unresolved and is a separate reason to keep evaporation out of permanent buried channels.

### D17 — pressure avoidance and liquid routing must be co-designed

Pure pressure avoidance maximizes the current thermal screen but lengthens liquid routes. At the converged 24 x 24 backpack+straps reference:

- pure thermal optimum: `beta=0`, route weight `0.20`, body heat flux ~112.84 W/m², liquid `d95` ~20.16 mm;
- co-design anchor: `beta=0.125`, route weight `0.35`, body heat flux ~110.83 W/m², liquid `d95` ~16.77 mm.

Using the same protected-trunk `r^-4` burden proxy for both candidates, the co-design anchor retains ~98.21% of thermal performance while reducing the hydraulic p95 proxy by ~16.79%.

This makes `beta=0.125 / route weight=0.35` the current VP-E terminal-placement anchor rather than the pure thermal optimum.

### D18 — current BOM screens do not make mass the dominant blocker

The nominal pressure-relocation BOM screen gives roughly 169 g dry / 181 g operating mass, including a ~109 g base textile. Broad deterministic parameter sampling puts the median added functional dry mass near 71 g. These are design-range calculations only; real materials and construction have not been measured.

## E. Public-release readiness

| Item | Status |
|---|---|
| Public GitHub repository | PASS |
| Apache-2.0 | PASS |
| Integrated technical disclosure | PASS / development |
| 34-module executable screening stack | PASS / development |
| Regression tests / dedicated workflows | PASS / development |
| Explicit pressure/load architecture | PASS / development |
| Explicit liquid-routing architecture | PASS / development |
| Pressure/liquid co-design anchor | PASS / development |
| Salt nonvolatility / corrected leakage balance | PASS |
| Physical data | NOT AVAILABLE / not required for current computational record |
| Authoritative patent-family/claim verification | OPEN |
| Root `docs/current-results.md` fully consolidated to newest state | OPEN |
| Stable release tag | MISSING |
| Persistent archive / DOI | MISSING |
| Frozen release SHA-256 manifest | MISSING |

## F. Remaining queue

### P0 — repository consistency

- [x] update root README to prior 33-module architecture;
- [x] add pressure/load reference CSVs and dedicated CI;
- [x] add liquid-routing/salt reference CSVs and dedicated CI;
- [x] add pressure/liquid co-design module, regression test and reference CSV;
- [ ] update simulation index / README count from 33 to 34;
- [ ] obtain successful current-head runs for model/topology/pressure/liquid workflows;
- [ ] consolidate newest co-design conclusion into `docs/current-results.md`;
- [ ] update changelog and PR module count/verification section after CI success.

### P1 — model strengthening

- [x] first-order co-optimize terminal thermal performance and liquid-route burden;
- [x] add explicit trunk/channel radius-collapse sensitivity under pressure proxy;
- [ ] replace route-distance/hydraulic proxies with an integrated branched liquid network solve;
- [ ] map protected gap height/width/support spacing to vapor exchange instead of an effective air-access floor;
- [ ] model local wall-film evaporation/deposition and progressive hydraulic-radius loss;
- [ ] geometry-resolved exterior natural convection/cross-flow;
- [ ] complete hot/humid environmental map with independent wet/dry exposure controls at converged full reference resolution.

### P2 — virtual garment completion

- [x] screening mass/thickness budget including textile, high-`k` routes, capillary structures, terminal microtexture and stored liquid;
- [x] explicit integrated VP-E computational anchor combining one heat network, one liquid-network class and one terminal-placement rule;
- [ ] garment-scale regional layout using expected load zones rather than one repeating tile;
- [ ] curvature and seam placement;
- [ ] convert the current terminal/liquid co-design proxy into explicit garment-cell routing geometry.

### P3 — stable publication

- [ ] authoritative patent-office family/claim verification;
- [ ] freeze exact technical-disclosure + integrated virtual-prototype commit;
- [ ] regenerate reference artifacts and SHA-256 at that commit;
- [ ] update `CITATION.cff`, version and release notes;
- [ ] create stable tag/release;
- [ ] archive persistently after internal consistency review.
