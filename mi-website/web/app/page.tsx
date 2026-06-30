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
  const tier1 = countries.filter((c) => c.tier === 1).length;

  return (
    <div className="py-10 sm:py-12">
      <section className="mx-auto max-w-3xl text-center">
        <h1 className="serif text-[2.1rem] font-black leading-[1.05] sm:text-5xl">{SITE.tagline}</h1>
        <p className="mx-auto mt-5 max-w-xl text-[14px] leading-relaxed text-fg2 sm:text-[15px]">
          A structural diagnostic of how governed systems withstand pressure — computed
          deterministically from citable public data, not opinion. Look up any country: see how it&apos;s
          built, and what we can&apos;t yet see.
        </p>
        <div className="mono mt-6 flex flex-wrap justify-center gap-x-6 gap-y-2 text-[12px] text-fg3">
          <span>
            <b className="text-fg">{meta.count}</b> countries scored
          </span>
          <span>
            <b className="text-fg">{tier1}</b> highly modernized
          </span>
          <span>
            engine <b className="text-fg">{meta.engine}</b> · reproducible
          </span>
        </div>
      </section>

      <section className="mt-8">
        <WorldMap features={features} sphere={sphere} countries={countries} />
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
          {meta.count} of the world&apos;s ~195 states are scored here. The rest aren&apos;t graded —
          they&apos;re <span className="text-fg2">unmeasured</span>, missing the public data the engine
          needs. We show that honestly rather than guessing. The well-governed world is, not
          coincidentally, the well-measured world.
        </p>
      </section>
    </div>
  );
}
