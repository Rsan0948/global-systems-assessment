"""
Global Systems Measurement — a SYSTEM-level measurement category (distinct from the country-level MI).

Where the MI scores a single polity, this measures the *world system's* state from the same data,
aggregating the validated findings of the historical/golden-age work:

  - ENGINES: the three improvement engines (institutions / income / human-capital), each a global
    10-yr climb rate vs its historical-median "firing" bar. Golden ages are dimension-specific and
    out of phase (docs/longrun_golden_age_cycles.md).
  - CONTAINER: the institutional net (climb-minus-decline) trajectory — the supercycle discriminator
    that decides whether a growth deceleration is absorbed (strengthening, 1970s) or ruptures
    (eroding, 1910s). docs/globalization_supercycle_shape.md.
  - TEXTURE: surge / churn / stasis / collapse, from the climb vs decline mix.
  - MOVEMENT DISTRIBUTION: share of countries in each movement_quality class (real_ascent / windfall /
    ratchet_rise / hollow_stability / decline / stable), from the 5-pillar panel.

EXPLORATORY/descriptive: built on long-run PROXIES (V-Dem rule-of-law, Maddison GDP, life expectancy)
+ the mi-pipeline 5-pillar panel — NOT the country scoring engine, and it changes no country verdict.
Deterministic: same data in -> same measurement out.
"""
import csv
import json
import math
import statistics as st
from pathlib import Path

from mi.constants import (GLOBAL_ENGINE_MEDIAN, GLOBAL_ENGINE_THRESH,
                          GLOBAL_CONTAINER_STRENGTHENING, GLOBAL_CONTAINER_ERODING)
from mi.diagnostics import movement_quality

_SRC = Path(__file__).resolve().parent.parent / "data" / "sources"
_PANEL = Path(__file__).resolve().parent.parent.parent / "mi-pipeline" / "output" / "mi_scored_countries.csv"


def _load(name):
    try:
        return json.load(open(_SRC / name))
    except FileNotFoundError:
        return {}


def _engine_rate(series_by_iso, year, thresh, log=False, win=10):
    """Fraction of countries whose value climbed > thresh over the win-year window ending at `year`,
    and the decline fraction. series_by_iso: {iso: {str(year): val}}."""
    obs = climb = decline = 0
    for s in series_by_iso.values():
        a = s.get(str(year - win)); b = s.get(str(year))
        if a is None or b is None:
            continue
        if log:
            if a <= 0 or b <= 0:
                continue
            d = math.log(b) - math.log(a)
        else:
            d = b - a
        obs += 1
        climb += (d > thresh); decline += (d < -thresh)
    if obs < 10:
        return None
    return {"climb": climb / obs, "decline": decline / obs, "n": obs}


def _inst_forward_net(vd, year, span=12, win=10):
    """Institutional net (climb-minus-decline) averaged over the decade AHEAD [year, year+span] — the
    supercycle container discriminator. None if the forward window isn't observable yet (right-censored)."""
    inst = {i: vd[i]["rol"] for i in vd if "rol" in vd[i]}
    nets = []
    for y in range(year, year + span + 1):
        obs = cl = dc = 0
        for s in inst.values():
            a = s.get(str(y)); b = s.get(str(y + win))
            if a is None or b is None:
                continue
            obs += 1; cl += (b - a > 0.15); dc += (b - a < -0.15)
        if obs >= 10:
            nets.append((cl - dc) / obs)
    return st.mean(nets) if len(nets) >= 3 else None


