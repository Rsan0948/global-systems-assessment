#!/usr/bin/env python3
"""
Historical program, Test 1 — the INVERSION test (deep-past anchor).

Question: on the 25 pre-modern cases, does the STRUCTURAL signal (institutions +
human capital + stability) predict rupture, and does it BEAT WEALTH (P4) — the
inverse of the modern temporal-holdout result, where wealth beat structure?
Then split by shock type: structural decay should precede ENDOGENOUS collapse but
not EXOGENOUS (conquest/invasion) collapse.

Small-n (25) and rupture-heavy (17/25) → DESCRIPTIVE, underpowered. Statistical
weight lives in the epoch panel (264 countries), not here; this is the deep anchor.

Read-only; writes its own report.
"""
import json
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[2]
CASES = ROOT / "data" / "case_studies" / "ancient" / "ancient_cases.json"
OUT = ROOT / "data" / "robustness" / "historical" / "inversion_test.json"

# MI structural pillars (exclude P4 wealth). Institutional P1 is load-bearing.
STRUCT_W = {"P1": 0.34, "P2": 0.15, "P3": 0.16, "P5": 0.16}  # renormalized below


def struct(pil):
    tot = sum(STRUCT_W.values())
    return sum(STRUCT_W[k] * pil[k] for k in STRUCT_W) / tot


def shock_class(s):
    s = (s or "").lower()
    if s == "none":
        return "none"
    if "env" in s:
        return "exo_natural"
    if s.startswith("exo") and "endo" not in s:
        return "exo_agency"   # invasion / conquest / confederation
    if "endo" in s and "exo" not in s:
        return "endo"
    return "mixed"


def auc(scores, labels):
    """AUC that HIGHER score => label 1. Mann-Whitney U."""
    pos = [s for s, l in zip(scores, labels) if l]
    neg = [s for s, l in zip(scores, labels) if not l]
    if not pos or not neg:
        return None
    wins = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return wins / (len(pos) * len(neg))


def main():
    cases = json.loads(CASES.read_text())
    rows = []
    for c in cases:
        pk, pr = c.get("peak", {}), c.get("pre_stress", {})
        pkp = {k: pk[k]["score"] if isinstance(pk.get(k), dict) else pk.get(k) for k in ("P1", "P2", "P3", "P4", "P5")}
        prp = {k: pr[k]["score"] if isinstance(pr.get(k), dict) else pr.get(k) for k in ("P1", "P2", "P3", "P4", "P5")}
        m = c["metadata"]
        rows.append({
            "name": c["name"], "dq": m.get("data_quality"), "shock": shock_class(m.get("shock")),
            "rupture": 1 if m.get("outcome") == "rupture" else 0,
            # signals: lower structure / bigger decline => more vulnerable, so we
            # negate levels so "higher score => rupture" for AUC.
            "neg_struct_pre": -struct(prp), "struct_decline": struct(pkp) - struct(prp),
            "neg_P1_pre": -prp["P1"], "P1_decline": pkp["P1"] - prp["P1"],
            "neg_wealth_pre": -prp["P4"], "wealth_decline": pkp["P4"] - prp["P4"],
        })

    labels = [r["rupture"] for r in rows]
    def A(key): return auc([r[key] for r in rows], labels)
    disc = {
        "structural_composite_level": A("neg_struct_pre"),
        "structural_composite_decline": A("struct_decline"),
        "P1_institutional_level": A("neg_P1_pre"),
        "P1_institutional_decline": A("P1_decline"),
        "wealth_P4_level": A("neg_wealth_pre"),
        "wealth_P4_decline": A("wealth_decline"),
    }
    spread = {
        "struct_level_minus_wealth_level": (disc["structural_composite_level"] - disc["wealth_P4_level"]),
        "P1_decline_minus_wealth_decline": (disc["P1_institutional_decline"] - disc["wealth_P4_decline"]),
    }

    # Endo vs exo: does structural (P1) decay precede ENDOGENOUS but not exogenous rupture?
    by_shock = {}
    for sc in ("endo", "exo_agency", "exo_natural", "mixed", "none"):
        grp = [r for r in rows if r["shock"] == sc]
        if grp:
            by_shock[sc] = {
                "n": len(grp), "rupture_rate": round(mean(r["rupture"] for r in grp), 2),
                "mean_P1_decline": round(mean(r["P1_decline"] for r in grp), 3),
                "mean_wealth_decline": round(mean(r["wealth_decline"] for r in grp), 3),
            }

    report = {
        "test": "inversion_deep_anchor", "n": len(rows), "n_rupture": sum(labels),
        "caveat": "n=25, rupture-heavy; DESCRIPTIVE. Statistical weight is in the epoch panel.",
        "rupture_discrimination_AUC": {k: (round(v, 3) if v is not None else None) for k, v in disc.items()},
        "structure_minus_wealth_spread": {k: round(v, 3) for k, v in spread.items()},
        "by_shock_type": by_shock,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2))

    print(f"n={len(rows)} ({sum(labels)} rupture)\n")
    print("Rupture discrimination (AUC, higher=better; 0.5=chance):")
    for k, v in disc.items():
        print(f"  {k:32s} {v:.3f}" if v is not None else f"  {k:32s} n/a")
    print("\nStructure-minus-wealth spread (>0 => structure beats wealth):")
    for k, v in spread.items():
        print(f"  {k:36s} {v:+.3f}")
    print("\nBy shock type (structural decay should precede ENDO, not EXO-agency):")
    for sc, d in by_shock.items():
        print(f"  {sc:12s} n={d['n']} rupture={d['rupture_rate']}  P1_decline={d['mean_P1_decline']}  wealth_decline={d['mean_wealth_decline']}")
    print(f"\n-> {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
