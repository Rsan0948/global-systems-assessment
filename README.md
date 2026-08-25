# universalsystemgrade

A public research workspace for testing structural claims about human and
natural systems. It contains three connected research programs and one
authoritative claims ledger.

> **Status: pre-publication research code.** Every claim in this repo is
> tagged by epistemic status. Read the ledger section below before citing
> anything.

---

## Read this first: the claims ledger

This project keeps failed ideas visible. That is part of the method, not a footnote.

The authoritative record is [`mi-research/docs/CLAIMS_LEDGER.md`](mi-research/docs/CLAIMS_LEDGER.md). A machine-readable copy lives at [`mi-research/data/claims/claims.json`](mi-research/data/claims/claims.json). If another summary disagrees with the ledger, the ledger wins.

The ledger records two separate things for every claim:

- **Evidence design:** descriptive, hindsight retrodiction, blind out-of-sample, prospective, interpretive, or simulation.
- **Verdict:** supported, mixed, not supported, pending, or retired.

### The counts, without mixing them together

- The historical MI corpus contains **109 case studies**: 84 modern hindsight-retrodictive cases and 25 ancient interpreter-scored cases.
- The MI out-of-sample program contains **67 observations** across several blind cohorts. Its results are mixed.
- The relational layer contains **12 firewalled records**.
- The collectivization study is separate. It contains **30 cases and 109 formation cycles**.
- The public atlas currently contains **190 scored country pages**. Those pages are descriptive outputs, not validation cases.

### What the evidence currently supports

- River branching concentration passed a discovery and sealed geographic holdout.
- The MI score is deterministic for fixed inputs, but determinism does not establish prediction.
- The 84 modern historical cases show hindsight-retrodictive consistency.
- The P4 minus P1 durability gap recorded 17 of 19 in its derivation set. That is not a forward validation record.
- The backsliding inverted-U recorded an out-of-sample AUC of 0.746 and remains provisional.
- The collectivization depth result records rho = -0.84 within a curated historical dataset that still needs independent recoding.

### What failed or remains open

- The proposed universal constant near Euler's number was retired.
- The current DGS instability test was null.
- The preregistered golden-age forward test failed.
- The general collectivization ratchet was not supported.
- The sealed country flags are pending and cannot yet count as predictive evidence.
- The grand synthesis remains a research agenda, not a validated law.


---

## The three engines

**A. Fragmentation** (`fragmentation/`) - how systems subdivide.
Horton–Strahler / Tokunaga analysis with Kirchner-null discipline,
applied across rivers, neurons, trees, blood vessels, corals, fungi,
languages, corporations, political parties, religious bodies, military
units, administrative subdivisions, and state dissolutions.
`fragmentation/census/run.py` → `fragmentation/census/results/`.

**B. Modernization Index** (`mi-research/`, `mi-pipeline/`,
`mi-website/`) - five pillars (institutions, household position,
pressure, capacity, revealed system), six tiers of forward risk, scored
1900–2024 for 190+ countries. T1 gap → T2 topology → T3 momentum →
T4 scarring → T5 turbulence → T6 coupling. Tiers 5–6 are exploratory
and were weakened by the project's own adversarial audit (full six-tier
OOF AUC 0.63) - the corrected numbers are in
`docs/THREE_MODEL_FRAMEWORK.md`. Public site:
[mi-website/](mi-website/) (Next.js, deployed via Vercel).

**C. Collectivization** (`collectivization/`) - how polities reassemble.
A mechanical 15-binary-feature governance vector and Hamming-distance
classifier over 109 formation cycles in 30 cases spanning 1,143 years.
`collectivization/run.py` → `collectivization/results/`.

Context: `docs/capital_hubs_atlas.md` - 6,000 years of capital hubs as the capital-suppression
baseline; `docs/` - glossary, sources, unified timeline.

---

## What this is not

- **Not a rating agency.** Scores are structural readings of information-
  processing architecture, not league tables or moral judgments. The
  instrument is a **diagnostic** - it identifies configurations and
  vulnerabilities, not destinies.
- **Not a collapse predictor.** Structure is knowable 10–28 years out;
  timing is knowable 3–5 years at best. Tier 5 stress tests failed their
  10% ceiling and were honestly downgraded - the countdown lives in
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
