"""
DESIGNED governance fracture: state / union dissolutions.

DATA TIER — CURATED (the weakest tier; flagged honestly, like the org node).
Clean systematic successor data does NOT exist free: COW/ISD record state
births and deaths but NO parent->successor links, and automated co-date/co-region
clustering is too noisy to trust (it conflates WWII occupations, and coarse
regions merge unrelated births -- verified). So this is a transparently-sourced
table of the major 20th–21st century state/union dissolutions, with successor
counts from the standard historical record and suppression durations (years the
union/empire held before release). It tests the QUALITATIVE predictions, not a
precise law.

Predictions under the complexity-capacity theory (MASTER_REFERENCE §1.4–1.5):
  - DESIGNED fracture is DISPERSED: successor counts span a wide range (2..15+),
    high CV -- unlike the tight ~3 band of self-organized branching.
  - SUPPRESSION -> RELEASE: longer suppression and lower release-time capacity
    track MORE successors and MORE violence (Yugoslavia vs Czechoslovakia).
"""

from __future__ import annotations

import numpy as np

# (parent, suppression_years, successors, violent, note)  -- documented record
DISSOLUTIONS = [
    ("USSR",                69, 15, True,  "1922-1991; mostly peaceful, some conflict (Chechnya, Karabakh)"),
    ("Yugoslavia",          73,  7, True,  "1918-1991/2006; multiple wars"),
    ("Czechoslovakia",      41,  2, False, "suppressed 1948-1989; Velvet Divorce 1993, zero violence"),
    ("Austria-Hungary",     51,  8, True,  "1867-1918; dissolved in WWI"),
    ("Ottoman Empire",     100, 12, True,  "long decline; ~modern Turkey + many MENA successors, violent"),
    ("British Raj (India)",  90, 3, True,  "partition 1947 -> India, Pakistan (-> Bangladesh), violent"),
    ("Pakistan",            24,  2, True,  "1947-1971 -> Pakistan, Bangladesh; 1971 war"),
    ("United Arab Republic", 3,  2, False, "1958-1961 -> Egypt, Syria; peaceful"),
    ("Mali Federation",      1,  2, False, "1959-1960 -> Mali, Senegal; peaceful"),
    ("Gran Colombia",       12,  3, True,  "1819-1831 -> Colombia, Venezuela, Ecuador; unrest"),
    ("Ethiopia/Eritrea",    30,  2, True,  "Eritrea independence 1993 after ~30y war"),
    ("Sudan",               55,  2, True,  "South Sudan 2011 after decades of civil war"),
    ("Indonesia/Timor",     24,  2, True,  "Timor-Leste 2002 after 24y occupation"),
    ("Malaysia/Singapore",   2,  2, False, "federation 1963-1965 -> Malaysia, Singapore; peaceful"),
    ("Senegambia",           7,  2, False, "1982-1989 -> Senegal, Gambia; peaceful"),
    ("West Indies Fed.",     4, 10, False, "1958-1962 -> ~10 Caribbean states; peaceful"),
]


def analyze() -> dict:
    succ = np.array([d[2] for d in DISSOLUTIONS], dtype=float)
    supp = np.array([d[1] for d in DISSOLUTIONS], dtype=float)
    viol = np.array([1.0 if d[3] else 0.0 for d in DISSOLUTIONS])
    cv = float(succ.std(ddof=1) / succ.mean())
    # suppression -> successors and -> violence (rank correlations, small n)
    def spearman(a, b):
        ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
        ra = ra - ra.mean(); rb = rb - rb.mean()
        return float((ra @ rb) / (np.sqrt(ra @ ra) * np.sqrt(rb @ rb)))
    return {
        "data_tier": "CURATED (documented historical record; weakest tier, flagged)",
        "n_events": len(DISSOLUTIONS),
        "successor_mean": round(float(succ.mean()), 2),
        "successor_median": float(np.median(succ)),
        "successor_range": [int(succ.min()), int(succ.max())],
        "successor_CV": round(cv, 3),
        "dispersed_vs_natural": f"CV={cv:.2f} vs self-organized ~0.2 -> "
                                f"{'DISPERSED (designed-fracture signature)' if cv > 0.5 else 'not dispersed'}",
        "spearman_suppression_vs_successors": round(spearman(supp, succ), 3),
        "violent_mean_successors": round(float(succ[viol == 1].mean()), 2),
        "peaceful_mean_successors": round(float(succ[viol == 0].mean()), 2),
        "violent_mean_suppression": round(float(supp[viol == 1].mean()), 1),
        "peaceful_mean_suppression": round(float(supp[viol == 0].mean()), 1),
        "key_contrast": "Czechoslovakia (suppressed 41y, high capacity) -> 2 peaceful; "
                        "Yugoslavia (suppressed 73y, low capacity) -> 7 violent",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(analyze(), indent=2))
