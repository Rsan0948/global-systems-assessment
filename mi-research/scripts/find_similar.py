#!/usr/bin/env python3
"""
Find countries with the most similar MI configuration to a target.

Similarity = Euclidean distance over the shared pillar scores (P1-P5) at the
given year, across every country in the MI universe (via the multi-tier panel,
the same coverage the site has). Ordinal/diagnostic aid only — not a calibrated
forecast.

Usage:
    python scripts/find_similar.py --country "Rwanda" --year 2024
    python scripts/find_similar.py --country "Norway" --top 5
"""
import argparse
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mi.panel import all_indicators, indicators_for
from mi.scoring import score_country

PILLARS = ["P1", "P2", "P3", "P4", "P5"]


def _dist(a, b):
    shared = [p for p in PILLARS if a.get(p) is not None and b.get(p) is not None]
    if not shared:
        return None, 0
    return math.sqrt(sum((a[p] - b[p]) ** 2 for p in shared)), len(shared)


def main():
    ap = argparse.ArgumentParser(description="Find similar MI configurations")
    ap.add_argument("--country", required=True)
    ap.add_argument("--year", type=int, default=2024)
    ap.add_argument("--top", type=int, default=5)
    args = ap.parse_args()

    tgt_ind = indicators_for(args.country, args.year)
    if not tgt_ind:
        print(f"No data for {args.country} at {args.year} (not in the MI universe).")
        sys.exit(1)
    tgt = score_country(tgt_ind)["pillar_scores"]

    tkey = args.country.strip().lower()
    results = []
    for iso, (name, ind) in all_indicators(args.year).items():
        if name.lower() == tkey or iso.lower() == tkey:
            continue
        pil = score_country(ind)["pillar_scores"]
        d, n = _dist(tgt, pil)
        if d is not None:
            results.append((d, n, name))
    results.sort(key=lambda x: (x[0], x[2]))  # slug/name tiebreak → deterministic

    print(f"\nNearest MI configurations to {args.country} ({args.year}) "
          f"[P1-P5 Euclidean distance; lower = more similar]:")
    if not results:
        print("  (no other countries with overlapping pillars at this year)")
    for d, n, name in results[: args.top]:
        print(f"  {name:<24} distance={d:.3f}  (over {n} shared pillars)")
    print()


if __name__ == "__main__":
    main()
