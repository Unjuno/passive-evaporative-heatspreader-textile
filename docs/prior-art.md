# Prior-Art and Adjacent-Technology Map

Status: partial; patent landscape still requires expansion and authoritative family verification.  
Last checked: 2026-08-19.

This file is intentionally candid about closely related work. The purpose is to identify what is already known and to define which combinations, geometries, operating rules, and failure-aware implementations are being disclosed here.

## 1. Integrated heat conduction + sweat transport: i-Cool textile

**Peng, Y. et al. "Integrated cooling (i-Cool) textile of heat conduction and sweat transportation for personal perspiration management." Nature Communications 12, 6122 (2021).**  
DOI: https://doi.org/10.1038/s41467-021-26384-8

Reported concept: integration of heat-conductive pathways with water-transport channels to improve sweat evaporation and cooling.

### Relevance

This is highly relevant prior work. A broad concept such as "a textile containing a heat-conductive path and a sweat-transport path to enhance evaporative cooling" should not be treated as new by this project.

### Current project emphasis beyond that broad concept

The present repository focuses on a specific system-design branch including:

- deliberate whole-garment or large-area lateral heat redistribution toward spatially nonuniform evaporation zones;
- anisotropic, serpentine, island-bridge, or redundant flexible heat-spreader topologies;
- a separately engineered high-surface-area **exterior** evaporation morphology such as micro-ribs, short fins, 3D-knit relief, pile, lamellae, or graded structures;
- an explicit distinction between geometric exterior area and *effective accessible exchange area* through `alpha`;
- design against humid-boundary-layer overlap among adjacent exterior structures;
- dry-side thermal shielding/selective exposure for ambient temperatures above skin temperature;
- apparel-aesthetic integration of exterior evaporative structures;
- same-water-input artificial-skin heater-power benchmarking against a flat fast-dry textile.

These differences still require further prior-art searching. This document does not assert that every such element or combination is novel.

## 2. Directional liquid transport: skin-like fabric

**Lao, L.; Shou, D.; Wu, Y. S.; Fan, J. T. "Skin-like fabric for personal moisture management." Science Advances 6, eaaz0013 (2020).**  
DOI: https://doi.org/10.1126/sciadv.aaz0013

Reported concept: directional liquid-water transport through gradient-wettability channels, with outward liquid handling and resistance to external liquid ingress.

### Relevance

Directional sweat transport is treated as an available building block, not the primary inventive premise of this repository.

## 3. Humidity-responsive adaptive ventilation

**Li, X. et al. "Metalized polyamide heterostructure as a moisture-responsive actuator for multimodal adaptive personal heat management." Science Advances 7, eabj7906 (2021).**  
DOI: https://doi.org/10.1126/sciadv.abj7906

Reported concept: moisture-responsive textile flaps that adapt convection, sweat evaporation, and radiative heat transfer without electrical input.

### Relevance

Humidity-responsive vents/flaps are treated here as optional embodiments, not core requirements.

## 4. Directional sweat pumping and self-cooling fabric

**Zhu, R. et al. "Sweat-pumping cooling fabric for enhanced power generation and comfort." Nature Communications 17, 4374 (2026).**  
DOI: https://doi.org/10.1038/s41467-026-70856-8

Reported concept: a liquid-diode/gradient-wetting fabric that pumps sweat outward, spreads it over a larger area, evaporates it, and simultaneously supports hygroelectric power generation.

### Relevance

Outward sweat pumping and evaporation-area enlargement alone are established research directions. The present project therefore focuses on the combination with large-area heat redistribution, explicitly three-dimensional exterior evaporation morphology, boundary-layer-aware geometry, hot-ambient dry-side protection, and apparel integration.

## 5. Early cooling-garment patent: sorbent + exterior fins

**Japanese patent publication JPH04209808A, "Cooling garment / 冷房服", published 1992-07-31; priority/filing date reported as 1990-11-30.**

Public patent-index text reports a garment containing a moisture-reactive chemical heat-storage/sorbent material and identifies examples including lithium bromide, silica gel, zeolite, and calcium chloride. The claims also include an embodiment with fins disposed outside the heat-storage material.

### Relevance

This is important because it predates the current work by decades and directly undermines any broad proposition such as:

