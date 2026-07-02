# C-cases — blind validation of rules A & B (15 cases, run honestly)

**Date:** 2026-06-28. Source cases supplied externally; **their CONFIRMS/WEAKENS labels were not
trusted** — every verdict here is re-derived from real WGI/WDI via the engine (Safeguard J +
convergence + accountability_gap), then compared to the actual outcome. Pre-WGI cases (Iran 1979,
Romania 1989, Italy 1992-window) are **unrunnable** and excluded from scoring. Additive — the 51-case
ordinality baseline (213C/77P/0F) and 19 durability-gate verdicts are untouched.

## Pattern 1 — Convergence Qualifier (A): SURVIVES, and the honest run *rescues* it
| case | gap | J | dir | rents% | crisis | my verdict |
|---|---|---|---|---|---|---|
| Gabon | +0.43 | FLAG | widening | (oil) | YES | fragile — **TP** |
| Nicaragua | +0.34 | FLAG | widening | 2.7 | YES | fragile — **TP** |
| Equatorial Guinea | +0.42 | FLAG | **closing** | 27.8 | no | not-fragile — **TN** |
| Ireland | +0.08 | clear | – | 0.3 | no | not-fragile — **TN** |
| Greece | +0.24 | BORDER | widening | 0.3 | YES | indeterminate (crisis) |
| Botswana | +0.24 | BORDER | widening | 0.9 | no | indeterminate (no crisis) |
| Mali | +0.13 | clear | – | 8.9 | YES | not-fragile — **FN (out of scope)** |

**Where I disagree with the source doc:**
- The doc called **Equatorial Guinea the "strongest disconfirmation"** (huge gap, no crisis). Run
  honestly, the V3.2 *convergence qualifier handles it*: its gap is **closing** (P1 ticked up off the
  floor) → classified not-fragile → correct. So it does **not** break the rule. **The doc's #1
  recommendation — add a rent control — is empirically unnecessary here:** direction already separates
  rentier Gabon (widening → crisis) from rentier EqGuinea (closing → no crisis). (Honest caveat: the
  "developmental_catchup" *label* is wrong for EqGuinea — that's rent-financed stasis, not development;
  the prediction is right, the mechanism description isn't. Pair with Safeguard E for interpretation.)
- The doc framed **Mali as a "false-closing" disconfirmation.** In the data Mali's gap is **0.13 =
  clear** (both income and institutions near the floor) — never a closing-gap flag. Its 2012 collapse
  was territorial/jihadist, a *small-gap* failure → **out of scope** for a durability-gap rule, not a
  refutation of the closing-gap claim.
- **Confident calls hold:** FLAG+widening → crisis (Gabon, Nicaragua); FLAG+closing → no crisis
  (EqGuinea); clear → no crisis (Ireland). The **borderline band is honestly ambiguous** — Greece
  (crisis) and Botswana (no crisis) both sit at 0.24, exactly the unidentified zone; neither is a
  confident prediction (do not read borderline as "fragile").

**Net on A:** validated on an independent set and *strengthened* (the qualifier rescued the case the
doc said broke it). Two real scope notes: (1) the borderline band is genuinely uncertain; (2) a state
can collapse with a *small* durability gap (Mali — territorial/security), which Safeguard J cannot
see by construction.

## Pattern 2 — Accountability Gap (B): REFUTED on runnable data
| case | VA−P4 | status | succession crisis? | my verdict |
|---|---|---|---|---|
| Oman (2019) | −0.18 | balanced | no | no-crisis — TN |
| China (2011) | −0.46 | accountability_lag | no | no-crisis — TN |
| Cuba (2017) | −0.65 | **legitimacy_capped** | no | crisis — **FP** |

The single legitimacy-capped case (Cuba) managed succession with **no crisis** → false positive;
Oman/China weren't even capped in the data. **Zero confirmations** in WGI-era data (Iran/Romania,
the doc's confirmations, are pre-WGI and unrunnable). This **agrees with the doc's downweighting** —
derived independently — and with B's standing status: an **unvalidated hypothesis**, kept informational,
never a verdict. The doc's reformulation (the real variable is an *institutionalized succession rule*,
not accountability) is plausible but **unmeasurable in the MI** — flagged as the path, not adopted.

## Drift — top-tier: erosion ≠ structural crisis
| case | P1 (pre→now) | P5 now | gap | J | outcome |
|---|---|---|---|---|---|
| Israel | 0.73 → 0.73 | 0.50 | +0.09 | clear | erosion ongoing |
| Iceland | 0.85 → 0.80 | 0.84 | +0.09 | clear | recovered |
| Italy | 0.66 → 0.65 | 0.88 | +0.19 | clear | reconstituted |

All three read **clear** on the durability gate and **reconstituted/eroded rather than collapsed** —
the gate correctly does not flag them. Two honest nuances: (1) **Israel's P1 composite is flat**
(0.73→0.73) — its erosion lives in the Rule-of-Law and VA *sub-indicators*, masked by the composite,
so the durability gate cannot see Israel's drift. (2) By the gate, **the US (0.21 borderline) is more
structurally exposed than Israel (0.09 clear)** — the country in active erosion is *less* gap-exposed
than the one that merely looks fine, because Israel's institutions still match its income.

## What changes
- **A:** no engine change — validated and strengthened; the doc's rent-control add-on is unnecessary
  (trajectory already does the work). Scope caveats documented (borderline uncertainty; small-gap
  collapses out of scope).
- **B:** no change — remains an explicitly-labeled hypothesis, now with independent disconfirming
  evidence (Cuba); the succession-rule reformulation is the future path (unmeasurable now).
- **Corpus:** the 12 runnable cases added as a `rule_validation` class (the 3 pre-WGI flagged
  data-limited); they test rules A/B, not P1-ordinality, and are scored separately.
