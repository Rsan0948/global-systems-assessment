# Relational / Exposure Tier (T3) — Specification

**Status:** SPEC FOR REVIEW (no module built yet). **Date:** 2026-06-28.
**Author:** Claude Opus 4.8 (1M context), under the standing integrity rules (`HANDOFF.md` §8).

This is the highest-leverage artifact of the T3 increment. It is written **spec-first, on
purpose**: every key design decision is called out below in §A for review *before* any code is
written, because a wrong design choice is far cheaper to catch here than in the module. Read §A
first; the rest is detail.

---

## 0. One-paragraph framing

The MI is an **internal structural instrument**. It measures how a governed system is built and
therefore how it withstands stress *that comes from within or that it must absorb internally*. It is
**blind to externally-imposed shocks** (invasion, conquest, externally-imposed partition) — not
because such shocks are unmodelable, but because the signal lives in a **relational layer between
units** that the internal instrument never had. **T3 is that layer.** It is a **firewalled
conditioning tier**, not a verdict-changer: it never touches P1–P5, never touches a safeguard, never
enters the 213/77/0 retrodiction path. It reads the MI's internal read and external citable
relational data, and reports them **jointly** — "internally fragile/durable" × "exposed/insulated" —
so that a case the internal instrument *correctly* called internally-sound but that was nonetheless
destroyed from outside (Cyprus 1974) becomes a **conditioned consistency hit instead of a flat
miss**. T3 is a **risk gauge, not a war-predictor** (§A6).

---

## A. KEY DECISIONS FOR REVIEW

> These eight decisions are the review surface. If any is wrong, flag it before the module.

### A1 — Exposure component list (shock OCCURRENCE)
The Exposure Index **E ∈ [0,1]** (higher = more exposed) is the equal-weighted mean of five
deterministic sub-indicators, each normalized to [0,1]:

| # | Component | What it captures | Direction |
|---|-----------|------------------|-----------|
| E1 | **Relative military power** | unit's material capability vs. its single most-capable plausible adversary | weaker → more exposed |
| E2 | **Patron/alliance protection** | presence + credibility of a formal external defender | stronger patron → less exposed |
| E3 | **Contested borders / irredentism** | active territorial claim *against* the unit by another state | active claim → more exposed |
| E4 | **Bad-neighborhood / conflict diffusion** | active armed conflict in contiguous states | more neighborhood conflict → more exposed |
| E5 | **Great-power fault-line** | unit sits on a contested great-power boundary | on a fault-line → more exposed |

Note E2 (patron) lowers occurrence-risk **and** raises response (A2) — it is deliberately allowed to
appear on both axes because a credible patron both deters the shock and blunts it. This double-count
is intentional and documented, not an error.

### A2 — Response component list (shock RESPONSE)
The Response Index **R ∈ [0,1]** (higher = better able to absorb a shock that does land) is the
equal-weighted mean of four sub-indicators:

| # | Component | Source | Direction |
|---|-----------|--------|-----------|
| R1 | **Cohesion** | MI **P5** (read-only) | higher → better response |
| R2 | **Mobilization capacity** | MI **P1** (read-only) | higher → better response |
| R3 | **Patron intervention credibility** | E2 + Safeguard I axis | stronger → better response |
| R4 | **Strategic depth** | territory/population/geography (citable: area, population) | deeper → better response |

R1/R2 are **read** from the MI's already-computed pillars. T3 reads them; it never writes them.

### A3 — Data source per component (provenance is load-bearing)
Every value carries a `provenance` tag naming its dataset. **No hand-coded judgment inputs** (see
A8). Per-era citable sources:

| Component | Historical (1816+) | Modern (1949+) | Dataset |
|-----------|--------------------|----------------|---------|
| E1 relative power | COW **CINC** (National Material Capabilities, 1816–2016) | **SIPRI** milex ratio (1949+) | COW NMC / SIPRI |
| E2 patron | **ATOP** defense pacts (1815–2018) / COW Formal Alliances v4.1 | ATOP / treaty membership (NATO, US MDTs) | ATOP / COW |
| E3 contested borders | **ICOW** territorial claims (1816–2001, region-varying) | ICOW / UCDP territorial | ICOW |
| E4 neighborhood conflict | COW war list / Militarized Interstate Disputes | **UCDP/GED** (1989+) | COW MID / UCDP |
| E5 great-power fault-line | COW major-power + contiguity | bloc membership + contiguity | COW + Correlates contiguity |
| R4 strategic depth | Maddison/COW area+pop | WDI area+pop | Maddison / WDI |

**Coverage floor & the three provenance tiers.** COW/ATOP/ICOW begin ~1816; SIPRI ~1949; UCDP ~1989.
Below that floor the citable relational *primitives* don't exist — but established quantitative
historical *series* do. So provenance is **three tiers, decreasing confidence**, and every record is
tagged with one:

