# Repository Audit

Audit date: 2026-08-20  
Branch: `agent/initial-research-disclosure`

## Overall assessment

The branch contains a coherent technical disclosure, explicit implementation variants, **eleven executable screening/sensitivity/identification modules**, regression tests, reproducible reference-output generation, prior-art working notes, and staged physical protocols.

It remains a development branch. **No physical garment-performance measurements have been published yet.**

The present numerical record supports a narrower and more falsifiable exterior design direction:

> wet microstructures + strong lateral heat routing + continuously ambient-connected exterior valleys/islands, evaluated with both vapor-renewal quality and absolute body-coupled cooling.

Long covered passive chimneys, geometric area alone, centimeter-scale interruption alone, and high local vapor-retention `F` alone are no longer accepted as sufficient design criteria.

## A. Technical coherence

| Item | Status | Audit note |
|---|---|---|
| Directional sweat transport | PASS | Core layer retained. |
| Flexible whole-garment/routed heat spreader | PASS | Continuous, anisotropic, mesh, serpentine, island-bridge variants documented. |
| Capillary liquid delivery | PASS | Distributed liquid path retained. |
| Exterior micro-ribs / 3D knit / fins / lamellae | PASS | Multiple concrete families documented. |
| Hierarchical ambient-access exterior | PASS | Open valleys, cross-openings, short interruptions, islands and covered comparison channels explicit. |
| Sensible/vapor separation | PASS | Heat and vapor exchange are not forced to share one multiplier. |
| Hot-ambient dry-side protection | PASS/HYPOTHESIS | Required by several screens; physical validation still open. |
| Fan | OPTIONAL | Not required by primary architecture. |
| Sorbent/MOF | OPTIONAL | Secondary embodiment only. |
| Salt | PASS | Water evaporates; salt vapor flux is zero. |
| Apparel integration | PASS | Low-profile texture/pattern implementations documented. |

## B. Executable model stack

1. `simulations/passive_rib_screen.py` — historical coupled exterior heat/mass screen and multi-root audit.
2. `simulations/split_heat_mass_screen.py` — independent `M_h` and `M_m` lumped screen.
3. `simulations/split_transfer_sensitivity.py` — deterministic model-form sensitivity grid.
4. `simulations/rib_diffusion_screen.py` — periodic 2-D rib vapor-diffusion screen.
5. `simulations/corridor_buoyancy_screen.py` — prescribed-state thermo-solutal corridor buoyancy.
6. `simulations/self_consistent_corridor_1d.py` — covered/end-renewed corridor T/RH/flow coupling.
7. `simulations/open_valley_exchange_target.py` — local open-valley `R/F` target and measurement inversion.
8. `simulations/open_valley_distributed_1d.py` — axial diffusion/advection plus distributed lateral vapor renewal.
9. `simulations/open_valley_thermal_1d.py` — distributed open-valley heat/vapor/wet-wall energy coupling.
10. `simulations/heat_spreader_2d.py` — anisotropic lateral heat-routing screen.
11. `simulations/water_salt_1d.py` — nonvolatile salt/water mass-balance screen.

All are screening models. None is a validated CFD replacement or physical garment-performance measurement.

## C. Reproducibility / verification

| Item | Status | Audit note |
|---|---|---|
| Regression tests | PASS | Include multi-root, split transfer, E3, corridor, open-valley, heat-spreader and salt checks. |
| E3 grid convergence | PASS/SCREEN | 24 nodes/pitch within ~0.62% of 48-node reference for the screened case. |
| Distributed open-valley convergence | PASS/SCREEN | Center `F` stable over tested grids. |
| Wall-energy closure | PASS/NEW | Thermal open-valley test enforces `q_body + q_air = L_v m_evap` numerically. |
| Reference generator | PASS/UPDATED | Includes distributed and coupled open-valley CSVs plus metadata/SHA-256. |
| CI definition | PASS/UPDATED | All current models and generated outputs are exercised. |
| Verified computational integration | **PASS** | GitHub Actions `model-tests` **#231** succeeded at SHA `7f015b8e1b0278f29b545f41d24674b5a394ee79`. |
| Later documentation-only commits | INFO | May trigger newer CI runs; #231 is the explicitly verified thermal-model integration point. |

## D. Major numerical findings

