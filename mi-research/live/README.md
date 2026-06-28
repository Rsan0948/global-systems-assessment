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

The six-run validation sweep over the 20-case modern baseline. **3 of 6 are
present; runs 4–6 are expected in a later batch.**

| Run | File | Coverage |
|-----|------|----------|
| 1 of 6 | `runs/run1of6_groupA_traditional_fragmentation_cases1-4.md` | Group A, cases 1–4 (Post-Soviet, Yugoslavia, Velvet Divorce, Arab Spring) |
| 2 of 6 | `runs/run2of6_groupA_traditional_continued_cases5-8.md` | Group A, cases 5–8 (Sudan/S.Sudan, Pakistan/Bangladesh, Singapore/Malaysia, Ethiopia/Eritrea) |
| 3 of 6 | `runs/run3of6_groupB_recursive_suppressed_cases9-12.md` | Group B, cases 9–12 (Serbia/Kosovo, Indonesia/East Timor, Ethiopia/Tigray, Nigeria/Biafra) |
| 4 of 6 | _(pending)_ | expected: remaining Group C/D/E cases (13–20) |
| 5 of 6 | _(pending)_ | expected |
| 6 of 6 | _(pending)_ | expected |

## Notes for agents

- These runs introduce the STATIC-vs-LIVE comparison and the per-case (a)–(g)
  prediction scoring that the aggregate results in `../RESEARCH.md` rest on.
  Treat them as the authoritative case record.
- Per the Golden Rule (`../RESEARCH.md`): the 20-case baseline documented here is
  the floor. Any framework modification must not degrade performance on these runs.
- Each run carries its own caveats (WGI 2025 vintage break, ordinal-only scope,
  derived/estimated pillar values for non-dataset countries). Carry them forward.
