# Study 2C — River Networks (Horton bifurcation ratios)

This is the worked-out reference study for the pre-registration in
[`../../preregistration/PREREGISTRATION.md`](../../preregistration/PREREGISTRATION.md).
It is the cleanest physical test in the program: drainage networks are fully
self-organizing, every basin is an independent natural experiment, and the
source data (HydroSHEDS) is global and public.

## What this study does

For every drainage basin it estimates the **Horton bifurcation ratio** `Rb`
(the average factor by which the number of stream segments multiplies as you
go down one Strahler order), then asks of the pooled distribution of per-basin
`Rb` values: **is its center *e* ≈ 2.718, or 3, or π, or 2, or 4, or nothing
in particular?** That question is answered with Bayesian model comparison
(Bayes factors), exactly as the pre-registration's Phase 3A specifies, plus a
KDE mode estimate with a bootstrap CI. The pre-registered Tier decision
(§1.1 of the pre-reg) is computed from those numbers, not chosen by hand.

## Why the runnable result here uses simulated data

The build/firewall environment cannot reach the HydroSHEDS servers, so this
repository's runnable output is **not** a result about real rivers. It is the
pre-registration's required **calibration / power analysis**, which needs no
real data and answers a question the whole project depends on:

> Can the model-comparison procedure actually distinguish a true-*e* world
> from a true-3 world, and how many basins does it take?

This matters because *e* (2.718) and 3 are close together; if the test can't
separate them even with clean data, then the entire *e*-vs-3 debate is
statistically undecidable and Tier 1 should never be claimed. The power study
quantifies exactly where that line is.

There are two simulators, with different jobs (see `synthetic.py`):

- **`random_coalescent_basin`** builds a *real tree topology* so the Strahler
  ordering and Horton estimator run on genuine network structure. This neutral
  topology lands at `Rb ≈ 3.0` — **not** at *e*. The pipeline demo uses it to
  show the machinery returns the topology's true center and does **not**
  manufacture *e*. (When run, it correctly reports `best_model = "3"`, Tier 2,
  with the Bayes factor overwhelmingly against *e*.)
- **`sample_basin_rbs`** draws per-basin `Rb` from a population whose true
  center we set, so the power study can measure recovery of a *known* answer.

## Files

| file | role |
|------|------|
| `horton.py` | Strahler ordering + Horton `Rb` estimation (consumes real or synthetic topology identically) |
| `ingest.py` | **Real-data path**: HydroSHEDS/HydroRIVERS → per-basin link tables |
| `synthetic.py` | The two simulators described above |
| `analysis.py` | KDE mode + bootstrap CI; Bayesian model comparison; Tier decision |
| `power.py` | Pre-registered calibration / power grid |
| `run.py` | One-command driver; writes JSON + figures to `results/` |
| `tests/test_study2c.py` | Unit tests (Strahler correctness, recovery of known centers, neutral-topology guard) |

## Running

```bash
pip install -r requirements.txt
python run.py            # full: pipeline demo + power grid + figures
python run.py --quick    # fast smoke run
pytest tests/ -q         # unit tests
```

## Switching to real HydroSHEDS data

In an environment with network/disk access to the HydroSHEDS download
(e.g. `HydroRIVERS_v10.gdb`), run:

```bash
python run.py --hydrosheds /path/to/HydroRIVERS_v10.gdb
```

`ingest.load_hydrosheds_reaches` reads the `HYRIV_ID` / `NEXT_DOWN` /
`MAIN_BAS` attribute columns, groups reaches into basins, and feeds the
*identical* statistical stages. The only thing that changes is the data
source; the analysis, thresholds, and Tier logic are fixed by the
pre-registration.

## The pre-registered failure clause for this domain (do not forget it)

The river-networks literature frequently reports `Rb ≈ 4`. **If the real
pooled mode's 95% CI excludes *e* and includes 4, Tier 1 fails in the domain
registered as its strongest test**, and the program's headline downgrades to
Tier 2 or Tier 0. That is written down *before* any basin is measured, which
is the whole point.
