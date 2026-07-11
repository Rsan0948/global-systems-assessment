# Variance Compression & Conflict-Type Shift — Results

**Companion to** `VARIANCE_COMPRESSION_PREREGISTRATION.md` (sha256 `396e159…`, frozen
before analysis). Artifacts `data/robustness/varcomp/`; code
`scripts/robustness/varcomp_{A,B}.py`. Diagnosis only — **no MI modifications.**

> **Verdict.** The last two Finding-9 residuals: **Candidate A (variance compression)
> FAILS at its gate** — institutional-quality variance has *not* compressed. **Candidate
> B (conflict-type shift) passes its gate but does not carry the erosion** — the
> composition shift is real yet cannot explain the pre-1946 bulk and shows no strong
> intact governance-failure signal. **But the pre-registered A-decomposition delivers
> the most affirmative result in the entire fourteen-test program: the domestic
> "erosion" is not institutions *losing* predictive power — it is wealth *gaining* it.**
> `struct_auc` (institutions→domestic crisis) rose over 150 years; `wealth_auc` rose
> faster (p=0.005). The spread narrowed because **GDP caught up to institutions as a
> predictor of domestic rupture**, not because institutions decayed. This is Finding-9
> residual #1 (wealth as an improving state-capacity proxy) — now the standing lead
> with direct evidence, and the reframing the constraint profile was pointing to.

---

## CANDIDATE A — Variance compression

### A1 (GATE) — institutional-quality variance is NOT declining → FAIL

| measure | 1996/1850 | 2024/2010 | rel. change | trend p |
|---|---|---|---|---|
| modern **P1** SD | 0.170 | 0.173 | **−0.02** (flat/up) | 0.74 |
| V-Dem **rol** SD (1850→2010) | 0.299 | 0.309 | **−0.03** (flat/up) | 0.73 |

Neither the modern institutional-quality index (P1) nor the deep-history V-Dem
rule-of-law shows the variance compression the hypothesis requires. Both are flat-to-
slightly-*rising* across their spans. **The foundational premise is false; A1 fails →
Candidate A stops.** The confirmatory arms agree:
- **A2 sufficiency:** range restriction predicts only **1.9%** of the observed
  signal change (attenuation-predicted decline −0.007 vs actual −0.357).
- **A3 (Thorndike Case II, the definitive test):** with `u = SD_epoch/SD_ref ≈ 1`
  there is nothing to correct — raw and corrected |r| are nearly identical (raw slope
  +0.0010, corrected +0.0009); corrected is **not** flattened relative to raw.
- **A4 structure:** P10/P90 stable — modern P1 [0.30,0.76]→[0.31,0.76]; rol
  [0.07,0.89]→[0.12,0.97], the *top* if anything **rose**. No compression from either
  end.
- **A5:** V-Dem rol SD by decade dips slightly mid-century (0.273 @1960) then returns
  to 0.31 — no long-run decline; consistent with the flat modern P1 window.

### The A-decomposition — the affirmative finding (struct_auc vs wealth_auc)

Decomposing the Finding-12 domestic spread (= `struct_auc − wealth_auc`) into its
components over 1816–1996:

| | 1816 | 1876 | 1946 | 1996 | Δ | trend p |
|---|---|---|---|---|---|---|
| `struct_auc` (institutions→crisis) | 0.444 | 0.847 | 0.565 | 0.754 | **+0.31** | 0.20 (n.s.) |
| `wealth_auc` (GDP→crisis) | 0.222 | 0.771 | 0.520 | 0.779 | **+0.557** | **0.005** |
| spread ("erosion") | +0.222 | +0.076 | +0.046 | −0.025 | −0.247 | — |

**The domestic-channel erosion is wealth-side, not structure-side.** Institutions did
**not** lose their grip on domestic crises — `struct_auc` *rose* (0.44→0.75; if
anything institutions discriminate domestic rupture *better* now). What changed is that
**GDP went from a near-useless predictor of domestic conflict (AUC 0.22 in 1816) to a
co-equal one (0.78 by 1996)** — the only significantly-trending component (p=0.005).
The "institutional signal erosion" is a misnomer: it is the **narrowing of institutions'
*edge* over wealth**, produced by wealth catching up, not by institutions declining.
(Early wealth_auc < 0.5 partly reflects sparse/noisy pre-1866 Maddison GDP; the robust
climb is post-1866, where wealth_auc rises 0.64→0.78 while struct_auc holds 0.55–0.85.)

---

## CANDIDATE B — Secular conflict-type shift

### B1 (GATE) — domestic-conflict composition HAS shifted → PASS

Territory/identity share of domestic (intrastate) conflict onsets, UCDP incompatibility
codes, by decade: 0.32 (1946) → 0.40 → 0.40 → 0.35 → 0.49 → 0.47 → **0.63 (2006)** →
0.58 (2016). Trend slope +0.0040, **p=0.003**, Δ+0.26. The nature of domestic conflict
genuinely shifted from governance-failure toward identity/territorial. **B1 passes.**

### B2 (DISCRIMINATING) — does the signal differ by conflict type? → weak / inconclusive

