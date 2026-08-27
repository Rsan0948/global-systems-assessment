import Link from "next/link";

export const metadata = {
  title: "How the pieces fit together | Modernization Index",
  description:
    "How the score, safeguards, historical tests, and open questions fit into one research program.",
};

function BackLink() {
  return (
    <Link href="/research" className="link mono text-[12px]">
      ← Research
    </Link>
  );
}

const FEATURES = [
  [
    "Keep the detail visible",
    "The five pillars, safeguards, and two levels of measurement stay available instead of disappearing into one score.",
  ],
  [
    "Test relationships",
    "The strongest findings concern gaps and combinations among indicators, not any single raw value.",
  ],
  [
    "Allow patterns to change",
    "Different pillars matter in different periods. The framework does not assume one cause explains every case.",
  ],
  [
    "Show conflicting signals",
    "A country can improve in one area and weaken in another. Those disagreements remain visible in the result.",
  ],
  [
    "Compare within a period",
    "Countries and historical cases are read alongside their contemporaries, which makes comparisons across eras more careful.",
  ],
  [
    "Make results traceable",
    "The calculation uses published data and fixed code. Anyone can inspect the inputs and reproduce the output.",
  ],
];

export default function Substrate() {
  return (
    <div className="mx-auto max-w-2xl py-10 sm:py-12">
      <BackLink />
      <h1 className="serif mt-3 text-3xl font-black sm:text-4xl">How the pieces fit together</h1>
      <p className="mt-4 text-[15px] leading-relaxed text-fg2">
        The public score is only one part of the project. The pillar data, safeguards, historical
        cases, and failed tests are kept alongside it so people can inspect where a reading came from
        and where the evidence remains uncertain.
      </p>

      <section className="mt-10 space-y-4 text-[14.5px] leading-relaxed text-fg2">
        <p>
          A single ranking is easy to read, but it hides most of the useful information. A single
          theory creates a different problem because it can force unrelated cases into the same
          explanation. This project keeps several measurements and hypotheses in view at once.
        </p>
        <p>
          The common thread is simple: compare a system&apos;s resources, institutions, and exposure to
          pressure, then check whether the same relationships recur in other places and periods. The
          result is a research framework, not a claim that one number explains political history.
        </p>
      </section>

      <section className="mt-8">
        <div className="grid gap-3 sm:grid-cols-2">
          {FEATURES.map(([heading, body]) => (
            <div key={heading} className="rounded-lg border border-border bg-surface2/40 p-4">
              <h3 className="serif text-[15px] text-fg">{heading}</h3>
              <p className="mt-1 text-[13px] leading-relaxed text-fg2">{body}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mt-10 space-y-4 text-[14.5px] leading-relaxed text-fg2">
        <h2 className="serif text-xl text-fg">What the evidence supports</h2>
        <p>
          Several relationships recur in the modern panel and in the historical cases, including the
          durability gap and the institutional container. That makes them worth studying. It does not
          make them proven forecasts. Most historical cases were scored with the outcome already
          known, and some thresholds were adjusted during development.
        </p>
        <p>
          Failed tests are published for the same reason. The proposed golden-age signature did not
          survive its holdout test. Other ideas, including a fixed modernization sequence and a simple
          commodity explanation, also fell short. Recording those results helps prevent the same weak
          claims from being recycled later.
        </p>
        <p>
          The next stage is straightforward but demanding: add more cases, register tests before
          seeing the results, and improve coverage without hiding missing data. Until that work is
          done, the project should be used as a structural comparison tool rather than an event
          prediction system.
        </p>
      </section>

      <section className="mt-10 rounded-lg border border-border bg-surface2/40 p-4">
        <p className="text-[13px] leading-relaxed text-fg2">
          Today, the framework helps explain why a country receives a particular reading and which
          parts of that reading deserve caution. It also gives future research a clear set of claims
          to test.
        </p>
        <div className="mono mt-2 flex flex-wrap gap-x-5 gap-y-1 text-[13px]">
          <Link href="/validation" className="link">Review the evidence →</Link>
          <Link href="/limits" className="link">Read the limits →</Link>
          <Link href="/research" className="link">All research →</Link>
        </div>
      </section>
    </div>
  );
}
