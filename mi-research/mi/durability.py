"""
V2 headline output — the Durability Ratio.

The MI residual against log-GDP per capita: fit MI ~ a + b*ln(GDPpcPPP) across a
reference set, then for a country residual = actual MI - predicted MI.
  residual > 0  -> institutions EXCEED what income predicts  (earned / durable)
  residual < 0  -> income EXCEEDS what institutions predict   (granted / fragile)

It answers "is this prosperity going to last?" in one number. Computed on demand
from the internal Data API + the active V2 scoring (so it tracks the lens + data).
Pure stdlib OLS (no numpy dependency).
"""
import math
from mi import datasource as ds
from mi.scoring import score_country


def _fit(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return my, 0.0
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    a = my - b * mx
    return a, b


def _reference(reference_year, countries=None):
    """Reference (ln GDP, MI) points across the Data API entities at reference_year."""
    names = countries or list(_all_country_names())
    xs, ys, used = [], [], []
    for nm in names:
        ind = ds.get_indicators(nm, reference_year)
        if not ind:
            continue
        gdp = ind.get("gdp_per_capita_ppp")
        mi = score_country(ind, event_year=reference_year)["mi_score"]
        if gdp and gdp > 0 and mi is not None:
            xs.append(math.log(gdp))
            ys.append(mi)
            used.append(nm)
    return xs, ys, used


def _all_country_names():
    data, _, _ = ds._wb()
    return list(data.keys())


def durability_ratio(country, year, reference_year=None):
    """Return the durability ratio for (country, year).

    reference_year defaults to `year` (cross-section at the same time point).
    Returns a dict: residual, predicted_mi, actual_mi, classification, n_reference.
    """
    reference_year = reference_year or year
    ind = ds.get_indicators(country, year)
    if not ind:
        return None
    gdp = ind.get("gdp_per_capita_ppp")
    mi = score_country(ind, event_year=year)["mi_score"]
    if not gdp or gdp <= 0 or mi is None:
        return {"residual": None, "classification": "undefined (missing GDP or MI)",
                "actual_mi": mi, "predicted_mi": None, "n_reference": 0}
    xs, ys, used = _reference(reference_year)
    if len(xs) < 5:
        return {"residual": None, "classification": "insufficient reference set",
                "actual_mi": mi, "predicted_mi": None, "n_reference": len(xs)}
    a, b = _fit(xs, ys)
    predicted = a + b * math.log(gdp)
    residual = mi - predicted
    cls = ("earned / durable (institutions exceed income)" if residual > 0.02 else
           "granted / fragile (income exceeds institutions)" if residual < -0.02 else
           "on the line (institutions ~ income)")
    return {"residual": round(residual, 3), "predicted_mi": round(predicted, 3),
            "actual_mi": round(mi, 3), "classification": cls,
            "n_reference": len(xs), "reference_year": reference_year}
