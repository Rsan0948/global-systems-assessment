# Modernization Index website

This directory contains the website and the script that prepares its public data.

- `web/` is the Next.js application.
- `scripts/refresh_and_build.py` refreshes available inputs, runs the Python scoring engine, and writes the JSON used by the site.
- `DESIGN_SPEC.md` documents the information architecture and visual system.
- `REDESIGN_PLAN.md` records the completed redesign goals and remaining ideas.

The site is a reader of the `mi-research` output. Scoring logic belongs in the Python engine and should not be duplicated in TypeScript.

## Local development

From the repository root:

```bash
python mi-website/scripts/refresh_and_build.py
cd mi-website/web
npm ci
npm run dev
```

Open <http://localhost:3000>.

## Verification

```bash
cd mi-website/web
npm run check
npm run build
npm audit --omit=dev --audit-level=high
```

The generated files in `web/public/data/` are committed so a hosting provider can build the site without running Python or downloading upstream research data.
