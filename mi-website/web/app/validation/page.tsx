import Link from "next/link";

export const metadata = {
  title: "How we know it works (and where it doesn't) — Modernization Index",
  description:
    "The validation corpus, reported honestly: 109 cases across hindsight retrodiction and genuinely blind prediction — including where the blind tests came back weak.",
};

function Stat({ value, label, tone = "fg" }: { value: string; label: string; tone?: string }) {
  const color =
    tone === "warn" ? "text-warn" : tone === "bad" ? "text-danger" : tone === "good" ? "text-good" : "text-fg";
  return (
    <div className="rounded-lg border border-border bg-surface2/40 p-3">
      <div className={`mono text-lg font-semibold ${color}`}>{value}</div>
      <div className="mt-0.5 text-[12px] leading-snug text-fg3">{label}</div>
    </div>
  );
}

export default function Validation() {
  return (
    <div className="mx-auto max-w-2xl py-10 sm:py-12">
      <h1 className="serif text-3xl font-black sm:text-4xl">
        How we know it works — and where it doesn&apos;t
      </h1>
      <p className="mt-4 text-[15px] leading-relaxed text-fg2">
        The engine has been run against a corpus of <span className="mono">109</span> historical
        cases. Two very different things are going on in that number, and the honest story depends on
        keeping them apart: <span className="text-fg">hindsight retrodiction</span> (scored knowing
        how it turned out) and <span className="text-fg">blind prediction</span> (scored before the
        outcome was revealed). The first is strong and reproducible; the second is where the candor
        lives.
      </p>

      <section className="mt-10">
        <h2 className="serif text-xl">The corpus, honestly</h2>
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <Stat value="109" label="total cases" />
          <Stat value="84 + 25" label="modern + ancient (firewalled)" />
        </div>
        <p className="mt-4 text-[14px] leading-relaxed text-fg2">
          The 84 modern cases are three separate sets that test different claims and are scored
          separately:
        </p>
        <div className="mt-4 space-y-3">
          <div className="rounded-lg border border-border bg-surface2/40 p-4">
            <div className="flex items-baseline gap-2">
              <span className="mono text-[13px] font-semibold text-primary">51</span>
              <h3 className="serif text-base text-fg">P1-ordinality cases</h3>
            </div>
            <p className="mt-1 text-[13px] leading-relaxed text-fg2">
              The retrodiction baseline: does the framework rank who fractures worse, and why? Best
              estimate <span className="mono">~78%</span> clean — honestly a{" "}
              <span className="mono">62–85%</span> range — with{" "}
              <span className="mono text-good">~100% directional</span> (zero falsifications). After
              re-scoring every case on live data, the tally landed at{" "}
              <span className="mono">109C / 38P / 0F ≈ 74%</span>, within that band.
            </p>
          </div>
          <div className="rounded-lg border border-border bg-surface2/40 p-4">
            <div className="flex items-baseline gap-2">
              <span className="mono text-[13px] font-semibold text-primary">19</span>
              <h3 className="serif text-base text-fg">durability-gate cases</h3>
            </div>
            <p className="mt-1 text-[13px] leading-relaxed text-fg2">
              Tests whether the durability gap (Safeguard J: income running ahead of institutions)
              correctly calls crisis vs absorption.{" "}
              <span className="mono text-good">17 of 19 correct (89%)</span>.
            </p>
          </div>
          <div className="rounded-lg border border-border bg-surface2/40 p-4">
            <div className="flex items-baseline gap-2">
              <span className="mono text-[13px] font-semibold text-primary">14</span>
              <h3 className="serif text-base text-fg">rule-validation cases</h3>
            </div>
            <p className="mt-1 text-[13px] leading-relaxed text-fg2">
              Blind tests of the convergence and accountability rules:{" "}
              <span className="mono">8 confirmed · 2 indeterminate · 2 falsified · 2 pre-WGI N/A</span>
              . The two falsifications are kept on the record, not laundered out.
            </p>
          </div>
        </div>
        <p className="mt-4 text-[13px] leading-relaxed text-fg3">
          A separate <span className="mono">25</span> pre-modern cases (c. 2686 BCE – 1797 CE) are
          <span className="text-fg2"> firewalled</span> at the lowest-confidence tier: interpreter-scored,
          with hindsight, they inform hypotheses only and never touch the modern baseline.
        </p>
      </section>

      <section className="mt-10">
        <h2 className="serif text-xl">The blind tests — directional, but weak</h2>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          Most of the track record above was scored knowing outcomes — that is reproducibility, not
          validated prediction. The genuinely out-of-sample runs, where a framework-naive agent picked
          the cases at random, are the honest measure. They point the right way and land soft.
        </p>
        <div className="mt-4 space-y-3">
          <div className="rounded-lg border border-warn/25 bg-warn/[0.05] p-4">
            <h3 className="serif text-base text-fg">30 blind modern cases</h3>
            <p className="mt-1 text-[13px] leading-relaxed text-fg2">
              Both load-bearing claims pointed the right way out of sample, but only weakly —{" "}
              <span className="mono">Cohen d ≈ 0.37</span>, not significant, on a small non-severe n.
              In the docs&apos; own words: <span className="text-fg italic">&quot;Not a validation, not
              a refutation.&quot;</span> A random draw from coup and conflict catalogs is dominated by
              exogenous shocks — invasions, external defeats — which is exactly the regime the
              framework <em>disclaims</em>. The sample over-sampled the blind spot. The clean signal
              still showed at the extremes: the lowest-institution states all ruptured; the highest
              took the mildest paths.
            </p>
          </div>
          <div className="rounded-lg border border-warn/25 bg-warn/[0.05] p-4">
            <h3 className="serif text-base text-fg">10 blind ancient cases</h3>
            <p className="mt-1 text-[13px] leading-relaxed text-fg2">
              Fatally, near-zero outcome variance — <span className="mono">9 of 10</span> ended in
              collapse, because pre-modern shocks are remembered <em>because</em> they ended states. It
              cannot validate anything; it offers one anecdote in the right direction (survivors&apos;
              mean pre-shock institutions <span className="mono">≈ 4.5</span> vs{" "}
              <span className="mono">≈ 2.4</span> for those that ceased to exist).
            </p>
          </div>
        </div>
        <p className="mt-4 text-[13px] leading-relaxed text-fg3">
          The design lesson is the real deliverable: a fair test must be selected on the{" "}
          <em>shock</em>, not the outcome, and stratified by endogenous vs exogenous stress. Testing a
          structural framework on an invasion-dominated random sample tests it largely where it says it
          can&apos;t predict.
        </p>
      </section>

      <section className="mt-10">
        <div className="rounded-lg border border-border bg-surface2/40 p-4">
          <p className="text-[13.5px] leading-relaxed text-fg2">
            <span className="font-medium text-fg">The bottom line. </span>
            Strongly and reproducibly consistent across data and eras; one pre-registered forward test
            (the golden-age signature) failed; true predictive validation is still owed. We report the
            range, never a single triumphant number.
          </p>
        </div>
      </section>

      <section className="mt-8">
        <p className="text-[13px] leading-relaxed text-fg3">
          A full case-by-case explorer — every prediction, its verdict, and the live data behind it —
          is the next build sprint. It isn&apos;t here yet.
        </p>
        <div className="mono mt-3 flex flex-wrap gap-x-5 gap-y-1 text-[13px]">
          <Link href="/research/golden-ages" className="link">
            The forecast that failed →
          </Link>
          <Link href="/research/substrate" className="link">
            What the whole thing means →
          </Link>
          <Link href="/limits" className="link">
            What it can&apos;t tell you →
          </Link>
        </div>
      </section>
    </div>
  );
}
