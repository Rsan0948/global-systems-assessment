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
        indicators = entity_data.get("indicators", {})
        context = entity_data.get("context", {})

        score = score_country(indicators)
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


def validate_baseline(completed_dir: str):
    """Validate all completed case studies against the baseline."""
    completed_path = Path(completed_dir)
    if not completed_path.exists():
        print(f"Directory not found: {completed_dir}")
        return

    total = {"confirmed": 0, "partial": 0, "falsified": 0}
    cases_processed = 0

    for case_file in sorted(completed_path.glob("*.json")):
        with open(case_file) as f:
            case_data = json.load(f)

        case_name = case_data.get("metadata", {}).get("case_name", case_file.stem)
        verification = case_data.get("verification", {})

        for pred_name, result in verification.items():
            coding = result.get("result", "").upper()
            if "CONFIRMED" in coding and "PARTIAL" not in coding:
                total["confirmed"] += 1
            elif "PARTIAL" in coding:
                total["partial"] += 1
            elif "FALSIF" in coding:
                total["falsified"] += 1

        cases_processed += 1

    if cases_processed > 0:
        total_scored = total["confirmed"] + total["partial"] + total["falsified"]
        print(f"\nBASELINE VALIDATION — {cases_processed} cases")
        print(f"  Total predictions: {total_scored}")
        print(f"  Confirmed: {total['confirmed']}")
        print(f"  Partial: {total['partial']}")
        print(f"  Falsified: {total['falsified']}")
        if total_scored > 0:
            print(f"  Clean rate (per-letter count): {total['confirmed']/total_scored:.0%}")
            print(f"  Directional: {(total['confirmed']+total['partial'])/total_scored:.0%}")
            print("\n  HONESTY NOTE — report as a RANGE, not a single number.")
            print("  The records carry the run6 STRICT re-code (post-hoc 'primary dimension'")
            print("  d-calls -> PARTIAL; narrow-gap a-trajectory annotated with Mod4), so this")
            print("  per-letter clean rate now lands at the canonical best estimate (~78%).")
            print("  The HONEST figure is a RANGE: ~62% (strict) - 85% (generous), best ~78%;")
            print("  directional ~100% (zero falsifications, partly by construction). It remains")
            print("  partly redundant with WGI standalone. See")
            print("  live/runs/run6of6_definitive_synthesis_20cases.md and completed/README.md.")


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

    case_name = case_data.get("metadata", {}).get("case_name", "Unknown")
    print(f"\nMI RETRODICTION PROTOCOL — {case_name}")
    print(f"Timestamp: {datetime.now().isoformat()}")

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
