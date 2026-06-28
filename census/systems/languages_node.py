"""
Census system: LANGUAGE FAMILIES (real data) -- the self-organized HUMAN control.

Languages fragment as speech communities grow and disperse: no central designer
decides the splits, so language families are a *self-organized human* system --
the clean test of "grown, whoever does the growing" (cf. cities). If they land
in the concentrated band with rivers/neurons/trees, the real axis is
grown-vs-designed, not biology-vs-human.

Observable: Horton-Strahler bifurcation ratio Rb per language FAMILY, measured by
the SAME instrument as rivers and neurons. Each family is a rooted tree of
languoids (family -> subfamilies -> ... -> languages -> dialects); we Strahler-
order it and read Rb.

Data: Glottolog (glottolog-cldf, CC BY 4.0, no login) -- each languoid's
`classification` value is its ancestry path of glottocodes, which reconstructs
the full phylogeny. `ingest_languages.py` caches results/rb_languages.json.

Mechanism-free null: random binary merging topology measured by the same Horton
code, sized to family leaf counts (the triviality control).
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.dirname(HERE)
RESULTS = os.path.join(CENSUS, "results")
_2C = os.path.join(CENSUS, "..", "studies", "2C_river_networks")
CACHE = os.path.join(RESULTS, "rb_languages.json")

PRIMARY_MIN_ORDERS = 4
_NULL_POOL_SIZE = 8000
_NULL_SIZE_RANGE = (15, 400)          # family leaf (language) counts


def real_rb(min_orders: int = PRIMARY_MIN_ORDERS) -> np.ndarray:
    if not os.path.exists(CACHE):
        raise FileNotFoundError(f"missing {CACHE}; run `python ingest_languages.py`.")
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
    with open(os.path.join(RESULTS, "rb_languages_null_pool.json"), "w") as f:
        json.dump({"size": _NULL_POOL_SIZE, "fields": ["rb", "max_order"], "records": recs}, f)
    return np.array(recs, dtype=float)


def _load_null_pool() -> np.ndarray:
    path = os.path.join(RESULTS, "rb_languages_null_pool.json")
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
        name="languages",
        ratios=ratios,
        null_sampler=make_null_sampler(min_orders),
        is_self_organizing=True,
        source=f"Glottolog language families (real); Horton Rb, "
               f"min_orders={min_orders}; n={ratios.size} families",
    )
