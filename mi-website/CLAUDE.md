# CLAUDE.md — MI Website (agent guide)

A new root for the **public website** of the Modernization Index. Separate project
from the others in this repo; **nothing is built yet** — this directory currently
holds only the design spec.

## What this is

The planned institutional home of the MI: a public diagnostic tool + research
platform + interactive case-study teaching tool + contribution portal. Aesthetic
target: "Bloomberg Terminal for geopolitics" (dark, data-dense, precise). The full
concept is in **`DESIGN_SPEC.md`** (v0.1, tentative) — read it first; it is the
source of truth for IA, features, design language, stack, and build phases.

## Status

**Pre-development.** No app scaffold, package.json, or code exists yet. Don't
assume a framework is installed. Phase 1 (MVP: country profiles + dataset explorer
+ data download) is the first thing to build per `DESIGN_SPEC.md` §6.

## How it relates to the other sub-projects (do NOT duplicate them)

This site is a **consumer** of the existing MI work — it should read from those
projects, not re-implement them:

- **`../mi-research/`** — the scoring/diagnostic/retrodiction engine + the
  validated data. The website's scores, pillar values, safeguard evaluations,
  strategy classifications, and case studies all originate here:
  - scoring engine: `../mi-research/mi/` (Python) — §5 of the spec flags an open
    decision: call it as a Python API vs. port to Supabase Edge Functions (TS).
    **Don't silently re-implement the scoring math** in JS; that risks divergence
    from the validated engine. Wrap it.
  - case-study content: the canonical record is `../mi-research/live/runs/`; the
    "51 case studies" the site references = the 50-case expansion + Somaliland
    promotion in `../mi-research/docs/expansion_plan/`.
- **`../mi_pipeline/`** — builds the raw indicator panel (World Bank + manual
  CSVs). The site's daily data pipeline (spec §5.4) is conceptually the same
  ingestion; reuse its source list/normalization rather than re-deriving.
- **Root `../` (universalsystemgrade)** — the unrelated fragmentation study. Not
  used by the website except as the conceptual origin of the branching empirics.

## Stack (from the spec — not yet installed)

Next.js (React, SSR) + Tailwind + Recharts/D3 + Mapbox GL + Framer Motion;
Supabase (Postgres, Auth, Edge Functions, Realtime); deploy on Vercel. Note the
session environment already has Chromium/Playwright available for any browser-driven
testing (see the repo's environment notes).

## Open decisions to resolve before building (spec §9)

These are genuine forks the spec leaves open — surface them to the user rather than
picking silently: monetization / case-study gating (free 10 vs. paid 41), scoring-
engine location (Python API vs. TS port), map provider (Mapbox vs. Leaflet vs. D3),
and alert delivery channels.

## Conventions

- Keep the spec (`DESIGN_SPEC.md`) as the design source of truth; if the build
  diverges, update the spec in the same change.
- When the app is scaffolded, add the usual `.gitignore` (node_modules, .next,
  .env*) and keep secrets out of the repo.
