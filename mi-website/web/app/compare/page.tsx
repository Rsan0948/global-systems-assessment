import { getCountries } from "@/lib/data";
import Compare from "@/components/Compare";
import { PageHeader } from "@/components/ui";

export const metadata = { title: "Compare", alternates: { canonical: "/compare" } };

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
        lede="Choose two countries to compare their overall scores and five pillar profiles. Differences smaller than 0.03 are treated as too close to rank."
      />
      <div className="mx-auto max-w-2xl">
        <Compare countries={getCountries()} initialA={a} initialB={b} />
      </div>
    </div>
  );
}
