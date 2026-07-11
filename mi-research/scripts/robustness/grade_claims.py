#!/usr/bin/env python3
"""
Priority 1 (GRADE half) — run AFTER derive_claim.py is committed/frozen.

Compares the spec-driven derived claims (data/robustness/derived_claims.json,
frozen at the prior commit) against the frozen verification{} codings and the
actual outcomes baked into each case. Two questions, kept separate:

  (A) REPRODUCTION: does the spec-driven derivation reconstruct the frozen
      prediction? (The core Priority-1 question: is the missing derivation
      faithfully recomputable, i.e. is the "100%" reproducible from the engine?)
  (B) RECOMPUTED CRISIS ACCURACY: for the durability (sig, actual_acute_crisis)
      and rule (rv, actual_outcome_crisis) families — clean outcome booleans —
      does the derived directional call match reality, and does it beat the base
      rate?

Ordinality independent accuracy (pre-P1 ordering vs post-outcome ordering) needs
post_event re-scoring and is a documented follow-up; here we grade ordinality
REPRODUCTION only (derived ranking vs the frozen stated ordering).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DERIVED = ROOT / "data" / "robustness" / "derived_claims.json"
CASEDIR = ROOT / "data" / "case_studies" / "completed"
OUT = ROOT / "data" / "robustness" / "grade_report.json"


def _case_path(rec):
    """Locate the source case JSON via the record's source_file (case_id is a
    display name for sig/rv cases, so globbing by it fails)."""
    sf = rec.get("source_file")
    if sf:
        p = CASEDIR / sf
        if p.exists():
            return p
    hits = list(CASEDIR.glob(f"{rec.get('case_id','')}*.json"))
    return hits[0] if hits else None


def _parse_frozen_ordering(expl):
    """Pull the 'A > B > C' ordering the frozen coding claims (by pre-P1)."""
    if not expl:
        return None
    # e.g. "full ordering matches: Estonia > Russia > Ukraine (by pre-P1) == ..."
    m = re.search(r"ordering[^:]*:\s*([A-Za-z .'\-]+(?:>[A-Za-z .'\-]+)+)", expl)
    if not m:
        return None
    return [t.strip() for t in m.group(1).split(">")]


def grade():
    derived = json.loads(DERIVED.read_text())
    cases = derived["cases"] if isinstance(derived, dict) and "cases" in derived else derived

    fam = {"ordinality": [], "durability": [], "rule": []}
    for rec in cases:
        cid = rec.get("case_id", "")
        schema = rec.get("schema")
        if schema in ("comparative", "comparative_degraded_single"):
            fam["ordinality"].append(rec)
        elif schema == "durability_gate":
            fam["durability"].append(rec)
        elif schema == "rule_validation":
            fam["rule"].append(rec)

    report = {"reproduction": {}, "recomputed_crisis_accuracy": {}, "divergences": []}

    # ---- (A) Ordinality: classify how each frozen coding was ACTUALLY derived. ----
    # The 51-case "100%" is heterogeneous: some codings were mechanically auto-
    # derived (a definite ordering), some auto-derived but ABSTAINED (Mod4 margin
    # gate), some had auto-derivation skipped with human judgment preserved, and
    # some are free-text narrative. Only the "auto ordering" subset is a clean
    # mechanical reproduction target; the rest are not a single recomputable number.
    basis = {"auto_ordering": 0, "auto_abstain_mod4": 0,
             "judgment_preserved": 0, "narrative_or_other": 0}
    for rec in fam["ordinality"]:
        cp = _case_path(rec)
        if not cp:
            basis["narrative_or_other"] += 1
            continue
        expl = (json.loads(cp.read_text()).get("verification", {})
                .get("a_trajectory", {}) or {}).get("explanation", "") or ""
        if "AUTO (Mod4)" in expl and "abstain" in expl:
            basis["auto_abstain_mod4"] += 1
        elif "AUTO:" in expl and "ordering" in expl:
            basis["auto_ordering"] += 1
        elif any(m in expl for m in ("data-limited", "auto-derivation skipped",
                                     "judgment preserved")):
            basis["judgment_preserved"] += 1
        else:
            basis["narrative_or_other"] += 1
    report["ordinality_derivation_basis"] = {
        "note": ("Of 51 P1-ordinality cases, how the frozen coding was derived. "
                 "Only 'auto_ordering' is a clean mechanical reproduction target; "
                 "'auto_abstain_mod4' are mechanical NON-calls counted as confirmed; "
                 "'judgment_preserved'/'narrative' rest on human judgment, not a "
                 "recomputable rule."),
        "counts": basis, "total": sum(basis.values())}

    # ---- (A)+(B) durability + rule: reconstruct original call, grade both ----
    for family, actual_key in (("durability", "actual_acute_crisis"),
                               ("rule", "actual_outcome_crisis")):
        n = repro = 0
        correct = abstain = 0
        crises = 0
        confusion = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
        details = []
        for rec in fam[family]:
            if not rec.get("derivable"):
                continue
            cp = _case_path(rec)
            if not cp:
                continue
            case = json.loads(cp.read_text())
            actual = bool(case.get(actual_key))
            vkey = "j_durability_gate" if family == "durability" else "rule_test"
            frozen = case.get("verification", {}).get(vkey, {})
            frozen_result = frozen.get("result")
            call = rec["summary"]["directional_call"]  # crisis_vulnerable/absorber/watch
            pred = (True if call == "crisis_vulnerable"
                    else False if call == "absorber" else None)  # None = abstain
            n += 1
            crises += int(actual)

            # (A) reproduction: reconstruct the original call from (result, actual)
            if frozen_result == "CONFIRMED":
                orig = actual                      # original call was correct
            elif frozen_result == "FALSIFIED":
                orig = not actual                  # original call was wrong
            else:
                orig = None                        # INDETERMINATE/borderline
            orig_call = (True if orig is True else False if orig is False else None)
            reproduced = (pred == orig_call)
            repro += int(reproduced)

            # (B) recomputed accuracy vs actual outcome
            if pred is None:
                abstain += 1
            else:
                if pred and actual:
                    confusion["tp"] += 1; correct += 1
                elif pred and not actual:
                    confusion["fp"] += 1
                elif (not pred) and actual:
                    confusion["fn"] += 1
                else:
                    confusion["tn"] += 1; correct += 1
            details.append({"case": rec["case_id"], "derived_call": call,
                            "predict_crisis": pred, "actual_crisis": actual,
                            "frozen_result": frozen_result, "reproduced": reproduced})
            if not reproduced:
                report["divergences"].append(
                    {"case": rec["case_id"], "claim": vkey, "derived_call": call,
                     "predict": pred, "actual": actual, "frozen_result": frozen_result})

        graded = n - abstain
        base_rate = crises / n if n else None
        # base-rate baseline = always predict the majority class
        base_acc = max(base_rate, 1 - base_rate) if base_rate is not None else None
        acc = correct / graded if graded else None
        report["reproduction"][family] = {"n": n, "reproduced": repro,
                                           "rate": round(repro / n, 4) if n else None}
        report["recomputed_crisis_accuracy"][family] = {
            "n": n, "abstained": abstain, "graded": graded,
            "accuracy": round(acc, 4) if acc is not None else None,
            "base_rate_crisis": round(base_rate, 4) if base_rate is not None else None,
            "majority_baseline_acc": round(base_acc, 4) if base_acc is not None else None,
            "lift_over_baseline": round(acc - base_acc, 4) if (acc is not None and base_acc is not None) else None,
            "confusion": confusion, "details": details}

    OUT.write_text(json.dumps(report, indent=2))

    # console
    r = report["reproduction"]
    b = report["ordinality_derivation_basis"]["counts"]
    print("=== ORDINALITY (51): how the frozen '100%' coding was actually derived ===")
    print(f"  auto_ordering (clean mechanical) : {b['auto_ordering']}")
    print(f"  auto_abstain_mod4 (non-call)     : {b['auto_abstain_mod4']}")
    print(f"  judgment_preserved (human)       : {b['judgment_preserved']}")
    print(f"  narrative_or_other               : {b['narrative_or_other']}")
    print("\n=== (A) REPRODUCTION of the frozen call (durability/rule, recomputable) ===")
    for f in ("durability", "rule"):
        print(f"  {f:11s}: {r[f]['reproduced']}/{r[f]['n']} ({r[f]['rate']})")
    print("\n=== (B) RECOMPUTED CRISIS ACCURACY (derived call vs actual outcome) ===")
    for f in ("durability", "rule"):
        a = report["recomputed_crisis_accuracy"][f]
        print(f"  {f:11s}: acc={a['accuracy']} on {a['graded']} graded "
              f"(abstain {a['abstained']}); base-rate={a['base_rate_crisis']} "
              f"majority={a['majority_baseline_acc']} LIFT={a['lift_over_baseline']}; {a['confusion']}")
    print(f"\n  divergences logged: {len(report['divergences'])}")
    print(f"-> {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    grade()
