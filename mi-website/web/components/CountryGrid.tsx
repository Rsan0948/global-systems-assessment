"use client";
import { useMemo, useState } from "react";
import Link from "next/link";
import type { Summary } from "@/lib/data";
import { PILLAR_ORDER, SCORE_BANDS, scoreBandColor, clamp01, NODATA, TRACK } from "@/lib/config";

const FLAG_LABEL: Record<string, string> = {
  durability: "granted",
  resource: "resource",
  aid: "aid",
};

function Tile({ c }: { c: Summary }) {
  const col = scoreBandColor(c.tier);
  const flags = c.chips.filter((ch) => FLAG_LABEL[ch.key] && (ch.valence === "warn" || ch.valence === "bad"));
  return (
    <Link href={`/country/${c.slug}`} className="card lift group flex flex-col gap-2 p-3">
      <div className="flex items-start justify-between gap-2">
        <span className="text-[13px] font-medium leading-tight group-hover:text-white">{c.name}</span>
        <span className="num text-[13px] font-semibold" style={{ color: col }}>
          {c.mi.toFixed(2)}
        </span>
      </div>
      <div className="flex items-end gap-[3px]" style={{ height: 22 }}>
        {PILLAR_ORDER.map((p) => {
          const v = c.pillars[p];
          return (
            <div key={p} className="flex flex-1 items-end rounded-sm" style={{ background: TRACK, height: "100%" }}>
              <div
                style={{
                  width: "100%",
                  background:
                    v == null
                      ? `repeating-linear-gradient(45deg,${NODATA},${NODATA} 2px,transparent 2px,transparent 4px)`
                      : col + "cc",
                  height: v == null ? "100%" : `${Math.max(6, clamp01(v) * 100)}%`,
                  borderRadius: 2,
                }}
              />
            </div>
          );
        })}
      </div>
      <div className="mono flex flex-wrap items-center gap-x-1.5 gap-y-1 text-[10px] text-fg3">
        <span style={{ color: col }}>● Band {c.tier}</span>
        {c.coverage.present < 5 && <span>· {c.coverage.present}/5 data</span>}
        {flags.map((f) => {
          const fc = f.valence === "bad" ? "#f87171" : "#fbbf24";
          return (
            <span
              key={f.key}
              title={f.label}
              className="rounded px-1 py-px text-[9px] font-medium"
              style={{ background: fc + "1f", color: fc }}
            >
              {FLAG_LABEL[f.key]}
            </span>
          );
        })}
      </div>
    </Link>
  );
}

export default function CountryGrid({ countries }: { countries: Summary[] }) {
  const [q, setQ] = useState("");
  const [band, setBand] = useState(0);
  const [fullOnly, setFullOnly] = useState(false);
  const filtered = useMemo(
    () =>
      countries.filter(
        (c) =>
          (band === 0 || c.tier === band) &&
          (!fullOnly || c.coverage.present === 5) &&
          c.name.toLowerCase().includes(q.toLowerCase())
      ),
    [countries, q, band, fullOnly]
  );
  return (
    <div>
      <div className="mb-4 flex flex-wrap items-center gap-2">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Search any country…"
          aria-label="Search countries"
          className="w-full min-w-0 flex-1 rounded-md border border-border bg-surface px-3 py-1.5 text-[13px] outline-none placeholder:text-fg3 focus:border-primary sm:w-52 sm:flex-none"
        />
        <div className="flex gap-1">
          <button
            onClick={() => setBand(0)}
            className="rounded px-2 py-1 text-[11px] transition-colors"
            style={{
              background: band === 0 ? "#232338" : "transparent",
              color: "#9a9ab0",
              border: `1px solid ${band === 0 ? "#3a3a52" : "transparent"}`,
            }}
          >
            All
          </button>
          {SCORE_BANDS.map((scoreBand) => (
            <button
              key={scoreBand.n}
              onClick={() => setBand(scoreBand.n)}
              className="rounded px-2 py-1 text-[11px] transition-colors"
              style={{
                background: band === scoreBand.n ? scoreBand.color + "22" : "transparent",
                color: scoreBand.color,
                border: `1px solid ${band === scoreBand.n ? scoreBand.color + "66" : "transparent"}`,
              }}
            >
              B{scoreBand.n}
            </button>
          ))}
        </div>
        <button
          onClick={() => setFullOnly((v) => !v)}
          className="mono rounded px-2 py-1 text-[11px] transition-colors"
          style={{
            background: fullOnly ? "#3b82f622" : "transparent",
            color: fullOnly ? "#60a5fa" : "#8a8aa4",
            border: `1px solid ${fullOnly ? "#3b82f655" : "#232338"}`,
          }}
          title="Only countries measured on all five pillars are directly comparable"
        >
          Full data 5/5
        </button>
        <span className="mono ml-auto text-[11px] text-fg3">{filtered.length} shown</span>
      </div>
      {filtered.length === 0 ? (
        <p className="py-12 text-center text-[13px] text-fg3">No countries match. Try a different filter.</p>
      ) : (
        <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
          {filtered.map((c) => (
            <Tile key={c.slug} c={c} />
          ))}
        </div>
      )}
    </div>
  );
}
