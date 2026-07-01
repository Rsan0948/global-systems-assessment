"use client";
import { INDICATOR_META, labelFor, fmtVal } from "@/lib/indicators";
import { PILLARS } from "@/lib/config";
import { usePopover } from "@/lib/usePopover";

export default function IndicatorRow({
  ind,
}: {
  ind: { key: string; value: number; source: string };
}) {
  const { open, setOpen, ref, pos } = usePopover<HTMLDivElement>();
  const meta = INDICATOR_META[ind.key];
  const pillar = meta ? PILLARS[meta.pillar] : null;

  return (
    <div className="relative flex items-baseline justify-between gap-3 border-b border-border/50 py-1.5 text-[13px]">
      {open && (
        <button
          aria-label="Close"
          tabIndex={-1}
          className="fixed inset-0 z-20 cursor-default"
          onClick={() => setOpen(false)}
        />
      )}
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        className="cursor-help border-b border-dotted border-fg3 text-left text-fg2 underline-offset-2 transition-colors hover:border-primary hover:text-primary"
      >
        {labelFor(ind.key)}
      </button>
      <span className="num font-semibold text-fg">{fmtVal(ind.value)}</span>
      {open && meta && (
        <div
          ref={ref}
          style={{ transform: `translateX(${pos.x}px)` }}
          className={`absolute left-0 z-30 w-72 max-w-[calc(100vw-1rem)] rounded-lg border border-border bg-surface p-3 text-left text-[12px] font-normal ${pos.above ? "bottom-full mb-1" : "top-full mt-1"}`}
        >
          <div className="font-medium text-fg">{labelFor(ind.key)}</div>
          <p className="mt-1 leading-relaxed text-fg2">{meta.what}</p>
          <div className="mono mt-2 flex flex-wrap gap-x-3 gap-y-0.5 text-[10.5px] text-fg3">
            <span>Source: {ind.source}</span>
            {pillar && <span>Feeds: {pillar.full}</span>}
          </div>
        </div>
      )}
    </div>
  );
}
