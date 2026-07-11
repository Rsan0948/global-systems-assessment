#!/usr/bin/env python3
"""
Convergence-confirmation shared library. Self-contained loaders + stats so the
convergence tests do not import esi_tests (whose module-level GDP_RAW load is a
gitignored heavy file). Reuses the EXACT committed conventions:

  * historical structure = V-Dem rule-of-law (vdem_longrun.json 'rol')
  * historical wealth    = log Maddison GDP (longrun_pillars.json 'P4_gdp')
  * domestic onsets      = contagion/crisis_classification.json classification_primary
  * struct_auc = auc_roc(-rol, label);  wealth_auc = auc_roc(-logGDP, label)
  * epoch grid 1816..1996 step 10, min 12 obs, both classes; 25-yr forward window

Frozen spec: docs/CONVERGENCE_PREREGISTRATION.md (sha256 4071b996). Read-only.
"""
from __future__ import annotations
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[2]

VDEM = ROOT / "data/sources/vdem_longrun.json"
LONGRUN = ROOT / "data/sources/longrun_pillars.json"
CLASS = ROOT / "data/robustness/contagion/crisis_classification.json"
SPLIT = ROOT / "data/robustness/contagion/t2_split_curve.json"
MI_PANEL = ROOT / "data/robustness/decoupling/mi_5pt_panel.json"
WDI = ROOT / "data/robustness/decoupling/wdi_decoupling.json"
FORM = ROOT / "data/robustness/formation/state_formation.json"

WINDOW = 25
EPOCHS = list(range(1816, 1997, 10))
MI_YEARS = [1996, 2004, 2012, 2018, 2024]
L2 = 1e-3


def _ser(v):
    return json.loads(v) if isinstance(v, str) else v


# --------------------------------------------------------------------------- stats
def auc_roc(scores, labels):
    """Mann-Whitney AUC (higher score -> higher predicted crisis). Identical to esi_tests."""
    s = np.asarray(scores, float); y = np.asarray(labels, int)
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    ranks = stats.rankdata(s)
    return (ranks[y == 1].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))


def zscore(x):
    x = np.asarray(x, float); sd = x.std()
    return (x - x.mean()) / sd if sd > 0 else x - x.mean()


def logit_fit(X, y):
    """Ridge-regularized logistic MLE via BFGS. X includes intercept col.
    Returns (coef, auc, loglik). Identical spec to esi_tests.logit_fit (L2=1e-3)."""
    X = np.asarray(X, float); y = np.asarray(y, float)
    n, k = X.shape

    def nll(b):
        z = X @ b
        ll = np.sum(y * z - np.logaddexp(0.0, z))
        pen = L2 * np.sum(b[1:] ** 2)
        return -ll + pen

    res = minimize(nll, np.zeros(k), method="BFGS")
    b = res.x
    p = 1.0 / (1.0 + np.exp(-(X @ b)))
    return b, auc_roc(p, y), -nll(b)


def logit_coef_se(X, y, b, n_boot=400, seed=0):
    """Bootstrap SE for logistic coefficients (deterministic seed)."""
    X = np.asarray(X, float); y = np.asarray(y, float)
    n, k = X.shape
    rng = np.random.default_rng(seed)
    boots = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        Xi, yi = X[idx], y[idx]
        if len(set(yi.tolist())) < 2:
            continue
        try:
            bi, _, _ = logit_fit(Xi, yi)
            boots.append(bi)
        except Exception:
            continue
    if len(boots) < 30:
        return [float("nan")] * k
    B = np.array(boots)
    return B.std(axis=0, ddof=1).tolist()


def trend(xs, ys):
    r = stats.linregress(xs, ys)
    return {"slope": float(r.slope), "p": float(r.pvalue), "r": float(r.rvalue)}


# --------------------------------------------------------------------------- loaders
def load_rol_gdp():
    vdem = json.loads(VDEM.read_text())
    longrun = json.loads(LONGRUN.read_text())
    rol = {i: _ser(v["rol"]) for i, v in vdem.items() if "rol" in v}
    gdp = {i: {int(y): val for y, val in _ser(v["P4_gdp"]).items()}
           for i, v in longrun.items() if "P4_gdp" in v}
    return rol, gdp


def domestic_years():
    data = json.loads(CLASS.read_text())["classification_primary"]
    out = defaultdict(set)
    for key, origins in data.items():
        iso, y = key.split("|")
        if "domestic" in origins:
            out[iso].add(int(y))
    return out


def all_onset_years(tag=None):
    """iso -> set(years) for any tag (None = any origin)."""
    data = json.loads(CLASS.read_text())["classification_primary"]
    out = defaultdict(set)
    for key, origins in data.items():
        iso, y = key.split("|")
        if tag is None or tag in origins:
            out[iso].add(int(y))
    return out


def committed_decomp():
    """The committed Finding-14 struct/wealth curve (domestic channel)."""
    split = json.loads(SPLIT.read_text())
    return split["primary"]["domestic"]["curve"]


def epoch_decomp(labels_for, isos_filter=None, epochs=None):
    """Generic struct/wealth AUC decomposition over epochs.

    labels_for(iso, year) -> 0/1/None crisis label in [year, year+WINDOW].
    isos_filter: optional set of isos to restrict to.
    Returns list of per-epoch dicts (year,n,n_pos,struct_auc,wealth_auc,spread).
    """
    rol, gdp = load_rol_gdp()
    epochs = epochs or EPOCHS
    universe = set(rol) & set(gdp)
    if isos_filter is not None:
        universe = universe & set(isos_filter)
    pts = []
    for y in epochs:
        rv, gv, lab = [], [], []
        for iso in universe:
            if iso.startswith("OWID"):
                continue
            r = rol[iso].get(str(y)); g0 = gdp[iso].get(y)
            if r is None or g0 is None or g0 <= 0:
                continue
            l = labels_for(iso, y)
            if l is None:
                continue
            rv.append(float(r)); gv.append(-math.log(g0)); lab.append(int(l))
        if len(rv) < 12 or len(set(lab)) < 2:
            pts.append({"year": y, "n": len(rv), "n_pos": int(sum(lab)),
                        "struct_auc": None, "wealth_auc": None, "spread": None})
            continue
        sa = float(auc_roc([-v for v in rv], lab))
        wa = float(auc_roc(gv, lab))
        pts.append({"year": y, "n": len(rv), "n_pos": int(sum(lab)),
                    "struct_auc": round(sa, 4), "wealth_auc": round(wa, 4),
                    "spread": round(sa - wa, 4)})
    return pts


def domestic_label_fn():
    dom = domestic_years()
    def f(iso, y):
        return 1 if any(y <= oy <= y + WINDOW for oy in dom.get(iso, set())) else 0
    return f


def load_mi_panel():
    return json.loads(MI_PANEL.read_text())


def load_wdi():
    return json.loads(WDI.read_text())


def wdi_val(wdi, indicator, iso, year):
    ser = wdi.get(indicator, {}).get(iso)
    if not isinstance(ser, dict):
        return None
    v = ser.get(str(year))
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def wdi_isos(wdi, indicator):
    return [iso for iso, v in wdi.get(indicator, {}).items()
            if isinstance(v, dict) and not iso.startswith("_")]


def load_formation():
    form = json.loads(FORM.read_text())
    classes = form.get("states", form)
    return {iso: (v.get("group") if isinstance(v, dict) else v) for iso, v in classes.items()}
