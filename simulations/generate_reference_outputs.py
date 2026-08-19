"""Generate reproducible reference tables and figures from repository models.

Usage:
    python simulations/generate_reference_outputs.py --output-root /tmp/reference-output

The generator writes:
- CSV tables for passive equilibrium branches, 2D heat-spreader orientation,
  and normalized water/salt screening;
- PNG figures derived directly from those tables;
- metadata.json including the git commit when available;
- sha256.txt covering generated artifacts.

All generated performance quantities are SIMULATION outputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Support both `python simulations/generate_reference_outputs.py` and
# `python -m simulations.generate_reference_outputs` from the repository root.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from simulations.heat_spreader_2d import orientation_demo
from simulations.passive_rib_screen import U_FLAT, stable_equilibria
from simulations.water_salt_1d import run_parameter_screen


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unknown"


def generate_passive_branch_table() -> pd.DataFrame:
    rows: list[dict[str, float | int | str]] = []
    for rh in (0.50, 0.70, 0.85):
        control_roots = stable_equilibria(35.0, rh, 150.0, 1.0, U_FLAT)
        if not control_roots:
            raise RuntimeError(f"no flat-control root at RH={rh}")
        # Conservative flat reference: warmest stable branch.
        control = max(control_roots, key=lambda r: r.surface_temp_C)

        for m_eff in np.linspace(1.0, 10.0, 91):
            roots = stable_equilibria(35.0, rh, 150.0, float(m_eff), 100.0)
            for root_index, root in enumerate(roots):
                rows.append(
                    {
                        "model": "passive_rib_screen",
                        "ambient_C": 35.0,
                        "RH_percent": rh * 100.0,
                        "water_g_h": 150.0,
                        "U_body_W_m2K": 100.0,
                        "M": float(m_eff),
                        "n_stable_roots": len(roots),
                        "root_index_cool_to_warm": root_index,
                        "surface_temp_C": root.surface_temp_C,
                        "body_cooling_W": root.body_cooling_W,
                        "gain_vs_flat_W": root.body_cooling_W - control.body_cooling_W,
                        "evaporation_g_h": root.evaporation_g_h,
                    }
                )
    return pd.DataFrame(rows)


def generate_heat_spreader_table() -> pd.DataFrame:
    rows = []
    for name, result in orientation_demo().items():
        rows.append(
            {
                "model": "heat_spreader_2d",
                "case": name,
                "body_cooling_W": result.body_cooling_W,
                "temperature_std_C": result.temperature_std_C,
                "temperature_min_C": result.temperature_min_C,
                "temperature_max_C": result.temperature_max_C,
            }
        )
    return pd.DataFrame(rows)


def plot_passive_branches(df: pd.DataFrame, out_path: Path) -> None:
    plt.figure(figsize=(7.4, 5.0))
    for rh in sorted(df["RH_percent"].unique()):
        group = df[df["RH_percent"] == rh]
        plt.scatter(
            group["M"],
            group["gain_vs_flat_W"],
            s=10,
            label=f"RH {rh:.0f}%",
        )
    plt.axhline(10.0, linestyle="--", linewidth=1.0, label="+10 W physical-test target")
    plt.xlabel("Effective exterior exchange multiplier M (-)")
    plt.ylabel("Modeled body-cooling gain vs flat control (W)")
    plt.title("SIMULATION: all detected stable equilibrium branches")
    plt.grid(alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    plt.close()


def plot_heat_spreader(df: pd.DataFrame, out_path: Path) -> None:
    plt.figure(figsize=(6.8, 4.6))
    plt.bar(df["case"], df["body_cooling_W"])
    plt.ylabel("Modeled body-side heat routed to sink (W)")
    plt.title("SIMULATION: anisotropic heat-spreader orientation")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    plt.close()


def plot_salt_threshold(out_path: Path) -> None:
    c0 = np.linspace(0.01, 1.0, 200)
    threshold = 1.0 - c0
    plt.figure(figsize=(6.8, 4.6))
    plt.plot(c0, threshold)
    plt.xlabel("Normalized inlet concentration C_in / C_sat (-)")
    plt.ylabel("Internal water-loss fraction at saturation onset (-)")
    plt.title("SIMULATION / NORMALIZED MASS BALANCE: leak threshold = 1 - C/Csat")
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    plt.close()


def write_sha256(root: Path) -> None:
    lines = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name == "sha256.txt":
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(root).as_posix()}")
    (root / "sha256.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=Path("generated-reference"))
    args = parser.parse_args()

    root = args.output_root
    data_dir = root / "data"
    fig_dir = root / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    passive = generate_passive_branch_table()
    spreader = generate_heat_spreader_table()
    salt = run_parameter_screen()

    passive.to_csv(data_dir / "passive_equilibrium_branches.csv", index=False)
    spreader.to_csv(data_dir / "heat_spreader_orientation.csv", index=False)
    salt.to_csv(data_dir / "water_salt_parameter_screen.csv", index=False)

    plot_passive_branches(passive, fig_dir / "passive_equilibrium_branches.png")
    plot_heat_spreader(spreader, fig_dir / "heat_spreader_orientation.png")
    plot_salt_threshold(fig_dir / "water_salt_saturation_threshold.png")

    metadata = {
        "classification": "SIMULATION",
        "git_commit": git_commit(),
        "generator": "simulations/generate_reference_outputs.py",
        "primary_environment": {
            "ambient_C": 35.0,
            "water_g_h": 150.0,
            "RH_percent": [50.0, 70.0, 85.0],
        },
        "warning": (
            "The passive model may contain multiple stable roots. Tables include all detected stable roots; "
            "figures must not be interpreted as measured garment performance."
        ),
    }
    (root / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    write_sha256(root)

    print(f"Generated reference outputs under {root}")
    print(f"git_commit={metadata['git_commit']}")


if __name__ == "__main__":
    main()
