# Governing Equations and Screening Assumptions

This document describes the current low-order numerical model. It is a screening model, not CFD and not a validated garment-performance model.

## 1. Evaporative latent heat

\[
\dot Q_{evap} = \dot m_{evap} L_v
\]

where `m_dot_evap` is the water evaporation rate and `L_v` is water latent heat of vaporization.

Example: at `L_v = 2.42 MJ/kg`, an additional 50 W of latent heat corresponds to approximately:

\[
\dot m = \frac{50}{2.42\times10^6} \approx 2.07\times10^{-5}\ kg/s \approx 74.4\ g/h
\]

This is latent heat at the evaporation site. It is not automatically equal to heat removed from the body, because part of the latent heat can be supplied by ambient convection/radiation.

## 2. Exterior vapor-transfer capacity

The current model uses:

\[
\dot m''_{cap} = M k_m \left[\rho_{v,sat}(T_s)-\phi_\infty\rho_{v,sat}(T_\infty)\right]_+
\]

and limits actual evaporation by the supplied liquid-water flux:

\[
\dot m''_{evap}=\min(\dot m''_{cap},\dot m''_{water})
\]

where `[x]_+ = max(x,0)`.

## 3. Surface energy balance

Per projected area:

\[
U_b(T_{skin}-T_s)+M h_c(T_\infty-T_s)+h_r(T_\infty-T_s)-L_v\dot m''_{evap}=0
\]

Terms are defined positive toward the evaporating surface before the latent sink.

Body-side cooling is:

\[
\dot Q_{body}=A U_b(T_{skin}-T_s)
\]

The project compares `Q_dot_body` between an advanced sample and a flat fast-dry control at the same commanded water input.

## 4. Natural-convection screening

The current implementation uses a Churchill-Chu-type vertical-plate correlation as a low-order approximation. The buoyancy driver is estimated from the density difference between ambient moist air and saturated air adjacent to the wet surface.

This approximation is intentionally treated as uncertain for a ribbed textile canopy because temperature and humidity buoyancy can oppose or partially cancel one another, and the true flow is three-dimensional.

The correlation is used only to screen design regions before physical testing.

## 5. Rib geometry

For a rectangular-rib approximation:

\[
G_{panel}\approx1+\frac{2h}{p}
\]

For structured-panel coverage `f` and effective added-area accessibility `alpha`:

\[
M\approx1+\alpha f(G_{panel}-1)
\]

This construction deliberately prevents the model from treating all geometric surface area as automatically useful.

## 6. Heat-spreader abstraction

The current integrated surface model represents body-to-evaporator thermal coupling with an effective coefficient `U_b`.

Separate earlier spatial models represent in-plane heat spreading by a 2D conduction equation of the form:

\[
\rho c t\frac{\partial T}{\partial t}=\nabla\cdot(t\mathbf{k}_{\parallel}\nabla T)+q''_{sources}-q''_{sinks}
\]

where `k_parallel` may be isotropic or anisotropic.

For steady screening:

\[
0=\nabla\cdot(t\mathbf{k}_{\parallel}\nabla T)+q''_{sources}-q''_{sinks}
\]

The main qualitative result from that branch is that lateral spreading is most valuable when evaporation is spatially nonuniform. If evaporation is already uniform, increasing in-plane conductivity produces much smaller benefit.

## 7. Salt mass balance

Salt is treated as nonvolatile under garment operating conditions:

\[
\dot m_{salt,vapor}=0
\]

Salt can be advected in liquid:

\[
\frac{\partial (\epsilon_l C_s)}{\partial t}+\nabla\cdot(C_s\mathbf{u}_l)=S_{dissolution}-S_{precipitation}
\]

Water evaporation can increase liquid concentration until precipitation occurs. Any purge removes salt only by removing salt-containing liquid. No model should represent salt loss as an evaporative vapor flux.

## 8. Variables

| Symbol | Meaning | SI unit | Definition / assumption | Type |
|---|---|---:|---|---|
| `A` | projected active area | m² | area used to normalize garment comparison | scalar |
| `T_skin` | artificial-skin temperature | K or °C difference-compatible | currently 34 °C screening setpoint | scalar |
| `T_s` | wet exterior surface temperature | K or °C difference-compatible | solved equilibrium value | scalar |
| `T_inf` | ambient air temperature | K or °C difference-compatible | chamber condition | scalar |
| `phi_inf` | ambient relative humidity | 1 | 0–1 | scalar |
| `L_v` | latent heat of water vaporization | J/kg | temperature-dependent; screened with a representative value | scalar |
| `m_dot_evap` | evaporation rate | kg/s | water only | scalar |
| `m_dot_water` | supplied liquid-water rate | kg/s | same input across comparison samples | scalar |
| `rho_v,sat` | saturated water-vapor density | kg/m³ | function of temperature | scalar field/value |
| `k_m` | exterior mass-transfer coefficient | m/s | natural-convection screening | scalar |
| `h_c` | convective heat-transfer coefficient | W/(m² K) | natural-convection screening | scalar |
| `h_r` | linearized radiative coefficient | W/(m² K) | screening approximation | scalar |
| `U_b` | effective body-to-evaporator coupling | W/(m² K) | aggregates textile/contact coupling | scalar |
| `M` | effective exterior exchange multiplier | 1 | relative to flat wet textile | scalar |
| `G_panel` | local geometric surface multiplier | 1 | rectangular-rib approximation | scalar |
| `alpha` | effective accessibility of added area | 1 | 0–1 by definition in the basic model | scalar |
| `f` | structured-panel coverage | 1 | 0–1 | scalar |
| `h` | rib height | m | geometric design variable | scalar |
| `p` | rib pitch | m | geometric design variable | scalar |
| `k_parallel` | in-plane conductivity tensor | W/(m K) | isotropic or anisotropic | tensor |
| `C_s` | dissolved salt concentration | kg/m³ or mol/m³ | consistent basis required within a model | scalar field |

## 9. Dimensional checks

### Latent heat

\[
(kg/s)(J/kg)=J/s=W
\]

### Rib geometry

\[
h/p=m/m=1
\]

so `G_panel` and `M` are dimensionless.

### Body heat flux

\[
A U_b \Delta T = m^2\frac{W}{m^2 K}K=W
\]

## 10. Numerical caution

The model can exhibit abrupt changes when evaporation switches between transfer-limited and water-supply-limited regimes or when multiple equilibrium roots exist. Threshold values such as a required `M` should therefore be treated as approximate design screens and tested for numerical stability and physical plausibility before use.
