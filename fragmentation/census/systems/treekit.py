"""
Shared helpers for tree-topology census systems (languages, Linux distros,
admin hierarchies, denominations, ...). Each such system reduces to a
parent-map {child: parent}; this turns that into per-root Horton-Strahler Rb
plus a cached random-topology null -- the SAME instrument and null doctrine used
for rivers/neurons/trees.
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_2C = os.path.join(_HERE, "..", "..", "natural-systems", "rivers")
RESULTS = os.path.join(_HERE, "..", "results")


def rb_per_root(parent: dict, min_orders_floor: int = 3, min_nodes: int = 6):
    """parent: {child: parent_or_None}. Strahler Rb for each root's subtree."""
    sys.path.insert(0, _2C)
    from horton import measure_basin
    children: dict = {}
    nodes = set()
    for c, p in parent.items():
        nodes.add(c)
        if p is not None:
            nodes.add(p)
            children.setdefault(p, []).append(c)
    roots = [n for n in nodes if parent.get(n) is None]
    out = []
    for root in roots:
        sub, stack = [], [root]
        while stack:
            u = stack.pop()
            sub.append(u)
            stack.extend(children.get(u, []))
        if len(sub) < min_nodes:
            continue
        idx = {n: i for i, n in enumerate(sub)}
        downstream = {idx[root]: -1}
        for p, kids in children.items():
            if p in idx:
                for k in kids:
                    if k in idx:
                        downstream[idx[k]] = idx[p]
        if len(downstream) != len(sub):
            continue
        try:
            m = measure_basin(downstream, min_orders=min_orders_floor)
        except ValueError:
            continue
        out.append([round(float(m.rb), 6), int(m.max_order)])
    return out


def _null_pool(tag: str, size_range, size: int = 8000) -> np.ndarray:
    path = os.path.join(RESULTS, f"rb_{tag}_null_pool.json")
    if os.path.exists(path):
        with open(path) as f:
            return np.array(json.load(f)["records"], dtype=float)
    sys.path.insert(0, _2C)
    from horton import measure_basin
    from river_node import _fast_coalescent_basin
    rng = np.random.default_rng(2718)
    recs = []
    while len(recs) < size:
        try:
            m = measure_basin(_fast_coalescent_basin(int(rng.integers(*size_range)), rng),
                              min_orders=3)
        except ValueError:
            continue
        recs.append([round(float(m.rb), 6), int(m.max_order)])
    os.makedirs(RESULTS, exist_ok=True)
    with open(path, "w") as f:
        json.dump({"size": size, "fields": ["rb", "max_order"], "records": recs}, f)
    return np.array(recs, dtype=float)


def make_null_sampler(tag: str, size_range, min_orders: int):
    pool = _null_pool(tag, size_range)
    rb_pool = pool[pool[:, 1] >= min_orders, 0]

    def sampler(n: int, rng: np.random.Generator) -> np.ndarray:
        return rng.choice(rb_pool, size=n, replace=True)

    return sampler


def load_cache_rb(tag: str, min_orders: int) -> np.ndarray:
    path = os.path.join(RESULTS, f"rb_{tag}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"missing {path}; run its ingest.")
    with open(path) as f:
        rec = np.array(json.load(f)["records"], dtype=float)
    return rec[rec[:, 1] >= min_orders, 0]


def build_tree_node(name: str, tag: str, size_range=(15, 400), min_orders: int = 4,
                    source: str = ""):
    sys.path.insert(0, os.path.join(_HERE, "..", "..", "integration"))
    from node_api import DomainNode
    ratios = load_cache_rb(tag, min_orders)
    return DomainNode(
        name=name, ratios=ratios,
        null_sampler=make_null_sampler(tag, size_range, min_orders),
        is_self_organizing=True,
        source=source or f"{name} (real); Horton Rb, min_orders={min_orders}; n={ratios.size}")
