#!/usr/bin/env python3
"""
Decoupling — Test 1 historical robustness: is the declining rule-of-law <-> log-GDP
coupling (1850->1970) a genuine decoupling, or a decolonization COMPOSITION artifact
(the 1970 anchor's sample doubles as post-colonial states enter)?

Re-runs the historical coupling on: (a) the FULL common set (baseline), (b) a
BALANCED set of polities present at ALL anchors, (c) MATURE states only
(state_formation.json). If the decline vanishes on (b)/(c), the one surviving
positive is composition, echoing Finding 9-A. Read-only.
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
VDEM = ROOT / "data/sources/vdem_longrun.json"
LONGRUN = ROOT / "data/sources/longrun_pillars.json"
FORM = ROOT / "data/robustness/formation/state_formation.json"
OUT = ROOT / "data/robustness/decoupling/t1_historical_robust.json"
ANCHORS = [1850, 1880, 1910, 1940, 1970]


def _ser(v):
    return json.loads(v) if isinstance(v, str) else v


def load():
    vdem = json.loads(VDEM.read_text())
    longrun = json.loads(LONGRUN.read_text())
    rol = {iso: _ser(v["rol"]) for iso, v in vdem.items() if "rol" in v}
    gdp = {iso: {int(y): val for y, val in _ser(v["P4_gdp"]).items()}
           for iso, v in longrun.items() if "P4_gdp" in v}
    return rol, gdp


def point(rol, gdp, iso, y):
    r = rol.get(iso, {}).get(str(y))
    g = gdp.get(iso, {}).get(y)
    if r is None or g is None or g <= 0:
        return None
    return r, math.log10(g)


def corr_at(rol, gdp, isos, y):
    xs, ys = [], []
    for iso in isos:
        p = point(rol, gdp, iso, y)
        if p:
            xs.append(p[0]); ys.append(p[1])
    if len(xs) < 5:
        return None
    r = stats.pearsonr(xs, ys)
    return {"n": len(xs), "r": round(float(r.statistic), 3), "R2": round(float(r.statistic ** 2), 3)}


def curve(rol, gdp, isos):
    per = {y: corr_at(rol, gdp, isos, y) for y in ANCHORS}
    valid = [(y, per[y]["r"]) for y in ANCHORS if per[y]]
    tr = stats.linregress([y for y, _ in valid], [r for _, r in valid]) if len(valid) >= 3 else None
    return {"per_anchor": per,
            "trend": ({"slope": round(float(tr.slope), 6), "p": round(float(tr.pvalue), 3)} if tr else None),
            "delta_r": (round(valid[-1][1] - valid[0][1], 3) if len(valid) >= 2 else None)}


def main():
    rol, gdp = load()
    universe = set(rol) & set(gdp)

    # (a) full common set per anchor (baseline; sample grows over time)
    full = curve(rol, gdp, universe)

    # (b) balanced: present (rol+gdp) at ALL anchors
    balanced = [iso for iso in universe
                if all(point(rol, gdp, iso, y) for y in ANCHORS)]
    bal = curve(rol, gdp, balanced)

    # (c) mature states only (Finding 9-A classification)
    mature = None
    if FORM.exists():
        form = json.loads(FORM.read_text())
        classes = form.get("states", form) if isinstance(form, dict) else {}
        mature_isos = {iso for iso, v in classes.items()
                       if (v.get("group") if isinstance(v, dict) else v) == "mature"}
        mature = {"n_mature_total": len(mature_isos),
                  **curve(rol, gdp, universe & mature_isos)}

    out = {"test": "T1_historical_robustness",
           "question": "does the 1850-1970 coupling decline survive constant/mature sample?",
           "full_common_set": full,
           "balanced_all_anchors": {"n_balanced": len(balanced), **bal},
           "mature_only": mature}
    OUT.write_text(json.dumps(out, indent=1))

    def show(tag, c):
        line = "  ".join(f"{y}:{(c['per_anchor'][y]['r'] if c['per_anchor'][y] else float('nan'))}"
                         f"(n{c['per_anchor'][y]['n'] if c['per_anchor'][y] else 0})" for y in ANCHORS)
        t = c["trend"]
        print(f"  {tag}: {line}")
        print(f"      trend slope={t['slope'] if t else 'na'} p={t['p'] if t else 'na'} Δr={c['delta_r']}")

    print("=== Test 1 historical robustness — coupling decline vs composition ===")
    show("FULL common set (grows) ", full)
    show(f"BALANCED n={len(balanced)} (constant)", bal)
    if mature:
        show(f"MATURE only (n≤{mature['n_mature_total']})    ", mature)


if __name__ == "__main__":
    main()
