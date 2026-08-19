# Current Numerical Results

Status: **SIMULATION / SCREENING ONLY — NO PHYSICAL GARMENT PERFORMANCE DATA YET**  
Compiled: 2026-08-20

This file summarizes the results that currently affect design decisions. Detailed derivations and historical exploratory results remain in the model-specific documents and code.

## 1. Results currently retained

### 1.1 Whole-garment heat spreading helps most under patchy evaporation

A prior 2-D screen with spatially nonuniform evaporation showed increasing body-side heat routing and reduced temperature nonuniformity as in-plane conductivity increased. The effect was much smaller when the evaporation sink was made spatially uniform.

**Retained conclusion:** use lateral heat spreading primarily to route heat toward spatially active wet zones, not as an isolated cooling mechanism.

### 1.2 Heat-spreader orientation can matter

For the abstract anisotropic screen, orienting the high-conductivity axis toward a localized evaporation band produced more body-side heat routing than rotating the same anisotropy by 90 degrees.

**Retained conclusion:** heat-spreader topology should follow the wet-zone layout.

### 1.3 Dry high-conductivity exterior regions can be harmful in hot ambient air

Earlier hot-ambient screens and the newer coupled open-valley model both show that ambient sensible heat can be conducted/convected toward the body when ambient temperature exceeds the wet surface or skin-side setpoint.

**Retained conclusion:** dry conductive regions require shielding, segmentation, anisotropy, or other routing that limits parasitic inward heat pickup.

### 1.4 Exterior geometric area is not the same as useful evaporative area

The E3 periodic 2-D vapor-diffusion screen shows that nearby wet ribs can share one humid boundary layer.

For `h=2.5 mm`, structured-area fraction `f=0.65`:

| idealized renewal gap above rib tips | p=0.8 mm | p=1.0 mm | p=1.5 mm |
|---:|---:|---:|---:|
| 0.5 mm | 3.785 | 3.548 | 3.098 |
| 1.0 mm | 2.481 | 2.400 | 2.229 |
| 5.0 mm | 1.312 | 1.304 | 1.286 |

Values are whole-area **vapor mass-transfer multipliers**, not cooling wattages.

**Retained conclusion:** microstructure must be paired with an explicit ambient-air/vapor access mechanism.

### 1.5 Sensible heat and vapor transfer must be separated

The repository now uses distinct external quantities:

- `M_h` or equivalent heat-transfer treatment for sensible convection;
- `M_m` or equivalent vapor-transfer treatment for mass transfer;
- radiation separately.

The older `M_h=M_m=M` formulation is retained only as a regression-tested special case.

**Retained conclusion:** stronger air access can improve vapor removal while simultaneously increasing harmful sensible heat pickup in hot ambient conditions.

## 2. Covered-corridor result

`simulations/self_consistent_corridor_1d.py` solves signed buoyancy/friction velocity, wet-wall temperature, channel T/RH, evaporation, and body-side heat flux for a covered/end-renewed rectangular-duct limit.

At 35 °C / 70% RH, 100 mm length:

| width × depth | signed velocity | axial Pe | mean RH | body-side wet-wall heat flux |
|---|---:|---:|---:|---:|
| 3 × 2 mm | +0.228 mm/s | 0.81 | ~100% | +0.10 W/m² |
| 6 × 3 mm | +0.594 mm/s | 2.12 | ~100% | +0.40 W/m² |
| 10 × 5 mm | +1.60 mm/s | 5.70 | ~99.9% | +1.81 W/m² |

At 35 °C / 85% RH the 10 × 5 mm case reverses flow. At 40 °C / 70% RH it produces stronger downward flow and slightly negative body-side heat flux.

**Retained conclusion:** a long wet passive chimney is not the preferred architecture. Nonzero velocity and even a relatively large Péclet number do not prove useful vapor renewal.

## 3. Local open-valley renewal target

Define

\[
R=G_a/G_w,
\qquad
F=\frac{R}{1+R},
\]

where `G_a` is local valley-to-ambient vapor-renewal conductance and `G_w` is wet-surface-to-valley conductance.

| retained driving-force fraction `F` | required `R` |
|---:|---:|
| 0.50 | 1 |
| 0.80 | 4 |
| 0.90 | 9 |
| 0.95 | 19 |

Local T/RH and wet-surface temperature can be converted to normalized vapor loading and `F`. Exact high `R` is secondary because its inverse measurement becomes poorly conditioned near ambient vapor loading.

**Retained conclusion:** `F` is a useful local renewal-quality metric, but it is not an integrated cooling metric.

## 4. Distributed open-valley result

`simulations/open_valley_distributed_1d.py` solves

\[
D_vA\theta''-uA\theta'+G'_w(1-\theta)-G'_a\theta=0
\]

with ambient vapor loading at both axial ends.

For a representative 6 × 3 mm valley, the current screened lateral-exchange range gives an exchange length of roughly

\[
\ell_{exchange}\approx0.7\text{–}1.1\;mm.
\]

Selected zero-axial-flow center `F` values:

| effective lateral exchange parameter | segment length | center `F` |
|---:|---:|---:|
| 0.25 mm | 1 mm | 0.935 |
| 0.25 mm | 20 mm | 0.680 |
| 0.50 mm | 1 mm | 0.931 |
| 0.50 mm | 2 mm | 0.797 |
| 0.50 mm | 20 mm | 0.515 |
| 1.00 mm | 1 mm | 0.929 |
| 1.00 mm | 20 mm | 0.347 |

