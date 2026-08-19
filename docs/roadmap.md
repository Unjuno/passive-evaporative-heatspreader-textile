# Research Roadmap

Date: 2026-08-19

## Objective

Develop and publicly document a reproducible passive cooling garment architecture based on coupled heat spreading, liquid transport, and exterior evaporation. The roadmap prioritizes falsification of the core cooling premise before optimization for durability, aesthetics, and manufacturability.

## Gate 0 — Scope freeze

Status: **substantially complete**

- [x] Primary architecture is passive and does not require an onboard fan.
- [x] Core elements separated from optional embodiments.
- [x] Exterior design treated as apparel texture rather than exposed machine-like hardware.
- [x] Salt transport corrected: water evaporates; nonvolatile salts do not.
- [ ] Freeze a numbered architecture diagram and layer nomenclature.

## Gate 1 — Prior-art map

Status: **in progress**

Map adjacent work by function rather than by superficial product similarity:

- [x] directional sweat/liquid transport;
- [x] evaporative cooling textiles;
- [x] humidity-responsive garment ventilation;
- [x] heat-conductive/cooling textiles;
- [ ] fan garments and dehumidifying garment patents;
- [ ] 3D-knit/pile/fin evaporative structures;
- [ ] heat-spreader + exterior evaporation combinations;
- [ ] claim-oriented patent landscape.

Deliverable: `docs/prior-art.md` with verified primary-source references and explicit differences.

## Gate 2 — Reproducible master model

Status: **in progress**

- [x] latent heat balance;
- [x] natural-convection screening;
- [x] accessible exchange multiplier `M`;
- [x] rib geometry multiplier;
- [x] whole-body heat-spreader coupling parameter;
- [x] same-water-input comparison rule;
- [ ] consolidate all earlier exploratory models into one versioned package;
- [ ] add uncertainty propagation;
- [ ] add regression tests for known numerical cases;
- [ ] add machine-readable parameter metadata.

## Gate 3 — Minimum bench validation

Status: **not started**

Priority order:

1. B0 flat fast-dry control vs B4 integrated architecture.
2. B0/B2/B3/B4 ablation comparison.
3. Rib pitch sweep to estimate effective surface accessibility.
4. Humidity limit testing at 50/70/85% RH.
5. Heat-spreader orientation test.
6. Dry-side shielding test at hot ambient temperature.

The first physical objective is not a wearable human trial. It is a controlled artificial-skin heat-flow experiment.

## Gate 4 — Mechanical and textile validation

Status: **not started**

- compression recovery;
- bending and stretch;
- wash durability;
- wetting recovery after drying;
- contamination and salt exposure;
- snagging and abrasion;
- visual thickness/silhouette;
- wearer-contact safety.

## Gate 5 — Apparel design optimization

Status: **concept stage**

Compare exterior implementations at similar projected area and material mass:

- micro-rib 3D knit;
- short flexible lamellae;
- low-profile pleats;
- patterned pile;
- mixed-height rib field;
- seam-integrated evaporation structures.

Optimize cooling performance together with appearance, snag resistance, compressibility, washability, and mass.

## Gate 6 — Public versioned releases

Status: **repository initiated**

For stable releases:

- [ ] freeze technical disclosure;
- [ ] freeze source code and input data;
- [ ] generate SHA-256 manifest;
- [ ] create GitHub release/tag;
- [ ] archive the exact release in a persistent public repository/DOI service;
- [ ] never overwrite an older public release; publish experimental additions as later versions.

## Research priorities

### P0 — Does the integrated architecture actually outperform a normal fast-dry textile?

Primary decision metric: artificial-skin heater-power difference at equal sweat input.

### P1 — Is the gain due to integration rather than only one component?

Use B2/B3/B4 ablation.

### P2 — What exterior geometry maximizes effective area rather than geometric area?

Measure the accessible-area parameter indirectly from heat transfer and near-surface humidity.

### P3 — Where does passive operation fail?

Map high-humidity and hot-ambient limits.

### P4 — Can the architecture survive clothing mechanics?

Stretch, compression, washing, abrasion, and repeated wet/dry cycles.

## Stop conditions

The project should be substantially redesigned if controlled tests show all of the following:

- integrated B4 gains less than 5 W over a flat control under the primary condition;
- exterior geometric area increases without measurable improvement in effective mass transfer;
- heat spreading adds mass/stiffness without measurable body-side cooling benefit;
- passive high-humidity operation provides no useful advantage within wearable geometry.

Negative results remain part of the technical record.
