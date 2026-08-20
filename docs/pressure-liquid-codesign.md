# Pressure-aware terminal / liquid-route co-design

Status: virtual/computational screening only. No physical garment or bench specimen exists and no measured cooling claim is made.

## Correction status

This document originally promoted a mildly regularized terminal layout as the current VP-E anchor because it reduced the relative route proxy

\[
J_h=d_{95}\hat r^{-4}
\]

by ~16.8% while retaining ~98.2% of the thermal optimum.

A later explicit branched liquid-resistor network shows that this interpretation was too strong for the current short 50–200 µm-class distributed-trunk architecture. At tile-scaled flow, predicted pressure losses are orders of magnitude below available collector capillary drive. The regularized layout therefore remains a geometric/manufacturing Pareto alternative, but it is **not preferred over the pure thermal pressure-aware layout solely on hydraulic-pressure grounds**.

See `docs/branched-liquid-resistor-network.md` for the correcting model.

## Purpose of the original proxy

The pressure-aware thermal screen favors moving wet evaporator terminals away from compressed regions because compression closes ambient vapor-renewal paths. That can lengthen geometric liquid collection routes.

The proxy screen asked whether a small thermal sacrifice could shorten those routes before a full fluid-network model existed.

## Relative hydraulic proxy

For a laminar circular-equivalent channel, Poiseuille scaling gives

\[
\Delta p_f \propto \frac{L\dot V}{r^4}.
\]

The proxy was therefore

\[
J_h = d_{95}\,\hat r^{-4},
\]

where `d95` is the 95th-percentile geometric distance to the nearest wet terminal and `r_hat` is a retained equivalent-radius ratio. The reference used `r_hat=0.90`.

## Variable table

| Symbol | Meaning | SI unit | Definition / assumption | Type |
|---|---|---:|---|---|
| `d95` | 95th-percentile source-to-terminal distance | m | geometric terminal-distance statistic | model output |
| `r_hat` | retained channel radius ratio | 1 | compressed radius / nominal radius | design assumption |
| `J_h` | relative route burden proxy | m-equivalent | `d95 r_hat^-4` | derived metric |
| `q_b` | body-side heat flux | W/m² | pressure-aware thermal-model output | model output |
| `beta` | four-island regularization weight | 1 | terminal-placement score weight | design variable |
| `w_r` | heat-route overlap weight | 1 | terminal-placement score weight | design variable |

Dimensional check:

\[
[J_h]=[d_{95}][\hat r]^{-4}=\mathrm m.
\]

`J_h` is not a pressure drop because it omits flow splitting, absolute channel conductance and network connectivity.

## 24 x 24 proxy result

Pure thermal optimum:

- `beta=0`;
- route weight `0.20`;
- body-side heat flux `112.84 W/m²`;
- liquid `d95=20.16 mm`;
- proxy `30.72 mm-equivalent`.

Mildly regularized candidate:

- `beta=0.125`;
- route weight `0.35`;
- body-side heat flux `110.83 W/m²`;
- thermal retention `98.21%`;
- liquid `d95=16.77 mm`;
- proxy `25.56 mm-equivalent`;
- relative proxy reduction `16.79%`.

This remains a valid **geometric Pareto result**.

## Explicit-network correction

The later 24 x 24 branched-flow model uses:

- 60 mm tile;
- tile-scaled flow equivalent to 150 g/h over 0.30 m²;
- 200 µm nominal liquid trunks;
- 50 µm collector radius;
- 15 mm lift;
- pressure-linked radius retention down to 0.70.

Under the strongest screened collapse map, maximum predicted liquid-network pressure drops are only approximately:

- pure thermal pressure-aware layout: `0.526 Pa`;
- regularized layout: `0.470 Pa`;
- four-island layout: `0.205 Pa`.

Available collector capillary drive is about `2278 Pa`. The one-network safety-factor-3 radius boundary is only ~26–32 µm depending on terminal layout.

Therefore, for the current 50–200 µm-class short distributed trunks, route-length differences are **not first-order capillary-head constraints** in the dense-network embodiment.

## Current design interpretation

The terminal decision is now:

- use the pure thermal pressure-aware layout as the current thermal reference when local trunks are hydraulically generous;
- retain the regularized layout as a candidate when sparse routing, seam placement, material volume, source localization or manufacturing makes route length expensive;
- do not freeze either as a final garment-wide layout until network sparsity and regional garment geometry are included.

## H / T / D / C / U

### H

A pressure-aware layout can be regularized to shorten geometric source-to-terminal routes with little thermal loss.

### T

Equal wet area, equal heat-route fraction, converged pressure/thermal model, common geometric route metric.

### D

The geometric claim passes: the regularized candidate retains >98% of thermal output and shortens `d95` by >10%.

The stronger hydraulic-pressure claim is **not supported** for the current dense 50–200 µm distributed-trunk network because absolute pressure losses are negligible relative to capillary drive.

### C

The regularized layout could become hydraulically relevant if:

- effective radius is much smaller;
- network edges are sparse;
- flow sources are strongly localized;
- lift is larger;
- trunks collapse or block completely;
- junction losses dominate.

### U

Dominant uncertainty is network topology/material density and effective hydraulic radius. The proxy itself has low numerical uncertainty but high model-form uncertainty.

## Salt conservation

Salt moves only with liquid and does not evaporate:

\[
J_{salt,vapor}=0.
\]

## Reproducibility

Relative proxy:

- `simulations/pressure_liquid_codesign.py`
- `tests/test_pressure_liquid_codesign.py`
- `data/pressure_liquid_codesign_reference.csv`

Correcting absolute-flow network:

- `simulations/branched_liquid_resistor_network.py`
- `tests/test_branched_liquid_resistor_network.py`
- `data/branched_liquid_resistor_reference.csv`
