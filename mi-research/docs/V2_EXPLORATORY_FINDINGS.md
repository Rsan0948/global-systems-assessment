# V1/V2 Exploratory Signal Search — Disciplined "throw it at the wall"

**Method (`scripts/v2/exploratory_screen.py`).** 21 predictors (V1 overall + pillars P1–P5;
V2 Level/Equity/Combined + pillars F1–F6; the V1–V2 gaps; the V2 Level–Equity imbalance; V2
spread) × 15 niche outcomes (V-Dem democracy changes; GDP growth/volatility/drawdown;
inflation volatility; gross savings; FDI; fertility; life-expectancy change; suicide;
life satisfaction; unemployment; conflict onset) → **266 Spearman tests**, **BH-FDR at 0.05**
across the whole family (**77 survive**, crit p≤0.0134), then **every survivor re-tested with
log GDP-per-capita partialled out** (the development confounder), then the non-obvious
survivors confirmed with **multivariate OLS** (net of level and income). Cross-sectional /
contemporaneous — associations, not forward prediction (V2 has no time series).

## Headline: it predicts *slow societal* variables, not *fast political* ones

**No political outcome — democratic backsliding, electoral-democracy change, rule-of-law
change, or conflict onset — produced a GDP-surviving signal from either V1 or V2.** The
questions we kept asking (does it predict rupture / erosion?) are exactly where the null
lives. Every robust signal is in **demographics, wellbeing, and the health trajectory** —
consistent with the program's own "reads structure, not timing" spine.

## What survives GDP control

- **Fertility (demographic transition).** The single strongest signal in the whole screen,
  net of income: **F3 infrastructure-conversion → fertility, partial ρ = −0.41** — infra
  conversion predicts the fertility transition *better than income does* (P3 −0.35, F5 −0.35,
  v1 −0.29). Real, but a known development story.
- **Life-expectancy gains (convergence/ceiling).** Higher V1/V2 → *smaller* LE gains 2004–24
  (partial −0.20 to −0.32) — high scorers were already near the ceiling. Expected.
- **THE novel, robust find — V2 configuration predicts life satisfaction.** The **V2
  Level–Equity imbalance** (|V2-Level − V2-Equity|) predicts **lower life satisfaction**,
  and it holds in multivariate OLS **net of both the V2 level and log GDP**:
  `life_sat ~ V2-Combined + |L−E| + logGDP` → **imbalance β = −0.178, t = −3.06** (R²=0.70).
  Balanced conversion (efficiency ≈ equity) → more satisfied citizens, independent of how
  rich or how high-scoring the country is. **This is the V2 configuration/equity thesis
  showing a real signal — on subjective wellbeing, not political stability.** It reframes
  what V2's equity dimension is *for*: capturing the lived-experience mismatch, which shows
  up in how people rate their lives, not in coup counts.
- **Stability → FDI.** P5 → FDI inflows, partial +0.26 (sensible, survives income).

## What got culled by discipline (honest graveyard)

- **V1–V2 gap → inflation volatility** (bivariate ρ=−0.29, FDR-significant) **washed out** in
  multivariate — t=−1.27 once GDP is controlled. A confounded mirage.
- **Health-conversion (F2) → lower suicide** (bivariate, protective) is **fragile**: F2 loses
  significance (t=−1.58) when raw health *spending* is added, so it is not cleanly a
  *conversion* effect. The broader Durkheim pattern (institutional development ↔ higher
  suicide; P1 t≈+1.95) is present but weak (R²=0.14).

## Takeaway

The instruments are **structural-societal, not political-tactical**. Their robust
associations are with the slow variables — demographic transition, health trajectory, and
**subjective wellbeing via configuration balance** — and *not* with democratic erosion or
conflict once income is controlled. The one genuinely new, discipline-surviving result is
that **V2's Level–Equity balance predicts life satisfaction net of income** — the equity
dimension earns its keep as a *wellbeing* signal even though it failed as a *political-stress*
predictor. Artifacts: `data/v2/{exploratory_screen,exploratory_outcomes}.json`.
