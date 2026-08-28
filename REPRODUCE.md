# Reproducing the results

This guide covers the shortest fresh-clone path for each research program. The repository includes the data snapshots needed for its standard test suites, so the basic checks do not require network access.

Reproducing a number confirms that the committed code and inputs produce the same output. It does not, by itself, establish that a claim is externally valid. Use the [claims ledger](mi-research/docs/CLAIMS_LEDGER.md) to see how each result was tested.

## Setup

Python 3.11 or newer is recommended.

```bash
git clone https://github.com/Rsan0948/universalsystemgrade.git
cd universalsystemgrade
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1`.

## Run the complete test set

From the repository root:

```bash
pytest -q -p no:cacheprovider mi-research/tests
pytest -q -p no:cacheprovider collectivization/tests
pytest -q -p no:cacheprovider fragmentation/tests
```

## Modernization Index

```bash
cd mi-research

# Score one country
python scripts/score_country.py --country "Estonia" --year 2024

# Compare two countries
python scripts/compare_countries.py --a "Estonia" --b "Russia" --year 2024

# Run the historical case validator
python scripts/run_retrodiction.py --validate data/case_studies/completed/

# Run the focused tests
pytest -q -p no:cacheprovider tests
```

The country score command prints the five pillars, relevant diagnostics, data coverage, and the scoring version. Historical validation results must be described as hindsight retrodiction, not as a forecast record.

Rebuilding all upstream inputs is a separate and heavier process. See [`mi-pipeline/README.md`](mi-pipeline/README.md) and [`mi-pipeline/DATA_PROVENANCE.md`](mi-pipeline/DATA_PROVENANCE.md).

## Fragmentation census

```bash
cd fragmentation/census
python run.py

cd ../integration
python run.py

cd ..
pytest -q -p no:cacheprovider tests
```

The census command refreshes `fragmentation/census/results/`. The integration command refreshes `fragmentation/integration/results/`. Consult the preregistrations and the claims ledger before treating a reported pattern as a confirmed claim.

## Collectivization

```bash
cd collectivization
python run.py
pytest -q -p no:cacheprovider tests
```

The main command rebuilds `results/cycle_analysis.json` and `results/cycle_summary.png` from the committed 30-case casebook.

## Website

The website reads generated JSON from `mi-website/web/public/data/`. It does not calculate country scores in the browser.

```bash
# From the repository root, rebuild the published dataset
python mi-website/scripts/refresh_and_build.py

# Build the site
cd mi-website/web
npm ci
npm run check
npm run build
```

Node.js 20.9 or newer is required.

## Reporting a mismatch

Open a replication challenge using the GitHub issue template. Include:

- The commit SHA
- The exact command
- The expected and observed values
- Your Python or Node.js version and operating system
- The data snapshot, source vintage, seed, and sample window when relevant
- Any local changes, including changes that seem unrelated

Exploratory work under `sandbox/` and `mi-research/sandbox/` is not part of the published claim set unless the claims ledger says otherwise.
