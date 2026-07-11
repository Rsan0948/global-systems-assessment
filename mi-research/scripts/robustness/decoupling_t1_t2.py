#!/usr/bin/env python3
"""
Decoupling — Test 1 (P1-GDP coupling over time) and Test 2 (institutional
variance at income levels). Frozen spec: docs/DECOUPLING_PREREGISTRATION.md.

Read-only; writes data/robustness/decoupling/{t1_coupling,t2_variance}.json.
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
import decoupling_panel as dp  # noqa: E402  (sibling module)

YEARS = [1996, 2004, 2012, 2018, 2024]
VDEM = ROOT / "data" / "sources" / "vdem_longrun.json"
LONGRUN = ROOT / "data" / "sources" / "longrun_pillars.json"
OUT1 = ROOT / "data" / "robustness" / "decoupling" / "t1_coupling.json"
OUT2 = ROOT / "data" / "robustness" / "decoupling" / "t2_variance.json"


def _series(v):
    return json.loads(v) if isinstance(v, str) else v


def trend(xs, ys):
    """OLS slope of ys~xs plus p; xs are years."""
    xs = np.array(xs, float)
    ys = np.array(ys, float)
    res = stats.linregress(xs, ys)
    return {"slope": float(res.slope), "intercept": float(res.intercept),
            "p": float(res.pvalue), "r_of_trend": float(res.rvalue)}


def collect(rows, isos, year, keyx="P1", keyy="logGDP"):
    xs, ys = [], []
    for iso in isos:
        e = rows[iso]["years"].get(str(year))
        if not e:
            continue
        a, b = e.get(keyx), e.get(keyy)
        if a is not None and b is not None:
            xs.append(a)
            ys.append(b)
    return np.array(xs, float), np.array(ys, float)


def corr_block(x, y):
    if len(x) < 4:
        return None
    pr = stats.pearsonr(x, y)
    sp = stats.spearmanr(x, y)
    return {"n": int(len(x)), "pearson_r": float(pr.statistic),
            "pearson_p": float(pr.pvalue), "spearman_rho": float(sp.statistic),
            "spearman_p": float(sp.pvalue), "R2": float(pr.statistic ** 2)}


def test1(panel):
    rows = panel["rows"]
    bal = panel["balanced"]

    def run_universe(isos_per_year):
        per_year = {}
        for y in YEARS:
            isos = isos_per_year(y)
            x, yv = collect(rows, isos, y)
            per_year[y] = corr_block(x, yv)
        rs = [per_year[y]["pearson_r"] for y in YEARS]
        r2 = [per_year[y]["R2"] for y in YEARS]
        return per_year, {
            "r_trend": trend(YEARS, rs),
            "R2_trend": trend(YEARS, r2),
            "delta_r_2024_1996": rs[-1] - rs[0],
            "early_half_r_1996_2012": (rs[0] + rs[1] + rs[2]) / 3,
            "late_half_r_2012_2024": (rs[2] + rs[3] + rs[4]) / 3,
        }

    balanced_per_year, balanced_summary = run_universe(lambda y: bal)
    # sensitivity: all available per year
    all_isos = lambda y: [iso for iso in rows
                          if str(y) in rows[iso]["years"]
                          and rows[iso]["years"][str(y)]["P1"] is not None
                          and rows[iso]["years"][str(y)]["logGDP"] is not None]
    sens_per_year, sens_summary = run_universe(all_isos)

    # historical extension (F2)
    vdem = json.loads(VDEM.read_text())
    longrun = json.loads(LONGRUN.read_text())
    rol = {iso: _series(v["rol"]) for iso, v in vdem.items() if "rol" in v}
    gdp = {iso: {int(y): val for y, val in _series(v["P4_gdp"]).items()}
           for iso, v in longrun.items() if "P4_gdp" in v}
    hist = {}
    for anchor in [1850, 1880, 1910, 1940, 1970]:
        xs, ys = [], []
        for iso in set(rol) & set(gdp):
            r = rol[iso].get(str(anchor))
            g = gdp[iso].get(anchor)
            if r is None or g is None or g <= 0:
                continue
            xs.append(r)
            ys.append(math.log10(g))
        hist[anchor] = corr_block(np.array(xs, float), np.array(ys, float))
    hist_years = [a for a in [1850, 1880, 1910, 1940, 1970] if hist[a]]
    hist_rs = [hist[a]["pearson_r"] for a in hist_years]
    hist_trend = trend(hist_years, hist_rs) if len(hist_years) >= 3 else None

    return {
        "test": "T1_P1_GDP_coupling",
        "spec": "Pearson/Spearman/R2 of P1 vs log10(GDPpc PPP) at 5 MI points; "
                "OLS trend of r vs year; historical rule-of-law vs log Maddison GDP.",
        "balanced": {"per_year": balanced_per_year, "summary": balanced_summary},
        "sensitivity_all_available": {"per_year": sens_per_year,
                                      "summary": sens_summary},
        "historical": {"note": "structure=V-Dem rule-of-law (P1 subcomponent), "
                               "wealth=log Maddison GDP; rough proxies",
                       "per_anchor": hist, "r_trend": hist_trend},
    }


def test2(panel):
    rows = panel["rows"]
    bal = panel["balanced"]
    out = {"test": "T2_institutional_variance_at_income", "per_year": {}}
    top_sd, bot_sd = [], []
    for y in YEARS:
        recs = []
        for iso in bal:
            e = rows[iso]["years"].get(str(y))
            if e and e["P1"] is not None and e["gdp"]:
                recs.append((e["gdp"], e["P1"]))
        recs.sort(key=lambda t: t[0])
        n = len(recs)
        q = n // 4
        top = [p for _, p in recs[-q:]]
        bot = [p for _, p in recs[:q]]

        def disp(v):
            a = np.array(v, float)
            return {"n": len(v), "mean_P1": float(a.mean()),
                    "sd_P1": float(a.std(ddof=1)),
                    "iqr_P1": float(np.percentile(a, 75) - np.percentile(a, 25))}
        out["per_year"][y] = {"n_total": n, "top_quartile": disp(top),
                              "bottom_quartile": disp(bot)}
        top_sd.append(disp(top)["sd_P1"])
        bot_sd.append(disp(bot)["sd_P1"])
    out["top_sd_trend"] = trend(YEARS, top_sd)
    out["bottom_sd_trend"] = trend(YEARS, bot_sd)
    out["delta_top_sd_2024_1996"] = top_sd[-1] - top_sd[0]
    out["delta_bottom_sd_2024_1996"] = bot_sd[-1] - bot_sd[0]
    out["asymmetry"] = ("top_only" if (top_sd[-1] - top_sd[0]) > 0.02
                        and (bot_sd[-1] - bot_sd[0]) < 0.02
                        else "bidirectional" if (top_sd[-1] - top_sd[0]) > 0.02
                        and (bot_sd[-1] - bot_sd[0]) > 0.02
                        else "neither")
    return out


def main():
    panel = dp.load()
    t1 = test1(panel)
    t2 = test2(panel)
    OUT1.write_text(json.dumps(t1, indent=1))
    OUT2.write_text(json.dumps(t2, indent=1))

    print("=== TEST 1 — P1 vs log GDP coupling (balanced, N=%d) ===" % panel["n_balanced"])
    for y in YEARS:
        b = t1["balanced"]["per_year"][y]
        print(f"  {y}: r={b['pearson_r']:+.3f} (p={b['pearson_p']:.3f})  "
              f"rho={b['spearman_rho']:+.3f}  R2={b['R2']:.3f}  n={b['n']}")
    s = t1["balanced"]["summary"]
    print(f"  r-trend slope={s['r_trend']['slope']:+.5f}/yr p={s['r_trend']['p']:.3f} | "
          f"Δr(2024-1996)={s['delta_r_2024_1996']:+.3f}")
    print("  historical (rule-of-law vs log Maddison GDP):")
    for a, v in t1["historical"]["per_anchor"].items():
        if v:
            print(f"    {a}: r={v['pearson_r']:+.3f} R2={v['R2']:.3f} n={v['n']}")
    ht = t1["historical"]["r_trend"]
    if ht:
        print(f"    hist r-trend slope={ht['slope']:+.6f}/yr p={ht['p']:.3f}")

    print("\n=== TEST 2 — P1 dispersion within income quartiles ===")
    for y in YEARS:
        tq = t2["per_year"][y]["top_quartile"]
        bq = t2["per_year"][y]["bottom_quartile"]
        print(f"  {y}: TOP sd={tq['sd_P1']:.3f} iqr={tq['iqr_P1']:.3f} | "
              f"BOT sd={bq['sd_P1']:.3f} iqr={bq['iqr_P1']:.3f}")
    print(f"  top-sd trend slope={t2['top_sd_trend']['slope']:+.5f}/yr "
          f"Δ={t2['delta_top_sd_2024_1996']:+.3f} | "
          f"bot-sd Δ={t2['delta_bottom_sd_2024_1996']:+.3f} | asym={t2['asymmetry']}")


if __name__ == "__main__":
    main()
