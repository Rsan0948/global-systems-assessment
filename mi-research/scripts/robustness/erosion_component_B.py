#!/usr/bin/env python3
"""
Component B — CONSEQUENCE ELIMINATION.  Tests B1, B2, B3.

Hypothesis: the MI's institutional signal was calibrated in a world where
institutional failure -> state death (conquest, absorption, partition, collapse).
After 1945 the territorial-integrity norm + nuclear deterrence made state death rare;
institutional failure now yields chronic dysfunction in a permanent container. The
signal is still "correct" (these states are structurally vulnerable) but the terminal
outcome it was calibrated against was eliminated.

  B1  Structural break: single linear vs piecewise (break @1918/1945/1960/1991) on
      a DENSE erosion curve; AIC/BIC.
  B2  Does the signal predict DYSFUNCTION when it can't predict death? (pre-registered
      composite dysfunction outcome; make-or-break for B.)
  B3  State-death rate per decade vs the erosion signal strength (time series).

Read-only; writes data/robustness/decomposition/component_B.json.
"""
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import xlrd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "robustness"))
sys.path.insert(0, str(ROOT / "scripts" / "historical"))

from esi_tests import auc_roc, zscore, logit_fit         # noqa: E402
from conflict_outcome import onset_in_window             # noqa: E402
from build_conflict_onsets import build_ccode_iso        # noqa: E402

VDEM = ROOT / "data/sources/vdem_longrun.json"
LONGRUN = ROOT / "data/sources/longrun_pillars.json"
HOLDOUT = ROOT / "data/robustness/temporal_holdout_panel.json"
GDP_RAW = ROOT / "data/robustness/outcomes/gdp_pcap_ppp_kd_raw.json"
FSI_CSV = ROOT.parent / "mi-pipeline/data/fsi.csv"
POLITY = ROOT / "data/robustness/outcomes/polity/p5v2018.xls"
COW = ROOT / "data/robustness/outcomes/cow/states2016.csv"
FORM = ROOT / "data/robustness/formation/state_formation.json"
OUT = ROOT / "data/robustness/decomposition/component_B.json"

WINDOW = 25


def _ser(v):
    return json.loads(v) if isinstance(v, str) else v


# --------------------------------------------------------------------------- B1
def dense_curve(step=10, start=1816, stop=1996):
    vdem = json.loads(VDEM.read_text())
    longrun = json.loads(LONGRUN.read_text())
    rol = {i: _ser(v["rol"]) for i, v in vdem.items() if "rol" in v}
    gdp = {i: {int(y): val for y, val in _ser(v["P4_gdp"]).items()} for i, v in longrun.items() if "P4_gdp" in v}
    pts = []
    for y in range(start, stop + 1, step):
        rows = []
        for iso in set(rol) & set(gdp):
            if iso.startswith("OWID"):
                continue
            r = rol[iso].get(str(y)); g0 = gdp[iso].get(y)
            if r is None or g0 is None or g0 <= 0:
                continue
            rows.append((-float(r), -math.log(g0), 1 if onset_in_window(iso, y, y + WINDOW) else 0))
        labels = [x[2] for x in rows]
        if len(rows) < 12 or len(set(labels)) < 2:
            continue
        s = auc_roc([x[0] for x in rows], labels)
        w = auc_roc([x[1] for x in rows], labels)
        pts.append({"year": y, "n": len(rows), "onset_rate": round(sum(labels) / len(rows), 3),
                    "spread": round(s - w, 4)})
    return pts


def _aic_bic(rss, n, k):
    # gaussian AIC/BIC from RSS
    ll = -0.5 * n * (math.log(2 * math.pi) + math.log(rss / n) + 1)
    return 2 * k - 2 * ll, k * math.log(n) - 2 * ll


def fit_linear(years, spreads):
    x = np.asarray(years, float); y = np.asarray(spreads, float)
    b = np.polyfit(x, y, 1)
    rss = float(np.sum((y - np.polyval(b, x)) ** 2))
    aic, bic = _aic_bic(rss, len(x), 2)
    return {"params": 2, "rss": round(rss, 6), "aic": round(aic, 3), "bic": round(bic, 3),
            "slope": round(float(b[0]), 6)}


