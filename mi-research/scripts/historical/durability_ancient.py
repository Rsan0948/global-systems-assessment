#!/usr/bin/env python3
"""
Historical add-on #1 — the durability gate (Safeguard J: P4-P1 gap direction) on
the 25 pre-modern cases.

Modern J flags when P4-P1 >= 0.28 (economy outruns institutions => durability
risk). Test whether gap DIRECTION predicts pre-modern rupture more cleanly than it
did on the modern temporal holdout (where the composite signal only matched the
baseline). If pre-modern accuracy jumps >80%, the signal is stronger because there
is less exogenous (capital) noise.

Read-only; writes its own report.
"""
import json
import sys
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config                               # noqa: E402  (config/robustness.json)

CASES = ROOT / "data" / "case_studies" / "ancient" / "ancient_cases.json"
OUT = ROOT / "data" / "robustness" / "historical" / "durability_ancient.json"
J_FLOOR = config.robustness()["historical"]["durability_ancient"]["j_floor"]  # 0.28 modern Safeguard-J flag threshold


def shock_class(s):
    s = (s or "").lower()
    if s == "none":
        return "none"
    if "env" in s:
        return "exo_natural"
    if s.startswith("exo") and "endo" not in s:
        return "exo_agency"
    if "endo" in s and "exo" not in s:
        return "endo"
    return "mixed"


def auc(scores, labels):
    pos = [s for s, l in zip(scores, labels) if l]
    neg = [s for s, l in zip(scores, labels) if not l]
    if not pos or not neg:
        return None
    return sum((p > n) + 0.5 * (p == n) for p in pos for n in neg) / (len(pos) * len(neg))


def main():
    cases = json.loads(CASES.read_text())
    rows = []
    for c in cases:
        pk, pr = c["peak"], c["pre_stress"]
        def s(ph, k): return ph[k]["score"] if isinstance(ph.get(k), dict) else ph.get(k)
        gap_peak = s(pk, "P4") - s(pk, "P1")
        gap_pre = s(pr, "P4") - s(pr, "P1")
        rows.append({
            "name": c["name"], "shock": shock_class(c["metadata"].get("shock")),
            "rupture": 1 if c["metadata"].get("outcome") == "rupture" else 0,
            "gap_peak": round(gap_peak, 3), "gap_pre": round(gap_pre, 3),
            "gap_widened": round(gap_pre - gap_peak, 3),
        })

    labels = [r["rupture"] for r in rows]

    def acc(pred):  # directional accuracy
        return sum(int(p == l) for p, l in zip(pred, labels)) / len(labels)

    # Predictors:
    #  (a) direction: gap_pre > 0  (economy outruns institutions)
    #  (b) modern J threshold: gap_pre >= 0.28
    #  (c) gap widened peak->pre-stress (institutions decayed under stable economy)
    pred_dir = [1 if r["gap_pre"] > 0 else 0 for r in rows]
    pred_j = [1 if r["gap_pre"] >= J_FLOOR else 0 for r in rows]
    pred_widen = [1 if r["gap_widened"] > 0 else 0 for r in rows]

    report = {
        "test": "durability_gate_ancient", "n": len(rows), "n_rupture": sum(labels),
        "accuracy": {
            "gap_direction_pre (>0)": round(acc(pred_dir), 3),
            "modern_J_threshold (>=0.28)": round(acc(pred_j), 3),
            "gap_widened_peak_to_prestress (>0)": round(acc(pred_widen), 3),
        },
        "auc_gap_pre_for_rupture": round(auc([r["gap_pre"] for r in rows], labels), 3),
        "auc_gap_widened_for_rupture": round(auc([r["gap_widened"] for r in rows], labels), 3),
        "modern_reference": "temporal holdout composite AUC 0.69-0.73, LOST to GDP-only baseline (0.75-0.81)",
        "by_shock": {},
        "rows": rows,
    }
    for sc in ("endo", "exo_agency", "exo_natural", "mixed", "none"):
        grp = [r for r in rows if r["shock"] == sc]
        if grp:
            gl = [r["rupture"] for r in grp]
            gp = [1 if r["gap_pre"] > 0 else 0 for r in grp]
            report["by_shock"][sc] = {
                "n": len(grp),
                "gap_direction_accuracy": round(sum(int(a == b) for a, b in zip(gp, gl)) / len(grp), 3),
                "mean_gap_pre": round(mean(r["gap_pre"] for r in grp), 3),
            }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2))

    print(f"n={len(rows)} ({sum(labels)} rupture)\n")
    print("Directional accuracy (P4-P1 gap predicting rupture):")
    for k, v in report["accuracy"].items():
        print(f"  {k:38s} {v:.3f}")
    print(f"\nAUC gap_pre for rupture: {report['auc_gap_pre_for_rupture']}   "
          f"gap_widened: {report['auc_gap_widened_for_rupture']}")
    print(f"Modern reference: {report['modern_reference']}")
    print("\nBy shock (gap-direction accuracy — should be cleanest for endo):")
    for sc, d in report["by_shock"].items():
        print(f"  {sc:12s} n={d['n']} acc={d['gap_direction_accuracy']} mean_gap_pre={d['mean_gap_pre']}")
    print(f"\n-> {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
