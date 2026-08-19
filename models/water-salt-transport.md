# Water / Salt Transport Model

Status: governing-model specification; numerical implementation pending.

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

Any proposed "salt removal" mechanism must therefore be one of:

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

A design objective can be set such as:

- `f_leak <= 0.10` for at least 90% terminal evaporation;
- `f_leak <= 0.01` for at least 99% terminal evaporation.

These are possible engineering targets, not established requirements.

## 8. Why leakage matters

If water evaporates continuously along a small internal liquid channel while salt remains, local salt concentration rises upstream of the intended exterior evaporator. This can increase precipitation risk in inaccessible small pores.

The design response is not to make salt volatile. It is to control **where water phase change is allowed to occur**.

## 9. Ordinary washable variant

A dedicated terminal/crystallization architecture is not mandatory. Ordinary sports textiles also retain sweat residue. The default garment may simply use sufficiently open, washable capillary/exterior structures if comparative testing shows no abnormal clogging or performance loss relative to conventional controls.

The dedicated protected-channel architecture should be justified experimentally rather than added by default.

## 10. Variables

| Symbol | Meaning | SI unit | Assumption/type |
|---|---|---:|---|
| `epsilon_l` | liquid-filled porosity | 1 | 0–1 scalar/field |
| `epsilon_g` | gas-filled porosity | 1 | 0–1 scalar/field |
| `rho_l` | liquid density | kg/m³ | scalar/field |
| `rho_v` | water-vapor density | kg/m³ | scalar/field |
| `u_l` | liquid Darcy/superficial velocity | m/s | vector field |
| `u_g` | gas velocity | m/s | vector field |
| `C_s` | dissolved salt concentration | kg/m³ or mol/m³ | use one consistent basis |
| `D_eff` | effective vapor diffusivity | m²/s | porous-media parameter |
| `D_s` | liquid salt diffusivity | m²/s | parameter |
| `S_evap` | water phase-change source | kg/(m³ s) | water only |
| `S_precip` | salt precipitation source | mass/(m³ s) | salt only |
| `f_leak` | internal evaporation fraction | 1 | 0–1 |

## 11. Dimensional check

For the water-vapor diffusion term:

\[
D_{eff}\nabla\rho_v
\sim \frac{m^2}{s}\frac{kg/m^3}{m}
=\frac{kg}{m^2 s}
\]

which is a mass flux, consistent with the advective term `rho_v u_g`.

## 12. Minimum future numerical experiment

A 1D internal-channel + terminal-evaporator model should sweep:

- internal vapor leakage conductance;
- terminal vapor conductance;
- liquid flow rate;
- incoming normalized salt concentration `C/C_sat`;
- channel length;
- wash/drain boundary condition.

Primary output:

- fraction of water evaporating internally vs terminally;
- maximum normalized salt concentration along the internal path;
- location and onset condition of precipitation.

Until that numerical model is added, no exact crystallization threshold is claimed.
