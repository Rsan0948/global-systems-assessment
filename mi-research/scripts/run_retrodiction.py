#!/usr/bin/env python3
"""
Run the MI retrodiction protocol on a case study.

The protocol enforces strict phase separation:
  Phase 1: Score pre-event data
  Phase 2: Generate predictions (BEFORE examining outcomes)
  Phase 3: Verify against post-event data

Usage:
    python scripts/run_retrodiction.py --case data/case_studies/in_progress/my_case.json
    python scripts/run_retrodiction.py --case data/case_studies/in_progress/my_case.json --phase 1
    python scripts/run_retrodiction.py --validate data/case_studies/completed/
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from mi.scoring import score_country, calculate_pillar_spread, get_configuration_profile
from mi.safeguards import evaluate_all_safeguards
from mi.diagnostics import classify_strategy, assess_vulnerability, generate_predictions


def run_phase1(case_data: dict) -> dict:
    """Phase 1: Score pre-event data for all entities."""
    print("\n" + "=" * 60)
    print("PHASE 1 — PRE-EVENT SCORING")
    print("=" * 60)

    pre_event = case_data.get("pre_event", {})
    results = {}

    for entity_name, entity_data in pre_event.get("entities", {}).items():
        # Reference-based records resolve indicators via the Data API (country_ref +
        # pre_year). Legacy records that embed "indicators" still work.
        indicators = entity_data.get("indicators")
        if not indicators and entity_data.get("country_ref"):
            from mi import datasource
            indicators = datasource.get_indicators(
                entity_data["country_ref"], entity_data.get("pre_year")) or {}
        context = entity_data.get("context", {})

        score = score_country(indicators or {})
        safeguards = evaluate_all_safeguards(score, context)
        strategy = classify_strategy(score, context)
        vulnerability = assess_vulnerability(score, safeguards)

        results[entity_name] = {
            "scoring": score,
            "safeguards": safeguards,
            "strategy": strategy,
            "vulnerability": vulnerability,
        }

        pillars = score["pillar_scores"]
        print(f"\n--- {entity_name} ---")
        print(f"  MI Score: {score.get('mi_score', 'N/A')}")
        for p in ["P1", "P2", "P3", "P4", "P5"]:
            v = pillars.get(p)
            print(f"  {p}: {v:.3f}" if v else f"  {p}: N/A")
        print(f"  Spread: {score.get('pillar_spread', 'N/A')}")
        print(f"  Strategy: {strategy.get('strategy', 'unknown')}")
        print(f"  Risk: {vulnerability.get('risk_level', 'unknown')}")

        triggered = [name for name, sg in safeguards.items()
                     if sg.get("triggered") and name not in ("Mod8",)]
        if triggered:
            print(f"  Safeguards: {', '.join(triggered)}")

    return results


def run_phase2(case_data: dict, phase1_results: dict) -> dict:
    """Phase 2: Generate predictions from pre-event data ONLY."""
    print("\n" + "=" * 60)
    print("PHASE 2 — PREDICTIONS")
    print("(Generated BEFORE examining post-event data)")
    print("=" * 60)

    # Generate comparison-based predictions if multiple entities
    comparison_scores = {name: result["scoring"]
                        for name, result in phase1_results.items()}

    predictions = {}
    if len(comparison_scores) >= 2:
        # Use first entity's score as reference
        first_score = list(phase1_results.values())[0]["scoring"]
        first_safeguards = list(phase1_results.values())[0]["safeguards"]
        predictions = generate_predictions(first_score, first_safeguards, comparison_scores)
    elif len(comparison_scores) == 1:
        score = list(phase1_results.values())[0]["scoring"]
        safeguards = list(phase1_results.values())[0]["safeguards"]
        predictions = generate_predictions(score, safeguards)

    for pred_name, pred in predictions.items():
        print(f"\n  [{pred_name}]")
        for key, val in pred.items():
            if isinstance(val, list):
                print(f"    {key}: {', '.join(str(v) for v in val)}")
            else:
                print(f"    {key}: {val}")

    print("\n  *** STOP HERE IF RUNNING BLIND ***")
    print("  *** Record predictions before examining post-event data ***")

    return predictions


def run_phase3(case_data: dict) -> dict:
    """Phase 3: Verify predictions against post-event data."""
    print("\n" + "=" * 60)
    print("PHASE 3 — VERIFICATION")
    print("=" * 60)

    verification = case_data.get("verification", {})
    scorecard = {"confirmed": 0, "partial": 0, "falsified": 0, "na": 0}

    for pred_name, result in verification.items():
        coding = result.get("result", "").upper()
        if "CONFIRMED" in coding and "PARTIAL" not in coding:
            scorecard["confirmed"] += 1
        elif "PARTIAL" in coding:
            scorecard["partial"] += 1
        elif "FALSIF" in coding:
            scorecard["falsified"] += 1
        else:
            scorecard["na"] += 1

        print(f"\n  [{pred_name}] {coding}")
        if result.get("evidence"):
            print(f"    Evidence: {result['evidence'][:100]}")
        if result.get("explanation"):
            print(f"    Analysis: {result['explanation'][:100]}")

    total_scored = scorecard["confirmed"] + scorecard["partial"] + scorecard["falsified"]
    if total_scored > 0:
        clean_rate = scorecard["confirmed"] / total_scored
        directional = (scorecard["confirmed"] + scorecard["partial"]) / total_scored
        print(f"\n  Scorecard: {scorecard['confirmed']}C / {scorecard['partial']}P / {scorecard['falsified']}F")
        print(f"  Clean rate: {clean_rate:.0%} | Directional: {directional:.0%}")

    return scorecard


def _check_track3_confidence(case_data: dict):
    """Print a confidence warning for Track 3 (ancient proxy) cases."""
    if case_data.get("track") != 3:
        return
    low_count = 0
    total_count = 0
    for tp_key in ("peak", "pre_stress"):
        tp = case_data.get(tp_key, {})
        for p in ("P1", "P2", "P3", "P4", "P5"):
            indicators = tp.get(p, {}).get("indicators", {})
            for ind in indicators.values():
                total_count += 1
                if ind.get("confidence") == "LOW":
                    low_count += 1
    if total_count > 0 and low_count > 0:
        pct = 100 * low_count / total_count
        rob = case_data.get("robustness", {})
        claims = rob.get("total_defensible_claims", "?")
        max_claims = rob.get("max_possible_claims", "?")
        print(f"\n  ⚠  TRACK 3 CONFIDENCE NOTE")
        print(f"     {low_count}/{total_count} indicators ({pct:.0f}%) are LOW confidence")
        print(f"     {claims}/{max_claims} pillar-level claims survive uncertainty")
        print(f"     Pillar-level comparisons are more defensible than composite MI ranking")


def validate_baseline(completed_dir: str):
    """Validate all completed case studies against the baseline."""
    completed_path = Path(completed_dir)
    if not completed_path.exists():
        print(f"Directory not found: {completed_dir}")
        return

    # Two classes in the 70-case corpus: P1-ORDINALITY cases (51) and DURABILITY-GATE / Safeguard-J
    # test cases (19, stress_type="durability_gate_test"). Scored separately — different claims.
    cls = {"ordinality": {"confirmed": 0, "partial": 0, "falsified": 0, "n": 0},
           "durability_gate": {"confirmed": 0, "partial": 0, "falsified": 0, "n": 0},
           "rule_validation": {"confirmed": 0, "partial": 0, "falsified": 0, "n": 0}}
    cases_processed = 0

    for case_file in sorted(completed_path.glob("*.json")):
        with open(case_file) as f:
            case_data = json.load(f)
        st = case_data.get("metadata", {}).get("stress_type")
        k = ("durability_gate" if st == "durability_gate_test"
             else "rule_validation" if st == "rule_validation"
             else "ordinality")
        cls[k]["n"] += 1
        for pred_name, result in case_data.get("verification", {}).items():
            coding = result.get("result", "").upper()
            if "CONFIRMED" in coding and "PARTIAL" not in coding:
                cls[k]["confirmed"] += 1
            elif "PARTIAL" in coding or "INDETERMIN" in coding:
                cls[k]["partial"] += 1
            elif "FALSIF" in coding:
                cls[k]["falsified"] += 1
        cases_processed += 1

    total = cls["ordinality"]  # back-compat: the headline scorecard is the ordinality baseline
    if cases_processed > 0:
        o = cls["ordinality"]; g = cls["durability_gate"]; rv = cls["rule_validation"]
        total_scored = o["confirmed"] + o["partial"] + o["falsified"]
        print(f"\nCORPUS: {cases_processed} cases = {o['n']} P1-ordinality + {g['n']} durability-gate "
              f"+ {rv['n']} rule-validation (A/B)")
        print(f"\nP1-ORDINALITY BASELINE — {o['n']} cases")
        print(f"  Total predictions: {total_scored}")
        print(f"  Confirmed: {o['confirmed']}")
        print(f"  Partial: {o['partial']}")
        print(f"  Falsified: {o['falsified']}")
        gscored = g["confirmed"] + g["partial"] + g["falsified"]
        if gscored:
            print(f"\nDURABILITY-GATE (Safeguard J) TEST SET — {g['n']} cases: "
                  f"{g['confirmed']} correct / {g['falsified']} wrong "
                  f"({g['confirmed']/gscored*100:.0f}% accuracy)")
        rvs = rv["confirmed"] + rv["partial"] + rv["falsified"]
        if rvs:
            print(f"\nRULE-VALIDATION (A/B) TEST SET — {rv['n']} cases: "
                  f"{rv['confirmed']} confirmed / {rv['partial']} indeterminate / {rv['falsified']} falsified")
        if total_scored > 0:
            print(f"  Clean rate (per-letter count): {total['confirmed']/total_scored:.0%}")
            print(f"  Directional: {(total['confirmed']+total['partial'])/total_scored:.0%}")
            print("\n  HONESTY NOTE — report as a RANGE, not a single number.")
            print("  Records are MI v1, scored on real data via the Data API. a_trajectory &")
            print("  c_convergence are AUTO-DERIVED from the re-scored data (Mod4-gated); the")
            print("  run6 strict re-code (post-hoc d-calls -> PARTIAL) is also applied. The")
            print("  per-letter clean rate now ~74% (real-data auto-derivation moved 5 verdicts")
            print("  off the prior ~78% — all CONFIRMED->PARTIAL, e.g. Mod4 near-ties).")
            print("  HONEST figure is a RANGE: ~62-85%, and directional ~100% (zero")
            print("  falsifications, partly by construction; capacity partly redundant w/ WGI).")
            print("  See live/runs/run6of6_definitive_synthesis_20cases.md & completed/README.md.")


def main():
    parser = argparse.ArgumentParser(description="Run MI retrodiction protocol")
    parser.add_argument("--case", type=str, help="Path to case study JSON")
    parser.add_argument("--phase", type=int, choices=[1, 2, 3],
                        help="Run specific phase only (default: all)")
    parser.add_argument("--validate", type=str,
                        help="Validate all completed cases in directory")

    args = parser.parse_args()

    if args.validate:
        validate_baseline(args.validate)
        return

    if not args.case:
        print("Provide --case <path> or --validate <dir>")
        sys.exit(1)

    with open(args.case) as f:
        case_data = json.load(f)

    case_name = case_data.get("metadata", {}).get("case_name", case_data.get("name", "Unknown"))
    print(f"\nMI RETRODICTION PROTOCOL — {case_name}")
    print(f"Timestamp: {datetime.now().isoformat()}")

    _check_track3_confidence(case_data)

    if args.phase is None or args.phase == 1:
        phase1_results = run_phase1(case_data)

    if args.phase is None or args.phase == 2:
        if "phase1_results" not in dir():
            phase1_results = run_phase1(case_data)
        run_phase2(case_data, phase1_results)

    if args.phase is None or args.phase == 3:
        run_phase3(case_data)


if __name__ == "__main__":
    main()
