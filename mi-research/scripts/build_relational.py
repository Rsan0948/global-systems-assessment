#!/usr/bin/env python3
"""
Enrich the site's country files with the T3 relational/exposure read, where we have it.

Runs the validated T3 engine (mi.relational) over its records and, for any record whose
country matches a scored country on the site, writes a `relational` block into that
country's JSON - exposure (structural vs net), response, patron shield, the 2x2 reading.
These are historical snapshots (the relational layer is rolled out case by case), tagged
with their year and provenance tier. Run AFTER build_site_dataset.py.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mi.relational import load_records, relational_reading

OUT = Path(__file__).resolve().parent.parent.parent / "mi-website" / "web" / "public" / "data" / "country"


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def main():
    recs = load_records()
    written = []
    for key in recs:
        unit, _, yr = key.partition("@")
        try:
            r = relational_reading(unit, int(yr) if yr else None)
        except Exception:
            continue
        slug = slugify(unit)
        fpath = OUT / f"{slug}.json"
        if not fpath.exists():
            continue  # only enrich countries that are actually on the site
        ex, rp = r["exposure"], r["response"]
        block = {
            "year": r["year"],
            "tier": r["provenance_tier"],
            "label": r["label"],
            "exposure_structural": round(ex["E_structural"], 3) if ex["E_structural"] is not None else None,
            "exposure_structural_band": ex["structural_band"],
            "exposure_net": round(ex["E"], 3) if ex["E"] is not None else None,
            "patron_present": ex["patron_present"],
            "response": round(rp["R"], 3) if rp["R"] is not None else None,
            "response_band": rp["band"],
            "joint_reading": r["joint_reading"],
            "outcome_factual": r["outcome_factual"],
        }
        data = json.load(open(fpath))
        data["relational"] = block
        json.dump(data, open(fpath, "w"), indent=1)
        written.append(f"{slug}@{r['year']} [{r['provenance_tier']}]")
    print(f"Enriched {len(written)} country files with the relational layer:")
    for w in written:
        print(f"  {w}")


if __name__ == "__main__":
    main()
