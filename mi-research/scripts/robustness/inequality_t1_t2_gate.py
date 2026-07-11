#!/usr/bin/env python3
"""
Inequality — Tests 1 & 2 (THE GATE). Frozen spec: docs/INEQUALITY_PREREGISTRATION.md.
  T1: does inequality predict DOMESTIC crises + does P1 recover when it's controlled?
  T2: does the Finding-12 domestic-channel erosion track mean top-10% share over epochs?
Read-only; writes data/robustness/inequality/{t1_signal,t2_longitudinal}.json.
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
from esi_tests import auc_roc, zscore, logit_fit  # noqa: E402
import erosion_component_B as B  # noqa: E402

HOLDOUT = ROOT / "data/robustness/temporal_holdout_panel.json"
CLASS = ROOT / "data/robustness/contagion/crisis_classification.json"
INEQ = ROOT / "data/robustness/inequality/inequality.json"
SPLIT = ROOT / "data/robustness/contagion/t2_split_curve.json"
OUT1 = ROOT / "data/robustness/inequality/t1_signal.json"
OUT2 = ROOT / "data/robustness/inequality/t2_longitudinal.json"


def ineq_at(series, iso, year, back=3):
    d = series.get(iso)
    if not d:
        return None
    for dy in range(0, back + 1):
        for y in (year - dy, year + dy):
            if str(y) in d:
                return d[str(y)]
    return None


def domestic_onset_years():
    """iso -> set of domestic-origin onset years (Finding-12 primary classification)."""
    data = json.loads(CLASS.read_text())["classification_primary"]
    out = defaultdict(set)
    for key, origins in data.items():
        iso, y = key.split("|")
        if "domestic" in origins:
            out[iso].add(int(y))
    return out


def test1():
    ineqdata = json.loads(INEQ.read_text())
    top10 = ineqdata["top10"]; gini = ineqdata["gini_wb"]
    holdout = json.loads(HOLDOUT.read_text())["windows"]
    dom = domestic_onset_years()
    GDP, FSI = B.load_gdp(), B.load_fsi()

    res = {"test": "T1_inequality_predicts_domestic_crises", "windows": {}}
    for win, rows in holdout.items():
        origin = int(win)
        recs = []
        for r in rows:
            if r["P1"] is None:
                continue
            ineq = ineq_at(top10, r["iso"], origin)
            dom_crisis = any(origin <= oy <= 2024 for oy in dom.get(r["iso"], set()))
            g = GDP.get(r["iso"], {}).get(origin)
            fsi = FSI.get(r["iso"], {}).get(origin) or (B.load_fsi().get(r["iso"], {}))
            recs.append({"iso": r["iso"], "P1": r["P1"], "ineq": ineq,
                         "dom": 1 if dom_crisis else 0,
                         "neg_loggdp": (-math.log(g)) if (g and g > 0) else None,
                         "fsi": FSI.get(r["iso"], {}).get(origin)})
        sub = [r for r in recs if r["ineq"] is not None]
        y = np.array([r["dom"] for r in sub], float)
        if len(sub) < 20 or len(set(y)) < 2:
            res["windows"][win] = {"n": len(sub), "note": "insufficient"}
            continue
        negp1 = zscore([1 - r["P1"] for r in sub])
        ineqz = zscore([r["ineq"] for r in sub])
        inter = zscore(negp1 * ineqz)
        ones = np.ones(len(sub))
        m1 = logit_fit(np.column_stack([ones, negp1]), y)
        m2 = logit_fit(np.column_stack([ones, ineqz]), y)
        m3 = logit_fit(np.column_stack([ones, negp1, ineqz]), y)
        m4 = logit_fit(np.column_stack([ones, negp1, ineqz, inter]), y)

        # baselines
        def auc_of(sig):
            idx = [i for i, s in enumerate(sig) if s is not None]
            if len({y[i] for i in idx}) < 2:
                return None
            return round(float(auc_roc([sig[i] for i in idx], [y[i] for i in idx])), 3)
        gdp_auc = auc_of([r["neg_loggdp"] for r in sub])
        fsi_auc = auc_of([r["fsi"] for r in sub])
        # significance of ineq-only coef via correlation test proxy: use logit + bootstrap-free t is unavailable;
        # report point-biserial corr of ineq vs outcome for a p-value
        pb = stats.pointbiserialr(y, ineqz)
        recovery = (m3[0][1] - m1[0][1]) / abs(m1[0][1]) if m1[0][1] != 0 else None
        res["windows"][win] = {
            "n": len(sub), "n_pos": int(y.sum()), "base_rate": round(float(y.mean()), 3),
            "M1_negP1": {"coef": round(float(m1[0][1]), 4), "auc": round(float(m1[1]), 3)},
            "M2_ineq": {"coef": round(float(m2[0][1]), 4), "auc": round(float(m2[1]), 3),
                        "pointbiserial_r": round(float(pb.statistic), 3), "p": round(float(pb.pvalue), 4)},
            "M3_both": {"coef_negP1": round(float(m3[0][1]), 4), "coef_ineq": round(float(m3[0][2]), 4),
                        "auc": round(float(m3[1]), 3)},
            "M4_interaction": {"coef_negP1": round(float(m4[0][1]), 4), "coef_ineq": round(float(m4[0][2]), 4),
                               "coef_inter": round(float(m4[0][3]), 4), "auc": round(float(m4[1]), 3),
                               "inter_sign": "negative(mechanism)" if m4[0][3] < 0 else "positive(null)"},
            "P1_recovery_M1_to_M3_rel": (round(float(recovery), 3) if recovery is not None else None),
            "baselines": {"gdp_only_auc": gdp_auc, "fsi_only_auc": fsi_auc},
        }
    # verdict arm A
    prim = res["windows"].get("2004", {})
    passA = False
    if "M2_ineq" in prim:
        sig = prim["M2_ineq"]["p"] < 0.05 and prim["M2_ineq"]["pointbiserial_r"] > 0
        rec = (prim["P1_recovery_M1_to_M3_rel"] or 0) >= 0.15
        passA = bool(sig or rec)
    res["arm_A_pass"] = passA
    return res


def test2():
    split = json.loads(SPLIT.read_text())
    dom_curve = {p["year"]: p["spread"] for p in split["primary"]["domestic"]["curve"]
                 if p["spread"] is not None}
    top10 = json.loads(INEQ.read_text())["top10"]
    majors = ["USA", "GBR", "FRA", "DEU", "SWE", "JPN", "ITA", "NLD", "IND", "RUS"]

    def mean_ineq(year, isos, back=3):
        vals = []
        for iso in isos:
            v = ineq_at(top10, iso, year, back)
            if v is not None:
                vals.append(v)
        return (round(float(np.mean(vals)), 2), len(vals)) if vals else (None, 0)

    epochs = {}
    for y in sorted(dom_curve):
        m_major, n_major = mean_ineq(y, majors)
        m_all, n_all = mean_ineq(y, list(top10.keys()))
        epochs[y] = {"domestic_spread": dom_curve[y],
                     "top10_majors_mean": m_major, "n_majors": n_major,
                     "top10_all_mean": m_all, "n_all": n_all}
    # correlation over epochs with major-mean available (n>=3)
    shared = [(y, e) for y, e in epochs.items() if e["top10_majors_mean"] is not None and e["n_majors"] >= 3]
    corr = None
    if len(shared) >= 4:
        xs = [e["domestic_spread"] for _, e in shared]
        ii = [e["top10_majors_mean"] for _, e in shared]
        pr = stats.pearsonr(ii, xs)
        corr = {"n_epochs": len(shared), "pearson_r": round(float(pr.statistic), 3),
                "p": round(float(pr.pvalue), 4),
                "span": [shared[0][0], shared[-1][0]]}
    # Piketty-U fingerprint: mid-century (1916-1976) mean spread vs tails
    def mean_spread(lo, hi):
        v = [e["domestic_spread"] for y, e in epochs.items() if lo <= y <= hi]
        return round(float(np.mean(v)), 4) if v else None
    fingerprint = {
        "pre1914_tail_spread(1876-1906)": mean_spread(1876, 1906),
        "compression_spread(1916-1976)": mean_spread(1916, 1976),
        "post1980_tail_spread(1986-1996)": mean_spread(1986, 1996),
        "note": "hypothesis: spread HIGHER during 1914-1980 compression than in the "
                "high-inequality tails. Monotonic decline through compression => no U-fingerprint."}
    # US vs SE compression sensitivity (descriptive)
    def traj(iso, yrs):
        return {y: ineq_at(top10, iso, y, 3) for y in yrs}
    yrs = [1930, 1950, 1970, 1990, 2010]
    usse = {"USA": traj("USA", yrs), "SWE": traj("SWE", yrs)}

    passB = bool(corr and corr["pearson_r"] <= -0.4)
    return {"test": "T2_domestic_erosion_vs_inequality", "epochs": epochs,
            "correlation_over_epochs": corr, "piketty_U_fingerprint": fingerprint,
            "US_vs_SE_top10_trajectory": usse, "arm_B_pass": passB}


def main():
    t1 = test1(); t2 = test2()
    OUT1.write_text(json.dumps(t1, indent=1))
    OUT2.write_text(json.dumps(t2, indent=1))

    print("=== TEST 1 — inequality predicts domestic crises? ===")
    for win, w in t1["windows"].items():
        if "M2_ineq" not in w:
            print(f"  {win}: {w.get('note')}"); continue
        print(f"  window {win} (n={w['n']} pos={w['n_pos']} base={w['base_rate']}):")
        print(f"    M2 ineq-only: coef={w['M2_ineq']['coef']} auc={w['M2_ineq']['auc']} "
              f"pb_r={w['M2_ineq']['pointbiserial_r']} p={w['M2_ineq']['p']}")
        print(f"    M1 negP1 coef={w['M1_negP1']['coef']} (auc {w['M1_negP1']['auc']}) -> "
              f"M3 negP1 coef={w['M3_both']['coef_negP1']} | recovery={w['P1_recovery_M1_to_M3_rel']}")
        print(f"    M4 interaction={w['M4_interaction']['coef_inter']} ({w['M4_interaction']['inter_sign']})")
        print(f"    baselines: gdp_auc={w['baselines']['gdp_only_auc']} fsi_auc={w['baselines']['fsi_only_auc']}")
    print(f"  >>> ARM A PASS: {t1['arm_A_pass']}")

    print("\n=== TEST 2 — domestic-channel erosion vs mean top-10% share over epochs ===")
    for y, e in t2["epochs"].items():
        if e["top10_majors_mean"] is not None:
            print(f"  {y}: dom_spread={e['domestic_spread']:+.4f} | top10_majors={e['top10_majors_mean']}"
                  f"(n{e['n_majors']}) all={e['top10_all_mean']}(n{e['n_all']})")
    c = t2["correlation_over_epochs"]
    print(f"  correlation (top10 vs domestic spread): {c}")
    print(f"  Piketty-U: {t2['piketty_U_fingerprint']}")
    print(f"  >>> ARM B PASS: {t2['arm_B_pass']}")

    both_fail = (not t1["arm_A_pass"]) and (not t2["arm_B_pass"])
    print(f"\n>>> GATE: armA={t1['arm_A_pass']} armB={t2['arm_B_pass']} -> "
          f"{'BOTH FAIL — STOP' if both_fail else 'proceed (>=1 arm)'}")


if __name__ == "__main__":
    main()
