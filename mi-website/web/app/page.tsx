import Link from "next/link";
import { getCountries, getMeta } from "@/lib/data";
import { SITE } from "@/lib/config";
import { buildWorldPaths } from "@/lib/worldmap";
import CountryGrid from "@/components/CountryGrid";
import WorldMap from "@/components/WorldMap";

export default function Home() {
  const countries = getCountries();
  const meta = getMeta();
  const { features, sphere } = buildWorldPaths();
  const band1 = countries.filter((c) => c.tier === 1).length;

  return (
    <div className="py-10 sm:py-12">
      <section className="mx-auto max-w-3xl text-center">
        <h1 className="serif text-[2.1rem] font-black leading-[1.05] sm:text-5xl">{SITE.tagline}</h1>
        <p className="mx-auto mt-5 max-w-xl text-[14px] leading-relaxed text-fg2 sm:text-[15px]">
          Compare how countries are equipped to handle political and economic stress. Every score
          comes from public data and a fixed formula. Open a country to see its five pillars, its data
          gaps, and the checks that affect its reading.
        </p>
        <div className="mono mt-6 flex flex-wrap justify-center gap-x-6 gap-y-2 text-[12px] text-fg3">
          <span>
            <b className="text-fg">{meta.count}</b> countries scored
          </span>
          <span>
            <b className="text-fg">{band1}</b> in the highest score band
          </span>
          <span>
            formula <b className="text-fg">{meta.engine}</b> · reproducible
          </span>
        </div>
        <p className="mt-4 text-[13px] text-fg3">
          New here?{" "}
          <Link href="/how-it-works" className="link">
            Start with what this measures →
          </Link>
        </p>
      </section>

      <section className="mt-8">
        <WorldMap features={features} sphere={sphere} countries={countries} />
        <p className="mono mt-2 text-[10px] text-fg3">
          Select a country on the map to see its score and open its profile. Small countries and
          island states, including Singapore and San Marino, may be easier to find in the list below.
        </p>
      </section>

      <section className="mt-12">
        <div className="mb-4 flex items-baseline justify-between">
          <h2 className="serif text-lg">Browse every country</h2>
          <Link href="/atlas" className="link text-[13px]">
            Open the atlas →
          </Link>
        </div>
        <CountryGrid countries={countries} />
        <p className="mt-5 max-w-2xl text-[12px] leading-relaxed text-fg3">
          {meta.count} of about 195 states are scored. Countries without enough source data are labeled{" "}
          <span className="text-fg2">unmeasured</span> and are not assigned an estimated score.
        </p>
      </section>
    </div>
  );
}
