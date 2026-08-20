# Water / Salt Transport Model

Status: governing specification plus a normalized 1D bookkeeping implementation in `simulations/water_salt_1d.py`.

This model exists to prevent a recurring conceptual error: **water can evaporate from the garment; sweat salts are treated as nonvolatile under garment operating conditions.**

## 1. Phases and species

Tracked quantities:

- liquid water;
- water vapor;
- dissolved nonvolatile salt/electrolyte surrogate;
- precipitated solid salt where concentration exceeds a solubility limit.

The salt species is a conservative surrogate for the nonvolatile fraction of sweat. Real sweat contains multiple ions and organics; later experiments may use synthetic sweat rather than a single-salt approximation.

## 2. Liquid water balance

In a porous transport region:

\[
\frac{\partial (\epsilon_l \rho_l)}{\partial t}
+ \nabla\cdot(\rho_l \mathbf{u}_l)
= S_{in} - S_{evap} - S_{drain}
\]

where `S_evap` is nonzero only where liquid-to-vapor phase change is permitted by the local architecture/model.

## 3. Water vapor balance

In a gas-accessible region:

\[
\frac{\partial (\epsilon_g \rho_v)}{\partial t}
+ \nabla\cdot(\rho_v \mathbf{u}_g - D_{eff}\nabla\rho_v)
= S_{evap}
\]

At the external boundary, water vapor can leave to ambient air according to an appropriate mass-transfer boundary condition.

## 4. Dissolved salt balance

\[
\frac{\partial (\epsilon_l C_s)}{\partial t}
+ \nabla\cdot(C_s \mathbf{u}_l - D_s\nabla C_s)
= S_{dissolve} - S_{precip} - S_{salt,drain}
\]

Salt can move with liquid water and by liquid-phase diffusion. It does not receive an evaporation sink.

## 5. Solid salt balance

\[
\frac{\partial m_{s,solid}}{\partial t}
= S_{precip} - S_{dissolve} - S_{solid,removed}
\]

The precipitation/dissolution constitutive law can initially be represented by a concentration cap or equilibrium-solubility rule and later replaced by measured kinetics if required.

## 6. Zero salt vapor flux

The garment-temperature model imposes:

\[
\mathbf{J}_{salt,vapor}=0
\]

and therefore:

\[
\dot m_{salt,vapor}=0
\]

Any proposed salt-removal mechanism must therefore be one of:

- drainage/purge of salt-containing liquid;
- washing/rinsing;
- mechanical removal of precipitated solids;
- replacement of a contaminated component.

Salt is never removed by the water-vapor stream in this model.

## 7. Protected internal transport variant

A useful architecture for testing separates transport and evaporation:

- internal capillary route: high liquid conductance, low vapor leakage;
- terminal exterior region: high liquid access and high vapor conductance.

Define:

\[
f_{leak}=\frac{\dot m_{evap,internal}}{\dot m_{evap,total}}
\]

Possible design targets include `f_leak <= 0.10` for at least 90% terminal evaporation or `f_leak <= 0.01` for at least 99% terminal evaporation. These are engineering examples, not established requirements.

## 8. Normalized 1D precipitation screen

The current executable screen normalizes inlet water flow to `W_0=1` and concentration by a saturation concentration:

\[
c_0 = \frac{C_{in}}{C_{sat}}
\]

For a simple steady path with no salt loss and total internal water-loss fraction `f_leak`, the remaining normalized water flow is:

\[
W_{out}=1-f_{leak}
\]

Before precipitation, normalized dissolved-salt inventory is `S_0=c_0`. Saturation can first be reached when:

\[
W_{out} \le S_0
\]

which gives the simple onset condition:

\[
f_{leak} \ge 1-c_0
\]

Examples under this deliberately simple model:

- `C_in/C_sat = 0.10` -> saturation requires at least 90% internal water loss;
- `0.20` -> at least 80%;
- `0.40` -> at least 60%;
- `0.80` -> at least 20%.

This does **not** establish real sweat crystallization thresholds. It shows that, for dilute inlet solution in a continuously replenished through-flow path, moderate distributed evaporation need not automatically imply upstream precipitation. Real pore-scale dry-out, stagnant zones, mixed salts, activities, nucleation, and repeated cycles can behave differently.

The executable implementation conserves inlet salt between upstream solid deposition and salt reaching the terminal in liquid form. It contains no salt-vapor term.

## 9. Why leakage can still matter

If water evaporates continuously along a small internal liquid channel while salt remains, local salt concentration rises upstream of the intended exterior evaporator. Stagnant/local dry-out can be more severe than the simple through-flow model.

The design response is not to make salt volatile. It is to control **where water phase change is allowed to occur** and then compare degradation against an ordinary textile control.

## 10. Ordinary washable variant

A dedicated terminal/crystallization architecture is not mandatory. Ordinary sports textiles also retain sweat residue. The default garment may simply use sufficiently open, washable capillary/exterior structures if comparative testing shows no abnormal clogging or performance loss relative to conventional controls.

The dedicated protected-channel architecture should be justified experimentally rather than added by default.

## 11. Variables

| Symbol | Meaning | SI unit | Assumption/type |
|---|---|---:|---|
| `epsilon_l` | liquid-filled porosity | 1 | 0–1 scalar/field |
| `epsilon_g` | gas-filled porosity | 1 | 0–1 scalar/field |
| `rho_l` | liquid density | kg/m³ | scalar/field |
| `rho_v` | water-vapor density | kg/m³ | scalar/field |
| `u_l` | liquid Darcy/superficial velocity | m/s | vector field |
| `u_g` | gas velocity | m/s | vector field |
| `C_s` | dissolved salt concentration | kg/m³ or mol/m³ | use one consistent basis |
| `C_sat` | saturation concentration for chosen surrogate/system | same as `C_s` | parameter |
| `c_0` | normalized inlet concentration `C_in/C_sat` | 1 | 0–1 in current screen |
| `D_eff` | effective vapor diffusivity | m²/s | porous-media parameter |
| `D_s` | liquid salt diffusivity | m²/s | parameter |
| `S_evap` | water phase-change source | kg/(m³ s) | water only |
| `S_precip` | salt precipitation source | mass/(m³ s) | salt only |
| `f_leak` | internal evaporation fraction | 1 | 0–1 |

## 12. Dimensional checks

For the water-vapor diffusion term:

\[
D_{eff}\nabla\rho_v
\sim \frac{m^2}{s}\frac{kg/m^3}{m}
=\frac{kg}{m^2 s}
\]

which is a mass flux, consistent with `rho_v u_g`.

For normalized concentration:

\[
c_0 = \frac{C_{in}}{C_{sat}}
\]

has identical concentration units in numerator and denominator, so `c_0` is dimensionless.

## 13. Remaining model extensions

The normalized 1D implementation should eventually be extended to include:

- nonuniform/stagnant flow;
- pore-scale or segment dry-out;
- measured synthetic-sweat solubility/activity behavior;
- repeated evaporation/wash cycles;
- precipitation/dissolution kinetics;
- coupling to actual capillary hydraulic resistance and wetting changes.

Until those are added and experimentally constrained, no exact real-garment crystallization threshold is claimed.
