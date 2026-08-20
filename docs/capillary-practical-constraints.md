# Practical capillary constraints and two-scale liquid network

Status: **SIMULATION / ANALYTIC SCREENING / VIRTUAL PROTOTYPE ONLY — NO PHYSICAL SPECIMEN**

## Why add a radius constraint?

The ideal area optimum can select capillaries that are too large for a low-profile textile. This screen adds a maximum equivalent trunk radius and separates short-range liquid capture from longer-range transport.

## Radius-cap penalty

Reference local cell:

- 37.5 g/h per cell (4 cells carrying 150 g/h total);
- 50 mm trunk path;
- 25 mm vertical rise;
- pressure safety factor 3.

The unconstrained ideal discrete optimum is near 244 µm equivalent radius. Imposing a maximum radius gives approximately:

| radius cap | selected radius | channels/cell | cross-section/cell | penalty vs unconstrained |
|---:|---:|---:|---:|---:|
| 75 µm | ~75 µm | ~83 | ~1.46 mm² | ~1.95x |
| 100 µm | ~99 µm | ~38 | ~1.17 mm² | ~1.56x |
| 150 µm | ~148 µm | ~13 | ~0.90 mm² | ~1.19x |
| 200 µm | ~190 µm | ~7 | ~0.79 mm² | ~1.06x |
| 300 µm | ~244 µm | ~4 | ~0.75 mm² | ~1.00x |

Thus the local/distributed architecture remains hydraulically attractive even when the ideal trunk radius is capped around 150–200 µm in this idealized model.

## Two-scale liquid network

The current architecture should not demand the same pore size for capture and transport.

### Micro-wick role

- 20–50 µm equivalent radius class;
- only a few millimeters long;
- provides wetting/collection and high capillary pressure;
- should be protected from direct evaporation where salt precipitation could block permanent pores.

### Transport-trunk role

- roughly 100–300 µm equivalent hydraulic radius in the current screen;
- carries most of the long-distance flow with much lower viscous resistance;
- remains liquid filled;
- terminates in an accessible outer evaporator.

A Pareto screen over micro-wick length/radius, trunk radius and number of local cells favors many short local cells. One representative low-area point uses 12 cells, 50 µm / 2 mm micro collection and ~200 µm / 25 mm trunks, with a total ideal micro+trunk cross-section proxy of roughly 1.9 mm² and liquid inventory of roughly 0.04 mL.

This is not a manufacturable geometry claim; wall volume and porous matrix are excluded.

## Blockage redundancy

If `N_live` channels are required after blockage and a design blockage fraction is `b`, the installed count screen is

\[
N_{installed}\ge \frac{N_{live}}{1-b}.
\]

Examples:

- 4 local cells, 200 µm trunk, ~7 live channels/cell: 30% blockage requires ~10 installed channels/cell; 50% requires ~14;
- 8 local cells, 200 µm trunk, ~2 live channels/cell: 30% blockage requires ~3 installed channels/cell;
- 12 local cells, 150 µm trunk, ~2 live channels/cell: 30% blockage requires ~3 installed channels/cell.

The independence/uniform-blockage assumption is simplistic; correlated salt or compression blockage is a harder future case.

## Design implication

The current preferred liquid architecture is hierarchical and distributed:

> local skin-side collector wick -> short protected micro-wick -> larger low-resistance liquid trunk -> nearby pressure-aware wet terminal.

Do not use the terminal evaporating microtexture itself as the only garment-scale transport pore network.

## Salt constraint

Water evaporates only at the accessible exterior terminal. Sweat salts remain in liquid/solid phases. Permanent internal microchannels should therefore be shielded from evaporation as far as practical; otherwise concentration and crystallization can increase hydraulic resistance or block the route.

## Uncertainty

- ideal tube resistance, not measured textile permeability;
- no branch-junction losses;
- no channel wall/material thickness;
- no dry-start priming time;
- no pressure-collapse mechanics;
- no dynamic changes in viscosity/contact angle from sweat composition;
- blockage is represented as loss of entire channels rather than progressive pore narrowing.

## Next work

1. chemistry/wetting sensitivity;
2. distributed partial blockage and salt-concentration leakage model;
3. pressure-collapse screen for trunks under garment loads;
4. co-design terminal locations with heat and liquid route cost;
5. full virtual garment mass and thickness accounting.
