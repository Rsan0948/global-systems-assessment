#!/usr/bin/env python3
"""
Historical program, Test 2 — the DECAY CURVE (epoch panel).

For each epoch anchor year, score every available polity on a STRUCTURE signal
(V-Dem rule-of-law, the institutional core) and a WEALTH signal (Maddison GDP),
then measure how well each discriminates a subsequent RUPTURE outcome. The
reported quantity is the STRUCTURE-minus-WEALTH AUC spread per epoch — internal to
each period, so shared data-quality noise cancels. Hypothesis: the spread is
structure-positive deep in the past and erodes toward the present (wealth-positive)
as a mobile capital order decouples prosperity from institutions.

Outcome is pluggable. v1 = economic rupture (severe GDP collapse in the window),
the one outcome available across all epochs from committed data. NOTE: pre-1900
Maddison GDP is heavily interpolated, so economic-rupture may be undercounted early
— the per-epoch rupture rate is printed so unusable epochs are visible; conflict
onset (UCDP 1946+, COW 1816+) is the complementary outcome to add for the middle band.

Read-only; writes its own report.
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VDEM = ROOT / "data" / "sources" / "vdem_longrun.json"
LONGRUN = ROOT / "data" / "sources" / "longrun_pillars.json"
OUT = ROOT / "data" / "robustness" / "historical" / "decay_curve.json"

ANCHORS = [1800, 1850, 1900, 1950, 1980]
WINDOW = 30            # outcome window (years after the anchor)
COLLAPSE = 0.80        # rupture = trough/level < this (a >20% GDP collapse)


def _series(v):
    return json.loads(v) if isinstance(v, str) else v


def auc(scores, labels):
    pos = [s for s, l in zip(scores, labels) if l]
    neg = [s for s, l in zip(scores, labels) if not l]
    if not pos or not neg:
        return None
    wins = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return wins / (len(pos) * len(neg))


def main():
    vdem = json.loads(VDEM.read_text())
    longrun = json.loads(LONGRUN.read_text())
    rol = {iso: _series(v["rol"]) for iso, v in vdem.items() if "rol" in v}
    gdp = {iso: {int(y): val for y, val in _series(v["P4_gdp"]).items()}
           for iso, v in longrun.items() if "P4_gdp" in v}

    epochs = []
    for y in ANCHORS:
        rows = []
        for iso in set(rol) & set(gdp):
            r = rol[iso].get(str(y))
            g0 = gdp[iso].get(y)
            if r is None or g0 is None or g0 <= 0:
                continue
            window_g = [gdp[iso][yy] for yy in range(y, y + WINDOW + 1) if yy in gdp[iso]]
            if len(window_g) < WINDOW // 2:      # need enough of the window covered
                continue
            trough = min(window_g)
            rupture = 1 if trough / g0 < COLLAPSE else 0
            rows.append({
                "iso": iso,
                "neg_struct": -float(r),          # low rule-of-law => rupture
                "neg_wealth": -math.log(g0),      # low GDP => rupture
                "rupture": rupture,
            })
        labels = [x["rupture"] for x in rows]
        s_auc = auc([x["neg_struct"] for x in rows], labels)
        w_auc = auc([x["neg_wealth"] for x in rows], labels)
        epochs.append({
            "year": y, "n": len(rows), "n_rupture": sum(labels),
            "rupture_rate": round(sum(labels) / len(rows), 3) if rows else None,
            "structure_auc": round(s_auc, 3) if s_auc is not None else None,
            "wealth_auc": round(w_auc, 3) if w_auc is not None else None,
            "spread_struct_minus_wealth": (round(s_auc - w_auc, 3)
                                           if (s_auc is not None and w_auc is not None) else None),
        })

    report = {
        "test": "decay_curve_epoch_panel",
        "outcome": f"economic rupture = GDP trough/level < {COLLAPSE} within {WINDOW}y",
        "structure_signal": "V-Dem rule-of-law (institutional core)",
        "wealth_signal": "log Maddison GDP-per-capita",
        "caveat": "pre-1900 Maddison GDP is interpolated -> economic-rupture likely undercounted; "
                  "watch rupture_rate; add conflict-onset (UCDP/COW) for the middle band.",
        "epochs": epochs,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2))

    print(f"outcome: GDP collapse <{COLLAPSE} within {WINDOW}y\n")
    print(f"{'year':6s} {'n':>4s} {'rupt%':>6s} {'struct_AUC':>11s} {'wealth_AUC':>11s} {'SPREAD':>8s}")
    for e in epochs:
        print(f"{e['year']:6d} {e['n']:4d} {str(e['rupture_rate']):>6s} "
              f"{str(e['structure_auc']):>11s} {str(e['wealth_auc']):>11s} "
              f"{('%+.3f' % e['spread_struct_minus_wealth']) if e['spread_struct_minus_wealth'] is not None else 'n/a':>8s}")
    print(f"\n-> {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
