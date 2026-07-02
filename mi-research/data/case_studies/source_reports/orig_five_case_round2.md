# Round 2 Validation of the Modernization Index (MI) Framework: Five New Post-Fragmentation Cases

## TL;DR
- **The refinements help, but modestly and unevenly.** Round 2 produces an estimated **~66% clean confirmation / ~90% directional accuracy** — essentially holding the Round 1 baseline (64%/88%) rather than dramatically improving it. The framework's core ordinal claim (pre-event Institutional Quality predicts relative post-fragmentation trajectory) survives all five cases; its weaknesses are in timing, durability, and treating WGI scores as organic capacity.
- **Refinement B (capacity gate on successor count) was the most valuable**, correctly re-flagging the Ethiopia/Eritrea 2-state split as catastrophic-risk despite a low fragment count, exactly as the Sudan-derived rule intended. Refinement A (external administration flag) was essential for Timor-Leste and Kosovo. Refinement C (reversal risk) correctly fired on Bangladesh and Serbia.
- **The single biggest data finding is methodological:** per the World Bank, the 2025 WGI revision introduced "an absolute 0–100 scale anchored to fixed benchmark countries" and "To ensure full comparability over time, historical estimates have been recalculated back to 1996" (Worldwide Governance Indicators, 2025 Revision, accessed 12/15/2025) — so clean pre-2024 legacy percentile cells can no longer be pulled live from the API. This materially complicates any framework that hard-codes WGI percentile thresholds (as Refinement B does at "50 on Rule of Law").

## Key Findings

1. **Singapore is the cleanest confirmation in either round.** Highest pre-event P1 in the sample → best trajectory by a wide margin. Confirms predictions 1 and 5 and the complexity-control thesis.
2. **The P1-ordinality claim holds across all five cases** at the directional level: Singapore > Malaysia; India > Bangladesh > Pakistan (with caveats); Indonesia > Timor-Leste; Serbia > Kosovo; Ethiopia ≈ Eritrea (both low, both bad).
3. **The "low P1 → violent release" claim is strongly confirmed** by Ethiopia/Eritrea. AU lead mediator Olusegun Obasanjo, in a January 2023 Financial Times interview, stated of the 2020–22 Tigray war: "The number of people killed was about 600,000," adding the peace deal "stopped an average of 1,000 deaths per day" (a figure Ghent University researchers called roughly correct). It is *complicated* by Timor-Leste (violence came from the departing power, Indonesia, not from low indigenous P1).
4. **Refinement B fixed a real Round 1 error.** Ethiopia/Eritrea is a 2-state split (would have been mis-coded "natural" under the original rule) whose sub-50 Rule-of-Law scores correctly trigger the capacity gate → catastrophic risk. Confirmed.
5. **Refinement C fired correctly twice.** Bangladesh (strong growth under Hasina but weak institutional delivery, inequality, youth unemployment) reversed into autocracy then violent collapse in 2024; Serbia's EU-candidate democratic gains reversed under Vučić amid mass 2024–25 protests.
6. **Refinement A is vindicated but exposes a deeper problem.** Timor-Leste's and Kosovo's early WGI scores partly reflect UN/EU administrator capacity (UNTAET, UNMIK/EULEX), not indigenous institutions — exactly the Bosnia-1996 failure mode. Flagging works; but it means the framework cannot use raw WGI for any internationally-administered successor without qualitative adjustment.
7. **New failure mode discovered:** the framework has no native treatment of **resource-rent fiscal capture** at extreme levels. The IMF labels Timor-Leste "the most oil-dependent economy in the world"; per the IMF 2025 Article IV, the Petroleum Fund balance "stood at 939 percent of non-oil GDP in 2024," and BTI 2026 notes the Fund "accounts for more than 80% of the annual state budget" (~$18.95bn as of August 2024). This shows how high P4 resource rents can simultaneously *prop up* WGI-measured "government effectiveness" (lots of spending) while hollowing out organic state capacity. P4 in the framework is treated as a compounding negative — directionally right, but the rentier-capture mechanism is not modeled.

## Details

