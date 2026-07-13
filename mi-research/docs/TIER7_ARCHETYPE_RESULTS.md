# Tier 7 — Mule Archetype Derivation — Results

Frozen prereg sha256 `02bed840`. Code `scripts/v2/tier7_archetype.py`; 63 countries with a
documented dominant modern destabilization, hand-coded (single-coder — disclosed deviation).

> **The question:** the *specific* individual is the irreducible Mule, but is the *TYPE* of
> destabilizer (populist / military / insurgent / kleptocrat / theocrat / external /
> institutional) structurally determined by the six-tier shape?

## Verdict: the reduction reaches its limit here — agency is largely irreducible

**M1 (the gate) FAILS.** Among country pairs with cosine-similar six-tier shapes (>0.85),
same-archetype rate = **0.22** — essentially identical to the all-pairs baseline **0.21**
(lift **+0.01**). Similar state shapes do **not** produce the same actor archetype. The core
hypothesis — that configuration strongly constrains the destabilizer type — is **not supported.**

**M2 is weakly positive.** Leave-one-out classification of archetype from the shape vector is
**38%** accurate vs a majority-class baseline of **29%** (random 1/7 = 14%). So shape carries
*some* information (+0.09 over baseline) — but **62% of cases are misclassified.** The type is
*weakly* shape-linked, not determined.

**Where the weak signal lives — the extremes, not the middle.** The distinct fingerprints are
at the edges: **A6 external** (Iraq: V1 45 / T4 90 / T6 93 — scarred + spark-saturated), **A7
institutional** (Tunisia/Israel: high V1 + high V3 + flickering T5 51), **A3 insurgent**
(low-V1 weak states). The *middle* — A1 populist vs A2 military vs A4 kleptocrat — is **not
separable by shape**; the classifier defaults them toward the majority class (A1).

**The pre-registered predictions — 2 of 4 hit, and the misses are the point.**
- **United States → A1 (MATCH).** The shape alone (high V1, low V2-equity, moderate V3/T4, low
  T5/T6) predicts *civilian populist-nationalist* — the Trump archetype derived from
  configuration without the name. **Poland → A1 (MATCH).**
- **Korea → predicted A1, actual A2 (MISS).** The shape said populist; reality was a *military*
  martial-law attempt (Yoon). **Israel → predicted A1, actual A7 (MISS).** The shape said
  populist; reality was *institutional* (judicial-capture). **In both misses the actual pathway
  came from a specific feature — a coup-prone military, a particular judicial crisis — that the
  general six-tier shape does not encode.** The "who" was not in the shape.

**M4 — the Netherlands check, honestly read.** The clean democracies (Netherlands, Denmark,
Norway, Germany, Canada, Japan) all classify to A1 at **p ≈ 0.20 — barely above uniform (0.14).**
So the framework does **not** confidently assign them a destabilization archetype (correct — no
viable pathway), but it also does not produce a clean "none"; it defaults to the majority class
at chance-level confidence. The right reading: *low confidence everywhere for the clean set*,
which is the honest version of the pre-registered "no viable pathway."

**M5 — where it does cohere.** For the flickering (high-T5) countries the coded archetype
matches the observed direction: Poland/Brazil/Sri Lanka **A1** (populist backsliding),
Korea/Thailand **A2** (military), Tunisia **A7** (institutional). So *combined with the timing
signal*, the archetype reads sensibly — T5 says how close, the archetype (where codeable) says
who. But this is confirmation of coded history, not shape-derived prediction.

## What this means for the Mule — the final, honest boundary

The framework reduced the Mule across six dimensions — *why* (V1/V2/T4), *how close* (T5), *how
dense the sparks* (T6). Tier 7 tried to take the last step: derive *who* — even just the type —
from the shape. **It mostly fails.** State configuration weakly leans toward an archetype (US
correctly reads populist), and the *extremes* (external, institutional, insurgent) are somewhat
shape-determined — but the core actor types are not separable by structure, and the two sharpest
recent cases (Korea's soldier, Israel's judge) were **not** in the shape.

**This is the appropriate end.** After six tiers that progressively lit the environment around
the trigger, the seventh finds that the trigger's *human type* — not just the individual — retains
real freedom. The Mule shrinks one last increment (you can say "this shape leans populist") and
then **stops**, because the actor is where structure runs out and agency begins. The specific
person was always the Mule; Tier 7 shows the *archetype* is only weakly less free. **The
framework can describe the ecosystem in exquisite detail and still not name the species of the
animal that walks out of it — and that irreducible gap, measured here at last, is the honest
floor of structural prediction.**

## Honest bounds
- **Single-coder** (spec wants two + κ≥0.70) — actor codes are mine, from documented cases;
  inter-coder reliability untestable. Country-level (one dominant archetype/country), current
  shape as proxy, n=63, rare classes (A5=2, A6=1, A7=2). All weaken M2. The direction of the
  finding (weak-to-null) is robust to these, but a full event-level two-coder study could shift
  the magnitude.
