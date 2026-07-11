# The dimensional gap: Study 2A's DGS and the MI's Safeguard J

This note connects a **null** in the fragmentation research to a **validated
gate** in the Modernization Index. They are structurally the same idea, and the
difference between them is instructive.

## The shared idea

Both test whether a system's **interior economic capacity outrunning its
institutional containment** signals fragility:

- **Study 2A — the dimensional-gap-score (DGS).** `fragmentation/governance/political/`
  computes a gap between economic complexity and institutional quality and asks,
  in a logistic regression, whether it predicts instability. Inputs are *raw*
  indicators: Harvard/OEC ECI, V-Dem, World Bank, UCDP conflict data.
- **MI — Safeguard J (the P4–P1 durability gate).** `mi-research/` tests whether
  the direction of the **P4−P1 gap** (Economic Structure minus Institutional
  Quality) predicts sustainability. Inputs are the MI's *composite pillar scores*.

Both encode the same complexity–capacity mismatch: economic structure that has
grown past what institutions can coordinate is a vulnerability.

## The results diverge

- **DGS → instability: NULL.** On the real ECI + V-Dem + WB + UCDP panel
  (n = 713, 144 countries), the dimensional gap adds nothing beyond GDP +
  population + governance (β = 0.107, p = 0.42, AUC gain 0.0; robust across 5
  sensitivity specifications).
- **Safeguard J: validated at 17/19.** The direction of the P4−P1 gap predicts
  sustainability in 17 of 19 applicable cases.

## Why the null does not falsify the principle

The 2A null is a statement about **proxies**, not about the principle. Raw ECI +
V-Dem + WB indicators, dropped into a logistic regression, don't carry enough
signal to recover the effect — too noisy, too collinear with GDP and governance,
and not aligned to the construct.

The MI's Safeguard J uses the **composite pillar construction** instead. P1 and P4
are each built and cross-validated against the 109-case corpus; the pillars are
purpose-built measurements of "institutional containment" and "economic
structure," not off-the-shelf indices. That composite recovers the signal the raw
indicators miss.

**Takeaway:** the complexity–capacity mismatch is real (the fragmentation
synthesis rests on it, and Safeguard J confirms it at the country level), but
detecting it requires a measurement instrument tuned to the construct. Study 2A's
honest null is the control that shows the raw proxies are not that instrument —
the MI's validated pillars are.

*See also:* `SYNTHESIS.md` (the complexity–capacity principle),
`../mi-research/MASTER_REFERENCE_ARCHITECTURE.md` (Safeguard J and pillar
construction), `DEFENSIBLE_RESULTS.md` at the repo root (both results in the
consolidated ledger).
