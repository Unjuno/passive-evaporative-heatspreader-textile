# Collector fouling / hydraulic-radius-loss screen

Status: **computational failure-mode screen only; no physical textile specimen exists.**

This note adds a progressive collector-radius-loss failure mode to the sparse two-scale liquid-network model.

## Physical interpretation

The model does **not** allow salt to evaporate:

\[
J_{salt,vapor}=0.
\]

Dissolved nonvolatile material can remain in liquid, reach a terminal, or deposit after local water loss. This screen does not predict deposition chemistry or kinetics. It imposes an inward hydraulic-radius loss `delta` and asks when the capillary safety margin falls below 3.

For collector cells:

\[
r_{eff}(x,y)=\max\left(r_{min},r_0-\delta(x,y)\right)s_p(x,y),
\]

where `s_p` is the existing pressure-linked radius-retention factor. Edge conductance remains

\[
G_e=\frac{\pi r_e^4}{8\mu L_e}.
\]

Thus small local radius loss can strongly increase viscous burden.

## Reference geometry

The reference screen uses the existing sparse-network conditions:

- 60 mm computational tile;
- tile flow ~1.8 g/h, scaled from 150 g/h over 0.30 m²;
- 200 µm-class sparse trunks;
- 60 mm trunk pitch;
- 35, 40 or 50 µm nominal collector radius;
- 15 mm lift;
- synthetic backpack + shoulder-strap pressure field;
- localized sweat-source challenge;
- sampled trunk-grid phase offsets;
- capillary safety target `drive / max pressure >= 3`.

## Uniform-film result

Direct network re-solves give the following first 1 µm-grid failure boundaries:

| collector radius | largest tested uniform inward deposit still passing SF=3 | first tested failing deposit | initial worst margin |
|---:|---:|---:|---:|
| 35 µm | ~3 µm | ~4 µm | ~3.95 |
| 40 µm | ~8 µm | ~9 µm | ~5.86 |
| 50 µm | ~18 µm | ~19 µm | ~11.30 |

The result materially changes interpretation of the earlier minimum-volume choice. A 35 µm collector at 60 mm trunk pitch is hydraulically feasible when clean, but has little radius-loss margin. A 50 µm collector consumes slightly more ideal filled-network volume while providing much larger collapse/fouling tolerance in this screen.

## Localized deposit result

The same mean deposit can be more damaging when concentrated into a small fraction of the collector network.

For deposits concentrated into 20% of cells, worst tested seeds/offsets gave approximately:

- 35 µm collector: mean 1 µm passes; mean 2 µm can fail SF=3;
- 40 µm collector: mean 3 µm passes; mean 5 µm can fail;
- 50 µm collector: mean 5 µm passes; mean 8 µm can fail.

This is a fault-morphology result, not a claim that actual sweat residue deposits in this pattern.

## Design implication

The current liquid design should not minimize clean-state liquid volume alone. Collector selection should include at least:

1. clean-state capillary margin;
2. trunk pitch and phase;
3. localized source position;
4. pressure-linked radius collapse;
5. nonvolatile-deposit / contamination radius-loss allowance;
6. cleaning and replaceability of evaporation terminals.

At the present screening level, 40–50 µm collectors are more defensible robustness anchors than the clean-state minimum-volume 35 µm point when 60 mm trunk pitch is retained.

## Uncertainty / limitations

- `delta` is an imposed failure variable, not a time-dependent deposition prediction;
- deposit morphology, adhesion, dissolution and wash reset are not modeled;
- the collector is represented as an equivalent cylindrical hydraulic radius;
- correlated local plugs may be worse than the sampled random fields;
- salt, organics and other sweat constituents are not separated chemically;
- there is no measured textile permeability, pore distribution or clogging threshold.

## Falsifiable future validation

If a specimen is ever built, a direct validation can measure pressure-flow curves before and after controlled nonvolatile loading, compare inferred hydraulic-radius loss with the model, and test whether local blockage produces earlier failure than an equal-mass uniform deposit.
