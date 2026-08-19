# Measurement Uncertainty Budget and Minimum Resolution Targets

Date: 2026-08-20  
Status: pre-bench design requirement

## Purpose

The numerical models now predict mechanism differences that can be much smaller than the eventual product-level +10 W target. A physical experiment can therefore fail by **insufficient measurement resolution** even when the specimen difference is real.

This document defines instrument-independent performance requirements. It does not select brands or claim that these targets are external standards.

## 1. Signed heat-flow measurement

Primary product metric:

\[
\Delta Q=P_{B4}-P_{B0}.
\]

E3c also uses an interim open-vs-covered target of approximately 3 W.

### Recommended measurement goal

For a 3 W mechanism difference, the expanded uncertainty of the paired heat-flow difference should preferably be no more than about 1 W and ideally closer to 0.5 W.

This is a project design target, not a formal statistical power calculation.

Near the environmental sign boundary, the apparatus must resolve both positive and negative heat flow. A heater-only controller is insufficient once environmental heat can enter the artificial skin.

## 2. Water balance

For each run:

\[
m_{feed}=m_{evap}+m_{runoff}+\Delta m_{sample}+m_{unaccounted}.
\]

Primary-quality target:

\[
|m_{unaccounted}|/m_{feed}\le0.05.
\]

At 150 g/h feed over a one-hour run, 5% corresponds to 7.5 g. The balance and runoff collection should have substantially finer resolution than this closure allowance; sub-gram mass resolution is preferred for component balances.

## 3. Temperature-corrected vapor-renewal metric

For E3c:

\[
\theta=
\frac{\rho_{v,valley}-\rho_{v,\infty}}
{\rho_{v,sat}(T_s)-\rho_{v,\infty}},
\qquad
F=1-\theta.
\]

`F` depends on four measured quantities:

- ambient dry-bulb temperature;
- ambient RH;
- local valley/near-field dry-bulb temperature;
- local valley/near-field RH;
- plus wet-surface temperature through the saturation state.

A local RH number without the corresponding dry-bulb temperature is insufficient.

## 4. Numerical sensor-uncertainty screen for `F`

A fixed-seed Monte Carlo screen was performed at a representative 35 °C / 70% RH ambient, 34 °C wet surface/local dry-bulb state.

The values below assume the listed quantities are **1-sigma independent uncertainties** for all temperature channels and all RH channels. This is a sensitivity screen, not a calibrated uncertainty budget for a real instrument system.

Representative true `F=0.8` results:

| sigma T | sigma RH | 5th percentile F | median | 95th percentile F |
|---:|---:|---:|---:|---:|
| 0.05 °C | 0.25 percentage point | 0.774 | 0.800 | 0.827 |
| 0.05 °C | 0.50 pp | 0.757 | 0.800 | 0.845 |
| 0.10 °C | 0.25 pp | 0.761 | 0.800 | 0.839 |
| 0.10 °C | 0.50 pp | 0.748 | 0.800 | 0.854 |
| 0.10 °C | 1.00 pp | 0.715 | 0.800 | 0.892 |
| 0.20 °C | 1.00 pp | 0.699 | 0.800 | 0.910 |

Interpretation:

- distinguishing `F=0.80` from `F=0.75` is difficult with ~0.2 °C / 1 pp-class uncertainty;
- around 0.1 °C / 0.5 pp gives materially tighter mechanism discrimination;
- exact high `R=F/(1-F)` should not be reported when its uncertainty becomes highly asymmetric.

## 5. Probe intrusion and spatial resolution

The relevant exterior structures are millimeter-scale. A sensor that is comparable to the valley width or rib height can alter the field being measured.

Record:

- sensing-element dimensions;
- support/stem dimensions;
- distance from wet surface;
- lateral position relative to rib/valley/island;
- orientation to expected flow;
- mounting repeatability.

Where direct RH probes are too intrusive, use smaller temperature probes plus validated optical/tracer methods or redesign the test geometry at larger scale while preserving the relevant dimensionless ratios.

## 6. Air-speed measurement

Primary still-air target is nominally <0.05 m/s.

Because current passive corridor screens produce predicted velocities far below ordinary anemometer ranges in some cases, classify local flow as:

- positive direction;
- negative direction;
- reversing/intermittent;
- below resolution.

Do not replace “below resolution” with zero.

Qualitative tracer imaging may be more informative than a noisy point velocity when the predicted speed is sub-mm/s.

## 7. Artificial-skin temperature

The environmental sign boundary is sensitive to skin/artificial-skin setpoint. In the current same-path analytic model at 70% RH:

| artificial-skin setpoint | zero-body-flux ambient temperature |
|---:|---:|
| 32 °C | ~37.54 °C |
| 33 °C | ~38.63 °C |
| 34 °C | ~39.73 °C |
| 35 °C | ~40.82 °C |
| 36 °C | ~41.91 °C |

Therefore artificial-skin temperature must be measured and logged continuously; it is not merely a nominal chamber setting.

## 8. Calibration and run metadata

Every published physical run should record at minimum:

- instrument make/model and serial/identifier where available;
- calibration date/source;
- resolution;
- stated accuracy/uncertainty;
- sampling rate;
- averaging/filtering procedure;
- probe positions;
- chamber setpoints and measured stability;
- specimen conditioning;
- water-feed calibration;
- active/wet area;
- experiment start/end timestamps;
- raw data file hashes.

## 9. Uncertainty propagation policy

For primary reported quantities:

- report run-to-run variation separately from instrument uncertainty;
- propagate temperature/RH uncertainty into vapor density and `F`;
- propagate mass/area uncertainty into evaporation flux and `k_eff`;
- propagate power/heat-flux uncertainties into paired `Delta Q`;
- state covariance assumptions rather than silently assuming independence;
- avoid numerical precision unsupported by the expanded uncertainty.

## 10. Go/no-go before physical PASS claims

Do not call an E1/E3c/E4/E6 physical result PASS-quality unless:

1. water-balance closure meets the declared target;
2. signed heat-flow uncertainty is materially smaller than the claimed difference;
3. T/RH uncertainty is sufficient to discriminate the claimed `F` difference;
4. sensor intrusion has been assessed;
5. the run is not silently supply-limited;
6. calibration and raw-data metadata are preserved.