Erosion spread split by incompatibility (1946–1996, the UCDP-coded window):
- **Government-incompatibility:** mean spread **+0.007**, slope −0.0013 (p=0.43) —
  near-zero and flat, **not** the strong intact governance-failure signal predicted.
- **Territory-incompatibility:** mean spread −0.036, slope +0.0020 (p=0.07).

Government-type only marginally out-spreads territory-type (+0.007 vs −0.036), and
neither is strong: by mid-century wealth already predicts *both* types as well as
institutions do (echoing the A-decomposition — wealth had caught up for all conflict
types). **Decisive limitation:** UCDP incompatibility exists only from 1946, so B is
**blind to the pre-1946 two-thirds of the erosion** (spread 0.222→0.046 by 1946). B
cannot be the primary mechanism.

### B3 — post-colonial conflict-type story → refuted

Territory share by formation: mature **0.556**, post-colonial **0.522**, early-post-
colonial (Latin America) 0.0 (all governance-type). Post-colonial conflict is **not**
disproportionately territory-type — it is comparable to mature. Yet the rol→crisis
signal is far weaker for post-colonial (`struct_auc` **0.577**, r=−0.14) than mature
(**0.714**, r=−0.34). So the weaker post-colonial signal (consistent with F9-A's
mature-state-instrument finding) is **not** explained by conflict-type composition. The
specific "post-colonial identity conflict dilutes the signal" residual does not hold.

**Candidate B verdict: partial at most.** A real composition shift (B1) that may modestly
add to post-1946 domestic dilution, but with no strong intact governance-failure signal
(B2), no post-colonial-type mechanism (B3), and structurally unable to address the
pre-1946 bulk of the erosion.

---

## Synthesis

| test | prediction | result | supports? |
|---|---|---|---|
| A1 P1/rol variance declining | yes | **flat/rising** (p≈0.74) | **No (gate fail)** |
| A2 decline tracks erosion | strong +corr, sufficient | 1.9% explained | **No** |
| A3 range correction recovers signal | corrected flat | corrected ≈ raw | **No** |
| A4 compression structure | bottom rising | P10/P90 stable, top rose | **No** |
| A5 V-Dem long-run variance decline | clear decline | none | **No** |
| B1 conflict composition shifted | territory share rising | +0.26, p=0.003 | **Yes** |
| B2 signal strong for governance type | strong & non-eroding | ≈0, flat; pre-1946 blind | **No** |
| B3 post-colonial disproportionately identity | yes, weaker P1 link | terr-share ≈ mature | **No** |

**Overlap / decomposition.** Candidate A is refuted; Candidate B contributes at most a
modest post-1946 outcome-composition effect (real shift, but no strong governance-signal
to dilute and blind to pre-1946). There is little to decompose between them — the
dominant, statistically-significant, full-span signal is neither A nor B but the
**A-decomposition byproduct: wealth's predictive power over domestic rupture rose**
(`wealth_auc` +0.557, p=0.005) while institutions' held or rose (`struct_auc` +0.31,
n.s.).

## Bottom line — the shape of the answer, after fourteen tests

The two final Finding-9 residuals do not, as pre-registered, explain the erosion:
variance compression is **absent** (A1), and the conflict-type shift, though **real**
(B1), is neither sufficient nor able to reach the pre-1946 curve. But the exercise
resolved the phenomenon's *character*: **the 150-year "erosion of the institutional
signal" is not institutions losing predictive power over domestic political rupture —
`struct_auc` rose. It is GDP *gaining* predictive power (0.22→0.78, p=0.005), catching
up to and slightly overtaking institutions, so their *edge* (the spread) narrowed.**

This is the one Finding-9 residual never given a primary test — "improving GDP
measurement + industrialization making wealth a better proxy for state capacity over
time" — and it is the only candidate that fits the *entire* constraint profile
simultaneously: continuous (industrialization + improving economic statistics are
continuous), domestic-channel (it is a domestic-crisis predictor race), coexisting with
**strengthening P1↔GDP** (F10 — the same convergence viewed from the wealth side),
within mature states, and invisible to every distributional / regime / support /
contagion test because it is a property of the **wealth predictor improving**, not of
institutions changing. It reconciles F10, F11, F12, and F13 in one mechanism.

**It is a lead, not a confirmed result** — it emerges from a pre-registered *decomposition*,
not a hypothesis run as a primary with its own falsification gate. The right next step
is a dedicated pre-registration: does a *revealed* state-capacity/GDP series' rising
discrimination of domestic conflict fully account for the spread narrowing, on a
constant sample, with the wealth-data-quality improvement controlled? Until then the
erosion's cause is **best characterized, not closed**: after fourteen adversarial tests,
the most defensible statement is that *institutions did not weaken — wealth became a
better predictor of the same outcomes,* and the program's headline should shift from
"the institutional signal is eroding" to "the wealth signal caught up."

## Artifacts

- Code: `scripts/robustness/varcomp_A.py`, `varcomp_B.py`
- Data: `data/robustness/varcomp/{candidate_A,candidate_B}.json`
- Pre-registration: `docs/VARIANCE_COMPRESSION_PREREGISTRATION.md` (frozen, sha256 `396e159…`)
