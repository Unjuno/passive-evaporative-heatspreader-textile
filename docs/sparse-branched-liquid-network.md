# Sparse branched liquid network: trunk pitch vs collector radius

Status: virtual/computational screening only. No physical textile network or specimen exists.

## Motivation

The fully connected 200 µm-trunk grid has enormous capillary pressure margin. That network is intentionally over-connected, so its useful implication is not that hydraulic design is solved; it is that the next variable is **how much of the grid can be replaced by finer collector paths before pressure loss becomes binding**.

This screen embeds a periodic 200 µm-class high-conductance trunk lattice inside a continuous finer collector mesh. A localized sweat-source field is used and the trunk lattice is shifted through several offsets so that a favorable line placement is not mistaken for a general result.

## Edge conductance

Every edge uses

\[
G_e=\frac{\pi r_e^4}{8\mu L_e},
\qquad
Q_e=G_e\Delta p_e.
\]

Edges on the trunk lattice use nominal radius `r_t=200 µm`; all other edges use the selected collector radius `r_c`.

Pressure-linked collapse applies to both scales:

\[
r_e=r_{e,0}\max(r_{min},1-s_c c_e).
\]

The current reference uses `r_min=0.70` and `s_c=1`.

## Variable table

| Symbol | Meaning | SI unit | Reference | Type |
|---|---|---:|---:|---|
| `r_t` | large trunk radius | m | 200 µm | design input |
| `r_c` | collector hydraulic radius | m | 20–50 µm | sweep input |
| `P_t` | trunk lattice pitch | m | 10–60 mm | sweep input |
| `mu` | liquid viscosity | Pa·s | 0.9 mPa·s | screening input |
| `Delta p_drive` | collector capillary drive minus lift | Pa | depends on `r_c`, 15 mm lift | derived |
| `M` | capillary pressure margin | 1 | `Delta p_drive / Delta p_max` | output |

Unit check:

\[
[G_e]=\mathrm{m^3/(s\,Pa)},\quad
[G_e\Delta p]=\mathrm{m^3/s}.
\]

## Source and pressure challenge

- 60 mm square tile, 24 x 24 network;
- total tile flow 1.8 g/h, scaled from 150 g/h over 0.30 m²;
- localized center source plus a nonzero distributed background;
- synthetic backpack+strap pressure field;
- pure thermal pressure-aware terminal mask;
- five sampled trunk-grid phase offsets per pitch;
- decision requirement: **every sampled offset has margin >=3**.

## Offset-robust results

Largest tested trunk pitch for which all sampled offsets pass safety factor 3:

| collector radius | largest robust tested trunk pitch |
|---:|---:|
| 20 µm | 15 mm |
| 25 µm | 20 mm |
| 30 µm | 30 mm |
| 35 µm | 60 mm |
| 40 µm | 60 mm |
| 50 µm | 60 mm |

Worst sampled margin values show the transition directly:

| trunk pitch | 20 µm collector | 25 µm | 30 µm | 35 µm | 40 µm | 50 µm |
|---:|---:|---:|---:|---:|---:|---:|
| 10 mm | 10.61 | 20.42 | 34.56 | 53.27 | 76.31 | 131.60 |
| 15 mm | 4.78 | 9.24 | 15.72 | 24.44 | 35.45 | 63.58 |
| 20 mm | **2.80** | 5.42 | 9.24 | 14.39 | 20.96 | 38.11 |
| 30 mm | 1.41 | **2.74** | 4.69 | 7.38 | 10.87 | 20.54 |
| 60 mm | 0.75 | 1.46 | **2.51** | 3.95 | 5.86 | 11.29 |

Bold values are below the safety-factor-3 decision boundary.

## Interpretation

The explicit network now gives a more useful hierarchy:

1. **Dense 50–200 µm trunks:** pressure loss is negligible relative to capillary drive.
2. **Sparse 200 µm trunks + 35–50 µm collector mesh:** still generous in the tested 60 mm tile.
3. **Sparse trunks + 20–30 µm collector mesh:** trunk pitch becomes a binding design variable.

Therefore the earlier statement that source-to-terminal geometric distance alone should determine the terminal layout is too broad. What matters is the joint combination of:

- collector hydraulic radius;
- large-trunk pitch;
- trunk-grid phase relative to source and terminal locations;
- source localization;
- compression-induced radius loss.

## H / T / D / C / U

### H

For a two-scale liquid network, there is a collector-radius-dependent maximum trunk pitch beyond which some plausible lattice phases violate a capillary safety factor of 3.

### T

Five deterministic lattice offsets are tested at each radius/pitch pair under the same localized source and pressure map.

### D

PASS for a radius/pitch pair only if **all sampled offsets** have `Delta p_drive / Delta p_max >= 3`.

### C

The non-monotonic pressure values seen at a single fixed grid phase are a topology-alignment artifact; this is why the design boundary is based on the worst sampled phase rather than one placement.

### U

Major uncertainties:

- circular-equivalent hydraulic radius;
- number and selection of phase offsets;
- actual sweat-source localization;
- junction and porous-medium losses;
- complete channel closure under compression;
- real network wall/material mass.

The values are design-screen boundaries, not measured textile permeability limits.

## Salt conservation

Salt remains in the liquid/solid phases. Salt vapor flux is zero:

\[
J_{salt,vapor}=0.
\]

No internal evaporation is introduced by this network model.

## Reproducibility

- `simulations/sparse_branched_liquid_network.py`
- `tests/test_sparse_branched_liquid_network.py`
- `data/sparse_branched_liquid_reference.csv`
