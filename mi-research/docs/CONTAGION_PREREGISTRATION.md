# Crisis-Origin Shift (Domestic → Systemic Contagion) — Pre-Registration

**Purpose.** Test whether the ~150-year erosion of the institutional signal
(Findings 2/7; the 19-point curve of Finding 9-B1; steepest & only-significant in the
post-1971 fiat era, Finding 11) is explained by the **source of political instability
shifting from domestic-endogenous causes to exogenous-systemic ones** — and whether
the institutional signal **remains at full ancient strength for domestically-
originated crises**.

**The contradiction this resolves.** Institutional quality is becoming *more*
predictive of wealth (Finding 10: P1↔GDP r 0.770→0.818) and *less* predictive of
political outcomes (Findings 7/11), simultaneously and accelerating. No mechanism
that weakens the institution→outcome link *in general* can also strengthen the
institution→wealth link. Something is **specifically severing institution→political-
stability while preserving institution→economics.** Candidate: the *outcome variable*
changed — an increasing share of "crises" are **transmitted shocks** (financial
contagion, interstate war, commodity/sanction/pandemic shocks) that overwhelm domestic
institutions regardless of quality. Institutions determine whether *your* governance
produces stability; they cannot determine whether a crisis originating *elsewhere*
reaches you. (This is Finding-9 candidate-residual #2 — "the conflict outcome changing
character" — now formally tested, and distinct from all prior nulls: not external
*support* masking weakness [ESI], but external *risk* overwhelming strength.)

**Predictions.** (i) signal stays strong for domestic-origin crises across the full
panel incl. modern; (ii) erosion concentrated in external-origin crises; (iii)
external-origin share rises over time; (iv) its rise tracks the erosion curve; (v)
global-interconnection metrics correlate with the erosion.

---

## Binding rules

1. **Pre-register before running.** This scheme is frozen (sha256 on commit); the
   deterministic classified-event table is committed **before** any split analysis.
2. **Test 2 is the gate.** If the signal erodes *equally* for domestic and external
   crises (or *more* for domestic), the hypothesis fails → report null and **STOP**.
3. **Classification is the hard part.** Primary rule is the conflict **type code**
   (reproducible, no hand-coding); every ambiguous class gets a **sensitivity flip**.
4. **No tuning.** Test 5 systemic-exposure index = equal weights, first pass.
5. **Report all results,** including sub-predictions that fail and power limitations
   where a type is sparse in an epoch.
6. **Reproduce the Finding-7 baseline exactly.** The re-derived "all crises" onset set
   must reproduce the committed `conflict_onsets.json` (143 iso, 1176 events); the
   domestic/external split partitions *that* set. Panel/curve machinery
   (`dense_curve`, V-Dem rule-of-law, log Maddison GDP, 25y window) is used unmodified
   from Findings 7/9.
7. **Consistency with Findings 10 & 11 mandatory;** contradictions flagged.

---

## Test 1 — Crisis-origin classification scheme (FROZEN)

**Universe.** Every conflict onset used in Finding 7 (the committed union: UCDP/PRIO
ACD v24.1 all types + COW Inter-State v4.0 + COW Intra-State v4.1), re-derived with an
origin tag via the *same inclusion logic* as `build_conflict_onsets.py`. Sovereign
defaults (`crag`) enter only for the holdout Tests 4–5.

**Primary classification (by source + type code — no hand-coding):**

| origin | sources / type codes |
|---|---|
| **DOMESTIC-endogenous** | COW **Intra**-State; UCDP `type_of_conflict` **3** (intrastate); UCDP **4** (internationalized intrastate — *primary* origin is domestic; civil war that later drew foreign troops) |
| **EXTERNAL-systemic** | COW **Inter**-State; UCDP `type_of_conflict` **2** (interstate); UCDP **1** (extrasystemic / colonial — external to the domestic institutional system) |

A given (iso, year) onset carries the **set** of origins present (a country can have
both a civil-war onset and an interstate onset in the same window). Window outcome
labels (25y window per the committed curve): **all** = any onset; **domestic** = any
domestic-origin onset; **external** = any external-origin onset. A country whose only
window onset is external gets domestic-label 0, and vice-versa — this is the point
(does P1 predict *domestic* crises?).

**Frozen sensitivity flips** (rule 3), each re-run end-to-end:
- **S1:** UCDP type 4 (internationalized intrastate) → **EXTERNAL** instead of
  domestic.
- **S2:** UCDP type 1 (extrasystemic/colonial) → **excluded** instead of external.
- **S3:** COW inter-state **initiator** (StartYear side that began it, where COW codes
  it) → domestic (aggressive foreign policy is a domestic choice); target/defender →
  external. Reported for the COW-interstate subset only.

**Holdout crises (Tests 4–5).** UCDP onset → classified by the same type rule; `crag`
**sovereign default** → **EXTERNAL** if it falls within 24 months of a documented
systemic financial crisis (Asian 1997, GFC 2008, Euro 2010–12), else **domestic-
fiscal**; frozen crisis-date windows: 1997–1999, 2007–2010, 2010–2013.

**Commit** the full classified table (`crisis_classification.json`: every (iso, year,
origin-set, source, type)) before any split analysis.

