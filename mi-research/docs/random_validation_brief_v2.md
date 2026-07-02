# FROZEN BRIEF v2 — ~30 polity-shock cases via SHOCK-COHORT sampling

**Frozen: 2026-06-28.** Redesign of `random_validation_brief.md` after the first out-of-sample runs
(`validation_run_modern_30.md`, `validation_run_ancient_10.md`) returned directional-but-weak because the
random coup/conflict frame over-sampled (a) exogenous shocks (the framework's blind spot) and (b)
memorable collapses (near-zero outcome variance). v2 fixes both by **selecting on the SHOCK and taking
the whole cohort it hit — survivors included — stratified by shock origin.** Sent to a framework-naive
agent. Internal note at the bottom was NOT part of the agent's prompt.

---

## RESEARCH BRIEF v2: ~30 polity-shock cases via SHOCK-COHORT sampling (1900–2015)

### What this is
I'm stress-testing a model of how states respond to major shocks. I need real cases selected **without
bias** capturing the **full spread of outcomes** — including states that came through a shock *fine*, not
just dramatic collapses. Randomness and neutrality are the job. Do not score, rate, interpret, or
theorize. Do **not** read about any "modernization index," "MI," or scoring framework.

### The key change
Don't hunt individual famous crises. Pick a **shock** and take the **whole cohort of states it hit** —
strong and weak, survivors and casualties alike. A real shock hits many countries and they end up in very
different places; **capturing that full spread is the entire point.** The common mistake is silently
dropping countries whose outcome was unremarkable — do not.

### The unit
A **polity-shock observation**: one sovereign state, one shock it experienced, its condition just before,
and what happened after (~10 years).

### How to select (random, documented, auditable)
1. **Build a pool of ≥20 multi-country shock EVENTS/WAVES, 1900–2015**, each hitting *many* polities,
   mixing two origins:
   - **Internally-originating** (stressor arose inside the polity/economy): banking/currency/sovereign-
     debt crises, depressions/recessions, succession/leadership-death crises, contested elections,
     domestic mass-uprising waves.
   - **Externally-originating** (from outside or nature): foreign invasions/wars, pandemics, global
     commodity-price collapses hitting dependent economies, major natural disasters.
2. **Number the pool and RNG-draw ~6–8 shocks.** Document the pool and draws.
3. For each drawn shock, **list every polity it materially hit**; if >~8 members, take a documented
   **random subset**, never hand-picked. **Include members regardless of outcome.**
4. Aim for **~30 total observations** across the cohorts; group by shock so each cohort is visible.
5. **Coverage:** ≥half the observations from internally-originating shocks, ≥quarter from
   externally-originating.
6. **Recency preference (soft):** prefer cohorts after ~1995 (richer data); historical cohorts welcome.

### Report per observation (neutral facts only)
1. **Cohort** (e.g., "2014–16 oil-price collapse") + **polity** (state; ISO3 if modern) + **region**.
2. **The shock** + **onset year**.
3. **Origin tag:** `internal` / `external` / `mixed` (one sentence on where the stressor came from).
4. **Pre-shock snapshot** — 3–5 factual, citable sentences ~2–3 years before (governance/administration,
   economy, social/political stability). **Describe; do not rate.**
5. **Outcome tag** (single best fit, ~10 years after) + 1–2 sentences + key date:
   1 Collapse/fragmentation · 2 Violent rupture · 3 Peaceful discontinuity · 4 Stressed but continuous ·
   5 Absorbed/stable.
6. **Era flag:** `post-1996` / `1950–1995` / `1900–1949`.
7. **Sources:** 2–3 citable references.

### Hard constraints
- Sovereign or de-facto-sovereign states only; one named cohort/shock per observation; onset 1900–2015;
  ~10 years of aftermath.
- **Include every cohort member you can document, whatever its outcome.**
- Do **not** balance outcome or origin tags beyond the coverage rule.

### EXCLUSIONS (already-used — drop the member, keep the rest of its cohort)
post-Soviet/Yugoslav transitions ~1989–92 (Estonia, Latvia, Lithuania, Russia, Ukraine, Poland, Hungary,
Czechia, Slovakia, Slovenia, Croatia, Serbia, Bosnia, Kosovo, Georgia, Armenia, Azerbaijan, Kazakhstan,
Uzbekistan, Turkmenistan, Kyrgyzstan, Tajikistan, Belarus, Moldova, Mongolia, Romania 1989); Arab Spring
2011 (Tunisia, Egypt, Libya, Syria, Yemen, Morocco, Jordan, Bahrain, Algeria); 1997 Asian-crisis members
Indonesia, Malaysia, Thailand, South Korea; 2008/eurozone members Greece, Ireland, Iceland; Turkey
2013–16; Brazil 2013–16; South Africa 2021; Peru 2022; Sri Lanka 2022; Argentina 2001; Venezuela
(1989 & post-2010); Lebanon 2019; Chile 2019; Mali 2012; Gabon 2023; Nicaragua 2018; Oman 2020;
China 2012; Cuba 2018; Iran 1979/1953; Israel 2023; Italy 1992; Pakistan 1947/1958/1971; Nigeria, Ghana,
Côte d'Ivoire, Botswana, Bolivia, Nepal, Myanmar, Vietnam, Fiji, Colombia, Honduras, Guatemala, PNG,
East Timor, Somaliland, Uruguay, Mexico (post-2010); plus the v1 set: Norway 1905, Newfoundland 1933,
Siam 1932, Finland 1918, Spain 1936, Portugal 1926, Cuba 1933, Egypt 1952, Iraq 1958, Togo 1963, Paraguay
1954, Zanzibar 1964, Liberia 1980, Greece 1922, Czechoslovakia 1948, North Yemen 1962, Libya 1969,
Cambodia 1970, Madagascar 1972, Ethiopia 1974, Cyprus 1974, Tonga 2006, Nauru 1990s, Western Samoa 1918.
**Frequently-studied countries — use only a pre-1990 episode or skip:** United States, United Kingdom,
France, Germany, Japan, Canada, Italy, Spain, Portugal, Netherlands, Belgium, Sweden, Switzerland,
Australia, Saudi Arabia, India, China, Russia, South Korea. **Everything else is open** — lean on the
open members of each cohort.

### What NOT to do (these void the test)
- **Don't drop a cohort member because its outcome was boring or it survived** — the exact bias this
  version removes.
- Don't hand-pick cohort members; take all, or a documented random subset.
- Don't balance tags beyond the coverage rule.
- Don't score, rate, or explain causes — facts and the two tags only.
- Don't read about any index/scoring framework.
- Deliver ~30 observations grouped by cohort, with the documented shock-pool and draws attached.

---

## Internal note (NOT sent to the agent)
- **Why v2 is the real test:** cohorts hold the shock roughly constant and *guarantee* outcome variation
  (a shock always hits strong and weak states), and the origin tag lets us test the framework where it
  claims to work (internal/endogenous) separately from the blind spot (external/exogenous). Recent
  cohorts (2008 GFC, 2014 oil crash, etc.) are WGI-era → full 5-pillar deterministic scoring, not just
  P1/P4.
- **Scoring protocol:** for each cohort, pull pre-shock pillar data deterministically, apply the fixed
  rules, log predictions, *then* compare to the agent's outcome tags — **within cohort** (the clean
  test) and pooled, split by origin tag.
