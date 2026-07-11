#!/usr/bin/env python3
"""
Decoupling — Test 3 (economic composition moderates the signal) and Test 4
(financial depth moderates the signal). Frozen spec: DECOUPLING_PREREGISTRATION.md.

Reuses committed machinery: dysfunction outcome (erosion_component_B), logit/AUC
(esi_tests). Read-only; writes t3_composition.json / t4_financial.json.
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "robustness"))
sys.path.insert(0, str(ROOT / "scripts" / "historical"))

from esi_tests import auc_roc, zscore, logit_fit  # noqa: E402
import erosion_component_B as B  # noqa: E402
from mi import panel  # noqa: E402

HOLDOUT = ROOT / "data/robustness/temporal_holdout_panel.json"
WDI = ROOT / "data/robustness/decoupling/wdi_decoupling.json"
OUT3 = ROOT / "data/robustness/decoupling/t3_composition.json"
OUT4 = ROOT / "data/robustness/decoupling/t4_financial.json"


def load_wdi():
    return json.loads(WDI.read_text())


def wdi_val(wdi, label, iso, year, back=3):
    """Value at year, else nearest earlier within `back` years (WDI gaps)."""
    ser = wdi.get(label, {})
    d = ser.get(iso)
    if not d:
        return None
    for y in range(year, year - back - 1, -1):
        if str(y) in d and d[str(y)] is not None:
            return d[str(y)]
    return None


def build_holdout_records():
    """Per window: list of dicts with iso, P1, gdp, crisis, dys_polity."""
    holdout = json.loads(HOLDOUT.read_text())["windows"]
    cc_iso, _ = B.build_ccode_iso()
    GDP, FSI, POL, LIB = B.load_gdp(), B.load_fsi(), B.load_polity(cc_iso), B.load_libdem()
    out = {}
    for win, rows in holdout.items():
        yr = int(win)
        recs = []
        for r in rows:
            if r["P1"] is None:
                continue
            fl = B.dysfunction_flags(r["iso"], yr, 2024, GDP, FSI, POL, LIB, r.get("ucdp"))
            dys = B.composite(fl, ["D1_polity_backslide", "D2_gdp_drop15",
                                   "D3_conflict_onset", "D4_fsi_rise10"])
            g = GDP.get(r["iso"], {}).get(yr)
            recs.append({"iso": r["iso"], "country": r["country"], "P1": r["P1"],
                         "gdp": g, "crisis": bool(r["crisis"]), "dys_polity": dys})
        out[win] = recs
    return out, GDP


def auc_for(recs, outcome, signal_fn):
    sub = [(signal_fn(r), 1 if r[outcome] else 0) for r in recs
           if r.get(outcome) is not None and signal_fn(r) is not None]
    ys = {y for _, y in sub}
    if len(ys) < 2 or len(sub) < 10:
        return None, len(sub)
    a = auc_roc([s for s, _ in sub], [y for _, y in sub])
    return (None if math.isnan(a) else round(float(a), 3)), len(sub)


def neg_p1(r):
    return -r["P1"]


def neg_loggdp(r):
    g = r["gdp"]
    return -math.log(g) if (g and g > 0) else None


# ------------------------------------------------------------------ Test 3
def test3(hold, wdi):
    res = {"test": "T3_economic_composition", "windows": {}}
    for win, recs in hold.items():
        yr = int(win)
        # institution-light share = resource_rents + manufacturing %GDP
        for r in recs:
            ind = panel.indicators_for(r["iso"], yr) or {}
            rents = ind.get("resource_rents_pct_gdp")
            manf = wdi_val(wdi, "manufacturing_pct_gdp", r["iso"], yr)
            r["light_share"] = ((rents or 0.0) + (manf or 0.0)) if (rents is not None or manf is not None) else None
        scored = [r for r in recs if r["light_share"] is not None]
        med = float(np.median([r["light_share"] for r in scored]))
        groupL = [r for r in scored if r["light_share"] > med]   # institution-light
        groupH = [r for r in scored if r["light_share"] <= med]  # institution-heavy
        wres = {"median_light_share": round(med, 2),
                "mean_light_share": round(float(np.mean([r["light_share"] for r in scored])), 2),
                "n_scored": len(scored), "groups": {}}
        for gname, g in [("H_institution_heavy", groupH), ("L_institution_light", groupL)]:
            gd = {"n": len(g)}
            for oc in ["crisis", "dys_polity"]:
                np1, n1 = auc_for(g, oc, neg_p1)
                wa, _ = auc_for(g, oc, neg_loggdp)
                gd[oc] = {"n_eval": n1, "negP1_auc": np1, "wealth_auc": wa,
                          "negP1_minus_wealth": (None if (np1 is None or wa is None) else round(np1 - wa, 3))}
            wres["groups"][gname] = gd
        # H - L difference in (negP1 - wealth)
        diffs = {}
        for oc in ["crisis", "dys_polity"]:
            h = wres["groups"]["H_institution_heavy"][oc]["negP1_minus_wealth"]
            l = wres["groups"]["L_institution_light"][oc]["negP1_minus_wealth"]
            diffs[oc] = (None if (h is None or l is None) else round(h - l, 3))
        wres["H_minus_L_signal_edge"] = diffs
        res["windows"][win] = wres
    return res


# ------------------------------------------------------------------ Test 4
def minmax(vals):
    v = np.array([x for x in vals if x is not None], float)
    if len(v) == 0:
        return None, None
    return float(v.min()), float(v.max())


def test4(hold, wdi):
    res = {"test": "T4_financial_depth", "windows": {}}
    for win, recs in hold.items():
        yr = int(win)
        for r in recs:
            smc = wdi_val(wdi, "stockmkt_cap_pct_gdp", r["iso"], yr, back=4)
            pcr = wdi_val(wdi, "private_credit_pct_gdp", r["iso"], yr, back=4)
            r["_smc"], r["_pcr"] = smc, pcr
        smc_lo, smc_hi = minmax([r["_smc"] for r in recs])
        pcr_lo, pcr_hi = minmax([r["_pcr"] for r in recs])

        def norm(v, lo, hi):
            if v is None or hi is None or hi == lo:
                return None
            return (v - lo) / (hi - lo)
        for r in recs:
            a = norm(r["_smc"], smc_lo, smc_hi)
            b = norm(r["_pcr"], pcr_lo, pcr_hi)
            comps = [c for c in (a, b) if c is not None]
            r["findepth"] = float(np.mean(comps)) if comps else None

        wout = {"n_total": len(recs)}
        for oc in ["crisis", "dys_polity"]:
            sub = [r for r in recs if r.get(oc) is not None and r["P1"] is not None
                   and r["findepth"] is not None]
            y = np.array([1 if r[oc] else 0 for r in sub], float)
            if len(sub) < 15 or len(set(y)) < 2:
                wout[oc] = {"n": len(sub), "note": "insufficient"}
                continue
            negp1 = zscore([-r["P1"] for r in sub])
            fd = zscore([r["findepth"] for r in sub])
            inter = zscore(negp1 * fd)
            ones = np.ones(len(sub))
            m1 = logit_fit(np.column_stack([ones, negp1]), y)
            m2 = logit_fit(np.column_stack([ones, negp1, fd]), y)
            m3 = logit_fit(np.column_stack([ones, negp1, fd, inter]), y)
            wout[oc] = {
                "n": len(sub), "n_pos": int(y.sum()), "base_rate": round(float(y.mean()), 3),
                "mean_findepth": round(float(np.mean([r["findepth"] for r in sub])), 3),
                "M1_negP1": {"coef_negP1": round(float(m1[0][1]), 4), "auc": round(float(m1[1]), 3)},
                "M2_plus_findepth": {"coef_negP1": round(float(m2[0][1]), 4),
                                     "coef_findepth": round(float(m2[0][2]), 4), "auc": round(float(m2[1]), 3)},
                "M3_interaction": {"coef_negP1": round(float(m3[0][1]), 4),
                                   "coef_findepth": round(float(m3[0][2]), 4),
                                   "coef_interaction": round(float(m3[0][3]), 4),
                                   "auc": round(float(m3[1]), 3)},
                "interaction_sign": ("negative(financialization-supported)" if m3[0][3] < 0
                                     else "positive(null)"),
            }
        res["windows"][win] = wout
    return res


def system_findepth(wdi):
    """Mean financial depth across balanced panel at 5 MI points (context)."""
    import decoupling_panel as dp
    p = dp.load()
    bal = p["balanced"]
    out = {}
    for y in [1996, 2004, 2012, 2018, 2024]:
        vals = []
        for iso in bal:
            smc = wdi_val(wdi, "stockmkt_cap_pct_gdp", iso, y, back=2)
            pcr = wdi_val(wdi, "private_credit_pct_gdp", iso, y, back=2)
            comps = [c for c in (smc, pcr) if c is not None]
            if comps:
                vals.append(np.mean(comps))
        out[y] = {"n": len(vals), "mean_findepth_pct_gdp": round(float(np.mean(vals)), 1) if vals else None}
    return out


def main():
    wdi = load_wdi()
    hold, _ = build_holdout_records()
    t3 = test3(hold, wdi)
    t4 = test4(hold, wdi)
    t4["system_financial_deepening"] = system_findepth(wdi)
    OUT3.write_text(json.dumps(t3, indent=1))
    OUT4.write_text(json.dumps(t4, indent=1))

    print("=== TEST 3 — composition moderates signal (neg-P1 minus wealth AUC by group) ===")
    for win, w in t3["windows"].items():
        print(f"  window {win} (median light-share={w['median_light_share']}%, n={w['n_scored']}):")
        for gname, g in w["groups"].items():
            c = g["crisis"]; d = g["dys_polity"]
            print(f"    {gname:22s} n={g['n']:2d} | crisis: negP1={c['negP1_auc']} wealth={c['wealth_auc']} edge={c['negP1_minus_wealth']}"
                  f" | dysf: negP1={d['negP1_auc']} wealth={d['wealth_auc']} edge={d['negP1_minus_wealth']}")
        print(f"    H-L signal edge: crisis={w['H_minus_L_signal_edge']['crisis']} dysf={w['H_minus_L_signal_edge']['dys_polity']}")

    print("\n=== TEST 4 — financial depth interaction (M3) ===")
    for win, w in t4["windows"].items():
        print(f"  window {win}:")
        for oc in ["crisis", "dys_polity"]:
            o = w.get(oc, {})
            if "M3_interaction" not in o:
                print(f"    {oc}: {o.get('note','?')} (n={o.get('n')})"); continue
            m3 = o["M3_interaction"]
            print(f"    {oc}: n={o['n']} base={o['base_rate']} | M1auc={o['M1_negP1']['auc']} "
                  f"M3: negP1={m3['coef_negP1']} findepth={m3['coef_findepth']} "
                  f"INTER={m3['coef_interaction']} ({o['interaction_sign']}) auc={m3['auc']}")
    print("  system financial deepening (balanced panel mean %GDP):")
    for y, v in t4["system_financial_deepening"].items():
        print(f"    {y}: {v['mean_findepth_pct_gdp']} (n={v['n']})")


if __name__ == "__main__":
    main()
