# SEALED prospective flags — acute pre-turn signature (2024 baseline)

> **STATUS: SEALED 2026-06-28, before outcomes.** This is a genuine out-of-sample forecast — the
> framework's strongest test. Do **not** re-tune the flags or thresholds after this commit.
> **Score out ~2030** (once WGI through ~2028 is published). Machine-readable companion:
> `data/forecasts/sealed_flags_2024.json`.

## What this is
Applying MI v3 to the full 180-country panel, these countries show the **acute pre-turn signature**
the lead-time analysis isolated (`docs/lead_time_analysis.md`): **P1 (institutions) eroding ≥0.03
and the pillar spread widening ≥0.03 since 2018, from a level that still has something to lose**
(P1 > 0.33). That is the Chile-2014→2018 / Lebanon-pre-2019 configuration — the signal that only
emerges ~3–5 years before a turn.

**These are directional RISK flags, not dated forecasts (Mod8).** The framework predicts elevated
vulnerability *configuration*, not the date or the trigger. The acute-timing horizon is calibrated
on only n=2 turns (Chile, Lebanon) — so these flags are *also* the out-of-sample test of that
horizon. Most are **not** in the 51-case set, so this is the framework pointing forward, not fitting.

## Tier A — consolidated states showing the pre-turn signature (the novel flags)
| country | 2024 P1 | 2024 P5 | spread | Δ since 2018 (P1 / P5 / spread) |
|---|---|---|---|---|
| **United States** | 0.731 | **0.633** | 0.310 | −0.043 / **−0.064** / +0.066 |
| **United Kingdom** | 0.757 | 0.677 | 0.267 | −0.055 / −0.034 / +0.047 |
| **Chile** | 0.673 | 0.664 | 0.418 | −0.040 / −0.054 / +0.041 |

**Prediction:** elevated risk of a **stability/cohesion shock or contested institutional episode
(managed instability)** in 2025–2029 — **not** state fragmentation/collapse (P3/P4 stay high). If
the flag is real, P5 keeps falling and the spread keeps widening. The US is the sharpest: it scores
*well* on level, but institutions + cohesion are sliding while the economy (P4 0.94) holds — the
exact profile that preceded Chile's 2019 turn.
**Falsification:** false positive if, by score-out, **P5 has recovered toward its 2018 level AND
the spread has narrowed**, with no notable national instability episode in the window.

## Tier B — authoritarian / low-P1 states sliding further
| country | 2024 P1 | 2024 P5 | spread | Δ since 2018 (P1 / spread) |
|---|---|---|---|---|
| Russia | 0.355 | 0.416 | **0.541** | −0.065 / +0.137 |
| Belarus | 0.355 | 0.506 | 0.509 | −0.089 / +0.083 |
| Kyrgyz Republic | 0.367 | 0.471 | 0.409 | −0.043 / +0.061 |
| Mali | 0.336 | 0.202 | 0.353 | −0.048 / +0.032 |

**Prediction:** continued institutional stagnation at/near the floor; elevated fragmentation/violence
risk under shock; no recovery without institutional change. **Russia caveat:** its P4 *rose* to 0.90
— a war-economy / 2024-GDP-gap artifact masking the institutional collapse; read P1/P5, not MI (same
lesson as Venezuela).
**Falsification:** flag wrong if P1 materially recovers (≥ +0.05 toward the median) and the spread
narrows by score-out.

## Why not Venezuela / Yemen / Sudan
Those already **turned** — they sit at the floor; the acute window is behind them. This list is for
states that still look intact on *level* but show the late-emerging erosion + widening spread.

## How to score this out (~2030)
Re-pull WGI through ~2028, recompute P1/P5/spread for each flag, and check each prediction against
its falsification condition. Honest accounting: report confirmations **and** false positives — a
flag that quietly stabilizes is a miss, and counts as one.
