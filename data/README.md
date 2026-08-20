# Data Conventions

This directory is for versioned simulation outputs and processed experimental tables that are useful across experiments.

## Principles

- Preserve SI units in column names or metadata.
- Keep raw physical measurements under `experiments/<ID>/raw/`; do not rewrite them here.
- Store assumptions with generated simulation data.
- Distinguish simulated, inferred, and measured values explicitly.
- Use UTF-8 CSV for tabular exchange unless another format is justified.
- Record code commit SHA and parameter-set version for generated outputs.

## Naming

Recommended pattern:

`<model>_<environment>_<parameter-set>_<version>.csv`

Example:

`passive-rib_35C_70RH_150gph_v1.csv`

## Required provenance fields for model output

Where practical include:

- `model_version`;
- `git_commit`;
- `ambient_C`;
- `RH_percent`;
- `water_g_h`;
- geometry variables;
- thermal-coupling assumptions;
- whether the value is an input, direct model output, or derived metric.
