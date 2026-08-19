# Self-Consistent 1-D Corridor Model

Date: 2026-08-19  
Classification: **SIMULATION / SCREENING — NOT PHYSICAL GARMENT DATA**

## 1. Why this model exists

E3 showed that wet micro-ribs lose most of their geometric-area benefit if the
whole field sits beneath a stagnant humid layer.  The first corridor model then
showed that moist-air buoyancy can reverse sign, but that model prescribed the
channel temperature and RH.

`simulations/self_consistent_corridor_1d.py` removes that prescribed-state
assumption for one deliberately limited geometry: a straight rectangular duct
that exchanges air primarily through its ends.

The model solves the following quantities together:

1. signed buoyancy-driven air speed;
2. wet-wall temperature;
3. mean and outlet channel temperature;
4. mean and outlet water-vapor concentration/RH;
5. evaporation flux;
6. body-to-wet-wall heat flux.

It is a limiting-case model for a covered or poorly laterally ventilated
corridor.  It is **not** a model of a fully open exterior groove.  That
distinction is central to the current design decision.

## 2. Geometry and flow closure

For rectangular corridor width `w`, depth `d`, and length `L`:

\[
A = wd
\]

\[
D_h = \frac{4A}{2(w+d)} = \frac{2wd}{w+d}
\]

The rectangular-duct Darcy Poiseuille number is screened as

\[
Po = 96(1 - 1.3553\alpha + 1.9467\alpha^2 - 1.7012\alpha^3
+0.9564\alpha^4 -0.2537\alpha^5)
\]

where

\[
\alpha=\frac{\min(w,d)}{\max(w,d)}.
\]

The signed fully-developed laminar screening relation is

\[
\bar u = \frac{2D_h^2}{Po\,\mu}
 g\Pi(\rho_\infty-\bar\rho),
\]

where `Pi` is the signed vertical projection of the corridor axis.

This flow closure and the channel thermodynamic state are solved iteratively by
root finding rather than prescribing `T_channel` and `RH_channel`.

## 3. Heat and vapor approach along the corridor

Screening transfer coefficients are

\[
h_c = \frac{Nu\,k_{air}}{D_h}
\]

and

\[
k_m = \frac{Sh\,D_v}{D_h}.
\]

The present code uses fixed `Nu = Sh = 7.54` only as a low-order laminar
screen.  Exact values depend on geometry and boundary conditions and remain a
model-form uncertainty.

For wet perimeter `P_w`, air mass flow `m_dot`, and corridor length `L`:

\[
NTU_h=\frac{h_cP_wL}{\dot m c_p}
\]

\[
NTU_m=\frac{k_mP_wL}{|\bar u|A}.
\]

The mean exponential approach factor is

\[
\Phi(NTU)=\frac{1-e^{-NTU}}{NTU}.
\]

Therefore

\[
\bar T = T_s + (T_\infty-T_s)\Phi(NTU_h)
\]

and

\[
\bar\rho_v = \rho_{v,sat}(T_s)
-\left[\rho_{v,sat}(T_s)-\rho_{v,\infty}\right]\Phi(NTU_m).
\]

The mean fraction of the inlet wall-to-air vapor-density difference retained in
the corridor is therefore exactly `Phi(NTU_m)` in this model.  A large axial
Péclet number alone does **not** imply useful vapor renewal if `NTU_m` is also
very large.

## 4. Wet-wall energy balance

Wet-wall temperature is solved from

\[
U_{body}(T_{skin}-T_s)
+h_c(\bar T-T_s)
=L_v k_m\left[\rho_{v,sat}(T_s)-\bar\rho_v\right]_+.
\]

The first term is heat from the wearer/spreader to the wet wall.  The second
term is sensible heat from channel air to the wall when the air is hotter.  The
right-hand side is latent heat demand.

A negative reported body heat flux means the local model predicts heat flowing
from the wet surface toward the body rather than useful wearer cooling.

## 5. Variable table

| Symbol | Meaning | SI unit | Definition / assumption |
|---|---|---:|---|
| `w` | corridor width | m | in-plane duct width |
| `d` | corridor depth | m | gap normal to garment surface |
| `L` | corridor/segment length | m | distance between end-renewal openings |
| `A` | flow cross-section | m² | `wd` |
| `D_h` | hydraulic diameter | m | `2wd/(w+d)` |
| `Po` | Darcy Poiseuille number | 1 | rectangular laminar resistance screen |
| `u` | signed mean corridor velocity | m/s | root of buoyancy/friction closure |
| `Pi` | vertical projection | 1 | +1 upward axis, 0 horizontal, -1 downward axis |
| `h_c` | sensible transfer coefficient | W/(m² K) | fixed-Nu screen |
| `k_m` | vapor mass-transfer coefficient | m/s | fixed-Sh screen |
| `NTU_h` | heat exchange number | 1 | `h_c P_w L/(m_dot c_p)` |
| `NTU_m` | vapor exchange number | 1 | `k_m P_w L/(|u|A)` |
| `Phi` | mean driving-force retention | 1 | `(1-exp(-NTU))/NTU` |
| `U_body` | body-to-wet-wall coupling | W/(m² K) | screening parameter |
| `T_s` | wet-wall temperature | °C | solved algebraically |
| `rho_v` | water-vapor density | kg/m³ | ideal-mixture screen |
| `Pe_m` | axial mass Péclet number | 1 | `|u|L/D_v` |

