# Passive Evaporative Heat-Spreader Textile

Open research on a passive personal-cooling garment combining directional liquid transport, distributed capillary delivery, routed heat spreading, pressure-aware terminal placement, and exterior evaporation.

> **Current state: virtual/computational prototype only. No physical garment or bench specimen currently exists, and no physical performance claim is made.**

## Current architecture

The current fanless hypothesis is:

1. directional sweat collection away from skin;
2. distributed local collection cells rather than one garment-scale liquid manifold;
3. short protected micro-wicks feeding larger low-resistance liquid trunks;
4. nearby wet exterior terminals placed by a pressure-aware **thermal/liquid co-design** rather than pure pressure avoidance;
5. low-profile micro-rib / 3D-knit / short-fin evaporative texture with continuously ambient-connected valleys/gaps;
6. short in-plane high-`k/rho` heat routes connecting dry/compressed regions to active wet terminals;
7. limited cross-link redundancy for damage tolerance;
8. explicit dry-side shielding where hot ambient sensible pickup would be harmful.

The objective is **body-coupled useful evaporation**, not maximum geometric surface area or evaporation mass alone.

## Current numerical conclusions

### Exterior evaporation

- Dense ribs can share one humid boundary layer; geometric area is not automatically useful area.
- Long covered passive wet corridors can remain nearly saturated despite nonzero natural flow.
- Sensible heat transfer and water-vapor transfer are treated separately.
- Positive evaporation can coexist with negative body-side heat flow in hot ambient conditions.
- Stronger ambient exchange is not always better after water supply becomes limiting.

### Heat routing

- Heat spreading produces little integrated value in a deliberately symmetric wet/dry boundary condition.
- Value appears when heat is routed from dry/shielded/compressed regions toward active evaporators.
- Ideal routing burden grows approximately with routing pitch squared.
- Contact resistance can dominate sheet conductivity.
- Explicit equal-material sparse traces tested so far do not beat an ideal homogenized conductivity field, although route orientation strongly changes performance.
- Under the current combined stretch/contact/fracture failure map, a lightly cross-linked directed network (`lambda≈0.125`) is the robustness anchor.

### Pressure / garment loading

- Global compression can initially improve solid thermal contact, but stronger compression eventually closes vapor access and moves the system into a transfer-limited fully-wet state.
- With synthetic backpack/strap/seat pressure maps, low-pressure evaporator placement outperforms putting the main wet terminal directly under persistent load in the primary screen.
- A loaded evaporator can remain competitive only if its vapor path is mechanically protected strongly while load-bearing support occupies little active wet area.
- Ideal state-adaptive wet-layout switching adds less than about 1% over the best fixed pressure-aware layout in the current quasisteady usage scenarios, so active switching is not the baseline direction.

### Thermal / liquid terminal co-design

Pure pressure avoidance improves evaporation under load but can lengthen liquid collection routes. The current terminal co-design therefore screens both body-side heat flux and a protected-trunk hydraulic burden

\[
J_h=d_{95}\hat r^{-4}.
\]

For the converged 24 x 24 backpack + shoulder-strap reference:

| candidate | body-side heat flux | liquid `d95` | protected-trunk hydraulic proxy |
|---|---:|---:|---:|
| pure thermal optimum | 112.84 W/m² | 20.16 mm | 30.72 mm-eq |
| current co-design anchor | 110.83 W/m² | 16.77 mm | 25.56 mm-eq |

The co-design anchor (`template beta=0.125`, route weight `0.35`) retains **98.21%** of the modeled thermal optimum while reducing the same hydraulic p95 proxy by **16.79%**. This is a screening result, not a full hydraulic-network solution.

### Liquid routing

Ideal capillary screen:

\[
\Delta P_f=\frac{8\mu LQ}{\pi r^4N},\quad
\Delta P_c=\frac{2\gamma\cos\theta}{r},\quad
\Delta P_h=\rho g\Delta z.
\]

For positive vertical lift, the ideal radius minimizing total capillary cross-sectional area is

\[
\boxed{r_* = \frac{\gamma\cos\theta}{\rho g\Delta z}}.
\]

The current screen strongly favors **many short local liquid routes** over one long upward centralized route. In one explicit equal-total-flow illustration (150 g/h), a 200 mm / 100 mm-rise central route requires an ideal total capillary cross-section of ~48 mm², while four 50 mm / 25 mm-rise local cells require ~3 mm². This is geometry-dependent, not a universal performance ratio.

A practical two-scale liquid architecture is therefore:

> local collector wick -> short fine-pore section -> larger transport trunk -> nearby exterior terminal.

### Virtual garment mass

