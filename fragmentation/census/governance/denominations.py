"""
The in-between case: RELIGIOUS DENOMINATIONS (porosity vs suppression).

DATA TIER — CURATED (documented, flagged; global denomination counts are
contested and the cleanest source, the World Christian Database, is paywalled;
Wikipedia's tree is buried in navigation noise). So this is a transparently-
sourced table of major Christian traditions with their approximate body counts
and their GOVERNANCE TYPE on the central<->congregational (suppression<->porosity)
axis.

Why religion is the sharp test (MASTER_REFERENCE 1.3): schism is *permitted*
(porous) but doctrine is *engineered* (suppressive), so the theory doesn't
cleanly predict where it lands -- UNTIL you split by governance type:
  - CENTRAL authority (Catholic, Orthodox) suppresses schism -> very few bodies,
    but rare splits are massive (1054, 1517).
  - CONGREGATIONAL / porous (Baptist, Pentecostal) vent continuously -> hundreds
    to thousands of bodies (continuous micro-fragmentation).
Prediction: porosity score predicts denomination count; the cross-tradition
spread is enormous (the designed/imposed dispersion signature).
"""

from __future__ import annotations

import numpy as np

# (tradition, approx_bodies, porosity 0=central..1=congregational, note)
TRADITIONS = [
    ("Roman Catholic",        1,   0.00, "single central magisterium (+Eastern Catholic in communion)"),
    ("Eastern Orthodox",     14,   0.15, "~14 autocephalous churches; conciliar"),
    ("Oriental Orthodox",     6,   0.15, "~6 churches; conciliar"),
    ("Anglican",             42,   0.45, "~42 provinces in communion"),
    ("Lutheran",            150,   0.55, "~150+ bodies; episcopal/synodal"),
    ("Methodist",            80,   0.55, "~80+ bodies"),
    ("Reformed/Presbyterian",250, 0.70, "~250+ bodies; presbyterian polity"),
    ("Restorationist",      100,   0.75, "~100+ bodies"),
    ("Baptist",             240,   0.85, "~240+ bodies; congregational autonomy"),
    ("Pentecostal",         700,   0.95, "~700+ bodies; highly congregational"),
]


def analyze() -> dict:
    bodies = np.array([t[1] for t in TRADITIONS], dtype=float)
    poros = np.array([t[2] for t in TRADITIONS], dtype=float)
    lb = np.log(bodies)

    def spearman(a, b):
        ra = np.argsort(np.argsort(a)).astype(float); rb = np.argsort(np.argsort(b)).astype(float)
        ra -= ra.mean(); rb -= rb.mean()
        return float((ra @ rb) / (np.sqrt(ra @ ra) * np.sqrt(rb @ rb)))

    cv = float(bodies.std(ddof=1) / bodies.mean())
    central = bodies[poros <= 0.2]
    congreg = bodies[poros >= 0.7]
    return {
        "system": "religious_denominations",
        "data_tier": "CURATED (documented; global counts contested, WCD paywalled)",
        "n_traditions": len(TRADITIONS),
        "body_count_range": [int(bodies.min()), int(bodies.max())],
        "body_count_CV": round(cv, 2),
        "spearman_porosity_vs_log_bodies": round(spearman(poros, lb), 3),
        "central_authority_mean_bodies": round(float(central.mean()), 1),
        "congregational_mean_bodies": round(float(congreg.mean()), 1),
        "verdict": "porosity strongly predicts fragmentation: central-authority "
                   "traditions (Catholic/Orthodox) stay near-unitary and fracture "
                   "rarely-but-massively (suppression); congregational/porous ones "
                   "(Baptist/Pentecostal) fragment continuously into hundreds. "
                   "Cross-tradition spread is huge -> religion is NOT a single tight "
                   "band; it splits ALONG the porosity<->suppression axis (MASTER 1.3).",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(analyze(), indent=2))
