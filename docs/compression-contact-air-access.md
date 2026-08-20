# Compression: Contact Benefit vs Ambient-Access Loss

Status: **SIMULATION / MECHANISM SCREEN ONLY — NO PHYSICAL SPECIMEN**  
Date: 2026-08-20

## Question

Garment compression can produce competing effects:

- better thermal contact between the routed heat spreader and the wet outer evaporator;
- worse ambient access because open valleys/gaps collapse.

The first effect can improve body-to-evaporator heat delivery. The second reduces vapor transfer and eventually prevents all available liquid from evaporating.

## Explicit hypothetical compression laws

Compression fraction is `c` with `0 <= c < 1`.

Contact is screened as

\[
h_c(c)=h_{c,0}(1+a c),
\]

with nominal `a=2`.

Ambient access is screened as

\[
s_{air}(c)=(1-c)^n,
\]

and the wet sensible/vapor coefficients are multiplied by `s_air`. The dry sensible coefficient is scaled the same way.

`n=1,2,3` are **model-form sensitivity cases**, not fitted textile properties.

## Regime handling

The solver explicitly separates:

1. **supply-limited partial wetness** — fully wet transfer capacity exceeds the 100 g/h feed, so the wet fraction is solved from the water balance;
2. **transfer-limited full wetness** — even 100% wet area cannot evaporate the imposed feed, so wet fraction is fixed to one and evaporation falls below feed.

This correction is important. A previous exploratory solve reached the `beta≈1` bound and looked like nonlinear solver failure. It was actually the onset of the transfer-limited regime.

## Representative `n=2` result

At 35 °C / 50% RH, 100 g/h over 0.195 m²:

| compression | regime | evaporation | body-side heat removal |
|---:|---|---:|---:|
| 0% | partial wet | 100 g/h | ~55.9 W |
| 10% | partial wet | 100 g/h | ~56.7 W |
| 20% | partial wet | 100 g/h | ~57.5 W |
| 30% | partial wet | 100 g/h | ~58.3 W |
| 35% | full wet / near transition | ~99 g/h | ~58.0 W |
| 40% | transfer limited | ~88 g/h | ~52.3 W |
| 50% | transfer limited | ~66 g/h | ~40.5 W |
| 60% | transfer limited | ~46 g/h | ~28.7 W |
| 80% | transfer limited | ~13 g/h | ~8.4 W |

Under this explicit hypothesis, modest compression is slightly beneficial because thermal contact improves while enough vapor capacity remains. Once the open-air path collapses enough to make the surface transfer limited, cooling decreases rapidly.

## Model-form sensitivity

The transition location depends strongly on the assumed air-closure exponent:

| air-closure exponent `n` | first transfer-limited compression | modeled best compression |
|---:|---:|---:|
| 1 | ~58% | ~57% |
| 2 | ~35% | ~35% |
| 3 | ~25% | ~25% |

Therefore **the numerical compression percentage is not a garment design limit**. The robust conclusion is the existence of a competition and a regime transition.

For the same three cases, body-side heat removal first falls below 90% of the uncompressed state at approximately 67%, 42%, and 31% compression respectively.

## Design implication

The exterior should not rely on evaporative valleys that collapse globally under ordinary garment pressure. A useful architecture should instead combine:

- compression-resistant local air openings near active evaporator fields;
- spacer/3D-knit geometry that preserves lateral ambient access;
- broad compliant thermal terminal contacts underneath those openings;
- alternate ambient escape paths so local pressure does not isolate an entire wet field;
- deliberate separation between load-bearing/contact structures and vapor-renewal voids.

This creates an important design target:

> **increase solid thermal contact without proportionally closing the vapor path.**

That is a more specific objective than simply making the garment soft, thick, or highly conductive.

## H / T / D / C / U

**H**: Moderate compression can initially improve the body-to-evaporator thermal path, but sufficiently strong compression causes a transfer-limited transition when ambient vapor access collapses.

**T**: Deterministic low-order sweep over `c=0–0.8`, with three explicit air-closure exponents and a separate full-wet transfer-limited solve.

**D**: Supported if body heat removal has a shallow initial increase/plateau followed by a clear decline after full-wet capacity falls below feed.

**C**: Real compression may change valley geometry, liquid distribution, contact area, conductor path length and local airflow nonlinearly; pressure can also displace liquid rather than only change transfer coefficients.

**U**: The largest uncertainty is the constitutive mapping from physical pressure/compression to ambient exchange. The exponent cases are not probabilities or fitted measurements.

## Next numerical step

Replace global compression with spatial pressure fields representing:

- backpack contact;
- chair/seat-back contact;
- shoulder/strap loads;
- garment curvature/contact around torso regions.

The key question is whether a network of uncompressed lateral escape corridors can preserve evaporation when some evaporator fields are mechanically loaded.
