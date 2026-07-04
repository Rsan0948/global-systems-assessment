"""
Read Maddison GDP per capita from the existing longrun_pillars.json
(mi-research/data/sources/) and compute growth rates for specified windows.

No network calls -- reads from the repo's committed data.
"""

from __future__ import annotations

import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LONGRUN = os.path.join(HERE, "../../../mi-research/data/sources/longrun_pillars.json")


def load_gdp_series(iso3: str) -> dict[int, float]:
    """Load annual GDP per capita for a country. Returns {year: gdp_pc}."""
    if not os.path.exists(LONGRUN):
        return {}
    with open(LONGRUN) as f:
        data = json.load(f)
    entry = data.get(iso3, {})
    gdp = entry.get("P4_gdp", {})
    return {int(y): float(v) for y, v in gdp.items() if v is not None}


def avg_annual_growth(series: dict[int, float], start: int, end: int) -> float:
    """Average annualized growth rate of GDP/cap over [start, end].
    Uses the earliest and latest available data points within the window."""
    pts = [(y, v) for y, v in sorted(series.items()) if start <= y <= end and v > 0]
    if len(pts) < 2:
        return float("nan")
    y0, v0 = pts[0]
    y1, v1 = pts[-1]
    span = y1 - y0
    if span <= 0 or v0 <= 0:
        return float("nan")
    return (v1 / v0) ** (1.0 / span) - 1.0


def gdp_growth_window(iso3: str, center_year: int, window: int = 30) -> float:
    """Compute avg annual GDP growth in a 30-year window around center_year."""
    series = load_gdp_series(iso3)
    return avg_annual_growth(series, center_year, center_year + window)


def gdp_subseries(iso3: str, start: int, end: int) -> dict[int, float]:
    """Extract a GDP subseries for a time range."""
    series = load_gdp_series(iso3)
    return {y: v for y, v in series.items() if start <= y <= end}


def multi_country_growth(iso3s: list[str], center_year: int,
                         window: int = 30) -> float:
    """Average growth across multiple countries (e.g., EU members)."""
    rates = []
    for iso in iso3s:
        r = gdp_growth_window(iso, center_year, window)
        if not np.isnan(r):
            rates.append(r)
    return float(np.mean(rates)) if rates else float("nan")
