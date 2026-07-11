"""
Synthetic data for Study 2C.

TWO DISTINCT GENERATORS, with different jobs. Neither is evidence about real
rivers; both exist so the pipeline and the statistics can be exercised and
validated before real HydroSHEDS data is available.

1. `random_coalescent_basin` — builds a REAL tree topology (random binary
   sequential-merging / Yule model) so that the Strahler/Horton code in
   `horton.py` runs on genuine network structure. This model is parameter-free
   and emergent; empirically it produces Rb ~ 3.0 (verified in the tests).
   That is *useful for honesty*: it is a neutral topology with no e built in,
   and it lands near 3 (NOT at e, and NOT at the ~4 that Shreve's random-
   topology model and real rivers give), so it demonstrates the pipeline does
   not spuriously manufacture e. It is a pipeline exerciser, not a calibrated
   model of real drainage networks.

2. `sample_basin_rbs` — directly samples per-basin Rb values from a population
   whose TRUE center we choose (`center`). This is the generator used by the
   power/calibration analysis: we ask whether the model-comparison procedure
   can recover a known center and distinguish a true-e world from a true-3
   world. It makes no topological claim; the per-basin Rb is the unit of
   analysis exactly as in the real study.
"""

from __future__ import annotations

import numpy as np


def random_coalescent_basin(n_sources: int, rng: np.random.Generator) -> dict[int, int]:
    """Random binary merging tree with `n_sources` leaves.

    Repeatedly join two active subtree-roots into a new parent until one root
    remains (the outlet). Returns a {node -> downstream} dict, outlet -> -1.
    """
    if n_sources < 2:
        raise ValueError("need at least 2 sources")
    downstream: dict[int, int] = {}
    active = list(range(n_sources))          # leaf ids 0..n_sources-1
    next_id = n_sources
    while len(active) > 1:
        i, j = rng.choice(len(active), size=2, replace=False)
        a, b = active[i], active[j]
        parent = next_id
        next_id += 1
        downstream[a] = parent
        downstream[b] = parent
        # remove a and b, add parent
        active = [x for k, x in enumerate(active) if k not in (i, j)]
        active.append(parent)
    downstream[active[0]] = -1               # outlet
    return downstream


def coalescent_rb_population(
    n_basins: int,
    size_range: tuple[int, int] = (50, 800),
    min_orders: int = 3,
    seed: int = 0,
) -> np.ndarray:
    """Measure Rb across many random-coalescent basins. Returns array of Rb."""
    from horton import measure_basin

    rng = np.random.default_rng(seed)
    out: list[float] = []
    while len(out) < n_basins:
        n_src = int(rng.integers(size_range[0], size_range[1]))
        basin = random_coalescent_basin(n_src, rng)
        try:
            out.append(measure_basin(basin, min_orders=min_orders).rb)
        except ValueError:
            continue
    return np.asarray(out)


def sample_basin_rbs(
    n_basins: int,
    center: float,
    log_sd: float = 0.18,
    seed: int = 0,
) -> np.ndarray:
    """Per-basin Rb drawn from a lognormal whose median is `center`.

    `log_sd` is the standard deviation on the log scale; 0.18 gives a realistic
    spread (most basins within roughly +/-20% of the center), matching the
    basin-to-basin variability seen in empirical Horton-ratio compilations.
    The TRUE center is `center` by construction — this is the ground truth the
    power analysis tries to recover.
    """
    rng = np.random.default_rng(seed)
    return center * np.exp(rng.normal(0.0, log_sd, size=n_basins))
