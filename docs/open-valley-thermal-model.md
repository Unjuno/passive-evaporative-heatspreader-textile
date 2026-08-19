# Coupled Open-Valley Thermal / Vapor Screen

Date: 2026-08-20  
Classification: **SIMULATION / SCREENING — NOT PHYSICAL GARMENT PERFORMANCE**

## Purpose

The distributed vapor model can say whether a valley remains locally dry enough for evaporation, but it cannot say where the latent heat comes from.

`simulations/open_valley_thermal_1d.py` therefore solves a low-order coupled wet-valley problem with separate lateral heat and vapor exchange parameters.

The model is designed to answer two different questions:

1. does stronger vapor renewal increase evaporation capacity?;
2. does the resulting evaporation actually remove heat from the body, or is much of the latent heat supplied by hot ambient air?

## State equations

Valley-air sensible energy is screened as

\[
k_{air}A\frac{d^2T}{dz^2}
-\rho c_puA\frac{dT}{dz}
+h_wP_w(T_s-T)
+h_aP_a(T_\infty-T)=0.
\]

Valley vapor is screened as

\[
D_vA\frac{d^2C}{dz^2}
-uA\frac{dC}{dz}
+k_{m,w}P_w(C_{sat}(T_s)-C)
+k_{m,a}P_a(C_\infty-C)=0.
\]

The local wet-wall balance is

\[
U_{body}(T_{skin}-T_s)
+h_w(T-T_s)
-L_vk_{m,w}(C_{sat}(T_s)-C)=0.
\]

The wall equation is solved iteratively with the two distributed air equations.

## Variable table

| symbol | meaning | SI unit | current screening treatment |
|---|---|---:|---|
| `T` | valley-air dry-bulb temperature | K or °C difference | solved along valley |
| `T_s` | wet-surface temperature | K or °C | solved locally |
| `C` | water-vapor density | kg/m³ | solved along valley |
| `u` | axial mean velocity | m/s | prescribed in this model |
| `h_w` | wet-wall sensible coefficient | W/(m² K) | `Nu k_air/D_h` |
| `h_a` | lateral ambient sensible coefficient | W/(m² K) | `k_air/delta_heat` |
| `k_m,w` | wet-wall vapor coefficient | m/s | `Sh D_v/D_h` |
| `k_m,a` | lateral ambient vapor coefficient | m/s | `D_v/delta_vapor` |
| `U_body` | body-to-wet-wall effective coupling | W/(m² K) | screening parameter, default 100 |
| `L_v` | latent heat | J/kg | fixed screening value |

### Unit / energy check

At steady wall balance:

\[
q''_{body}+q''_{air}=L_v\dot m''_{evap}.
\]

This identity is enforced by regression testing to numerical tolerance.

## Independent heat and vapor exchange

`delta_vapor` and `delta_heat` are intentionally independent model-form parameters. This does **not** claim that real air heat and mass transfer are independent. It allows the consequences of incorrectly forcing them to be equal to be examined.

A Lewis-like baseline is obtained by setting

`delta_heat = delta_vapor`.

The next higher-fidelity flow model should constrain their physical relationship rather than treating either equality or total independence as exact.

## Primary 35 °C / 70% RH result

Representative geometry: 6 × 3 × 50 mm, zero prescribed axial flow, `U_body=100 W/(m² K)`.

Selected cases:

| `delta_vapor` | `delta_heat` | mean wet surface | mean valley RH | evaporation | body-side heat flux | ambient sensible heat to wall |
|---:|---:|---:|---:|---:|---:|---:|
| 0.1 mm | 0.1 mm | 31.01 °C | 0.740 | 700 g/m²h | +299 W/m² | +172 W/m² |
| 0.1 mm | 0.5 mm | 30.81 °C | 0.792 | 645 g/m²h | +319 W/m² | +115 W/m² |
| 0.1 mm | 1.0 mm | 30.70 °C | 0.822 | 615 g/m²h | +330 W/m² | +83 W/m² |
| 0.5 mm | 0.5 mm | 31.46 °C | 0.828 | 522 g/m²h | +254 W/m² | +97 W/m² |
| 1.0 mm | 1.0 mm | 31.84 °C | 0.876 | 414 g/m²h | +216 W/m² | +63 W/m² |

Screen interpretation:

- stronger vapor renewal increases evaporation and body-side heat removal at the primary condition;
- for the same vapor renewal, weaker sensible access from the 35 °C ambient forces a larger fraction of latent heat to come from the body;
- this is a mechanism decomposition, not proof that a textile can independently tune the two coefficients over the full parameter range.

## Hot-ambient reversal

At 40 °C / 70% RH, selected cases are:

| `delta_vapor` | `delta_heat` | evaporation | body-side heat flux | ambient sensible heat to wall |
|---:|---:|---:|---:|---:|
| 0.1 mm | 0.1 mm | 346 g/m²h | **−18 W/m²** | +251 W/m² |
| 0.5 mm | 0.5 mm | 215 g/m²h | **−16 W/m²** | +160 W/m² |
| 1.0 mm | 1.0 mm | 150 g/m²h | **−13 W/m²** | +114 W/m² |
| 0.1 mm | 0.5 mm | 261 g/m²h | +9 W/m² | +167 W/m² |
| 0.1 mm | 1.0 mm | 215 g/m²h | +24 W/m² | +121 W/m² |

The key finding is not the exact numbers. It is the sign result:

> positive evaporation does not imply positive body cooling.

When heat and vapor access follow the same strong ambient-air path in this low-order model, hot ambient sensible heat can supply the evaporation and additionally heat the body-side system.

This supports continued dry-side shielding / thermal-routing work and requires hot-ambient physical validation.

## Water-supply audit

The current model is a transfer-capacity screen and has no liquid-feed cap.

At 35 °C / 70% RH, even the strongest linked case (`delta=0.1 mm`) gives about 700 g/m²h. If wet fields occupy 65% of a 0.30 m² active area, that is about 136.5 g/h, below the project's 150 g/h primary feed.

At 35 °C / 50% RH, the same linked case gives about 1273 g/m²h, or about 248 g/h over 65% of 0.30 m². That case would be **liquid-supply-limited** under a 150 g/h experiment and must not be interpreted as achievable evaporation at fixed feed.

A future version may impose the feed limit directly, but current screening already labels this regime explicitly.

## Design consequence

The target is not simply maximum air exchange. The desired direction is:

1. high enough vapor renewal to prevent local saturation;
2. adequate absolute vapor conductance / evaporation mass flux;
3. limited harmful sensible heat pickup from hotter ambient air;
4. strong body-to-wet-zone thermal routing;
5. sufficient liquid supply without runoff.

The physically realizable coupling between heat and mass transfer remains an open model question.

## Physical validation

E3c/E6 should measure simultaneously:

- wet-surface temperature;
- valley/near-field T and RH;
- evaporation mass balance;
- heater-power difference;
- far-field ambient T/RH and air speed.

A design with lower valley RH but no heater-power benefit is not a cooling success. Likewise, a design with high evaporation but negative body-side heater-power difference under hot ambient conditions is not a cooling success.

## Major uncertainties

- `Nu=Sh=7.54` is a screening choice, not a measured open-valley correlation;
- lateral `delta_heat` / `delta_vapor` are effective exchange parameters, not direct garment dimensions;
- liquid feed is not capped in the current solver;
- radiation within/above the valley is omitted;
- axial velocity is prescribed rather than solved from the open-valley state;
- 2-D/3-D external plume/cross-flow is not resolved.

Absolute W/m² values remain model-form uncertain until physical data constrain these assumptions.
