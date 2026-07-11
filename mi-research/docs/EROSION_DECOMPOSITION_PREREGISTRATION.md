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

## B2 — Composite dysfunction outcome (committed at Component B, before grading)

*Placeholder — the binding spec is committed separately in this file's B2 section
prior to running B2. See commit "prereg(B2): …".*

## C1 — Revealed-outcome P1 specification (committed at Component C, before grading)

*Placeholder — the binding spec is committed separately in this file's C1 section
prior to running C1. See commit "prereg(C1): …".*
