# Data provenance — mi_pipeline real run

This records exactly how the inputs in `./data/` were acquired and shaped for the
first real end-to-end run. The CSVs (and the generated `./output/`) **are committed
to the repo** as of 2026-06-28; this file is the reproducible record of where each
one came from.

Acquired 2026-06-27. All sources are free/public. **No values were invented or
interpolated** — every figure is a real upstream observation; the only
transformations applied are documented normalizations using each provider's own
published methodology, and "nearest available year" snaps consistent with the
pipeline's own `_snap_to_target_years` logic.

## Automatic — World Bank API (`data/wb_cached.csv`)

Pulled by `python mi_pipeline.py` (cached for `--skip-api`). 1275 country-year rows,
259 countries, all 5 time points, 9 indicators.

**Important upstream change handled in code:** the World Bank restructured the WGI
database. The legacy percentile-rank codes (`GE.PER.RNK`, etc.) now return
*"indicator not found — deleted or archived."* The pipeline now uses the current
WGI 0–100 governance-score codes `GOV_WGI_<dim>.SC` under `source=3` (direct
successor to the percentile ranks; same 0–100 range → `÷100` normalization
unchanged). Verified anchors, e.g. Switzerland 2024 GovEff ≈ 87, Lebanon ≈ 29.

| Source | Notes |
|--------|-------|
| WGI GE/RL/RQ/CC/PV `.SC` (source 3) | 0–100 governance scores |
| WDI GDPpcPPP, ResRents, ODA, RD | default source |

Known real data lag: **WDI natural-resource-rents (`ResRents`) has no 2024 value
yet** (latest ≈ 2021; outside the ±2yr snap window), so every 2024 row carries a
ResRents gap. This is honestly reported by the gap counter; P4 still scores from
GDP + ODA, and the "resource penalty" thesis cannot run for 2024.

## Manual CSV 1 — CPI (`data/cpi.csv`)

- **Source:** Transparency International, `CPI2024-Results-and-trends.xlsx`
  (`https://files.transparencycdn.org/images/CPI2024-Results-and-trends.xlsx`).
- File is **Strict OOXML** (namespace `purl.oclc.org/...`), which openpyxl/pandas
  cannot open via the high-level API; parsed the `CPI Timeseries 2012 - 2024`
  worksheet XML + shared strings directly.
- Extracted `CPI score {2012,2018,2024}` → `iso3,country,year,CPI` (0–100).
- 535 rows, 181 countries. Spot-check vs README: Denmark 2024 = 90 ✓, NZ 83, CHE 81, LBN 22.

## Manual CSV 2 — GII (`data/gii.csv`)  ✅ all 3 years

All three required editions obtained, from two complementary sources:

- **2024:** WIPO GII 2024 data annex
  (`https://www.wipo.int/edocs/pubdocs/en/wipo-pub-2000-2024-tech1.xlsx`), overall
  "Global Innovation Index" score from the `Data` sheet. 133 economies.
  Spot-check vs README: CHE 67.5 ✓, SWE 64.5 ✓, USA 62.4 ✓.
