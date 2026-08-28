# Contributing

Contributions are welcome. Useful work includes correcting a source, reproducing a result, testing a claim with a different method, improving the software, or making the documentation easier to understand.

## Before you begin

For a typo or a small documentation fix, you can open a pull request directly. For changes to scoring, thresholds, taxonomies, datasets, or published claims, open an issue first. This gives maintainers and reviewers a place to agree on the evidence standard before substantial work begins.

Please read:

- [README.md](README.md) for the project map
- [REPRODUCE.md](REPRODUCE.md) for setup and verification
- [The claims ledger](mi-research/docs/CLAIMS_LEDGER.md) before changing or citing a research claim
- [The Code of Conduct](CODE_OF_CONDUCT.md) for community expectations

## High-value research contributions

The project especially welcomes:

1. Independent recoding of the 25 ancient cases using the published historical scoring protocol
2. Replication of the language-fragmentation result using different tree sources or reconstruction methods
3. Alternative null models for the tree-shape baselines
4. Out-of-sample tests that follow the existing sealed-flag rules without changing thresholds after seeing results
5. Corrections to sources, dates, interpretations, or dataset provenance

A failed replication is useful. It should be reported with the same care as a successful one.

## Development setup

Python 3.11 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
pytest -q mi-research/tests
pytest -q collectivization/tests
pytest -q fragmentation/tests
```

For website work:

```bash
cd mi-website/web
npm ci
npm run build
```

## Research standards

- Prefer primary data when proposing a scoring change. If you use a composite index, explain why it is appropriate.
- Specify the null model before presenting a discovery claim.
- Keep development, holdout, and prospective evidence separate. Do not tune a threshold on the data used to evaluate it.
- Add or update the relevant entry in `mi-research/docs/CLAIMS_LEDGER.md` and `mi-research/data/claims/claims.json` when a public claim changes.
- Preserve retired and failed claims. Add the new evidence and verdict instead of deleting the old record.
- Keep source attribution and upstream license information with any added data.

## Pull requests

Keep each pull request focused. Include:

- A short explanation of the problem and the proposed change
- The files, datasets, and claims affected
- Commands used to verify the change
- Seeds, sample windows, and source versions for quantitative work
- Before-and-after screenshots for visible website changes

Do not commit credentials, API tokens, local paths, private correspondence, or downloaded data that cannot legally be redistributed.

By contributing, you agree that your contribution will be distributed under the repository's existing noncommercial license terms. See [LICENSE](LICENSE).

## Getting help

Open a focused issue if you are unsure where a contribution belongs. Security concerns should follow [SECURITY.md](SECURITY.md), not a public issue.
