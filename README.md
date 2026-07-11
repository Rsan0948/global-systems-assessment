# The Modernization Index & Structural Governance Analysis Platform

This repository houses a quantitative research program studying how complex
systems — from river networks to nation-states — accumulate and release
structural complexity. The **Modernization Index (MI)** measures where countries
sit on the institutional-quality spectrum: how much of a nation's prosperity is
structurally *earned* versus circumstantially *granted*. The **fragmentation
research** establishes *why* systems fracture the way they do — self-organizing
systems in a tight, predictable band, engineered systems dispersedly and
catastrophically. The **collectivization study** models *how* political entities
reconsolidate after they fragment. Together they form a structural diagnostic
framework for understanding governance durability. It is a **diagnostic** — it
identifies configurations and vulnerabilities, not destinies.

---

## The three projects

### Modernization Index — `mi-research/`, `mi-pipeline/`, `mi-website/`
A five-pillar governance diagnostic (Institutional Quality 34%, Economic
Structure 20%, Human Capital 16%, Stability 16%, Innovation 15%) scoring **191
countries** and evaluated against a **109-case retrodiction corpus** (84 modern +
25 ancient) spanning ~4,700 years.

> **Robustness finding (2026-07-11).** A pre-registered adversarial program found
> that **institutional structure is the dominant predictor of political rupture
> across pre-modern history** (25 cases, ~4,700 years; AUC 0.66–0.68 vs wealth
> 0.52–0.64), that this signal has been **monotonically eroding for ~150 years**
> (143-polity panel, p = 0.033) in lockstep with modern capital systems, and that
> the erosion is **distortion, not inversion** — structure still leads on armed
> conflict today. Separately, the marketing figure "100% directional accuracy"
> was decomposed and found soft (~20% mechanically recomputable); it is superseded
> by the above. Full record + epistemic labels: `mi-research/docs/ROBUSTNESS_RESULTS.md`.

- **Status:** V3.3 live; automated weekly data refresh; website deployable.
- **Key findings:** institutional quality (P1) is the most central variable in
  the construct (|r| ≈ 0.79–0.80 with everything else); **configuration**
  (balanced pillars) predicts durability better than peak performance on any
  single dimension; a resource-wealth penalty; a global modernization
  deceleration.
- **Entry point:** [`mi-research/MASTER_REFERENCE_ARCHITECTURE.md`](mi-research/MASTER_REFERENCE_ARCHITECTURE.md)

### Fragmentation Research — `fragmentation/`
A cross-domain empirical study of how self-organizing versus designed systems
subdivide, built as a pre-registered discovery program with a sealed-holdout
confirmation protocol.

- **Status:** Concluded at **rung 1** — domain-specific laws, no universal
  constant. Census ongoing.
- **Key findings:** self-organized systems (rivers, neurons, botanical trees,
  human languages) fracture in a **tight band (CV ~0.2)** that beats their
  random-topology null; designed systems fracture **dispersedly**, CV scaling
  monotonically with how engineered they are (~0.3 for corporations up to ~2.3
  for administrative hierarchies); suppression duration predicts rupture
  magnitude.
- **Entry point:** [`fragmentation/SYNTHESIS.md`](fragmentation/SYNTHESIS.md)

### Collectivization Cycle Study — `collectivization/`
A 30-case comparative analysis of fragmentation–collectivization dynamics across
civilizations (25 core + 5 controls), using a 15-binary-feature governance vector
to mechanically classify political forms.

- **Status:** Active — core engine and case data complete, expansion ongoing.
- **Key findings:** predecessor institutional depth predicts restructuring
  magnitude (ρ = −0.84, p < 0.001); among high-depth cases, collectivization
  speed predicts integration loss (ρ = 0.83, p < 0.001); four empirical pathway
  types (construction, restoration, negotiation, redesign); **negotiated**
  collectivizations are the most durable.
- **Entry point:** [`collectivization/README.md`](collectivization/README.md)

---

## How they connect

One principle runs through all three, drawn from
[`fragmentation/SYNTHESIS.md`](fragmentation/SYNTHESIS.md): *a growing system's
interior complexity outruns its interface capacity, and the mismatch must be
released as subdivision.* Grown systems vent continuously (tight, predictable
fracturing); designed systems suppress the venting, so pressure accumulates and
releases catastrophically, in proportion to how long and how rigidly it was held.

- The **fragmentation research** establishes the *physics* — that self-assembly
  fractures tightly and engineering makes fracturing dispersed and severe.
- The **Modernization Index** measures the *state* — it operationalizes the
  complexity–capacity match as a country-level instrument (its P4–P1 durability
  gate, Safeguard J, is the same idea as the fragmentation study's dimensional
  gap; see [`fragmentation/DGS_AND_SAFEGUARD_J.md`](fragmentation/DGS_AND_SAFEGUARD_J.md)).
- The **collectivization study** models the *process* — how fragmented polities
  reconsolidate, and why predecessor institutional depth (a P1-like variable)
  governs the outcome.

They are one intellectual program with three empirical legs. They deliberately do
**not** share code (each is independently runnable and testable); the connection
is conceptual, not an import graph.

---

## Quick start

```bash
# Score a country (Modernization Index)
cd mi-research && python scripts/score_country.py --country "Estonia" --year 2024

# Run the fragmentation census
cd fragmentation/census && python run.py

# Run the full fragmentation ladder + controls + calibrations
cd fragmentation/integration && python run.py

# Run the collectivization cycle analysis
cd collectivization && python run.py
```

Python 3.11+. Core deps: `numpy`, `scipy`, `matplotlib`, `pytest`. Real river
ingestion additionally needs `geopandas`/`pyogrio` (optional, import-guarded);
the MI data pipeline needs `requests`.

---

## Data sources

| Project | Sources |
|---------|---------|
| Modernization Index | World Bank WGI/WDI, UNDP HDR, Transparency International CPI, WIPO GII, Harvard/OEC ECI, Fund for Peace FSI, Maddison Project, V-Dem |
| Fragmentation | HydroRIVERS (HydroSHEDS), NeuroMorpho, Glottolog, SEC EDGAR, ParlGov, GeoNames, NCBI taxonomy |
| Collectivization | Maddison Project, V-Dem, constitutional/legal documents (15-feature coding) |

All sources are public and (where relevant) no-login. Raw multi-megabyte
downloads are git-ignored; derived caches and the committed panels are in-repo.
