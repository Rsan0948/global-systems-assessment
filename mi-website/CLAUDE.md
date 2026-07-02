# CLAUDE.md — MI Website (agent guide)

The **public website** for the Modernization Index — a built Next.js app that is
a *consumer* of `mi-research` (it does not re-implement the scoring). Separate
project from the others in this repo.

## Layout

- **`web/`** — the Next.js app. Its own agent guide is **`web/AGENTS.md`**
  (read it before touching the app); `web/CLAUDE.md` points there. Pages:
  home, `atlas`, `compare`, `country/[slug]`, `data`, `stories`, `how-it-works`,
  `limits`. Stack: Next.js (App Router) + Tailwind + Recharts/D3 + Framer Motion;
  deploys on Vercel.
- **`web/public/data/`** — the generated dataset the site reads
  (`countries.json` + `country/<slug>.json` + `meta.json`). This is a build
  artifact, committed so Vercel deploys without running Python.
- **`scripts/refresh_and_build.py`** — the data pipeline: (best-effort) refresh
  upstream sources, then run the validated `mi-research` engine over all data and
  publish `web/public/data/`.
- **`DESIGN_SPEC.md`** — the design source of truth (IA, features, design
  language). Keep it in sync if the build diverges.

## Data flow — do NOT re-implement scoring

```
mi-research canonical panel ─► mi-research/scripts/build_site_dataset.py
      └► build_similar.py ─► build_relational.py ─► web/public/data/*  ─► the site
```

`scripts/refresh_and_build.py` chains those `mi-research` scripts; the engine
(`mi-research/mi/`) is the single source of truth for scores, pillars,
safeguards, and case studies. Never port the scoring math into JS — regenerate
the dataset instead.

## Build / verify

```bash
python mi-website/scripts/refresh_and_build.py        # regenerate web/public/data
cd mi-website/web && npm install && npm run build      # ~200 static pages; node_modules is gitignored
```

The site dataset is deterministic given fixed source data (sorted iteration +
stable tiebreaks in the mi-research build scripts).
