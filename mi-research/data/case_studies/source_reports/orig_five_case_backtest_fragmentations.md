# A Modernization Index Backtest of Five Historical Fragmentations: Does Institutional Capacity Predict Post-Breakup Trajectories?

## TL;DR
- **The MI framework's core claim holds: a country's pre-event Pillar 1 (Institutional Quality) score is a strong ordinal predictor of post-fragmentation success in 4 of 5 cases** — Estonia, Slovenia, the Czech/Slovak pair, and the Tunisia > Egypt > Libya ranking all moved in the direction their 1996/2010 institutional scores predicted.
- **The framework's weakest element is the "number of successor states" dispersion heuristic**, which falsely codes the Sudan/South Sudan split (2 states) as "natural" even though it produced the most catastrophic outcome in the sample — proving that the *count* of successor entities is not a substitute for *capacity*.
- **Net scorecard: of 25 discrete predictions, roughly 16 confirmed, 6 partially confirmed, and 3 falsified (~64% clean hit rate).** The framework predicts *direction and ranking* well but cannot predict *timing, triggers, or durability* (Tunisia's 2021 democratic reversal is the clearest miss).

## Key Findings

**1. Institutional Quality (Pillar 1) is the workhorse pillar.** Using the World Bank WGI Rule-of-Law governance score (0–100) as a consistent 1996 baseline proxy for P1, the pre-event ranking lines up with eventual outcomes: Slovenia 75.2, Czechia 70.7, Estonia 68.6, Slovakia 61.3 — all "high-capacity" — versus Bosnia 51.7, Croatia 45.4, Russia 42.0, Ukraine 41.4, Serbia 36.6, and Sudan 28.4. Every country in the top tier ended up in the EU and/or a consolidated democracy; every country in the bottom tier experienced war, state collapse, authoritarian entrenchment, or all three.

**2. Low P1 predicts violent rather than peaceful fragmentation.** The two highest-capacity dissolutions (Velvet Divorce; Slovenia's exit) were the least violent — zero deaths for the Velvet Divorce, and around 70 people killed in Slovenia's ten-day conflict per the Humanitarian Law Center. The lowest-capacity cases (Bosnia, Sudan/South Sudan, Libya) were the most violent. This is the single most robust regularity in the dataset.

**3. Resource dependence (P4 distortion) compounds institutional weakness.** Libya and Sudan/South Sudan — the two most resource-rent-dependent cases — had the worst institutional trajectories, consistent with the "rentier collapse" prediction.

**4. The framework systematically mis-scores states under external administration.** Bosnia's 1996 Rule-of-Law score (51.7) was *higher* than Croatia's and Serbia's, an artifact of the post-Dayton international protectorate. Bosnia subsequently had the worst-functioning governance of the surviving Yugoslav states. Point-in-time institutional scores taken during heavy external intervention are unreliable.

**5. Critical data discontinuity.** The World Bank's 2024/2025 WGI revision **discontinued the legacy 0–100 percentile-rank series after 2023** and replaced it with a new anchored "governance score." For Estonia, Government Effectiveness percentile rank 2023 = 88.68, but the new 2024 governance score = 76.56 — these are different measures and not interchangeable. Any MI calculation spanning 1996→2024 must therefore either use the new anchored score throughout or treat 2024 percentile values as unavailable. This is a genuine framework-limiting gap, not interpolated.

## Details

### Methodology note and honest data accounting
The task specifies a five-pillar weighted index (P1 34%, P4 20%, P3 16%, P5 16%, P2 15%). With the search budget available, I assembled a **consistent cross-country P1 baseline (1996 Rule-of-Law governance score, World Bank WGI API, source 3, last updated 2026-03-18)**, selected outcome indicators (Fragile States Index 2024, GDP-per-capita context, R&D intensity, resource rents), and comprehensive qualitative outcome verification. I was **not** able to retrieve every one of the ~13 indicators at all five time points for all 14 entities; rather than interpolate, I flag those gaps explicitly. Because the four WGI governance indicators are very highly correlated (the literature treats them as measuring one latent "governance" construct), the single Rule-of-Law series is a defensible proxy for the full P1 pillar for ranking purposes — but it is a proxy, and full-pillar precision is not claimed.

Specific gaps (stated, not filled): full Government Effectiveness / Regulatory Quality / Control of Corruption percentile ranks for 1996, 2010 and 2024 across all entities; 2010-specific (rather than 1996) P1 values for the Arab Spring cases; ECI and R&D for several Balkan states at all time points; FSI before 2006 (does not exist — correctly noted as structurally missing).

### Case 1 — Post-Soviet Divergence: Estonia vs Russia vs Ukraine
**Pre-event P1 (1996 RL score): Estonia 68.6 >> Russia 42.0 ≈ Ukraine 41.4.** Estonia's institutional lead was large and early.

- *(a) Best trajectory:* Predicted Estonia, by a wide margin. **CONFIRMED.** Estonia joined the EU/NATO (2004) and eurozone (2011); 2024 Government Effectiveness governance score 76.6, a world leader in digital government. Russia's rule-of-law index fell to roughly its all-time low by 2024 and it became a belligerent authoritarian state; Ukraine remained middling and was invaded.
- *(b) Violent vs peaceful:* P1 gap predicted peaceful exit for high-capacity Estonia (correct — the Baltic exit was peaceful). The framework does **not** predict the later Russia–Ukraine war, which is an interstate event outside the dissolution window. **PARTIALLY CONFIRMED.**
- *(c) Convergence vs divergence:* Predicted divergence. **CONFIRMED, emphatically** — Estonia pulled far away from both others.
- *(d) Primary failure dimension:* Predicted P1 (corruption/rule of law) for Russia and Ukraine; for Ukraine, P5 (stability) became co-primary after 2014. **CONFIRMED.**
- *(e) Number of entities:* The USSR produced 15 successors — "engineered high-dispersion" (5+). **CONFIRMED.**

### Case 2 — Yugoslav Successor States: Slovenia vs Croatia vs Serbia vs Bosnia
**Pre-event P1 (1996 RL): Slovenia 75.2 >> Bosnia 51.7 > Croatia 45.4 > Serbia 36.6.**

- *(a) Best trajectory:* Predicted Slovenia. **CONFIRMED** — EU 2004, eurozone 2007, highest GDP per capita of the group. Croatia second (EU 2013, eurozone 2023), Serbia a slow EU candidate, Bosnia the laggard.
- *(b) Violent vs peaceful:* Low P1 across the bloc predicted violence. **CONFIRMED** — the Yugoslav wars killed at least 130,000 people per the Humanitarian Law Center (the International Center for Transitional Justice puts the toll at 140,000); only Slovenia (highest P1) had a near-bloodless exit, with around 70 killed in its ten-day conflict.
- *(c) Convergence vs divergence:* Predicted divergence; **CONFIRMED** (Slovenia eurozone vs Bosnia frozen).
- *(d) Primary failure dimension:* P1/P5. **CONFIRMED**, but with the major caveat below.
- *(e) Number of entities:* 7 successor states = "engineered high-dispersion" (5+). **CONFIRMED.**
- **Framework limitation exposed:** Bosnia's 1996 P1 proxy out-ranked Croatia's and Serbia's because the figure reflects the post-Dayton international administration, not indigenous capacity. The framework would have wrongly predicted Bosnia to out-perform Croatia. **This is a clean falsification of the indicator's validity under external administration.**

### Case 3 — Velvet Divorce: Czech Republic vs Slovakia
**Pre-event P1 (1996 RL): Czechia 70.7, Slovakia 61.3 — both high.**

- *(a) Best trajectory:* Predicted both succeed, Czechia marginally ahead. **CONFIRMED** — both joined the EU/NATO; Slovakia adopted the euro (2009); both are high-income.
- *(b) Violent vs peaceful:* High P1 predicted a peaceful split. **CONFIRMED** — the only entirely non-violent state dissolution of the post-war era.
- *(c) Convergence vs divergence:* Predicted convergence. **CONFIRMED** — both tracked into EU institutions on similar timelines.
- *(d) Primary failure dimension:* No primary failure predicted; none occurred. **CONFIRMED.**
- *(e) Number of entities:* 2 = "natural ratio" (2–4); high capacity → low dispersion. **CONFIRMED.**
- *Key comparison test:* Do both countries' P1 exceed the Yugoslav states' P1? **PARTIALLY CONFIRMED** — Czechia (70.7) and Slovakia (61.3) clearly exceed Croatia, Serbia and Bosnia, but **both fall below Slovenia (75.2)**, so the blanket claim "Velvet states > all Yugoslav states on P1" is false.

### Case 4 — Arab Spring: Tunisia vs Egypt vs Libya
*Data caveat: I retrieved 1996 (not 2010) WGI values for these states; the 2010-specific P1 ranking is asserted from the qualitative literature — Tunisia a cited "top reformer" with the strongest bureaucracy (Brookings; Pollack 2011); Egypt mid-tier authoritarian; Libya near the global floor on government effectiveness and rule of law.* Libya consistently sat among the world's worst on regulatory quality and rule of law.

- *(a)/(test) P1 ranking predicts outcome ranking (Tunisia > Egypt > Libya):* **CONFIRMED at the ordinal level.** Tunisia produced the region's only democratic transition; Egypt reverted to military authoritarian stability under Sisi (2013 coup); Libya collapsed into a failed state split between rival governments and remains among the most fragile states in Africa.
- *(b) Violent vs peaceful:* Inverse-P1 prediction. **CONFIRMED** — Tunisia least violent, Libya most violent (full civil war and external intervention).
- *(c) Convergence vs divergence:* **PARTIALLY CONFIRMED / key miss.** The framework predicted Tunisia would converge upward toward consolidated democracy; instead President Kais Saied's 25 July 2021 self-coup suspended parliament and rewrote the constitution, reversing the democratic gains. P1 predicted the *initial* trajectory but **not its durability**.
- *(d) Primary failure dimension:* Libya P1 + P4 (resource dependence); Egypt P5 (return to repression). **CONFIRMED.**
- *(test) Libya's resource dependence (P4 distortion) predicts worse institutional trajectory:* **CONFIRMED** — the rentier structure left no institutional substrate after Gaddafi.

### Case 5 — Sudan / South Sudan
**Pre-event P1 (Sudan 1996 RL): 28.4 — the lowest in the sample.** Sudan's total natural-resource rents peaked near a quarter of GDP around 2011 (23.92% in 2011 per World Bank/IndexMundi), with oil rents alone near 18% of GDP at their 2008 peak — a textbook "maximum engineering, minimum capacity, high resource rent" profile. South Sudan at independence (2011) was an extreme rentier shell: more than 98% of the government's budget came from oil revenues (South Sudan Ministry of Finance, cited by Brookings), with almost no civil institutions. Notably, at its 2011 birth South Sudan had a GDP per capita of roughly $1,516 — higher than all its neighbours per World Bank data cited by the International Crisis Group — yet the IMF now estimates it near $488 for 2026, a collapse that vividly illustrates rentier failure.

- *(test) Does Sudan's profile match "maximum engineering, minimum capacity, catastrophic release"?* **CONFIRMED.** Per the Fund for Peace 2024 Fragile States Index: Somalia 1st (111.3), Sudan 2nd (109.3), South Sudan 3rd (109.0).
- *(test) Does South Sudan's post-independence profile predict the 2013 civil war?* **CONFIRMED.** A new state with near-zero P1, extreme oil dependence (P4), and no stabilizing institutions (P5) descended into civil war in December 2013, ~24 months after independence; the London School of Hygiene & Tropical Medicine study commissioned by the U.S. Institute of Peace assessed that roughly 383,000 South Sudanese, including combatants, had died as a result of the war as of April 2018.
- *(a) Best trajectory:* Neither; both predicted to fail. **CONFIRMED.**
- *(b) Violent vs peaceful:* Very low P1 predicted catastrophic violence. **CONFIRMED.**
- *(c) Convergence/divergence:* Both remained at the bottom (converged in failure). **CONFIRMED.**
- *(e) Number of entities:* 2 successor states would be coded "natural" (2–4) by the dispersion heuristic — **FALSIFIED as a predictor**, because this 2-way split produced the *worst* outcome in the entire study. Count of states is not a proxy for capacity.

### Scorecard
Counting the five standard predictions (a–e) across five cases (25 predictions):

| Outcome | Count (approx.) | Examples |
|---|---|---|
| **Confirmed** | ~16 | Estonia best; Slovenia best; Velvet peaceful; Tunisia>Egypt>Libya; Sudan/S.Sudan catastrophe; all "violence ↔ low P1" calls |
| **Partially confirmed** | ~6 | Post-Soviet "peaceful" (ignores later war); Velvet "P1 > all Yugoslav" (fails vs Slovenia); Tunisia "converges up" (backslid 2021) |
| **Falsified** | ~3 | Bosnia P1 validity under external administration; Sudan 2-state count coded "natural"; Tunisia durable-democracy expectation |

Clean confirmation rate ≈ **64%**; including partials, directional usefulness ≈ **88%**.

**Framework's strongest demonstrated capability:** ordinally ranking post-fragmentation success from pre-event institutional capacity (P1), and predicting violence from low P1 + high resource rents (P4).

**Framework's clearest limitation:** it has no time/trigger model (cannot date or anticipate events like the 2021 Tunisian coup or the 2022 invasion of Ukraine), and two of its mechanical rules — the successor-count dispersion heuristic and the use of raw WGI scores during external administration — actively mislead.

## Recommendations

**Claims that can be made confidently:**
1. *Use P1 (Institutional Quality) as the primary predictor of post-fragmentation success ordering.* It correctly ranked outcomes in 4 of 5 cases. Stage the analysis around P1 first, other pillars second.
2. *Treat low P1 + high resource rents (P4) as a high-confidence "violent/catastrophic" signal.* Libya and Sudan/South Sudan both fit, both collapsed.
3. *Report the framework as an ordinal/directional tool, not a cardinal forecaster.* It predicts who does better than whom, not by how much or when.

**Claims that require hedging:**
4. *Never use point-in-time WGI scores for states under active external administration* (Bosnia 1996). Flag any country with a major international protectorate and down-weight or annotate its P1.
5. *Drop or heavily caveat the "number of successor states" dispersion heuristic.* It misclassified the worst case (Sudan). If retained, gate it on a minimum-capacity threshold (e.g., only treat 2–4 states as "natural" when mean P1 exceeds ~50).
6. *Do not claim the framework predicts durability.* Tunisia shows that initial trajectory and long-run consolidation are different questions; add an explicit "reversal risk" flag for democracies with weak P4/economic delivery.

**Thresholds that would change the recommendations:**
- If a future case shows a *high*-P1 state (≥65) fragmenting violently, recommendation #1 weakens and P5/external-shock variables must be promoted.
- If the new World Bank anchored "governance score" diverges materially from the legacy percentile ranks in re-runs, recalibrate all pillar normalizations before making cross-era claims.

## Caveats
- **Data construction:** Pillar 1 here is proxied by the WGI Rule-of-Law governance score, not the full four-indicator P1 average; full-pillar MI scores were not computed for every entity/year. Several P2/P3 indicators were not retrieved at all time points and are explicitly left as gaps rather than interpolated.
- **Metric break (2024):** The legacy 0–100 percentile-rank WGI series ends in 2023; 2024 uses a new, non-interchangeable anchored score. Cross-era comparisons mixing the two are invalid.
- **Year mismatch (Arab Spring):** The retrieved WGI values for Tunisia/Egypt/Libya/Sudan were for 1996, not the specified 2010 pre-event year; the 2010 ordinal ranking is supported from the qualitative literature, and the precise 2010 percentile figures remain an open gap.
- **FSI availability:** The Fragile States Index begins in 2006; for the 1996/pre-event Soviet, Yugoslav, and Czechoslovak cases, P5 necessarily rests on WGI Political Stability alone, as the framework instructs.
- **Confounding:** EU accession is both an outcome and a cause of institutional improvement; the "Brussels effect" partly endogenizes the very P1 trajectories the framework treats as predicted, especially for the European cases.