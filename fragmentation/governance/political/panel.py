"""
Synthetic country-period panel for calibrating the DGS -> instability test.

A tunable TRUE DGS effect (`beta_dgs_true`) lets us verify the test (a) detects
a real effect through the GDP/population/region/decade controls, and (b) is
null when there is no effect. This is the calibration that no real data is
needed for; ingest() swaps in COW/V-Dem/WGI/Atlas.

The confounding is built in deliberately: GDP per capita lowers instability and
correlates with the interface (institutional) proxy, so a naive test could
mistake the confound for a DGS effect. The controls must absorb it.
"""

from __future__ import annotations

import numpy as np


def make_panel(n_countries: int = 170, n_periods: int = 6,
               beta_dgs_true: float = 0.6, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    N = n_countries * n_periods

    region = rng.integers(0, 6, size=N)
    decade = rng.integers(0, n_periods, size=N)
    log_gdppc = rng.normal(8.5, 1.1, size=N)              # ~ ln GDP per capita
    log_pop = rng.normal(16.0, 1.5, size=N)

    # interior (econ complexity) and interface (institutions); institutions rise
    # with GDP -> confound. DGS = interior - interface (both standardized).
    interior = rng.normal(0, 1, size=N)
    interface = 0.5 * (log_gdppc - 8.5) / 1.1 + rng.normal(0, 0.8, size=N)
    dgs = _z(interior) - _z(interface)

    # true data-generating process for instability
    eta = (-2.2
           + beta_dgs_true * dgs
           - 0.55 * (log_gdppc - 8.5)          # richer -> less instability (confound)
           + 0.12 * (log_pop - 16.0)
           + 0.15 * (region == 3)              # one region slightly higher
           )
    p = 1.0 / (1.0 + np.exp(-eta))
    instability = (rng.random(N) < p).astype(int)

    return {
        "dgs": dgs, "log_gdppc": log_gdppc, "log_pop": log_pop,
        "region": region, "decade": decade, "period": decade,
        "instability": instability,
    }


def _z(x: np.ndarray) -> np.ndarray:
    return (x - x.mean()) / x.std()