---

## Test 2 — Split the erosion curve by crisis origin (THE GATE)

Recompute the dense erosion curve (spread = structure_AUC − wealth_AUC, per epoch,
1816–1996 step 10; structure = V-Dem rule-of-law, wealth = log Maddison GDP) **three
times**: **all** (must reproduce Finding 7), **domestic-only**, **external-only**.
Fit the spread~year trend (Pearson r + OLS slope) for each. Report n and onset counts
per type per epoch (power).

**PASS (frozen):** the **domestic** erosion is materially **flatter/absent** relative
to all-crises — operationally `|slope_domestic| ≤ 0.5·|slope_all|` **and**
`slope_domestic ≥ slope_external` (domestic less negative than external) — i.e. the
signal holds for domestic crises while the aggregate erosion is carried by external
ones. → proceed to Tests 3–6.
**PARTIAL:** domestic flatter than all-crises but external not clearly steeper, or the
pattern holds only in some epochs. → proceed, flagged weak.
**FAIL:** domestic and external erode similarly (both ≈ all-crises), **or** domestic
erodes **more** than external. → report null and **STOP.**

Also compute the **external-origin share** of onsets per epoch (feeds Test 6).

---

## Test 3 — Global interconnection tracks the erosion *(if gate passes)*

Interconnection index per epoch from available proxies (coverage-bounded, disclosed):
global-mean **trade openness** (`NE.TRD.GNFS.ZS`, 1960+) and global-mean **financial
depth** (`FS.AST.PRVT.GD.ZS`, ~1960+); pre-1960 crude proxy = **gold-standard
participation rate** and onset-panel size (documented as weak). Correlate
interconnection level vs institutional-signal spread across epochs. **Support:** strong
**negative** correlation (more connection → weaker signal); check whether the post-1971
capital-mobility jump aligns with the Finding-11 acceleration. **Null:** no
correlation. Limitation: pre-1960 interconnection proxies are crude; correlation is
descriptive, N≈epochs.

## Test 4 — Gate false-negatives are disproportionately external-origin *(if gate passes)*

On the 2004/2012 temporal holdout, classify the gate's **true positives** vs **false
negatives** (crisis occurred) by origin (Test-1 rule). **Support:** external-origin
share **higher among false negatives** than true positives; and gate
accuracy/sensitivity for **domestic-only** crises ≫ **external-only**. **Null:** equal.
Uses the committed holdout crisis definition.

## Test 5 — Does controlling for systemic exposure recover the signal? *(if gate passes)*

**Systemic-exposure index** (equal weights, min-max normalized 0–1; components used
listed honestly given offline data): **resource dependence** (`resource_rents_pct_gdp`,
have), **trade openness** (`NE.TRD.GNFS.ZS`, have), **financial openness proxy**
(`FS.AST.PRVT.GD.ZS`, have), **external-debt exposure** (`DT.DOD.DECT.GN.ZS`, fetch),
**neighbor instability** (region-mean `fsi` as a border-proxy; flagged as a proxy —
true land-border adjacency not built offline). Components genuinely unavailable are
dropped and documented; no synthetic fill.

Logistic (holdout, 2004; crisis primary, dysfunction secondary), predictors
standardized: **M1** neg-P1; **M2** +exposure; **M3** +neg-P1×exposure. **KEY:** does
the neg-P1 coefficient **increase** M1→M2 (signal recovery when external risk is
controlled)? Is exposure a significant crisis predictor? Is the interaction negative
(institutions matter less for highly-exposed states)? Compare AUCs vs GDP-only and
FSI-only, and vs GDP+exposure / FSI+exposure (does exposure help the MI *more* than the
baselines?). **Support:** neg-P1 coef rises with exposure controlled AND exposure is
significant. **Null:** neg-P1 coef flat/falls.

## Test 6 — External-origin share over time + reweighted decomposition *(if gate passes)*

External-origin share per epoch (from Test 2). **Support:** rising share that tracks
the erosion. **Decomposition:** reweight the aggregate erosion holding the
domestic/external onset mix at its earliest-epoch level; if the erosion **disappears**,
it is composition of crisis types; if it **persists**, the signal genuinely weakened
for domestic crises too. Report the share explained.

---

## Synthesis (frozen)

Table T1–T6 (measure / prediction / result / supports?). Verdict logic:
- **T2 fails** → hypothesis fails at the gate; **12th registered null**; STOP.
- **T2 passes + T6 rising-share-tracks + T5 signal-recovery + T4 external FNs** →
  the erosion is **outcome-composition** (crisis mix shifted); the institutional signal
  is intact for domestic crises; the framework needs a **systemic-exposure dimension**
  (a scope characterization + extension path, not a weakness).
- **T2 passes, T5 null** → domestic signal intact but no country-level exposure
  recovery (mechanism is compositional/system-level, not a tractable country control).

Diagnosis only — **no framework changes** this session. Artifacts
`data/robustness/contagion/`; code `scripts/robustness/contagion_*.py`; narrative in
`docs/CONTAGION_RESULTS.md` + Finding 12 of `docs/ROBUSTNESS_RESULTS.md`.
