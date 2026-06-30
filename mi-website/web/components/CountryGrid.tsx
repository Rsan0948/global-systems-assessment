"use client";
import { useMemo, useState } from "react";
import Link from "next/link";
import type { Summary } from "@/lib/data";

const TIER = ["#10b981", "#3b82f6", "#f59e0b", "#fb923c", "#ef4444"];
const tierColor = (t: number) => TIER[t - 1] ?? "#2a2a3a";
const PORDER = ["P1", "P2", "P3", "P4", "P5"];

function Tile({ c }: { c: Summary }) {
  const col = tierColor(c.tier);
  return (
    <Link
      href={`/country/${c.slug}`}
      className="card group flex flex-col gap-2 p-3 transition hover:border-fg3"
    >
      <div className="flex items-start justify-between gap-2">
        <span className="text-[13px] font-medium leading-tight group-hover:text-white">{c.name}</span>
        <span className="num text-[13px] font-semibold" style={{ color: col }}>
          {c.mi.toFixed(2)}
        </span>
      </div>
      <div className="flex items-end gap-[3px]" style={{ height: 22 }}>
        {PORDER.map((p) => {
          const v = c.pillars[p];
          return (
            <div key={p} className="flex-1 rounded-sm" style={{ background: "#1a1a28", height: "100%" }}>
              <div
                style={{
                  background: v == null ? "repeating-linear-gradient(45deg,#2a2a3a,#2a2a3a 2px,transparent 2px,transparent 4px)" : col + "cc",
                  height: v == null ? "100%" : `${Math.max(6, v * 100)}%`,
                  marginTop: v == null ? 0 : "auto",
                  borderRadius: 2,
                }}
              />
            </div>
          );
        })}
      </div>
      <div className="mono flex items-center gap-1.5 text-[10px] text-fg3">
        <span style={{ color: col }}>● Tier {c.tier}</span>
        {c.coverage.present < 5 && <span>· {c.coverage.present}/5 data</span>}
      </div>
    </Link>
  );
}

export default function CountryGrid({ countries }: { countries: Summary[] }) {
  const [q, setQ] = useState("");
  const [tier, setTier] = useState(0);
  const [fullOnly, setFullOnly] = useState(false);
  const filtered = useMemo(
    () =>
      countries.filter(
        (c) =>
          (tier === 0 || c.tier === tier) &&
          (!fullOnly || c.coverage.present === 5) &&
          c.name.toLowerCase().includes(q.toLowerCase())
      ),
    [countries, q, tier, fullOnly]
  );
  return (
    <div>
      <div className="mb-4 flex flex-wrap items-center gap-2">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Search any country…"
          className="w-52 rounded-md border border-border bg-surface px-3 py-1.5 text-[13px] outline-none placeholder:text-fg3 focus:border-primary"
        />
        <div className="flex gap-1">
          {[0, 1, 2, 3, 4, 5].map((t) => (
            <button
              key={t}
              onClick={() => setTier(t)}
              className="rounded px-2 py-1 text-[11px] transition"
              style={{
                background: tier === t ? (t === 0 ? "#232338" : tierColor(t) + "22") : "transparent",
                color: t === 0 ? "#9a9ab0" : tierColor(t),
                border: `1px solid ${tier === t ? (t === 0 ? "#3a3a52" : tierColor(t) + "66") : "transparent"}`,
              }}
            >
              {t === 0 ? "All" : `T${t}`}
            </button>
          ))}
        </div>
        <button
          onClick={() => setFullOnly((v) => !v)}
          className="mono rounded px-2 py-1 text-[11px] transition"
          style={{
            background: fullOnly ? "#3b82f622" : "transparent",
            color: fullOnly ? "#60a5fa" : "#6b6b82",
            border: `1px solid ${fullOnly ? "#3b82f655" : "#232338"}`,
          }}
          title="Only countries measured on all five pillars are directly comparable"
        >
          Full data 5/5
        </button>
        <span className="mono ml-auto text-[11px] text-fg3">{filtered.length} shown</span>
      </div>
      <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
        {filtered.map((c) => (
          <Tile key={c.slug} c={c} />
        ))}
      </div>
    </div>
  );
}
