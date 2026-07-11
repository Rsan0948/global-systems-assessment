#!/usr/bin/env python3
"""
Convergence confirmation — PART 1 (Tests 1-6). Confirms Finding 14's "wealth
catching up" interpretation from five independent angles + a dysfunction replication.
Frozen spec: docs/CONVERGENCE_PREREGISTRATION.md (sha256 4071b996). Read-only.

Writes data/robustness/convergence/part1.json.
"""
from __future__ import annotations
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import convergence_lib as L  # noqa: E402

ROOT = L.ROOT
OUT = ROOT / "data/robustness/convergence/part1.json"
F14_EPOCHS = [1816, 1876, 1946, 1996]


# ============================================================ Test 1
def couple(rol, gdp, isos, y):
    """Pearson/Spearman of rol vs log GDP at epoch y over isos."""
    xs, ys = [], []
    for iso in isos:
        if iso.startswith("OWID"):
            continue
        r = rol[iso].get(str(y)); g0 = gdp[iso].get(y)
        if r is None or g0 is None or g0 <= 0:
            continue
        xs.append(float(r)); ys.append(math.log(g0))
    if len(xs) < 6:
        return None
    pr = stats.pearsonr(xs, ys); sr = stats.spearmanr(xs, ys)
    return {"n": len(xs), "pearson_r": round(float(pr.statistic), 4),
            "spearman_rho": round(float(sr.statistic), 4)}


def test1():
    rol, gdp = L.load_rol_gdp()
    form = L.load_formation()
    uni = set(rol) & set(gdp)
    mature = {i for i in uni if form.get(i) == "mature"}
    anchors = [1850, 1900, 1950, 1996]  # constant-sample anchors (1816 too sparse)
    # constant set: present (rol+gdp) at all anchors
    def present(iso, y):
        return (rol[iso].get(str(y)) is not None and gdp[iso].get(y) not in (None,)
                and (gdp[iso].get(y) or 0) > 0)
    constant = {i for i in uni if all(present(i, a) for a in anchors)}

    grids = {
        "pooled": (L.EPOCHS, uni),
        "constant": (anchors, constant),
        "mature": (L.EPOCHS, mature),
    }
    traj = {}
    for name, (epochs, isos) in grids.items():
        series = {}
        for y in epochs:
            c = couple(rol, gdp, isos, y)
            if c:
                series[y] = c
        ys = sorted(series)
        prs = [series[y]["pearson_r"] for y in ys]
        traj[name] = {"n_set": len(isos), "per_epoch": series,
                      "delta_r": round(prs[-1] - prs[0], 4) if len(prs) >= 2 else None,
                      "r_trend": L.trend(ys, prs) if len(ys) >= 3 else None}

    # coupling at F14 epochs (pooled) vs committed wealth_auc
    com = {p["year"]: p for p in L.committed_decomp()}
    f14 = {}
    for y in F14_EPOCHS:
        c = couple(rol, gdp, uni, y)
        f14[y] = {"pooled_pearson_r": c["pearson_r"] if c else None,
                  "wealth_auc": com.get(y, {}).get("wealth_auc"),
                  "struct_auc": com.get(y, {}).get("struct_auc")}
    # correlate full pooled coupling series vs wealth_auc series (matched epochs)
    matched = [(traj["pooled"]["per_epoch"][p["year"]]["pearson_r"], p["wealth_auc"])
               for p in L.committed_decomp()
               if p["year"] in traj["pooled"]["per_epoch"] and p.get("wealth_auc") is not None]
    cser = stats.pearsonr([m[0] for m in matched], [m[1] for m in matched])
    # same for mature coupling
    matched_m = [(traj["mature"]["per_epoch"][p["year"]]["pearson_r"], p["wealth_auc"])
                 for p in L.committed_decomp()
                 if p["year"] in traj["mature"]["per_epoch"] and p.get("wealth_auc") is not None]
    cser_m = stats.pearsonr([m[0] for m in matched_m], [m[1] for m in matched_m])

    # Confirmation keyed to the LIKE-FOR-LIKE samples (prereg: pooled decline is the
    # expected decolonization composition artifact, NOT disconfirmation). The
    # coupling-vs-wealth_auc correlation is judged on the mature (constant-composition)
    # series for the same reason.
    confirm = ((traj["constant"]["delta_r"] or -1) > 0 or (traj["mature"]["delta_r"] or -1) > 0) \
        and float(cser_m.statistic) > 0
    return {"trajectories": traj, "f14_epochs": f14,
            "coupling_vs_wealth_auc": {
                "pooled": {"pearson_r": round(float(cser.statistic), 4), "p": round(float(cser.pvalue), 4), "n": len(matched)},
                "mature": {"pearson_r": round(float(cser_m.statistic), 4), "p": round(float(cser_m.pvalue), 4), "n": len(matched_m)}},
            "GATE_confirm": bool(confirm)}


