"""
Census system: BOTANICAL TREES (real data).

Observable: Horton bifurcation ratio Rb per tree, measured by the SAME
Strahler/Horton instrument used for rivers and neurons (natural-systems/rivers/horton.py).
Each tree is a rooted branch skeleton; we root at the trunk base (minimum z) and
Strahler-order the branch tree.

Data: BioDiv-3DTrees (Göttingen Research Online, doi:10.25625/8PB1IF, CC BY 4.0,
no login) -- TLS-scanned trees as GraphML branch skeletons (nodes carry x,y,z +
radius; undirected edges). `ingest_trees.py` measures Rb per tree and caches
results/rb_trees.json. Raw GraphML (1.7 GB) is not committed.

Mechanism-free null: random binary merging topology measured by the same Horton
code, sized to tree leaf counts -- the triviality control. NOTE (Kirchner 1993):
random binary trees already give Rb ~ 3.8-4, so trees may be CONCENTRATED yet sit
AT this null. The census reports whichever the data shows.
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.dirname(HERE)
RESULTS = os.path.join(CENSUS, "results")
_2C = os.path.join(CENSUS, "..", "natural-systems", "rivers")
CACHE = os.path.join(RESULTS, "rb_trees.json")

PRIMARY_MIN_ORDERS = 4
_NULL_POOL_SIZE = 8000
_NULL_SIZE_RANGE = (20, 400)          # tree tip counts


def real_rb(min_orders: int = PRIMARY_MIN_ORDERS) -> np.ndarray:
    if not os.path.exists(CACHE):
        raise FileNotFoundError(f"missing {CACHE}; run `python ingest_trees.py`.")
    with open(CACHE) as f:
        rec = np.array(json.load(f)["records"], dtype=float)   # rb, max_order
    return rec[rec[:, 1] >= min_orders, 0]


def _build_null_pool() -> np.ndarray:
    sys.path.insert(0, _2C)
    from horton import measure_basin
    from river_node import _fast_coalescent_basin
    rng = np.random.default_rng(2718)
    recs = []
    while len(recs) < _NULL_POOL_SIZE:
        try:
            m = measure_basin(_fast_coalescent_basin(int(rng.integers(*_NULL_SIZE_RANGE)), rng),
                              min_orders=3)
        except ValueError:
            continue
        recs.append([round(float(m.rb), 6), int(m.max_order)])
    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "rb_trees_null_pool.json"), "w") as f:
        json.dump({"size": _NULL_POOL_SIZE, "fields": ["rb", "max_order"], "records": recs}, f)
    return np.array(recs, dtype=float)


def _load_null_pool() -> np.ndarray:
    path = os.path.join(RESULTS, "rb_trees_null_pool.json")
    if os.path.exists(path):
        with open(path) as f:
            return np.array(json.load(f)["records"], dtype=float)
    return _build_null_pool()


def make_null_sampler(min_orders: int = PRIMARY_MIN_ORDERS):
    pool = _load_null_pool()
    rb_pool = pool[pool[:, 1] >= min_orders, 0]

    def sampler(n: int, rng: np.random.Generator) -> np.ndarray:
        return rng.choice(rb_pool, size=n, replace=True)

    return sampler


def build_node(min_orders: int = PRIMARY_MIN_ORDERS):
    sys.path.insert(0, os.path.join(CENSUS, "..", "integration"))
    from node_api import DomainNode
    ratios = real_rb(min_orders)
    return DomainNode(
        name="trees",
        ratios=ratios,
        null_sampler=make_null_sampler(min_orders),
        is_self_organizing=True,
        source=f"BioDiv-3DTrees TLS skeletons (real); Horton Rb, "
               f"min_orders={min_orders}; n={ratios.size} trees",
    )
