# Integrated Technical Disclosure

Version: 0.1 pre-release  
Date: 2026-08-20

## 1. Technical field

This project concerns wearable passive thermal management, evaporative cooling textiles, directional liquid transport, capillary-fed evaporation, flexible heat spreading, high-surface-area textile structures, ambient-air renewal around wet exterior structures, and management of sensible heat pickup from hot ambient air.

## 2. Problem statement

Conventional fast-dry garments can move sweat away from skin and expose it to ambient air, but cooling is limited by local sweat availability, local heat supply, exterior mass-transfer resistance, humidity, and coupling between the wearer and evaporation site.

A garment that merely adds geometric surface area may fail when adjacent wet surfaces share one humid boundary layer. A narrow or covered wet corridor may contain nonzero flow while remaining nearly saturated. A conductive or aggressively ventilated exterior may also receive enough sensible heat from hot ambient air to reduce or reverse body-side cooling.

The disclosed architecture therefore treats heat routing, liquid routing, evaporation geometry, ambient-access topology, liquid supply, and hot-ambient thermal protection as one coupled system.

## 3. Core architecture

A representative garment comprises:

1. **Skin-side directional liquid-transport layer.** Liquid sweat is preferentially transported away from skin.
2. **Flexible in-plane heat-spreader layer.** Heat is redistributed laterally over a substantial garment area toward active wet evaporation regions.
3. **Distributed liquid-transport network.** Capillary yarns, porous strips, grooves, channels, meshes, or equivalent structures deliver liquid to exterior wet regions.
4. **High-surface-area exterior evaporator.** Examples include micro-ribs, short fins, 3D-knit relief, pile, loops, filaments, lamellae, pleats, scales, porous relief, or combinations.
5. **Ambient-access topology.** Wet microstructures may be arranged with unroofed valleys, side openings, transverse openings, spacer paths, pleat gaps, discontinuous fields, ambient-connected gaps, or covered/end-renewed comparison channels.
6. **Optional thermal shielding/routing.** Dry conductive regions and/or selected ambient-facing paths may be thermally isolated, shielded, or anisotropically routed to reduce harmful inward sensible heat gain.

The primary embodiment is passive and requires no onboard fan.

## 4. Heat-spreader embodiments

The heat spreader may be continuous or discontinuous and may include:

- thin conductive films;
- metallized or carbon-based textile elements;
- graphite-like sheets or strips;
- conductive-yarn meshes;
- anisotropic networks aligned toward evaporation zones;
- serpentine conductors accommodating stretch;
- island-bridge structures;
- redundant meshes preserving partial conductivity after local damage;
- laminated, knitted, woven, printed, coated, or embroidered conductive paths.

Anisotropy may be intentional. Higher in-plane conductivity may be directed toward defined wet panels while through-thickness or dry-region heat pickup is restricted.

## 5. Exterior evaporation and ambient-access embodiments

The exterior evaporator need not resemble exposed bristles. It may be integrated into normal apparel aesthetics as:

- 3D-knit ribs;
- short rounded fins;
- diagonal lamellae;
- low-profile pleats;
- patterned pile;
- scale-like textures;
- seam-integrated fins;
- panelized rib fields;
- mixed-height structures;
- sparse or graded wet structures.

The exterior may cover the entire garment or selected back, chest, side, shoulder, sleeve, or other panels.

### 5.1 Hierarchical microstructure + ambient access

A first length scale supplies wet area through ribs, loops, short fins, porous relief, pile, or 3D knit.

A second length scale connects the wet field to ambient air through one or more of:

- unroofed valleys exposed continuously along their length;
- side-open grooves;
- widened gaps between wet fields;
- transverse/cross openings;
- intersecting open channels;
- discontinuous evaporator islands separated by ambient-connected gaps;
- spacer-knit openings;
- pleat gaps;
- seam or panel boundaries functioning as renewal paths;
- branched or diagonal open paths aligned with likely motion or environmental airflow.

The ambient-access feature need not generate one fixed flow direction. It may tolerate upward, downward, reversing, intermittent, externally driven, or wearer-motion-driven flow.

### 5.2 Continuously laterally open valleys

One preferred research embodiment uses a shallow valley with no continuous roof. A wet floor and/or edges contain capillary-fed ribs, porous textile, 3D-knit relief, or another evaporative structure. Ambient exchange occurs continuously through the open top and/or sides rather than only through two axial ends.

Representative starting research dimensions include, without limitation:

