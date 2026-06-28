#!/usr/bin/env python3
"""Global Systems Measurement CLI — the system-level category (see mi/global_systems.py).

  python scripts/global_systems.py            # measure the current world system
  python scripts/global_systems.py --year 1980 --json
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mi.global_systems import measure_global_system  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--year", type=int, default=2024)
ap.add_argument("--json", action="store_true")
a = ap.parse_args()
m = measure_global_system(a.year)

if a.json:
    print(json.dumps(m, indent=2)); sys.exit()

print(f"\n=== GLOBAL SYSTEMS MEASUREMENT — as of {m['as_of']} (10y windows) ===\n")
print(f"IMPROVEMENT ENGINES ({m['engines_firing']}/3 firing vs historical norm):")
for k, e in m["engines"].items():
    if e.get("available") is False:
        print(f"  {k:14}: no data"); continue
    print(f"  {k:14}: climb {e['climb_rate']*100:3.0f}%  decline {e['decline_rate']*100:3.0f}%  "
          f"(median {e['historical_median']*100:.0f}%)  -> {'FIRING' if e['firing'] else 'quiet'}")
c = m.get("container", {})
if c:
    print(f"\nINSTITUTIONAL CONTAINER:")
    print(f"  trailing (decade behind): net {c['net_trailing']*100:+.0f}pp -> {c['trajectory_trailing'].upper()}")
    fn = c['net_forward']
    fns = f"net {fn*100:+.0f}pp" if fn is not None else "unobservable (future)"
    print(f"  FORWARD (the discriminator): {fns} -> {c['trajectory_forward'].upper()}")
    print(f"    {c['forward_reading']}")
    print(f"TEXTURE (trailing): {m.get('texture','?').upper()}")
md = m.get("movement_distribution", {})
if md.get("available") is not False:
    print(f"\nMOVEMENT DISTRIBUTION (countries, {md['window']}, n={md['n']}):")
    for k, v in md["share"].items():
        print(f"  {k:18}: {v*100:.0f}%")
print("\ncaveats:")
for cv in m["caveats"]:
    print(f"  - {cv}")
