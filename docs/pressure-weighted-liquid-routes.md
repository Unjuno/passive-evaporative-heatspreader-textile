# Pressure-weighted liquid routing and protected escape trunks

Status: **SIMULATION / GEOMETRIC-HYDRAULIC PROXY ONLY — NO PHYSICAL SPECIMEN**

## Question

Pressure-aware wet-terminal placement moves evaporation away from persistent load, but sweat generated inside the loaded zone still has to leave that zone hydraulically. If liquid trunks flatten under pressure, the first part of the route can dominate the burden.

## Model

A synthetic backpack+strap pressure field is converted to local compression using the same `cmax=0.5` screen as the thermal pressure model.

Equivalent hydraulic-radius retention is prescribed as

\[
\eta_r(x,y)=1-s_c c(x,y),
\]

where `s_c` is a **hypothetical collapse-severity coefficient**.

Circular-channel resistance scaling is then used as a spatial route cost:

\[
w(x,y)\propto \eta_r^{-4}.
\]

A grid shortest-path calculation finds the least weighted cost from each source cell to the nearest wet terminal.

This is not a full capillary network solution. The cost is reported in mm-equivalent weighted route length.

## Main finding

Moving the wet terminal to low-pressure regions does not automatically reduce liquid-route burden. If sources remain distributed over the whole loaded tile, fluid generated under the load must still traverse an initially compressed region.

At collapse severity 0.5 in the 24 x 24 development screen:

| layout | unprotected p95 hydraulic path | radius-floor 0.90 | fully protected |
|---|---:|---:|---:|
| four islands | ~25.6 mm-eq | ~19.1 | ~15.0 |
| pressure-focused | ~49.0 | ~33.5 | ~22.5 |
| regularized | ~47.3 | ~30.5 | ~20.0 |

Thus the long-route penalty of pressure-aware terminals is strongly affected by whether the **early escape trunk** preserves its cross-section.

## Interpretation

The current architecture should distinguish:

1. **local collection under load** — short wetting/collection path;
2. **protected escape trunk** — the first liquid path that exits the high-pressure patch;
3. **lower-pressure transport / terminal region** — where ordinary flexible capillary routing can resume;
4. **exterior terminal** — where evaporation is intentionally allowed.

This is analogous to thermal routing: the loaded region can remain a source region while the phase-change terminal is elsewhere.

## Why protect only the escape section?

The screen suggests a large fraction of the pressure-weighted hydraulic penalty comes from crossing the loaded region. It may therefore be unnecessary to make every liquid route mechanically stiff. Protecting the short exit path can capture much of the benefit with lower thickness/material burden.

Possible implementation families include:

- arch/bridge protected trunks across strap contact;
- grooved channels beneath local spacer ribs;
- redundant parallel trunks leaving the pressure region in several directions;
- local vertical-through-thickness transfer into a protected plane followed by lateral routing.

## Important uncertainty

- the pressure-to-radius relation is hypothetical;
- flattened noncircular channels do not exactly follow cylindrical `r^-4` scaling;
- the route model ignores capillary head and flow sharing at junctions;
- uniform source distribution is assumed;
- protected-radius floor is an effective parameter, not a structural specification;
- route cost does not include salt deposition or priming.

## Design conclusion

> Pressure-aware evaporator relocation should be paired with a pressure-resistant **short liquid escape path** out of the loaded source region. Moving the terminal alone is incomplete.

## Next work

1. combine this weighted route cost with the capillary flow/head equations instead of using a geometric proxy;
2. optimize several escape directions for strap/backpack maps;
3. include heat and liquid escape paths in one regional garment tile;
4. add curvature and seam obstacles;
5. map a chosen protected trunk geometry to pressure-collapse behavior.