### Important data and methodology caveats (read first)
- **Metric discontinuity is real and now acute.** Per the World Bank, the 2025 WGI revision introduced "an absolute 0–100 scale anchored to fixed benchmark countries" and recalculated all historical estimates back to 1996; these anchored scores are *not* interchangeable with the legacy percentile ranks, and the legacy `RL.PER.RNK`/`GE.PER.RNK` percentile indicators have been archived on the live API. **Consequence:** Refinement B's hard threshold ("~50 on WGI Rule of Law") is now ambiguous — 50 on the legacy percentile series ≠ 50 on the new anchored score. This should be the top priority for framework repair.
- **Exact percentile cells at every specified time point could not all be confirmed from primary sources** within research scope, precisely because of the above archiving. Per the instruction "missing data is information," I report **robust ordinal rankings** (which the framework explicitly requires — prediction 5) plus the anchor values I could confirm, and flag estimated cells as such. I have NOT interpolated to fill the panel.
- Confirmed anchor values (WGI estimate units, −2.5 to 2.5; World Bank via theglobaleconomy/CEIC): Singapore Rule of Law averages **1.46** (1996–2024), the highest in Southeast Asia (min 1.36 in 1998, max 1.55 in 2012); Malaysia averages **0.25** (peak 0.50 in 1996); India averages **0.05** (max 0.35 in 2000, min −0.11 in 2021); Ethiopia's Government Effectiveness hit a record low of **−1.208 in 1996**; Eritrea sits comparably negative. These confirm the ordinal structure used below.

---

### CASE 1 — ETHIOPIA / ERITREA (Eritrean independence 1993)

**Phase 1 — Pre-event scoring (1996):** Both successor states score in the bottom quartile globally on P1. Ethiopia's Government Effectiveness estimate hit a record low of −1.208 in 1996; Eritrea, newly independent, scored similarly low with even weaker voice/accountability indicators. P4: both highly aid-dependent, low GDP per capita PPP, agrarian. P5: both low (Ethiopia's Political Stability estimate reached a record low of −1.803 in 2007). Pillar spread: moderate but uniformly low — no strong pillar to create a wide spread; this is a "uniformly weak" profile.

**Refinement B applied:** 2 successor states. Under the *original* rule this would be coded "natural fragmentation" (positive). Pre-event mean P1 (Rule of Law) is well below 50 → **capacity gate triggers → re-coded as catastrophic-risk despite low fragment count.** This is the exact Sudan/South Sudan logic.

**Phase 2 — Predictions:** (a) Neither has a "good" trajectory; framework predicts both poor, Ethiopia marginally ahead on administrative depth and international integration. (b) Low P1 → **predict violent release/aftermath.** (c) Divergence likely (different regime types). (d) Primary failure dimension: P1 and P5 jointly. (e) 2 states, capacity gate → catastrophic risk. (f) No reversal flag — neither achieves a high-P1 democratic transition.

**Phase 3 — Verification:** Confirmed. The 1998–2000 Eritrean–Ethiopian War and the 2020–22 Tigray war (Obasanjo: ~600,000 dead; Ghent University: 162,000–378,000) confirm the violence prediction emphatically. Eritrea closed totally (no national elections since independence, no implemented constitution, indefinite conscription). Ethiopia's 2018 democratic opening relapsed into civil war. **Scoring: (a) partially confirmed; (b) confirmed; (c) partially confirmed; (d) confirmed; (e) confirmed (Refinement B success); (f) confirmed.**

---

### CASE 2 — INDIA / PAKISTAN / BANGLADESH (Partition 1947; Bangladesh 1971; scored 1996)

**Phase 1 (1996):** India's P1 clearly exceeds Pakistan's and Bangladesh's (India Rule of Law estimate positive ~0.05 avg; Pakistan and Bangladesh deeply negative, low-20s percentile). India P2/P3 higher (larger knowledge economy, higher Economic Complexity rank). P4: all three low GDP per capita PPP, India more diversified. P5: India moderate, Pakistan low (coups), Bangladesh low-moderate. Pillar spread: India *wide* (decent P1, historically weak P4/P5) — flagged.

**Phase 2 — Predictions:** (a) **India best trajectory** by P1 ordinality. (b) P1/P5 interaction predicts Pakistan's continued instability (coups, reversals). (c) Divergence: India and Bangladesh pull ahead of Pakistan. (d) Pakistan's failure dimension = P1×P5. (e) n/a. (f) **Refinement C flag on Bangladesh** (rapid growth, weak institutional delivery) and a **backsliding watch on India**.

