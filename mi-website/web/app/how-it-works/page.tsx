import Link from "next/link";
import { GLOSSARY, PILLAR_KEYS } from "@/lib/glossary";
import { SCORE_BANDS, scoreBandColor } from "@/lib/config";

export const metadata = { title: "How it works - Modernization Index" };

function Concept({ id }: { id: string }) {
  const e = GLOSSARY[id];
  return (
    <section id={e.id} className="scroll-mt-20">
      <h2 className="serif text-xl">{e.term}</h2>
      <p className="mt-2 text-[14px] leading-relaxed text-fg2">{e.what}</p>
      <p className="mt-2 text-[14px] leading-relaxed text-fg2">
        <span className="font-medium text-fg">Why it matters. </span>
        {e.why}
      </p>
      {e.example && (
        <p className="mt-2 rounded-lg border border-border bg-surface2/40 p-3 text-[13px] leading-relaxed text-fg2">
          <span className="font-medium text-fg">For example. </span>
          {e.example}
        </p>
      )}
    </section>
  );
}

export default function HowItWorks() {
  return (
    <div className="mx-auto max-w-2xl py-12">
      <h1 className="serif text-3xl font-black">How it works</h1>
      <p className="mt-4 text-[15px] leading-relaxed text-fg2">
        Every country gets a structural health check: not how rich or powerful it looks today, but how
        it is <em>built</em> to withstand stress. We measure five things, read the shape they make, and
        turn it into one score. Here is what each piece means, in plain language.
      </p>

      <div className="mt-10 space-y-10">
        <Concept id="mi" />
        <Concept id="tier" />

        <section id="pillars" className="scroll-mt-20">
          <h2 className="serif text-xl">The five pillars</h2>
          <p className="mt-2 text-[14px] leading-relaxed text-fg2">
            These are the five traits we measure for every country. Each is scored 0 to 1 from citable
            public data, then combined with equal 20 percent weights into the MI v3.3 score.
          </p>
          <div className="mt-5 space-y-7">
            {PILLAR_KEYS.map((k, i) => {
              const e = GLOSSARY[k];
              return (
                <div key={k} id={e.id} className="scroll-mt-20">
                  <div className="flex items-baseline gap-2">
                    <span className="mono text-[13px] font-semibold text-primary">P{i + 1}</span>
                    <h3 className="serif text-base">{e.term}</h3>
                  </div>
                  <p className="mt-1.5 text-[14px] leading-relaxed text-fg2">{e.what}</p>
                  <p className="mt-1.5 text-[14px] leading-relaxed text-fg2">
                    <span className="font-medium text-fg">Why it matters. </span>
                    {e.why}
                  </p>
                  {e.example && (
                    <p className="mt-1.5 rounded-lg border border-border bg-surface2/40 p-3 text-[13px] leading-relaxed text-fg2">
                      <span className="font-medium text-fg">For example. </span>
                      {e.example}
                    </p>
                  )}
                </div>
              );
            })}
          </div>
        </section>

        <section className="scroll-mt-20">
          <h2 className="serif text-xl">It is the shape, not just the average</h2>
          <p className="mt-2 text-[14px] leading-relaxed text-fg2">
            Two countries can share the same score and be built very differently. So we look at two
            relationships that a single number hides.
          </p>
          <div className="mt-5 space-y-8">
            <Concept id="durability-gap" />
            <Concept id="shape" />
          </div>
        </section>

        <section id="relational" className="scroll-mt-20">
          <h2 className="serif text-xl">The neighborhood</h2>
          <p className="mt-2 text-[14px] leading-relaxed text-fg2">
            The five pillars read a country from the <em>inside</em>. But a perfectly-built country can
            still be invaded. A separate layer reads its <em>position</em> in the world. It is the newest
            part of the system and is filled in country by country.
          </p>
          <div className="mt-5 space-y-8">
            <Concept id="exposure" />
            <Concept id="protection" />
            <Concept id="response" />
          </div>
        </section>

        <section className="scroll-mt-20">
          <h2 className="serif text-xl">The score is a formula</h2>
          <p className="mt-2 text-[14px] leading-relaxed text-fg2">
            The core score is a fixed calculation over published inputs. The same inputs, version, and
            settings give the same answer. Some safeguards and historical context are curated by people.
            Those parts are labeled separately and never silently folded into the score.
          </p>
          <Link href="/data" className="link mt-3 inline-block text-[13px]">
            Get the data and the engine →
          </Link>
        </section>
      </div>

      <div className="mt-12 rounded-lg border border-border bg-surface2/40 p-4">
        <p className="text-[13px] text-fg2">Ready to look around?</p>
        <div className="mono mt-2 flex flex-wrap gap-x-5 gap-y-1 text-[13px]">
          <Link href="/" className="link">
            The world map →
          </Link>
          <Link href="/atlas" className="link">
            Rank every country →
          </Link>
          <Link href="/stories" className="link">
            Read the stories →
          </Link>
        </div>
      </div>

      {/* A quick visual of the public score bands. */}
      <div className="mt-8">
        <p className="mb-2 text-[12px] text-fg3">The score bands, at a glance:</p>
        <div className="flex flex-wrap gap-x-4 gap-y-1.5">
          {SCORE_BANDS.map((band) => (
            <span key={band.n} className="flex items-center gap-1.5 text-[12px] text-fg2">
              <span
                className="inline-block h-2.5 w-2.5 rounded-[3px]"
                style={{ background: scoreBandColor(band.n) }}
              />
              B{band.n} {band.short}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
