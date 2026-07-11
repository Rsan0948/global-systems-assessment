# Modernization Index — Data Pipeline

Complete pipeline to build the expanded MI dataset across 150+ countries and 5 time points (1996, 2004, 2012, 2018, 2024).

## Quick Start

```bash
cd mi-pipeline
pip install -r requirements.txt

# See data setup instructions
python mi_pipeline.py --setup

# Place manual CSV files in ./data/ (see below)

# Run the full pipeline
python mi_pipeline.py

# Skip API calls (use cached data from previous run)
python mi_pipeline.py --skip-api
```

## What It Does

1. **Pulls WGI + WDI** from the World Bank API automatically (9 indicators)
1. **Loads 5 manual CSVs** you place in `./data/` (CPI, GII, ECI, HDR sub-indices, FSI)
1. **Merges** into a single country-year panel
1. **Normalizes** per the MI methodology (log-GDP, inverted rents/ODA/FSI, min-max ECI, etc.)
1. **Scores** every country-year under both v1 (anchor-based, Switzerland/Lebanon) and v2 (percentile-GPA)
1. **Reports** coverage, gaps, tier distributions, and analytical findings
1. **Outputs** to `./output/` as CSV, Excel, and text reports

## Automatic Data (World Bank API)

These are pulled automatically — no manual download needed:

|Indicator                                 |API Code         |Source|
|------------------------------------------|-----------------|------|
|Government Effectiveness (percentile rank)|GE.PER.RNK       |WGI   |
|Rule of Law (percentile rank)             |RL.PER.RNK       |WGI   |
|Regulatory Quality (percentile rank)      |RQ.PER.RNK       |WGI   |
|Control of Corruption (percentile rank)   |CC.PER.RNK       |WGI   |
|Political Stability (percentile rank)     |PV.PER.RNK       |WGI   |
|GDP per capita PPP                        |NY.GDP.PCAP.PP.CD|WDI   |
|Natural resource rents (% GDP)            |NY.GDP.TOTL.RT.ZS|WDI   |
|Net ODA received (% GNI)                  |DT.ODA.ODAT.GN.ZS|WDI   |
|R&D expenditure (% GDP)                   |GB.XPD.RSDV.GD.ZS|WDI   |

After the first run, results are cached in `./data/wb_cached.csv` so subsequent runs can use `--skip-api`.

## Manual Data Files

Place these 5 CSV files in `./data/`. The loaders auto-detect common column name variations, but the cleanest format is shown below.

### 1. `cpi.csv` — Corruption Perceptions Index

**Download from:** <https://www.transparency.org/en/cpi/>

Go to the CPI page → look for “Download full dataset” or “Export” → save as CSV.

**Expected format:**

```csv
iso3,country,year,CPI
DNK,Denmark,2024,90
NZL,New Zealand,2024,87
FIN,Finland,2024,87
...
```

**Notes:**

- CPI uses a 0–100 scale (only comparable from 2012 onward)
- For 1996/2004, the pipeline uses WGI Control of Corruption instead (pulled automatically)
- You only need 2012, 2018, and 2024 rows

### 2. `gii.csv` — Global Innovation Index

**Download from:** <https://www.wipo.int/global_innovation_index/en/>

Each year’s edition has a downloadable data annex (usually Excel). Combine the years you need into one CSV.

**Expected format:**

```csv
iso3,country,year,GII
CHE,Switzerland,2024,67.5
SWE,Sweden,2024,64.5
USA,United States,2024,62.4
...
```

**Notes:**

- GII uses a 0–100 score
- Available from 2007 only; for 1996/2004 the pipeline uses R&D expenditure instead
- You need 2012, 2018, and 2024 editions

### 3. `eci.csv` — Economic Complexity Index

**Download from:** <https://atlas.hks.harvard.edu/data-downloads/>
**Or Dataverse:** <https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/XTAQMC>

The Atlas bulk download includes annual ECI values for ~145 countries from 1995 onward.

**Expected format:**

```csv
iso3,country,year,ECI
JPN,Japan,2024,2.27
KOR,South Korea,2024,1.95
CHE,Switzerland,2024,2.15
...
```

**Notes:**

- Use **Harvard Growth Lab Atlas** values, NOT OEC (they differ)
- The pipeline will snap annual data to target years
- ⚠ Pin to pre-2026 methodology vintage (2026 switches from binary to continuous RCA)
- The column may be called `eci_value` or `economic_complexity_index` in the download — the loader handles this

### 4. `hdr.csv` — Human Development Report Sub-Indices

**Download from:** <https://hdr.undp.org/data-center/documentation-and-downloads>

Download the statistical annex tables (usually Excel). You need the **Education Index** and **Life Expectancy Index** columns (both 0–1 scale). These are separate from the composite HDI.

