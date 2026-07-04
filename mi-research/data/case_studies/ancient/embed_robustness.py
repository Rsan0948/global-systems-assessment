#!/usr/bin/env python3
"""Embed robustness summaries from Monte Carlo + pillar analysis into ancient_cases.json.

Adds a `robustness` block to each case with:
  - MI rank range (min/max/median across 10k runs)
  - per-pillar ironclad claims count (how many others this case clearly beats)
  - overall confidence assessment
"""
import json
from pathlib import Path

def main():
    base = Path(__file__).parent
    cases = json.load(open(base / "ancient_cases.json"))
    mc = json.load(open(base / "montecarlo_report.json"))
    pa = json.load(open(base / "pillar_analysis_report.json"))

    mi_stability = {r["case"]: r for r in mc["mi_rank_stability"]}
    pillar_rankings = pa["pillar_rankings"]
    profiles = {p["case"]: p for p in pa["profiles"]}

    for case in cases:
        name = case["name"]
        ms = mi_stability.get(name, {})
        prof = profiles.get(name, {})

        ironclad_by_pillar = {}
        for p in ["P1", "P2", "P3", "P4", "P5"]:
            ranking = pillar_rankings[p]["ranking"]
            entry = next((r for r in ranking if r["case"] == name), None)
            ironclad_by_pillar[p] = entry["beats_clearly"] if entry else 0

        total_ironclad = sum(ironclad_by_pillar.values())
        max_possible = (len(cases) - 1) * 5

        if total_ironclad > max_possible * 0.5:
            confidence = "HIGH"
        elif total_ironclad > max_possible * 0.2:
            confidence = "MODERATE"
        else:
            confidence = "LOW"

        case["robustness"] = {
            "method": "Monte Carlo 10k runs + pillar band analysis",
            "mi_rank": {
                "point": ms.get("base_rank"),
                "median": ms.get("median"),
                "range": [ms.get("min"), ms.get("max")],
                "iqr": ms.get("iqr"),
            },
            "pillar_claims_that_survive_uncertainty": ironclad_by_pillar,
            "total_defensible_claims": total_ironclad,
            "max_possible_claims": max_possible,
            "confidence": confidence,
            "strongest_pillar": prof.get("strongest"),
            "weakest_pillar": prof.get("weakest"),
            "profile_shape_robust": prof.get("robust", False),
            "note": (
                "Track 3 cases are best compared at the pillar level, not by composite MI. "
                "The composite rank can wobble significantly under uncertainty; pillar-level "
                "claims flagged here survive 10,000 Monte Carlo alternative scorings."
            ),
        }

    out_path = base / "ancient_cases.json"
    out_path.write_text(json.dumps(cases, indent=2))
    print(f"Embedded robustness summaries into {len(cases)} cases")
    print(f"Wrote {out_path} ({out_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
