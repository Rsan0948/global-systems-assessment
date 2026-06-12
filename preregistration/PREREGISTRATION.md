# Pre-Registration: A Discovery Program for Lawful Subdivision in Self-Organizing Hierarchical Systems

**Status:** DRAFT for public deposit (OSF / arXiv / personal research site)
**Version:** 0.2 — *discovery reframe* (supersedes v0.1, which pre-registered a
single confirmatory claim that the optimum is *e*)
**Date drafted:** 2026-06-12
**Authors:** _[to be completed by human author(s) before deposit]_
**Binding commitment:** No real-domain data has been analyzed at the time this
document is timestamped and deposited. The document hash at deposit is the
record. A separate **sealed holdout** of domains/data (named in §7) is not
inspected until the confirmation stage.

---

## 0. What changed, and why it matters

Version 0.1 asked a **confirmatory** question — "is the subdivision constant
*e*?" — and pre-registered *e* with falsifiers. The actual research goal is
different and prior: **is there a theorem at all?** Is there *any* lawful
regularity in how self-organizing hierarchical systems subdivide, above what
mundane mechanisms already produce — and if so, is it one universal law or many
domain-specific ones, what is its value, and is there a mechanism that predicts
it?

That is a **discovery** question, and discovery and confirmation have different
— partly opposed — inferential logics. Running an open-ended search and then
reporting it as if a specific value had been predicted is the cardinal error
(HARKing). So this program is explicitly **two-stage**:

- **Stage A — Discovery (exploratory).** Characterize the data, decompose its
  variance, locate structure, and read off whatever value/mechanism the data
  supports. Held to *descriptive* standards and labeled exploratory throughout.
- **Stage B — Confirmation (pre-registered).** Take the *specific* hypothesis
  Stage A produced, freeze it, and test it on a **sealed holdout** of domains
  and/or data that Stage A never saw. Pre-registration now binds *the
  discovered hypothesis*, not *e*.

The value *e* has no privileged status in this document. It may emerge as the
pooled estimate, or not. The point of the program is the **existence, kind, and
mechanism** of a regularity — not the defense of a number.

---

## 1. The ladder of claims (what "a theorem" can mean)

"Is there a theorem?" is, statistically, a question about **variance
components**, not a mean. We decompose it into nested claims, each a genuine
(progressively stronger) result. The program reports the **highest rung the
evidence earns** and no higher.

| rung | claim | earned when |
|------|-------|-------------|
| **0** | **No theorem** | within-domain dispersion is large, *or* the signal is statistically indistinguishable from a mechanism-free trivial null (§3). |
| **1** | **Domain-specific laws** | each domain has a concentrated characteristic subdivision factor that differs from its own trivial null — but the factors differ *across* domains (high between-domain heterogeneity). Many small laws. |
| **2** | **Universality** | domains share one value (Cochran Q not significant, low I²) **and** that shared concentration exceeds the trivial null. One law. |
| **3** | **Named constant** | the pooled value's CI is tight enough to include a *principled* constant (e, 3, golden ratio, π, …) and exclude its rivals. |
| **4** | **Mechanism** | the interior−interface **dimensional gap** *predicts* the subdivision factor across domains (and, where a cost functional exists, systems sit at its minimum). This is the only rung that makes the regularity a *law* rather than a recurring number; it is **not decidable from subdivision ratios alone** and requires the exponent measurements of §5. |

Pre-registered decision thresholds for each rung are the operational criteria
implemented in `discovery/ladder.py` and fixed here:

- **Concentration (rung 1 gate):** median within-domain coefficient of
  variation < 0.30.
- **Universality (rung 2):** Cochran Q p > 0.05 **and** I² < 0.25.
- **Named constant (rung 3):** pooled 95% CI contains exactly one principled
  constant from {e, 3, π, φ, φ²} and excludes the others. *(Why a CI-isolation
  rule and not a Bayes factor: see Appendix A — point-hypothesis Bayes factors
  for "e vs 3" diverge toward the nearer value with sample size even when
  neither is correct, so they are sample-size-hackable.)*
