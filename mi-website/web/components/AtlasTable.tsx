"use client";
import { useMemo, useState } from "react";
import Link from "next/link";
import type { Summary } from "@/lib/data";
import { PILLARS, scoreBandColor, heat } from "@/lib/config";

const COLS = [
  ["name", "Country"],
  ["mi", "MI"],
  ["P1", PILLARS.P1.short],
  ["P2", PILLARS.P2.short],
  ["P3", PILLARS.P3.short],
  ["P4", PILLARS.P4.short],
  ["P5", PILLARS.P5.short],
  ["cov", "Data"],
] as const;

const cell = (v: number | null) =>
  v == null ? <span className="text-fg3">-</span> : <span style={{ color: heat(v) }}>{v.toFixed(2)}</span>;

export default function AtlasTable({ countries }: { countries: Summary[] }) {
  const [sort, setSort] = useState<string>("mi");
  const [q, setQ] = useState("");
  const rows = useMemo(() => {
    const f = countries.filter((c) => c.name.toLowerCase().includes(q.toLowerCase()));
    return f.sort((a, b) => {
      if (sort === "name") return a.name.localeCompare(b.name);
      if (sort === "cov") return b.coverage.present - a.coverage.present || b.mi - a.mi;
      if (sort === "mi") {
        const fa = a.coverage.present === 5 ? 1 : 0;
        const fb = b.coverage.present === 5 ? 1 : 0;
        if (fa !== fb) return fb - fa; // full-coverage first (comparable)
        return b.mi - a.mi;
      }
      return (b.pillars[sort] ?? -1) - (a.pillars[sort] ?? -1);
    });
  }, [countries, sort, q]);

  return (
    <div>
      <div className="mb-3 flex flex-wrap items-center gap-2">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Filter…"
          aria-label="Filter countries"
          className="w-48 rounded-md border border-border bg-surface px-3 py-1.5 text-[13px] outline-none placeholder:text-fg3 focus:border-primary"
        />
        {/* Sort control for the stacked mobile layout (the desktop table sorts
            via its column headers). */}
        <label className="mono flex items-center gap-1.5 text-[11px] text-fg3 sm:hidden">
          Sort
          <select
            value={sort}
            onChange={(e) => setSort(e.target.value)}
            aria-label="Sort countries"
            className="rounded-md border border-border bg-surface px-2 py-1.5 text-[12px] text-fg outline-none focus:border-primary"
          >
            {COLS.map(([key, label]) => (
              <option key={key} value={key}>
                {label}
              </option>
            ))}
          </select>
        </label>
      </div>

      {/* Mobile: stacked cards (no horizontal scroll on narrow screens). */}
      <div className="flex flex-col gap-2 sm:hidden">
        {rows.length === 0 && (
          <p className="card px-3 py-10 text-center text-[13px] text-fg3">No countries match “{q}”.</p>
        )}
        {rows.map((c) => (
          <Link
            key={c.slug}
            href={`/country/${c.slug}`}
            className="card lift block px-3 py-3 active:bg-surface2"
          >
            <div className="flex items-baseline justify-between gap-2">
              <span className="flex min-w-0 items-center gap-2">
                <span style={{ color: scoreBandColor(c.tier) }}>●</span>
                <span className="truncate font-medium">{c.name}</span>
              </span>
              <span className="mono shrink-0 text-[15px] font-semibold" style={{ color: scoreBandColor(c.tier) }}>
                {c.mi.toFixed(3)}
              </span>
            </div>
            <div className="mono mt-2 flex flex-wrap gap-x-3 gap-y-1 text-[11px]">
              {["P1", "P2", "P3", "P4", "P5"].map((p) => (
                <span key={p} className="text-fg3">
                  {PILLARS[p].short} {cell(c.pillars[p])}
                </span>
              ))}
              <span className="text-fg3">
                Data{" "}
                {c.coverage.present < 5 ? (
                  <span className="text-warn/80">{c.coverage.present}/5</span>
                ) : (
                  <span>5/5</span>
                )}
              </span>
            </div>
          </Link>
        ))}
      </div>

      {/* Desktop / tablet: the sortable table. */}
      <div className="card hidden overflow-x-auto sm:block">
        <table className="w-full text-[12px]">
          <thead>
            <tr className="border-b border-border text-left text-fg3">
              {COLS.map(([key, label]) => (
                <th key={key} className="px-3 py-2 font-medium">
                  <button
                    onClick={() => setSort(key)}
                    className={`mono hover:text-fg ${sort === key ? "text-primary" : ""}`}
                  >
                    {label} {sort === key && "▾"}
                  </button>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="mono">
            {rows.length === 0 && (
              <tr>
                <td colSpan={COLS.length} className="px-3 py-10 text-center font-sans text-[13px] text-fg3">
                  No countries match “{q}”.
                </td>
              </tr>
            )}
            {rows.map((c) => (
              <tr key={c.slug} className="border-b border-border/50 hover:bg-surface2">
                <td className="px-3 py-1.5">
                  <Link href={`/country/${c.slug}`} className="flex items-center gap-2 hover:text-white">
                    <span style={{ color: scoreBandColor(c.tier) }}>●</span>
                    <span className="font-sans">{c.name}</span>
                  </Link>
                </td>
                <td className="px-3 py-1.5 font-semibold" style={{ color: scoreBandColor(c.tier) }}>
                  {c.mi.toFixed(3)}
                </td>
                {["P1", "P2", "P3", "P4", "P5"].map((p) => (
                  <td key={p} className="px-3 py-1.5">
                    {cell(c.pillars[p])}
                  </td>
                ))}
                <td className="px-3 py-1.5 text-fg3">
                  {c.coverage.present < 5 ? (
                    <span className="text-warn/80">{c.coverage.present}/5</span>
                  ) : (
                    <span className="text-fg3">5/5</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
