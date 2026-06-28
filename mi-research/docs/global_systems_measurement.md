# Global Systems Measurement — a system-level category

**Date:** 2026-06-28. A new **measurement category, distinct from the country-level MI**: where the MI
scores a single polity, this measures the *world system's* state from the same data. It collects the
validated historical/golden-age findings into one runnable instrument. **EXPLORATORY/descriptive** —
built on long-run proxies, not the country scoring engine; it changes no country verdict and leaves the
51-case baseline untouched (213C/0F).

Code: `mi/global_systems.py` · CLI: `scripts/global_systems.py` · constants: `GLOBAL_*` in
`mi/constants.py`.

## What it measures (four sub-measures)
1. **Engines** — the three improvement engines, each a global 10-yr climb rate vs its 1850–2012
   historical-median "firing" bar: **institutions** (V-Dem rule-of-law), **income** (Maddison GDP),
   **human capital** (life expectancy). Golden ages are dimension-specific and out of phase, so the
   engines are reported separately, never collapsed.
2. **Container** — the institutional **net** (climb-minus-decline) trajectory: *strengthening* (robust,
   absorbs a deceleration — cf. 1970s) / *eroding* (brittle, a deceleration can't vent — cf. 1910s) /
   *flat* (ambiguous). This is the supercycle discriminator (`globalization_supercycle_shape.md`).
3. **Texture** — surge / churn / stasis / collapse, from the climb-vs-decline mix.
4. **Movement distribution** — share of countries in each `movement_quality` class (real_ascent /
   windfall / ratchet_rise / hollow_stability / decline / stable), from the 5-pillar panel.

## Current reading (as of 2024)
```
ENGINES (1/3 firing):  institutions climb 8% / decline 7% (med 5%) -> FIRING-but-churning
                       income climb 2% (med 5%) -> quiet
                       human_capital climb 2% (med 7%) -> quiet
CONTAINER:             net +1pp -> FLAT (ambiguous — neither repairing nor clearly collapsing)
TEXTURE:               CHURN
MOVEMENT (n=135):      ratchet_rise 39% · stable 22% · decline 13% · hollow_stability 13%
                       · windfall 12% · real_ascent 2%
```
Read together: the world system is in a **multi-engine lull** (income and human-capital quiet,
institutions churning to a near-flat net), on a **flat-to-eroding container**, in a **CHURN** texture —
and only **2% of countries** are in a genuine institution-led ascent while **~25%** are in *fake*
improvement (income windfall or hollow stability masked by the human-capital ratchet). This is the
brittle-leaning configuration of `globalization_supercycle_shape.md`, quantified in one instrument.

## How to use it
`python scripts/global_systems.py` (add `--year` for a historical reading, `--json` for the record).
It is a **descriptive system gauge**, not a forecast — pair every reading with the caveats it prints.

## Honest limits (printed with every measurement)
- System-level proxy measurement — NOT the country scoring engine; no country verdict changes.
- Engines on long-run proxies; "firing" = above the historical-median climb rate (so "firing" can
  coexist with high decline — that's the CHURN case, read the container/texture for the net).
- The container trajectory is the supercycle discriminator: **n=3 shapes / n=2 outcomes** — a
  mechanism-consistent reading, not a powered law.
- Recent windows are right-censored (latest climbs need forward data) — provisional.
- The movement window snaps to the 5-pillar panel's span (1996–2024 here), which is long; over a long
  window the human-capital ratchet inflates `ratchet_rise`.

## Where it sits in the framework
The MI now has **two measurement tiers**: **country-level** (pillars P1–P5, safeguards A–J, mods,
durability/ascent/movement diagnostics) and **system-level** (this category). They share data and the
"trust the level, distrust the slope" epistemic; they answer different questions (is *this country*
durable? vs what state is *the world system* in?).
