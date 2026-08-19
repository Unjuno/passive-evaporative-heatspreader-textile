# Identifying Effective Exterior Area (`alpha`)

## Purpose

The exterior structure may have a large geometric surface area without providing a proportional increase in evaporation, because neighboring wet ribs/fins can share the same humid boundary layer. The parameter `alpha` is therefore treated as an experimentally inferred effective-accessibility factor rather than a material constant.

For the current rectangular-rib screen:

\[
G_{panel}\approx1+\frac{2h}{p}
\]

\[
M\approx1+\alpha f(G_{panel}-1)
\]

where `M` is the effective whole-garment exchange multiplier relative to a flat wet reference.

## Experimental identification strategy

Use a family of samples with known projected area and measured exterior geometry.

Suggested first set:

- same base textile and chemistry;
- same approximate rib height, e.g. ~2.5 mm;
- pitch: 0.8, 1.0, 1.5 mm;
- comparable panel coverage;
- same liquid feed per projected area;
- same artificial-skin setpoint and ambient chamber condition.

Measure:

1. heater power;
2. liquid feed and water balance;
3. surface temperature;
4. ambient T/RH;
5. T/RH approximately 2, 5, 10, 20, and 40 mm above rib tips;
6. actual wet fraction of the exterior texture;
7. rib height under wet/compressed operating conditions.

## Primary inference

Do **not** infer `alpha` from evaporation mass alone if the objective is body cooling. First fit/identify an effective exchange level using the measured thermal and vapor field, then map that exchange level back to `alpha` through the known geometry.

Because the present lumped model can have multiple stable equilibria, a fitted `M` must also report:

- number of model roots under the fitted condition;
- which branch corresponds to the measured surface temperature;
- sensitivity to initial temperature and root-search method.

## Boundary-layer-overlap indicator

Define a simple concentration indicator from measured near-surface humidity:

\[
B_H = \frac{\rho_v(z_{near})-\rho_{v,\infty}}
{\rho_{v,sat}(T_s)-\rho_{v,\infty}}
\]

where `z_near` is a fixed small distance above the rib tips.

Interpretation:

- `B_H -> 0`: near-surface air remains close to ambient humidity; exterior exchange is relatively unblocked.
- `B_H -> 1`: near-surface air approaches saturation at the surface temperature; local vapor-removal resistance is large.

This is an experimental diagnostic, not a universal correlation.

## Variables

| Symbol | Meaning | SI unit | Range/type |
|---|---|---:|---|
| `alpha` | effective accessibility of added exterior area | 1 | nominally 0–1 in the basic geometry model |
| `M` | effective exchange multiplier | 1 | >=1 for enhancement model |
| `G_panel` | local geometric area multiplier | 1 | >=1 |
| `f` | structured-panel projected coverage | 1 | 0–1 |
| `h` | rib height | m | >0 |
| `p` | rib pitch | m | >0 |
| `B_H` | near-surface humidity-blocking indicator | 1 | approximately 0–1 under intended definition |
| `rho_v` | water-vapor density | kg/m³ | measured/derived |
| `z_near` | sensor distance above rib tips | m | fixed by protocol |

## Dimensional check

`B_H` is a ratio of vapor-density differences:

\[
\frac{kg/m^3}{kg/m^3}=1
\]

so it is dimensionless.

## Hypothesis / test / decision / alternatives / uncertainty

### H

At fixed height and water input, reducing pitch initially increases effective exterior exchange, but beyond a point humid-boundary-layer overlap causes diminishing or negative returns.

### T

Compare at least three pitches under 35 °C / 70% RH / equal water input, n>=3 per geometry, with heater-power and near-field RH/T profiles.

### D

Support the hypothesis if geometric area continues to rise while fitted `alpha` or body-cooling gain per added geometric area declines at the densest geometry.

### C

Alternative explanations include incomplete wetting, rib collapse, different liquid pressure drop, manufacturing differences, or sensor disturbance of the local boundary layer.

### U

Dominant uncertainties are local humidity sensing, sensor position, true wet surface temperature, rib geometry under load/wetting, liquid feed, and model inadequacy. Report these separately before combining uncertainty.
