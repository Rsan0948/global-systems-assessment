import fs from "node:fs";
import path from "node:path";
import type { Summary, Country, Meta } from "@/lib/types";

export type { Chip, Summary, Country, Meta } from "@/lib/types";

const DIR = path.join(process.cwd(), "public", "data");

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
