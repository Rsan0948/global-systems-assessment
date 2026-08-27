import Link from "next/link";

export const metadata = {
  title: "Are golden ages predictable? | Modernization Index",
  description:
    "A prediction recorded in advance that failed when tested on reserved data, plus the weaker patterns that remained.",
};

function BackLink() {
  return (
    <Link href="/research" className="link mono text-[12px]">
      ← Research
    </Link>
  );
}

export default function GoldenAges() {
  return (
    <div className="mx-auto max-w-2xl py-10 sm:py-12">
      <BackLink />
      <h1 className="serif mt-3 text-3xl font-black sm:text-4xl">Are golden ages predictable?</h1>
      <p className="mt-4 text-[15px] leading-relaxed text-fg2">
        Here, a golden age means an institutional improvement that continues over time. We tested
        whether the index could forecast one. The proposed signal failed its test. A weaker pattern
        based on a country&apos;s starting level appeared in one period, but it did not continue after 2012.
      </p>

      <section className="mt-10">
        <div className="flex items-center gap-2">
          <span className="mono rounded bg-danger/15 px-2 py-0.5 text-[11px] font-semibold text-danger">
            TEST DID NOT REPEAT
          </span>
          <h2 className="serif text-xl">The registered prediction failed</h2>
        </div>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          Before examining the second dataset, we recorded a specific claim in Git: a sudden
          improvement in control of corruption would predict a sustained institutional climb. The
          pattern appeared among 89 countries used to develop the idea, but not among the 112 countries
          reserved for testing it.
        </p>
        <div className="mt-4 overflow-x-auto">
          <table className="w-full min-w-[24rem] text-[13px]">
            <thead>
              <tr className="text-left text-fg3">
                <th className="pb-2 font-normal">Set</th>
                <th className="pb-2 font-normal">Sustained climb</th>
                <th className="pb-2 font-normal">Overall rate</th>
                <th className="pb-2 font-normal">z score</th>
                <th className="pb-2 font-normal">Events</th>
              </tr>
            </thead>
            <tbody className="text-fg2">
              <tr className="border-t border-border">
                <td className="py-2">Discovery (89)</td>
                <td className="mono py-2">31%</td>
                <td className="mono py-2">18%</td>
                <td className="mono py-2 text-good">+3.0</td>
                <td className="mono py-2">87</td>
              </tr>
              <tr className="border-t border-border">
                <td className="py-2 font-medium text-fg">Reserved test set (112)</td>
                <td className="mono py-2">17%</td>
                <td className="mono py-2">17%</td>
                <td className="mono py-2 text-danger">−0.0</td>
                <td className="mono py-2">137</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p className="mt-3 text-[14px] leading-relaxed text-fg2">
          Across 137 events in the reserved test data, countries with the proposed signal improved at
          the same rate as the full group. The original pattern was concentrated around post-communist
          transitions and EU accession, so it did not generalize to other settings. No other
          institutional component produced the proposed effect either.
        </p>
        <p className="mt-2 text-[12px] leading-relaxed text-fg3">
          The z score shows how far each result is from the overall rate after accounting for sample
          size. A value near zero means no detectable difference.
        </p>
      </section>

      <section className="mt-10">
        <h2 className="serif text-xl">What appeared in the reserved data</h2>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          Two other relationships appeared in the reserved data. Neither was based on the country&apos;s
          recent institutional movement.
        </p>
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <div className="rounded-lg border border-border bg-surface2/40 p-4">
            <div className="mono text-lg font-semibold text-good">z score +2.4</div>
            <div className="mt-1 text-[13px] leading-relaxed text-fg2">
              <span className="font-medium text-fg">Low starting level</span> (Institutions below 0.40)
              was associated with a 20 percent climb rate, compared with 16 percent overall.
            </div>
          </div>
          <div className="rounded-lg border border-border bg-surface2/40 p-4">
            <div className="mono text-lg font-semibold text-danger">z score −1.7</div>
            <div className="mt-1 text-[13px] leading-relaxed text-fg2">
              <span className="font-medium text-fg">Recent gains often reversed.</span> Countries that
              had just improved were somewhat more likely to give back part of the gain.
            </div>
          </div>
        </div>
        <p className="mt-3 text-[14px] leading-relaxed text-fg2">
          Sustained climbs also clustered in time, especially from 2002 to 2005. The measured
          clustering was about twice the level expected from a random timing model. This suggests that
          wider historical conditions mattered, although this study did not isolate a single cause.
        </p>
      </section>

      <section className="mt-10">
        <div className="flex items-center gap-2">
          <span className="mono rounded bg-warn/15 px-2 py-0.5 text-[11px] font-semibold text-warn">
            PERIOD-SPECIFIC RESULT
          </span>
        </div>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          The low-starting-level pattern appeared when testing a different set of countries, but it
          did not appear when testing a later period. It was concentrated in the 2002 to 2011 window:
        </p>
        <div className="mt-4 overflow-x-auto">
          <table className="w-full min-w-[22rem] text-[13px]">
            <thead>
              <tr className="text-left text-fg3">
                <th className="pb-2 font-normal">Window</th>
                <th className="pb-2 font-normal">Low-start climb</th>
                <th className="pb-2 font-normal">High-start climb</th>
                <th className="pb-2 font-normal">z score</th>
              </tr>
            </thead>
            <tbody className="text-fg2">
              <tr className="border-t border-border">
                <td className="py-2">Discovery 2002 to 2011</td>
                <td className="mono py-2">15%</td>
                <td className="mono py-2">6%</td>
                <td className="mono py-2 text-good">+6.2</td>
              </tr>
              <tr className="border-t border-border">
                <td className="py-2 font-medium text-fg">Reserved test 2012 to 2019</td>
                <td className="mono py-2">5%</td>
                <td className="mono py-2">6%</td>
                <td className="mono py-2 text-danger">−0.6</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p className="mt-3 text-[14px] leading-relaxed text-fg2">
          Since 2012, countries starting at a low level have improved no more often than countries
          starting at a high level. Resource-rich countries also showed no special boost, so a simple
          commodity-cycle explanation was rejected. EU enlargement, debt relief, and post-Cold-War
          reforms are possible explanations for the earlier period, but none has been isolated.
        </p>
      </section>

      <section className="mt-10">
        <h2 className="serif text-xl">What the study currently supports</h2>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          The study does not identify a reliable current predictor of a sustained institutional
          climb. Recent movement failed the registered test, and the low-starting-level pattern did
          not persist after 2012. The most defensible result is that the 2002 to 2011 period was
          different, even though the cause of that difference remains uncertain.
        </p>
        <p className="mt-3 text-[13px] leading-relaxed text-fg3">
          A low starting value also has more room to rise, so part of the earlier pattern may be simple
          movement back toward the average. The possible historical explanations remain candidates,
          not confirmed causes.
        </p>
      </section>

      <section className="mt-10 rounded-lg border border-border bg-surface2/40 p-4">
        <p className="text-[13px] leading-relaxed text-fg2">
          The failed forecast remains published because it sets a clear limit on what the project can claim.
        </p>
        <div className="mono mt-2 flex flex-wrap gap-x-5 gap-y-1 text-[13px]">
          <Link href="/research/global-systems" className="link">
            State of the world →
          </Link>
          <Link href="/validation" className="link">
            Review the evidence →
          </Link>
          <Link href="/limits" className="link">
            What it can&apos;t tell you →
          </Link>
        </div>
      </section>
    </div>
  );
}
