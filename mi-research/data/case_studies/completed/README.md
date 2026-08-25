# completed/ - structured case records

> These 84 modern records are hindsight-retrodictive. The outcomes were
> known during selection, scoring, or calibration. They are useful for
> reproducibility and internal consistency, but they are not blind
> validation. See `../../../docs/CLAIMS_LEDGER.md`.

**84-case modern historical corpus, three classes (`--validate` scores them separately):**
- **51 P1-ordinality cases** (`case01`–`case51`): the retrodiction baseline (213C/77P/0F).
- **19 durability-gate / Safeguard-J test cases** (`sig01`–`sig19`, `stress_type=durability_gate_test`):
  the N=19 acute-signature set; each tests whether Safeguard J (P4−P1 gap) correctly predicts
  crisis vs absorption (17/19 correct, 89%). NOT P1-ordinality cases - see
  `docs/signature_validation_N21.md` + `docs/architectural_decisions/v3_1_durability_gate.md`.
- **14 rule-validation A/B cases** (`rv01`–`rv14`): blind convergence-qualifier and accountability-gap
  tests. 8 confirmed / 2 indeterminate / 2 falsified / 2 pre-WGI N/A. See
  `docs/c_cases_blind_validation.md`.

Additionally, `../ancient/ancient_cases.json` contains **25 pre-modern cases** (c. 2686 BCE – 1797 CE),
firewalled at lowest confidence. Historical corpus: **109 case studies** (84 modern hindsight-retrodictive + 25 ancient interpretive). The 67 blind out-of-sample observations are separate.

The 51 ordinality cases: the 20-case baseline (`case01`–`case20`, from `live/runs/run1`–`run5`),
Batch 1 (`case21`–`case25`), and Batches 2–6 (`case26`–`case51`).

## Report the clean rate as a RANGE, not a single number.

`python scripts/run_retrodiction.py --validate data/case_studies/completed/`
prints a per-letter tally - it counts the a–h prediction slots, excludes
`NOT_APPLICABLE`, and labels each by its committed `result`. The faithful (generous)
transcription of each run's §6 labels lands that tally near ~90%, **above** the
framework's honestly-documented accuracy. The records therefore carry the **run6
strict re-code** (see below), after which the tally lands at the canonical best
historical coding estimate **about 78% clean, with no recorded directional falsifications** (114C/33P/0F across 25 cases). Always
report the **range**, never a single triumphant number.

## Strict re-code applied (per run6)
Two downgrades, exactly as run6's §3–4 prescribe, annotated in each affected record's
`verification[*].explanation` and flagged in `analysis.strict_recode_note`:
1. **Post-hoc "primary dimension" (`d_failure_dimension`) CONFIRMED → PARTIAL** - run6
   §3(d): identifying the "primary" failure/success dimension post hoc invites
   confirmation bias.
2. **Mod4 narrow-gap `a_trajectory` annotated "too close to call"** for the three
   within-margin pairs (Sudan/South Sudan, Pakistan/Bangladesh, Ethiopia/Eritrea);
   those were already coded PARTIAL by the faithful transcription.

**The honest figure (canonical, from `live/runs/run6of6_definitive_synthesis_20cases.md`):**
- **Clean confirmation: ~62% (strict) – 85% (generous), best ~78%** for LIVE (STATIC ~73%).
- **Directional: ~100%** (zero falsifications - partly by construction; directional
  claims are hard to falsify).
- ~130 discrete predictions across the 20 baseline cases.

## Why a *faithful* transcription alone over-states (and what the re-code fixes)

