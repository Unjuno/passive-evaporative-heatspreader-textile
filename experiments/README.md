# Experiments

Physical validation data will be stored here by experiment ID.

**Current status:** no physical garment-performance experiment has yet been executed. Files in this directory are planned protocols unless explicitly labeled as measured results.

Recommended structure:

```text
experiments/
  E1_direct_comparison/
  E2_ablation/
  E3_rib_accessibility/
  E3b_hierarchical_air_renewal/
  E4_humidity_limit/
  E5_spreader_orientation/
  E6_hot_ambient_shielding/
  E7_durability/
```

Current standalone protocol:

- `e3b_hierarchical_air_renewal.md` — micro-rib-only versus hierarchical microstructure + macro air-renewal paths.

Each experiment directory should contain:

- `protocol.md` — exact procedure and deviations from the master plan;
- `metadata.yaml` — sample IDs, instruments, calibration dates, chamber conditions;
- `raw/` — immutable raw measurements;
- `processed/` — derived tables;
- `analysis.py` — reproducible analysis;
- `results.md` — result summary including negative/null results;
- `sha256.txt` — hashes for frozen releases when appropriate.

## Current experiment sequence

1. **E1 — direct comparison:** flat fast-dry control versus integrated architecture at equal water input.
2. **E2 — ablation:** separate exterior-structure and heat-spreader contributions.
3. **E3 — rib pitch/accessibility:** determine whether denser exterior geometry creates useful exchange or only geometric area.
4. **E3b — hierarchical air renewal:** test microstructure plus macro corridors/valleys/spacer channels against a micro-rib-only control.
5. **E4 — humidity boundary:** repeat best architecture at lower/higher RH.
6. **E5 — heat-spreader orientation:** test anisotropic heat routing.
7. **E6 — hot-ambient shielding:** quantify dry conductive heat pickup.
8. **E7 — durability:** bending, stretch, compression, washing and wet/dry cycling.

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

For E3/E3b additionally record:

- rib height, pitch and width under wet operating conditions;
- macro-corridor width/spacing/open fraction where applicable;
- structure orientation relative to gravity;
- RH/T probe height above rib tips and corridors;
- wetting fraction and any visible collapse/bundling.

Do not silently delete failed runs. Flag exclusion criteria and preserve the original data.
