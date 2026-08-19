# Close Patent Notes

Status: working patent map; public-index findings require authoritative patent-office verification before stable release.  
Last checked: 2026-08-19.

This file records close patent disclosures found during repository audit. It is not a legal opinion and does not assert novelty/non-infringement.

## P01 — JPH04209808A — cooling garment / sorbent + exterior fins

- Public index publication: JPH04209808A.
- Reported priority/filing date: 1990-11-30.
- Reported publication date: 1992-07-31.
- Public-index text describes moisture-reactive chemical heat-storage/sorbent material, including examples such as lithium bromide, silica gel, zeolite, and calcium chloride.
- An indexed claim/embodiment includes fins outside the heat-storage material.

### Design consequence

Do not treat a broad "desiccant/sorbent cooling garment" or "sorbent garment with exterior fins" as a unique premise of this project.

## P02 — WO2005063065A1 / JPWO2005063065A1 — fan air-conditioning garment

- Public index publication: WO2005063065A1.
- Reported priority: 2003-12-25.
- Family includes a Japanese publication indexed as JPWO2005063065A1.
- Public-index text describes an air-blowing means/fan attached to a garment, creating airflow between garment and body/underwear and promoting sweat evaporation.

### Design consequence

Onboard fan, body-parallel forced airflow, outlet flow through garment openings, and forced sweat evaporation are treated as established building blocks. Fan assistance in this repository is optional/secondary.

## P03 — EP1978836B1 / EP1978836A1 — ribbed capillary moisture transport to exterior evaporation surface

- Title: "Breathable multi-purpose clothing".
- Public index publication: EP1978836B1; corresponding published application EP1978836A1.
- Public index priority date: 2006-01-27.
- Inventor indexed: Bodo W. Lambertz.
- Assignee indexed: X Technology Swiss GmbH.

### Particularly close disclosure

The public patent text describes a wave-shaped textile element producing webs and ribs. The rib base absorbs sweat; rib walls provide a wicking/capillary function transporting sweat away from skin toward webs; the web material releases moisture to the environment for evaporation. The text explicitly states that the evaporation surface is moved away from the skin and describes capillary transport through textile ribs toward the textile surface.

### Design consequence

This is highly relevant. The following broad concept must be treated as pre-existing:

`skin moisture -> capillary textile rib/wall transport -> exterior textile surface -> evaporation`

Therefore, **capillary transport plus an exterior ribbed evaporation surface alone is not a sufficient differentiator** for this repository.

The remaining project-specific search space must be evaluated at a more integrated level, including for example:

- whole-garment/large-area lateral heat redistribution toward spatially nonuniform evaporators;
- intentionally anisotropic/stretchable heat-routing topology;
- explicit optimization of exterior geometry by effective accessible exchange rather than geometric area;
- humid-boundary-layer overlap design;
- hot-ambient dry-side thermal shielding/selective exposure;
- complete combinations of those elements with outward liquid transport.

## P04 — US8443463B2 / US20110283722A1 — externally supplied liquid + wicking evaporative garment

- Title: "Evaporative cooling clothing system for reducing body temperature of a wearer of the clothing system".
- Public index prior-art/priority date: 2008-08-06.
- Published application indexed: US20110283722A1.
- Grant indexed: US8443463B2.
- Inventor indexed: Leslie Owen Paull.

### Close disclosure

The public patent text describes a wicking-fabric clothing article, a liquid reservoir and hollow transport/dispensing section delivering liquid to an upper region, capillary/wicking transfer through the garment, exposure of liquid at a garment region to surrounding air, and evaporation for cooling.

### Design consequence

A broad architecture of:

`liquid supply -> capillary/wicking garment -> distributed wet region -> ambient evaporation -> wearer cooling`

is established prior art. This project therefore cannot rely on liquid distribution and exterior evaporation alone as its defining technical distinction.

## P05 — US12209335B2 / US20240125016A1 — wicking 3D-knitted spacer fabric

- Title: "Wicking structure of 3D-knitted spacer fabric".
- Public index priority date: 2022-10-18.
- Published application indexed: US20240125016A1.
- Grant indexed: US12209335B2.
- Assignee indexed: Honeywell Safety Products USA Inc / Honeywell International Inc in the recorded history.

### Close disclosure

The public text describes a 3D knitted spacer fabric with improved liquid transfer through wicking yarns from the skin-side layer to the outer layer, increasing the area over which liquid is exposed to air and improving evaporation/thermal comfort.

### Design consequence

A 3D textile structure that carries liquid outward and enlarges the evaporation area is also not, by itself, a unique project premise.

## P06 — WO2010082204A1 — 3D knit as liquid evaporation medium with salt deposition

- Title indexed: "Mono-filament fabric device for evaporation of liquids and removal of salt precipitation depositions".
- Public text describes 3D-knit fabric wetted by a salt-containing liquid stream, evaporation from wetted filaments, and cleaning/stretching after salt deposition/clogging.

### Design consequence

3D knit as an evaporation medium, including salt-containing water and cleanability concerns, exists outside wearable cooling. This is relevant to the terminal-evaporator and salt-tolerance variants even though the application context differs.

## Combined prior-art implication

The repository should avoid treating any of the following individually as its core distinction:

- capillary sweat transport;
- outward moisture transport;
- ribbed textile capillary transport to an exterior evaporative surface;
- 3D spacer knit for outward moisture transfer/evaporation;
- externally supplied liquid distributed through wicking clothing;
- fan-assisted sweat evaporation;
- sorbent garment cooling;
- exterior fins by themselves.

The project is therefore most meaningfully documented as a **specific integrated architecture and design methodology**: large-area/whole-garment thermal routing + directional/capillary liquid routing + deliberately engineered low-profile exterior evaporation geometry + effective-area/boundary-layer analysis + hot-ambient protection + stretch/apparel integration, together with concrete embodiments and falsifiable benchmark methods.

## Verification queue

Before stable release, retrieve authoritative records where available and record:

- earliest priority document/date;
- full patent family;
- independent claims;
- relevant claim dependencies;
- original-language passages where machine translation may affect meaning;
- legal status only if needed, clearly separated from technical prior-art relevance.
