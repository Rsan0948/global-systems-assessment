# data/countries/ — retired (superseded by the internal Data API)

Per-country indicator JSON copies used to live here. They are **gone on purpose**:
indicator data is now served by the internal Data API (`mi/datasource.py`), which
assembles values **live from the canonical sources** — `data/sources/wb_anchored.json`
(World Bank 2025-anchored WGI/WDI snapshot; refresh with `scripts/refresh_wgi_wdi.py`)
plus the committed `mi_pipeline/` panel CSVs (CPI/GII/ECI/FSI/HDR).

Why: single source of truth + propagation. Edit a source (or re-run the refresh) and
every case re-scores from it — no copies to keep in sync. Case records reference
`(country, year)`; `mi.scoring.load_country_data` resolves through the Data API.

Score any covered country:  `python scripts/score_country.py --country "Estonia" --year 2024`