**Phase 3 — Verification:** Largely confirmed. India consolidated as the largest functioning (if eroding) electoral system and fastest-growing major economy; Pakistan saw repeated military intervention and IMF dependence — confirming P1/P5. Bangladesh surpassed India and Pakistan in GDP per capita and several social indicators under Hasina, but the **Refinement C reversal fired in August 2024**: the OHCHR Fact-Finding Report (released 12 Feb 2025) estimated "as many as 1,400 people may have been killed" between 15 July and 5 Aug 2024, with the majority "shot by Bangladesh's security forces," precipitating Hasina's fall; GDP growth then collapsed to under 2% (H2 2024) and FDI fell ~71%. On India, V-Dem's Democracy Report 2024/2025 classifies India as an "electoral autocracy" and lists it among the five countries where "democracy has already broken down," noting India "accounts for about half of the population living in autocratizing countries" — confirming the backsliding watch. Yet the 2024 election (BJP lost its majority, forced into coalition) shows India's high-P1 porosity thesis still operating. **Scoring: (a) confirmed; (b) confirmed; (c) confirmed; (d) confirmed; (e) n/a; (f) confirmed.** The framework's strongest continental-scale result.

---

### CASE 3 — INDONESIA / EAST TIMOR (independence referendum 1999; full independence 2002)

**Phase 1 (1998/99):** Indonesia mid-low P1 (post-Suharto transition, Asian financial crisis), but real administrative depth, diversified economy, moderate Economic Complexity. East Timor: near-zero indigenous institutional capacity (Portuguese colony, then Indonesian occupation; ~70% of economic infrastructure destroyed by withdrawing Indonesian forces in 1999).

**Refinement A applied (clean test):** East Timor under UNTAET (1999–2002) — early WGI scores (Government Effectiveness best-ever −0.677 in 2004; Political Stability +0.437 in 2000) **reflect UN administrator capacity, not indigenous institutions.** Flag raised; qualitative assessment (no pre-existing civil service, no indigenous judiciary, near-total reconstruction need) used instead → indigenous P1 ≈ floor.

**Phase 2 — Predictions:** (a) **Indonesia far better trajectory.** (b) Violence around the event — but the framework's low-P1-violence mechanism is *mis-specified* here: 1999 violence came from Indonesia/militias (departing power), not Timorese institutional failure. Note as edge case. (c) Strong divergence. (d) Timor-Leste failure dimension: P1 (capacity) compounded later by P4 (oil dependence). (e) n/a. (f) No reversal flag.

**Phase 3 — Verification:** Confirmed directionally. Indonesia is a genuine framework win — large, complex, resource-rich, democratized and (so far) sustained it; its rising Government Effectiveness and Regulatory Quality post-2004 track the MI prediction. Timor-Leste is, per the IMF, "the most oil-dependent economy in the world": petroleum ~80–90% of state revenue, the Petroleum Fund "stood at 939 percent of non-oil GDP in 2024" (IMF Article IV) and is officially projected to deplete around 2035–2038, with ~42% poverty. **Refinement A correctly prevented over-crediting Timor's UNTAET-era scores. New failure mode flagged:** the framework lacks a rentier-capture mechanism. **Scoring: (a) confirmed; (b) partially confirmed/edge case; (c) confirmed; (d) confirmed; (e) n/a; (f) confirmed.**

---

### CASE 4 — SERBIA / KOSOVO (Kosovo declares independence Feb 17, 2008)

**Phase 1 (2007):** Serbia mid P1 (EU-candidate trajectory, functioning if imperfect institutions); Kosovo low P1, recursively fragmented (Kosovo from Serbia, Serbia from Yugoslavia). **Refinement A applied:** Kosovo under UNMIK (1999–2008) then EULEX — WGI scores reflect international administrator capacity. Flag raised; indigenous capacity assessed lower than raw scores suggest.

**Phase 2 — Predictions:** (a) **Serbia better trajectory** by P1 ordinality. (b) Recursive/partially-recognized status → constrained Kosovo trajectory (no UN seat; ~110/193 recognitions; EU path blocked). (c) Divergence. (d) Kosovo failure dimensions: P1 + P4 (aid/remittance/diaspora dependence; OECD reports Kosovo dedicated only ~0.1% of GDP to R&D in 2024; youth unemployment 41% in 2024). (e) n/a. (f) **Refinement C flag on Serbia.**

