# Golden-age signature — PRE-REGISTRATION (frozen before the holdout was inspected)

**Frozen: 2026-06-28**, before the unseen WGI countries were pulled/inspected. This fixes the test in
git so the geographic-holdout confirmation cannot be re-tuned after the fact. Mirrors the root
project's discover/confirm discipline.

## The frozen claim (discovered on the 89-country set)
A **control-of-corruption (CC) punctuated jump** forecasts a durable institutional climb better than
the base rate.

## Frozen definitions (NOT to be changed after seeing the holdout)
- **Event (signature):** in country-year `t`, `CC(t+2) − CC(t) > 0.05` AND `CC(t) < 0.65` (room to
  rise). CC, P1 in 0–1 (P1 = mean of GE/RL/RQ/CC). Requires ≥5y forward P1 data.
- **Outcome (durable climb):** `P1(t+7) − P1(t+2) > 0.03` (use `t+5` if `t+7` missing) — institutions
  keep climbing *after* the jump.
- **Base rate:** among all country-years with forward data, the fraction followed by a durable climb
  (same outcome definition).
- **Success criterion:** event durable-rate > base-rate, one-sided two-proportion z, **p < 0.05**.

## Holdout design
- **Discovery set:** the 89 countries already in `data/sources/wb_anchored.json` (where the signature
  was found — Georgia, Rwanda, post-Soviet/Balkan reformers, etc.).
- **Holdout set (the test):** all WGI economies NOT in the discovery set (the ~120 unseen countries,
  `data/sources/wgi_full_panel.json`). Never inspected during discovery.
- The headline verdict is the **holdout** result. Secondary: full-panel pooled, and whether the
  temporal-null (2011–2017 events showed no lift in discovery) recurs.

## Pre-registered interpretation
- **PASS** (holdout event-rate > base, p<0.05): the CC-jump golden-age signature is real and general.
- **FAIL** (no lift in holdout): the in-sample/discovery-era signal (38% vs 23%, 1996–2010) was a
  **post-communist/EU-accession transition-era artifact**, not a general law — itself a rich finding
  (golden ages are wave/era-driven, not predictable from a country's own CC trajectory).
- No re-tuning of thresholds post-holdout. If the signature fails, exploratory follow-ups (other
  components, starting level, regional/era waves) are reported as **new exploration**, clearly
  separated from this frozen confirmation.