Run 6's "honesty note on counting" explains why the raw per-letter labels round up:
- **Only Run 2 was rigorously counted** (25 predictions, 21C/4P/0F = 84%). Runs 1, 3,
  4, 5 were summarized qualitatively, and **qualitative runs round up**. (Reassuringly,
  `case05`–`case08` reproduce Run 2's audited 21C/4P/0F exactly.)
- The honest ~78% is an **aggregate-level** discipline layered on top - chiefly the
  two strict-coding downgrades above, plus awareness of double-counting (one datum,
  e.g. a single P1 gap, can spawn several per-letter "predictions").

After applying the strict re-code, the per-letter tally itself lands at **78%**
(114C/33P/0F), matching run6's best estimate - so the records now carry the discipline
rather than relying on a footnote. Still: report the **range** (62–85%), and remember
the capacity construct is partly redundant with WGI standalone and the zero-falsification
record is partly by construction.

## Phase 3 rebuild - MI v1, reference-based, auto-derived verification (2026-06-28)
All 25 records were migrated to the two-layer architecture:
- **No embedded indicator copies.** Each entity stores `country_ref` + `pre_year`/`post_year`;
  indicators are resolved live via `mi.datasource` at score time (`post_event.resolved_scores`
  caches the computed pre/post P1 & MI for transparency).
- **Predictions stay locked**; **mechanical verdicts auto-derived** from the re-scored real
  data - `a_trajectory` (full P1-ordering vs post-MI, Mod4-gated) and `c_convergence`
  (MI-range over time, material-change-gated). `b/d/e/f/g/h` preserved as judgment.
- Data-limited cases (Sudan/S.Sudan, Serbia/Kosovo, Indonesia/E.Timor pre-event; Germany
  pre-WGI) are **not** auto-derived (an entity lacks a complete pre-event MI) - judgment
  preserved, limitation flagged.

**Re-scoring on real data moved 5 verdicts** (all CONFIRMED→PARTIAL; **zero new falsifications**):
| Case | Field | Change | Why |
|---|---|---|---|
| 03 Czech/Slovakia | a_trajectory | CONFIRMED→PARTIAL | Mod4: pre-P1 gap 0.069 < 0.10 → too close to call |
| 24 DRC/Rwanda | a_trajectory | CONFIRMED→PARTIAL | Mod4: 1996 gap 0.096 < 0.10 → abstain |
| 02 Yugoslavia | a_trajectory | CONFIRMED→PARTIAL | Slovenia top correct, Serbia/Bosnia sub-pair swapped |
| 02 Yugoslavia | c_convergence | CONFIRMED→PARTIAL | predicted divergence; MI-range converged 0.316→0.198 |
| 19 India/Pak/Bang | c_convergence | CONFIRMED→PARTIAL | predicted convergence; MI-range diverged 0.082→0.145 |

Aggregate after the rebuild: **109C / 38P / 0F, about 74% clean in the historical coding** - within the
honest 62–85% band; the drop from ~78% is the cost of honest real-data re-scoring (mostly the
framework correctly abstaining on Mod4 near-ties).

## Judgment-verdict refresh (2026-06-28)
After the Phase-3 mechanical auto-derivation, the **judgment verdicts (b/d/e/f/g/h)** of the 20
baseline cases were individually re-examined against the MI v1 real-data scores:
- **No verdict flips** - the directional/qualitative readings are robust to the legacy→anchored
  vintage change (low-P1 cases still show institutional vulnerability + realized violence;
  high-P1 cases still show management-load, not collapse).
- **`b_violence` risk-levels refreshed** from real pre-P1 (`data_refreshed` field).
- **`d_failure_dimension` augmented** with the real pillar config (`computed_config`): it lists
  the *below-median* pillars as genuine vulnerabilities (e.g. Russia P1+P5 behind high P2/P3/P4;
  Sudan P2/P5/P1/P3) and explicitly says "no binding vulnerability" for high-capacity cases
  (NI/Germany/Belgium) rather than mislabelling a relatively-lowest-but-high pillar.
- **Safeguards re-evaluated** on the real data and attached (`safeguard_state_now`).
- Stale legacy-vintage numbers in evidence superseded by the refreshed values; the substantive
  outcome judgments (real-world events) are preserved.

Caveat: `d_failure_dimension` is **not** purely mechanical - the numeric-lowest pillar is only a
*vulnerability* when actually low; interpreting "primary failure dimension" needs judgment, which
is why d is augmented (not overwritten) and kept PARTIAL under the run6 strict-coding.

## Batch 1 (cases 21–25)
Inputs sourced from the committed `mi-pipeline/` panel (commit 9487dd0) for cross-project
consistency; panel grid to 2024. The batch writeup reports **~75% clean** (in-range) with
0 falsifications and the Rwanda reversal-risk prediction logged as **open/prospective**
(not counted as a closed confirmation). See `live/runs/run7_expansion_batch1_cases21-25.md`.
