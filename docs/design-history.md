# Design History and Branch Status

This file prevents obsolete exploratory assumptions from being mistaken for the current design.

## Stage A — dehumidifying garment concept

Early exploration considered reducing humidity near skin using desiccants, silica gel, or MOF-type sorbents.

**Current status:** not the primary architecture.

Reason: broad desiccant/dehumidifying garment concepts have substantial prior-art exposure, adsorption creates thermal/regeneration issues, and drying all incoming air is not necessary if liquid sweat can be moved directly to an efficient exterior evaporator.

MOF or other gas-phase capture remains an optional secondary embodiment only.

## Stage B — closed-loop / low-flow dehumidification

Explored as a way to avoid drying all ambient air.

**Current status:** archived secondary branch.

## Stage C — outward liquid transport and exterior 'sweating'

The concept shifted to transporting sweat/water outward and making the exterior textile itself the evaporation site.

**Current status:** retained as core.

This branch removes the need to store large quantities of adsorbed water inside the garment.

## Stage D — hair-like evaporative fins

Exploration considered capillary-fed hair-like filaments as high-area exterior evaporators.

**Current status:** retained as one embodiment, but not the preferred visual form.

Long exposed hairs can create thermal-efficiency, snagging, appearance, compression, and humid-boundary-layer problems.

## Stage E — whole-garment heat spreading

The garment was reframed so a large fraction of the body surface participates in lateral heat redistribution, feeding active evaporation zones from less-wet regions.

**Current status:** retained as a central design element.

Key model lesson: lateral spreading matters most when evaporation is spatially nonuniform; it adds much less when evaporation is already uniform.

## Stage F — fan/microjet exploration

Forced-air and microjet concepts were modeled as upper-bound cases.

**Current status:** not primary. Optional active embodiment/comparison only.

The current design target is passive operation without an onboard fan.

## Stage G — thermal switching concepts

Various approaches were considered to isolate conductive structures from hot ambient air when dry.

**Current status:** simplified.

Rather than requiring an elaborate active thermal switch, current embodiments emphasize:

- dry-side shielding;
- selective exposure of wet regions;
- anisotropic heat paths;
- lower through-thickness heat pickup where possible;
- optional humidity-responsive passive vents.

## Stage H — salt/crystallization concern

Early salt modeling treated local crystallization in microscopic evaporating capillaries as a major architecture risk and considered terminal crystallization zones or liquid brine purge.

**Correction:** salt does not evaporate. Water evaporates; nonvolatile salts remain in liquid/solid phases.

**Current status:** ordinary washability is the default requirement. Dedicated salt-management components are optional and should only be justified if the new architecture degrades materially faster than ordinary sweat-handling textiles.

Any future brine purge model means physical removal of salt-containing liquid, never gas-phase salt transport.

## Stage I — exterior apparel integration

The preferred exterior moved from obvious hair/bristle geometry to low-profile structures that read visually as ordinary performance apparel:

- micro-ribs;
- short rounded fins;
- 3D knit;
- lamellae;
- pleats;
- patterned pile;
- functional seam/panel geometry.

**Current status:** primary product-design direction.

## Current primary architecture

As of 2026-08-19:

`skin-side directional liquid transport -> flexible whole/large-area heat spreader -> distributed capillary delivery -> low-profile high-area exterior evaporator -> ambient evaporation`

with optional dry-side shielding and no required onboard fan.

## Rule for future design changes

When an old branch is revived, do not silently rewrite this history. Mark the branch as revived, state why, and identify which previous failure mode has been addressed.
