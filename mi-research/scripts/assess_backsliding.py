#!/usr/bin/env python3
"""CLI for the backsliding-risk diagnostic (mi/backsliding.py).

    python scripts/assess_backsliding.py --country "Hungary"
    python scripts/assess_backsliding.py --country Netherlands --year 2024
    python scripts/assess_backsliding.py --universe --top 20      # safest countries
    python scripts/assess_backsliding.py --universe --risk        # highest-risk (danger zone)
"""
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mi import backsliding as B


def _print_one(r):
    if not r:
        print("no data for that country/year"); return
    print(f"\n{r['iso3']}  ({r['year']})")
    print(f"  rule-of-law capacity : {r['capacity_rule_of_law']}  (percentile {r['capacity_percentile']:.2f})")
    print(f"  band                 : {r['band'].upper()}")
    print(f"  5y backslide hazard  : {r['backslide_hazard_5y']:.1%}  (empirical, for this capacity decile)")
    print(f"  safety ceiling (>80th): {'YES — structurally protected' if r['safety_ceiling'] else 'no'}")
    print(f"  mid-capacity danger  : {'YES — hybrid/anocratic peak-risk zone' if r['danger_zone'] else 'no'}")
    print(f"  relational cap−voice : {r['relational_capacity_gap']}  ({'capacity ahead' if (r['relational_capacity_gap'] or 0)>=0 else 'voice ahead of capacity — risk direction'})")
    print(f"  note                 : {r['relational_note']}")
    print(f"  provenance           : {r['provenance']}")


def main():
    ap = argparse.ArgumentParser(description="Structural backsliding-risk diagnostic (additive to MI v3.3)")
    ap.add_argument("--country")
    ap.add_argument("--year", type=int, default=2024)
    ap.add_argument("--universe", action="store_true")
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--risk", action="store_true", help="show highest-risk (danger-zone) instead of safest")
    a = ap.parse_args()
    if a.country:
        _print_one(B.backsliding_risk(a.country, a.year))
    elif a.universe:
        u = B.universe_backsliding(a.year)
        if a.risk:
            u = sorted(u, key=lambda r: -(r["backslide_hazard_5y"] or 0))
            print(f"\nHIGHEST structural backsliding risk ({a.year}):")
        else:
            print(f"\nSAFEST (highest capacity, above the ceiling) ({a.year}):")
        print(f"  {'iso':>4} {'cap':>6} {'pctl':>6} {'hazard':>8}  band")
        for r in u[:a.top]:
            print(f"  {r['iso3']:>4} {r['capacity_rule_of_law']:>6} {r['capacity_percentile']:>6.2f} "
                  f"{r['backslide_hazard_5y']:>8.1%}  {r['band']}")
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
