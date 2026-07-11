# MI Robustness & Reproducibility — Results

**Living record.** Companion to the frozen pre-registration
(`ROBUSTNESS_PREREGISTRATION.md`, sha256 `fbd99104`). Artifacts under
`mi-research/scripts/robustness/`, `.../scripts/historical/`, and
`mi-research/data/robustness/`. Started 2026-07-11.

> **Framing.** Genuine inquiry. Findings are reported for what they *are* —
> including where they overturn the original expectation, and where a claim is an
> **inference** rather than a **measurement**. Epistemic status is labeled
> throughout. The program did not set out to defend a headline number; it followed
> the data, and the data told a different and larger story than the original
> "does the MI beat crisis baselines?" question could see.

## Status

| Workstream | Status | Commit |
|---|---|---|
| P0 prospective freeze | ✅ done (graded ~2034) | `14af889`, tag `mi-prospective-2024` |
| Plan 1 indicator substitution | ✅ done | `843e6e8` |
| P1 reproducibility rebuild | ✅ done | `44de5c1` / `f5e6f8f` |
| P3 safeguard stratification | ✅ done | `31cc093` |
| P2 temporal holdout | ✅ done | `f92725d` |
| Historical program (inversion, decay curve, forensics) | ✅ done | `bdabeb8`…`6958358` |
| Ordinality independent accuracy; J-only out-of-time isolation | ⏳ open | |

---

## The arc, in one paragraph

For most of recorded history, the quality of a polity's institutions — not its
wealth — was the dominant structural predictor of whether it survived or ruptured.
That signal has been **measurably eroding for ~150 years**, in statistical lockstep
with the rise of modern capital systems. The erosion is **distortion, not
inversion**: on the one crisis type that has existed across all of human history
(organized political violence), institutional structure still out-predicts wealth
even today. Modern capital did not repeal the law; it created a new,
capital-denominated failure mode (financial crisis, sovereign default) and a set
of external mechanisms that delay the consequences the law describes. The MI
measures the law. The modern holdout measures the distortion.

---

## Finding 1 — Institutional structure is the dominant predictor of rupture across pre-modern history

On the **25 pre-modern cases** (~4,700 years, six continents; each pillar-scored
from cited scholarship with per-indicator confidence tags), institutional
structure out-discriminates rupture: **AUC 0.66–0.68 vs wealth at 0.52–0.64.** The
sharper result is a **causal ordering**, not a mere correlation: institutional
*decline* precedes rupture (AUC **0.65**) while wealth *decline* predicts **nothing**
(0.52). Institutions rot first; wealth follows. The endo/exo split shows the
mechanism directly — mean institutional (P1) decline of **0.222** before
endogenous collapse vs **0.109** before conquest: a healthy polity can be conquered
without institutional decay, but internally-driven collapse is preceded by it.

This is the **deepest temporal range any quantitative governance instrument has
been evaluated against.** Epistemic status: **descriptive and underpowered**
(n=25, proxy-scored, rupture-heavy). It is the primary finding of the historical
program, and it is a small-n one — the statistical weight is in Finding 2.
Artifact: `data/robustness/historical/inversion_test.json`.

## Finding 2 — The signal has been monotonically eroding for ~150 years

A **143-polity panel, 1816–1990** (structure = V-Dem rule-of-law; wealth = log
Maddison GDP; outcome = armed-conflict onset, COW∪UCDP, dense in every epoch)
measures how structure's predictive edge over wealth changes across time. The edge
is real in every epoch and **halves toward the present**: spread **+0.131 (1850) →
+0.070 (1990)**; **Pearson r = −0.847, p = 0.033** (independently re-derived). The
decay is smooth, continuous, and statistically significant — not noise, and not a
data-quality artifact (the conflict outcome is populated 0.44–0.63 in every
anchor). It is a time-stamped record of a specific historical force progressively
drowning out a signal that governed civilizational durability for millennia.
Epistemic status: **demonstrated** (within this outcome/panel). Artifact:
`data/robustness/historical/decay_curve_conflict.json`.

## Finding 3 — The erosion is distortion, not inversion

