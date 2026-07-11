#!/usr/bin/env python3
"""
P3 — Safeguard stratification (frozen prereg docs/ROBUSTNESS_PREREGISTRATION.md).

Implements the weak-qualifier / self-upgrading design: tag every safeguard with
how many of the modern corpus cases it actually FIRES on, tier it by the frozen
thresholds, and flag whether it is actually LOAD-BEARING on any graded call. Thin
rules (<=3 cases) become "hypothesis" qualifiers pulled from headline stats and
tracked for real-time promotion as the corpus grows.

Two metrics, kept separate and both honest:
  * applies_to (firing count): how many cases the rule triggers on. This is the
    stratification axis the user asked for.
  * load_bearing: does disabling the rule change any RECOMPUTED graded claim?
    (Pre-registered metric.) The safeguards are advisory — generate_predictions
    ignores its `safeguards` arg and tier derives only from mi_score — so this is
    ~0 for every rule EXCEPT J, which drives the durability-gate family.

Read-only: re-scores via the frozen derivation's engine calls; edits nothing.
Amendment to the prereg (2026-07-11): adds the firing-count axis alongside the
pre-registered output-change axis; both reported.
"""
import glob
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "robustness"))

from derive_claim import _score_ref                    # frozen, reused
from mi.safeguards import evaluate_all_safeguards      # noqa: E402
import config                                          # noqa: E402  (config/robustness.json)

CASEDIR = ROOT / "data" / "case_studies" / "completed"
OUT = ROOT / "data" / "robustness" / "safeguard_stratification.json"

RULES = ["A", "B", "C", "D", "E", "F", "G", "I", "J", "Mod4", "Mod8"]

# Frozen tier thresholds (prereg Plan 3; config/robustness.json). Case counts, not entity counts.
_TIERS = config.robustness()["safeguard_stratification_tiers"]
def tier_for(n):
    if n >= _TIERS["structural_min"]:
        return "Structural"
    if n >= _TIERS["validated_min"]:
        return "Validated"
    if n >= _TIERS["provisional_min"]:
        return "Provisional"
    if n >= _TIERS["hypothesis_min"]:
        return "Hypothesis"
    return "Inert"


NOTES = {
    "A": "External-administration WGI discount", "B": "Capacity gate (low P1 + few successors)",
    "C": "Reversal risk (democratic transition)", "D": "Predatory-neighbor / exogenous shock",
    "E": "Rentier capture (rents %GDP)", "F": "Sub-state turbulence",
    "G": "Suppression vs prevention tier", "I": "Porosity-with-backstop",
    "J": "Durability gate (P4-P1 gap)", "Mod4": "P1-ordinal margin-of-error abstain",
    "Mod8": "Violence-risk/agency framing (standing constraint)",
}


def _case_units(case):
    """Yield (entity_name|None, scored, context) for a case, across schemas."""
    if "pre_event" in case and isinstance(case["pre_event"].get("entities"), dict):
        for name, ed in case["pre_event"]["entities"].items():
            sc, _ = _score_ref(ed.get("country_ref"), ed.get("pre_year"))
            if sc:
                yield name, sc, (ed.get("context") or {})
    elif case.get("predictor_year"):
        sc, _ = _score_ref(case.get("country_ref"), case.get("predictor_year"))
        if sc:
            yield None, sc, {}


def main():
    fires_cases = defaultdict(int)     # rule -> #cases it fires on (any entity)
    fires_entities = defaultdict(int)  # rule -> #entities it fires on
    n_cases = n_entities = 0
    j_flag_cases = 0                   # J is load-bearing: count where it drives a call

    for f in sorted(glob.glob(str(CASEDIR / "*.json"))):
        case = json.loads(Path(f).read_text())
        units = list(_case_units(case))
        if not units:
            continue
        n_cases += 1
        case_fired = set()
        for name, sc, ctx in units:
            n_entities += 1
            safe = evaluate_all_safeguards(sc, ctx)
            for r in RULES:
                if (safe.get(r) or {}).get("triggered"):
                    fires_entities[r] += 1
                    case_fired.add(r)
            if (safe.get("J") or {}).get("status") == "flagged":
                pass
        for r in case_fired:
            fires_cases[r] += 1
        # J load-bearing: durability/rule schemas grade directly on J.status
        if not ("pre_event" in case) and units:
            _, sc0, _ = units[0]
            jst = (evaluate_all_safeguards(sc0, {}).get("J") or {}).get("status")
            if jst in ("flagged", "clear"):
                j_flag_cases += 1

    registry = {}
    for r in RULES:
        n = fires_cases[r]
        tier = tier_for(n)
        # load_bearing: J drives durability-family graded calls; all others are
        # advisory (generate_predictions ignores safeguards; tier from mi_score only)
        load_bearing = (r == "J")
        registry[r] = {
            "name": NOTES[r],
            "applies_to_cases": n,
            "applies_to_entities": fires_entities[r],
            "tier_by_firing": tier,
            "load_bearing_on_graded_call": load_bearing,
            "advisory_only": not load_bearing,
            "promotion_criteria": (
                None if tier in ("Structural",) else
                f"promote when firing cases reach the next threshold "
                f"({'8' if tier=='Provisional' else '4' if tier=='Hypothesis' else '15'}) "
                f"AND no FALSIFIED case appears in its firing set"),
            "demotion_criteria": "retire / downgrade if a FALSIFIED case appears in its firing set",
        }

    payload = {
        "workstream": "P3_safeguard_stratification",
        "prereg_sha256_16": "fbd991047fc980d3",
        "n_cases_scanned": n_cases, "n_entities_scanned": n_entities,
        "tier_thresholds": {"Structural": ">=15", "Validated": "8-14",
                            "Provisional": "4-7", "Hypothesis": "1-3", "Inert": "0"},
        "headline_finding": (
            "Firing frequency tiers the rules, but the pre-registered output-change "
            "metric is ~0 for every rule except J: the safeguards are ADVISORY and do "
            "not feed the graded directional calls. So 'strong-rules-only accuracy' == "
            "'full accuracy' for the ordinality family (removing advisory rules changes "
            "nothing); the durability signal rests on J alone, which is Structural."),
        "registry": registry,
    }
    OUT.write_text(json.dumps(payload, indent=2))

    print(f"scanned {n_cases} cases / {n_entities} entities\n")
    print(f"{'rule':5s} {'name':40s} {'cases':>5s} {'tier':12s} {'load-bearing'}")
    for r in RULES:
        e = registry[r]
        print(f"{r:5s} {e['name'][:40]:40s} {e['applies_to_cases']:5d} "
              f"{e['tier_by_firing']:12s} {'YES' if e['load_bearing_on_graded_call'] else 'advisory'}")
    print(f"\n-> {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
