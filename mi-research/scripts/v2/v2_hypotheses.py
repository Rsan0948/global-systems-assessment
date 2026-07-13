#!/usr/bin/env python3
"""
MI V2 pre-registered hypotheses. H4 (cross-model construct validity) FIRST as gate, then
H1/H3/H5/H6 (+ H2 best-effort). Outcome = committed domestic-onset stress (2004-2024).
Frozen spec: docs/MI_V2_PREREGISTRATION.md (sha256 93c87741). Read-only.
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
import convergence_lib as L  # noqa: E402
from mi import panel as MP  # noqa: E402
from mi.scoring import calculate_pillar_scores, calculate_mi_score  # noqa: E402

V2 = json.loads((ROOT / "data/v2/v2_scores.json").read_text())["scores"]
OUT = ROOT / "data/v2/v2_hypotheses.json"
PILL = ["F1", "F2", "F3", "F4", "F5", "F6"]
ANALYST = {"F1": 0.22, "F2": 0.22, "F6": 0.18, "F3": 0.16, "F4": 0.12, "F5": 0.10}


def weighted(scores_by_pillar, w):
    num = den = 0.0
    for p in PILL:
        v = scores_by_pillar.get(p)
        if v is not None:
            num += w[p] * v; den += w[p]
    return num / den if den > 0 else None


def corr_weights(matrix_rows):
    """matrix_rows: list of dicts pillar->value (complete cases). weight_p = mean|corr|."""
    cols = {p: np.array([r[p] for r in matrix_rows]) for p in PILL}
    w = {}
    for p in PILL:
        cs = [abs(stats.spearmanr(cols[p], cols[q]).statistic) for q in PILL if q != p]
        w[p] = float(np.mean(cs))
    s = sum(w.values())
    return {p: w[p] / s for p in PILL}


def v1_score(iso, year=2024):
    ind = MP.indicators_for(iso, year)
    if not ind:
        return None
    try:
        pil = calculate_pillar_scores(ind)
        return calculate_mi_score(pil)
    except Exception:
        return None


def domestic_outcome():
    dom = L.domestic_years()
    return {iso: (1 if any(2004 <= y <= 2024 for y in ys) else 0) for iso, ys in dom.items()}


def auc(scores, labels):
    return float(L.auc_roc(scores, labels))


def logit_auc(cols, y):
    n = len(y)
    X = np.column_stack([np.ones(n)] + [L.zscore(c) for c in cols])
    _, a, _ = L.logit_fit(X, np.array(y, float))
    return round(float(a), 4)


def main():
    isos = [i for i in V2 if V2[i]["V2_Combined"] is not None]
    out = {"n": len(isos)}

    # ===== H4 — cross-model validation (Level / Equity / Combined) =====
    # build per-country pillar L, E, and pillar-score dicts
    def pillar_dim(dim):  # 'L','E','score'
        rows = {}
        for i in isos:
            d = {}
            for p in PILL:
                if dim == "L":
                    v = V2[i]["_L"].get(p)
                elif dim == "E":
                    v = V2[i]["_E"].get(p)
                else:
                    v = V2[i]["pillars"][p]["score"]
                d[p] = v
            rows[i] = d
        return rows

    h4 = {}
    for dim in ["L", "E", "score"]:
        rows = pillar_dim(dim)
        complete = [i for i in isos if all(rows[i][p] is not None for p in PILL)]
        if len(complete) < 20:
            h4[dim] = {"note": "too few complete cases", "n": len(complete)}
            continue
        mat = [rows[i] for i in complete]
        wb = corr_weights(mat)
        schemes = {"a_equal": {p: 1 for p in PILL}, "b_corr": wb, "c_analyst": ANALYST}
        vals = {s: {i: weighted(rows[i], w) for i in complete} for s, w in schemes.items()}
        pairs = [("a_equal", "b_corr"), ("a_equal", "c_analyst"), ("b_corr", "c_analyst")]
        rhos = {}
        for x, yv in pairs:
            xs = [vals[x][i] for i in complete]; ys = [vals[yv][i] for i in complete]
            rhos[f"{x}~{yv}"] = round(float(stats.spearmanr(xs, ys).statistic), 4)
        h4[dim] = {"n_complete": len(complete), "corr_weights": {p: round(wb[p], 3) for p in PILL},
                   "pairwise_rho": rhos, "min_rho": min(rhos.values())}
    out["H4_cross_model"] = h4
    gate_pass = all(("min_rho" in h4[d] and h4[d]["min_rho"] >= 0.90) for d in ["L", "score"]) \
        and ("min_rho" in h4["E"])
    out["H4_gate_pass"] = bool(gate_pass)
    out["H4_equity_single_construct"] = bool(h4.get("E", {}).get("min_rho", 0) >= 0.90)

    # ===== outcome + V1 =====
    outc = domestic_outcome()
    rows = []
    for i in isos:
        y = outc.get(i)
        v1 = v1_score(i)
        r = V2[i]
        if y is None or v1 is None or r["V2_Level"] is None or r["V2_Equity"] is None:
            continue
        rows.append({"iso": i, "y": y, "v1": v1, "vL": r["V2_Level"], "vE": r["V2_Equity"],
                     "vC": r["V2_Combined"],
                     "spread": float(np.std([r["pillars"][p]["score"] for p in PILL
                                             if r["pillars"][p]["score"] is not None]))})
    out["n_analysis"] = len(rows)
    y = [r["y"] for r in rows]

    if len(rows) >= 30 and len(set(y)) == 2:
        # ===== H5 — does V2-Equity add beyond V1 + V2-Level? =====
        a_v1 = logit_auc([[r["v1"] for r in rows]], y)
        a_vL = logit_auc([[r["vL"] for r in rows]], y)
        a_vE = logit_auc([[r["vE"] for r in rows]], y)
        a_v1L = logit_auc([[r["v1"] for r in rows], [r["vL"] for r in rows]], y)
        a_v1LE = logit_auc([[r["v1"] for r in rows], [r["vL"] for r in rows], [r["vE"] for r in rows]], y)
        out["H5"] = {"auc_v1": a_v1, "auc_v2Level": a_vL, "auc_v2Equity": a_vE,
                     "auc_v1+v2L": a_v1L, "auc_v1+v2L+v2E": a_v1LE,
                     "equity_gain_over_v1+level": round(a_v1LE - a_v1L, 4),
                     "adds_power(gain>=0.05)": bool(a_v1LE - a_v1L >= 0.05)}

        # ===== H3 — V1-V2 gap, decomposed =====
        gapL = [[r["v1"] - r["vL"] for r in rows]]
        gapE = [[r["v1"] - r["vE"] for r in rows]]
        out["H3"] = {"auc_v1_only": a_v1, "auc_v2C_only": logit_auc([[r["vC"] for r in rows]], y),
                     "auc_gap_level": logit_auc(gapL, y), "auc_gap_equity": logit_auc(gapE, y),
                     "equity_gap_more_predictive": bool(logit_auc(gapE, y) > logit_auc(gapL, y))}

        # ===== H1 — spread beyond level =====
        out["H1"] = {"auc_combined": logit_auc([[r["vC"] for r in rows]], y),
                     "auc_spread": logit_auc([[r["spread"] for r in rows]], y),
                     "auc_combined+spread": logit_auc([[r["vC"] for r in rows], [r["spread"] for r in rows]], y),
                     "spread_adds": None}
        out["H1"]["spread_adds"] = bool(out["H1"]["auc_combined+spread"] - out["H1"]["auc_combined"] >= 0.02)

        # ===== H6 — HL-LE configuration =====
        medL = np.median([r["vL"] for r in rows]); medE = np.median([r["vE"] for r in rows])
        quad = {"HL_HE": [], "HL_LE": [], "LL_HE": [], "LL_LE": []}
        for r in rows:
            hi_L = r["vL"] >= medL; hi_E = r["vE"] >= medE
            key = ("HL_HE" if hi_L and hi_E else "HL_LE" if hi_L and not hi_E
                   else "LL_HE" if not hi_L and hi_E else "LL_LE")
            quad[key].append(r)
        stress_rate = {k: round(float(np.mean([r["y"] for r in v])), 3) if v else None for k, v in quad.items()}
        ns = {k: len(v) for k, v in quad.items()}
        out["H6"] = {"median_L": round(float(medL), 1), "median_E": round(float(medE), 1),
                     "n_by_quadrant": ns, "stress_rate_by_quadrant": stress_rate,
                     "HL_LE_vs_LL_HE": (round(stress_rate["HL_LE"] - stress_rate["LL_HE"], 3)
                                        if stress_rate["HL_LE"] is not None and stress_rate["LL_HE"] is not None else None),
                     "confirmed(HL_LE>LL_HE)": bool(stress_rate.get("HL_LE") is not None and
                                                    stress_rate.get("LL_HE") is not None and
                                                    stress_rate["HL_LE"] > stress_rate["LL_HE"])}

    # ===== US showcase =====
    if "USA" in V2:
        r = V2["USA"]
        out["US_case"] = {"V2_Level": r["V2_Level"], "V2_Equity": r["V2_Equity"], "V2_Combined": r["V2_Combined"],
                          "V1": round(v1_score("USA"), 3) if v1_score("USA") else None,
                          "pillars": {p: r["pillars"][p] for p in PILL},
                          "note": "conversion instrument: US F2(health) Level is near worst-in-class (spends most, converts least)"}

    OUT.write_text(json.dumps(out, indent=1))

    print("=== H4 (GATE) — cross-model validation ===")
    for d in ["L", "E", "score"]:
        h = out["H4_cross_model"][d]
        if "min_rho" in h:
            print(f"  {d}: pairwise ρ {h['pairwise_rho']} | min={h['min_rho']} (n={h['n_complete']})")
        else:
            print(f"  {d}: {h}")
    print(f"  >>> H4 gate pass (Level+Combined ρ≥0.90): {out['H4_gate_pass']} | Equity single construct: {out['H4_equity_single_construct']}")
    print(f"\nanalysis n={out.get('n_analysis')}")
    for h in ["H1", "H3", "H5", "H6"]:
        if h in out:
            print(f"\n=== {h} ===")
            for k, v in out[h].items():
                print(f"  {k}: {v}")
    if "US_case" in out:
        print(f"\n=== US showcase ===\n  V1={out['US_case']['V1']} | V2 L/E/C = {out['US_case']['V2_Level']}/{out['US_case']['V2_Equity']}/{out['US_case']['V2_Combined']}")
        for p in PILL:
            print(f"    {p}: {out['US_case']['pillars'][p]}")


if __name__ == "__main__":
    main()
