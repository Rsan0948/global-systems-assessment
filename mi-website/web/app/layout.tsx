import type { Metadata } from "next";
import { Fraunces, DM_Sans, JetBrains_Mono } from "next/font/google";
import Link from "next/link";
import { SITE } from "@/lib/config";
import "./globals.css";

const fraunces = Fraunces({ subsets: ["latin"], variable: "--font-fraunces", weight: ["400", "600", "900"] });
const dmSans = DM_Sans({ subsets: ["latin"], variable: "--font-dm-sans", weight: ["400", "500", "700"] });
const jetbrains = JetBrains_Mono({ subsets: ["latin"], variable: "--font-jetbrains", weight: ["400", "600"] });

export const metadata: Metadata = {
  metadataBase: new URL(SITE.url),
  title: `${SITE.name} — ${SITE.tagline.toLowerCase()}`,
  description: SITE.description,
  openGraph: { title: SITE.name, description: SITE.description, url: SITE.url, type: "website" },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${fraunces.variable} ${dmSans.variable} ${jetbrains.variable}`}>
      <body className="min-h-screen">
        <header className="sticky top-0 z-50 border-b border-border bg-bg/85 backdrop-blur">
          <div className="mx-auto flex max-w-6xl items-center justify-between gap-3 px-4 py-3 sm:px-5">
            <Link href="/" className="flex shrink-0 items-baseline gap-2">
              <span className="serif text-base font-semibold tracking-tight sm:text-lg">{SITE.name}</span>
              <span className="mono hidden text-[10px] text-fg3 sm:inline">{SITE.version}</span>
            </Link>
            <nav className="-mr-2 flex items-center gap-0.5 overflow-x-auto text-[13px] text-fg2 sm:gap-1">
              {SITE.nav.map(([label, href]) => (
                <Link
                  key={href}
                  href={href}
                  className="whitespace-nowrap rounded px-2 py-1.5 transition-colors hover:bg-surface2 hover:text-fg sm:px-2.5"
                >
                  {label}
                </Link>
              ))}
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-6xl px-4 sm:px-5">{children}</main>
        <footer className="mt-24 border-t border-border">
          <div className="mx-auto max-w-6xl px-4 py-8 text-[12px] text-fg3 sm:px-5">
            <p className="max-w-2xl">
              A deterministic structural diagnostic computed from citable public data — not a forecast.{" "}
              <Link href="/limits" className="link">
                What this can and can&apos;t tell you →
              </Link>
            </p>
            <p className="mono mt-3 text-[11px]">
              Engine: {SITE.name} {SITE.version} · open source · reproducible. Same data in → same answer out.
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
