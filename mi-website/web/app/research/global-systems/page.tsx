import Link from "next/link";

export const metadata = {
  title: "State of the world - Modernization Index",
  description:
    "A system-level reading of the whole world from the same data: three improvement engines, an institutional container, texture, and the movement distribution.",
};

function BackLink() {
  return (
    <Link href="/research" className="link mono text-[12px]">
      ← Research
    </Link>
  );
}

function Stat({ value, label, tone = "fg" }: { value: string; label: string; tone?: string }) {
  const color = tone === "warn" ? "text-warn" : tone === "bad" ? "text-danger" : tone === "good" ? "text-good" : "text-fg";
  return (
    <div className="rounded-lg border border-border bg-surface2/40 p-3">
      <div className={`mono text-lg font-semibold ${color}`}>{value}</div>
      <div className="mt-0.5 text-[12px] leading-snug text-fg3">{label}</div>
    </div>
  );
}

export default function GlobalSystems() {
  return (
    <div className="mx-auto max-w-2xl py-10 sm:py-12">
      <BackLink />
      <h1 className="serif mt-3 text-3xl font-black sm:text-4xl">State of the world</h1>
      <p className="mt-4 text-[15px] leading-relaxed text-fg2">
        Where the country index scores one polity, this reads the whole{" "}
        <em>world system</em> from the same kind of data. It is a separate, system-level tier - a
        descriptive gauge, not a forecast, and it changes no country&apos;s score. Built on long-run
        proxies (V-Dem for institutions, Maddison for income), it is deliberately{" "}
        <span className="text-fg">exploratory</span>.
      </p>

      <section className="mt-10">
        <h2 className="serif text-xl">The three improvement engines</h2>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          Golden ages are dimension-specific and out of phase, so the engines are read separately,
          never collapsed into one number. Each is a global 10-year climb rate, compared against its
          own 1850-2012 historical-median &quot;firing&quot; bar.
        </p>
        <div className="mt-4 grid gap-3 sm:grid-cols-3">
          <Stat value="8% / 7%" label="Institutions - climb vs decline (median 5%): firing, but churning" tone="warn" />
          <Stat value="2%" label="Income climb (median 5%): quiet" />
          <Stat value="2%" label="Human capital climb (median 7%): quiet" />
        </div>
        <p className="mt-3 text-[13px] leading-relaxed text-fg3">
          As of 2024, only <span className="mono text-fg2">1 of 3</span> engines is firing - and the
          one that is (institutions) is running high climb <em>and</em> high decline at once, which
          nets to almost nothing. That is the churn case: activity without direction.
        </p>
      </section>

      <section className="mt-10">
        <h2 className="serif text-xl">The container - does a boom get absorbed, or rupture?</h2>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          The institutional <span className="text-fg">container</span> is net institutional change -
          climb minus decline. It is read two ways, and they can point opposite directions:
        </p>
        <ul className="mt-3 space-y-2 text-[14px] leading-relaxed text-fg2">
          <li>
            <span className="font-medium text-fg">Trailing</span> - the decade behind.
          </li>
          <li>
            <span className="font-medium text-fg">Forward</span> - the decade ahead. This is the actual
            discriminator between rupture and absorption.
          </li>
        </ul>
        <p className="mt-3 text-[14px] leading-relaxed text-fg2">
          The two really do diverge. In <span className="mono">1973</span> the trailing container read{" "}
          <span className="text-danger">collapse</span> (it was catching the 1960s decolonization
          reversals), yet forward it was <span className="text-good">strengthening +8pp</span> - the
          Third Wave of democratization was about to absorb the shock. In{" "}
          <span className="mono">1913</span> the reverse: trailing calm, forward brittle.
        </p>
        <div className="mt-4 rounded-lg border border-border bg-surface2/40 p-4">
          <p className="text-[13.5px] leading-relaxed text-fg2">
            <span className="font-medium text-fg">Why the present is genuinely unknowable. </span>
            The container that decides rupture-vs-absorption is the <em>forward</em> one - and for now
            it is right-censored: the decade ahead isn&apos;t observable yet. The current net reads{" "}
            <span className="mono text-warn">+1pp - flat</span>: neither clearly repairing nor clearly
            collapsing. That ambiguity is honest, not reassuring.
          </p>
        </div>
      </section>

      <section className="mt-10">
        <h2 className="serif text-xl">The supercycle shape - and what decides the sequel</h2>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          Three times, a sustained global growth boom has been followed by a rapid fall of nearly the
          same magnitude - roughly <span className="mono">1.5pp per decade</span>. The shape is real
          and it recurs.
        </p>
        <div className="mt-4 overflow-x-auto">
          <table className="w-full min-w-[26rem] text-[13px]">
            <thead>
              <tr className="text-left text-fg3">
                <th className="pb-2 font-normal">Episode</th>
                <th className="pb-2 font-normal">Peak → +10y</th>
                <th className="pb-2 font-normal">Fall</th>
                <th className="pb-2 font-normal">Sequel</th>
              </tr>
            </thead>
            <tbody className="text-fg2">
              <tr className="border-t border-border">
                <td className="py-2">Belle Époque</td>
                <td className="mono py-2">1.8% → 0.5%</td>
                <td className="mono py-2 text-danger">−1.3pp</td>
                <td className="py-2">WWI, interwar collapse, WWII</td>
              </tr>
              <tr className="border-t border-border">
                <td className="py-2">Trente glorieuses</td>
                <td className="mono py-2">3.3% → 1.4%</td>
                <td className="mono py-2 text-warn">−1.9pp</td>
                <td className="py-2">Stagflation, then survivable regime-shift</td>
              </tr>
              <tr className="border-t border-border">
                <td className="py-2">Second globalization</td>
                <td className="mono py-2">3.4% → 2.0%</td>
                <td className="mono py-2 text-warn">−1.4pp</td>
                <td className="py-2">GFC, stagnation, populism - ongoing</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p className="mt-3 text-[14px] leading-relaxed text-fg2">
          The same shape produced one catastrophe and one manageable transition. So you{" "}
          <span className="text-fg">cannot</span> read the outcome off the deceleration. What
          modulates it is the container&apos;s trajectory <em>during</em> the fall: 1913&apos;s
          institutions were collapsing alongside the slowdown (
          <span className="mono text-danger">net −1pp → −6pp by the 1930s</span>) and it ruptured;
          1973&apos;s were surging (<span className="mono text-good">net +8pp</span>) and it was
          absorbed. Today reads <span className="mono text-warn">+2pp on V-Dem but eroding
          underneath</span> - flat-to-eroding, leaning brittle.
        </p>
        <p className="mt-3 text-[13px] leading-relaxed text-fg3">
          Honest limit: this is <span className="mono">n=3</span> supercycles and{" "}
          <span className="mono">n=2</span> clean outcomes - a mechanism-consistent reading, not a
          statistically powered law. It is not a prediction of catastrophe. It is a precise statement
          of why the present is concerning: we are decelerating <em>without</em> the institutional
          strengthening that absorbed the last comparable deceleration.
        </p>
      </section>

      <section className="mt-10">
        <h2 className="serif text-xl">Texture &amp; the movement distribution</h2>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          <span className="font-medium text-fg">Texture</span> classifies the climb-vs-decline mix as
          surge, churn, stasis, or collapse. The current reading is{" "}
          <span className="mono text-warn">churn</span> - gains and losses both elevated, netting to
          flat. And the <span className="font-medium text-fg">movement distribution</span> splits the
          5-pillar panel by the quality of each country&apos;s trajectory:
        </p>
        <div className="mt-4 grid gap-3 sm:grid-cols-3">
          <Stat value="39%" label="ratchet rise (n=135)" />
          <Stat value="22%" label="stable" />
          <Stat value="13%" label="decline" tone="bad" />
          <Stat value="13%" label="hollow stability" tone="warn" />
          <Stat value="12%" label="windfall" tone="warn" />
          <Stat value="2%" label="real ascent" tone="good" />
        </div>
        <p className="mt-3 text-[13px] leading-relaxed text-fg3">
          Only <span className="mono text-good">2%</span> of countries are in a genuine
          institution-led ascent, while roughly a quarter are in <em>fake</em> improvement - income
          windfall or hollow stability masked by the human-capital ratchet. Read together: a
          multi-engine lull on a flat-to-eroding container. Over a long window the human-capital
          ratchet inflates the &quot;ratchet rise&quot; share, so read the container and texture for
          the net.
        </p>
      </section>

      <section className="mt-10 rounded-lg border border-border bg-surface2/40 p-4">
        <p className="text-[13px] leading-relaxed text-fg2">
          This gauge shares the country index&apos;s epistemic -{" "}
          <em>trust the level, distrust the slope</em> - but answers a different question. Pair every
          reading with its printed caveats.
        </p>
        <div className="mono mt-2 flex flex-wrap gap-x-5 gap-y-1 text-[13px]">
          <Link href="/research/golden-ages" className="link">
            Are golden ages predictable? →
          </Link>
          <Link href="/how-it-works" className="link">
            How the country score works →
          </Link>
          <Link href="/limits" className="link">
            What it can&apos;t tell you →
          </Link>
        </div>
      </section>
    </div>
  );
}
