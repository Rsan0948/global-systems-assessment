import Link from "next/link";
import { notFound } from "next/navigation";
import { getCountries, getCountry } from "@/lib/data";
import { tier as tierOf, tierColor, clamp01, SHAPE_BALANCED, SHAPE_LOPSIDED, DURABILITY_TOL } from "@/lib/config";
import Radar from "@/components/Radar";
import ChipRow from "@/components/ChipRow";

export function generateStaticParams() {
  return getCountries().map((c) => ({ slug: c.slug }));
}

const fmtKey = (k: string) =>
  k.replace(/_/g, " ").replace(/\bpct\b/g, "%").replace(/\bgdp\b/gi, "GDP").replace(/\boda\b/gi, "ODA");

function RelStat({
  label,
  value,
  band,
  hint,
  invert = false,
}: {
  label: string;
  value: number | null;
  band: string;
  hint: string;
  invert?: boolean;
}) {
  const palette = invert
    ? { high: "#f87171", moderate: "#fbbf24", low: "#4ade80" }
    : { high: "#4ade80", moderate: "#fbbf24", low: "#f87171" };
  const col = palette[band as keyof typeof palette] ?? "#9a9ab0";
  return (
    <div className="rounded-lg border border-border bg-surface2/40 p-3">
      <div className="mono text-[10px] uppercase tracking-wider text-fg3">{label}</div>
      <div className="mt-1 flex items-baseline gap-2">
        <span className="num text-[15px] font-semibold" style={{ color: col }}>
          {value == null ? "—" : value.toFixed(2)}
        </span>
        <span className="text-[12px] capitalize" style={{ color: col }}>
          {band}
        </span>
      </div>
      <div className="mt-1.5 h-1.5 overflow-hidden rounded-full bg-surface2">
        <div className="h-full rounded-full" style={{ width: `${clamp01(value ?? 0) * 100}%`, background: col }} />
      </div>
      <div className="mt-1 text-[11px] text-fg3">{hint}</div>
    </div>
  );
}

