# The Fragmentation–Collectivization Cycle Study

A 30-case comparative analysis (**25 core + 5 controls**) of how political
entities reconsolidate after fragmentation, across China, the EU, Maurya and
Mughal India, Muscovy Russia, the Netherlands, Silla Korea, the Inca, Gran
Colombia, and more — spanning ~4,000 years. Political forms are classified
**mechanically** from a 15-binary-feature governance vector, so the analysis
measures how much a polity changes through a cycle without hand-waving about
regime "type."

This is the **process** leg of the platform: the Modernization Index measures a
country's *state*, the fragmentation research establishes the *physics* of how
systems fracture, and this study models how fractured polities come back together.

> **Diagnostic, not predictive.** The study classifies forms and measures
> restructuring magnitude and durability. It does not predict specific outcomes.

## The three hypotheses

1. **Ratchet** — do collectivization cycles monotonically increase integration
   depth (a one-way ratchet toward tighter union)? **Result: not supported**
   (sign-test p = 0.64). Integration is not a ratchet; polities lose depth too.
2. **Form-shift** — does a collectivization cycle change a polity's *type* (its
   feature vector crosses a template boundary)? **Result: supported** — most
   cases shift form, though not all types shift.
3. **Timing–intensity** — do the *speed* and *conflict intensity* of
   collectivization predict how much integration is gained or lost? **Result:
   supported** for the high-depth subset (see below).

## Key findings

*Verified against `results/cycle_analysis.json`.*

- **Predecessor depth predicts restructuring magnitude:** depth → flip-count
  Spearman ρ = **−0.84**, p < 0.001. A deeper predecessor flips fewer governance
  features — an **institutional-ceiling** effect.
- **Speed predicts integration loss:** among high-depth cases, collectivization
  speed → integration-features-lost ρ = **0.83**, p < 0.001. Fast collectivization
  of a deep predecessor loses more integration.
- **Four empirical pathway types**, with **negotiation** the most durable
  (mean durability 308 vs 119–149 for the others):

  | pathway | count | mean durability |
  |---|---|---|
  | construction | 13 | 118.7 |
  | restoration | 5 | 131.2 |
  | negotiation | 4 | 308.0 |
  | redesign | 3 | 148.7 |

- **Dominant mechanism channel:** coordination failure.
- **Warning-signals framework** operational (0.76 hit rate on cases with
  sufficient data).

## The 15-feature governance vector

Each case is coded on 15 binary features verifiable from constitutional
documents, legal codes, or observable institutional facts (two researchers
reading the same documents check the same boxes): single executive, hereditary
succession, independent militaries, independent foreign policy, shared currency,
shared legal code, unilateral exit, central tax reaching individuals, popular
sovereignty, elected leadership, free movement of persons, free movement of
goods, shared supreme court, central standing army, and pre-existing polities.
**Feature definitions and the reference type-templates are fixed BEFORE any case
is coded** (the pre-registration equivalent) — see `feature_vector.py`. A case's
form is the nearest template; a *form-shift* is when pre- and post-cycle vectors
map to different templates.

## Failure modes and warning signals

- `failure_catalog.py` — a catalog of the ways collectivizations fail (the
  coordination-failure channel dominates).
- `warning_signals.py` — an operational framework flagging efficiency decay,
  integration reversal, and legitimacy erosion where the data supports it.
- `ratchet.py`, `form_shift.py`, `pathway_analysis.py`, `timing_intensity` in
  `cycle_engine.py` — the four analysis stages behind the findings above.

## The 25 core cases and their pathways

| case | pathway | integration depth (pre→post) | durability |
|---|---|---|---|
| China | construction | 0→6 | 15 |
| European Union | construction | 1→5 | 33 |
| Argentina | redesign | 5→6 | 144 |
| Australia | construction | 2→5 | 123 |
| Brazil | redesign | 5→6 | 144 |
| Canada | construction | 2→5 | 153 |
| Egypt (Middle Kingdom) | restoration | 5→5 | 200 |
| Inca (Tawantinsuyu) | construction | 0→5 | 40 |
| Korea (Silla) | construction | 0→5 | 259 |
| Russia (Muscovy) | negotiation | 5→5 | 370 |
| Switzerland | construction | 1→6 | 176 |
| Ethiopia | restoration | 5→6 | 85 |
| France | negotiation | 6→3 | 128 |
| India (Maurya) | construction | 0→6 | 137 |
| India (Mughal) | restoration | 6→6 | 154 |
| Netherlands | construction | 2→3 | 207 |
| Persia (Safavid) | restoration | 6→6 | 134 |
| Poland-Lithuania | negotiation | 6→3 | 226 |
| Spain | negotiation | 6→2 | 508 |
| Vietnam | restoration | 6→6 | 83 |
| Zulu Kingdom | construction | 2→5 | 51 |
| Germany | construction | 1→6 | 47 |
| Italy | construction | 0→6 | 165 |
| Japan | construction | 0→6 | 137 |
| United States | redesign | 5→6 | 158 |

Plus 5 controls (Greek poleis, post-Ottoman Middle East, post-Soviet space,
sub-Saharan Africa, and one comparative baseline) used to check that the engine
distinguishes genuine collectivization cycles from mere co-location.

## Connection to the Modernization Index

The **institutional-ceiling** result — predecessor integration depth predicts how
much a polity can restructure — is the collectivization analogue of the MI's P1
(Institutional Quality). Predecessor depth behaves like a P1-like variable: deeper
prior institutions constrain and shape the reconsolidation, exactly as the MI
finds P1 to be the load-bearing pillar for durability. See
`../mi-research/MASTER_REFERENCE_ARCHITECTURE.md` and the fragmentation
dispersion dial (`../fragmentation/SYNTHESIS.md`), of which political
fragmentation/collectivization is the human-governance instance.

## Quick start

```bash
python run.py                 # runs on the pre-built case JSONs -> results/
python run.py --build-cases   # rebuild cases from Maddison/V-Dem first
pytest -q -p no:cacheprovider # 315 tests
```