## 6. Unit checks

For the flow closure,

\[
\frac{D_h^2}{\mu} g\Delta\rho
\rightarrow
\frac{m^2}{Pa\,s}\frac{m}{s^2}\frac{kg}{m^3}
=\frac{m}{s}.
\]

For the vapor NTU,

\[
\frac{k_m P_w L}{uA}
\rightarrow
\frac{(m/s)m m}{(m/s)m^2}=1.
\]

Both are dimensionally consistent.

## 7. Current deterministic findings

Default screen: wet floor only, `U_body=100 W/(m² K)`.

### 7.1 35 °C / 70% RH, 100 mm end-renewed duct

| width × depth | signed velocity | Pe_m | mean RH | wet-wall body heat flux |
|---|---:|---:|---:|---:|
| 3 × 2 mm | +0.228 mm/s | 0.81 | ~100.0% | +0.10 W/m² |
| 6 × 3 mm | +0.594 mm/s | 2.12 | ~99.99% | +0.40 W/m² |
| 10 × 5 mm | +1.60 mm/s | 5.70 | ~99.92% | +1.81 W/m² |

Interpretation: the small/medium covered channels are diffusion-dominated or
mixed, and all three approach a nearly saturated internal air state.  The
natural-buoyancy end flow is not enough to maintain a large vapor driving force.

### 7.2 Humidity and hot-ambient sign reversal, 10 × 5 × 100 mm

| environment | signed velocity | Pe_m | mean RH | wet-wall body heat flux |
|---|---:|---:|---:|---:|
| 35 °C / 50% RH | +4.82 mm/s | 17.2 | 99.6% | +9.94 W/m² |
| 35 °C / 70% RH | +1.60 mm/s | 5.70 | 99.9% | +1.81 W/m² |
| 35 °C / 85% RH | -1.01 mm/s | 3.59 | 99.97% | +0.42 W/m² |
| 40 °C / 70% RH | -14.94 mm/s | 53.4 | 99.0% | **-1.67 W/m²** |

Positive velocity is along an upward-positive vertical corridor axis.  Negative
velocity means the self-consistent density state drives downward flow.

The 40 °C result is especially important: stronger buoyancy-driven throughput
does not guarantee wearer cooling.  In the local wet-wall screen, hot-air
sensible input makes the body-side heat flux slightly inward.

### 7.3 Segment length, 10 × 5 mm at 35 °C / 70% RH

| end-to-end length | velocity | Pe_m | mean RH | wet-wall body heat flux |
|---:|---:|---:|---:|---:|
| 20 mm | +1.38 mm/s | 0.98 | 99.65% | +7.67 W/m² |
| 100 mm | +1.60 mm/s | 5.70 | 99.92% | +1.81 W/m² |
| 200 mm | +1.63 mm/s | 11.65 | 99.96% | +0.92 W/m² |

The longer duct has a larger axial Péclet number but a **smaller useful vapor
driving force** because its air becomes more equilibrated with the wet wall.
This is why `Pe_m` and `NTU_m`/mean-RH must be reported together.

## 8. Design decision from this model

The project should **not** optimize the exterior as a set of long, covered,
end-vented micro-chimneys.

Preferred direction:

- open valleys rather than enclosed ducts;
- frequent interruptions / cross-openings;
- discontinuous evaporator islands;
- lateral exposure to ambient air along the path, not only at its ends;
- geometry that works with either upward or downward buoyancy flow;
- hot-ambient shielding/routing so stronger air exchange does not simply carry
  sensible heat inward.

This does not prove the open-valley design works.  It establishes a falsifiable
reason to compare it against the covered-duct limit.

## 9. H / T / D / C / U

**H:** end-renewed covered corridors saturate too strongly at the primary hot/
humid condition to provide the air-renewal assumed by the earlier E3 boundary.

**T:** self-consistent signed velocity + wall/air heat and vapor state for
3×2, 6×3, and 10×5 mm rectangular corridors over 20–200 mm lengths and RH
50/70/85%, plus 40 °C hot-ambient screening.

**D:** supported numerically when mean RH approaches saturation and useful
wet-wall body heat flux falls despite nonzero signed flow; physical decision
requires E3c.

**C:** the model is intentionally pessimistic for an exterior groove because it
allows ambient renewal mainly at the ends.  A laterally open groove may perform
substantially better.  Fixed `Nu/Sh`, neglected axial diffusion, and omitted
entrance mixing are also important alternatives.

**U:** dominant uncertainty is model form, not numerical root tolerance.  The
most important next uncertainty reduction is a physical open-vs-covered
corridor comparison and a model with distributed lateral exchange.
