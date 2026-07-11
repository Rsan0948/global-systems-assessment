#!/usr/bin/env python3
"""
Inequality — Tests 3-6 (post-gate characterization; arm A passed, arm B failed).
  T3 mature-state inequality split; T4 F10-vs-F12 partial-correlation resolution;
  T5 long-run deep subset; T6 EXPLORATORY P6 distribution pillar.
Frozen spec: docs/INEQUALITY_PREREGISTRATION.md. Read-only.
"""
from __future__ import annotations
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "robustness"))
sys.path.insert(0, str(ROOT / "scripts" / "historical"))
from esi_tests import auc_roc  # noqa: E402
import erosion_component_B as B  # noqa: E402
import decoupling_panel as dp  # noqa: E402
from mi import panel  # noqa: E402
from mi.scoring import calculate_pillar_scores  # noqa: E402

HOLDOUT = ROOT / "data/robustness/temporal_holdout_panel.json"
CLASS = ROOT / "data/robustness/contagion/crisis_classification.json"
INEQ = ROOT / "data/robustness/inequality/inequality.json"
FORM = ROOT / "data/robustness/formation/state_formation.json"
OUT = ROOT / "data/robustness/inequality/t3_t6.json"


def ineq_at(series, iso, year, back=4):
    d = series.get(iso)
    if not d:
        return None
    for dy in range(0, back + 1):
        for y in (year - dy, year + dy):
            if str(y) in d:
                return d[str(y)]
    return None


def dom_years():
    data = json.loads(CLASS.read_text())["classification_primary"]
    out = defaultdict(set)
    for key, origins in data.items():
        iso, y = key.split("|")
        if "domestic" in origins:
            out[iso].add(int(y))
    return out


def mature_isos():
    form = json.loads(FORM.read_text())
    classes = form.get("states", form)
    return {iso for iso, v in classes.items()
            if (v.get("group") if isinstance(v, dict) else v) == "mature"}


def auc_safe(sig, y):
    if len(set(y)) < 2 or len(sig) < 8:
        return None
    return round(float(auc_roc(sig, y)), 3)


def test3(top10, dom, mature):
    holdout = json.loads(HOLDOUT.read_text())["windows"]
    res = {}
    for win, rows in holdout.items():
        origin = int(win)
        recs = []
        for r in rows:
            if r["P1"] is None or r["iso"] not in mature:
                continue
            iq = ineq_at(top10, r["iso"], origin)
            if iq is None:
                continue
            recs.append({"iso": r["iso"], "P1": r["P1"], "ineq": iq,
                         "dom": 1 if any(origin <= oy <= 2024 for oy in dom.get(r["iso"], set())) else 0})
        if len(recs) < 10:
            res[win] = {"n": len(recs), "note": "insufficient mature+ineq"}
            continue
        med = float(np.median([r["ineq"] for r in recs]))
        low = [r for r in recs if r["ineq"] <= med]
        high = [r for r in recs if r["ineq"] > med]
        def grp(g):
            y = [r["dom"] for r in g]
            return {"n": len(g), "n_pos": sum(y), "mean_ineq": round(float(np.mean([r["ineq"] for r in g])), 1),
                    "negP1_auc": auc_safe([1 - r["P1"] for r in g], y)}
        res[win] = {"median_top10": round(med, 1), "n_mature": len(recs),
                    "low_ineq": grp(low), "high_ineq": grp(high),
                    "low_iso": sorted(r["iso"] for r in low), "high_iso": sorted(r["iso"] for r in high)}
    return res


def test4(top10, dom):
    """Raw vs inequality-partialled P1<->domestic-stability corr, holdout windows."""
    holdout = json.loads(HOLDOUT.read_text())["windows"]
    res = {}
    for win, rows in holdout.items():
        origin = int(win)
        recs = []
        for r in rows:
            if r["P1"] is None:
                continue
            iq = ineq_at(top10, r["iso"], origin)
            if iq is None:
                continue
            stab = 0 if any(origin <= oy <= 2024 for oy in dom.get(r["iso"], set())) else 1
            recs.append((r["P1"], iq, stab))
        if len(recs) < 15:
            res[win] = {"n": len(recs), "note": "insufficient"}
            continue
        P1 = np.array([r[0] for r in recs]); IQ = np.array([r[1] for r in recs])
        ST = np.array([r[2] for r in recs], float)
        raw = stats.pearsonr(P1, ST)
        # partial corr of P1,ST controlling IQ
        def resid(a, b):
            s = stats.linregress(b, a)
            return a - (s.intercept + s.slope * b)
        pr = stats.pearsonr(resid(P1, IQ), resid(ST, IQ))
        res[win] = {"n": len(recs),
                    "raw_P1_stability_r": round(float(raw.statistic), 3),
                    "partial_P1_stability_given_ineq_r": round(float(pr.statistic), 3)}
    return res


def test5(top10):
    """Long-run: Finding-7 all-crisis spread vs deep-subset mean top10 (descriptive)."""
    split = json.loads(ROOT.joinpath("data/robustness/contagion/t2_split_curve.json").read_text())
    all_curve = {p["year"]: p["spread"] for p in split["primary"]["all"]["curve"] if p["spread"] is not None}
    deep = ["USA", "FRA", "SWE", "IND", "RUS", "GBR", "DEU"]
    epochs = {}
    for y in sorted(all_curve):
        vals = [ineq_at(top10, iso, y, 3) for iso in deep]
        vals = [v for v in vals if v is not None]
        epochs[y] = {"all_spread": all_curve[y],
                     "deep_top10_mean": round(float(np.mean(vals)), 2) if vals else None,
                     "n": len(vals)}
    shared = [(e["all_spread"], e["deep_top10_mean"]) for e in epochs.values()
              if e["deep_top10_mean"] is not None and e["n"] >= 3]
    corr = None
    if len(shared) >= 4:
        pr = stats.pearsonr([s[1] for s in shared], [s[0] for s in shared])
        corr = {"n": len(shared), "pearson_r": round(float(pr.statistic), 3), "p": round(float(pr.pvalue), 4)}
    return {"epochs": epochs, "correlation": corr, "note": "deep subset 3-7 countries; underpowered"}


