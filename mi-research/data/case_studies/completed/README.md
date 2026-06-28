# completed/ — structured case records (read the counting caveat before quoting any rate)

25 machine-readable case records: the 20-case baseline (`case01`–`case20`,
transcribed from `live/runs/run1`–`run5`) plus the 5 expansion cases
(`case21`–`case25`, Batch 1).

## ⚠ The naive `--validate` clean rate OVER-states the framework. Do not headline it.

`python scripts/run_retrodiction.py --validate data/case_studies/completed/`
prints a **naive per-letter tally** — it counts the a–h prediction slots,
excludes `NOT_APPLICABLE`, and labels each by its committed `result`. That count
currently lands around **~90% clean / 100% directional**, which is **higher than
the framework's honestly-documented accuracy** and must NOT be quoted as the result.

**The honest figure (canonical, from `live/runs/run6of6_definitive_synthesis_20cases.md`):**
- **Clean confirmation: ~62% (strict) – 85% (generous), best ~78%** for LIVE (STATIC ~73%).
- **Directional: ~100%** (zero falsifications — partly by construction; directional
  claims are hard to falsify).
- ~130 discrete predictions across the 20 baseline cases.

## Why the naive count is too high

Run 6 spells this out (its "honesty note on counting" and "caveat on aggregation effects"):

1. **Only Run 2 was rigorously counted** (25 predictions, 21C/4P/0F = 84%). Runs 1,
   3, 4, 5 were summarized qualitatively, and **qualitative runs round up** — which
   is exactly why 11 of these 25 records show a 100%-clean per-letter tally.
   (Reassuringly, `case05`–`case08` reproduce Run 2's audited 21C/4P/0F exactly.)
2. **Strict coding downgrades** the per-letter labels: post-hoc "primary dimension"
   calls (`d_*`) invite confirmation bias and should be PARTIAL under strict standards.
3. **Mod4 narrow-gap conversions**: where the P1 gap is within the margin of error
   (Pakistan/Bangladesh, Ethiopia/Eritrea, Sudan/South Sudan), a directional call is
   "too close to call", not a confirmation.
4. **Double-counting**: a single datum (e.g. one P1 gap) can spawn several per-letter
   "predictions", inflating the denominator's clean share.

The per-letter `result` fields are faithful to each run's own §6 codings (the
*generous* reading). The honest ~78% is an **aggregate-level** adjustment layered on
top — it is NOT recoverable by naively counting letters. Always report the **range**,
never the single naive number (project rule: "report as a range, never a triumphant number").

## Batch 1 (cases 21–25)
Scored on real 2025-anchored data; the batch writeup reports **~75% clean** (in-range)
with 0 falsifications and the Rwanda reversal-risk prediction logged as **open/prospective**
(not counted as a closed confirmation). See `live/runs/run7_expansion_batch1_cases21-25.md`.
