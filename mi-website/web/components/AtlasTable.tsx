"use client";
import { useMemo, useState } from "react";
import Link from "next/link";
import type { Summary } from "@/lib/data";

const TIER = ["#10b981", "#3b82f6", "#f59e0b", "#fb923c", "#ef4444"];
const COLS = [
  ["name", "Country"],
  ["mi", "MI"],
  ["P1", "Institutions"],
  ["P2", "Complexity"],
  ["P3", "Human Cap."],
  ["P4", "Economy"],
  ["P5", "Stability"],
] as const;

const cell = (v: number | null) =>
  v == null ? (
    <span className="text-fg3">—</span>
  ) : (
    <span style={{ color: `hsl(${v * 130}, 55%, 60%)` }}>{v.toFixed(2)}</span>
  );

export default function AtlasTable({ countries }: { countries: Summary[] }) {
  const [sort, setSort] = useState<string>("mi");
  const [q, setQ] = useState("");
  const rows = useMemo(() => {
    const f = countries.filter((c) => c.name.toLowerCase().includes(q.toLowerCase()));
    return f.sort((a, b) => {
      if (sort === "name") return a.name.localeCompare(b.name);
      const av = sort === "mi" ? a.mi : (a.pillars[sort] ?? -1);
      const bv = sort === "mi" ? b.mi : (b.pillars[sort] ?? -1);
      return bv - av;
    });
  }, [countries, sort, q]);

  return (
    <div>
      <input
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="Filter…"
        className="mb-3 w-48 rounded-md border border-border bg-surface px-3 py-1.5 text-[13px] outline-none placeholder:text-fg3 focus:border-primary"
      />
      <div className="card overflow-x-auto">
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
            {rows.map((c) => (
              <tr key={c.slug} className="border-b border-border/50 hover:bg-surface2">
                <td className="px-3 py-1.5">
                  <Link href={`/country/${c.slug}`} className="flex items-center gap-2 hover:text-white">
                    <span style={{ color: TIER[c.tier - 1] }}>●</span>
                    <span className="font-sans">{c.name}</span>
                  </Link>
                </td>
                <td className="px-3 py-1.5 font-semibold" style={{ color: TIER[c.tier - 1] }}>
                  {c.mi.toFixed(3)}
                </td>
                {["P1", "P2", "P3", "P4", "P5"].map((p) => (
                  <td key={p} className="px-3 py-1.5">
                    {cell(c.pillars[p])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
