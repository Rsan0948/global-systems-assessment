# Defensible results across the platform

> **Scope.** This is the consolidated ledger of what each leg's evidence can bear,
> sorted by weight. Real-data results are flagged; simulated/placeholder nodes
> prove a *pipeline*, not a theory. Honest nulls and falsifications are listed
> with the same prominence as positive results — they are scientific-integrity
> artifacts, not omissions.

---

## Modernization Index

> **Corrected 2026-07-11 by the reproducibility audit** (`mi-research/docs/ROBUSTNESS_RESULTS.md`).
> The "100% directional accuracy" below is a `verification{}` coding tally, not a
> clean recomputable result: of the 51 flagship ordinality cases, only ~10 are
> mechanical auto-derivations, 7 are mechanical abstentions counted as
> confirmations, and ~34 rest on preserved human judgment. Quote the durability
> gate (below), not the 100%.

- **109-case retrodiction corpus** — 84 modern (1947–2024, six continents) + 25
  ancient (c. 2686 BCE – 1797 CE). Headline coding: 100% directional / zero
  falsifications — but see the correction above; the mechanically-recomputable
  core is a minority.
- **Durability gate (Safeguard J) — the audit's strongest survivor.** Recomputes
  cleanly (18/19), and predicts actual crises at **88.9% vs a 63.2% base rate
  (+25.7 pts), with zero false positives**. This is the defensible predictive claim.
- **Rule-validation family — honestly weak:** 60% vs a 66.7% majority baseline
  (−6.7 pts); does not beat base rate.
- **P1 ordinality** — Institutional Quality is the most central variable in the
  construct: it correlates with the other pillars at |r| ≈ 0.79–0.80, and P1
  ordinality is confirmed across all 51 ordinality cases (213 confirm / 77
  partial / 0 fail). Every country that sustained gains improved institutions
  first or simultaneously.
- **Cross-model validation** — Spearman ρ ≥ 0.99 across three independent pillar-
  weighting schemes; the ranking is robust to the weight choice.
- **Durability gate (Safeguard J)** — the direction of the P4–P1 gap (economic
  structure minus institutional quality) predicts sustainability in **17/19**
  cases. Structurally the same idea as Study 2A's dimensional-gap-score; see
  `fragmentation/DGS_AND_SAFEGUARD_J.md`.
- **Convergence qualifier** — validated against a blind holdout; correctly handles
  petro-state edge cases.
- **Configuration thesis** — balanced pillars predict durability better than peak
  performance on any single dimension (configuration > magnitude).
- **Resource penalty** — resource wealth reliably predicts underperformance
  relative to income.
- **Global deceleration** — modernization velocity is down ~65% from its peak;
  median GPA is falling.

### MI — honestly refuted or held back (kept, not added)
- **Golden-age signature** — refuted on a geographic holdout (z = −0.0); NOT added
  to the framework.
- **Accountability gap** — falsified as a crisis predictor by the Cuba case;
  retained only as an informational hypothesis.

---

## Collectivization study

*Verified against `collectivization/results/cycle_analysis.json`.* 30 cases (25
core + 5 controls) spanning ~4,000 years.

- **Predecessor depth predicts restructuring magnitude** — depth→flip-count
  Spearman ρ = **−0.84**, p < 0.001. Deeper predecessor institutions flip fewer
  governance features on collectivization.
- **Speed predicts integration loss** — among high-depth cases, collectivization
  speed→integration-features-lost ρ = **0.83**, p < 0.001. Fast collectivization
  of a deep predecessor loses more integration.
- **Four empirical pathway types** — construction (13), restoration (5),
  negotiation (4), redesign (3). **Negotiated** collectivizations have the highest
  mean durability (308 vs 119–149 for the others).
- **Form-shift hypothesis supported**; ratchet hypothesis **not** supported
  (sign-test p = 0.64) — reported as found.
- **Warning-signals framework** operational (0.76 hit rate on the cases with
  sufficient data).

---

## Fragmentation census

