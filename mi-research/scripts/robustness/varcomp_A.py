#!/usr/bin/env python3
"""
Candidate A — variance compression. A1 (gate) P1/rol variance decline; A2 tracks
erosion + attenuation sufficiency; A3 Thorndike Case II range-restriction correction
(definitive); A4 P10/P90 structure; A5 V-Dem long-run. Frozen spec:
docs/VARIANCE_COMPRESSION_PREREGISTRATION.md. Read-only.
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
import decoupling_panel as dp  # noqa: E402
import erosion_component_B as B  # noqa: E402

CLASS = ROOT / "data/robustness/contagion/crisis_classification.json"
OUT = ROOT / "data/robustness/varcomp/candidate_A.json"
MI_YEARS = [1996, 2004, 2012, 2018, 2024]
WINDOW = 25


def _ser(v):
    return json.loads(v) if isinstance(v, str) else v


def disp(vals):
    a = np.array(vals, float)
    if len(a) < 4:
        return None
    return {"n": len(a), "sd": float(a.std(ddof=1)),
            "iqr": float(np.percentile(a, 75) - np.percentile(a, 25)),
            "range": float(a.max() - a.min()), "mean": float(a.mean()),
            "cv": float(a.std(ddof=1) / a.mean()) if a.mean() else None,
            "p10": float(np.percentile(a, 10)), "p90": float(np.percentile(a, 90))}


def trend(xs, ys):
    r = stats.linregress(xs, ys)
    return {"slope": float(r.slope), "p": float(r.pvalue), "r": float(r.rvalue)}


def load_rol_gdp():
    vdem = json.loads(B.VDEM.read_text())
    longrun = json.loads(B.LONGRUN.read_text())
    rol = {i: _ser(v["rol"]) for i, v in vdem.items() if "rol" in v}
    gdp = {i: {int(y): val for y, val in _ser(v["P4_gdp"]).items()}
           for i, v in longrun.items() if "P4_gdp" in v}
    return rol, gdp


def domestic_years():
    data = json.loads(CLASS.read_text())["classification_primary"]
    out = defaultdict(set)
    for key, origins in data.items():
        iso, y = key.split("|")
        if "domestic" in origins:
            out[iso].add(int(y))
    return out


# ---------- A1 modern P1 variance ----------
def a1_modern():
    pnl = dp.load(); rows = pnl["rows"]
    out = {}
    for y in MI_YEARS:
        vals = [rows[iso]["years"][str(y)]["P1"] for iso in rows
                if str(y) in rows[iso]["years"] and rows[iso]["years"][str(y)]["P1"] is not None]
        out[y] = disp(vals)
    sds = [out[y]["sd"] for y in MI_YEARS]
    return {"per_year": out, "sd_trend": trend(MI_YEARS, sds),
            "sd_rel_decline": round((sds[0] - sds[-1]) / sds[0], 3)}


# ---------- A1/A5 historical rol variance ----------
def a5_rol_variance():
    rol, _ = load_rol_gdp()
    epochs = list(range(1850, 2017, 10))
    out = {}
    for y in epochs:
        vals = [float(rol[i][str(y)]) for i in rol if str(y) in rol[i] and rol[i][str(y)] is not None]
        d = disp(vals)
        if d:
            out[y] = d
    ys = sorted(out)
    sds = [out[y]["sd"] for y in ys]
    return {"per_decade": out, "sd_trend": trend(ys, sds),
            "sd_rel_decline": round((sds[0] - sds[-1]) / sds[0], 3),
            "span": [ys[0], ys[-1]]}


# ---------- A2/A3 on the committed domestic-curve panel ----------
def domestic_panel_curve():
    """Per epoch: rol SD, point-biserial r(rol,domestic-onset), struct/wealth auc."""
    rol, gdp = load_rol_gdp()
    dom = domestic_years()
    from esi_tests import auc_roc
    pts = []
    for y in range(1816, 1997, 10):
        rvals, labels = [], []
        for iso in set(rol) & set(gdp):
            if iso.startswith("OWID"):
                continue
            r = rol[iso].get(str(y)); g0 = gdp[iso].get(y)
            if r is None or g0 is None or g0 <= 0:
                continue
            lab = 1 if any(y <= oy <= y + WINDOW for oy in dom.get(iso, set())) else 0
            rvals.append(float(r)); labels.append(lab)
        if len(rvals) < 12 or len(set(labels)) < 2:
            continue
        rvals = np.array(rvals); labels = np.array(labels)
        pb = stats.pointbiserialr(labels, rvals)  # high rol -> fewer crises => negative
        signal = -float(pb.statistic)              # positive = institutions protect
        struct_auc = float(auc_roc((-rvals).tolist(), labels.tolist()))
        pts.append({"year": y, "n": len(rvals), "n_pos": int(labels.sum()),
                    "rol_sd": float(rvals.std(ddof=1)), "signal_negpb": round(signal, 4),
                    "r_struct": round(float(pb.statistic), 4), "struct_auc": round(struct_auc, 4)})
    return pts


def thorndike_correct(r_obs, u):
    """Case II: correct restricted r_obs up to unrestricted, u = SD_epoch/SD_ref (<1)."""
    inv = 1.0 / u
    return r_obs * inv / math.sqrt(1 - r_obs ** 2 + r_obs ** 2 * inv ** 2)


def attenuate(r_unrestricted, u):
    """Predicted restricted r given unrestricted r and u = SD_epoch/SD_ref."""
    return r_unrestricted * u / math.sqrt(1 - r_unrestricted ** 2 + r_unrestricted ** 2 * u ** 2)


def a2_a3(pts):
    ys = [p["year"] for p in pts]
    sd = [p["rol_sd"] for p in pts]
    sig = [abs(p["r_struct"]) for p in pts]  # magnitude of institution->crisis correlation
    sd_ref = sd[0]
    # A2 correlation SD vs signal
    corr = stats.pearsonr(sd, sig)
    # A2 sufficiency: predicted attenuation from earliest signal + SD ratios
    r_unrestricted = sig[0]
    predicted = [attenuate(r_unrestricted, s / sd_ref) for s in sd]
    actual_decline = sig[0] - sig[-1]
    predicted_decline = predicted[0] - predicted[-1]
    pct_explained = round(predicted_decline / actual_decline, 3) if actual_decline else None
    # A3 Thorndike correction
    corrected = [thorndike_correct(p["r_struct"], s / sd_ref) for p, s in zip(pts, sd)]
    raw = [p["r_struct"] for p in pts]  # signed (negative)
    raw_slope = trend(ys, [abs(r) for r in raw])
    corr_slope = trend(ys, [abs(c) for c in corrected])
    return {
        "epochs": ys, "rol_sd": [round(s, 4) for s in sd],
        "signal_abs_r_struct": [round(s, 4) for s in sig],
        "A2_sd_vs_signal_corr": {"pearson_r": round(float(corr.statistic), 3), "p": round(float(corr.pvalue), 4)},
        "A2_sufficiency": {"actual_signal_decline": round(actual_decline, 4),
                           "attenuation_predicted_decline": round(predicted_decline, 4),
                           "pct_explained_by_range_restriction": pct_explained},
        "A3_raw_abs_r": [round(abs(r), 4) for r in raw],
        "A3_corrected_abs_r": [round(abs(c), 4) for c in corrected],
        "A3_raw_slope": raw_slope, "A3_corrected_slope": corr_slope,
        "A3_corrected_flat": bool(abs(corr_slope["slope"]) < 0.5 * abs(raw_slope["slope"])
                                  and corr_slope["p"] > 0.05),
    }


def struct_vs_wealth_decomp():
    split = json.loads(ROOT.joinpath("data/robustness/contagion/t2_split_curve.json").read_text())
    dc = split["primary"]["domestic"]["curve"]
    ys = [p["year"] for p in dc if p.get("struct_auc") is not None]
    sa = [p["struct_auc"] for p in dc if p.get("struct_auc") is not None]
    wa = [p["wealth_auc"] for p in dc if p.get("wealth_auc") is not None]
    return {"struct_auc_trend": trend(ys, sa), "wealth_auc_trend": trend(ys, wa),
            "struct_auc_delta": round(sa[-1] - sa[0], 4), "wealth_auc_delta": round(wa[-1] - wa[0], 4)}


def main():
    a1m = a1_modern()
    a5 = a5_rol_variance()
    pts = domestic_panel_curve()
    a2a3 = a2_a3(pts)
    decomp = struct_vs_wealth_decomp()
    gate_pass = (a5["sd_rel_decline"] >= 0.10) or (a1m["sd_rel_decline"] >= 0.10)

    out = {"candidate": "A_variance_compression",
           "A1_modern_P1_variance": a1m, "A5_rol_variance_longrun": a5,
           "A1_gate_pass": gate_pass,
           "domestic_panel_curve": pts, "A2_A3": a2a3,
           "spread_decomposition_struct_vs_wealth": decomp}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))

    print("=== A1 GATE — institutional variance decline ===")
    print("  modern P1 SD:", {y: round(a1m["per_year"][y]["sd"], 3) for y in MI_YEARS},
          f"rel_decline={a1m['sd_rel_decline']} trend_p={a1m['sd_trend']['p']:.3f}")
    rd = a5["per_decade"]
    print(f"  V-Dem rol SD {a5['span'][0]}-{a5['span'][1]}: "
          + " ".join(f"{y}:{rd[y]['sd']:.3f}" for y in sorted(rd) if y % 30 == 10 or y == a5['span'][1]))
    print(f"    rol SD rel_decline={a5['sd_rel_decline']} trend slope={a5['sd_trend']['slope']:.5f} p={a5['sd_trend']['p']:.4f}")
    print(f"  >>> A1 GATE PASS: {gate_pass}")

    print("\n=== A2 — variance vs signal + sufficiency ===")
    print(f"  SD vs |signal| corr: {a2a3['A2_sd_vs_signal_corr']}")
    print(f"  sufficiency: {a2a3['A2_sufficiency']}")
    print(f"  spread decomposition: struct_auc Δ={decomp['struct_auc_delta']} (slope p={decomp['struct_auc_trend']['p']:.3f}) "
          f"| wealth_auc Δ={decomp['wealth_auc_delta']} (slope p={decomp['wealth_auc_trend']['p']:.3f})")

    print("\n=== A3 DEFINITIVE — Thorndike range-restriction correction ===")
    print("  epoch : raw|r|  corrected|r|")
    for i, y in enumerate(a2a3["epochs"]):
        print(f"    {y}: {a2a3['A3_raw_abs_r'][i]:.3f}   {a2a3['A3_corrected_abs_r'][i]:.3f}")
    print(f"  raw |r| slope={a2a3['A3_raw_slope']['slope']:+.6f} (p={a2a3['A3_raw_slope']['p']:.3f}) | "
          f"corrected |r| slope={a2a3['A3_corrected_slope']['slope']:+.6f} (p={a2a3['A3_corrected_slope']['p']:.3f})")
    print(f"  >>> A3 corrected FLAT (variance fully explains)? {a2a3['A3_corrected_flat']}")

    print("\n=== A4 — compression structure (P10/P90) ===")
    print("  modern P1: " + " ".join(f"{y}:[{a1m['per_year'][y]['p10']:.2f},{a1m['per_year'][y]['p90']:.2f}]" for y in MI_YEARS))
    rd = a5["per_decade"]
    print("  rol P10/P90: " + " ".join(f"{y}:[{rd[y]['p10']:.2f},{rd[y]['p90']:.2f}]"
          for y in [1850, 1900, 1950, 2000, a5['span'][1]] if y in rd))


if __name__ == "__main__":
    main()
