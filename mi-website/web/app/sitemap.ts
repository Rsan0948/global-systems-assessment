import type { MetadataRoute } from "next";
import { SITE } from "@/lib/config";
import { getCountries, getMeta } from "@/lib/data";

const pages = [
  "",
  "/atlas",
  "/compare",
  "/research",
  "/research/collectivization",
  "/research/global-systems",
  "/research/golden-ages",
  "/research/substrate",
  "/validation",
  "/how-it-works",
  "/limits",
  "/data",
  "/stories",
];

export default function sitemap(): MetadataRoute.Sitemap {
  const built = getMeta().built;
  const lastModified = /^\d{4}-\d{2}-\d{2}/.test(built) ? built : undefined;

  return [
    ...pages.map((path, index) => ({
      url: `${SITE.url}${path}`,
      lastModified,
      changeFrequency: "monthly" as const,
      priority: index === 0 ? 1 : 0.8,
    })),
    ...getCountries().map((country) => ({
      url: `${SITE.url}/country/${country.slug}`,
      lastModified,
      changeFrequency: "monthly" as const,
      priority: 0.7,
    })),
  ];
}
