# Transient terminal water-buffer screen

Status: **computational only; no physical garment exists.**

This model adds time dependence to the steady VP-E architecture. It is intended to answer three questions that steady-state screens cannot:

1. how quickly liquid delivery reaches the exterior terminal after sweat production changes;
2. how long stored water can continue to support evaporation after sweat production falls;
3. whether terminal water hold-up is a useful buffer or merely unnecessary wet mass.

## Water-mass states

The model explicitly conserves water in two state variables:

- `M_line`: water in the transport path;
- `M_terminal`: water retained at the evaporative terminal.

For a liquid-delivery time constant `tau_l`:

\[
\dot M_{line}=\dot m_{sweat}-\dot m_{delivered},
\qquad
\dot m_{delivered}=M_{line}/\tau_l.
\]

Terminal storage follows

\[
\dot M_{terminal}=\dot m_{delivered}-\dot m_{evap}-\dot m_{overflow}.
\]

The implementation checks the cumulative water balance directly. In the reference run the maximum numerical water-balance error was below `1e-12 g`.

## Thermal response

The body-side heat-flux target is interpolated between the existing VP-E dry/shield and full-wet steady states according to the fraction of full-wet evaporation capacity actually supplied. A separate first-order thermal time constant is then applied.

This is a low-order transient bridge, not a measured textile thermal capacitance.

## Reference environment and pulse

The current reference uses:

- 35 °C / 70% RH;
- structured area `0.195 m²`;
- full-wet evaporation capacity `~22.08 g/h` over that area;
- full-wet signed body-side heat flux `~58.64 W/m²`;
- dry/shield reference `~-2.03 W/m²`;
- nominal VP-E modeled terminal water hold-up `~12.42 g`;
- sweat schedule: 10 min at 10 g/h, 30 min at 100 g/h, then zero.

## Ideal capillary filling lower bound

For an ideal horizontal cylindrical capillary, Lucas-Washburn gives

\[
t=\frac{2\mu L^2}{\gamma r\cos\theta}.
\]

At `L=30 mm` the ideal lower-bound filling times are approximately:

- 35 µm radius: `0.76 s`;
- 50 µm: `0.53 s`;
- 100 µm: `0.27 s`;
- 200 µm: `0.13 s`.

Real textiles can be much slower because tortuosity, unsaturated flow, pore-size distribution and air displacement are omitted. The ideal values are therefore lower bounds, not response-time claims.

## Startup vs persistence tradeoff

With a 2 min thermal time constant, increasing the liquid-delivery time constant from 0 to 10 min increased the time to 90% of the full-wet body-flux response from roughly `3.37 min` to `4.93 min`.

At the same time, delayed delivery carries water past the end of the sweat pulse and reduces overflow. In the mass-conserving model this extends post-exercise cooling.

The correct interpretation is not that slower transport is intrinsically better. A transport/storage system can smooth a large water pulse, trading slower startup against lower overflow and longer recovery-period evaporation.

## Terminal storage-capacity sweep

For the reference pulse and `tau_liquid=tau_thermal=2 min`:

| terminal water capacity | time after exercise stop to half body-flux response | total evaporated water | overflow/drain |
|---:|---:|---:|---:|
| 0 g | ~6.3 min | ~14.2 g | ~37.5 g |
| 2 g | ~11.8 min | ~16.2 g | ~35.5 g |
| 4 g | ~17.2 min | ~18.2 g | ~33.5 g |
| 8 g | ~28.1 min | ~22.2 g | ~29.5 g |
| 12.42 g | ~40.1 min | ~26.6 g | ~25.1 g |
| 20 g | ~60.7 min | ~34.2 g | ~17.5 g |

Across this particular pulse, persistence rises almost linearly at roughly `~2.7 min/g`. No intrinsic optimum appears in the model.

Therefore storage capacity should be selected using product constraints that are not yet modeled: wet mass, drying time, tactile comfort, retained-sweat hygiene, washability and desired post-exercise cooling duration.

## Design implication

The current architecture should distinguish:

- **transport inventory**, which should remain small and protected;
- **intentional terminal storage**, which may be useful as a short-term evaporative buffer;
- **uncontrolled saturation/overflow**, which should be drained rather than treated as useful storage.

A lighter garment can intentionally choose less terminal hold-up if rapid drying matters more than cooling persistence.

## Limitations

- steady VP-E heat-flux states are used as the transient endpoints;
- no measured garment thermal capacitance exists;
- liquid time constants are screening variables;
- body sweat production is prescribed rather than thermophysiologically coupled;
- stored-water comfort, microbial effects and textile feel are not modeled;
- salt remains nonvolatile, but transient solute concentration/deposition is not yet coupled to this water-buffer model.