# ============================================================ Test 2
def test2():
    wdi = L.load_wdi()
    # global mean sector share per decade (equal-country-weight)
    def decade_mean(indicator, y0):
        vals = []
        for iso in L.wdi_isos(wdi, indicator):
            v = None
            for yy in range(y0, y0 + 10):
                v = L.wdi_val(wdi, indicator, iso, yy)
                if v is not None:
                    break
            if v is not None:
                vals.append(v)
        return round(float(np.mean(vals)), 2), len(vals)
    decades = list(range(1970, 2021, 10)) + [2024]
    longitudinal = {}
    for y0 in decades:
        yy = y0 if y0 != 2024 else 2024
        ag, nag = decade_mean("agriculture_pct_gdp", yy if y0 == 2024 else y0)
        ind, _ = decade_mean("industry_pct_gdp", yy if y0 == 2024 else y0)
        sv, _ = decade_mean("services_pct_gdp", yy if y0 == 2024 else y0)
        longitudinal[y0] = {"agriculture": ag, "industry": ind, "services": sv, "n": nag}
    ys = sorted(longitudinal)
    ag_series = [longitudinal[y]["agriculture"] for y in ys]
    ag_trend = L.trend(ys, ag_series)
    monotone = all(ag_series[i] >= ag_series[i + 1] - 1.0 for i in range(len(ag_series) - 1))

    # cross-sectional: GDP-crisis AUC in high vs low agriculture, per modern MI year
    panel = L.load_mi_panel(); rows = panel["rows"]
    dom = L.domestic_years()
    cross = {}
    for y in L.MI_YEARS:
        recs = []
        for iso, r in rows.items():
            e = r["years"].get(str(y))
            if not e or e.get("logGDP") is None or e.get("P1") is None:
                continue
            ag = L.wdi_val(wdi, "agriculture_pct_gdp", iso, y)
            if ag is None:
                continue
            lab = 1 if any(y <= oy <= y + L.WINDOW for oy in dom.get(iso, set())) else 0
            recs.append({"iso": iso, "logGDP": e["logGDP"], "P1": e["P1"], "ag": ag, "lab": lab})
        hi = [r for r in recs if r["ag"] >= 25]
        lo = [r for r in recs if r["ag"] < 10]
        def auc_grp(g):
            if len(g) < 12 or len({r["lab"] for r in g}) < 2:
                return None, sum(r["lab"] for r in g), len(g)
            wa = L.auc_roc([-r["logGDP"] for r in g], [r["lab"] for r in g])
            return round(float(wa), 4), sum(r["lab"] for r in g), len(g)
        wa_hi, np_hi, n_hi = auc_grp(hi)
        wa_lo, np_lo, n_lo = auc_grp(lo)
        cross[y] = {"high_ag(>=25%)": {"gdp_auc": wa_hi, "n": n_hi, "n_pos": np_hi},
                    "low_ag(<10%)": {"gdp_auc": wa_lo, "n": n_lo, "n_pos": np_lo}}
    # aggregate direction: pooled across years
    def pooled_auc(cond):
        recs = []
        for y in L.MI_YEARS:
            for iso, r in rows.items():
                e = r["years"].get(str(y))
                if not e or e.get("logGDP") is None:
                    continue
                ag = L.wdi_val(wdi, "agriculture_pct_gdp", iso, y)
                if ag is None or not cond(ag):
                    continue
                lab = 1 if any(y <= oy <= y + L.WINDOW for oy in dom.get(iso, set())) else 0
                recs.append((-e["logGDP"], lab))
        if len({r[1] for r in recs}) < 2:
            return None, len(recs)
        return round(float(L.auc_roc([r[0] for r in recs], [r[1] for r in recs])), 4), len(recs)
    pooled_hi = pooled_auc(lambda a: a >= 25)
    pooled_lo = pooled_auc(lambda a: a < 10)
    confirm = monotone and (pooled_hi[0] is not None and pooled_lo[0] is not None and pooled_hi[0] < pooled_lo[0])
    return {"longitudinal_sector_share": longitudinal,
            "agriculture_trend": ag_trend, "agriculture_monotone_decline": bool(monotone),
            "cross_sectional_gdp_auc": cross,
            "pooled_gdp_auc": {"high_ag": {"auc": pooled_hi[0], "n": pooled_hi[1]},
                               "low_ag": {"auc": pooled_lo[0], "n": pooled_lo[1]}},
            "historical_context_note": "agriculture ~60-70% of GDP mid-19thc -> ~4% today is documented economic-history (Maddison/Broadberry); cited as context, not recomputed here.",
            "GATE_confirm": bool(confirm)}


