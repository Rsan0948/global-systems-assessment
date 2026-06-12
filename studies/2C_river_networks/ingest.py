"""
Data ingestion for Study 2C.

Two paths:

1. `load_hydrosheds_reaches(path)` — the REAL-DATA path. HydroSHEDS' river
   network (the HydroRIVERS attribute table) provides, per reach, a unique id
   (`HYRIV_ID`) and the id of the next reach downstream (`NEXT_DOWN`), with 0
   marking an outlet. We translate that into the {node -> downstream} dict that
   `horton.measure_basin` consumes, and we split reaches into complete drainage
   networks using `MAIN_RIV` — the id of the most-downstream reach of each
   river, so every group is one tree flowing to a single outlet. (NOTE: the
   real HydroRIVERS v10 table has NO `MAIN_BAS` field — that belongs to
   HydroBASINS; verified empirically against `HydroRIVERS_v10_na`. The grouping
   key is `MAIN_RIV`.) This function is what you run in an environment with
   disk access to the HydroRIVERS download. It is import-guarded so the module
   loads even where geopandas/pyogrio are absent.

2. `basins_from_downstream_table(df, ...)` — a thin adapter used by both the
   real path and the synthetic generators, so the statistical code never sees
   the difference between real and simulated basins.

REAL DATA IS LIVE: `studies/2C_river_networks/compute_real_rb.py` runs this
path against the HydroRIVERS download and caches per-basin Rb to `results/`,
which `river_node.build_node()` consumes. The synthetic generators
(`synthetic.py`) remain as the pre-registered calibration/power study and as
the mechanism-free null, not as evidence about real rivers.
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
    basin_field: str = "MAIN_RIV",
    layer: str | None = None,
) -> dict[int, dict[int, int]]:
    """Load a HydroRIVERS layer into per-basin downstream dicts.

    Reads only the three attribute columns we need; geometry is ignored —
    topology is all the Horton analysis uses. Prefers pyogrio (vectorised, ~1M
    reaches in seconds); falls back to geopandas. `basin_field` defaults to
    `MAIN_RIV` (the real HydroRIVERS grouping key; `MAIN_BAS` does not exist in
    this table — see module docstring).
    """
    cols = [id_field, next_field, basin_field]
    try:
        import pyogrio  # noqa: WPS433 (optional heavy dep; fast path)

        df = pyogrio.read_dataframe(path, columns=cols, read_geometry=False, layer=layer)
        rows = list(zip(
            df[id_field].to_numpy().astype("int64").tolist(),
            df[next_field].to_numpy().astype("int64").tolist(),
            df[basin_field].to_numpy().astype("int64").tolist(),
        ))
    except ImportError:
        try:
            import geopandas as gpd  # noqa: WPS433 (fallback)
        except ImportError as exc:  # pragma: no cover - exercised only with real data
            raise ImportError(
                "load_hydrosheds_reaches requires pyogrio or geopandas; install "
                "one in an environment with access to the HydroRIVERS download."
            ) from exc
        gdf = gpd.read_file(path, layer=layer, columns=cols)
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
