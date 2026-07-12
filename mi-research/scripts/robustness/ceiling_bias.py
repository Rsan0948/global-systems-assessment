#!/usr/bin/env python3
"""
WGI ceiling-bias test. Does perception-based P1 overstate DECLINE at the top of the
distribution vs revealed-outcome functional indicators (tax revenue primary; education,
LPI robustness)? Frozen spec: docs/CEILING_BIAS_PREREGISTRATION.md (sha256 ed1c717c).
Read-only.
"""
from __future__ import annotations
import csv
import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "robustness"))
import convergence_lib as L  # noqa: E402

WB = ROOT.parent / "mi-pipeline/data/wb_cached.csv"
REV = ROOT / "data/robustness/convergence/revealed_outcomes.json"
FORM = ROOT / "data/robustness/formation/state_formation.json"
OUT = ROOT / "data/robustness/convergence/ceiling_bias.json"
WGI = ["GovEff", "RuleLaw", "RegQual", "CtrlCorr"]
MI_YEARS = [1996, 2004, 2012, 2018, 2024]


def load_wgi():
    D = {}
    for r in csv.DictReader(open(WB, encoding="utf-8")):
        D.setdefault(r["iso3"], {})[r["year"]] = r
    def p1(iso, y):
        r = D.get(iso, {}).get(str(y))
        if not r:
            return None
        vs = [r.get(k) for k in WGI]
        return None if any(v in (None, "") for v in vs) else float(np.mean([float(v) for v in vs]))
    return D, p1


def nearest(series_iso, year, tol=3):
    """value at year or nearest within +/-tol."""
    if not series_iso:
        return None
    for d in range(tol + 1):
        for yy in ([year] if d == 0 else [year - d, year + d]):
            v = series_iso.get(str(yy))
            if v is not None:
                return float(v)
    return None


def percentile_series(rev, indicator, real_isos):
    """Per year, cross-sectional percentile rank (0-100) within real countries.
    Returns {iso: {year: pctile}} for the MI-year grid (nearest within 3)."""
    ser = rev["series"].get(indicator, {})
    out = {}
    for y in MI_YEARS:
        vals = []
        for iso in real_isos:
            v = nearest(ser.get(iso), y)
            if v is not None:
                vals.append((iso, v))
        if len(vals) < 10:
            continue
        arr = np.array([v for _, v in vals])
        ranks = stats.rankdata(arr) / len(arr) * 100.0
        for (iso, _), pr in zip(vals, ranks):
            out.setdefault(iso, {})[y] = float(pr)
    return out


