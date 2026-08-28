import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getCountries, getCountry } from "@/lib/data";
import { scoreBand, scoreBandColor, clamp01, SHAPE_BALANCED, SHAPE_LOPSIDED } from "@/lib/config";
import Radar from "@/components/Radar";
import ChipRow from "@/components/ChipRow";
import Define from "@/components/Define";
import IndicatorRow from "@/components/IndicatorRow";
import SafeguardBoard from "@/components/SafeguardBoard";
import Diagnostics from "@/components/Diagnostics";
import WhatIf from "@/components/WhatIf";
import { ScoreBandDot } from "@/components/ui";

export const dynamicParams = false; // 190 country pages are fully known at build; no on-demand slugs

export function generateStaticParams() {
  return getCountries().map((c) => ({ slug: c.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const country = getCountry(slug);

  if (!country) return {};

  return {
    title: country.name,
    description: `${country.name} Modernization Index profile, including its overall score, five pillars, data coverage, and structural diagnostics.`,
    alternates: { canonical: `/country/${slug}` },
  };
}

function RelStat({
  label,
  value,
  band,
  hint,
  invert = false,
  defId,
}: {
  label: string;
  value: number | null;
  band: string;
  hint: string;
  invert?: boolean;
  defId?: string;
}) {
  const palette = invert
    ? { high: "#f87171", moderate: "#fbbf24", low: "#4ade80" }
    : { high: "#4ade80", moderate: "#fbbf24", low: "#f87171" };
  const col = palette[band as keyof typeof palette] ?? "#9a9ab0";
  return (
    <div className="rounded-lg border border-border bg-surface2/40 p-3">
      <div className="mono text-[10px] uppercase tracking-wider text-fg3">
        {defId ? <Define id={defId}>{label}</Define> : label}
      </div>
      <div className="mt-1 flex items-baseline gap-2">
        <span className="num text-[15px] font-semibold" style={{ color: col }}>
          {value == null ? "n/a" : value.toFixed(2)}
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
  const col = scoreBandColor(c.tier);
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
        ← Country atlas
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
            Band {c.tier} · {scoreBand(c.tier).name}
          </div>
          <div className="mono mt-1 text-[10px] text-fg3">
            <Define id="mi">what is this score?</Define>
          </div>
        </div>
      </div>

      {/* Fingerprint */}
      <section className="mt-7">
        <h2 className="mono mb-2 text-[11px] uppercase tracking-wider text-fg3">What stands out</h2>
        <ChipRow chips={c.chips} />
        <p className="mt-2 text-[11px] text-fg3">Select any label for its definition and scoring rule.</p>
      </section>

      {/* Structural shape */}
      <section className="card mt-8 p-5">
        <div className="flex flex-col items-center gap-5 sm:flex-row sm:items-center">
          <div className="shrink-0">
            <Radar pillars={c.pillars} />
          </div>
          <div className="text-[13px] leading-relaxed text-fg2">
            <h2 className="serif text-base text-fg">Structural shape</h2>
            <p className="mt-1.5">
              Each spoke shows one pillar, with 0 at the center and 1 at the edge. The shape reveals
              whether the pillars are similar or whether one is much lower than the others. That
              difference is called the <Define id="shape">pillar spread</Define>.
            </p>
            {spreadLabel && (
              <p className="mono mt-2 text-[11px] text-fg3">
                Read as <span className="text-fg2">{spreadLabel}</span>
                {c.spread != null && <> · spread {c.spread.toFixed(2)}</>}
              </p>
            )}
          </div>
        </div>
      </section>

      {/* Safeguard board - the case-study engine, run on this country */}
      {c.safeguards && c.safeguards.length > 0 && <SafeguardBoard safeguards={c.safeguards} />}

      {/* Engine diagnostics - strategy, vulnerability, trajectory, robustness */}
      {c.diagnostics && <Diagnostics d={c.diagnostics} />}

      {/* Genuine interactivity: recompute the score yourself */}
      <WhatIf name={c.name} pillars={c.pillars} actualMi={c.mi} />

      {/* Neighborhood (relational tier) - only where we have it */}
      {c.relational && (
        <section className="card mt-6 p-5">
          <div className="flex flex-wrap items-baseline justify-between gap-2">
            <h2 className="serif text-base">External security context</h2>
            <span className="mono text-[11px] text-fg3">reviewed for {c.relational.year}</span>
          </div>
          <div className="mt-3 grid gap-3 sm:grid-cols-3">
            <RelStat
              label="Exposure"
              defId="exposure"
              value={c.relational.exposure_structural}
              band={c.relational.exposure_structural_band}
              invert
              hint="threats from outside the country"
            />
            <div className="rounded-lg border border-border bg-surface2/40 p-3">
              <div className="mono text-[10px] uppercase tracking-wider text-fg3">
                <Define id="protection">Protection</Define>
              </div>
              <div
                className="mt-1 text-[15px] font-semibold"
                style={{ color: c.relational.patron_present ? "#60a5fa" : "#f87171" }}
              >
                {c.relational.patron_present ? "Protected by an ally" : "No major ally identified"}
              </div>
              <div className="mt-0.5 text-[11px] text-fg3">whether a credible ally was expected to defend it</div>
            </div>
            <RelStat
              label="Response"
              defId="response"
              value={c.relational.response}
              band={c.relational.response_band}
              hint="capacity to respond after an external shock"
            />
          </div>
          <p className="mt-4 rounded-lg border border-border bg-surface2/40 p-3 text-[13px] leading-relaxed text-fg">
            {c.relational.joint_reading}
          </p>
          <p className="mt-2 text-[12px] text-fg3">
            <span className="text-fg2">What happened:</span> {c.relational.outcome_factual}
          </p>
        </section>
      )}

      {/* The underlying indicators */}
      <section className="card mt-6 p-5">
        <div className="flex items-baseline justify-between">
          <h2 className="serif text-base">The indicators behind the score</h2>
          <span className="mono text-[11px] text-fg3">
            {c.coverage.present}/5 pillars · {c.data_year}
          </span>
        </div>
        {c.coverage.missing.length > 0 && (
          <p className="mt-1 text-[12px] text-warn">
            Not measured: {c.coverage.missing.map((p) => c.pillar_names[p]).join(", ")}
          </p>
        )}
        <div className="mt-3 grid gap-x-8 gap-y-0 sm:grid-cols-2">
          {c.indicators.map((ind) => (
            <IndicatorRow key={ind.key} ind={ind} />
          ))}
        </div>
        <p className="mt-3 text-[11px] text-fg3">Select an indicator to see what it measures and where it comes from.</p>
      </section>

      {/* Structurally similar countries */}
      {c.similar && c.similar.length > 0 && (
        <section className="card mt-6 p-5">
          <h2 className="serif text-base">Countries with similar pillar profiles</h2>
          <p className="mt-1 text-[12px] text-fg3">
            These countries have the closest five-pillar pattern to {c.name}. Similarity does not mean
            that their politics or histories are the same.
          </p>
          <div className="mt-3 flex flex-wrap gap-2">
            {c.similar.map((s) => (
              <Link
                key={s.slug}
                href={`/compare?a=${c.slug}&b=${s.slug}`}
                className="lift flex items-center gap-2 rounded-lg border border-border bg-surface2/40 px-3 py-2 text-[13px]"
              >
                <ScoreBandDot band={s.tier} size={7} />
                <span className="font-medium">{s.name}</span>
                <span className="num text-[12px]" style={{ color: scoreBandColor(s.tier) }}>
                  {s.mi.toFixed(2)}
                </span>
              </Link>
            ))}
          </div>
          <Link href={`/compare?a=${c.slug}`} className="link mt-3 inline-block text-[12px]">
            Compare {c.name} head-to-head with any country →
          </Link>
        </section>
      )}
    </div>
  );
}
