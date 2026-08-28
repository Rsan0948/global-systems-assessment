import Link from "next/link";

export const metadata = {
  title: "What the evidence shows",
  alternates: { canonical: "/validation" },
  description:
    "A clear account of the historical cases, blind tests, failed forward test, and pending forecasts.",
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
      <h1 className="serif text-3xl font-black sm:text-4xl">What the evidence shows</h1>
      <p className="mt-4 text-[15px] leading-relaxed text-fg2">
        This project contains several kinds of evidence. They answer different questions, so we keep
        them separate. Reproducing an old case is useful, but it is not the same thing as predicting a
        case whose outcome was hidden.
      </p>

      <section className="mt-10">
        <h2 className="serif text-xl">Four evidence collections</h2>
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <Stat value="84" label="modern cases scored with outcomes known" />
          <Stat value="25" label="ancient cases interpreted by a human coder" tone="warn" />
          <Stat value="67" label="observations tested without using their outcomes" />
          <Stat value="12" label="external-security records kept separate from scoring" tone="warn" />
        </div>
        <p className="mt-4 text-[14px] leading-relaxed text-fg2">
          The number <span className="mono">109</span> refers only to the historical case collection:
          84 modern cases plus 25 ancient cases. It is not a record of 109 blind predictions. The
          separate collectivization study also contains 109 formation cycles, but those cycles are
          not part of the Modernization Index evidence collection.
        </p>
      </section>

      <section className="mt-10">
        <h2 className="serif text-xl">The historical cases</h2>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          The 84 modern cases show that the framework can reproduce many expected relationships across
          different eras and types of stress. The outcomes were known during selection, scoring, or
          calibration. These results show historical consistency, not successful forecasting.
        </p>
        <div className="mt-4 rounded-lg border border-warn/25 bg-warn/[0.05] p-4">
          <h3 className="serif text-base text-fg">The ancient extension</h3>
          <p className="mt-1 text-[13px] leading-relaxed text-fg2">
            The 25 ancient cases are a lower-confidence consistency check. A human coder interpreted
            them with outcome knowledge. They are kept separate and need independent recoding.
          </p>
        </div>
      </section>

      <section className="mt-10">
        <h2 className="serif text-xl">The blind tests</h2>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          The 67 observations tested without using their outcomes come from several designs. They
          should not be compressed into one accuracy percentage.
        </p>
        <div className="mt-4 space-y-3">
          <div className="rounded-lg border border-border bg-surface2/40 p-4">
            <h3 className="serif text-base text-fg">Random sample of modern cases</h3>
            <p className="mt-1 text-[13px] leading-relaxed text-fg2">
              The main signal pointed in the expected direction, but it was weak, at about{" "}
              <span className="mono">a standardized difference of 0.37</span>. This was not a clear validation or a clear
              rejection of the idea.
            </p>
          </div>
          <div className="rounded-lg border border-border bg-surface2/40 p-4">
            <h3 className="serif text-base text-fg">Ancient cases tested blind</h3>
            <p className="mt-1 text-[13px] leading-relaxed text-fg2">
              Nine of ten sampled cases ended in collapse. With almost no outcome variation, the
              group could not show whether the method separates collapse from survival.
            </p>
          </div>
          <div className="rounded-lg border border-border bg-surface2/40 p-4">
            <h3 className="serif text-base text-fg">Groups exposed to major shocks</h3>
            <p className="mt-1 text-[13px] leading-relaxed text-fg2">
              Later tests showed stronger results within some groups, but no overall effect when all
              groups were combined. This suggests that any useful relationship may depend on context.
            </p>
          </div>
        </div>
      </section>

      <section className="mt-10">
        <h2 className="serif text-xl">Tests registered before the outcome</h2>
        <div className="mt-4 space-y-3">
          <div className="rounded-lg border border-danger/25 bg-danger/[0.05] p-4">
            <h3 className="serif text-base text-fg">Golden-age signature</h3>
            <p className="mt-1 text-[13px] leading-relaxed text-fg2">
              The forward test recorded in advance failed. The signal was not added to the live framework.
            </p>
          </div>
          <div className="rounded-lg border border-warn/25 bg-warn/[0.05] p-4">
            <h3 className="serif text-base text-fg">Sealed country flags</h3>
            <p className="mt-1 text-[13px] leading-relaxed text-fg2">
              These forecasts are still pending. Each has written conditions for deciding whether it
              succeeds or fails, but none can count as evidence until its review date arrives.
            </p>
          </div>
        </div>
      </section>

      <section className="mt-10 rounded-lg border border-border bg-surface2/40 p-4">
        <p className="text-[13.5px] leading-relaxed text-fg2">
          <span className="font-medium text-fg">The bottom line. </span>
          The framework is reproducible and historically suggestive. Its blind evidence is mixed, one
          forward-looking test failed, and its main forecasts are still pending. That is enough to keep
          testing. It is not enough to claim reliable political prediction.
        </p>
      </section>

      <section className="mt-8">
        <div className="mono flex flex-wrap gap-x-5 gap-y-1 text-[13px]">
          <a
            href="https://github.com/Rsan0948/universalsystemgrade/blob/main/mi-research/docs/CLAIMS_LEDGER.md"
            className="link"
          >
            Read the claims ledger →
          </a>
          <Link href="/research/golden-ages" className="link">
            Read about the failed test →
          </Link>
          <Link href="/limits" className="link">
            See the limits →
          </Link>
        </div>
      </section>
    </div>
  );
}
