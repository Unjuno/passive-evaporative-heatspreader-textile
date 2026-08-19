# Integrated Technical Disclosure

Version: 0.1 pre-release  
Date: 2026-08-19

## 1. Technical field

This project concerns wearable passive thermal management, evaporative cooling textiles, directional liquid transport, capillary-fed evaporation, flexible heat spreading, high-surface-area textile structures, and ambient-air renewal around wet exterior structures.

## 2. Problem statement

Conventional fast-dry garments can move sweat away from skin and expose it to ambient air, but cooling is limited by local sweat availability, local heat supply, exterior mass-transfer resistance, humidity, and the coupling between the wearer and the evaporation site. A garment that simply adds geometric surface area may fail if adjacent surfaces share the same humid boundary layer. A highly conductive exterior may also become harmful in hot ambient conditions if dry regions collect heat from the environment and conduct it inward.

A further limitation is that a narrow or covered wet corridor can contain nonzero buoyancy-driven flow while still becoming nearly saturated. Therefore the disclosed architecture treats heat transport, liquid transport, evaporation geometry, **ambient access topology**, and dry-side thermal protection as one coupled system.

## 3. Core architecture

A representative garment comprises:

1. **Skin-side directional liquid-transport layer.** Liquid sweat is preferentially transported away from the skin.
2. **Flexible in-plane heat-spreader layer.** Heat is redistributed laterally over a substantial fraction of the garment area so that dry or weakly sweating body regions can thermally feed active evaporation regions.
3. **Distributed liquid-transport network.** Capillary channels, yarns, porous strips, grooves, or equivalent structures deliver liquid to exterior evaporation regions.
4. **High-surface-area exterior evaporation structure.** Examples include micro-ribs, short fins, 3D-knit relief, pile, looped structures, hair-like filaments, lamellae, pleats, scales, porous relief, or combinations thereof.
5. **Ambient-air renewal topology.** Wet microstructures may be arranged in discontinuous fields connected to laterally open valleys, cross-openings, spacer paths, pleat gaps, segmented grooves, ambient-connected gaps, or covered/end-renewed channels.
6. **Optional dry-side shielding.** Exterior regions that are not actively wet may use low-conductivity, reflective, porous, or otherwise thermally resistive layers to reduce inward heat gain under ambient temperatures above skin temperature.

The primary embodiment is passive and uses no onboard fan.

## 4. Heat-spreader embodiments

The heat-spreader may be continuous or discontinuous and may include:

- thin conductive films;
- metallized or carbon-based textile elements;
- graphite-like sheets or strips;
- conductive yarn meshes;
- anisotropic networks aligned toward evaporation zones;
- serpentine conductors that accommodate stretch;
- island-bridge structures;
- redundant meshes that preserve partial conductivity after local damage;
- laminated, knitted, woven, printed, coated, or embroidered conductive paths.

Anisotropy may be intentional. Where evaporative panels form bands or preferred regions, higher in-plane thermal conductivity may be aligned toward those regions.

## 5. Exterior evaporation embodiments

The exterior evaporation structure is not restricted to exposed bristles. It may be integrated into normal apparel aesthetics as:

- 3D-knit ribs;
- short rounded fins;
- diagonal lamellae;
- low-profile pleats;
- patterned pile;
- scale-like textures;
- seam-integrated fins;
- panelized rib fields;
- mixed-height structures;
- sparse or graded structures intended to reduce humid-boundary-layer overlap.

The exterior structure may cover the entire garment or selected panels such as the back, chest, sides, shoulders, sleeves, or combinations thereof.

### 5.1 Hierarchical microstructure + ambient-access topology

The high-area wet structure may be arranged at two or more length scales.

A first scale provides local wetted area, for example micro-ribs, loops, short fins, porous relief, pile, or 3D knit.

A second scale provides ambient access, for example:

