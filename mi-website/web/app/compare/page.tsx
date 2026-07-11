import { getCountries } from "@/lib/data";
import Compare from "@/components/Compare";
import { PageHeader } from "@/components/ui";

export const metadata = { title: "Compare - Modernization Index" };

export default async function ComparePage({
  searchParams,
}: {
  searchParams: Promise<{ a?: string; b?: string }>;
}) {
  const { a, b } = await searchParams;
  return (
    <div className="py-10">
      <PageHeader
        title="Compare"
        lede="Put two countries side by side: their pillar shapes, their scores, and where they actually differ."
      />
      <div className="mx-auto max-w-2xl">
        <Compare countries={getCountries()} initialA={a} initialB={b} />
      </div>
    </div>
  );
}
