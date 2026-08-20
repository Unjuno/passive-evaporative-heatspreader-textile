# Close Patent Notes

Status: **v1.0.0 technical prior-art map; not a legal opinion**  
Public-index cross-check: 2026-08-20  
Stable-release office-verification policy: **no item is labeled authoritatively office-verified in v1.0.0**

This file separates three different things that should not be conflated:

1. **bibliographic cross-check** — publication/application numbers, dates, inventor/assignee fields as shown by public patent indexes;
2. **technical relevance** — what the published text/embodiments appear to disclose;
3. **legal/claim conclusion** — novelty, scope, validity, infringement, freedom to operate, or family/legal status. This repository does **not** make those conclusions.

## Stable-release verification decision

For v1.0.0, the repository does **not** label any patent family, legal-status statement, or claim-scope conclusion as authoritatively verified by a patent office. Public official deep links were identified where available, but some WIPO PatentScope, J-PlatPat, USPTO, and related office interfaces were not reliably machine-readable from the release-preparation environment. Rather than overstate confidence, v1.0.0 keeps the six items below as a **public-index technical map**.

This is sufficient for the role these references play in the release: they identify adjacent technical disclosures and prevent the repository from presenting individual building blocks as unique. The stable release does not rely on exact family/legal-status assertions for any technical conclusion.

If a later version performs office-record verification, it should record the office, record URL/identifier, retrieval date, exact fact verified, and the independent claim text actually relied upon.

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

Release caveat: exact Japanese family/legal-status facts are not labeled patent-office verified in v1.0.0.

## P02 — WO2005063065A1 / JPWO2005063065A1 — fan air-conditioning garment

Public-index cross-check:

- PCT publication: `WO2005063065A1`;
- PCT application shown: `PCT/JP2003/016741`;
- priority/filing date shown: 2003-12-25;
- publication date shown: 2005-07-14;
- Japanese publication is indexed as `JPWO2005063065A1`;
- indexed text describes fan/blowing means producing body-parallel airflow and promoting sweat evaporation.

Technical consequence:

Onboard fans, body-parallel forced airflow, garment outlets/openings, and fan-assisted sweat evaporation are treated as established building blocks. The repository's baseline remains fanless.

Release caveat: exact PCT/Japanese family and closest-independent-claim facts are not labeled patent-office verified in v1.0.0.

## P03 — EP1978836A1 / EP1978836B1 — breathable multi-purpose clothing

Public-index cross-check:

- application publication: `EP1978836A1`;
- grant publication indexed: `EP1978836B1`;
- priority date shown: 2006-01-27;
- application publication date shown: 2008-10-15;
- grant publication date shown: 2010-09-29;
- inventor indexed: Bodo W. Lambertz;
- public indexes associate `WO2007085214A1` with this record.

Technical relevance:

The indexed patent text contains climate-control textile structures, air channels, moisture handling, and rib/web textile descriptions relevant to outward moisture transport and exterior release. These disclosures make ribbed textile moisture transport highly relevant adjacent art.

Important claim-scope caveat:

The independent EP claim surfaced in the public index is directed to breathable multi-layer clothing with coordinated climatic zones and air channels. The repository therefore does **not** describe a rib/capillary embodiment as though it were necessarily an independent-claim limitation.

Technical consequence:

Capillary/outward moisture transport through structured textile ribs or zones is not treated alone as the project distinction.

## P04 — US20110283722A1 / US8443463B2 — supplied-liquid evaporative garment

Public-index cross-check:

- published application: `US20110283722A1`;
- grant publication: `US8443463B2`;
- priority lineage shown from 2008-08-06;
- published application date shown: 2011-11-24;
- grant publication date shown: 2013-05-21;
- inventor indexed: Leslie Owen Paull.

Indexed abstract/claim content includes a wicking garment and hollow transport that delivers liquid from a reservoir to a garment region, followed by wicking/distribution and exposure to ambient air for evaporation.

Technical consequence:

`liquid supply -> wicking garment -> wet region -> ambient evaporation -> wearer cooling` is treated as established adjacent art and is not the repository's defining distinction.

Release caveat: current legal status and exact continuation/family scope are not needed by, and are not asserted by, v1.0.0.

## P05 — US20240125016A1 / US12209335B2 — wicking 3D-knitted spacer fabric

Public-index cross-check:

- published application: `US20240125016A1`;
- grant publication: `US12209335B2`;
- US application shown: `US18/480,243`;
- priority claim shown to a Chinese application dated 2022-10-18;
- application publication date shown: 2024-04-18;
- grant publication date shown: 2025-01-28;
- indexed assignee/inventor data identify Honeywell-related ownership history and the listed inventors.

Indexed claims describe a 3D-knitted spacer fabric with hydrophilic/heat-fusible yarn structures and moisture-management use.

Technical consequence:

3D spacer-knit outward moisture handling and increased exposed area are not, by themselves, unique premises of this project.

Release caveat: ownership/legal-status changes are not used as technical evidence and are not labeled office-verified in v1.0.0.

## P06 — WO2010082204A1 — monofilament fabric evaporation / salt-deposition cleaning

Public-index cross-check:

- PCT publication: `WO2010082204A1`;
- PCT application shown: `PCT/IL2010/000044`;
- priority date shown: 2009-01-19;
- publication date shown: 2010-07-22;
- indexed title concerns a monofilament fabric device for liquid evaporation and removal of salt precipitation deposits.

Technical consequence:

3D/knitted fabric as a salt-containing liquid evaporation medium, including deposition/cleaning concerns, is relevant adjacent technology even though the application is not a wearable cooling garment.

Release caveat: PCT national-phase/legal-status details are outside the technical conclusion and are not asserted as office-verified.

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

| item | public-index bibliographic cross-check | technical-text cross-check | v1.0.0 office-verified label |
|---|---|---|---|
| JPH04209808A | done | done at index level | **not claimed** |
| WO2005063065A1 | done | done at index level | **not claimed** |
| EP1978836A1/B1 | done | done; claim caveat recorded | **not claimed** |
| US20110283722A1 / US8443463B2 | done | done at index level | **not claimed** |
| US20240125016A1 / US12209335B2 | done | done at index level | **not claimed** |
| WO2010082204A1 | done | done at index level | **not claimed** |

## Stable-release rule

v1.0.0 is intentionally conservative: patent identifiers and dates are retained as a technical discovery map at the confidence level actually checked, while exact family relationships, legal status, infringement, validity, novelty, patentability, and freedom-to-operate conclusions remain outside scope. This closes the release blocker without converting incomplete office-record access into a false verification claim.
