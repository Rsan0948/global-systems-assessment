import Link from "next/link";
import { RESEARCH_TOPICS } from "@/lib/research";

export const metadata = {
  title: "Research - Modernization Index",
  description:
    "Distilled findings from the Modernization Index research program - what held up, what failed, and what it all means.",
};

export default function Research() {
  return (
    <div className="py-10 sm:py-12">
      <section className="mx-auto max-w-2xl">
        <h1 className="serif text-3xl font-black sm:text-4xl">Research</h1>
        <p className="mt-4 text-[15px] leading-relaxed text-fg2">
          The country scores are the instrument&apos;s output. These four pieces are the research
          behind and around it - read the whole world from the same data, ask what history is
          actually predictable, watch orders rebuild after they fragment, and step back to what the
          project is really <em>for</em>. We report the failures with the same prominence as the
          wins; on this program, a clean failed prediction is a feature.
        </p>
      </section>

      <section className="mx-auto mt-10 grid max-w-4xl gap-4 sm:grid-cols-2">
        {RESEARCH_TOPICS.map((t) => (
          <Link
            key={t.slug}
            href={`/research/${t.slug}`}
            className="card lift flex flex-col gap-2 p-5"
          >
            <div className="flex items-center justify-between gap-2">
              <span className="mono text-[10px] uppercase tracking-wider text-fg3">{t.kind}</span>
              <span className="mono text-[10px] text-fg3">{t.status}</span>
            </div>
            <h2 className="serif text-lg text-fg">{t.title}</h2>
            <p className="text-[13.5px] leading-relaxed text-fg2">{t.lede}</p>
            <span className="link mt-1 text-[13px]">Read →</span>
          </Link>
        ))}
      </section>

      <section className="mx-auto mt-8 max-w-2xl">
        <div className="rounded-lg border border-border bg-surface2/40 p-4">
          <p className="text-[13px] text-fg2">
            Looking for how the score itself is built, or how far it can be trusted?
          </p>
          <div className="mono mt-2 flex flex-wrap gap-x-5 gap-y-1 text-[13px]">
            <Link href="/how-it-works" className="link">
              How it works →
            </Link>
            <Link href="/validation" className="link">
              How we know it works →
            </Link>
            <Link href="/limits" className="link">
              What it can&apos;t tell you →
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