export default async function CountryPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const c = getCountry(slug);
  if (!c) notFound();
  const col = tierColor(c.tier);
  const spreadLabel =
    c.spread == null
      ? null
      : c.spread < SHAPE_BALANCED
      ? "Balanced"
      : c.spread < SHAPE_LOPSIDED
      ? "Some imbalance"
      : "Lopsided";

  return (
    <div className="py-10">
      <Link href="/atlas" className="mono text-[11px] text-fg3 hover:text-fg2">
        ← atlas
      </Link>

      {/* Verdict */}
      <div className="mt-3 flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="serif text-3xl font-black sm:text-4xl">{c.name}</h1>
          <p className="mt-2 max-w-xl text-[14px] text-fg2 sm:text-[15px]">{c.verdict}</p>
        </div>
        <div className="text-right">
          <div className="num text-4xl font-bold" style={{ color: col, textShadow: `0 0 24px ${col}55` }}>
            {c.mi.toFixed(3)}
          </div>
          <div className="mono mt-1 text-[11px]" style={{ color: col }}>
            Tier {c.tier} · {tierOf(c.tier).name}
          </div>
        </div>
      </div>

      {/* Fingerprint */}
      <section className="mt-7">
        <h2 className="mono mb-2 text-[11px] uppercase tracking-wider text-fg3">Classifiers</h2>
        <ChipRow chips={c.chips} />
        <p className="mt-2 text-[11px] text-fg3">Tap any classifier for the rule that set it.</p>
      </section>

      <div className="mt-8 grid gap-6 md:grid-cols-2">
        {/* Shape */}
        <section className="card p-5">
          <h2 className="serif text-base">Structural shape</h2>
          <div className="mt-2 flex justify-center">
            <Radar pillars={c.pillars} />
          </div>
          {spreadLabel && (
            <p className="mt-1 text-center text-[12px] text-fg2">
              {spreadLabel}
              {c.spread != null && <span className="mono text-fg3"> · spread {c.spread.toFixed(2)}</span>}
            </p>
          )}
        </section>

        {/* Configuration */}
        <section className="card p-5">
          <h2 className="serif text-base">Configuration</h2>
          <p className="mt-1 text-[12px] text-fg3">Pillars ranked strongest → weakest.</p>
          <div className="mt-3 space-y-2.5">
            {c.config.map(([p, v]) => (
              <div key={p} className="flex items-center gap-3">
                <span className="mono w-7 text-[12px] font-semibold">{p}</span>
                <span className="w-32 text-[12px] text-fg2">{c.pillar_names[p]}</span>
                <div className="h-2 flex-1 overflow-hidden rounded-full bg-surface2">
                  <div className="h-full rounded-full" style={{ width: `${clamp01(v) * 100}%`, background: col }} />
                </div>
                <span className="num w-10 text-right text-[12px]">{v.toFixed(2)}</span>
              </div>
            ))}
          </div>
          {c.residual != null && (
            <div className="mt-4 border-t border-border pt-3 text-[12px] text-fg2">
              <span className="text-fg3">Durability gap: </span>
              {c.residual < -DURABILITY_TOL ? (
                <span className="text-danger">
                  prosperity outruns institutions ({c.residual.toFixed(2)}) — granted, historically fragile
                </span>
              ) : c.residual > DURABILITY_TOL ? (
                <span className="text-good">
                  institutions exceed income ({c.residual.toFixed(2)}) — earned, durable
                </span>
              ) : (
                <span>prosperity in line with institutions ({c.residual.toFixed(2)})</span>
              )}
            </div>
          )}
        </section>
      </div>

      {/* Neighborhood (relational tier) */}
      <section className="card mt-6 p-5">
        <div className="flex flex-wrap items-baseline justify-between gap-2">
          <h2 className="serif text-base">The neighborhood</h2>
          {c.relational && (
            <span className="mono text-[11px] text-fg3">
              historical snapshot · {c.relational.year} · {c.relational.tier} tier
            </span>
          )}
        </div>
        {c.relational ? (
          <div className="mt-3">
            <div className="grid gap-3 sm:grid-cols-3">
              <RelStat
                label="Exposure"
                value={c.relational.exposure_structural}
                band={c.relational.exposure_structural_band}
                invert
                hint="raw external adversity"
              />
              <div className="rounded-lg border border-border bg-surface2/40 p-3">
                <div className="mono text-[10px] uppercase tracking-wider text-fg3">Patron shield</div>
                <div
                  className="mt-1 text-[15px] font-semibold"
                  style={{ color: c.relational.patron_present ? "#60a5fa" : "#f87171" }}
                >
                  {c.relational.patron_present ? "Shielded" : "Standing alone"}
                </div>
                <div className="mt-0.5 text-[11px] text-fg3">credible external defender</div>
              </div>
              <RelStat
                label="Response"
                value={c.relational.response}
                band={c.relational.response_band}
                hint="capacity to absorb a shock"
              />
            </div>
            <p className="mt-4 rounded-lg border border-border bg-surface2/40 p-3 text-[13px] leading-relaxed text-fg">
              {c.relational.joint_reading}
            </p>
            <p className="mt-2 text-[12px] text-fg3">
              <span className="text-fg2">Outcome:</span> {c.relational.outcome_factual}
            </p>
          </div>
        ) : (
          <>
            <p className="mt-2 max-w-2xl text-[13px] text-fg2">
              The relational layer — exposure to stronger neighbors, contested borders, and whether a
              patron would actually show up — is built from a separate set of sources (alliances,
              relative military power, territorial disputes).{" "}
              <span className="text-fg3">
                It isn&apos;t yet computed for {c.name}. Where it exists, it&apos;s the difference between
                a weak state that survives and one that gets swallowed.
              </span>
            </p>
            <Link href="/how-it-works" className="link mt-2 inline-block text-[12px]">
              How the relational layer works →
            </Link>
          </>
        )}
      </section>

      {/* Data & gaps */}
      <section className="card mt-6 p-5">
        <div className="flex items-baseline justify-between">
          <h2 className="serif text-base">The data — and what&apos;s missing</h2>
          <span className="mono text-[11px] text-fg3">vintage {c.data_year}</span>
        </div>
        <div className="mt-1 text-[12px] text-fg2">
          <span className="num font-semibold text-fg">{c.coverage.present}/5</span> pillars covered
          {c.coverage.missing.length > 0 && (
            <span className="text-warn">
              {" "}
              · missing: {c.coverage.missing.map((p) => c.pillar_names[p]).join(", ")}
            </span>
          )}
        </div>
        <div className="mt-3 grid gap-x-6 gap-y-1 sm:grid-cols-2">
          {c.indicators.map((ind) => (
            <div key={ind.key} className="flex items-baseline justify-between border-b border-border/60 py-1 text-[12px]">
              <span className="text-fg2">{fmtKey(ind.key)}</span>
              <span className="mono text-fg3">
                <span className="text-fg">{typeof ind.value === "number" ? ind.value.toFixed(1) : ind.value}</span> · {ind.source}
              </span>
            </div>
          ))}
        </div>
        <p className="mt-3 text-[11px] text-fg3">
          Every value is a citable public figure. The score is a fixed formula over these inputs —{" "}
          <Link href="/how-it-works" className="link">
            run it yourself
          </Link>
          .
        </p>
      </section>
    </div>
  );
}
