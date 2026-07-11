#!/usr/bin/env python3
"""
Component A — DENOMINATOR DILUTION.  Tests A2, A3, A4.

Hypothesis: the ~150y erosion of the MI's institutional signal is (partly) a
sample-composition effect — the state system filled with institutionally-young
post-colonial states that don't fail by institutional *decline* (the dynamic the MI
detects) but by chronic institutional *absence* (correlated with poverty), diluting
the structure-over-wealth edge and strengthening wealth predictors.

Reads the FROZEN A1 classification (state_formation.json) + the same erosion panel
(V-Dem rule-of-law, log Maddison GDP, conflict-onset) as Finding 2/7, and the frozen
temporal-holdout panel. Reuses esi_tests' auc/zscore/logit helpers unchanged.

  A2  Split the epoch erosion curve by formation group.
  A3  Split the temporal holdout by formation group (gate vs GDP/FSI baselines).
  A4  State age as a predictor; does controlling for age recover the signal?

Read-only; writes data/robustness/decomposition/component_A.json.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "robustness"))
sys.path.insert(0, str(ROOT / "scripts" / "historical"))

from esi_tests import auc_roc, zscore, logit_fit          # noqa: E402
from conflict_outcome import onset_in_window              # noqa: E402

FORM = ROOT / "data/robustness/formation/state_formation.json"
VDEM = ROOT / "data/sources/vdem_longrun.json"
LONGRUN = ROOT / "data/sources/longrun_pillars.json"
HOLDOUT = ROOT / "data/robustness/temporal_holdout_panel.json"
GDP_RAW = ROOT / "data/robustness/outcomes/gdp_pcap_ppp_kd_raw.json"
FSI_CSV = ROOT.parent / "mi-pipeline/data/fsi.csv"
OUT = ROOT / "data/robustness/decomposition/component_A.json"

ANCHORS = [1816, 1850, 1880, 1910, 1940, 1970, 1990]
WINDOW = 25


def _ser(v):
    return json.loads(v) if isinstance(v, str) else v


def auc_pair(rows, key):
    """structure/wealth/spread AUC over rows (low signal -> onset)."""
    labels = [r["onset"] for r in rows]
    if len(set(labels)) < 2:
        return None, None, None
    s = auc_roc([r["neg_struct"] for r in rows], labels)
    w = auc_roc([r["neg_wealth"] for r in rows], labels)
    return s, w, (s - w)


def pearson(xs, ys):
    if len(xs) < 3:
        return None, None
    r, p = stats.pearsonr(xs, ys)
    return float(r), float(p)


def ols_slope(xs, ys):
    if len(xs) < 2:
        return None
    x = np.asarray(xs, float); y = np.asarray(ys, float)
    return float(np.polyfit(x, y, 1)[0])


# ---------------------------------------------------------------------------
def build_panel(form):
    vdem = json.loads(VDEM.read_text())
    longrun = json.loads(LONGRUN.read_text())
    rol = {i: _ser(v["rol"]) for i, v in vdem.items() if "rol" in v}
    gdp = {i: {int(y): val for y, val in _ser(v["P4_gdp"]).items()} for i, v in longrun.items() if "P4_gdp" in v}
    panel = {}   # anchor -> list of rows with group
    for y in ANCHORS:
        rows = []
        for iso in set(rol) & set(gdp):
            if iso.startswith("OWID") or iso not in form:
                continue
            r = rol[iso].get(str(y))
            g0 = gdp[iso].get(y)
            if r is None or g0 is None or g0 <= 0:
                continue
            rows.append({
                "iso": iso, "group": form[iso]["group"], "alt": form[iso]["alt_group"],
                "neg_struct": -float(r), "neg_wealth": -math.log(g0),
                "onset": 1 if onset_in_window(iso, y, y + WINDOW) else 0,
            })
        panel[y] = rows
    return panel


def group_curve(panel, member):
    """spread curve over anchors for rows where member(row) is True."""
    out = []
    for y in ANCHORS:
        rows = [r for r in panel[y] if member(r)]
        n = len(rows)
        npos = sum(r["onset"] for r in rows)
        s, w, sp = auc_pair(rows, None) if n else (None, None, None)
        flags = []
        if n < 12:
            flags.append("small_n")
        if n and (npos / n < 0.1 or npos / n > 0.9):
            flags.append("degenerate_rate")
        if sp is None:
            flags.append("auc_undefined")
        out.append({"year": y, "n": n, "n_onset": npos,
                    "structure_auc": None if s is None else round(s, 3),
                    "wealth_auc": None if w is None else round(w, 3),
                    "spread": None if sp is None else round(sp, 3),
                    "flags": flags})
    return out


def curve_erosion(curve, require_clean=True):
    """OLS slope + Pearson of spread vs year over trustworthy anchors."""
    pts = [(e["year"], e["spread"]) for e in curve
           if e["spread"] is not None and (not require_clean or not e["flags"])]
    if len(pts) < 3:
        # relax: allow small_n but not undefined/degenerate
        pts = [(e["year"], e["spread"]) for e in curve
               if e["spread"] is not None and "auc_undefined" not in e["flags"]
               and "degenerate_rate" not in e["flags"]]
    ys = [p[0] for p in pts]; sp = [p[1] for p in pts]
    r, p = pearson(ys, sp)
    return {"anchors_used": ys, "spreads": sp, "slope_per_year": ols_slope(ys, sp),
            "pearson_r": r, "pearson_p": p,
            "endpoint_drop": (round(sp[0] - sp[-1], 3) if len(sp) >= 2 else None)}


def test_A2(panel, form):
    groups = {
        "full": lambda r: True,
        "mature": lambda r: r["group"] == "mature",
        "post_colonial": lambda r: r["group"] == "post_colonial",
        "early_post_colonial": lambda r: r["group"] == "early_post_colonial",
        "post_colonial_incl_early": lambda r: r["group"] in ("post_colonial", "early_post_colonial"),
        # India special-case: mature curve WITH india moved in
        "mature_plus_india": lambda r: r["group"] == "mature" or r["iso"] == "IND",
        # sensitivity: all flagged edges moved to their alt_group
        "mature_sensitivity": lambda r: (r["alt"] == "mature") or (r["group"] == "mature" and r["alt"] is None) or (r["group"] == "mature" and r["alt"] != "post_colonial"),
    }
    curves = {name: group_curve(panel, m) for name, m in groups.items()}
    erosion = {name: curve_erosion(c) for name, c in curves.items()}

    # % post-colonial state-years per epoch vs full-sample spread
    comp = []
    for i, y in enumerate(ANCHORS):
        rows = panel[y]
        n = len(rows)
        pc = sum(1 for r in rows if r["group"] in ("post_colonial", "early_post_colonial"))
        comp.append({"year": y, "n": n, "pct_post_colonial": round(pc / n, 3) if n else None,
                     "full_spread": curves["full"][i]["spread"]})
    pc_series = [(c["pct_post_colonial"], c["full_spread"]) for c in comp
                 if c["pct_post_colonial"] is not None and c["full_spread"] is not None]
    r_pc, p_pc = pearson([a for a, _ in pc_series], [b for _, b in pc_series])

    # A's share of erosion: how much of full erosion does NOT appear in mature-only?
    full_e = erosion["full"]["slope_per_year"]
    mat_e = erosion["mature"]["slope_per_year"]
    a_share = None
    if full_e not in (None, 0) and mat_e is not None:
        a_share = round(1.0 - (mat_e / full_e), 3)   # mature erosion / full erosion removed
    return {
        "method": "Finding 2/7 structure-minus-wealth AUC spread by epoch, split by A1 formation group",
        "curves": curves, "erosion": erosion,
        "composition_vs_spread": {"per_epoch": comp,
                                  "pearson_pctPC_vs_fullspread": {"r": r_pc, "p": p_pc}},
        "A_share_of_erosion": {
            "full_slope_per_year": full_e, "mature_slope_per_year": mat_e,
            "estimate": a_share,
            "reading": "fraction of the full-sample erosion slope NOT reproduced within mature-only states "
                       "(1.0 => mature signal doesn't erode => erosion is pure composition)"},
    }


# ---------------------------------------------------------------------------
def load_gdp():
    out = {}
    for rec in json.loads(GDP_RAW.read_text()):
        if rec.get("value") is not None:
            out.setdefault(rec["iso3"], {})[int(rec["year"])] = float(rec["value"])
    return out


def load_fsi():
    import csv
    out = {}
    if FSI_CSV.exists():
        for r in csv.DictReader(FSI_CSV.open()):
            try:
                out.setdefault(r["iso3"], {})[int(r["year"])] = float(r["FSI"])
            except (ValueError, KeyError):
                pass
    return out


def confusion(flags, labels):
    TP = sum(1 for f, l in zip(flags, labels) if f and l)
    FP = sum(1 for f, l in zip(flags, labels) if f and not l)
    FN = sum(1 for f, l in zip(flags, labels) if (not f) and l)
    TN = sum(1 for f, l in zip(flags, labels) if (not f) and (not l))
    n = len(labels); pos = TP + FN
    sens = TP / pos if pos else None
    spec = TN / (TN + FP) if (TN + FP) else None
    acc = (TP + TN) / n if n else None
    ppv = TP / (TP + FP) if (TP + FP) else None
    base = pos / n if n else None
    lift = (ppv / base) if (ppv is not None and base) else None
    return {"TP": TP, "FP": FP, "FN": FN, "TN": TN, "N": n, "pos": pos,
            "base_rate": round(base, 3) if base is not None else None,
            "sensitivity": round(sens, 3) if sens is not None else None,
            "specificity": round(spec, 3) if spec is not None else None,
            "PPV": round(ppv, 3) if ppv is not None else None,
            "accuracy": round(acc, 3) if acc is not None else None,
            "lift_over_base": round(lift, 3) if lift is not None else None}


def test_A3(form):
    holdout = json.loads(HOLDOUT.read_text())["windows"]
    GDP = load_gdp(); FSI = load_fsi()
    res = {}
    for win, rows in holdout.items():
        yr = int(win)
        groups = {
            "full": lambda r: True,
            "mature": lambda r: form.get(r["iso"], {}).get("group") == "mature",
            "post_colonial": lambda r: form.get(r["iso"], {}).get("group") == "post_colonial",
            "early_post_colonial": lambda r: form.get(r["iso"], {}).get("group") == "early_post_colonial",
            "mature_plus_india": lambda r: form.get(r["iso"], {}).get("group") == "mature" or r["iso"] == "IND",
            "post_colonial_no_india": lambda r: form.get(r["iso"], {}).get("group") == "post_colonial" and r["iso"] != "IND",
        }
        win_res = {}
        for gname, member in groups.items():
            sub = [r for r in rows if member(r) and r.get("crisis") is not None]
            n = len(sub)
            if n < 8:
                win_res[gname] = {"n": n, "note": "too_small"}
                continue
            labels = [1 if r["crisis"] else 0 for r in sub]
            if len(set(labels)) < 2:
                win_res[gname] = {"n": n, "note": "no_outcome_variation", "base_rate": round(sum(labels) / n, 3)}
                continue
            gap = [r["P4"] - r["P1"] for r in sub]          # durability gap (structural)
            negP1 = [-r["P1"] for r in sub]                 # institutional quality (low -> crisis)
            vuln = [r["vuln"] for r in sub]
            gdp = [GDP.get(r["iso"], {}).get(yr) for r in sub]
            fsi = [FSI.get(r["iso"], {}).get(yr) for r in sub]
            neg_gdp = [(-math.log(g)) if g and g > 0 else None for g in gdp]

            def _auc(sig):
                idx = [i for i, s in enumerate(sig) if s is not None]
                if len({labels[i] for i in idx}) < 2 or len(idx) < 8:
                    return None, len(idx)
                return round(auc_roc([sig[i] for i in idx], [labels[i] for i in idx]), 3), len(idx)

            gap_auc, _ = _auc(gap)
            p1_auc, _ = _auc(negP1)
            vuln_auc, _ = _auc(vuln)
            gdp_auc, gdp_n = _auc(neg_gdp)
            fsi_auc, fsi_n = _auc(fsi)
            conf = confusion([bool(r["elevated"]) for r in sub], [bool(x) for x in labels])
            win_res[gname] = {
                "n": n, "base_rate": round(sum(labels) / n, 3),
                "gate_confusion(elevated_flag)": conf,
                "AUC": {"durability_gap": gap_auc, "neg_P1_institutional": p1_auc,
                        "vuln_score": vuln_auc,
                        "wealth_neg_logGDP": gdp_auc, "FSI": fsi_auc},
                "AUC_n": {"gdp": gdp_n, "fsi": fsi_n},
                "gate_beats_wealth": (None if (gap_auc is None or gdp_auc is None) else round(gap_auc - gdp_auc, 3)),
                "gate_beats_FSI": (None if (gap_auc is None or fsi_auc is None) else round(gap_auc - fsi_auc, 3)),
            }
        res[win] = win_res
    return res


def test_A4(form):
    holdout = json.loads(HOLDOUT.read_text())["windows"]
    res = {}
    for win, rows in holdout.items():
        yr = int(win)
        sub = [r for r in rows if r.get("crisis") is not None and form.get(r["iso"], {}).get("cow_entry_year")]
        for r in sub:
            r["_age"] = yr - form[r["iso"]]["cow_entry_year"]
        labels = np.array([1 if r["crisis"] else 0 for r in sub])
        if len(set(labels.tolist())) < 2 or len(sub) < 12:
            res[win] = {"n": len(sub), "note": "insufficient"}
            continue
        age = np.array([r["_age"] for r in sub], float)
        gap = np.array([r["P4"] - r["P1"] for r in sub], float)
        # younger -> more crisis => predictor is -age
        age_auc = round(auc_roc((-age).tolist(), labels.tolist()), 3)
        # is age a significant univariate predictor? logistic on standardized -age
        ones = np.ones(len(sub))
        b_age, auc_age, _ = logit_fit(np.column_stack([ones, zscore(-age)]), labels)
        # does controlling for age change the gap coefficient / recover signal?
        b_gap, auc_gap, _ = logit_fit(np.column_stack([ones, zscore(gap)]), labels)
        b_both, auc_both, _ = logit_fit(np.column_stack([ones, zscore(gap), zscore(-age)]), labels)
        # spearman age vs gap (are young states also the high-gap ones?)
        rho, prho = stats.spearmanr(age, gap)
        res[win] = {
            "n": len(sub),
            "median_age": float(np.median(age)),
            "age_alone_AUC(neg_age)": age_auc,
            "logit_neg_age": {"coef_neg_age_z": round(float(b_age[1]), 4), "auc": round(auc_age, 4)},
            "logit_gap_only": {"coef_gap_z": round(float(b_gap[1]), 4), "auc": round(auc_gap, 4)},
            "logit_gap_plus_age": {"coef_gap_z": round(float(b_both[1]), 4),
                                    "coef_neg_age_z": round(float(b_both[2]), 4), "auc": round(auc_both, 4)},
            "gap_coef_change_when_age_added": round(float(b_both[1] - b_gap[1]), 4),
            "spearman_age_vs_gap": {"rho": round(float(rho), 3), "p": round(float(prho), 3)},
            "reading": "if gap coef GROWS when age added AND age is significant => youth was masking the "
                       "institutional signal (erosion = youth). If gap coef is flat => age doesn't explain it.",
        }
    return res


def main():
    form = json.loads(FORM.read_text())["states"]
    panel = build_panel(form)
    report = {
        "component": "A_denominator_dilution",
        "classification_source": "data/robustness/formation/state_formation.json (frozen A1)",
        "A2_split_erosion_curve": test_A2(panel, form),
        "A3_split_temporal_holdout": test_A3(form),
        "A4_state_age_predictor": test_A4(form),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, default=lambda o: None))

    # ---- console summary ----
    a2 = report["A2_split_erosion_curve"]
    print("=== A2 — erosion curve by formation group (structure-minus-wealth spread) ===")
    print(f"{'year':>5} " + "".join(f"{g[:12]:>14}" for g in ["full", "mature", "post_colonial", "early_post_col"]))
    gmap = {"post_colonial": "post_colonial", "early_post_col": "early_post_colonial"}
    for i, y in enumerate(ANCHORS):
        cells = []
        for g in ["full", "mature", "post_colonial", "early_post_colonial"]:
            e = a2["curves"][g][i]
            sp = e["spread"]
            cells.append(f"{('%+.3f' % sp) if sp is not None else '·':>14}")
        print(f"{y:>5} " + "".join(cells))
    for g in ["full", "mature", "post_colonial_incl_early"]:
        e = a2["erosion"][g]
        print(f"  {g:26} slope/yr={e['slope_per_year']}  r={e['pearson_r']}  p={e['pearson_p']}")
    print(f"  A_share_of_erosion = {a2['A_share_of_erosion']['estimate']}  "
          f"(pctPC vs spread r={a2['composition_vs_spread']['pearson_pctPC_vs_fullspread']['r']})")

    print("\n=== A3 — temporal holdout by group (2004): gate durability-gap AUC vs wealth/FSI ===")
    for g, v in report["A3_split_temporal_holdout"]["2004"].items():
        if "AUC" in v:
            a = v["AUC"]
            print(f"  {g:22} n={v['n']:3} base={v['base_rate']}  gap={a['durability_gap']} "
                  f"P1={a['neg_P1_institutional']} wealth={a['wealth_neg_logGDP']} FSI={a['FSI']} "
                  f"| gate-wealth={v['gate_beats_wealth']}")
        else:
            print(f"  {g:22} {v}")

    print("\n=== A4 — state age (2004 window) ===")
    v = report["A4_state_age_predictor"].get("2004", {})
    if "n" in v and "note" not in v:
        print(f"  n={v['n']} age_alone_AUC={v['age_alone_AUC(neg_age)']} "
              f"gap_only_coef={v['logit_gap_only']['coef_gap_z']} gap+age_coef={v['logit_gap_plus_age']['coef_gap_z']} "
              f"(Δ={v['gap_coef_change_when_age_added']}) age_coef={v['logit_gap_plus_age']['coef_neg_age_z']}")
    print(f"\n-> {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
