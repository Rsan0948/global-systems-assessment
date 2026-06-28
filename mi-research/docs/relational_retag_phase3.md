# Phase 3 — corpus re-tag, T3 consistency check, and the missing-cell problem

**Date:** 2026-06-28. Companion to `relational_tier_spec.md` / `relational_tier_proof.md`. Additive,
firewalled, baseline `213C/77P/0F` unchanged. Reproduce: `python scripts/retag_corpus.py` and
`python scripts/relational_tier.py --all`.

This phase did three things: (1) re-tagged the 51-case baseline by shock origin; (2) ran T3 on the
engine-alone misses as a consistency check; (3) located the structural reason the corpus can't yet
*test* T3 — a missing 2×2 cell — and assessed whether the frozen v2 design fixes it. The headline is a
**negative-but-clarifying** result, reported as such.

---

## 1. Corpus re-tag — the baseline is endogenous by construction
The §C rule (frozen in the spec, assigned from each case's factual shock text **before** outcomes were
joined) tags the 51 P1-ordinality cases. Frozen artifact: `data/case_studies/relational_tags.json`.

| origin | cases | predictions | partial rate |
|--------|------:|------------:|-------------:|
| endogenous | 47 | 266 | 26% |
| mixed | 2 (case06 Bangladesh-1971, case08 Eritrea) | 13 | 38% |
| exogenous | 2 (case10 Timor, case30 Iraq-2003) | 11 | 18% |
| **exo + mixed** | **4** | **24** | **29%** |

