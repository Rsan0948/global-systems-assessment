"""
Domain node 2F: open-source forks.

Observable: number of viable forks (a fork that itself passed a popularity
threshold, e.g. >100 stars) per parent project, for projects above a star
threshold. This is the software analogue of a subdivision factor.

BOUNDARY PROBE (PREREGISTRATION sec.3/sec.6): software has near-zero marginal
replication cost, a regime the theory predicts it should NOT cleanly govern. So
2F is registered as a boundary probe, not a core confirmation -- viable-fork
counts are expected to be heavy-tailed (preferential attachment), with high
variance, plausibly NOT a tight law.

REAL-DATA path (`ingest_github`): GitHub REST/GraphQL API (free, rate-limited)
or GH Archive (free bulk) -- NOT GHTorrent, which is defunct. No Crunchbase.
Import-guarded.

RUNNABLE: viable-fork counts sampled from a heavy-tailed (log-series-like)
process, matching the expected preferential-attachment behavior. Trivial null:
the same preferential-attachment process -- so a non-trivial result would
require the observed concentration to BEAT preferential attachment, which is the
honest high bar here.
"""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "integration"))
from node_api import DomainNode  # noqa: E402


def _viable_forks(n: int, rng: np.random.Generator) -> np.ndarray:
    """Heavy-tailed viable-fork counts (>=2), preferential-attachment-like."""
    # 2 + geometric-ish tail; produces a right-skewed cluster with high variance
    return 2 + rng.geometric(p=0.55, size=n) - 1


def build_node(seed: int = 0) -> DomainNode:
    rng = np.random.default_rng(seed)
    ratios = _viable_forks(150, rng).astype(float)
    return DomainNode(
        name="opensource",
        ratios=ratios,
        null_sampler=_viable_forks,           # null == the same heavy-tailed process
        is_self_organizing=True,              # but flagged as a boundary probe in docs
        source="GitHub fork-graph summary (illustrative; boundary probe; replace via ingest_github)",
    )


def ingest_github(*a, **k):  # pragma: no cover - needs network
    raise NotImplementedError(
        "Use the GitHub API or GH Archive to count viable forks (>100 stars) per "
        "popular parent repo; the build environment cannot reach GitHub."
    )
