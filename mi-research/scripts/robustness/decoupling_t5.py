#!/usr/bin/env python3
"""
Decoupling — Test 5 (institutional reorientation from people to capital).
  5A P1-P3 decoupling; 5B P1-P4 tightening (+ GDP-decontaminated P4*);
  5C people- vs capital-orientation correlation with P1; 5D 1979 inflection.
Frozen spec: DECOUPLING_PREREGISTRATION.md. Read-only; writes t5_reorientation.json.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "robustness"))
import decoupling_panel as dp  # noqa: E402
from mi import panel  # noqa: E402

YEARS = [1996, 2004, 2012, 2018, 2024]
WDI = ROOT / "data/robustness/decoupling/wdi_decoupling.json"
OUT = ROOT / "data/robustness/decoupling/t5_reorientation.json"


def trend(xs, ys):
    r = stats.linregress(np.array(xs, float), np.array(ys, float))
    return {"slope": float(r.slope), "p": float(r.pvalue)}


def corr(x, y):
    if len(x) < 4:
        return None
    pr = stats.pearsonr(x, y)
    sp = stats.spearmanr(x, y)
    return {"n": len(x), "pearson_r": float(pr.statistic), "pearson_p": float(pr.pvalue),
            "spearman_rho": float(sp.statistic)}


def pillar_corr(pnl, keyy):
    """corr(P1, keyy) at each of 5 points on the balanced panel."""
    rows = pnl["rows"]; bal = pnl["balanced"]
    per = {}
    rs = []
    for y in YEARS:
        xs, ys = [], []
        for iso in bal:
            e = rows[iso]["years"].get(str(y))
            if e and e.get("P1") is not None and e.get(keyy) is not None:
                xs.append(e["P1"]); ys.append(e[keyy])
        c = corr(np.array(xs, float), np.array(ys, float))
        per[y] = c
        rs.append(c["pearson_r"] if c else None)
    valid = [(y, r) for y, r in zip(YEARS, rs) if r is not None]
    tr = trend([y for y, _ in valid], [r for _, r in valid]) if len(valid) >= 3 else None
    return {"per_year": per, "r_trend": tr,
            "delta_r_last_first": (rs[-1] - rs[0]) if (rs[0] is not None and rs[-1] is not None) else None}


def wdi_val(wdi, label, iso, year, back=3):
    d = wdi.get(label, {}).get(iso)
    if not d:
        return None
    for y in range(year, year - back - 1, -1):
        if str(y) in d and d[str(y)] is not None:
            return d[str(y)]
    return None


def minmax_norm(pairs):
    """pairs: list of (iso, value|None) -> dict iso->normalized (skip None)."""
    vals = [v for _, v in pairs if v is not None]
    if not vals:
        return {}
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return {iso: 0.5 for iso, v in pairs if v is not None}
    return {iso: (v - lo) / (hi - lo) for iso, v in pairs if v is not None}


def orientation_index(wdi, isos, year, labels):
    """Equal-weight mean of min-max normalized component labels, per iso."""
    norms = []
    for lab in labels:
        pairs = [(iso, wdi_val(wdi, lab, iso, year)) for iso in isos]
        norms.append(minmax_norm(pairs))
    idx = {}
    for iso in isos:
        comps = [n[iso] for n in norms if iso in n]
        if comps:
            idx[iso] = float(np.mean(comps))
    return idx


def test5c(pnl, wdi):
    rows = pnl["rows"]; bal = pnl["balanced"]
    people_labels = ["edu_exp_pct_gdp", "health_pub_exp_pct_gdp", "social_protection_pct_gdp"]
    capital_labels = ["stockmkt_cap_pct_gdp", "private_credit_pct_gdp",
                      "trade_openness_pct_gdp", "fdi_net_inflow_pct_gdp"]
    per = {}
    p_rs, c_rs = [], []
    for y in YEARS:
        people = orientation_index(wdi, bal, y, people_labels)
        capital = orientation_index(wdi, bal, y, capital_labels)
        # correlate with P1
        def c_with(idx):
            xs, ys = [], []
            for iso in bal:
                e = rows[iso]["years"].get(str(y))
                if e and e.get("P1") is not None and iso in idx:
                    xs.append(e["P1"]); ys.append(idx[iso])
            return corr(np.array(xs, float), np.array(ys, float))
        cp, cc = c_with(people), c_with(capital)
        per[y] = {"P1_vs_people": cp, "P1_vs_capital": cc}
        p_rs.append(cp["pearson_r"] if cp else None)
        c_rs.append(cc["pearson_r"] if cc else None)
    vp = [(y, r) for y, r in zip(YEARS, p_rs) if r is not None]
    vc = [(y, r) for y, r in zip(YEARS, c_rs) if r is not None]
    return {"per_year": per,
            "people_corr_trend": trend([y for y, _ in vp], [r for _, r in vp]) if len(vp) >= 3 else None,
            "capital_corr_trend": trend([y for y, _ in vc], [r for _, r in vc]) if len(vc) >= 3 else None}


def test5d(wdi, isos):
    """Long-series people-spending (edu+health) vs capital metrics 1970-2020."""
    anchors = [1970, 1980, 1990, 2000, 2010, 2020]
    people_labels = ["edu_exp_pct_gdp", "health_pub_exp_pct_gdp"]
    capital_labels = ["trade_openness_pct_gdp", "fdi_net_inflow_pct_gdp",
                      "private_credit_pct_gdp"]
    series = {}
    for y in anchors:
        def mean_of(labels):
            vals = []
            for iso in isos:
                comp = [wdi_val(wdi, lab, iso, y, back=2) for lab in labels]
                comp = [c for c in comp if c is not None]
                if comp:
                    vals.append(np.mean(comp))
            return (round(float(np.mean(vals)), 2), len(vals)) if vals else (None, 0)
        edu_only, ne = mean_of(["edu_exp_pct_gdp"])
        people, npv = mean_of(people_labels)
        capital, ncv = mean_of(capital_labels)
        series[y] = {"edu_only_mean": edu_only, "n_edu": ne,
                     "people_mean(edu+health)": people, "n_people": npv,
                     "capital_mean": capital, "n_capital": ncv}
    return {"note": "WB public-health series begins ~2000; pre-2000 people=edu-only. "
                    "Coverage-bounded per prereg.",
            "anchors": series}


def main():
    pnl = dp.load()
    wdi = json.loads(WDI.read_text())
    isos_all = list(pnl["rows"].keys())

    out = {"test": "T5_institutional_reorientation",
           "5A_P1_P3_decoupling": pillar_corr(pnl, "P3"),
           "5B_P1_P4_tightening": pillar_corr(pnl, "P4"),
           "5B_P1_P4star_gdp_removed": pillar_corr(pnl, "P4star"),
           "5C_orientation": test5c(pnl, wdi),
           "5D_washington_consensus": test5d(wdi, isos_all)}
    OUT.write_text(json.dumps(out, indent=1))

    def show(tag, block):
        per = block["per_year"]; tr = block["r_trend"]
        line = "  ".join(f"{y}:{(per[y]['pearson_r'] if per[y] else float('nan')):+.3f}" for y in YEARS)
        ts = f"slope={tr['slope']:+.5f} p={tr['p']:.3f}" if tr else "n/a"
        print(f"  {tag}: {line}  | trend {ts}  Δ={block['delta_r_last_first']:+.3f}"
              if block['delta_r_last_first'] is not None else f"  {tag}: {line} | trend {ts}")

    print("=== TEST 5A/5B — P1 correlations over time (balanced panel) ===")
    show("P1-P3 (5A, expect DOWN)", out["5A_P1_P3_decoupling"])
    show("P1-P4 (5B, expect UP) ", out["5B_P1_P4_tightening"])
    show("P1-P4* GDP-removed    ", out["5B_P1_P4star_gdp_removed"])

    print("\n=== TEST 5C — P1 vs people- vs capital-orientation ===")
    c = out["5C_orientation"]
    for y in YEARS:
        pp = c["per_year"][y]["P1_vs_people"]; cc = c["per_year"][y]["P1_vs_capital"]
        print(f"  {y}: P1-people r={pp['pearson_r']:+.3f}(n={pp['n']}) | "
              f"P1-capital r={cc['pearson_r']:+.3f}(n={cc['n']})" if (pp and cc) else f"  {y}: partial")
    pt, ct = c["people_corr_trend"], c["capital_corr_trend"]
    print(f"  people-corr trend slope={pt['slope']:+.5f} p={pt['p']:.3f} | "
          f"capital-corr trend slope={ct['slope']:+.5f} p={ct['p']:.3f}"
          if (pt and ct) else "  trend: partial")

    print("\n=== TEST 5D — long-series orientation (edu+health vs capital), 1970-2020 ===")
    for y, v in out["5D_washington_consensus"]["anchors"].items():
        print(f"  {y}: edu-only={v['edu_only_mean']}(n{v['n_edu']}) "
              f"people={v['people_mean(edu+health)']}(n{v['n_people']}) "
              f"capital={v['capital_mean']}(n{v['n_capital']})")


if __name__ == "__main__":
    main()
