# Claims and evidence ledger

This is the authoritative record of the project's public claims.

If a summary elsewhere in the repository disagrees with this file, this file wins. A result does not become predictive evidence simply because it is reproducible. The evidence design and the result are recorded separately so readers can see what was tested and how much weight it can carry.

Last reviewed: 2026-08-25

## How to read the ledger

Each claim has two labels.

**Evidence design**

- **Descriptive:** A measured pattern in observed data. It does not establish prediction or causation.
- **Hindsight retrodiction:** The outcome was known when cases were selected, scored, or calibrated.
- **Blind out-of-sample:** Cases or outcomes were held apart from the derivation process.
- **Prospective:** The prediction was sealed before the outcome occurred.
- **Interpretive:** A human coded historical judgment is part of the evidence.
- **Simulation:** The result shows what a model can produce, not what the world necessarily does.

**Verdict**

- **Supported:** The stated test passed within the stated scope.
- **Mixed:** Some parts passed and others did not.
- **Not supported:** The stated test failed or returned a null result.
- **Pending:** The outcome is not ready to grade.
- **Retired:** The claim has been withdrawn and remains visible for the record.

## Corpus counts

These collections answer different questions and must not be added together without explanation.

| Collection | Count | What it is | What it is not |
| --- | ---: | --- | --- |
| Modern MI case corpus | 84 case studies | Hindsight-calibrated retrodiction | Blind validation |
| Ancient MI extension | 25 case studies | Firewalled, interpreter-scored consistency check | Mechanical or blind validation |
| Historical MI corpus | 109 case studies | The 84 modern and 25 ancient sets together | A set of 109 independent predictions |
| MI out-of-sample program | 67 observations | Blind tests across several cohorts | One uniform validation sample |
| Relational layer | 12 records | Firewalled relational probes | Part of the 109 historical cases |
| Approximate MI research total | 188 records | 84 + 25 + 67 + 12 records | 188 distinct cases; about five records overlap |
| Collectivization study | 30 cases, 109 formation cycles | A separate historical coding study | Part of the MI corpus |
| Public country atlas | 190 scored pages | Current descriptive country outputs, including partial coverage | Validation observations |

## Modernization Index claims

### MI-001: The public country score is deterministic

- **Evidence design:** Descriptive
- **Verdict:** Supported
- **Claim:** With the same inputs, version, and settings, the scoring engine returns the same result.
- **Limit:** Determinism shows reproducibility. It does not show that the score predicts future events.
- **Sources:** `mi-research/mi/scoring.py`, `mi-research/mi/constants.py`

### MI-002: The 84 modern historical cases are internally consistent with the framework

- **Evidence design:** Hindsight retrodiction
- **Verdict:** Supported within the coded corpus
- **Claim:** The framework reproduces many expected directional relationships across the 84 modern cases.
- **Limit:** Outcomes were known during selection, scoring, or calibration. Report this as retrodictive consistency, never as an 84-case forecast record.
- **Sources:** `mi-research/docs/SYSTEM_STATE.md`, `mi-research/data/case_studies/completed/`

### MI-003: The 25 ancient cases extend the pattern across earlier periods

- **Evidence design:** Interpretive and hindsight retrodiction
- **Verdict:** Mixed
- **Claim:** The ancient coding is broadly consistent with the framework.
- **Limit:** One coder interpreted the cases with outcome knowledge. The set is firewalled and needs independent recoding.
- **Sources:** `mi-research/docs/SYSTEM_STATE.md`, `mi-research/data/case_studies/ancient/`

### MI-004: The combined out-of-sample program supports predictive use

- **Evidence design:** Blind out-of-sample
- **Verdict:** Mixed
- **Claim:** Some directional signals survived blind testing, but the full program does not yet establish reliable prediction.
- **Result:** The random modern cohort was right-signed but weak, at about d = 0.37. The ancient cohort had no outcome variance. The second shock cohort was stronger within cohorts but null when pooled.
- **Limit:** The 67 observations come from different designs and should not be presented as one accuracy percentage.
- **Sources:** `mi-research/docs/SYSTEM_STATE.md`, `mi-research/data/case_studies/source_reports/VALIDATION_v1_30_random_modern.md`

### MI-005: The P4 minus P1 durability gap identifies structural vulnerability

- **Evidence design:** Hindsight derivation
- **Verdict:** Supported in derivation
- **Claim:** A large gap between economic structure and institutions separated many crisis cases from absorbers in the derivation sample.
- **Result:** The commonly cited count is 17 of 19 in the hindsight-calibrated set.
- **Limit:** This is not a forward validation record. The regression residual called the durability ratio is a different measure and should not share the same name.
- **Sources:** `mi-research/docs/architectural_decisions/v3_1_durability_gate.md`, `mi-research/mi/durability.py`

### MI-006: Backsliding risk follows an inverted-U across institutional capacity

- **Evidence design:** Blind out-of-sample
- **Verdict:** Supported provisionally
- **Claim:** The middle-capacity danger-zone signal achieved an out-of-sample AUC of 0.746 in the recorded test.
- **Limit:** This is one model result, not a universal law. It needs independent replication and sensitivity checks before policy use.
- **Sources:** `mi-research/docs/ROBUSTNESS_RESULTS.md`, repository issue 23

### MI-007: Institutional structure and wealth have moved closer over the long run

- **Evidence design:** Descriptive panel analysis
- **Verdict:** Supported provisionally
- **Claim:** The recorded 143-polity panel shows the structure-versus-wealth spread narrowing from about 0.131 to 0.070, with p = 0.033 in the current analysis.
- **Limit:** Some inferential values were reconstructed through bootstrap analysis rather than printed directly by the source workflow. Independent reproduction is required before publication.
- **Sources:** `mi-research/docs/ROBUSTNESS_RESULTS.md`, repository issue 16

