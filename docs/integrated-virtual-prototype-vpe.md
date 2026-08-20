# Integrated virtual prototype VP-E

Status: **VIRTUAL / COMPUTATIONAL PROTOTYPE ONLY — NO PHYSICAL GARMENT**

VP-E freezes one internally consistent design anchor so future model changes can be compared against the same architecture instead of moving all assumptions simultaneously.

## VP-E architecture

### Heat network

- directed routing with limited cross-link redundancy;
- current score-blend anchor: approximately `lambda=0.125`;
- ~35% high-`k` route material fraction in the regional tile.

### Wet-terminal geography

- regularized pressure-aware layout;
- pressure-avoidance term + distributed four-island regularization + route-overlap term;
- current coefficients: template `beta=0.125`, route weight `0.35`;
- ~23% active wet-terminal area in the regional screen.

### Liquid network

- 8 local collection/terminal cells for a 150 g/h total reference flow;
- 18.75 g/h per cell;
- nominal transport trunk equivalent radius: 200 µm;
- trunk path: 30 mm;
- vertical rise: 15 mm;
- 30% blocked-channel design reserve;
- short fine-pore collector/micro-wick remains upstream of the larger trunk.

### Environmental state

The terminal is allowed an ideal numerical endpoint state:

- `open`: ordinary wet-side ambient heat/vapor exchange;
- `shield`: wet-side exchange closed in the low-order model.

The selected state maximizes signed body-side heat flow. No actuator is included; this is an upper-level control rule used to test whether an environmental open/shield mechanism is worth retaining as an embodiment.

### Garment BOM

VP-E uses the nominal pressure-relocation BOM:

- dry mass: ~168.7 g;
- operating liquid hold-up: ~12.4 g;
- operating mass: ~181.1 g;
- added dry functional mass above base shell: ~60.0 g;
- dry functional peak stack: ~1.9 mm;
- wet-terminal peak additive stack: ~4.1 mm.

These values are design-budget assumptions, not measured garment specifications.

## Environment map

Converged 20 x 20 reference outputs:

| ambient | open body flux | shield body flux | selected state | selected body flux | open vapor-capacity index |
|---|---:|---:|---|---:|---:|
| 35 °C / 50% RH | ~111.0 W/m² | ~-2.0 | open | ~111.0 | ~205 g/(m² h) |
| 35 °C / 70% RH | ~58.6 | ~-2.0 | open | ~58.6 | ~113 |
| 35 °C / 85% RH | ~20.4 | ~-2.0 | open | ~20.4 | ~46 |
| 40 °C / 50% RH | ~50.1 | ~-12.2 | open | ~50.1 | ~153 |
| 40 °C / 70% RH | ~-15.2 | **~-12.2** | shield | **~-12.2** | ~39 |
| 40 °C / 85% RH | ~-37.2 | **~-12.2** | shield | **~-12.2** | 0 |
| 45 °C / 30% RH | ~66.5 | ~-22.4 | open | ~66.5 | ~236 |
| 45 °C / 50% RH | ~-17.8 | ~-22.4 | open | ~-17.8 | ~89 |

The selected state can still have negative body-side heat flow. The open/shield rule reduces modeled harm; it does not make every hot/humid environment cooling-positive.

## Liquid robustness margin

For the 8-cell, 200 µm nominal trunk geometry:

| retained equivalent radius | live channels/cell | installed channels/cell with 30% blockage reserve | total installed channels |
|---:|---:|---:|---:|
| 100% | 2 | 3 | 24 |
| 90% | 2 | 3 | 24 |
| 80% | 3 | 5 | 40 |
| 70% | 4 | 6 | 48 |

This is an ideal circular-channel screen. It does not specify a manufacturable textile channel count.

## What VP-E demonstrates

VP-E is useful because it combines the previously separate conclusions without claiming physical validation:

1. **mass** — the nominal relocation architecture is not automatically ruled out by the current BOM;
2. **thickness** — relocation remains under the internal 5 mm terminal-stack gate, unlike the nominal protected-under-load stack;
3. **pressure geography** — terminals are distributed away from persistent loads rather than clustered only at the absolute lowest pressure;
4. **heat routes** — short directed routes with limited redundancy remain the anchor;
5. **liquid routes** — distributed local transport and protected escape sections are preferred;
6. **environment** — terminal exposure changes sign/value with hot/humid conditions.

## Internal engineering gates

The following are project-specific screening gates, not standards:

- operating mass <= 220 g;
- added dry functional mass <= 80 g;
- wet-terminal local stack <= 5 mm;
- 35 °C / 70% RH selected body-side heat flow > 0;
- 40 °C / 70% RH: environmental shield state must be no worse than open state;
- 8-cell liquid network must retain a finite design channel count at 80% equivalent-radius retention plus 30% blocked-channel reserve.

VP-E passes these numerical gates under the current assumptions. Passing does not predict real-garment performance.

## Main failure still exposed by VP-E

The integrated prototype remains body-heating in the current 40 °C / 70–85% RH screen even after closing the wet terminal. This points to the next high-value problem:

> dry-side hostile-ambient shielding / isolation must be designed together with the environmental terminal state.

The current dry shield is represented in the BOM and qualitative architecture, but its thermal switching/isolation behavior is not yet resolved in VP-E.

## Next VP-E revisions

- VP-E2: explicit dry-side environmental shielding conductance;
- replace nearest-route proxies with one solved heat + hydraulic regional network;
- assign capillary trunk wall/porous-matrix mass rather than an areal allowance;
- include curvature and seams;
- resolve protected vapor-gap geometry where load avoidance is impossible;
- add local salt-wall deposition without any salt vapor flux.
