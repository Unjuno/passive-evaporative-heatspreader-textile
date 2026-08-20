# Passive Evaporative Heat-Spreader Textile v1.0.0

Release date: 2026-08-20

## Scope

v1.0.0 freezes the first stable **computational technical record** for a passive evaporative cooling textile architecture combining:

- directional local sweat collection;
- short distributed two-scale capillary liquid routing;
- pressure/ambient-aware exterior wet terminals;
- continuously ambient-connected evaporative microtexture, open valleys, gaps, or islands;
- short high-`k/rho` heat routes with limited cross-link redundancy;
- terminal contact/load management;
- dry-side protection against harmful hot-ambient sensible coupling;
- separate water and nonvolatile-solute balances with `J_salt,vapor = 0`.

The primary embodiment is fanless. Fan, sorbent, adaptive, detachable, and assisted-flow embodiments remain optional alternatives.

## Evidence level

This release is a **virtual/computational prototype only**.

It does not claim:

- a manufactured garment;
- a bench specimen;
- measured garment cooling power;
- human-subject performance;
- validated CFD;
- measured fouling lifetime;
- a proven manufacturing process;
- a legal conclusion of novelty, patentability, invalidity, infringement, or freedom to operate.

Numerical values in the repository are simulation, analytic-screening, or explicit design-variable results unless stated otherwise.

## Reproducible stack

The frozen research stack contains:

- 45 indexed executable screening/sensitivity/audit/virtual-prototype models;
- one reference-output generator;
- regression tests;
- five dedicated CI workflows;
- canonical documentation and correction history;
- generated reference data, figures, `metadata.json`, and `sha256.txt`.

The release workflow regenerates the reference package from the exact `v1.0.0` release commit, checks that the recorded Git SHA matches that commit, and publishes both the package ZIP and its SHA-256 digest as release assets.

## Major retained conclusions

- Geometric evaporator area is not automatically accessible evaporative area because neighboring wet structures can share a humid boundary layer.
- Long covered passive wet corridors can remain nearly saturated; nonzero natural flow does not prove useful air renewal.
- Thermo-solutal buoyancy can produce upward, downward, or near-neutral corridor-flow tendencies.
- Sensible heat transfer and vapor transfer must be treated separately.
- Positive evaporation does not necessarily imply positive body-side cooling in hot ambient air.
- Feed limitation can change the optimum external-exchange condition.
- Heat spreading creates integrated value when it connects regions with genuinely different wet/dry, exposure, shielding, or load boundary conditions.
- Routing pitch and terminal contact are first-order heat-spreader burdens.
- Short distributed liquid routes are strongly favored over one long upward centralized route in the current ideal capillary screens.
- Sparse liquid-network feasibility depends jointly on collector radius, trunk pitch, route phase/placement, source localization, and collapse assumptions.
- Collector-fouling calculations are imposed hydraulic-radius-loss sensitivities, not measured deposition kinetics.
- Transient terminal buffering is a mass-conserving low-order model, not a measured textile time constant.
- Salt is treated as nonvolatile at garment temperatures; water evaporates while dissolved salts remain, concentrate, or precipitate.

## Important corrections preserved

v1.0.0 intentionally preserves rather than hides several corrections made during development:

- The earlier claim that aligned sparse high-conductivity traces outperform an equal-material homogenized field was withdrawn. The retained equal-material ordering is `uniform homogenized > x-aligned / mesh >> y-transverse` for the tested geometry.
- Passive vertical corridors are not assumed to provide upward chimney flow; the sign can reverse or approach neutral.
- A common heat/mass multiplier was replaced by independent sensible and vapor-transfer factors.
- The earlier `d95*r^-4` route metric is retained only as a geometric burden proxy; explicit branched resistor networks supersede it for hydraulic-pressure conclusions.
- Water and salt mass balances were separated explicitly so salt vapor flux is zero.

## Prior-art policy

The release contains a technical prior-art map so individual building blocks are not presented as unique merely because they appear in the integrated architecture. Patent identifiers and dates are retained at the confidence level actually checked through public indexes. v1.0.0 deliberately does **not** label patent family, legal-status, or claim-scope facts as authoritatively patent-office verified when that verification was not completed.

The repository therefore makes no legal novelty or freedom-to-operate conclusion.

## Canonical entry points

- `README.md` — project overview and navigation.
- `docs/technical-disclosure.md` — integrated technical disclosure.
- `docs/embodiment-matrix.md` — concrete implementation families.
- `docs/current-results.md` — canonical numerical-results summary.
- `docs/research-freeze.md` — frozen technical core and change-control rule.
- `simulations/README.md` — executable model index.
- `AUDIT.md` — repository/release-readiness audit.
- `docs/patent-notes.md` and `docs/prior-art.md` — technical prior-art map and confidence boundaries.

## After v1.0.0

Further 3-D CFD, garment-scale curvature, measured constitutive properties, fouling kinetics, physical specimens, and human/bench validation are later-version research. They are not reasons to keep expanding this release candidate.