def fit_broken(years, spreads, brk):
    """continuous broken-stick: y = a + b1*(x-brk) + b2*max(0, x-brk).  3 params."""
    x = np.asarray(years, float); y = np.asarray(spreads, float)
    x1 = x - brk
    x2 = np.maximum(0.0, x - brk)
    X = np.column_stack([np.ones_like(x), x1, x2])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    rss = float(np.sum((y - X @ beta) ** 2))
    aic, bic = _aic_bic(rss, len(x), 3)
    return {"break": brk, "params": 3, "rss": round(rss, 6), "aic": round(aic, 3), "bic": round(bic, 3),
            "slope_before": round(float(beta[1]), 6), "slope_after": round(float(beta[1] + beta[2]), 6)}


def test_B1(curve):
    years = [p["year"] for p in curve]; spreads = [p["spread"] for p in curve]
    lin = fit_linear(years, spreads)
    broken = {str(b): fit_broken(years, spreads, b) for b in (1918, 1945, 1960, 1991)}
    best = min(list(broken.values()) + [lin], key=lambda m: m["aic"])
    return {
        "method": "dense erosion curve (10y anchors); single-linear vs continuous broken-stick; lower AIC/BIC better",
        "n_points": len(years), "year_span": [years[0], years[-1]],
        "single_linear": lin, "broken_stick": broken,
        "best_by_aic": ("linear" if best is lin else f"break@{best.get('break')}"),
        "reading": "sharp 1945 break => territorial-integrity norm is the mechanism; "
                   "smooth linear or non-1945 break => consequence-elimination is one force among several",
    }


# --------------------------------------------------------------------------- loaders
def load_gdp():
    out = {}
    for rec in json.loads(GDP_RAW.read_text()):
        if rec.get("value") is not None:
            out.setdefault(rec["iso3"], {})[int(rec["year"])] = float(rec["value"])
    return out


def load_fsi():
    out = {}
    if FSI_CSV.exists():
        for r in csv.DictReader(FSI_CSV.open()):
            try:
                out.setdefault(r["iso3"], {})[int(r["year"])] = float(r["FSI"])
            except (ValueError, KeyError):
                pass
    return out


def load_polity(cc_iso):
    wb = xlrd.open_workbook(POLITY); sh = wb.sheet_by_index(0)
    hdr = [sh.cell_value(0, c) for c in range(sh.ncols)]
    ci = {h: i for i, h in enumerate(hdr)}
    out = defaultdict(dict)
    for r in range(1, sh.nrows):
        cc = sh.cell_value(r, ci["ccode"]); yr = sh.cell_value(r, ci["year"]); p2 = sh.cell_value(r, ci["polity2"])
        if cc == "" or yr == "" or p2 == "":
            continue
        iso = cc_iso.get(int(cc))
        if iso:
            out[iso][int(yr)] = float(p2)
    return out


def load_libdem():
    vdem = json.loads(VDEM.read_text())
    return {i: {int(y): v for y, v in _ser(val["libdem"]).items()}
            for i, val in vdem.items() if "libdem" in val}


# --------------------------------------------------------------------------- B2
def dysfunction_flags(iso, base, out_year, GDP, FSI, POL, LIB, ucdp):
    """Return dict of sub-outcome booleans (None where uncoverable)."""
    f = {}
    # D1 Polity backsliding (>=3 pt drop), Polity5 ends 2018
    pol = POL.get(iso, {})
    yrs = [y for y in pol if base <= y <= min(out_year, 2018)]
    if base in pol and len(yrs) >= 2:
        f["D1_polity_backslide"] = (min(pol[y] for y in yrs) - pol[base]) <= -3
    else:
        f["D1_polity_backslide"] = None
    # D2 GDPpc >=15% drop from within-window peak
    g = GDP.get(iso, {}); gy = sorted(y for y in g if base <= y <= out_year)
    d2 = None
    if len(gy) >= 3:
        d2 = False
        for i, y in enumerate(gy):
            peak = g[y]
            for y2 in gy[i:]:
                if g[y2] / peak < 0.85:
                    d2 = True
    f["D2_gdp_drop15"] = d2
    # D3 conflict onset in window
    f["D3_conflict_onset"] = bool(ucdp)
    # D4 FSI rise >=10 (needs base-year FSI; series starts 2012)
    fs = FSI.get(iso, {})
    if base in fs:
        latest = max(y for y in fs if y <= out_year)
        f["D4_fsi_rise10"] = (fs[latest] - fs[base]) >= 10
    else:
        f["D4_fsi_rise10"] = None
    # D1' V-Dem libdem backsliding (>=0.10 drop), full window to 2024
    lib = LIB.get(iso, {}); ly = [y for y in lib if base <= y <= out_year]
    if base in lib and len(ly) >= 2:
        f["D1v_libdem_backslide"] = (min(lib[y] for y in ly) - lib[base]) <= -0.10
    else:
        f["D1v_libdem_backslide"] = None
    return f


