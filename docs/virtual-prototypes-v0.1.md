# Virtual prototypes v0.1

Status: **SIMULATION / VIRTUAL PROTOTYPE ONLY — NO PHYSICAL SPECIMEN**

## Purpose

Replace an abstract garment concept with several concrete, reproducible parameter combinations. These cases are not product claims. They are design anchors for subsequent model refinement and defensive technical disclosure.

All four cases use the current asymmetric wet/dry mechanism model at 35 °C / 50% RH to isolate spreader value under partial wetness. Their reported `spreader_gain` is the difference relative to the same wet/dry boundary conditions with `g_mix=0`; it is **not** the total garment-vs-control cooling gain.

## Shared model assumptions

- structured wet/dry area: 0.195 m² (`0.30 × 0.65`);
- spreader mass normalized over 0.30 m²;
- wet open-valley side uses the current low-order 6 × 3 mm / 0.5 mm exchange screen;
- body-side coupling: current mechanism default;
- periodic-stripe topology mapping uses `Gamma=4` nominally;
- effective spreader conductance includes two identical thermal contacts in series;
- no physical material is named; `k` and density are explicit screening properties.

## VP-A — short-pitch baseline

- routing pitch: 10 mm;
- `k_parallel = 100 W/(m K)`;
- density: `1600 kg/m³`;
- conductive thickness: 100 µm;
- coverage: 100%;
- each-side contact conductance: `2000 W/(m² K)`;
- dry-side ambient sensible coefficient: `5 W/(m² K)`.

Nominal result:

- sheet-only `g_sheet ≈ 400 W/(m² K)`;
- contact-limited effective `g_eff ≈ 286 W/(m² K)`;
- spreader mass ≈48 g over 0.30 m²;
- outer-fiber strain at 10 mm bend radius ≈0.5%;
- modeled spreader mechanism gain at 100 g/h ≈5.3 W over 0.195 m².

## VP-B — 20 mm simpler routing

Same property class as VP-A, but:

- routing pitch: 20 mm;
- thickness: 200 µm.

Nominal result:

- `g_sheet ≈ 200 W/(m² K)`;
- `g_eff ≈ 167 W/(m² K)`;
- mass ≈96 g;
- bend strain at 10 mm radius ≈1.0%;
- modeled spreader mechanism gain at 100 g/h ≈4.9 W.

Interpretation: doubling routing pitch creates a large `P²` penalty. Doubling thickness does not recover the short-pitch conductance and doubles mass.

## VP-C — sparse high-`k/rho` routed case

- routing pitch: 15 mm;
- `k_parallel = 300 W/(m K)`;
- density: `1800 kg/m³`;
- thickness: 100 µm;
- coverage: 50%;
- contact: `1500 W/(m² K)`;
- dry-side sensible coefficient: `5 W/(m² K)`.

Nominal result:

- `g_sheet ≈ 267 W/(m² K)`;
- `g_eff ≈ 197 W/(m² K)`;
- mass ≈27 g;
- modeled spreader mechanism gain at 100 g/h ≈5.0 W.

Important interpretation: this case is lighter than VP-A **because it changes material `k/rho`, pitch and coverage together**. It is not evidence that sparse coverage alone reduces required mass.

## VP-D — short pitch with stronger dry-side shielding

Same spreader geometry as VP-A, but dry-side ambient sensible coefficient is reduced to `2 W/(m² K)`.

Nominal result:

- same `g_sheet ≈400 W/(m² K)` and `g_eff ≈286 W/(m² K)`;
- same ≈48 g spreader mass;
- modeled spreader mechanism gain at 100 g/h ≈6.1 W.

This is the strongest current mechanism result because dry/wet boundary asymmetry gives lateral routing a useful external sink/source contrast.

## Feed sensitivity

Modeled spreader mechanism gain over 0.195 m²:

| feed | VP-A | VP-B | VP-C | VP-D |
|---:|---:|---:|---:|---:|
| 50 g/h | ~4.2 W | ~4.0 W | ~4.1 W | ~4.9 W |
| 75 g/h | ~5.1 W | ~4.8 W | ~4.9 W | ~5.9 W |
| 100 g/h | ~5.3 W | ~4.9 W | ~5.0 W | ~6.1 W |
| 150 g/h | ~3.2 W | ~3.0 W | ~3.1 W | ~3.6 W |

The benefit peaks at intermediate feed in this partial-wetness mechanism model and declines as the wet fraction approaches broader coverage.

## Topology/contact robustness at 100 g/h

The screen perturbs:

- topology factor `Gamma = 2, 3, 4`;
- each-side contact conductance = 500, 1000, 2000, 5000 W/(m² K).

Resulting spreader-gain ranges:

| prototype | min | median | max |
|---|---:|---:|---:|
| VP-A | ~4.4 W | ~5.0 W | ~5.4 W |
| VP-B | ~3.9 W | ~4.5 W | ~5.0 W |
| VP-C | ~4.1 W | ~4.7 W | ~5.2 W |
| VP-D | ~5.1 W | ~5.7 W | ~6.2 W |

These ranges are deterministic model-form sensitivity, not probabilities.

## Current selection

### Preferred performance anchor: VP-D

Reason: strongest modeled routing gain at the same spreader mass as VP-A, demonstrating that dry-side thermal protection and heat spreading are complementary.

### Preferred lightweight anchor: VP-C

Reason: low modeled mass while retaining a similar mechanism gain, but it relies on a higher `k/rho` property class and must therefore be treated as a different material/design family rather than a coverage trick.

### Negative/manufacturability comparison: VP-B

Reason: illustrates the quadratic routing-distance penalty and provides a useful comparison if larger panel pitch is much easier to fabricate.

## Next virtual-prototype upgrade

The next model should remove the single `g_mix` coupling and solve the spreader spatially with:

- direct `k_parallel` / anisotropy;
- thickness field;
- wet/dry patch geometry;
- thermal contacts;
- dry shielding;
- actual routing distance;
- distributed body coupling;
- distributed evaporative sink strength.

VP-A through VP-D should be preserved as regression cases so the distributed model can show when and why it departs from the two-node approximation.
