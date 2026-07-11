#!/usr/bin/env python3
"""ESI Phase 2 — test the mechanism (ESI_PREREGISTRATION.md Tests 2A-2D).

Runs against the FROZEN joined holdout panel (temporal_holdout_panel.json) and the
built ESI (esi_scores.json). Does NOT re-derive crisis labels or optimize ESI.

  2A  Does ESI predict which countries the durability gate gets wrong?
  2B  Does controlling for ESI recover the institutional signal? (make-or-break)
  2D  Concentration & fragility among high-ESI states.
  (2C historical is a separate script if a historical ESI proxy is built.)

Structural predictor (specified here, before running): the P4-P1 durability GAP
(higher = economy outruns institutions = more structurally vulnerable) — the exact
signal Safeguard J / Finding 5 is about. mi_score (overall) reported as a variant.

    python scripts/robustness/esi_tests.py
"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

ESIDIR = ROOT / "data" / "robustness" / "esi"
PANEL = ROOT / "data" / "robustness" / "temporal_holdout_panel.json"
GDP_RAW = ROOT / "data" / "robustness" / "outcomes" / "gdp_pcap_ppp_kd_raw.json"
OUT = ESIDIR / "esi_test_report.json"
L2 = 1e-3  # tiny ridge on standardized predictors: numerical stability, consistent across models


def auc_roc(scores, labels):
    """Mann-Whitney AUC (higher score -> higher predicted crisis)."""
    s = np.asarray(scores, float); y = np.asarray(labels, int)
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    ranks = stats.rankdata(s)
    return (ranks[y == 1].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))


def zscore(x):
    x = np.asarray(x, float); sd = x.std()
    return (x - x.mean()) / sd if sd > 0 else x - x.mean()


def logit_fit(X, y):
    """Ridge-regularized logistic MLE via BFGS. X already includes intercept col.
    Returns (coef, auc, loglik). Predictors (non-intercept) should be standardized."""
    X = np.asarray(X, float); y = np.asarray(y, float)
    n, k = X.shape

    def nll(b):
        z = X @ b
        # stable log(1+exp(z))
        ll = np.sum(y * z - np.logaddexp(0.0, z))
        pen = L2 * np.sum(b[1:] ** 2)  # don't penalize intercept
        return -ll + pen

    res = minimize(nll, np.zeros(k), method="BFGS")
    b = res.x
    p = 1.0 / (1.0 + np.exp(-(X @ b)))
    return b, auc_roc(p, y), -nll(b)


def cliffs_delta(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    gt = sum((x > y) for x in a for y in b)
    lt = sum((x < y) for x in a for y in b)
    return (gt - lt) / (len(a) * len(b)) if len(a) and len(b) else float("nan")


def cohens_d(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return float("nan")
    sp = np.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    return (a.mean() - b.mean()) / sp if sp > 0 else float("nan")


def load_window(window):
    panel = json.loads(PANEL.read_text())["windows"][window]
    esi = json.loads((ESIDIR / "esi_scores.json").read_text())["esi"]
    yr = int(window)
    rows = []
    for r in panel:
        e = esi.get(r["iso"], {}).get(str(yr), {})
        rows.append({**r, "esi": e.get("ESI"), "esi_sub": e.get("sub_dimensions", {})})
    return rows, yr


def gdp_baseyear(iso, year):
    return _GDP.get(iso, {}).get(year)


def test_2A(rows):
    """Mean ESI by gate confusion bucket; FP vs TP effect size."""
    have = [r for r in rows if r["esi"] is not None]
    buckets = {"TP": [], "FP": [], "FN": [], "TN": []}
    for r in have:
        el, cr = bool(r["elevated"]), bool(r["crisis"])
        key = ("TP" if el and cr else "FP" if el and not cr else
               "FN" if (not el) and cr else "TN")
        buckets[key].append(r["esi"])
    summary = {k: {"n": len(v), "mean_esi": round(float(np.mean(v)), 4) if v else None,
                   "median_esi": round(float(np.median(v)), 4) if v else None} for k, v in buckets.items()}
    fp, tp = buckets["FP"], buckets["TP"]
    test = {}
    if len(fp) >= 2 and len(tp) >= 2:
        u, p = stats.mannwhitneyu(fp, tp, alternative="two-sided")
        t, pt = stats.ttest_ind(fp, tp, equal_var=False)
        test = {"FP_mean": round(float(np.mean(fp)), 4), "TP_mean": round(float(np.mean(tp)), 4),
                "mannwhitney_U": float(u), "mannwhitney_p": float(p),
                "welch_t": float(t), "welch_p": float(pt),
                "cliffs_delta_FP_vs_TP": round(cliffs_delta(fp, tp), 4),
                "cohens_d_FP_vs_TP": round(cohens_d(fp, tp), 4),
                "hypothesis": "FP ESI > TP ESI (propped-up states flagged, no crisis)"}
    return {"n_scored": len(have), "buckets": summary, "FP_vs_TP": test}


def test_2B(rows, yr):
    """Logistic regressions: does adding ESI raise the MI structural coefficient / AUC?"""
    have = [r for r in rows if r["esi"] is not None and r["P4"] is not None and r["P1"] is not None]
    y = np.array([1 if r["crisis"] else 0 for r in have])
    gap = zscore([r["P4"] - r["P1"] for r in have])       # MI structural vulnerability (durability gap)
    esi = zscore([r["esi"] for r in have])
    mi_overall = zscore([r["mi_score"] for r in have if r["mi_score"] is not None])
    n = len(have); ones = np.ones(n)

    def fit(cols, names):
        X = np.column_stack([ones] + cols)
        b, auc, ll = logit_fit(X, y)
        return {"coef": {nm: round(float(c), 4) for nm, c in zip(["intercept"] + names, b)},
                "auc": round(auc, 4), "loglik": round(ll, 3), "n": n}

    m1 = fit([gap], ["MI_gap"])
    m2 = fit([gap, esi], ["MI_gap", "ESI"])
    m3 = fit([gap, esi, gap * esi], ["MI_gap", "ESI", "MI_gap_x_ESI"])

    # baselines: GDPpc + ESI, FSI + ESI (FSI only where available)
    gdp = [gdp_baseyear(r["iso"], yr) for r in have]
    base = {}
    if all(g is not None for g in gdp):
        lgdp = zscore(np.log(gdp))
        base["gdppc_only"] = fit([lgdp], ["lnGDPpc"])
        base["gdppc_plus_esi"] = fit([lgdp, esi], ["lnGDPpc", "ESI"])
    fsi = [_FSI.get(r["iso"], {}).get(yr) for r in have]
    if sum(f is not None for f in fsi) >= 0.8 * n:
        idx = [i for i, f in enumerate(fsi) if f is not None]
        yf = y[idx]; of = np.ones(len(idx))
        fz = zscore([fsi[i] for i in idx]); ez = zscore([esi[i] for i in idx])
        def fitf(cols, names):
            X = np.column_stack([of] + cols); b, auc, ll = logit_fit(X, yf)
            return {"coef": {nm: round(float(c), 4) for nm, c in zip(["intercept"] + names, b)},
                    "auc": round(auc, 4), "n": len(idx)}
        base["fsi_only"] = fitf([fz], ["FSI"])
        base["fsi_plus_esi"] = fitf([fz, ez], ["FSI", "ESI"])

    recovery = {
        "MI_gap_coef_M1": m1["coef"]["MI_gap"],
        "MI_gap_coef_M2_with_ESI": m2["coef"]["MI_gap"],
        "coef_increased": abs(m2["coef"]["MI_gap"]) > abs(m1["coef"]["MI_gap"]),
        "auc_M1": m1["auc"], "auc_M2": m2["auc"], "auc_M3": m3["auc"],
        "auc_gain_M2_over_M1": round(m2["auc"] - m1["auc"], 4),
    }

    # Pre-registered variant: overall mi_score as the structural predictor (-mi_score so
    # higher = more vulnerable, consistent direction with the gap).
    variant = {}
    if all(r["mi_score"] is not None for r in have):
        mineg = zscore([-r["mi_score"] for r in have])
        v1 = fit([mineg], ["negMI"]); v2 = fit([mineg, esi], ["negMI", "ESI"])
        variant = {"model1_negMI": v1, "model2_negMI_ESI": v2,
                   "negMI_coef_M1": v1["coef"]["negMI"], "negMI_coef_M2_with_ESI": v2["coef"]["negMI"],
                   "coef_increased": abs(v2["coef"]["negMI"]) > abs(v1["coef"]["negMI"]),
                   "auc_M1": v1["auc"], "auc_M2": v2["auc"]}

    return {"n": n, "model1_MI_only": m1, "model2_MI_ESI": m2, "model3_interaction": m3,
            "baselines": base, "signal_recovery": recovery, "variant_mi_score": variant,
            "note": "predictors z-standardized; ridge L2=%.0e consistent across models" % L2}


def test_2D(rows, yr):
    """Concentration among high-ESI (>75th pct) states across the 3 sub-dimensions."""
    have = [r for r in rows if r["esi"] is not None and r["esi_sub"]]
    if not have:
        return {}
    thr = float(np.percentile([r["esi"] for r in have], 75))
    high = [r for r in have if r["esi"] >= thr]
    out = []
    for r in high:
        subs = list(r["esi_sub"].values())
        tot = sum(subs)
        hhi = sum((s / tot) ** 2 for s in subs) if tot > 0 else None  # 0.33=even, 1=single-source
        out.append({"iso": r["iso"], "country": r["country"], "esi": round(r["esi"], 4),
                    "n_sub": len(subs), "concentration_hhi": round(hhi, 4) if hhi else None,
                    "elevated": bool(r["elevated"]), "crisis": bool(r["crisis"])})
    out.sort(key=lambda x: (-(x["concentration_hhi"] or 0), -x["esi"]))
    single_point = [x for x in out if x["concentration_hhi"] and x["concentration_hhi"] >= 0.6]
    return {"esi_75th_pct": round(thr, 4), "n_high_esi": len(high),
            "high_esi_states": out,
            "single_point_of_failure_flag": [x["iso"] for x in single_point]}


# ---- FSI + GDP loaders (base-year baselines) ----
def _load_gdp():
    out = {}
    for r in json.loads(GDP_RAW.read_text()):
        if r["value"] is not None and r["iso3"] and len(r["iso3"]) == 3:
            out.setdefault(r["iso3"], {})[r["year"]] = r["value"]
    return out


def _load_fsi():
    import csv
    out = {}
    p = ROOT.parent / "mi-pipeline" / "data" / "fsi.csv"
    if p.exists():
        for r in csv.DictReader(open(p)):
            out.setdefault(r["iso3"], {})[int(r["year"])] = float(r["FSI"])
    return out


_GDP = _load_gdp()
_FSI = _load_fsi()


def main():
    report = {"_meta": {"prereg": "docs/ESI_PREREGISTRATION.md",
                        "structural_predictor": "P4-P1 durability gap (z-standardized)",
                        "crisis_label": "frozen holdout definition (UCDP onset OR CRAG default)"},
              "windows": {}}
    for window in ("2004", "2012"):
        rows, yr = load_window(window)
        report["windows"][window] = {
            "test_2A_gate_error_esi": test_2A(rows),
            "test_2B_signal_recovery": test_2B(rows, yr),
            "test_2D_concentration": test_2D(rows, yr),
        }
    OUT.write_text(json.dumps(report, indent=1, default=str))
    for w in ("2004", "2012"):
        R = report["windows"][w]
        a = R["test_2A_gate_error_esi"]; b = R["test_2B_signal_recovery"]["signal_recovery"]
        fp = a["FP_vs_TP"]
        print(f"\n===== {w} window =====")
        print(f"2A buckets mean ESI: " + ", ".join(f"{k}={v['mean_esi']}(n{v['n']})" for k, v in a["buckets"].items()))
        if fp:
            print(f"2A FP vs TP: FP={fp['FP_mean']} TP={fp['TP_mean']} | MWU p={fp['mannwhitney_p']:.3f} "
                  f"Cliff's d={fp['cliffs_delta_FP_vs_TP']} Cohen's d={fp['cohens_d_FP_vs_TP']}")
        print(f"2B recovery: MI_gap coef {b['MI_gap_coef_M1']} -> {b['MI_gap_coef_M2_with_ESI']} "
              f"(increased={b['coef_increased']}) | AUC {b['auc_M1']} -> {b['auc_M2']} (M3 {b['auc_M3']})")
    print(f"\n-> {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
