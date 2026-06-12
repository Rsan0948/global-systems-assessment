"""
Domain node 2D: biological branching.

Observable (comparable factor, per PREREGISTRATION sec.4): the branching ratio
of self-organizing biological hierarchies -- bronchial trees, vascular beds,
botanical branching. One measurement = one species/tissue/vessel-bed's reported
ratio.

REAL-DATA path (`ingest_*`): US Forest Service FIA for tree branching, published
morphometry supplementary tables (e.g. LMFIT lung data) for bronchial/vascular
ratios. Import-guarded; not reachable from the firewalled build environment.

RUNNABLE node: measurements are sampled from literature-reported summary
statistics (central ratio + spread + n) per subdomain. These encode published
*ranges*, not invented precision, and are swappable for raw measurements via
`ingest_*`. Clearly a pipeline input, not a finding.

Trivial null (sec.3): random binary branching topology, which lands near ~3
(see studies/2C). The biological signal counts only if it sits away from this.
"""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "integration"))
from node_api import DomainNode, lognormal_null  # noqa: E402

# (subdomain, central branching ratio, CV, n_measurements, note)
# Central values reflect commonly reported literature ranges; bronchial Horton
# ratios ~2.5-3, many vascular beds ~2.7-3.4, botanical branching broader.
LITERATURE = [
    ("human_bronchial", 2.8, 0.12, 14, "Horton ratio, conducting airways"),
    ("rat_pulmonary_arterial", 3.0, 0.15, 10, "pulmonary arterial tree"),
    ("human_coronary", 2.9, 0.16, 9, "coronary arterial branching"),
    ("retinal_vascular", 2.7, 0.14, 12, "retinal arteriolar network"),
    ("cerebral_arterial", 3.1, 0.18, 8, "cerebral arterial tree"),
    ("oak_botanical", 3.4, 0.22, 11, "botanical branch ratio, deciduous"),
    ("pine_botanical", 3.2, 0.20, 10, "botanical branch ratio, conifer"),
    ("kidney_arterial", 2.85, 0.15, 7, "renal arterial branching"),
]


def build_node(seed: int = 0) -> DomainNode:
    rng = np.random.default_rng(seed)
    measurements = []
    for _name, center, cv, n, _note in LITERATURE:
        log_sd = np.sqrt(np.log(1 + cv ** 2))
        measurements.extend(list(center * np.exp(rng.normal(0, log_sd, size=n))))
    ratios = np.array(measurements)
    # Murray's law -> exponent ~3 (interior metabolic/volume scaling); the
    # interface (surface/transport) exponent ~2. Gap ~1. These illustrative
    # exponents feed the rung-4 harness; 3B's estimator replaces them from raw
    # allometry when available.
    return DomainNode(
        name="biology",
        ratios=ratios,
        null_sampler=lognormal_null(center=3.1, log_sd=0.16),
        is_self_organizing=True,
        interior_exp=3.0, interior_exp_se=0.15,
        interface_exp=2.0, interface_exp_se=0.18,
        source="literature summary stats (replace via ingest_*)",
    )


def ingest_fia(path: str):  # pragma: no cover - needs real data + network
    """Hook for US Forest Service FIA tree data -> branching ratios."""
    raise NotImplementedError(
        "Wire FIA tree records to per-tree branching ratios here; the build "
        "environment cannot reach the FIA download."
    )
