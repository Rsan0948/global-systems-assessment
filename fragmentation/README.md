# Fragmentation Research

*Supporting evidence for the platform: the physics underneath the governance
analysis. A self-contained, pre-registered discovery program on how systems
subdivide. For the narrative synthesis read [`SYNTHESIS.md`](SYNTHESIS.md); for
the ongoing catalog read [`CENSUS.md`](CENSUS.md).*

---

## The question

Is there a **lawful regularity** in how self-organizing hierarchical systems
subdivide — above what mundane mechanisms (random topology) already produce? The
program was deliberately reframed from *confirming a specific constant* (is the
subdivision factor *e* ≈ 2.718?) to *discovering whether there is a theorem at
all*, and if so, what kind. **The number *e* has no privileged status.**

## How it answered it

**The ladder.** The central question is decomposed into nested claims, each a
genuine result on its own:

```
rung 0  no theorem      (scatter, or indistinguishable from a mechanism-free null)
rung 1  domain-specific laws   (each domain lawful, values differ)
rung 2  universality    (domains share one value, beating the null)
rung 3  named constant  (pooled CI isolates a principled constant)
rung 4  mechanism       (the dimensional gap predicts the value)
```

**The trivial-null doctrine.** A branching ratio near 3–4 is near-inevitable for
any binary tree (Shreve 1966; Kirchner 1993 — ~96% of possible networks fall in
Rb 3–5 with no optimization). So clustering near ~3 proves nothing on its own.
Every domain must ship a **mechanism-free `null_sampler`**; a finding counts only
as the signal *above* that null, and only with low dispersion. Both are required.

**The variance-components engine** (`discovery/`). A DerSimonian–Laird
between/within-domain variance decomposition + Q-test decides the rung. Rung 3
uses **CI-isolation, not point-hypothesis Bayes factors** (fixed-point BFs are
sample-size-hackable). Discovery and confirmation use **disjoint data**, enforced
by a git-frozen discovery claim and sealed holdouts.

## What it found: rung 1

**Domain-specific laws. No universal constant; no mechanism shown.** Self-
organizing domains are each individually concentrated but do not share one value
(I² ≈ 0.98); the pooled CI excludes *e*. Both pre-registered confirmations were
run and are **spent**:

- **Prediction A (rivers, cross-continent): CONFIRMED.** South America reproduces
  the North-America finding (geom Rb 3.539; criteria A1/A2/A3 pass).
- **Prediction B (cross-domain holdout = corporate): B1 fail, B2 pass — not fully
  confirmed.** On 108 real SEC EDGAR spin-off events, corporate splitting is
  indistinguishable from its mechanism-free binary-default null (a trivial
  domain), but adding it keeps the verdict at rung 1 — it does not collapse to
  universality or isolate a constant. Reported symmetrically.

The program was *built to be able to conclude "no theorem of a universal
constant,"* and that is where the real data lands.

## What survived and matters

Two claims are real, mostly systematic, and new:

- **The concentration finding.** Self-assembly fractures in a **tight band**
  (CV ~0.2) that beats its own random-topology null — rivers, 6 neuron cell
  types, botanical trees, and (decisively) **human languages**, a self-organized
  human system with no central designer, in the same band. The dividing line is
  *how a system came to be, not what it is made of*.
- **The grown-vs-designed dispersion dial.** Designed/institutional systems
  fracture **dispersedly**, and the dispersion (CV) rises monotonically with how
  engineered the structure is — corporations (~0.3) → parties → states → religious
  bodies → administrative hierarchies (~2.3). Sub-laws: suppression → release
  (longer-held fractures shatter bigger and bloodier) and porosity →
  fragmentation.

## How it connects to the Modernization Index

This is the empirical bottom of the **complexity–capacity matching principle**
that the MI operationalizes (`../mi-research/MASTER_REFERENCE_ARCHITECTURE.md`
§1): a growing system's interior complexity outruns its interface capacity; the
mismatch must be released as subdivision. Grown systems vent continuously;
designed systems suppress the venting until it releases catastrophically. The MI
measures where a country sits on that spectrum. In particular, Study 2A's
dimensional-gap-score and the MI's Safeguard J (the P4–P1 durability gate) are the
same idea measured two ways — see [`DGS_AND_SAFEGUARD_J.md`](DGS_AND_SAFEGUARD_J.md).

## What is real vs. simulated

- **REAL data:** rivers (HydroRIVERS, both continents), biology (NeuroMorpho, 6
  cell types), negative controls (NCBI taxonomy + specs), DGS (ECI+V-Dem+WB+UCDP),
  corporate (SEC EDGAR, 108 splits), languages (Glottolog), trees.
- **SIMULATED / deferred:** organizations (doctrine-table literature values);
  open-source (2F) — real-ingest code is committed but the GitHub crawl is
  deferred (descoped from holdout B, logged as a prereg amendment).
- **Rung-4 mechanism test → RUN on real allometry, result NULL.** Across the 6
  biology cell types the dimensional gap does not predict the subdivision factor
  (slope 0.14, 95% CI [−0.07, 0.35], p = 0.15). The gaps themselves are consistent
  with the dimensional prediction Δ≈1, but the gap→factor link is absent.

## Scope explicitly closed out

Concluded at the confirmation + mechanism stages above. Genuinely out of reach
here (not blockers, clean future extensions): the **governance/opensource** real
GitHub crawl (needs a token), the **cross-domain** rung-4 extension to
rivers/corporate (needs raw spatial re-ingest), real **governance/organizations**
doctrine parsing (low value), and a public OSF/arXiv deposit (needs a human
author identity). The engine, the real-data nodes, the spent confirmations, and a
real (null) mechanism test are all in place.

## Layout

```
preregistration/PREREGISTRATION.md   The two-stage discovery pre-analysis plan (v0.2)
                FROZEN_DISCOVERY_CLAIM.md   The git-frozen NA claim + falsifiable predictions
discovery/                           Reusable core: variance-components + trivial-null + ladder
integration/                         Node interface + runner: assemble all nodes -> ladder + controls
census/                              The fragmentation CENSUS (catalog.py, systems/, governance/)
natural-systems/rivers/              Rivers: Strahler/Horton + power study (real HydroRIVERS)
natural-systems/biology/             Biology node (real NeuroMorpho arbors, 6 cell types)
natural-systems/mechanism/           Rung-4 mechanism test
natural-systems/negative-controls/   Engineered + classification controls
governance/political/                DGS -> instability mechanism test (NOT a ratio node)
governance/corporate/                Corporate split factor + survival/hazard (sealed holdout)
governance/organizations/            Inter-echelon org scaling ratio
governance/opensource/               Viable-fork factor (boundary probe; real crawl deferred)
CENSUS.md SYNTHESIS.md DGS_AND_SAFEGUARD_J.md   Narrative + catalog + MI bridge
```

Run `integration/run.py` for the full ladder + controls + calibrations, or
`census/run.py` for the standalone census catalog. Each study is also runnable
on its own (`pytest tests/ -q` from its directory).
