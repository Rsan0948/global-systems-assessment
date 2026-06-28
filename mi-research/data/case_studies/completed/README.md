# completed/ — structured case records (read the counting caveat before quoting any rate)

25 machine-readable case records: the 20-case baseline (`case01`–`case20`,
transcribed from `live/runs/run1`–`run5`) plus the 5 expansion cases
(`case21`–`case25`, Batch 1).

## Report the clean rate as a RANGE, not a single number.

`python scripts/run_retrodiction.py --validate data/case_studies/completed/`
prints a per-letter tally — it counts the a–h prediction slots, excludes
`NOT_APPLICABLE`, and labels each by its committed `result`. The faithful (generous)
transcription of each run's §6 labels lands that tally near ~90%, **above** the
framework's honestly-documented accuracy. The records therefore carry the **run6
strict re-code** (see below), after which the tally lands at the canonical best
estimate **~78% clean / 100% directional** (114C/33P/0F across 25 cases). Always
report the **range**, never a single triumphant number.

## Strict re-code applied (per run6)
Two downgrades, exactly as run6's §3–4 prescribe, annotated in each affected record's
`verification[*].explanation` and flagged in `analysis.strict_recode_note`:
1. **Post-hoc "primary dimension" (`d_failure_dimension`) CONFIRMED → PARTIAL** — run6
   §3(d): identifying the "primary" failure/success dimension post hoc invites
   confirmation bias.
2. **Mod4 narrow-gap `a_trajectory` annotated "too close to call"** for the three
   within-margin pairs (Sudan/South Sudan, Pakistan/Bangladesh, Ethiopia/Eritrea);
   those were already coded PARTIAL by the faithful transcription.

**The honest figure (canonical, from `live/runs/run6of6_definitive_synthesis_20cases.md`):**
- **Clean confirmation: ~62% (strict) – 85% (generous), best ~78%** for LIVE (STATIC ~73%).
- **Directional: ~100%** (zero falsifications — partly by construction; directional
  claims are hard to falsify).
- ~130 discrete predictions across the 20 baseline cases.

## Why a *faithful* transcription alone over-states (and what the re-code fixes)

Run 6's "honesty note on counting" explains why the raw per-letter labels round up:
- **Only Run 2 was rigorously counted** (25 predictions, 21C/4P/0F = 84%). Runs 1, 3,
  4, 5 were summarized qualitatively, and **qualitative runs round up**. (Reassuringly,
  `case05`–`case08` reproduce Run 2's audited 21C/4P/0F exactly.)
- The honest ~78% is an **aggregate-level** discipline layered on top — chiefly the
  two strict-coding downgrades above, plus awareness of double-counting (one datum,
  e.g. a single P1 gap, can spawn several per-letter "predictions").

After applying the strict re-code, the per-letter tally itself lands at **78%**
(114C/33P/0F), matching run6's best estimate — so the records now carry the discipline
rather than relying on a footnote. Still: report the **range** (62–85%), and remember
the capacity construct is partly redundant with WGI standalone and the zero-falsification
record is partly by construction.

## Batch 1 (cases 21–25)
Inputs sourced from the committed `mi_pipeline/` panel (commit 9487dd0) for cross-project
consistency; panel grid to 2024. The batch writeup reports **~75% clean** (in-range) with
0 falsifications and the Rwanda reversal-risk prediction logged as **open/prospective**
(not counted as a closed confirmation). See `live/runs/run7_expansion_batch1_cases21-25.md`.
