# Erosion Decomposition — Pre-Registration

**Purpose.** Diagnose *why* the MI's institutional signal erodes in the modern era
(Findings 2/7 — the ~150-year erosion curve, Pearson r=−0.847, p=0.033; and
Finding 8 — the ESI system-level null). The organizing thesis: the post-1945
international system is structurally analogous to the dawn of organized polities
(mass state creation from near-zero institutional baselines) *while simultaneously
blocking* the historical mechanisms (conquest, failure→death) that forced
institutional development. Three independent, separately-tested components:

- **A — Denominator dilution.** The sample filled with institutionally-young states.
- **B — Consequence elimination.** State death became structurally impossible after 1945.
- **C — Measurement regime change.** Perception-based P1 (WGI) lags functional reality.

**Rules (binding).** (1) Test the three components *independently*; do not combine
into a composite variable. (2) Report all numbers; no cherry-picking. (3) This
session is **diagnosis only** — no framework fixes. (4) Crisis-based tests reuse the
committed temporal-holdout crisis definition (`ucdp_onset OR crag_default`); the B2
dysfunction outcome is *additional*, not a replacement. (5) This document + the
three coded specs are committed **before** any outcome split is computed.

Freeze order (separate commits): **A1 classification → B2 dysfunction def → C1
revealed-P1 spec**, each before the corresponding outcome analysis.

---

## A1 — State-formation classification (committed here)

**Code + data (the actual pre-registration):**
`scripts/robustness/formation_classify.py` → `data/robustness/formation/state_formation.json`.

**Universe.** The 167 sovereign states in the union of the erosion panel (V-Dem
rule-of-law ∩ Maddison GDP at anchors 1816…1990) and the temporal holdout. Hong
Kong is excluded (not a sovereign state; absent from COW).

**Entry-year anchor.** Correlates of War State System Membership (`states2016.csv`,
fetched from correlatesofwar.org), keyed to ISO3 via the repo's existing
`build_ccode_iso()` (name-based, 0 unmapped ccodes).

**Groups (primary).**

