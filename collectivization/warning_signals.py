"""
Warning signals: the fragmentation pressure index.

Three time-series indicators that may precede the NEXT fragmentation of a
collectivized entity. All computed from existing datasets (Maddison GDP,
V-Dem liberal democracy).

For cases where the cycle repeated (Germany: Empire -> WWI), checks whether
the warning signals fired before the next fragmentation.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class WarningSignal:
    name: str
    fired: bool
    year_fired: int | None
    detail: str


@dataclass
class WarningResult:
    case_name: str
    efficiency_decay: WarningSignal
    integration_reversal: WarningSignal
    legitimacy_erosion: WarningSignal
    any_fired: bool
    all_fired: bool


def _rolling_growth(series: dict[int, float], window: int = 10) -> dict[int, float]:
    """Compute rolling annualized growth rate over a window."""
    years = sorted(series.keys())
    result = {}
    for i, y in enumerate(years):
        start_year = y - window
        candidates = [(yr, v) for yr, v in series.items()
                      if start_year <= yr < y]
        if len(candidates) < 2:
            continue
        yr0, v0 = candidates[0]
        yr1, v1 = candidates[-1]
        span = yr1 - yr0
        if span > 0 and v0 > 0 and v1 > 0:
            result[y] = (v1 / v0) ** (1.0 / span) - 1.0
    return result


def check_efficiency_decay(
    gdp_series: dict[int, float],
    post_collect_year: int,
    baseline_window: int = 30,
    decay_threshold_years: int = 10,
) -> WarningSignal:
    """Flag when rolling GDP growth drops below the first-generation
    post-collectivization growth rate for 10+ consecutive years."""
    rolling = _rolling_growth(gdp_series, window=10)
    if not rolling:
        return WarningSignal("efficiency_decay", False, None, "insufficient GDP data")

    baseline_years = [y for y in rolling
                      if post_collect_year < y <= post_collect_year + baseline_window]
    if not baseline_years:
        return WarningSignal("efficiency_decay", False, None,
                             "no GDP data in baseline window")
    baseline_rate = np.mean([rolling[y] for y in baseline_years])

    consecutive_below = 0
    for y in sorted(rolling.keys()):
        if y <= post_collect_year + baseline_window:
            continue
        if rolling[y] < baseline_rate:
            consecutive_below += 1
            if consecutive_below >= decay_threshold_years:
                fire_year = y - decay_threshold_years + 1
                return WarningSignal(
                    "efficiency_decay", True, fire_year,
                    f"growth below baseline {baseline_rate:.3f} for {decay_threshold_years}+ "
                    f"years starting ~{fire_year}")
        else:
            consecutive_below = 0

    return WarningSignal("efficiency_decay", False, None,
                         f"growth never dropped below baseline {baseline_rate:.3f} "
                         f"for {decay_threshold_years}+ consecutive years")


def check_integration_reversal(
    features_post: list[int],
    features_later: list[int] | None,
) -> WarningSignal:
    """Count features that flipped back to pre-collectivization values.
    Requires a re-scored feature vector at a later date."""
    if features_later is None:
        return WarningSignal("integration_reversal", False, None,
                             "no later feature vector available")

    reversals = sum(features_post[i] != features_later[i]
                    for i in range(len(features_post)))
    if reversals >= 2:
        return WarningSignal("integration_reversal", True, None,
                             f"{reversals} features reversed from post-collectivization state")
    return WarningSignal("integration_reversal", False, None,
                         f"only {reversals} feature(s) reversed")


def check_legitimacy_erosion(
    vdem_series: dict[int, float],
    post_collect_year: int,
    decline_window: int = 20,
    threshold: float = -0.05,
) -> WarningSignal:
    """Flag sustained decline in V-Dem liberal democracy index.
    Looks for a drop > threshold over any decline_window-year span
    after the post-collectivization year."""
    years = sorted(y for y in vdem_series if y > post_collect_year)
    if len(years) < decline_window:
        return WarningSignal("legitimacy_erosion", False, None,
                             "insufficient V-Dem data after collectivization")

    for i, y0 in enumerate(years):
        y1 = y0 + decline_window
        if y1 not in vdem_series:
            continue
        delta = vdem_series[y1] - vdem_series[y0]
        if delta < threshold:
            return WarningSignal(
                "legitimacy_erosion", True, y0,
                f"V-Dem dropped {delta:.3f} over {y0}-{y1}")

    return WarningSignal("legitimacy_erosion", False, None,
                         f"no sustained V-Dem decline > {threshold} "
                         f"over any {decline_window}-year window")


def analyze_case(
    case_name: str,
    gdp_series: dict[int, float],
    vdem_series: dict[int, float],
    features_post: list[int],
    post_collect_year: int,
    features_later: list[int] | None = None,
) -> WarningResult:
    """Run all three warning signal checks for a single case."""
    eff = check_efficiency_decay(gdp_series, post_collect_year)
    integ = check_integration_reversal(features_post, features_later)
    legit = check_legitimacy_erosion(vdem_series, post_collect_year)

    return WarningResult(
        case_name=case_name,
        efficiency_decay=eff,
        integration_reversal=integ,
        legitimacy_erosion=legit,
        any_fired=eff.fired or integ.fired or legit.fired,
        all_fired=eff.fired and integ.fired and legit.fired,
    )
