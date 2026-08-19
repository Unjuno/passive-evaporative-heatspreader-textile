# Experiments

Physical validation data will be stored here by experiment ID.

Recommended structure:

```text
experiments/
  E1_direct_comparison/
  E2_ablation/
  E3_rib_accessibility/
  E4_humidity_limit/
  E5_spreader_orientation/
  E6_hot_ambient_shielding/
  E7_durability/
```

Each experiment directory should contain:

- `protocol.md` — exact procedure and deviations from the master plan;
- `metadata.yaml` — sample IDs, instruments, calibration dates, chamber conditions;
- `raw/` — immutable raw measurements;
- `processed/` — derived tables;
- `analysis.py` — reproducible analysis;
- `results.md` — result summary including negative/null results;
- `sha256.txt` — hashes for frozen releases when appropriate.

## Minimum metadata per run

- run ID and timestamp;
- operator;
- sample ID/version;
- active projected area;
- artificial-skin temperature setpoint;
- ambient temperature/RH;
- air speed and sensor location;
- liquid composition and feed command;
- measured feed mass;
- heater-power acquisition method;
- balance/thermometer/humidity-sensor calibration information;
- known anomalies.

Do not silently delete failed runs. Flag exclusion criteria and preserve the original data.
