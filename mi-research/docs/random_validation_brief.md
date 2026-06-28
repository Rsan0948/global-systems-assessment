# FROZEN BRIEF — 30 randomly-selected modern "polity-shock" case studies

**Frozen: 2026-06-28.** This is the verbatim research brief sent to an external AI agent **with no
knowledge of the index/framework**, to gather genuinely out-of-sample validation cases. Kept in git so
the eventual results have an auditable, un-tuned prompt to point back to. (Design rationale at the
bottom is for internal use and was NOT sent to the agent.)

---

## RESEARCH BRIEF: 30 randomly-selected "polity-shock" case studies

### What this is
I am stress-testing a model of how states respond to major shocks. I need **30 real historical cases,
selected without bias**, so the test is genuinely out-of-sample. **Randomness and neutrality are the
entire job.** Do not try to make the cases interesting, clean, dramatic, or balanced. Do not interpret,
rate, or theorize. Just find real cases by a documented random procedure and report citable facts. Do
**not** search for or read about any "modernization index," "MI," or scoring framework — you don't need
it, and it would bias you.

### The unit of analysis
A **polity-shock episode**: a sovereign (or de-facto sovereign) state that experienced a single,
identifiable, significant shock in a specific year, with at least ~10 years of observable aftermath.

A "shock" is any of: a financial/economic/currency crisis; a war (civil or external) or major military
defeat; a coup or contested succession; a leader's sudden death; mass unrest/revolution; a secession
crisis; a pandemic's national impact; a commodity-price collapse for a dependent economy; a severe
disaster-driven state crisis. One clear primary shock per case.

### How to select them (random, documented, auditable)
1. Assemble a **candidate pool of ≥150 shock events, 1900–2015**, drawn from general-reference, neutral
   catalogs (e.g., published lists of banking/currency crises, coups d'état, civil wars/armed conflicts,
   regime transitions, major successions). Do not curate for outcome or interest — include mundane and
   ambiguous ones.
2. **Number the full candidate list** and use a random-number generator to draw your selections.
   Document the numbered list and which numbers the RNG picked (I need to see the procedure).
3. Light spread only (applied *after* the draw, by re-drawing clustered picks): **max 2 cases per
   country**, and aim for representation across **all world regions and across the decades**
   1900s–2010s. Do not otherwise tune the sample.
4. Discard a draw only if it (a) hits the exclusion list, (b) lacks ~10 years of observable aftermath,
   or (c) has too little documentation to describe factually — then **draw a random replacement**, don't
   hand-pick one.
5. Deliver **exactly 30**.

### What to report for each case (neutral facts only)
1. **Polity** (state name; ISO3 code if modern) and **region**.
2. **The shock** and the **year it began** (one sentence).
3. **Pre-shock snapshot** — 3–5 factual, citable sentences describing the state's condition ~2–3 years
   *before* the shock: how it was governed/administered, its economy, its social/political stability.
   **Describe; do not rate or judge.**
4. **Outcome** — pick the single best-fit tag below for the **10 years after the shock**, plus 1–2
   sentences of factual justification and the date of the key outcome event:
   - **1 — Collapse/fragmentation:** state broke apart or lost effective control of significant
     territory / ceased to function as a unified state.
   - **2 — Violent rupture:** civil war, revolution, coup, or violent forced regime change (state
     survived but through violent discontinuity).
   - **3 — Peaceful discontinuity:** major *non-violent* regime change or constitutional
     rupture/transformation.
   - **4 — Stressed but continuous:** serious unrest/crisis/instability, but the basic state and
     institutional order survived and recovered.
   - **5 — Absorbed/stable:** weathered with broad continuity; little lasting institutional disruption.
5. **Era flag:** onset `post-1996` / `1950–1995` / `1900–1949` / `pre-1900`.
6. **Sources:** 2–3 citable references (books, peer-reviewed work, or authoritative reference sources).

### Hard constraints
- Sovereign or de-facto-sovereign states only (not provinces or cities).
- One clear primary shock per case; shock onset **1900–2015**.
- Enough documentation to state the pre-shock condition and the outcome as **facts**, not inference.
- Full outcome spectrum must be allowed to appear — do **not** deliberately balance the five tags;
  report whatever the random draw yields.

