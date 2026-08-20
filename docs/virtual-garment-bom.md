# Virtual garment mass and thickness budget

Status: **VIRTUAL / COMPUTATIONAL DESIGN BUDGET ONLY — NO PHYSICAL GARMENT**

## Purpose

The previous models established mechanism requirements but did not answer a product-level question: can the current architecture remain plausibly shirt-like rather than becoming heavy or locally bulky?

This screen converts the current architecture into an explicit bill of materials (BOM) and peak-stack thickness budget.

All areal masses, densities, thicknesses and water hold-up values below are **design assumptions**, not measured material specifications.

## Geometry used

- total shirt-shell material area: swept by assumption set (0.65–0.90 m²);
- functional active area: 0.30 m²;
- active wet-terminal fraction: 23% of functional area;
- high-`k` route material fraction: 35% of functional area.

The total shell area is intentionally larger than the functional area used in the thermal models.

## Component accounting

The BOM separates:

1. base textile shell;
2. directional skin-side collection layer;
3. high-`k` heat routes;
4. capillary liquid structure;
5. exterior terminal microtexture;
6. heat-route encapsulation/contact layer;
7. dry-side shielding;
8. optional protected-gap support skeleton;
9. operating liquid hold-up.

## Nominal result

### Pressure-relocation architecture

Nominal design assumptions give approximately:

- base textile: 108.8 g;
- directional collection: 13.5 g;
- high-`k` routes: 16.8 g;
- capillary structure allowance: 9.0 g;
- terminal microtexture: 8.3 g;
- heat-route encapsulation: 3.2 g;
- dry-side shield: 9.2 g;
- dry garment mass: **~168.7 g**;
- operating liquid hold-up: **~12.4 g**;
- operating mass: **~181.1 g**;
- added dry functional mass above the base shell: **~60.0 g**.

Peak additive stack proxy:

- dry functional region: ~1.9 mm;
- wet terminal region: **~4.1 mm**.

The stack is an upper-envelope additive proxy. Real knitted/interpenetrating layers may not add linearly.

### Protected-under-load architecture

Using a representative 5% support footprint and 2.5 mm protected gap:

- dry mass: ~171.8 g;
- operating mass: ~184.3 g;
- added dry functional mass: ~63.1 g;
- wet-terminal peak stack: **~6.6 mm**.

The protected structure adds only about 3 g in this nominal mass model but adds about 2.5 mm to local terminal thickness. Thus **local bulk/thickness is currently a stronger penalty than support mass**.

## Broad design-range screen

A deterministic random range screen sampled broad input intervals uniformly. The sampling distribution is **not a probability model for a real garment**; it only maps design-space sensitivity.

5th / median / 95th percentiles of the sampled design space were approximately:

| metric | 5% | median | 95% |
|---|---:|---:|---:|
| dry garment mass | 145 g | 183 g | 227 g |
| operating mass | 159 g | 199 g | 244 g |
| added dry functional mass | 52 g | 71 g | 93 g |
| operating water hold-up | 4.6 g | 15.4 g | 26.4 g |

These are ranges under the chosen design-variable bounds, not confidence intervals.

## Added-mass sensitivity

Spearman rank sensitivity of added dry functional mass in the range screen was dominated by:

1. heat-route thickness;
2. capillary-structure areal mass;
3. directional collection-layer areal mass;
4. dry-side shielding areal mass;
5. high-`k` coverage;
6. terminal-microtexture local areal mass.

The base-shirt mass dominates total garment mass, but it is not an added functional burden.

## Routing pitch appears directly in mass

Using the ideal heat-routing relation

\[
g_{mix}\approx \Gamma\frac{k t c}{P^2},
\]

and route mass

\[
m=A\rho t c,
\]

eliminating `t*c` gives

\[
\boxed{m=\frac{A\rho g_{mix}P^2}{\Gamma k}}.
\]

Therefore at fixed target routing conductance and material `k/rho`, route mass scales as

\[
m\propto P^2.
\]

This converts the previous thermal conclusion into a direct garment-design rule: **keep wet terminals regionally distributed so heat-routing pitch stays short**.

## Variables

| symbol | meaning | SI unit | role |
|---|---|---:|---|
| `A` | functional active area | m² | geometry |
| `A_g` | base garment material area | m² | base-shell mass |
| `f_w` | wet-terminal area fraction | 1 | terminal mass / water hold-up |
| `c` | high-`k` route coverage | 1 | route mass |
| `rho` | route density | kg/m³ | route mass |
| `t` | route thickness | m | route mass / thermal conductance |
| `P` | routing pitch | m | thermal burden |
| `m''` | component areal mass | kg/m² or g/m² | BOM input |
| `delta_w` | equivalent retained-water thickness | m | operating liquid mass |

Dimensional check for route mass:

\[
A\rho t = (m^2)(kg/m^3)(m)=kg.
\]

Water hold-up:

\[
m_w=A_w\rho_w\delta_w,
\]

also has units of kg.

## Internal engineering gates

The following may be useful as **project design gates**, not industry standards:

- operating garment mass <= 220 g;
- added dry functional mass <= 80 g;
- dry functional stack <= 2.5 mm;
- wet-terminal local stack <= 5.0 mm for relocation-type regions;
- operating water hold-up <= 20 g.

Under those internal gates:

- lean relocation passes comfortably;
- nominal relocation passes;
- nominal protected-under-load fails the 5 mm local-thickness gate even though mass remains acceptable;
- conservative cases fail multiple mass/thickness gates.

This strengthens pressure-aware relocation as the default architecture and keeps protected under-load evaporation as a localized optional solution.

## Main design conclusion

The current architecture is **not automatically disqualified by mass** in the nominal virtual BOM. The dominant design risks are instead:

1. local terminal thickness/bulk;
2. heat-route thickness and pitch;
3. capillary structural mass if real porous/trunk structures are much heavier than the current allowance;
4. water hold-up if drainage/evaporation dynamics allow large liquid storage;
5. spacer/protected-gap height in loaded zones.

## Important uncertainty

- no named commercial materials are represented;
- garment area depends strongly on size/cut;
- real multi-layer textiles can share fibers/volume, so additive thickness can overestimate local stack;
- seams, hems, closures and aesthetic panels are not included;
- capillary structure mass is still an areal allowance, not a wall/porous-matrix geometry calculation;
- terminal microtexture mass is not linked to mechanical stiffness yet;
- operating liquid hold-up is an assumed equivalent water thickness, not a transient flow simulation.

## Next work

1. create one integrated virtual prototype (VP-E) with fixed numerical geometry/material assumptions;
2. add actual capillary trunk wall/porous-matrix volume to the BOM;
3. combine hot/humid thermal maps with the same VP-E BOM;
4. add curvature/seam/fit allowances;
5. optimize heat-route pitch and terminal geography against added mass rather than thermal output alone.
