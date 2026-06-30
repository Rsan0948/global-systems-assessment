import { getCountries } from "@/lib/data";
import AtlasTable from "@/components/AtlasTable";
import { PageHeader, TierLegend } from "@/components/ui";

export const metadata = { title: "Atlas — Modernization Index" };

export default function Atlas() {
  const countries = getCountries();
  return (
    <div className="py-10">
      <PageHeader
        title="The Atlas"
        lede="Every scored country, rankable by any pillar. The score is a deterministic formula over public data — sort it, don't trust it blindly. Partial-data countries sort below the comparable ones."
      />
      <div className="mb-5">
        <TierLegend countries={countries} />
      </div>
      <AtlasTable countries={countries} />
    </div>
  );
}
