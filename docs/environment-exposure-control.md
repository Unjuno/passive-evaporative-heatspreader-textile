# Environment-dependent wet-terminal exposure

Status: **SIMULATION / VIRTUAL PROTOTYPE ONLY — NO PHYSICAL SPECIMEN**

## Question

A pressure-aware evaporator should be open to ambient air when evaporation removes body heat, but the same open structure can become a sensible-heat path from hot humid ambient air. Should wet-terminal exposure change with environment?

## Model

The synthetic backpack+strap pressure map and pressure-focused wet layout are retained. A global wet-terminal exposure fraction `e` scales wet-side sensible and vapor exchange together:

\[
h_{wet}=e\,h_{wet,0},\qquad k_{m,wet}=e\,k_{m,0}.
\]

This is **not** a selective membrane model. Closing the wet terminal reduces both vapor removal and sensible heat transfer. Dry-side ambient exposure remains in the model, so closing a wet terminal does not guarantee positive body cooling.

## Environment sweep

Representative 20 x 20 converged results:

| environment | best exposure | fully-open body heat flux | closed body heat flux | interpretation |
|---|---:|---:|---:|---|
| 35 °C / 50% RH | 1.0 | ~112.8 W/m² | ~-2.0 | open |
| 35 °C / 70% RH | 1.0 | ~59.6 | ~-2.0 | open |
| 35 °C / 85% RH | 1.0 | ~20.7 | ~-2.0 | open |
| 40 °C / 50% RH | 1.0 | ~51.4 | ~-11.9 | open |
| 40 °C / 70% RH | 0.0 | ~-14.9 | **~-11.9** | closure reduces harm |
| 40 °C / 85% RH | 0.0 | ~-38.2 | **~-11.9** | closure strongly reduces harm |
| 45 °C / 30% RH | 1.0 | ~68.5 | ~-21.7 | evaporation still useful |
| 45 °C / 50% RH | 1.0 | ~-17.1 | ~-21.7 | open is less harmful, but body heat flow remains negative |

The optimum in this same-path screen is generally near an endpoint: fully open or nearly closed, rather than a broad intermediate optimum.

## Interpretation

Two distinct forms of "switching" should be separated:

### Load-state switching

Changing wet-terminal location between backpack/no-backpack states gave less than ~1% ideal benefit over the best fixed pressure-aware layout. It is not currently worth baseline complexity.

### Environment-state exposure switching

Opening or closing the same wet terminal can materially change heat gain/loss in hot humid conditions. This remains technically important because the sign of body-side heat flow changes with environment.

Therefore the current product direction can remain **fixed in terminal geography** while allowing **passive exposure state** to change with temperature/humidity if a low-complexity mechanism exists.

## Possible passive embodiments

- humidity/temperature-responsive flap over the evaporator;
- geometry that collapses/shields when evaporation driving force is low;
- reversible cover layer with exposed/open and shielded states;
- passive sorption/swelling actuator that changes terminal exposure.

These are optional embodiments; no actuator has been modeled mechanically.

## Critical limitation

Closing wet terminals alone did not make the 40 °C / 70–85% RH cases body-cooling-positive because dry-side ambient heat ingress remained. Full hostile-environment protection therefore also requires dry-side shielding / thermal isolation.

## Design conclusion

> Use pressure-aware fixed terminal geography, but preserve an optional environmental **open/shield** state because the useful sign of ambient exposure changes with hot/humid conditions.

Do not interpret this as a medical safety boundary or measured garment control threshold.
