"""
Governance fragmentation census -- how DESIGNED governance systems fracture,
placed against the self-organized baseline (rivers/trees/neurons/languages, the
concentrated ~3 band with CV ~0.2 that beats its random null).

    python run.py   -> results/governance.json

Thesis (MASTER_REFERENCE 1.4-1.5): self-organized systems fracture in a tight,
predictable band; designed/imposed systems fracture DISPERSEDLY, with severity
set by how long fragmentation was suppressed and how porous the structure is.
"""

from __future__ import annotations

import json
import os

import state_dissolutions
import party_splits
import denominations
import admin_subdivisions

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "..", "results")


def main():
    states = state_dissolutions.analyze()
    parties = party_splits.analyze()
    denoms = denominations.analyze()
    admin = admin_subdivisions.analyze()
    out = {
        "baseline_self_organized": {"systems": ["rivers", "trees", "neurons", "languages"],
                                    "factor_band": "2.9-3.8", "CV": "0.11-0.25",
                                    "beats_random_null": True},
        "designed_systems": {
            "corporate_splits": {"factor": 2.24, "CV": 0.31, "data": "systematic (EDGAR)",
                                 "note": "sits AT its binary null (trivial)"},
            "party_splits": {"factor": parties["split_factor_mean"], "CV": parties["CV"],
                             "range": parties["split_factor_range"], "n": parties["n_splits"],
                             "data": "systematic (ParlGov)"},
            "admin_subdivisions": {"fanout_mean": admin["admin2_per_admin1"]["mean_fanout"],
                                   "CV": admin["CV"], "range": admin["admin2_per_admin1"]["range"],
                                   "n": admin["admin2_per_admin1"]["n_parents"],
                                   "data": "systematic (GeoNames)"},
            "state_dissolutions": {"factor": states["successor_mean"], "CV": states["successor_CV"],
                                   "range": states["successor_range"], "n": states["n_events"],
                                   "data": "curated"},
        },
        "suppression_to_release_law (states, MASTER 1.5)": {
            "violent_mean_suppression_years": states["violent_mean_suppression"],
            "peaceful_mean_suppression_years": states["peaceful_mean_suppression"],
            "violent_mean_successors": states["violent_mean_successors"],
            "peaceful_mean_successors": states["peaceful_mean_successors"],
            "spearman_suppression_vs_successors": states["spearman_suppression_vs_successors"],
        },
        "porosity_axis (religion, MASTER 1.3)": {
            "spearman_porosity_vs_log_bodies": denoms["spearman_porosity_vs_log_bodies"],
            "central_authority_mean_bodies": denoms["central_authority_mean_bodies"],
            "congregational_mean_bodies": denoms["congregational_mean_bodies"],
        },
        "headline": "Self-organized systems (incl. human language) fracture in a tight "
                    "~3 band (CV ~0.2) that beats chance. Designed governance fractures "
                    "DISPERSED, rising with how engineered the structure is: corporate "
                    "CV 0.31, party splits 0.58, state dissolutions 0.90 (range 2-15), "
                    "admin subdivisions 1.2-2.3 (fan-out ~17) -- up to ~10x the natural "
                    "spread. Severity tracks suppression (violent breakups ~53y vs ~10y) "
                    "and porosity (central religions ~7 bodies vs congregational ~322).",
        "data_caveats": "SYSTEMATIC: corporate (EDGAR), party_splits (ParlGov), "
                        "admin_subdivisions (GeoNames). CURATED (flagged): "
                        "state_dissolutions, denominations -- no systematic free "
                        "successor/schism data exists. Qualitative confirmation.",
    }
    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "governance.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
