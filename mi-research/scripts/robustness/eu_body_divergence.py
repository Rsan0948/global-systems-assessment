#!/usr/bin/env python3
"""
"Treat the EU as one big body" — does the EU-27, aggregated into a single polity, exhibit
the dangerous-divergence configuration (wealth up, institutions flat/declining)?

The answer is weighting-dependent, and that IS the finding: population- and GDP-weighted
(i.e. the EU as an actual unified polity/economy) it DIVERGES — institutions declined while
wealth grew, like the US/UK/France pattern; one-country-one-vote it does NOT — the small
eastern-accession risers (Baltics, Croatia, Slovenia, Poland, Romania) outvote the eroding
western core (Germany, France, Italy, Spain, Netherlands). The EU's institutional gains came
from new members catching up; its per-capita/per-dollar quality drifted down.

WGI + GDP-pc PPP from the full WB longitudinal panel (mi-pipeline/data/wb_cached.csv). Fixed
2024 populations (Eurostat order-of-magnitude, millions) as weights, applied to BOTH endpoints
so the aggregate reflects institutional/wealth CHANGE, not demographic reweighting. Read-only.
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
OUT = ROOT / "data/robustness/convergence/eu_body_divergence.json"
WGI = ["GovEff", "RuleLaw", "RegQual", "CtrlCorr"]

POP = {"DEU": 83.5, "FRA": 68.3, "ITA": 59.0, "ESP": 48.6, "POL": 36.7, "ROU": 19.0,
       "NLD": 17.9, "BEL": 11.7, "CZE": 10.9, "SWE": 10.6, "PRT": 10.6, "GRC": 10.4,
       "HUN": 9.6, "AUT": 9.1, "BGR": 6.4, "DNK": 5.9, "FIN": 5.6, "SVK": 5.4, "IRL": 5.3,
       "HRV": 3.9, "LTU": 2.9, "SVN": 2.1, "LVA": 1.9, "EST": 1.4, "CYP": 0.9, "LUX": 0.7,
       "MLT": 0.5}


def load():
    D = {}
    for r in csv.DictReader(open(WB, encoding="utf-8")):
        D.setdefault(r["iso3"], {})[r["year"]] = r
    return D


def main():
    D = load()

    def p1(iso, y):
        r = D.get(iso, {}).get(str(y))
        if not r:
            return None
        vs = [r.get(k) for k in WGI]
        return None if any(v in (None, "") for v in vs) else float(np.mean([float(v) for v in vs]))

    def gdp(iso, y):
        r = D.get(iso, {}).get(str(y))
        v = r.get("GDPpcPPP") if r else None
        return float(v) if v not in (None, "") else None

    def agg(y):
        isos = [i for i in POP if p1(i, y) is not None and gdp(i, y) is not None]
        pop = np.array([POP[i] for i in isos]); p = np.array([p1(i, y) for i in isos])
        g = np.array([gdp(i, y) for i in isos])
        return {"n": len(isos), "missing": [i for i in POP if i not in isos],
                "p1_popw": float(np.average(p, weights=pop)),
                "p1_gdpw": float(np.average(p, weights=g * pop)),
                "p1_equal": float(p.mean()),
                "gdp_popw": float(np.average(g, weights=pop)),
                "gdp_equal": float(g.mean())}

    a0, a1 = agg(1996), agg(2024)
    variants = {}
    for lab, pk, gk in [("population_weighted", "p1_popw", "gdp_popw"),
                        ("gdp_weighted", "p1_gdpw", "gdp_popw"),
                        ("equal_per_country", "p1_equal", "gdp_equal")]:
        dp = a1[pk] - a0[pk]; gg = (a1[gk] / a0[gk] - 1) * 100
        gap = (normalize_gdp_ppp(a1[gk]) - a1[pk] / 100) - (normalize_gdp_ppp(a0[gk]) - a0[pk] / 100)
        variants[lab] = {"p1_1996": round(a0[pk], 2), "p1_2024": round(a1[pk], 2),
                         "dP1avg_pts": round(dp, 2), "gdp_1996": round(a0[gk]), "gdp_2024": round(a1[gk]),
                         "gdp_growth_pct": round(gg, 1), "gap_delta": round(gap, 3),
                         "divergence": bool(gg > 20 and dp < 2), "p1_declined": bool(dp < 0)}

    out = {"body": "EU-27", "n_members_with_data": a1["n"], "missing": a1["missing"],
           "weights": "fixed 2024 populations (millions), applied to both endpoints",
           "caveat": "eastern members were not EU members in 1996; this is a counterfactual "
                     "'as if these 27 were one polity throughout'. Time-varying populations would "
                     "shift weights (western pop grew via migration, eastern shrank) but would not "
                     "flip the population/GDP-weighted decline, which is driven by the large core.",
           "variants": variants}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))

    print(f"EU-27 as one body (n={a1['n']}/27), 1996 -> 2024:\n")
    for lab, v in variants.items():
        tag = "P1 DECLINED" if v["p1_declined"] else "P1 rose"
        print(f"  [{lab:<20}] P1 {v['p1_1996']}->{v['p1_2024']} (Δ{v['dP1avg_pts']:+.2f})  "
              f"GDP-pc {v['gdp_1996']}->{v['gdp_2024']} (+{v['gdp_growth_pct']}%)  "
              f"divergence={v['divergence']} ({tag})")


if __name__ == "__main__":
    main()
