# Capital-Suppression Sub-Law — Pre-Registration

**Purpose.** The convergence narrative (`docs/ROBUSTNESS_RESULTS.md` §"Convergence")
and the capital-hubs atlas (`docs/capital_hubs_atlas.md`) carry an **inference**: that
the modern capital system is an *engineered suppression mechanism*, so the fragmentation
sub-law **"release is proportional to how long the fracture was held shut"** (demonstrated
[curated] on state break-ups: violent ≈53 yrs held → 5.6 successors vs peaceful ≈10 yrs →
3.3) should extend to the **economic/capital domain**. That extrapolation is currently
labeled *"grounded but not confirmed."* This program **tests it directly** and commits, in
advance, to **promote it** if it passes or **retire it to context-only** if it fails.

**The claim under test (magnitude limb of the suppression→release sub-law):**

> When an economy is held in a configuration where wealth exceeds what its institutions
> would sustain (a positive economy–institution gap), the **longer** that configuration is
> held, the **larger** the eventual release (economic collapse and/or political rupture).

This is the country-level, testable instantiation of the system-level (n=1, untestable)
capital-suppression thesis. The **dispersion limb** (grown-vs-designed CV dial) is NOT
tested here — only magnitude, which is what "proportional to how long it was held" claims.

---

## Binding rules

1. **Pre-register before running** (this file, sha256 on commit).
2. **Test 1 is the gate.** If duration does NOT positively predict release magnitude
   (Spearman ≤ 0 or p ≥ 0.05), OR the effect vanishes when peak-gap magnitude is
   controlled, the sub-law **does not extend to the capital domain** → **retire the
   capital-suppression thesis to context-only** in the atlas and grand synthesis.
3. **Report all results and all sensitivity cuts**, including a null. A null here is a
   real finding: it would mean active-stabilization / self-reform (which the repo already
   flags as a disanalogy) breaks the law at the country level.
4. **No threshold tuned to produce a pass.** All thresholds fixed below; sensitivity grid
   pre-specified.
5. Diagnosis only — no MI or engine changes.

---

## Data (fixed — same committed sources as the erosion program)

- **Wealth = log Maddison GDP per capita** (`longrun_pillars.json` `P4_gdp`, annual).
- **Institutions = V-Dem rule-of-law** (`vdem_longrun.json` `rol`).
- **Political release = committed domestic conflict onsets** (`contagion/crisis_classification.json`,
  `domestic` tag) — same set used in Findings 12/14.
- **Universe:** countries with ≥ 40 years of overlapping annual GDP + rol. OWID pseudo-
  entities excluded.

## Construction (fixed)

- **Gap (the "suppression" configuration), per country-year:** within the cross-section of
  countries covered in that year (require ≥ 15 countries or the year is skipped),
  standardize `log(GDP)` and `rol` to z-scores; `gap = z(logGDP) − z(rol)`. `gap > 0` =
  wealth exceeds institutional capacity = the held configuration. (This is the deep-panel
  analogue of Safeguard J's P4−P1 gap.)
- **Suppression episode:** a maximal run of **≥ 5 consecutive covered years** with
  `gap ≥ 0.75` (0.75 SD above the institution-implied level). **Duration** = years in run;
  **peak_gap** = max gap in the run; the episode "ends" at its last covered year.
- **Release (primary — economic):** the maximum GDP-pc **peak-to-trough drawdown (%)**
  that occurs within the window `[episode_end, episode_end + 15]` years (peak taken at or
  after episode_end). Episodes that resolve gracefully take release ≈ 0 — this is
  intended (graceful venting = small release).
- **Release (secondary — political):** 1 if any domestic conflict onset occurs in the
  same window, else 0.

## Tests

**Test 1 (GATE) — duration → economic release magnitude.**
Spearman(duration, drawdown_%) across all episodes. **Partial** Spearman controlling for
`peak_gap` (so the effect is *duration*, not merely a bigger imbalance).
- **Predicted:** ρ > 0, p < 0.05, and partial-ρ > 0.
- **Confirm:** both hold. **Disconfirm:** ρ ≤ 0, or p ≥ 0.05, or partial-ρ ≤ 0.

**Test 2 — duration → political release (secondary).**
Logistic / Mann-Whitney of duration for episodes with vs without a conflict-onset release.
Reported for completeness; not a gate.

**Test 3 — sensitivity grid (pre-specified).** Re-run Test 1 across
`gap_thresh ∈ {0.5, 0.75, 1.0}` × `min_len ∈ {3, 5}` × `horizon ∈ {10, 15, 20}`.
The gate verdict must hold on the **registered cell (0.75, 5, 15)** and be *directionally
stable* (majority same-sign) across the grid to promote; if the registered cell passes but
the grid is a coin-flip, report as "fragile / registered-cell-only."

## Interpretation gates (frozen)

- **Test 1 passes (registered cell + directionally stable grid):** the suppression→release
  sub-law extends to the capital/economic domain. **Promote** the capital-suppression
  reading from [inferred] to [demonstrated within this operationalization], with the
  self-reform caveat retained. Add as a robustness finding.
- **Test 1 fails:** the sub-law does **not** extend at the country level. **Retire** the
  capital-suppression thesis to **context-only** — strip its load-bearing role in
  `docs/capital_hubs_atlas.md`, `docs/GRAND_SYNTHESIS.md` §4, and the ROBUSTNESS_RESULTS
  convergence section; keep the atlas as historical context, not a mechanism.
