# Capillary architecture tradeoff: centralized vs distributed routing

Status: **SIMULATION / ANALYTIC SCREENING / VIRTUAL PROTOTYPE ONLY — NO PHYSICAL SPECIMEN**

## Why this follows from the pressure-aware layout work

The pressure-map screen prefers low-pressure wet terminals near loaded regions. The liquid-routing question is therefore whether all sweat should be collected into a central manifold or whether many local collection cells should feed nearby terminals.

The ideal cylindrical-capillary model makes the tradeoff analytically visible.

## Cross-sectional-area objective

For `N` parallel capillaries,

\[
\Delta P_f=\frac{8\mu LQ}{\pi r^4N},
\qquad
\Delta P_c-\Delta P_h=\frac{2\gamma\cos\theta}{r}-\rho g\Delta z.
\]

With a pressure safety factor `S`, the minimum required total channel cross-sectional area is

\[
A_{tot}=N\pi r^2
=\frac{8S\mu LQ}{r(C-Hr)},
\]

where

\[
C=2\gamma\cos\theta,
\qquad
H=\rho g\Delta z.
\]

For positive vertical rise, maximizing `r(C-Hr)` gives

\[
\boxed{r_* = \frac{C}{2H}
=\frac{\gamma\cos\theta}{\rho g\Delta z}}.
\]

The largest radius that can support the same rise statically is `C/H`, so the ideal area-optimal radius is exactly half the static-radius limit.

At zero rise there is no finite optimum in this ideal area objective: larger radius keeps reducing hydraulic burden until another constraint (priming, thickness, leakage, garment geometry, etc.) becomes active.

## Dimensional check

`r_*`:

\[
\frac{N/m}{(kg/m^3)(m/s^2)(m)}
=\frac{N/m}{Pa}=m.
\]

At the positive-rise optimum,

\[
A_{tot,min}
=\frac{8S\mu LQ\rho g\Delta z}{\gamma^2\cos^2\theta},
\]

which has units of area.

## Reference optimum radii

Using the current screening inputs (`gamma=0.070 N/m`, contact angle 30 deg):

| vertical rise | area-optimal equivalent radius |
|---:|---:|
| 25 mm | ~247 µm |
| 50 mm | ~124 µm |
| 100 mm | ~61.8 µm |
| 200 mm | ~30.9 µm |

The optimum depends on capillary head, not directly on flow or route length. Flow and route length scale the required total area/channel count.

## Centralized vs distributed illustration

All architectures below transport the same total 150 g/h, but the local architectures deliberately shorten both hydraulic route and vertical rise.

| architecture | cells | flow/cell | path | rise | ideal discrete total capillary area | liquid inventory |
|---|---:|---:|---:|---:|---:|---:|
| central | 1 | 150 g/h | 200 mm | 100 mm | ~48.0 mm² | ~9.61 mL |
| 4 local | 4 | 37.5 | 50 mm | 25 mm | ~3.01 mm² | ~0.15 mL |
| 8 local | 8 | 18.75 | 30 mm | 15 mm | ~1.34 mm² | ~0.04 mL |
| 12 local | 12 | 12.5 | 25 mm | 10 mm | ~1.21 mm² | ~0.03 mL |

This is **not** a universal 16–40x performance claim. The advantage comes from the explicit geometry change: distribution reduces route length and lift.

## Scaling insight

For positive rise,

\[
A_{tot,min}\propto
\frac{\mu LQ\Delta z}{\gamma^2\cos^2\theta}.
\]

Therefore the highest-leverage liquid-routing choices are:

- reduce vertical lift;
- reduce route length;
- split total flow into nearby local cells when that split allows shorter routes;
- preserve wetting/contact angle and avoid contamination;
- avoid relying on extremely small pores solely for capillary head, because viscous burden grows sharply.

## Current design implication

The pressure-aware architecture should be tiled into local thermal/liquid cells rather than use one garment-scale liquid manifold.

A candidate cell has:

1. local directional sweat collection;
2. short capillary branch(es), preferably tens rather than hundreds of millimeters;
3. limited vertical lift;
4. a low-pressure/open-air wet terminal;
5. a separate short heat-routing network connecting nearby dry/compressed zones to that terminal.

Liquid and heat routing should be co-designed around the same terminal geography, but they need not occupy the same physical channels.

## Important limitations

- ideal cylindrical tubes omit porous-media tortuosity;
- the discrete optimizer allows large channels that may be impractical in a textile;
- zero-rise optimum is unbounded without a maximum-radius/thickness constraint;
- manifolds, branching junction losses and priming are omitted;
- pressure-induced channel collapse is omitted;
- sweat chemistry may change viscosity, surface tension and contact angle;
- salt does not evaporate and must not be concentrated inside permanent narrow channels.

## Next work

1. sensitivity to viscosity/contact angle/surface tension and partial blockage;
2. add explicit maximum channel radius / textile thickness constraints;
3. compare hierarchical porous wick + larger trunk channels;
4. co-optimize liquid paths, heat paths and pressure-aware terminal locations;
5. estimate mass/volume penalty for practical channel wall/porous structures, not liquid volume alone.
