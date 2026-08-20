# Research freeze and release-preparation state

Date: 2026-08-20

## Decision

The numerical/theoretical exploration phase is considered **sufficient for the present public technical record**. The project is now in repository-consolidation and release-preparation mode.

No additional model is required merely to make the architecture more elaborate. New modeling should occur only if it resolves a specific contradiction, release blocker, or independently identified technical gap.

## What is frozen as the current technical core

The current passive design family consists of:

1. directional local sweat collection away from skin;
2. short distributed liquid routes rather than one garment-scale central lift;
3. a two-scale capillary architecture with fine collector paths and larger transport trunks;
4. exterior wet terminals placed with local pressure / ambient-access conditions in mind;
5. continuously ambient-connected evaporative microtexture, open valleys, gaps, or islands rather than reliance on long covered passive chimneys;
6. short high-`k/rho` heat routes that move heat from dry/compressed regions toward active wet terminals;
7. limited cross-link redundancy rather than a topology chosen only for peak nominal conductance;
8. terminal contact management and optional mechanically protected vapor gaps under load;
9. dry-side thermal shielding or reduced ambient coupling where hot ambient sensible pickup is harmful;
10. explicit separation of water evaporation from nonvolatile sweat solutes, with `J_salt,vapor = 0`.

The primary embodiment remains fanless. Fans, sorbents, adaptive mechanisms, detachable terminals, and other variants remain optional embodiments rather than baseline requirements.

## Canonical retained findings

- Geometric evaporator area is not automatically accessible evaporative area because neighboring wet features can share one humid boundary layer.
- Long covered/end-renewed passive wet corridors can remain nearly saturated; nonzero natural flow is not sufficient evidence of useful renewal.
- Sensible heat transfer and vapor transfer must be tracked separately.
- Positive evaporation is not equivalent to positive body-side cooling in hot ambient conditions.
- Water/feed limitation can change the optimum external exchange condition.
- Heat spreading has integrated value only when it connects regions with genuinely different wet/dry, exposure, shielding, or load boundary conditions.
- Routing pitch and terminal contact are first-order heat-spreader burdens.
- Corrected equal-material ordering is `uniform homogenized > x-aligned / mesh >> y-transverse`; the earlier contrary conclusion is withdrawn.
- Under the tested combined stretch/contact/fracture map, a lightly cross-linked directed heat network (`lambda≈0.125`) is the current robustness anchor.
- Synthetic load maps favor moving active wet terminals away from persistent high-pressure regions unless vapor access is strongly protected with little support-area occupation.
- Fixed passive terminal placement is preferred over active load-state switching in the current quasisteady schedules because the modeled adaptive uplift is small.
- Short distributed liquid delivery is strongly preferred over one long upward centralized route in the ideal capillary screens.
- The earlier `d95*r^-4` route proxy is a geometric burden metric, not proof of binding hydraulic pressure loss; explicit branched-network models supersede that interpretation.
- Sparse liquid-network feasibility is governed jointly by collector radius, trunk pitch, route phase, source localization, and collapse assumptions.
- Salt is nonvolatile in the garment-temperature model. Small upstream water loss does not by itself imply bulk crystallization.

## Corrections that must remain visible

The following are intentionally preserved rather than erased:

- aligned sparse high-`k` traces were initially reported as exceeding an equal-material homogenized field; the corrected model shows they do not;
- passive vertical/open corridors were initially discussed too strongly as upward chimney mechanisms; thermo-solutal effects can reverse or neutralize buoyancy;
- a common heat/mass multiplier was split into independent sensible and vapor-transfer factors;
- the terminal-distance `d95*r^-4` proxy was initially given too much hydraulic significance; explicit resistor-network pressure solves show large margin for the current short dense routes;
- salt and water balances were separated so that salt vapor flux is zero.

## What is not established

This freeze does **not** claim:

- a measured cooling power;
- a manufactured garment;
- a human-subject result;
- validated CFD;
- measured textile constitutive laws;
- a validated salt/fouling lifetime;
- a proven manufacturing process;
- a legal conclusion of novelty, patentability, freedom to operate, or invalidity of any patent.

Future physical experiments remain useful if a specimen is ever built, but are not represented as completed work.

## Release-critical work remaining

Only repository/publication tasks are considered blockers for a stable release:

1. keep README, current-results, audit, simulation index, changelog, citation metadata, and PR metadata synchronized;
2. verify the stable-release commit with all defined CI workflows;
3. perform authoritative patent-family/publication verification for identifiers and dates used in the prior-art notes;
4. freeze one exact commit and regenerate release reference artifacts / hashes at that commit;
5. create a versioned GitHub release/tag;
6. create a persistent archival copy/DOI if desired and link it to the exact release.

## Optional future research, not release blockers

The following are now backlog items rather than reasons to postpone publication:

- geometry-resolved 3-D exterior natural convection or cross-flow;
- garment-scale curvature and seam modeling;
- time-varying sweat-source migration;
- detailed spacer/gap deformation mechanics;
- wall-film precipitation/dissolution kinetics and measured fouling rates;
- physical prototype construction and controlled bench validation.

## Change-control rule after freeze

After this point, technical edits should be classified as one of:

- **correction** — fixes an error or inconsistency;
- **clarification** — improves wording without changing the disclosed architecture;
- **release metadata** — version, citation, hash, archival information;
- **new research** — should normally be deferred to a later version rather than added to the release candidate.

This rule is intended to prevent an indefinitely expanding research branch from obscuring the already-developed technical record.
