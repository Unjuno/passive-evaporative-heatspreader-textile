# Prior-Art and Adjacent-Technology Map

Status: **release-candidate technical map**  
Working-note cross-check: 2026-08-20  
Authoritative patent-office family/claim verification: **OPEN**

This file identifies close public technical work and records what the repository does **not** treat as a unique premise. It is not a legal opinion and does not assert novelty, patentability, invalidity, non-infringement, or freedom to operate.

Detailed patent-publication notes and the distinction between public-index cross-checks and authoritative office verification are maintained in [`patent-notes.md`](patent-notes.md).

## 1. Integrated heat conduction + sweat transport — i-Cool textile

**Peng, Y. et al. “Integrated cooling (i-Cool) textile of heat conduction and sweat transportation for personal perspiration management.” Nature Communications 12, 6122 (2021).**  
DOI: `10.1038/s41467-021-26384-8`

Reported concept: integration of heat-conductive pathways with water-transport channels to improve sweat evaporation and cooling.

### Consequence for this repository

A broad concept such as “heat-conductive textile path + sweat-transport path + evaporative cooling” is not treated as new here.

The current repository instead documents a more specific integrated design methodology involving distributed pressure-aware wet terminals, explicit heat-routing topology and contact burden, boundary-layer-aware exterior microstructure, hot-ambient protection, liquid-network pressure/failure modeling, and apparel robustness.

Those combinations are disclosed here without asserting that every element or combination is legally novel.

## 2. Directional liquid transport — skin-like fabric

**Lao, L.; Shou, D.; Wu, Y. S.; Fan, J. T. “Skin-like fabric for personal moisture management.” Science Advances 6, eaaz0013 (2020).**  
DOI: `10.1126/sciadv.aaz0013`

Reported concept: directional liquid-water transport through wettability-structured channels.

### Consequence

Directional sweat transport is treated as an available subsystem/building block, not as the project’s defining premise.

## 3. Humidity-responsive adaptive ventilation

**Li, X. et al. “Metalized polyamide heterostructure as a moisture-responsive actuator for multimodal adaptive personal heat management.” Science Advances 7, eabj7906 (2021).**  
DOI: `10.1126/sciadv.abj7906`

Reported concept: moisture-responsive textile structures that alter convection, evaporation, and radiative heat transfer without electrical power.

### Consequence

Humidity-responsive vents/flaps remain optional embodiments, not core requirements.

## 4. Directional sweat pumping / enlarged evaporation area

**Zhu, R. et al. “Sweat-pumping cooling fabric for enhanced power generation and comfort.” Nature Communications 17, 4374 (2026).**  
DOI: `10.1038/s41467-026-70856-8`

Reported concept: directional/liquid-diode sweat transport, outward spreading, evaporation, cooling, and coupled power-generation functions.

### Consequence

Outward sweat pumping and evaporation-area enlargement are treated as established research directions. The present record therefore does not rely on either one alone as its technical distinction.

## 5. Close patent-publication families / adjacent implementations

The current working patent map includes:

- `JPH04209808A` — sorbent/heat-storage cooling garment; public-index text includes an exterior-fin embodiment;
- `WO2005063065A1` / `JPWO2005063065A1` — fan-based air-conditioning garment family promoting sweat evaporation through body-parallel airflow;
- `EP1978836A1` / `EP1978836B1` — breathable multi-purpose clothing / climate-zone textile structures relevant to structured moisture transport and air channels;
- `US20110283722A1` / `US8443463B2` — supplied-liquid wicking evaporative garment;
- `US20240125016A1` / `US12209335B2` — moisture-management 3D-knitted spacer fabric;
- `WO2010082204A1` — fabric evaporation medium with salt-deposition/removal considerations.

See [`patent-notes.md`](patent-notes.md) for bibliographic fields, technical relevance, and claim-scope caveats.

### Important claim-scope rule

An embodiment described in patent specification text must not be rewritten here as though it were necessarily an independent-claim limitation. In particular, the current working note for `EP1978836` records that the surfaced independent EP claim is directed to coordinated climatic zones / air-channel clothing; rib/capillary description should therefore be treated as specification-level adjacent disclosure unless exact claim dependencies are verified.

## 6. Concepts explicitly not treated as unique premises

The repository should not present any of the following individually as its defining contribution:

- sweat evaporation cools a wearer;
- capillary textiles transport liquid;
- directional wetting transports sweat outward;
- conductive textile elements redistribute heat;
- increasing suitably exposed wet area can increase evaporation;
- ribbed/structured textiles can transport and release moisture;
- 3D spacer knits can move moisture outward and increase exposure to air;
- supplied water can be distributed through wicking clothing for evaporation;
- humidity-responsive textile vents can alter heat/mass transfer;
- onboard fan garments can accelerate sweat evaporation;
- sorbent/desiccant garment cooling;
- exterior fins by themselves;
- 3D fabric evaporation of salt-containing liquid.

## 7. What this repository actually records

The useful public record is the **integrated architecture and failure-aware design methodology**, including combinations of:

- directional/local liquid collection;
- short distributed two-scale capillary routing;
- exterior wet terminal placement based on local pressure and ambient access;
- deliberately engineered low-profile evaporative microstructure;
- explicit accessible-area / boundary-layer analysis rather than geometric area alone;
- short routed flexible heat spreading with contact/topology burden;
- dry-side hot-ambient protection;
- stretch/contact/fracture/load failure screens;
- explicit dense/sparse liquid-network pressure calculations;
- nonvolatile-solute mass balance and separate local-deposition failure treatment;
- concrete apparel-compatible embodiments and benchmark protocols.

This framing is deliberately narrower and more candid than claiming ownership of the individual building blocks above.

## 8. Stable-release source verification remaining

Before the stable release uses patent-family facts as final bibliographic assertions:

1. verify patent publication numbers and earliest relevant dates from authoritative patent-office records;
2. verify family relationships actually relied upon in the release summary;
3. inspect the closest independent claims rather than relying only on abstracts/specification excerpts;
4. use original-language text where machine translation could materially affect interpretation;
5. keep legal status separate from technical prior-art relevance unless legal status is genuinely needed.

This is a publication-integrity task. It is **not** a reason to resume open-ended thermal/fluid modeling.

## 9. Interpretation rule

A statement that an architecture is “the project concept” means only that the repository documents that architecture. It is not a legal conclusion that the architecture, subsystem, or combination is novel or inventive.
