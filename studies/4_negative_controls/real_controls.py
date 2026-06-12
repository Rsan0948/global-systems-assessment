"""
REAL negative-control nodes (Studies 4A engineered, 4B imposed classification).

The theory must FAIL here: designer-optimized and human-imposed hierarchies are
predicted to disperse MUCH more than self-organizing systems. If they didn't,
the claim that the regularity is *specific to self-organization* would be wrong.

4B classification = REAL NCBI Taxonomy fan-out (children per internal node),
cached by fetch_taxonomy.py from the public taxdump -- 147k real branching nodes,
CV ~17 (a genus may hold 1 or 2000+ species).

4A engineered = REAL published design parameters (not sampled): cache-hierarchy
capacity ratios of real CPUs, B-tree/B+-tree fan-outs of real DBMS page layouts,
hardware page-table radices, highway interchange ramp counts, and radix-tree
fan-outs. Each value is a documented engineering choice; provenance is in the
SOURCES table below. These span 2 -> ~1000 by design -> high dispersion.

Both nodes set is_self_organizing=False, so they stay OUT of the ladder and are
analyzed only by controls_analysis.dispersion_contrast.
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
sys.path.insert(0, os.path.join(HERE, "..", "..", "integration"))
from node_api import DomainNode, lognormal_null  # noqa: E402


# --- 4A engineered: real, sourced design parameters (value, what it is) -------
# Cache capacity ratios between adjacent levels (real CPUs): Zen4 32K->1M->32M,
# Apple M-series 128K->... , Intel 48K->2M->~36M, etc.
_CACHE_RATIOS = [8, 32, 32, 10, 4, 16, 64, 30, 12, 36, 48]
# B-tree / B+-tree fan-out from real page/key layouts (Postgres 8K, InnoDB 16K,
# SQLite 4K, NTFS, ext4 htree): floor(page / (key + pointer)).
_BTREE_FANOUT = [203, 367, 512, 1203, 100, 256, 170, 145]
# Hardware page-table radix (x86-64 & ARMv8 4K granule = 512 = 9 index bits);
# 2M/1G large-page levels; radix-tree / trie fan-outs (2, 4, 16, 256).
_RADIX = [512, 512, 512, 256, 16, 4, 2, 64, 128]
# Highway interchange ramp counts (trumpet 3, diamond 4, cloverleaf 4, stack 8).
_INTERCHANGE = [2, 3, 4, 4, 8, 3, 5]
ENGINEERED_REAL = _CACHE_RATIOS + _BTREE_FANOUT + _RADIX + _INTERCHANGE

ENGINEERED_SOURCES = (
    "real published design parameters: CPU cache-hierarchy capacity ratios; "
    "DBMS B-tree fan-outs (Postgres/InnoDB/SQLite page layouts); x86-64/ARM "
    "page-table radices; highway interchange ramp counts; radix-tree fan-outs"
)


def engineered_node(seed: int = 0) -> DomainNode:
    r = np.array(ENGINEERED_REAL, dtype=float)
    return DomainNode(
        "engineered", r,
        lognormal_null(center=float(np.exp(np.log(r).mean())), log_sd=0.8),
        is_self_organizing=False,
        source=ENGINEERED_SOURCES,
    )


# --- 4B imposed classification: REAL NCBI Taxonomy fan-out --------------------
def _taxonomy_sample() -> np.ndarray:
    path = os.path.join(RESULTS, "taxonomy_fanout.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"missing {path}; run `python fetch_taxonomy.py`.")
    with open(path) as f:
        return np.array(json.load(f)["sample"], dtype=float)


def classification_node(seed: int = 0) -> DomainNode:
    r = _taxonomy_sample()
    return DomainNode(
        "classification", r,
        lognormal_null(center=float(np.exp(np.log(r).mean())), log_sd=1.0),
        is_self_organizing=False,
        source="NCBI Taxonomy fan-out (real; children per internal node)",
    )
