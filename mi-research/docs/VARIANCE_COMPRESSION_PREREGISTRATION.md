# Variance Compression & Conflict-Type Shift — Pre-Registration

**Purpose.** Test the **last two Finding-9 residuals** for the 150-year erosion of the
institutional signal, now constrained by thirteen prior nulls to a mechanism that is
continuous since ~1850, sits in the **domestic** crisis channel (F12), coexists with
**strengthening** P1↔GDP (F10), operates **within mature states** (F9-A), and is
independent of external support (F8), composition (F9), consequence-elimination (F9),
perception-lag (F9), wealth decoupling / reorientation (F10), monetary regimes (F11),
systemic contagion (F12), and inequality (F13).

- **Candidate A — Variance compression.** Institutional-quality scores converged as
  formal-legal institutions diffused globally; a predictor with shrinking range
  mechanically loses predictive power (range restriction) even if the underlying
  relationship is unchanged. Would erode the domestic signal (P1 the predictor) while
  P1↔GDP tightens (GDP range stays wide), continuously, most within mature states — a
  property of the **measurement**, not the relationship.
- **Candidate B — Secular conflict-type shift.** Domestic crises shifted from
  governance-failure (which institutions prevent) to identity/territorial conflict
  (which they don't), so the domestic signal erodes through **outcome composition**
  within the domestic channel — a change in *what domestic crises are*, not whether
  institutions prevent them.

Both can be simultaneously, partially true (A = predictor-side range restriction; B =
outcome-side composition). If both positive, decompose shares and **acknowledge
overlap** (do not sum as independent).

---

## Binding rules

1. **Pre-register before running** (sha256 on commit).
2. **A1 and B1 are gates.** If A1 fails, stop Candidate A; if B1 fails, stop B.
3. **Candidate A uses the standard Thorndike (1949) Case II range-restriction
   correction — not an invented one.** Note the bivariate-normality assumption as a
   limitation.
4. **Candidate B uses UCDP `incompatibility` codes as-is** (1=territory, 2=government,
   3=both) — mechanical, no narrative reclassification.
5. **Report all results,** including partial/overlapping shares and power limits (B's
   incompatibility coding is UCDP-only → effective span 1946–2016; COW intra pre-1946
   has no incompatibility code — disclosed).
6. Diagnosis only — **no MI modifications** proposed from these results.

---

## Data (fixed)

- **Modern P1**: engine pillars on the MI 5-point panel (1996/2004/2012/2018/2024),
  all scored countries per year.
- **Historical institutional proxy = V-Dem rule-of-law** (`rol`, `vdem_longrun.json`;
  202 countries, coverage 107@1850 / 154@1900 / 181@1950). This is the structure
  signal of the Finding-7/12 curve — coherent with the erosion being explained.
- **Domestic-crisis outcome = Finding-12 domestic-origin classification** (COW intra +
  UCDP type 3/4). Panel/curve machinery (rol, log Maddison GDP, 25y window, epochs
  1816–1996 step 10) used **unmodified**; the domestic-channel curve already stores
  per-epoch `struct_auc` and `wealth_auc` (`t2_split_curve.json`).
- **Conflict incompatibility (Candidate B)**: UCDP `incompatibility` on intrastate
  (type 3/4) conflicts; onset tagged by its conflict's incompatibility. Government =
  2, territory = 1, both = 3 (reported separately). 1946–2016.
- **Formation classification** (`state_formation.json`) for B3 mature vs post-colonial.

---

## CANDIDATE A — VARIANCE COMPRESSION

### Test A1 — Is institutional-quality variance declining? (GATE)

Modern: SD, IQR, range (max−min), CV of **P1** at each of the 5 MI points (all scored
countries). Historical: same for **V-Dem rol** at decadal epochs 1850–2016 (all
countries with rol). OLS trend of each dispersion measure vs time.
**PASS:** SD (primary) **declines** — negative trend and ≥10% relative decline in SD
across the span (modern or historical). **FAIL:** SD flat/rising → stop Candidate A.
**Structure note (reported):** is the decline bottom-rising (P10 up, diffusion) or
top-falling (P90 down, decay)? (feeds A4).

### Test A2 — Does the variance decline track the erosion, and is it quantitatively sufficient?

On the committed domestic-curve sample per epoch: (i) SD of rol; (ii) the institution→
crisis signal as a point-biserial correlation `r_struct` between rol and domestic-onset
(and cross-check vs stored `struct_auc`). Correlate the SD trajectory with `r_struct`
across epochs. **Sufficiency:** using the range-restriction *attenuation* formula
`r_restricted = r_unrestricted·u / √(1 − r_unrestricted² + r_unrestricted²·u²)` with
`u = SD_epoch / SD_reference`, predict each epoch's attenuated `r_struct` from the
earliest epoch's `r_struct` + observed SD ratio; compare predicted vs actual decline.
**Report %-explained:** ≥80% ⇒ fully mechanical; 30–80% ⇒ major contributor; <30% ⇒
real but insufficient. **Also decompose** whether the *spread* erosion is
`struct_auc`-driven (institutions losing discrimination — consistent with compression)
or `wealth_auc`-driven (wealth gaining — inconsistent).

### Test A3 — Does range-restriction correction recover the signal? (DEFINITIVE)

Thorndike Case II: `r_corrected = r_observed·(1/u) / √(1 − r_observed² + r_observed²·(1/u)²)`
with `u = SD_epoch / SD_reference`, reference = earliest (widest) rol SD. Apply to
`r_struct` at each epoch; compare corrected vs raw trajectories.
**PASS (variance fully explains):** corrected `r_struct` is **flat/stable** (trend not
significantly negative AND |corrected slope| < 0.5·|raw slope|) while raw declines →
erosion is a measurement artifact. **PARTIAL:** corrected declines less than raw but
still declines (compression contributes; report residual share). **FAIL:** corrected
declines ≈ raw. Limitation: Thorndike assumes bivariate normality + linear homoscedastic
relation; noted.

### Test A4 — Internal structure of the compression

P10 and P90 of P1 (modern) and rol (historical) per time point. Bottom-rising
(diffusion, benign) vs top-falling (mature-state decay) vs both. Reported, not pass/fail.

### Test A5 — V-Dem rule-of-law long-run variance

rol SD/IQR/range by decade 1850–2016 (all countries). Clear long-run decline? Overlay
on the F12 domestic erosion; do they track? Consistency check: V-Dem long trajectory vs
WGI/P1 1996–2024 (same process should show in both windows).

---

## CANDIDATE B — SECULAR CONFLICT-TYPE SHIFT

### Test B1 — Has domestic-conflict composition shifted (governance→identity)? (GATE)

Domestic (intrastate, UCDP type 3/4) onsets by incompatibility: government (2) vs
territory (1). Share of each per decadal epoch 1946–2016. OLS trend of territory share.
**PASS:** territory/identity share **rises** over the span (positive trend, material).
**FAIL:** composition flat → stop Candidate B.

### Test B2 — Does the institutional signal differ by conflict type? (DISCRIMINATING)

Split the domestic erosion curve by incompatibility: recompute `struct_auc`/spread for
**government-incompatibility** onsets vs **territory-incompatibility** onsets per epoch
(1946+; label = onset of that type in window). **Support:** signal **strong &
non-eroding** for government-incompatibility (institutions predict governance-failure at
historical strength) and **weak/absent** for territory-incompatibility; aggregate
erosion driven by rising territory share. **Null:** both types erode similarly.

### Test B3 — Post-colonial civil conflict specifically

Using formation classes: is the P1/rol↔domestic-crisis link weaker for **post-colonial**
civil conflict than **mature**? Are post-colonial domestic conflicts disproportionately
**territory/identity** type? Is the post-colonial share of the total domestic-conflict
pool (and of territory-type) rising? **Support:** post-colonial conflicts skew
territory-type, weaker P1 link, rising pool weight — a crisis type never in the signal's
domain growing heavier. (Distinct from F9-A: not whether young states dilute the
mature-state signal — they don't — but whether the *type* they contribute erodes the
*aggregate* domestic signal.)

---

## Synthesis (frozen)

Table A1–A5, B1–B3 (measure / prediction / result / supports?). Verdict:
- **A3 corrected-flat AND B2 government-signal-intact** → the erosion is **not
  substantive**: predictor-range compressed (A) + outcome pool shifted to
  identity/territorial crises outside the signal's domain (B). Strip both ⇒ the ancient
  institution→governance-failure relationship stands at full strength. *The measurement
  got harder to read; the world did not get harder to predict.*
- **A partial / B partial** → decompose shares, acknowledge overlap (post-colonial
  identity conflicts may also sit in compressed-P1 countries); report residual.
- **Both fail** → the erosion survives all fourteen tested mechanisms; document as the
  program's precisely-bounded open question.

Artifacts `data/robustness/varcomp/`; code `scripts/robustness/varcomp_*.py`; narrative
`docs/VARIANCE_COMPRESSION_RESULTS.md` + Finding 14 of `docs/ROBUSTNESS_RESULTS.md`.