### D1 — nonlinear equilibrium branches

The original lumped passive heat/mass model can contain multiple stable equilibria. Historical single-value `M` thresholds are retained only as exploratory references. Current code exposes all detected stable roots.

### D2 — rib boundary-layer sharing

For the E3 screen (`h=2.5 mm`, structured fraction `f=0.65`), whole-area vapor multipliers fall from roughly 3–4 at a 0.5 mm idealized renewal gap to roughly 1.3 at a 5 mm gap. Tight pitch alone cannot overcome a shared stagnant humidity layer.

### D3 — sensible and vapor exchange differ

`M_h` and `M_m` are distinct. In hot ambient air, improved vapor transfer can help evaporation while improved sensible transfer can increase inward environmental heat pickup.

### D4 — passive corridor flow can reverse

Thermo-solutal buoyancy can produce upward, downward or near-neutral flow. A vertical groove is not a guaranteed chimney.

### D5 — covered/end-renewed corridors saturate

The self-consistent 100 mm corridor screen at 35 °C / 70% RH gives nonzero natural flow but mean RH near saturation for 3×2, 6×3 and 10×5 mm channels. High axial Péclet number is not proof that useful vapor driving force remains.

### D6 — open-valley renewal requirement

For local conductance ratio

\[
R=G_a/G_w,
\qquad F=\frac{R}{1+R},
\]

`F=0.8` requires `R=4`; `F=0.9` requires `R=9`. Exact high inferred `R` is measurement-ill-conditioned, so `F` is the preferred mechanism metric.

### D7 — centimeter-scale segmentation correction

The distributed vapor model gives a representative exchange length of roughly 0.7–1.1 mm for a 6×3 mm valley across the screened lateral-exchange range. Therefore 20–50 mm interruption alone does not materially rescue a weakly renewed interior.

Current E3c roles are:

- O1 — continuously laterally open: principal hypothesis;
- O2a — 20–50 mm interruption: negative/control;
- O2b — 1–3 mm segments: extreme end-access test;
- O3 — discontinuous ambient-connected wet islands: apparel-relevant implementation.

### D8 — `F` is not absolute evaporation capacity

For local resistances in series:

\[
k_{eff}=\frac{k_wk_a}{k_w+k_a}=k_wF.
\]

In the current geometry mapping, deeper valleys can increase `F` while decreasing `k_eff`. Therefore every design must report both renewal quality (`F`) and absolute useful transfer (evaporation flux, `k_eff`, and ultimately heater power).

### D9 — coupled open-valley thermal result

Representative 6×3×50 mm, zero prescribed axial flow, `U_body=100 W/(m² K)`:

At 35 °C / 70% RH:

| `delta_vapor` | `delta_heat` | evaporation | body-side heat flux | ambient sensible heat to wet wall |
|---:|---:|---:|---:|---:|
| 0.1 mm | 0.1 mm | ~700 g/m²h | +299 W/m² | +172 W/m² |
| 0.1 mm | 0.5 mm | ~645 g/m²h | +319 W/m² | +115 W/m² |
| 0.5 mm | 0.5 mm | ~522 g/m²h | +254 W/m² | +97 W/m² |
| 1.0 mm | 1.0 mm | ~414 g/m²h | +216 W/m² | +63 W/m² |

At 40 °C / 70% RH with Lewis-like linked exchange (`delta_heat=delta_vapor`), evaporation remains positive while body-side heat flux is negative in all screened linked cases, for example approximately −16 W/m² at `delta=0.5 mm`.

**Audit conclusion:** positive evaporation is not equivalent to wearer cooling. Heater power/body-side heat flow remains the integrated endpoint.

### D10 — liquid-supply limit

The coupled thermal solver currently predicts transfer capacity without imposing a water-feed cap.

For 65% of a 0.30 m² active area:

- 35 °C / 70% RH, strongest linked screened case: ~136.5 g/h capacity, below the primary 150 g/h feed;
- 35 °C / 50% RH, same exchange case: ~248 g/h capacity, above 150 g/h and therefore **supply-limited** in the planned experiment.

No numerical capacity above available feed may be reported as achievable evaporation at fixed feed.

## E. Experimental readiness

