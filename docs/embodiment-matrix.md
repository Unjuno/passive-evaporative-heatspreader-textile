# Embodiment Matrix

This matrix makes concrete combinations explicit rather than relying only on broad lists of interchangeable elements. It is a technical design-space record, not a legal claim set.

## Common layer vocabulary

- **L1 — skin-side liquid interface:** wicking/directional sweat transport.
- **L2 — heat-spreader:** continuous, anisotropic, mesh, serpentine, or island-bridge thermal path.
- **L3 — liquid distribution:** capillary yarn/channel/porous network.
- **L4 — exterior evaporator:** flat, ribbed, finned, 3D-knit, pile, lamellar, pleated, scale-like, or mixed geometry.
- **L5 — optional environmental control:** dry-side shield, passive vent, or forced airflow.

## E01 — passive micro-rib baseline

- L1: directional liquid transport textile.
- L2: thin flexible whole-area in-plane heat spreader.
- L3: distributed capillary yarn network.
- L4: rounded parallel micro-ribs over 55–70% of active area.
- Representative geometry: 2–3 mm rib height, 0.8–1.0 mm pitch.
- L5: no fan; dry regions may be low-conductivity textile.
- Intended mode: natural evaporation in still or weak ambient airflow.

## E02 — anisotropic routed heat spreader

- L1: directional transport.
- L2: anisotropic spreader with the high-conductivity axis directed from torso regions toward evaporative side/back bands.
- L3: capillary branches parallel or partially parallel to the high-k direction.
- L4: ribbed or 3D-knit evaporative bands.
- L5: optional dry-side shielding.
- Intended mode: improve cooling when sweating/wetting is spatially nonuniform.

## E03 — serpentine stretch garment

- L1: stretch wicking knit.
- L2: serpentine conductive traces designed to retain thermal conductance during 5–30% extension.
- L3: stretch-tolerant capillary yarns.
- L4: short flexible rib/loop evaporators.
- L5: none required.
- Intended mode: sleeves, torso side panels, joints, or athletic garments.

## E04 — island-bridge / redundant mesh

- L1: directional textile.
- L2: thermally conductive islands connected by multiple compliant bridge paths.
- L3: liquid distribution crosses or surrounds islands.
- L4: exterior evaporative panels aligned with high-conductance islands.
- L5: optional insulation over non-wet bridges.
- Intended mode: damage tolerance, bending, repeated laundering.

## E05 — 3D-knit apparel texture

- L1: hydrophobic-to-hydrophilic or otherwise directional thickness gradient.
- L2: conductive yarns integrated into the knit ground structure.
- L3: capillary transport formed by yarn selection and knit topology.
- L4: 3D-knit relief appearing visually as ordinary technical sportswear texture.
- L5: none required.
- Intended mode: low snag risk and aesthetic integration.

## E06 — graded exterior spacing

- L1: directional liquid transport.
- L2: heat spreader.
- L3: capillary feed.
- L4: mixed-height or graded-pitch ribs/fins, with more open spacing near expected humid-plume accumulation regions.
- L5: none required.
- Intended mode: reduce shared humid-boundary-layer overlap while retaining area.

## E07 — lamellar / scale exterior

- L1: directional liquid transport.
- L2: thin heat-spreader sheet or yarn network.
- L3: capillary feed at lamella roots.
- L4: short angled lamellae or overlapping scale-like evaporative structures rather than cylindrical hairs.
- L5: orientation may favor motion-induced airflow.
- Intended mode: reduce visual bulk and snagging while providing exterior area.

## E08 — dry-side shielded hot-weather architecture

- L1: directional liquid transport.
- L2: high in-plane, comparatively lower through-thickness thermal path.
- L3: liquid feed restricted to defined wet panels.
- L4: exposed wet evaporative ribs/fins.
- L5: reflective/insulating/low-conductivity cover over dry conductive regions.
- Intended mode: ambient air hotter than skin, where exposed dry conductor would cause inward heat gain.

## E09 — humidity-responsive exposure

- L1–L4: any passive integrated architecture above.
- L5: moisture-responsive flap or vent exposes wet evaporative panels and/or increases spacing when local humidity rises.
- Intended mode: passive adaptation without electrical power.

## E10 — motion/ambient-air assisted

- L1–L4: integrated architecture.
- L5: external airflow from walking, cycling, wind, vehicle motion, or stationary environmental fans.
- No onboard fan is required.
- Intended mode: exploit available airflow without garment electrical power.

## E11 — auxiliary-fan variant

- L1–L4: integrated architecture.
- L5: one or more onboard fans direct air across or through exterior evaporation zones.
- Intended mode: upper-bound/active variant when power and noise are acceptable.
- This is secondary to the primary passive architecture.

## E12 — gas-phase moisture capture coupled to liquid evaporation

- L1: may include directional liquid handling.
- L2: heat spreader optional or present.
- L3: liquid pathway connected to a hygroscopic or porous sorbent region after captured water is condensed/desorbed into a transportable phase.
- L4: exterior evaporator/regeneration region.
- L5: may use solar/ambient regeneration or airflow.
- Intended mode: secondary research branch; not required for sweat-driven operation.

## E13 — protected internal capillary / terminal evaporation

- L1: sweat collection.
- L2: heat spreader.
- L3: internal liquid channel with comparatively low vapor leakage along its path.
- L4: high-vapor-conductance terminal exterior pad/rib field.
- Intended mode: concentrate phase change at accessible terminal regions and reduce upstream concentration/crystallization risk.
- Salt vapor flux remains zero; salt travels only in liquid/solid phases.

## E14 — washable ordinary-salt-tolerance architecture

- L1–L4: integrated passive architecture.
- No special salt-management component.
- Materials and pore sizes are selected for ordinary rinsing/washing and recovery.
- Intended mode: default if comparative testing shows salt deposition is no worse than normal sports textiles.

## E15 — detachable exterior evaporator panel

- L1: permanent skin-side textile.
- L2: permanent or semi-permanent heat spreader.
- L3: releasable capillary interface.
- L4: removable ribbed/3D-knit evaporative panel.
- Intended mode: cleaning, replacement, alternate climate panels, or experimentation.

## E16 — pattern-as-function apparel

- L1: directional base textile.
- L2: visible decorative lines are conductive heat-routing paths.
- L3: selected pattern branches are capillary liquid paths.
- L4: textured portions of the same visual pattern form evaporative ribs/pleats.
- Intended mode: integrate function into stripes, geometric motifs, seams, or panel graphics rather than adding visible machine components.

## Cross-combination rule

The listed embodiments are not intended to be mutually exclusive. For example, E02 anisotropic heat routing may be combined with E05 3D-knit texture, E08 dry-side shielding, and E09 humidity-responsive exposure. Likewise, E03 serpentine stretch paths may be used under E07 lamellae or E15 detachable panels.

For future updates, newly proposed components should be documented both individually and in at least one concrete complete stack so that the repository records operable combinations rather than only menus of parts.
