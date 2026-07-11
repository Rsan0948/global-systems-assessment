#!/usr/bin/env python3
"""
Component C — MEASUREMENT REGIME CHANGE (perception replaced function).  C1, C2.

Hypothesis: modern P1 uses WGI = *perceptions* of governance (expert surveys), a
laggier proxy for true institutional quality than the functional evidence used to
score the ancient corpus. If P1 is a noisier/laggier proxy, the temporal-holdout
signal degrades with no change in the structural relationship.

  C1  Rebuild the 2004-vintage MI with a REVEALED-OUTCOME P1 (tax %GDP, edu %GDP) via
      the Finding-1 substitution seam, run the same holdout, compare vs perception-P1.
  C2  Perception-lag: for 2010-2024 crisis countries, did functional indicators (tax)
      decline BEFORE WGI did?

Read-only w.r.t. scoring math (mutates only the flat indicator dict, exactly like
substitute.py). Writes data/robustness/decomposition/component_C.json.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "robustness"))

from mi.panel import iter_universe                 # noqa: E402
from mi.diagnostics import full_diagnostic         # noqa: E402
from prospective_freeze import predict             # noqa: E402  same frozen rule set
from substitute import pct_rank                    # noqa: E402
from esi_tests import auc_roc                       # noqa: E402

REVEALED = ROOT / "data/robustness/outcomes/p1_revealed_timeseries.json"
HOLDOUT = ROOT / "data/robustness/temporal_holdout_panel.json"
WGI = ROOT / "data/sources/wgi_full_panel.json"
ONSETS = ROOT / "data/robustness/historical/conflict_onsets.json"
OUT = ROOT / "data/robustness/decomposition/component_C.json"

P1_WGI = ["gov_effectiveness", "rule_of_law", "regulatory_quality"]


def nearest(series_iso, target, lo, hi):
    """value at the year in [lo,hi] closest to target (ties -> later year)."""
    cand = {y: v for y, v in series_iso.items() if lo <= y <= hi}
    if not cand:
        return None
    y = min(cand, key=lambda yy: (abs(yy - target), -yy))
    return cand[y], y


def revealed_pct_2004(series, target=2004, lo=2002, hi=2006):
    """{iso: percentile(0-100)} for one revealed series at 2004 vintage."""
    raw = {}
    for iso, s in series.items():
        s = {int(y): v for y, v in s.items()}
        got = nearest(s, target, lo, hi)
        if got is not None:
            raw[iso] = got[0]
    return pct_rank(raw), raw


def confusion(flags, labels):
    TP = sum(1 for f, l in zip(flags, labels) if f and l)
    FP = sum(1 for f, l in zip(flags, labels) if f and not l)
    FN = sum(1 for f, l in zip(flags, labels) if (not f) and l)
    TN = sum(1 for f, l in zip(flags, labels) if (not f) and (not l))
    n = len(labels); pos = TP + FN
    ppv = TP / (TP + FP) if (TP + FP) else None
    base = pos / n if n else None
    return {"TP": TP, "FP": FP, "FN": FN, "TN": TN,
            "sensitivity": round(TP / pos, 3) if pos else None,
            "specificity": round(TN / (TN + FP), 3) if (TN + FP) else None,
            "PPV": round(ppv, 3) if ppv is not None else None,
            "lift_over_base": round(ppv / base, 3) if (ppv is not None and base) else None,
            "accuracy": round((TP + TN) / n, 3) if n else None}


def metrics(recs):
    """recs: list of dicts with P1,P4,vuln,elevated,crisis. Returns AUC + confusion."""
    sub = [r for r in recs if r.get("crisis") is not None and r.get("P1") is not None]
    labels = [1 if r["crisis"] else 0 for r in sub]
    if len(set(labels)) < 2:
        return {"n": len(sub), "note": "no_variation"}

    def _auc(sig):
        idx = [i for i, s in enumerate(sig) if s is not None]
        if len({labels[i] for i in idx}) < 2:
            return None
        return round(auc_roc([sig[i] for i in idx], [labels[i] for i in idx]), 3)
    return {
        "n": len(sub), "base_rate": round(sum(labels) / len(sub), 3),
        "AUC": {"vuln_score": _auc([r["vuln"] for r in sub]),
                "durability_gap": _auc([r["P4"] - r["P1"] for r in sub]),
                "neg_P1_institutional": _auc([-r["P1"] for r in sub])},
        "elevated_confusion": confusion([bool(r["elevated"]) for r in sub], [bool(x) for x in labels]),
    }


def test_C1():
    series = json.loads(REVEALED.read_text())["series"]
    tax_pct, tax_raw = revealed_pct_2004(series["tax_rev_pct_gdp"])
    edu_pct, edu_raw = revealed_pct_2004(series["gov_edu_exp_pct_gdp"])
    composite_pct = {}
    for iso in set(tax_pct) | set(edu_pct):
        vals = [p[iso] for p in (tax_pct, edu_pct) if iso in p]
        composite_pct[iso] = sum(vals) / len(vals)

    # committed crisis labels by iso (2004 window)
    crisis = {r["iso"]: r["crisis"] for r in json.loads(HOLDOUT.read_text())["windows"]["2004"]}
    perception = json.loads(HOLDOUT.read_text())["windows"]["2004"]

    variants = {"P1_tax": tax_pct, "P1_edu": edu_pct, "P1_tax_edu": composite_pct}
    rebuilt = {}
    coverage = {}
    for vname, pct in variants.items():
        recs = []
        covered = 0
        for iso, name, display, ind, tier in iter_universe(2004):
            if iso not in crisis:      # only grade the committed holdout set
                continue
            ind = dict(ind)
            if iso in pct:
                for k in P1_WGI:
                    ind[k] = pct[iso]
                covered += 1
            else:
                continue               # no revealed P1 -> excluded from revealed variant
            r = full_diagnostic(ind, {})
            sc = r["scoring"]; pil = sc.get("pillar_scores", {})
            p1, p4, spread = pil.get("P1"), pil.get("P4"), sc.get("pillar_spread")
            if p1 is None or p4 is None or spread is None:
                continue
            pr = predict(p1, p4, spread)
            recs.append({"iso": iso, "P1": p1, "P4": p4,
                         "vuln": pr["vulnerability_score_0_3"],
                         "elevated": pr["elevated_crisis_vulnerability"],
                         "crisis": crisis[iso]})
        rebuilt[vname] = {"coverage": covered, "metrics": metrics(recs), "isos": [r["iso"] for r in recs]}
        coverage[vname] = covered

    # perception baseline on the SAME iso subset (for a fair AUC comparison per variant)
    perc_metrics_full = metrics(perception)
    per_variant_perc = {}
    for vname, v in rebuilt.items():
        isos = set(v["isos"])
        per_variant_perc[vname] = metrics([r for r in perception if r["iso"] in isos])

    return {
        "method": "Finding-1 seam: inject 0-100 percentile-ranked revealed series into P1 WGI keys at 2004; "
                  "re-score; run frozen predict(); grade vs committed 2004->2024 crisis labels.",
        "revealed_2004_coverage": coverage,
        "perception_P1_full_holdout": perc_metrics_full,
        "revealed_variants": rebuilt,
        "perception_baseline_on_matched_isos": per_variant_perc,
        "reading": "if revealed-P1 AUC/lift > perception-P1 on the matched iso set, perception is a bottleneck (C contributes).",
    }


def test_C2():
    series = json.loads(REVEALED.read_text())["series"]["tax_rev_pct_gdp"]
    tax = {iso: {int(y): v for y, v in s.items()} for iso, s in series.items()}
    wgi = json.loads(WGI.read_text())
    onsets = json.loads(ONSETS.read_text())["onsets"]
    crisis_countries = {i: sorted(y for y in ys if 2010 <= y <= 2024) for i, ys in onsets.items()}
    crisis_countries = {i: ys for i, ys in crisis_countries.items() if ys}

    def series_change(s, y0, y1):
        """value(y1_nearest) - value(y0_nearest); None if <2 points in [y0-1,y1+1]."""
        cand = {y: v for y, v in s.items() if y0 - 1 <= y <= y1 + 1}
        if len(cand) < 2:
            return None
        ylo = min(cand); yhi = max(cand)
        if yhi - ylo < 3:
            return None
        return cand[yhi] - cand[ylo], (ylo, yhi)

    rows = []
    both_decline = wgi_lags = 0
    for iso, ys in crisis_countries.items():
        onset = ys[0]
        y0, y1 = onset - 10, onset - 1
        ge = {int(y): v for y, v in wgi.get(iso, {}).get("GE", {}).items()}
        tx = tax.get(iso, {})
        dge = series_change(ge, y0, y1)
        dtx = series_change(tx, y0, y1)
        if dge is None or dtx is None:
            continue
        rec = {"iso": iso, "onset": onset,
               "wgi_GE_change_pre": round(dge[0], 2), "tax_change_pre": round(dtx[0], 2)}
        rows.append(rec)
        if dtx[0] < 0 and dge[0] >= 0:      # functional down while perception flat/up
            wgi_lags += 1
        if dtx[0] < 0 and dge[0] < 0:
            both_decline += 1

    n = len(rows)
    mean_ge = round(float(np.mean([r["wgi_GE_change_pre"] for r in rows])), 2) if rows else None
    mean_tax = round(float(np.mean([r["tax_change_pre"] for r in rows])), 2) if rows else None
    return {
        "method": "for 2010-2024 (UCDP/COW-onset) crisis countries, compare change in WGI gov-effectiveness "
                  "vs change in tax %GDP over the ~10y pre-crisis window.",
        "n_crisis_countries_evaluable": n,
        "mean_wgi_GE_change_pre": mean_ge,
        "mean_tax_change_pre": mean_tax,
        "n_functional_down_while_perception_flat_or_up": wgi_lags,
        "n_both_decline": both_decline,
        "per_country": sorted(rows, key=lambda r: r["tax_change_pre"]),
        "reading": "if tax systematically falls pre-crisis while WGI stays flat/up, perceptions mask early "
                   "institutional decay (bottlenecks the holdout). Small-n descriptive.",
    }


def main():
    report = {"component": "C_measurement_regime_change",
              "C1_revealed_P1_holdout": test_C1(),
              "C2_perception_lag": test_C2()}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, default=lambda o: None))

    c1 = report["C1_revealed_P1_holdout"]
    print("=== C1 — revealed-outcome P1 holdout vs perception-P1 (2004 window) ===")
    pf = c1["perception_P1_full_holdout"]
    print(f"  perception-P1 (full n={pf['n']} base={pf['base_rate']}): "
          f"vuln_AUC={pf['AUC']['vuln_score']} gap={pf['AUC']['durability_gap']} negP1={pf['AUC']['neg_P1_institutional']} "
          f"lift={pf['elevated_confusion']['lift_over_base']}")
    for vname, v in c1["revealed_variants"].items():
        m = v["metrics"]; pm = c1["perception_baseline_on_matched_isos"][vname]
        if "AUC" not in m:
            print(f"  {vname}: {m}"); continue
        print(f"  {vname} (n={m['n']} cov={v['coverage']} base={m['base_rate']}):")
        print(f"      revealed : vuln={m['AUC']['vuln_score']} gap={m['AUC']['durability_gap']} "
              f"negP1={m['AUC']['neg_P1_institutional']} lift={m['elevated_confusion']['lift_over_base']} "
              f"sens={m['elevated_confusion']['sensitivity']} spec={m['elevated_confusion']['specificity']}")
        print(f"      percept. : vuln={pm['AUC']['vuln_score']} gap={pm['AUC']['durability_gap']} "
              f"negP1={pm['AUC']['neg_P1_institutional']} lift={pm['elevated_confusion']['lift_over_base']} "
              f"sens={pm['elevated_confusion']['sensitivity']} spec={pm['elevated_confusion']['specificity']}")

    c2 = report["C2_perception_lag"]
    print(f"\n=== C2 — perception lag (n={c2['n_crisis_countries_evaluable']} crisis countries) ===")
    print(f"  mean pre-crisis WGI-GE change={c2['mean_wgi_GE_change_pre']}  mean tax change={c2['mean_tax_change_pre']}")
    print(f"  functional-down-while-perception-flat/up: {c2['n_functional_down_while_perception_flat_or_up']}  "
          f"both-decline: {c2['n_both_decline']}")
    print(f"\n-> {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
