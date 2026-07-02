#!/usr/bin/env python3
"""
Compare two countries side-by-side under the Modernization Index.

Reports both pillar profiles, the MI scores, and applies the Mod4
margin-of-error gate to the P1 gap — abstaining from an ordinal call when the
gap is within the margin (the framework is ordinal/directional only).

Usage:
    python scripts/compare_countries.py --a "Rwanda" --b "DR Congo" --year 2023
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mi.scoring import score_country, load_country_data
from mi.safeguards import evaluate_mod4

MOD4_MARGIN = 0.10


def _load(country, year):
    data = load_country_data(country, year)
    if data is None:
        print(f"No data for {country}" + (f" at {year}" if year else "") +
              " in the canonical panel (mi/panel.py).")
        sys.exit(1)
    return data


def main():
    ap = argparse.ArgumentParser(description="Compare two countries under the MI")
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--year", type=int, default=2024)
    args = ap.parse_args()

    sa = score_country(_load(args.a, args.year))
    sb = score_country(_load(args.b, args.year))
    pa, pb = sa["pillar_scores"], sb["pillar_scores"]

    yr = f" ({args.year})" if args.year else ""
    print("\n" + "=" * 56)
    print(f"MI COMPARISON{yr}: {args.a}  vs  {args.b}")
    print("=" * 56)
    print(f"{'Pillar':<28}{args.a[:12]:>13}{args.b[:12]:>13}")
    print("-" * 56)
    for p in ["P1", "P2", "P3", "P4", "P5"]:
        va, vb = pa.get(p), pb.get(p)
        sva = f"{va:.3f}" if va is not None else "N/A"
        svb = f"{vb:.3f}" if vb is not None else "N/A"
        print(f"{p:<28}{sva:>13}{svb:>13}")
    print("-" * 56)
    ma, mb = sa.get("mi_score"), sb.get("mi_score")
    print(f"{'MI Score':<28}{(f'{ma:.3f}' if ma else 'N/A'):>13}{(f'{mb:.3f}' if mb else 'N/A'):>13}")

    # Mod4 gate on the P1 gap
    p1a, p1b = pa.get("P1"), pb.get("P1")
    if p1a is not None and p1b is not None:
        gap = p1a - p1b
        mod4 = evaluate_mod4({}, {"p1_comparison_gap": gap})
        print(f"\nP1 gap = {gap:+.3f} (margin {MOD4_MARGIN}).")
        if mod4["triggered"]:
            print(f"  Mod4 ABSTAIN — gap within margin; too close to call ordinally.")
        else:
            lead = args.a if gap > 0 else args.b
            print(f"  Ordinal call WARRANTED — higher P1: {lead}.")
    print()


if __name__ == "__main__":
    main()
