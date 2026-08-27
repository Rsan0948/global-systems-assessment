"use client";
import { useState } from "react";
import Link from "next/link";
import type { SafeguardTile } from "@/lib/types";
import { SG_STATUS } from "@/lib/config";

const GROUPS: { title: string; note: string; keys: string[] }[] = [
  {
    title: "Structural gates",
    note: "Evaluated for every scored country, from the pillars and public data.",
    keys: ["J", "E"],
  },
  {
    title: "Conditions & events",
    note: "These safeguards come from the case studies. When the required context has not been reviewed, the result says “not assessed” instead of implying that everything is clear.",
    keys: ["A", "B", "C", "D", "F", "G", "I"],
  },
];

function Tile({ t }: { t: SafeguardTile }) {
  const [open, setOpen] = useState(false);
  const s = SG_STATUS[t.status] ?? SG_STATUS.clear;
  const dim = t.status === "not_assessed";
  return (
    <div
      className="rounded-lg border bg-surface2/40"
      style={{ borderColor: t.status === "firing" ? s.color + "55" : "#232338", opacity: dim ? 0.72 : 1 }}
    >
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        className="flex w-full items-center gap-3 p-3 text-left"
      >
        <span
          className={`inline-block h-2.5 w-2.5 shrink-0 rounded-full ${t.status === "firing" ? "pulse-dot" : ""}`}
          style={{ background: s.dot, color: s.dot }}
        />
        <span className="min-w-0 flex-1">
          <span className="text-[13px] font-medium text-fg">{t.name}</span>
          <span className="ml-2 text-[12px] text-fg3">{t.headline}</span>
        </span>
        <span className="mono shrink-0 text-[10px] uppercase tracking-wide" style={{ color: s.color }}>
          {s.label}
        </span>
      </button>
      {open && (
        <div className="border-t border-border px-3 pb-3 pt-2.5 text-[12px] leading-relaxed">
          {t.detail && <p className="text-fg2">{t.detail}</p>}
          {t.modification && (
            <p className="mt-2 text-fg3">
              <span className="mono text-[10px] uppercase tracking-wide text-fg3">If it fires: </span>
              {t.modification}
            </p>
          )}
          {t.why && (
            <div className="mt-2.5 rounded-md border border-border bg-bg/40 p-2.5">
              <div className="mono text-[10px] uppercase tracking-wide text-fg3">
                Where this safeguard came from
                {t.origin_cases.length > 0 && <> · {t.origin_cases.join(", ")}</>}
              </div>
              <p className="mt-1 text-fg2">{t.why}</p>
              {t.validated_by.length > 0 && (
                <p className="mt-1.5 text-[11px] text-fg3">Held up on: {t.validated_by.join(", ")}</p>
              )}
            </div>
          )}
          <div className="mono mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-[10px] text-fg3">
            {t.status === "firing" && <span>{t.share_firing} scored countries are currently flagged by this check</span>}
            {t.status === "borderline" && (
              <span>on watch: {t.share_firing} countries are currently flagged by this check</span>
            )}
            {t.status === "not_assessed" && <span>needs a reviewed context input before it can be assessed</span>}
          </div>
        </div>
      )}
    </div>
  );
}

export default function SafeguardBoard({ safeguards }: { safeguards: SafeguardTile[] }) {
  const byKey = Object.fromEntries(safeguards.map((t) => [t.key, t]));
  const firing = safeguards.filter((t) => t.status === "firing").length;
  const assessed = safeguards.filter((t) => t.status !== "not_assessed").length;
  return (
    <section className="card mt-6 p-5">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h2 className="serif text-base">The safeguard board</h2>
        <span className="mono text-[11px] text-fg3">
          {firing} flagged · {assessed}/{safeguards.length} assessed
        </span>
      </div>
      <p className="mt-1 text-[12px] leading-relaxed text-fg3">
        These are the same structural checks used in the case studies, applied to this country. Each one came from a
        historical case; tap any tile to see the rule, what it means here, and{" "}
        <span className="text-fg2">the case study it came from</span>.
      </p>

      {GROUPS.map((g) => {
        const tiles = g.keys.map((k) => byKey[k]).filter(Boolean) as SafeguardTile[];
        if (tiles.length === 0) return null;
        return (
          <div key={g.title} className="mt-4">
            <div className="mono mb-1.5 text-[10px] uppercase tracking-wider text-fg3">{g.title}</div>
            <p className="mb-2.5 text-[11px] leading-relaxed text-fg3">{g.note}</p>
            <div className="grid gap-2 sm:grid-cols-2">
              {tiles.map((t) => (
                <Tile key={t.key} t={t} />
              ))}
            </div>
          </div>
        );
      })}

      <p className="mt-4 text-[11px] text-fg3">
        A standing rule (Mod8) frames every reading: the index predicts structural <em>risk</em>, never who acts
        first. The margin-of-error gate (Mod4) applies when two countries are{" "}
        <Link href="/compare" className="link">
          compared head-to-head
        </Link>
        .
      </p>
    </section>
  );
}
