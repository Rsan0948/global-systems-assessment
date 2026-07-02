# Golden-age theory — granular, 1996→2024, at 1/3/5/7/10-year horizons

**Date:** 2026-06-28. **Prompt:** explore the golden-age (real-ascent) signal from ~1994 onward with
the same 1/3/5/7/10-year granularity used for crises. **Data note:** WGI (the institutional series)
begins **1996** — pre-1996 would need a different, non-comparable source, so this runs **1996→2024**
on annual WGI for **91 countries**. Golden age = sustained ascent of **P1** (institutional quality =
mean of GE/RL/RQ/CC). **EXPLORATORY/descriptive** — structure, not a validated predictor.

## Leaderboard — the real golden ages (P1 rise, earliest→peak)
| country | ΔP1 | path |
|---|---|---|
| **Georgia** | +0.354 | 0.30 (1996) → 0.65 (2016) — the singular case |
| **Rwanda** | +0.299 | 0.30 → 0.59 (2023) |
| Kazakhstan | +0.206 | 0.31 → 0.52 |
| Latvia | +0.181 | 0.52 → 0.70 |
| Serbia / Croatia / Estonia / Lithuania | +0.15–0.18 | post-Soviet/Balkan/EU-accession |
| Saudi Arabia | +0.153 | (windfall-adjacent; institutions did rise) |
| Uzbekistan | +0.152 | 0.28 → 0.43 (recent reform) |

Post-Soviet/Balkan reformers + Rwanda dominate. (Note: the *income*-led "golden ages" from the
panel — Iraq, Kuwait, UAE — do **not** appear here; this is the institutional ascent, not the windfall.)

## Finding 1 — golden ages are a 5–10-year phenomenon (mirror of the crisis lead-time)
Rolling ΔP1 across all countries/start-years:
| horizon | SD (annual noise) | p90 rise | % windows that are ascents (>0.05) | big ascents (>0.10) |
|---|---|---|---|---|
| 1y | **0.014** | 0.016 | 1% | 0% |
| 3y | 0.026 | 0.034 | 4% | 0% |
| 5y | 0.034 | 0.046 | 9% | 1% |
| 7y | 0.042 | 0.056 | 12% | 2% |
| 10y | 0.052 | 0.069 | **18%** | **4%** |

**At 1 year, institutional movement is essentially noise** (SD 0.014; only 1% of 1-yr windows are
ascents). A real golden age (ΔP1 > 0.10) **basically only appears in 10-year windows**. So just as
crises emerge late, **golden ages accumulate slowly — you cannot confirm one before ~5–7 years.**
Detection threshold: a move must clear ~2× annual noise (>0.03), which only happens at 5y+.

## Finding 2 — weak persistence (a faint flywheel, not a strong one)
corr(past-h ΔP1, next-h ΔP1): 1y +0.07, **3y +0.14, 5y +0.15, 7y +0.15**, 10y +0.13. Once an ascent is
~3–7 years underway there is a *weak* tendency to continue (r≈0.15, ~2% of variance) — more than the
coarse-grid zero, but still faint. Golden ages do **not** strongly self-sustain; momentum is real but small.

## Finding 3 — institutions and income are COUPLED, not causally ordered
| horizon | ΔP1 → next ΔlnGDP | ΔlnGDP → next ΔP1 |
|---|---|---|
| 3y | +0.12 | +0.15 |
| 5y | +0.14 | +0.13 |
| 7y | +0.14 | +0.13 |

Neither clearly leads — they **co-move** (~0.13 both ways), with income *marginally* leading
institutions at 3y. The romantic "good institutions → growth" precedence is **not** in the data;
golden ages are institutions and income rising together.

## Finding 4 — two shapes of golden age, signalled by the leading component
Year-by-year anatomy of the top episodes (P1 ascent slices from the start year):
| country | start | lead component | 1y | 3y | 5y | 7y | 10y | shape |
|---|---|---|---|---|---|---|---|---|
| **Georgia** | 2003 | **CC** (anti-corruption) +0.38 | **+0.09** | +0.16 | +0.19 | +0.22 | +0.26 | **punctuated reform-shock** |
| **Rwanda** | 2000 | **GE** (state effectiveness) +0.33 | – | +0.04 | +0.10 | +0.15 | +0.20 | **gradual developmental** |
| Estonia | 1996 | CC +0.24 | – | – | – | +0.07 | +0.11 | slow (high base) |
| Kazakhstan | 2000 | GE +0.24 | – | +0.00 | +0.04 | +0.04 | +0.06 | narrow (GE only) |
| Croatia | 2000 | RQ (regulatory/EU) +0.11 | – | +0.04 | +0.05 | +0.04 | +0.04 | EU-convergence, modest |

- **Punctuated reform-shock** (Georgia): a big *early* jump (1y +0.09, far above the 0.014 noise floor),
  led by **control of corruption** — the only kind detectable at 1–3 years. Rare.
- **Gradual developmental** (Rwanda): a steady decade climb led by **government effectiveness**, invisible
  before ~5y.
- **The leading WGI component flags the entry point:** CC = anti-corruption reform burst; GE =
  state-building; RQ = EU/regulatory convergence.

## What this says (honest)
- **Golden ages are slow and late-confirming (5–10y), weakly self-sustaining (~0.15), and coupled to
  income rather than causing it.** The only early-detectable kind is a **CC-led punctuated reform shock**
  (Georgia); gradual developmental ascents (Rwanda) need 5–7 years to clear noise.
- **Candidate early-signature (exploratory):** a control-of-corruption jump > ~0.05 in 1–2 years, or a
  sustained P1 rise clearing 2× annual noise (>0.03) over ≥5y. The leading component types the ascent.
- Caveats: 1996 floor (no pre-1996); P1 only (income/stability ascents are a separate story —
  windfall vs real, see `movement_signal_exploration.md`); descriptive, no outcome attached; the
  persistence and lead-lag correlations are weak (~0.15) — suggestive, not strong.
