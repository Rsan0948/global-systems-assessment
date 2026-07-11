#!/usr/bin/env python3
"""
Priority 0 — Prospective freeze (see docs/ROBUSTNESS_PREREGISTRATION.md).

Emits mechanical 2024->2034 predictions for every scored country, using ONLY the
frozen rule set. No case-by-case judgment. This is the only genuinely
uncontaminated test in the program: it is committed now and graded in ~2034
against the frozen outcome definitions (relative GDP-pc-PPP growth; UCDP conflict
onset OR Bank-of-Canada-CRAG sovereign default).

Read-only w.r.t. the engine: imports the scoring engine, writes nothing but its
own predictions file.

    python scripts/robustness/prospective_freeze.py
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # mi-research/
sys.path.insert(0, str(ROOT))

from mi.panel import iter_universe          # noqa: E402
from mi.diagnostics import full_diagnostic  # noqa: E402

YEAR = 2024
HORIZON = 2034
PREREG = ROOT / "docs" / "ROBUSTNESS_PREREGISTRATION.md"
OUT = ROOT / "data" / "robustness" / "prospective_2024_predictions.json"

# --- FROZEN mechanical rule set (reuses the engine's own Safeguard-J thresholds) ---
J_FLAG_FLOOR = 0.28      # gap >= this: economy outruns institutions -> stress
J_CLEAR_CEILING = 0.20   # gap <= this: institutions keep pace -> sustain/improve
SPREAD_HIGH = 0.25
SPREAD_LOW = 0.15
P1_DECLINE = 0.30
P1_IMPROVE = 0.50


def predict(p1, p4, spread):
    """Apply the frozen rules. Returns a dict of mechanical predictions."""
    gap = p4 - p1  # == Safeguard J's gap
    if gap >= J_FLAG_FLOOR:
        trajectory = "stress"
    elif gap <= J_CLEAR_CEILING:
        trajectory = "sustain_or_improve"
    else:
        trajectory = "monitor"

    if spread > SPREAD_HIGH:
        volatility = "high"
    elif spread < SPREAD_LOW:
        volatility = "low"
    else:
        volatility = "moderate"

    if p1 < P1_DECLINE:
        level = "decline_risk"
    elif p1 > P1_IMPROVE:
        level = "improvement_capacity"
    else:
        level = "hold"

    durability = "durable_balanced" if spread < SPREAD_LOW else "unbalanced"

    # Crisis-vulnerability, graded 0-3 = count of conditions met (for AUC-ROC).
    # The frozen binary (>=1 condition) is retained but is deliberately loose;
    # grading uses the graded score with a threshold sweep + baseline lift.
    conditions = [p1 < P1_DECLINE, gap >= J_FLAG_FLOOR, spread > SPREAD_HIGH]
    vuln_score = sum(conditions)

    return {
        "p4_minus_p1_gap": round(gap, 4),
        "trajectory": trajectory,
        "volatility": volatility,
        "level": level,
        "durability": durability,
        "vulnerability_score_0_3": vuln_score,
        "elevated_crisis_vulnerability": vuln_score >= 1,  # frozen binary (loose)
    }


def main():
    records = []
    skipped = []
    for iso, name, display, ind, tier in iter_universe(YEAR):
        r = full_diagnostic(ind, {})
        sc = r["scoring"]
        pil = sc.get("pillar_scores", {})
        p1, p4, spread = pil.get("P1"), pil.get("P4"), sc.get("pillar_spread")
        if p1 is None or p4 is None or spread is None:
            skipped.append({"iso": iso, "country": display,
                            "reason": "insufficient pillars", "data_gaps": sc.get("data_gaps")})
            continue
        j = r.get("safeguards", {}).get("J", {})
        records.append({
            "iso": iso,
            "country": display,
            "mi_score": round(sc["mi_score"], 4) if sc.get("mi_score") is not None else None,
            "tier": (sc.get("tier") or {}).get("tier"),
            "P1": round(p1, 4),
            "P4": round(p4, 4),
            "pillar_spread": round(spread, 4),
            "safeguard_J_status": j.get("status"),
            "predictions": predict(p1, p4, spread),
        })

    prereg_hash = hashlib.sha256(PREREG.read_bytes()).hexdigest()[:16]
    payload = {
        "workstream": "P0_prospective_freeze",
        "made_at_year": YEAR,
        "grade_at_year": HORIZON,
        "prereg_sha256_16": prereg_hash,
        "rule_set": {
            "J_flag_floor": J_FLAG_FLOOR, "J_clear_ceiling": J_CLEAR_CEILING,
            "spread_high": SPREAD_HIGH, "spread_low": SPREAD_LOW,
            "p1_decline": P1_DECLINE, "p1_improve": P1_IMPROVE,
        },
        "outcome_definitions": {
            "relative_growth": "GDP-pc-PPP change 2024->2034, above/below cross-country median",
            "crisis_binary": "UCDP conflict onset OR BoC-CRAG sovereign default in 2024-2034",
            "components_reported_separately": ["ucdp_conflict_onset", "crag_sovereign_default"],
        },
        "n_predicted": len(records),
        "n_skipped": len(skipped),
        "predictions": records,
        "skipped": skipped,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))

    # console summary
    from collections import Counter
    traj = Counter(r["predictions"]["trajectory"] for r in records)
    elev = sum(r["predictions"]["elevated_crisis_vulnerability"] for r in records)
    print(f"Predicted {len(records)} countries (skipped {len(skipped)} for insufficient pillars).")
    print(f"Trajectory: {dict(traj)}")
    print(f"Elevated crisis-vulnerability: {elev}/{len(records)}")
    print(f"prereg hash: {prereg_hash}")
    print(f"-> {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
