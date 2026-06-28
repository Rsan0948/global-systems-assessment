"""
Census system: LINUX DISTRIBUTIONS (real data) -- self-organized SOFTWARE control.

Distros fork permissionlessly (no central authority over the family tree), so the
distro genealogy is a self-organized system. Observable: Horton-Strahler Rb per
distro FAMILY (Debian, Slackware, Red Hat, ...). Tests whether permissionless
software lineage also lands in the concentrated band.

Data: GLDT `ldt.csv` (github.com/FabioLolix/LinuxTimeline, open) -- one CSV with
an explicit Parent column. `ingest_linux.py` caches results/rb_linux.json.
"""

from __future__ import annotations

import csv
import io
import json
import os
import urllib.request

import numpy as np

import treekit

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "..", "results")
URL = "https://raw.githubusercontent.com/FabioLolix/LinuxTimeline/master/ldt.csv"
TAG = "linux"
SIZE_RANGE = (6, 120)
MIN_ORDERS = 3                      # distro families are shallower than rivers


def ingest():
    raw = urllib.request.urlopen(
        urllib.request.Request(URL, headers={"User-Agent": "usg-research"}), timeout=40
    ).read().decode("utf-8", "replace")
    parent = {}
    for row in csv.reader(io.StringIO(raw)):
        if len(row) < 4 or row[0] != "N":
            continue
        name, par = row[1].strip(), row[3].strip()
        if not name:
            continue
        parent[name] = par if par else None
    # ensure named parents exist as nodes (roots)
    for p in list(parent.values()):
        if p and p not in parent:
            parent[p] = None
    recs = treekit.rb_per_root(parent, min_orders_floor=MIN_ORDERS)
    arr = np.array(recs, dtype=float)
    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "rb_linux.json"), "w") as f:
        json.dump({"source": "GLDT ldt.csv (Linux distro genealogy, open)",
                   "n_families": len(recs),
                   "geom_rb": float(np.exp(np.log(arr[arr[:, 0] > 0, 0]).mean())) if recs else None,
                   "fields": ["rb", "max_order"], "records": recs}, f)
    print(f"wrote rb_linux.json: {len(recs)} families"
          + (f", geom Rb={np.exp(np.log(arr[arr[:,0]>0,0]).mean()):.3f}" if recs else ""))


def build_node(min_orders: int = MIN_ORDERS):
    return treekit.build_tree_node("linux_distros", TAG, SIZE_RANGE, min_orders,
                                   source=f"GLDT Linux distro genealogy (real); Horton Rb")


if __name__ == "__main__":
    ingest()
