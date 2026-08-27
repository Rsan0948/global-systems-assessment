"use client";
import { useState } from "react";
import type { Summary } from "@/lib/types";
import { scoreBandColor, scoreBand, PILLAR_ORDER, PILLARS, clamp01 } from "@/lib/config";
import Radar from "@/components/Radar";
import Define from "@/components/Define";
import { ScoreBandDot } from "@/components/ui";

const CA = "#60a5fa";
const CB = "#f472b6";

function Picker({
  countries,
  value,
  onChange,
  color,
  placeholder,
}: {
  countries: Summary[];
  value: string;
  onChange: (slug: string) => void;
  color: string;
  placeholder: string;
}) {
  const [q, setQ] = useState("");
  const [open, setOpen] = useState(false);
  const sel = countries.find((c) => c.slug === value);
  const matches = countries
    .filter((c) => c.name.toLowerCase().includes(q.toLowerCase()))
    .slice(0, 30);
  return (
    <div className="relative flex-1">
      <input
        value={open ? q : sel?.name ?? ""}
        onFocus={() => {
          setOpen(true);
          setQ("");
        }}
        onChange={(e) => {
          setQ(e.target.value);
          setOpen(true);
        }}
        placeholder={placeholder}
        aria-label={placeholder}
        className="w-full rounded-md border bg-surface px-3 py-2 text-[14px] outline-none focus:border-primary"
        style={{ borderColor: sel ? color + "88" : "#232338" }}
      />
      {open && (
        <>
          <button aria-label="Close" tabIndex={-1} className="fixed inset-0 z-10 cursor-default" onClick={() => setOpen(false)} />
          <div className="absolute z-20 mt-1 max-h-64 w-full overflow-auto rounded-md border border-border bg-surface p-1 shadow-xl">
            {matches.map((c) => (
              <button
                key={c.slug}
                onClick={() => {
                  onChange(c.slug);
                  setOpen(false);
                }}
                className="flex w-full items-center gap-2 rounded px-2 py-1.5 text-left text-[13px] hover:bg-surface2"
              >
                <ScoreBandDot band={c.tier} size={7} />
                <span className="flex-1">{c.name}</span>
                <span className="num text-[12px]" style={{ color: scoreBandColor(c.tier) }}>
                  {c.mi.toFixed(2)}
                </span>
              </button>
            ))}
            {matches.length === 0 && (
              <p className="px-2 py-3 text-center text-[12px] text-fg3">No country matches that search.</p>
            )}
          </div>
        </>
      )}
    </div>
  );
}

function Head({ c, color }: { c: Summary; color: string }) {
  return (
    <div className="text-center">
      <div className="num text-3xl font-bold" style={{ color, textShadow: `0 0 22px ${color}44` }}>
        {c.mi.toFixed(3)}
      </div>
      <div className="serif mt-0.5 text-[15px]">{c.name}</div>
      <div className="mono text-[11px]" style={{ color }}>
        Band {c.tier} · {scoreBand(c.tier).name}
      </div>
    </div>
  );
}