| Tier | Name | Relative-power source (E1) | Alliance/claim source (E2/E3) | Example |
|------|------|----------------------------|-------------------------------|---------|
| 1 | **citable** | COW **CINC** / SIPRI ratio (`method:"cinc"`) | ATOP / ICOW codings | Cyprus 1974, South Korea |
| 2 | **historical-proxy** | Maddison **economic mass** = GDPpc × population (`method:"economic_mass"`) | documented historical fact | Poland-Lithuania 1772 |
| 3 | **interpreted** | none — pure hindsight | none | the ancient tier's domain |

Tier 2 is **real, reproducible data** (Maddison GDP + V-Dem rule-of-law already in the repo), not
judgment — a notch below citable (population is supplied from standard historical demography, and the
relational codings are historical fact rather than ICOW/ATOP), and a clear step *above* interpretation.
Tier 3 is the ancient tier's firewalled domain and is not populated by T3 here. The **clean proof
(§A7) uses tier-1 cases only**; tier-2 is shown as a corroborating illustration, never as proof
evidence.

### A4 — Thresholds / output shape
- E and R are each reported as a **continuous score in [0,1]** plus a **band**: `low [0,0.33)`,
  `moderate [0.33,0.66)`, `high [0.66,1.0]`. Cutpoints are **pre-registered here** and fixed.
- T3's output object is **`{E, R, bands, per_component, provenance, joint_reading}`** — a separate
  report, never folded into the MI score.
- The **joint reading** is a 2×2 placement of (internal MI fragility) × (exposure E), with R as the
  modifier. It is descriptive text + the two indices; it returns **no pass/fail verdict and no MI
  delta**.

### A5 — Precise firewall boundary
1. T3 **reads** MI pillar outputs (P1, P5) and external relational data. It **never writes** to any
   pillar, safeguard, diagnostic, or the MI score.
2. `run_retrodiction.py --validate` **does not call T3.** T3 lives in its own module and its own
   script; the 213/77/0 path is byte-for-byte independent of T3's existence.
3. Every record carries a `provenance_tier` (citable / historical-proxy / interpreted). Only **tier-1
   (citable)** records may enter a clean-proof claim. Tier-2 (historical-proxy) is corroborating
   illustration; tier-3 (interpreted) is the ancient tier's firewalled domain. The tier is surfaced
   on every T3 output so a reader always knows the confidence of what they're looking at.
4. T3 output never appears in the validated baseline, the durability gate, or the rule-validation
   sets.

### A6 — Exposure is a RISK GAUGE, not a war-predictor
T3 conditions on **who is exposed**; it does **not** call **when** a war starts. The specific actor's
decision to initiate a specific war at a specific time is the **irreducible kernel** — the project's
"trust the level, distrust the slope" applied to the relational layer. E is therefore stated as a
**standing probabilistic exposure**, never as a forecast of a war. The spec and every T3 output must
say this in those words.

### A7 — Honest framing of the proof (consistency, NOT validation)
The Phase-2 proof shows T3 resolves **the very cases it was designed to resolve** (Cyprus 1974, the
patron-shielded mirror). That is a **consistency / "rescue" check by construction** — evidence the
tier is internally coherent and does what it was built to do — and is **explicitly NOT evidence that
it predicts.** The real out-of-sample test is **Phase 4** (the frozen v2 shock-cohort design,
`random_validation_brief_v2.md`). Every proof artifact is labeled "consistency check," never
"validation."

### A8 — Provenance discipline + tech-debt note
- Built from citable datasets from the start. The existing hand-coded context fields
  (`neighbor_threat_level`, `neighbor_details`, `external_backstop`, `backstop_details`) that feed
  Safeguards A/D/I are **interpreter judgment** and are **NOT used by T3**.
- **Tech debt (logged here, not fixed now):** those hand-coded fields should be migrated/retired to
  citable sources over time. Safeguard D's `neighbor_threat_level` is the canonical example — it was
  derived "from the Ukraine observation," i.e. hindsight. T3 is the citable replacement for that
  signal; eventually Safeguards A/D/I should read T3's citable inputs rather than hand codes. Not in
  scope for this increment.

---

## B. Proof cases (Phase 2) — chosen where the data is real and the tier will live

| Case | Internal MI read | Exposure (E) | Response (R) | Outcome | What T3 demonstrates |
|------|------------------|--------------|--------------|---------|----------------------|
| **Cyprus 1974** (new relational case) | internally OK-ish (the documented "miss" — not catastrophically fragile) | **high** (adverse CINC vs Turkey; active ICOW claim; Greek-junta patron non-credible) | **low** (no credible patron honored) | invasion + partition | turns a flat exogenous **miss → conditioned consistency hit** |
| **South Korea / Taiwan** (already in corpus: `case32`, `sig16`) | exposed, internally mid | **high** (adverse cross-strait/peninsular power; active irredentist claim) | **high** (credible US patron — MDT/forward presence) | persists, not overrun | the **mirror**: high exposure + high response (patron) → survival, explaining why an exposed unit persisted |

