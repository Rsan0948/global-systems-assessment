#!/usr/bin/env python3
"""
Score a country using the Modernization Index.

Usage:
    python scripts/score_country.py --country "Estonia" --year 2024
    python scripts/score_country.py --data '{"gov_effectiveness": 88.68, ...}'
    python scripts/score_country.py --file path/to/country.json --year 2024

--country resolves against the canonical panel (mi/panel.py); any country the
site covers works.
"""

import argparse
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mi.scoring import score_country, load_country_data
from mi.safeguards import evaluate_all_safeguards
from mi.diagnostics import full_diagnostic, classify_strategy


def main():
    parser = argparse.ArgumentParser(description="Score a country using the MI")
    parser.add_argument("--country", type=str, help="Country name or iso3 (resolved via the canonical panel)")
    parser.add_argument("--year", type=int, default=2024, help="Year to score (default: 2024, the site vintage)")
    parser.add_argument("--data", type=str, help="JSON string of raw indicators")
    parser.add_argument("--file", type=str, help="Path to country JSON file")
    parser.add_argument("--context", type=str, help="JSON string of context for safeguards")
    parser.add_argument("--format", choices=["full", "summary", "json"], default="summary")

    args = parser.parse_args()

    # Load indicator data
    indicators = None

    if args.data:
        indicators = json.loads(args.data)
    elif args.file:
        with open(args.file) as f:
            data = json.load(f)
        if args.year:
            indicators = data.get("indicators_by_year", {}).get(str(args.year))
        else:
            indicators = data.get("indicators", data)
    elif args.country:
        data = load_country_data(args.country, args.year)
        if data:
            indicators = data
        else:
            print(f"No data found for {args.country}" +
                  (f" at year {args.year}" if args.year else "") +
                  " in the canonical panel (mi/panel.py). Re-run "
                  "scripts/build_canonical_panel.py if a source refreshed.")
            sys.exit(1)

    if indicators is None:
        print("No indicator data provided. Use --country, --file, or --data.")
        sys.exit(1)

    # Parse context if provided
    context = json.loads(args.context) if args.context else {}

    # Run diagnostic
    result = full_diagnostic(indicators, context)

    if args.format == "json":
        print(json.dumps(result, indent=2, default=str))
        return

    # Print results
    scoring = result["scoring"]
    pillars = scoring["pillar_scores"]

    print("\n" + "=" * 60)
    print(f"MODERNIZATION INDEX DIAGNOSTIC")
    if args.country:
        print(f"Country: {args.country}" + (f" ({args.year})" if args.year else ""))
    print("=" * 60)

    # Pillar scores
    print(f"\n{'Pillar':<35} {'Score':>8}")
    print("-" * 45)
    for pillar in ["P1", "P2", "P3", "P4", "P5"]:
        val = pillars.get(pillar)
        label = {
            "P1": "Institutional Quality (34%)",
            "P2": "Innovation & Knowledge (15%)",
            "P3": "Human Capital (16%)",
            "P4": "Economic Structure (20%)",
            "P5": "Stability & Resilience (16%)",
        }[pillar]
        print(f"  {label:<33} {val:>8.3f}" if val else f"  {label:<33} {'N/A':>8}")

    print("-" * 45)
    mi = scoring.get("mi_score")
    print(f"  {'MI Score':<33} {mi:>8.3f}" if mi else f"  {'MI Score':<33} {'N/A':>8}")

    tier = scoring.get("tier")
    if tier:
        print(f"  {'Tier':<33} {tier['tier']:>3} — {tier['name']}")

    spread = scoring.get("pillar_spread")
    if spread:
        print(f"  {'Pillar Spread':<33} {spread:>8.3f}")

    # Configuration
    config = scoring.get("configuration", [])
    if config:
        config_str = " > ".join(f"{p}({v:.2f})" for p, v in config)
        print(f"\n  Configuration: {config_str}")

    # Data gaps
    gaps = scoring.get("data_gaps", [])
    if gaps:
        print(f"\n  Data gaps: {', '.join(gaps)}")

    # Strategy
    strategy = result.get("strategy", {})
    if strategy.get("strategy") != "unknown":
        print(f"\n  Strategy: {strategy.get('strategy', 'unknown').upper()}")
        if strategy.get("tier"):
            print(f"  Suppression Tier: {strategy.get('tier_label', 'N/A')}")
        print(f"  Failure Mode: {strategy.get('failure_mode', 'N/A')}")

    # Vulnerability
    vuln = result.get("vulnerability", {})
    print(f"\n  Risk Level: {vuln.get('risk_level', 'N/A').upper()}")
    for flag in vuln.get("flags", []):
        print(f"    ⚠ {flag}")

    # Safeguards
    safeguards = result.get("safeguards", {})
    triggered = [(name, sg) for name, sg in safeguards.items()
                 if sg.get("triggered") and name not in ("Mod8",)]
    if triggered:
        print(f"\n  Active Safeguards:")
        for name, sg in triggered:
            print(f"    [{name}] {sg.get('name', name)}: {sg.get('explanation', '')[:100]}")

    if args.format == "full":
        # Sensitivity analysis
        sensitivity = scoring.get("sensitivity", {})
        if sensitivity:
            print(f"\n  Sensitivity Analysis:")
            for model, val in sensitivity.items():
                print(f"    {model}: {val:.3f}" if val else f"    {model}: N/A")

        # Full safeguard details
        print(f"\n  All Safeguard Evaluations:")
        for name, sg in safeguards.items():
            status = "TRIGGERED" if sg.get("triggered") else "clear"
            print(f"    [{name}] {status}: {sg.get('explanation', '')[:120]}")

    print()


if __name__ == "__main__":
    main()
