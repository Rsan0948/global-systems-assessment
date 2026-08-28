# Modernization Index frontend

This is the Next.js application for the public Modernization Index website. It reads generated JSON from `public/data/` and does not calculate scores in the browser.

## Develop locally

Node.js 20.9 or newer is required.

```bash
npm ci
npm run dev
```

Open <http://localhost:3000>.

To rebuild the data first, run this from the repository root:

```bash
python mi-website/scripts/refresh_and_build.py
```

## Check a change

```bash
npm run check
npm run build
npm audit --omit=dev --audit-level=high
```

Keep scoring changes in `mi-research`. The frontend should display the generated output without reimplementing the research formula.
