"use client";
import { useState } from "react";
import Link from "next/link";
import type { Chip } from "@/lib/data";
import { scoreBand, valenceColor } from "@/lib/config";

const CHIP_ANCHOR: Record<string, string> = {
  tier: "score-bands",
  score_band: "score-bands",
  durability: "durability-gap",
  shape: "shape",
  partial: "the-score",
};

function publicLabel(chip: Chip): string {
  if (chip.key === "tier" || chip.key === "score_band") {
    const match = chip.label.match(/(?:Tier|Band)\s+(\d)/i);
    if (match) {
      const bandNumber = Number(match[1]);
      return `Band ${bandNumber}: ${scoreBand(bandNumber).name}`;
    }
  }
  if (chip.key === "durability") {
    return chip.label.toLowerCase().includes("granted")
      ? "Institutions lag income"
      : "Institutions keep pace with income";
  }
  return chip.label;
}

export default function ChipRow({ chips }: { chips: Chip[] }) {
  const [open, setOpen] = useState<string | null>(null);
  const active = chips.find((c) => c.key === open);
  return (
    <div>
      <div className="flex flex-wrap gap-2">
        {chips.map((c) => {
          const cl = valenceColor(c.valence);
          const on = open === c.key;
          const label = publicLabel(c);
          return (
            <button
              key={c.key}
              onClick={() => setOpen(on ? null : c.key)}
              aria-expanded={on}
              aria-controls={on ? "chip-detail" : undefined}
              className="rounded-full border px-3 py-1 text-[12px] font-medium transition-colors"
              style={{ borderColor: cl + "66", color: cl, background: on ? cl + "1f" : cl + "12" }}
            >
              {label}
            </button>
          );
        })}
      </div>
      {active && (
        <div id="chip-detail" role="region" className="card mt-3 p-4 text-[13px]">
          <div className="font-medium" style={{ color: valenceColor(active.valence) }}>
            {publicLabel(active)}
          </div>
          <p className="mt-1 text-fg2">{active.why}</p>
          <p className="mono mt-2 text-[11px] text-fg3">How it is calculated: {active.rule}</p>
          {CHIP_ANCHOR[active.key] && (
            <Link href={`/how-it-works#${CHIP_ANCHOR[active.key]}`} className="link mt-2 inline-block text-[11px]">
              Learn more →
            </Link>
          )}
        </div>
      )}
    </div>
  );
}
