import { PILLAR_ORDER, PILLARS } from "@/lib/config";

export const metadata = { title: "How it works - Modernization Index" };

export default function HowItWorks() {
  return (
    <div className="mx-auto max-w-2xl py-12">
      <h1 className="serif text-3xl font-black">How it works</h1>
      <p className="mt-4 text-[15px] leading-relaxed text-fg2">
        The Modernization Index reads how a country is <em>built</em> to withstand stress. It measures
        five structural dimensions from citable public data, then reads the <em>shape</em> they make -
        because the relationship between a country&apos;s strengths and weaknesses says more than any
        single score.
      </p>

      <h2 className="serif mt-9 text-xl">The five pillars</h2>
      <div className="mt-3 space-y-2">
        {PILLAR_ORDER.map((k) => (
          <div key={k} className="card flex gap-3 p-3">
            <span className="mono mt-0.5 text-[13px] font-semibold text-primary">{k}</span>
            <div>
              <div className="text-[14px] font-medium">{PILLARS[k].full}</div>
              <div className="text-[12px] text-fg2">{PILLARS[k].desc}</div>
            </div>
          </div>
        ))}
      </div>

      <h2 className="serif mt-9 text-xl">The relationships, not the levels</h2>
      <p className="mt-2 text-[14px] leading-relaxed text-fg2">
        Two relationships carry most of the signal. The <strong className="text-fg">durability gap</strong>{" "}
        asks whether a country&apos;s prosperity is <em>earned</em> (institutions match its wealth) or{" "}
        <em>granted</em> (wealth has outrun institutions - historically fragile). The{" "}
        <strong className="text-fg">shape</strong> asks whether the pillars are balanced or lopsided. A
        rich country built on a hollow institutional base reads as fragile here, even when its headline
        numbers look fine.
      </p>

      <h2 className="serif mt-9 text-xl">The relational layer</h2>
      <p className="mt-2 text-[14px] leading-relaxed text-fg2">
        The pillars read a country from the <em>inside</em>. A separate layer reads its{" "}
        <em>position</em> - how exposed it is to stronger or hostile neighbors, and whether a patron or
        alliance would actually defend it. This is what separates a weak state that survives (because
        someone has its back) from an identical one that gets swallowed (because it stands alone). It&apos;s
        the newest part of the system and is rolled out country by country.
      </p>

      <h2 className="serif mt-9 text-xl">It&apos;s a formula - run it yourself</h2>
      <p className="mt-2 text-[14px] leading-relaxed text-fg2">
        No model interprets anything. Every score is a fixed, deterministic calculation over public
        numbers - the same inputs always produce the same answer. The engine is open source, the data is
        public, and the outputs are published. The whole chain is yours to audit.
      </p>
      <a href="/data" className="link mt-3 inline-block text-[13px]">
        Get the data and the engine →
      </a>
    </div>
  );
}
