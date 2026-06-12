"""
Negative-control nodes (Studies 4A, 4B). The theory predicts these do NOT show
the lawful concentration of self-organizing systems -- they should have much
HIGHER and more variable subdivision ratios, because they are optimized by
external designers (4A) or imposed by human categorization (4B), not produced by
the interior/interface dimensional gap.

If a control node clustered as tightly as the self-organizing nodes, the claim
that the regularity is *specific to self-organization* would be wrong -- so
these are real falsifiers of the boundary conditions, not decoration.

`is_self_organizing=False` keeps them OUT of the universality ladder; they are
analyzed separately by `analysis.dispersion_contrast`.
"""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "integration"))
from node_api import DomainNode, lognormal_null  # noqa: E402


# --- 4A engineered systems: designer-chosen fan-outs span orders of magnitude
ENGINEERED_RATIOS = [
    4, 8, 16, 8, 4, 16, 2,          # memory/cache hierarchy size ratios
    128, 256, 100, 170, 200,        # filesystem / DB B-tree fan-out (order)
    3, 4, 3, 4, 2, 5,               # highway interchange branching degree
    32, 64, 10, 1000,               # page-table / radix / wide indexes
]

# --- 4B imposed classifications: human categories, high + variable
CLASSIFICATION_RATIOS = [
    5, 7, 12, 3, 40, 2, 60, 8, 15, 4,    # species per genus (very skewed)
    6, 9, 20, 11, 30,                    # genera per family
    10, 10, 10, 10,                      # Dewey: exactly 10 by construction
    21, 21,                              # LoC top classes
]


def engineered_node(seed: int = 0) -> DomainNode:
    rng = np.random.default_rng(seed)
    r = np.array(ENGINEERED_RATIOS, float) * np.exp(rng.normal(0, 0.05, len(ENGINEERED_RATIOS)))
    return DomainNode("engineered", r, lognormal_null(center=20, log_sd=0.8),
                      is_self_organizing=False,
                      source="memory/filesystem/DB/highway design parameters (illustrative)")


def classification_node(seed: int = 0) -> DomainNode:
    rng = np.random.default_rng(seed)
    r = np.array(CLASSIFICATION_RATIOS, float) * np.exp(rng.normal(0, 0.05, len(CLASSIFICATION_RATIOS)))
    return DomainNode("classification", r, lognormal_null(center=12, log_sd=0.7),
                      is_self_organizing=False,
                      source="taxonomy / Dewey / LoC ratios (illustrative)")
