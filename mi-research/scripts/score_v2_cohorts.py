#!/usr/bin/env python3
"""
Score the v2 shock-cohort out-of-sample set (data/case_studies/source_reports/
VALIDATION_v2_shock_cohort_modern.md) against the pre-registered rule.

PROTOCOL (matches the v1 standard): blind SELECTION (framework-naive agent), MECHANICAL predictor
(V-Dem rule-of-law at the pre-shock year, the P1 proxy r=0.87 with WGI P1), PRE-REGISTERED rule
(higher pre-shock institutions -> better outcome). Outcomes are the agent's neutral tags (1 collapse,
2 violent rupture, 3 peaceful discontinuity, 4 stressed-continuous, 5 absorbed). Reading outcomes to
score is acceptable because selection+predictor are blind/mechanical (same caveat as the v1 run).

Scored WITHIN-COHORT (shock held ~constant — the clean test) and POOLED, split by origin.
Firewalled from the 213/77/0 baseline. Deterministic.

NOTE: this set tests the INTERNAL engine only. Every drawn 'external' cohort is a natural-disaster or
price shock (tsunami, Ebola, oil) — there is NO external-military/conquest shock, so the T3 relational
tier is NOT exercised by v2 (see docs/validation_run_v2_cohorts.md).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VDEM = ROOT / "data" / "sources" / "vdem_longrun.json"

# 27 observations transcribed from VALIDATION_v2_shock_cohort_modern.md.
# (iso3, pre_shock_year ~2-3yr pre-onset, cohort, origin, outcome_tag)
OBS = [
    ("CHL", 1927, "A_GreatDep", "internal", 3), ("PER", 1927, "A_GreatDep", "internal", 2),
    ("BOL", 1927, "A_GreatDep", "internal", 2), ("SLV", 1927, "A_GreatDep", "internal", 2),
    ("CRI", 1979, "B_Debt82", "internal", 4), ("PHL", 1979, "B_Debt82", "internal", 3),
    ("DOM", 1979, "B_Debt82", "internal", 4), ("JAM", 1979, "B_Debt82", "internal", 4),
    ("CIV", 1991, "C_CFA94", "internal", 2), ("CMR", 1991, "C_CFA94", "internal", 4),
    ("BEN", 1991, "C_CFA94", "internal", 3), ("MLI", 1991, "C_CFA94", "internal", 4),
    ("ARG", 1992, "D_Tequila", "external", 4),
    ("AGO", 2011, "E_Oil", "external", 4), ("AZE", 2011, "E_Oil", "external", 4),
    ("KAZ", 2011, "E_Oil", "external", 4), ("COG", 2011, "E_Oil", "external", 4),
    ("GAB", 2011, "E_Oil", "external", 4), ("GNQ", 2011, "E_Oil", "external", 4),
    ("MDV", 2001, "F_Tsunami", "external", 4), ("LKA", 2001, "F_Tsunami", "external", 4),
    ("SOM", 2001, "F_Tsunami", "external", 4), ("SYC", 2001, "F_Tsunami", "external", 5),
    ("SLE", 2011, "G_Ebola", "external", 4), ("LBR", 2011, "G_Ebola", "external", 4),
    ("GIN", 2011, "G_Ebola", "external", 4), ("SEN", 2011, "G_Ebola", "external", 5),
]


def _rol(vd, code, yr):
    b = vd.get(code, {}).get("rol", {})
    le = [int(y) for y in b if int(y) <= yr]
    return round(b[str(max(le))], 3) if le else None


def _pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs); syy = sum((y - my) ** 2 for y in ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return sxy / ((sxx * syy) ** 0.5) if sxx and syy else None


def _rank(v):
    s = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[s[j + 1]] == v[s[i]]:
            j += 1
        avg = sum(range(i, j + 1)) / (j - i + 1)
        for k in range(i, j + 1):
            r[s[k]] = avg
        i = j + 1
    return r


def _spearman(xs, ys):
    return _pearson(_rank(xs), _rank(ys)) if len(xs) >= 3 else None


def main():
    vd = json.load(open(VDEM))
    rows = [(iso, yr, co, org, _rol(vd, iso, yr), tag) for iso, yr, co, org, tag in OBS]

    def block(rs, label):
        rol = [r[4] for r in rs]; tag = [r[5] for r in rs]
        p, sp = _pearson(rol, tag), _spearman(rol, tag)
        print(f"{label:22} n={len(rs):2}  Pearson={p:+.2f}  Spearman={sp:+.2f}" if p is not None
              else f"{label:22} n={len(rs)} (too few)")

    print("PRE-REGISTERED: higher pre-shock rol -> better outcome (higher tag). Expect POSITIVE.\n" + "=" * 70)
    block(rows, "POOLED (all 27)")
    block([r for r in rows if r[3] == "internal"], "  internal-origin")
    block([r for r in rows if r[3] == "external"], "  external-origin")
    print("-" * 70 + "\nWITHIN-COHORT (the clean test; Spearman where outcomes vary):")
    from collections import defaultdict
    co = defaultdict(list)
    for r in rows:
        co[r[2]].append(r)
    for c, rs in sorted(co.items()):
        tags = sorted(r[5] for r in rs)
        if len(rs) >= 3 and len(set(tags)) > 1:
            print(f"  {c:12} n={len(rs)} rho={_spearman([r[4] for r in rs], [r[5] for r in rs]):+.2f}  outcomes={tags}")
        else:
            print(f"  {c:12} n={len(rs)} -> degenerate (no/low variance: {tags})")
    print("\nREAD: within-cohort 4/5 variance-cohorts concordant (~+0.77); pooled ~null (+0.09) — "
          "entrenched low-institution autocracies absorb ECONOMIC shocks (oil cohort), which rol "
          "doesn't capture. Internal engine only; T3 not exercised (no military shock drawn).")


if __name__ == "__main__":
    main()
