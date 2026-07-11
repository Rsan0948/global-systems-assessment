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

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "integration"))
from node_api import DomainNode  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
CACHE = os.path.join(RESULTS, "corporate_splits_edgar.json")
SCALE = 3.0                                   # E/S unit scaling (unchanged observable)


# ----------------------------------------------------------- real observed data
def _load_cache() -> dict:
    if not os.path.exists(CACHE):
        raise FileNotFoundError(
            f"missing {CACHE}; run `python ingest_edgar.py --start 2001 --end 2024` "
            f"to fetch the real SEC EDGAR split factors.")
    with open(CACHE) as f:
        return json.load(f)


def real_split_factors() -> np.ndarray:
    """Real per-event split factor E/S * SCALE from the committed EDGAR cache."""
    return np.array(_load_cache()["ratios"], dtype=float)


# ----------------------------------------------- mechanism-free null (real S pool)
def make_binary_null(s_pool: list[int]):
    """Binary-by-default null: the mundane expectation that a firm splits in TWO
    relative to its ACTUAL reportable-segment structure (PREREGISTRATION sec.3).
    Successors E ~ 2 + small Poisson noise; segments S resampled from the real
    pool. The corporate signal counts only as the part of E/S that exceeds this
    binary baseline (firms fragmenting into MORE than two viable pieces)."""
    pool = np.array(s_pool, dtype=float)
    pool = pool[pool > 0]

    def sampler(n: int, rng: np.random.Generator) -> np.ndarray:
        E = 2 + rng.poisson(0.2, size=n)               # mundane "split in two"
        S = rng.choice(pool, size=n, replace=True)
        return E / S * SCALE

    return sampler


# --------------------------------------------------------------------- the node
def build_node(seed: int = 0) -> DomainNode:
    cache = _load_cache()
    ratios = np.array(cache["ratios"], dtype=float)
    s_pool = cache.get("real_S_pool") or [int(e["segments_S"]) for e in cache["events"]]
    cov = cache.get("coverage", {})
    return DomainNode(
        name="corporate",
        ratios=ratios,
        null_sampler=make_binary_null(s_pool),
        is_self_organizing=True,
        # No real allometric exponents for firms -> excluded from the rung-4
        # mechanism test, which runs ONLY on domains with REAL exponents (the
        # biology cell types). Placeholder values removed (were 2.0/1.0).
        interior_exp=None, interface_exp=None,
        source=f"SEC EDGAR (REAL): {cov.get('events_with_segments', len(ratios))} spin-off "
               f"events, split factor E/S x{SCALE:.0f}; via ingest_edgar",
    )


def ingest_edgar(start: int = 2001, end: int = 2024, **k):  # pragma: no cover - needs network
    """Fetch the real split factors from SEC EDGAR and write the committed cache.
    Delegates to ingest_edgar.ingest (the network crawler in this directory)."""
    sys.path.insert(0, HERE)
    import ingest_edgar as _ig
    return _ig.ingest(start=start, end=end, **k)
