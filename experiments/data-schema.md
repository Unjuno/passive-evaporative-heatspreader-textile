# Physical Experiment Raw-Data Schema

Date: 2026-08-20

## Purpose

Define a common, machine-readable record for E1/E2/E3/E3c/E4/E6 physical runs before any physical performance result is collected.

The schema is intentionally broader than any one experiment so negative or inconvenient measurements are not silently omitted.

## 1. Run identity

Every run must have:

- `run_id` — unique immutable identifier;
- `experiment_id` — e.g. `E1`, `E3c`, `E4`, `E6`;
- `sample_id` — e.g. `B0`, `B4-open`, `D1`, `O1`;
- `specimen_id` — physical specimen identifier;
- `start_time_utc`;
- `end_time_utc`;
- `operator` or acquisition-system identifier;
- git commit/tag defining the protocol/model state used to plan the run.

## 2. Configuration metadata

Record once per run or in a linked metadata file:

- artificial-skin setpoint °C;
- projected active area m²;
- measured wet projected area m²;
- sample mass dry/wet as applicable;
- microstructure height/pitch;
- valley/gap width/depth/segment length;
- open fraction;
- orientation relative to gravity;
- heat-spreader topology/orientation;
- commanded water feed g/h;
- fluid composition;
- preconditioning procedure;
- chamber target T/RH;
- intended far-field air-speed condition;
- compression/contact condition.

## 3. Time-series columns

Recommended CSV columns:

```text
timestamp_s,
run_id,
sample_id,
plate_temp_C,
plate_heat_flux_W_m2,
plate_electrical_power_W,
ambient_temp_C,
ambient_RH_percent,
far_field_air_speed_m_s,
wet_surface_temp_C,
local_temp_C,
local_RH_percent,
local_probe_z_mm,
local_probe_x_mm,
local_air_speed_m_s,
local_flow_direction,
water_feed_rate_g_h,
feed_reservoir_mass_g,
runoff_mass_g,
sample_mass_g,
notes_flag
```

Not every experiment requires every instantaneous channel. Missing values should be blank/NA, not zero unless zero was actually measured.

## 4. Sign conventions

### Heat

Recommended:

- `plate_heat_flux_W_m2 > 0`: heat leaves artificial skin and enters garment/environment;
- `< 0`: heat enters artificial skin from garment/environment.

Electrical heater/cooler power must use a separately documented sign convention and must not be substituted for calibrated heat flux without the apparatus energy balance.

### Air flow

Store both magnitude and a declared direction label, for example:

- `up`;
- `down`;
- `inlet_to_outlet`;
- `outlet_to_inlet`;
- `reversing`;
- `below_resolution`.

Never encode `below_resolution` as numeric zero.

## 5. Water-balance summary

For each run publish a summary row containing:

- total feed mass;
- sample mass change;
- collected runoff/drip mass;
- inferred evaporated mass;
- unaccounted mass;
- closure fraction;
- supply-limited flag;
- visible dryout flag;
- condensation flag.

Primary-quality closure target is >=95%.

## 6. Derived vapor quantities

Derived data should be stored separately from raw measurements.

For E3c, calculate:

\[
\theta=
\frac{\rho_{v,local}-\rho_{v,ambient}}
{\rho_{v,sat}(T_s)-\rho_{v,ambient}},
\qquad F=1-\theta.
\]

Where valid:

\[
k_{eff,exp}=\frac{\dot m''_{evap}}
{\rho_{v,sat}(T_s)-\rho_{v,ambient}}.
\]

Store the calculation version/git commit and propagated uncertainty with derived outputs.

## 7. Calibration metadata

Each sensor/channel should have a machine-readable record containing:

```text
channel_name,
instrument_type,
manufacturer,
model,
serial_or_identifier,
calibration_date,
calibration_source,
resolution,
standard_uncertainty,
units,
sampling_rate_Hz,
filtering,
position_description
```

If manufacturer/serial information is unavailable, record that fact rather than omitting the field silently.

## 8. File layout for a physical run

Recommended:

```text
experiments/runs/<run_id>/
  metadata.yaml
  calibration.csv
  raw_timeseries.csv
  water_balance.csv
  derived.csv
  photos/
  thermal_images/
  notes.md
  sha256.txt
```

Raw files should not be overwritten after publication. Corrected processing should produce a new derived file/version while preserving original measurements.

## 9. Exclusion / failure policy

A run may be excluded from a primary aggregate only for a predeclared reason, such as:

- apparatus fault;
- chamber excursion outside acceptance band;
- feed interruption;
- sensor failure;
- water-balance failure;
- specimen mechanical failure.

The raw run should remain published and its exclusion reason should be machine-readable.

Do not discard a run merely because its result is unfavorable to the concept.

## 10. Minimum release package for first physical evidence

The first physical-data release should contain:

1. protocol version;
2. sample construction description;
3. raw time series;
4. calibration metadata;
5. water balance;
6. analysis script;
7. uncertainty calculation;
8. negative/failed runs;
9. generated figures/tables;
10. SHA-256 manifest and git commit.
