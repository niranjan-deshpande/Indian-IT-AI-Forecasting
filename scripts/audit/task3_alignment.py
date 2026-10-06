"""Audit Task 1b, item 3: fiscal-year alignment, cal_q mapping checks, comparator correlations under variants.

Outputs (ROOT/audit/):
  calq_mapping_check.csv        per firm x raw file: cal_q vs period_end, fiscal_q vs period_end, collisions
  yoy_lag_consistency.csv       reported USD YoY growth vs log change over 4 calendar quarters, per firm
  comparator_corr_variants.csv  corr / mean gap / n for every variant x comparator x metric x period
  comparator_n_per_quarter.csv  number of Indian entities in the cross-firm aggregate, per quarter and scheme
  comparator_aggregates.csv     the quarterly Indian aggregate series under each variant (for inspection)
Run:  python3 scripts/audit/task3_alignment.py   [--yoy path --core path to run on corrected files]
"""
import argparse
import glob
import re
import numpy as np
import pandas as pd
from audit_common import (ROOT, AUD, EXCL, qadd, load_yoy, load_core, indian_panel, aggregate, count_firms)

ap = argparse.ArgumentParser()
ap.add_argument("--yoy", default=None)
ap.add_argument("--core", default=None)
ap.add_argument("--tag", default="")
args = ap.parse_args()

# --------------------------------------------------------------------------------------------- 1. raw mapping checks
def expected_end(firm, fq):
    """(year, month) of the quarter end implied by the firm's own fiscal label, or None if not a quarter label."""
    m = re.fullmatch(r"Q([1-4])FY(\d{2,4})", str(fq))
    if firm == "cognizant":
        m2 = re.fullmatch(r"(\d{4})Q([1-4])", str(fq))
        return (int(m2.group(1)), 3 * int(m2.group(2))) if m2 else None
    if not m:
        return None
    q, fy = int(m.group(1)), int(m.group(2))
    fy = fy + 2000 if fy < 100 else fy
    if firm == "accenture":                                 # FY ends 31 Aug: Q1 Sep-Nov ... Q4 Jun-Aug
        return {1: (fy - 1, 11), 2: (fy, 2), 3: (fy, 5), 4: (fy, 8)}[q]
    if firm == "hcltech" and fy <= 2015:                    # FY ended 30 Jun until FY15
        return {1: (fy - 1, 9), 2: (fy - 1, 12), 3: (fy, 3), 4: (fy, 6)}[q]
    if firm == "hcltech" and fy == 2016:                    # 9-month transition FY Jul-2015..Mar-2016
        return {1: (2015, 9), 2: (2015, 12), 3: (2016, 3)}.get(q, ("INVALID", q))
    return {1: (fy - 1, 6), 2: (fy - 1, 9), 3: (fy - 1, 12), 4: (fy, 3)}[q]   # Apr-Mar FY


rows = []
for f in sorted(glob.glob(str(ROOT / "data" / "raw" / "*.csv"))):
    d = pd.read_csv(f, low_memory=False, dtype={"cal_q": str})
    d["pe"] = pd.to_datetime(d.period_end, errors="coerce")
    d["cal_from_pe"] = d.pe.dt.year.astype("Int64").astype(str) + "Q" + d.pe.dt.quarter.astype("Int64").astype(str)
    for firm, g in d.groupby("firm"):
        qt = g[g.period_type.isin(["quarter", "point", "ltm"])]
        lab = qt.drop_duplicates(["fiscal_q", "period_end"])
        bad_label = 0
        for r in lab.itertuples():
            e = expected_end(firm, r.fiscal_q)
            if e is None or (r.pe.year, r.pe.month) != e:
                bad_label += 1
        rows.append(dict(
            file=f.split("/")[-1], firm=firm, rows=len(g), rows_quarterly=len(qt),
            period_end_months=",".join(str(m) for m in sorted(g.pe.dt.month.dropna().astype(int).unique())),
            n_cal_q=qt.cal_q.nunique(), first_cal_q=qt.cal_q.min(), last_cal_q=qt.cal_q.max(),
            period_end_missing=int(g.pe.isna().sum()),
            calq_ne_quarter_of_period_end=int((g.cal_from_pe != g.cal_q).sum()),
            fiscal_label_inconsistent_with_period_end=bad_label,
            calq_with_gt1_period_end=int((qt.groupby("cal_q").period_end.nunique() > 1).sum()),
            calq_with_gt1_fiscal_q=int((qt.groupby("cal_q").fiscal_q.nunique() > 1).sum()),
            fiscal_q_with_gt1_period_end=int((qt.groupby("fiscal_q").period_end.nunique() > 1).sum()),
        ))
mapchk = pd.DataFrame(rows)
mapchk.to_csv(AUD / f"calq_mapping_check{args.tag}.csv", index=False)
print(mapchk.to_string())