For 6 × 3 × 50 mm with the 0.5 mm effective lateral parameter, prescribed axial velocity from 0 to 100 mm/s changes center `F` negligibly; hundreds of mm/s are required before a large center effect appears in this screen.

**Correction:** the earlier design idea that 20–50 mm segmentation alone would provide adequate renewal is no longer supported. End-opening benefit is localized to a few exchange lengths.

Current physical candidates are therefore:

- continuously laterally open valleys;
- frequent cross-openings;
- discontinuous wet islands;
- 1–3 mm interrupted segments only as an extreme mechanism test.

The model parameter used for lateral exchange is an **effective diffusion thickness**, not a product dimension.

## 5. Renewal quality is not absolute evaporation capacity

For the local two-resistance screen:

\[
k_{eff}=\frac{k_wk_a}{k_w+k_a}=k_wF.
\]

At a fixed 6 mm valley width and one screened ambient-side parameter, increasing depth raises `F` but decreases `k_eff`:

| depth | `F` | `k_eff` |
|---:|---:|---:|
| 0.5 mm | 0.550 | 0.126 m/s |
| 1 mm | 0.695 | 0.0855 m/s |
| 2 mm | 0.799 | 0.0562 m/s |
| 3 mm | 0.841 | 0.0444 m/s |
| 5 mm | 0.879 | 0.0340 m/s |
| 8 mm | 0.901 | 0.0277 m/s |

**Correction:** never optimize `F` alone. Pair renewal quality with evaporation mass flux, effective conductance, and ultimately body-side heater power.

## 6. Coupled open-valley thermal / vapor result

`simulations/open_valley_thermal_1d.py` couples valley-air heat, vapor transport, wet-surface temperature, evaporation, and body-side heat flux while keeping effective lateral heat and vapor exchange separately parameterized.

Representative geometry: 6 × 3 × 50 mm, zero prescribed axial flow, `U_body=100 W/(m² K)`.

### 6.1 Primary 35 °C / 70% RH screen

| vapor parameter | heat parameter | evaporation | body-side heat flux | ambient sensible heat to wet wall |
|---:|---:|---:|---:|---:|
| 0.1 mm | 0.1 mm | ~700 g/m²h | +299 W/m² | +172 W/m² |
| 0.1 mm | 0.5 mm | ~645 g/m²h | +319 W/m² | +115 W/m² |
| 0.1 mm | 1.0 mm | ~615 g/m²h | +330 W/m² | +83 W/m² |
| 0.5 mm | 0.5 mm | ~522 g/m²h | +254 W/m² | +97 W/m² |
| 1.0 mm | 1.0 mm | ~414 g/m²h | +216 W/m² | +63 W/m² |

**Screen interpretation:** stronger vapor renewal helps, while reducing sensible heat access from hotter ambient air increases the body-supplied fraction of the latent heat. This is a model-form decomposition; it does not prove a textile can tune heat and vapor coefficients independently.

### 6.2 Hot-ambient sign reversal

At 40 °C / 70% RH with a Lewis-like linked baseline (`heat parameter = vapor parameter`), evaporation remains positive but body-side heat flux is negative across the screened linked cases. Example:

- linked 0.5 mm case: evaporation ~215 g/m²h;
- body-side heat flux ~−16 W/m²;
- ambient sensible heat to wet wall ~+160 W/m².

**Retained conclusion:** positive evaporation does not imply wearer cooling.

### 6.3 Liquid-supply audit

The thermal solver is currently a transfer-capacity screen and does not cap evaporation by liquid feed.

If wet fields occupy 65% of a 0.30 m² active area:

- 35 °C / 70% RH, strongest linked screened case: ~136.5 g/h, below the planned 150 g/h feed;
- 35 °C / 50% RH, strongest linked case: ~248 g/h, above 150 g/h and therefore supply-limited.

Any capacity above available feed must be labeled supply-limited rather than reported as achievable evaporation.

## 7. Salt / residue status

No current model assumes salt evaporation. Water evaporates; nonvolatile solutes remain in liquid/solid phases. Ordinary garments also retain sweat residue, so dedicated salt-management hardware is not a default requirement.

## 8. Results explicitly downgraded or corrected

The following are **not** current design conclusions:

- a single `M≈2.5–3.5` value as a validated +10 W threshold;
- geometric rib area as usable evaporative area;
- guaranteed upward chimney flow in vertical wet grooves;
- axial Péclet number as proof of useful renewal;
- 20–50 mm segmentation as a sufficient renewal mechanism;
- high `F` as proof of high evaporation capacity;
- positive evaporation as proof of positive body cooling.

## 9. Current design hypothesis

The present falsifiable architecture is:

1. directional liquid transport from skin;
2. flexible routed/whole-area in-plane heat spreading;
3. capillary delivery to wet exterior fields;
4. low-profile micro-rib / 3D-knit / fin-like evaporative texture;
5. continuous lateral ambient access through open valleys/gaps/islands rather than long covered ducts;
6. hot-ambient shielding or thermal routing that limits harmful sensible heat pickup;
7. geometry assessed using `F` **and** absolute transfer/body-cooling metrics.

## 10. Next numerical and physical work

Numerical:

- impose explicit liquid-feed limitation in the coupled thermal model;
- constrain the heat/mass exchange relationship with physically plausible Lewis-type coupling;
- move toward geometry-resolved 2-D/3-D external-flow treatment.

Physical:

- E1 B0 vs B4;
- E2 ablation;
- E3/E3b boundary-layer access;
- E3c D1/O1/O2a/O2b/O3;
- E4 humidity boundary with supply-limit classification;
- E6 hot-ambient shielding and sensible-heat penalty.
