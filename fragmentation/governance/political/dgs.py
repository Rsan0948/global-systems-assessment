"""
Domain node 2A: political fragmentation -- the DGS -> instability test.

Why this, and not a "successor-count clusters at e" test: a polity's
administrative hierarchy is *designed* (imposed), so it is a boundary-condition
control, not a self-organizing branching ratio; and raw successor counts
conflate parent size with subdivision tendency (the USSR's 15 successors
reflect its 15 republics). So this domain does NOT contribute a clean ratio to
the universality ladder. Its real, e-independent contribution is a MECHANISM
prediction: does the Dimensional-Gap Score predict subsequent instability?

DGS = (interior complexity, z) - (interface capacity, z)
    interior proxy  = Economic Complexity Index (Harvard Atlas)
    interface proxy = institutional quality (V-Dem polyarchy / WGI gov-eff)

Test (PREREGISTRATION P-INST): logistic regression
    instability(t..t+10) ~ DGS + log(GDPpc) + log(pop) + region + decade
with the pre-registered null "DGS adds nothing beyond GDPpc and population."
Primary statistic = likelihood-ratio test on the DGS term; validation =
out-of-sample AUC gain on a temporal split.

REAL-DATA path (`ingest`): Correlates of War (fragmentation/instability events),
V-Dem, World Bank WGI, Harvard Atlas of Economic Complexity. Import-guarded.
RUNNABLE here: a synthetic country-period panel with a *tunable* true DGS
effect, used to calibrate the test (can it detect the effect through the
controls, and is it null when there is no effect?).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


# --- logistic regression (IRLS) + LR test, dependency-light -------------------
def _irls(X: np.ndarray, y: np.ndarray, iters: int = 50, ridge: float = 1e-6):
    n, p = X.shape
    beta = np.zeros(p)
    for _ in range(iters):
        eta = X @ beta
        mu = 1.0 / (1.0 + np.exp(-eta))
        w = np.clip(mu * (1 - mu), 1e-9, None)
        z = eta + (y - mu) / w
        WX = X * w[:, None]
        H = X.T @ WX + ridge * np.eye(p)
        beta_new = np.linalg.solve(H, X.T @ (w * z))
        if np.max(np.abs(beta_new - beta)) < 1e-8:
            beta = beta_new
            break
        beta = beta_new
    eta = X @ beta
    mu = 1.0 / (1.0 + np.exp(-eta))
    ll = float(np.sum(y * np.log(np.clip(mu, 1e-12, 1)) + (1 - y) * np.log(np.clip(1 - mu, 1e-12, 1))))
    return beta, ll


def _auc(y_true: np.ndarray, scores: np.ndarray) -> float:
    pos = scores[y_true == 1]
    neg = scores[y_true == 0]
    if pos.size == 0 or neg.size == 0:
        return float("nan")
    # Mann-Whitney U / (n_pos*n_neg)
    allv = np.concatenate([pos, neg])
    order = allv.argsort()
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, allv.size + 1)
    # average ranks for ties
    _, inv, counts = np.unique(allv, return_inverse=True, return_counts=True)
    avg = np.zeros(allv.size)
    cum = np.cumsum(np.concatenate([[0], counts]))
    for i in range(len(counts)):
        avg_rank = (cum[i] + 1 + cum[i + 1]) / 2.0
        avg[inv == i] = avg_rank
    r_pos = avg[:pos.size].sum()
    return float((r_pos - pos.size * (pos.size + 1) / 2.0) / (pos.size * neg.size))


@dataclass
class DGSResult:
    n: int
    beta_dgs: float
    lr_stat: float
    lr_df: int
    lr_p: float
    auc_full: float
    auc_reduced: float
    auc_gain: float


def fit_dgs(panel: dict) -> DGSResult:
    """panel keys: dgs, log_gdppc, log_pop, region (int), decade (int),
    instability (0/1), period (int for temporal split)."""
    y = np.asarray(panel["instability"], dtype=float)
    region = _dummies(panel["region"])
    decade = _dummies(panel["decade"])
    controls = np.column_stack([
        np.ones_like(y), panel["log_gdppc"], panel["log_pop"], region, decade
    ])
    full = np.column_stack([controls, panel["dgs"]])

    beta_r, ll_r = _irls(controls, y)
    beta_f, ll_f = _irls(full, y)
    lr = 2.0 * (ll_f - ll_r)
    from scipy.stats import chi2
    p = float(chi2.sf(lr, 1))

    # out-of-sample temporal split
    period = np.asarray(panel["period"])
    cut = np.median(period)
    tr, te = period <= cut, period > cut
    bf, _ = _irls(full[tr], y[tr])
    br, _ = _irls(controls[tr], y[tr])
    auc_f = _auc(y[te], full[te] @ bf)
    auc_r = _auc(y[te], controls[te] @ br)

    return DGSResult(
        n=int(y.size), beta_dgs=float(beta_f[-1]),
        lr_stat=float(lr), lr_df=1, lr_p=p,
        auc_full=auc_f, auc_reduced=auc_r, auc_gain=float(auc_f - auc_r),
    )


def _dummies(labels) -> np.ndarray:
    labels = np.asarray(labels)
    levels = np.unique(labels)[1:]            # drop first as reference
    return np.column_stack([(labels == lv).astype(float) for lv in levels]) if levels.size \
        else np.zeros((labels.size, 0))


def ingest(*args, **kw):  # pragma: no cover - needs real data + network
    raise NotImplementedError(
        "Wire COW + V-Dem + WGI + Atlas of Economic Complexity into the panel "
        "schema of fit_dgs(); the build environment cannot reach these sources."
    )