| Item | Status | Audit note |
|---|---|---|
| B0/B2/B3/B4 controls | PASS | Defined. |
| Primary environment | PASS | 35 °C / 70% RH / 150 g/h / nominal still air / 34 °C artificial skin. |
| Primary endpoint | PASS | Heater-power difference. |
| Water balance | PASS | >=95% target. |
| E3/E3b | PASS/PLANNED | Pitch/boundary-layer and hierarchical access tests defined. |
| E3c | PASS/UPDATED | D1/O1/O2a/O2b/O3 defined with `F` plus absolute-transfer metrics. |
| E4 humidity | PASS/PLANNED | Supply-limit classification added. |
| E6 hot ambient | PASS/UPDATED | Positive evaporation with negative body cooling is an explicit failure mode. |
| Physical data | **MISSING** | No bench experiment executed yet. |
| Exact hardware/calibration budget | PARTIAL | Still required before a PASS-quality physical run. |

## F. Public-release readiness

| Item | Status |
|---|---|
| Public GitHub repository | PASS |
| Apache-2.0 | PASS |
| Integrated technical disclosure | PASS / development |
| Concrete embodiment matrix | PASS / development |
| Reproducible model stack | PASS / screening |
| Experimental protocols | PASS / planned |
| Authoritative patent-office claim mapping | OPEN |
| Physical evidence | MISSING |
| Stable release tag | MISSING |
| Persistent archive / DOI | MISSING |
| Frozen release SHA-256 manifest | MISSING |

## G. Remaining queue

### P0 — repository quality

- [x] distributed open-valley vapor model;
- [x] `F`/`k_eff` metric audit;
- [x] coupled open-valley thermal/vapor model;
- [x] regression energy closure and hot-ambient sign tests;
- [x] reference-generator / CI integration;
- [x] verified thermal integration: `model-tests` #231 at `7f015b8e1b0278f29b545f41d24674b5a394ee79`;
- [x] update master experiment plan for O2a/O2b, `F`, `k_eff`, supply limits and hot-ambient sign;
- [ ] synchronize README/current-results/roadmap/changelog/PR narrative after the thermal result.

### P1 — model strengthening

- [x] axial diffusion + distributed lateral vapor renewal;
- [x] low-order open-valley heat/vapor/wet-wall coupling;
- [ ] add an explicit liquid-feed-limited solution rather than only a supply-limit flag;
- [ ] constrain heat/mass exchange coupling using physically plausible Lewis/Chilton-Colburn-style relations rather than arbitrary independent exchange distances;
- [ ] predict lateral exchange from geometry-resolved 2-D/3-D natural convection/cross-flow;
- [ ] re-test lumped-model multi-equilibrium behavior under improved external-flow treatment;
- [ ] sensitivity to Nu/Sh, compression, opening losses and external drift.

### P2 — physical evidence

- [ ] E1 B0 vs B4;
- [ ] E2 ablation;
- [ ] E3/E3b;
- [ ] E3c D1/O1/O2a/O2b/O3;
- [ ] E4 humidity boundary;
- [ ] E6 hot-ambient shielding / sensible-heat penalty;
- [ ] publish raw data, calibration metadata, uncertainty and negative results.

### P3 — stable publication

- [ ] authoritative patent-family/claim verification;
- [ ] freeze one exact technical-disclosure commit;
- [ ] regenerate reference artifacts and SHA-256 at that commit;
- [ ] update `CITATION.cff` / version / release notes;
- [ ] create stable tag/release;
- [ ] create persistent public archive/DOI without overwriting earlier records.

## H. Audit rules

Every significant result must answer:

1. measurement, simulation, analytic screen, inference, or hypothesis?
2. reproducible from code/data?
3. does it supersede an earlier conclusion?
4. is the broad mechanism already prior art?
5. are nonlinear branch choices explicit?
6. is geometric area being confused with accessible area?
7. is vapor transfer being reused as sensible heat transfer?
8. is axial Péclet number being confused with vapor renewal?
9. is a covered-channel result being generalized to an open valley?
10. is centimeter-scale segmentation assumed useful without comparison to exchange length?
11. is high `F` being confused with high evaporation capacity?
12. is positive evaporation being confused with positive body cooling?
13. does predicted evaporation exceed available liquid feed?
14. is any large inferred `R` reported more precisely than T/RH uncertainty supports?

If any answer is unclear, keep the item open.