- **Mechanism (rung 4):** across domains, the estimated dimensional gap Δ
  predicts the observed log subdivision factor with a slope whose 95% CI
  excludes 0, and Δ's own 95% CI includes 1 (§5).

---

## 2. The instrument: between- vs within-domain variance decomposition

Implemented and calibrated in `discovery/` (see its README and the
known-truth calibration in `discovery/results/`).

Each **domain** contributes one estimate of its characteristic subdivision
factor (mean log-ratio) with a standard error from its within-domain scatter
and sample size. A DerSimonian–Laird random-effects model yields:

- the **within-domain** dispersion (rung-1 evidence),
- the **between-domain** variance τ² and I² (rung-2 evidence),
- the **pooled value and 95% CI** (rung-3 readout),
- Cochran's **Q** test of the universality null.

This single model answers "is there a theorem, and what kind" without ever
committing to a value in advance. The calibration demo confirms it returns
rung 3 / rung 1 / rung 0 correctly on universal / domain-specific / trivial
known-truth worlds, and that a discover→confirm split behaves.

---

## 3. The triviality doctrine (the central control)

The most dangerous failure mode is discovering a **tautology**: random binary
topology already clusters near 3, and Shreve's random-topology model near 4,
with *no optimization law* (directly demonstrated in
`studies/2C_river_networks`). So "self-organizing systems cluster near k" is, by
itself, possibly free combinatorics.

**Therefore every domain must supply a mechanism-free `null_sampler`** — a
random-topology / random-merging / size-only generator — and a finding counts
*only* as the part of the signal that survives above that baseline:

- **per-domain:** the observed factor must differ from the domain's own trivial
  null (the domain is doing something non-trivial), and/or
- **cross-domain:** observed between-domain concentration must be *tighter* than
  independent trivial processes produce (a non-trivial universal pull), and/or
- the observed pooled value must be **displaced** from the trivial pooled value.

A rung-2/3 result whose concentration the trivial nulls already reproduce is
demoted to **rung 0 (trivial)**. This is pre-registered, not discretionary.

---

## 4. The observable must be a comparable *factor*

The theory is about a subdivision **factor k**, so the per-domain observable
must be a *ratio*, commensurable across domains — not a raw count that conflates
parent size with subdivision tendency.

- Rivers / lungs / vasculature / trees: branching ratio (Horton / bifurcation).
- **Political fragmentation (revised):** successor states **per pre-existing
  internal division** (federal/administrative/ethnic units), *not* the raw
  successor count. The USSR producing 15 states reflects its 15 republics, not a
  preference to split 15 ways; raw counts are not comparable to a river's
  bifurcation ratio. (This corrects the v0.1 Study-2A observable.)
- Corporate: resulting viable entities per reported business segment.
- Open-source: viable forks per major module/sub-project.

Where the count/ratio definition is genuinely ambiguous, the ambiguity is
entered as **modeled uncertainty** (multiple defensible codings carried through
a sensitivity analysis), not resolved by a single analyst choice.

---

## 5. The mechanism / optimization apex (rung 4 — promoted to centerpiece)

A recurring number is numerology until a mechanism predicts it. The former
"hardest test" is now the program's apex:

- **Independently** estimate, per domain, the scaling exponent of *interior
  complexity* and of *interface/boundary capacity* with system size, and their
  gap Δ.
- Test (a) whether Δ clusters at 1, and (b) whether **Δ predicts the domain's
  observed subdivision factor** across domains.
