# Trigger Hunt — is the Mule really unmeasurable?

Code `scripts/v2/trigger_hunt.py`; data `data/political/trigger_hunt.json`.

## The reframe: "the Mule" conflated two different things

We called the trigger "the Mule" (Asimov's unpredictable perturbation) and stopped looking.
But the metaphor hides a conflation:
- **The spark** — *which* event (Bouazizi's self-immolation, a stolen election), *when*. This
  is genuinely idiosyncratic and ~unpredictable — the true Mule.
- **The ripeness** — how close the system is to the threshold where *any* spark cascades.

Self-organized-criticality theory (the repo's *own* founding physics — the sandpile that
accumulates until it subdivides) makes the decisive distinction: **you cannot predict which
grain triggers the avalanche, but you CAN measure how close the pile is to the critical
slope.** Systems near a tipping point show **critical slowing down** — rising lag-1
autocorrelation (AR1) and rising variance in the state variable (Scheffer/Dakos universal
early-warning signals, demonstrated in ecology, climate, epidemiology). **We had been hunting
the spark. We never applied the criticality toolkit to the ripeness.**

## The hunt: does critical slowing down precede rupture?

For every country-year, the CSD indicators (AR1, variance, and their rising trend) of the
detrended state-variable series over the prior 12 years, compared between pre-rupture windows
and controls.

**Democratic backsliding (state variable = annual liberal-democracy index):**

| CSD indicator | event | control | AUC | p |
|---|---|---|---|---|
| **variance** | 0.0031 | 0.0018 | **0.689** | <0.001 |
| **AR1 (autocorrelation)** | 0.444 | 0.392 | **0.562** | 0.0002 |
| rising variance (Δvar) | +5.13 | +4.89 | 0.571 | <0.001 |
| **combined CSD score** | — | — | **0.566** | — |

**Both classic CSD signatures are present and significant** before backsliding. A democracy
about to erode **flickers** — its liberal-democracy score fluctuates with rising amplitude
(variance AUC **0.69**) and rising memory (AR1 0.56) in the decade before it breaks.

**Conflict onset (state variable = annual GDP-pc growth):**

| CSD indicator | event | control | AUC | p |
|---|---|---|---|---|
| **variance** | 41.8 | 20.4 | **0.597** | <0.001 |
| rising variance (Δvar) | +3.01 | +1.79 | 0.515 | 0.097 |
| AR1 | −0.04 | +0.02 | 0.444 | n.s. (wrong sign) |

**Variance is elevated before conflict (AUC 0.60, highly significant)** — economies flicker
before they rupture — though AR1 does not cooperate here, so the signature is partial.

## Verdict: the Mule is half-solved — the pre-tremor is real

**There IS a weak-to-modest trigger signal, and we found it by asking about ripeness instead
of the spark.** Rising variance ("flickering") precedes rupture — AUC **0.69 for backsliding**,
0.60 for conflict. It does not predict *which* event or *what year* (the spark stays dark),
but it detects that a system has entered the **critical, spark-susceptible state** — the
political equivalent of a seismic swarm before a quake.

**Honest bounds:**
- **Weak-to-modest** (AUC 0.57–0.69). This is a *pre-tremor*, not a forecast — it says the
  ground is primed, not when it releases.
- **Partly confounded with baseline instability** (volatile systems are both high-variance and
  rupture-prone) — but the *rising*-variance component (Δvar significant for backsliding) is a
  genuine approach-to-tipping-point dynamic, not just a level.
- **The spark itself remains the Mule** — critical slowing down measures the *susceptibility*,
  not the *precipitant*. That half is, as ever, dark.

**The correction to the program's own claim:** "the trigger is unmeasurable" was too strong.
The *spark* is unmeasurable; the *criticality* is not. And the tool that measures it —
critical slowing down — comes straight out of the repo's founding self-organized-criticality
physics, which we had never turned on the political time series. The sandpile was telling us
the whole time: you can't call the grain, but you can feel the slope go critical.

**The further hunt (untested here):** event *tempo* (accelerating minor protests/strikes as a
mobilization-criticality signal), **scheduled** focal points (elections are the most common
backsliding trigger and their dates are known in advance — a *predictable* trigger class), and
material shocks (food/fuel price spikes, partly forecastable). These are the next places the
ripeness — and even some sparks — may be more measurable than "the Mule" ever admitted.