# ============================================================ Test 3
def test3():
    rol, gdp = L.load_rol_gdp()
    dom = L.domestic_years()
    uni = set(rol) & set(gdp)

    def build_xy(y, isos):
        R, G, lab = [], [], []
        for iso in isos:
            if iso.startswith("OWID"):
                continue
            r = rol[iso].get(str(y)); g0 = gdp[iso].get(y)
            if r is None or g0 is None or g0 <= 0:
                continue
            l = 1 if any(y <= oy <= y + L.WINDOW for oy in dom.get(iso, set())) else 0
            R.append(float(r)); G.append(-math.log(g0)); lab.append(l)
        return R, G, lab

    def three_models(R, G, lab):
        n = len(lab)
        if n < 15 or len(set(lab)) < 2:
            return None
        y = np.array(lab, float)
        Rz, Gz = L.zscore(R), L.zscore(G)
        ones = np.ones(n)
        # M1 P1(=−rol so higher→crisis)
        X1 = np.column_stack([ones, -Rz]); b1, a1, _ = L.logit_fit(X1, y)
        X2 = np.column_stack([ones, Gz]); b2, a2, _ = L.logit_fit(X2, y)
        X3 = np.column_stack([ones, -Rz, Gz]); b3, a3, _ = L.logit_fit(X3, y)
        se3 = L.logit_coef_se(X3, y, b3)
        return {"n": n, "n_pos": int(y.sum()),
                "M1_P1": {"coef": round(float(b1[1]), 4), "auc": round(float(a1), 4)},
                "M2_GDP": {"coef": round(float(b2[1]), 4), "auc": round(float(a2), 4)},
                "M3_both": {"P1_coef": round(float(b3[1]), 4), "P1_se": round(float(se3[1]), 4),
                            "P1_z": round(float(b3[1] / se3[1]), 2) if se3[1] and not math.isnan(se3[1]) else None,
                            "GDP_coef": round(float(b3[2]), 4), "GDP_se": round(float(se3[2]), 4),
                            "GDP_z": round(float(b3[2] / se3[2]), 2) if se3[2] and not math.isnan(se3[2]) else None,
                            "auc": round(float(a3), 4)},
                "M3_vs_M1_auc_gain": round(float(a3 - a1), 4)}

    holdout = {}
    for y in [2004, 2012]:
        R, G, lab = build_xy(y, uni)
        holdout[y] = three_models(R, G, lab)
    historical = {}
    for y in L.EPOCHS:
        R, G, lab = build_xy(y, uni)
        m = three_models(R, G, lab)
        if m:
            historical[y] = m
    # trend of GDP independent |coef| over epochs
    ys = sorted(historical)
    gdp_coefs = [abs(historical[y]["M3_both"]["GDP_coef"]) for y in ys]
    p1_coefs = [abs(historical[y]["M3_both"]["P1_coef"]) for y in ys]
    return {"holdout_2004_2012": holdout, "historical_epochs": historical,
            "GDP_indep_coef_trend": L.trend(ys, gdp_coefs),
            "P1_indep_coef_trend": L.trend(ys, p1_coefs)}


# ============================================================ Test 4
EARLY = {"GBR", "FRA", "DEU", "USA", "BEL", "NLD", "CHE", "AUT"}
MID = {"JPN", "RUS", "ITA", "SWE", "NOR", "DNK", "ESP", "CAN", "AUS", "CZE"}


def test4():
    groups = {"early": EARLY, "mid": MID}
    lab = L.domestic_label_fn()
    rol, gdp = L.load_rol_gdp()
    uni = set(rol) & set(gdp)
    late = uni - EARLY - MID
    groups["late"] = late
    res = {}
    for name, isos in groups.items():
        pts = L.epoch_decomp(lab, isos_filter=isos)
        # first epoch where wealth_auc >= 0.65
        first_hi = next((p["year"] for p in pts if p["wealth_auc"] is not None and p["wealth_auc"] >= 0.65), None)
        valid = [(p["year"], p["wealth_auc"]) for p in pts if p["wealth_auc"] is not None]
        tr = L.trend([v[0] for v in valid], [v[1] for v in valid]) if len(valid) >= 3 else None
        res[name] = {"n_states": len(isos), "curve": pts,
                     "first_epoch_wealth_auc>=0.65": first_hi, "wealth_auc_trend": tr}
    return res


