import { TIERS, tierColor } from "@/lib/config";
import type { Summary } from "@/lib/data";

// Reusable primitives — one definition, used everywhere. Keeps the site consistent.

export function Card({ className = "", children }: { className?: string; children: React.ReactNode }) {
  return <div className={`card ${className}`}>{children}</div>;
}

export function TierDot({ tier, size = 8 }: { tier: number; size?: number }) {
  const col = tierColor(tier);
  return (
    <span
      aria-hidden
      style={{ background: col, width: size, height: size, boxShadow: `0 0 ${size}px ${col}88` }}
      className="inline-block shrink-0 rounded-full"
    />
  );
}

export function PageHeader({ title, lede }: { title: string; lede?: string }) {
  return (
    <header className="mb-6">
      <h1 className="serif text-3xl font-black sm:text-4xl">{title}</h1>
      {lede && <p className="mt-3 max-w-2xl text-[14px] leading-relaxed text-fg2">{lede}</p>}
    </header>
  );
}

export function TierDistribution({ countries }: { countries: Summary[] }) {
  const total = countries.length;
  return (
    <div className="flex h-2 w-full overflow-hidden rounded-full" title="Distribution of scored countries by tier">
      {TIERS.map((t) => {
        const n = countries.filter((c) => c.tier === t.n).length;
        const pct = total ? (n / total) * 100 : 0;
        return pct > 0 ? <div key={t.n} style={{ width: `${pct}%`, background: t.color }} /> : null;
      })}
    </div>
  );
}

export function TierLegend({ countries }: { countries?: Summary[] }) {
  return (
    <div className="flex flex-wrap items-center gap-x-4 gap-y-1.5">
      {TIERS.map((t) => {
        const n = countries?.filter((c) => c.tier === t.n).length;
        return (
          <span key={t.n} className="mono flex items-center gap-1.5 text-[11px] text-fg3">
            <TierDot tier={t.n} size={7} /> T{t.n} {t.short}
            {n != null && <span className="text-fg2">{n}</span>}
          </span>
        );
      })}
    </div>
  );
}
