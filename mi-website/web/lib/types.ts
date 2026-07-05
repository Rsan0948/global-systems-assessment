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

export type SafeguardStatus = "firing" | "borderline" | "clear" | "not_assessed";
export type SafeguardTile = {
  key: string;
  name: string;
  status: SafeguardStatus;
  triggered: boolean;
  headline: string;
  detail: string;
  modification: string | null;
  tier?: string | null;
  origin_cases: string[];
  why: string | null;
  validated_by: string[];
  share_firing: number;
};

export type Diagnostics = {
  context_curated: boolean;
  strategy: {
    strategy: string;
    confidence?: string;
    tier?: number;
    tier_label?: string;
    explanation?: string;
    failure_mode?: string;
    examples?: string;
  };
  vulnerability: {
    risk_level: "low" | "moderate" | "high" | "critical";
    flags: string[];
    structural_vulnerability?: { p4_minus_p1_gap: number; status: string; reading: string } | null;
    summary: string;
  };
  movement: { class: string; dMI: number; lead: string; dP1: number; reading: string; caveat: string } | null;
  accountability_gap: { status: string; reading: string; va_minus_p4: number; caveat: string } | null;
  sensitivity: Record<string, number> | null;
  prior_year: number | null;
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
  safeguards?: SafeguardTile[];
  diagnostics?: Diagnostics;
  similar?: { slug: string; name: string; mi: number; tier: number }[];
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