- valley width approximately 2–20 mm;
- valley depth/relief approximately 0.5–8 mm;
- local wet microstructure approximately 0.2–5 mm high;
- local microstructure pitch approximately 0.2–10 mm;
- continuously open path lengths from millimeters to garment-panel scale.

Valleys may form stripes, chevrons, grids, branches, curves, seams, decorative panel boundaries, or other apparel-compatible patterns.

### 5.3 Segmented paths and evaporator islands

A wet path may be interrupted by transverse openings, dry gaps, widened nodes, perforations, or crossing ambient paths. Separate wet islands may remain thermally connected by the heat spreader and hydraulically connected by capillary branches while being aerodynamically separated by open gaps.

The disclosure includes both:

- **millimeter-scale interruptions/segments**, including approximately 0.5–5 mm wet lengths or gaps, as high-frequency ambient-access embodiments; and
- **centimeter-scale interruptions**, including approximately 10–100 mm field lengths, as comparison, manufacturing, motion-assisted, externally assisted, or lower-open-area embodiments.

Current low-order diffusion screening indicates that centimeter-scale end openings alone may be too coarse when distributed lateral exchange is weak. This numerical result does not exclude those geometries from use under stronger cross-flow, motion, fan assistance, or other renewal mechanisms.

### 5.4 Covered/end-renewed corridors

Another embodiment uses a roofed or partially covered corridor with ambient connection primarily at its ends. The floor and optionally sidewalls may be wet and capillary fed.

Representative research dimensions include, without limitation:

- width approximately 2–20 mm;
- depth approximately 1–10 mm;
- end-to-end length approximately 5–300 mm.

Passive still-air screening indicates that long covered/end-renewed wet corridors can approach saturation. They remain disclosed as comparison structures, protected flow paths, motion-assisted channels, externally ventilated channels, or fan-assisted variants.

## 6. Representative geometry and exchange metrics

For rectangular-rib screening:

\[
G_{panel}\approx1+\frac{2h}{p}.
\]

An earlier phenomenological mapping was

\[
M\approx1+\alpha f(G_{panel}-1),
\]

where `alpha` represented effective accessibility rather than geometric area alone.

Later models make the ambient-access mechanism more explicit and separate heat from vapor transfer.

For a local laterally open vapor balance:

\[
R=G_a/G_w,
\qquad
F=\frac{R}{1+R},
\]

where `G_a` is ambient-renewal vapor conductance and `G_w` is wet-surface-to-local-air conductance. `F` is the fraction of bulk-to-saturated-wall vapor driving force retained locally.

Absolute vapor-transfer capacity may also be represented by the series conductance

\[
k_{eff}=\frac{k_wk_a}{k_w+k_a}=k_wF.
\]

A high `F` alone is not sufficient because weakening `k_w` can raise `F` while lowering total evaporation capacity.

## 7. Representative research ranges

Without limiting the disclosure, current studies include:

- projected active garment area approximately 0.1–1.0 m²;
- wet/evaporative projected fraction approximately 5–100%;
- rib/fin/relief height approximately 0.1–15 mm;
- rib/fin pitch approximately 0.1–15 mm;
- ambient-connected valley/gap width approximately 0.2–50 mm;
- relief/open depth approximately 0.2–20 mm;
- interrupted wet-field length from sub-millimeter scale to hundreds of millimeters;
- continuous open paths over whole garment panels;
- flexible heat-spreader body-to-wet-zone coupling over tens to hundreds of W/(m² K) in screening models;
- still air, walking/motion air, environmental wind, and forced-air variants;
- dry through high-humidity ambient conditions;
- ambient temperatures below and above nominal skin/wet-surface temperatures.

Current aesthetic bench candidates emphasize low-profile 2–3 mm-class texture with laterally open ambient-connected topology. These are research starting points, not optimized or claimed product dimensions.

## 8. Water and salt transport

Water and nonvolatile sweat solutes are treated separately.

- liquid water and dissolved solutes may move through the garment;
- water may undergo liquid-to-vapor phase change at exterior regions;
- salt vapor flux is taken as zero under garment-temperature conditions;
- salts remain, concentrate, and may crystallize as water is removed;
- intentional salt removal requires physical removal of salt-containing liquid or solids.

Internal liquid paths may be protected from distributed evaporation, or the architecture may simply be designed for ordinary rinsing/washing if comparative testing shows no abnormal degradation relative to conventional sports textiles.

