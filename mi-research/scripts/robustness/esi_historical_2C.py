#!/usr/bin/env python3
"""ESI Test 2C — does a historical external-support proxy explain the 150-year erosion?

The erosion (Finding 2): structure's (V-Dem rule-of-law) predictive edge over wealth
for conflict onset declines monotonically across epochs 1816->1990 (spread r=-0.847).
2C asks: does that decline FLATTEN when a crude external-support proxy is controlled?

Crude proxy (the only ESI dimension buildable pre-1960): great-power DEFENSE-PACT
membership from COW Formal Alliances v4.1 — a polity in a defense pact with a COW
major power that year = external security support (Systemic-Insurance analogue).

Per epoch: logistic onset ~ z(rule_of_law) + z(logGDP), with and without z(support).
If structure's coefficient decline across epochs flattens once support is added, the
erosion is (partly) explained by rising external support. Reports the null honestly.

    python scripts/robustness/esi_historical_2C.py
"""
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy import stats
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "historical"))
import config  # noqa: E402
from lib.iso_map import COW_NAME_MANUAL, name_to_iso  # noqa: E402
from conflict_outcome import onset_in_window  # noqa: E402

VDEM = ROOT / "data" / "sources" / "vdem_longrun.json"
LONGRUN = ROOT / "data" / "sources" / "longrun_pillars.json"
COW_DYAD = ROOT / "data" / "robustness" / "outcomes" / "cow_alliance" / "alliance_v4.1_by_dyad_yearly.csv"
OUT = ROOT / "data" / "robustness" / "esi" / "esi_2C_historical.json"

_HC = config.robustness()["historical"]["decay_curve_conflict"]
ANCHORS = _HC["anchors"]
WINDOW = _HC["window"]
L2 = 1e-3

# COW major powers (official list) -> ccode: [(start,end)] active spans
MAJOR_POWERS = {
    2:   [(1898, 2020)],               # USA
    200: [(1816, 2020)],               # UK
    220: [(1816, 1940), (1945, 2020)], # France
    255: [(1816, 1918), (1925, 1945), (1991, 2020)],  # Germany/Prussia
    300: [(1816, 1918)],               # Austria-Hungary
    325: [(1860, 1943)],               # Italy
    365: [(1816, 1917), (1922, 2020)], # Russia/USSR
    710: [(1950, 2020)],               # China
    740: [(1895, 1945), (1991, 2020)], # Japan
}


def is_major(ccode, year):
    return any(s <= year <= e for s, e in MAJOR_POWERS.get(ccode, []))


def _series(v):
    return json.loads(v) if isinstance(v, str) else v


def build_support():
    """support[iso][year] = 1 if in a defense pact with a great power that year."""
    ccode_iso = {}
    def iso_for(cc, name):
        if cc not in ccode_iso:
            ccode_iso[cc] = name_to_iso(name, COW_NAME_MANUAL)
        return ccode_iso[cc]
    sup = {}
    for r in csv.DictReader(open(COW_DYAD, encoding="latin-1")):
        if r.get("defense") != "1":
            continue
        y = int(r["year"])
        if y not in ANCHORS:
            continue
        c1, c2 = int(r["ccode1"]), int(r["ccode2"])
        # polity c1 supported if partner c2 is a great power that year (and c1 isn't the same GP)
        if is_major(c2, y) and c1 != c2:
            iso = iso_for(c1, r["state_name1"])
            if iso:
                sup.setdefault(iso, {}).setdefault(y, 1)
    return sup


def auc(scores, labels):
    s = np.asarray(scores, float); y = np.asarray(labels, int)
    pos, neg = (y == 1).sum(), (y == 0).sum()
    if pos == 0 or neg == 0:
        return None
    ranks = stats.rankdata(s)
    return float((ranks[y == 1].sum() - pos * (pos + 1) / 2) / (pos * neg))


def zscore(x):
    x = np.asarray(x, float); sd = x.std()
    return (x - x.mean()) / sd if sd > 0 else x - x.mean()


def logit_coef(X, y, names):
    X = np.asarray(X, float); yv = np.asarray(y, float)
    def nll(b):
        z = X @ b
        return -np.sum(yv * z - np.logaddexp(0.0, z)) + L2 * np.sum(b[1:] ** 2)
    b = minimize(nll, np.zeros(X.shape[1]), method="BFGS").x
    return {nm: float(c) for nm, c in zip(names, b)}


