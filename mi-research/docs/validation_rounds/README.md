# Validation rounds — the refinement history

These documents are the **process record** of how the MI score was tested and
refined over time — the retrodiction studies behind the 20-case modern baseline
summarized in `../../RESEARCH.md` ("What's Been Done"). They are **not** the
canonical run 1–6 reference (that is the source-of-truth scoring record and lives
in the project's working/live area; it will be added separately).

Treat these as evidence and derivation history: each round runs ~5 new (or
re-examined) cases, scores the framework's predictions honestly, and — crucially —
is where each Safeguard and Mod was *derived*. The headline rates climbed across
rounds (Round 1 ≈ 64% clean / 88% directional → aggregate ≈ 78% / ~100% directional
in the LIVE version) as safeguards were added.

## Contents

| File | What it is | Cases | Derived / tested |
|------|-----------|-------|------------------|
| `round1_backtest_five_fragmentations.md` | **Round 1** — original backtest, no safeguards yet (~64% clean). Found the successor-count heuristic falsified and *recommended* the first safeguards. | Post-Soviet, Yugoslavia, Velvet Divorce, Arab Spring, Sudan/South Sudan | → motivates Safeguards A, B, C |
| `round1_diagnostic_safeguards_A-C_five_cases.md` | Re-run of the Round 1 cases **with Safeguards A/B/C applied** — validates them on the original five. (Position in the sequence is inferred from content: same five cases as Round 1, but safeguards now operational. Title as published: "Testing the MI: A Five-Case Diagnostic.") | same five as Round 1 | tests A, B, C |
| `round2_validation_five_cases.md` | **Round 2** — five new cases (~66% clean / ~90% directional, holds baseline). | Ethiopia/Eritrea, India/Pakistan/Bangladesh, Indonesia/East Timor, Serbia/Kosovo, Singapore/Malaysia | confirms A/B/C; flags rentier-capture, violence-source (→ E, Mod8) |
| `round3_validation_structural_stress.md` | **Round 3** — five new cases; broadens to reconstruction/fusion. | Pakistan/Bangladesh, Ethiopia/Tigray, South Africa, Northern Ireland/GFA, German Reunification | high-P1 turbulence blind spot (→ Safeguard F) |
| `round4_validation_structural_stress.md` | **Round 4** — five structural-stress cases (5/5 ordinal confirmed). | Nigeria/Biafra, Spain/Catalonia, Myanmar, Baltics vs Central Asia, Belgium | → Safeguards F, G (three-tier suppression), bidirectional E |

## Notes for agents

- These are **narrative** validation reports. The structured, machine-readable
  case records belong in `../../data/case_studies/completed/` (follow
  `data/case_studies/templates/case_template.json`); building those JSON cases
  from these narratives is open work.
- The aggregate "~78% clean / ~100% directional / 20-of-20 P1 ordinality" claim in
  `RESEARCH.md` rests on Rounds 1–4 here plus the LIVE safeguards/mods. Each round
  also documents its own caveats (WGI 2025 vintage break, small-N, confirmation
  risk) — carry those forward; don't launder them out.
- Per the Golden Rule, any modification must not degrade performance on these
  baseline cases.
