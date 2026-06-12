"""
Domain nodes built from literature-reported summary statistics, so the full
pipeline (assemble -> ladder -> verdict) runs end-to-end without network access.

These are ILLUSTRATIVE inputs, not measurements: each node's ratios are sampled
from a documented central value + spread (published ranges, not invented
precision). Swap in raw per-measurement data via each study's `ingest_*` to make
it a real result. Treating each biological subsystem as its own domain is
defensible -- they are independent natural experiments with distinct mechanisms.

NOTE: rivers are NO LONGER here -- the rivers node is now REAL data
(studies/2C_river_networks/river_node.build_node(), from the HydroRIVERS
download). Only the biology subsystems below remain literature-summary
placeholders, pending their own ingest_* wiring (FIA + morphometry).

Documented central branching/bifurcation ratios (typical literature ranges):
  bronchial tree       ~ 2.5-3
  arterial beds        ~ 2.7-3.4
  botanical branching  ~ 3-3.6 (broader)
"""

from __future__ import annotations

import numpy as np

from node_api import DomainNode, lognormal_null

# (name, central ratio, CV, n, null center, interior_exp, interface_exp)
SPEC = [
    ("bronchial",  2.8, 0.12, 16, 3.0, 3.0, 2.0),
    ("vascular",   3.0, 0.15, 20, 3.2, 3.0, 2.0),
    ("botanical",  3.3, 0.22, 18, 3.4, 2.8, 1.9),
]


def _sample(center: float, cv: float, n: int, rng) -> np.ndarray:
    log_sd = np.sqrt(np.log(1 + cv ** 2))
    return center * np.exp(rng.normal(0, log_sd, size=n))


def literature_nodes(seed: int = 0) -> list[DomainNode]:
    rng = np.random.default_rng(seed)
    nodes = []
    for name, center, cv, n, null_c, ie, fe in SPEC:
        nodes.append(DomainNode(
            name=name,
            ratios=_sample(center, cv, n, rng),
            null_sampler=lognormal_null(center=null_c, log_sd=0.16),
            is_self_organizing=True,
            interior_exp=ie, interior_exp_se=0.15,
            interface_exp=fe, interface_exp_se=0.18,
            source="literature summary stats (illustrative; replace via ingest_*)",
        ))
    return nodes