- **2012 & 2018:** WIPO's own Data Explorer only serves 2023–2025 and the
  `tech1.xlsx` pattern only goes back to 2022, so the older editions came from a
  **GII panel dataset on Mendeley Data** (Elsevier's research-data repository),
  `doi:10.17632/cvkdzr8tv3.4` — "Global Innovation Index: panel data (2011–2022)",
  `Scores` sheet, `Global Innovation Index` column. Downloaded via the Mendeley
  public-files API. 141 economies (2012), 126 (2018).
- **Validated against the official WIPO figures before use** (this is a third-party
  compilation, so it was cross-checked, not trusted blindly): the panel reproduces
  the published GII scores *exactly* —
  - 2012: Switzerland 68.20, Sweden 64.80, Singapore 63.50, Finland 61.80, UK 61.20,
    Netherlands 60.50 (matches the official GII 2012 top-6 order and scores).
  - 2018: Switzerland 68.40, Netherlands 63.30, Sweden 63.10, UK 60.10, US 59.80,
    Singapore 59.80 (matches the WIPO 2018 press-release ranking and scores exactly).
- Names mapped to ISO3 via the WB name list + 17 explicit overrides
  (e.g. "Iran (Islamic Republic of)"→IRN, "Republic of Korea (the)"→KOR); 0 unmapped.
- gii.csv total: 400 rows — 2012 (141) / 2018 (126) / 2024 (133).

## Manual CSV 3 — ECI (`data/eci.csv`)

- **Source:** Harvard Growth Lab Atlas, Dataverse `doi:10.7910/DVN/XTAQMC`, file
  `growth_proj_eci_rankings.csv` (downloaded via the public Dataverse access API).
- Used `eci_hs92` (Atlas headline ECI, full 1995–2024 coverage; **classic binary-RCA
  vintage, pre-2026 methodology** as the README requires). NOT OEC.
- Provided as the full annual series (1995–2024); the pipeline snaps to target years.
- 4319 rows, 145 countries. Ordering matches the Atlas (Japan #1 ≈ 1.73 in 2024,
  CHE 1.58, USA 1.12, LBN 0.38).

## Manual CSV 4 — HDR (`data/hdr.csv`)

- **Source:** UNDP HDR 2025 composite-indices time series
  (`https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Composite_indices_complete_time_series.csv`).
- UNDP publishes the **components** (`le`, `eys`, `mys`), not the dimension indices.
  Derived the Education Index and Life Expectancy Index with UNDP's own published
  goalposts (HDR Technical Note 1):
  - `LifeExpIdx = clip((le − 20) / (85 − 20), 0, 1)`
  - `EduIdx = (clip(eys/18,0,1) + clip(mys/15,0,1)) / 2`
  This is normalization via the provider's documented method, not interpolation;
  missing components stay NaN (reported as gaps).
- Target years 1996/2004/2012/2018 use that exact year; **2024 uses 2023** (the latest
  published — UNDP has no 2024 yet), a 1-yr "latest available" snap.
- 975 rows, 195 countries. Spot-check vs README: Norway EduIdx 0.937 ✓.

## Manual CSV 5 — FSI (`data/fsi.csv`)

- **Source:** Fund for Peace Fragile States Index, per-year Excel from
  `fragilestatesindex.org/excel/` — `fsi-2012.xlsx`, `fsi-2018.xlsx`, and
  `FSI-2023-DOWNLOAD.xlsx`. Took the `Total` (0–120) score.
- FSI files have no ISO3; mapped country names → ISO3 from the World Bank name list
  plus 22 explicit overrides (e.g. "Congo Democratic Republic"→COD,
  "Israel and West Bank"→ISR, "Turkey"→TUR). 0 names left unmapped.
- Target years 2012/2018 use that exact edition; **2024 uses the 2023 edition** (no
  2024/2025 edition published yet at the predicted URLs), a "latest available" snap.
- 535 rows, 179 countries. Spot-check vs README: Somalia 111.9, Yemen 108.9, Norway 14.5.

## Run result (sanity checks)

`python mi_pipeline.py --skip-api` → 180 unique countries scored; per year
1996:154 / 2004:174 / 2012:168 / 2018:167 / 2024:143 (806 scoreable obs).
Anchors resolved (Switzerland 2024 v1_MScore = 1.000, Lebanon = 0.000). P3
(Human Capital) populated, not all-NaN. Top MI 2024: Switzerland 1.00, Singapore
0.99, Norway 0.90, Germany/Japan 0.88 — all plausible. `test_smoke.py` 5/5.
(Adding GII 2012/2018 lifted 2012 scoreable 160→168 and 2018 162→167.)

**Disclaimer unchanged:** this proves the *pipeline* on real inputs. The only
remaining coverage caveats are the two "latest available" snaps (HDR/FSI 2024←2023,
because the 2024 editions aren't published yet) and the WDI resource-rents 2024 lag —
all reported as gaps rather than filled. No values were invented or interpolated.
