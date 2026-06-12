"""
Domain node 2C: river networks (REAL DATA).

Observable: the Horton bifurcation ratio Rb per drainage basin, measured by
Strahler ordering of the HydroRIVERS reach topology (see horton.py). One Rb per
basin is the unit of analysis; the node's `ratios` are the real per-basin Rb
values for the discovery continent (North America), cached by
`compute_real_rb.py` from the HydroRIVERS download.

Mechanism-free null: genuine random binary merging topology
(`synthetic.random_coalescent_basin`), measured by the SAME Strahler/Horton
code and thresholded to the SAME min Strahler order as the observed data. This
is the triviality control's baseline for rivers — random topology with no
optimization law, which empirically lands near 3-4. A non-trivial rivers result
must beat this null, not merely "cluster near 3".

PRE-REGISTERED THRESHOLD (PREREGISTRATION §8): primary cut is min_orders = 4
(drops 3-point Rb regressions that systematically under-estimate Rb on tiny
basins). The full sensitivity over {3,4,5,6} is exposed by `sensitivity_table`
and is computed from the same cache.

HOLDOUT: rivers have no temporal axis, so the within-domain holdout is
geographic — discovery on North America, a sealed different continent reserved
for confirmation (see results/SEALED_HOLDOUT.md). This node loads ONLY the
discovery continent.

Real exponents for the rung-4 mechanism test (interior/interface allometry) are
NOT yet estimated, so `interior_exp`/`interface_exp` are None here (Phase 3).
"""

from __future__ import annotations

import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")

DISCOVERY_CONTINENT = "na"
PRIMARY_MIN_ORDERS = 4
_NULL_POOL_SIZE = 8000      # bootstrap pool; sampler draws with replacement
_NULL_SIZE_RANGE = (50, 800)


# ---------------------------------------------------------------- observed Rb
def _load_real_records(continent: str = DISCOVERY_CONTINENT) -> np.ndarray:
    """Load cached per-basin (rb, max_order, r2) records for a continent."""
    path = os.path.join(RESULTS, f"rb_real_{continent}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"missing {path}; run `python compute_real_rb.py --continent "
            f"{continent} --shp data/HydroRIVERS_v10_{continent}_shp/"
            f"HydroRIVERS_v10_{continent}.shp` against the HydroRIVERS download."
        )
    with open(path) as f:
        payload = json.load(f)
    return np.array(payload["records"], dtype=float)  # columns: rb, max_order, r2


def real_rb(continent: str = DISCOVERY_CONTINENT, min_orders: int = PRIMARY_MIN_ORDERS) -> np.ndarray:
    """Real per-basin Rb at the given Strahler-order cut."""
    rec = _load_real_records(continent)
    return rec[rec[:, 1] >= min_orders, 0]


def sensitivity_table(continent: str = DISCOVERY_CONTINENT) -> dict:
    """Rb central value across min_orders cuts (PREREGISTRATION §8 sensitivity)."""
    rec = _load_real_records(continent)
    out = {}
    for mo in (3, 4, 5, 6):
        rb = rec[rec[:, 1] >= mo, 0]
        out[mo] = {
            "n_basins": int(rb.size),
            "geom_mean": float(np.exp(np.log(rb).mean())),
            "median": float(np.median(rb)),
            "p5": float(np.percentile(rb, 5)),
            "p95": float(np.percentile(rb, 95)),
        }
    return out


# ------------------------------------------------------------ mechanism-free null
def _fast_coalescent_basin(n_sources: int, rng: np.random.Generator) -> dict[int, int]:
    """O(n) random binary merging tree (same distribution as
    synthetic.random_coalescent_basin, but swap-pop instead of list-rebuild so
    the 1000s-of-basins null pool is tractable). Verified to match the canonical
    generator's Rb distribution by `_verify_fast_matches_canonical`.
    """
    downstream: dict[int, int] = {}
    active = list(range(n_sources))
    next_id = n_sources
    while len(active) > 1:
        m = len(active)
        i = int(rng.integers(m))
        j = int(rng.integers(m - 1))
        if j >= i:
            j += 1
        a, b = active[i], active[j]
        parent = next_id
        next_id += 1
        downstream[a] = parent
        downstream[b] = parent
        # swap-pop both chosen indices (remove larger first to keep indices valid)
        hi, lo = (i, j) if i > j else (j, i)
        active[hi] = active[-1]; active.pop()
        active[lo] = active[-1]; active.pop()
        active.append(parent)
    downstream[active[0]] = -1
    return downstream


def _build_null_pool() -> np.ndarray:
    """Generate (and cache) a pool of random-topology (rb, max_order) records.

    Uses random binary merging (mechanism-free) measured by the same Horton
    code, so the null reflects free branching, not a hand-tuned distribution.
    Cached so the triviality control (which samples the null ~400x) is fast.
    """
    import sys
    sys.path.insert(0, HERE)
    from horton import measure_basin

    rng = np.random.default_rng(2718)
    recs = []
    while len(recs) < _NULL_POOL_SIZE:
        n_src = int(rng.integers(*_NULL_SIZE_RANGE))
        basin = _fast_coalescent_basin(n_src, rng)
        try:
            m = measure_basin(basin, min_orders=3)
        except ValueError:
            continue
        recs.append([round(float(m.rb), 6), int(m.max_order)])
    arr = np.array(recs, dtype=float)
    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "rb_null_pool.json"), "w") as f:
        json.dump({"size": _NULL_POOL_SIZE, "size_range": list(_NULL_SIZE_RANGE),
                   "fields": ["rb", "max_order"], "records": recs}, f)
    return arr


def _load_null_pool() -> np.ndarray:
    path = os.path.join(RESULTS, "rb_null_pool.json")
    if os.path.exists(path):
        with open(path) as f:
            return np.array(json.load(f)["records"], dtype=float)
    return _build_null_pool()


def make_null_sampler(min_orders: int = PRIMARY_MIN_ORDERS):
    """Return null_sampler(n, rng) -> n random-topology Rb at the same cut."""
    pool = _load_null_pool()
    rb_pool = pool[pool[:, 1] >= min_orders, 0]

    def sampler(n: int, rng: np.random.Generator) -> np.ndarray:
        return rng.choice(rb_pool, size=n, replace=True)

    return sampler


# --------------------------------------------------------------------- the node
def build_node(min_orders: int = PRIMARY_MIN_ORDERS, continent: str = DISCOVERY_CONTINENT):
    """Build the real rivers DomainNode (discovery continent only)."""
    import sys
    sys.path.insert(0, os.path.join(HERE, "..", "..", "integration"))
    from node_api import DomainNode

    ratios = real_rb(continent, min_orders)
    return DomainNode(
        name="rivers",
        ratios=ratios,
        null_sampler=make_null_sampler(min_orders),
        is_self_organizing=True,
        interior_exp=None, interface_exp=None,   # real allometry deferred to Phase 3
        source=f"HydroRIVERS v10 {continent.upper()} (real); Horton Rb, "
               f"min_orders={min_orders}; n={ratios.size} basins",
    )
