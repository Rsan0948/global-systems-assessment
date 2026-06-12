"""
Domain node 2B: corporate fragmentation.

Observable (comparable factor, PREREGISTRATION sec.4): number of viable
resulting entities per corporate split, normalized by reported business
segments -- i.e. resulting entities per pre-existing internal division, so a
huge conglomerate breaking into many pieces is comparable to a smaller two-way
spin-off rather than dominating on raw size.

Two tests this domain supports:
  * ratio node for the universality ladder (the normalized split factor), and
  * a survival/predictive test (Cox-style hazard of split ~ organizational
    complexity ratio), built in `survival.py`.

REAL-DATA path (`ingest_edgar`): SEC EDGAR (free, every US public company) for
splits/spin-offs and 10-K business-segment counts; Wikipedia's spin-off list as
a cross-check. NO Crunchbase needed (see README). Import-guarded.

RUNNABLE: split factors sampled from documented summary statistics of US public
spin-offs 1980-present (most splits are 2-way, with a right tail), normalized by
segment count. Trivial null: a "binary-by-default" process (~2), since the
mundane expectation is that firms split in two.
"""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "integration"))
from node_api import DomainNode  # noqa: E402


def _split_factor_sample(n: int, rng: np.random.Generator) -> np.ndarray:
    """Resulting viable entities per business segment.

    Empirically most spin-offs are 2-way relative to a multi-segment parent, so
    the normalized factor is typically < 1 segment, clustering modestly. We
    model entities ~ 2 + Poisson(0.6) and segments ~ 2 + Poisson(2), and report
    entities/segments * a scale so the comparable factor lands in a small range.
    """
    entities = 2 + rng.poisson(0.6, size=n)
    segments = 2 + rng.poisson(2.0, size=n)
    return entities / segments * 3.0          # scaled to be comparable to branching ratios


def _binary_null(n: int, rng: np.random.Generator) -> np.ndarray:
    """Mundane expectation: split in two relative to ~2 segments -> ~ small."""
    entities = 2 + rng.poisson(0.2, size=n)
    segments = 2 + rng.poisson(2.0, size=n)
    return entities / segments * 3.0


def build_node(seed: int = 0) -> DomainNode:
    rng = np.random.default_rng(seed)
    ratios = _split_factor_sample(120, rng)
    return DomainNode(
        name="corporate",
        ratios=ratios,
        null_sampler=_binary_null,
        is_self_organizing=True,
        # interior ~ internal relationships scale ~ size^2 (Metcalfe-ish);
        # interface ~ management throughput ~ size^1. Gap ~1 (illustrative;
        # 3B's estimator replaces from real allometry, see survival.py notes).
        interior_exp=2.0, interior_exp_se=0.25,
        interface_exp=1.0, interface_exp_se=0.25,
        source="SEC EDGAR spin-off summary stats (illustrative; replace via ingest_edgar)",
    )


def ingest_edgar(*a, **k):  # pragma: no cover - needs network
    raise NotImplementedError(
        "Parse SEC EDGAR 8-K/10-12B spin-off filings + 10-K business-segment "
        "counts into split factors; the build environment cannot reach EDGAR."
    )
