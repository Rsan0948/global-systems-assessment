import fs from "node:fs";
import path from "node:path";
import { geoNaturalEarth1, geoPath, geoArea } from "d3-geo";
import { getCountries } from "@/lib/data";
import { tierColor, MAP_W, MAP_H } from "@/lib/config";
import type { MapFeature } from "@/lib/types";

// d3-geo fills a polygon's COMPLEMENT when its ring winding is reversed (common on
// antimeridian-crossing countries). If a feature covers >half the sphere, its winding
// is inverted - reverse every ring so it fills the country, not the ocean.
function fixWinding(feature: { geometry?: { type: string; coordinates: unknown } | null }) {
  if (!feature.geometry) return feature;
  if (geoArea(feature as never) <= 2 * Math.PI) return feature;
  const g = feature.geometry;
  const rev = (rings: number[][][]) => rings.map((r) => [...r].reverse());
  if (g.type === "Polygon") g.coordinates = rev(g.coordinates as number[][][]);
  else if (g.type === "MultiPolygon") g.coordinates = (g.coordinates as number[][][][]).map(rev);
  return feature;
}

// Project the world once at build time → path strings + joined MI data. No d3 on the client.
export function buildWorldPaths(): { features: MapFeature[]; sphere: string } {
  const geo = JSON.parse(
    fs.readFileSync(path.join(process.cwd(), "public", "world.geo.json"), "utf8")
  ) as { features: { id: string; properties: { name: string }; geometry: unknown }[] };

  const byIso = new Map(getCountries().map((c) => [c.iso3, c]));
  geo.features.forEach((f) => fixWinding(f as never));
  const projection = geoNaturalEarth1().fitExtent(
    [
      [4, 4],
      [MAP_W - 4, MAP_H - 4],
    ],
    geo as never
  );
  const pathGen = geoPath(projection);
  const sphere = pathGen({ type: "Sphere" } as never) ?? "";

  const features = geo.features
    .map((f) => {
      const d = pathGen(f as never);
      if (!d) return null;
      const c = byIso.get(f.id);
      return {
        iso3: f.id,
        d,
        name: c?.name ?? f.properties.name,
        slug: c?.slug ?? null,
        mi: c?.mi ?? null,
        tier: c?.tier ?? null,
        color: c ? tierColor(c.tier) : "#20202e",
      } as MapFeature;
    })
    .filter((x): x is MapFeature => x !== null);
  return { features, sphere };
}
