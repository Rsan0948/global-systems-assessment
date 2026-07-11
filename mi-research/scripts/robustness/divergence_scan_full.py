#!/usr/bin/env python3
"""
DANGEROUS-DIVERGENCE SCAN — FULL longitudinal universe. Companion to divergence_scan.py
(which is limited to the canonical panel's 90-country longitudinal arm). This version
screens the COMPLETE WB longitudinal source that underlies the canonical panel
(`mi-pipeline/data/wb_cached.csv`, ~215 economies with WGI + GDP-pc PPP 1996->latest),
so countries the canonical store keeps only as 2024 snapshots (USA, NLD, ECU, PRT, ...)
are now assessable.

Criteria (earliest -> latest full-coverage year): GDP-pc PPP grew > 20% AND mean of the
four P1 WGI indicators (0-100) moved < +2 pts. Also emits the inverse — the biggest
institutional RISERS. Gap on a consistent GDP-only P4. Read-only.
"""
from __future__ import annotations
import csv
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from mi.scoring import normalize_gdp_ppp  # noqa: E402

WB = ROOT.parent / "mi-pipeline/data/wb_cached.csv"
FORM = ROOT / "data/robustness/formation/state_formation.json"
OUT = ROOT / "data/robustness/convergence/divergence_scan_full.json"
WGI = ["GovEff", "RuleLaw", "RegQual", "CtrlCorr"]
GROWTH_MIN, P1_MOVE_MAX = 20.0, 2.0


def p1(r):
    vs = [r.get(k) for k in WGI]
    return None if any(v in (None, "") for v in vs) else float(np.mean([float(v) for v in vs]))


def gdp(r):
    v = r.get("GDPpcPPP")
    return float(v) if v not in (None, "") else None


def load():
    D = {}
    for r in csv.DictReader(open(WB, encoding="utf-8")):
        D.setdefault(r["iso3"], {})[r["year"]] = r
    return D


def formation():
    form = json.loads(FORM.read_text())
    classes = form.get("states", form)
    return {k: (v.get("group") if isinstance(v, dict) else v) for k, v in classes.items()}


def endpoints(yr):
    good = sorted(y for y in yr if p1(yr[y]) is not None and gdp(yr[y]) is not None)
    return (good[0], good[-1]) if len(good) >= 2 else (None, None)


def main():
    D = load(); F = formation()
    qual, risers = [], []
    screened = 0
    for iso, yr in D.items():
        y0, y1 = endpoints(yr)
        if y0 is None:
            continue
        screened += 1
        g = (gdp(yr[y1]) / gdp(yr[y0]) - 1) * 100
        dp = p1(yr[y1]) - p1(yr[y0])
        rec = {"iso": iso, "name": yr[y1]["country"], "y0": y0, "y1": y1,
               "gdp_growth_pct": round(g, 1), "dP1avg_pts": round(dp, 2),
               "p1avg_start": round(p1(yr[y0]), 2), "p1avg_current": round(p1(yr[y1]), 2),
               "gdp_current": round(gdp(yr[y1]), 0),
               "gap_delta": round(normalize_gdp_ppp(gdp(yr[y1])) - p1(yr[y1]) / 100
                                  - (normalize_gdp_ppp(gdp(yr[y0])) - p1(yr[y0]) / 100), 3),
               "formation": F.get(iso, "unclassified"), "p1_declined": bool(dp < 0)}
        if g > GROWTH_MIN and dp < P1_MOVE_MAX:
            qual.append(rec)
        if g > GROWTH_MIN and dp > 0:  # institutions rose while wealth grew (inverse)
            risers.append(rec)

    if qual:
        gg = np.array([r["gdp_growth_pct"] for r in qual]); dd = np.array([r["dP1avg_pts"] for r in qual])
        gz = (gg - gg.mean()) / gg.std(); dz = ((-dd) - (-dd).mean()) / (-dd).std()
        for i, r in enumerate(qual):
            r["divergence_score"] = round(float(gz[i] + dz[i]), 3)
    qual.sort(key=lambda r: -r["divergence_score"])
    risers.sort(key=lambda r: -r["dP1avg_pts"])

    out = {"source": "mi-pipeline/data/wb_cached.csv (full WB longitudinal panel underlying the canonical store)",
           "criteria": {"gdp_growth_gt_pct": GROWTH_MIN, "p1_move_lt_pts": P1_MOVE_MAX,
                        "p1": "mean of GovEff/RuleLaw/RegQual/CtrlCorr on 0-100 WGI scale",
                        "window": "earliest->latest full-coverage year per country"},
           "n_screened": screened, "n_qualifying": len(qual),
           "n_active_decline": sum(1 for r in qual if r["p1_declined"]),
           "qualifiers": qual, "risers": risers}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"screened={screened}  qualifying={len(qual)}  active-decline={out['n_active_decline']}  risers={len(risers)}")


if __name__ == "__main__":
    main()