def main():
    vdem = json.loads(VDEM.read_text())
    longrun = json.loads(LONGRUN.read_text())
    support = build_support()

    epochs = []
    for y in ANCHORS:
        rows = []
        for iso, rec in vdem.items():
            if len(iso) != 3:
                continue
            rol = _series(rec.get("rol"))
            gdp = _series((longrun.get(iso, {}) or {}).get("P4_gdp"))
            if not rol or not gdp:
                continue
            rv = rol.get(str(y)); gv = gdp.get(str(y))
            if rv is None or gv is None or gv <= 0:
                continue
            onset = 1 if onset_in_window(iso, y, y + WINDOW) else 0
            sup = 1 if support.get(iso, {}).get(y) else 0
            rows.append({"iso": iso, "rol": rv, "lgdp": math.log(gv), "onset": onset, "sup": sup})
        n = len(rows)
        onset_rate = sum(r["onset"] for r in rows) / n if n else None
        sup_rate = sum(r["sup"] for r in rows) / n if n else None
        rec = {"year": y, "n": n, "onset_rate": onset_rate, "support_prevalence": sup_rate}
        if n >= 12 and onset_rate not in (None, 0, 1):
            y_ = [r["onset"] for r in rows]
            rol_z = zscore([r["rol"] for r in rows])
            gdp_z = zscore([r["lgdp"] for r in rows])
            ones = np.ones(n)
            # structure & wealth AUC (predict onset; -rol and -lgdp so higher=more vulnerable)
            rec["structure_auc"] = auc([-r["rol"] for r in rows], y_)
            rec["wealth_auc"] = auc([-r["lgdp"] for r in rows], y_)
            if rec["structure_auc"] and rec["wealth_auc"]:
                rec["spread"] = round(rec["structure_auc"] - rec["wealth_auc"], 4)
            # structure coefficient with/without support control
            base = logit_coef(np.column_stack([ones, rol_z, gdp_z]), y_, ["b0", "rol", "lgdp"])
            rec["struct_coef_baseline"] = round(base["rol"], 4)
            if sup_rate not in (None, 0, 1):
                sup_z = zscore([r["sup"] for r in rows])
                withsup = logit_coef(np.column_stack([ones, rol_z, gdp_z, sup_z]), y_,
                                     ["b0", "rol", "lgdp", "sup"])
                rec["struct_coef_with_support"] = round(withsup["rol"], 4)
                rec["support_coef"] = round(withsup["sup"], 4)
        epochs.append(rec)

    # --- trend of structure's edge across epochs, baseline vs support-controlled ---
    def trend(key):
        pts = [(e["year"], e[key]) for e in epochs if e.get(key) is not None]
        if len(pts) < 3:
            return None
        xs, ys = zip(*pts)
        r, p = stats.pearsonr(xs, ys)
        slope = np.polyfit(xs, ys, 1)[0]
        return {"n_epochs": len(pts), "pearson_r": round(float(r), 4),
                "p": round(float(p), 4), "slope_per_year": float(slope)}

    spread_trend = trend("spread")                      # reproduces Finding 2 erosion
    coef_base_trend = trend("struct_coef_baseline")     # structure |coef| erosion (baseline)
    coef_sup_trend = trend("struct_coef_with_support")  # ... controlling for support

    # structure coef is negative (higher rule-of-law -> fewer onsets); erosion = coef -> 0
    # (rising toward zero across epochs). Flattening = the support-controlled trend is LESS
    # steep (rises less toward zero) than baseline.
    verdict = {
        "spread_erosion_trend": spread_trend,
        "struct_coef_trend_baseline": coef_base_trend,
        "struct_coef_trend_with_support": coef_sup_trend,
        "support_prevalence_by_epoch": {e["year"]: e.get("support_prevalence") for e in epochs},
        "interpretation": ("Flattening iff |support-controlled coef trend slope| < |baseline slope| "
                           "AND support prevalence rises across epochs. Otherwise erosion is not "
                           "explained by the great-power-alliance support proxy."),
    }
    if coef_base_trend and coef_sup_trend:
        verdict["baseline_slope"] = coef_base_trend["slope_per_year"]
        verdict["support_controlled_slope"] = coef_sup_trend["slope_per_year"]
        verdict["flattens"] = abs(coef_sup_trend["slope_per_year"]) < abs(coef_base_trend["slope_per_year"])

    payload = {"_meta": {"test": "2C historical erosion vs external-support proxy",
                         "proxy": "great-power defense-pact membership (COW Alliances v4.1)",
                         "prereg": "docs/ESI_PREREGISTRATION.md", "anchors": ANCHORS, "window": WINDOW},
               "epochs": epochs, "verdict": verdict}
    OUT.write_text(json.dumps(payload, indent=1))
    print("epoch | n | onset% | support% | spread | struct_coef base->+sup")
    for e in epochs:
        print(f"  {e['year']} | n={e['n']:3d} | onset={e['onset_rate'] and round(e['onset_rate'],2)} | "
              f"sup={e.get('support_prevalence') and round(e['support_prevalence'],2)} | "
              f"spread={e.get('spread')} | coef {e.get('struct_coef_baseline')} -> {e.get('struct_coef_with_support')}")
    print("\nspread erosion trend:", spread_trend)
    print("struct-coef trend baseline:", coef_base_trend)
    print("struct-coef trend +support:", coef_sup_trend)
    if "flattens" in verdict:
        print(f"FLATTENS when support controlled? {verdict['flattens']} "
              f"(baseline slope {verdict['baseline_slope']:.4g} vs +support {verdict['support_controlled_slope']:.4g})")
    print(f"-> {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
