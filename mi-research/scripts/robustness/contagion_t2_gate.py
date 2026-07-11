#!/usr/bin/env python3
"""
Contagion — Test 2 (THE GATE): split the dense erosion curve by crisis origin.
Recompute spread (structure_AUC - wealth_AUC) per epoch for all / domestic-only /
external-only crises, using the committed curve machinery (V-Dem rule-of-law, log
Maddison GDP, 25y window). Frozen spec: docs/CONTAGION_PREREGISTRATION.md.

Read-only; writes data/robustness/contagion/t2_split_curve.json.
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "robustness"))
sys.path.insert(0, str(ROOT / "scripts" / "historical"))
import erosion_component_B as B  # noqa: E402  (dense_curve internals: VDEM, LONGRUN, auc)
from esi_tests import auc_roc  # noqa: E402

CLASS = ROOT / "data" / "robustness" / "contagion" / "crisis_classification.json"
OUT = ROOT / "data" / "robustness" / "contagion" / "t2_split_curve.json"
WINDOW = 25
START, STOP, STEP = 1816, 1996, 10


def _ser(v):
    return json.loads(v) if isinstance(v, str) else v


def origin_onset_sets(field):
    """iso -> {'all':set, 'domestic':set, 'external':set} of onset YEARS."""
    data = json.loads(CLASS.read_text())[field]
    sets = {}
    for key, origins in data.items():
        iso, y = key.split("|"); y = int(y)
        d = sets.setdefault(iso, {"all": set(), "domestic": set(), "external": set()})
        d["all"].add(y)
        if "domestic" in origins:
            d["domestic"].add(y)
        if "external" in origins:
            d["external"].add(y)
    return sets


def curve(onset_sets, kind):
    """Replicate dense_curve, but onset label = origin-specific onset in window."""
    vdem = json.loads(B.VDEM.read_text())
    longrun = json.loads(B.LONGRUN.read_text())
    rol = {i: _ser(v["rol"]) for i, v in vdem.items() if "rol" in v}
    gdp = {i: {int(y): val for y, val in _ser(v["P4_gdp"]).items()}
           for i, v in longrun.items() if "P4_gdp" in v}
    pts = []
    for y in range(START, STOP + 1, STEP):
        rows = []
        for iso in set(rol) & set(gdp):
            if iso.startswith("OWID"):
                continue
            r = rol[iso].get(str(y)); g0 = gdp[iso].get(y)
            if r is None or g0 is None or g0 <= 0:
                continue
            ys = onset_sets.get(iso, {}).get(kind, set())
            label = 1 if any(y <= oy <= y + WINDOW for oy in ys) else 0
            rows.append((-float(r), -math.log(g0), label))
        labels = [x[2] for x in rows]
        if len(rows) < 12 or len(set(labels)) < 2:
            pts.append({"year": y, "n": len(rows), "n_pos": sum(labels),
                        "spread": None, "note": "insufficient"})
            continue
        s = auc_roc([x[0] for x in rows], labels)
        w = auc_roc([x[1] for x in rows], labels)
        pts.append({"year": y, "n": len(rows), "n_pos": sum(labels),
                    "onset_rate": round(sum(labels) / len(rows), 3),
                    "struct_auc": round(float(s), 4), "wealth_auc": round(float(w), 4),
                    "spread": round(float(s - w), 4)})
    return pts


def trend(pts):
    xs = [p["year"] for p in pts if p["spread"] is not None]
    ys = [p["spread"] for p in pts if p["spread"] is not None]
    if len(xs) < 3:
        return None
    r = stats.linregress(xs, ys)
    return {"slope": float(r.slope), "pearson_r": float(r.rvalue), "p": float(r.pvalue),
            "n_epochs": len(xs), "delta": round(ys[-1] - ys[0], 4),
            "mean_spread": round(float(np.mean(ys)), 4)}


def external_share(field):
    data = json.loads(CLASS.read_text())[field]
    per_epoch = {}
    for y0 in range(START, STOP + 1, STEP):
        dom = ext = 0
        for key, origins in data.items():
            _, y = key.split("|"); y = int(y)
            if y0 <= y <= y0 + WINDOW:
                if "domestic" in origins:
                    dom += 1
                if "external" in origins:
                    ext += 1
        tot = dom + ext
        per_epoch[y0] = {"domestic": dom, "external": ext,
                         "external_share": round(ext / tot, 3) if tot else None}
    return per_epoch


def run(field):
    sets = origin_onset_sets(field)
    res = {}
    for kind in ["all", "domestic", "external"]:
        pts = curve(sets, kind)
        res[kind] = {"curve": pts, "trend": trend(pts)}
    return res


def gate_verdict(prim):
    ta = prim["all"]["trend"]; td = prim["domestic"]["trend"]; te = prim["external"]["trend"]
    sa, sd, se = ta["slope"], td["slope"], te["slope"]
    flatter = abs(sd) <= 0.5 * abs(sa)
    dom_ge_ext = sd >= se
    if flatter and dom_ge_ext:
        return "PASS", {"domestic_flatter_half_all": flatter, "domestic_ge_external": dom_ge_ext}
    if (abs(sd) < abs(sa)) and dom_ge_ext:
        return "PARTIAL", {"domestic_flatter_than_all": abs(sd) < abs(sa), "domestic_ge_external": dom_ge_ext}
    if sd < se:  # domestic erodes MORE than external
        return "FAIL_domestic_worse", {}
    return "FAIL_similar", {"slope_all": sa, "slope_dom": sd, "slope_ext": se}


def main():
    prim = run("classification_primary")
    verdict, detail = gate_verdict(prim)
    out = {"test": "T2_gate_split_erosion_curve",
           "primary": prim,
           "external_share_by_epoch": external_share("classification_primary"),
           "sensitivity_S1_type4_external": run("classification_S1_type4_external"),
           "sensitivity_S2_type1_excluded": run("classification_S2_type1_excluded"),
           "verdict": verdict, "verdict_detail": detail}
    OUT.write_text(json.dumps(out, indent=1))

    def show(tag, block):
        line = "  ".join(f"{p['year']}:{p['spread'] if p['spread'] is not None else 'NA'}"
                         for p in block["curve"])
        t = block["trend"]
        print(f"  {tag}: {line}")
        if t:
            print(f"      slope={t['slope']:+.6f} r={t['pearson_r']:+.3f} p={t['p']:.3f} "
                  f"Δ={t['delta']:+.4f} mean={t['mean_spread']:+.4f} (n={t['n_epochs']})")

    print("=== TEST 2 GATE — erosion curve split by crisis origin (primary) ===")
    show("ALL crises (repro F7)", prim["all"])
    show("DOMESTIC-origin only ", prim["domestic"])
    show("EXTERNAL-origin only ", prim["external"])
    print("\nexternal-origin share of onsets by epoch:")
    es = out["external_share_by_epoch"]
    print("  " + "  ".join(f"{y}:{es[y]['external_share']}" for y in sorted(es)))
    print("\nsensitivity S1 (type4->external): dom slope="
          f"{out['sensitivity_S1_type4_external']['domestic']['trend']['slope']:+.6f} "
          f"ext slope={out['sensitivity_S1_type4_external']['external']['trend']['slope']:+.6f}")
    print("sensitivity S2 (type1 excluded): dom slope="
          f"{out['sensitivity_S2_type1_excluded']['domestic']['trend']['slope']:+.6f} "
          f"ext slope={out['sensitivity_S2_type1_excluded']['external']['trend']['slope']:+.6f}")
    print(f"\n>>> VERDICT: {verdict}  {detail}")


if __name__ == "__main__":
    main()
