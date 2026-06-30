"use client";
import { useState } from "react";
import type { Chip } from "@/lib/data";

const color = (v: Chip["valence"]) =>
  v === "good" ? "#4ade80" : v === "warn" ? "#fbbf24" : v === "bad" ? "#f87171" : "#9a9ab0";

export default function ChipRow({ chips }: { chips: Chip[] }) {
  const [open, setOpen] = useState<string | null>(null);
  return (
    <div>
      <div className="flex flex-wrap gap-2">
        {chips.map((c) => {
          const cl = color(c.valence);
          const active = open === c.key;
          return (
            <button
              key={c.key}
              onClick={() => setOpen(active ? null : c.key)}
              className="rounded-full border px-3 py-1 text-[12px] font-medium transition"
              style={{
                borderColor: cl + "66",
                color: cl,
                background: active ? cl + "1f" : cl + "12",
              }}
            >
              {c.label}
            </button>
          );
        })}
      </div>
      {open &&
        (() => {
          const c = chips.find((x) => x.key === open)!;
          return (
            <div className="card mt-3 p-4 text-[13px]">
              <div className="font-medium" style={{ color: color(c.valence) }}>
                {c.label}
              </div>
              <p className="mt-1 text-fg2">{c.why}</p>
              <p className="mono mt-2 text-[11px] text-fg3">Rule: {c.rule}</p>
            </div>
          );
        })()}
    </div>
  );
}
