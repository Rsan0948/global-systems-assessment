"use client";
import { useMemo, useState } from "react";
import { PILLAR_ORDER, PILLARS, TIERS, tier as tierOf, tierColor, clamp01 } from "@/lib/config";
import Radar from "@/components/Radar";
import Define from "@/components/Define";

type Vals = Record<string, number>;
const tierFromMi = (mi: number) => TIERS.find((t) => mi >= t.min)?.n ?? 5;

export default function WhatIf({
  name,
  pillars,
  actualMi,
}: {
  name: string;
  pillars: Record<string, number | null>;
  actualMi: number;
}) {
  const present = PILLAR_ORDER.filter((p) => pillars[p] != null) as string[];
  const base: Vals = Object.fromEntries(present.map((p) => [p, pillars[p] as number]));

  const [vals, setVals] = useState<Vals>(base);
  const [weights, setWeights] = useState<Vals>(Object.fromEntries(present.map((p) => [p, 1])));
  const [showWeights, setShowWeights] = useState(false);

  const wsum = present.reduce((s, p) => s + weights[p], 0);
  const mi = useMemo(
    () => (wsum > 0 ? present.reduce((s, p) => s + weights[p] * vals[p], 0) / wsum : 0),
    [vals, weights, wsum, present]
  );
  const tnum = tierFromMi(mi);
  const col = tierColor(tnum);
  const dirty =
    present.some((p) => Math.abs(vals[p] - base[p]) > 0.001) ||
    present.some((p) => Math.abs(weights[p] - 1) > 0.001);
  const delta = mi - actualMi;

  const reset = () => {
    setVals(base);
    setWeights(Object.fromEntries(present.map((p) => [p, 1])));
  };

  const radarPillars: Record<string, number | null> = Object.fromEntries(
    PILLAR_ORDER.map((p) => [p, present.includes(p) ? clamp01(vals[p]) : null])
  );

  return (
    <section className="card mt-6 p-5">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 className="serif text-base">Run the engine yourself</h2>
          <p className="mt-1 max-w-md text-[12px] leading-relaxed text-fg3">
            Drag the pillars - or re-weight them - and watch the Modernization Index and tier recompute live. This
            is the real aggregation (an equal-weighted mean of the five pillars), not an animation.
          </p>
        </div>
        <div className="text-right">
          <div className="num text-3xl font-bold" style={{ color: col, textShadow: `0 0 22px ${col}44` }}>
            {mi.toFixed(3)}
          </div>
          <div className="mono text-[11px]" style={{ color: col }}>
            Tier {tnum} · {tierOf(tnum).name}
          </div>
          <div className="mono mt-0.5 text-[10px] text-fg3">
            {dirty ? (
              <span style={{ color: delta >= 0 ? "#4ade80" : "#f87171" }}>
                {delta >= 0 ? "+" : ""}
                {delta.toFixed(3)} vs actual
              </span>
            ) : (
              "= the published score"
            )}
          </div>
        </div>
      </div>

      <div className="mt-4 flex flex-col items-center gap-5 sm:flex-row sm:items-start">
        <div className="shrink-0">
          <Radar pillars={radarPillars} colors={[col, "#f472b6"]} />
        </div>

        <div className="w-full flex-1">
          <div className="space-y-3">
            {present.map((p) => (
              <div key={p}>
                <div className="flex items-baseline justify-between text-[12px]">
                  <span className="text-fg2">
                    <Define id={p.toLowerCase()}>{PILLARS[p].full}</Define>
                  </span>
                  <span className="num text-fg3">{vals[p].toFixed(2)}</span>
                </div>
                <input
                  type="range"
                  min={0}
                  max={1}
                  step={0.01}
                  value={vals[p]}
                  onChange={(e) => setVals((v) => ({ ...v, [p]: parseFloat(e.target.value) }))}
                  aria-label={`${PILLARS[p].full} value`}
                  className="mt-1 w-full accent-current"
                  style={{ color: col }}
                />
              </div>
            ))}
          </div>

          <button
            type="button"
            onClick={() => setShowWeights((s) => !s)}
            className="mono mt-4 text-[11px] text-fg3 hover:text-fg2"
            aria-expanded={showWeights}
          >
            {showWeights ? "− hide weights" : "+ adjust pillar weights"} (what if institutions mattered more?)
          </button>

          {showWeights && (
            <div className="mt-3 space-y-2 border-t border-border pt-3">
              {present.map((p) => (
                <div key={p} className="flex items-center gap-3">
                  <span className="mono w-16 shrink-0 text-[11px] text-fg3">{PILLARS[p].short}</span>
                  <input
                    type="range"
                    min={0}
                    max={3}
                    step={0.1}
                    value={weights[p]}
                    onChange={(e) => setWeights((w) => ({ ...w, [p]: parseFloat(e.target.value) }))}
                    aria-label={`${PILLARS[p].full} weight`}
                    className="w-full accent-current"
                    style={{ color: "#a78bfa" }}
                  />
                  <span className="num w-10 shrink-0 text-right text-[11px] text-fg3">
                    {wsum > 0 ? Math.round((weights[p] / wsum) * 100) : 0}%
                  </span>
                </div>
              ))}
            </div>
          )}

          {dirty && (
            <button
              type="button"
              onClick={reset}
              className="mt-4 rounded-md border border-border px-3 py-1.5 text-[12px] text-fg2 transition-colors hover:bg-surface2"
            >
              Reset to {name}&apos;s actual profile ↺
            </button>
          )}
        </div>
      </div>

      <p className="mt-4 text-[11px] leading-relaxed text-fg3">
        Honest scope: you&apos;re re-weighting and nudging the <em>published pillars</em>, not re-deriving them from
        raw indicators (the normalization lives in the engine). The durability gate, safeguards, and diagnostics
        above are computed by the Python engine and don&apos;t move here.
      </p>
    </section>
  );
}
