"use client";
import { useState } from "react";
import type { Chip } from "@/lib/data";
import { valenceColor } from "@/lib/config";

export default function ChipRow({ chips }: { chips: Chip[] }) {
  const [open, setOpen] = useState<string | null>(null);
  const active = chips.find((c) => c.key === open);
  return (
    <div>
      <div className="flex flex-wrap gap-2">
        {chips.map((c) => {
          const cl = valenceColor(c.valence);
          const on = open === c.key;
          return (
            <button
              key={c.key}
              onClick={() => setOpen(on ? null : c.key)}
              aria-expanded={on}
              aria-controls={on ? "chip-detail" : undefined}
              className="rounded-full border px-3 py-1 text-[12px] font-medium transition-colors"
              style={{ borderColor: cl + "66", color: cl, background: on ? cl + "1f" : cl + "12" }}
            >
              {c.label}
            </button>
          );
        })}
      </div>
      {active && (
        <div id="chip-detail" role="region" className="card mt-3 p-4 text-[13px]">
          <div className="font-medium" style={{ color: valenceColor(active.valence) }}>
            {active.label}
          </div>
          <p className="mt-1 text-fg2">{active.why}</p>
          <p className="mono mt-2 text-[11px] text-fg3">Rule: {active.rule}</p>
        </div>
      )}
    </div>
  );
}
