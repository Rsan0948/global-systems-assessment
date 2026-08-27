import Link from "next/link";
import { RESEARCH_TOPICS } from "@/lib/research";

export const metadata = {
  title: "Research | Modernization Index",
  description:
    "Results, failed tests, and open questions from the Modernization Index research program.",
};

export default function Research() {
  return (
    <div className="py-10 sm:py-12">
      <section className="mx-auto max-w-2xl">
        <h1 className="serif text-3xl font-black sm:text-4xl">Research</h1>
        <p className="mt-4 text-[15px] leading-relaxed text-fg2">
          The country scores are one output of a larger research program. These pages examine global
          patterns, test whether historical change can be anticipated, compare how political orders
          rebuild, and explain how the pieces fit together. Failed tests are included because they
          narrow the claims the project can responsibly make.
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
              Review the evidence →
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