- "put a desiccant/sorbent in clothing to promote sweat-vapor removal"; or
- "add exterior fins to a sorbent cooling garment."

Accordingly:

- sorbent/MOF variants are secondary here and cannot be treated broadly as a new premise;
- exterior fins **by themselves** are not a sufficient differentiator;
- the current project must be evaluated at the level of specific liquid-fed evaporative exterior structures, heat-routing architecture, boundary-layer-aware geometry, and combined operation.

### Verification status

Publication number and claim text have been located in a public patent index. Before a stable release, verify the bibliographic record, original Japanese text, legal-family information, and any related publications against an authoritative patent-office record such as J-PlatPat or an equivalent official database.

## 6. Fan-based air-conditioning garment family

**WO2005063065A1, "Air-conditioning clothing / 空調衣服"; public patent-index records identify priority/filing date 2003-12-25.** A Japanese publication of the PCT family is indexed as **JPWO2005063065A1**.

The patent-family text describes an air-blowing means/fan attached to the garment so that air flows in the space between clothing and the body/underwear. The generated body-parallel airflow promotes evaporation of sweat. Public indexed embodiments include intake and exhaust arrangements, garment spacing structures, detachable fans, and quantitative fan/flow examples.

Later fan-garment patents repeatedly cite WO2005/063065 as prior literature for the now-standard architecture in which fan-driven air passes along the body/underwear and exits through garment openings while promoting sweat evaporation.

### Relevance

This establishes that the following broad elements are not treated as unique here:

- mounting an electric fan in a garment;
- forming an internal body-parallel airflow path;
- exhausting air through garment openings;
- using that airflow to accelerate sweat evaporation and cooling.

The primary architecture in this repository is intentionally passive and does not require an onboard fan. Fan assistance remains an optional active embodiment and an upper-bound/comparison condition.

### Verification status

The publication number, PCT family relationship, priority date, and technical description have been located in public patent indexes. Before stable release, verify original bibliographic/family data and closest independent claims from an authoritative patent-office source.

## 7. What is explicitly *not* claimed as a unique premise here

The following ideas are known or broadly established and should not be presented alone as this project's contribution:

- sweat evaporation cools the body;
- capillary textiles transport liquid water;
- directional wetting can move sweat outward;
- heat-conductive textile elements can redistribute heat;
- increasing wet area can increase evaporation in suitable conditions;
- humidity-responsive textile vents can alter heat/mass transfer;
- fan garments can create body-parallel airflow and increase sweat evaporation;
- sorbents/desiccants can capture water vapor;
- sorbent cooling garments can include exterior fins.

## 8. Current disclosure space to search more aggressively

The following combinations need dedicated patent/literature searches before any novelty statement:

1. whole-garment flexible heat spreader + capillary-fed exterior 3D ribs/fins for sweat evaporation;
2. anisotropic heat routing specifically toward exterior wet evaporators;
3. micro-rib/lamella pitch optimization based on accessible exchange rather than geometric area;
4. thermal shielding of dry high-conductivity garment regions while wet regions remain exposed;
5. conductive path geometry that doubles as apparel patterning or structured evaporative panel support;
6. stretchable serpentine/island-bridge heat-spreader garments coupled to evaporative cooling;
7. mixed-height or graded exterior evaporative fins intended to reduce shared humid boundary layers;
8. selective evaporation-terminal architectures that protect upstream capillary routes from evaporation and salt concentration;
9. a complete stack combining large-area heat routing, directional liquid transport, distributed capillary feed, and low-profile exterior 3D evaporators.

## 9. Patent-search queue

For each close family record:

- earliest priority date;
- publication number(s);
- inventor/assignee;
- independent-claim summary;
- relevant figures/embodiments;
- overlap with this repository;
- remaining design space;
- authoritative source used for verification.

Priority topics:

- heat-conductive evaporative garments;
- finned/3D structured evaporative textiles;
- sweat-routing clothing;
- flexible heat-spreader apparel;
- humidity-actuated textile ventilation;
- combinations of the above with capillary-fed exterior evaporation.

## 10. Interpretation rule

No statement in this repository that something is "the project concept" should be read as a legal conclusion of novelty or inventiveness. Prior art is continuously incorporated, and the technical disclosure is intentionally broader than any single proposed product configuration.
