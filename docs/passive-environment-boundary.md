# Passive Environmental Sign Boundary

Date: 2026-08-20  
Classification: **ANALYTIC / LOW-ORDER MODEL BOUNDARY**

## Purpose

The coupled open-valley screen showed that at sufficiently hot/humid ambient conditions water can continue evaporating while body-side heat flow becomes negative.

For the same-path heat/vapor baseline, the zero-body-heat-flow boundary can be reduced to an analytic temperature/RH equation. This provides a compact environmental falsification boundary independent of the chosen exchange multiplier within the stated model assumptions.

## Derivation

At zero body-side heat flux,

\[
q''_{body}=U_{body}(T_{skin}-T_s)=0,
\]

so for finite `U_body`:

\[
T_s=T_{skin}.
\]

For the same external characteristic exchange length and the same screening `Nu=Sh`, the wall balance becomes

\[
\frac{k_{air}}{D_v}(T_\infty-T_{skin})
=
L_v\left[
\rho_{v,sat}(T_{skin})
-\phi_\infty\rho_{v,sat}(T_\infty)
\right].
\]

The common geometric transfer factor cancels.

### Variable table

| symbol | meaning | SI unit | definition/assumption |
|---|---|---:|---|
| `T_inf` | ambient dry-bulb temperature | K or °C difference | solved boundary value |
| `T_skin` | skin/artificial-skin temperature | K or °C | repository default 34 °C |
| `phi_inf` | ambient RH fraction | 1 | 0–1 |
| `k_air` | air thermal conductivity | W/(m K) | fixed screening value 0.027 |
| `D_v` | water-vapor diffusivity in air | m²/s | fixed screening value 2.80e-5 |
| `L_v` | latent heat of vaporization | J/kg | fixed screening value 2.42e6 |
| `rho_v,sat` | saturated vapor density | kg/m³ | saturation-pressure relation used throughout repository |

### Dimensional check

Left side:

\[
[k_{air}/D_v][\Delta T]
=
\frac{W/(mK)}{m^2/s}K
=J/m^3.
\]

Right side:

\[
[L_v][\Delta\rho_v]
=(J/kg)(kg/m^3)=J/m^3.
\]

The equation is dimensionally consistent.

## Numerical boundary for `T_skin=34 °C`

| RH | zero-body-flux ambient temperature |
|---:|---:|
| 30% | 53.85 °C |
| 40% | 48.98 °C |
| 50% | 45.25 °C |
| 60% | 42.24 °C |
| 70% | 39.73 °C |
| 75% | 38.61 °C |
| 80% | 37.57 °C |
| 85% | 36.59 °C |
| 90% | 35.68 °C |
| 95% | 34.81 °C |

Interpretation inside this model:

- below the line, the same-path passive wet surface can have positive body-to-surface heat flow;
- above the line, ambient sensible heat dominates enough that body-side heat flow is negative even though evaporation may remain positive.

## Verification against the distributed thermal solver

The analytic boundary was compared against `open_valley_thermal_1d.py` using equal effective heat and vapor exchange distances over RH 30–95%.

Maximum absolute difference in the numerical comparison was approximately

\[
1.2\times10^{-8}\;^{\circ}C.
\]

The agreement is expected because the analytic equation is the zero-body-flux reduction of the same linked heat/mass assumptions.

## Design implication

This result changes the interpretation of very hot/humid operation.

Increasing heat-spreader coupling does not automatically solve the problem. Once the wet exterior is above the skin-side setpoint, stronger body-to-surface thermal coupling can transport more environmental heat inward.

The primary design should therefore distinguish:

1. normal hot-weather operation below the linked-model sign boundary;
2. near-boundary operation where the net body-cooling margin is small;
3. above-boundary operation where ordinary same-path passive heat/vapor exchange is not expected to provide positive body-side cooling in this model.

Any proposed mechanism that claims cooling above this boundary must identify what changes relative to the baseline—for example a physically demonstrated difference between vapor and sensible heat exchange, another heat sink, or a different skin/wet-surface state. It should not merely cite a larger evaporation rate.

## Limitations

This line is **not**:

- a human survivability or heat-stress threshold;
- a medical safety limit;
- a measured garment limit;
- a universal wet-bulb criterion independent of the model assumptions.

It is specific to the repository's same-path heat/vapor transfer analogy, fixed property approximations, and stated skin-side temperature. Real airflow, radiation, skin temperature, wetness, clothing geometry, and physiological response can move the physical boundary.

## Experimental use

E4/E6 should include test points on both sides of the modeled line when practical. For example, with a 34 °C artificial skin:

- 35 °C / 70% RH is below the model boundary;
- 40 °C / 70% RH is slightly above it;
- 35 °C / 90% RH is close to it.

The physical endpoint remains heater power, not evaporation rate alone.
