# Readiness + architecture — the six deep angles

Verified before executing. Shared substrate = **`common.py`** (imports `deep_time`); every angle imports it so data access, normalization, and rigor primitives are identical (no drift). Rigor bar held throughout: permutation nulls, out-of-sample where predictive, report nulls as loudly as hits, no in-sample AUC.

## Shared substrate (`common.py`) — verified working
- Deep instruments **LIB / ROL / CSO** (176 isos, annual, 1789–2025) + **ONS** conflict onsets; `anocracy`, `pconf`.
- **WGI** capacity (`wgi`, independent of V-Dem, 191 isos 1996–2024).
- Attributes: `resource_rents` (257), `population` (260), `ethnic` (EPR excluded-share/n_groups, 165 isos), `state_age`, `dem_age` (**current spell**, fixed).
- Adjacency: `neighbors` (ISO3 land borders, 163 isos), `HAVE_BORDER`.
- Rigor: `partial_spearman`, `perm_null`, `velocity` (OLS slope over trailing window), `zwithin_year`.

## Per-angle readiness

| # | Angle | Data | Verdict | Script (planned) |
|---|---|---|---|---|
| 1 | **Dynamic (rates)** | LIB/ROL/CSO **100% annual** → clean d/dt; WGI 88% annual | ✅ READY | `angle1_dynamic.py` |
| 2 | **Within-country FE** | 176 ctry, median 24 cohorts; **120 have within-country backslide variation** | ✅ READY | `angle2_within.py` |
| 3 | **Contagion** | ISO3 adjacency for 163 ctry | ✅ READY — **modern-era only** (borders are current; pre-1990 anachronistic) | `angle3_contagion.py` |
| 4 | **Attributes** | resource (257), pop (260), **EPR ethnic in-panel** (165), age derivable | ✅ READY except **colonial/legal origin = GAP** | `angle4_attributes.py` |
| 5 | **Survival/hazard** | 90 transitions, median 36y follow-up; `dem_age` = current spell | ✅ READY | `angle5_survival.py` |
| 6 | **Nonlinear thresholds** | existing deep panel | ✅ READY (method-only) | `angle6_nonlinear.py` |

## Alignment notes / caveats (baked into the substrate)
- **Contagion is modern-only.** `neighbors()` reflects *today's* borders — USSR/colonial empires make deep adjacency wrong. Restrict Angle 3 to ≥1990 (or ≥1960 with care).
- **EPR ethnic data is a single snapshot** (not time-varying) → use as a *static* country attribute/moderator, not a lagged predictor.
- **`dem_age` = current uninterrupted spell** (fixed; Poland 2010→20y, not interwar). Interpretation: V-Dem scores some old democracies' liberal-democracy spell as starting mid-20th-c (USA→~1950 on civil rights) — democracy-age is *liberal*-democracy-spell age, note when interpreting.
- **rol/libdem circularity** (corr ~0.85) is a standing threat for any V-Dem-capacity result → every angle that uses rol as capacity must also cross-check with **independent WGI** and orthogonalize, per `deep_audit.py`.
- All keys are **ISO3**; adjacency `I2I3` handles the iso2→iso3 bridge.

## The one gap — colonial / legal origin (Angle 4)
Not in the repo. Options when we reach Angle 4: (a) add a compact static La-Porta legal-origin table (English/French/German/Scandinavian/Socialist — published, ~150 countries) + colonizer; (b) proxy via region; (c) run Angle 4 on the available attributes (resource, ethnic, size, age) and mark colonial/legal as deferred. **Decision needed at Angle 4, not blocking angles 1–3, 5–6.**

## Execution order (one at a time, per request)
1 Dynamic → 2 Within-country → 3 Contagion → 4 Attributes → 5 Survival → 6 Nonlinear.
Each: build `angleN_*.py` on `common.py`, run, permutation-null + OOS check, write result to the ledger, add a regression test to `test_harness.py`, then pause for the next.