def composite(flags, keys):
    vals = [flags[k] for k in keys]
    observed = [v for v in vals if v is not None]
    if not observed:
        return None
    return any(observed)


def test_B2(form):
    holdout = json.loads(HOLDOUT.read_text())["windows"]
    cc_iso, _ = build_ccode_iso()
    GDP, FSI, POL, LIB = load_gdp(), load_fsi(), load_polity(cc_iso), load_libdem()
    res = {}
    for win, rows in holdout.items():
        yr = int(win); out_year = 2024
        recs = []
        for r in rows:
            fl = dysfunction_flags(r["iso"], yr, out_year, GDP, FSI, POL, LIB, r.get("ucdp"))
            recs.append({**r, "dys_flags": fl,
                         "dys_polity": composite(fl, ["D1_polity_backslide", "D2_gdp_drop15", "D3_conflict_onset", "D4_fsi_rise10"]),
                         "dys_vdem": composite(fl, ["D1v_libdem_backslide", "D2_gdp_drop15", "D3_conflict_onset", "D4_fsi_rise10"])})

        def eval_outcome(field):
            sub = [r for r in recs if r.get(field) is not None and r["P1"] is not None and r["P4"] is not None]
            y = [1 if r[field] else 0 for r in sub]
            if len(set(y)) < 2 or len(sub) < 12:
                return {"n": len(sub), "note": "insufficient", "base_rate": (round(sum(y) / len(sub), 3) if sub else None)}
            gap = [r["P4"] - r["P1"] for r in sub]
            negp1 = [-r["P1"] for r in sub]
            gdp = [GDP.get(r["iso"], {}).get(yr) for r in sub]
            neg_gdp = [(-math.log(g)) if g and g > 0 else None for g in gdp]

            def _auc(sig):
                idx = [i for i, s in enumerate(sig) if s is not None]
                if len({y[i] for i in idx}) < 2:
                    return None
                return round(auc_roc([sig[i] for i in idx], [y[i] for i in idx]), 3)
            # logit gap coefficient
            ones = np.ones(len(sub))
            b, _, _ = logit_fit(np.column_stack([ones, zscore(gap)]), np.asarray(y))
            gap_auc = _auc(gap); gdp_auc = _auc(neg_gdp)
            # gate confusion
            TP = sum(1 for r in sub if r["elevated"] and r[field])
            FP = sum(1 for r in sub if r["elevated"] and not r[field])
            FN = sum(1 for r in sub if not r["elevated"] and r[field])
            TN = sum(1 for r in sub if not r["elevated"] and not r[field])
            pos = TP + FN
            return {
                "n": len(sub), "n_pos": sum(y), "base_rate": round(sum(y) / len(sub), 3),
                "AUC": {"durability_gap": gap_auc, "neg_P1_institutional": _auc(negp1),
                        "wealth_neg_logGDP": gdp_auc},
                "gap_beats_wealth": (None if (gap_auc is None or gdp_auc is None) else round(gap_auc - gdp_auc, 3)),
                "logit_gap_coef_z": round(float(b[1]), 4),
                "gate_confusion": {"TP": TP, "FP": FP, "FN": FN, "TN": TN,
                                   "sensitivity": round(TP / pos, 3) if pos else None,
                                   "specificity": round(TN / (TN + FP), 3) if (TN + FP) else None},
            }

        # sub-outcome coverage counts
        cov = {}
        for k in ["D1_polity_backslide", "D2_gdp_drop15", "D3_conflict_onset", "D4_fsi_rise10", "D1v_libdem_backslide"]:
            vals = [r["dys_flags"][k] for r in recs]
            cov[k] = {"observed": sum(1 for v in vals if v is not None), "positive": sum(1 for v in vals if v)}
        res[win] = {
            "sub_outcome_coverage": cov,
            "crisis(committed)": eval_outcome("crisis"),
            "dysfunction_polity": eval_outcome("dys_polity"),
            "dysfunction_vdem": eval_outcome("dys_vdem"),
        }
    return res


