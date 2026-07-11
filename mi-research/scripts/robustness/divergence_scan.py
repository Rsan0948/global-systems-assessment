#!/usr/bin/env python3
"""
DANGEROUS-DIVERGENCE SCAN — the configuration Finding 15 / the durability gate detect:
wealth growing while institutional quality stagnates or declines.

Universe: the canonical panel's longitudinal set (countries with the four WGI indicators
+ GDP-pc PPP at >=2 years). Criteria (earliest -> latest available point):
  (1) GDP-pc PPP grew > 20%
  (2) mean of the four P1 WGI indicators (Government Effectiveness, Rule of Law,
      Regulatory Quality, Control of Corruption; 0-100 scale) declined OR moved < +2 pts

Per qualifier: name, GDP growth %, ΔP1avg (pts), P4-P1 gap direction, current GDP-pc,
current P1avg, formation class. Sorted by divergence magnitude = z(GDP growth) +
z(-ΔP1avg) (large growth AND large institutional decline both rank high). Acute-risk
subset = P1avg actively DECLINED. Read-only.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from mi import panel  # noqa: E402
from mi.scoring import normalize_gdp_ppp  # noqa: E402

WGI = ["gov_effectiveness", "rule_of_law", "regulatory_quality", "control_of_corruption"]
FORM = ROOT / "data/robustness/formation/state_formation.json"
OUT = ROOT / "data/robustness/convergence/divergence_scan.json"
GROWTH_MIN = 20.0        # % GDP-pc PPP growth
P1_MOVE_MAX = 2.0        # ΔP1avg must be < +2 pts (stagnate or decline)
GAP_BAND = 0.02          # |Δ(P4-P1)| < band => "stable"


def p1avg(ind):
    vals = [ind.get(k) for k in WGI]
    if any(v is None for v in vals):
        return None
    return float(np.mean(vals))


def has_all(ind):
    return (ind and p1avg(ind) is not None and ind.get("gdp_per_capita_ppp") is not None)


def load_formation():
    form = json.loads(FORM.read_text())
    classes = form.get("states", form)
    return {iso: (v.get("group") if isinstance(v, dict) else v) for iso, v in classes.items()}


def gap_gdp_only(ind):
    """P4-P1 durability gap on a CONSISTENT GDP-only P4 (so the gap direction is not an
    artifact of resource/ODA inputs being present in one year but not the other). P4* =
    normalize_gdp_ppp(GDP); P1 = WGI-average rescaled to [0,1]. Gap = P4* - P1."""
    gdp = ind.get("gdp_per_capita_ppp")
    pa = p1avg(ind)
    if gdp is None or pa is None:
        return None
    return float(normalize_gdp_ppp(gdp) - pa / 100.0)


def main():
    canon = panel._canonical()
    form = load_formation()
    rows = []
    for iso, rec in canon.items():
        iby = rec["indicators_by_year"]
        yrs = sorted(int(y) for y in iby if has_all(iby[y]))
        if len(yrs) < 2:
            continue
        y0, y1 = yrs[0], yrs[-1]
        i0, i1 = iby[str(y0)], iby[str(y1)]
        g0, g1 = i0["gdp_per_capita_ppp"], i1["gdp_per_capita_ppp"]
        if g0 <= 0:
            continue
        growth = (g1 / g0 - 1.0) * 100.0
        p0, p1 = p1avg(i0), p1avg(i1)
        dP1 = p1 - p0
        if not (growth > GROWTH_MIN and dP1 < P1_MOVE_MAX):
            continue
        gap0 = gap_gdp_only(i0)
        gap1 = gap_gdp_only(i1)
        if gap0 is not None and gap1 is not None:
            dgap = gap1 - gap0
            gdir = ("widening" if dgap > GAP_BAND else "closing" if dgap < -GAP_BAND else "stable")
        else:
            dgap, gdir = None, "n/a"
        rows.append({
            "iso": iso, "name": rec["name"], "y0": y0, "y1": y1,
            "gdp_growth_pct": round(growth, 1),
            "dP1avg_pts": round(dP1, 2),
            "p1avg_start": round(p0, 2), "p1avg_current": round(p1, 2),
            "gdp_current": round(g1, 0),
            "gap_start": round(gap0, 3) if gap0 is not None else None,
            "gap_current": round(gap1, 3) if gap1 is not None else None,
            "gap_delta": round(dgap, 3) if dgap is not None else None,
            "gap_direction": gdir,
            "formation": form.get(iso, "unclassified"),
            "p1_declined": bool(dP1 < 0),
        })

    # divergence magnitude = z(growth) + z(-dP1)
    if rows:
        gr = np.array([r["gdp_growth_pct"] for r in rows], float)
        dp = np.array([r["dP1avg_pts"] for r in rows], float)
        gz = (gr - gr.mean()) / (gr.std() or 1)
        dz = ((-dp) - (-dp).mean()) / ((-dp).std() or 1)
        for i, r in enumerate(rows):
            r["divergence_score"] = round(float(gz[i] + dz[i]), 3)
    rows.sort(key=lambda r: -r["divergence_score"])

    acute = [r for r in rows if r["p1_declined"]]
    n_long = sum(1 for iso, rec in canon.items()
                 if len([y for y in rec["indicators_by_year"] if has_all(rec["indicators_by_year"][y])]) >= 2)

    out = {"criteria": {"gdp_growth_gt_pct": GROWTH_MIN, "p1_move_lt_pts": P1_MOVE_MAX,
                        "p1_definition": "mean of GE/RoL/RQ/CoC on 0-100 WGI scale",
                        "window": "earliest->latest available canonical year per country"},
           "universe": {"canonical_total": len(canon),
                        "longitudinal_assessable": n_long,
                        "note": "%d countries have <2 full-coverage years (mostly 2024-only snapshots) and cannot be assessed longitudinally" % (len(canon) - n_long)},
           "n_qualifying": len(rows), "n_acute_declining": len(acute),
           "qualifiers": rows, "acute_risk_declining": [r["iso"] for r in acute]}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))

    print(f"Universe: {len(canon)} canonical countries; {n_long} longitudinally assessable "
          f"(the rest are 2024-only snapshots).")
    print(f"Criteria: GDP-pc growth > {GROWTH_MIN:.0f}% AND ΔP1avg < +{P1_MOVE_MAX:.0f} pts "
          f"(0-100 WGI mean), earliest->latest.\n")
    print(f"{len(rows)} COUNTRIES EXHIBIT THE DIVERGENCE CONFIGURATION "
          f"(sorted by divergence magnitude):\n")
    hdr = (f"{'#':>2} {'Country':<24}{'GDPgrw%':>9}{'ΔP1':>7}{'P1now':>7}{'GDPnow':>9}"
           f"  {'gapΔ':>6} {'gap dir':<9}{'formation':<15}")
    print(hdr); print("-" * len(hdr))
    for n, r in enumerate(rows, 1):
        star = " *DECLINE" if r["p1_declined"] else ""
        gd = f"{r['gap_delta']:+.3f}" if r["gap_delta"] is not None else "  n/a"
        print(f"{n:>2} {r['name']:<24}{r['gdp_growth_pct']:>9}{r['dP1avg_pts']:>7}{r['p1avg_current']:>7}"
              f"{int(r['gdp_current']):>9}  {gd:>6} {r['gap_direction']:<9}{str(r['formation']):<15}{star}")

    print(f"\n=== ACUTE-RISK: P1 ACTIVELY DECLINED while GDP grew ({len(acute)} countries) ===")
    print("(the exact configuration Safeguard J / the durability gate is built to detect)\n")
    for n, r in enumerate(acute, 1):
        yr = f"{r['y0']}-{r['y1']}"
        print(f"{n:>2} {r['name']:<24} GDP +{r['gdp_growth_pct']}%  ΔP1avg {r['dP1avg_pts']} pts "
              f"({r['p1avg_start']}->{r['p1avg_current']})  gap {r['gap_direction']}  [{yr}] {r['formation']}")


if __name__ == "__main__":
    main()