- unroofed valleys exposed to ambient air continuously along their length;
- widened grooves between rib fields;
- transverse openings that interrupt a long valley;
- intersecting open channels;
- discontinuous evaporator islands separated by ambient-connected gaps;
- spacer-knit openings;
- pleat gaps;
- seam or panel boundaries functioning as air-renewal paths;
- branched or diagonal open paths aligned with likely body motion or environmental airflow.

The ambient-access feature need not generate one particular flow direction. It may operate with upward, downward, reversing, intermittent, motion-driven, or externally driven flow.

### 5.2 Laterally open valleys

One disclosed embodiment uses a shallow valley with no continuous roof. The wet floor and/or valley edges may contain capillary-fed ribs, porous textile, 3D-knit relief, or other evaporative structures. Ambient air can exchange with the valley through its open top and/or sides along the valley length rather than only through two end openings.

Representative starting research dimensions include, without limitation:

- valley width approximately 3–15 mm;
- valley depth/open height approximately 1–5 mm;
- local wet microstructure approximately 1–3 mm high;
- uninterrupted segment lengths approximately 10–100 mm, including approximately 20–50 mm segmented variants.

The valleys may form stripes, chevrons, grids, branches, curves, seams, decorative panel boundaries, or other apparel-compatible patterns.

### 5.3 Segmented valleys and evaporator islands

A valley or wet field may be interrupted by transverse openings, dry gaps, widened nodes, perforations, or crossing ambient paths. Separate wet islands may be thermally connected by the heat spreader and hydraulically connected by capillary branches while remaining aerodynamically separated by open gaps.

Representative island dimensions may be approximately 5–30 mm with approximately 1–10 mm ambient-connected gaps as starting research ranges.

### 5.4 Covered/end-renewed corridors

Another disclosed embodiment uses a corridor with a roof or cover and ambient connection primarily at two ends. The corridor floor and optionally sidewalls may be wet and capillary fed.

Representative research dimensions include, without limitation:

- width approximately 3–10 mm;
- depth approximately 2–5 mm;
- end-to-end length approximately 20–200 mm.

Passive still-air screening indicates that long covered/end-renewed corridors may approach saturation under hot/humid conditions. They remain disclosed as comparison structures, protected channels, externally assisted channels, motion-assisted channels, or fan-assisted variants.

## 6. Representative rib geometry

For rectangular-rib screening, a local geometric surface multiplier is approximated as:

\[
G_{panel} \approx 1 + \frac{2h}{p}
\]

where `h` is rib height and `p` is rib pitch.

An earlier phenomenological whole-garment effective exchange multiplier is modeled as:

\[
M \approx 1 + \alpha f (G_{panel}-1)
\]

where `f` is projected-area coverage of ribbed panels and `alpha` represents the fraction of added geometric area that is actually effective for exchange.

`alpha` captures boundary-layer overlap, incomplete wetting, shielding by neighboring structures, collapse, and related losses. The model therefore does not equate geometric area with useful evaporation area.

Later models separate sensible heat exchange and vapor mass exchange and do not require the same multiplier for both.

## 7. Representative design ranges for testing

Current screening work includes, without limiting the disclosure:

- projected active garment area: approximately 0.1–1.0 m²;
- rib/fin height: approximately 0.2–10 mm;
- rib/fin pitch: approximately 0.2–10 mm;
- exterior structured-panel coverage: approximately 10–100% of active projected area;
- open ambient-access path width: approximately 0.5–30 mm;
- open-path depth/height: approximately 0.5–10 mm;
- uninterrupted wet-field or valley length: approximately 5–300 mm;
- flexible heat-spreader effective body-to-evaporator coupling explored over tens to hundreds of W/(m² K);
- still-air, walking-air, and externally forced-air operation;
- ambient relative humidity from dry conditions through high-humidity failure regimes.

