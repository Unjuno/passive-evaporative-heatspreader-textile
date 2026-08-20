# Explicit branched liquid resistor network

Status: virtual/computational screening only. No physical specimen exists and no measured textile permeability or cooling claim is made.

## Why this model was added

The earlier terminal co-design used a geometric/hydraulic proxy

\[
J_h=d_{95}\hat r^{-4}
\]

and showed that a mildly regularized terminal pattern shortened geometric routes by about 16.8% at a ~1.8% thermal penalty.

That proxy did **not** include distributed flow splitting. This model replaces the distance-only pressure argument with an explicit 2-D resistor network: distributed source flow is injected at non-terminal grid nodes and drains through many terminal nodes. Hydraulic conductance is based on Poiseuille scaling for circular-equivalent trunks.

## Governing edge law

For one liquid trunk edge,

\[
Q_e = G_e\Delta p_e,
\qquad
G_e=\frac{\pi r_e^4}{8\mu L_e}.
\]

The nodal network solves

\[
\sum_j G_{ij}(p_i-p_j)=\dot V_i
\]

for every non-terminal node, while wet-terminal nodes are assigned zero reference pressure.

Pressure-linked radius retention is

\[
r_e=r_0\max\left(r_{min},1-s_c c_e\right),
\]

where `c_e` is local normalized compression and `s_c` is a collapse-severity factor.

Collector capillary drive is screened as

\[
\Delta p_{drive}
=\frac{2\gamma\cos\theta}{r_c}-\rho g\Delta z.
\]

## Variable table

| Symbol | Meaning | SI unit | Current reference | Type |
|---|---|---:|---:|---|
| `Q_e` | trunk edge volumetric flow | m³/s | solved | output |
| `G_e` | edge hydraulic conductance | m³/(s·Pa) | Poiseuille | derived |
| `r_e` | effective trunk radius | m | nominal 200 µm before compression | design input |
| `L_e` | edge length | m | 2.5 mm at 24 x 24 / 60 mm tile | geometry |
| `mu` | liquid viscosity | Pa·s | 0.9 mPa·s | screening input |
| `r_c` | fine collector radius producing capillary drive | m | 50 µm | screening input |
| `Delta z` | vertical lift | m | 15 mm | screening input |
| `Delta p_drive` | available capillary drive | Pa | ~2278 Pa | derived |
| `s_c` | pressure-to-radius collapse severity | 1 | 0 to 1 | sensitivity parameter |

Dimensional check:

\[
[G_e\Delta p]
=\frac{\mathrm{m^3}}{\mathrm{s\,Pa}}\mathrm{Pa}
=\mathrm{m^3/s},
\]

which matches volumetric flow.

## 24 x 24 local-cell reference

A 60 mm square tile is assigned flow proportional to a 150 g/h total feed over 0.30 m² active garment area:

\[
\dot m_{tile}=150\,\frac{0.06^2}{0.30}\approx1.8\ \mathrm{g/h}.
\]

With nominal 200 µm trunks, minimum radius retention 0.70, and the strongest screened pressure-collapse map (`s_c=1`):

| terminal layout | maximum network pressure drop | capillary-drive / pressure margin |
|---|---:|---:|
| thermal-only pressure-aware | ~0.526 Pa | ~4330 |
| regularized terminal layout | ~0.470 Pa | ~4850 |
| four-island layout | ~0.205 Pa | ~11100 |

The collector drive is ~2278 Pa. Every tested layout therefore exceeds a safety-factor-3 pressure margin by orders of magnitude in this **dense local-network** embodiment.

Using the `r^-4` scaling, the single-network safety-factor-3 boundary occurs only around:

- thermal-only layout: ~32.5 µm nominal trunk radius;
- regularized layout: ~31.6 µm;
- four-island layout: ~25.6 µm.

For 50–200 µm-class local trunks, hydraulic pressure drop is therefore **not currently the binding reason** to sacrifice thermal performance.

## Correction to the earlier pressure/liquid proxy interpretation

The earlier `d95 r^-4` result remains useful as a relative geometric route index, but the explicit branched-flow solve shows that it should not be treated as evidence that the 16.8% shorter route materially improves capillary feasibility for the current 50–200 µm distributed-trunk concept.

Accordingly:

- the regularized terminal layout is retained as an optional geometry/manufacturing Pareto alternative;
- it is **not** promoted over the pure thermal pressure-aware layout solely on hydraulic-pressure grounds;
- VP-E terminal selection remains open until sparse trunk density, solid channel mass, seam/curvature constraints, and actual source localization are included.

This is a substantive correction, not a numerical failure.

## Why the result does not eliminate hydraulic design concerns

The reference network is dense: a 24 x 24 square grid contains 1104 trunk edges and about 2.76 m total edge length per 60 mm tile. At 200 µm radius the liquid volume of those ideal trunks is about 0.35 mL per tile. Real construction also has wall/material mass, finite routing coverage, junction losses, non-circular pores and correlated collapse.

Therefore the next useful hydraulic variable is **network sparsity/material burden**, not raw capillary pressure in a fully connected grid.

## H / T / D / C / U

### H

For short distributed 50–200 µm-class trunks at tile-scaled flow, explicit flow branching yields pressure losses far below available fine-pore collector capillary drive, so terminal geometric distance is not a first-order capillary-head constraint.

### T

- 60 mm tile;
- distributed source injection equivalent to 150 g/h over 0.30 m²;
- 24 x 24 orthogonal trunk grid;
- 200 µm nominal trunk radius;
- 50 µm collector radius;
- 15 mm lift;
- pressure-linked radius retention down to 0.70;
- terminal layouts compared at equal wet fraction.

### D

PASS if the worst tested layout at maximum collapse retains capillary pressure margin >3. The current reference margin is >4000.

### C

Alternative explanation / failure modes:

- the fully connected grid is much denser than a practical textile network;
- source flow may be spatially concentrated rather than uniform;
- real porous channels can have much smaller effective hydraulic radius;
- junction/contact losses are omitted;
- wetting hysteresis and multiphase air entrapment are omitted;
- compression may close channels completely rather than smoothly reduce radius.

### U

The dominant uncertainty is model form and network density. Numerical linear-solver error is small compared with uncertainty in effective hydraulic radius, source localization, pore connectivity and pressure deformation.

## Salt conservation

Salt remains nonvolatile:

\[
J_{salt,vapor}=0.
\]

This hydraulic network transports salt only with liquid. It does not include precipitation; buried-channel evaporation remains excluded from the preferred architecture.

## Reproducibility

- `simulations/branched_liquid_resistor_network.py`
- `tests/test_branched_liquid_resistor_network.py`
- `data/branched_liquid_resistor_reference.csv`
