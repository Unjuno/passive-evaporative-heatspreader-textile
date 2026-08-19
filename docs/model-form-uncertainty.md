# Model-Form Uncertainty Framework

Date: 2026-08-19

## Status

**Research uncertainty framework. The intervals below are screening ranges, not measured confidence intervals.**

The project now distinguishes three kinds of uncertainty:

1. **parameter uncertainty** — uncertain numerical values inside a chosen model;
2. **model-form uncertainty** — uncertainty caused by the governing approximation itself;
3. **experimental uncertainty** — instrument, calibration, repeatability, and environmental uncertainty once bench data exist.

## 1. Current high-impact uncertain quantities

| Quantity | Screening range / alternatives | Why it matters |
|---|---|---|
| body-to-evaporator coupling `U_body` | 30–150 W m^-2 K^-1 | controls how much latent cooling is supplied by the body rather than ambient heat |
| sensible multiplier `M_h` | 1–2 initial screen | hot-air sensible heat pickup can increase with exterior exchange |
| vapor multiplier `M_m` | 1–4 initial screen; E3-dependent | directly changes evaporation capacity |
| linearized radiation `h_r` | 4–8 W m^-2 K^-1 | affects surface energy balance |
| artificial-skin temperature | 33–35 °C | changes both thermal and vapor-pressure driving forces |
| ambient RH | 50–85% | dominant evaporation constraint in hot/humid use |
| liquid feed | 75–300 g h^-1 equivalent | determines whether the exterior is transfer-limited or water-limited |
| E3 renewal boundary | geometry-dependent | dominant model-form assumption in the pure-diffusion rib screen |
| equilibrium branch | all stable roots vs explicit warm/cool policy | can change low-order predicted cooling discontinuously |

These are **project sensitivity ranges**, selected to reveal fragility. They are
not statistical 95% intervals.

## 2. Required reporting rule

A numerical conclusion is not considered robust if it changes sign or changes
PASS/FAIL category under a reasonable combination of the screening ranges
above.

For every headline simulation result, report at least:

- nominal assumptions;
- one-at-a-time sensitivity for major parameters;
- at least one joint adverse-case combination;
- stable-root count and root-selection policy;
- whether the result is water-limited or vapor-transfer-limited;
- whether `M_h` and `M_m` are coupled or independent in that run.

## 3. Model-form alternatives to compare

### External exchange

A. current Churchill–Chu-like low-order natural-convection screen;

B. prescribed E3 vapor-renewal plane;

C. split `M_h` / `M_m` model;

D. future buoyancy-driven corridor flow / boundary-layer model;

E. future CFD or experimentally fitted surrogate.

### Heat spreading

A. lumped `U_body` coupling;

B. 2-D anisotropic in-plane conduction;

C. future contact-resistance + spatial wetting map.

### Moisture/salt transport

A. normalized one-dimensional liquid transport;

B. protected internal liquid route with evaporation concentrated at exterior terminals;

C. future porous-media flow with measured permeability and capillary-pressure curves.

## 4. Decision categories

- **ROBUST:** conclusion survives all predeclared reasonable model variants and sensitivity ranges.
- **MODEL-SENSITIVE:** sign remains the same but magnitude or decision category changes.
- **FORM-UNCERTAIN:** conclusion changes sign or depends on one unvalidated model form.
- **MEASUREMENT-RESOLVABLE:** a defined bench measurement can directly distinguish the competing models.

At present, absolute garment cooling wattage is **FORM-UNCERTAIN**. The need to
avoid equating geometric area with accessible vapor-transfer area is more
robust, because it is supported by the E3 diffusion screen and is directly
measurable through near-surface RH and evaporation tests.

## 5. Next implementation step

Add a parameter-sweep script that samples `U_body`, `M_h`, `M_m`, RH, and
radiative exchange, then reports the fraction of screened assumptions under
which a design advantage remains positive. This is a sensitivity study, not a
probabilistic reliability estimate unless justified probability distributions
are later supplied.
