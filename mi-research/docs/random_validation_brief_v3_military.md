# FROZEN BRIEF v3 — military-shock cohorts (the test that exercises the relational tier)

**Frozen: 2026-06-28.** v1 (`random_validation_brief.md`) and v2 (`random_validation_brief_v2.md`)
between them tested the INTERNAL engine. Neither tested the relational/exposure tier (T3): v1's random
coup/conflict draw landed in the blind spot with near-zero outcome variance, and **v2's shock-cohort
draw contained zero external-military/conquest shocks** (all "external" cohorts were natural-disaster
or price shocks) — so T3 was never exercised, and the discriminating 4th cell (internally fragile but
externally SHIELDED → survives) stayed empty. v3 fixes both: it **selects on MILITARY shocks**, takes
the whole cohort survivor-inclusive, and — the key change — **collects the strategic/relational facts**
(alliances, relative military strength, contested borders) in the pre-shock snapshot, so the relational
layer can be scored. Sent to a framework-naive agent. The internal note at the bottom is NOT part of
the agent's prompt.

---

## RESEARCH BRIEF v3: ~25–30 polity-military-shock observations via cohort sampling (1816–2010)

### What this is
I'm stress-testing a model of how states come through **major military shocks** — wars, invasions,
occupations, conquest waves. I need real cases selected **without bias**, capturing the **full spread
of outcomes** — states that were conquered, states that lost territory, AND states that were threatened
or attacked but **came through intact**. Survivors matter as much as casualties. Randomness and
neutrality are the job. Do **not** score, rate, interpret, or theorize. Do **not** read about any
"modernization index," "MI," exposure model, or scoring framework.

### The unit
A **polity-military-shock observation**: one sovereign (or de-facto sovereign) state, one military
shock it was exposed to, its situation just before, and what happened to it (~5–10 years after).

### How to select (random, documented, auditable)
1. **Build a pool of ≥15 multi-party MILITARY shock events/waves, 1816–2010**, each involving *many*
   states as belligerents, targets, or threatened neighbors. Mix the types:
   - **Invasions / interstate wars** (one state attacks another or a region).
   - **Conquest / partition waves** (a great power or coalition redraws a region's map).
   - **Occupations** (wartime or imposed).
   - **Standoffs / coercion** where war was threatened (some targets attacked, some deterred).
2. **Number the pool and RNG-draw ~5–7 shocks.** Document the pool and the draws.
3. For each drawn shock, **list every polity it materially involved or threatened** — aggressors,
   defenders, conquered, AND neighbors that were exposed but not attacked. If >~8, take a documented
   **random subset**. **Include members regardless of outcome** (do not drop the survivors).
4. Aim for **~25–30 total observations**, grouped by shock so each cohort is visible.
5. **Alignment-spread rule (important):** within each cohort, make sure you include BOTH states that
   had a formal external protector / great-power ally / alliance at the time AND states that stood
   alone. If a cohort is all-aligned or all-isolated, note it and prefer a cohort with a mix.
6. **Era preference (soft):** all eras 1816–2010 welcome; 1900–2010 has richer records.

### Report per observation (NEUTRAL FACTS ONLY — describe, do not rate)
1. **Cohort** (e.g., "WWII European occupations, 1939–42") + **polity** (state; ISO3 if modern) + **region**.
2. **The military shock** + **onset year**.
3. **Pre-shock snapshot ~2–3 years before — TWO parts, both factual & citable:**
   - **(a) Internal:** governance/administration, economy, social/political stability (3–4 sentences).
   - **(b) Strategic situation (REQUIRED — this is new):** Did the state have a formal **military
     alliance or great-power protector** (name the treaty/patron, or state "none")? Its **relative
     military strength versus the attacking/threatening power** (roughly comparable / weaker / far
     weaker — with any citable figures: army size, spending). Any **active territorial dispute or claim**
     against it. Whether it sat on a **contested great-power frontier**. Describe; do not rate.
4. **Outcome tag** (single best fit, ~5–10 years after) + 1–2 sentences + key date:
   **1** Conquered / sovereignty extinguished · **2** Major territorial loss / partition / occupied ·
   **3** Defeated but survived as a sovereign state · **4** Attacked/threatened, held without major loss ·
   **5** Successfully defended or deterred (repelled the attack, or was never attacked despite the threat).
5. **Era flag:** `1900–2010` / `1816–1899`.
6. **Sources:** 2–3 citable references.

### Hard constraints
- Sovereign or de-facto-sovereign states only; one named cohort/shock per observation; onset 1816–2010.
- **Include every cohort member you can document, whatever its outcome** — especially the ones that
  came through fine.
- Do not hand-pick members; take all, or a documented random subset. Do not balance outcome tags.
- **Onset ≥ 1816** (older cases lack the structured records this needs; flag any pre-1816 you find but
  do not count it).

### EXCLUSIONS (already used elsewhere — drop the member, keep the rest of the cohort)
Cyprus 1974; Kuwait 1990; Bosnia 1995; Taiwan 1996; Estonia/Baltics post-2004; South Korea; Greece
1919–22; Spain 1936; Poland-Lithuania partitions; Afghanistan 2001/2021; Finland 1939; the Inca/Aztec
Spanish conquests. **Frequently-studied powers — use only a peripheral/older episode or skip:** USA,
UK, France, Germany, Russia/USSR, Japan, China.

### What NOT to do (these void the test)
- Don't drop a cohort member because it survived or its outcome was unremarkable — that is the exact
  bias this removes (the 4th cell — weak states that came through because someone protected them).
- Don't omit the **strategic-situation** facts in 3(b) — they are the point of v3.
- Don't score, rate, or explain causes — neutral facts plus the one outcome tag only.
- Don't read about any index/scoring/exposure framework.
- Deliver ~25–30 observations grouped by cohort, with the documented shock-pool and RNG draws attached.

---

## Internal note (NOT sent to the agent)
- **Why v3 is the test T3 needs.** A military-shock cohort holds the shock ~constant and *guarantees*
  the relational channel is in play; the alignment-spread rule (5) + survivor-inclusion *force* the
  empty 4th cell to fill (fragile-but-shielded survivors + fragile-unshielded fallers in the same
  cohort). The strategic-situation fields 3(b) are exactly the T3 inputs — patron (E2/R3), relative
  power (E1), contested border (E3), great-power frontier (E5) — collected as neutral facts so the agent
  stays naive.
- **Scoring protocol (deterministic, pre-registered).** For each returned observation: pull the citable
  relational layer at the pre-shock year — **COW CINC** (relative power), **ATOP/COW alliances**
  (patron), **ICOW** (contested border) — and score T3 (structural & net exposure, response, with the
  deterrence-patron vs response-patron split). Read internal P1/P5 from the case (V-Dem rol for
  pre-WGI). **Pre-registered rule:** higher structural exposure → worse outcome tag *unless* a credible
  patron/response shield is present, which should move the case toward survival. Test **within cohort**
  (the clean natural experiment) and pooled, **split by shield status** (the discrimination test:
  among high-exposure states, do the shielded survive and the unshielded fall?). Log predictions before
  reading outcomes; the airtightness is the blind selection + mechanical relational pull + pre-registered
  rule (per the v1/v2 standard).
- **Success criterion (honest).** This is the first genuine *out-of-sample* test of T3. A real result
  is: among internally-fragile, highly-exposed cohort members, shielded ones survive and unshielded
  ones fall at rates the rule predicts — on cases T3 never saw. Distrust the slope: T3 gauges standing
  exposure/risk, not the timing of any particular war.
