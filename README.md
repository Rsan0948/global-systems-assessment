# Universal System Grade

Universal System Grade is a public research project about how complex systems divide, endure stress, and form again. It combines three related research programs with a country-level website and a claims ledger that keeps successful, mixed, failed, and pending findings separate.

Explore the country data at the [Modernization Index website](https://web-gamma-bice-97.vercel.app).

## Start with the evidence

The [claims ledger](mi-research/docs/CLAIMS_LEDGER.md) is the authoritative record of the project's findings. A [machine-readable copy](mi-research/data/claims/claims.json) is also available. If a summary elsewhere in the repository disagrees with the ledger, use the ledger.

Each claim records two things:

- Its evidence design, such as descriptive analysis, hindsight retrodiction, blind out-of-sample testing, prospective testing, interpretation, or simulation
- Its current verdict, such as supported, mixed, not supported, pending, or retired

This distinction matters. A reproducible score is not automatically a validated forecast, and a result that fits historical cases is not automatically predictive.

## What is in the repository

### Modernization Index

The Modernization Index is a five-pillar description of a country's structural capacity. It covers institutions, economic complexity, human capital, economic structure, and stability. The public atlas currently includes 190 scored country profiles.

- Research and scoring code: [`mi-research/`](mi-research/)
- Data preparation pipeline: [`mi-pipeline/`](mi-pipeline/)
- Website and publishing pipeline: [`mi-website/`](mi-website/)

### Fragmentation

The fragmentation program studies branching structure across natural and social systems. It uses Horton-Strahler and Tokunaga measures, along with null models designed to separate genuine structure from patterns that appear in random trees.

- Research program: [`fragmentation/`](fragmentation/)
- Main census: [`fragmentation/census/`](fragmentation/census/)
- Preregistrations and governance records: [`fragmentation/preregistration/`](fragmentation/preregistration/) and [`fragmentation/governance/`](fragmentation/governance/)

### Collectivization

The collectivization program studies how political systems form and reform. It uses a fixed 15-feature governance vector and a Hamming-distance classifier across 109 formation cycles in 30 historical cases.

- Research program: [`collectivization/`](collectivization/)
- Casebook: [`collectivization/cases/`](collectivization/cases/)
- Results: [`collectivization/results/`](collectivization/results/)

## Current evidence in plain language

The repository contains 109 Modernization Index historical cases: 84 modern hindsight cases and 25 ancient cases scored by interpretation. The separate out-of-sample program contains 67 observations across several cohorts. The collectivization study contains 30 cases and 109 formation cycles. The public country atlas is descriptive and should not be counted as validation evidence.

Some findings have held up. River branching concentration passed both discovery and a sealed geographic holdout. The backsliding model recorded an out-of-sample AUC of 0.746, although it remains provisional. Other ideas did not survive testing. The proposed constant near Euler's number was retired, the current DGS instability test was null, and the preregistered golden-age forward test failed.

That mixed record is intentional. Failed tests remain visible because the audit trail is part of the research.

## What this project does not claim

- It is not a rating agency. Country scores describe structural configurations, not national worth or political virtue.
- It is not a collapse clock. The public score is descriptive, and timing claims remain limited and exploratory.
- It is not immune to weak inputs. Some historical cases require interpretation, public statistics can be manipulated, and automated scoring can flatten important context.
- It does not treat one successful historical fit as proof of a universal law.

See [Defensible Results](DEFENSIBLE_RESULTS.md) for the shortest account of what can be stated confidently.

## Quick start

Python 3.11 or newer is recommended.

```bash
git clone https://github.com/Rsan0948/universalsystemgrade.git
cd universalsystemgrade
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

# Run the repository test suites
pytest -q mi-research/tests
pytest -q collectivization/tests
pytest -q fragmentation/tests

# Score one country
cd mi-research
python scripts/score_country.py --country "Estonia" --year 2024
```

For the full set of commands and expected outputs, see [Reproducing the Results](REPRODUCE.md).

## Contributing

Corrections, replications, independent recoding, new null models, documentation improvements, and focused software changes are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md). Please use the issue templates for claim disputes and replication challenges so the evidence trail remains easy to follow.

## Data and provenance

The project draws on public and research datasets including V-Dem, the Worldwide Governance Indicators, World Development Indicators, Polity5, UCDP/PRIO, Glottolog, WALS, HYDE, Seshat, FAO GAUL, ITU, SEC EDGAR, ParlGov, CINC/NMC, Geacron, and Our World in Data.

The repository's license does not replace the terms of upstream data providers. Each upstream dataset remains subject to its original license and access terms. See [`mi-pipeline/DATA_PROVENANCE.md`](mi-pipeline/DATA_PROVENANCE.md) and the source notes within each research program before redistributing data.

## License and citation

The project is source available for noncommercial use:

- Code is available under the [PolyForm Noncommercial License 1.0.0](LICENSE).
- Original documentation, analysis, and curated datasets are available under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
- Third-party data remains governed by its original provider.

You may inspect, copy, modify, and redistribute the project for permitted noncommercial purposes. Commercial use requires separate written permission. See [LICENSE](LICENSE) for the exact scope and [CITATION.cff](CITATION.cff) for citation metadata.
