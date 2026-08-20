# Capillary trunk radius-collapse sensitivity

Status: **SIMULATION / PARAMETRIC SCREEN ONLY — NO PHYSICAL SPECIMEN**

## Question

How sensitive is the distributed liquid network to partial collapse of an equivalent hydraulic trunk radius under bending or garment pressure?

This screen does **not** predict pressure-to-deformation mechanics. Instead it directly prescribes the retained hydraulic radius and recomputes the capillary/viscous burden.

## Why radius matters

Ideal circular-channel viscous resistance scales as

\[
R_h\propto r^{-4}.
\]

At the same time capillary pressure increases as `1/r`, so the full channel-count penalty is less severe than the pure `r^-4` resistance multiplier but remains strong.

## Reference: 4-local-cell, 200 µm nominal trunk

Per cell:

- 37.5 g/h;
- 50 mm path;
- 25 mm vertical rise;
- safety factor 3;
- nominal equivalent radius 200 µm;
- nominal required live channels: ~7.

| radius retained | effective radius | live channels needed | multiplier vs nominal |
|---:|---:|---:|---:|
| 100% | 200 µm | 7 | 1.00x |
| 90% | 180 | 8 | 1.14x |
| 85% | 170 | 10 | 1.43x |
| 80% | 160 | 11 | 1.57x |
| 75% | 150 | 13 | 1.86x |
| 70% | 140 | 16 | 2.29x |
| 60% | 120 | 23 | 3.29x |
| 50% | 100 | 38 | 5.43x |

## Collapse + blockage redundancy

For the same nominal 200 µm trunk:

- 90% radius retention + 30% blocked-channel design fraction -> ~12 installed channels/cell;
- 80% retention + 30% blockage -> ~16/cell;
- 70% retention + 30% blockage -> ~23/cell.

This is a simple independent lost-channel reserve. Correlated collapse/deposition is not represented.

## Design implication

The current architecture should not place unprotected hydraulic trunks directly in severe garment-pressure regions if the cross-section is easily flattened.

Candidate mitigations include:

- route liquid trunks around persistent pressure zones, analogous to pressure-aware evaporator placement;
- use multiple parallel trunks rather than one critical channel;
- use geometries/material structures that preserve hydraulic cross-section under bending;
- reserve fine compliant pores for short collection distances while using more collapse-resistant transport pathways for longer liquid movement.

The numerical screen strengthens the preference for **distributed local routing**, because local networks can add hydraulic redundancy without creating one garment-scale single point of failure.

## Limits

- circular equivalent radius does not describe flattened noncircular channels exactly;
- capillary pressure after severe noncircular collapse may not follow the simple cylindrical formula;
- no shell/buckling mechanics or actual pressure value is predicted;
- no recovery/hysteresis after unloading;
- no coupling to salt deposition or textile swelling.

## Next work

1. add a geometry-specific collapse law only when a candidate trunk construction is chosen;
2. co-map hydraulic trunks around the same load fields used for wet-terminal placement;
3. test correlated blockage + collapse spatially;
4. include channel wall/porous-matrix mass and thickness in the integrated virtual prototype.
