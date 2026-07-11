#!/usr/bin/env python3
"""
Cross-era conflict-onset outcome for the decay-curve panel.

Loads the merged UCDP (1946-2023) u COW (1816-2007) onset table produced by
build_conflict_onsets.py and exposes:

    onset_in_window(iso3, y0, y1) -> bool
        True iff iso3 has >=1 war/conflict ONSET year in the inclusive [y0, y1].

    onset_years(iso3) -> set[int]
        Raw onset years for a country (empty set if none / unknown iso3).

    coverage_span() -> (min_year, max_year)

Read-only. Regenerate the underlying JSON with build_conflict_onsets.py.
"""
import json
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_ONSETS_JSON = _ROOT / "data" / "robustness" / "historical" / "conflict_onsets.json"

_data = json.loads(_ONSETS_JSON.read_text())
_ONSETS = {iso: set(ys) for iso, ys in _data["onsets"].items()}
_ALL = sorted({y for ys in _ONSETS.values() for y in ys})


def onset_years(iso3: str) -> set:
    return _ONSETS.get(iso3, set())


def onset_in_window(iso3: str, y0: int, y1: int) -> bool:
    return any(y0 <= y <= y1 for y in _ONSETS.get(iso3, ()))


def coverage_span():
    return (_ALL[0], _ALL[-1]) if _ALL else (None, None)


if __name__ == "__main__":
    lo, hi = coverage_span()
    print(f"conflict onsets: {len(_ONSETS)} iso3, span {lo}-{hi}")
    for iso in ("USA", "FRA", "RWA", "COL"):
        print(f"  {iso}: {sorted(onset_years(iso))[:12]}...")
