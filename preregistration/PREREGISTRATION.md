# Pre-Registration: The *e*-Subdivision and Dimensional-Gap Theory of Self-Organizing Hierarchical Systems

**Status:** DRAFT for public deposit (OSF / arXiv / personal research site)
**Version:** 0.1
**Date drafted:** 2026-06-12
**Authors:** _[to be completed by human author(s) before deposit]_
**Pre-registration commitment:** No data described in Phase 2 onward has been analyzed at the time this document is timestamped and deposited. The hash of this document at deposit time is the binding record.

> This is a *pre-analysis plan*. Its purpose is to fix, in advance and in public, (a) exactly what the theory predicts, (b) exactly what would count as the theory failing, and (c) exactly how every analysis will be conducted — so that no analytic choice can be made after seeing the results. Where the plan leaves a defensible choice open, that choice is resolved by a pre-specified rule, not by the analyst's discretion at analysis time.

---

## 0. How to read this document

Every numbered prediction (P-#) is paired with:
- a **null hypothesis** (H0) — what we expect if the theory is *wrong*;
- a **decision rule** — the exact statistical threshold that distinguishes "support" from "failure"; and
- a **failure clause** — what observation would falsify or force revision of the prediction.

A prediction that cannot fail is not in this document. If you find one, it is a defect to be corrected before deposit.

---

## 1. The theory in falsifiable form

The theory makes claims about **self-organizing hierarchical systems**: systems whose branching/subdivision structure emerges from internal dynamics under a cost trade-off, *not* from an external designer optimizing for a domain-specific objective, *not* from imposed human categorization, and *not* in regimes where the marginal cost of replication is near zero. (These exclusions are not hedges added after the fact; they are pre-registered boundary conditions — see §4 — and they are themselves tested.)

### 1.1 The central numeric claim — committed as an explicitly tiered hypothesis

The single biggest threat to this project's credibility is the "range loophole": predicting an optimum of *e* ≈ 2.71828 while accepting any value in [2, 4] as confirmation. A [2, 4] band cannot distinguish *e* from 3 from π's neighborhood, which is precisely the question Phase 3 exists to settle. We therefore commit the numeric claim as a **tiered hypothesis with pre-specified downgrade rules**, decided before data:

- **Tier 1 (strong claim — primary hypothesis): the optimum is *e* specifically.**
  Predicted central value k\* = *e* = 2.71828. This tier is *supported* in a domain only if the estimated **center of the distribution has a 95% interval that includes *e* and excludes both 3 and π** — i.e. the data localise the center *to e specifically*, not merely "nearer e than 3." Tier 1 is the program-level headline only if this separation holds in a pre-specified majority of domains (≥ 4 of the ≤ 6 testable Phase-2 domains) **and** is not contradicted in the river-network domain 2C (the cleanest physical test).

  > **Criterion correction (made before deposit, after a calibration probe — see Study 2C).** An earlier draft set the Tier-1 bar at "Bayes factor ≥ 10 for *e* vs 3." Simulation showed this is **sample-size-hackable**: with fixed-point models, BF(e vs 3) diverges toward whichever value is *nearer* the true center even when neither is correct — a true center of 2.85 produces BF(e:3) growing past 10⁷ as n grows, falsely "endorsing" *e*. The center-interval-separation criterion above is used instead because more data narrows the interval around the *true* center, so a true-2.85 world correctly *fails* Tier 1. Point-model Bayes factors are still reported as descriptive model-fit statistics but do **not** decide the tier.

- **Tier 2 (weak claim — fallback): the optimum is a small value "near 3."**
  Predicted central value in the interval that the data's own mode-estimation supports, with the theory making no commitment to *e* over 3. This tier is the *recorded result* if Tier 1's Bayes-factor bar is not met but a unimodal optimum in roughly [2.3, 3.7] is nonetheless established.

- **Tier 0 (failure): no stable preferred subdivision factor.**
  Recorded if the distribution of observed subdivision factors is not unimodal in the small-integer range, or its mode is outside [2, 4], or model comparison favors the uniform-distribution null.

**Downgrade rule (committed now):** We report Tier 1 as the headline result **only if** its bar above is met. Otherwise we report Tier 2 (if its condition holds) or Tier 0, **with equal prominence**, in the abstract and the title. The analyst does not choose the tier; the pre-specified Bayes-factor and mode-location criteria choose it. The "[2, 4] range" appears in this document **only** as the Tier-0 failure boundary, never as a confirmation band for Tier 1.

### 1.2 The dimensional-gap claim

- **P-DG:** In self-organizing systems, the scaling exponent of *interior complexity* (with system size) exceeds the scaling exponent of *interface/boundary capacity* by Δ ≈ 1. Physical prediction: Δ = 1 exactly (volume vs. surface, d vs. d−1). Organizational prediction: Δ ≈ 1.

### 1.3 The instability claim

- **P-INST:** Systems whose interface capacity (P1-type measures) is exceeded by their interior complexity (P2/P4-type measures) — i.e., **Dimensional-Gap Score DGS > 0** — are more likely to undergo fragmentation/failure than systems with DGS ≤ 0, *after controlling for obvious confounds*.

### 1.4 Two honesty caveats fixed in advance

These are written here so they cannot be quietly dropped if convenient:

1. **Pipeline-recovery is not novel evidence.** Several predictions recover results already established in the literature — Horton bifurcation ratios ≈ 3–5 (and empirically often ≈ 4, *not e*), and Murray's-law exponent ≈ 3. Reproducing these validates our measurement pipeline but provides **no independent confirmation** of the *e*-specific claim. Any write-up must label these as pipeline checks, and the river-network domain in particular is registered as a place where the data may land near 4 and thereby *contradict Tier 1* (see §3, Study 2C failure clause).
2. **The DGS→fragmentation construct carries most of the theory's risk** because its operationalization (economic complexity as "interior," institutional quality as "interface") is the most novel and least constrained. Its operational definitions are frozen in §3 Study 2A *before* any outcome data is examined.

---

## 2. Pre-registered predictions (master list)

| ID | Prediction | H0 (theory wrong) | Decision rule | Failure clause |
|----|-----------|-------------------|---------------|----------------|
| **P1** | Subdivision factor of self-organizing systems is *e* (Tier 1) / near 3 (Tier 2). | Subdivision factors are uniform/unstructured over a wide range, or centered outside [2,4]. | Tier logic in §1.1; per-domain tests in §3. | Mode outside [2,4], or uniform model wins, or *e* loses to 3 **and** π everywhere → Tier 1 fails. |
| **P-DG** | Interior-minus-interface scaling exponent Δ ≈ 1. | Δ indistinguishable from 0, or not stably ≈1. | 95% CI on Δ excludes 0 and includes 1 (Study 3B). | 95% CI excludes 1 → P-DG fails. |
| **P-INST** | DGS > 0 predicts subsequent instability beyond GDPpc + population. | DGS adds no predictive power beyond controls. | Likelihood-ratio test of DGS term, p < 0.05 two-tailed, **and** out-of-sample AUC improvement > 0 with non-overlapping bootstrap CI (Study 2A). | DGS coefficient n.s. or wrong sign → P-INST fails. |
| **P-FRAG-k** | Count of viable successor states/entities/forks clusters at *e*/near-3. | Counts uniform, or binary (always 2), or centered elsewhere. | χ² goodness-of-fit + Bayesian model comparison vs. {2,3,4,π,uniform} (2A,2B,2F). | Best model is uniform or 2 → fails. |
| **P-NEG-1** | Engineered systems do **not** cluster at *e* (wider variance). | Engineered systems cluster at *e* as tightly as natural ones. | Variance ratio test: engineered dispersion > natural dispersion, p<0.05 (4A). | Engineered systems cluster at *e* ≥ as tightly as natural → boundary condition wrong. |
| **P-NEG-2** | Classification systems do **not** cluster at *e*. | They cluster at *e*. | As 4A (4B). | Same as P-NEG-1. |
| **P-PRED-C** | Top-decile DGS countries fragment more than bottom-decile over 2026–2046. | No difference. | Pre-frozen ranking; evaluated 2036/2046 (5A). | No difference at evaluation → fails. |
| **P-PRED-F** | High org-complexity-ratio firms split more within 10y. | No difference. | Pre-frozen ranking; evaluated 2036 (5B). | No difference → fails. |

---

## 3. Phase 2 — per-study analysis plans

General standards (apply to **all** studies; see §6 for the full list): two-tailed tests; exact p-values reported; effect sizes alongside every p-value; Benjamini–Hochberg FDR control across the family of primary tests within each phase; pre-specified sensitivity analyses; all code and data public.

### Study 2A — Political fragmentation (n ≥ 200 states, 1816–present)
- **Data:** Correlates of War (state system membership, territorial change), Polity V, World Bank WGI, V-Dem.
- **Successor-count test (P-FRAG-k):** For every state that fragmented since 1816, count viable successor states at 5y and 20y (viability = recognized + continuous government + above pre-specified population/GDP floor, frozen here: ≥ 500k population **and** appears in COW state list). χ² goodness-of-fit of the successor-count distribution against each of {2, 3, 4, π-rounded, uniform}; Bayesian model comparison reports Bayes factors.
- **DGS predictive test (P-INST):** **Frozen operationalization** — interface proxy = V-Dem `v2x_polyarchy` (primary) / WGI government-effectiveness (robustness); interior proxy = Economic Complexity Index (Harvard Atlas) standardized to the same scale; DGS = (interior z) − (interface z). Logistic regression: instability event (coup, civil war onset per UCDP, territorial loss, or regime change |Δpolity| ≥ 3) within 10y ~ DGS + log(GDPpc) + log(population) + region FE + decade FE. Primary test = likelihood-ratio test on the DGS term. Out-of-sample validation = temporal split (train ≤ 1990, test > 1990), report ΔAUC with 1000-bootstrap CI.
- **Failure clause:** DGS term n.s. (p ≥ 0.05) **or** wrong sign **or** ΔAUC CI includes 0.

### Study 2B — Corporate fragmentation (n ≥ 500 US public firms, 1980–present)
- **Data:** SEC EDGAR; Compustat/WRDS (needs credentials); Wikipedia spin-off list (cross-check).
- **k-test:** viable-successor count per split (viability = operating + revenue above frozen floor at 5y). Model comparison as 2A.
- **Survival test:** Cox PH, hazard of {split, acquisition, delisting} ~ org-complexity ratio (reported 10-K business segments ÷ executive-team size) + size + sector + year. Proportional-hazards assumption checked (Schoenfeld); if violated, stratify per pre-spec.
- **Failure clause:** complexity-ratio hazard ratio CI includes 1, or uniform wins the k-test.

### Study 2C — River networks (n ≥ 10,000 basins) — **cleanest physical test; built out in `/studies/2C_river_networks`**
- **Data:** HydroSHEDS (primary), NHD (US robustness), GRDC.
- **Measurement:** per-basin Horton bifurcation ratio Rb via regression of ln(N_ω) on Strahler order ω (Rb = exp(−slope)); basins with ≥ 3 orders only.
- **Test:** KDE of the pooled Rb distribution with bootstrap CI on the mode; Bayesian model comparison of center ∈ {*e*, 3, π, 2, 4} vs. a free-center model and a uniform null.
- **Pre-registered risk (honesty caveat 1):** the literature mode is often ≈ 4. **If the pooled mode's 95% CI excludes *e* and includes 4, Tier 1 fails in the domain registered as its strongest test, and the headline downgrades to Tier 2 or Tier 0 per §1.1.** This is stated before looking at any basin.
- **Calibration/power (runnable now, no data needed):** before real data, demonstrate via simulation that the model-comparison procedure recovers the true center and quantify the n required to distinguish a true-*e* world from a true-3 world at BF ≥ 10. Implemented in this repo.

### Study 2D — Biological branching (n ≥ 1000 measurements)
- **Data:** published vascular/bronchial morphometry; US Forest Service FIA.
- **Test:** pooled branching-ratio distribution mode vs. {*e*,3,π,...}; Murray's-law exponent with 95% CI per species (predicted 3.0 — **pipeline check, not novel evidence**, per §1.4).
- **Failure clause:** Murray exponent CI excludes 3 across most species (pipeline fault), or branching-ratio mode outside [2,4].

### Study 2E — Organizational scaling (n ≥ 1000 groups)
- **Data:** published team-performance meta-analyses; military doctrine tables (≥ 5 countries/eras); Dunbar data.
- **Test:** random-effects meta-analysis of per-capita performance vs. team size (peak location + heterogeneity I²); inter-echelon scaling ratios vs. {*e*,3,4}.
- **Failure clause:** no reliable peak, or peak/ratios outside [2,4], or I² so high the pooled estimate is uninterpretable (pre-spec I² > 90% → report as inconclusive, not as support).

### Study 2F — Open-source forks (n ≥ 500)
- **Data:** GitHub API / GH Archive (GHTorrent is defunct — registered substitution).
- **Test:** viable-fork count (fork itself > 100 stars) at 2y/5y; distribution vs. {2,3,4,π,uniform}.
- **Boundary check:** software has near-zero replication cost — this domain is registered as **partially excluded** by §4's third boundary condition and is reported as a boundary probe, not a core confirmation.

---

## 4. Phase 4 — pre-registered boundary conditions (negative controls)

The theory **must** fail here, or it explains too much to explain anything.

- **B1 — Engineered systems (Study 4A):** memory hierarchies, filesystem trees, DB index fan-out, highway interchanges. **Prediction: do NOT cluster at *e*; dispersion strictly greater than the natural-systems pooled dispersion.** Test: Levene/Brown–Forsythe variance comparison, p < 0.05.
- **B2 — Imposed classifications (Study 4B):** biological taxonomy (species/genus, genera/family), Dewey, LoC. **Prediction: higher and more variable ratios than self-organizing systems.**
- **Failure of the whole theory's specificity:** if engineered or classification systems cluster at *e* **as tightly as** natural systems, the claim that *e* emerges *specifically from self-organization* is wrong, and that is reported as a primary finding — not buried.

---

## 5. Phase 5 — predictive validation (frozen now, evaluated later)

- **5A:** Rank all in-scope countries by DGS and k_eff; freeze the ranking (hash in this repo). **Prediction:** top-decile fragments more than bottom-decile by 2036 (interim) / 2046 (final). Binary, time-bounded.
- **5B:** 50 largest public firms by market cap; freeze org-complexity-ratio ranking. **Prediction:** high-ratio firms split more within 10 years (eval 2036).
- These cannot be automated to completion; the rankings are generated and frozen now, evaluation is a future human action.

---

## 6. Analysis standards (binding for every test)

1. **Two-tailed** hypothesis testing throughout; no one-tailed tests.
2. **Exact p-values** reported, never just "< 0.05."
3. **Effect sizes** reported with every p-value (Cohen's d / odds ratio / hazard ratio / Bayes factor as appropriate); a significant-but-tiny effect is reported as weak support, explicitly.
4. **Multiple-comparison control:** Benjamini–Hochberg FDR at q = 0.05 across the family of primary tests within each phase; the family is enumerated *in this document* before analysis.
5. **Sensitivity analysis** for every primary result: vary each frozen threshold (viability floors, order minimums, proxy choices) across a pre-specified grid; report how conclusions move. A conclusion that flips under a reasonable alternative assumption is reported as fragile.
6. **Model comparison** uses Bayes factors with priors stated in code; Jeffreys scale for interpretation (BF ≥ 10 "strong/decisive," 3–10 "moderate," < 3 "inconclusive").
7. **Reproducibility:** all code, data-access scripts, environment specs, and random seeds public; every figure regenerable by one command.
8. **Symmetric reporting:** failures occupy the abstract, title, and first results paragraph with the same prominence as successes. The tier actually achieved (§1.1) is the headline, whatever it is.

---

## 7. What is fixed by depositing this document

At deposit, the following are no longer changeable without a public, timestamped amendment that is itself reported in the final paper: the tiered numeric claim and its Bayes-factor bars (§1.1); the DGS operationalization (§3, 2A); all viability floors and order minimums; the family of primary tests for FDR; the boundary conditions (§4); and the frozen Phase-5 rankings (§5). Anything not fixed here is, by definition, a researcher degree of freedom and must be reported as such.
