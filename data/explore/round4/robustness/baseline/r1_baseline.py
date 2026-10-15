"""R1 robustness: how the Part A decomposition depends on the counterfactual baseline (top six, simple average).

    python3 data/explore/round4/robustness/baseline/r1_baseline.py

Inputs (read only):
  output/final/table_A.csv          group rows (Indian simple average) -> reproduces the synthesis numbers
  output/final/table_A_firms.csv    firm-level FY growth (log x 100) for the six Indian entities + ACN, CTSH
  data/corrected/core_quarterly_final.csv, yoy_metrics_final.csv
                                    pre-FY16 firm growth for the deceleration slope (counterfactual d)
  data/explore/round4/demand_shift/d_bounds.csv   M5 measured demand shifts

Outputs (this folder):
  r1_firm_counterfactuals.csv   firm x metric x counterfactual: actual FY24-26 mean, counterfactual, gap
  r1_deceleration_slope.csv     FY12-FY20 growth-on-year slopes used in (d)
  r1_pre_fy16_growth.csv        the firm-year growth series behind those slopes
  r1_counterfactuals.csv        group-level counterfactual, delta g_L and delta g_R per counterfactual
  r1_decomposition.csv          delta g_Q, delta d, AI share, residual vs M5, for s_bar in {0, 1.2, 2.5}
  r1_summary.csv                one row per counterfactual (central values and ranges) -> FINDINGS table
  r1_comparators_levels.csv     ACN/CTSH: FY21-23 overshoot vs FY16-20 trend and level-based delta (hangover check)
  r1_level_gaps_group.csv       group log-level gaps vs FY16-20 trend at FY23 and FY26 (headcount, cc revenue, RPE, util, residual)

Conventions. Growth = log change x 100, same definitions as table_A (headcount = average-based; revenue cc
aggregated from firm-reported cc YoY with prior-year USD weights). "Actual" = mean of FY24, FY25, FY26.
Every delta is averaged over the firms that have both the actual and the counterfactual (matched firms); the
synthesis' unmatched table_A numbers are reproduced in row a0 for reference.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent

S_BAR = {"low": 0.0, "central": 1.2, "high": 2.5}
PHI_S = 0.2          # M2: AI-driven price cut, FY24-26 (held fixed across s_bar; it is measured separately)
INDIAN = ["tcs", "infosys", "hcltech", "wipro", "techm", "lti_group"]
COMP = ["accenture", "cognizant"]
METRICS = {"headcount": "L", "rev_cc": "R", "rev_usd": "R_usd"}

F = pd.read_csv(ROOT / "output/final/table_A_firms.csv")
F = F[~F.period.str.contains("Q1")].copy()
F["fy"] = F.period.str[2:].astype(int) + 2000
A = pd.read_csv(ROOT / "output/final/table_A.csv")
A = A[(A.group == "Indian simple average") & ~A.period.str.contains("Q1")].copy()
A["fy"] = A.period.str[2:].astype(int) + 2000


def series(firm, metric):
    s = F[F.firm == firm].set_index("fy")[metric]
    return s


def mean_years(s, y0, y1):
    v = s.loc[y0:y1].dropna()
    return v.mean() if len(v) else np.nan


# ---------------------------------------------------------------- (d) deceleration slope from FY12-FY20
core = pd.read_csv(ROOT / "data/corrected/core_quarterly_final.csv", dtype={"cal_q": str})
yoy = pd.read_csv(ROOT / "data/corrected/yoy_metrics_final.csv", dtype={"cal_q": str})
q = yoy.merge(core[["firm", "cal_q", "rev_usd"]], on=["firm", "cal_q"], how="left").set_index(["firm", "cal_q"])


def qadd(qq, k):
    y, n = int(qq[:4]), int(qq[-1])
    t = y * 4 + n - 1 + k
    return f"{t // 4}Q{t % 4 + 1}"


def fy_quarters(fy):
    return [f"{fy - 1}Q2", f"{fy - 1}Q3", f"{fy - 1}Q4", f"{fy}Q1"]


def fy_metrics(firm, fy):
    """Same aggregation as scripts/final/tables_figures.py:fy_metrics (all four quarters required)."""
    qs = fy_quarters(fy)
    get = lambda col, qq: q[col].get((firm, qq), np.nan)
    base = np.array([get("rev_usd", qadd(x, -4)) for x in qs], float)
    out = {}
    for lab, col in [("rev_usd", "gR_usd"), ("rev_cc", "gR")]:
        g = np.array([get(col, x) for x in qs], float)
        ok = np.isfinite(g).all() and np.isfinite(base).all()
        out[lab] = 100 * np.log((base * np.exp(g / 100)).sum() / base.sum()) if ok else np.nan
    g = np.array([get("gL", x) for x in qs], float)
    out["headcount"] = g.mean() if np.isfinite(g).all() else np.nan
    return out


# LTI group has no pre-FY16 data; Wipro FY16-20 headcount is excluded in table_A (decision 3) and TechM's
# pre-FY16 perimeter differs (Mahindra Satyam merger, 2013), so its FY12 point is dropped.
pre_rows = []
for f in ["tcs", "infosys", "hcltech", "wipro", "techm"]:
    for fy in range(2009, 2021):
        m = fy_metrics(f, fy)
        pre_rows.append(dict(firm=f, fy=fy, **m))
P = pd.DataFrame(pre_rows)
# use table_A_firms for FY16-20 (identical definitions, includes the audit exclusions)
for f in ["tcs", "infosys", "hcltech", "wipro", "techm"]:
    for fy in range(2016, 2021):
        for m in METRICS:
            P.loc[(P.firm == f) & (P.fy == fy), m] = series(f, m).get(fy, np.nan)
P.loc[P.firm == "techm", ["rev_usd", "rev_cc", "headcount"]] = P.loc[P.firm == "techm", ["rev_usd", "rev_cc", "headcount"]].where(P.fy >= 2016)
P.round(3).to_csv(OUT / "r1_pre_fy16_growth.csv", index=False)

# check: the re-implementation reproduces table_A_firms where both exist (before overwrite they were computed)
chk = []
for f in ["tcs", "infosys"]:
    for fy in range(2016, 2021):
        m = fy_metrics(f, fy)
        for k in METRICS:
            chk.append(abs(m[k] - series(f, k).get(fy)) if np.isfinite(m[k]) else 0)
assert max(chk) < 0.01, max(chk)


def fe_slope(df, metric, y0, y1, firms):
    d = df[(df.fy >= y0) & (df.fy <= y1) & df.firm.isin(firms)].dropna(subset=[metric]).copy()
    d = d[d.groupby("firm")[metric].transform("count") >= 2]
    d["x"] = d.fy - d.groupby("firm").fy.transform("mean")
    d["y"] = d[metric] - d.groupby("firm")[metric].transform("mean")
    b = (d.x * d.y).sum() / (d.x ** 2).sum()
    resid = d.y - b * d.x
    k = d.firm.nunique()
    se = np.sqrt((resid ** 2).sum() / max(len(d) - k - 1, 1) / (d.x ** 2).sum())
    return b, se, len(d), ";".join(sorted(d.firm.unique()))


slopes = []
# USD revenue is used as the revenue slope for cc too (TCS has no cc YoY before FY16)
for metric in ["headcount", "rev_usd", "rev_cc"]:
    for lab, y0, y1, firms in [
        ("FY12-20, TCS+Infosys (continuous series)", 2012, 2020, ["tcs", "infosys"]),
        ("FY12-20, all Indian firms with data (FE)", 2012, 2020, ["tcs", "infosys", "hcltech", "wipro", "techm"]),
        ("FY13-20, TCS+Infosys (drops FY12 post-GFC rebound)", 2013, 2020, ["tcs", "infosys"]),
        ("FY16-20, top-six firms (FE, window only)", 2016, 2020, INDIAN),
    ]:
        src = P if y0 < 2016 else F[F.firm.isin(INDIAN)]
        b, se, n, fs = fe_slope(src, metric, y0, y1, firms)
        slopes.append(dict(metric=metric, sample=lab, slope_pp_per_yr=b, se=se, n_obs=n, firms=fs))
SL = pd.DataFrame(slopes)
SL.round(3).to_csv(OUT / "r1_deceleration_slope.csv", index=False)


def slope(metric, sample, cc_own=False):
    m = "rev_usd" if (metric == "rev_cc" and sample[:4] in ("FY12", "FY13") and not cc_own) else metric
    return SL[(SL.metric == m) & (SL["sample"] == sample)].slope_pp_per_yr.iloc[0]


# ---------------------------------------------------------------- comparators (e)
comp_delta = {}
for metric in METRICS:
    for c in COMP:
        s = series(c, metric)
        comp_delta[(c, metric)] = mean_years(s, 2024, 2026) - mean_years(s, 2016, 2020)
    comp_delta[("avg", metric)] = np.mean([comp_delta[(c, metric)] for c in COMP])

comp_rows = []
for c in COMP:
    for metric in METRICS:
        s_ = series(c, metric)
        g0_ = mean_years(s_, 2016, 2020)
        act_ = mean_years(s_, 2024, 2026)
        boom_ = s_.loc[2021:2023]
        cf_c = (6 * g0_ - boom_.sum()) / 3
        comp_rows.append(dict(firm=c, metric=metric, base_fy16_20=g0_, n_base_years=int(s_.loc[2016:2020].notna().sum()),
                              sum_fy21_23=boom_.sum(), overshoot_vs_trend_by_fy23=boom_.sum() - 3 * g0_,
                              actual_fy24_26=act_, delta_vs_a=act_ - g0_, cf_level_c=cf_c, delta_vs_c=act_ - cf_c))
for metric in METRICS:   # same numbers for the Indian matched panel, for comparison
    s_ = F[F.firm.isin(INDIAN)].pivot(index="fy", columns="firm", values=metric)
    ok = [f for f in INDIAN if s_.loc[2016:2020, f].notna().any() and s_.loc[2021:2026, f].notna().all()]
    g0_ = s_.loc[2016:2020, ok].mean().mean()
    comp_rows.append(dict(firm="indian_matched_avg", metric=metric, base_fy16_20=g0_, n_base_years=np.nan,
                          sum_fy21_23=s_.loc[2021:2023, ok].sum().mean(),
                          overshoot_vs_trend_by_fy23=(s_.loc[2021:2023, ok].sum() - 3 * s_.loc[2016:2020, ok].mean()).mean(),
                          actual_fy24_26=s_.loc[2024:2026, ok].mean().mean(), delta_vs_a=np.nan, cf_level_c=np.nan,
                          delta_vs_c=np.nan, ))
pd.DataFrame(comp_rows).round(3).to_csv(OUT / "r1_comparators_levels.csv", index=False)

# ---------------------------------------------------------------- firm-level counterfactuals
CF_LABEL = {
    "a": "FY16-20 mean (current)",
    "b": "FY16-23 mean (incl. FY21 dip and FY22-23 boom)",
    "c": "Level trend: FY20 level + FY16-20 mean growth; FY24-26 growth needed to reach trend by FY26",
    "c_fit": "Level trend: OLS line through FY15/16-FY20 log levels, reach trend by FY26",
    "c21": "Level trend anchored at FY21 (COVID dip kept as permanent; only FY22-23 boom treated as pull-forward)",
    "d": "Decelerating: FY16-20 mean + 7 x slope (slope: FY12-20, TCS+Infosys)",
    "d_fe": "Decelerating: slope FY12-20, all Indian firms with data (FE)",
    "d13": "Decelerating: slope FY13-20, TCS+Infosys",
    "d_cc": "Decelerating: as d, but cc revenue uses its own FY12-20 cc slope (Infosys FY12-20 + TCS FY16-20)",
    "d_win": "Decelerating: slope fitted within FY16-20 (top six, FE) [check only: window shows no deceleration]",
    "e": "DiD: FY16-20 mean + avg(ACN, CTSH) change FY16-20 -> FY24-26",
    "e_acn": "DiD with Accenture only",
    "e_ctsh": "DiD with Cognizant only",
}

rows = []
for f in INDIAN:
    for metric in METRICS:
        s = series(f, metric)
        act = mean_years(s, 2024, 2026) if s.loc[2024:2026].notna().all() else np.nan
        g0 = mean_years(s, 2016, 2020)
        cf = {}
        cf["a"] = g0
        cf["b"] = mean_years(s, 2016, 2023)
        boom = s.loc[2021:2023]
        cf["c"] = (6 * g0 - boom.sum()) / 3 if boom.notna().all() and np.isfinite(g0) else np.nan
        cf["c21"] = (5 * g0 - s.loc[2022:2023].sum()) / 3 if s.loc[2022:2023].notna().all() and np.isfinite(g0) else np.nan
        # OLS on log level index built from consecutive growths ending FY20
        base = s.loc[2016:2020]
        if base.notna().all():
            yrs, lvl = [2015], [0.0]
        else:
            first = base.first_valid_index()
            ok = first is not None and base.loc[first:].notna().all()
            yrs, lvl = ([first], [0.0]) if ok else ([], [])
            base = base.loc[first:] if ok else base.iloc[0:0]
            if ok:
                base = base.iloc[1:]
        for y, g in base.items():
            yrs.append(y)
            lvl.append(lvl[-1] + g)
        if len(yrs) >= 3 and boom.notna().all():
            bb, aa = np.polyfit(yrs, lvl, 1)
            lvl23 = lvl[-1] + boom.sum()
            cf["c_fit"] = ((aa + bb * 2026) - lvl23) / 3
        else:
            cf["c_fit"] = np.nan
        cf["d"] = g0 + 7 * slope(metric, "FY12-20, TCS+Infosys (continuous series)")
        cf["d_fe"] = g0 + 7 * slope(metric, "FY12-20, all Indian firms with data (FE)")
        cf["d13"] = g0 + 7 * slope(metric, "FY13-20, TCS+Infosys (drops FY12 post-GFC rebound)")
        cf["d_cc"] = g0 + 7 * slope(metric, "FY12-20, TCS+Infosys (continuous series)", cc_own=True)
        cf["d_win"] = g0 + 7 * slope(metric, "FY16-20, top-six firms (FE, window only)")
        cf["e"] = g0 + comp_delta[("avg", metric)]
        cf["e_acn"] = g0 + comp_delta[("accenture", metric)]
        cf["e_ctsh"] = g0 + comp_delta[("cognizant", metric)]
        for k, v in cf.items():
            rows.append(dict(firm=f, metric=metric, cf=k, actual_fy24_26=act, counterfactual=v,
                             gap=act - v if np.isfinite(act) and np.isfinite(v) else np.nan,
                             n_base_years=int(s.loc[2016:2020].notna().sum())))
FC = pd.DataFrame(rows)
FC.round(3).to_csv(OUT / "r1_firm_counterfactuals.csv", index=False)

# ---------------------------------------------------------------- group level
grp = []
for k in CF_LABEL:
    r = dict(cf=k, label=CF_LABEL[k])
    for metric, sym in METRICS.items():
        d = FC[(FC.cf == k) & (FC.metric == metric)].dropna(subset=["gap"])
        r[f"cf_{sym}"] = d.counterfactual.mean()
        r[f"actual_{sym}"] = d.actual_fy24_26.mean()
        r[f"dg_{sym}"] = d.gap.mean()
        r[f"dg_{sym}_se_across_firms"] = d.gap.std(ddof=1) / np.sqrt(len(d)) if len(d) > 1 else np.nan
        r[f"n_{sym}"] = len(d)
        r[f"firms_{sym}"] = ";".join(d.firm)
    grp.append(r)
G = pd.DataFrame(grp)

# a0: the synthesis numbers (table_A group rows, unmatched panel)
a0 = dict(cf="a0", label="FY16-20 mean, table_A group rows (synthesis; unmatched firm sets)")
b0 = dict(cf="b0", label="FY16-23 mean, table_A group rows (unmatched firm sets)")
for metric, sym in METRICS.items():
    s = A[A.metric == metric].set_index("fy").value
    act = s.loc[2024:2026].mean()
    for row, (y0, y1) in [(a0, (2016, 2020)), (b0, (2016, 2023))]:
        row[f"cf_{sym}"] = s.loc[y0:y1].mean()
        row[f"actual_{sym}"] = act
        row[f"dg_{sym}"] = act - s.loc[y0:y1].mean()
G = pd.concat([pd.DataFrame([a0, b0]), G], ignore_index=True)
G.round(3).to_csv(OUT / "r1_counterfactuals.csv", index=False)

# ---------------------------------------------------------------- decomposition
DB = pd.read_csv(ROOT / "data/explore/round4/demand_shift/d_bounds.csv").set_index("component")
m5 = DB.loc["delta_d total: vendor (excl. GCC), US-weighted"]
gcc = DB.loc["delta_d_share via GCC (India, vendor scope only)"]

dec = []
for _, r in G.iterrows():
    is_did = r.cf.startswith("e")
    # For DiD the delta is India minus comparators: common shocks (US market, US in-housing, any AI common to
    # all vendors) difference out. The comparable measured shift is the India-specific part of M5 (GCC
    # channel, itself an upper bound since GCCs also take work from ACN/CTSH India delivery).
    M5c, M5lo, M5hi = (gcc.central, gcc.low, gcc.high) if is_did else (m5.central, m5.low, m5.high)
    for case, s in S_BAR.items():
        dL, dR = r.dg_L, r.dg_R
        dQ_L = dL + s
        dQ_R = dR + PHI_S
        dd = dQ_L  # delta d ~ delta g_Q (eps * phi s_bar <= 0.3)
        dec.append(dict(
            cf=r.cf, label=r.label, s_bar_case=case, s_bar=s, dg_L=dL, dg_R=dR,
            dg_Q_from_L=dQ_L, dg_Q_from_R=dQ_R, L_minus_R_route=dQ_L - dQ_R,
            delta_d=dd,
            ai_share_of_L_slowdown=(s / -dL) if dL < 0 else np.nan,
            m5_used="GCC channel only (India-specific)" if is_did else "vendor total excl. GCC",
            m5_central=M5c, m5_low=M5lo, m5_high=M5hi,
            residual_central_m5=dd - M5c,
            residual_if_m5_low=dd - M5lo, residual_if_m5_high=dd - M5hi,
            residual_R_route_central_m5=dQ_R - M5c,
        ))
D = pd.DataFrame(dec)
D.round(3).to_csv(OUT / "r1_decomposition.csv", index=False)

summ = []
for k, g in D.groupby("cf", sort=False):
    c = g[g.s_bar_case == "central"].iloc[0]
    rr = g.residual_if_m5_low.tolist() + g.residual_if_m5_high.tolist()
    rG = G[G.cf == k].iloc[0]
    summ.append(dict(cf=k, label=c.label, dg_L=c.dg_L, dg_R_cc=c.dg_R, dg_R_usd=rG.dg_R_usd,
                     n_L=rG.n_L, n_R_cc=rG.n_R,
                     dg_Q_L_route=c.dg_Q_from_L,
                     dg_Q_L_route_lo=g.dg_Q_from_L.min(), dg_Q_L_route_hi=g.dg_Q_from_L.max(),
                     dg_Q_R_route_cc=c.dg_Q_from_R, dg_Q_R_route_usd=rG.dg_R_usd + PHI_S,
                     ai_share_central=c.ai_share_of_L_slowdown,
                     ai_share_at_s2_5=g[g.s_bar_case == "high"].ai_share_of_L_slowdown.iloc[0],
                     m5_central=c.m5_central,
                     residual_L_route=c.residual_central_m5, residual_L_route_min=min(rr), residual_L_route_max=max(rr),
                     residual_R_route_cc=c.residual_R_route_central_m5,
                     residual_R_route_usd=rG.dg_R_usd + PHI_S - c.m5_central))
pd.DataFrame(summ).round(2).to_csv(OUT / "r1_summary.csv", index=False)

pd.set_option("display.width", 250)
print(SL.round(2).to_string())
print({k: round(v, 2) for k, v in comp_delta.items()})
print(G[["cf", "cf_L", "actual_L", "dg_L", "dg_L_se_across_firms", "n_L", "cf_R", "actual_R", "dg_R", "n_R", "dg_R_usd", "n_R_usd"]].round(2).to_string())
c = D[D.s_bar_case == "central"][["cf", "dg_L", "dg_R", "dg_Q_from_L", "dg_Q_from_R", "ai_share_of_L_slowdown", "residual_central_m5", "residual_R_route_central_m5"]]
print(c.round(2).to_string())

# ---------------------------------------------------------------- level check on revenue per employee (M1 under logic c)
# Cumulative FY21-FY26 growth vs 6 x the FY16-20 mean, table_A group rows (unbalanced firm sets, indicative only).
lv = []
for metric in ["headcount", "rev_cc", "rpe_cc", "util_change", "residual"]:
    s_ = A[A.metric == metric].set_index("fy").value
    g0_ = s_.loc[2016:2020].mean()
    lv.append(dict(metric=metric, base_fy16_20=g0_, cum_fy21_23=s_.loc[2021:2023].sum(),
                   gap_vs_trend_fy23=s_.loc[2021:2023].sum() - 3 * g0_,
                   cum_fy21_26=s_.loc[2021:2026].sum(), gap_vs_trend_fy26=s_.loc[2021:2026].sum() - 6 * g0_))
pd.DataFrame(lv).round(2).to_csv(OUT / "r1_level_gaps_group.csv", index=False)
print(pd.DataFrame(lv).round(2).to_string())
