# Combined Heat-Network Failure Screen

Status: **SIMULATION / VIRTUAL DESIGN ONLY — NO PHYSICAL SPECIMEN**  
Date: 2026-08-20

## Purpose

Separate robustness screens showed that intact-network stretch, conductor loss, and thermal-contact loss affect heat routing differently. This screen combines three apparel-relevant penalties in one deterministic condition:

1. 20% uniaxial stretch using the compliant-serpentine x-conduction factor;
2. low thermal contact around one active wet evaporator island;
3. localized removal of 5% of the initial high-k conductor cells near that same island.

The matched low-conductivity background is recomputed under the same stretch/contact condition, so reported values are **routing-mechanism gains**, not total garment cooling.

## Reference result

For the current four-island / ~35% high-k screen:

| topology | nominal gain | all-three gain | retained |
|---|---:|---:|---:|
| blend `lambda=0.125` | ~5.86 W | **~4.96 W** | **~84.6%** |
| blend `lambda=0.375` | ~5.93 W | ~4.70 W | ~79.2% |
| directed | ~5.63 W | ~4.68 W | ~83.1% |
| leaf/venation | ~5.17 W | ~4.23 W | ~81.9% |
| redundant mesh | ~5.35 W | ~4.20 W | ~78.4% |

The nominal maximum (`lambda=0.375`) is not the best combined-failure candidate. The lightly cross-linked directed network (`lambda=0.125`) retains the largest absolute gain in this screen.

## Failure decomposition

For `lambda=0.125`, approximate retained routing gain is:

- 20% stretch only: ~98.7%;
- localized 5% conductor fracture: ~95.2%;
- localized wet-island contact loss: ~87.0%;
- stretch + contact: ~85.7%;
- contact + fracture: ~85.9%;
- all three: ~84.6%.

The current ranking therefore continues to identify **wet-evaporator terminal contact** as the strongest of these first-order penalties.

## Design implication

The current virtual design should not maximize nominal network gain alone. A more appropriate objective is multi-condition gain, for example:

\[
J = w_0 Q_{nominal} + w_1 Q_{wet\ shift} + w_2 Q_{localized\ damage} + w_3 Q_{contact\ loss},
\]

or a conservative objective such as

\[
J_{worst}=\min_i Q_i.
\]

For the currently tested patterns, this pushes the design toward:

- predominantly directed short heat paths;
- limited cross-links rather than a dense fine mesh;
- broad/robust terminal contact pads at wet evaporators;
- compliant bridges between terminals;
- redundancy concentrated near critical evaporator connections instead of uniformly everywhere.

## Important limitations

The three penalties are still stylized:

- stretch does not generate new cracks automatically;
- contact loss uses an imposed coefficient map rather than pressure mechanics;
- conductor fracture is binary cell removal;
- wet islands are static during each solve;
- curvature and compression are absent;
- external air exchange remains low order.

The result is therefore a **design-screen ranking under stated failure maps**, not a predicted service-life retention percentage.

## Next work

1. pressure/compression-dependent contact around wet terminals;
2. moving wet islands during deformation;
3. stretch-triggered fracture/contact maps rather than independent imposed maps;
4. optimize redundancy spatially instead of blending two fixed score fields;
5. add added-mass and visual-width penalties to the network objective.
