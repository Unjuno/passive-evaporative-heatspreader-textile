# Split Sensible-Heat and Vapor-Transfer Model

Date: 2026-08-19

## Status

**Simulation / model-form refinement. Not a measurement.**

This note supersedes the simplifying assumption that one exterior exchange
multiplier must scale sensible convection and water-vapor mass transfer by the
same factor.

## 1. Motivation

The periodic E3 rib-diffusion model estimates a **vapor mass-transfer** effect.
It does not establish that sensible convective heat transfer increases by the
same factor. A ribbed wet exterior may therefore have:

- strong enhancement of vapor transport;
- weaker enhancement of sensible heat transfer;
- or, in some geometries, different signs/magnitudes of the two effects.

The thermal screen now permits those mechanisms to be varied independently.

## 2. Energy balance

The split model uses

\[
q''_{body} + M_h h (T_\infty-T_s) + h_r(T_\infty-T_s)
- L_v\dot m''_{evap}=0,
\]

with

\[
\dot m''_{evap}=
\min\left[
M_m k_m\left(\rho_{v,sat}(T_s)-\phi_\infty\rho_{v,sat}(T_\infty)\right)_+,
\dot m''_{feed}
\right].
\]

### Variables

| Symbol | Meaning | SI unit | Definition / assumption |
|---|---|---:|---|
| `M_h` | sensible convective heat-transfer multiplier | 1 | scales only `h` |
| `M_m` | vapor mass-transfer multiplier | 1 | scales only `k_m` |
| `h` | baseline convective heat-transfer coefficient | W m^-2 K^-1 | low-order natural-convection correlation |
| `k_m` | baseline vapor mass-transfer coefficient | m s^-1 | heat/mass analogy screen |
| `h_r` | linearized radiation coefficient | W m^-2 K^-1 | not multiplied by `M_h` or `M_m` |
| `L_v` | water latent heat | J kg^-1 | model constant |
| `T_s` | wet exterior surface temperature | K or °C difference-compatible | solved equilibrium |
| `phi_inf` | ambient relative humidity | 1 | 0 to 1 |

### Dimensional check

`M_h` and `M_m` are dimensionless. Therefore

\[
M_h h\Delta T
\]

has units W m^-2, while

\[
L_v M_m k_m\Delta\rho_v
\]

has units

\[
(J\,kg^{-1})(m\,s^{-1})(kg\,m^{-3})=W\,m^{-2}.
\]

The balance is dimensionally consistent.

## 3. Relationship to E3

E3's periodic diffusion result is interpreted only as a candidate constraint on
`M_m`. It must **not** be copied into `M_h` automatically.

Example workflow:

1. choose geometry and air-renewal boundary assumption in E3;
2. obtain a whole-area vapor multiplier `M_m`;
3. sweep `M_h` independently over a conservative interval;
4. report all stable thermal equilibria or state an explicit root-selection
   policy;
5. do not convert the result into a garment-performance claim without physical
   validation.

## 4. Current executable implementation

- `simulations/split_heat_mass_screen.py`
- `tests/test_split_heat_mass_screen.py`

The regression test verifies that setting `M_h = M_m = M` reproduces the
legacy coupled-multiplier formulation at the same environment and body-side
coupling.

## 5. Interpretation

This refinement is deliberately conservative. It prevents a large E3 vapor
multiplier from automatically creating an equally large sensible-heat
multiplier in the energy balance.

It also makes hot-ambient risk easier to study: increasing `M_h` can increase
inward sensible heat gain when `T_inf > T_s`, whereas increasing `M_m` can still
increase latent removal if vapor-pressure driving force remains positive.

## 6. Open questions

- What range of `M_h` is physically plausible for the same hierarchical rib
  geometry that produces a given `M_m`?
- Does natural convection couple `M_h` and `M_m` strongly enough that they
  cannot be treated independently?
- Does a macro corridor improve vapor renewal while also increasing unwanted
  hot-air sensible heat transfer?
- Does the multi-equilibrium behavior persist when the external boundary layer
  is solved rather than represented by low-order correlations?
