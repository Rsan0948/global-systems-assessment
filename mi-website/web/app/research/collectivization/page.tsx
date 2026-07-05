import Link from "next/link";

export const metadata = {
  title: "How orders rebuild after they fragment — Modernization Index",
  description:
    "A 30-polity study of how political systems re-integrate after collapse: four pathways, which ones last, and what predicts the outcome.",
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
    desc: "Integration built from shallow or fragmented predecessors — the state assembled where little existed. China, the EU, the Inca, Silla Korea, Meiji Japan.",
  },
  {
    name: "Restoration",
    count: 5,
    dur: 131.2,
    tone: "text-fg",
    desc: "A deep prior order rebuilt largely as it was — few institutional features flip. Middle-Kingdom Egypt and other high-ceiling revivals.",
  },
  {
    name: "Negotiation",
    count: 4,
    dur: 308.0,
    tone: "text-good",
    desc: "A deep order re-integrated slowly, by bargain rather than conquest — the most durable pathway by a wide margin.",
  },
  {
    name: "Redesign",
    count: 3,
    dur: 148.7,
    tone: "text-fg",
    desc: "A deep order rapidly reforged into a new institutional form — many features flip, fast. Argentina, Brazil.",
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
        how political orders <em>re-integrate</em> — collectivize — after they break apart. It covers{" "}
        <span className="mono">30</span> polities (<span className="mono">25</span> core cases plus{" "}
        <span className="mono">5</span> controls), from Tawantinsuyu and the Zulu Kingdom to the
        European Union.
      </p>

      <div className="mt-5 rounded-lg border border-innovation/30 bg-innovation/[0.06] p-4">
        <p className="text-[13px] leading-relaxed text-fg2">
          <span className="font-medium text-fg">A note on where this lives. </span>
          This study sits in a <em>sibling</em> research program — the fragmentation study — and is
          conceptually related to the Modernization Index but computed entirely separately. It is{" "}
          <span className="text-fg">not part of any country&apos;s MI score.</span>
        </p>
      </div>

      <section className="mt-10">
        <h2 className="serif text-xl">Four pathways — and which ones last</h2>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          Every re-integration falls into one of four pathways, sorted by how deep the predecessor
          order was and how fast the rebuild happened. The mean durability figures are the study&apos;s
          sharpest result:
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
                  <span className="mono ml-1 text-[11px] text-fg3">yr mean</span>
                </div>
              </div>
              <p className="mt-1.5 text-[13px] leading-relaxed text-fg2">{p.desc}</p>
            </div>
          ))}
        </div>
        <p className="mt-3 text-[14px] leading-relaxed text-fg2">
          <span className="font-medium text-fg">Negotiation wins, and it isn&apos;t close. </span>
          Bargained re-integrations lasted <span className="mono text-good">~308 years</span> on
          average, against <span className="mono">~119–149</span> for construction, restoration, and
          redesign. Orders talked back together outlast orders forced back together.
        </p>
      </section>

      <section className="mt-10">
        <h2 className="serif text-xl">What predicts the outcome</h2>
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <div className="rounded-lg border border-border bg-surface2/40 p-4">
            <div className="mono text-lg font-semibold text-fg">ρ = −0.84</div>
            <div className="mt-1 text-[13px] leading-relaxed text-fg2">
              <span className="font-medium text-fg">Depth predicts form-shift. </span>
              The deeper the predecessor&apos;s integration, the fewer institutional features flip in
              the rebuild — a strong, tight relationship (p &lt; 0.001).
            </div>
          </div>
          <div className="rounded-lg border border-border bg-surface2/40 p-4">
            <div className="mono text-lg font-semibold text-fg">ρ ≈ 0.83</div>
            <div className="mt-1 text-[13px] leading-relaxed text-fg2">
              <span className="font-medium text-fg">Speed predicts integration loss. </span>
              Among deep orders, the slower and more drawn-out the re-integration, the more of the old
              integration it sheds — a gradual bargain loosens the prior order more than a sharp
              reforging does.
            </div>
          </div>
          <div className="rounded-lg border border-border bg-surface2/40 p-4">
            <div className="mono text-lg font-semibold text-warn">76%</div>
            <div className="mt-1 text-[13px] leading-relaxed text-fg2">
              <span className="font-medium text-fg">Warning signals fired</span> in 76% of core cases
              — efficiency decay, integration reversal, or legitimacy erosion showed up before the
              trouble did.
            </div>
          </div>
          <div className="rounded-lg border border-border bg-surface2/40 p-4">
            <div className="mono text-sm font-semibold text-danger">coordination failure</div>
            <div className="mt-1 text-[13px] leading-relaxed text-fg2">
              <span className="font-medium text-fg">The dominant failure channel. </span>
              When these orders came apart, they most often did so because the parts could no longer
              coordinate — not because any single part was conquered.
            </div>
          </div>
        </div>
        <p className="mt-3 text-[13px] leading-relaxed text-fg3">
          Two of the study&apos;s framing hypotheses split: form-shift <span className="text-fg2">is</span>{" "}
          supported (re-integration genuinely changes institutional form), but a strict one-way
          &quot;ratchet&quot; is <span className="text-fg2">not</span> — orders do not only tighten;
          some shed integration on the way through.
        </p>
      </section>

      <section className="mt-10">
        <h2 className="serif text-xl">The polities studied</h2>
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
            What the whole thing means →
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