### MI-008: The full six-layer model adds strong predictive power

- **Evidence design:** Cross-validated model audit
- **Verdict:** Not supported as a strong claim
- **Claim:** The full model remains exploratory.
- **Result:** Honest out-of-fold AUC was about 0.63, below the earlier in-sample estimate of about 0.71.
- **Limit:** Model layers 5 and 6 should not be presented as validated prediction.
- **Sources:** `mi-research/docs/AUDIT_2026_07_12.md`

### MI-009: The golden-age signature predicts future outcomes

- **Evidence design:** Prospective
- **Verdict:** Not supported
- **Claim:** The preregistered forward golden-age test failed.
- **Limit:** This failure must remain visible whenever the project's prospective record is summarized.
- **Sources:** `mi-research/docs/PROJECT_SYNTHESIS.md`

### MI-010: The sealed country flags predict outcomes around 2030 to 2034

- **Evidence design:** Prospective
- **Verdict:** Pending
- **Claim:** The flags are recorded with falsification conditions and cannot yet be scored.
- **Limit:** They are predictions, not evidence of predictive accuracy.
- **Sources:** `mi-research/data/forecasts/sealed_flags_2024.json`

## Fragmentation claims

### FRAG-001: River branching concentration replicated across continents

- **Evidence design:** Discovery followed by blind geographic holdout
- **Verdict:** Supported
- **Claim:** The North American discovery estimate of about 3.488 was followed by a sealed South American estimate of about 3.539.
- **Limit:** This supports a river-network regularity. It does not establish a universal constant across all domains.
- **Sources:** `fragmentation/natural-systems/rivers/README.md`

### FRAG-002: Self-organizing systems converge on Euler's number

- **Evidence design:** Cross-domain testing
- **Verdict:** Retired
- **Claim:** The proposed universal value near e did not survive testing.
- **Limit:** The retired claim stays in the repository as part of the audit trail.
- **Sources:** `fragmentation/README.md`, `fragmentation/SYNTHESIS.md`

### FRAG-003: The current DGS measure predicts instability

- **Evidence design:** Observational model test
- **Verdict:** Not supported
- **Claim:** The current proxies produced beta = 0.107, p = 0.42, and no AUC gain.
- **Limit:** Better measures may justify a new preregistered test, but the current result is null.
- **Sources:** `fragmentation/DGS_AND_SAFEGUARD_J.md`

### FRAG-004: Grown and designed systems have sharply different dispersion

- **Evidence design:** Mixed observational, curated, and simulated comparison
- **Verdict:** Supported provisionally
- **Claim:** The collected domains show a large dispersion contrast between grown and designed systems.
- **Limit:** Some designed-system inputs are curated and the organization result is simulated. The GitHub open-source holdout remains deferred.
- **Sources:** `fragmentation/README.md`, `DEFENSIBLE_RESULTS.md`

## Collectivization claims

### COLL-001: Deeper predecessor institutions are associated with fewer form changes

- **Evidence design:** Interpretive historical coding
- **Verdict:** Supported within the coded dataset
- **Claim:** Across 30 cases, predecessor depth and flip count have Spearman rho = -0.84 with p < 0.001.
- **Limit:** The coding is curated and needs independent recoding.
- **Sources:** `collectivization/results/cycle_analysis.json`, `collectivization/README.md`

### COLL-002: Faster consolidation is associated with integration loss in high-depth cases

- **Evidence design:** Interpretive historical coding
- **Verdict:** Supported within a subset
- **Claim:** The high-depth subset records rho = 0.83 between consolidation speed and integration loss.
- **Limit:** This is a subset result and should be reported with its group size and selection rule.
- **Sources:** `collectivization/results/cycle_analysis.json`

### COLL-003: Negotiated unions are more durable

- **Evidence design:** Interpretive historical coding
- **Verdict:** Exploratory
- **Claim:** The negotiated pathway has the longest mean durability in the current coding.
- **Limit:** The negotiated group contains only four cases. Treat the result as a lead for further study.
- **Sources:** `collectivization/README.md`, `collectivization/results/cycle_analysis.json`

### COLL-004: Collectivization creates a general ratchet toward greater scope

- **Evidence design:** Interpretive historical coding
- **Verdict:** Not supported
- **Claim:** The current ratchet test returned p = 0.64.
- **Limit:** The stronger supported pattern concerns changes in institutional form, not a general increase in scope.
- **Sources:** `collectivization/README.md`

### COLL-005: Designed systems tend to lose a parent function dimension

- **Evidence design:** Curated cross-domain comparison
- **Verdict:** Supported provisionally
- **Claim:** The current coding records function loss in 12 of 13 designed cases.
- **Limit:** The result depends on curated classifications and needs independent recoding.
- **Sources:** `fragmentation/README.md`, `DEFENSIBLE_RESULTS.md`

## Synthesis claim

### SYN-001: One structural law unifies all three research programs

- **Evidence design:** Conceptual synthesis
- **Verdict:** Exploratory
- **Claim:** The three programs share useful concepts and may describe related structural processes.
- **Limit:** The evidence is uneven across domains. The synthesis is a research agenda, not a validated law.
- **Sources:** `docs/GRAND_SYNTHESIS.md`, `mi-research/docs/PROJECT_SYNTHESIS.md`

## Changing a claim

A claim can move in either direction when evidence changes. Open a claim dispute and include:

1. The claim ID.
2. The exact data, code, or source at issue.
3. A reproducible challenge.
4. The proposed evidence design or verdict.
5. What result would settle the dispute.

Retired and unsupported claims are never deleted from this ledger.
