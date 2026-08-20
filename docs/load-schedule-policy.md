# Quasisteady load-schedule policy screen

Status: **SIMULATION / VIRTUAL PROTOTYPE ONLY — NO PHYSICAL SPECIMEN**

## Question

Is it worth adding active or switchable wet-terminal control so the evaporator layout changes when the wearer goes from no load to shoulder straps, backpack contact or seated contact?

This screen composes the static spatial-pressure states from `spatial_pressure_layout.py`. It is intentionally quasisteady: there is no transient wicking, valve, flap or control-system dynamics.

## Hypothetical usage schedules

The schedule fractions are design scenarios, not measured user behavior.

### Commuter backpack

- no load: 20%;
- shoulder straps: 15%;
- backpack + straps: 65%.

### Seated office

- no load: 45%;
- seat-back contact: 55%.

### Mixed day

- no load: 25%;
- backpack panel: 20%;
- shoulder straps: 15%;
- seat back: 20%;
- backpack + straps: 20%.

## Policies

### Fixed

One wet-layout pattern is used for every state.

### Ideal adaptive

For each load state, the model is allowed to select whichever tested wet layout gives the largest body-side heat flux. This is an optimistic upper bound because switching cost and transient water redistribution are ignored.

## 24 x 24 reference result

| schedule | best fixed | adaptive uplift over 0.195 m² | relative uplift | break-even control penalty |
|---|---|---:|---:|---:|
| commuter backpack | pressure-aware | ~0.10 W | ~0.45% | ~0.44% |
| mixed day | pressure-aware | ~0.13 W | ~0.55% | ~0.55% |
| seated office | pressure-aware | ~0.23 W | ~0.97% | ~0.96% |

The ideal adaptive policy mostly switches only between:

- ordinary four-island layout when unloaded; and
- pressure-aware layout when loaded.

## Design conclusion

The current model does **not** justify a complex active wet-terminal switching mechanism. The screened benefit is small enough that a sub-percent control/actuation/pumping/redistribution penalty can erase it in the 24 x 24 reference.

Therefore the current priority is:

> use a robust fixed pressure-aware architecture in load-prone garment zones, rather than add active wet-layout switching solely for backpack/seat state changes.

This conclusion can change if future models introduce strongly different pressure fields, active cooling, substantially nonuniform sweat availability, or a nearly lossless passive switching mechanism.

## Why keep adaptive embodiments in the disclosure?

Although not preferred as the current product direction, switchable embodiments remain technically relevant:

- capillary valves selecting different terminal pads;
- pressure-responsive passive valves;
- mechanically exposed/covered wet panels;
- reversible liquid routing between terminal groups;
- humidity/pressure-responsive flaps.

These should be described as alternatives rather than the baseline architecture.

## Limitations

- static states are time-averaged; transition dynamics are omitted;
- schedule fractions are hypothetical;
- current pressure-aware rule itself is not globally optimized;
- liquid redistribution time and stored liquid inventory are omitted;
- control energy and added mass are represented only through a break-even penalty, not explicit hardware models.

## Next work

Given the small adaptive upside, numerical effort should move toward passive structural robustness:

1. geometry-resolved protected vapor channels under load;
2. curvature + pressure + contact coupling;
3. capillary routing to fixed low-pressure terminal fields;
4. full garment mass/thickness budget;
5. hot/humid virtual prototype maps.
