"""
Core measurement for Study 2C: Strahler stream ordering and the Horton
bifurcation ratio (Rb) of a drainage network.

A drainage network is represented as a directed tree over integer node ids:
each node flows to exactly one downstream node, the outlet flows to -1
(sentinel, no downstream), and source nodes are the leaves. This is the
topology that HydroSHEDS / NHD reach tables encode (each reach has a
"next-downstream" id), so the same functions consume real data and
synthetic data without modification.

Definitions
-----------
Strahler order:
    - a source (leaf) has order 1;
    - an internal node whose children's maximum order m is shared by >= 2
      children has order m + 1; otherwise it has order m.

A "stream of order w" is a maximal path of consecutive same-order links. The
number of order-w streams N_w equals the number of nodes that *begin* a new
order-w stream, i.e. a leaf with w == 1, or an internal node of order w none
of whose children also has order w (so the order was newly formed there).

Horton bifurcation ratio:
    Rb estimated from the regression of ln(N_w) on order w:
        ln(N_w) = a - w * ln(Rb)   =>   Rb = exp(-slope).
    Requires at least `min_orders` distinct orders to be defined.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

import numpy as np


@dataclass
class BasinMeasurement:
    """Result of measuring one basin."""
    rb: float                      # estimated Horton bifurcation ratio
    max_order: int                 # highest Strahler order present
    stream_counts: dict[int, int]  # N_w per order w
    n_nodes: int
    r_squared: float               # fit quality of the ln(N_w)~w regression


def strahler_orders(downstream: dict[int, int]) -> dict[int, int]:
    """Compute Strahler order for every node.

    Parameters
    ----------
    downstream : mapping node_id -> downstream node_id. The outlet maps to a
        sentinel value (-1) that is not itself a key. Every other node's
        downstream value must be a key in the mapping (or the sentinel).

    Returns
    -------
    dict node_id -> Strahler order (>= 1).
    """
    children: dict[int, list[int]] = defaultdict(list)
    nodes = set(downstream.keys())
    for n, d in downstream.items():
        if d in nodes:
            children[d].append(n)
        elif d != -1:
            raise ValueError(f"node {n} flows to unknown node {d}")

    order: dict[int, int] = {}

    # Iterative post-order traversal (avoids recursion limits on big basins).
    # Process a node only after all its children are ordered.
    indeg = {n: len(children[n]) for n in nodes}
    ready = [n for n in nodes if indeg[n] == 0]  # leaves / sources
    pending_children_done: dict[int, int] = defaultdict(int)

    while ready:
        n = ready.pop()
        kids = children.get(n, [])
        if not kids:
            order[n] = 1
        else:
            child_orders = [order[c] for c in kids]
            m = max(child_orders)
            order[n] = m + 1 if child_orders.count(m) >= 2 else m
        d = downstream[n]
        if d in nodes:
            pending_children_done[d] += 1
            if pending_children_done[d] == indeg[d]:
                ready.append(d)

    if len(order) != len(nodes):
        raise ValueError("graph is not a tree (cycle or disconnected node)")
    return order


def stream_counts(downstream: dict[int, int], order: dict[int, int]) -> dict[int, int]:
    """Count the number of streams N_w at each Strahler order w."""
    children: dict[int, list[int]] = defaultdict(list)
    nodes = set(downstream.keys())
    for n, d in downstream.items():
        if d in nodes:
            children[d].append(n)

    counts: dict[int, int] = defaultdict(int)
    for n in nodes:
        w = order[n]
        kids = children.get(n, [])
        if not kids:                                  # source: starts order-1 stream
            counts[1] += 1
        elif all(order[c] != w for c in kids):        # order newly formed here
            counts[w] += 1
    return dict(counts)


def horton_rb(stream_counts_by_order: dict[int, int], min_orders: int = 3) -> tuple[float, float]:
    """Estimate Rb from N_w via the ln(N_w) ~ order regression.

    Returns (Rb, r_squared). Raises ValueError if fewer than `min_orders`
    orders are present (Rb is undefined for such basins and they are excluded
    per the pre-registration).
    """
    orders = sorted(stream_counts_by_order)
    if len(orders) < min_orders:
        raise ValueError(f"need >= {min_orders} orders, got {len(orders)}")
    w = np.array(orders, dtype=float)
    y = np.log(np.array([stream_counts_by_order[o] for o in orders], dtype=float))
    slope, intercept = np.polyfit(w, y, 1)
    yhat = slope * w + intercept
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return float(np.exp(-slope)), r2


def measure_basin(downstream: dict[int, int], min_orders: int = 3) -> BasinMeasurement:
    """Full measurement pipeline for one basin's downstream-link table."""
    order = strahler_orders(downstream)
    counts = stream_counts(downstream, order)
    rb, r2 = horton_rb(counts, min_orders=min_orders)
    return BasinMeasurement(
        rb=rb,
        max_order=max(order.values()),
        stream_counts=counts,
        n_nodes=len(downstream),
        r_squared=r2,
    )
