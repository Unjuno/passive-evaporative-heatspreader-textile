"""Generate reproducible reference tables and figures from repository models.

All generated performance quantities are SIMULATION or analytic screening
outputs unless explicitly labeled otherwise.
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

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from simulations.corridor_buoyancy_screen import (
    neutral_curve as corridor_neutral_curve,
    run_screen as run_corridor_screen,
)
from simulations.heat_spreader_2d import orientation_demo
from simulations.open_valley_distributed_1d import run_screen as run_open_valley_distributed_screen
from simulations.open_valley_exchange_target import target_table as open_valley_target_table
from simulations.open_valley_thermal_1d import run_screen as run_open_valley_thermal_screen
from simulations.passive_rib_screen import U_FLAT, stable_equilibria
from simulations.rib_diffusion_screen import run_screen as run_diffusion_screen
from simulations.self_consistent_corridor_1d import run_screen as run_self_consistent_corridor_screen
from simulations.split_heat_mass_screen import run_split_screen
from simulations.split_transfer_sensitivity import run_sensitivity, summarize
from simulations.supply_limit_audit import run_screen as run_supply_limit_audit
from simulations.water_salt_1d import run_parameter_screen


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "unknown"


def generate_passive_branch_table() -> pd.DataFrame:
    rows = []
    for rh in (0.50, 0.70, 0.85):
        control_roots = stable_equilibria(35.0, rh, 150.0, 1.0, U_FLAT)
        if not control_roots:
            raise RuntimeError(f"no flat-control root at RH={rh}")
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
    return pd.DataFrame(
        [
            {
                "model": "heat_spreader_2d",
                "case": name,
                "body_cooling_W": result.body_cooling_W,
                "temperature_std_C": result.temperature_std_C,
                "temperature_min_C": result.temperature_min_C,
                "temperature_max_C": result.temperature_max_C,
            }
            for name, result in orientation_demo().items()
        ]
    )


def plot_passive_branches(df: pd.DataFrame, out_path: Path) -> None:
    plt.figure(figsize=(7.4, 5.0))
    for rh in sorted(df["RH_percent"].unique()):
        group = df[df["RH_percent"] == rh]
        plt.scatter(group["M"], group["gain_vs_flat_W"], s=10, label=f"RH {rh:.0f}%")
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
    plt.figure(figsize=(6.8, 4.6))
    plt.plot(c0, 1.0 - c0)
    plt.xlabel("Normalized inlet concentration C_in / C_sat (-)")
    plt.ylabel("Internal water-loss fraction at saturation onset (-)")
    plt.title("SIMULATION / NORMALIZED MASS BALANCE: leak threshold = 1 - C/Csat")
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    plt.close()


def plot_rib_diffusion(df: pd.DataFrame, out_path: Path) -> None:
    plt.figure(figsize=(7.2, 4.8))
    for pitch in sorted(df["pitch_mm"].unique()):
        group = df[df["pitch_mm"] == pitch]
        plt.plot(
            group["renewal_gap_above_tip_mm"],
            group["whole_garment_mass_transfer_multiplier"],
            marker="o",
            label=f"pitch {pitch:.1f} mm",
        )
    plt.axhline(3.5, linestyle="--", linewidth=1.0, label="legacy screening reference M=3.5")
    plt.xscale("log")
    plt.xlabel("Idealized bulk-air renewal gap above rib tips (mm)")
    plt.ylabel("Whole-garment mass-transfer multiplier M_m (-)")
    plt.title("SIMULATION: periodic 2-D rib diffusion / boundary-layer sharing")
    plt.grid(alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    plt.close()


def write_sha256(root: Path) -> None:
    lines = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name == "sha256.txt":
            continue
        lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(root).as_posix()}")
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
    split = run_split_screen()
    sensitivity = run_sensitivity()
    sensitivity_summary = summarize(sensitivity)
    corridor = run_corridor_screen()
    corridor_neutral = corridor_neutral_curve()
    corridor_self_consistent = run_self_consistent_corridor_screen()
    open_valley_targets = open_valley_target_table()
    open_valley_distributed = run_open_valley_distributed_screen()
    open_valley_thermal = run_open_valley_thermal_screen()
    supply_limit = run_supply_limit_audit()
    spreader = generate_heat_spreader_table()
    salt = run_parameter_screen()
    diffusion = run_diffusion_screen()

    outputs = {
        "passive_equilibrium_branches.csv": passive,
        "split_heat_mass_screen.csv": split,
        "split_transfer_sensitivity.csv": sensitivity,
        "split_transfer_sensitivity_summary.csv": sensitivity_summary,
        "corridor_buoyancy_screen.csv": corridor,
        "corridor_neutral_density_curve.csv": corridor_neutral,
        "self_consistent_corridor_1d.csv": corridor_self_consistent,
        "open_valley_renewal_targets.csv": open_valley_targets,
        "open_valley_distributed_1d.csv": open_valley_distributed,
        "open_valley_thermal_1d.csv": open_valley_thermal,
        "supply_limit_audit.csv": supply_limit,
        "heat_spreader_orientation.csv": spreader,
        "water_salt_parameter_screen.csv": salt,
        "rib_diffusion_boundary_layer.csv": diffusion,
    }
    for name, table in outputs.items():
        table.to_csv(data_dir / name, index=False)

    plot_passive_branches(passive, fig_dir / "passive_equilibrium_branches.png")
    plot_heat_spreader(spreader, fig_dir / "heat_spreader_orientation.png")
    plot_salt_threshold(fig_dir / "water_salt_saturation_threshold.png")
    plot_rib_diffusion(diffusion, fig_dir / "rib_diffusion_boundary_layer.png")

    metadata = {
        "classification": "SIMULATION/ANALYTIC_SCREENING",
        "git_commit": git_commit(),
        "generator": "simulations/generate_reference_outputs.py",
        "warnings": [
            "Physical garment performance has not been measured.",
            "The passive lumped model may contain multiple stable roots.",
            "Heat and vapor transfer are not assumed to share one multiplier.",
            "Open-valley lateral exchange is parameterized through effective exchange distances, not CFD-resolved geometry.",
            "The coupled open-valley thermal solver is a fully-wet transfer-capacity model; supply_limit_audit.csv marks cases whose capacity exceeds available feed.",
            "Supply-limited cases do not have a solved dryout/wet-fraction temperature field; capacity-model body heat flux must not be reused as a feed-limited prediction.",
            "Salt vapor flux is zero in the garment-temperature models.",
        ],
    }
    (root / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    write_sha256(root)

    print(f"Generated reference outputs under {root}")
    print(f"git_commit={metadata['git_commit']}")


if __name__ == "__main__":
    main()
