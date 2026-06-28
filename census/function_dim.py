"""
#2 -- Function as a testable census dimension.

Instead of asking "is there a universal constant?" (rejected) or "does the
interior-interface dimensional GAP predict the factor?" (null), this asks:

    Does a system's FUNCTIONAL CLASS -- what the network is FOR, and the
    optimization principle that shapes it -- organize its fragmentation factor?

Each system is tagged with a function class + the optimization principle the
literature attributes to it (see WHY_FRAGMENTATION.md). We then decompose the
between-system variance in the (log) factor into BETWEEN-class and WITHIN-class
parts. If function organizes the factor, most variance is between classes
(high eta^2); if not, classes are no better than arbitrary grouping.

HONEST CAVEAT (Kirchner 1993, WHY_FRAGMENTATION.md sec.0): the bifurcation ratio
is statistically near-inevitable, so this tests a WEAK observable. A class
"explaining" the factor is only meaningful for systems that already BEAT their
null. The stronger version of this test uses scaling EXPONENTS, not the ratio --
flagged as the next step, not done here.
"""

from __future__ import annotations

import numpy as np

# system name -> (function class, optimization principle [WHY_FRAGMENTATION.md])
FUNCTION = {
    "rivers": ("energy-transport", "minimum energy dissipation / OCN (Rinaldo)"),
    "trees": ("resource-distribution", "pipe model / area-preservation (Shinozaki, Eloy)"),
    "vessels": ("mass-distribution", "Murray's law (Murray 1926)"),
    "retinal_vessels": ("mass-distribution", "Murray's law (Murray 1926)"),
    "lungs": ("mass-distribution", "branching morphogenesis (Metzger 2008)"),
    "lung_airways": ("mass-distribution", "branching morphogenesis (Metzger 2008)"),
    "leaf_venation": ("resource-distribution", "area-preservation venation (Eloy)"),
}
# every neuro_* cell type -> information-sampling
_NEURO = ("information-sampling", "wiring economy (Chklovskii, Cuntz)")


def function_of(name: str):
    if name.startswith("neuro_"):
        return _NEURO
    return FUNCTION.get(name, ("unclassified", ""))


def analyze(entries) -> dict:
    """entries: catalog SystemEntry list. Group natural systems by function class
    and decompose log-factor variance between vs within classes."""
    nat = [e for e in entries if e.kind == "natural"]
    rows = [(e.name, *function_of(e.name), float(np.log(e.factor)), e.lawful, e.factor)
            for e in nat]
    classes: dict[str, list] = {}
    for name, cls, principle, lf, lawful, factor in rows:
        classes.setdefault(cls, []).append({"system": name, "log_factor": lf,
                                             "factor": factor, "lawful": lawful,
                                             "principle": principle})

    all_lf = np.array([r[3] for r in rows])
    grand = float(all_lf.mean())
    ss_total = float(((all_lf - grand) ** 2).sum())
    ss_between = 0.0
    class_summ = {}
    for cls, members in classes.items():
        lfs = np.array([m["log_factor"] for m in members])
        ss_between += len(lfs) * (lfs.mean() - grand) ** 2
        class_summ[cls] = {
            "n_systems": len(members),
            "principle": members[0]["principle"],
            "geom_factor": round(float(np.exp(lfs.mean())), 3),
            "factor_range": [round(min(m["factor"] for m in members), 2),
                             round(max(m["factor"] for m in members), 2)],
            "n_lawful": sum(m["lawful"] for m in members),
            "systems": [m["system"] for m in members],
        }
    eta2 = float(ss_between / ss_total) if ss_total > 0 else float("nan")
    k = len(classes)
    n = len(rows)
    return {
        "n_classes": k,
        "n_systems": n,
        "eta_squared_function_explains_factor": round(eta2, 3) if np.isfinite(eta2) else None,
        "classes": class_summ,
        "interpretation": _interpret(eta2, k, n, class_summ),
        "caveat": "Ratio is near-inevitable (Kirchner 1993); only lawful systems "
                  "(those that beat their null) count. Scaling-exponent version is "
                  "the stronger, not-yet-built test.",
    }


def _interpret(eta2, k, n, class_summ):
    if k < 2 or n < 3:
        return ("under-powered: need >= 2 function classes with >= 3 systems total "
                "(add trees / vessels / lungs).")
    if not np.isfinite(eta2):
        return "degenerate variance."
    if eta2 >= 0.5:
        return (f"function organizes the factor (eta^2={eta2:.2f}: most between-system "
                f"variance is between functional classes, not within).")
    return (f"function does NOT clearly organize the factor (eta^2={eta2:.2f}: "
            f"within-class spread rivals between-class). Consistent with the ratio "
            f"being a weak observable.")
