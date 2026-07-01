"use client";
import Link from "next/link";
import { GLOSSARY } from "@/lib/glossary";
import { usePopover } from "@/lib/usePopover";

// Inline "what does this mean?" affordance. Dotted underline; click to reveal a
// plain-language definition with a link to the fuller explanation. Beginner-friendly,
// never in the way. Escape closes; the popover nudges to stay on-screen.
export default function Define({
  id,
  children,
  className = "",
}: {
  id: string;
  children?: React.ReactNode;
  className?: string;
}) {
  const { open, setOpen, ref, pos } = usePopover<HTMLSpanElement>();
  const e = GLOSSARY[id];
  if (!e) return <>{children ?? id}</>;

  return (
    <span className="relative inline-block">
      {open && (
        <button
          aria-label="Close definition"
          tabIndex={-1}
          className="fixed inset-0 z-20 cursor-default"
          onClick={() => setOpen(false)}
        />
      )}
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        className={`cursor-help border-b border-dotted border-fg3 decoration-dotted underline-offset-2 transition-colors hover:border-primary hover:text-primary ${className}`}
      >
        {children ?? e.term}
      </button>
      {open && (
        <span
          ref={ref}
          style={{ transform: `translateX(${pos.x}px)` }}
          className={`absolute left-0 z-30 block w-64 max-w-[calc(100vw-1rem)] rounded-lg border border-border bg-surface p-3 text-left text-[12px] font-normal normal-case tracking-normal ${pos.above ? "bottom-full mb-1.5" : "top-full mt-1.5"}`}
        >
          <span className="block font-medium text-fg">{e.term}</span>
          <span className="mt-1 block leading-relaxed text-fg2">{e.short}</span>
          <Link
            href={`/how-it-works#${e.id}`}
            className="link mt-2 inline-block text-[11px]"
            onClick={() => setOpen(false)}
          >
            Learn more →
          </Link>
        </span>
      )}
    </span>
  );
}
