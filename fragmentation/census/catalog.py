"""
The fragmentation census — per-system analysis.

The project's question was restructured (2026-06-27) away from "is there a
UNIVERSAL subdivision constant?" (the data rejected it: no shared value, no
mechanism) toward a CENSUS:

    "Which natural systems have a CONSISTENT fragmentation point -- a
     characteristic branching/splitting factor that is concentrated AND beats
     its own mechanism-free null -- and what is each one's number?"

There is no pooling, no shared-constant test, no ladder. Each system stands on
its own. A system earns "lawful fragmentation point" iff:

  * CONCENTRATED  : within-system coefficient of variation < 0.30
                    (it HAS a characteristic value, not just scatter), AND
  * BEATS NULL    : its characteristic value is significantly displaced from its
                    mechanism-free (random-topology / size-only) null
                    (two-sided bootstrap p < 0.05) -- i.e. the value is not just
                    free combinatorics.

Systems that are concentrated but do NOT beat their null (e.g. corporate splits)
are reported as "candidate -- trivial"; systems that beat the null but are not
concentrated as "candidate -- dispersed". Honest, symmetric reporting.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np

CV_CONCENTRATED = 0.30
ALPHA = 0.05


@dataclass
class SystemEntry:
    name: str
    kind: str                 # "natural" | "contrast" (non-natural / boundary)
    n: int
    factor: float             # geometric-mean fragmentation factor
    ci_low: float
    ci_high: float
    cv: float
    null_factor: float        # geometric-mean of the mechanism-free null
    direction: str            # "above" | "below" | "at" the null
    beats_null_p: float
    concentrated: bool
    beats_null: bool
    lawful: bool
    verdict: str
    source: str


def assess_system(name: str, ratios, null_sampler, kind: str = "natural",
                  source: str = "", n_sims: int = 4000, seed: int = 0) -> SystemEntry:
    r = np.asarray(ratios, dtype=float)
    r = r[r > 0]
    n = r.size
    logr = np.log(r)
    mean_log = float(logr.mean())
    factor = float(np.exp(mean_log))
    se_log = float(logr.std(ddof=1) / np.sqrt(n)) if n > 1 else float("nan")
    ci_low = float(np.exp(mean_log - 1.96 * se_log))
    ci_high = float(np.exp(mean_log + 1.96 * se_log))
    cv = float(r.std(ddof=1) / r.mean()) if n > 1 else float("nan")

    rng = np.random.default_rng(seed)
    null_geoms = np.array([
        float(np.exp(np.log(np.clip(null_sampler(n, rng), 1e-9, None)).mean()))
        for _ in range(n_sims)])
    null_factor = float(null_geoms.mean())
    p_above = float((null_geoms >= factor).mean())
    p_below = float((null_geoms <= factor).mean())
    p = float(2.0 * min(p_above, p_below))
    p = min(p, 1.0)

    concentrated = bool(cv < CV_CONCENTRATED)
    beats_null = bool(p < ALPHA)
    lawful = bool(concentrated and beats_null)
    direction = ("above" if factor > null_factor * 1.02
                 else "below" if factor < null_factor * 0.98 else "at")

    if lawful:
        verdict = f"LAWFUL fragmentation point ~{factor:.2f} ({direction} null)"
    elif concentrated and not beats_null:
        verdict = f"candidate -- trivial (concentrated ~{factor:.2f} but = its null)"
    elif beats_null and not concentrated:
        verdict = f"candidate -- dispersed (beats null but CV={cv:.2f} too high)"
    else:
        verdict = f"not lawful (CV={cv:.2f}, indistinguishable from null)"

    return SystemEntry(
        name=name, kind=kind, n=int(n), factor=round(factor, 3),
        ci_low=round(ci_low, 3), ci_high=round(ci_high, 3), cv=round(cv, 3),
        null_factor=round(null_factor, 3), direction=direction,
        beats_null_p=round(p, 4), concentrated=concentrated, beats_null=beats_null,
        lawful=lawful, verdict=verdict, source=source)


def to_dict(e: SystemEntry) -> dict:
    return asdict(e)
