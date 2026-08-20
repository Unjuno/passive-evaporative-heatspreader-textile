# Protected under-load evaporator: support-skeleton frontier

Status: **SIMULATION / VIRTUAL PROTOTYPE ONLY — NO PHYSICAL SPECIMEN**

## Question

A protected vapor gap needs load-bearing ribs, arches, spacers or bridges. Those structures can preserve air access under a backpack/seat load, but they also consume active evaporating area.

This screen adds that area penalty to the protected-air-channel model.

## Setup

- synthetic backpack + shoulder-strap pressure map;
- loaded center-panel evaporator footprint;
- same routed high-`k` network as the pressure-map screen;
- 35 °C / 50% RH;
- `cmax=0.5`, air-closure exponent `n=2`;
- support cells are removed from the active wet area;
- load-bearing support follows a deterministic grid-rib score;
- wet-side vapor access is bounded below by a protected-air floor `s_min`.

The support geometry is a topology screen, not a structural mechanics model.

## Key result

Pressure-aware relocation gives the comparison target of about **112.76 W/m²** body-side heat flux in the converged 24 x 24 reference.

With **no support-area penalty**, a center panel with `s_min=0.85` slightly exceeds that target (~114.0 W/m²).

Once support area is charged against the active wet footprint, the feasible design space becomes narrow:

| protected wet-side air floor | maximum screened support fraction that still matches relocation |
|---:|---:|
| 0.80 | none |
| 0.85 | ~0% |
| 0.90 | ~2.5% |
| 0.95 | ~7.5% |
| 1.00 | ~10% |

At `s_min=0.85`, even the first 5% support-area case falls below the relocation reference in this screen.

## Design implication

The current model therefore disfavors a coarse load-bearing lattice covering a large fraction of the wet terminal. A protected under-load evaporator is more plausible if load is carried by:

- narrow ribs;
- point or perimeter supports;
- arches/bridges that leave most wet area exposed;
- spacer structures whose load-bearing footprint is small relative to the open vapor area.

The supported design rule is:

> preserve vapor gap height with minimal support-area occupation; do not treat "protected air channel" as free area.

## Comparison with pressure-aware relocation

Two implementation families remain viable:

### Relocation

- move wet terminals away from persistent load zones;
- use short heat routes from loaded dry regions to low-pressure evaporators;
- little need for structural vapor-gap supports under the load.

### Protected under-load terminal

- retain wet terminal under load;
- preserve near-uncompressed vapor access;
- use low-area-fraction support skeletons;
- accept added structural thickness/material complexity.

The current numerical screen makes relocation the simpler default unless the protected structure can maintain very high air access with very low support footprint.

## Uncertainty

- no explicit rib bending/buckling/contact mechanics;
- support fraction is not yet converted to rib width, height, modulus or pressure rating;
- no geometry-resolved air flow through the support skeleton;
- active liquid supply around support elements is not solved;
- wetting and salt deposition around support contact points are omitted.

## Next work

1. map support area fraction to explicit rib width/spacing/height;
2. solve rib compression/buckling as a separate structural screen;
3. couple protected gap geometry to vapor-transfer conductance;
4. compare mass/thickness of protected skeleton against extra heat-routing mass for relocation.
