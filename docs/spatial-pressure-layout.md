# Spatial pressure-map evaporator-layout screen

Status: **SIMULATION / VIRTUAL PROTOTYPE ONLY — NO PHYSICAL SPECIMEN**

## Question

How should wet evaporator islands be placed when a garment is locally compressed by a backpack panel, shoulder straps, or a seat back?

The previous compression model was spatially uniform. This screen makes the constitutive assumptions spatially varying and compares equal-area wet layouts while holding the heat-routing network material fraction fixed.

## Constitutive screen

A normalized pressure field `p(x,y)` is mapped to local compression

\[
c(x,y)=c_{max}p(x,y).
\]

Thermal contact is assumed to improve with compression:

\[
h_c(x,y)=h_{c,0}[1+a c(x,y)].
\]

Ambient access is assumed to decrease:

\[
s_{air}(x,y)=[1-c(x,y)]^n.
\]

Wet-side sensible and vapor exchange are scaled by `s_air`; dry-side sensible exposure is scaled the same way in this first-order screen.

These laws are **hypothetical model inputs**, not measured pressure/contact/porosity relations for a textile.

## Equal-area layouts

All tested layouts use approximately 23% wet area:

- four islands;
- peripheral islands;
- center panel;
- upper/lower bands;
- side columns;
- pressure-aware placement, which preferentially chooses low-pressure cells with a small bias toward the existing `lambda=0.125` routed heat network.

The conductive network is held near 35% high-`k` material fraction.

## Primary condition

Reference numerical condition:

- ambient: 35 °C / 50% RH;
- skin boundary: 34 °C;
- `cmax=0.5`;
- air-closure exponent `n=2`;
- 24 x 24 grid;
- convergence tolerance approximately `2e-6 °C` final fixed-point change in the archived reference run.

### Backpack + shoulder straps

Converged 24 x 24 reference:

| wet layout | body-side heat flux | vapor-capacity index | mean local compression |
|---|---:|---:|---:|
| pressure-aware | ~112.8 W/m² | ~211 g/(m² h) | ~0.061 |
| peripheral islands | ~106.4 | ~194 | ~0.129 |
| side columns | ~103.9 | ~191 | ~0.130 |
| upper/lower bands | ~86.1 | ~152 | ~0.270 |
| four islands | ~84.3 | ~147 | ~0.303 |
| center panel | ~60.9 | ~105 | ~0.421 |

The vapor-capacity value is an area-averaged transfer-capacity output of the mechanism screen, not an equal-feed garment evaporation claim.

### Other synthetic pressure maps

At the same primary constitutive setting, pressure-aware placement ranked first in body-side heat flux for backpack-panel, shoulder-strap, seat-back and combined backpack+strap maps.

Without pressure, the ordinary four-island layout ranked above the pressure-aware layout. Therefore the supported conclusion is **not** "always place evaporation at the perimeter." It is:

> where persistent local compression is expected, keep active evaporator/open-valley area away from strongly compressed regions while retaining short thermal routes from those regions to nearby low-pressure wet terminals.

## Sensitivity

Three constitutive corners were screened during development:

- mild closure: `cmax=0.3`, `n=1`;
- primary: `cmax=0.5`, `n=2`;
- severe closure: `cmax=0.7`, `n=3`.

Pressure-aware placement dominates more consistently as the assumed air-path closure becomes stronger. Under weak closure, ordinary four-island or peripheral layouts can remain competitive because improved contact partially offsets loss of ambient access.

This sensitivity is the main reason no absolute pressure limit is claimed.

## Design implication

The current virtual garment should separate three roles spatially:

1. **load-bearing / compressed zones** — preserve solid contact and collect body heat;
2. **short routed heat paths** — move heat laterally out of the compressed zone;
3. **low-pressure wet terminals with open vapor escape** — perform evaporation where external renewal is preserved.

This suggests backpack-compatible or seated-use garments should not put the highest-value evaporator area directly under the broadest pressure patches unless a mechanically protected air channel is provided.

## Failure modes / uncertainty

- the pressure maps are synthetic, normalized fields;
- pressure-to-compression mapping is unknown;
- compression-to-contact and compression-to-air-access laws are hypothetical;
- curvature, shear, sliding contact, fabric buckling and time-varying pressure are omitted;
- liquid supply is not yet co-optimized with the pressure-aware evaporator location;
- current pressure-aware placement is a simple score rule, not an optimized topology.

## Next numerical work

1. time-varying backpack/seat pressure maps;
2. co-optimize capillary liquid routes and heat routes to low-pressure wet terminals;
3. add protected spacer/open-valley structures under nominally compressed zones;
4. compare pressure-avoiding evaporation with pressure-resistant air-channel architectures;
5. move from normalized pressure to explicit pressure/contact constitutive parameter sweeps.
