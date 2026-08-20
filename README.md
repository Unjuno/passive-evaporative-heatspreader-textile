# Passive Evaporative Heat-Spreader Textile

Public computational research on a fanless cooling-textile architecture that combines directional sweat transport, distributed capillary delivery, routed heat spreading, pressure-aware evaporative terminals, and ambient-connected exterior evaporation.

> **Project state:** `v1.0.0` is the stable computational technical record. The tagged release is bound to commit `e544f64630119c88425b49cc3e5a00e06d15ad84`. This repository contains simulation, analytic screening, virtual-prototype, regression, and future-validation materials. **No physical garment or bench specimen exists, and no measured garment-performance claim is made.**

## Current architecture

The retained passive design family is:

1. directional local sweat collection away from skin;
2. short distributed liquid routes rather than one garment-scale central wick/lift;
3. fine collector paths feeding larger low-resistance liquid trunks;
4. nearby exterior wet terminals placed with local pressure and ambient access in mind;
5. low-profile micro-rib / 3D-knit / short-fin evaporative texture with continuously ambient-connected valleys, gaps, or islands;
6. short in-plane high-`k/rho` heat routes connecting dry/compressed regions to active wet terminals;
7. limited cross-link redundancy for damage tolerance;
8. robust terminal contact and, where needed, mechanically protected vapor gaps;
9. dry-side shielding or reduced ambient coupling when hot-air sensible pickup is harmful;
10. separate water and nonvolatile-solute balances, with `J_salt,vapor = 0`.

The objective is **body-coupled useful evaporation**, not maximum geometric surface area, maximum evaporation mass, or maximum conductivity in isolation.

## Retained numerical conclusions

- Dense wet ribs can share one humid boundary layer; geometric area is not automatically useful area.
- Long covered passive wet corridors can remain nearly saturated; nonzero natural flow is not proof of useful renewal.
- Sensible heat transfer and vapor transfer are tracked separately.
- Positive evaporation can coexist with negative body-side heat flow in hot ambient conditions.
- Water/feed limitation changes the optimum external exchange condition.
- Heat spreading creates integrated value only across genuinely different local wet/dry, exposure, shielding, or load conditions.
- Routing pitch and terminal contact are first-order heat-spreader burdens.
- Corrected equal-material ordering is `uniform homogenized > x-aligned / mesh >> y-transverse`; the earlier opposite claim is explicitly withdrawn.
- Under the current combined stretch/contact/fracture screen, a lightly cross-linked directed network (`lambda≈0.125`) is the heat-routing robustness anchor.
- Synthetic backpack/strap/seat maps favor moving active wet terminals out of persistent load zones unless vapor access is strongly protected with little support-area occupation.
- Ideal load-state wet-layout switching adds less than about 1% over the best fixed pressure-aware layout in current quasisteady schedules, so active switching is not the baseline direction.
- Short distributed liquid routing is strongly favored over one long upward centralized route in the ideal capillary screens.
- A `d95*r^-4` route proxy is retained only as a geometric burden metric; explicit branched-flow models supersede it for hydraulic-pressure claims.
- Sparse liquid-network feasibility depends jointly on collector radius, trunk pitch, phase/placement, source localization, and collapse assumptions.
- Sweat salts are nonvolatile in the models. Small upstream water leakage does not by itself imply bulk crystallization.

## Representative screened results

These values are **model outputs under stated assumptions**, not measured garment performance.

### Pressure-aware terminal placement

For the converged synthetic backpack + shoulder-strap screen (`cmax=0.5`, air-closure exponent `n=2`):

| equal-area wet layout | body-side heat flux | vapor-capacity index | mean local compression |
|---|---:|---:|---:|
| pressure-aware | **~112.8 W/m²** | **~211 g/(m² h)** | **~0.061** |
| peripheral islands | ~106.4 | ~194 | ~0.129 |
| side columns | ~103.9 | ~191 | ~0.130 |
| four islands | ~84.3 | ~147 | ~0.303 |
| center panel | ~60.9 | ~105 | ~0.421 |

Under no load, ordinary four-island placement can rank above the pressure-aware rule. The conclusion is **load-aware placement**, not universal peripheral evaporation.

### Sparse two-scale liquid network

For sampled 200 µm trunk lattices embedded in a finer collector mesh, with localized source and phase-offset checks, the largest tested trunk pitch retaining capillary safety factor >=3 at every sampled phase was:

