"""Shared helpers for the audit scripts (Task 1b). Read-only with respect to the pilot's files.

Paths: ROOT is the project root; audit outputs go to ROOT/audit/.
"""
from pathlib import Path
import importlib.util
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
TIDY = ROOT / "data" / "tidy"
CORR = ROOT / "data" / "corrected"
AUD = ROOT / "audit"
AUD.mkdir(exist_ok=True)

INDIAN6 = ["tcs", "infosys", "hcltech", "wipro", "techm", "ltim"]
INDIAN_ALL = INDIAN6 + ["lti", "mindtree"]
EXCL = ["2020Q2", "2020Q3", "2020Q4", "2021Q1", "2021Q2"]      # pilot's COVID exclusion (03_part2.py)


def load_module(name, path):
    """Import a module whose file name starts with a digit (e.g. 01_build_tidy.py) without editing it."""
    import sys
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def qadd(q, k):
    y, n = int(q[:4]), int(q[-1])
    t = y * 4 + n - 1 + k
    return f"{t // 4}Q{t % 4 + 1}"


def qrange(a, b):
    out, q = [], a
    while q <= b:
        out.append(q)
        q = qadd(q, 1)
    return out


def indian_fiscal(cal_q):
    """Indian FY (Apr-Mar) label of a calendar quarter: 2024Q2 -> Q1FY25; 2023Q1 -> Q4FY23."""
    y, n = int(cal_q[:4]), int(cal_q[-1])
    fq = {2: 1, 3: 2, 4: 3, 1: 4}[n]
    fy = y + 1 if n >= 2 else y
    return f"Q{fq}FY{fy % 100:02d}"


def indian_fy(cal_q):
    y, n = int(cal_q[:4]), int(cal_q[-1])
    return (y + 1 if n >= 2 else y)


def accenture_fiscal(cal_q):
    """Accenture label of the quarter the pilot assigns to cal_q (Nov->Q4, Feb->Q1, May->Q2, Aug->Q3)."""
    y, n = int(cal_q[:4]), int(cal_q[-1])
    fq = {4: 1, 1: 2, 2: 3, 3: 4}[n]
    fy = y + 1 if n == 4 else y
    return f"Q{fq}FY{fy % 100:02d}"


def load_yoy(path=None):
    return pd.read_csv(path or TIDY / "yoy_metrics.csv")


def load_core(path=None):
    return pd.read_csv(path or TIDY / "core_quarterly.csv", low_memory=False)


def ltim_chain(yoy, core):
    """One-entity LTI-group series (alternative to the pilot's 3-entity treatment), built from growth rates only:
    - gL: YoY log change of (LTI + Mindtree) standalone headcount through 2022Q1 (both ends standalone sums),
          LTIM restated combined headcount from 2022Q2 (both ends restated) -> no level splice.
    - gR (cc): LTI's reported cc YoY through 2022Q3 (Mindtree reports no cc YoY), LTIM from 2022Q4.
    - du: LTI series through 2022Q1, LTIM from 2022Q2.
    Returns a yoy-like frame with firm='ltim_chain'."""
    c = core[core.firm.isin(["lti", "mindtree"])].pivot(index="cal_q", columns="firm", values="headcount")
    hsum = (c["lti"] + c["mindtree"]).dropna()
    rows = []
    lti = yoy[yoy.firm == "lti"].set_index("cal_q")
    lm = yoy[yoy.firm == "ltim"].set_index("cal_q")
    for q in qrange("2016Q2", "2026Q2"):
        r = dict(firm="ltim_chain", cal_q=q)
        if q <= "2022Q1":
            l = qadd(q, -4)
            r["gL"] = 100 * np.log(hsum[q] / hsum[l]) if q in hsum.index and l in hsum.index else np.nan
            r["du"] = lti["du"].get(q, np.nan)
        else:
            r["gL"] = lm["gL"].get(q, np.nan)
            r["du"] = lm["du"].get(q, np.nan)
        r["gR"] = lti["gR"].get(q, np.nan) if q <= "2022Q3" else lm["gR"].get(q, np.nan)
        rows.append(r)
    d = pd.DataFrame(rows)
    d["gRPE"] = d.gR - d.gL
    d["resid"] = d.gR - d.gL - d.du
    return d


def indian_panel(yoy, core, scheme="pilot"):
    """Firm x quarter Indian panel under different entity schemes.
    pilot : INDIAN6 + lti + mindtree, ltim dropped before 2022Q3 (exactly as 03_part2.py; ltim, lti, mindtree all in 2022Q3)
    dedup : as pilot but ltim also dropped in 2022Q3 (lti/mindtree end 2022Q3, ltim from 2022Q4) -> no double count
    chain : tcs, infosys, hcltech, wipro, techm + one 'ltim_chain' entity (see ltim_chain)"""
    if scheme in ("pilot", "dedup"):
        ind = yoy[yoy.firm.isin(INDIAN_ALL)].copy()
        cut = "2022Q3" if scheme == "pilot" else "2022Q4"
        ind = ind[~((ind.firm == "ltim") & (ind.cal_q < cut))]
        return ind
    if scheme == "chain":
        ind = yoy[yoy.firm.isin(["tcs", "infosys", "hcltech", "wipro", "techm"])].copy()
        return pd.concat([ind, ltim_chain(yoy, core)], ignore_index=True)
    raise ValueError(scheme)


def aggregate(ind, metrics=("gR", "gL", "gRPE"), how="median", core=None):
    """Cross-firm aggregate per quarter. how = median | mean | revw (USD-revenue-weighted mean, weights = firm's
    rev_usd in the same quarter; lti/mindtree use their own revenue, ltim_chain uses LTI+Mindtree / LTIM revenue)."""
    if how == "median":
        return ind.groupby("cal_q")[list(metrics)].median()
    if how == "mean":
        return ind.groupby("cal_q")[list(metrics)].mean()
    if how == "revw":
        w = core[["firm", "cal_q", "rev_usd"]].copy()
        lm = core[core.firm.isin(["lti", "mindtree"])].groupby("cal_q").rev_usd.sum(min_count=2)
        lt = core[core.firm == "ltim"].set_index("cal_q").rev_usd
        ch = pd.concat([lm[lm.index <= "2022Q1"], lt[lt.index >= "2022Q2"]])
        w = pd.concat([w, pd.DataFrame(dict(firm="ltim_chain", cal_q=ch.index, rev_usd=ch.values))], ignore_index=True)
        d = ind.merge(w, on=["firm", "cal_q"], how="left")
        out = {}
        for m in metrics:
            x = d[d[m].notna() & d.rev_usd.notna()]
            out[m] = x.groupby("cal_q").apply(lambda g: np.average(g[m], weights=g.rev_usd), include_groups=False)
        return pd.DataFrame(out)
    raise ValueError(how)


def count_firms(ind, metrics=("gR", "gL")):
    return ind.groupby("cal_q")[list(metrics)].count()
