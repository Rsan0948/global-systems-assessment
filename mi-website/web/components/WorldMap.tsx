"use client";
import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import type { MapFeature, Summary } from "@/lib/types";
import { MAP_W, MAP_H, COVERAGE_SCORED, COVERAGE_UNSCORED } from "@/lib/config";
import { ScoreBandLegend } from "@/components/ui";

type Layer = "structure" | "coverage";
const TOOLTIP_W = 220;

export default function WorldMap({
  features,
  sphere,
  countries,
}: {
  features: MapFeature[];
  sphere: string;
  countries: Summary[];
}) {
  const router = useRouter();
  const [hover, setHover] = useState<MapFeature | null>(null);
  // Pinned selection is the touch-friendly two-step model: first tap pins a
  // readout, a second tap (or the "View →" affordance) navigates. Kept in React
  // state (unlike hover position, which is written to the DOM via `tip`).
  const [pinned, setPinned] = useState<MapFeature | null>(null);
  const [layer, setLayer] = useState<Layer>("structure");
  const wrap = useRef<HTMLDivElement>(null);
  const tip = useRef<HTMLDivElement>(null);

  const open = (f: MapFeature) => f.slug && router.push(`/country/${f.slug}`);

  // On a device with a real hover (desktop mouse), the tooltip already previews
  // the country, so a click navigates directly - no pin-first step. The two-step
  // pin→confirm model is only for touch (no hover), where there is no tooltip.
  const tapCountry = (f: MapFeature) => {
    const hoverCapable =
      typeof window !== "undefined" &&
      typeof window.matchMedia === "function" &&
      window.matchMedia("(hover: hover)").matches;
    if (hoverCapable) {
      open(f);
      return;
    }
    if (pinned?.iso3 === f.iso3) {
      open(f);
    } else {
      setPinned(f);
    }
  };

  const fill = (f: MapFeature) =>
    layer === "coverage" ? (f.slug ? COVERAGE_SCORED : COVERAGE_UNSCORED) : f.color;

  // Position the tooltip by writing to the DOM directly - NO React state on mouse
  // move, so moving the cursor never re-renders the ~180 map paths.
  const moveTip = (e: React.MouseEvent) => {
    const r = wrap.current?.getBoundingClientRect();
    const t = tip.current;
    if (!r || !t) return;
    const x = e.clientX - r.left;
    const y = e.clientY - r.top;
    const left = x + 14 + TOOLTIP_W > r.width ? x - TOOLTIP_W - 14 : x + 14;
    t.style.left = `${Math.max(4, left)}px`;
    t.style.top = `${Math.max(4, Math.min(y + 14, r.height - 66))}px`;
  };

  return (
    <div className="relative">
      <div className="absolute right-0 top-0 z-10 flex gap-1 text-[11px]">
        {(["structure", "coverage"] as Layer[]).map((l) => (
          <button
            key={l}
            onClick={() => setLayer(l)}
            aria-pressed={layer === l}
            className="mono rounded px-2 py-1 capitalize transition-colors"
            style={{
              background: layer === l ? "#3b82f622" : "transparent",
              color: layer === l ? "#60a5fa" : "#8a8aa4",
              border: `1px solid ${layer === l ? "#3b82f655" : "#232338"}`,
            }}
          >
            {l}
          </button>
        ))}
      </div>

      <div ref={wrap} className="relative" onMouseMove={moveTip} onMouseLeave={() => setHover(null)}>
        <div
          aria-hidden
          className="pointer-events-none absolute left-1/2 top-1/2 h-[80%] w-[70%] -translate-x-1/2 -translate-y-1/2 rounded-full opacity-40 blur-3xl"
          style={{ background: "radial-gradient(ellipse at center, #1e3a8a55, transparent 70%)" }}
        />
        <svg
          viewBox={`0 0 ${MAP_W} ${MAP_H}`}
          className="relative w-full"
          style={{ filter: "drop-shadow(0 8px 24px #00000066)" }}
          role="img"
          aria-label="World map of Modernization Index score bands. Browse and select any country in the keyboard-accessible list below."
        >
          <defs>
            <radialGradient id="ocean" cx="50%" cy="42%" r="75%">
              <stop offset="0%" stopColor="#10131f" />
              <stop offset="100%" stopColor="#0b0d16" />
            </radialGradient>
          </defs>
          <path
            d={sphere}
            fill="url(#ocean)"
            stroke="#232338"
            strokeWidth={0.8}
            onMouseEnter={() => setHover(null)}
            onClick={() => setPinned(null)}
          />
          {features.map((f, i) => {
            const on = hover === f || pinned?.iso3 === f.iso3;
            return (
              <path
                key={`${f.iso3}-${i}`}
                d={f.d}
                fill={fill(f)}
                stroke={on ? "#e6e6ee" : "#0a0a14"}
                strokeWidth={on ? 1.1 : 0.4}
                aria-hidden
                style={{ cursor: f.slug ? "pointer" : "default" }}
                onMouseEnter={() => setHover(f)}
                onClick={() => tapCountry(f)}
              />
            );
          })}
        </svg>

        {/* tooltip: always mounted, positioned via ref, shown only while hovering */}
        <div
          ref={tip}
          className="pointer-events-none absolute z-20 rounded-lg border border-border bg-surface/95 px-3 py-2 backdrop-blur"
          style={{ width: TOOLTIP_W, display: hover ? "block" : "none", boxShadow: "0 10px 30px #000000aa" }}
        >
          {hover && (
            <>
              <div className="text-[13px] font-medium">{hover.name}</div>
              {hover.slug ? (
                <div className="mono mt-0.5 text-[11px]">
                  <span style={{ color: layer === "coverage" ? "#a6a6bd" : hover.color }}>
                    MI {hover.mi?.toFixed(3)} · Band {hover.tier}
                  </span>
                  <span className="text-fg3"> · click to open</span>
                </div>
              ) : (
                <div className="mono mt-0.5 text-[11px] text-fg3">not yet scored</div>
              )}
            </>
          )}
        </div>
      </div>

      {/* Pinned readout: always-visible (no pointer needed), highlights the
          selected country and offers a tap target to open it. */}
      {pinned && (
        <div
          role="status"
          aria-live="polite"
          className="mt-3 flex items-center gap-3 rounded-lg border border-border bg-surface/95 px-3 py-2"
        >
          <div className="min-w-0 flex-1">
            <div className="truncate text-[13px] font-medium">{pinned.name}</div>
            {pinned.slug ? (
              <div className="mono mt-0.5 text-[11px]">
                <span style={{ color: layer === "coverage" ? "#a6a6bd" : pinned.color }}>
                  MI {pinned.mi?.toFixed(3)} · Band {pinned.tier}
                </span>
              </div>
            ) : (
              <div className="mono mt-0.5 text-[11px] text-fg3">not yet scored</div>
            )}
          </div>
          {pinned.slug && (
            <button
              onClick={() => open(pinned)}
              className="mono shrink-0 rounded px-2.5 py-1.5 text-[12px] transition-colors"
              style={{ background: "#3b82f622", color: "#60a5fa", border: "1px solid #3b82f655" }}
            >
              View →
            </button>
          )}
          <button
            onClick={() => setPinned(null)}
            aria-label="Dismiss selection"
            className="mono shrink-0 rounded px-2 py-1.5 text-[12px] text-fg3 transition-colors hover:text-fg"
          >
            ✕
          </button>
        </div>
      )}

      <div className="mt-3">
        {layer === "structure" ? (
          <ScoreBandLegend countries={countries} />
        ) : (
          <p className="mono flex flex-wrap items-center gap-x-1.5 gap-y-1 text-[11px] text-fg3">
            <span
              className="inline-block h-2.5 w-2.5 rounded-[2px] border border-border align-middle"
              style={{ background: COVERAGE_SCORED }}
            />
            scored ·
            <span
              className="inline-block h-2.5 w-2.5 rounded-[2px] border border-border align-middle"
              style={{ background: COVERAGE_UNSCORED }}
            />
            not yet measured - roughly half the world is dark, missing the public data the engine needs.
          </p>
        )}
      </div>
    </div>
  );
}
