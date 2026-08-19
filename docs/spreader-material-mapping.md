# Heat-spreader material / geometry mapping

Status: **SIMULATION / LOW-ORDER GEOMETRY SCREEN — NO MATERIAL OR GARMENT MEASUREMENT**

## Purpose

The asymmetric wet/dry model uses an effective areal lateral conductance

\[
g_{mix}\quad [\mathrm{W/(m^2 K)}]
\]

between dry and wet regions. This document translates that abstract mechanism parameter into a first-order sheet geometry requirement.

## Periodic-stripe mapping

For a repeating wet/dry stripe pair with two parallel center-to-center heat paths, the screening relation is

\[
g_{sheet}\approx \Gamma\frac{k_{\parallel}t c}{P^2},
\qquad \Gamma=4.
\]

Variables:

| symbol | meaning | SI unit | screen assumption |
|---|---|---:|---|
| `g_sheet` | sheet-only wet/dry lateral conductance per total area | W/(m² K) | two-node equivalent |
| `k_parallel` | in-plane conductivity | W/(m K) | effective property |
| `t` | conductive thickness | m | uniform effective thickness |
| `c` | conductive coverage fraction | 1 | linear-area scaling only |
| `P` | wet/dry routing pitch | m | repeating stripe period |
| `Gamma` | topology factor | 1 | 4 for ideal periodic alternating stripes |

Dimensional check:

\[
\frac{k t}{P^2}
=
\frac{\mathrm{W}}{\mathrm{m K}}\frac{\mathrm m}{\mathrm{m^2}}
=
\mathrm{W/(m^2 K)}.
\]

This mapping is **not** a validated textile correlation. Real topology, finite patch size, contact area, anisotropy, serpentine routing and compression can change `Gamma` and the effective path length.

## Main scaling result

Required heat-routing burden grows as

\[
k t \propto g_{mix} P^2.
\]

Therefore halving routing pitch reduces the required `k*t` by a factor of four.

This makes pattern placement at least as important as pursuing very high conductivity.

## Corrected nonlinear spreader target

A dense sweep of the asymmetric wet/dry mechanism model initially exposed a branch-jump artifact in the unconstrained nonlinear solver. The solver was changed to bounded least squares with explicit balance-residual acceptance and continuation support.

For the representative dry-side shielding screen `h_dry=5 W/(m² K)`, the corrected `g_mix` needed to capture approximately 90% of the high-mixing asymptotic gain is:

| feed over 0.195 m² | `g_mix` for 90% gain |
|---:|---:|
| 30 g/h | ~117 W/(m² K) |
| 50 g/h | ~192 W/(m² K) |
| 75 g/h | ~285 W/(m² K) |
| 100 g/h | ~330 W/(m² K) |
| 150 g/h | ~258 W/(m² K) |

These are mechanism-model targets, not measured garment requirements.

The modeled asymptotic gain is also finite. At `h_dry=5 W/(m² K)`, the high-mixing gain over the 0.195 m² structured area is roughly 3.0, 4.5, 5.7, 6.0 and 3.5 W for 30, 50, 75, 100 and 150 g/h respectively.

## Example material-property mapping

For the 100 g/h / 90%-gain target (`g_mix≈330 W/(m² K)`):

### Abstract `k=100 W/(m K)`, `rho=1600 kg/m³` class

- `P=10 mm`: required full-coverage thickness ≈83 µm; mass over 0.30 m² ≈40 g.
- `P=20 mm`: thickness ≈330 µm; mass ≈159 g.
- `P=30 mm`: thickness ≈743 µm; mass ≈357 g.

### Abstract `k=300 W/(m K)`, `rho=1800 kg/m³` class

- `P=10 mm`: thickness ≈28 µm; mass ≈15 g.
- `P=20 mm`: thickness ≈110 µm; mass ≈59 g.
- `P=30 mm`: thickness ≈248 µm; mass ≈134 g.

The property classes are explicit screening inputs, not claims for named products or measured commercial textiles.

## Coverage correction

Under the simple assumption

\[
g_{sheet}\propto t c,
\]

reducing conductive coverage requires inversely increasing thickness. Therefore the total mass required for a fixed target `g_sheet` is

\[
m=A\rho t c
=
A\rho\frac{g_{sheet}P^2}{\Gamma k},
\]

which is independent of `c` in this idealized model.

So a sparse network does **not** automatically reduce mass. It only improves the mass result if topology changes the path length/topology factor, permits a better material, removes inactive area, or supplies some other non-linear advantage.

The mass figure of merit in this simple limit is therefore

\[
\frac{k}{\rho}.
\]

## Contact-resistance burden

A two-contact series screen is

\[
\frac{1}{g_{eff}}
=
\frac{1}{g_{sheet}}+
\frac{2}{h_c}.
\]

Even for an infinitely conductive sheet,

\[
g_{eff}<\frac{h_c}{2}.
\]

Thus the absolute minimum each-side contact conductance is

\[
h_c>2g_{target}.
\]

For the representative `g_target≈330 W/(m² K)` case, even an ideal sheet requires each interface to exceed roughly 660 W/(m² K). If the sheet itself is only twice the target (`g_sheet≈660 W/(m² K)`), the same screen requires each contact to be about 1320 W/(m² K).

These numbers are **contact-model validation burdens**, not measured textile contact coefficients.

## Design consequence

The current preferred heat-spreader direction is therefore:

1. keep dry-to-wet routing distances short, preferably around the 10–20 mm scale in the next virtual prototypes;
2. use high `k/rho` pathways rather than adding thickness indiscriminately;
3. integrate the spreader so that wet/dry contact resistance does not dominate;
4. retain dry-side shielding because symmetric wet/dry boundary conditions remove most area-integrated spreader benefit in the two-node screen;
5. do not claim a spreader benefit from conductivity alone — the benefit depends on spatially heterogeneous wetting/exposure and actual thermal contacts.

## Next model step

Replace the two-node mapping with a spatially distributed wet/dry field where material `k`, thickness, anisotropy, contact conductance, patch pitch and dry-side shielding enter directly rather than through a single `g_mix` parameter.
