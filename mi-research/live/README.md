# live/ — canonical run record (source of truth)

This holds the **canonical validation runs** the MI work is built on — the
"run 1–6" series. These are the source-of-truth record, distinct from the
exploratory refinement history in `../docs/validation_rounds/` (the "Round 1–4"
studies, ancient extension, and blind-prediction study, which are *how* the score
was tested and refined, not the canonical record).

> Naming: placed under `live/` per the project's "LIVE" framework branding (the
> runs validate the LIVE version with Mods + Safeguards A–I). If you'd rather this
> live under `data/baselines/` ("validated baseline results — do not modify",
> per RESEARCH.md), it can be moved; the content is the same.

## runs/

The original six-run validation sweep over the initial 20-case modern baseline.
**All 6 runs are present.** Runs 1–5 score cases; Run 6 is the definitive synthesis.
The corpus has since expanded to 84 modern cases (51 ordinality + 19 durability-gate
+ 14 rule-validation) plus 25 ancient; see `../data/case_studies/completed/README.md`.

| Run | File | Coverage |
|-----|------|----------|
| 1 of 6 | `runs/run1of6_groupA_traditional_fragmentation_cases1-4.md` | Group A, cases 1–4 (Post-Soviet, Yugoslavia, Velvet Divorce, Arab Spring) |
| 2 of 6 | `runs/run2of6_groupA_traditional_continued_cases5-8.md` | Group A, cases 5–8 (Sudan/S.Sudan, Pakistan/Bangladesh, Singapore/Malaysia, Ethiopia/Eritrea) — only run with an audited count (21/25, 84%) |
| 3 of 6 | `runs/run3of6_groupB_recursive_suppressed_cases9-12.md` | Group B, cases 9–12 (Serbia/Kosovo, Indonesia/East Timor, Ethiopia/Tigray, Nigeria/Biafra) |
| 4 of 6 | `runs/run4of6_groupC_nontraditional_cases13-17.md` | Group C, cases 13–17 (South Africa, Northern Ireland, Germany, Spain/Catalonia, Belgium) |
| 5 of 6 | `runs/run5of6_groupD-E_comparative_prospective_cases18-20.md` | Group D cases 18–19 (Baltics vs Central Asia; India/Pakistan/Bangladesh) + Group E case 20 (Myanmar, prospective) |
| 6 of 6 | `runs/run6of6_definitive_synthesis_20cases.md` | Definitive synthesis: master scorecard, STATIC-vs-LIVE verdict, honest ~62–85% (best ~78%) confirmation range, zero falsifications, WGI-redundancy caveat |

### Headline result (per Run 6)
~130 discrete predictions across 20 cases, **zero outright falsifications**, clean
confirmation ~78% best-estimate (62% strict – 85% generous). LIVE (Mods 1–12 +
Safeguards A–I) ≥ STATIC in every run. Reported honestly as a range, ordinal/
directional only — not a calibrated forecaster, and the capacity construct is
partly redundant with WGI standalone.

## Notes for agents

- These runs introduce the STATIC-vs-LIVE comparison and the per-case (a)–(g)
  prediction scoring that the aggregate results in `../RESEARCH.md` rest on.
  Treat them as the authoritative case record.
- Per the Golden Rule (`../RESEARCH.md`): the full 84-case modern corpus is
  the floor. Any framework modification must not degrade performance on existing cases.
- Each run carries its own caveats (WGI 2025 vintage break, ordinal-only scope,
  derived/estimated pillar values for non-dataset countries). Carry them forward.