A nominal VP-E pressure-relocation BOM screen gives about **169 g dry / 181 g operating mass**, including about 109 g of base textile. Broad deterministic parameter sampling places the median added functional dry mass near 71 g. These are design-range calculations, not measured material or garment masses.

### Salt

Sweat salts are nonvolatile in the models:

\[
J_{salt,vapor}=0.
\]

Water-only upstream evaporation raises bulk salt concentration as

\[
\sigma_{out}=\frac{\sigma_0}{1-f_{leak}}.
\]

Small upstream water leakage therefore does **not** mathematically guarantee bulk crystallization. Internal evaporation is still discouraged because it wastes terminal water delivery and can create local wall-film drying/deposition that this bulk model does not resolve.

## Representative current pressure-map result

For the synthetic backpack + shoulder-strap map at the primary constitutive setting (`cmax=0.5`, air-closure exponent `n=2`), the converged 24 x 24 screen gives approximately:

| equal-area wet layout | body-side heat flux | vapor-capacity index | mean local compression |
|---|---:|---:|---:|
| pressure-aware | **112.8 W/m²** | **211 g/(m² h)** | **0.061** |
| peripheral islands | 106.4 | 194 | 0.129 |
| side columns | 103.9 | 191 | 0.130 |
| four islands | 84.3 | 147 | 0.303 |
| center panel | 60.9 | 105 | 0.421 |

These are model outputs under synthetic normalized pressure fields, not measured garment pressures or cooling claims.

## Repository map

### Technical record

- `docs/technical-disclosure.md` — integrated disclosure
- `docs/architecture.md` — functional architecture
- `docs/embodiment-matrix.md` — implementation combinations
- `docs/current-results.md` — integrated numerical summary
- `docs/spatial-pressure-layout.md` — local load / wet-terminal placement
- `docs/terminal-route-codesign.md` — pressure avoidance vs terminal-distance tradeoff
- `docs/pressure-liquid-codesign.md` — thermal / protected-trunk hydraulic co-design
- `docs/protected-air-channel-tradeoff.md` — relocation vs protected under-load vapor path
- `docs/protected-support-skeleton.md` — air-gap preservation vs support-area penalty
- `docs/load-schedule-policy.md` — fixed vs ideal adaptive wet-layout policy
- `docs/capillary-liquid-network.md` — passive liquid-routing burden
- `docs/capillary-architecture-tradeoff.md` — analytic optimum and central/local comparison
- `docs/capillary-practical-constraints.md` — radius caps, hierarchy and blockage
- `docs/virtual-garment-bom.md` — mass/thickness design-range screen
- `docs/integrated-virtual-prototype-vpe.md` — integrated VP-E anchor
- `docs/salt-leakage-budget.md` — corrected nonvolatile-solute bulk balance
- `docs/roadmap.md` — virtual-prototype-first roadmap
- `docs/prior-art.md` / `docs/patent-notes.md` — adjacent work / working patent notes
- `AUDIT.md` — repository audit

### Executable stack

The branch currently contains **41 executable screening/sensitivity/audit/virtual-prototype models**, plus `generate_reference_outputs.py` as a reproducibility generator. See `simulations/README.md` for the indexed list.

Dedicated workflows cover the broad model stack, topology/apparel models, pressure/load models and liquid-routing models.

## Reproducibility

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Reference CSVs in `data/` distinguish converged screening outputs from analytic identities. Generated artifacts are intended to carry git-commit metadata and hashes before a stable release is frozen.

## Interpretation rules

Do not treat any of the following alone as proof of garment cooling:

- geometric surface area;
- one exchange multiplier;
- air velocity or Péclet number;
- evaporation mass;
- fully-wet capacity above available feed;
- high sheet conductivity without path/contact burden;
- synthetic pressure percentages as real garment pressure limits;
- ideal cylindrical capillary counts as real textile permeability;
- route-distance or `d95 r^-4` proxies as a full hydraulic network;
- virtual BOM values as measured garment mass;
- bulk salt concentration as proof of local crystallization.

## Current next tasks

1. replace the route-distance/hydraulic proxy with an explicit branched heat + liquid network on a garment-scale regional map;
2. add explicit channel/spacer collapse and garment curvature under local load;
3. replace effective protected-air floors with geometry-resolved vapor paths;
4. model local wall-film salt deposition and progressive hydraulic-radius loss;
5. rerun independent wet/dry hot/humid exposure control at full converged reference resolution;
6. continue prior-art/claim verification and prepare a frozen stable release only after the computational record is internally consistent.

## Physical clarification: sweat salts

At garment temperatures, water evaporates; sweat salts do not. Salt vapor flux is zero in this project.

## License

Apache License 2.0. See `LICENSE`.

## Citation / release state

See `CITATION.cff`. Stable v1.0 has not yet been frozen or persistently archived with a DOI.