def measure_global_system(year=2024, win=10):
    """Produce the global systems measurement for the window ending at `year`."""
    vd = _load("vdem_longrun.json")
    lr = _load("longrun_pillars.json")
    inst = {i: vd[i]["rol"] for i in vd if "rol" in vd[i]}
    income = {i: lr[i]["P4_gdp"] for i in lr if "P4_gdp" in lr[i]}
    life = {i: lr[i]["P3_lifeexp"] for i in lr if "P3_lifeexp" in lr[i]}

    def latest_with_data(series_by_iso, log=False):
        for y in range(year, year - 8, -1):
            r = _engine_rate(series_by_iso, y, GLOBAL_ENGINE_THRESH["institutions"] if not log else 0, log, win)
            if r:
                return y
        return year

    out = {"as_of": year, "window_years": win, "engines": {}, "_note": "system-level proxy measurement"}

    # ENGINES
    specs = [("institutions", inst, False), ("income", income, True), ("human_capital", life, False)]
    firing = 0
    for key, series, log in specs:
        # use the most recent year with data for this dimension
        yy = year
        r = _engine_rate(series, yy, GLOBAL_ENGINE_THRESH[key], log, win)
        while r is None and yy > year - 8:
            yy -= 1
            r = _engine_rate(series, yy, GLOBAL_ENGINE_THRESH[key], log, win)
        if r is None:
            out["engines"][key] = {"available": False}
            continue
        med = GLOBAL_ENGINE_MEDIAN[key]
        is_firing = r["climb"] > med
        firing += is_firing
        out["engines"][key] = {"window_end": yy, "climb_rate": round(r["climb"], 3),
                               "decline_rate": round(r["decline"], 3), "historical_median": med,
                               "firing": is_firing, "n": r["n"]}
    out["engines_firing"] = firing

    # CONTAINER (institutional net) + TEXTURE
    inst_e = out["engines"].get("institutions", {})
    if inst_e.get("available") is not False:
        cl, dc = inst_e["climb_rate"], inst_e["decline_rate"]
        net = cl - dc
        traj = ("strengthening" if net >= GLOBAL_CONTAINER_STRENGTHENING
                else "eroding" if net <= GLOBAL_CONTAINER_ERODING else "flat")
        texture = ("surge" if cl - dc > 0.06 else "collapse" if dc - cl > 0.04
                   else "stasis" if cl + dc < 0.06 else "churn")
        # FORWARD container = the supercycle discriminator (net over the decade AHEAD). The trailing
        # net is the decade BEHIND and can be the OPPOSITE of what matters (1973 trailing=collapse but
        # forward=Third-Wave-surge -> absorbed; 1913 trailing=calm but forward=brittle -> ruptured).
        fwd = _inst_forward_net(_load("vdem_longrun.json"), year)
        if fwd is None:
            fwd_traj, fwd_reading = "censored", "the decade ahead isn't observable yet — the discriminator is unknowable now"
        else:
            fwd_traj = ("strengthening" if fwd >= GLOBAL_CONTAINER_STRENGTHENING
                        else "eroding" if fwd <= GLOBAL_CONTAINER_ERODING else "flat")
            fwd_reading = {"strengthening": "robust — absorbed the deceleration (cf. 1970s/Third Wave)",
                           "eroding": "brittle — the deceleration ruptured (cf. 1910s)",
                           "flat": "neither clearly repairing nor collapsing"}[fwd_traj]
        out["container"] = {"net_trailing": round(net, 3), "trajectory_trailing": traj,
                            "net_forward": (round(fwd, 3) if fwd is not None else None),
                            "trajectory_forward": fwd_traj, "forward_reading": fwd_reading,
                            "note": "the FORWARD container is the supercycle discriminator; trailing is the decade behind."}
        out["texture"] = texture

    # MOVEMENT DISTRIBUTION (5-pillar panel)
    out["movement_distribution"] = _movement_distribution(year - win, year)
    out["caveats"] = [
        "Proxy/system-level — NOT the country scoring engine; changes no country verdict.",
        "Engines on long-run proxies (V-Dem rule-of-law, Maddison GDP, life expectancy); 'firing' = "
        "above the 1850-2012 historical-median climb rate.",
        "Container trajectory is the supercycle discriminator (n=3 shapes / n=2 outcomes) — a "
        "mechanism-consistent reading, not a powered law.",
        "Recent windows are right-censored (latest climbs need forward data) — read as provisional.",
    ]
    return out


def _movement_distribution(y0, y1):
    if not _PANEL.exists():
        return {"available": False}
    rows = {(r["iso3"], r["year"]): r for r in csv.DictReader(open(_PANEL, encoding="latin-1"))}
    P = ["P1", "P2", "P3", "P4", "P5"]
    # the 5-pillar panel is on grid years (e.g. 2012/2018/2024) — snap to its actual span
    pyears = sorted({int(y) for (_, y) in rows})
    if len(pyears) >= 2:
        y0, y1 = pyears[0], pyears[-1]

    def pill(iso, y):
        r = rows.get((iso, str(y)))
        if not r:
            return None
        try:
            v = {p: float(r[p]) for p in P}
        except (ValueError, KeyError):
            return None
        return v
    counts = {}
    isos = {i for (i, _) in rows}
    for iso in isos:
        a, b = pill(iso, y0), pill(iso, y1)
        if not a or not b:
            continue
        mq = movement_quality(b, a)
        if mq:
            counts[mq["class"]] = counts.get(mq["class"], 0) + 1
    total = sum(counts.values())
    if not total:
        return {"available": False}
    share = {k: round(v / total, 3) for k, v in sorted(counts.items(), key=lambda x: -x[1])}
    return {"window": f"{y0}-{y1}", "n": total, "share": share,
            "hollow_stability_share": share.get("hollow_stability", 0.0)}
