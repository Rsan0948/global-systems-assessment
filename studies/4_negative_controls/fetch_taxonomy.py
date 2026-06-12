"""
REAL imposed-classification data (Study 4B): branching fan-out of the NCBI
Taxonomy tree (the standard machine-readable Linnaean hierarchy -- human-imposed
categories, the project's canonical imposed-classification control).

Downloads the free NCBI taxdump, parses nodes.dmp (tax_id, parent, rank), and
records the per-node fan-out (number of children) for every internal node that
is a genuine branching point (>=2 children) -- the imposed subdivision factor.
The theory predicts this disperses MUCH more than self-organizing systems: real
taxonomy fan-out ranges from 2 to hundreds (a genus with 1 vs 500 species).

Caches a fan-out summary + a capped per-node sample to
results/taxonomy_fanout.json. Raw taxdump (~75 MB) is git-ignored. Run:
    python fetch_taxonomy.py
"""

from __future__ import annotations

import json
import os
import tarfile
import urllib.request

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
DATA = os.path.join(HERE, "data")
TAXDUMP_URL = "https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz"
SOURCE = "NCBI Taxonomy taxdump (ftp.ncbi.nlm.nih.gov, public domain)"
SAMPLE_CAP = 4000          # capped per-rank sample stored in the cache


def download():
    os.makedirs(DATA, exist_ok=True)
    tgz = os.path.join(DATA, "taxdump.tar.gz")
    if not os.path.exists(tgz):
        urllib.request.urlretrieve(TAXDUMP_URL, tgz)
    nodes = os.path.join(DATA, "nodes.dmp")
    if not os.path.exists(nodes):
        with tarfile.open(tgz) as t:
            t.extract("nodes.dmp", DATA, filter="data")
    return nodes


def parse_fanout(nodes_path: str):
    """Return (child_count, rank) dicts keyed by tax_id."""
    child_count: dict[int, int] = {}
    rank: dict[int, str] = {}
    with open(nodes_path, encoding="utf-8") as f:
        for line in f:
            parts = line.split("\t|\t")
            tid = int(parts[0]); parent = int(parts[1]); rk = parts[2]
            rank[tid] = rk
            if parent != tid:                          # root is its own parent
                child_count[parent] = child_count.get(parent, 0) + 1
    return child_count, rank


def main():
    nodes_path = download()
    child_count, rank = parse_fanout(nodes_path)

    # fan-out at genuine branching points (>=2 children), overall and per parent-rank
    fanouts = np.array([c for c in child_count.values() if c >= 2], dtype=float)
    by_rank: dict[str, list[int]] = {}
    for tid, c in child_count.items():
        if c >= 2:
            by_rank.setdefault(rank.get(tid, "no rank"), []).append(c)

    rng = np.random.default_rng(0)
    sample = fanouts if fanouts.size <= SAMPLE_CAP else rng.choice(fanouts, SAMPLE_CAP, replace=False)
    rank_summary = {
        rk: {"n": len(v), "geom_mean": float(np.exp(np.log(v).mean())),
             "cv": float(np.std(v, ddof=1) / np.mean(v)), "max": int(max(v))}
        for rk, v in sorted(by_rank.items(), key=lambda kv: -len(kv[1]))[:8]
    }
    payload = {
        "source": SOURCE,
        "observable": "fan-out (children per internal node), branching points >=2",
        "n_branching_nodes": int(fanouts.size),
        "geom_mean_fanout": float(np.exp(np.log(fanouts).mean())),
        "cv_fanout": float(fanouts.std(ddof=1) / fanouts.mean()),
        "max_fanout": int(fanouts.max()),
        "by_parent_rank": rank_summary,
        "sample": [round(float(x), 3) for x in sample],
    }
    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "taxonomy_fanout.json"), "w") as f:
        json.dump(payload, f)
    print(f"taxonomy: {fanouts.size:,} branching nodes  geom-mean fanout="
          f"{payload['geom_mean_fanout']:.2f}  CV={payload['cv_fanout']:.2f}  "
          f"max={payload['max_fanout']}")
    for rk, s in rank_summary.items():
        print(f"  {rk:14s}: n={s['n']:>6}  geom={s['geom_mean']:.2f}  CV={s['cv']:.2f}  max={s['max']}")


if __name__ == "__main__":
    main()