- Where a cost functional is physically defined (river energy dissipation;
  Murray's law for vasculature, which is *itself* a cost-minimization result),
  test whether observed structures sit at the cost minimum and whether that
  minimum coincides with the cross-domain pooled value.

Rung 4 is the difference between "these systems happen to share a number" and
"there is a law." Only a positive rung-4 result licenses calling the regularity
a theorem.

---

## 6. Domains as nodes; boundary conditions as expected rung-0

Every Phase-2 domain from v0.1 (rivers 2C, vasculature/lungs/trees 2D, polities
2A, corporations 2B, organizations 2E, open-source 2F) is recast as a **node**
feeding the §2 instrument, each with its own trivial null (§3) and comparable
observable (§4).

The v0.1 **boundary conditions become predictions of rung 0**, i.e. negative
controls where the trivial null *should fully explain* the data:

- **Engineered systems** (memory hierarchies, filesystem/B-tree fan-out,
  interchanges): designer-optimized, so predicted **rung 0 / domain-specific
  scatter**, not a shared law.
- **Imposed classifications** (taxonomy, Dewey, LoC): human impositions,
  predicted higher and more variable ratios, **rung 0**.
- **Near-zero replication-cost systems** (some software): predicted to behave
  differently; treated as a boundary probe.

If these *also* show non-trivial universal concentration, the claim that the
regularity is specific to self-organization is wrong — reported as a primary
finding.

---

## 7. What is fixed now / discovered later / sealed

**Fixed at deposit (Stage A method):** the ladder and its thresholds (§1); the
variance-components instrument (§2); the triviality doctrine and the requirement
that every domain ship a trivial null (§3); the comparable-factor observable
rule (§4); the rung-4 mechanism test design (§5); the analysis standards (§8).

**Discovered in Stage A (exploratory, reported as such):** which rung the
evidence reaches; the pooled value, if any; which domains are lawful; the form
of any domain-specific pattern.

**Sealed until Stage B (named now, not inspected):** a holdout of **≥ 2
domains** chosen before any analysis — provisionally **open-source forks (2F)
and corporate splits (2B)** — plus, within each discovery domain, a **temporal
holdout** (the most recent 20% of events/measurements). The Stage-A verdict and
its pooled CI are frozen; Stage B re-runs the *identical* `assess` on the sealed
data and passes only if the holdout reaches a rung ≥ min(discovery rung, 2) with
an overlapping pooled CI.

---

## 8. Analysis standards (binding)

1. Two-tailed throughout; exact p-values; effect sizes (and the **variance
   components themselves**) reported alongside every test.
2. Benjamini–Hochberg FDR (q = 0.05) across the enumerated family of per-domain
   tests.
3. Sensitivity analysis on every coding/threshold choice (observable
   definition, viability floors, null-model specification); a verdict that flips
   under a reasonable alternative is reported as fragile.
4. The triviality control (§3) is mandatory for every domain; a domain without a
   defensible trivial null is excluded, not given a pass.
5. Discovery and confirmation use **disjoint** data (§7); no holdout inspection
   during Stage A.
6. All code, data-access scripts, seeds, and the engine's calibration public;
   every figure regenerable by one command.
7. Symmetric reporting: rung 0 (no theorem / trivial) is reported in the title
   and abstract with the same prominence as a positive rung. The whole program
   is built to be *able* to conclude "no theorem."

---

## Appendix A — why rung 3 uses CI-isolation, not point-hypothesis Bayes factors

A calibration probe (logged in `studies/2C_river_networks/results/INTERPRETATION.md`)
showed that fixed point-hypothesis Bayes factors for "e vs 3" **diverge toward
whichever value is nearer the truth as n grows, even when neither is correct**:
a true center of 2.85 drove BF(e:3) past 10⁷, falsely "endorsing" e. A
"BF ≥ 10" bar is therefore sample-size-hackable. The CI-isolation rule (§1,
rung 3) is used instead because a credible/confidence interval on the *center*
narrows around the *true* value, so a true-2.85 world correctly fails to isolate
any principled constant. Point Bayes factors may still be reported as
descriptive model-fit statistics, but they do not decide a rung.
