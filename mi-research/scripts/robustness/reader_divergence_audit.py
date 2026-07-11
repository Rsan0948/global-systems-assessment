#!/usr/bin/env python3
"""Phase B audit — do the two engine data readers agree?

Compares mi/datasource.py's live multi-source stitch (wb_anchored + pipeline CSVs,
used by durability/relational) against mi/panel.py's canonical_panel.json (the main
scoring path) for every overlapping country-year-indicator. Establishes whether
re-pointing datasource at the canonical panel is a pure refactor (agree on values) or
a behavior change (differ). See DATA_FLOW_MAP.md §1, §8 item 5.

Finding (committed): 6685 values compared, ZERO divergences — they agree on values;
they differ only in SCOPE (datasource serves ~91 curated countries, canonical 191), so
unification would expand durability's reference set and change the corpus. Deferred.

    python scripts/robustness/reader_divergence_audit.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from mi import datasource as ds   # noqa: E402
from mi import panel             # noqa: E402

YEARS = [1996, 2004, 2012, 2018, 2024]
TOL = 1e-6


def main():
    compared = missing_ds = missing_panel = 0
    diffs = []
    for iso, name, display, ind_panel, tier in panel.iter_universe(2024):
        for y in YEARS:
            pind = panel.indicators_for(iso, y) or {}
            try:
                dind = ds.get_indicators(display, y) or {}
            except Exception:
                dind = {}
            if not pind and not dind:
                continue
            if not dind:
                missing_ds += 1
                continue
            if not pind:
                missing_panel += 1
                continue
            for k in set(pind) & set(dind):
                a, b = pind[k], dind[k]
                if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                    compared += 1
                    if abs(a - b) > TOL:
                        diffs.append((display, y, k, a, b))
    print(f"numeric values compared      : {compared}")
    print(f"datasource had no data (panel did): {missing_ds}  (the scope gap)")
    print(f"panel had no data (datasource did): {missing_panel}")
    print(f"divergences (>|{TOL}|)         : {len(diffs)}")
    for d in diffs[:30]:
        print("  DIFF", d)
    if not diffs:
        print("VERDICT: readers AGREE on all overlapping values. Unification is safe on VALUES "
              "but changes SCOPE (durability reference set) -> corpus behavior change, deferred.")


if __name__ == "__main__":
    main()
