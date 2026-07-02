#!/usr/bin/env python3
"""
Experiment: P1 composite vs. decomposed (capacity vs. accountability).

Hypothesis (from docs/expansion_plan/case_revisions...md, "The Rwanda
Architectural Decision"): Rwanda's high government-effectiveness / corruption-
control alongside low voice may break a single-composite P1. Test whether
decomposing P1 into
    P1a (capacity)        = mean(Government Effectiveness, Regulatory Quality)
    P1b (accountability)  = mean(Rule of Law, Voice & Accountability, Control of Corruption)
predicts Rwanda (and the Batch-1 set) better than the current single composite
    P1 (current)          = mean(Gov Effectiveness, Rule of Law, Regulatory Quality, Control of Corruption)
NOTE: the *current* composite already EXCLUDES Voice & Accountability. The only
new information decomposition introduces is injecting VA into P1b.

Deterministic; reads only committed country files. Run from mi-research/:
    python sandbox/experiments/rwanda_p1_decomposition/run_experiment.py
"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from mi.scoring import score_country, calculate_pillar_scores  # noqa: E402

MARGIN = 0.10  # Mod4 default margin of error on the 0-1 P1 scale


def decomposed(ind):
    g = lambda k: ind.get(k)
    cap = [g("gov_effectiveness"), g("regulatory_quality")]
    acc = [g("rule_of_law"), g("voice_accountability"), g("control_of_corruption")]
    cap = [x / 100 for x in cap if x is not None]
    acc = [x / 100 for x in acc if x is not None]
    p1a = sum(cap) / len(cap) if cap else None
    p1b = sum(acc) / len(acc) if acc else None
    return p1a, p1b


def main():
    cases = {
        "Rwanda": ["1996", "2023"], "DR Congo": ["1996", "2023"],
        "Venezuela": ["1998", "2023"], "Colombia": ["2012", "2023"],
        "Haiti": ["1996", "2023"], "Dominican Republic": ["1996", "2023"],
    }
    print(f"{'entity/year':28}{'P1_comp':>9}{'P1a_cap':>9}{'P1b_acc':>9}{'cap-acc':>9}  within Mod4 margin?")
    for c, yrs in cases.items():
        data = json.loads((ROOT / "data" / "countries" / (c.lower().replace(" ", "_") + ".json")).read_text())
        for y in yrs:
            ind = data["indicators_by_year"][y]
            p1 = calculate_pillar_scores(ind)["P1"]
            a, b = decomposed(ind)
            gap = a - b
            print(f"{c+' '+y:28}{p1:>9.3f}{a:>9.3f}{b:>9.3f}{gap:>9.3f}  {'YES (abstain)' if abs(gap) < MARGIN else 'no'}")

    print("\nOrdinal-stability / Golden-Rule check (2023): does splitting P1 (0.34 -> 0.17+0.17) change the Rwanda>DRC ordinal?")
    w2 = {"P1a": 0.17, "P1b": 0.17, "P2": 0.15, "P3": 0.16, "P4": 0.20, "P5": 0.16}
    for c in ["Rwanda", "DR Congo"]:
        data = json.loads((ROOT / "data" / "countries" / (c.lower().replace(" ", "_") + ".json")).read_text())
        ind = data["indicators_by_year"]["2023"]
        mi_comp = score_country(ind)["mi_score"]
        ps = calculate_pillar_scores(ind)
        a, b = decomposed(ind)
        d = {"P1a": a, "P1b": b, "P2": ps["P2"], "P3": ps["P3"], "P4": ps["P4"], "P5": ps["P5"]}
        avail = {k: v for k, v in d.items() if v is not None}
        tw = sum(w2[k] for k in avail)
        mi_dec = sum(avail[k] * w2[k] for k in avail) / tw
        print(f"  {c:10} MI_composite={mi_comp:.3f}  MI_decomposed={mi_dec:.3f}")
    print("\nVerdict: see results.md")


if __name__ == "__main__":
    main()
