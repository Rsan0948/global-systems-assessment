import type { Metadata } from "next";
import { Fraunces, DM_Sans, JetBrains_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const fraunces = Fraunces({ subsets: ["latin"], variable: "--font-fraunces", weight: ["400", "600", "900"] });
const dmSans = DM_Sans({ subsets: ["latin"], variable: "--font-dm-sans", weight: ["400", "500", "700"] });
const jetbrains = JetBrains_Mono({ subsets: ["latin"], variable: "--font-jetbrains", weight: ["400", "600"] });

export const metadata: Metadata = {
  title: "Modernization Index — how nations weather stress",
  description:
    "A structural diagnostic of how governed systems withstand stress. Deterministic, from citable public data. Look up any country — see how it's built, and what we can't yet see.",
};

const NAV = [
  ["Atlas", "/atlas"],
  ["Stories", "/stories"],
  ["How it works", "/how-it-works"],
  ["Limits", "/limits"],
  ["Data", "/data"],
];

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${fraunces.variable} ${dmSans.variable} ${jetbrains.variable}`}>
      <body className="min-h-full">
        <header className="sticky top-0 z-50 border-b border-border bg-bg/85 backdrop-blur">
          <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-3">
            <Link href="/" className="flex items-baseline gap-2">
              <span className="serif text-lg font-semibold tracking-tight">Modernization Index</span>
              <span className="mono text-[10px] text-fg3">v3.3</span>
            </Link>
            <nav className="flex items-center gap-1 text-[13px] text-fg2">
              {NAV.map(([label, href]) => (
                <Link key={href} href={href} className="rounded px-2.5 py-1.5 hover:bg-surface2 hover:text-fg">
                  {label}
                </Link>
              ))}
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-6xl px-5">{children}</main>
        <footer className="mt-24 border-t border-border">
          <div className="mx-auto max-w-6xl px-5 py-8 text-[12px] text-fg3">
            <p className="max-w-2xl">
              A deterministic structural diagnostic computed from citable public data — not a forecast.{" "}
              <Link href="/limits" className="link">
                What this can and can&apos;t tell you →
              </Link>
            </p>
            <p className="mono mt-3 text-[11px]">Engine: MI v3.3 · open source · reproducible. Same data in → same answer out.</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
