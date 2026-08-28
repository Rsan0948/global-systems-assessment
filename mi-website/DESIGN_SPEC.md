# Modernization Index Website — Design Specification

**Version:** 0.2 **Date:** 2026-06-30 **Status:** live at https://web-gamma-bice-97.vercel.app
(190 countries, full coverage with visible gaps; data pipeline wired via `scripts/refresh_and_build.py`
+ `.github/workflows/update-mi-data.yml`)

> v0.2 supersedes v0.1 (2026-06-27). v0.1 predated the relational/exposure tier and the project's
> honesty reckoning; it led with "Zero falsifications" and was an academic platform (contribution
> portal, peer review, freemium gating). v0.2 reorients around three principles, adds the relational
> layer, makes the public source code the source of truth, and makes intellectual honesty a
> visible feature rather than fine print.

---

## 1. The concept

**The site is the engine, running in public.** Not a site *about* the Modernization Index — the index
*itself*, alive: fed by public data, computed by a public deterministic engine, showing its
work, placing every country *in relation to* others, and honest about its own edges. The metaphor is a
**diagnostic instrument / observatory for how nations weather stress** — serious, transparent, alive —
not a crystal ball and not a ranked list.

## 2. Three principles (these resolve every fork)

1. **Relationships are the primary object, not scores.** A country is never shown alone — it's placed
   against its peers, against its own wealth (the durability gap), and against its neighbors (the
   relational/exposure layer). Most index sites are ranked lists; this one shows the geometry.
2. **Transparency is the product.** Every number traces to a source and a date; the engine is open
   source; the gaps are visible; "run it yourself" is one click away. The openness *is* the credibility.
3. **Honesty as authority, not apology.** Confident front door; candid limits one graceful layer down.
   The candor is a flex — it signals rigor — never a hedge. Lead with what it does; never bury a caveat
   in a way that reads as weakness.

## 3. Information architecture

```
/                  Landing — the living map (layers: structure / coverage / relations)
/country/:slug     Country page — the heart
/atlas             Explorer — rank, filter, compare, find peers
/stories           Curated case studies (pop-culture reframes; the book holds the full library)
/stories/:slug     One case study
/how-it-works      Methodology, layered: plain -> technical -> "run it yourself"
/limits            "What this can and can't tell you" (honesty, with authority)
/data              Download everything + link to the public source repository
/signals           Structural-change feed (the living part — diagnostic, never forecast) [later phase]
```

**Cut from v0.1** (served an academic platform, not a public instrument): contribution portal, peer
review, contributor profiles, community threads, freemium case-study gating, the "accuracy
leaderboard." The book + the open engine do the field-building.

## 4. The country page (the heart)

A top-down drill: a person gets the headline in five seconds and can fall as deep as they want.
**Show what we have; make what we don't have visible.**

