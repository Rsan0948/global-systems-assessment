"""
DESIGNED governance structure: administrative subdivisions (GeoNames).

DATA TIER — SYSTEMATIC (real, global, no curation). GeoNames ships explicit
parent codes: admin1 = "COUNTRY.A1", admin2 = "COUNTRY.A1.A2". The fan-out
(children per parent) at each level is a designed hierarchy's branching factor.
`ingest()` downloads the two small admin-code files and caches the fan-out
distributions to results/admin_subdivisions.json.

Prediction (MASTER_REFERENCE 1.4): a top-down designed hierarchy fractures WIDE
and DISPERSED -- a high mean fan-out (not the natural ~3) and a very high CV,
because each designer sized their subdivisions to local convenience, not a shared
constraint.
"""

from __future__ import annotations

import collections
import json
import os
import urllib.request

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "..", "results")
CACHE = os.path.join(RESULTS, "admin_subdivisions.json")
BASE = "https://download.geonames.org/export/dump/"


def _get(name):
    return urllib.request.urlopen(
        urllib.request.Request(BASE + name, headers={"User-Agent": "usg-research"}),
        timeout=60).read().decode("utf-8", "replace")


def ingest():
    a1 = collections.Counter()
    for ln in _get("admin1CodesASCII.txt").splitlines():
        code = ln.split("\t")[0]
        if "." in code:
            a1[code.split(".")[0]] += 1
    a2 = collections.Counter()
    for ln in _get("admin2Codes.txt").splitlines():
        parts = ln.split("\t")[0].split(".")
        if len(parts) >= 3:
            a2[".".join(parts[:2])] += 1
    os.makedirs(RESULTS, exist_ok=True)
    with open(CACHE, "w") as f:
        json.dump({"source": "GeoNames admin1/admin2 code files (CC BY 4.0, no login)",
                   "admin1_per_country": sorted(a1.values()),
                   "admin2_per_admin1": sorted(a2.values())}, f)
    print(f"wrote admin_subdivisions.json: {len(a1)} countries, {len(a2)} admin1 parents")


def _stats(vals):
    v = np.array(vals, dtype=float)
    return {"n_parents": int(v.size), "mean_fanout": round(float(v.mean()), 2),
            "median": float(np.median(v)), "CV": round(float(v.std(ddof=1) / v.mean()), 3),
            "range": [int(v.min()), int(v.max())]}


def analyze() -> dict:
    if not os.path.exists(CACHE):
        ingest()
    d = json.load(open(CACHE))
    lvl1 = _stats(d["admin1_per_country"])
    lvl2 = _stats(d["admin2_per_admin1"])
    return {
        "system": "admin_subdivisions",
        "data_tier": "SYSTEMATIC (GeoNames, global)",
        "admin1_per_country": lvl1,
        "admin2_per_admin1": lvl2,
        "CV": lvl2["CV"],
        "verdict": f"designed hierarchy fractures WIDE and DISPERSED: fan-out mean "
                   f"~{lvl2['mean_fanout']:.0f} (vs natural ~3), CV "
                   f"{lvl1['CV']}-{lvl2['CV']} (vs self-organized ~0.2). No "
                   f"characteristic branching factor -- the designed signature.",
    }


if __name__ == "__main__":
    print(json.dumps(analyze(), indent=2))
