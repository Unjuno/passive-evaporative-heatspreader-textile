# Passive Evaporative Heat-Spreader Textile

Open research on a passive personal-cooling garment that combines whole-garment heat spreading, directional moisture transport, capillary liquid delivery, and high-surface-area exterior evaporation.

## Concept

The primary architecture is fully passive: no onboard fan is required.

1. A skin-side layer transports liquid sweat outward.
2. A lightweight in-plane heat spreader redistributes body heat over the garment.
3. Capillary transport routes liquid toward exterior evaporation zones.
4. Exterior micro-ribs, short fins, 3D-knit relief, pile-like structures, or related high-area textures evaporate water to ambient air.
5. Dry exterior regions may be thermally shielded from hot ambient air to reduce parasitic inward heat flow.

The design goal is not simply to evaporate more water. It is to increase the fraction of evaporation that is thermally coupled to the wearer while remaining wearable, washable, flexible, and visually acceptable as normal apparel.

## Current status

This repository currently contains numerical screening models and experimental protocols. Physical garment performance has not yet been validated.

Current model targets for a 0.30 m² active-area equivalent at 35 °C, 70% RH, 150 g/h water supply, and nominal still-air conditions include:

- compare against a flat fast-dry textile at the same liquid-water input;
- use artificial-skin heater power at 34 °C as the primary cooling metric;
- treat an approximately +10 W cooling advantage as a provisional PASS threshold;
- treat an approximately +20 W advantage as a provisional STRONG PASS threshold;
- experimentally determine the effective accessibility of added exterior area rather than assuming all geometric area is useful.

These thresholds are research decision rules, not measured product claims.

## Key model variables

For a rectangular-rib screening geometry:

\[
G_{panel} \approx 1 + \frac{2h}{p}
\]

\[
M \approx 1 + \alpha f (G_{panel}-1)
\]

where:

- `h` = rib height;
- `p` = rib pitch;
- `f` = fraction of active projected garment area covered by ribbed evaporative panels;
- `alpha` = fraction of added geometric rib area that is effectively accessible for independent heat and mass exchange;
- `M` = effective exterior exchange multiplier relative to a flat wet textile.

The principal unresolved parameter is `alpha`, because dense exterior structures may share a humid boundary layer and therefore fail to use all of their geometric surface area.

## Repository map

- `docs/technical-disclosure.md` — integrated technical description and embodiments
- `docs/roadmap.md` — research and publication roadmap
- `docs/experiment-plan.md` — staged physical validation plan
- `docs/prior-art.md` — prior-art map and known adjacent technologies
- `models/governing-equations.md` — equations, assumptions, variables, and checks
- `simulations/passive_rib_screen.py` — reproducible screening model
- `experiments/README.md` — experiment structure and data requirements
- `data/README.md` — data conventions
- `figures/README.md` — figure conventions
- `AUDIT.md` — repository completeness and uncertainty audit

## Important physical clarification: sweat salts

At garment temperatures, sweat salts are treated as nonvolatile. Water evaporates; dissolved salts remain in the liquid/solid phases. Any salt removal mechanism discussed in this project must therefore involve physical removal of salt-containing liquid or solids, not evaporation of salt.

## Scope

The core research focus is the passive architecture. Optional variants may include external airflow, auxiliary fans, humidity-responsive vents, different heat-spreader topologies, or gas-phase moisture-capture layers, but those are secondary embodiments unless explicitly stated otherwise.

## License

Apache License 2.0. See `LICENSE`.

## Citation

See `CITATION.cff` once a stable release is created.
