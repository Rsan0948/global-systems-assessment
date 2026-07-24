# universalsystemgrade

An open research platform testing whether human macro-systems — like
self-organizing physical systems — obey structural law. Three engines,
one claims ledger, zero astrology.

> **Status: pre-publication research code.** Every claim in this repo is
> tagged by epistemic status. Read the ledger section below before citing
> anything.

---

## Read this first: the claims ledger

This project kills its own ideas in public. That is not a caveat — it is
the method. Before citing any result, check its tag. The authoritative
ledger lives at `mi-research/docs/curated/CLAIMS_AND_EPISTEMIC_STATUS_LEDGER.md`;
this is the summary.

**`[demonstrated]` — systematic-data tier, passed preregistered gates**

- Grown systems subdivide in a tight band; engineered systems disperse.
  Rivers Rb 4.55 ± 0.24 (σ/μ ≈ 0.053, n=60, null-p < 0.000001).
  Languages fall in the same band (3.40, CV 0.20, discovery).
  Corporate splits (2.16) and party splits (2.06) fall below it.
  The diagnostic is **dispersion, not central value** — grown vs
  designed is the dial.
- Rule-of-law erosion is functionally corroborated (NL/UK/US vs DE,
  r = 0.64) — while raw proxy degradation (DGS) is a **reported null**
  (β=0.107, p=0.42, zero AUC gain). That null is why this repo exists.
- Tier 1 durability gap P4−P1: AUC 0.855 (n=246, era-relative z-scores);
  validated 17/19 on a derivation set — **hindsight-calibrated**, the
  forward test is the sealed flags below.
- Democratic backsliding risk is an inverted-U in rule-of-law capacity,
  peaking mid-capacity, with a safety ceiling near the 80th percentile
  (OOS AUC 0.746; beats democracy level itself). Post-1945 decoupling
  of democratic form from state capacity is a structural determinant of
  today's backsliding stock.

**`[curated]` — systematic method, curated or interpretive samples**

- Institutional quality is more stable than economic output (5/6 tests,
  26/28 windows; σ_inst = 4.1 vs σ_econ = 13.3).
- The dominant fragmentation pathway is simplification: children
  systematically *lose* parent function dimension (12/13 cases).
- Collectivization leg (n=30, 109 cycles): deep predecessor →
  restoration, shallow → flips (ρ = −0.84); negotiated unions ~2× more
  durable than conquests (n=4, exhibition-only); archetype accuracy
  21/30 (70%), null p = 0.015.
- The 150-year erosion: institutions' edge over GDP in predicting
  instability eroded because **wealth caught up** — GDP became a
  complementary state-capacity measure (confirmed pre-registered;
  structure holds; p-values are bootstrapped [inferred]).

**`[exploratory]` — recorded patterns, unconstrained mechanism**

- Movement typology: headline stability decomposes as windfall, hollow
  stability, real ascent, or real decay (G7 = windfalls + hollow
  stability + one resource economy).
- Atlas: capital-hub divergence is metastable; the largest hubs sit in
  slow-decay basins.
- T5 turbulence: crisis-recurrence variance confirmed, growth slowdown
  confirmed (placebo-passed); AR1 null; poverty-growth link died.

**`[pending]` — sealed forward flags, grading ~2030–2034**

- Acute: US, UK, Chile. Floor: Russia, Belarus, Kyrgyz Republic, Mali.
  Each flag has a written falsification condition and watch signals in
  `mi-research/data/forecasts/sealed_flags_2024.json` (sha256-sealed
  2024-05-13). The acute-timing signature is calibrated on n=2 turns —
  disclosed in the file itself.

**`[retired]` — killed by the project's own tests. Do NOT cite as live.**

- ~~A universal subdivision constant (e)~~ — executed at rung 2.
- ~~Golden-age signature~~ — zero lift on a frozen holdout.
- ~~Capital suppression→release thesis~~ — **reversed** on its own
  preregistered test (ρ = −0.218, all 18 cells; long-held gaps mark
  self-stabilizers). The system-level thesis survives only as a live
  observation with no mechanism.