The available liquid supply is also a system constraint. If a fully wet transfer-capacity calculation exceeds the delivered sweat/water rate, the physical state is supply-limited and requires a partial-wetting/dryout treatment rather than extrapolation of the fully wet solution.

## 9. Hot-ambient behavior and environmental sign boundary

When ambient temperature exceeds skin or wet-surface temperature, ambient sensible heat can supply part or all of the latent heat of evaporation and may additionally flow toward the wearer.

For the repository's same-path heat/vapor transfer baseline, zero body-side heat flow reduces to

\[
\frac{k_{air}}{D_v}(T_\infty-T_{skin})
=
L_v\left[
\rho_{v,sat}(T_{skin})
-\phi_\infty\rho_{v,sat}(T_\infty)
\right].
\]

For a 34 °C artificial-skin setpoint, the current model gives example zero-body-flux boundaries near:

- 45.25 °C at 50% RH;
- 42.24 °C at 60% RH;
- 39.73 °C at 70% RH;
- 37.57 °C at 80% RH;
- 36.59 °C at 85% RH;
- 35.68 °C at 90% RH.

This is a low-order model sign boundary, not a medical, physiological, or measured garment limit.

Embodiments addressing hot-ambient operation may include:

- shielding dry conductive regions;
- selective heat routing toward wet zones only when beneficial;
- reduced through-thickness conductivity;
- anisotropic heat spreaders;
- vapor-transfer paths whose sensible heat coupling is separately controlled where physically achievable;
- external heat rejection or airflow conditions different from the passive same-path baseline;
- switching, bypassing, or isolating heat-routing regions when a wet exterior would otherwise conduct environmental heat inward.

## 10. Optional embodiments

Secondary embodiments include:

- external environmental airflow;
- onboard auxiliary fans;
- walking/motion-induced ventilation;
- humidity/wetting-responsive vents or flaps;
- gas-phase water-capture/sorbent layers coupled to transport/regeneration zones;
- detachable exterior evaporators;
- replaceable wash/crystallization regions;
- liquid brine purge, physically removing salt-containing liquid;
- localized rather than whole-garment heat spreading;
- conductive/capillary/evaporative paths integrated into visible decorative patterns;
- combinations of open and covered renewal paths;
- architectures with passive mode below an environmental threshold and reduced/isolated heat coupling above that threshold.

These are alternatives; the primary concept does not require them.

## 11. Failure modes intentionally included

The architecture may lose advantage when:

- ambient humidity removes vapor-pressure driving force;
- microstructures share a humid boundary layer;
- covered corridors saturate despite flow;
- end openings are spaced much farther apart than the relevant exchange length while lateral renewal remains weak;
- high `F` is achieved only by reducing absolute wet-surface transfer;
- ribs/fins collapse, foul, or remain dry;
- body-to-wet-zone thermal contact is insufficient;
- dry conductive regions collect hot ambient heat;
- wet exterior sensible heat input offsets latent body cooling;
- evaporation remains positive while net body-side heat flow becomes zero or negative;
- liquid delivery is below transfer capacity, causing partial dryout;
- excess liquid causes runoff;
- salt/contamination degrades wetting;
- stretch/washing damages conductive or capillary paths;
- backpacks, outer garments, seating, or posture close ambient-access paths.

These are engineering boundaries, not exclusions from the disclosure.

## 12. Testable central hypotheses

Primary product hypothesis:

> at equal liquid input and ambient conditions below the relevant passive sign boundary, a garment combining routed heat spreading, capillary-fed high-area wet exterior structures, and sufficient ambient access can remove more heat from an artificial skin than a conventional flat fast-dry textile.

Mechanism hypotheses include:

- continuously laterally open wet fields maintain more vapor driving force than matched covered/end-renewed channels;
- centimeter-scale interruption alone may be insufficient when distributed lateral exchange is weak;
- renewal quality must be paired with absolute evaporation transfer;
- in hot ambient conditions, evaporation rate alone can misidentify a body-heating state as a cooling state;
- liquid supply can become the limiting step under dry/high-transfer conditions.

Primary testing uses artificial-skin heater power, water balance, wet-surface temperature, local T/RH, wet area, and local airflow where measurable.

## 13. Interpretation

This document discloses a system architecture, operating/failure boundaries, and multiple concrete implementation families. Numerical values are simulations, analytic screens, or research ranges unless explicitly labeled as measurements.

No physical garment-performance claim should be inferred until controlled bench measurements are published.
