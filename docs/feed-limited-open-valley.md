# Feed-Limited Open-Valley Screen

Status: **SIMULATION / HOMOGENIZED PARTIAL-WETNESS MODEL**  
Date: 2026-08-20

## 1. Why this model was added

`open_valley_thermal_1d.py` originally described a fully wet transfer-capacity state. That is appropriate only while liquid supply is sufficient to sustain the predicted evaporation flux.

If fully-wet evaporation capacity exceeds available liquid feed, simply clipping evaporation to the feed while retaining the fully-wet surface temperature and body heat flux is inconsistent.

`simulations/open_valley_feed_limited.py` therefore adds an explicit sub-grid wet fraction `beta`.

## 2. Homogenized partial-wetness model

The strong-heat-spreader limit is represented by one thermally averaged floor temperature while only a fraction `beta` of the sub-grid surface supplies vapor.

The vapor source becomes

\[
\dot m'' = \beta k_{m,w}\left(\rho_{v,sat}(T_s)-\rho_v\right),
\]

and the local wall energy balance becomes

\[
U_{body}(T_{skin}-T_s)
+h_w(T_a-T_s)
-L_v\dot m''=0.
\]

The sensible wall/body coupling is retained over the whole thermally connected floor.

### Variables

| Symbol | Meaning | SI unit | Definition / assumption |
|---|---|---:|---|
| `beta` | homogenized wet fraction | 1 | `0 <= beta <= 1` |
| `k_m,w` | wet-wall vapor-transfer coefficient | m/s | current low-order Sherwood screen |
| `rho_v,sat` | saturated water-vapor density | kg/m³ | evaluated at wet-surface temperature |
| `rho_v` | local valley water-vapor density | kg/m³ | solved 1-D field |
| `U_body` | body/spreader-to-surface conductance | W/(m² K) | screening parameter |
| `h_w` | valley-air-to-floor sensible coefficient | W/(m² K) | current low-order Nusselt screen |
| `L_v` | latent heat of vaporization | J/kg | fixed screening value |

Dimensional check:

\[
[k_m(\rho_{sat}-\rho_v)]
=(m/s)(kg/m^3)=kg/(m^2s),
\]

so

\[
[L_v\dot m'']=(J/kg)(kg/(m^2s))=W/m^2.
\]

## 3. Feed constraint

For imposed liquid feed per panel area `m_feed''`:

- if the fully-wet capacity is below the feed, use `beta=1` and classify the state as **transfer-limited**;
- if the fully-wet capacity exceeds the feed, solve `0 < beta < 1` such that

\[
\overline{\dot m''}(\beta)=\dot m''_{feed}.
\]

This is a steady screening closure, not a resolved wetting-front model.

## 4. Representative result: 150 g/h over 65% of 0.30 m²

The nominal structured area is

\[
A_w=0.30\times0.65=0.195\;m^2,
\]

so a 150 g/h total feed corresponds to approximately

\[
769\;g/(m^2h)
\]

over the structured panel.

At 35 °C / 50% RH with linked heat/vapor exchange distances:

- `delta=0.10 mm`: supply-limited, `beta≈0.37`, body-side heat flux ≈331 W/m²;
- `delta=0.25 mm`: supply-limited, `beta≈0.43`, body-side heat flux ≈356 W/m²;
- `delta=0.50 mm`: supply-limited, `beta≈0.55`, body-side heat flux ≈383 W/m²;
- around `delta≈0.95–1.0 mm`: evaporation capacity is approximately matched to the 150 g/h supply and the current screen gives the largest body-side heat flux in the linked-exchange sweep;
- weaker exchange beyond this point becomes transfer-limited and evaporation/body cooling decrease.

The exact optimum is model-form dependent and must not be treated as a product dimension.

## 5. Design consequence

When water supply is capped, maximizing external transfer coefficient is not necessarily the same as maximizing body cooling.

Once the water feed is fully consumed, stronger linked heat/vapor exchange can mainly increase the fraction of latent energy supplied by warmer ambient air rather than by the body.

The design objective is therefore closer to:

> sufficient vapor exchange to use the available sweat/feed, while avoiding unnecessary sensible heat pickup from hot ambient air.

This reinforces the need to treat vapor transfer, sensible transfer, liquid supply and body heat coupling as separate constraints.

## 6. Humidity dependence

In the 150 g/h screen:

- at 35 °C / 50% RH, supply limitation appears for the strongest linked-exchange cases and a finite exchange optimum appears;
- at 35 °C / 70% RH, the screened linked cases remain transfer-limited at the primary feed and stronger exchange is still beneficial over the scanned range;
- at 35 °C / 85% RH, vapor-pressure driving force is small and the model remains transfer-limited;
- at 40 °C / 70% RH with ordinary linked heat/vapor access, evaporation can remain positive while body-side heat flux remains negative.

## 7. What `beta` does not mean

`beta` is **not** a measured visible wet-area fraction and must not be interpreted as one without validation.

The model does not resolve:

- individual dry and wet patches;
- capillary redistribution dynamics;
- dry-patch surface temperature differences;
- contact-angle hysteresis;
- transient sweat pulses;
- local salt concentration differences;
- compression-induced liquid redistribution.

E1/E3c physical runs should use imaging or another wetness indicator if a geometric wet-area fraction is to be compared with modeled `beta`.

## 8. Falsifiable experiment addition

At 35 °C / 50% RH, hold geometry fixed and sweep water feed while recording heater power and total evaporation.

The model predicts three qualitative regimes:

1. low feed: partial-wetness / supply-limited, evaporation follows feed;
2. transition: wet fraction approaches one and useful body heat removal peaks or changes slope;
3. high feed: transfer-limited, added liquid is retained/run off rather than increasing evaporation.

The predicted location of the transition should be treated as a hypothesis. Failure to observe a feed-dependent transition is evidence against the homogenized partial-wetness closure.