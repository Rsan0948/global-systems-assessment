// ─────────────────────────────────────────────────────────────────────────────
// SINGLE SOURCE OF TRUTH for the whole site.
// Tiers, pillars, valences, thresholds, copy. Every component imports from here -
// change a color or a label once and it propagates everywhere.
// (UI-chrome colors - bg/surface/fg - live in globals.css @theme; the DATA-DRIVEN
//  colors below are used in inline styles and must live in JS.)
// ─────────────────────────────────────────────────────────────────────────────

export type Valence = "good" | "warn" | "bad" | "neutral";

export const SITE = {
  name: "Modernization Index",
  version: "v3.3",
  tagline: "How nations weather stress",
  url: "https://modernization-index.vercel.app",
  description:
    "A structural diagnostic of how governed systems withstand stress. Deterministic, from citable public data. Look up any country - see how it's built, and what we can't yet see.",
  nav: [
    ["Atlas", "/atlas"],
    ["Compare", "/compare"],
    ["Research", "/research"],
    ["Validation", "/validation"],
    ["How it works", "/how-it-works"],
    ["Data", "/data"],
  ] as const,
};

export type Tier = { n: number; name: string; short: string; color: string; min: number };
export const TIERS: Tier[] = [
  { n: 1, name: "Highly Modernized", short: "Highly modernized", color: "#10b981", min: 0.8 },
  { n: 2, name: "Durable", short: "Durable", color: "#38bdf8", min: 0.6 },
  { n: 3, name: "Mixed", short: "Mixed", color: "#eab308", min: 0.4 },
  { n: 4, name: "Fragile", short: "Fragile", color: "#f97316", min: 0.2 },
  { n: 5, name: "Floor", short: "Floor", color: "#dc2626", min: 0.0 },
];
export const tier = (n: number): Tier => TIERS[n - 1] ?? TIERS[TIERS.length - 1];
export const tierColor = (n: number): string => tier(n).color;

export const PILLAR_ORDER = ["P1", "P2", "P3", "P4", "P5"] as const;
export const PILLARS: Record<string, { short: string; full: string; desc: string }> = {
  P1: { short: "Institutions", full: "Institutions", desc: "Government effectiveness, rule of law, corruption control, accountability." },
  P2: { short: "Complexity", full: "Economic Complexity", desc: "How sophisticated and diversified the productive economy is." },
  P3: { short: "Human cap.", full: "Human Capital", desc: "Education and health - the population's capacity." },
  P4: { short: "Economy", full: "Economic Structure", desc: "Income and the material base." },
  P5: { short: "Stability", full: "Stability & Resilience", desc: "Political stability and the absence of structural fragility." },
};

export const VALENCE: Record<Valence | "primary", string> = {
  good: "#4ade80",
  warn: "#fbbf24",
  bad: "#f87171",
  neutral: "#9a9ab0",
  primary: "#60a5fa",
};
export const valenceColor = (v: string): string => VALENCE[v as Valence] ?? VALENCE.neutral;

// a 0-1 pillar value → a red→amber→green hue (used in the atlas heat cells)
export const heat = (v: number): string => `hsl(${Math.round(v * 130)}, 55%, 60%)`;

// world-map viewport (client-safe constants; the geometry builder lives in lib/worldmap.ts)
export const MAP_W = 980;
export const MAP_H = 500;

// shared chrome colors (kept in sync across components - single source of truth)
export const NODATA = "#2a2a3a"; // null pillar / unmatched feature
export const TRACK = "#1a1a28"; // empty bar/track background
export const COVERAGE_SCORED = "#46637e";
export const COVERAGE_UNSCORED = "#181826";

// classification thresholds (mirror the engine; keep the page in sync with the chips)
export const SHAPE_BALANCED = 0.15;
export const SHAPE_LOPSIDED = 0.35;
export const clamp01 = (v: number) => Math.max(0, Math.min(1, v));

// safeguard-board status → color + label (single source of truth for the board + drill-downs)
export const SG_STATUS: Record<string, { color: string; label: string; dot: string }> = {
  firing: { color: "#f87171", label: "firing", dot: "#f87171" },
  borderline: { color: "#fbbf24", label: "watch", dot: "#fbbf24" },
  clear: { color: "#4ade80", label: "clear", dot: "#4ade80" },
  not_assessed: { color: "#8a8aa4", label: "not assessed", dot: "#3a3a52" },
};

// risk-level → color (vulnerability badge)
export const RISK_COLOR: Record<string, string> = {
  low: "#4ade80",
  moderate: "#fbbf24",
  high: "#f97316",
  critical: "#dc2626",
};