A current aesthetic/performance candidate band for bench testing is roughly 55–70% structured-panel coverage, 2–3 mm local microstructure height, 0.8–1.5 mm local pitch, and laterally open/segmented ambient-access features. These values are research ranges and not product claims.

## 8. Water and salt transport

Water and nonvolatile sweat solutes are treated separately.

- Liquid water and dissolved solutes can be transported through the garment.
- Water can undergo liquid-to-vapor phase change at exterior evaporation regions.
- Under garment-temperature conditions, salt vapor flux is taken as zero.
- As water evaporates, dissolved salts remain, concentrate, and may crystallize.
- Any intentional salt removal requires removal of salt-containing liquid or solids; salt is not assumed to evaporate.

Internal transport routes may be protected from distributed evaporation so that phase change occurs preferentially at accessible exterior terminal regions. Alternatively, ordinary washable textile architectures may tolerate salt deposition without dedicated salt-management components if testing shows no abnormal performance loss relative to conventional garments.

## 9. Hot-ambient behavior

When ambient temperature exceeds skin or garment temperature, a dry high-conductivity exterior or an aggressively ventilated cooler surface can receive environmental sensible heat. Embodiments therefore include:

- thermal shielding over dry areas;
- selective exposure of wet evaporative zones;
- reduced through-thickness conductivity where external heat pickup is undesirable;
- high in-plane but lower through-thickness conductivity;
- segmented or routed heat spreaders;
- humidity/wetting-responsive exposure mechanisms;
- ambient-access geometry arranged so that increased air exchange does not unnecessarily expose dry conductive regions.

## 10. Optional embodiments

Secondary embodiments include:

- externally supplied airflow;
- onboard auxiliary fans;
- walking- or motion-induced ventilation;
- passive humidity-responsive vents or flaps;
- gas-phase water-capture layers, including porous sorbent materials, coupled to liquid transport or regeneration zones;
- detachable or replaceable exterior evaporation panels;
- replaceable crystallization/wash zones;
- liquid brine purge, where salt-containing liquid is physically removed;
- garments with localized rather than whole-body heat spreading;
- garments in which conductive paths and decorative patterns are the same structure;
- combinations of open and covered air-renewal paths in one garment.

These are alternatives; the primary concept does not require them.

## 11. Failure modes intentionally included in the disclosure

The architecture may fail or lose advantage when:

- ambient humidity reduces vapor-pressure driving force;
- exterior structures are so dense that they share a humid boundary layer;
- covered corridors become internally saturated despite nonzero airflow;
- long channels have large axial Péclet number but insufficient retained vapor driving force;
- ribs/fins collapse or remain dry;
- contact resistance prevents body heat from reaching evaporation regions;
- dry exterior conductive areas collect heat from hotter ambient air;
- stronger ventilation increases sensible heat input enough to offset latent benefit;
- liquid transport is insufficient, causing dry-out;
- liquid transport is excessive, causing runoff rather than evaporation;
- salt or contamination degrades wetting or capillary transport;
- mechanical stretch or washing breaks conductive paths;
- open valleys are blocked by compression, backpack contact, garment layers, or body posture.

These are not excluded cases; they define engineering boundaries to be tested.

## 12. Testable central hypothesis

At equal liquid-water input and equal ambient conditions, a garment combining lateral heat spreading with capillary-fed high-area exterior evaporation and sufficient ambient-air access can remove more heat from an artificial skin than a conventional flat fast-dry textile.

The primary proposed test compares required heater power to maintain an artificial skin at 34 °C. A larger heater requirement indicates greater heat removal by the garment.

Secondary mechanism tests compare dense microstructures, covered corridors, laterally open valleys, segmented valleys, and discontinuous evaporator fields while measuring heater power, water balance, local RH/T, and signed local airflow.

## 13. Interpretation

This document discloses a system architecture and multiple concrete implementation families. Numerical values in this repository are simulation outputs or screening assumptions unless explicitly labeled as measurements. No physical performance claim should be inferred until bench data are published.
