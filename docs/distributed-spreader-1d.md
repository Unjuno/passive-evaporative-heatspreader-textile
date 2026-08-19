# Distributed direct-material spreader model

Status: **SIMULATION / 1-D BRIDGE MODEL — NO PHYSICAL SPECIMEN**

## Purpose

The earlier asymmetric wet/dry model represented lateral heat routing with one scalar coupling `g_mix`. This model replaces that abstraction with direct material inputs:

- in-plane conductivity `k_parallel`;
- effective conductive thickness `t`;
- repeating wet/dry routing pitch `P`;
- local spreader-to-outer thermal contact `h_contact`;
- wet-side open-valley sensible/vapor exchange;
- dry-side sensible exposure `h_dry`;
- continuous wet-stripe width solved from liquid feed.

VP-A through VP-D are used as regression anchors.

## Governing spreader equation

For a periodic 1-D sheet:

\[
\frac{d}{dx}\left(k_{\parallel}t\frac{dT_s}{dx}\right)
+U_b(T_{skin}-T_s)
+h_c(T_o-T_s)=0.
\]

### Variables

| symbol | meaning | SI unit | assumption |
|---|---|---:|---|
| `T_s` | spreader temperature | K or °C difference-compatible | periodic 1-D field |
| `T_o` | outer-layer temperature | K or °C | local field |
| `k_parallel` | in-plane conductivity | W/(m K) | scalar in v0.1 |
| `t` | effective conductive thickness | m | VP-C coverage is homogenized into `t` |
| `U_b` | body-to-spreader coupling | W/(m² K) | low-order constant |
| `h_c` | spreader-to-outer contact | W/(m² K) | lumped local contact |
| `P` | repeating wet/dry pitch | m | periodic cell |

Dimensional check:

\[
[k t T'' ]
=\frac{W}{mK}m\frac{K}{m^2}
=\frac{W}{m^2},
\]

matching all other areal heat-flux terms.

## Outer local balance

A cell can have wet sub-area weight `w(x)` between 0 and 1. Boundary cells are allowed to be fractionally wet so wet width is continuous rather than quantized by the numerical grid.

\[
h_c(T_s-T_o)
+h_{amb}(w)(T_\infty-T_o)
-L_v w k_m[\rho_{v,sat}(T_o)-\rho_{v,\infty}]_+
=0.
\]

with

\[
h_{amb}(w)=w h_{wet}+(1-w)h_{dry}.
\]

The total wet width is solved so integrated evaporation matches imposed feed when the exterior has enough transfer capacity.

## Numerical verification

For the 100 g/h VP screen:

- feed closure is better than 0.001 g/h in the checked cases;
- maximum local outer-energy residual is numerically near zero;
- maximum spreader-equation residual is about 0.004 W/m² or less;
- VP-A body flux changes by about 0.01 W/m² between 32 and 96 nodes per period;
- VP-C remains similarly stable once fractional boundary wetness is used.

This is numerical convergence of the low-order equations, not validation against reality.

## VP-A through VP-D at 100 g/h

Equal-feed comparison against an analytic no-lateral-conduction baseline:

| prototype | solved wet fraction | body heat flux | distributed spreader gain over 0.195 m² |
|---|---:|---:|---:|
| VP-A | ~0.444 | ~285 W/m² | ~5.48 W |
| VP-B | ~0.448 | ~284 W/m² | ~5.32 W |
| VP-C | ~0.451 | ~283 W/m² | ~5.30 W |
| VP-D | ~0.447 | ~290 W/m² | ~6.29 W |

The direct-material distributed results remain within roughly 0.8 W of the corresponding scalar-`g_mix` virtual-anchor gains. This is useful continuity, not independent validation, because the two model families share exterior and body-coupling assumptions.

## Interpretation

The distributed model retains the main v0.1 conclusions:

1. short routing pitch remains favorable;
2. VP-B's 20 mm path underperforms VP-A despite greater thickness/mass;
3. VP-D's stronger dry-side shielding increases the value of the same short-pitch spreader;
4. VP-C remains competitive under a homogenized high-`k/rho` effective sheet;
5. the absolute mechanism gain remains in a finite few-watt range over 0.195 m² rather than increasing indefinitely with conductivity.

## Important limitation: VP-C coverage

VP-C's 50% conductive coverage is represented here as an **effective uniform thickness** equal to physical thickness × coverage. This preserves average `k*t` but does not resolve trace spacing, path tortuosity, dead zones, or local contact loss.

Therefore the next model must resolve actual routed-network topology rather than assuming coverage can be homogenized perfectly.

## Next extension

Move from 1-D periodic scalar `k` to a 2-D field with:

- anisotropic `k_x`, `k_y`;
- explicit routed traces / sparse coverage geometry;
- spatially varying contact resistance;
- wet islands / valley geometry;
- dry shielding map;
- garment curvature/compression sensitivity.

This model is intentionally a bridge between the two-node mechanism screen and that future geometry-resolved virtual garment model.