# --------------------------------------------------------------------------- B3
def test_B3(curve):
    cc_iso, _ = build_ccode_iso()
    rows = list(csv.DictReader(COW.open()))
    # state death = a membership spell ending before 2016 (exit from the system)
    deaths = defaultdict(int)
    seen = set()
    for r in rows:
        ey = int(r["endyear"])
        key = (r["ccode"], r["styear"], ey)
        if ey < 2016 and key not in seen:
            seen.add(key)
            deaths[(ey // 10) * 10] += 1
    # align to curve decades
    by_decade = {(p["year"] // 10) * 10: p["spread"] for p in curve}
    decs = sorted(set(list(deaths.keys()) + list(by_decade.keys())))
    series = []
    for d in decs:
        if d < 1816 or d > 2010:
            continue
        series.append({"decade": d, "state_deaths": deaths.get(d, 0), "spread": by_decade.get(d)})
    paired = [(s["state_deaths"], s["spread"]) for s in series if s["spread"] is not None]
    r_val, p_val = (stats.pearsonr([a for a, _ in paired], [b for _, b in paired]) if len(paired) >= 3 else (None, None))
    return {
        "method": "COW system exits (endyear<2016) per decade vs erosion spread per decade",
        "series": series,
        "pearson_deaths_vs_spread": {"r": (round(float(r_val), 3) if r_val is not None else None),
                                     "p": (round(float(p_val), 3) if p_val is not None else None),
                                     "n": len(paired)},
        "reading": "both declining together (positive r: fewer deaths <-> lower spread) is consistent with the "
                   "signal's erosion tracking the elimination of the outcome it predicted",
    }


def main():
    form = json.loads(FORM.read_text())["states"]
    curve = dense_curve()
    report = {
        "component": "B_consequence_elimination",
        "B1_structural_break": test_B1(curve),
        "B2_dysfunction_holdout": test_B2(form),
        "B3_state_death_vs_signal": test_B3(curve),
        "dense_curve": curve,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, default=lambda o: None))

    b1 = report["B1_structural_break"]
    print("=== B1 — structural break (dense curve, %d pts %s) ===" % (b1["n_points"], b1["year_span"]))
    print(f"  linear:      aic={b1['single_linear']['aic']} bic={b1['single_linear']['bic']} slope={b1['single_linear']['slope']}")
    for b, m in b1["broken_stick"].items():
        print(f"  break@{b}: aic={m['aic']} bic={m['bic']} slope_before={m['slope_before']} slope_after={m['slope_after']}")
    print(f"  BEST by AIC: {b1['best_by_aic']}")

    print("\n=== B2 — dysfunction holdout (gap AUC & gap-beats-wealth on crisis vs dysfunction) ===")
    for win, v in report["B2_dysfunction_holdout"].items():
        print(f"  window {win}:")
        for oc in ["crisis(committed)", "dysfunction_polity", "dysfunction_vdem"]:
            o = v[oc]
            if "AUC" in o:
                print(f"    {oc:22} n={o['n']} base={o['base_rate']} gap_AUC={o['AUC']['durability_gap']} "
                      f"wealth={o['AUC']['wealth_neg_logGDP']} gap-wealth={o['gap_beats_wealth']} gap_coef={o['logit_gap_coef_z']}")
            else:
                print(f"    {oc:22} {o}")

    b3 = report["B3_state_death_vs_signal"]
    print(f"\n=== B3 — state-death rate vs signal ===  pearson r={b3['pearson_deaths_vs_spread']['r']} p={b3['pearson_deaths_vs_spread']['p']}")
    for s in b3["series"]:
        print(f"  {s['decade']}: deaths={s['state_deaths']:2d} spread={s['spread']}")
    print(f"\n-> {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
