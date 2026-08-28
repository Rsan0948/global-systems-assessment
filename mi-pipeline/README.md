# Modernization Index data pipeline

This directory builds the country-year panel used by the Modernization Index. It downloads World Bank indicators, combines them with five manually sourced datasets, normalizes the inputs, and writes scored CSV, Excel, and text outputs.

The public website uses the scoring implementation in `mi-research`. This pipeline is kept separately so source acquisition and score calculation remain auditable.

## Quick start

```bash
cd mi-pipeline
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

# Print the required data layout
python mi_pipeline.py --setup

# Build from committed and cached inputs without API calls
python mi_pipeline.py --skip-api

# Refresh World Bank data, then build
python mi_pipeline.py
```

The full refresh requires network access. The manual source files are already committed for reproducibility. If you replace them with a newer vintage, document the source and date in [`DATA_PROVENANCE.md`](DATA_PROVENANCE.md).

## Inputs

The pipeline uses:

- Worldwide Governance Indicators and World Development Indicators from the World Bank API
- Corruption Perceptions Index data from Transparency International
- Global Innovation Index data from WIPO and the documented historical panel
- Economic Complexity Index data from the Harvard Growth Lab Atlas
- Human Development Report components from UNDP
- Fragile States Index data from the Fund for Peace

Exact files, editions, transformations, coverage limits, and checks are recorded in [`DATA_PROVENANCE.md`](DATA_PROVENANCE.md).

## Outputs

Generated files are written to `output/`:

| File | Purpose |
| --- | --- |
| `mi_master_dataset.csv` | Complete merged country-year panel |
| `mi_scored_countries.csv` | Rows with enough coverage to score |
| `mi_complete.xlsx` | Workbook with master and yearly sheets |
| `mi_coverage_report.txt` | Missingness and regional coverage |
| `mi_analytical_findings.txt` | Pipeline-level analytical checks |

The pipeline supports target years 1996, 2004, 2012, 2018, and 2024. Source gaps remain visible rather than being silently invented or interpolated.

## Live API identification

GitHub and SEC ingestion utilities elsewhere in the repository accept an identifying user agent through `USG_HTTP_USER_AGENT`. For live research pulls, set it to a real project name and contact address:

```bash
export USG_HTTP_USER_AGENT="Universal System Grade research contact@example.org"
```

Never commit the contact address, credentials, or API tokens to the repository.

## Verification

```bash
python test_smoke.py
```

After a successful run, review coverage and anchor checks before committing generated outputs. A successful pipeline run confirms that the transformation works on the supplied inputs. It does not validate the research claims that use the panel.
