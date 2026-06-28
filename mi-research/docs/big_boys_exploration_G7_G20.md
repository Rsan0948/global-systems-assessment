# Big-boys exploration — G7 / G10 / G20: latent signal & candidate rules

**Date:** 2026-06-28. **Scope:** all G7 + G10-extras (Belgium, Netherlands, Sweden, Switzerland) +
G20-extras (Argentina, Australia, Brazil, China, India, Indonesia, Mexico, Russia, Saudi Arabia,
South Africa, South Korea, Turkey) = 23 large economies, profiled from the 180-country panel + a live
Voice-&-Accountability (VA) pull. **Goal (per request):** pattern-match the big economies to our
70-case corpus and hunt *niche* signal we've not used — we've over-fit on failing states; this looks
for nuance at the top. **Status: EXPLORATORY (no holdout) — candidate rules, not yet adopted.**

## Two clean new structures (the headline)

### Candidate Rule A — the Convergence Qualifier (refines Safeguard J)
Safeguard J (P4−P1 durability gap) is a *level*. Adding its **trajectory** splits the flagged set by
actual outcome — cleanly:

| direction (Δgap 2012→2024) | states | outcome |
|---|---|---|
| **CLOSING** (gap narrowing, P1 rising) | China, India, Indonesia, Italy, Argentina | **no acute crisis** — developmental catch-up / recovery |
| **WIDENING** (gap widening, P1 falling) | Brazil, Russia, South Africa, Turkey, Mexico | **crisis / instability** (Brazil '16, SA '21, Turkey '16, Russia, Mexico ongoing) |

So a high durability gap means opposite things by direction: a **closing** gap is a state *building
institutions toward its income* (earning durability); a **widening** gap is the *grant eroding*
(fragility). The static gate over-flags catch-up states (China/India/Indonesia would read "crisis-prone"
on level alone — they're not, they're converging up). **This is the strongest candidate for V3.2** —
additive, validatable, and it directly sharpens the rule we already shipped.
*Note on the US:* gap +0.21 (borderline) **and WIDENING** (Δ +0.06, P1 falling) — the one advanced
democracy drifting toward the gap from above, not just sitting near it.

### Candidate Rule B — the Accountability Gap ("capacity without consent") — a NEW axis
P1 deliberately excludes Voice & Accountability (VA). Among the big boys, VA is the *only* thing
separating the rich authoritarians from the democracies at similar capacity — and it's invisible to
the entire MI. Measuring VA against income (P4):

| VA − P4 | states | reading |
|---|---|---|
| **< −0.50 (legitimacy-capped)** | Saudi −0.63, Russia −0.58, China −0.57, Turkey −0.51 | rich + capable, **no accountability channel** |
| −0.20 to −0.35 (accountability lag) | Mexico, Indonesia, India, US, Brazil, S.Korea | partial |
| > −0.16 (balanced) | all of W. Europe, Japan, Canada, Australia | accountability ≈ capacity |

The hypothesis: **capacity-without-accountability is a distinct, brittle failure mode** — a state that
delivers economically but has no pressure-release valve fails *suddenly* (succession/legitimacy shock),
not gradually. It's orthogonal to the durability gap: China is *closing* its durability gap (Rule A
says "developmental") **but** is deeply legitimacy-capped (Rule B says "brittle"). The two axes
disagree on China precisely because they measure different things. This is the niche big-boys signal —
but we have **no crisis evidence for it yet** (Saudi/China haven't broken; Russia/Turkey did backslide,
consistent). Propose as a hypothesis + a future case class; it needs VA wired into the panel to operate.

## Two softer signals

### Candidate Rule C — decompose the spread before reading it
"Wide pillar spread = vulnerable" is false for rich states when the spread is **P2-driven**: Australia
(spread 0.39!), Saudi, Canada are wide *because innovation (P2) lags*, not because institutions do.
P1-driven spread (Russia, Mexico, Turkey) is the dangerous kind. Rule: **attribute the spread to its
driving pillar — P1-driven = fragility; P2-driven = competitiveness lag, benign.**

### Candidate Rule D — the innovation-drag / maturity plateau
Among the highest-MI democracies the **binding constraint is systematically P2 (innovation)** — Canada,
Germany, Belgium, Netherlands, Sweden, Switzerland, Australia, Japan are all P2-bound, and most are
*declining* on P2 (dP2 < 0). Meanwhile the developing big boys are *gaining* P2 (China +0.06, India
+0.03). Not a crisis signal — a **competitiveness convergence**: mature economies plateau on innovation
while developing ones close the gap. Worth tracking as a slow relative-decline indicator.

## Pattern-match to the 70-case corpus
| country / cluster | nearest case archetype |
|---|---|
| Switzerland, Sweden, Netherlands, Germany, Canada, Australia, **Japan** | true-negative archetypes (Canada/Germany/Japan/Uruguay); Japan = the anti-fragile balanced model (lowest spread, P1 & P5 *rising*) |
| **United States** | NOVEL — borderline durability, **widening**, P5/cohesion eroding from the top; closest to the Chile-pre-2019 *configuration* but cleared-on-gap. No clean case match. |
| UK, France | milder US-type — clear on gap but **P5/cohesion-bound** |
| **Italy** | its own 1992 First-Republic collapse — now the "**recovered-from-collapse**" archetype (flagged-but-closing, P1 rising) |
| Russia, Turkey | failing/autocratized petro-states (widening gap + legitimacy-capped) |
| Saudi Arabia | Gulf rentier (case42) **+** the most legitimacy-capped — adds the brittle dimension |
| Brazil, Mexico, South Africa | widening-gap + **accountability>capacity** ("loud weak-state") — their own signature cases |
| **China, Indonesia, India** | **NO MATCH** — closing-gap developmental capacity-builders (China also legitimacy-capped) |

## Meta-finding — three coverage gaps in the corpus
We've hammered *failing* states; the big boys expose what we're **missing**:
1. **Closing-gap developmental capacity-builder** (China / Indonesia / India): institutions rising fast
   under high income, *no* crisis. We have no such case — the corpus only knows gaps that *widen*.
2. **Legitimacy-capped brittle** (Saudi / China): the capacity-without-accountability failure mode is
   entirely untested — no case has broken on it yet.
3. **Top-tier democracy drifting down** (US): erosion *from the ceiling* (P5/cohesion + widening gap),
   distinct from every floor-ward case we have.

## Integrity note
Exploratory, no holdout — none of A–D is adopted into the engine here. Rule A (Convergence Qualifier)
is the lead candidate: well-evidenced, additive, and a direct refinement of the shipped Safeguard J —
slate it for V3.2 with a proper validation pass. Rule B (Accountability Gap) is the most novel but
needs VA wired into the panel and lacks crisis evidence; treat as a hypothesis + a target for new cases.
