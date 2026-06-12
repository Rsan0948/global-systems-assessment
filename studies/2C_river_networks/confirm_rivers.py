"""
Rivers CROSS-CONTINENT CONFIRMATION (Study 2C).

Discovery froze the rivers claim on North America (FROZEN_DISCOVERY_CLAIM.md,
predictions A1-A3). This re-runs the frozen test on the sealed holdout continent
(South America), which discovery never inspected. Run only AFTER the freeze.

    python confirm_rivers.py        # requires results/rb_real_sa.json
"""

from __future__ import annotations

import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import river_node as rn

E = math.e


def confirm(discovery="na", holdout="sa", min_orders=4, seed=99) -> dict:
    na = rn.real_rb(discovery, min_orders)
    sa = rn.real_rb(holdout, min_orders)
    na_g = float(np.exp(np.log(na).mean()))
    sa_g = float(np.exp(np.log(sa).mean()))

    sampler = rn.make_null_sampler(min_orders)
    rng = np.random.default_rng(seed)
    null = np.array([np.exp(np.log(sampler(sa.size, rng)).mean()) for _ in range(2000)])
    p_beats_null = float((null >= sa_g).mean())
    frac_above_e = float((sa > E).mean())

    a1 = p_beats_null < 0.05                       # A1: holdout beats random topology
    a2 = 3.2 <= sa_g <= 3.8                        # A2: consistent with NA (~3.49)
    a3 = sa_g > E and frac_above_e > 0.5           # A3: above e
    return {
        "discovery_continent": discovery, "discovery_geom_rb": round(na_g, 3),
        "holdout_continent": holdout, "holdout_geom_rb": round(sa_g, 3),
        "holdout_n_basins": int(sa.size), "holdout_null_geom_rb": round(float(null.mean()), 3),
        "A1_beats_null": a1, "A1_p": p_beats_null,
        "A2_in_band": a2, "A3_above_e": a3, "A3_frac_above_e": round(frac_above_e, 3),
        "CONFIRMED": bool(a1 and a2 and a3),
    }


if __name__ == "__main__":
    r = confirm()
    for k, v in r.items():
        print(f"  {k:22s}: {v}")
    print("\nCONFIRMATION:", "PASS — holdout reproduces the discovery finding"
          if r["CONFIRMED"] else "FAIL")
