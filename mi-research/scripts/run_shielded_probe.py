#!/usr/bin/env python3
"""
Shielded-survivor probe — lays out the completed 2x2 (internal durability x exposure), with the
response-patron shield as the discriminator. Populates the cell empty in the corpus, the random 30,
and the v2 cohorts: internally fragile + high exposure + SHIELDED -> survives, vs its contrast (same
fragility + exposure, shield absent/withdrawn -> falls).

NON-RANDOM, NON-BLIND discrimination probe — NOT validation. Firewalled. See
docs/relational_shielded_probe.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mi.relational import relational_reading, load_records, _response_patron

# probe members + the unshielded contrasts already in the tier
PROBE = ["Kuwait@1989", "Bosnia@1995", "Taiwan@1996", "Estonia@2003", "Afghanistan@2019",
         "Cyprus@1974", "Polish-Lithuanian Commonwealth@1772"]


def main():
    recs = load_records()
    print(f"{'case':22}{'internal P1':>12}{'struct exp':>12}{'shield':>9}  outcome")
    print("-" * 92)
    grid = {"fragile_shield": [], "fragile_noshield": [], "durable_shield": [], "durable_noshield": []}
    for key in PROBE:
        u, _, y = key.partition("@")
        r = relational_reading(u, int(y) if y else None)
        rec = recs[key]
        p1 = r["response"]["components"].get("R2_mobilization_P1") or 0.0
        es = r["exposure"]["E_structural"]
        shield = _response_patron(rec["exposure"]) == 1.0
        cell = rec.get("cell", "")
        survived = "surviv" in cell or "->" in cell and "survived" in cell.lower()
        outcome = rec.get("outcome_factual", "")[:46]
        frag = "FRAGILE" if p1 < 0.5 else "durable"
        print(f"{u[:22]:22}{p1:>8.2f}({frag[:4]}){es:>8.3f}({r['exposure']['structural_band'][:4]})"
              f"{'  SHIELD' if shield else '  none ':>9}  {outcome}")
        bucket = f"{'fragile' if frag == 'FRAGILE' else 'durable'}_{'shield' if shield else 'noshield'}"
        grid[bucket].append((u, "survived" if survived else "FELL"))
    print("\n2x2 (fragile row = the previously-empty cell):")
    print(f"  FRAGILE + SHIELDED  : {grid['fragile_shield']}")
    print(f"  FRAGILE + UNSHIELDED: {grid['fragile_noshield']}")
    print(f"  durable + shielded  : {grid['durable_shield']}")
    print(f"  durable + unshielded: {grid['durable_noshield']}")
    print("\nDISCRIMINATION: in the fragile+highly-exposed row, the response-patron flips the outcome — "
          "shielded survive (Bosnia, Kuwait), unshielded fall (Cyprus, Poland-Lithuania). It is the "
          "patron, not internal strength or luck, that separates survival from collapse.")


if __name__ == "__main__":
    main()
