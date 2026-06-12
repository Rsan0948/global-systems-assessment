"""
Domain node 2E: organizational scaling.

Observable: the inter-echelon scaling ratio of human organizations -- how many
sub-units aggregate into the next level up (squad -> platoon -> company; small
teams -> departments). Compiled from military doctrine tables across countries
and from team-size studies (Dunbar, Hackman, Wheelan).

Honest caveat: organizations are PARTLY designed (span-of-control doctrine), so
this domain sits between self-organizing and engineered. We keep it in the
ladder but its trivial null is a span-of-control prior (Graicunas ~5-6); the
organizational signal counts only if it departs from that.

REAL-DATA path: parse publicly downloadable doctrine manuals (e.g. US Army FM
7-0) and published team-performance meta-analysis tables. Import-guarded.
RUNNABLE: inter-echelon ratios sampled from documented doctrine values (~3-4
across echelons and armies).
"""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "integration"))
from node_api import DomainNode, lognormal_null  # noqa: E402

# Documented inter-echelon fan-out ratios (sub-units per parent unit) across
# several armies/echelons; these cluster ~3-4.
DOCTRINE_RATIOS = [3.0, 3.0, 4.0, 3.0, 4.0, 3.0, 3.0, 4.0, 3.0, 3.5,
                   3.0, 4.0, 3.0, 3.0, 2.5, 4.0, 3.0, 3.5, 3.0, 3.0]


def build_node(seed: int = 0) -> DomainNode:
    rng = np.random.default_rng(seed)
    base = np.array(DOCTRINE_RATIOS, dtype=float)
    ratios = base * np.exp(rng.normal(0, 0.08, size=base.size))   # small measurement jitter
    return DomainNode(
        name="organizations",
        ratios=ratios,
        null_sampler=lognormal_null(center=5.5, log_sd=0.25),     # span-of-control prior
        is_self_organizing=True,
        interior_exp=2.0, interior_exp_se=0.3,                    # internal comms ~ size^2
        interface_exp=1.0, interface_exp_se=0.3,                  # management throughput ~ size
        source="military doctrine tables + team-size studies (illustrative)",
    )