### EXCLUSIONS (so we don't re-test on cases already used)
**Rule A — never select these specific country-and-shock cases** (any era close to the one noted):
post-Soviet/Yugoslav/post-communist transitions ~1989–1992 (Estonia, Latvia, Lithuania, Russia,
Ukraine, Poland, Hungary, Czech Republic, Slovakia, Slovenia, Croatia, Serbia, Bosnia, Kosovo, Georgia,
Armenia, Azerbaijan, Kazakhstan, Uzbekistan, Turkmenistan, Kyrgyzstan, Tajikistan, Belarus, Moldova,
Mongolia, Romania 1989); the **Arab Spring 2011** (Tunisia, Egypt, Libya, Syria, Yemen, Morocco, Jordan,
Bahrain, Algeria); Turkey 2013–16; Thailand 2014; Brazil 2013–16; South Africa 2021; Peru 2022;
Sri Lanka 2022; Greece 2010; Ireland 2008; Iceland 2008; Mali 2012; Gabon 2023; Nicaragua 2018;
Oman 2020; China 2012; Cuba 2018; Argentina 2001; Venezuela (1989 *and* post-2010); Lebanon 2019;
Chile 2019; Indonesia 1997–98; Malaysia 1997; Iran 1979; Israel 2023; Italy 1992; India/Pakistan 1947
partition; Pakistan/Bangladesh 1971; Ethiopia/Eritrea 1990s; Sudan/South Sudan 2011; DR Congo/Rwanda
1990s; Haiti & Dominican Republic; Singapore/Malaysia 1965; Costa Rica, Cameroon, Mauritius, Nigeria,
Ghana, Côte d'Ivoire, Botswana, Bolivia, Nepal, Myanmar, Vietnam, Fiji, Colombia, Honduras, Guatemala,
Papua New Guinea, East Timor, Somaliland, Uruguay, Mexico (post-2010).

**Rule B — for these frequently-studied countries the modern period is already covered; pick only a
pre-1990 episode for them, or skip:** United States, United Kingdom, France, Germany, Japan, Canada,
Italy, Spain, Portugal, Netherlands, Belgium, Sweden, Switzerland, Australia, Saudi Arabia, UAE, Kuwait,
Qatar, South Korea, India, China, Russia.

**Anything not on Rule A or Rule B is fully open, any era.** (There are ~100+ less-studied states —
across Africa, the Caribbean, the Pacific, Central America, smaller Europe and Asia — plus the entire
pre-1990 history of the big ones. Lean into that long tail; that's where unbiased cases live.) If a
country appears on Rule A, a *clearly different* episode ≥20 years away is acceptable but flag it.

### What NOT to do (these void the test)
- Don't cherry-pick famous, clean, or "good example" cases; include boring and ambiguous ones.
- Don't deliberately balance outcomes or regions beyond the light spread rule.
- Don't score, rate, rank, or theorize about *why* anything happened — facts and the one outcome tag only.
- Don't read about any index/scoring framework.
- Don't skip a random draw because it seems uninteresting — only skip for the three listed reasons, then
  random-replace.
- Deliver exactly 30, with the documented random-selection list attached.

---

## Internal rationale (NOT sent to the agent)
- **Why airtight:** the agent selects blind (no fitting to our hypotheses), reports a *neutral* outcome
  tag + raw facts (no framework language), and on our end the pre-shock pillar data is pulled
  **deterministically** (WGI/V-Dem/Maddison for the pre-shock year) and the fixed rules applied — so
  neither selection nor scoring has degrees of freedom to fit. Their outcome is ground truth; our
  prediction is mechanical; we compare. This is the out-of-sample test the retrodiction baseline isn't.
- **Expected tradeoff:** the exclusions + long-tail tilt will yield many smaller and pre-1990 cases,
  where rich WGI data is thin; those get scored on V-Dem(P1)/Maddison(P4)/life-exp(P3) — partial-pillar,
  sufficient for the two load-bearing claims (durability gap, container) but not full 5-pillar verdicts.