**Poland-Lithuania 1772 (pre-1816): HISTORICAL-PROXY illustration (tier 2), not part of the clean
proof.** No COW/ATOP/ICOW data exists pre-1816, so it can't be tier-1 — but it is *not* mere
interpretation either. Its relative-power E1 is built from **Maddison economic mass** (GDPpc ×
population: Commonwealth ~11.7k vs the joint ~61.8k of Russia+Prussia+Austria → E1 ≈ 0.84), and its
internal read from **V-Dem rule-of-law @1789 (0.18** — the liberum-veto paralysis *in the data*, vs
partitioners Prussia 0.64 / Austria 0.70). It demonstrates the same logic as Cyprus at a clearly
labeled lower-confidence tier — corroboration, never proof evidence. (Tech debt: population is
supplied from standard historical demography; the repo's Maddison subset carries GDPpc but not pop.)

A two-sided proof (one miss-rescued, one survivor-explained) is the minimum that shows the tier
captures **both** outcomes from the **same** exposure logic rather than fitting one direction.

---

## C. Phase 3 endo/exo classification rule (PRE-SPECIFIED, applied before checking resolution)

To avoid fitting the labels to the answer, the endogenous/exogenous tag for every corpus case is
assigned **mechanically from each case's factual shock description**, and the rule is frozen here
**before** any check of whether conditioning resolves the known misses:

> **A shock is `EXOGENOUS`** if the case's factual `event_description` / `stress_type` names an
> **external state actor as the proximate initiator** of the territorial or sovereignty change
> (invasion, conquest, externally-imposed partition, occupation).
> **A shock is `ENDOGENOUS`** if the proximate driver is **internal** (civil war, secession, coup,
> institutional collapse, negotiated devolution) with **no external state initiating** the change.
> **`MIXED`** if both are present; tag both and record the **primary** initiator.

The tag is read from the existing factual fields, recorded for all cases, and **only then** is the
"does conditioning on exposure resolve the misses?" question asked. The rule and the per-case tags
are committed as an artifact so the classification is auditable and not retrofitted.

---

## D. Module shape (to build *after* this spec is approved)

- `mi/relational.py` — pure-Python stdlib, deterministic. Mirrors the `durability.py` /
  `global_systems.py` pattern (a separate tier module, not woven into `scoring.py`).
  - `compute_exposure(unit, year, rel_data) -> {E, per_component, provenance}`
  - `compute_response(pillars, unit, year, rel_data) -> {R, per_component, provenance}`
  - `relational_reading(mi_result, unit, year, rel_data) -> {E, R, bands, joint_reading}`
- `data/sources/relational/` — committed citable inputs per component, each value provenance-tagged.
  Firewalled-interpreted values (pre-1816) live in a separate clearly-named file.
- `scripts/relational_tier.py` — CLI to score a unit/year and print the joint reading. **Never**
  imported by `run_retrodiction.py`.

## E. Golden Rule enforcement (same increment as the module)
When the module lands, re-run `run_retrodiction.py --validate` and show **213C / 77P / 0F
byte-for-byte unchanged** — T3 is additive and the baseline path does not import it. This is a
required artifact of the module commit, not a later step.

---

## F. Stop point — STATUS: increment BUILT, awaiting review
Per the approved increment: **spec → module → two-sided proof → prove baseline unchanged → STOP for
review before Phase 3** (full-corpus endo/exo re-tag). This document is the spec; its §A decisions
are the review surface.

**Built (this increment):**
- `mi/relational.py` — the T3 engine (deterministic, stdlib, firewalled).
- `scripts/relational_tier.py` — CLI (`--all` reproduces the proof).
- `data/sources/relational/exposure_inputs.json` (citable) + `historical_proxy_inputs.json` (tier 2).
- `docs/relational_tier_proof.md` — the Phase-2 **consistency check** (labeled NOT validation).

**Design change forced by the data (logged honestly):** the patron double-count (A1) deflated South
Korea's net exposure, muddying the mirror. Fix: T3 now reports **structural exposure** (raw adversity,
patron-independent) *alongside* net exposure, so "exposed but shielded" stays legible. Result: Cyprus
(0.829) and South Korea (0.813) have near-identical structural exposure — the patron is the whole
difference. This was data-motivated, not a tuning choice.

**Golden Rule verified:** post-build `--validate` = **213C / 77P / 0F** unchanged; no baseline path
imports `relational`.
