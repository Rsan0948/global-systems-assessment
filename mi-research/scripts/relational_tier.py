#!/usr/bin/env python3
"""
T3 Relational / Exposure Tier — CLI.

Score a polity's relational position (Exposure E x Response R) and print the joint reading.
This is a FIREWALLED third tier: it reads the MI pillars but changes no MI score, and
run_retrodiction.py never imports it. See docs/relational_tier_spec.md.

  python scripts/relational_tier.py --unit "Cyprus" --year 1974
  python scripts/relational_tier.py --all          # every T3 record (the Phase-2 proof)
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mi.relational import relational_reading, load_records


def _fmt(x):
    return "n/a" if x is None else f"{x:.3f}"


def _print(reading):
    print(f"\n=== {reading['unit']} @ {reading['year']}  [{reading['provenance_tier']} tier] ===")
    print(f"    {reading['label']}")
    ex, rp = reading["exposure"], reading["response"]
    patron = "patron-shielded" if ex["patron_present"] else "no patron"
    print(f"  EXPOSURE  structural = {_fmt(ex['E_structural'])} ({ex['structural_band']})"
          f"   net = {_fmt(ex['E'])} ({ex['band']})   [{patron}]")
    for k, v in ex["components"].items():
        print(f"      {k:28} {_fmt(v)}")
    print(f"  RESPONSE  R = {_fmt(rp['R'])}  ({rp['band']})   [pillars: {rp['pillar_source']}]")
    for k, v in rp["components"].items():
        print(f"      {k:28} {_fmt(v)}")
    print(f"  JOINT: {reading['joint_reading']}")
    print(f"  OUTCOME (factual): {reading['outcome_factual']}")
    print(f"  NB: {reading['DISCLAIMER']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--unit")
    ap.add_argument("--year", type=int)
    ap.add_argument("--all", action="store_true", help="print every T3 record")
    args = ap.parse_args()

    if args.all:
        for key in load_records():
            unit, _, yr = key.partition("@")
            _print(relational_reading(unit, int(yr) if yr else None))
        return
    if not args.unit:
        ap.error("give --unit (and optionally --year), or --all")
    _print(relational_reading(args.unit, args.year))


if __name__ == "__main__":
    main()
