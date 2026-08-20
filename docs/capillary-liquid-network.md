# Passive capillary liquid-routing screen

Status: **SIMULATION / ANALYTIC SCREENING / VIRTUAL PROTOTYPE ONLY — NO PHYSICAL SPECIMEN**

## Question

Can sweat-like liquid be transported passively from collection regions to pressure-aware / ambient-open evaporator terminals without a pump?

This screen uses ideal parallel cylindrical capillaries. Real yarn bundles, porous textiles and grooves will have different hydraulic resistance, contact angle hysteresis, tortuosity and saturation behavior. The model is therefore a burden/feasibility screen rather than a validated textile flow law.

## Governing screen

Viscous pressure drop for `N` identical parallel cylindrical channels:

\[
\Delta P_f=\frac{8\mu LQ}{\pi r^4N}.
\]

Capillary pressure:

\[
\Delta P_c=\frac{2\gamma\cos\theta}{r}.
\]

Hydrostatic penalty:

\[
\Delta P_h=\rho g\Delta z.
\]

The design condition is

\[
\Delta P_c-\Delta P_h\ge S\Delta P_f,
\]

with `S=3` in the current reference screen.

## Variables

| symbol | meaning | SI unit | current reference assumption |
|---|---|---:|---|
| `mu` | liquid dynamic viscosity | Pa s | 0.9e-3 |
| `gamma` | surface tension | N/m | 0.070 |
| `theta` | liquid/solid contact angle | rad or deg | 30 deg |
| `rho` | liquid density | kg/m³ | 1000 |
| `L` | hydraulic route length | m | swept |
| `r` | equivalent capillary radius | m | swept |
| `N` | parallel channels | 1 | solved |
| `Delta z` | vertical rise | m | swept |
| `S` | pressure safety factor | 1 | 3 |

Dimensional check:

\[
\mu LQ/r^4=(Pa\,s)(m)(m^3/s)/m^4=Pa,
\]

so the viscous, capillary and hydrostatic terms are all pressures.

## Main tradeoff

The capillary pressure scales as `1/r`, while Poiseuille resistance scales as `1/r^4`.

Therefore:

- larger channels strongly reduce viscous resistance;
- but larger channels lose capillary head and become poor at vertical lift;
- smaller channels preserve lift but need many parallel paths for garment-scale flow.

### Static capillary-rise upper bound

Before reserving any pressure for flow, the current reference inputs give approximate static rise limits:

| radius | rise limit |
|---:|---:|
| 20 µm | ~618 mm |
| 30 µm | ~412 mm |
| 50 µm | ~247 mm |
| 75 µm | ~165 mm |
| 100 µm | ~124 mm |
| 150 µm | ~82 mm |
| 200 µm | ~62 mm |
| 300 µm | ~41 mm |

These are model-input-dependent upper bounds, not measured textile wick heights.

## 150 g/h reference burden

For a 100 mm route and safety factor 3:

### No vertical rise

- 50 µm radius: ~1891 parallel channels;
- 100 µm: ~237;
- 150 µm: ~71;
- 200 µm: ~30;
- 300 µm: ~9.

### 50 mm vertical rise

- 50 µm: ~2370 channels;
- 100 µm: ~397;
- 150 µm: ~178;
- 200 µm: ~155;
- 300 µm: impossible because hydrostatic head exceeds capillary pressure.

### 100 mm vertical rise

- 50 µm: ~3174;
- 75 µm: ~1424;
- 100 µm: ~1237;
- 150 µm and larger: no positive capillary-pressure margin in the current screen.

## Local-routing examples

Short, nearly lateral routes are much more favorable. At 150 g/h total flow:

- 20 mm route, zero rise, 300 µm radius: ~2 parallel channels;
- 20 mm route, 25 mm rise, 300 µm: ~5;
- 50 mm route, zero rise, 300 µm: ~5;
- 20 mm route, 25 mm rise, 200 µm: ~10;
- 50 mm route, 25 mm rise, 300 µm: ~12;
- 20 mm route, zero rise, 150 µm: ~15.

The cylindrical-channel liquid inventory of these local examples is small in the ideal model.

## Design conclusion

The current liquid-routing screen reinforces the same architecture selected by the heat/pressure models:

> do not collect garment-scale liquid and lift it a long distance to one evaporator. Use distributed collection and short local capillary routes to nearby wet terminals.

This also reduces the amount of heat routing needed because the evaporator remains close to the source region.

A pressure-aware garment can therefore use many local cells:

1. collect liquid from a local skin-side region;
2. route it tens of millimeters, preferably with little vertical rise;
3. terminate at a low-pressure / ambient-open evaporator island;
4. route heat from nearby compressed/dry regions to the same terminal through a separate high-`k` path.

## Failure modes / missing physics

- ideal circular capillaries omit porous tortuosity and pore-size distributions;
- contact-angle hysteresis and surface contamination are omitted;
- saturation-dependent permeability is omitted;
- channel collapse under bending/pressure is omitted;
- capillary priming and dry-start time are omitted;
- branching/manifold losses are omitted;
- sweat salts and proteins may change wetting/resistance; salt remains nonvolatile;
- liquid must not be allowed to evaporate inside protected permanent microchannels if salt crystallization would block them.

## Next numerical work

1. optimize equivalent radius for a specified route length and vertical rise;
2. compare centralized collection against many local feeder cells at equal total flow;
3. add branching/manifold resistance;
4. co-optimize liquid route length with heat-route length and pressure-aware wet-terminal placement;
5. add channel collapse and partial blockage sensitivity.
