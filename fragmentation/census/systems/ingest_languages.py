"""
Ingest Glottolog language-family trees -> per-family Horton Rb -> rb_languages.json.

    python ingest_languages.py

Data (free, no login, CC BY 4.0): glottolog-cldf `cldf/values.csv`. Each languoid
has a `classification` value = its ancestry path of glottocodes (root family ...
immediate parent). We rebuild the full phylogeny, then Strahler-order each family
tree with the SAME horton.measure_basin used for rivers/neurons/trees.
"""

from __future__ import annotations

import csv
import io
import json
import os
import sys
import urllib.request

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.dirname(HERE)
RESULTS = os.path.join(CENSUS, "results")
sys.path.insert(0, os.path.join(CENSUS, "..", "natural-systems", "rivers"))
from horton import measure_basin  # noqa: E402

URL = "https://raw.githubusercontent.com/glottolog/glottolog-cldf/master/cldf/values.csv"
UA = {"User-Agent": "universalsystemgrade-research"}
PRIMARY_MIN_ORDERS = 4


def _fetch_classifications():
    raw = urllib.request.urlopen(urllib.request.Request(URL, headers=UA), timeout=120).read()
    rows = csv.DictReader(io.StringIO(raw.decode("utf-8", "replace")))
    cls = {}
    for r in rows:
        if r["Parameter_ID"] == "classification":
            cls[r["Language_ID"]] = r["Value"]
    return cls


def _build_forest(cls: dict):
    """parent[child]=parent_glottocode (root family -> None); families = roots."""
    parent = {}
    all_nodes = set()
    for lid, path in cls.items():
        toks = [t for t in path.replace(" ", "/").split("/") if t]
        all_nodes.add(lid)
        parent[lid] = toks[-1] if toks else None
        # chain the ancestry path itself so internal nodes exist & are linked
        chain = toks + [lid]
        for i in range(1, len(chain)):
            all_nodes.add(chain[i - 1])
            parent.setdefault(chain[i], chain[i - 1])
        if toks:
            all_nodes.add(toks[0])
            parent.setdefault(toks[0], None)
    roots = sorted({n for n in all_nodes if parent.get(n) is None})
    children = {}
    for c, p in parent.items():
        if p is not None:
            children.setdefault(p, []).append(c)
    return parent, children, roots


def _family_rb(root, children, min_orders_floor=3):
    """Strahler Rb for one family subtree (downstream = parent toward root)."""
    nodes = []
    stack = [root]
    while stack:
        u = stack.pop()
        nodes.append(u)
        stack.extend(children.get(u, []))
    if len(nodes) < 6:
        return None
    idx = {n: i for i, n in enumerate(nodes)}
    downstream = {idx[root]: -1}
    for n in nodes:
        if n != root:
            # parent is the node whose children include n; reconstruct via children map
            pass
    # build downstream from children map
    for p, kids in children.items():
        if p in idx:
            for k in kids:
                if k in idx:
                    downstream[idx[k]] = idx[p]
    if len(downstream) != len(nodes):
        return None
    try:
        m = measure_basin(downstream, min_orders=min_orders_floor)
    except ValueError:
        return None
    return round(float(m.rb), 6), int(m.max_order)


def ingest():
    print("fetching Glottolog classifications ...", flush=True)
    cls = _fetch_classifications()
    print(f"  {len(cls)} languoids with classification", flush=True)
    parent, children, roots = _build_forest(cls)
    print(f"  {len(roots)} root families", flush=True)
    recs = []
    for r in roots:
        out = _family_rb(r, children)
        if out is not None:
            recs.append(list(out))
    arr = np.array(recs, dtype=float)
    os.makedirs(RESULTS, exist_ok=True)
    payload = {
        "source": "Glottolog (glottolog-cldf values.csv classification, CC BY 4.0)",
        "n_families_measured": len(recs),
        "geom_rb": float(np.exp(np.log(arr[arr[:, 0] > 0, 0]).mean())) if recs else None,
        "fields": ["rb", "max_order"], "records": recs,
    }
    with open(os.path.join(RESULTS, "rb_languages.json"), "w") as f:
        json.dump(payload, f)
    print(f"\nwrote rb_languages.json: {len(recs)} families, geom Rb="
          f"{payload['geom_rb']:.3f}" if recs else "no families measured", flush=True)


if __name__ == "__main__":
    ingest()
