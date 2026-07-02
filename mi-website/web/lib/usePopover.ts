"use client";
import { useEffect, useLayoutEffect, useRef, useState } from "react";

// Shared popover behaviour for the inline "click to learn" affordances.
// Handles: open state, Escape-to-close, and viewport collision (nudge left when
// it would overflow the right edge, flip above when it would overflow the bottom).
export function usePopover<T extends HTMLElement = HTMLElement>() {
  const [open, setOpen] = useState(false);
  const ref = useRef<T>(null);
  const [pos, setPos] = useState<{ x: number; above: boolean }>({ x: 0, above: false });

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  useLayoutEffect(() => {
    if (!open || !ref.current) return;
    // measure at natural position, then correct
    const el = ref.current;
    el.style.transform = "";
    const r = el.getBoundingClientRect();
    const pad = 8;
    let x = 0;
    if (r.right > window.innerWidth - pad) x = window.innerWidth - pad - r.right;
    if (r.left + x < pad) x = pad - r.left;
    const above = r.bottom > window.innerHeight - pad && r.top - r.height > pad;
    setPos({ x, above });
  }, [open]);

  return { open, setOpen, ref, pos };
}