def main():
    Dwgi, p1 = load_wgi()
    rev = json.loads(REV.read_text())
    real = [iso for iso in Dwgi if p1(iso, 1996) is not None]  # real countries w/ 1996 P1

    # --- Step 1: groups by 1996 P1 ---
    ranked = sorted(real, key=lambda i: (-p1(i, 1996), i))
    top20 = ranked[:20]
    middle = ranked[40:60]
    bottom20 = ranked[-20:]
    name = {iso: Dwgi[iso][sorted(Dwgi[iso])[0]]["country"] for iso in ranked}

    # --- revealed percentile series (primary=tax; robustness basket) ---
    tax_pct = percentile_series(rev, "tax_rev_pct_gdp", real)
    edu_pct = percentile_series(rev, "gov_edu_exp_pct_gdp", real)
    lpi_pct = percentile_series(rev, "lpi_overall", real)

    def revealed_p1(iso, y, basket=False):
        if not basket:
            return tax_pct.get(iso, {}).get(y)
        vals = [d.get(iso, {}).get(y) for d in (tax_pct, edu_pct, lpi_pct)]
        vals = [v for v in vals if v is not None]
        return float(np.mean(vals)) if vals else None

    def wgi_pct_series():
        """WGI-P1 is already 0-100 percentile; use raw P1 avg (already percentile scale)."""
        return {iso: {y: p1(iso, y) for y in MI_YEARS if p1(iso, y) is not None} for iso in real}
    wgi = wgi_pct_series()

    def perception_gap(iso, basket=False):
        w0 = wgi.get(iso, {}).get(1996); w1 = wgi.get(iso, {}).get(2024)
        r0 = revealed_p1(iso, 1996, basket); r1 = revealed_p1(iso, 2024, basket)
        if None in (w0, w1, r0, r1):
            return None
        return (w1 - w0) - (r1 - r0)  # ΔWGI - Δrevealed; negative = perception overstates decline

    def group_gaps(g, basket=False):
        return [(iso, perception_gap(iso, basket)) for iso in g if perception_gap(iso, basket) is not None]

    # --- Step 4: ceiling test (primary=tax) ---
    def step4(basket=False):
        t = [v for _, v in group_gaps(top20, basket)]
        m = [v for _, v in group_gaps(middle, basket)]
        if len(t) < 5 or len(m) < 5:
            return {"note": "insufficient", "n_top": len(t), "n_mid": len(m)}
        u = stats.mannwhitneyu(t, m, alternative="less")  # top more negative
        tt = stats.ttest_ind(t, m, equal_var=False)
        # Cliff's delta
        gt = sum((a > b) for a in t for b in m); lt = sum((a < b) for a in t for b in m)
        cd = (gt - lt) / (len(t) * len(m))
        return {"n_top": len(t), "n_mid": len(m),
                "top_mean_gap": round(float(np.mean(t)), 2), "top_median": round(float(np.median(t)), 2),
                "mid_mean_gap": round(float(np.mean(m)), 2), "mid_median": round(float(np.median(m)), 2),
                "mannwhitney_p_top_more_negative": round(float(u.pvalue), 4),
                "welch_t": round(float(tt.statistic), 2), "welch_p": round(float(tt.pvalue), 4),
                "cliffs_delta": round(float(cd), 3),
                "ceiling_bias_confirmed": bool(u.pvalue < 0.05 and np.mean(t) < np.mean(m))}

    s4_tax = step4(False); s4_basket = step4(True)

    # --- Step 5: country profiles ---
    profiles = {}
    tax_ser = rev["series"].get("tax_rev_pct_gdp", {})
    edu_ser = rev["series"].get("gov_edu_exp_pct_gdp", {})
    for iso in ["NLD", "DNK", "NZL", "FIN", "NOR", "CHE", "SWE", "DEU", "GBR", "USA"]:
        if iso not in wgi:
            continue
        traj = {}
        for y in MI_YEARS:
            traj[y] = {"wgi": round(wgi.get(iso, {}).get(y), 1) if wgi.get(iso, {}).get(y) is not None else None,
                       "tax_pct": round(tax_pct.get(iso, {}).get(y), 1) if tax_pct.get(iso, {}).get(y) is not None else None,
                       "basket_pct": round(revealed_p1(iso, y, True), 1) if revealed_p1(iso, y, True) is not None else None}
        # absolute raw functional change
        raw_tax0 = nearest(tax_ser.get(iso), 1996); raw_tax1 = nearest(tax_ser.get(iso), 2024)
        raw_edu0 = nearest(edu_ser.get(iso), 1996); raw_edu1 = nearest(edu_ser.get(iso), 2024)
        profiles[iso] = {"name": name.get(iso, iso), "rank_1996": ranked.index(iso) + 1 if iso in ranked else None,
                         "trajectory": traj,
                         "perception_gap_tax": round(perception_gap(iso), 2) if perception_gap(iso) is not None else None,
                         "raw_tax_pct_gdp": [round(raw_tax0, 1) if raw_tax0 else None, round(raw_tax1, 1) if raw_tax1 else None],
                         "raw_edu_pct_gdp": [round(raw_edu0, 1) if raw_edu0 else None, round(raw_edu1, 1) if raw_edu1 else None]}

    # --- Step 6: divergence scan recomputed with revealed-P1 (tax percentile) ---
    def divergence_recount():
        # WGI-based decline set (ΔWGI < -2 & tax data available), vs revealed decline
        surv = {"wgi_decliners": [], "still_decline_on_revealed": [], "flip_to_stable_on_revealed": []}
        for iso in real:
            w0 = wgi.get(iso, {}).get(1996); w1 = wgi.get(iso, {}).get(2024)
            r0 = revealed_p1(iso, 1996); r1 = revealed_p1(iso, 2024)
            if None in (w0, w1, r0, r1):
                continue
            dW = w1 - w0; dR = r1 - r0
            if dW < -2:  # WGI decliner (ceiling-relevant threshold)
                surv["wgi_decliners"].append(iso)
                (surv["still_decline_on_revealed"] if dR < 0 else surv["flip_to_stable_on_revealed"]).append(iso)
        return {k: [name.get(i, i) for i in v] if k != "counts" else v for k, v in surv.items()} | {
            "n_wgi_decliners": len(surv["wgi_decliners"]),
            "n_still_decline_revealed": len(surv["still_decline_on_revealed"]),
            "n_flip_to_stable": len(surv["flip_to_stable_on_revealed"]),
            "mature_focus": {i: {"dWGI": round(wgi[i][2024] - wgi[i][1996], 1),
                                 "dTax_pct": round(revealed_p1(i, 2024) - revealed_p1(i, 1996), 1)}
                             for i in ["NLD", "GBR", "FRA", "DEU", "USA"] if i in wgi and revealed_p1(i, 1996) is not None and revealed_p1(i, 2024) is not None}}

    # --- Step 7: floor effect (bottom-20) ---
    def step7():
        b = [v for _, v in group_gaps(bottom20)]
        t = [v for _, v in group_gaps(top20)]
        if len(b) < 5:
            return {"note": "insufficient", "n_bottom": len(b)}
        return {"n_bottom": len(b), "bottom_mean_gap": round(float(np.mean(b)), 2),
                "bottom_median_gap": round(float(np.median(b)), 2),
                "top_mean_gap": round(float(np.mean(t)), 2) if t else None,
                "interpretation": ("floor effect present (bottom revealed-decline exceeds perception, gap > 0) "
                                   "→ WGI compresses range" if np.mean(b) > 0 else
                                   "no floor effect (bottom perception gap not positive)")}

    out = {"prereg_sha256": "ed1c717c",
           "groups": {"top20": [name[i] for i in top20], "middle_41_60": [name[i] for i in middle],
                      "bottom20": [name[i] for i in bottom20]},
           "step4_ceiling_tax_primary": s4_tax, "step4_ceiling_basket_robustness": s4_basket,
           "step5_profiles": profiles, "step6_divergence_recount": divergence_recount(),
           "step7_floor_effect": step7()}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))

    print("=== STEP 1 — groups by 1996 WGI-P1 ===")
    print("  TOP-20:", ", ".join(out["groups"]["top20"]))
    print("  MIDDLE(41-60):", ", ".join(out["groups"]["middle_41_60"]))
    print("\n=== STEP 4 (GATE) — ceiling bias: perception gap (ΔWGI - Δrevealed), Top-20 vs Middle ===")
    for lab, s in [("TAX primary", s4_tax), ("BASKET robustness", s4_basket)]:
        if "note" in s:
            print(f"  [{lab}] {s}"); continue
        print(f"  [{lab}] top mean gap={s['top_mean_gap']} (n={s['n_top']}) vs mid={s['mid_mean_gap']} (n={s['n_mid']}) | "
              f"MW p(top more neg)={s['mannwhitney_p_top_more_negative']} Cliff δ={s['cliffs_delta']} | "
              f">>> CONFIRMED: {s['ceiling_bias_confirmed']}")
    print("\n=== STEP 5 — top-tier profiles (WGI | tax-pctile | basket-pctile per year; perception_gap; raw tax/edu %GDP 96->24) ===")
    for iso, p in out["step5_profiles"].items():
        tr = " ".join(f"{y}:[{p['trajectory'][y]['wgi']}/{p['trajectory'][y]['tax_pct']}/{p['trajectory'][y]['basket_pct']}]" for y in MI_YEARS)
        print(f"  {p['name']:<14}(rank{p['rank_1996']}) gap={p['perception_gap_tax']} rawTax{p['raw_tax_pct_gdp']} rawEdu{p['raw_edu_pct_gdp']}")
        print(f"       {tr}")
    print("\n=== STEP 6 — divergence scan on revealed-P1 (tax) ===")
    d6 = out["step6_divergence_recount"]
    print(f"  WGI decliners (ΔWGI<-2, tax avail): {d6['n_wgi_decliners']} | still decline on revealed: {d6['n_still_decline_revealed']} | flip to stable: {d6['n_flip_to_stable']}")
    print(f"  mature focus (ΔWGI / ΔtaxPctile): {d6['mature_focus']}")
    print(f"  flip-to-stable countries: {', '.join(d6['flip_to_stable_on_revealed'][:25])}")
    print("\n=== STEP 7 — floor effect (bottom-20) ===")
    print(f"  {out['step7_floor_effect']}")


if __name__ == "__main__":
    main()
