"""
REAL biology nodes (Study 2D): neuronal/dendritic arbor branching.

One DomainNode per mechanistically-distinct cell type (pyramidal, Purkinje,
granule, ganglion, interneuron, motoneuron) -- independent natural experiments,
each its own domain in the ladder (so the engine can tell "one biological law"
from "many"). Ratios = per-arbor Horton Rb cached by fetch_neuromorpho.py from
NeuroMorpho.org, measured by the SAME Strahler/Horton code as rivers.

Mechanism-free null: random binary merging topology at neuron-arbor scale,
measured by the same Horton code (the rivers triviality-control logic). A
biological sub-domain counts only if it sits away from this ~3 null.

Real allometric exponents (rung-4 mechanism test) are not yet estimated, so
interior_exp/interface_exp are None here (Phase 3).
"""

from __future__ import annotations

import glob
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
_2C = os.path.join(HERE, "..", "2C_river_networks")

PRIMARY_MIN_ORDERS = 3            # neuron arbors are smaller than river basins
_NULL_POOL_SIZE = 8000
_NULL_SIZE_RANGE = (15, 250)      # leaf counts comparable to dendritic arbors


# --------------------------------------------------------------- observed Rb
def _cache_path(cell_type: str) -> str:
    return os.path.join(RESULTS, f"rb_bio_{cell_type.lower()}.json")


def _load_records(cell_type: str) -> np.ndarray:
    path = _cache_path(cell_type)
    if not os.path.exists(path):
        raise FileNotFoundError(f"missing {path}; run `python fetch_neuromorpho.py`.")
    with open(path) as f:
        payload = json.load(f)
    return np.array(payload["records"], dtype=float)  # rb, max_order, r2


def available_cell_types() -> list[str]:
    out = []
    for p in sorted(glob.glob(os.path.join(RESULTS, "rb_bio_*.json"))):
        base = os.path.basename(p)[len("rb_bio_"):-len(".json")]
        if base != "null_pool":
            out.append(base)
    return out


def real_rb(cell_type: str, min_orders: int = PRIMARY_MIN_ORDERS) -> np.ndarray:
    rec = _load_records(cell_type)
    return rec[rec[:, 1] >= min_orders, 0]


def sensitivity_table(cell_type: str) -> dict:
    rec = _load_records(cell_type)
    out = {}
    for mo in (3, 4, 5):
        rb = rec[rec[:, 1] >= mo, 0]
        out[mo] = {"n": int(rb.size),
                   "geom_mean": float(np.exp(np.log(rb).mean())) if rb.size else None,
                   "median": float(np.median(rb)) if rb.size else None}
    return out


# ----------------------------------------------------------- mechanism-free null
def _build_null_pool() -> np.ndarray:
    sys.path.insert(0, _2C)
    from horton import measure_basin
    from river_node import _fast_coalescent_basin   # same generator rivers' null uses

    rng = np.random.default_rng(31415)
    recs = []
    while len(recs) < _NULL_POOL_SIZE:
        n_src = int(rng.integers(*_NULL_SIZE_RANGE))
        try:
            m = measure_basin(_fast_coalescent_basin(n_src, rng), min_orders=3)
        except ValueError:
            continue
        recs.append([round(float(m.rb), 6), int(m.max_order)])
    arr = np.array(recs, dtype=float)
    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "rb_bio_null_pool.json"), "w") as f:
        json.dump({"size": _NULL_POOL_SIZE, "size_range": list(_NULL_SIZE_RANGE),
                   "fields": ["rb", "max_order"], "records": recs}, f)
    return arr


def _load_null_pool() -> np.ndarray:
    path = os.path.join(RESULTS, "rb_bio_null_pool.json")
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


# --------------------------------------------------------------------- the nodes
def build_nodes(min_orders: int = PRIMARY_MIN_ORDERS) -> list:
    sys.path.insert(0, os.path.join(HERE, "..", "..", "integration"))
    from node_api import DomainNode

    sampler = make_null_sampler(min_orders)
    nodes = []
    for ct in available_cell_types():
        ratios = real_rb(ct, min_orders)
        if ratios.size < 2:
            continue
        nodes.append(DomainNode(
            name=f"neuro_{ct}",
            ratios=ratios,
            null_sampler=sampler,
            is_self_organizing=True,
            interior_exp=None, interface_exp=None,   # real allometry deferred (Phase 3)
            source=f"NeuroMorpho {ct} arbors (real); Horton Rb, "
                   f"min_orders={min_orders}; n={ratios.size}",
        ))
    return nodes
