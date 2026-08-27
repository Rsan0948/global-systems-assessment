import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center py-32 text-center">
      <p className="mono text-[12px] text-fg3">404 · not measured</p>
      <h1 className="serif mt-3 text-3xl font-black">No reading for that.</h1>
      <p className="mt-3 max-w-md text-[14px] text-fg2">
        Either this page does not exist or that country has not been scored yet. Many countries are
        still missing enough public data to produce a useful score.
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