def test6(top10, dom):
    """EXPLORATORY P6 = 1 - normalized top10 at 2024; 6-pillar vs 5-pillar domestic pred."""
    canon = panel._canonical()
    # 2024 top10 across universe for normalization
    vals = {iso: ineq_at(top10, iso, 2024, 6) for iso in canon}
    have = {iso: v for iso, v in vals.items() if v is not None}
    lo, hi = min(have.values()), max(have.values())
    recs = []
    for iso in canon:
        if iso not in have:
            continue
        ind = panel.indicators_for(iso, 2024)
        if not ind:
            continue
        try:
            pil = calculate_pillar_scores(ind)
        except Exception:
            continue
        ps = [pil[k] for k in ("P1", "P2", "P3", "P4", "P5") if pil.get(k) is not None]
        if len(ps) < 3:
            continue
        mi5 = float(np.mean(ps))
        p6 = 1 - (have[iso] - lo) / (hi - lo)
        mi6 = float(np.mean(ps + [p6]))
        # recent domestic instability outcome: domestic onset in [2010,2024]
        dcrisis = 1 if any(2010 <= oy <= 2024 for oy in dom.get(iso, set())) else 0
        recs.append({"iso": iso, "mi5": mi5, "mi6": mi6, "p6": round(p6, 3), "dom": dcrisis})
    y = [r["dom"] for r in recs]
    auc5 = auc_safe([-r["mi5"] for r in recs], y)   # lower MI -> more crisis
    auc6 = auc_safe([-r["mi6"] for r in recs], y)
    movers = sorted(recs, key=lambda r: r["mi6"] - r["mi5"])
    watch = {r["iso"]: {"mi5": round(r["mi5"], 3), "mi6": round(r["mi6"], 3),
                        "delta": round(r["mi6"] - r["mi5"], 3), "p6": r["p6"]}
             for r in recs if r["iso"] in ("USA", "SWE", "NOR", "DNK", "GBR", "DEU", "CHN", "ARE", "SAU", "ZAF")}
    return {"n": len(recs), "n_pos": sum(y), "auc_5pillar": auc5, "auc_6pillar": auc6,
            "biggest_drops_with_p6": [(m["iso"], round(m["mi6"] - m["mi5"], 3)) for m in movers[:6]],
            "biggest_rises_with_p6": [(m["iso"], round(m["mi6"] - m["mi5"], 3)) for m in movers[-6:]],
            "watchlist": watch, "caveat": "EXPLORATORY ONLY — not a confirmed improvement; P6 not adopted."}


def main():
    ineqdata = json.loads(INEQ.read_text())
    top10 = ineqdata["top10"]
    dom = dom_years(); mature = mature_isos()
    out = {"gate_status": "arm A passed (bivariate), arm B failed (reversed) — partial, cautionary",
           "T3_mature_split": test3(top10, dom, mature),
           "T4_partial_correlation": test4(top10, dom),
           "T5_longrun": test5(top10),
           "T6_exploratory_P6": test6(top10, dom)}
    OUT.write_text(json.dumps(out, indent=1))

    print("=== TEST 3 — inequality split WITHIN mature states (neg-P1 AUC on domestic crises) ===")
    for win, w in out["T3_mature_split"].items():
        if "note" in w:
            print(f"  {win}: {w['note']} (n={w['n']})"); continue
        lo, hi = w["low_ineq"], w["high_ineq"]
        print(f"  {win} (median top10={w['median_top10']}, n_mature={w['n_mature']}):")
        print(f"    LOW-ineq  n={lo['n']} pos={lo['n_pos']} meanIneq={lo['mean_ineq']} negP1_auc={lo['negP1_auc']}")
        print(f"    HIGH-ineq n={hi['n']} pos={hi['n_pos']} meanIneq={hi['mean_ineq']} negP1_auc={hi['negP1_auc']}")

    print("\n=== TEST 4 — raw vs inequality-partialled P1<->domestic-stability corr ===")
    for win, w in out["T4_partial_correlation"].items():
        if "note" in w:
            print(f"  {win}: {w['note']}"); continue
        print(f"  {win}: raw r={w['raw_P1_stability_r']:+.3f} | partial(|ineq) r={w['partial_P1_stability_given_ineq_r']:+.3f} (n={w['n']})")

    print("\n=== TEST 5 — long-run all-spread vs deep-subset top10 ===")
    print(f"  correlation: {out['T5_longrun']['correlation']} ({out['T5_longrun']['note']})")

    print("\n=== TEST 6 — EXPLORATORY P6 (2024) ===")
    t6 = out["T6_exploratory_P6"]
    print(f"  n={t6['n']} pos={t6['n_pos']} | AUC 5-pillar={t6['auc_5pillar']} vs 6-pillar={t6['auc_6pillar']}")
    print(f"  biggest drops w/ P6: {t6['biggest_drops_with_p6']}")
    print(f"  biggest rises w/ P6: {t6['biggest_rises_with_p6']}")
    print(f"  watchlist: {json.dumps(t6['watchlist'])}")


if __name__ == "__main__":
    main()