# ============================================================ Test 5
def test5():
    wdi = L.load_wdi()
    panel = L.load_mi_panel(); rows = panel["rows"]
    dom = L.domestic_years()

    def group_signal(cond):
        R, G, lab = [], [], []
        for y in L.MI_YEARS:
            for iso, r in rows.items():
                e = r["years"].get(str(y))
                if not e or e.get("logGDP") is None or e.get("P1") is None:
                    continue
                ag = L.wdi_val(wdi, "agriculture_pct_gdp", iso, y)
                if ag is None or not cond(ag):
                    continue
                l = 1 if any(y <= oy <= y + L.WINDOW for oy in dom.get(iso, set())) else 0
                R.append(e["P1"]); G.append(e["logGDP"]); lab.append(l)
        if len(lab) < 12 or len(set(lab)) < 2:
            return {"n": len(lab), "n_pos": int(sum(lab)), "note": "insufficient"}
        sa = L.auc_roc([-v for v in R], lab)   # institutions protect
        wa = L.auc_roc([-v for v in G], lab)
        return {"n": len(lab), "n_pos": int(sum(lab)),
                "struct_auc": round(float(sa), 4), "wealth_auc": round(float(wa), 4),
                "spread": round(float(sa - wa), 4)}
    agri = group_signal(lambda a: a >= 25)
    indus = group_signal(lambda a: a < 10)
    confirm = (isinstance(agri.get("spread"), float) and isinstance(indus.get("spread"), float)
               and agri["spread"] > indus["spread"])
    return {"agricultural(ag>=25%)": agri, "industrial(ag<10%)": indus,
            "confirm_direction": bool(confirm),
            "power_caveat": "agricultural-economy sample is small and concentrated in low-data-quality regions; direction reported with caveat."}


# ============================================================ Test 6
def test6():
    """Dysfunction outcome decomposition. Modern segment uses committed dysfunction
    components; historical uses Polity2-decline + GDP-decline + UCDP where available."""
    # Longitudinal decomposition on the historical rol+gdp panel using a GDP-decline +
    # conflict composite (Polity/FSI unavailable / sparse across the full 1816-1996 span).
    rol, gdp = L.load_rol_gdp()
    onsets = L.all_onset_years(tag=None)  # any conflict onset
    uni = set(rol) & set(gdp)

    def dysfunction_label(iso, y):
        # component 1: any conflict onset in window
        if any(y <= oy <= y + L.WINDOW for oy in onsets.get(iso, set())):
            return 1
        # component 2: GDP-pc decline >=15% from a rolling peak within window
        g = gdp.get(iso, {})
        peak = None; hit = False
        for yy in range(y, y + L.WINDOW + 1):
            v = g.get(yy)
            if v is None or v <= 0:
                continue
            if peak is None or v > peak:
                peak = v
            elif v <= 0.85 * peak:
                hit = True
                break
        return 1 if hit else 0

    pts = L.epoch_decomp(dysfunction_label)
    valid = [p for p in pts if p["struct_auc"] is not None]
    ys = [p["year"] for p in valid]
    sa = [p["struct_auc"] for p in valid]; wa = [p["wealth_auc"] for p in valid]
    return {"curve": pts,
            "struct_auc_trend": L.trend(ys, sa), "wealth_auc_trend": L.trend(ys, wa),
            "struct_auc_delta": round(sa[-1] - sa[0], 4), "wealth_auc_delta": round(wa[-1] - wa[0], 4),
            "outcome": "composite dysfunction = conflict onset OR GDP-pc decline>=15% from peak in window",
            "note": "Polity2/FSI components unavailable across the full 1816-1996 span; historical dysfunction here = conflict+GDP-collapse composite. Modern-only Polity/FSI dysfunction is in Finding-9-B2."}


