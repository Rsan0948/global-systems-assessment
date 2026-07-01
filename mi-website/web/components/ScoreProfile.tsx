"use client";
import { useState, useRef, useEffect } from "react";
import { tierColor, clamp01, PILLARS } from "@/lib/config";
import type { Check } from "@/lib/types";
import Define from "@/components/Define";

const C: Record<Check["status"], string> = { flag: "#f87171", info: "#60a5fa", clear: "#4ade80" };
const LBL: Record<Check["status"], string> = { flag: "flagged", info: "noted", clear: "clear" };

export default function ScoreProfile({
  name,
  tier,
  mi,
  config,
  checks,
}: {
  name: string;
  tier: number;
  mi: number;
  config: [string, number][];
  checks: Check[];
}) {
  const [started, setStarted] = useState(false);
  const [revealed, setRevealed] = useState(0);
  const [open, setOpen] = useState<string | null>(null);
  const timers = useRef<number[]>([]);
  const col = tierColor(tier);

  const clearT = () => {
    timers.current.forEach(clearTimeout);
    timers.current = [];
  };
  useEffect(() => clearT, []);

  const run = () => {
    clearT();
    setOpen(null);
    const reduced =
      typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
    if (reduced) {
      setStarted(true);
      setRevealed(checks.length);
      return;
    }
    setStarted(false);
    setRevealed(0);
    timers.current.push(window.setTimeout(() => setStarted(true), 60));
    checks.forEach((_, i) => timers.current.push(window.setTimeout(() => setRevealed(i + 1), 1150 + i * 460)));
  };

  const done = started && revealed >= checks.length;

  return (
    <section className="card mt-6 p-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="serif text-base">Watch the engine grade {name}</h2>
          <p className="mt-1 text-[12px] text-fg3">
            The same deterministic checks a case study runs, live from the five pillars.
          </p>
        </div>
        <button
          onClick={run}
          className="shrink-0 rounded-md border px-3 py-1.5 text-[12px] font-medium transition-colors"
          style={{ borderColor: col + "66", color: col, background: col + "14" }}
        >
          {!started ? "Run the engine ▶" : done ? "Replay ↻" : "running…"}
        </button>
      </div>

      {/* the five pillars build */}
      <div className="mt-5 space-y-2">
        {config.map(([p, v], i) => (
          <div key={p} className="flex items-center gap-3">
            <span className="mono w-7 text-[11px] font-semibold text-fg3">{p}</span>
            <span className="w-28 text-[11px] text-fg2">
              <Define id={p.toLowerCase()}>{PILLARS[p]?.full ?? p}</Define>
            </span>
            <div className="h-2 flex-1 overflow-hidden rounded-full bg-surface2">
              <div
                className="h-full rounded-full"
                style={{
                  width: started ? `${clamp01(v) * 100}%` : "0%",
                  background: col,
                  transition: `width 700ms cubic-bezier(.2,.7,.3,1) ${i * 90}ms`,
                }}
              />
            </div>
            <span
              className="num w-9 text-right text-[11px]"
              style={{ opacity: started ? 1 : 0.25, transition: "opacity .5s" }}
            >
              {v.toFixed(2)}
            </span>
          </div>
        ))}
        <div className="flex items-center gap-3 pt-1">
          <span className="mono w-7 text-[11px] font-semibold" style={{ color: col }}>
            MI
          </span>
          <span className="w-28 text-[11px] font-medium text-fg">Combined score</span>
          <div className="flex-1" />
          <span className="num w-9 text-right text-[13px] font-bold" style={{ color: col, opacity: started ? 1 : 0.25, transition: "opacity .6s" }}>
            {mi.toFixed(2)}
          </span>
        </div>
      </div>

      {/* checks firing */}
      {started && (
        <div className="mt-5 border-t border-border pt-4">
          <p className="mono mb-2.5 text-[10px] uppercase tracking-wider text-fg3">
            {done ? `${checks.length} structural checks` : "running structural checks…"}
          </p>
          <div className="space-y-2">
            {checks.slice(0, revealed).map((c) => (
              <div key={c.key} className="fire-in rounded-lg border border-border bg-surface2/40">
                <button
                  type="button"
                  onClick={() => setOpen(open === c.key ? null : c.key)}
                  aria-expanded={open === c.key}
                  className="flex w-full items-center gap-3 p-3 text-left"
                >
                  <span
                    className={`inline-block h-2.5 w-2.5 shrink-0 rounded-full ${c.status === "flag" ? "pulse-dot" : ""}`}
                    style={{ background: C[c.status], color: C[c.status] }}
                  />
                  <span className="min-w-0 flex-1">
                    <span className="text-[13px] font-medium text-fg">{c.title}</span>
                    <span className="ml-2 text-[12px] text-fg3">{c.headline}</span>
                  </span>
                  <span className="mono shrink-0 text-[10px] uppercase" style={{ color: C[c.status] }}>
                    {LBL[c.status]}
                  </span>
                </button>
                {open === c.key && (
                  <p className="px-3 pb-3 text-[12px] leading-relaxed text-fg2">{c.detail}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {!started && (
        <p className="mt-4 text-center text-[12px] text-fg3">
          {checks.length} structural checks ready. Press run to watch them fire.
        </p>
      )}
    </section>
  );
}