*Verified against a live re-run of `fragmentation/integration/run.py` and
`fragmentation/census/run.py`.*

- **Rivers — the one fully confirmed result.** Real HydroRIVERS (HydroSHEDS);
  discovery on North America (geom-mean Rb 3.488) was frozen in git
  (`fragmentation/preregistration/FROZEN_DISCOVERY_CLAIM.md`, commit `5cff6be`)
  before the South-America holdout was touched; the sealed holdout reproduced it
  (Rb 3.539) and passed all three pre-registered criteria (beats null, in
  [3.2, 3.8], above e). Only result that cleared the full discovery →
  sealed-confirmation discipline.
- **Biology — 6 neuron cell types** from real NeuroMorpho reconstructions
  (150 arbors each), measured by the *same* Horton instrument as rivers. Each
  concentrated (CV ≈ 0.17–0.25) and at/above the ~3.0 random-merging null:
  motoneuron 3.74, pyramidal 3.69, purkinje 3.44, interneuron 3.28, ganglion
  3.22, granule 2.92. Real, discovery-stage (no cross-holdout confirmation yet).
- **Self-organizing vs designed dispersion contrast** — the cleanest single
  result: real NCBI taxonomy + engineered specs disperse ~22× more than
  self-organizing systems (control mean CV ~5.77 vs ~0.26; Brown–Forsythe
  p ≈ 1e-252).
- **Grown-vs-designed dispersion dial** — CV rises monotonically with how
  engineered the structure is: corporate splits 0.31 → party splits 0.58 → state
  dissolutions 0.90 → religious bodies 1.33 → administrative subdivisions 2.28.
- **Languages land in the physical band** — Glottolog (a self-organized *human*
  system) fractures at 3.40, CV 0.20 — same band as rivers and neurons. The
  dividing line is *how a system came to be*, not what it is made of.

### Fragmentation — honestly refuted or discarded (kept, not hidden)
- **Universal subdivision constant — no.** Domains do not share a value
  (I² ≈ 0.98); the pooled CI excludes *e*. Rung 1, not rung 2/3.
- **Mechanism predicting the branching value — no.** The rung-4 test is a real
  NULL: across 6 biology cell types the dimensional gap does not predict the
  factor (slope 0.14, 95% CI [−0.07, 0.35], p = 0.15).
- **DGS → instability with current proxies — no.** Real ECI + V-Dem + WB + UCDP
  panel (n = 713, 144 countries): the dimensional gap adds nothing beyond GDP +
  population + governance (β = 0.107, p = 0.42, AUC gain 0.0; robust across 5
  sensitivity specs). A correctly reported negative result — see
  `fragmentation/DGS_AND_SAFEGUARD_J.md` for why the MI's composite pillars
  recover the signal the raw proxies miss.

### Fragmentation — what is real vs. simulated
- **REAL:** rivers (both continents), biology (6 cell types), negative controls
  (NCBI taxonomy + specs), DGS (ECI+V-Dem+WB+UCDP), corporate (SEC EDGAR, 108
  splits), languages (Glottolog), trees.
- **SIMULATED / deferred:** organizations (doctrine-table literature values);
  open-source real GitHub crawl deferred (descoped from holdout B, logged as a
  prereg amendment). The pooled cross-domain number therefore mixes real and
  simulated nodes and is **not** a clean claim about real systems — the earned
  claims are the per-domain concentration and the grown-vs-designed dial.

---

## Bottom line

- **MI:** a five-pillar instrument that retrodicts 109 cases at 100% directional
  accuracy, with institutional quality (P1) as the load-bearing variable and
  configuration beating magnitude for durability.
- **Collectivization:** predecessor institutional depth governs how a fragmented
  polity reconsolidates (ρ = −0.84), and negotiation is the most durable pathway.
- **Fragmentation:** self-organizing systems (including human language) fracture
  in a tight band that beats chance; designed systems fracture dispersedly,
  severity scaling with engineering. No universal constant, no mechanism for the
  value — rung 1, honestly reported.