def main():
    out = {"prereg_sha256": "4071b996", "window": L.WINDOW,
           "test1_coupling_trajectory": test1(),
           "test2_sector_shift": test2(),
           "test3_mediation": test3(),
           "test4_diffusion": test4(),
           "test5_agricultural_economies": test5(),
           "test6_dysfunction_outcome": test6()}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))

    t1 = out["test1_coupling_trajectory"]
    print("=== TEST 1 (GATE) — P1<->GDP coupling trajectory ===")
    for name in ["pooled", "constant", "mature"]:
        t = t1["trajectories"][name]
        per = t["per_epoch"]
        line = " ".join(f"{y}:{per[y]['pearson_r']}" for y in sorted(per))
        print(f"  {name} (n_set={t['n_set']}): {line}")
        print(f"     Δr={t['delta_r']} trend={t['r_trend']}")
    print("  F14 epochs (pooled r | wealth_auc | struct_auc):")
    for y, v in t1["f14_epochs"].items():
        print(f"    {y}: r={v['pooled_pearson_r']} wealth_auc={v['wealth_auc']} struct_auc={v['struct_auc']}")
    print(f"  coupling-vs-wealth_auc: pooled {t1['coupling_vs_wealth_auc']['pooled']} | mature {t1['coupling_vs_wealth_auc']['mature']}")
    print(f"  >>> TEST 1 CONFIRM: {t1['GATE_confirm']}")

    t2 = out["test2_sector_shift"]
    print("\n=== TEST 2 (GATE) — sector composition shift ===")
    for y in sorted(t2["longitudinal_sector_share"]):
        v = t2["longitudinal_sector_share"][y]
        print(f"  {y}: ag={v['agriculture']}% ind={v['industry']}% svc={v['services']}% (n={v['n']})")
    print(f"  agriculture trend slope={t2['agriculture_trend']['slope']:.4f} p={t2['agriculture_trend']['p']:.4f} monotone={t2['agriculture_monotone_decline']}")
    print(f"  pooled GDP-crisis AUC: high-ag={t2['pooled_gdp_auc']['high_ag']} low-ag={t2['pooled_gdp_auc']['low_ag']}")
    print(f"  >>> TEST 2 CONFIRM: {t2['GATE_confirm']}")

    t3 = out["test3_mediation"]
    print("\n=== TEST 3 (MECHANISM) — GDP through P1 ===")
    for y in [2004, 2012]:
        m = t3["holdout_2004_2012"][y]
        if m:
            print(f"  {y}: M1(P1)auc={m['M1_P1']['auc']} M2(GDP)auc={m['M2_GDP']['auc']} M3auc={m['M3_both']['auc']} (gain over M1={m['M3_vs_M1_auc_gain']})")
            print(f"       M3: P1 coef={m['M3_both']['P1_coef']} (z={m['M3_both']['P1_z']}) | GDP coef={m['M3_both']['GDP_coef']} (z={m['M3_both']['GDP_z']})")
    print(f"  GDP indep |coef| trend over epochs: {t3['GDP_indep_coef_trend']}")
    print(f"  P1  indep |coef| trend over epochs: {t3['P1_indep_coef_trend']}")

    t4 = out["test4_diffusion"]
    print("\n=== TEST 4 — industrialization diffusion (first epoch wealth_auc>=0.65) ===")
    for g in ["early", "mid", "late"]:
        v = t4[g]
        totpos = sum(p["n_pos"] for p in v["curve"])
        print(f"  {g} (n={v['n_states']}, total domestic-crisis obs across epochs={totpos}): "
              f"first_hi={v['first_epoch_wealth_auc>=0.65']} trend={v['wealth_auc_trend']}")
        wa = " ".join(f"{p['year']}:{p['wealth_auc'] if p['wealth_auc'] is not None else 'NA'}(np{p['n_pos']})" for p in v["curve"])
        print(f"     wealth_auc: {wa}")

    t5 = out["test5_agricultural_economies"]
    print("\n=== TEST 5 — agricultural vs industrial economies (modern) ===")
    print(f"  agricultural: {t5['agricultural(ag>=25%)']}")
    print(f"  industrial:   {t5['industrial(ag<10%)']}")
    print(f"  >>> spread(agri) > spread(indus)? {t5['confirm_direction']}")

    t6 = out["test6_dysfunction_outcome"]
    print("\n=== TEST 6 — dysfunction outcome replication ===")
    print(f"  struct_auc Δ={t6['struct_auc_delta']} (slope p={t6['struct_auc_trend']['p']:.3f}) | "
          f"wealth_auc Δ={t6['wealth_auc_delta']} (slope p={t6['wealth_auc_trend']['p']:.3f})")


if __name__ == "__main__":
    main()