| collector radius | largest robust tested trunk pitch |
|---:|---:|
| 20 µm | ~15 mm |
| 25 µm | ~20 mm |
| 30 µm | ~30 mm |
| 35–50 µm | >=60 mm |

This is a screening boundary, not a measured textile permeability result.

### Heat-network robustness

Under simultaneous 20% compliant-path stretch, localized wet-terminal contact loss, and localized 5% conductor fracture, the `lambda≈0.125` directed/cross-linked network retains about **4.96 W** of the modeled routing gain over 0.195 m², about **84.6%** of its nominal value in that failure map.

### Virtual garment mass

The nominal VP-E pressure-relocation BOM screen gives approximately **169 g dry / 181 g operating mass**, including roughly 109 g of base textile. These are virtual design-variable calculations, not measured garment masses.

## Corrected interpretation of salt

At garment temperatures in this project:

\[
J_{salt,vapor}=0.
\]

If upstream evaporation removes water fraction `f_leak` while dissolved nonvolatile-solute flux is conserved, a bulk concentration screen is

\[
\sigma_{out}=\frac{\sigma_0}{1-f_{leak}}.
\]

Thus 10% water loss increases bulk concentration by only about 1.11x. Local thin-film drying or deposition is a separate failure mechanism and is not inferred from bulk concentration alone.

## Repository guide

Start with:

- [`docs/technical-disclosure.md`](docs/technical-disclosure.md) — integrated technical disclosure;
- [`docs/current-results.md`](docs/current-results.md) — canonical detailed numerical findings and limitations;
- [`docs/architecture.md`](docs/architecture.md) — subsystem architecture;
- [`docs/embodiment-matrix.md`](docs/embodiment-matrix.md) — concrete implementation variants;
- [`docs/research-freeze.md`](docs/research-freeze.md) — research-freeze and change-control policy;
- [`docs/release-notes-v1.0.0.md`](docs/release-notes-v1.0.0.md) — stable release scope and evidence boundary;
- [`docs/release-verification-v1.0.0.md`](docs/release-verification-v1.0.0.md) — post-release integrity record;
- [`docs/README.md`](docs/README.md) — full documentation index;
- [`simulations/README.md`](simulations/README.md) — indexed executable model stack;
- [`AUDIT.md`](AUDIT.md) — release/readiness and verification audit.

The repository contains **45 indexed executable screening/sensitivity/audit/virtual-prototype models**, plus one reference-output generator, regression tests, committed reference CSVs, and five domain/test CI workflows.

## Reproducibility

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

`model-tests` can generate commit-traced reference artifacts from the current source tree. The archived `v1.0.0` verifier checks out the immutable release tag, reruns the full regression suite, executes the indexed branched-network script directly, regenerates the release reference package from outside the checkout directory, verifies the recorded Git commit, and produces a fresh verification ZIP plus SHA-256 file.

## Interpretation rules

Do not treat any one of the following as proof of real-garment performance:

- geometric surface area;
- evaporation mass alone;
- one heat/mass exchange multiplier;
- a fully-wet capacity above available feed;
- high sheet conductivity without route/contact burden;
- synthetic pressure percentages as measured garment pressure limits;
- ideal cylindrical capillary counts as measured textile permeability;
- route-distance proxies as a complete hydraulic network;
- virtual BOM values as measured garment mass.

## Research freeze / release state

The exploratory modeling phase is complete for `v1.0.0`. Additional 3-D CFD, garment-scale curvature, measured fouling kinetics, and physical prototypes are **optional later-version research**, not blockers for this computational disclosure.

The `v1.0.0` patent map is intentionally conservative: public-index technical/bibliographic findings are retained, while patent family, legal-status, and claim-scope facts are not labeled authoritatively office-verified unless such verification is explicitly recorded. No legal novelty or freedom-to-operate conclusion is asserted.

The stable tag is immutable project history. Post-release maintenance on `main` does not alter the contents of `v1.0.0`.

## License

Apache License 2.0. See [`LICENSE`](LICENSE).

## Citation

See [`CITATION.cff`](CITATION.cff). Cite `v1.0.0` or the exact commit used. Stable `v1.0.0` resolves to `e544f64630119c88425b49cc3e5a00e06d15ad84`.
