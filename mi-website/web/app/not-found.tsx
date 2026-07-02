import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center py-32 text-center">
      <p className="mono text-[12px] text-fg3">404 · not measured</p>
      <h1 className="serif mt-3 text-3xl font-black">No reading for that.</h1>
      <p className="mt-3 max-w-md text-[14px] text-fg2">
        Either the page doesn&apos;t exist, or that country isn&apos;t scored yet - roughly half the
        world&apos;s states lack the public data the engine needs, and we don&apos;t guess.
      </p>
      <div className="mono mt-6 flex gap-4 text-[13px]">
        <Link href="/" className="link">
          ← Home
        </Link>
        <Link href="/atlas" className="link">
          Browse the atlas →
        </Link>
      </div>
    </div>
  );
}