export default function Compare({
  countries,
  initialA = "",
  initialB = "",
}: {
  countries: Summary[];
  initialA?: string;
  initialB?: string;
}) {
  const [a, setA] = useState(initialA);
  const [b, setB] = useState(initialB);
  const A = countries.find((c) => c.slug === a);
  const B = countries.find((c) => c.slug === b);

  const both = A && B;
  const incomplete = both && (A.coverage.present < 5 || B.coverage.present < 5);
  const diff = both ? A.mi - B.mi : 0;
  let verdict = "";
  if (both) {
    if (Math.abs(diff) < 0.03) {
      verdict = `${A.name} and ${B.name} have very similar scores (${A.mi.toFixed(2)} and ${B.mi.toFixed(2)}). The difference is below the 0.03 comparison margin, so they are treated as too close to rank.`;
    } else {
      const [hi, lo] = diff > 0 ? [A, B] : [B, A];
      // biggest pillar gap
      let gapP = "P1";
      let gapV = 0;
      for (const p of PILLAR_ORDER) {
        const va = A.pillars[p];
        const vb = B.pillars[p];
        if (va != null && vb != null && Math.abs(va - vb) > gapV) {
          gapV = Math.abs(va - vb);
          gapP = p;
        }
      }
      verdict = `${hi.name} has the higher overall score (${hi.mi.toFixed(2)} compared with ${lo.mi.toFixed(2)}). The largest pillar difference is in ${PILLARS[gapP].full.toLowerCase()}.`;
    }
  }

  return (
    <div>
      <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
        <Picker countries={countries} value={a} onChange={setA} color={CA} placeholder="Pick a country…" />
        <span className="mono text-center text-[12px] text-fg3">vs</span>
        <Picker countries={countries} value={b} onChange={setB} color={CB} placeholder="…and another" />
      </div>

      {!both ? (
        <p className="mt-10 text-center text-[13px] text-fg3">Pick two countries to compare their structural profiles.</p>
      ) : (
        <div className="mt-8">
          <div className="grid grid-cols-2 items-start gap-6">
            <Head c={A} color={CA} />
            <Head c={B} color={CB} />
          </div>

          {incomplete && (
            <p className="mt-5 rounded-lg border border-warn/30 bg-warn/[0.06] p-3 text-[12px] leading-relaxed text-fg2">
              At least one country is missing a pillar. This comparison uses the available data and
              is not directly comparable with a complete five-pillar comparison.
            </p>
          )}

          <div className="mt-6 flex justify-center">
            <Radar pillars={A.pillars} overlay={B.pillars} colors={[CA, CB]} size={300} />
          </div>
          <div className="mono mt-1 flex justify-center gap-4 text-[11px]">
            <span style={{ color: CA }}>● {A.name}</span>
            <span style={{ color: CB }}>● {B.name}</span>
          </div>

          <p className="card mt-6 p-4 text-center text-[13px] leading-relaxed text-fg">{verdict}</p>

          <div className="mt-6 space-y-3">
            {PILLAR_ORDER.map((p) => {
              const va = A.pillars[p];
              const vb = B.pillars[p];
              const aHi = va != null && vb != null && va > vb;
              const bHi = va != null && vb != null && vb > va;
              return (
                <div key={p} className="grid grid-cols-[3rem_1fr] items-center gap-3 sm:grid-cols-[8rem_1fr]">
                  <span className="text-[12px] text-fg2">
                    <span className="hidden sm:inline">
                      <Define id={p.toLowerCase()}>{PILLARS[p].full}</Define>
                    </span>
                    <span className="mono sm:hidden">{p}</span>
                  </span>
                  <div className="space-y-1.5">
                    <div className="flex items-center gap-2">
                      <div className="h-2 flex-1 overflow-hidden rounded-full bg-surface2">
                        <div className="h-full rounded-full" style={{ width: `${clamp01(va ?? 0) * 100}%`, background: CA, opacity: va == null ? 0.2 : 1 }} />
                      </div>
                      <span className="num w-9 text-right text-[11px]" style={{ color: aHi ? CA : "#a6a6bd", fontWeight: aHi ? 700 : 400 }}>
                        {va == null ? "n/a" : va.toFixed(2)}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="h-2 flex-1 overflow-hidden rounded-full bg-surface2">
                        <div className="h-full rounded-full" style={{ width: `${clamp01(vb ?? 0) * 100}%`, background: CB, opacity: vb == null ? 0.2 : 1 }} />
                      </div>
                      <span className="num w-9 text-right text-[11px]" style={{ color: bHi ? CB : "#a6a6bd", fontWeight: bHi ? 700 : 400 }}>
                        {vb == null ? "n/a" : vb.toFixed(2)}
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
