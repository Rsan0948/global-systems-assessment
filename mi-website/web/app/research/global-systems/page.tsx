import Link from "next/link";

export const metadata = {
  title: "State of the world | Modernization Index",
  description:
    "A global comparison of three improvement measures, institutional change, and the distribution of country-level movement.",
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
        This page looks for broad global patterns using long-term data from V-Dem for institutions
        and Maddison for income. It is a separate exploratory analysis, not a forecast, and it does
        not change any country&apos;s score.
      </p>

      <section className="mt-10">
        <h2 className="serif text-xl">Three measures of global improvement</h2>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          Institutions, income, and human capital can improve at different times, so they are shown
          separately. Each number is a global 10-year improvement rate compared with its own median
          from 1850 to 2012.
        </p>
        <div className="mt-4 grid gap-3 sm:grid-cols-3">
          <Stat value="8% / 7%" label="Institutional improvement versus decline; historical median 5%" tone="warn" />
          <Stat value="2%" label="Income improvement; historical median 5%" />
          <Stat value="2%" label="Human capital improvement; historical median 7%" />
        </div>
        <p className="mt-3 text-[13px] leading-relaxed text-fg3">
          As of 2024, only <span className="mono text-fg2">1 of 3</span> measures is above its historical
          median. Institutional gains and declines are both high, so the net change is small.
        </p>
      </section>

      <section className="mt-10">
        <h2 className="serif text-xl">Net institutional change</h2>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          This measure subtracts the share of countries in institutional decline from the share in
          institutional improvement. The study compares two periods:
        </p>
        <ul className="mt-3 space-y-2 text-[14px] leading-relaxed text-fg2">
          <li>
            <span className="font-medium text-fg">Previous decade:</span> what had already happened at the reference date.
          </li>
          <li>
            <span className="font-medium text-fg">Following decade:</span> what happened after the reference date.
          </li>
        </ul>
        <p className="mt-3 text-[14px] leading-relaxed text-fg2">
          The two periods can look different. At the 1973 reference point, the previous decade showed
          institutional decline, partly because of reversals during decolonization. The following
          decade improved by 8 percentage points during the Third Wave of democratization. The 1913
          reference point showed the opposite pattern: a calm previous decade followed by decline.
        </p>
        <div className="mt-4 rounded-lg border border-border bg-surface2/40 p-4">
          <p className="text-[13.5px] leading-relaxed text-fg2">
            <span className="font-medium text-fg">Why the current reading is incomplete. </span>
            The historical comparison depends on the following decade, which has not happened yet.
            The current net reads{" "}
            <span className="mono text-warn">+1 percentage point, roughly flat</span>. That is not a clear signal of
            either institutional repair or decline.
          </p>
        </div>
      </section>

      <section className="mt-10">
        <h2 className="serif text-xl">What followed three global slowdowns</h2>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          Three times, a sustained global growth boom has been followed by a rapid fall of nearly the
          same magnitude, roughly <span className="mono">1.5 percentage points per decade</span>. The sample contains
          only three episodes, so the comparison is descriptive.
        </p>
        <div className="mt-4 overflow-x-auto">
          <table className="w-full min-w-[26rem] text-[13px]">
            <thead>
              <tr className="text-left text-fg3">
                <th className="pb-2 font-normal">Episode</th>
                <th className="pb-2 font-normal">Peak to 10 years later</th>
                <th className="pb-2 font-normal">Fall</th>
                <th className="pb-2 font-normal">Sequel</th>
              </tr>
            </thead>
            <tbody className="text-fg2">
              <tr className="border-t border-border">
                <td className="py-2">Belle Époque</td>
                <td className="mono py-2">1.8% → 0.5%</td>
                <td className="mono py-2 text-danger">−1.3 points</td>
                <td className="py-2">WWI, interwar collapse, WWII</td>
              </tr>
              <tr className="border-t border-border">
                <td className="py-2">Trente glorieuses</td>
                <td className="mono py-2">3.3% → 1.4%</td>
                <td className="mono py-2 text-warn">−1.9 points</td>
                <td className="py-2">Stagflation, then a manageable political transition</td>
              </tr>
              <tr className="border-t border-border">
                <td className="py-2">Second globalization</td>
                <td className="mono py-2">3.4% → 2.0%</td>
                <td className="mono py-2 text-warn">−1.4 points</td>
                <td className="py-2">Global financial crisis, stagnation, and populism; still ongoing</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p className="mt-3 text-[14px] leading-relaxed text-fg2">
          The same shape produced one catastrophe and one manageable transition. So you{" "}
          <span className="text-fg">cannot</span> read the outcome off the deceleration. What
          appears to matter is net institutional change <em>during</em> the fall: 1913&apos;s
          institutions were collapsing alongside the slowdown (
          <span className="mono text-danger">net −1 point to −6 points by the 1930s</span>) and it ruptured;
          1973&apos;s were surging (<span className="mono text-good">net +8 points</span>) and it was
          absorbed. Today reads <span className="mono text-warn">+2 points on V-Dem but eroding
          underneath</span>. This is a flat or slightly weakening reading.
        </p>
        <p className="mt-3 text-[13px] leading-relaxed text-fg3">
          This comparison covers <span className="mono">three</span> global growth cycles and{" "}
          <span className="mono">n=2</span> completed outcomes. That is too small for a statistical law
          or a prediction of catastrophe. It does show that the current slowdown lacks the clear
          institutional strengthening seen during the comparable 1973 episode.
        </p>
      </section>

      <section className="mt-10">
        <h2 className="serif text-xl">How country scores are moving</h2>
        <p className="mt-2 text-[14px] leading-relaxed text-fg2">
          The current period has elevated gains and losses that largely cancel each other out. The
          categories below show how country-level scores are moving within the five-pillar dataset:
        </p>
        <div className="mt-4 grid gap-3 sm:grid-cols-3">
          <Stat value="39%" label="broad gradual rise (n=135)" />
          <Stat value="22%" label="stable" />
          <Stat value="13%" label="decline" tone="bad" />
          <Stat value="13%" label="uneven stability" tone="warn" />
          <Stat value="12%" label="income-led rise" tone="warn" />
          <Stat value="2%" label="institution-led ascent" tone="good" />
        </div>
        <p className="mt-3 text-[13px] leading-relaxed text-fg3">
          Only <span className="mono text-good">2%</span> of countries show an
          institution-led ascent, while roughly a quarter show income gains without similar
          institutional gains. Human capital usually changes slowly and tends to rise over long
          periods, so the 39 percent broad-rise category should not be read as rapid institutional
          improvement.
        </p>
      </section>

      <section className="mt-10 rounded-lg border border-border bg-surface2/40 p-4">
        <p className="text-[13px] leading-relaxed text-fg2">
          This gauge is more useful for describing the current level than for projecting the next
          movement. Its uncertainty notes should be read alongside every result.
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