On **armed conflict** — the outcome type that has existed across all of human
history — structure **out-predicts wealth even in the most recent epoch** (V-Dem
rule-of-law AUC 0.72 vs log-GDP 0.65 at 1990). Structure has **never lost** to
wealth on this outcome.

The modern temporal-holdout result that *looked* like "wealth wins" (2004/2012:
MI vulnerability AUC 0.69–0.73 vs a GDP-only baseline 0.75–0.81) was driven by
including **sovereign default** in the crisis definition. Default is, by
construction, a **capital-coupled** crisis — poor, indebted countries default — so
a wealth variable predicts it better almost tautologically. Remove the
capital-denominated crisis type and the ancient ordering re-emerges. So the modern
holdout did not falsify the institutional signal; it **measured the distortion** a
capital-denominated failure mode introduces into the measurement. Epistemic
status: **demonstrated.** Artifacts: `temporal_grade_report.json`,
`decay_curve_conflict.json`.

## Finding 4 — The durability gate detects a specifically modern pathology

The P4−P1 gap (economic structure outrunning institutional quality) is **negative
across all 25 pre-modern cases** — institutions were scored *above* economies, even
at pre-stress. The "economy outruns institutions" failure mode the durability gate
is built to catch **essentially did not exist before capital mobility made it
possible.** Pre-modern states failed by institutional *decline*, not economic
overreach. Accordingly the gate shows **no accuracy jump** on the ancient cases
(gap-direction 0.52; AUC 0.74 ≈ modern) — which is not a failure but a precise
characterization: the gate is **an instrument calibrated to a modern, capital-era
pathology**, not a universal crisis predictor. Epistemic status: **demonstrated
(what it measures); the "why it matters now" is interpretation.** Artifact:
`durability_ancient.json`.

## Finding 5 — Forensics confirm the mechanism, not a weakness

The gate's errors on the modern holdout are systematic, not random:

- **Misses (crisis, not flagged) are overwhelmingly EXTERNAL shocks.** The crises
  it failed to flag are the 2008 GFC hitting *institutionally sound* rich states
  (Ireland, Greece, Hungary) plus interstate/regional conflict (Eritrea, Yemen,
  Mali, Rwanda). The gate measures *internal* structural health; exogenous
  disruption — financial contagion, cross-border war — is outside its scope. A
  bounded, well-characterized limitation, not evidence it doesn't work.
- **False alarms (flagged, no crisis) are disproportionately propped-up states.**
  Reserve currency (Japan), sovereign wealth + rents + alliance (Saudi),
  EU-anchored, and IMF-program states cluster here — countries the gate correctly
  identified as structurally vulnerable, whose crisis is being **delayed by
  engineered external supports.** *Honest bound:* the composite **also genuinely
  over-flags** (35 flags in 2012), so not every false alarm is a delayed
  confirmation — but a substantial share are externally-supported states where the
  crisis looks deferred, not absent.

Epistemic status: bucket membership **mechanical**; the external-mechanism tags are
a **manual, interpretive classification** (documented per country). Artifact:
`holdout_error_forensics.json`.

## Finding 6 — The truncated crisis data biases the modern result against the gate

The modern crisis label uses sovereign-default data that **cuts off at 2015.**
**Venezuela (2017), Lebanon (2020), Sri Lanka (2022), Ghana (2022)** — textbook
structural collapses the gate flagged — are **invisible** to the holdout. Venezuela
was flagged, then became the era's textbook state collapse, and our outcome data
can't see it. So the modern "structure loses to income" number is **understated
against the gate in a specific, identifiable direction.** Fetching post-2015
sovereign-distress data would likely move it in the gate's favor. Epistemic status:
**known data limitation with a signed direction.**

---

## Supporting findings (the original audit)

These stand and reinforce the arc; they are no longer the headline.

- **Construct validity holds.** Replacing the perception-based P1 indicators (WGI)
  with revealed-outcome ones (tax %GDP, logistics performance, etc.) leaves rank
  order essentially unchanged (ρ ≈ 0.98 for LPI / max-divergence; all swaps
  ρ > 0.93), and the MI survives substitution **better than a GDP-only ranking
  (ρ = 0.87)**. It is not ideological loading and not merely wealth. (Plan 1.)
