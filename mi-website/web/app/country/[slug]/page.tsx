import Link from "next/link";
import { notFound } from "next/navigation";
import { getCountries, getCountry } from "@/lib/data";
import { tier as tierOf, tierColor, clamp01, SHAPE_BALANCED, SHAPE_LOPSIDED, DURABILITY_TOL } from "@/lib/config";
import Radar from "@/components/Radar";
import ChipRow from "@/components/ChipRow";
import Define from "@/components/Define";

export function generateStaticParams() {
  return getCountries().map((c) => ({ slug: c.slug }));
}

const INDICATOR_LABELS: Record<string, string> = {
  gov_effectiveness: "Government effectiveness",
  rule_of_law: "Rule of law",
  regulatory_quality: "Regulatory quality",
  control_of_corruption: "Control of corruption",
  voice_accountability: "Voice & accountability",
  political_stability: "Political stability",
  cpi: "Corruption Perceptions Index",
  gii: "Global Innovation Index",
  rd_pct_gdp: "R&D spending (% of GDP)",
  eci: "Economic Complexity Index",
  education_index: "Education index",
  life_expectancy_index: "Life expectancy index",
  gdp_per_capita_ppp: "GDP per capita (PPP)",
  resource_rents_pct_gdp: "Resource rents (% of GDP)",
  oda_pct_gni: "Aid received (% of GNI)",
  fsi: "Fragile States Index",
};
const labelFor = (k: string) => INDICATOR_LABELS[k] ?? k.replace(/_/g, " ");
const fmtVal = (v: number) =>
  v >= 1000 ? Math.round(v).toLocaleString() : Number.isInteger(v) ? String(v) : v.toFixed(1);

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
          {value == null ? "-" : value.toFixed(2)}
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
          <div className="mono mt-1 text-[10px] text-fg3">
            <Define id="mi">what is this score?</Define>
          </div>
        </div>
      </div>

      {/* Fingerprint */}
      <section className="mt-7">
        <h2 className="mono mb-2 text-[11px] uppercase tracking-wider text-fg3">What stands out</h2>
        <ChipRow chips={c.chips} />
        <p className="mt-2 text-[11px] text-fg3">Tap any flag to see what it means and why it matters.</p>
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
              <Define id="shape">{spreadLabel}</Define>
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
                <span className="w-32 text-[12px] text-fg2">
                  <Define id={p.toLowerCase()}>{c.pillar_names[p]}</Define>
                </span>
                <div className="h-2 flex-1 overflow-hidden rounded-full bg-surface2">
                  <div className="h-full rounded-full" style={{ width: `${clamp01(v) * 100}%`, background: col }} />
                </div>
                <span className="num w-10 text-right text-[12px]">{v.toFixed(2)}</span>
              </div>
            ))}
          </div>
          {c.residual != null && (
            <div className="mt-4 border-t border-border pt-3 text-[12px] text-fg2">
              <span className="text-fg3">
                <Define id="durability-gap">Durability gap</Define>:{" "}
              </span>
              {c.residual < -DURABILITY_TOL ? (
                <span className="text-danger">
                  prosperity outruns institutions ({c.residual.toFixed(2)}) - granted, historically fragile
                </span>
              ) : c.residual > DURABILITY_TOL ? (
                <span className="text-good">
                  institutions exceed income ({c.residual.toFixed(2)}) - earned, durable
                </span>
              ) : (
                <span>prosperity in line with institutions ({c.residual.toFixed(2)})</span>
              )}
            </div>
          )}
        </section>
      </div>

      {/* Neighborhood (relational tier) — only where we have it */}
      {c.relational && (
        <section className="card mt-6 p-5">
          <div className="flex flex-wrap items-baseline justify-between gap-2">
            <h2 className="serif text-base">The neighborhood</h2>
            <span className="mono text-[11px] text-fg3">how exposure shaped its fate · {c.relational.year}</span>
          </div>
          <div className="mt-3 grid gap-3 sm:grid-cols-3">
            <RelStat
              label="Exposure"
              defId="exposure"
              value={c.relational.exposure_structural}
              band={c.relational.exposure_structural_band}
              invert
              hint="how much external danger it faced"
            />
            <div className="rounded-lg border border-border bg-surface2/40 p-3">
              <div className="mono text-[10px] uppercase tracking-wider text-fg3">
                <Define id="protection">Protection</Define>
              </div>
              <div
                className="mt-1 text-[15px] font-semibold"
                style={{ color: c.relational.patron_present ? "#60a5fa" : "#f87171" }}
              >
                {c.relational.patron_present ? "Shielded" : "Standing alone"}
              </div>
              <div className="mt-0.5 text-[11px] text-fg3">did a powerful ally have its back?</div>
            </div>
            <RelStat
              label="Response"
              defId="response"
              value={c.relational.response}
              band={c.relational.response_band}
              hint="how well it could absorb a hit"
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
            <div
              key={ind.key}
              className="flex items-baseline justify-between gap-3 border-b border-border/50 py-1.5 text-[13px]"
            >
              <span className="text-fg2">{labelFor(ind.key)}</span>
              <span className="num font-semibold text-fg">{fmtVal(ind.value)}</span>
            </div>
          ))}
        </div>
        <p className="mt-3 text-[11px] text-fg3">
          Sources: {Array.from(new Set(c.indicators.map((i) => i.source))).join(", ")}.
        </p>
      </section>
    </div>
  );
}
