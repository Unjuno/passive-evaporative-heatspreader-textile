"""Equal-material 2-D heat-spreader topology/orientation screen.

This model extends ``distributed_spreader_1d.py`` to a periodic 2-D sheet so
explicit high-conductivity routing topology can be compared at the **same high-k
material fraction**.

The main comparison uses four fields over a 15 mm x 15 mm periodic cell:

- ``uniform_homogenized`` — 50% high-k material homogenized locally;
- ``x_aligned_traces`` — 50% high-k stripes running along the wet/dry routing
  direction x;
- ``y_aligned_traces`` — 50% high-k stripes perpendicular to the routing
  direction;
- ``connected_mesh`` — orthogonal stripe families whose exact union coverage is
  50%.

Fractional cell coverage is integrated analytically so the total high-k material
fraction is exactly 0.5 independent of grid resolution. Cell sheet conductance is
then linearly mixed between a high-k trace and background textile value. Face
conductance uses the harmonic mean.

This is still a screening model, not a resolved textile microstructure or CFD.
It is designed to answer a narrower question: can the earlier idealized
``coverage cancels from mass`` result change when topology/orientation changes
the effective routing factor?  The answer in the current screen is yes: material
aligned with the dominant dry-to-wet heat-flow direction is more useful than the
same amount placed perpendicular to it.

No physical specimen exists and no output is a measured garment claim.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import factorized

try:
    from simulations.distributed_spreader_1d import (
        H_WET,
        KM_WET,
        L_V,
        STRUCTURED_AREA_M2,
        T_SKIN,
        U_BODY,
        saturated_vapor_density,
        saturated_vapor_density_derivative,
    )
except ModuleNotFoundError:
    from distributed_spreader_1d import (
        H_WET,
        KM_WET,
        L_V,
        STRUCTURED_AREA_M2,
        T_SKIN,
        U_BODY,
        saturated_vapor_density,
        saturated_vapor_density_derivative,
    )

DEFAULT_DOMAIN_MM = 15.0
DEFAULT_TRACE_PERIOD_MM = 3.0
DEFAULT_HIGH_K_W_MK = 300.0
DEFAULT_HIGH_K_THICKNESS_UM = 100.0
DEFAULT_BACKGROUND_K_W_MK = 0.2
DEFAULT_BACKGROUND_THICKNESS_UM = 500.0
DEFAULT_H_CONTACT = 1500.0
DEFAULT_H_DRY = 5.0
DEFAULT_AMBIENT_C = 35.0
DEFAULT_AMBIENT_RH = 0.50


@dataclass(frozen=True)
class Topology2DResult:
    topology: str
    n: int
    high_k_material_fraction: float
    mean_sheet_conductance_W_K: float
    wet_fraction: float
    evap_total_g_h: float
    mean_body_heat_flux_W_m2: float
    gain_vs_no_lateral_W: float
    spreader_temperature_range_C: float
    max_outer_energy_residual_W_m2: float
    max_spreader_energy_residual_W_m2: float
    iterations: int
    converged: bool


def _harmonic(a: float, b: float) -> float:
    return 2.0 * a * b / (a + b + 1e-30)


def periodic_interval_fraction(
    n: int,
    domain_m: float,
    period_m: float,
    width_fraction: float,
) -> np.ndarray:
    """Return exact fractional periodic-stripe coverage for each 1-D cell."""
    if n <= 0 or domain_m <= 0 or period_m <= 0:
        raise ValueError("n, domain and period must be positive")
    if not 0.0 <= width_fraction <= 1.0:
        raise ValueError("width fraction must be in [0,1]")
    periods = domain_m / period_m
    if abs(periods - round(periods)) > 1e-10:
        raise ValueError("domain must contain an integer number of trace periods")

    dx = domain_m / n
    left = np.arange(n) * dx
    right = left + dx
    stripe_width = period_m * width_fraction
    fraction = np.zeros(n)
    for repeat in range(int(round(periods))):
        start = repeat * period_m
        end = start + stripe_width
        fraction += np.maximum(
            0.0,
            np.minimum(right, end) - np.maximum(left, start),
        ) / dx
    return np.clip(fraction, 0.0, 1.0)


def topology_fraction_field(
    topology: str,
    n: int,
    domain_mm: float = DEFAULT_DOMAIN_MM,
    trace_period_mm: float = DEFAULT_TRACE_PERIOD_MM,
) -> np.ndarray:
    """High-k material fraction in each cell; mean is exactly 0.5."""
    domain = domain_mm * 1e-3
    period = trace_period_mm * 1e-3

    if topology == "uniform_homogenized":
        field = np.full((n, n), 0.5)
    elif topology == "x_aligned_traces":
        # Traces run along x; their positions vary with y.
        fy = periodic_interval_fraction(n, domain, period, 0.5)
        field = np.tile(fy[:, None], (1, n))
    elif topology == "y_aligned_traces":
        # Traces run along y; their positions vary with x.
        fx = periodic_interval_fraction(n, domain, period, 0.5)
        field = np.tile(fx[None, :], (n, 1))
    elif topology == "connected_mesh":
        # Union of two orthogonal stripe families.  If each family covers f,
        # union coverage = 2f-f^2.  Set that equal to 0.5.
        f = 1.0 - np.sqrt(0.5)
        fx = periodic_interval_fraction(n, domain, period, f)
        fy = periodic_interval_fraction(n, domain, period, f)
        field = 1.0 - (1.0 - fy[:, None]) * (1.0 - fx[None, :])
    else:
        raise ValueError(f"unknown topology: {topology}")

    if abs(float(np.mean(field)) - 0.5) > 1e-10:
        raise RuntimeError("topology field does not preserve 50% material fraction")
    return field


def _wet_x_weights(beta: float, length_m: float, nx: int) -> np.ndarray:
    dx = length_m / nx
    centers = (np.arange(nx) + 0.5) * dx
    left = centers - dx / 2.0
    right = centers + dx / 2.0
    wet_left = length_m / 2.0 - beta * length_m / 2.0
    wet_right = length_m / 2.0 + beta * length_m / 2.0
    return np.maximum(
        0.0,
        np.minimum(right, wet_right) - np.maximum(left, wet_left),
    ) / dx


class TopologySpreader2D:
    def __init__(
        self,
        high_k_fraction_field: np.ndarray,
        domain_mm: float = DEFAULT_DOMAIN_MM,
        k_high_W_mK: float = DEFAULT_HIGH_K_W_MK,
        high_k_thickness_um: float = DEFAULT_HIGH_K_THICKNESS_UM,
        k_background_W_mK: float = DEFAULT_BACKGROUND_K_W_MK,
        background_thickness_um: float = DEFAULT_BACKGROUND_THICKNESS_UM,
        h_contact_W_m2K: float = DEFAULT_H_CONTACT,
        h_dry_W_m2K: float = DEFAULT_H_DRY,
        ambient_c: float = DEFAULT_AMBIENT_C,
        ambient_rh: float = DEFAULT_AMBIENT_RH,
    ) -> None:
        fraction = np.asarray(high_k_fraction_field, dtype=float)
        if fraction.ndim != 2 or fraction.shape[0] != fraction.shape[1]:
            raise ValueError("fraction field must be a square 2-D array")
        if np.any((fraction < 0.0) | (fraction > 1.0)):
            raise ValueError("material fraction must be in [0,1]")
        if h_contact_W_m2K <= 0 or h_dry_W_m2K < 0:
            raise ValueError("invalid contact or dry-side conductance")
        if not 0.0 <= ambient_rh <= 1.0:
            raise ValueError("ambient RH must be in [0,1]")

        self.fraction = fraction
        self.n = int(fraction.shape[0])
        self.length_m = domain_mm * 1e-3
        self.dx = self.length_m / self.n
        self.h_contact = float(h_contact_W_m2K)
        self.h_dry = float(h_dry_W_m2K)
        self.ambient_c = float(ambient_c)
        self.c_inf = float(ambient_rh * saturated_vapor_density(ambient_c))

        k_high_sheet = k_high_W_mK * high_k_thickness_um * 1e-6
        k_background_sheet = k_background_W_mK * background_thickness_um * 1e-6
        self.sheet_conductance = (
            k_background_sheet
            + fraction * (k_high_sheet - k_background_sheet)
        )

        rows: list[int] = []
        cols: list[int] = []
        values: list[float] = []

        def index(j: int, i: int) -> int:
            return j * self.n + i

        for j in range(self.n):
            for i in range(self.n):
                p = index(j, i)
                diagonal = -U_BODY - self.h_contact
                for dj, di in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    jj = (j + dj) % self.n
                    ii = (i + di) % self.n
                    conductance = _harmonic(
                        float(self.sheet_conductance[j, i]),
                        float(self.sheet_conductance[jj, ii]),
                    ) / self.dx**2
                    rows.append(p)
                    cols.append(index(jj, ii))
                    values.append(conductance)
                    diagonal -= conductance
                rows.append(p)
                cols.append(p)
                values.append(diagonal)

        matrix = coo_matrix(
            (values, (rows, cols)),
            shape=(self.n * self.n, self.n * self.n),
        ).tocsc()
        self._solve_spreader = factorized(matrix)

    def solve_wet_fraction(
        self,
        wet_fraction: float,
        tolerance_C: float = 4e-6,
        max_iterations: int = 220,
    ) -> dict[str, object]:
        wet_x = _wet_x_weights(wet_fraction, self.length_m, self.n)
        wet = np.tile(wet_x[None, :], (self.n, 1))
        spreader = np.full((self.n, self.n), 32.0)
        outer = np.full_like(spreader, 32.0)
        relax = 0.65
        change = np.inf

        for iteration in range(max_iterations):
            h_local = wet * H_WET + (1.0 - wet) * self.h_dry
            outer_new = (
                self.h_contact * spreader + h_local * self.ambient_c
            ) / (self.h_contact + h_local)

            for _ in range(12):
                vapor_excess = np.maximum(
                    saturated_vapor_density(outer_new) - self.c_inf,
                    0.0,
                )
                active = saturated_vapor_density(outer_new) > self.c_inf
                evap_flux = wet * KM_WET * vapor_excess
                residual = (
                    self.h_contact * (spreader - outer_new)
                    + h_local * (self.ambient_c - outer_new)
                    - L_V * evap_flux
                )
                derivative = (
                    -self.h_contact
                    - h_local
                    - L_V
                    * wet
                    * KM_WET
                    * saturated_vapor_density_derivative(outer_new)
                    * active
                )
                step = residual / derivative
                outer_new = np.clip(outer_new - step, 5.0, 55.0)
                if float(np.max(np.abs(step))) < 1e-10:
                    break

            rhs = np.full(spreader.size, -U_BODY * T_SKIN) - self.h_contact * outer_new.ravel()
            spreader_new = self._solve_spreader(rhs).reshape(spreader.shape)
            change = max(
                float(np.max(np.abs(spreader_new - spreader))),
                float(np.max(np.abs(outer_new - outer))),
            )
            spreader = (1.0 - relax) * spreader + relax * spreader_new
            outer = (1.0 - relax) * outer + relax * outer_new
            if change < tolerance_C:
                break

        h_local = wet * H_WET + (1.0 - wet) * self.h_dry
        outer = (
            self.h_contact * spreader + h_local * self.ambient_c
        ) / (self.h_contact + h_local)
        for _ in range(20):
            vapor_excess = np.maximum(
                saturated_vapor_density(outer) - self.c_inf,
                0.0,
            )
            active = saturated_vapor_density(outer) > self.c_inf
            evap_flux = wet * KM_WET * vapor_excess
            residual = (
                self.h_contact * (spreader - outer)
                + h_local * (self.ambient_c - outer)
                - L_V * evap_flux
            )
            derivative = (
                -self.h_contact
                - h_local
                - L_V
                * wet
                * KM_WET
                * saturated_vapor_density_derivative(outer)
                * active
            )
            step = residual / derivative
            outer = np.clip(outer - step, 5.0, 55.0)
            if float(np.max(np.abs(step))) < 1e-11:
                break

        evap_flux = wet * KM_WET * np.maximum(
            saturated_vapor_density(outer) - self.c_inf,
            0.0,
        )
        body_flux = U_BODY * (T_SKIN - spreader)
        outer_energy_residual = (
            self.h_contact * (spreader - outer)
            + h_local * (self.ambient_c - outer)
            - L_V * evap_flux
        )

        spreader_residual = np.zeros_like(spreader)
        for j in range(self.n):
            for i in range(self.n):
                conduction = 0.0
                for dj, di in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    jj = (j + dj) % self.n
                    ii = (i + di) % self.n
                    face = _harmonic(
                        float(self.sheet_conductance[j, i]),
                        float(self.sheet_conductance[jj, ii]),
                    )
                    conduction += (
                        face
                        * (spreader[jj, ii] - spreader[j, i])
                        / self.dx**2
                    )
                spreader_residual[j, i] = (
                    conduction
                    + U_BODY * (T_SKIN - spreader[j, i])
                    + self.h_contact * (outer[j, i] - spreader[j, i])
                )

        return {
            "wet_fraction": float(wet_fraction),
            "evap_total_g_h": float(
                np.mean(evap_flux) * 3.6e6 * STRUCTURED_AREA_M2
            ),
            "mean_body_heat_flux_W_m2": float(np.mean(body_flux)),
            "spreader_temperature_range_C": float(np.ptp(spreader)),
            "max_outer_energy_residual_W_m2": float(
                np.max(np.abs(outer_energy_residual))
            ),
            "max_spreader_energy_residual_W_m2": float(
                np.max(np.abs(spreader_residual))
            ),
            "iterations": iteration + 1,
            "converged": bool(change < tolerance_C),
        }

    def solve_feed(self, feed_total_g_h: float = 100.0) -> dict[str, object]:
        full = self.solve_wet_fraction(0.95)
        if full["evap_total_g_h"] <= feed_total_g_h:
            return full

        def mismatch(beta: float) -> float:
            return float(self.solve_wet_fraction(beta)["evap_total_g_h"]) - feed_total_g_h

        beta = brentq(mismatch, 0.001, 0.95, xtol=4e-5, maxiter=24)
        return self.solve_wet_fraction(beta)


def no_lateral_equal_feed_baseline(
    feed_total_g_h: float = 100.0,
    h_contact_W_m2K: float = DEFAULT_H_CONTACT,
    h_dry_W_m2K: float = DEFAULT_H_DRY,
    ambient_c: float = DEFAULT_AMBIENT_C,
    ambient_rh: float = DEFAULT_AMBIENT_RH,
) -> float:
    """Area-averaged body flux for the same wet/dry boundary conditions, no lateral routing."""
    c_inf = float(ambient_rh * saturated_vapor_density(ambient_c))

    def spreader_from_outer(outer_c: float) -> float:
        return float(
            (U_BODY * T_SKIN + h_contact_W_m2K * outer_c)
            / (U_BODY + h_contact_W_m2K)
        )

    def wet_balance(outer_c: float) -> float:
        spreader_c = spreader_from_outer(outer_c)
        evap = KM_WET * max(
            float(saturated_vapor_density(outer_c) - c_inf),
            0.0,
        )
        return (
            h_contact_W_m2K * (spreader_c - outer_c)
            + H_WET * (ambient_c - outer_c)
            - L_V * evap
        )

    wet_outer = brentq(wet_balance, 15.0, 40.0)
    wet_spreader = spreader_from_outer(wet_outer)
    wet_evap = KM_WET * max(
        float(saturated_vapor_density(wet_outer) - c_inf),
        0.0,
    )

    def dry_balance(outer_c: float) -> float:
        spreader_c = spreader_from_outer(outer_c)
        return (
            h_contact_W_m2K * (spreader_c - outer_c)
            + h_dry_W_m2K * (ambient_c - outer_c)
        )

    dry_outer = brentq(dry_balance, 15.0, 45.0)
    dry_spreader = spreader_from_outer(dry_outer)
    feed_flux = (feed_total_g_h / 1000.0 / 3600.0) / STRUCTURED_AREA_M2
    beta = min(feed_flux / wet_evap, 1.0)
    return float(
        beta * U_BODY * (T_SKIN - wet_spreader)
        + (1.0 - beta) * U_BODY * (T_SKIN - dry_spreader)
    )


def evaluate_topology(
    topology: str,
    n: int = 30,
    feed_total_g_h: float = 100.0,
) -> Topology2DResult:
    fraction = topology_fraction_field(topology, n)
    model = TopologySpreader2D(fraction)
    state = model.solve_feed(feed_total_g_h)
    baseline = no_lateral_equal_feed_baseline(feed_total_g_h)
    gain = (
        float(state["mean_body_heat_flux_W_m2"]) - baseline
    ) * STRUCTURED_AREA_M2
    return Topology2DResult(
        topology=topology,
        n=n,
        high_k_material_fraction=float(np.mean(fraction)),
        mean_sheet_conductance_W_K=float(np.mean(model.sheet_conductance)),
        wet_fraction=float(state["wet_fraction"]),
        evap_total_g_h=float(state["evap_total_g_h"]),
        mean_body_heat_flux_W_m2=float(state["mean_body_heat_flux_W_m2"]),
        gain_vs_no_lateral_W=float(gain),
        spreader_temperature_range_C=float(state["spreader_temperature_range_C"]),
        max_outer_energy_residual_W_m2=float(state["max_outer_energy_residual_W_m2"]),
        max_spreader_energy_residual_W_m2=float(state["max_spreader_energy_residual_W_m2"]),
        iterations=int(state["iterations"]),
        converged=bool(state["converged"]),
    )


def run_screen(n: int = 30) -> pd.DataFrame:
    topologies = (
        "uniform_homogenized",
        "x_aligned_traces",
        "y_aligned_traces",
        "connected_mesh",
    )
    return pd.DataFrame(
        [
            {"classification": "SIMULATION/SPREADER_TOPOLOGY_2D", **evaluate_topology(name, n).__dict__}
            for name in topologies
        ]
    )


if __name__ == "__main__":
    print(run_screen().to_string(index=False))
