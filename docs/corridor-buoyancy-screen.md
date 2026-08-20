# Moist-Air Corridor Buoyancy Screen

Date: 2026-08-19

## Status

**Simulation / hypothesis generator. Not CFD and not a measurement.**

This model is the first step toward replacing the prescribed E3 refreshed-air
plane with an explicit air-renewal mechanism.

## 1. Physical question

The hierarchical exterior proposes larger vertical/open corridors between wet
microstructured evaporation fields. The corridor may support passive air
renewal, but the buoyancy sign is not obvious because evaporation changes both:

- temperature: cooler air is denser;
- humidity: more humid air is lighter at fixed temperature.

These effects can oppose each other.

## 2. Screening model

For a wide vertical slot of gap `b`, the hydrostatic density head is represented
as

\[
\frac{dp}{dz} \approx g(\rho_\infty-\rho_{ch}).
\]

For fully developed laminar parallel-plate flow, the signed mean speed is
screened as

\[
\bar u \approx \frac{b^2}{12\mu}\frac{dp}{dz}
=\frac{b^2g(\rho_\infty-\rho_{ch})}{12\mu}.
\]

Positive velocity means the prescribed channel air is lighter than ambient and
tends upward; negative velocity means a downward tendency.

### Variables

| Symbol | Meaning | SI unit | Assumption |
|---|---|---:|---|
| `b` | corridor/slot gap | m | wide-slot approximation |
| `mu` | air dynamic viscosity | Pa s | fixed screening value |
| `rho_inf` | ambient moist-air density | kg m^-3 | ideal dry-air + water-vapor mixture |
| `rho_ch` | prescribed mean channel-air density | kg m^-3 | channel T/RH are inputs, not solved |
| `u_bar` | signed mean channel velocity | m s^-1 | fully developed laminar friction balance |

### Dimensional check

\[
\frac{b^2g\Delta\rho}{\mu}
=\frac{m^2(m\,s^{-2})(kg\,m^{-3})}{kg\,m^{-1}s^{-1}}
=m\,s^{-1}.
\]

## 3. Thermo-solutal neutral condition

For the project's common ambient screen of 35 °C / 70% RH, the model finds a
neutral-density condition near 34 °C at roughly 90% RH.

That means, at approximately 34 °C:

- channel RH below the neutral value tends to make the channel air denser than ambient;
- channel RH above the neutral value tends to make it lighter than ambient.

At lower channel temperatures, even saturated channel air can remain denser
than the 35 °C / 70% RH ambient. Therefore **evaporation does not guarantee an
upward chimney flow**. A passive corridor may flow downward, upward, reverse,
or remain weak depending on its coupled temperature/humidity state.

This is an important correction to any design intuition that simply adding a
vertical groove automatically creates a beneficial upward stack effect.

## 4. Outputs

`simulations/corridor_buoyancy_screen.py` reports:

- signed idealized slot velocity;
- flow direction;
- hydraulic-diameter Reynolds number;
- height-based vapor Peclet number;
- idealized residence time;
- neutral-density RH curve.

## 5. Limitations

The current screen does **not** solve:

- self-consistent channel temperature and humidity;
- entrance/exit pressure losses;
- garment curvature;
- ambient wind or body motion;
- turbulence;
- plume entrainment;
- coupling to local evaporation rate;
- multiple interacting corridors;
- horizontal/oblique channel behavior.

The parallel-plate relation can become invalid as Reynolds number increases.
Results should therefore be used mainly to identify sign changes, scaling, and
cases requiring a higher-fidelity flow model.

## 6. Design consequence

The next exterior prototype should not rely on one-way vertical chimney action
alone. Candidate macro-renewal paths should include combinations such as:

- open-ended vertical valleys;
- intersecting vertical and transverse channels;
- discontinuous evaporation islands separated by open gaps;
- spacer-knit cavities with multiple openings;
- pleat channels that can exploit wearer motion or weak external wind even when
  buoyancy is near neutral.

## 7. Next model step

Couple a 1-D channel conservation model for heat and water vapor to the buoyancy
pressure balance so that channel T/RH evolve along the flow direction rather
than being prescribed. That model can then provide physically related
constraints on both `M_h` and `M_m`.
