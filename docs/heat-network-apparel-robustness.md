# Heat-Network Apparel Robustness Screen

Status: **SIMULATION / VIRTUAL DESIGN ONLY — NO PHYSICAL SPECIMEN**  
Date: 2026-08-20

## Purpose

The heat-routing network must remain useful after clothing deformation and imperfect layer contact. This screen adds two first-order apparel constraints:

1. uniaxial stretch penalty on in-plane conduction;
2. spatial degradation of spreader-to-outer-layer thermal contact.

The models are deliberately low order. They identify which mechanism deserves more detailed modeling; they are not textile constitutive laws.

## Stretch model

For an imposed engineering strain `epsilon`, three x-direction conduction factors are compared.

### Straight geometry-only path

\[
f_x=(1+\epsilon)^{-2}.
\]

### Straight volume-preserving path

A further thickness/cross-section penalty is applied:

\[
f_x=(1+\epsilon)^{-3}.
\]

### Serpentine compliance screen

Previously generated geometry-only retention points are reused:

| stretch | retained path conductance |
|---:|---:|
| 5% | 95.2% |
| 10% | 90.8% |
| 15% | 86.9% |
| 20% | 83.3% |
| 30% | 76.9% |

The factor is applied to x-direction conductive faces only. The wet field, contact and exterior exchange remain unchanged, so this isolates routing sensitivity rather than simulating a fully deformed garment.

## Stretch result

For the four-island field, the heat-routing **gain** is less sensitive than the raw x-direction conductor factor because heat can also redistribute in y and through parallel routes.

At 20% stretch, retained routing gain in the current screen is approximately:

| topology | serpentine-mode retained gain |
|---|---:|
| directed | ~99.0% |
| blend `lambda=0.125` | ~98.7% |
| blend `lambda=0.375` | ~98.0% |
| mesh | ~97.4% |
| leaf | ~97.8% |

Under the harsher straight volume-preserving penalty, the same 20% stretch gives roughly 92–97% retained gain depending on topology.

**Interpretation:** in this low-order field, moderate stretch of an intact conductive network is not the dominant failure mode. This does not include cracking, delamination, contact loss, permanent set, or movement of wet zones.

## Spatial thermal-contact loss

Nominal spreader-to-outer contact is the same screening value used elsewhere. A degraded region uses a much lower contact coefficient. Four cases are compared:

- uniform contact;
- low-contact patch centered on one wet island;
- central seam-like low-contact strip;
- deterministic distributed 10% low-contact area.

The matched low-conductivity background is recomputed under the same contact map, so reported values remain **routing-mechanism gains**, not total garment cooling.

## Contact-loss result

Retention of nominal heat-routing gain:

| contact case | directed | blend 0.125 | blend 0.375 | mesh | leaf |
|---|---:|---:|---:|---:|---:|
| distributed 10% low contact | ~95% | ~95% | ~95% | ~94% | ~95% |
| localized wet-island contact loss | ~85% | **~87%** | ~83% | ~85% | ~86% |
| center seam-like strip | ~100% | ~100% | ~100% | ~100% | ~100% |

The seam result is specific to this symmetric screen and matched background reference; it must not be generalized as `seams do not matter`.

The strong result is that **contact loss at an active wet evaporator is more damaging than the first-order stretch penalties tested here**.

## Design implication

The current priority becomes:

1. preserve contact between the routed spreader and active wet evaporator fields;
2. keep directed heat paths short;
3. add only enough redundancy for expected wet-zone motion and damage morphology;
4. use serpentine/island-bridge mechanics where required by garment strain;
5. avoid assuming that conductor stretch alone determines durability.

Possible apparel implementations include:

- bonded or knitted contact zones around evaporator islands;
- local compression-maintaining spacer structures;
- broad contact pads at the ends of narrow conductive routes;
- compliant serpentine bridges between contact pads;
- redundant nearby terminal contacts rather than dense conductor everywhere.

## H / T / D / C / U

**H**: Heat-routing performance is more sensitive to loss of thermal contact at active wet zones than to moderate elastic stretch of an otherwise intact network.

**T**: Equal topology/wet field, deterministic x-conduction penalties, and explicit spatial contact maps.

**D**: Supported numerically if localized wet-zone contact loss produces a larger reduction in routed heat gain than 10–20% stretch in the intact-network screen.

**C**: Real stretch may cause cracking or delamination, which is not represented by the intact-network factor model. Real seam placement can also coincide with critical routes, unlike the current center strip.

**U**: Contact coefficients are screening inputs; actual pressure/contact-area dependence, nonlinear textile deformation, curvature and cycling are unresolved.

## Next step

The next robustness layer should combine deformation and contact failure instead of applying them independently:

- stretch-dependent contact maps;
- local compression around backpack/seat-contact regions;
- curvature-induced contact loss;
- cyclic damage accumulation;
- coupled moving wet islands.
