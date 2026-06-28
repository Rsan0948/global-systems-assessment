# MI v2 — 35-case synthesis (scorecard, V1↔V2 comparison, what breaks → V3)

**Date:** 2026-06-28. Corpus: 25 redone under V2 + 10 new (cases 26–35). The eventual target is
50; this is the 35-case checkpoint.

## Scorecard (V2, equal weights)
| segment | C | P | F | clean | directional |
|---|---|---|---|---|---|
| 25 redone (V2) | 109 | 38 | 0 | 74% | 100% |
| 10 new (26–35) | 45 | 15 | 0 | 75% | 100% |
| **all 35** | **154** | **53** | **0** | **74%** | **100%** |

Honest range, not a single number: clean ~62–85% depending on coding; **zero falsifications across
207 discrete predictions** (partly by construction — directional claims are hard to falsify);
capacity construct partly redundant with WGI standalone.

## V1 ↔ V2 comparison (honest, incl. where V2 is not better)
- **The 25 redone are identical to V1: 109C/38P/0F.** The V1→V2 weighting change (P1 0.34 → equal)
  flipped **zero** verdicts — confirmed by the A-vs-B retrodiction (equal and time-varying gave
  identical mechanical verdicts). So **V2 does not outperform V1 on the shared 25 cases; it ties.**
  That is the honest result: the predictive signal lives in P1 itself, not in the weighting.
- **V2's value-add is therefore not a higher score** — it is: (a) a more defensible/honest
  weighting rationale (rotation/artifact acknowledged); (b) graded, unit-correct Safeguard E
  (a real V1 bug fixed); (c) two new first-class outputs (durability ratio, below-floor
  diagnostic); (d) a refined Strategy 3; and (e) 10 new cases extending coverage with 0 falsifications.
- **No case where V2 scores worse than V1 would have** on the 25 (identical). V1 remains frozen at
  tag `mi-v1` / `archive/v1` for exact comparison.
- New cases (26–35): 75% clean, 0 falsified — V2 generalizes to new geography/stress types.

## What this run established
- **Configuration (spread) thesis strengthened** (Lebanon 29: spread > composite-MI as the
  vulnerability signal; reinforced by the below-floor partial-failure finding).
- **Effectiveness/voice = keep P1 composite** (Vietnam 31 is a second clean instance with Rwanda).
- **Mod4 abstention discipline held** (Czech/Slovakia, DRC/Rwanda, Ghana/CDI near-ties; Korea/Taiwan).
- **Safeguards confirmed on new ground:** A (Iraq), E×H (Bolivia), G-Tier-1 (Fiji), H (Malaysia),
  I/Mod9 (Aceh — the constructive counterpart to Myanmar/Tigray re-suppression).

## What breaks / limits → raw material for V3
1. **Non-WB polities have no data path.** Taiwan (case 32) is absent from the World Bank source →
   forced Mod4 abstention. V3 needs a documented proxy series (e.g. V-Dem/ICRG/WJP) for Taiwan and
   similar.
2. **Sub-state entities are proxy-scored** (Aceh, Kosovo, East Timor, South Sudan) — no full MI
   (<3 pillars). V3: a sub-national data layer or an explicit proxy methodology.
3. **2024 resource-rents / ODA unpublished** → P4 falls back to GDP for the 2024 endpoint. Refresh
   when the WB series updates.
4. **The pillar rotation is unexplained.** P2-leaning ~2012, P1 ~2018, P3 ~2024. V2 rejected
   time-varying weighting on the tie-breaker, but the rotation itself is an open V3 question: does
   the binding constraint on modernization shift with global macro conditions?
5. **P1 decomposition deferred.** The capacity/accountability gap is real and large for
   Singapore/Gulf but didn't improve predictions (all stable). V3: test it prospectively if/when a
   high-capacity/low-voice state actually reverses.
6. **`d_failure_dimension` is not purely mechanical.** The numeric-lowest pillar is only a
   vulnerability when actually low; V2 augments-not-overwrites and keeps it PARTIAL. V3 could
   formalize a "binding-constraint" rule.
7. **New outputs need their own validation.** The durability ratio (MI residual vs ln-GDP) and the
   below-floor diagnostic are introduced in V2 but not yet validated against *realized* durability /
   intervention outcomes — a V3 task (and they currently regress over the case-study set, not all
   ~180 countries).

## Status
V2 is the live model (`MI_ACTIVE_WEIGHTING="equal"`). The V2 archive/tag is deferred until the
corpus reaches 50 (per "I'll want 50 eventually"); V1 stays frozen at `mi-v1` for comparison.
