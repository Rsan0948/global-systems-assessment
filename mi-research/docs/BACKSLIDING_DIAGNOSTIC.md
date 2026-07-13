# Backsliding-risk diagnostic (v0.1)

**New, additive engine module** — `mi/backsliding.py` + `scripts/assess_backsliding.py`.
Productizes the two robust findings from the 2026-07 predictive-reach research sprint
(full record: repo `sandbox/tier_stress/FINAL_REPORT.md`).

## What it is
A structural read of a country's democratic-backsliding risk from its **rule-of-law
capacity position**, computed only from the canonical panel (`mi/panel.py`).

- **Nonlinear (the master signal).** Backsliding risk vs capacity is an **inverted-U**:
  peak risk at *mid* capacity (partially-institutionalised / hybrid states), low at both
  extremes. A **safety ceiling near the 80th percentile** — above it, backsliding is rare.
  (Out-of-sample: the ceiling alone AUC 0.73; nonlinear model 0.74 — the strongest, cleanest
  signal across ~40 analyses and 200 years of data.)
- **Relational (secondary).** Capacity relative to civic voice. The research used V-Dem
  civil-society participation, which is **not** in the canonical panel; this module proxies
  it with `voice_accountability` and labels it as such.

## Use
```
python scripts/assess_backsliding.py --country "Hungary"
python scripts/assess_backsliding.py --universe --risk --top 20   # highest-risk (danger zone)
python scripts/assess_backsliding.py --universe --top 20          # safest (above the ceiling)
```
```python
from mi.backsliding import backsliding_risk
backsliding_risk("Netherlands", 2024)   # -> {capacity_percentile, backslide_hazard_5y, safety_ceiling, band, ...}
```

## Face validity (2024)
- **Protected** (above ceiling): Denmark, Netherlands (pctl ~0.97–0.99); USA at the *low edge* (0.84).
- **Danger zone** (mid-capacity peak): Hungary (9.0%), Bosnia, Tunisia, Sri Lanka, Nepal — the textbook hybrid backsliders.
- Singapore: protected on capacity but a large capacity-over-voice relational gap (institutionalised without voice).

## Invariants (what it does NOT do)
- Does **not** alter pillar scoring, MI weights, tiers, or safeguards. MI v3.3 is untouched
  (`tests/` still 31/31, including the 84-case corpus floor).
- Reads **only** through `mi/panel.py` — the single canonical source. No new data store.
- Reports a **structural position, not a calibrated probability or timing** — backsliding
  triggers are unpredictable ("the Mule"). `backslide_hazard_5y` is the empirical rate for
  the country's capacity decile, not a forecast for that specific country.

## Provenance / calibration
The inverted-U hazard curve (`EMPIRICAL_HAZARD_BY_DECILE`) is the observed 5-year backsliding
rate by capacity decile from the deep panel 1900–2015 (`sandbox/tier_stress/angle6_nonlinear.py`,
`deep_time.py`). Tested in `tests/test_backsliding.py`.
