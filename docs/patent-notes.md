# Close Patent Notes

Status: **release-candidate working patent map; not a legal opinion**  
Public-index cross-check: 2026-08-20  
Authoritative patent-office/family/claim verification: **still open**

This file separates three different things that should not be conflated:

1. **bibliographic cross-check** — publication/application numbers, dates, inventor/assignee fields as shown by public patent indexes;
2. **technical relevance** — what the published text/embodiments appear to disclose;
3. **legal/claim conclusion** — novelty, scope, validity, infringement, freedom to operate, or family/legal status. This repository does **not** make those conclusions.

## P01 — JPH04209808A — cooling garment / sorbent + exterior fins

Public-index cross-check:

- publication: `JPH04209808A`;
- filing/priority date shown: 1990-11-30;
- publication date shown: 1992-07-31;
- indexed title: cooling garment / 冷房服;
- indexed claims include a moisture-reactive heat-storage/sorbent material and a dependent claim with fins outside the heat-storage material.

Technical consequence:

- a broad desiccant/sorbent cooling garment is not treated as unique here;
- exterior fins on a sorbent garment are not treated as a sufficient differentiator.

Release caveat: original Japanese bibliographic/family data and claim text should be checked in an authoritative Japanese patent-office/J-PlatPat record before a stable release asserts exact family details.

## P02 — WO2005063065A1 / JPWO2005063065A1 — fan air-conditioning garment

Public-index cross-check:

- PCT publication: `WO2005063065A1`;
- PCT application shown: `PCT/JP2003/016741`;
- priority/filing date shown: 2003-12-25;
- publication date shown: 2005-07-14;
- Japanese family publication is indexed as `JPWO2005063065A1`;
- indexed text describes fan/blowing means producing body-parallel airflow and promoting sweat evaporation.

Technical consequence:

Onboard fans, body-parallel forced airflow, garment outlets/openings, and fan-assisted sweat evaporation are treated as established building blocks. The repository's baseline remains fanless.

Release caveat: exact PCT/Japanese family data and closest independent claims still require authoritative office verification.

## P03 — EP1978836A1 / EP1978836B1 — breathable multi-purpose clothing

Public-index cross-check:

- application publication: `EP1978836A1`;
- grant: `EP1978836B1`;
- priority date shown: 2006-01-27;
- application publication date shown: 2008-10-15;
- grant publication date shown: 2010-09-29;
- inventor indexed: Bodo W. Lambertz;
- indexed family includes `WO2007085214A1`.

Technical relevance:

The patent text contains climate-control textile structures, air channels, moisture handling, and rib/web textile descriptions relevant to outward moisture transport and exterior release. These disclosures make ribbed textile moisture transport highly relevant adjacent art.

Important claim-scope caveat:

The independent EP claim surfaced in the public index is directed to breathable multi-layer clothing with coordinated climatic zones and air channels. The repository therefore should **not** describe a rib/capillary embodiment as though it were necessarily the independent-claim limitation without checking the exact specification/claim dependencies.

Technical consequence:

Capillary/outward moisture transport through structured textile ribs or zones is not treated alone as the project distinction.

## P04 — US20110283722A1 / US8443463B2 — supplied-liquid evaporative garment

Public-index cross-check:

- published application: `US20110283722A1`;
- grant: `US8443463B2`;
- priority lineage shown from 2008-08-06;
- published application date shown: 2011-11-24;
- grant publication date shown: 2013-05-21;
- inventor indexed: Leslie Owen Paull.

Indexed independent-claim/abstract content includes a wicking garment and hollow transport that delivers liquid from a reservoir to a garment region, followed by wicking/distribution and exposure to ambient air for evaporation.

Technical consequence:

`liquid supply -> wicking garment -> wet region -> ambient evaporation -> wearer cooling` is established prior art and is not treated as the repository's defining distinction.

## P05 — US20240125016A1 / US12209335B2 — wicking 3D-knitted spacer fabric

Public-index cross-check:

- published application: `US20240125016A1`;
- grant: `US12209335B2`;
- US application shown: `US18/480,243`;
- priority claim shown to Chinese application dated 2022-10-18;
- application publication date shown: 2024-04-18;
- grant publication date shown: 2025-01-28;
- indexed assignee/inventor data identify Honeywell-related ownership history and the listed inventors.

Indexed claims describe a 3D-knitted spacer fabric with hydrophilic/heat-fusible yarn structures and moisture-management use.

Technical consequence:

3D spacer-knit outward moisture handling and increased exposed area are not, by themselves, unique premises of this project.

## P06 — WO2010082204A1 — monofilament fabric evaporation / salt-deposition cleaning

Public-index cross-check:

- PCT publication: `WO2010082204A1`;
- PCT application shown: `PCT/IL2010/000044`;
- priority date shown: 2009-01-19;
- publication date shown: 2010-07-22;
- indexed title concerns a monofilament fabric device for liquid evaporation and removal of salt precipitation deposits.

Technical consequence:

3D/knitted fabric as a salt-containing liquid evaporation medium, including deposition/cleaning concerns, is relevant adjacent technology even though the application is not a wearable cooling garment.

## Combined technical implication

The repository should not present any one of the following alone as its technical distinction:

- capillary sweat transport;
- outward moisture transport;
- ribbed textile moisture transport;
- 3D spacer knit for moisture transfer/evaporation;
- supplied liquid distributed through a wicking garment;
- fan-assisted sweat evaporation;
- sorbent garment cooling;
- exterior fins alone.

The current record is therefore framed as an **integrated architecture and design methodology** combining thermal routing, distributed liquid routing, boundary-layer-aware exterior evaporation, local pressure/ambient-access placement, hot-ambient protection, apparel robustness, and explicit failure-boundary modeling.

## Verification status table

| item | public-index bibliographic cross-check | technical-text cross-check | authoritative office/family/claim verification |
|---|---|---|---|
| JPH04209808A | done | done at index level | OPEN |
| WO2005063065A1 | done | done at index level | OPEN |
| EP1978836A1/B1 | done | done; claim caveat recorded | OPEN |
| US20110283722A1 / US8443463B2 | done | done at index level | OPEN |
| US20240125016A1 / US12209335B2 | done | done at index level | OPEN |
| WO2010082204A1 | done | done at index level | OPEN |

## Stable-release rule

Before stable release, authoritative verification should focus on **identifiers, family relationships, dates, and the closest independent claims actually relied upon in the final prior-art summary**. Legal status should be included only if genuinely needed and clearly separated from technical prior-art relevance.