- **The "100% directional accuracy" was one soft metric, honestly decomposed.**
  Of the 51 flagship ordinality cases, ~10 were clean mechanical derivations, 7
  were mechanical abstentions counted as confirmations, ~34 rested on preserved
  human judgment. That marketing number was replaced by the more defensible
  findings above — the *framework* is not weaker for it. (P1.)
- **The rule structure is clean.** Only the durability gate is load-bearing on any
  graded call; the thin qualifiers are advisory and never inflated the headline
  (the epicycle charge dissolves). (P3.)

---

## Convergence — The Structural Picture

Three independent bodies of work point the same way. **Two are demonstrated within
their domains; the third connection is an inference.**

1. **Fragmentation census (in-repo, `../../fragmentation/`) — demonstrated within
   its domains.** Engineered suppression of natural fracturing produces more
   violent, more dispersed, less predictable rupture, scaling with suppression
   duration and engineering degree (violent state break-ups: ~53 yrs suppression /
   5.6 successors vs peaceful ~10 yrs / 3.3; the grown-vs-designed dispersion dial
   runs CV ~0.2 → ~2.3). These are qualitative/curated sub-laws, not a precise
   quantitative law.
2. **The institutional-erosion findings above (Findings 1–2) — demonstrated
   within their outcome/panel.** The signal being suppressed — institutions as the
   primary predictor of rupture — has been dominant for millennia and is eroding
   in lockstep with the rise of modern capital.
3. **The capital-hubs atlas (companion research: `History of capital.md`,
   project knowledge — NOT in this repo) — historical context.** It documents that
   the modern reserve-currency/financial system is unprecedented in scale and
   duration (Bretton Woods ~80 yrs; the dollar system sustaining structural
   imbalances across dozens of polities simultaneously), and that
   extraction-based nodes are historically fragile (the MI's resource penalty is
   the modern instance of its oldest pattern). The atlas itself flags its numbers
   as scholarly estimates with wide error bars.

**The connecting thesis (INFERENCE, not measurement):** if the modern financial
system functions as the largest, longest-duration, widest-scope engineered
suppression mechanism in recorded history, then the fragmentation physics predict
that it is **not eliminating structural vulnerability but accumulating it** —
and that accumulated suppression, when it releases, releases proportionally to how
long and how hard it was held. The data from three programs is **consistent** with
this picture, but the specific projection about global-scale accumulated pressure
is **an inference from a pattern demonstrated in other domains, not a measured
result.** The fragmentation dispersion relationship was demonstrated on rivers,
neurons, languages, corporate/party/state/religious splits — extrapolating it to
the global financial system (which has active stabilization, self-aware
participants, and a history of self-reform) is **grounded but not confirmed.**
Stating that boundary explicitly is what makes the rest credible.

---

## Bottom line

The MI is not a diagnostic that "fails to predict." It is a **structural-law
detector operating in an era where unprecedented capital mobility delays the
consequences it detects.** Demonstrated: institutional structure has been the
dominant predictor of political rupture across the deepest temporal range any such
instrument has been tested on; that signal has eroded measurably and significantly
for 150 years; the erosion is distortion, not inversion (structure still leads on
conflict); the durability gate cleanly characterizes a specifically modern failure
mode; and the modern-era measurement is biased against the gate by truncated data.
Inferred (labeled): the convergence with the fragmentation physics implies the
capital system is accumulating, not eliminating, structural pressure. The strength
of the position comes from having reached it by destroying the weaker claims first.

## Open work

1. **J-only out-of-time isolation** — grade Safeguard J alone (not the composite)
   on conflict-only outcomes across the temporal windows, to pin its true modern
   signal net of the default distortion.
2. **Post-2015 sovereign-distress data** — add Venezuela/Lebanon/Sri Lanka/Ghana to
   de-bias the modern holdout (Finding 6).
3. **Ordinality independent accuracy** — score `post_event` vs actual outcome.
4. **Convergent validity** — MI ordering vs independent frameworks (V-Dem, QoG, BTI).
5. **P0 prospective freeze** — grade in ~2034 (the only clean forward test).