# --------------------------------------------------------------------------------------------- 2. YoY lag consistency
core = load_core(args.core)
yoy = load_yoy(args.yoy)
lagrows = []
for f, g in core.groupby("firm"):
    g = g.set_index("cal_q")
    for q in g.index:
        l = qadd(q, -4)
        if q >= "2015Q2" and l in g.index and pd.notna(g.rev_usd.get(q)) and pd.notna(g.rev_usd.get(l)) and pd.notna(g.rev_rep_yoy.get(q)):
            calc = 100 * (g.rev_usd[q] / g.rev_usd[l] - 1)
            lagrows.append(dict(firm=f, cal_q=q, reported_usd_yoy=g.rev_rep_yoy[q], computed_4q=calc, diff=calc - g.rev_rep_yoy[q]))
lag = pd.DataFrame(lagrows)
lag.to_csv(AUD / f"yoy_lag_consistency{args.tag}.csv", index=False)
print(lag.groupby("firm")["diff"].agg(["count", "median", lambda s: (s.abs() > 1).sum()]).rename(columns={"<lambda_0>": "n_absdiff_gt1pp"}))

# --------------------------------------------------------------------------------------------- 3. comparator variants
PERIODS = {
    "pre (2016Q1-2022Q4, ex 2020Q2-2021Q2)": ("2016Q1", "2022Q4", True),
    "post (2023Q1-2026Q2)": ("2023Q1", "2026Q2", False),
    "FY25-27 window (2024Q2-2026Q2)": ("2024Q2", "2026Q2", False),
    "pre-COVID only (2016Q1-2020Q1)": ("2016Q1", "2020Q1", False),
}


def ar1(s):
    s = s.dropna()
    return s.autocorr(1) if len(s) > 3 else np.nan


def stats(a, b, lo, hi, excl):
    j = pd.concat([a, b], axis=1, keys=["ind", "cmp"]).dropna()
    j = j[(j.index >= lo) & (j.index <= hi)]
    if excl:
        j = j[~j.index.isin(EXCL)]
    n = len(j)
    r = j.ind.corr(j.cmp) if n > 2 else np.nan
    out = dict(corr=r, mean_gap=(j.ind - j.cmp).mean(), n=n, first=j.index.min(), last=j.index.max())
    if n > 3 and pd.notna(r):
        z, se = np.arctanh(r), 1 / np.sqrt(n - 3)
        out.update(ci95_lo=np.tanh(z - 1.96 * se), ci95_hi=np.tanh(z + 1.96 * se))
        p1, p2 = ar1(j.ind), ar1(j.cmp)
        neff = n * (1 - p1 * p2) / (1 + p1 * p2) if pd.notna(p1) and pd.notna(p2) else np.nan
        out["n_eff_bartlett"] = neff
        if pd.notna(neff) and neff > 3.5:
            se2 = 1 / np.sqrt(neff - 3)
            out.update(ci95_lo_neff=np.tanh(z - 1.96 * se2), ci95_hi_neff=np.tanh(z + 1.96 * se2))
    return out


def shifted(s, k):
    """Re-index a cal_q series by k quarters (k=+1: the Nov quarter is compared with the following calendar Q1)."""
    s = s.copy()
    s.index = [qadd(q, k) for q in s.index]
    return s


def annualize(s, kind="cal"):
    """Mean of the 4 quarterly YoY values in each year; only years with all 4 quarters present and none in EXCL.
    kind='cal': calendar year (cal_q Q1..Q4). kind='indfy': Indian FY (cal_q Q2..Q1 of next year), label FYyy."""
    s = s.dropna()
    s = s[~s.index.isin(EXCL)]
    if kind == "cal":
        key = pd.Series([q[:4] for q in s.index], index=s.index)
    else:
        key = pd.Series([f"FY{(int(q[:4]) + (1 if q[-1] != '1' else 0)) % 100:02d}" for q in s.index], index=s.index)
    g = s.groupby(key)
    m = g.mean()[g.count() == 4]
    return m


cmp = {f: yoy[yoy.firm == f].set_index("cal_q") for f in ["accenture", "cognizant"]}
panels = {s: indian_panel(yoy, core, s) for s in ["pilot", "dedup", "chain"]}
aggs = {}
for s, ind in panels.items():
    for how in ["median", "mean", "revw"]:
        aggs[(s, how)] = aggregate(ind, how=how, core=core)

