# Open-Valley Lateral Renewal Target

Date: 2026-08-19  
Classification: **ANALYTIC SCREEN / IDENTIFICATION METHOD — NOT GARMENT PERFORMANCE DATA**

## 1. Purpose

The covered/end-renewed 1-D corridor model showed why nonzero axial flow is not enough: local air may still approach saturation.

For a laterally open valley, the next question is therefore not simply “how fast does air move?” but:

> how strong must ambient renewal be relative to vapor supply from the wet surface to preserve a useful vapor-density difference?

This document gives a minimal local conductance balance that can also be inverted from physical T/RH measurements.

## 2. Local conductance balance

Define wet-surface vapor conductance

\[
G_w=k_wP_w
\]

and ambient-renewal conductance

\[
G_a=k_aP_a.
\]

Define

\[
R=\frac{G_a}{G_w}.
\]

For a local steady balance,

\[
G_w(C_{sat}-C)=G_a(C-C_\infty).
\]

The retained fraction of the maximum wet-wall vapor driving force is

\[
F=\frac{C_{sat}-C}{C_{sat}-C_\infty}
=\frac{R}{1+R}.
\]

The normalized valley vapor loading is

\[
\theta=\frac{C-C_\infty}{C_{sat}-C_\infty}
=\frac{1}{1+R}.
\]

Therefore

\[
R=\frac{F}{1-F}=\frac{1-\theta}{\theta}.
\]

## 3. Variable table

| Symbol | Meaning | SI unit | Definition / domain |
|---|---|---:|---|
| `G_w` | wet-surface-to-valley vapor conductance | m²/s per unit axial-length formulation or equivalent lumped conductance | `k_w P_w`, positive |
| `G_a` | valley-to-ambient renewal conductance | same as `G_w` | `k_a P_a`, nonnegative |
| `R` | renewal/wet conductance ratio | 1 | `G_a/G_w` |
| `C_sat` | saturated vapor density at wet-surface temperature | kg/m³ | water saturation state |
| `C_inf` | ambient vapor density | kg/m³ | ambient T/RH |
| `C` | local valley vapor density | kg/m³ | measured or modeled |
| `F` | retained vapor driving-force fraction | 1 | `(C_sat-C)/(C_sat-C_inf)` |
| `theta` | normalized valley vapor loading | 1 | `(C-C_inf)/(C_sat-C_inf)` |

## 4. Dimensional check

Because

\[
R=G_a/G_w,
\]

both conductances have identical units and `R` is dimensionless.

Likewise `F` and `theta` are ratios of vapor-density differences and are dimensionless.

## 5. Required renewal ratios

| Target retained driving force `F` | Required `R` | Valley loading `theta` |
|---:|---:|---:|
| 50% | 1.0 | 0.50 |
| 67% | 2.03 | 0.33 |
| 80% | 4.0 | 0.20 |
| 90% | 9.0 | 0.10 |
| 95% | 19.0 | 0.05 |

Interpretation:

- `R=1` is only enough to preserve half of the full ambient-to-wet-wall vapor-density difference.
- preserving 80% requires ambient renewal conductance about four times the wet-surface vapor conductance in this local balance;
- preserving 90% requires about nine times.

These are conductance-ratio requirements, **not predicted geometric dimensions**. The repository does not currently know `k_a` for a real open garment valley.

## 6. Measurement identification

Using local temperature and RH measurements, convert each state to water-vapor density.

Then

\[
\theta=
\frac{\rho_{v,valley}-\rho_{v,\infty}}
{\rho_{v,sat}(T_s)-\rho_{v,\infty}}.
\]

If `0 < theta < 1`, infer

\[
R=\frac{1-\theta}{\theta}.
\]

This is implemented in `simulations/open_valley_exchange_target.py`.

If the measured state lies outside the assumed local balance interval, the code returns an explicit status instead of clipping the value. Such a result can indicate probe disturbance, condensation, nonlocal transport, temperature mismatch, transient behavior, or model inadequacy.

## 7. Experimental use in E3c

For D1/O1/O2/O3, report at every usable sampling position:

- local T and RH;
- wet-surface T;
- ambient T and RH;
- inferred `theta`;
- inferred `F`;
- inferred `R` where the local balance is admissible.

Suggested mechanism-support targets:

- **minimum useful-renewal screen:** `F >= 0.5` (`R >= 1`);
- **stronger renewal screen:** `F >= 0.8` (`R >= 4`).

These are project mechanism thresholds only. Physical cooling PASS remains based on heater-power and water-balance criteria in E3c.

## 8. H / T / D / C / U

**H:** laterally open or segmented geometries can produce larger inferred `R` and `F` than a covered/end-renewed corridor under equal water input.

**T:** infer `R` from spatial T/RH/surface-T data in E3c while also measuring heater power and water balance.

**D:** mechanism support if open designs repeatedly increase `F`/`R` relative to D1; product-value PASS still requires heater-power improvement.

**C:** the local two-conductance model may be too simple when axial flow, transient plumes, condensation, probe heating, or strong temperature gradients dominate.

**U:** dominant uncertainty arises from near-surface RH/T probe placement and wet-surface temperature. Propagate those measurement uncertainties into `theta`, `F`, and `R`; do not report `R` when the denominator or `theta` is near zero.