**Finding (null, and that's the point):** the exo/mixed partial rate (29%) is indistinguishable from
endogenous (26%), on n=4 cases. Conditioning on exogeneity does **not** explain the baseline's
partials. The reason is structural: **the corpus is ~92% endogenous** (47/51 cases, 266/290
predictions). The within-corpus association test is **underpowered by construction** — and the famous
exogenous misses (Cyprus 1974, Spain 1936, Greece 1922, the ancient conquests) **are not in the
corpus at all.** The corpus was built around the instrument's strength (internal fragmentation), so
the blind spot was *selected out*. This is not a workaround to find — it is the real diagnosis.

---

## 2. T3 on the engine-alone misses — a CONSISTENCY check (NOT validation)
The 30-case out-of-sample run (`validation_run_modern_30.md`) named the engine-alone misses:
moderate/high-institution states that ruptured anyway. The full 30-case list was not materialized in
the repo (it lived in the naive agent's transcript), so this runs T3 on the **named** misses — the
discriminating subset. Internal read = V-Dem rol at the pre-shock year (same proxy as the 30-run);
exposure = citable COW-era data. **These cases motivated/shaped T3, so this shows the mechanism works
as intended — it cannot validate it.** Firewalled from any out-of-sample claim.

| engine-alone miss | rol (internal) | shock type (documented) | T3 structural exposure | T3 verdict |
|-------------------|:---:|---|:---:|---|
| **Cyprus 1974** | 0.67 | Turkish **invasion** (exogenous-military) | **0.829 (high)** | **RESOLVES** |
| **Greece 1919–22** | 0.55 | Anatolia **defeat** (exogenous-military) | **0.733 (high)** | **RESOLVES** |
| Spain 1936 | 0.66 | civil war / internal polarization | 0.000 (low) | does NOT resolve |
| Portugal 1926 | 0.59 | internal military coup | 0.000 (low) | does NOT resolve |
| Venezuela 1948 | 0.51 | internal military coup | 0.000 (low) | does NOT resolve |

**The result is discrimination, not flagging.** T3 resolves the **two exogenous-military** misses and
correctly stays silent on the **three internal** ones — pointing those to a *different* missing layer
(acute internal polarization / coup-propensity), not the relational one. A flag-everything tool would
have lit all five; T3 split them on the documented shock channel. (Honest caveats: the three internal
cases read *exactly* 0.000 because all their relational components were coded false per the documented
internal shock — the discrimination rests on coding each case from its shock facts, not from T3's
output. Spain 1936 is the borderline case — there *was* major foreign intervention — but it came in
support of factions, not as conquest of Spain, so T3 reads it as internal. Flagged in the data.)

---

## 3. The missing cell — why the corpus and the 30 can't yet TEST T3
T3 discriminating on the misses is necessary but not sufficient. To show T3 *discriminates* rather than
just *flags*, you need variation on **both** exposure and outcome — the 2×2:

| | low exposure | high exposure |
|---|---|---|
| **internally durable** | survives (normal hits) — ✓ in corpus | **can still rupture** (Cyprus, Greece) — ✓ the misses T3 resolves |
| **internally fragile** | **SURVIVES despite weakness (shielded)** — ✗ nearly empty | ruptures (over-determined) — ✓ in corpus |

**The bottom-left cell — internally fragile + low exposure (shielded) → survives — is nearly empty**
in both the 51-case corpus and the coup/invasion-heavy 30. Without it, "high-exposure cases ruptured"
is consistent with *both* "exposure matters" *and* "they were unlucky" — the two can't be separated.
The fragile-but-protected survivor (a weak state that came through because a patron/alliance shielded
it) is the discriminating observation, and it's the one a coup/invasion catalog almost never returns
(shielded survival is rare and undramatic).

---

## 4. Does the frozen v2 design return the 4th cell? — NO, not reliably (assessed; cohorts not yet returned)
The v2 shock-cohort brief (`random_validation_brief_v2.md`) fixes outcome variance (take the whole
cohort, survivors included) and stratifies by **shock origin**. But it does **not** reliably surface
the 4th cell, for two concrete reasons:
1. **Wrong stratification for this purpose.** It stratifies by where the *stressor* originated
   (internal/external shock), not by the polity's *exposure/shielding*. A fragile-but-shielded survivor
   could appear, but only by luck — the design doesn't target it.
2. **The relational layer isn't collected.** The per-observation pre-shock snapshot (brief item 4)
   records only *internal* facts — governance, economy, stability. It never records alliance/patron/
   relative-power. So even when a cohort returns a shielded survivor, **T3's inputs aren't captured**,
   and T3 can't be scored on the returned set without a separate relational pull. (Several obvious
   shielded survivors are also on the exclusion list: South Korea, Finland 1918.)

### Recommended fix (two parts, both flagged honestly)
1. **Add a deterministic relational pull to the v2 scoring protocol.** Keep the agent framework-naive
   and the selection blind, but when scoring the returned external-origin cohort members, pull the
   citable relational layer (COW CINC / ATOP / ICOW / SIPRI) at the pre-shock year and score T3 *within
   cohort*. This makes the 4th cell scorable **if** the cohort happens to return one.
2. **A targeted shielded-survivor supplement** — explicitly non-random, flagged as a **discrimination
   probe**, never folded into the out-of-sample claim. Deliberately populate the empty quadrant with
   known fragile-but-protected cases: Kuwait 1990 (reversed by coalition), Baltic states post-2004 NATO
   accession, South Korea, Finland 1939 (cohesion-shielded survival of invasion), Taiwan, West
   Germany/West Berlin (Cold War). Shielded survival is rare and undramatic — it *can't* be found
   randomly — so a deliberate, clearly-labeled set is the honest way to test whether T3's low-exposure
   read actually tracks survival in internally-weak states. This is a consistency/discrimination check,
   not validation.

**Net:** the 30-case re-run is a consistency check (done — T3 discriminates on the misses); the real
*test* of T3 needs the shielded-survivor cell, which means amending the v2 scoring protocol to collect
the relational layer **and** a flagged targeted supplement — not torturing the 30.

---

## Integrity
- Additive: `--validate` after this phase = **213C / 77P / 0F** unchanged; no baseline path imports
  `relational` or `retag_corpus`.
- Tags assigned from shock text before outcomes joined (`scripts/retag_corpus.py`, frozen artifact).
- Consistency checks labeled as such; the v2 cohort run remains the pending real out-of-sample test.
