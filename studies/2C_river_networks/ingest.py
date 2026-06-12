"""
Data ingestion for Study 2C.

Two paths:

1. `load_hydrosheds_reaches(path)` — the REAL-DATA path. HydroSHEDS' river
   network (e.g. the RiverATLAS / HydroRIVERS attribute table) provides, per
   reach, a unique id (`HYRIV_ID` / `ARCID`) and the id of the next reach
   downstream (`NEXT_DOWN`), with 0 marking an outlet. We translate that into
   the {node -> downstream} dict that `horton.measure_basin` consumes, and we
   split reaches into basins using the basin id field (`MAIN_BAS` / `HYBAS_ID`).
   This function is what you run in an environment with network/disk access to
   the HydroSHEDS download. It is import-guarded so the module loads even where
   geopandas/pyogrio are absent.

2. `basins_from_downstream_table(df, ...)` — a thin adapter used by both the
   real path and the synthetic generators, so the statistical code never sees
   the difference between real and simulated basins.

NOTE: the firewalled build environment cannot fetch HydroSHEDS. The real path
is written, typed, and documented but is exercised against a tiny fixture in
the tests; the runnable end-to-end result in this repo uses the synthetic
generators (see `synthetic.py`) as a pre-registered calibration/power study,
not as evidence about real rivers.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Iterator


def basins_from_downstream_table(
    rows: list[tuple[int, int, int]],
    outlet_sentinel: int = 0,
) -> dict[int, dict[int, int]]:
    """Group (reach_id, next_down_id, basin_id) rows into per-basin link dicts.

    `next_down_id == outlet_sentinel` marks a basin outlet; it is remapped to
    the -1 sentinel that `horton` expects.

    Returns {basin_id: {node_id: downstream_id}}.
    """
    by_basin: dict[int, dict[int, int]] = defaultdict(dict)
    for reach_id, next_down, basin_id in rows:
        d = -1 if next_down == outlet_sentinel else next_down
        by_basin[basin_id][reach_id] = d
    return dict(by_basin)


def load_hydrosheds_reaches(
    path: str,
    id_field: str = "HYRIV_ID",
    next_field: str = "NEXT_DOWN",
    basin_field: str = "MAIN_BAS",
    layer: str | None = None,
) -> dict[int, dict[int, int]]:
    """Load a HydroSHEDS/HydroRIVERS layer into per-basin downstream dicts.

    Requires geopandas (and a driver such as pyogrio/fiona). Reads only the
    three attribute columns we need. Geometry is ignored — topology is all the
    Horton analysis uses.
    """
    try:
        import geopandas as gpd  # noqa: WPS433 (optional heavy dep)
    except ImportError as exc:  # pragma: no cover - exercised only with real data
        raise ImportError(
            "load_hydrosheds_reaches requires geopandas; install it in an "
            "environment with access to the HydroSHEDS download."
        ) from exc

    gdf = gpd.read_file(path, layer=layer, columns=[id_field, next_field, basin_field])
    rows = [
        (int(r[id_field]), int(r[next_field]), int(r[basin_field]))
        for _, r in gdf.iterrows()
    ]
    return basins_from_downstream_table(rows, outlet_sentinel=0)


def iter_basin_measurements(
    basins: dict[int, dict[int, int]],
    min_orders: int = 3,
) -> Iterator[tuple[int, float, float, int]]:
    """Yield (basin_id, Rb, r_squared, max_order) for basins large enough to
    estimate Rb; silently skip basins with too few Strahler orders."""
    from horton import measure_basin

    for basin_id, links in basins.items():
        try:
            m = measure_basin(links, min_orders=min_orders)
        except ValueError:
            continue
        yield basin_id, m.rb, m.r_squared, m.max_order
