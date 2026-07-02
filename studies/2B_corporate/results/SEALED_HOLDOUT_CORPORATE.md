# Corporate — cross-domain holdout  [SPENT 2026-06-27 — prediction B run once]

> **STATUS: confirmation complete. The cross-domain seal is now SPENT.**
> The discovery claim was frozen first (`preregistration/FROZEN_DISCOVERY_CLAIM.md`),
> then corporate split factors were ingested from real SEC EDGAR data and
> `confirm_corporate.py` was run **once**. Corporate can no longer serve as a
> clean cross-domain confirmation set.

## What was held out
`FROZEN_DISCOVERY_CLAIM.md` prediction **B** named the cross-domain holdout as
**corporate (2B) + open-source (2F)** — two domains carrying no real data during
discovery. The discovery verdict (rivers + biology + controls + DGS) was frozen
as **rung 1 (domain-specific laws)**, pooled ratio ~3.16, CI ≈ [2.97, 3.37],
I² ≈ 0.98, pooled CI excluding *e*.

## Pre-registration amendment (logged here, before deposit)
**2F open-source is descoped from the holdout** and prediction B is run on
**corporate alone**. Rationale: a faithful, defensible 2F real ingest was found
to require either a long GH-Archive accumulation (fork-event data is dominated by
automated fork-spam and carries no lifetime star counts) or the rate-limited
GitHub REST API behind a token; that work is **deferred** (the real-ingest code
is committed in `studies/2F_opensource/ingest_github.py` for a later run). A
single-domain cross-domain holdout is a **weaker** test than the registered
two-domain holdout — it is reported as such. This is a conservative change (it
reduces the test's power; it does not make B easier to pass).

## Observable (real, SEC EDGAR — disjoint from discovery)
`ingest_edgar.py` → `results/corporate_splits_edgar.json`:
- **570** initial Form 10-12B SpinCo registrations (2001–2024) → **341** parent
  firms parsed from information statements → **108** split events with a parsed
  parent reportable-segment count.
- Split factor = **E / S × 3** (resulting viable entities per internal division;
  a comparable ratio, never a raw count). E = 1 + spun-off SpinCos; S = parent
  reportable segments from its 10-K.
- Real events recovered include Abbott→AbbVie+Hospira, Danaher→Fortive+Veralto,
  Cendant→Wyndham+Realogy, Dover→Knowles+Apergy, Air Products→Versum.
- Distribution: geom factor **2.24**, CV **0.31**, n=108; **99 binary** (E=2) and
  **9 multi-way** (E=3) splits.
- Mechanism-free **binary-default null**: firms split in two relative to their
  *real* segment structure (E≈2, S resampled from the observed pool).

## Result of prediction B (run once, `results/confirm_B_corporate.json`)

| test | claim | verdict |
|------|-------|---------|
| **B1** | corporate is a definable distribution, **not pure null** | **FAIL** |
| **B2** | adding corporate keeps rung 1 / **isolates no constant** | **PASS** |
| **B overall** | B1 ∧ B2 | **NOT confirmed** |

- **B1 FAIL.** Corporate is a well-defined distribution (n=108, geom 2.24,
  CV 0.31), but it is **statistically indistinguishable from its mechanism-free
  binary-default null** (per-domain z = **−1.21**, pooled-displacement
  p = **0.23**). Under the triviality doctrine (PREREGISTRATION §3) this **demotes
  corporate to rung 0 (trivial)**: corporate splitting is explained by the mundane
  "split in two" baseline and shows **no lawful subdivision above the null**. (The
  z is mildly negative — observed sits just *below* the binary null, because E is
  almost always 2.)
- **B2 PASS.** Adding corporate to the real discovery domains keeps the verdict at
  **rung 1**: I² = **0.98** (stays high), pooled CI **[3.01, 3.46]** isolates no
  single principled constant (only π is in-CI; *e* excluded). Corporate sits as a
  **low outlier (2.24)**, well below the lawful ~3.3–3.7 band, and does **not**
  collapse the verdict to universality or a named constant.
- The corporate holdout CI does **not** overlap the real discovery band
  (rivers + biology pooled ≈ 3.38, CI [3.19, 3.59]) — corporate is below it.

## What this means (symmetric reporting, PREREGISTRATION §8.7)
The cross-domain holdout does **not** extend the lawful-subdivision finding to a
new domain: corporate fragmentation is a trivial (binary-default) process, not a
lawful one. But the **substantive pre-registered prediction holds** — adding a new
real cross-domain node does **not** manufacture universality or a named constant;
the program's verdict remains **rung 1 (domain-specific laws), no theorem of a
universal constant.** The negative B1 and the positive B2 are reported with equal
prominence. The ladder rung the evidence earns is **1, and no higher.**