- ~~Ratchet / magnitude limb~~ — null and reversed, respectively.
- ~~Eight rival explanations for the erosion finding~~ — twelve
  consecutive registered nulls (composition, consequence-elimination,
  perception lag, external support, decoupling, gold standard,
  contagion shift, inequality, variance compression, conflict-type
  shift, and more). Full kill sheets in `mi-research/docs/curated/`.

The graveyard is the map. Full audit trail: `mi-research/RESEARCH.md`,
`mi-research/docs/curated/GRAND_SYNTHESIS.md`, and the git history
itself — hypotheses were frozen, tested, and corrected in sequence, and
nothing was squashed away.

---

## The three engines

**A. Fragmentation** (`fragmentation/`) — how systems subdivide.
Horton–Strahler / Tokunaga analysis with Kirchner-null discipline,
applied across rivers, neurons, trees, blood vessels, corals, fungi,
languages, corporations, political parties, religious bodies, military
units, administrative subdivisions, and state dissolutions.
`fragmentation/census/run.py` → `fragmentation/census/results/`.

**B. Modernization Index** (`mi-research/`, `mi-pipeline/`,
`mi-website/`) — five pillars (institutions, household position,
pressure, capacity, revealed system), six tiers of forward risk, scored
1900–2024 for 190+ countries. T1 gap → T2 topology → T3 momentum →
T4 scarring → T5 turbulence → T6 coupling. Tiers 5–6 are exploratory
and were weakened by the project's own adversarial audit (full six-tier
OOF AUC 0.63) — the corrected numbers are in
`mi-research/docs/curated/THREE_MODEL_FRAMEWORK.md`. Public site:
[mi-website/](mi-website/) (Next.js, deployed via Vercel).

**C. Collectivization** (`collectivization/`) — how polities reassemble.
A mechanical 15-binary-feature governance vector and Hamming-distance
classifier over 109 formation cycles in 30 cases spanning 1,143 years.
`collectivization/run.py` → `collectivization/results/`.

Context: `atlas/` — 6,000 years of capital hubs as the capital-suppression
baseline; `docs/` — glossary, sources, unified timeline.

---

## What this is not

- **Not a rating agency.** Scores are structural readings of information-
  processing architecture, not league tables or moral judgments. The
  instrument is a **diagnostic** — it identifies configurations and
  vulnerabilities, not destinies.
- **Not a collapse predictor.** Structure is knowable 10–28 years out;
  timing is knowable 3–5 years at best. Tier 5 stress tests failed their
  10% ceiling and were honestly downgraded — the countdown lives in
  Tier 6 coupling, which is directional and exploratory.
- **Not neutral to gaming.** V2's equity pillar can be gamed by
  authoritarian statistics; automated scoring can flatten edge cases;
  historical tiers are interpreter-scored with hindsight. All documented
  in the ledger.

## Quick start

```bash
python -m pip install -r requirements.txt

# Score a country
cd mi-research && python scripts/score_country.py --country "Estonia" --year 2024

# Backsliding danger-zone diagnostic
python scripts/assess_backsliding.py --country "Hungary"

# Run the other legs
cd ../fragmentation/census && python run.py
cd ../integration && python run.py
cd ../../collectivization && python run.py
```

Full reproduction paths and expected outputs: **[REPRODUCE.md](REPRODUCE.md)**.

## Contributing

The most valuable contribution is adversarial: independent recoding of
the historical tiers, replication of the languages result with different
tree sources, Kirchner-null extensions, out-of-sample challenges to the
sealed flags. See **[CONTRIBUTING.md](CONTRIBUTING.md)**.

## Data sources

V-Dem v15, WGI 2024, WDI, Polity5, UCDP/PRIO v25.1, Glottolog 5.2, WALS,
GEM/OPPID, HYDE 3.3, Seshat, FAO GAUL, ITU, SEC EDGAR, ParlGov, Varieties
of Party Identity, UDS, PRC BEPS, plus historical collections (Maddison,
CINC/NMC, Geacron, OWID). All upstream data used under their own licenses.

## License & citation

Code: MIT. Documents, analyses, and curated datasets: CC BY 4.0. See
[LICENSE](LICENSE) and [CITATION.cff](CITATION.cff).