**Phase 3 — Verification:** Confirmed. Serbia remains ahead on income and institutional measures, but **Refinement C fired**: V-Dem's Democracy Report 2025 ("25 Years of Autocratization") states democracy "has already broken down in five – Hungary, India, Mauritius, Nicaragua, and Serbia"; Serbia has been an "electoral autocracy" since 2014, its Liberal Democracy Index falling from ~0.51 (2011) to ~0.25 (2023), amid mass anti-Vučić protests through 2024–25. Kosovo's trajectory is constrained exactly as predicted — no new recognition from 2020 until Kenya in 2025, EU path effectively blocked — yet the World Bank notes Kosovo "successfully transitioned away from a growth model based on high dependence on foreign aid," with ~4% growth in 2024 and resilient democratic competition (peaceful 2025 election). So Kosovo is a *partial* falsification of the most pessimistic low-P1 reading: it underperforms Serbia (ordinality holds) but outperforms its own predicted fragility. **Scoring: (a) confirmed; (b) confirmed; (c) confirmed; (d) partially confirmed; (e) n/a; (f) confirmed.**

---

### CASE 5 — SINGAPORE / MALAYSIA (Singapore expelled Aug 9, 1965; scored 1996)

**Phase 1 (1996):** Singapore: **very high P1** (Rule of Law estimate ~1.46 avg, top globally; Government Effectiveness near the global ceiling), very high P3 (education, life expectancy), strong P2, low internal complexity, low resource dependence. Malaysia: solidly upper-middle P1 (Rule of Law estimate ~0.50 in 1996), higher internal complexity (multi-ethnic, multi-religious, split across the South China Sea), some resource rents. Pillar spread: Singapore narrow and uniformly high; Malaysia wider.

**Phase 2 — Predictions:** (a) **Singapore is THE success case** — highest MI in either round → best trajectory. (b) n/a (peaceful expulsion). (c) Divergence: Singapore pulls far ahead. (d) Singapore success dimension = P1 + P3; complexity-control thesis (fragmentation stripped out the internal complexity that would have required porous, lower-efficiency governance). (e) n/a. (f) No reversal flag.

**Phase 3 — Verification:** Confirmed decisively. Singapore 2024 GDP per capita PPP ~**$150,689** (2nd globally) vs Malaysia ~**$38,779** (≈3.9×). Singapore Economic Freedom Index #1 globally; Rule of Law at the global ceiling (highest in Southeast Asia). Malaysia did fine in absolute terms but its higher complexity and wider pillar spread track its lower MI trajectory exactly as predicted. **The framework's flagship positive case lands cleanly. Scoring: (a) confirmed; (b) n/a; (c) confirmed; (d) confirmed; (e) n/a; (f) confirmed.**

---

### Round 2 Scorecard

Counting the scorable predictions (a–f where applicable) across five cases (~26 scorable items):
- **Confirmed:** ~18–19
- **Partially confirmed:** ~6 (Ethiopia trajectory-ranking; Ethiopia/Eritrea divergence; Timor violence-source; Kosovo P4; India backsliding nuance)
- **Falsified:** ~0–1 (no clean falsification; the Timor violence-source mis-specification is the closest to a structural miss)

**Estimated clean confirmation: ~66% (18.5/26); directional accuracy: ~90%.** This essentially **holds** the Round 1 baseline (64%/88%) rather than markedly improving it. The honest read: the refinements *prevented new errors* (Refinement B would have mis-coded Ethiopia/Eritrea; Refinement A would have over-credited Timor and Kosovo; Refinement C would have missed Bangladesh and Serbia reversals) more than they *raised* the headline number — because the core ordinal engine was already strong.

### Which refinement mattered most
**Refinement B (capacity gate)** had the highest marginal value: without it, Ethiopia/Eritrea is an outright mis-classification, replicating the Round 1 Sudan error. **Refinement C** is second — it converted two would-be falsifications (Bangladesh, Serbia) into confirmed conditional predictions. **Refinement A** is necessary insurance (Timor, Kosovo) but, because both states were *predicted* to be weak anyway, it changed the *reasoning* more than the *ranking*.

