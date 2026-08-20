# Protected vapor-path vs pressure-aware evaporator relocation

Status: **SIMULATION / VIRTUAL PROTOTYPE ONLY — NO PHYSICAL SPECIMEN**

## Question

When an evaporator sits under a persistent backpack/strap load, is it better to:

1. move the active wet terminal toward a nearby low-pressure region; or
2. keep the wet terminal under the load but mechanically preserve its vapor-renewal path with a spacer/open channel?

This screen uses the same synthetic backpack+strap pressure map and constitutive assumptions as `spatial_pressure_layout.py`.

## Protected-air parameter

For the loaded center panel, the ordinary local air-access scale is

\[
s_{air}(x,y)=[1-c(x,y)]^n.
\]

A protected vapor path imposes a wet-side floor

\[
s_{wet}(x,y)=\max[s_{air}(x,y),s_{min}].
\]

The floor is a design variable representing a mechanically protected open-gap/spacer limit. It is not a measured porosity or velocity.

Thermal contact still follows the same compression-dependent law; only wet-side ambient access is protected in this screen.

## Primary 24 x 24 result

Synthetic condition:

- backpack + shoulder-strap map;
- `cmax=0.5`;
- air-closure exponent `n=2`;
- 35 °C / 50% RH;
- same routed high-k network used in the spatial-pressure screen.

Pressure-aware relocation without a protected channel gives approximately:

- body-side heat flux: **112.76 W/m²**;
- mean wet-side air-access scale: **0.883**.

The loaded center-panel baseline has mean wet-side air scale ~0.340 and only ~60.89 W/m² body-side heat flux in this mechanism screen.

As the protected minimum air-access floor is raised:

| minimum wet air-access floor | body-side heat flux | vapor-capacity index |
|---:|---:|---:|
| 0.50 | ~81.3 W/m² | ~143 g/(m² h) |
| 0.60 | ~91.9 | ~164 |
| 0.70 | ~101.5 | ~183 |
| 0.80 | ~110.0 | ~202 |
| 0.85 | **~114.0** | ~211 |
| 0.90 | ~117.8 | ~220 |
| 1.00 | ~125.0 | ~236 |

On the 0.05 screening grid, the first floor that exceeds the pressure-aware relocation reference is **0.85**. Linear interpolation between the 0.80 and 0.85 points places the crossover near **0.83–0.84**.

This number is **not** a real garment requirement because the pressure-to-air-closure law is hypothetical. The useful conclusion is comparative:

> a wet terminal can remain under a load if its vapor escape path is protected strongly enough; otherwise relocating active evaporation to a nearby low-pressure terminal is the safer current design direction.

## Design implication

Two explicit implementation families should remain in the disclosure:

### P1 — pressure-aware relocation

- compressed zone keeps thermal contact;
- short in-plane heat paths route body heat out of the load patch;
- capillary liquid paths feed nearby low-pressure evaporator islands;
- open valleys/gaps remain exposed to ambient air.

### P2 — protected under-load evaporator

- wet terminal remains under the load zone;
- load is carried by ribs/spacers/bridges that preserve a separate vapor escape gap;
- solid contact and vapor access are mechanically decoupled;
- drainage/capillary supply remains distinct from the air gap.

The two families are not mutually exclusive: a garment can use protected under-load evaporation where geometry allows it and pressure-aware relocation elsewhere.

## Uncertainty / failure modes

- `s_min` is an effective ambient-access parameter, not a directly specified channel height;
- no buckling, creep, shear or spacer collapse model is included;
- the pressure field is static;
- the open channel is not yet solved with geometry-resolved cross-flow/natural convection;
- liquid supply and salt deposition in the protected structure remain separate unresolved constraints.

## Next work

1. map protected channel height/width/rib spacing to an effective `s_min` using geometry-resolved flow/transport;
2. add curvature and repeated load cycles;
3. co-design the solid load-bearing skeleton, vapor gap and capillary feed;
4. compare the mass/thickness penalty of P2 with the extra routing distance required by P1.