VARIANTS = [
    # name, scheme, how, accenture shift k, month-weighting, annual
    ("a_pilot", "pilot", "median", 0, False, None, "exactly as 03_part2.py"),
    ("a2_pilot_dedup", "dedup", "median", 0, False, None, "pilot without the 2022Q3 lti+mindtree+ltim triple entry"),
    ("b_acn_nov_to_nextQ1", "pilot", "median", +1, False, None, "Accenture Sep-Nov qtr vs Indian Jan-Mar (4-month lag; requested variant b)"),
    ("b2_acn_nov_to_Q3", "pilot", "median", -1, False, None, "Accenture Sep-Nov qtr vs Indian Jul-Sep (nearest-preceding quarter end)"),
    ("f_month_weighted", "pilot", "median", 0, True, None, "Indian aggregate re-weighted to Accenture months: 2/3 x same cal_q + 1/3 x previous cal_q"),
    ("c_annual_calendar", "pilot", "median", 0, False, "cal", "calendar-year mean of quarterly YoY; years with 4 non-excluded quarters"),
    ("c2_annual_indianFY", "pilot", "median", 0, False, "indfy", "Indian-FY mean of quarterly YoY (Accenture Mar-Feb quarters)"),
    ("d_mean", "pilot", "mean", 0, False, None, "cross-firm mean instead of median (pilot entity set)"),
    ("d2_mean_dedup", "dedup", "mean", 0, False, None, "mean, no 2022Q3 double count"),
    ("e_revenue_weighted", "dedup", "revw", 0, False, None, "USD-revenue-weighted mean (same-quarter rev_usd), no double count"),
    ("g_chain_median", "chain", "median", 0, False, None, "one LTI-group entity (growth-rate chain), median of 6"),
    ("g2_chain_mean", "chain", "mean", 0, False, None, "one LTI-group entity, mean of 6"),
    ("h_dedup_median_monthw", "dedup", "median", 0, True, None, "recommended clean variant: no double count + month weighting"),
]

out = []
for name, scheme, how, k, mw, annual, desc in VARIANTS:
    agg = aggs[(scheme, how)]
    for comp in ["accenture", "cognizant"]:
        if comp == "cognizant" and (k != 0 or mw):
            continue     # Cognizant quarters are calendar quarters: exact alignment, shifting not meaningful
        for m in ["gR", "gL"]:
            a = agg[m]
            b = cmp[comp][m]
            if comp == "accenture" and k:
                b = shifted(b, k)
            if comp == "accenture" and mw:
                a = (2 / 3) * a + (1 / 3) * shifted(a, +1)          # value at t = 2/3 a(t) + 1/3 a(t-1)
            for per, (lo, hi, ex) in PERIODS.items():
                if annual:
                    if per.startswith("FY25-27") or per.startswith("pre-COVID"):
                        continue
                    aa, bb = annualize(a, annual), annualize(b, annual)
                    if annual == "cal":
                        lo2, hi2 = lo[:4], hi[:4]
                        if per.startswith("post"):
                            hi2 = "2025"
                    else:
                        lo2 = "FY17" if per.startswith("pre") else "FY24"
                        hi2 = "FY23" if per.startswith("pre") else "FY26"
                    st = stats(aa, bb, lo2, hi2, False)
                else:
                    st = stats(a, b, lo, hi, ex)
                out.append(dict(variant=name, description=desc, comparator=comp, metric=m, period=per, **st))
res = pd.DataFrame(out)
res.to_csv(AUD / f"comparator_corr_variants{args.tag}.csv", index=False)

# n per quarter
nq = []
for s, ind in panels.items():
    c = count_firms(ind)
    c.columns = [f"n_{s}_{x}" for x in c.columns]
    nq.append(c)
nq = pd.concat(nq, axis=1)
nq = nq[(nq.index >= "2016Q1") & (nq.index <= "2026Q2")]
nq["in_pilot_window"] = np.where(nq.index.isin(EXCL), "excluded (COVID)", np.where(nq.index <= "2022Q4", "pre", "post"))
nq.to_csv(AUD / f"comparator_n_per_quarter{args.tag}.csv")

# aggregates
ag = []
for (s, how), a in aggs.items():
    x = a[["gR", "gL"]].copy()
    x.columns = [f"{c}_{s}_{how}" for c in x.columns]
    ag.append(x)
ag = pd.concat(ag, axis=1)
ag = ag.join(cmp["accenture"][["gR", "gL"]].add_prefix("acn_")).join(cmp["cognizant"][["gR", "gL"]].add_prefix("ctsh_"))
ag[(ag.index >= "2015Q2") & (ag.index <= "2026Q2")].round(3).to_csv(AUD / f"comparator_aggregates{args.tag}.csv")

piv = res[res.period.str.startswith(("pre (", "post"))].pivot_table(index=["comparator", "variant"], columns=["metric", "period"], values="corr")
print(piv.round(2).to_string())
gap = res.pivot_table(index=["comparator", "variant"], columns=["metric", "period"], values="mean_gap")
print(gap.round(2).to_string())
