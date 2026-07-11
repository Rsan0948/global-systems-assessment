# Crisis-Origin Shift (Domestic → Systemic Contagion) — Results

**Companion to** `CONTAGION_PREREGISTRATION.md` (sha256 `068e2c5…`, frozen before
analysis). Artifacts `data/robustness/contagion/`; code
`scripts/robustness/contagion_{classify,t2_gate}.py`. Diagnosis only — **no framework
changes.**

> **Verdict: FAILS AT THE GATE (Test 2) — and reverses. Registered null, the 12th.**
> The erosion is **not** concentrated in external-origin crises with a preserved
> domestic signal. The **opposite** holds: the erosion lives **entirely in the
> domestic-origin channel** (slope −0.00122, r=−0.79, p<0.001), while the
> external-origin signal was **always flat** (slope −0.00006, p=0.76). The
> institutional signal has genuinely weakened for **exactly the crises institutions
> should predict best** — domestic political rupture. Per the pre-registered stop
> rule, **Tests 3–6 were not run.** This does not resolve the Finding-10-vs-7/11
> contradiction; it **sharpens** it.

---

## Test 1 — Crisis-origin classification (foundation) — validated

Onsets re-derived with a domestic/external origin tag from the raw sources (UCDP/PRIO
v24.1 type codes + COW Inter/Intra), using the **committed inclusion logic**. The
union **reproduces the Finding-7 baseline exactly**: 1176/1176 onset pairs, **0
missing, 0 extra**. Split: **798 domestic, 426 external, 48 both**. Scheme (frozen):
DOMESTIC = COW intra + UCDP type 3/4; EXTERNAL = COW inter + UCDP type 1/2. The
"all-crises" curve below reproduces the committed slope −0.001056 to the digit,
confirming the split is faithful.

## Test 2 (THE GATE) — Split erosion curve by crisis origin — REVERSED

Spread (structure_AUC − wealth_AUC) per epoch, 1816–1996, recomputed on the committed
curve machinery (V-Dem rule-of-law, log Maddison GDP, 25y window):

| curve | 1816 | 1906 | 1966 | 1996 | slope | Pearson r | p | Δ |
|---|---|---|---|---|---|---|---|---|
| **all crises** (repro F7) | 0.222 | 0.137 | 0.031 | −0.020 | −0.001056 | −0.823 | <0.001 | −0.242 |
| **domestic-origin only** | 0.222 | 0.121 | −0.008 | −0.025 | **−0.00122** | −0.787 | <0.001 | −0.247 |
| **external-origin only** | −0.050 | 0.079 | 0.044 | 0.051 | **−0.00006** | −0.074 | **0.76** | +0.101 |

**Every arm is the reverse of the prediction:**
- **Domestic-origin erosion is NOT flat — it is the whole erosion.** The domestic
  curve erodes as strongly as (marginally *more* than) the aggregate, from +0.222 to
  −0.025, highly significant. The institutional signal for *domestic* political
  failure has genuinely and fully weakened.
- **External-origin erosion is NOT steep — it is flat** (slope ≈ 0, p=0.76), and at a
  **lower level throughout** (mean spread 0.058 vs domestic 0.099). Structure never
  strongly out-predicted wealth for external crises (institutions don't determine
  whether you are invaded), and that weak signal has no trend.
- **Robust to both frozen sensitivity flips:** S1 (type-4 internationalized →
  external) domestic slope −0.00108 / external −0.00035; S2 (type-1 extrasystemic
  excluded) domestic −0.00122 / external −0.00004. The domestic-erodes-more,
  external-flat pattern holds in every variant.

**Gate = FAIL (domestic erodes more than external).** The pre-registered fail
condition — "domestic erodes *more* than external" — is met directly.

**External-origin share of onsets is hump-shaped, not rising.** By epoch: 0.10 (1816)
→ 0.66 (1926 peak) → **0.145 (1996)**. Interstate war peaked around the World Wars and
**declined** afterward as intrastate/civil conflict came to dominate — the
well-documented modern shift. So prediction (iii) also fails: in the modern era crises
became **more domestic**, not more external. The premise that a rising external share
mechanically dilutes the aggregate signal is empirically backwards for the modern
period.

**Power caveat (disclosed).** The earliest external epochs (1816: external share 0.10;
1826: 0.28) have few external onsets and noisy spreads (1816 external = −0.05). But the
verdict is driven by the **high-powered domestic result** (r=−0.79, p<0.001), which is
unambiguous; low external power cannot rescue a hypothesis that required the *domestic*
curve to be flat.

---

## Tests 3–6 — NOT RUN (pre-registered stop rule)

The pre-registration (rule 2) and the Test-2 interpretation guide are explicit: *"Test
2 is the gate. If it fails, stop and report."* The gate failed by reversal. Running
interconnection correlation (T3), gate-false-negatives-by-origin (T4), the
systemic-exposure control regression (T5), or the external-share decomposition (T6)
would be characterizing a mechanism the gate just falsified. They are not run.

---

## Reconciliation with Findings 10 & 11 (mandatory) — the contradiction sharpens

The motivating puzzle was: institutions predict **wealth** better over time (Finding
10, P1↔GDP 0.77→0.82) yet predict **political outcomes** worse (Findings 7/11). This
hypothesis proposed that the political-outcome erosion is an artifact of the *outcome
mix* shifting to external shocks, leaving the true domestic signal intact. **The data
refutes that comfort:** the political-outcome erosion is specifically in the
**domestic** channel. So the sharpened, harder puzzle is now:

> Institutional quality predicts a country's **wealth** better than ever, and its
> **own domestically-generated political rupture** worse than ever — at the same time,
> both accelerating.

This rules out the "scope-boundary" escape (the reassuring reading of Finding 5 that
the MI just can't see exogenous shocks). Whatever is happening, it is degrading the
institution → domestic-stability link itself, not merely diluting it with external
noise. Consistent with Findings 10/11 (nothing here contradicts them); fatal to the
contagion explanation.

---

## Bottom line

The **twelfth** hypothesis to fail on the longitudinal erosion, and the most
informative failure so far because it **localizes** the erosion: not composition (9-A),
not consequence-elimination (9-B), not perception-lag (9-C), not external support
(Finding 8), not wealth-institution decoupling (Finding 10), not monetary-regime
substitution (Finding 11), and **not crisis-origin shift** (Finding 12). The erosion is
**real, smooth, monotone, and specifically in the domestic-political-rupture channel.**

The surviving constraint set is now tight: the driver operates **continuously** (F11:
no regime structure), affects the **domestic** institution→stability link specifically
(F12), and coexists with a **strengthening** institution→wealth link (F10). The two
candidate residuals still standing from Finding 9 that fit this profile are (i)
**measurement-regime maturation / V-Dem rule-of-law variance-compression** as
formal-legal institutions diffused (a smooth, monotone measurement process that would
compress the rule-of-law discrimination for domestic conflict while GDP-based wealth
data simultaneously improved), and (ii) a genuine secular change in how domestic civil
conflict relates to measured rule-of-law in the post-colonial era (both low
institutions and low wealth predict civil war once the sample fills with young poor
states, shrinking structure's *edge* over wealth). Neither is tested here; both are the
right shape and are flagged for separate pre-registration.

## Artifacts

- Code: `scripts/robustness/contagion_classify.py`, `contagion_t2_gate.py`
- Data: `data/robustness/contagion/{crisis_classification,t2_split_curve}.json`
- Pre-registration: `docs/CONTAGION_PREREGISTRATION.md` (frozen, sha256 `068e2c5…`)
