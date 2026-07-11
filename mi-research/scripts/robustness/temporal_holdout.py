#!/usr/bin/env python3
"""
P2 — Temporal holdout (GENERATE half). Frozen prereg §Plan 2.

Reduced-contamination retrodiction: score every country with ONLY <year> data,
apply the SAME frozen mechanical rule set as P0, and emit predictions for
<year>->2024. Committed BEFORE any outcome data is fetched (generate-before-grade).

The mechanical predictions use pillar-level signals (P1, P4-P1 gap, pillar spread)
computed before weighting, so they are independent of the V1-vs-current weight
choice. Grading (GDP-pc growth, UCDP onset, BoC-CRAG default) is a separate step.

    python scripts/robustness/temporal_holdout.py 2004
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "robustness"))

from mi.panel import iter_universe          # noqa: E402
from mi.diagnostics import full_diagnostic   # noqa: E402
from prospective_freeze import predict        # SAME frozen rule set as P0

PREREG = ROOT / "docs" / "ROBUSTNESS_PREREGISTRATION.md"


def main():
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2004
    out = ROOT / "data" / "robustness" / f"temporal_{year}_predictions.json"
    records, skipped = [], []
    for iso, name, display, ind, tier in iter_universe(year):
        r = full_diagnostic(ind, {})
        sc = r["scoring"]
        pil = sc.get("pillar_scores", {})
        p1, p4, spread = pil.get("P1"), pil.get("P4"), sc.get("pillar_spread")
        if p1 is None or p4 is None or spread is None:
            skipped.append({"iso": iso, "country": display})
            continue
        records.append({
            "iso": iso, "country": display,
            "mi_score": round(sc["mi_score"], 4) if sc.get("mi_score") is not None else None,
            "P1": round(p1, 4), "P4": round(p4, 4), "pillar_spread": round(spread, 4),
            "safeguard_J_status": (r.get("safeguards", {}).get("J", {})).get("status"),
            "predictions": predict(p1, p4, spread),
        })
    payload = {
        "workstream": "P2_temporal_holdout_GENERATE",
        "made_at_year": year, "grade_at_year": 2024,
        "label": "reduced-contamination retrodiction (historical values are 2025-anchored revisions)",
        "prereg_sha256_16": hashlib.sha256(PREREG.read_bytes()).hexdigest()[:16],
        "note": "mechanical predictions are pillar-level, independent of V1-vs-current weights",
        "n_predicted": len(records), "n_skipped": len(skipped),
        "predictions": records, "skipped": skipped,
    }
    out.write_text(json.dumps(payload, indent=2))
    traj = Counter(r["predictions"]["trajectory"] for r in records)
    vuln = Counter(r["predictions"]["vulnerability_score_0_3"] for r in records)
    print(f"{year}: predicted {len(records)} countries (skipped {len(skipped)}).")
    print(f"  trajectory: {dict(traj)}")
    print(f"  vulnerability 0-3: {dict(sorted(vuln.items()))}")
    print(f"-> {out.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
