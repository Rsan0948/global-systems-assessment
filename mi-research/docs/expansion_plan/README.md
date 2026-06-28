# Expansion plan — toward a 50-case baseline

Forward-looking **roadmap** documents (proposals for future work), distinct from:
- the canonical results in `../../live/runs/` (the validated 20-case, 6-run record), and
- the refinement history in `../validation_rounds/`.

These describe how to grow the validated baseline from 20 cases to ~50, which gaps
each new case fills, and which cases are most likely to *falsify* the framework.
Nothing here is scored yet — treat it as the agenda referenced by `RESEARCH.md`
("What Needs Doing"), not as evidence.

## Contents

| File | What it is |
|------|-----------|
| `proposal_30_new_cases_to_50_case_baseline.md` | The main proposal: 30 new cases (Batches 1–6) filling every named geographic/stress-type gap, with per-case data-availability and difficulty ratings, a coverage map, a recommended testing sequence, and a top-5 likely-falsification risk list (Rwanda, Lebanon, Botswana/Gulf rent-stabilization, Mod4 near-ties, Aceh/Bougainville Safeguard I). |
| `case_revisions_replacements_and_bonus_cases.md` | Revisions to that proposal: replaces two overlapping cases (Singapore-standalone → Mauritius; Ethiopia-federal → Cameroon) to maximize independent information, promotes Somaliland/Somalia into the core (→51 cases), and retains bonus candidates (Zimbabwe, Hong Kong, Afghanistan) for future rounds. Also flags the "Rwanda architectural decision" — whether P1 must be decomposed into capacity vs. accountability — as a prerequisite call before running the batches. |

## Notes for agents

- Read `case_revisions_replacements_and_bonus_cases.md` *after* the proposal — it
  amends rather than replaces it.
- Per the Golden Rule (`../../RESEARCH.md`): any new case or safeguard must not
  degrade performance on the existing 20-case baseline in `../../live/runs/`.
- New cases should be scored with the same per-case (a)–(g) prediction discipline
  and STATIC-vs-LIVE comparison the runs use, and structured records added under
  `../../data/case_studies/` (template in `data/case_studies/templates/`).
