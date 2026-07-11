"""
Ingest BioDiv-3DTrees GraphML skeletons -> per-tree Horton Rb -> rb_trees.json.

    python ingest_trees.py --graph-dir /path/to/Graph

Data source (free, no login, CC BY 4.0): BioDiv-3DTrees, Goettingen Research
Online, doi:10.25625/8PB1IF -> file `Graphs.tar.zst` -> `Graph/*.graphml`.
Download (the runner streams it; here we read already-extracted GraphML):
    curl -sL "https://data.goettingen-research-online.de/api/access/datafile/142310" \
      | zstd -dc | tar -x      # -> ./Graph/*.graphml

Each GraphML: nodes carry pos_x/y/z + radius; undirected edges. We root at the
trunk base (minimum z), build a rooted tree, and Strahler-order it with the SAME
horton.measure_basin used for rivers and neurons.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import xml.etree.ElementTree as ET

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.dirname(HERE)
RESULTS = os.path.join(CENSUS, "results")
sys.path.insert(0, os.path.join(CENSUS, "..", "natural-systems", "rivers"))
from horton import measure_basin  # noqa: E402

NS = "{http://graphml.graphdrawing.org/xmlns}"


def _parse(path):
    root = ET.parse(path).getroot()
    g = root.find(f"{NS}graph")
    zkey = next(k.get("id") for k in root.findall(f"{NS}key") if k.get("attr.name") == "pos_z")
    nodes = {}
    for n in g.findall(f"{NS}node"):
        zs = [d.text for d in n.findall(f"{NS}data") if d.get("key") == zkey]
        nodes[n.get("id")] = float(zs[0]) if zs else 0.0
    edges = [(e.get("source"), e.get("target")) for e in g.findall(f"{NS}edge")]
    return nodes, edges


def tree_rb(path, min_orders_floor=3):
    nodes, edges = _parse(path)
    if len(nodes) < 6:
        return None
    adj = {n: [] for n in nodes}
    for a, b in edges:
        if a in adj and b in adj:
            adj[a].append(b)
            adj[b].append(a)
    root = min(nodes, key=lambda n: nodes[n])          # trunk base = lowest z
    idx = {n: i for i, n in enumerate(nodes)}
    downstream = {idx[root]: -1}
    seen = {root}
    stack = [root]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                downstream[idx[v]] = idx[u]
                stack.append(v)
    if len(seen) != len(nodes):                        # disconnected skeleton
        return None
    try:
        m = measure_basin(downstream, min_orders=min_orders_floor)
    except ValueError:
        return None
    return round(float(m.rb), 6), int(m.max_order)


def ingest(graph_dir: str, limit: int = 0):
    files = sorted(glob.glob(os.path.join(graph_dir, "*.graphml")))
    if limit:
        files = files[:limit]
    recs, fails = [], 0
    for i, f in enumerate(files):
        try:
            r = tree_rb(f)
        except Exception:                              # noqa: BLE001
            r = None
        if r is None:
            fails += 1
        else:
            recs.append(list(r))
        if (i + 1) % 100 == 0:
            print(f"  {i+1}/{len(files)} trees, {len(recs)} measured", flush=True)
    arr = np.array(recs, dtype=float)
    os.makedirs(RESULTS, exist_ok=True)
    payload = {
        "source": "BioDiv-3DTrees TLS skeletons (Goettingen, doi:10.25625/8PB1IF, CC BY 4.0)",
        "n_trees": len(recs), "n_failed": fails,
        "geom_rb": float(np.exp(np.log(arr[arr[:, 0] > 0, 0]).mean())) if recs else None,
        "fields": ["rb", "max_order"], "records": recs,
    }
    with open(os.path.join(RESULTS, "rb_trees.json"), "w") as f:
        json.dump(payload, f)
    print(f"\nwrote rb_trees.json: {len(recs)} trees, geom Rb={payload['geom_rb']:.3f}"
          if recs else "no trees measured")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph-dir", default="/tmp/trees_probe/ext/Graph")
    ap.add_argument("--limit", type=int, default=0)
    ingest(ap.parse_args().graph_dir, ap.parse_args().limit)
