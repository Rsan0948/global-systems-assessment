import Link from "next/link";

export const metadata = {
  title: "What the whole thing means - Modernization Index",
  description:
    "The capstone argument: not an index, not a forecast, but a substrate - the first coherent space in which structural laws of human macro-systems could live together.",
};

function BackLink() {
  return (
    <Link href="/research" className="link mono text-[12px]">
      ← Research
    </Link>
  );
}

const FEATURES = [
  ["Breadth, uncollapsed", "Five pillars, ten safeguards, two measurement tiers - deliberately not averaged into one number. A substrate has to have unused room; an index has spent all of it."],
  ["Relationships, not levels", "Every validated signal is a relationship - the durability gap, the container, the configuration - never a raw level. We measure the geometry between the parts."],
  ["Multiple centers, in tension", "The central pillar rotates across eras; the improvement engines peak in different decades. No single forced point of collapse, so competing hypotheses can coexist."],
  ["Contradiction preserved", "Hollow stability keeps both readings - human capital up, institutions down. Disagreement is treated as information, not averaged away."],
  ["Self-placement", "Each unit is scored relative to its contemporaries and placed in its era - which is why the same space can hold Old Kingdom Egypt and the eurozone at once."],
  ["Deterministic & citable", "Same inputs, same outputs, over authoritative external data - WGI, V-Dem, Maddison - not an AI's read of the world. Anyone can re-run it."],
];

export default function Substrate() {
  return (
    <div className="mx-auto max-w-2xl py-10 sm:py-12">
      <BackLink />
      <h1 className="serif mt-3 text-3xl font-black sm:text-4xl">What the whole thing means</h1>
      <p className="mt-4 text-[15px] leading-relaxed text-fg2">
        Step back from any single score and ask what the project actually is. It is not an index, not
        a predictive model, and not merely a pile of validated findings. It is an attempt at something
        stranger: <span className="text-fg">a substrate</span> - the first coherent, high-dimensional,
        self-placing space in which structural laws of human macro-systems, present and future, could
        live together.
      </p>

      <section className="mt-10 space-y-4 text-[14.5px] leading-relaxed text-fg2">
        <p>
          Everyone before faced a fork and chose one of two moves. One is to{" "}
          <span className="font-medium text-fg">collapse</span>: composite indices - HDI, the Fragile
          States Index, even V-Dem - project the world down to a score or a ranking. Once collapsed,
          there are no degrees of freedom left for hidden signal to live in; the room has been spent.
          The other is to <span className="font-medium text-fg">commit</span>: quantitative
          macro-history picks one master mechanism and explains everything through it - but one center
          can&apos;t hold the competing pulls real systems actually have.
        </p>
        <p>
          This project makes neither move. What it builds is a{" "}
          <span className="font-medium text-fg">structured phase space with a spine</span>: breadth
          kept uncollapsed, relationships as the primary object, several gravity centers held in
          tension, contradiction preserved rather than averaged, and self-placement instead of a fixed
          external yardstick - all still coherent because one mechanism runs through it all:{" "}
          <em>level and structure under stress</em>. That integration is the genuinely new thing.
        </p>
      </section>

      <section className="mt-8">
        <div className="grid gap-3 sm:grid-cols-2">
          {FEATURES.map(([h, b]) => (
            <div key={h} className="rounded-lg border border-border bg-surface2/40 p-4">
              <h3 className="serif text-[15px] text-fg">{h}</h3>
              <p className="mt-1 text-[13px] leading-relaxed text-fg2">{b}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mt-10 space-y-4 text-[14.5px] leading-relaxed text-fg2">
        <p>
          A substrate is only worth anything if the structure it preserves actually bears weight - and
          here the honesty has to be exact. The invariants (the durability gap, the container) recur
          deterministically across the modern panel, the three-cycle supercycle, and pre-modern cases
          from Old Kingdom Egypt to now. That is strong evidence the structure is real and coherent{" "}
          <em>in the data</em>. It is <span className="text-fg">not</span> out-of-sample validation:
          the 51-case retrodiction (best estimate ~78%, honestly a{" "}
          <span className="mono">62-85%</span> range) was scored knowing the outcomes, with thresholds
          tuned to fit - reproducibility, not freedom from overfitting. The one genuinely
          pre-registered forward test we ran, the golden-age signature, <span className="text-fg">
          failed</span>. True predictive validation is still owed.
        </p>
        <p>
          The failures are part of the map. A whole graveyard of killed signals - the golden-age
          signature, the modernization sequence, the commodity driver, the 1900-1910 parallel - each
          tells a future builder where <em>not</em> to dig, while the surviving relationships show
          where the ground holds. And the space knows its own edge: acute timing (~3-5 years at best),
          fortune (exogenous - era and starting level, not trajectory), and outside shocks like
          conquest and plague. Knowing exactly where the laws stop is part of being a substrate, not a
          failure of one.
        </p>
        <p>
          So what is it the foundation <em>of</em>? A genuine, predictive science of macro-systems -
          the kind that does not yet exist. We are explicit that what we have is not predictive, and
          that it does not need to be. Weather forecasting was impossible until thermodynamics existed;
          the laws were never a forecast, but no forecast was possible without them. This is that layer
          for human macro-systems - and when the predictive science comes, it will look like structural
          seismology or epidemiology (risk distributions over bands, horizon-bounded), not the dated
          certainty of a Seldon Plan. The space is built right but sparsely populated: a handful of
          validated relationships in a room built for hundreds. That is not a weakness of the claim -
          it is the research program it generates.
        </p>
      </section>

      <section className="mt-10 rounded-lg border border-border bg-surface2/40 p-4">
        <p className="text-[13px] leading-relaxed text-fg2">
          As a diagnostic <em>today</em>, it tells you who is structurally fragile and why - with an
          explicit &quot;I can&apos;t call that&quot; at its edges. As a substrate, it is the home base
          a predictive science will eventually need.
        </p>
        <div className="mono mt-2 flex flex-wrap gap-x-5 gap-y-1 text-[13px]">
          <Link href="/validation" className="link">
            How we know it works →
          </Link>
          <Link href="/limits" className="link">
            What it can&apos;t tell you →
          </Link>
          <Link href="/research" className="link">
            All research →
          </Link>
        </div>
      </section>
    </div>
  );
}
