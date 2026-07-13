# Tier 4 — Structural Scarring — Pre-Registration

**A fourth instrument.** V1 (capacity), V2 (conversion), V3 (pressure) all measure the
polity's *current state*. **Tier 4 measures the *ground* — accumulated structural damage from
prior violence that persists underneath the institutional surface and elevates future
conflict vulnerability independently of everything built on top.** Its empirical anchor is the
single most temporally-stable relationship in the whole program: the **conflict trap**
(prior-conflict → future-conflict, ρ = +0.21 to +0.67 in every epoch 1846–1996). Tier 4 is
the only tier that **carries history forward with decay.**

Frozen before any analysis touches outcomes. sha256 on commit.

## Binding rules
1. Pre-register construction, weights, and decay before testing.
2. **The decay half-life is a TESTABLE PARAMETER, not an assumption** (T4-3 chooses it).
3. Tier 4 does **not** modify V1/V2/V3. Additive only.
4. **Report all results including nulls.** If the scarring composite does not beat the raw
   prior-conflict binary (T4-6) or add beyond V1+V3 (T4-1), the conflict trap is simpler than
   the four-sub-dimension decomposition — report it.
5. Trust (S2) is culturally variable — acknowledge; prefer within-scope caveats.
6. Higher S-Score = MORE scarring = WORSE (consistent with V3).

## Data (what is actually reachable)
- **S1 conflict history [core, deep, near-universal]:** committed onset classification
  (COW∪UCDP domestic/interstate onsets **1818–2023**). Raw UCDP battle-deaths/active-years CSV
  is not committed/reachable → **intensity approximated by onset count**; conflict-years
  approximated by onset events in the window (disclosed proxy). Type from the domestic/external
  tag (civil weighted higher).
- **S2 trust damage:** OWID "self-reported trust" (WVS, 115 countries).
- **S3 demographic scarring:** OWID refugees-by-origin ÷ population (WDI); youth-share ×
  conflict-recency interaction. *(Population-pyramid "missing men" cohort analysis not built —
  disclosed gap; displacement + youth×recency stand in.)*
- **S4 legitimacy damage:** Political Terror Scale — cumulative PTS ≥ 4 in prior 30y (state
  perpetration). *(Coups [Powell-Thyne] and transitional-justice [TJRC] blocked/unreachable →
  S4 = state-perpetration only, degraded — disclosed.)*

## Construction (fixed)
- **Decay:** each historical event weighted `exp(−λ · years_since)`. Default half-life 30y
  (λ=0.0231); T4-3 sweeps {15, 25, 50, 75}.
- **S1** = decay-weighted sum of prior onsets (civil ×1.0, interstate ×0.5), normalized 0–100.
  Recency captured by the decay itself.
- **S2** = 100 − trust-percentile (low trust = high scarring).
- **S3** = mean of [refugees %pop percentile, youth×recency percentile].
- **S4** = decay-weighted cumulative PTS≥4 years, normalized 0–100.
- **S-Score** = **0.40·S1 + 0.20·S2 + 0.20·S3 + 0.20·S4** (pre-registered), computed from
  available sub-dimensions with the weights renormalized; **Track** flagged (T1 all four;
  T2 = S1 + 1–2; T3 = S1 only). Each sub-dim normalized 0–100 (5th/95th pct).

## Pre-registered hypotheses (outcome = domestic conflict onset, forward window; base 2012 → 2013–2024)
- **T4-1 (GATE) — independent predictive value.** Out-of-fold CV-AUC of conflict onset for:
  V1; V3; V1+V3; **V1+V3+Tier4**. Gate = Tier4 adds **≥ 0.03** AUC over V1+V3.
- **T4-3 — decay half-life.** Which half-life {15,25,50,75} maximizes S1's conflict-onset AUC?
  50+ ⇒ generational-to-civilizational; 15–25 ⇒ heals within a generation. Data decides.
- **T4-4 — fills the gap.** Among conflicts V1+V3 miss (false negatives), does Tier4 flag them
  (mean Tier4 of missed-conflict vs correctly-quiet)?
- **T4-6 (the crux) — does the composite MEDIATE the raw conflict trap?** In `onset ~ raw_prior_conflict + S-Score`,
  does S-Score absorb the raw binary's coefficient (mediation) or does the raw binary retain
  independent significance (⇒ the composite under-captures the trap)?
- **T4-5 — new archetypes.** Add Tier4 to the 3-vector archetypes; do *rebuilt-on-scars*
  (high V1/V2, low V3, **high T4** — Rwanda/Bosnia), *scar-trapped* (all bad + high T4 — DRC/
  Yemen), *clean-foundation* (all good + low T4 — Nordics/NL) emerge as populated cells?

## Interpretation gates (frozen)
- **T4-1 passes** ⇒ scarring carries conflict information beyond current capacity + pressure;
  Tier 4 earns its place as the fourth dimension. **T4-6** tells us whether it has
  *operationalized* the trap (mediation) or merely *re-expressed* part of it.
- **T4-1 fails / T4-6 shows the raw binary survives** ⇒ the conflict trap is not improved by
  the four-part decomposition; report Tier 4 as "raw prior-conflict is already the instrument;
  the sub-dimensions add nothing" — an honest null on a theoretically compelling tier.
