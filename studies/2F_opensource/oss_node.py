"""
Domain node 2F: open-source forks (REAL DATA).

Observable: number of viable forks per popular parent project, where a viable
fork is one whose own star count crossed a popularity threshold (it attracted an
independent following). The software analogue of a subdivision factor (viable
children per parent). One value per parent; the node's `ratios` are the real
per-parent viable-fork counts cached by `ingest_github.py` from the GitHub REST
forks API (sorted by stars -> lifetime star counts).

BOUNDARY PROBE (PREREGISTRATION sec.3/sec.6): software has near-zero marginal
replication cost, a regime the theory predicts it should NOT cleanly govern.
Viable-fork counts are expected heavy-tailed (preferential attachment), high
variance, plausibly NOT a tight law.

Mechanism-free null: a preferential-attachment process -- a memoryless
(geometric) heavy-tailed count matched in mean to the observed parents. A
non-trivial result would require the observed concentration to BEAT preferential
attachment, the honest high bar for this domain.

REAL-DATA path (`ingest_github`): GitHub REST `/repos/{p}/forks?sort=stargazers`
for lifetime star counts. GH Archive was REJECTED (fork-spam dominated; no
lifetime stars) -- see ingest_github.py. Primary viability threshold 10 stars
(node doc's ">100" is an illustrative "e.g."; >100-star forks are empirically
rare), full sensitivity {5,10,25,50,100} carried in the cache (PREREGISTRATION
sec.8).
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
CACHE = os.path.join(RESULTS, "oss_forks_github.json")


def _load_cache() -> dict:
    if not os.path.exists(CACHE):
        raise FileNotFoundError(
            f"missing {CACHE}; run `python ingest_github.py` to fetch the real "
            f"GitHub viable-fork counts.")
    with open(CACHE) as f:
        return json.load(f)


def real_viable_forks() -> np.ndarray:
    """Real per-parent viable-fork counts at the primary threshold."""
    return np.array(_load_cache()["ratios"], dtype=float)


def make_pa_null(observed_mean: float):
    """Preferential-attachment null: a memoryless (geometric) heavy-tailed
    viable-fork count, matched in mean to the observed parents. The domain beats
    it only if its dispersion is TIGHTER than this PA baseline (it will not be --
    the boundary-probe high bar, PREREGISTRATION sec.3)."""
    mean = max(1.0001, float(observed_mean))
    p = 1.0 / mean                                  # geometric mean = 1/p

    def sampler(n: int, rng: np.random.Generator) -> np.ndarray:
        return rng.geometric(p=p, size=n).astype(float)   # >= 1, heavy-tailed

    return sampler


def build_node(seed: int = 0) -> DomainNode:
    cache = _load_cache()
    ratios = np.array(cache["ratios"], dtype=float)
    cov = cache.get("coverage", {})
    return DomainNode(
        name="opensource",
        ratios=ratios,
        null_sampler=make_pa_null(ratios.mean() if ratios.size else 2.0),
        is_self_organizing=True,                    # flagged a boundary probe in docs
        source=f"GitHub forks API (REAL): {cov.get('parents_with_viable_primary', len(ratios))} "
               f"parents, viable forks >= {cache.get('primary_threshold_stars', 10)} stars; "
               f"boundary probe; via ingest_github",
    )


def ingest_github(target: int = 120, **k):  # pragma: no cover - needs network
    """Fetch real viable-fork counts from GitHub and write the committed cache.
    Delegates to ingest_github.ingest (the network crawler in this directory)."""
    sys.path.insert(0, HERE)
    import ingest_github as _ig
    return _ig.ingest(target_parents=target, **k)
