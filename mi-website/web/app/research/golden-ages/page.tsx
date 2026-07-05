import Link from "next/link";

export const metadata = {
  title: "Are golden ages predictable? — Modernization Index",
  description:
    "A pre-registered prediction that failed its geographic holdout — and the honest signal that survived. Trust the level; distrust the slope.",
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
        A golden age is a durable institutional climb — a country that starts rising and keeps
        rising. We asked whether the index could <em>forecast</em> one. The honest headline:{" "}
        <span className="text-fg">
          you can predict a climb from where a country starts and when it lives, but not from its own
          institutional trajectory.
        </span>{" "}
        Trust the level; distrust the slope.
      </p>

      <section className="mt-10">
        <div className="flex items-center gap-2">
          <span className="mono rounded bg-danger/15 px-2 py-0.5 text-[11px] font-semibold text-danger">
            FAILED HOLDOUT
          </span>
          <h2 className="serif text-xl">The pre-registered prediction did not survive</h2>
        </div>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          Before touching the unseen data, we froze a specific claim in git: a punctuated
          control-of-corruption jump forecasts a durable climb. We discovered it on 89 countries and
          tested it on 112 unseen ones. It fired cleanly in discovery and{" "}
          <span className="text-fg">evaporated</span> on the holdout.
        </p>
        <div className="mt-4 overflow-x-auto">
          <table className="w-full min-w-[24rem] text-[13px]">
            <thead>
              <tr className="text-left text-fg3">
                <th className="pb-2 font-normal">Set</th>
                <th className="pb-2 font-normal">Durable rate</th>
                <th className="pb-2 font-normal">Base rate</th>
                <th className="pb-2 font-normal">z</th>
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
                <td className="py-2 font-medium text-fg">Holdout (112 unseen)</td>
                <td className="mono py-2">17%</td>
                <td className="mono py-2">17%</td>
                <td className="mono py-2 text-danger">−0.0</td>
                <td className="mono py-2">137</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p className="mt-3 text-[14px] leading-relaxed text-fg2">
          <span className="mono">137</span> well-powered holdout events and{" "}
          <span className="text-fg">exactly zero lift</span> — not underpowered, a clean null. The
          discovery signal was a post-communist / EU-accession transition-era artifact, not a law. No
          other institutional-component jump rescued it either. This is the point of the page: a real
          pre-registered forecast, honestly failed.
        </p>
      </section>

      <section className="mt-10">
        <h2 className="serif text-xl">But golden ages are not random — the structure is elsewhere</h2>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          Casting a wide net on the holdout, two things <em>did</em> hold out of sample — and neither
          is the country&apos;s own slope.
        </p>
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <div className="rounded-lg border border-border bg-surface2/40 p-4">
            <div className="mono text-lg font-semibold text-good">+2.4z</div>
            <div className="mt-1 text-[13px] leading-relaxed text-fg2">
              <span className="font-medium text-fg">Low starting base</span> (P1 &lt; 0.40) predicts
              the climb: 20% vs a 16% base. Room to rise — where you <em>start</em> carries signal.
            </div>
          </div>
          <div className="rounded-lg border border-border bg-surface2/40 p-4">
            <div className="mono text-lg font-semibold text-danger">−1.7z</div>
            <div className="mt-1 text-[13px] leading-relaxed text-fg2">
              <span className="font-medium text-fg">Recent momentum is negative</span>: countries that
              just rose tend to give it back. No flywheel — the gains mean-revert.
            </div>
          </div>
        </div>
        <p className="mt-3 text-[14px] leading-relaxed text-fg2">
          And golden ages arrive in <span className="font-medium text-fg">waves</span>: climb-starts
          cluster in time at <span className="mono">CV 0.50</span> against a Poisson-random{" "}
          <span className="mono">~0.26</span> — about twice the clustering chance would produce, with
          a clear 2002–2005 wave. The driver is largely exogenous: a low starting position caught in a
          global reform window, which pillar slopes cannot see.
        </p>
      </section>

      <section className="mt-10">
        <div className="flex items-center gap-2">
          <span className="mono rounded bg-warn/15 px-2 py-0.5 text-[11px] font-semibold text-warn">
            AND EVEN THE LEVEL IS ERA-CONDITIONAL
          </span>
        </div>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          The candor goes one layer deeper. The low-base effect that survived the{" "}
          <em>geographic</em> holdout does <span className="text-fg">not</span> survive the{" "}
          <em>temporal</em> one. It was carried entirely by the 2002–2011 wave:
        </p>
        <div className="mt-4 overflow-x-auto">
          <table className="w-full min-w-[22rem] text-[13px]">
            <thead>
              <tr className="text-left text-fg3">
                <th className="pb-2 font-normal">Window</th>
                <th className="pb-2 font-normal">Low-base climb</th>
                <th className="pb-2 font-normal">High-base</th>
                <th className="pb-2 font-normal">z</th>
              </tr>
            </thead>
            <tbody className="text-fg2">
              <tr className="border-t border-border">
                <td className="py-2">Discovery 2002–11</td>
                <td className="mono py-2">15%</td>
                <td className="mono py-2">6%</td>
                <td className="mono py-2 text-good">+6.2</td>
              </tr>
              <tr className="border-t border-border">
                <td className="py-2 font-medium text-fg">Held-out 2012–19</td>
                <td className="mono py-2">5%</td>
                <td className="mono py-2">6%</td>
                <td className="mono py-2 text-danger">−0.6</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p className="mt-3 text-[14px] leading-relaxed text-fg2">
          Since roughly 2012, low base is dormant — no better than high base. We also{" "}
          <span className="text-fg">retracted</span> our own &quot;commodity cycle&quot; label:
          resource-rich states showed no boom-year boost (<span className="mono">z +0.6</span>); the
          entire era effect lives in resource-<em>poor</em> countries, so the mechanism is not
          commodities — it is an unidentified era wave (EU enlargement, debt relief, the post–Cold-War
          high tide are candidates, none isolated). Post-communist transition <em>does</em> add,
          net of base.
        </p>
      </section>

      <section className="mt-10">
        <h2 className="serif text-xl">The honest standing claim</h2>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          Within the 2002–2011 wave, low base and transition-origin forecast climbs; outside{" "}
          <em>all</em> structural conditions the climb rate drops below the base rate (
          <span className="mono">4% vs 7%, z −3.6</span>). The wave ended around 2012, and since then{" "}
          <span className="text-fg">nothing reliably forecasts a golden age</span> — not the internal
          slope (refuted), not low base (dormant), nothing. We are in a golden-age drought. That the
          system can find the <em>era</em> but not a <em>live</em> predictor is itself the finding.
        </p>
        <p className="mt-3 text-[13px] leading-relaxed text-fg3">
          Caveat: the low-base effect is partly mechanical mean-reversion (a low value has more
          headroom); the era mechanism is named only by candidates, not isolated. A trajectory-based
          instrument is simply the wrong shape for a phenomenon driven by level and exogenous waves.
        </p>
      </section>

      <section className="mt-10 rounded-lg border border-border bg-surface2/40 p-4">
        <p className="text-[13px] leading-relaxed text-fg2">
          This is the same discipline the whole index runs on: report the failed forecast as loudly as
          the win.
        </p>
        <div className="mono mt-2 flex flex-wrap gap-x-5 gap-y-1 text-[13px]">
          <Link href="/research/global-systems" className="link">
            State of the world →
          </Link>
          <Link href="/validation" className="link">
            How we know it works →
          </Link>
          <Link href="/limits" className="link">
            What it can&apos;t tell you →
          </Link>
        </div>
      </section>
    </div>
  );
}
