# Tier 7 — Mule Archetype Derivation — Pre-Registration

**The final reduction of the Mule.** Six tiers measure *why*, *how close*, and *how dense the
sparks* are. The last unmeasured element is *who* — the individual who triggers the cascade.
Hypothesis: the *specific* individual is unpredictable (the irreducible Mule), but the **TYPE**
of destabilizing actor — pathway to power, mobilization base, toolkit, legitimacy narrative —
is **structurally constrained by the six-tier configuration.** Similar state shapes should
produce similar actor archetypes. If so, the Mule shrinks from "anyone, any way" to "a specific
*class* of actor via a specific pathway is the dominant destabilization mode for this shape."

Frozen before computing any shape→archetype relationship. sha256 on commit.

## Binding rules + disclosed deviations
1. Typology (below) and predicted fingerprints (M2) + country predictions (M4) frozen here,
   before the actual fingerprints are computed.
2. **Single-coder deviation (disclosed):** the spec requires two independent coders + Cohen's
   κ ≥ 0.70. I am one agent; I code actor archetypes from *documented, well-known* facts about
   each case (who took/attempted power, by what pathway). Inter-coder reliability is therefore
   **untestable here** — a real limitation. To bound bias I restrict to **unambiguous modern
   cases** and allow **blended** codes.
3. Discriminant/classification uses **leave-one-out CV** — out-of-sample accuracy only.
4. Country-level deviation (disclosed): I code one **dominant modern destabilization archetype
   per country** (not per-event), and use the **current** six-tier vector as the country's
   shape (stable structural features; a good approximation for recent events, weaker for old
   ones). Event-level + event-time scores would be the ideal; this is the tractable version.
5. Report all nulls. If shape does not predict archetype (M1 fails), the Mule is bigger than
   hoped and agency is irreducible — an important finding, reported plainly.
6. Phase 3 (profile generator) is **exploratory** — "the configuration suggests," never "the
   framework predicts a person."

## The actor typology (exhaustive, mechanical)
- **A1 Civilian Populist-Nationalist** — wins/contests elections, consolidates via legal/
  constitutional means, anti-establishment/nationalist framing (Orbán, Chávez, Erdoğan-early,
  Bukele, Fujimori, Trump-attempt, PiS, Modi).
- **A2 Military Interventionist** — officer/institution seizes power by coup/martial law
  (Sisi, Thai coups, Myanmar junta, Sahel coups, Yoon-attempt).
- **A3 Insurgent Commander** — armed non-state group, excluded identity base, from outside the
  state (Syria opposition, Taliban, FARC, Sahel jihadists, TPLF, Boko Haram).
- **A4 Kleptocratic Strongman** — captures state for enrichment via patronage/rents/security
  loyalty, not mandate or coup (Putin, Nazarbayev, Lukashenko, Hun Sen, Mugabe, Bongo).
- **A5 Theocratic/Ideological Revolutionary** — transcendent religious/ideological mandate,
  clergy/vanguard base (Khomeini, Taliban-also-A3).
- **A6 External Intervention Agent** — foreign power drives regime change; domestic successor
  installed (Iraq-2003, Libya-2011, Cold-War coups).
- **A7 Constitutional/Institutional Capture** — dismantles democracy via legal/elite mechanisms
  *without* populist mass base (Saied-Tunisia, Netanyahu judicial-reform).

## Pre-registered predicted fingerprints (M2) — before computing actuals
- **A1 populist:** mod-high V1, low V2-equity, mod V3, low-mod T4, mod T5, **low T6.**
- **A2 military:** any V1, mod-high V3, mod T4, **high T6-military**; the military-in-politics
  component dominant.
- **A3 insurgent:** **low V1**, low V2, **high V3 (exclusion)**, **high T4**, low T5, **high T6.**
- **A4 kleptocratic:** low-mod V1, low V2, **low V3**, mod T4, low T5, **high T6-resource.**
- **A5 theocratic:** any V1, low V2, high V3, mod T4/T5, **high T6-transcendent.**
- **A6 external:** **low V1**, high V3, **high T4**, low T5, **high T6 (resource+geographic).**
- **A7 institutional:** high V1, high V3, low mass-mobilization, mod T5.

## Pre-registered country predictions (M4) — before computing
- **United States → A1** (high V1, low V2-equity, mod V3/T4, low T5/T6). Already produced Trump.
- **Israel → A7** (judicial capture) with **A2** backstop.
- **Korea → A2** (Yoon's martial law was literally A2, caught by V1 80).
- **Poland → A1** (PiS; same shape as Hungary).
- **Netherlands → NONE** (shape maximally distant from every crisis fingerprint).

## Hypotheses
- **M1 (GATE).** Among country pairs with cosine-similar six-tier shapes (>0.85), same-archetype
  rate: >70% strong / 50–70% partial / <50% fail.
- **M2.** Archetype fingerprints differ (LOO-CV classification of archetype from the six-tier
  vector; ≥ the majority-class baseline, target 60%+).
- **M3.** Fingerprint stability pre/post-1990 (era split, where n permits — else noted).
- **M4.** Predict dominant archetype for non-crisis countries from fingerprints; check the
  pre-registered five.
- **M5.** For flickering (high-T5) countries, does the predicted archetype match the observed
  flicker's direction?

## Gate
M1 ≥ 50% and M2 above baseline ⇒ state shape constrains actor type; the Mule reduces to a small
archetype set per configuration; build the (exploratory) profile generator. Else ⇒ agency is
irreducible to structure — reported as the honest finding.
