import fs from "node:fs";
import path from "node:path";

const DIR = path.join(process.cwd(), "public", "data");

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

export type Country = Summary & {
  verdict: string;
  spread: number | null;
  residual: number | null;
  config: [string, number][];
  pillar_names: Record<string, string>;
  indicators: { key: string; value: number; source: string }[];
  data_year: number;
};

export type Meta = {
  built: string;
  count: number;
  engine: string;
  data_vintage: string;
  note: string;
};

const read = <T,>(f: string): T => JSON.parse(fs.readFileSync(path.join(DIR, f), "utf8"));

export const getCountries = (): Summary[] => read<Summary[]>("countries.json");
export const getMeta = (): Meta => read<Meta>("meta.json");
export const getCountry = (slug: string): Country | null => {
  try {
    return read<Country>(path.join("country", `${slug}.json`));
  } catch {
    return null;
  }
};
