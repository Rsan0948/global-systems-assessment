import Link from "next/link";

export const metadata = {
  title: "How orders rebuild after they fragment | Modernization Index",
  description:
    "A 30-case study of how political systems reunite after fragmentation, including four pathways and the factors associated with each outcome.",
};

function BackLink() {
  return (
    <Link href="/research" className="link mono text-[12px]">
      ← Research
    </Link>
  );
}

const PATHWAYS = [
  {
    name: "Construction",
    count: 13,
    dur: 118.7,
    tone: "text-fg",
    desc: "Integration built from shallow or fragmented predecessors. Examples include China, the EU, the Inca, Silla Korea, and Meiji Japan.",
  },
  {
    name: "Restoration",
    count: 5,
    dur: 131.2,
    tone: "text-fg",
    desc: "A deep prior order rebuilt largely as it was, with few institutional features changing. Middle-Kingdom Egypt is one example.",
  },
  {
    name: "Negotiation",
    count: 4,
    dur: 308.0,
    tone: "text-good",
    desc: "A deep order reunited slowly through bargaining rather than conquest. This pathway had the longest average duration in the sample.",
  },
  {
    name: "Redesign",
    count: 3,
    dur: 148.7,
    tone: "text-fg",
    desc: "A deep order quickly rebuilt in a new institutional form, with many features changing. Argentina and Brazil are examples.",
  },
];

export default function Collectivization() {
  return (
    <div className="mx-auto max-w-2xl py-10 sm:py-12">
      <BackLink />
      <h1 className="serif mt-3 text-3xl font-black sm:text-4xl">
        How orders rebuild after they fragment
      </h1>
      <p className="mt-4 text-[15px] leading-relaxed text-fg2">
        The index reads a country at a moment. This study reads the opposite motion over the long run:
        how political orders reunite after they break apart. It covers{" "}
        <span className="mono">30</span> political systems (<span className="mono">25</span> core cases plus{" "}
        <span className="mono">5</span> comparison cases), from Tawantinsuyu and the Zulu Kingdom to the
        European Union.
      </p>

      <div className="mt-5 rounded-lg border border-innovation/30 bg-innovation/[0.06] p-4">
        <p className="text-[13px] leading-relaxed text-fg2">
          <span className="font-medium text-fg">A note on where this lives. </span>
          This study is part of a separate fragmentation research program. It is
          conceptually related to the Modernization Index but computed entirely separately. It is{" "}
          <span className="text-fg">not part of any country&apos;s MI score.</span>
        </p>
      </div>

      <section className="mt-10">
        <h2 className="serif text-xl">Four pathways and their duration</h2>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          Each reunification is placed in one of four pathways. The classification depends on how
          established the earlier system was and how quickly reunification happened. The average
          duration of each pathway is the study&apos;s main descriptive result:
        </p>
        <div className="mt-4 space-y-3">
          {PATHWAYS.map((p) => (
            <div key={p.name} className="rounded-lg border border-border bg-surface2/40 p-4">
              <div className="flex items-baseline justify-between gap-3">
                <div className="flex items-baseline gap-2">
                  <h3 className="serif text-base text-fg">{p.name}</h3>
                  <span className="mono text-[11px] text-fg3">n={p.count}</span>
                </div>
                <div className="text-right">
                  <span className={`mono text-lg font-semibold ${p.tone}`}>{p.dur.toFixed(0)}</span>
                  <span className="mono ml-1 text-[11px] text-fg3">year average</span>
                </div>
              </div>
              <p className="mt-1.5 text-[13px] leading-relaxed text-fg2">{p.desc}</p>
            </div>
          ))}
        </div>
        <p className="mt-3 text-[14px] leading-relaxed text-fg2">
          Bargained reunifications lasted <span className="mono text-good">about 308 years</span> on
          average, against <span className="mono">about 119 to 149 years</span> for construction, restoration, and
          redesign. The sample is small, but the difference is substantial.
        </p>
      </section>

      <section className="mt-10">
        <h2 className="serif text-xl">Relationships in the sample</h2>
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <div className="rounded-lg border border-border bg-surface2/40 p-4">
            <div className="mono text-lg font-semibold text-fg">Correlation −0.84</div>
            <div className="mt-1 text-[13px] leading-relaxed text-fg2">
              <span className="font-medium text-fg">Established systems changed less. </span>
              The more integrated the earlier system was, the fewer institutional features changed
              during reunification. This relationship is strong in the study sample (p &lt; 0.001).
            </div>
          </div>
          <div className="rounded-lg border border-border bg-surface2/40 p-4">
            <div className="mono text-lg font-semibold text-fg">Correlation about 0.83</div>
            <div className="mt-1 text-[13px] leading-relaxed text-fg2">
              <span className="font-medium text-fg">Slower reunification changed more. </span>
              Among well-established systems, slower reunification was associated with a larger loss
              of the old system&apos;s integration. Gradual bargaining changed more of the earlier
              arrangement than a rapid rebuild did.
            </div>
          </div>
          <div className="rounded-lg border border-border bg-surface2/40 p-4">
            <div className="mono text-lg font-semibold text-warn">76%</div>
            <div className="mt-1 text-[13px] leading-relaxed text-fg2">
              <span className="font-medium text-fg">Warning signals appeared</span> in 76% of core cases.
              Declining administrative performance, weakening coordination, or falling legitimacy
              appeared before the system came apart.
            </div>
          </div>
          <div className="rounded-lg border border-border bg-surface2/40 p-4">
            <div className="mono text-sm font-semibold text-danger">coordination problems</div>
            <div className="mt-1 text-[13px] leading-relaxed text-fg2">
              <span className="font-medium text-fg">The most common reason for failure. </span>
              When these orders came apart, they most often did so because the parts could no longer
              coordinate, rather than because one part was conquered.
            </div>
          </div>
        </div>
        <p className="mt-3 text-[13px] leading-relaxed text-fg3">
          The cases support the idea that reunification can change institutional form. They do not
          support a one-way process in which systems only become more integrated. Some became less
          integrated during reunification.
        </p>
      </section>

      <section className="mt-10">
        <h2 className="serif text-xl">Cases in the study</h2>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          The 25 core cases span roughly four millennia and every inhabited continent:
        </p>
        <p className="mt-3 text-[13px] leading-relaxed text-fg2">
          China · European Union · United States · France · Spain · Germany · Italy · Japan ·
          Argentina · Brazil · Australia · Canada · Netherlands · Switzerland · Ethiopia · Vietnam ·
          Poland-Lithuania · Russia (Muscovy) · Silla Korea · Mughal India · Maurya India · Safavid
          Persia · Middle-Kingdom Egypt · the Inca (Tawantinsuyu) · the Zulu Kingdom.
        </p>
      </section>

      <section className="mt-10 rounded-lg border border-border bg-surface2/40 p-4">
        <div className="mono flex flex-wrap gap-x-5 gap-y-1 text-[13px]">
          <Link href="/research/substrate" className="link">
            How the pieces fit together →
          </Link>
          <Link href="/research/global-systems" className="link">
            State of the world →
          </Link>
          <Link href="/how-it-works" className="link">
            How the country score works →
          </Link>
        </div>
      </section>
    </div>
  );
}