1. **Verdict** — name, region, and an engine-generated plain-language one-liner ("Granted prosperity —
   wealth has outrun institutions — internally lopsided"), plus the tier.
2. **The fingerprint — classifier chips.** One row of self-explaining badges, one visual grammar across
   all classifier families:
   - *Computable for every scored country:* `Tier`, `Earned/Granted prosperity` (durability gap),
     `Shape` (balanced / lopsided + weakest pillar), `Resource-dependent`, `Aid-dependent`.
   - *Where we have the data:* safeguards firing, strategy, and the **relational chips**
     (`Aggressive neighbor`, `Contested border`, `Patron-shielded`, `Standing alone`,
     `Great-power frontier`). Absent → shown as "not yet assessed," honestly.
   Every chip is clickable → what it means · the deterministic rule that set it · the historical cases
   it came from · **how many countries share it now**. The chip is the core UI primitive and is exactly
   "which classifiers belong to this country."
3. **The shape** — five-pillar radar; **missing pillars drawn as empty greyed axes labeled "no data,"**
   not omitted. Peer-overlay toggle (self-contextualization).
4. **Earned or granted** — the durability gap as one clean institutions-vs-income visual.
5. **The neighborhood** (web-native, new) — a small ego-network + placement in the exposure × durability
   2×2. "Not yet assessed" where relational data is absent.
6. **Echoes** — similar configurations; "countries that looked like this under stress" → story links.
7. **What we don't know** — coverage strip: indicators present/missing, each value's source + date, last
   computed, "download / re-run this country."

## 5. Landing — one globe, three layers
Honest hero (NOT "zero falsifications"): *"A structural diagnostic of how nations weather stress. Look
up any country — see how it's built, and what we can't yet see."* One interactive map, layer toggle:
- **Structure** — colored by tier/durability (default).
- **Coverage** — the **dark map**: unscored countries glow dark. Honest at global scale (V1: ~91 scored,
  the rest dark) and a standing argument for better data.
- **Relations** — who threatens whom, who shields whom (the exposure web). Showpiece; phase 2.

## 6. Stories (pop-culture reframes)
A curated ~15–20, chosen by **cultural pull**, not pedagogy (fall of Rome, the Spanish conquest of the
Aztecs/Inca, the post-Soviet trio, the fall of Kabul, the Gulf War, Venezuela, the Arab Spring fan-out,
the two Koreas, the Velvet Divorce). One shape each: *familiar event → what everyone thinks happened →
what the structure shows → the reframe → an optional "make your own read first" → the honest confidence
level* (firewalled-ancient cases say so — a hook, not a liability). Keep predict-before-reveal as
engagement, NOT as an accuracy score.

## 7. The honesty model
- **Front door:** confident, no caveats in the hero.
- **One layer down:** `/limits` — "what this can & can't tell you," written with authority (level vs.
  slope; diagnostic not forecast; hindsight vs. blind selection). A flex.
- **Inline, ambient:** a date on every number, a confidence tier on every story, gaps visible.

## 8. Architecture — the living engine (the reproducible chain)
```
[public source repository]  keystone; deterministic, pip-installable, its own tests
        | consumed by, NEVER reimplemented in JS
[scheduled pipeline]   pulls public APIs (WGI/V-Dem/Maddison/WDI + COW/ATOP/ICOW) ->
                       runs the engine -> publishes a versioned public dataset (JSON) +
                       detects changes
        v
[the site]   reads the published dataset (static-fast); a small DB holds only dynamic
             bits (signals history, user reads)
```
Every number links to its **source · date · "run this yourself."** Chain = open engine + public data +
published outputs, verifiable end to end. **Decision: the Python engine in `../mi-research/mi/` is the
single source of truth; the site is a pure consumer. No scoring math in JavaScript.**

**Stack:** Next.js (App Router) + Tailwind; the Python engine as a scheduled job publishing JSON;
Postgres (Supabase) only for dynamic data; **MapLibre** (open, not Mapbox); deploy on **Vercel**.

**V1 data:** `scripts/build_site_dataset.py` (in mi-research) runs the engine over the 91 scoreable
countries → `mi-website/web/public/data/countries.json` (+ per-country files). Pipeline/auto-update is
a later phase; V1 ships a committed generated dataset.

## 9. Design language
Dark, data-dense, serious — pulled a half-step from "trader terminal" toward **precision scientific
instrument**: room around the map and the relational network; serif headers (authority); **monospace
for every number** so data always reads as data. The feeling: a beautifully-made instrument you trust
*because* it's serious and unafraid to show its limits.
Palette (from v0.1, kept): bg `#0A0A14` / cards `#12121F` / borders `#1E293B`; tier scale emerald→blue→
amber→orange→red→dark-red, no-data gray. Accents: emerald success, blue primary, amber/orange warning,
red danger, purple innovation, teal neutral.

## 10. Build order
1. **Open-source engine repo + the published dataset** (keystone; verifiable).
2. **Country pages + the chip system + visible gaps** (the heart; static-fast off the JSON).
3. **The map** (structure + coverage layers; the dark map ships early — cheap and on-message).
4. **Stories** (the curated pop-culture set).
5. **The relational layer everywhere** (neighborhood panel + relations map layer) — the differentiator.
6. **Signals** (structural-change feed) — last; needs history to accrue.

**V1 scope (this build):** landing + 91 country pages with the chip system & visible gaps + /atlas
explorer + /how-it-works + /limits + /data, reading a committed engine-generated dataset, deployed on
Vercel. Map starts as a country grid/list with a coverage view; interactive globe + relational layer +
stories are the immediate fast-follows.

---
*Principle throughout: a serious research instrument that happens to be beautifully designed — whose
openness (open engine, visible gaps, candid limits) is the whole pitch.*
