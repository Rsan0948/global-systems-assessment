// Pure type definitions - NO runtime imports (no node:fs). Safe to import from
// client components. The fs-using loaders live in lib/data.ts and lib/worldmap.ts.

export type Chip = {
  key: string;
  label: string;
  valence: "good" | "warn" | "bad" | "neutral";
  why: string;
  rule: string;
};

export type Summary = {
  slug: string;
  name: string;
  iso3: string | null;
  mi: number;
  tier: number;
  pillars: Record<string, number | null>;
  chips: Chip[];
  coverage: { present: number; total: number; missing: string[] };
};

export type Relational = {
  year: number;
  tier: string;
  label: string;
  exposure_structural: number | null;
  exposure_structural_band: string;
  exposure_net: number | null;
  patron_present: boolean;
  response: number | null;
  response_band: string;
  joint_reading: string;
  outcome_factual: string;
};

export type Check = {
  key: string;
  title: string;
  status: "flag" | "info" | "clear";
  headline: string;
  detail: string;
};

export type Country = Summary & {
  verdict: string;
  spread: number | null;
  residual: number | null;
  config: [string, number][];
  pillar_names: Record<string, string>;
  indicators: { key: string; value: number; source: string }[];
  data_year: number;
  checks?: Check[];
  relational?: Relational;
};

export type Meta = {
  built: string;
  count: number;
  engine: string;
  data_vintage: string;
  note: string;
};

export type MapFeature = {
  iso3: string;
  d: string;
  name: string;
  slug: string | null;
  mi: number | null;
  tier: number | null;
  color: string;
};