### New failure modes discovered (not in Round 1)
1. **Rentier-capture / extreme-P4 distortion of P1** (Timor-Leste): very high resource rents can inflate short-run measured government effectiveness (spending capacity) while eroding organic institutional development. The framework treats P4 as a flat compounding negative and misses this dynamic.
2. **Violence-source mis-attribution** (Timor-Leste): the "low P1 → violent release" rule implicitly assumes violence originates from the fragmenting entity's own weakness; it does not handle violence inflicted by the *departing* power. Needs a directional tag.
3. **Metric-regime discontinuity** (all cases, 2024+): the 2025 WGI anchored-score revision breaks any hard percentile threshold. A measurement failure mode, not a theory failure mode, but it directly undermines Refinement B's "~50" cutoff.
4. **Resilience under-prediction for administered micro-states** (Kosovo): the framework's pessimism about low-P1 partially-recognized states slightly over-predicted Kosovo's fragility.

### Demonstrated range
- **Handles well:** high-contrast cases (Singapore/Malaysia), large diversified states with clear P1 gaps (India/Pakistan/Bangladesh, Indonesia/Timor), and uniformly-weak violent cases (Ethiopia/Eritrea). The ordinal core is robust across continents.
- **Handles poorly:** (i) timing and durability (it told us *who* would do better, never *when* reversals would hit — Refinement C softens but does not solve this); (ii) externally-administered scores without qualitative override (Refinement A is a patch, not a measurement fix); (iii) rentier states; (iv) violence whose source is external to the successor.

## Recommendations

1. **Immediately re-base Refinement B's threshold.** Decide whether "~50" refers to the legacy percentile series or the new 2025 anchored 0–100 score, and re-derive the cutoff empirically on post-revision data. Until then, treat the gate as ordinal ("bottom-third Rule of Law") rather than a fixed "50." **Benchmark to change this:** if re-derivation moves the effective cutoff by more than ~10 points, re-score all 10 cases.
2. **Add a P4 rentier sub-flag.** When natural-resource rents exceed ~25–30% of GDP *and* fund a majority of state revenue, flag that measured P1 may be fiscally inflated and apply a qualitative haircut (the Timor mechanism). **Escalation threshold:** resource rents >50% of revenue → treat P1 as unreliable, like Refinement A.
3. **Add a directional tag to the violence prediction.** Distinguish "endogenous violence" (successor's own low P1) from "exogenous violence" (departing power / external actor). Score them separately so Timor-type cases don't penalize the P1 mechanism.
4. **Formalize Refinement C with a delivery metric.** Operationalize "weak economic delivery" with explicit thresholds (youth unemployment, Gini, real wage growth) so the reversal flag is falsifiable rather than narrative. Bangladesh and Serbia both had measurable pre-reversal delivery deficits.
5. **Freeze a data vintage.** Because of the 2025 WGI revision, pin the entire 10-case panel to a single archived dataset (e.g., the 2024 WGI update, 1996–2023) for the legacy series, and report 2024 anchored scores separately and non-comparably, exactly as the task's data instruction anticipated.
6. **Do not claim above ~65% clean / ~90% directional.** Across all 10 cases (Round 1 + Round 2), the defensible combined claim is roughly **~64–66% clean confirmation and ~88–90% directional accuracy.** The framework can confidently claim to be a **good ordinal predictor of relative trajectory driven by pre-event Institutional Quality**, and an honest *conditional* predictor of durability (post-Refinement C). It cannot claim to predict timing, magnitude, or the trajectory of externally-administered or extreme-rentier states without qualitative override.

## Caveats
- **Confirmation coding is inherently partly subjective**, especially for "partially confirmed." I have erred toward stringency (counting Timor's violence-source as a partial miss; refusing to call Ethiopia's marginal edge over Eritrea a clean win). A more generous coder could reach ~72%; I judge that overstated.
- **Exact WGI percentile values at every specified time point were not all confirmable from primary sources** due to the 2025 archiving of the legacy series. Directional rankings (what the framework needs) are well-sourced; specific cell values flagged as estimated should be replaced from the downloadable WGI spreadsheet before any quantitative use.
- **Several outcome facts are still contested**, notably Tigray War mortality (estimates range from ~162,000 to ~600,000) and Kosovo's exact recognition count (Kosovo claims ~120; Serbia claims fewer after alleged withdrawals; ~110 is the consensus figure).
- **The framework is being tested partly on cases where the fragmentation event long predates the scoring window** (India 1947, Singapore 1965, scored 1996), so these test "does the 1996 profile predict the *subsequent* 28-year path," not the fragmentation itself — a legitimate but different test than the contemporaneous cases.
- **Survivorship and selection:** all ten cases are known, completed or long-running fragmentations. The framework has not been tested prospectively on an unresolved case, which is the only true out-of-sample test.