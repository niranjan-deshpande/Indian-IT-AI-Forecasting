"""Part 3 input: calibrate observation noise from pre-2023 data.

Method (documented in REPORT/DECISIONS):
 1. Metric series per firm-quarter (quarterly log changes x100): gR (cc revenue), gL (headcount),
    du (utilization), gTCV (deal value, YoY-free quarterly log change), SLc (service-line contrast).
 2. Window PRE_START..PRE_END, excluding COVID quarters. For each firm x metric, residual =
    value - firm mean - firm-specific quarter-of-year effect (seasonality).
 3. Pooled AR(1) coefficient rho_m per metric on residuals (consecutive quarters only).
 4. Innovations v = r_t - rho r_{t-1}; common component c_t = cross-firm mean of v in quarter t;
    idiosyncratic = v - c_t. Omega_common = cov(c) minus mean idio variance / N (small-sample
    correction, projected to PSD); Omega_idio_f = cov of firm f's idiosyncratic innovations
    (pairwise-complete). Firms with <8 innovations for a metric get the pooled median.
 5. tau_h (firm-specific persistent drift): dispersion across firms of the change in firm-relative
    mean gR between two pre sub-windows, net of sampling variance, annualized.
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
from common import PRE_START, PRE_END, COVID


def qnum(q: str) -> int:
    return int(q[:4]) * 4 + int(q[-1]) - 1


def residuals(panel: pd.DataFrame, metric: str, start=PRE_START, end=PRE_END, exclude=COVID, seasonal=False):
    """Residual = value - firm mean (- firm x quarter-of-year mean if seasonal). YoY metrics need no seasonal terms."""
    d = panel[["firm", "cal_q", metric]].dropna()
    d = d[(d.cal_q >= start) & (d.cal_q <= end) & (~d.cal_q.isin(exclude))].copy()
    if not seasonal:
        d["r"] = d[metric] - d.groupby("firm")[metric].transform("mean")
        d["t"] = d.cal_q.map(qnum)
        return d[["firm", "cal_q", "t", "r"]]
    d["qoy"] = d.cal_q.str[-1]
    d["r"] = d[metric] - d.groupby(["firm", "qoy"])[metric].transform("mean")
    # quarter-of-year means per firm need >=2 obs per cell; otherwise fall back to firm mean
    cnt = d.groupby(["firm", "qoy"])[metric].transform("count")
    fm = d[metric] - d.groupby("firm")[metric].transform("mean")
    d.loc[cnt < 3, "r"] = fm[cnt < 3]
    d["t"] = d.cal_q.map(qnum)
    return d[["firm", "cal_q", "t", "r"]]


def ar1(res: pd.DataFrame) -> float:
    r = res.sort_values(["firm", "t"]).copy()
    r["lag"] = r.groupby("firm")["r"].shift()
    r["gap"] = r.groupby("firm")["t"].diff()
    r = r[r.gap == 1]
    if len(r) < 10:
        return 0.0
    rho = (r.r * r.lag).sum() / (r.lag**2).sum()
    return float(np.clip(rho, -0.5, 0.9))


def psd(M):
    w, V = np.linalg.eigh(0.5 * (M + M.T))
    return (V * np.clip(w, 1e-8, None)) @ V.T


def calibrate(panel: pd.DataFrame, metrics: list, firms: list, window=(PRE_START, PRE_END), exclude=COVID):
    res = {m: residuals(panel, m, window[0], window[1], exclude) for m in metrics}
    rho = np.array([ar1(res[m]) for m in metrics])
    inn = []
    for i, m in enumerate(metrics):
        r = res[m].sort_values(["firm", "t"]).copy()
        r["lag"] = r.groupby("firm")["r"].shift()
        r["gap"] = r.groupby("firm")["t"].diff()
        r = r[r.gap == 1]
        r["v"] = r.r - rho[i] * r.lag
        r["metric"] = m
        inn.append(r[["firm", "cal_q", "metric", "v"]])
    inn = pd.concat(inn)
    inn["c"] = inn.groupby(["cal_q", "metric"])["v"].transform("mean")
    inn["n"] = inn.groupby(["cal_q", "metric"])["v"].transform("count")
    # deviation from a cross-firm mean that includes the firm itself has variance sigma_i^2 (n-1)/n: rescale
    inn["i"] = (inn.v - inn.c) * np.sqrt(inn.n / (inn.n - 1).clip(lower=1))
    inn.loc[inn.n < 3, ["c", "i"]] = np.nan          # common not identified with <3 firms
    C = inn.drop_duplicates(["cal_q", "metric"]).pivot(index="cal_q", columns="metric", values="c")
    C = C.reindex(columns=metrics)
    Om_c = C.cov(min_periods=8).reindex(index=metrics, columns=metrics).fillna(0).values
    I = inn.pivot_table(index=["firm", "cal_q"], columns="metric", values="i").reindex(columns=metrics)
    Om_i = {}
    pooled = I.cov(min_periods=10).reindex(index=metrics, columns=metrics).fillna(0).values
    for f in firms:
        if f in I.index.get_level_values(0):
            If = I.loc[f]
            O = If.cov(min_periods=8).reindex(index=metrics, columns=metrics)
            # fall back to pooled where firm-specific not estimable
            O = O.where(O.notna(), pd.DataFrame(pooled, index=metrics, columns=metrics)).values
        else:
            O = pooled.copy()
        Om_i[f] = psd(O)
    # cov of the cross-firm mean = Omega_common + mean(Omega_idio / n): subtract the full matrix, using mean(1/n)
    # over quarters where the common component is identified (n >= 3)
    q = inn[inn.n >= 3].drop_duplicates(["cal_q", "metric"])
    inv_n = q.assign(inv=1.0 / q.n).groupby("metric")["inv"].mean().reindex(metrics).fillna(0.2).values
    mean_idio = np.mean([Om_i[f] for f in firms], axis=0)
    Om_c = Om_c - mean_idio * np.sqrt(np.outer(inv_n, inv_n))
    Om_c = psd(Om_c)
    return dict(metrics=metrics, rho=rho, omega_common=Om_c, omega_idio=Om_i,
                n_innov=inn.groupby("metric").v.count().reindex(metrics).fillna(0).astype(int).to_dict())


def tau_h(panel: pd.DataFrame, metric="gR", w1=("2015Q2", "2018Q4"), w2=("2019Q1", "2022Q4"), exclude=COVID):
    """Std. dev. (annualized, %/yr) of persistent firm-specific drift changes."""
    out = []
    for a, b in (w1, w2):
        d = panel[(panel.cal_q >= a) & (panel.cal_q <= b) & (~panel.cal_q.isin(exclude))]
        g = d.groupby("firm")[metric].agg(["mean", "var", "count"])
        out.append(g)
    j = out[0].join(out[1], lsuffix="1", rsuffix="2").dropna()
    j = j[(j.count1 >= 6) & (j.count2 >= 6)]
    if len(j) < 3:
        return np.nan, j
    rel = (j.mean2 - j.mean1) - (j.mean2 - j.mean1).mean()
    samp = (j.var1 / j.count1 + j.var2 / j.count2).mean()
    tv = max(rel.var(ddof=1) - samp, 0.0)
    return float(np.sqrt(tv)), j      # YoY metrics are already annual rates


def to_json(cal: dict, path):
    out = dict(metrics=cal["metrics"], rho=cal["rho"].tolist(),
               omega_common=cal["omega_common"].tolist(),
               omega_idio={f: v.tolist() for f, v in cal["omega_idio"].items()},
               n_innov=cal["n_innov"])
    for k in ("tau_h", "tau_h_note"):
        if k in cal:
            out[k] = cal[k]
    json.dump(out, open(path, "w"), indent=1)
