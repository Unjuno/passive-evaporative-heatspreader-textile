"""Combined apparel-failure screen for the 2-D heat network.

The preceding screens treated stretch, conductor damage and thermal-contact loss
separately.  This module combines them in one deterministic mechanism screen:

- 20% uniaxial stretch using the compliant-serpentine x-conduction factor;
- localized low thermal contact around one wet evaporator island;
- localized removal of 5% of the initial high-k conductor cells near the same
  wet island.

The comparison uses matched low-conductivity background fields under the same
stretch/contact condition so reported values remain routing-mechanism gains.

This is a virtual robustness screen, not a lifetime or durability prediction.
No physical specimen exists.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

try:
    from simulations.distributed_spreader_1d import STRUCTURED_AREA_M2
    from simulations.heat_network_apparel_robustness import (
        RobustHeatNetworkTile,
        contact_field,
        stretch_conduction_factor,
    )
    from simulations.heat_network_topology_2d import (
        localized_damage,
        topology_mask,
        wet_mask,
    )
except ModuleNotFoundError:
    from distributed_spreader_1d import STRUCTURED_AREA_M2
    from heat_network_apparel_robustness import (
        RobustHeatNetworkTile,
        contact_field,
        stretch_conduction_factor,
    )
    from heat_network_topology_2d import localized_damage, topology_mask, wet_mask


def routing_gain(
    conductor: np.ndarray,
    wet: np.ndarray,
    contact: np.ndarray,
    x_factor: float = 1.0,
) -> tuple[float, bool]:
    background = RobustHeatNetworkTile(
        np.zeros_like(conductor),
        wet,
        contact,
        x_conduction_factor=x_factor,
    ).solve()
    routed = RobustHeatNetworkTile(
        conductor,
        wet,
        contact,
        x_conduction_factor=x_factor,
    ).solve()
    gain = (
        float(routed["body_heat_flux_W_m2"])
        - float(background["body_heat_flux_W_m2"])
    ) * STRUCTURED_AREA_M2
    return gain, bool(background["converged"] and routed["converged"])


def run_combined_screen(n: int = 24) -> pd.DataFrame:
    wet = wet_mask("four_islands", n)
    nominal_contact = contact_field("uniform", n)
    wet_contact_loss = contact_field("localized_wet_island", n)
    stretch20 = stretch_conduction_factor(0.20, "serpentine_screen")

    candidates = (
        ("directed", "directed_mesh_blend", 0.0),
        ("blend_0p125", "directed_mesh_blend", 0.125),
        ("blend_0p375", "directed_mesh_blend", 0.375),
        ("mesh", "redundant_mesh", None),
        ("leaf", "leaf_venation", None),
    )
    conditions = (
        ("nominal", False, False, False),
        ("stretch20", True, False, False),
        ("wet_contact_loss", False, True, False),
        ("local_5pct_fracture", False, False, True),
        ("stretch_plus_contact", True, True, False),
        ("contact_plus_fracture", False, True, True),
        ("all_three", True, True, True),
    )

    rows: list[dict[str, object]] = []
    for label, topology, mesh_weight in candidates:
        if topology == "directed_mesh_blend":
            conductor_nominal = topology_mask(
                topology,
                n,
                mesh_weight=mesh_weight,
            )
        else:
            conductor_nominal = topology_mask(topology, n)

        nominal_gain, nominal_ok = routing_gain(
            conductor_nominal,
            wet,
            nominal_contact,
            1.0,
        )

        for condition, use_stretch, use_contact_loss, use_fracture in conditions:
            conductor = conductor_nominal
            if use_fracture:
                conductor = localized_damage(
                    conductor_nominal,
                    0.25,
                    0.25,
                    0.05,
                )
            contact = wet_contact_loss if use_contact_loss else nominal_contact
            x_factor = stretch20 if use_stretch else 1.0
            gain, ok = routing_gain(conductor, wet, contact, x_factor)
            rows.append(
                {
                    "topology": label,
                    "condition": condition,
                    "gain_W": gain,
                    "retained_percent": 100.0 * gain / nominal_gain,
                    "converged": bool(ok and nominal_ok),
                }
            )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    result = run_combined_screen()
    print(result.to_string(index=False))
