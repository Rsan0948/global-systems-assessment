# MI website — frontend

This is the Next.js frontend for the **Modernization Index**. It is a *consumer*
of the `mi-research` engine — it does **not** re-implement scoring. The site
reads the generated dataset in `web/public/data/` (a build artifact committed so
Vercel deploys without running Python).

Start here:

- **`../DESIGN_SPEC.md`** — the design source of truth (information architecture,
  features, design language).
- **`../REDESIGN_PLAN.md`** — the redesign plan (surface the full engine,
  interactivity, mobile).
- **`../CLAUDE.md`** — the website agent guide (data flow, build/verify).
- **`AGENTS.md`** — app-specific conventions. **Read it before writing any code.**

## Develop

```bash
# regenerate the dataset from the mi-research engine (run from the repo root)
python mi-website/scripts/refresh_and_build.py

# then the app
cd mi-website/web && npm install && npm run dev   # http://localhost:3000
```

Never port the scoring math into JS — regenerate the dataset via
`mi-research` instead (see `../CLAUDE.md`).