**Expected format:**

```csv
iso3,country,year,EduIdx,LifeExpIdx
NOR,Norway,2024,0.937,0.952
CHE,Switzerland,2024,0.900,0.955
AUS,Australia,2024,0.926,0.948
...
```

**Notes:**

- Both sub-indices are already 0–1 scaled
- Available for ~193 countries with historical recomputation back to 1990s
- You need values at all 5 time points (1996, 2004, 2012, 2018, 2024)

### 5. `fsi.csv` — Fragile States Index

**Download from:** <https://fragilestatesindex.org/excel/>

**Expected format:**

```csv
iso3,country,year,FSI
SOM,Somalia,2024,111.3
YEM,Yemen,2024,108.8
SSD,South Sudan,2024,109.0
...
NOR,Norway,2024,12.7
FIN,Finland,2024,15.2
```

**Notes:**

- FSI uses a 0–120 scale (higher = more fragile); the pipeline inverts this
- Available from 2005 only (started with 60 countries, now 179)
- For 1996/2004, the pipeline uses WGI Political Stability alone
- You need 2012, 2018, and 2024

## Output Files

All outputs go to `./output/`:

|File                        |Description                                                                    |
|----------------------------|-------------------------------------------------------------------------------|
|`mi_master_dataset.csv`     |Complete panel: all country-year obs including those with >2 gaps              |
|`mi_scored_countries.csv`   |Only scoreable countries (≤2 indicator gaps)                                   |
|`mi_complete.xlsx`          |Excel workbook with Master sheet + per-year sheets                             |
|`mi_coverage_report.txt`    |Coverage counts, excluded countries, regional breakdown                        |
|`mi_analytical_findings.txt`|Phase 6 thesis tests: institutional centrality, resource penalty, configuration|

## Scoring Methodology

### v1 (Anchor-Based)

- Raw composite: `0.25(P1) + 0.25(P2) + 0.20(P3) + 0.20(P4) + 0.10(P5)`
- Final: `M = (raw - Lebanon_2024_raw) / (Switzerland_2024_raw - Lebanon_2024_raw)`
- No clamping — countries can exceed 1.0 or fall below 0.0

### v2 (Percentile-GPA)

- Each indicator percentile-ranked within its year’s cohort
- GPA = (percentile / 100) × 4.0
- Weighted: P1 34%, P2 15%, P3 16%, P4 20%, P5 16%

### Track 1 (2012, 2018, 2024)

Full formula with all 13 indicators

### Track 2 (1996, 2004)

Three substitutions:

- R&D expenditure replaces GII (P2)
- WGI Control of Corruption replaces CPI (P1)
- Political Stability alone carries P5 (no FSI)

## Normalization Rules

|Indicator             |Rule                                              |
|----------------------|--------------------------------------------------|
|WGI percentile ranks  |÷ 100                                             |
|CPI                   |÷ 100                                             |
|GII                   |÷ 100                                             |
|ECI                   |min-max across full dataset                       |
|R&D                   |min-max across full dataset                       |
|Education Index       |already 0–1                                       |
|Life Expectancy Index |already 0–1                                       |
|GDP per capita PPP    |log-transform → min-max                           |
|Resource rents (% GDP)|inverted: 1 − min(rents/50, 1)                    |
|Net ODA (% GNI)       |inverted: 1 − min(ODA/20, 1); 0 for non-recipients|
|FSI                   |inverted: 1 − (FSI/120)                           |

## Tips

- **First run** takes ~5 minutes (World Bank API rate-limited). Subsequent runs with `--skip-api` are fast.
- The pipeline tolerates missing files gracefully — it’ll score whatever data you provide and report gaps.
- For validating against the existing 85-country dataset, compare the `v1_MScore` column in the output with your original scores. Differences > 0.02 are likely from the expanded min-max normalization range.
- If a data source uses different country names, the pipeline joins on ISO-3 codes — make sure your CSVs include an `iso3` column.

---

## ⚠ Environment note (why this is a local-machine job)

This scaffold was prepared in a sandboxed remote environment that **cannot run
the pipeline end-to-end**. Two blockers, both confirmed:

1. **Outbound network is policy-restricted.** `api.worldbank.org` returns 403
   from the sandbox proxy (only package registries + Anthropic are whitelisted),
   so the automated WGI/WDI pull returns nothing there. Your local machine has
   open network and will work normally.
2. **The 5 manual CSVs require human downloads** from interactive portals
   (Transparency International, WIPO, Harvard Atlas, UNDP, Fund for Peace) — a
   manual step on *any* machine.

So: run this **locally**. See `CLAUDE.md` in this directory for the run procedure
and the known code issues a local agent should fix before the first real run.
