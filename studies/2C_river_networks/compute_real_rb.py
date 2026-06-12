"""
Ingestion + caching for the REAL rivers node (Study 2C).

Runs the real-data path (`ingest.load_hydrosheds_reaches`) against a downloaded
HydroRIVERS continent shapefile, measures the Horton bifurcation ratio Rb for
every basin with >= 3 Strahler orders, and caches the per-basin measurements to
`results/rb_real_<continent>.json`. `river_node.build_node()` consumes that
cache, so the integration runner does not need the 60+ MB raw download present.

Each record is (rb, max_order, r_squared); keeping max_order lets the node and
the sensitivity analysis re-threshold (min_orders 3/4/5/6) from one cache.

Usage (in an environment with the HydroRIVERS download on disk):
    python compute_real_rb.py --continent na \
        --shp data/HydroRIVERS_v10_na_shp/HydroRIVERS_v10_na.shp

Raw downloads live under data/ and are git-ignored; the small JSON cache is the
committed node input. Regenerable by one command given the download.

SEAL DISCIPLINE: run this ONLY for discovery continent(s). Do NOT run it for the
sealed cross-continent holdout until the confirmation stage (see
results/SEALED_HOLDOUT.md), or you contaminate the holdout.
"""

from __future__ import annotations

import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")

HYDRORIVERS_VERSION = "v10"
SOURCE = "HydroSHEDS HydroRIVERS v1.0 (data.hydrosheds.org), free download"


def compute(shp_path: str, basin_field: str = "MAIN_RIV", min_orders: int = 3):
    """Return (n_reaches, [(rb, max_order, r2), ...]) for one continent file."""
    import sys
    sys.path.insert(0, HERE)
    from ingest import load_hydrosheds_reaches, iter_basin_measurements

    basins = load_hydrosheds_reaches(shp_path, basin_field=basin_field)
    n_reaches = sum(len(b) for b in basins.values())
    records = [
        [round(float(rb), 6), int(mo), round(float(r2), 6)]
        for _, rb, r2, mo in iter_basin_measurements(basins, min_orders=min_orders)
    ]
    return n_reaches, records


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--continent", required=True, help="continent code, e.g. na, sa, au, eu")
    ap.add_argument("--shp", required=True, help="path to HydroRIVERS_v10_<c>.shp")
    ap.add_argument("--basin-field", default="MAIN_RIV")
    args = ap.parse_args()

    n_reaches, records = compute(args.shp, basin_field=args.basin_field, min_orders=3)
    payload = {
        "continent": args.continent,
        "source": SOURCE,
        "hydrorivers_version": HYDRORIVERS_VERSION,
        "basin_field": args.basin_field,
        "min_orders_floor": 3,
        "n_reaches": n_reaches,
        "n_basins": len(records),
        "fields": ["rb", "max_order", "r_squared"],
        "records": records,
    }
    os.makedirs(RESULTS, exist_ok=True)
    out = os.path.join(RESULTS, f"rb_real_{args.continent}.json")
    with open(out, "w") as f:
        json.dump(payload, f)
    print(f"wrote {out}: {len(records):,} basins from {n_reaches:,} reaches")


if __name__ == "__main__":
    main()
