#!/usr/bin/env python3
"""
Historical program, Test 2 (conflict variant) — the DECAY CURVE with a REAL,
cross-era conflict-ONSET outcome (UCDP 1946-2023 u COW 1816-2007).

Adapts epoch_panel.py's STRUCTURE (V-Dem rule-of-law) + WEALTH (log Maddison GDP)
signal logic UNCHANGED; only the outcome is swapped from GDP-collapse (unusable
pre-1900) to conflict-onset-in-window from conflict_outcome.onset_in_window.

For each epoch anchor the panel is the polities with BOTH rule-of-law and GDP at
the anchor year (a common set, so the structure-minus-wealth spread is internal to
each period and shared data noise cancels). We report per epoch: n, onset rate,
structure AUC (low rule-of-law => onset), wealth AUC (low GDP => onset), and the
structure-minus-wealth spread. Hypothesis (decay): structure's edge over wealth is
large deep in the past and erodes toward the present.

Read-only w.r.t. epoch_panel.py's engine; writes its own report.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conflict_outcome import onset_in_window, coverage_span  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config                               # noqa: E402  (config/robustness.json)

VDEM = ROOT / "data" / "sources" / "vdem_longrun.json"
LONGRUN = ROOT / "data" / "sources" / "longrun_pillars.json"
OUT = ROOT / "data" / "robustness" / "historical" / "decay_curve_conflict.json"

_DC = config.robustness()["historical"]["decay_curve_conflict"]
ANCHORS = _DC["anchors"]   # [1816, 1850, 1880, 1910, 1940, 1970, 1990]
WINDOW = _DC["window"]     # 25  outcome window (years after the anchor); onset in [y, y+WINDOW]


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
            onset = 1 if onset_in_window(iso, y, y + WINDOW) else 0
            rows.append({
                "iso": iso,
                "neg_struct": -float(r),          # low rule-of-law => onset
                "neg_wealth": -math.log(g0),      # low GDP => onset
                "onset": onset,
            })
        labels = [x["onset"] for x in rows]
        s_auc = auc([x["neg_struct"] for x in rows], labels)
        w_auc = auc([x["neg_wealth"] for x in rows], labels)
        epochs.append({
            "year": y, "window": [y, y + WINDOW], "n": len(rows),
            "n_onset": sum(labels),
            "onset_rate": round(sum(labels) / len(rows), 3) if rows else None,
            "structure_auc": round(s_auc, 3) if s_auc is not None else None,
            "wealth_auc": round(w_auc, 3) if w_auc is not None else None,
            "spread_struct_minus_wealth": (round(s_auc - w_auc, 3)
                                           if (s_auc is not None and w_auc is not None) else None),
        })

    # thin-epoch flags (small n, or onset rate near 0/1 -> AUC unreliable)
    for e in epochs:
        flags = []
        if e["n"] < _DC["small_n_max"]:
            flags.append("small_n")
        if e["onset_rate"] is not None and (e["onset_rate"] < _DC["degenerate_rate_low"] or e["onset_rate"] > _DC["degenerate_rate_high"]):
            flags.append("degenerate_base_rate")
        if e["structure_auc"] is None or e["wealth_auc"] is None:
            flags.append("auc_undefined")
        e["trust_flags"] = flags

    lo, hi = coverage_span()
    report = {
        "test": "decay_curve_epoch_panel_conflict_outcome",
        "outcome": f"conflict/war ONSET within [anchor, anchor+{WINDOW}]",
        "outcome_source": f"UCDP/PRIO ACD v24.1 u COW Inter+Intra war (onset span {lo}-{hi})",
        "structure_signal": "V-Dem rule-of-law (institutional core); low => onset",
        "wealth_signal": "log Maddison GDP-per-capita; low => onset",
        "panel": "polities with BOTH rule-of-law and GDP at the anchor year (common set)",
        "window_years": WINDOW,
        "hypothesis": "structure-minus-wealth spread positive & large early, eroding toward present",
        "epochs": epochs,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2))

    print(f"outcome: conflict onset within {WINDOW}y  (onset span {lo}-{hi})\n")
    hdr = f"{'year':6s} {'n':>4s} {'onset%':>7s} {'struct_AUC':>11s} {'wealth_AUC':>11s} {'SPREAD':>8s}  flags"
    print(hdr)
    for e in epochs:
        sp = e["spread_struct_minus_wealth"]
        print(f"{e['year']:6d} {e['n']:4d} {str(e['onset_rate']):>7s} "
              f"{str(e['structure_auc']):>11s} {str(e['wealth_auc']):>11s} "
              f"{('%+.3f' % sp) if sp is not None else 'n/a':>8s}  {','.join(e['trust_flags'])}")
    print(f"\n-> {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
