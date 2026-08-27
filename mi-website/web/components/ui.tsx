import { SCORE_BANDS, scoreBandColor } from "@/lib/config";
import type { Summary } from "@/lib/data";

// Reusable primitives - one definition, used everywhere. Keeps the site consistent.

export function Card({ className = "", children }: { className?: string; children: React.ReactNode }) {
  return <div className={`card ${className}`}>{children}</div>;
}

export function ScoreBandDot({ band, size = 8 }: { band: number; size?: number }) {
  const col = scoreBandColor(band);
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

export function ScoreBandDistribution({ countries }: { countries: Summary[] }) {
  const total = countries.length;
  return (
    <div className="flex h-2 w-full overflow-hidden rounded-full" title="Distribution of countries by score band">
      {SCORE_BANDS.map((band) => {
        const n = countries.filter((c) => c.tier === band.n).length;
        const pct = total ? (n / total) * 100 : 0;
        return pct > 0 ? <div key={band.n} style={{ width: `${pct}%`, background: band.color }} /> : null;
      })}
    </div>
  );
}

export function ScoreBandLegend({ countries }: { countries?: Summary[] }) {
  return (
    <div>
      <p className="mb-2 text-[11.5px] text-fg2">
        Each country scores 0 to 1. Higher score bands indicate greater structural capacity.
      </p>
      <div className="flex flex-wrap gap-x-5 gap-y-2">
        {SCORE_BANDS.map((band) => {
          const n = countries?.filter((c) => c.tier === band.n).length;
          const range = band.n === 1 ? "0.80+" : `${band.min.toFixed(2)} to ${(band.min + 0.2 - 0.01).toFixed(2)}`;
          return (
            <span key={band.n} className="flex items-center gap-2 text-[12.5px]">
              <span
                aria-hidden
                className="inline-block h-3 w-3 shrink-0 rounded-[3px]"
                style={{ background: band.color, boxShadow: `0 0 8px ${band.color}66` }}
              />
              <span className="font-medium text-fg">Band {band.n}</span>
              <span className="text-fg2">{band.short}</span>
              <span className="mono text-[10.5px] text-fg3">{range}</span>
              {n != null && (
                <span className="num rounded bg-surface2 px-1.5 text-[11px] text-fg2">{n}</span>
              )}
            </span>
          );
        })}
      </div>
    </div>
  );
}
