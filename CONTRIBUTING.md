# Contributing

The most valuable contribution to this project is **adversarial**: try to
break it. The repo is built around falsification discipline — frozen
hypotheses, null samplers, holdouts, and a public claims ledger — so a
failed replication or a killed claim is a contribution, not a complaint.

## Highest-value contributions

1. **Independent recoding of the historical tiers.** The ancient tier
   (n=25) and supercycle tier (n=3) are interpreter-scored by a single
   coder with hindsight. A second coder working from the published
   criteria (`mi-research/docs/historical_scoring_protocol_v1.md`) would
   materially change the project's confidence.
2. **Replication of the languages fragmentation result** with different
   tree sources or reconstruction methods (the current result rests on
   Glottolog family trees, which are linguist reconstructions —
   method-artifact controls are an open question).
3. **Kirchner-null extensions** — alternative null models for tree-shape
   baselines beyond frozen-seed random binary trees.
4. **Out-of-sample challenges** — run the sealed-flag logic on countries
   or windows the author did not select, and report what happens.
5. **Source corrections** — every curated claim carries per-stat sources;
   if one is wrong, misdated, or misattributed, that is a ledger event.

## Ground rules (inherited from the project's own discipline)

- **Primary data over derived indices** for any scoring change. Composite
  inputs must be justified against the DGS null lesson
  (`fragmentation/DGS_AND_SAFEGUARD_J.md`).
- **Null samplers before any discovery claim** (Kirchner 1993 discipline).
- **Holdout/CI isolation**: never tune on a holdout; if a claim needs a
  threshold, the derivation set must be named.
- **Tag every claim** with its epistemic status: `[demonstrated]`,
  `[curated]`, `[exploratory]`, `[pending]`, `[retired]`. The ledger in
  `mi-research/docs/curated/` is the single source of truth.
- **Never rewrite history.** Retired claims stay in the ledger with their
  kill evidence. Corrections go in new commits; the audit trail is the
  product.
- Data sources are used under their own licenses — keep attribution
  intact (README → Data sources).

## Process

1. Open an issue first for anything beyond a typo — especially for
   scoring, threshold, or taxonomy changes.
2. Keep PRs atomic: one claim, one fix, or one replication per PR.
3. Include seeds, commit SHAs, and sample windows for any numeric claim.
4. Expect to be asked for a null model. That is the culture, not a snub.

## Where things live

- `fragmentation/` — census, discovery, integration, preregistration,
  governance
- `mi-research/` — MI engine, tiers, backsliding, ledger, sealed flags
- `collectivization/` — 30-case casebook, classifier, cycle engine
- `atlas/` — 6,000-year capital-hubs narrative + data
- `sandbox/` (root and under `mi-research/`) — exploratory work; nothing
  here is a shipped claim
