#!/usr/bin/env python3
"""
Find countries with the most similar MI configuration to a target.

Similarity = Euclidean distance over available pillar scores (P1-P5) at the
given year, across all countries in data/countries/. Ordinal/diagnostic aid
only — not a calibrated forecast.

Usage:
    python scripts/find_similar.py --country "Rwanda" --year 2023
    python scripts/find_similar.py --country "Venezuela" --year 2023 --top 5
"""
import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mi.scoring import score_country

DATA = Path(__file__).parent.parent / "data" / "countries"
PILLARS = ["P1", "P2", "P3", "P4", "P5"]


def _pillars_for(path, year):
    data = json.loads(path.read_text())
    ind = None
    if year is not None:
        ind = data.get("indicators_by_year", {}).get(str(year))
    if ind is None:
        ind = data.get("indicators")
    if ind is None:
        return None, data.get("country", path.stem)
    return score_country(ind)["pillar_scores"], data.get("country", path.stem)


def _dist(a, b):
    shared = [p for p in PILLARS if a.get(p) is not None and b.get(p) is not None]
    if not shared:
        return None, 0
    return math.sqrt(sum((a[p] - b[p]) ** 2 for p in shared)), len(shared)


def main():
    ap = argparse.ArgumentParser(description="Find similar MI configurations")
    ap.add_argument("--country", required=True)
    ap.add_argument("--year", type=int)
    ap.add_argument("--top", type=int, default=5)
    args = ap.parse_args()

    target_file = DATA / (args.country.lower().replace(" ", "_") + ".json")
    if not target_file.exists():
        print(f"No data for {args.country}. Create {target_file}")
        sys.exit(1)
    tgt, tname = _pillars_for(target_file, args.year)
    if tgt is None:
        print(f"No indicators for {args.country} at year {args.year}.")
        sys.exit(1)

    results = []
    for path in sorted(DATA.glob("*.json")):
        if path == target_file:
            continue
        pil, name = _pillars_for(path, args.year)
        if pil is None:
            continue
        d, n = _dist(tgt, pil)
        if d is not None:
            results.append((d, n, name))
    results.sort(key=lambda x: x[0])

    yr = f" ({args.year})" if args.year else ""
    print(f"\nNearest MI configurations to {tname}{yr} "
          f"[P1-P5 Euclidean distance; lower = more similar]:")
    if not results:
        print("  (no other countries with overlapping pillars at this year)")
    for d, n, name in results[: args.top]:
        print(f"  {name:<24} distance={d:.3f}  (over {n} shared pillars)")
    print()


if __name__ == "__main__":
    main()