| group | criterion | n |
|---|---|---|
| **mature** | population had prior multi-generational experience operating institutions at/near current scale: pre-1816 sovereign; organic unification (DEU, ITA); revolution from internal traditions (USA); treaty partition with deep continuity (NOR 1905, CZE/SVK 1993); never-colonized deep states (JPN, CHN, THA, IRN, ETH, NPL, AFG, TUR, KOR); settler dominions whose admin class stayed (CAN, AUS, NZL, ZAF); brief-but-real interwar sovereignty (Baltics). | 54 |
| **post_colonial** | independence ≥1945 from a border-drawing colonial power that removed the administrative class, OR imperial-dissolution successor with no prior independent institutional tradition at current scale (Central Asian republics; Dayton BiH). | 93 |
| **early_post_colonial** | Iberian/French-colonial (Latin-American) bloc independent c.1804–1903 — post-colonial by origin, 120–220y of subsequent sovereign development (brief's explicit third group). | 20 |

**India (special case).** IND is coded `post_colonial` with `alt_group=mature`
(deep pre-colonial traditions but colonial borders + unified administration). Per
the brief, A2/A3 run India in **both** groups separately.

**Sensitivity flags.** 26 states carry an `alt_group` naming the group they move to
under sensitivity re-runs. These are the genuinely ambiguous cases — national-revival
Ottoman successors (GRC, BGR, ROU, ALB), post-Soviet European dissolution
(UKR, ARM, GEO, AZE), Yugoslav successors (SVN, HRV, MKD, BIH), Gulf protectorates
(KWT, QAT, BHR, ARE), deep-state/protectorate MENA (EGY, MAR, TUN, OMN, SAU, YEM),
and settler/founded edges (LBR). Every call carries a one-line rationale in the JSON
`note` field. **The load-bearing test (A2) must be reported both at face value and
with all flagged cases moved to `alt_group`.** If the A/mature-vs-post_colonial split
depends on the ~26 edges, that is reported as a weakness, not hidden.

**Per-anchor composition (mechanical, pre-outcome — the dilution the hypothesis
predicts):** mature share of panel states falls monotonically 0.83 (1816) → 0.34
(1990); combined post-colonial share rises 0.17 → 0.66, with the discontinuity at
1940→1970 (decolonization: 8→71 `post_colonial` entrants). This is a property of the
sample, computed before any outcome is touched.

---

## B2 — Composite dysfunction outcome (BINDING — committed before grading)

**Motivation.** Component B claims the MI's signal was calibrated against a
consequence — state death — that the post-1945 order eliminated, so institutional
failure now yields *chronic dysfunction in a permanent territorial container*
rather than death/partition/absorption. If the structural relationship is intact
but the consequence changed, then MI structural scores should still predict
negative outcomes short of state death. This test re-runs the temporal holdout with
a broader **dysfunction** outcome. It does **not** replace the committed crisis
definition — it is an additional outcome variable.

**Composite dysfunction = ANY of the four sub-outcomes within the validation
window** (2004→2024 and 2012→2024), pre-registered here before grading:

| sub-outcome | operationalization | source | window coverage |
|---|---|---|---|
| D1 democratic backsliding | Polity2 falls ≥ 3 points from its base-year value at any point in the window | Polity5 (`p5v2018.xls`, `polity2`) | 2004→2018 / 2012→2018 (Polity5 ends 2018 — coverage caveat, tail of window unobserved) |
| D2 economic deterioration | real GDP-pc falls ≥ 15% from its within-window peak | WB `NY.GDP.PCAP.PP.KD` | full window |
| D3 conflict onset | UCDP/COW armed-conflict onset in window (the `ucdp` field already in the holdout panel) | UCDP/PRIO ACD v24.1 | 2004→2023 / 2012→2023 |
| D4 fragility increase | FSI rises ≥ 10 points from base to latest available | Fund for Peace FSI (`fsi.csv`) | **2012 window only** (FSI series starts 2012) |

**Robustness variant (reported alongside, not replacing):** because Polity5 ends in
2018, a **V-Dem `libdem` backsliding** variant of D1 is also computed — `libdem`
falls ≥ 0.10 (0–1 scale; ≈ a 3-point Polity move) at any point through 2024 — using
the in-repo `vdem_longrun.json`, which covers the full window. Both the Polity and
the V-Dem composite are reported.

**Test.** Re-run the frozen holdout mechanics: for each window, compute the
predictive power (AUC, and logistic gap-coefficient) of the MI structural signals
(the P4−P1 durability **gap**, and neg-P1 institutional level) against the composite
dysfunction outcome, and against GDP-pc alone. Report AUC, sensitivity/specificity
of the `elevated` gate flag, and the gap vs wealth AUC delta. **What recovers the
signal:** if the structural gap predicts *dysfunction* significantly better than GDP
alone — even where it did not beat GDP on the death/default-coupled crisis outcome —
the signal is intact and the modern order has merely decoupled institutional failure
from terminal outcomes. **B's estimated share of erosion** = the gap in structural
predictive power between the crisis-definition holdout and the dysfunction-definition
holdout (how much of the "lost" signal the broader outcome recovers).

Coverage caveats (D1 tail, D4 single-window) are disclosed, not worked around; the
composite is ANY-of so a truncated sub-outcome only *weakens* detection (biases
against the hypothesis).

## C1 — Revealed-outcome P1 specification (BINDING — committed before grading)

**Motivation.** The MI's P1 pillar uses WGI — *perceptions* of governance from
expert surveys. The 25-case ancient validation scored institutions from *functional*
evidence (tax collection, legal codification, administrative records). Perceptions
lag reality: a functionally-decaying state can score well on WGI for years
(reputation + path dependence). If modern P1 is a laggier proxy for true
institutional quality, the temporal-holdout signal degrades without any change in
the underlying structural relationship.

**Revealed-outcome P1 at 2004 vintage.** Reuse the exact Finding-1 substitution seam
(`scripts/robustness/substitute.py`): replace the three WGI P1 keys
(`gov_effectiveness`, `rule_of_law`, `regulatory_quality`) in the flat indicator
dict with a **0–100 cross-country percentile rank** of a revealed state-capacity
series, then re-score with unmodified scoring math. All other pillars untouched.

**Indicators available at 2004** (fetched as full time series from WB API):

| revealed P1 series | WB code | note |
|---|---|---|
| tax revenue % GDP (fiscal/state capacity) | `GC.TAX.TOTL.GD.ZS` | primary |
| govt education expenditure % GDP | `SE.XPD.TOTL.GD.ZS` | secondary |

The Finding-1 LPI substitute is **excluded at 2004** — the LPI series begins 2007, so
it is not available at the 2004 prediction origin (honest coverage constraint, not a
choice). Each country uses the nearest year in **[2002, 2006]** to maximize coverage;
the year used is recorded.

**Variants (all reported):** `P1←tax`, `P1←edu`, `P1←tax+edu composite` (mean of the
two percentile ranks). For each, rebuild the 2004 MI scores, run the **same** frozen
holdout `predict()`, and grade against the **same committed 2004→2024 crisis
outcomes** as the perception-P1 holdout. Compare AUC (of the `elevated`/vuln gate, the
P4−P1 gap, and neg-P1), sensitivity, specificity, and lift over base rate against the
perception-based P1 holdout.

**C's estimated share of erosion** = the AUC/lift gain of revealed-P1 over
perception-P1 in the holdout. If revealed-P1 outperforms, perception measurement is a
bottleneck (C contributes). If it performs the same or worse, C is not a contributor.

## C2 — Perception-lag detection (specified with C1)

For countries with a crisis in 2010–2024, plot the WGI (`wgi_full_panel.json`,
government-effectiveness / rule-of-law) trajectory vs the revealed-indicator (tax %GDP)
trajectory over the ~10 pre-crisis years. Test whether functional indicators decline
**earlier** than WGI (perception lag) — operationalized as: mean lead/lag of the
revealed-series inflection vs the WGI inflection before crisis onset, and the fraction
of crisis countries where the revealed series had already declined while WGI was still
flat. Descriptive (small n); reported with counts, not over-claimed.
