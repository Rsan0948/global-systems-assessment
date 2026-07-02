#!/usr/bin/env python3
"""
Enrich each fully-measured country with its structurally-nearest neighbours - the
countries whose five-pillar shape is closest. Powers the "similar countries"
exploration on the site. Run after build_site_dataset.py.

Only full-coverage (5/5) countries take part, so the comparison is fair.
"""
import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent.parent / "mi-website" / "web" / "public" / "data"
P = ["P1", "P2", "P3", "P4", "P5"]


def main():
    countries = json.load(open(OUT / "countries.json"))
    full = [c for c in countries if c["coverage"]["present"] == 5]

    def dist(a, b):
        return math.sqrt(sum((a["pillars"][k] - b["pillars"][k]) ** 2 for k in P))

    n = 0
    for c in full:
        nearest = sorted((o for o in full if o["slug"] != c["slug"]),
                         key=lambda o: (dist(c, o), o["slug"]))[:5]  # slug tiebreak for determinism
        block = [{"slug": o["slug"], "name": o["name"], "mi": o["mi"], "tier": o["tier"]} for o in nearest]
        fp = OUT / "country" / f"{c['slug']}.json"
        data = json.load(open(fp))
        data["similar"] = block
        json.dump(data, open(fp, "w"), indent=1)
        n += 1
    print(f"Enriched {n} full-coverage countries with structural neighbours.")


if __name__ == "__main__":
    main()
