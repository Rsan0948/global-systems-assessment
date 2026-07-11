"""
Read V-Dem long-run liberal democracy index from the existing
vdem_longrun.json (mi-research/data/sources/).

No network calls -- reads from the repo's committed data.
"""

from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
VDEM = os.path.join(HERE, "../../../mi-research/data/sources/vdem_longrun.json")


def load_vdem_series(iso3: str, metric: str = "libdem") -> dict[int, float]:
    """Load V-Dem time series for a country.
    metric: 'libdem' (liberal democracy) or 'rol' (rule of law).
    Returns {year: score}."""
    if not os.path.exists(VDEM):
        return {}
    with open(VDEM) as f:
        data = json.load(f)
    entry = data.get(iso3, {})
    series = entry.get(metric, {})
    return {int(y): float(v) for y, v in series.items() if v is not None}


def vdem_subseries(iso3: str, start: int, end: int,
                   metric: str = "libdem") -> dict[int, float]:
    """Extract a V-Dem subseries for a time range."""
    series = load_vdem_series(iso3, metric)
    return {y: v for y, v in series.items() if start <= y <= end}


def multi_country_vdem(iso3s: list[str], start: int, end: int,
                       metric: str = "libdem") -> dict[int, float]:
    """Average V-Dem scores across multiple countries per year."""
    all_series = {}
    for iso in iso3s:
        for y, v in load_vdem_series(iso, metric).items():
            if start <= y <= end:
                all_series.setdefault(y, []).append(v)
    return {y: sum(vs) / len(vs) for y, vs in sorted(all_series.items())}
