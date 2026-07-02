#!/usr/bin/env python3
"""
Phase 3 — re-tag the 51 P1-ordinality cases by shock ORIGIN (endogenous/exogenous/mixed),
applying the FROZEN classification rule from docs/relational_tier_spec.md §C, and test whether
that origin is associated with the framework's PARTIAL outcomes.

DISCIPLINE (the no-fitting-labels-to-the-answer rule):
  - Tags are assigned ONLY from each case's factual shock description (case_name / key_test / notes /
    event_description / fragmentation_mechanism). The outcome counts are joined AFTERWARD, never used
    to assign a tag. The REVIEWED_TAGS overrides below cite only the shock text, never the outcome.
  - Firewalled & additive: this script reads case files read-only; it touches no MI score and is not
    imported by run_retrodiction.py. The 213/77/0 baseline is independent of it.

The §C rule:
  EXOGENOUS  = an external state actor is the proximate initiator of the territorial/sovereignty
               change (invasion, conquest, externally-imposed partition, occupation).
  ENDOGENOUS = the proximate driver is internal (civil war, secession, coup, institutional collapse,
               negotiated devolution) with no external state initiating the change.
  MIXED      = both present; record the primary initiator.
"""
import glob
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "data" / "case_studies" / "completed"

# Keyword pre-filter — external-state-initiator markers (surfaces candidates for review; not the final word).
EXO_MARKERS = ["invasion", "invaded", "invade", "conquest", "conquer", "annex", "occupation",
               "occupied", "occupy", "external administration", "externally imposed", "foreign milit",
               "interstate war", "border war", "cpa", "scorched-earth", "tni", "intervention", "partition"]

# Reviewed determinations where the §C 'proximate initiator' judgment needs reading (keywords can't decide).
# Each rationale cites ONLY the shock description — never the outcome.
REVIEWED_TAGS = {
    # external-state component is real:
    "case06": ("mixed", "endogenous",
               "1971 War of Independence: endogenous Bengali secession, but militarily DECIDED by India's "
               "external invasion of East Pakistan. Primary = endogenous secession; external state decisive."),
    "case08": ("mixed", "endogenous",
               "Eritrean independence 1993 (endogenous secession) FOLLOWED BY the 1998-2000 Ethiopia-Eritrea "
               "interstate border war (exogenous). Case spans both."),
    "case10": ("exogenous", "exogenous",
               "Timor-Leste was under Indonesian OCCUPATION (external power). Independence ended an external "
               "occupation, and the 1999 violence came from the departing external power (TNI), not the fragment."),
    "case30": ("exogenous", "exogenous",
               "Iraq rebuilt under EXTERNAL administration (CPA) after the 2003 US invasion; 'externally imposed' "
               "sectarian settlement. Paradigm exogenous statebuilding (Safeguard A)."),
    # keyword false positives — the marker is contextual, the scored shock is internal:
    "case01": ("endogenous", "endogenous",
               "'invasion/annex' refer to later Russia-Ukraine CONTEXT; the SCORED shock is the 1996 engineered "
               "USSR dissolution (internal imperial dissolution)."),
    "case04": ("endogenous", "endogenous",
               "'intervention' is the 2011 Libya context; the scored shock is the endogenous Arab Spring uprisings."),
    "case11": ("endogenous", "endogenous",
               "'occupy' is incidental; scored shock is Abiy's internal dismantling of ethnic federalism (re-suppression)."),
    "case33": ("endogenous", "endogenous",
               "'intervention' = the military as an internal veto actor (1987/2000 coups). Endogenous."),
    "case45": ("endogenous", "endogenous",
               "'intervention' incidental; scored shock is the failed 1990 Yemen fusion -> internal civil war."),
    "case51": ("endogenous", "endogenous",
               "'intervention' contextual; scored shock is the 1991 internal state collapse / warlordism."),
}


def _fulltext(d):
    m, pe = d.get("metadata", {}), d.get("pre_event", {})
    parts = [m.get("case_name", ""), m.get("key_test", ""), m.get("notes", ""), pe.get("event_description", "")]
    for _, ed in pe.get("entities", {}).items():
        parts.append(str(ed.get("context", {}).get("fragmentation_mechanism", "")))
    return " ".join(p for p in parts if p).lower()


def _outcomes(d):
    c = p = f = 0
    for _, r in d.get("verification", {}).items():
        s = (r.get("result", "") or "").upper()
        if "CONFIRMED" in s and "PARTIAL" not in s:
            c += 1
        elif "PARTIAL" in s or "INDETERMIN" in s:
            p += 1
        elif "FALSIF" in s:
            f += 1
    return c, p, f


def classify():
    rows = []
    for fpath in sorted(glob.glob(str(CASES / "case*.json"))):
        d = json.load(open(fpath))
        cid = d["metadata"]["case_id"]
        text = _fulltext(d)
        markers = [k for k in EXO_MARKERS if k in text]
        if cid in REVIEWED_TAGS:
            tag, primary, why = REVIEWED_TAGS[cid]
        else:
            tag, primary, why = "endogenous", "endogenous", "no external-state initiator in the shock description (rule default)."
        c, p, f = _outcomes(d)
        rows.append({"case_id": cid, "name": d["metadata"].get("case_name", ""),
                     "tag": tag, "primary_initiator": primary, "evidence": why,
                     "keyword_markers": markers, "outcomes": {"C": c, "P": p, "F": f}})
    return rows


def main():
    rows = classify()
    # freeze the artifact
    out = CASES.parent / "relational_tags.json"
    json.dump({"_meta": {"rule": "docs/relational_tier_spec.md §C; tags assigned from shock text BEFORE "
                         "joining outcomes; firewalled, additive, baseline untouched."},
               "tags": rows}, open(out, "w"), indent=1)
    # association
    agg = {"endogenous": [0, 0, 0, 0], "mixed": [0, 0, 0, 0], "exogenous": [0, 0, 0, 0]}
    for r in rows:
        a = agg[r["tag"]]
        a[0] += r["outcomes"]["C"]; a[1] += r["outcomes"]["P"]; a[2] += r["outcomes"]["F"]; a[3] += 1
    print(f"Wrote {out.relative_to(ROOT)} — {len(rows)} P1 cases tagged.\n")
    print(f"{'origin':12} {'cases':>5} {'preds':>6} {'C':>4} {'P':>4} {'F':>4} {'partial_rate':>13}")
    exo_like = [0, 0, 0, 0]
    for tag in ("endogenous", "mixed", "exogenous"):
        c, p, f, n = agg[tag]
        tot = c + p + f
        print(f"{tag:12} {n:>5} {tot:>6} {c:>4} {p:>4} {f:>4} {p/tot if tot else 0:>12.0%}")
        if tag in ("mixed", "exogenous"):
            for i in range(4): exo_like[i] += agg[tag][i]
    c, p, f, n = exo_like
    tot = c + p + f
    print(f"{'exo+mixed':12} {n:>5} {tot:>6} {c:>4} {p:>4} {f:>4} {p/tot if tot else 0:>12.0%}")
    print("\nHONEST READ: the corpus is ~92% endogenous; the exo/mixed cell is n=4 and the partial-rate "
          "gap is null (~29% vs ~26%). The within-corpus test is UNDERPOWERED BY CONSTRUCTION — the "
          "famous exogenous misses (Cyprus 1974, Spain 1936, Greece 1922, ancient conquests) are not in "
          "the corpus. See docs/relational_retag_phase3.md.")


if __name__ == "__main__":
    main()
