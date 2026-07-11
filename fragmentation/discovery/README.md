# Discovery engine

The reusable core instrument for the **discovery** reframe of this project. The
question is no longer "is the constant *e*?" but "**is there a lawful regularity
at all, and if so what kind?**" — answered as a four-rung ladder, with every
rung gated by a mechanism-free triviality control and confirmed on sealed data.

## The idea in one paragraph

"Is there a theorem?" is a question about **variance components**, not a mean.
Each domain (rivers, lungs, firms, polities, …) contributes one estimate of its
characteristic subdivision ratio with a standard error. A random-effects
(DerSimonian–Laird) decomposition then separates *within-domain* variance (is
each domain individually concentrated?) from *between-domain* variance τ² (do
domains share one value?). Cochran's Q tests universality. The candidate
constant falls out as the pooled estimate — it is a *readout*, never the entry
point. And nothing counts unless it survives comparison to a **trivial null**:
random-topology / random-merging baselines that already produce clustering near
3–4 with no law involved (demonstrated in `../natural-systems/rivers`).

## The ladder (`ladder.py`)

| rung | claim | how it's earned |
|------|-------|-----------------|
| 0 | **no theorem** | within-domain scatter large, *or* signal indistinguishable from the trivial null |
| 1 | **domain-specific laws** | each domain concentrated, but values differ across domains (high I²) |
| 2 | **universality** | domains share one value (Q n.s., low I²) *and* it beats the trivial null |
| 3 | **named constant** | pooled CI is tight enough to isolate a principled constant (e, 3, φ, π…) and exclude rivals |
| 4 | **mechanism** | the interior−interface dimensional gap *predicts* the ratio — **not decidable from ratios alone**; needs Study 3B exponent data (hook provided) |

The engine reports the **highest rung the evidence earns** and never claims more.

## Files

| file | role |
|------|------|
| `heterogeneity.py` | DerSimonian–Laird random-effects decomposition: pooled value + CI, τ², I², Cochran Q |
| `trivial_null.py` | runs the same analysis on mechanism-free draws; reports how far observed sits above the null |
| `ladder.py` | the four-rung verdict + the `split` / `confirm` discover→confirm discipline |
| `scenarios.py` | three known-truth worlds (universal / domain-specific / trivial) for calibration |
| `run.py` | calibration demo → `results/` |
| `tests/test_engine.py` | the engine returns rung 3 / 1 / 0 on the three worlds; heterogeneity math checks |

## Calibration result (`results/engine_calibration.json`, `.png`)

Run on known-truth synthetic worlds, the instrument returns the correct verdict
every time:

- **universal world** (all domains truly at *e*) → **rung 3**, pooled CI
  ≈ [2.68, 2.73], isolates *e*, excludes 3 and π.
- **domain-specific world** (each domain lawful, values differ) → **rung 1**,
  I² ≈ 1.0 — correctly *not* called universal.
- **trivial world** (domains = their mechanism-free null) → **rung 0**,
  flagged as indistinguishable from the null.
- **discover→confirm** on the universal world (two domains sealed) → discovery
  rung 3 confirmed on the holdout, CIs overlap.

This is a proof of the *instrument*, not a finding about real systems. It shows
the engine can tell "one law" from "many laws" from "no law" — which is the
prerequisite for trusting it on real data.

## Running

```bash
pip install numpy scipy matplotlib pytest
python run.py
pytest tests/ -q
```

## Using it on a real domain

Supply `{domain_name: array_of_ratio_measurements}` plus, per domain, a
`null_sampler(n, rng)` that generates mechanism-free baselines for that domain
(e.g. random river topology for rivers). Run `ladder.assess(...)`. To respect
the discover→confirm discipline, seal one or more domains with `ladder.split`
and only `ladder.confirm` against them after the discovery verdict is fixed.
