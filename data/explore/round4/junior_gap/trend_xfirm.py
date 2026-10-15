"""Designs 2 and 3 (firm scope): counterfactual trend and cross-firm boom-size comparison.

Works on log-odds of the under-30 share: logit(s) = ln(J/E), so a change in logit(s) is exactly
g_J - g_E (log points), the M4 observable. s_J - s_E = -(deviation of g_J - g_E from its counterfactual).

Design 2, per firm:
  pretrend  = OLS slope of logit(s) on fiscal year over the pre-boom years (<= FY21)
  dev_post  = annualised [logit(s_L) - logit(s_FY23)] - pretrend        (FY23 -> latest window)
  dev_cycle = annualised [logit(s_L) - logit(s_base)] - pretrend        (FY21 -> latest: spans boom and bust)
  bump B    = logit(s_FY23) - [logit(s_base) + (2023-base)*pretrend]    (excess junior share built in the boom)
  Boom-adjusted path: counterfactual at L = trend + r*B, r = share of the bump still present at L.
     r = 0  -> bump fully unwound by L (equals dev_cycle);  r = (1-d)^(L-2023) -> passive decay, d = annual
     outflow of the boom cohort from the under-30 pool (exits + ageing, 0.20-0.30 from the stock-flow).
  Breakdown: fraction of the bump that must unwind by L for the FY23->L deviation to be zero
     = -cum_dev_post / B (>1 means the boom cannot explain the gap even if fully unwound).

Design 3: regress the raw FY23->latest annual change in logit(s) on boom size across firms.
Inputs: round3/seniority_firms/under30_panel.csv, workforce/firm_year_junior_metrics.csv,
        workforce/workforce_firm_tidy.csv (Infosys job levels, LTI/Mindtree counts).
Outputs: design2_firm_trend.csv, design3_crossfirm.csv, design3_regressions.csv, infosys_joblevel_trend.csv
"""
import pathlib
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[3]
P = pd.read_csv(ROOT / "data/explore/round3/seniority_firms/under30_panel.csv")
B = pd.read_csv(ROOT / "data/explore/workforce/firm_year_junior_metrics.csv")
W = pd.read_csv(ROOT / "data/explore/workforce/workforce_firm_tidy.csv")
logit = lambda s: np.log(s / (100 - s))

# Under-30 share series. Large firms: workforce metrics (longer history); mid-tier: round3 panel.
S = {}
for f in ["infosys", "tcs", "hcltech", "wipro", "techm"]:
    x = B[B.firm == f].set_index("fy").sh_lt30.dropna()
    S[f] = x
# Wipro FY16-17 values are printed as round '60' (approximate): excluded from the trend
S["wipro"] = S["wipro"][S["wipro"].index >= 2019]
# LTIMindtree: combine LTI + Mindtree counts pre-merger where both exist (FY18, FY20); FY19 LTI from share x HC.
def cnt(firm, fy):
    x = W[(W.firm == firm) & (W.fiscal_year == fy) & (W.metric == "employees_by_age")]
    d = x.set_index("dimension").value_num
    if {"age_lt30", "age_30_50"} <= set(d.index) and d["age_lt30"] > 100:
        return d["age_lt30"], d["age_30_50"] + d.get("age_gt50", 0)
    return None
lt = {}
for fy in [2018, 2019, 2020]:
    m = cnt("mindtree", fy); l = cnt("lti", fy)
    if l is None:  # FY19: share only
        sh = B[(B.firm == "lti") & (B.fy == fy)].sh_lt30.iloc[0]; hc = B[(B.firm == "lti") & (B.fy == fy)].hc.iloc[0]
        l = (sh / 100 * hc, (1 - sh / 100) * hc)
    lt[fy] = 100 * (m[0] + l[0]) / (m[0] + l[0] + m[1] + l[1])
S["ltimindtree"] = pd.concat([pd.Series(lt), B[B.firm == "ltimindtree"].set_index("fy").sh_lt30])
for f in ["persistent", "mphasis", "hexaware", "coforge"]:
    S[f] = P[P.firm == f].set_index("fy").hc_share_lt30.dropna()
S["mindtree_only"] = B[B.firm == "mindtree"].set_index("fy").sh_lt30.dropna()

LARGE = ["infosys", "tcs", "hcltech", "wipro", "techm", "ltimindtree"]
MID = ["persistent", "mphasis", "hexaware", "coforge"]
rows = []
for f, s in S.items():
    if f == "mindtree_only":
        continue
    L = int(s.index.max())
    pre = s[s.index <= 2021]
    if f == "ltimindtree":
        base = 2020
    elif 2021 in s.index:
        base = 2021
    elif 2022 in s.index:
        base = 2022
    else:
        base = None
    r = dict(firm=f, tier="large" if f in LARGE else "mid", latest=L, base_year=base,
             pre_years=f"{int(pre.index.min())}-{int(pre.index.max())}" if len(pre) >= 2 else "",
             n_pre=len(pre))
    r["pretrend"] = np.polyfit(pre.index, logit(pre.values), 1)[0] if len(pre) >= 2 else np.nan
    r["pretrend_share_pp"] = np.polyfit(pre.index, pre.values, 1)[0] if len(pre) >= 2 else np.nan
    if 2023 in s.index and L > 2023:
        r["chg_post_raw"] = (logit(s[L]) - logit(s[2023])) / (L - 2023)
        r["dev_post"] = r["chg_post_raw"] - r["pretrend"]
    if base is not None and L > base:
        r["chg_cycle_raw"] = (logit(s[L]) - logit(s[base])) / (L - base)
        r["dev_cycle"] = r["chg_cycle_raw"] - r["pretrend"]
    if base is not None and 2023 in s.index:
        r["boom_raw"] = logit(s[2023]) - logit(s[base])           # raw change base -> FY23
        r["bump_B"] = r["boom_raw"] - (2023 - base) * r["pretrend"]
        if r.get("dev_post") is not None and not np.isnan(r["bump_B"]):
            cum = r["dev_post"] * (L - 2023)
            r["cum_dev_post"] = cum
            r["breakdown_unwind_share"] = -cum / r["bump_B"] if r["bump_B"] > 0 else np.inf
            for d in [0.20, 0.30]:
                rr = (1 - d) ** (L - 2023)
                r[f"dev_passive_d{int(d*100)}"] = (cum + (1 - rr) * r["bump_B"]) / (L - 2023)
    rows.append(r)
D2 = pd.DataFrame(rows)
for c in ["pretrend", "chg_post_raw", "dev_post", "chg_cycle_raw", "dev_cycle", "boom_raw", "bump_B",
          "cum_dev_post", "dev_passive_d20", "dev_passive_d30"]:
    D2[c + "_pp"] = D2[c] * 100
D2["sJsE_post_noboom_pp"] = -D2["dev_post_pp"]              # FY23->L, no boom correction
D2["sJsE_passive_d20_pp"] = -D2["dev_passive_d20_pp"]       # partial (passive) unwinding of the bump
D2["sJsE_passive_d30_pp"] = -D2["dev_passive_d30_pp"]
D2["sJsE_fullcycle_pp"] = -D2["dev_cycle_pp"]               # bump fully unwound by L
keep = ["firm", "tier", "base_year", "latest", "pre_years", "n_pre", "pretrend_share_pp", "pretrend_pp",
        "chg_post_raw_pp", "dev_post_pp", "chg_cycle_raw_pp", "dev_cycle_pp", "boom_raw_pp", "bump_B_pp",
        "cum_dev_post_pp", "breakdown_unwind_share", "sJsE_post_noboom_pp", "sJsE_passive_d20_pp",
        "sJsE_passive_d30_pp", "sJsE_fullcycle_pp"]
D2 = D2[keep]
D2.round(3).to_csv(HERE / "design2_firm_trend.csv", index=False)
pd.set_option("display.width", 260); pd.set_option("display.max_columns", 40)
print(D2.round(2).to_string())

# Pooled large-firm numbers (simple mean and headcount-weighted mean over firms with a pre-trend)
hc = B[B.fy == 2023].set_index("firm").hc
lg = D2[(D2.tier == "large") & D2.pretrend_pp.notna()].set_index("firm")
pool = []
for c in ["pretrend_pp", "dev_post_pp", "dev_cycle_pp", "sJsE_post_noboom_pp", "sJsE_passive_d20_pp",
          "sJsE_passive_d30_pp", "sJsE_fullcycle_pp", "bump_B_pp", "cum_dev_post_pp"]:
    v = lg[c].dropna(); w = hc.reindex(v.index)
    pool.append(dict(metric=c, n=len(v), mean=v.mean(), median=v.median(), hc_weighted=np.average(v, weights=w),
                     min=v.min(), max=v.max()))
pool = pd.DataFrame(pool)
pool.round(3).to_csv(HERE / "design2_pooled_large.csv", index=False)
print(pool.round(2).to_string())

# Excluding TCS (chart-read, India-only) and HCL (2-point pre-trend) as a robustness set
rob = lg.drop(index=[i for i in ["tcs", "hcltech"] if i in lg.index])
print("robust set", list(rob.index), rob[["sJsE_post_noboom_pp", "sJsE_passive_d20_pp", "sJsE_fullcycle_pp"]].mean().round(2).to_dict())

# ---------------- Design 3: cross-firm ----------------
# Boom measures: (a) raw change in logit(s) base->FY23; (b) under-30 hires FY22+FY23 relative to base-year under-30 HC.
hires = {}
def h(firm, fy):
    x = B[(B.firm == firm) & (B.fy == fy)].hires_lt30
    return x.iloc[0] if len(x) and not np.isnan(x.iloc[0]) else np.nan
J = lambda firm, fy: B[(B.firm == firm) & (B.fy == fy)].eval("sh_lt30/100*hc").iloc[0]
hires["infosys"] = (h("infosys", 2022) + h("infosys", 2023)) / J("infosys", 2021)
hires["wipro"] = (h("wipro", 2022) + h("wipro", 2023)) / J("wipro", 2021)
hires["techm"] = (h("techm", 2022) + h("techm", 2023)) / J("techm", 2021)
M = pd.read_csv(ROOT / "data/explore/round3/seniority_firms/midtier_age_tables.csv")
def mv(firm, fy, metric, band="<30"):
    x = M[(M.firm == firm) & (M.fiscal_year == fy) & (M.metric == metric) & (M.age_band == band)]
    x = x[~x.scope.fillna("").str.startswith("Level x age") & ~x.scope.fillna("").str.lower().str.startswith("contractual")]
    return x.value.iloc[-1]
hires["hexaware"] = (mv("Hexaware", "CY2022", "hires_by_age") + mv("Hexaware", "CY2023", "hires_by_age")) / mv("Hexaware", "CY2021", "headcount_by_age")
hires["mphasis"] = (mv("Mphasis", "FY22", "hires_by_age") + mv("Mphasis", "FY23", "hires_by_age")) / 10497  # FY21 <30 = sum of level rows
hires["persistent"] = (mv("Persistent", "FY22", "hires_by_age") + mv("Persistent", "FY23", "hires_by_age")) / mv("Persistent", "FY22", "headcount_by_age")
X = D2.set_index("firm")[["tier", "base_year", "latest", "boom_raw_pp", "chg_post_raw_pp", "pretrend_pp", "dev_post_pp"]].copy()
X["boom_hires_ratio"] = pd.Series(hires)
X = X[X.boom_raw_pp.notna() & X.chg_post_raw_pp.notna()]
X.round(3).to_csv(HERE / "design3_crossfirm.csv")
print(X.round(2).to_string())

def ols(y, x):
    Xm = np.column_stack([np.ones(len(x)), x]); b, *_ = np.linalg.lstsq(Xm, y, rcond=None)
    e = y - Xm @ b; n, k = Xm.shape
    s2 = e @ e / (n - k) if n > k else np.nan
    V = s2 * np.linalg.inv(Xm.T @ Xm)
    return b, np.sqrt(np.diag(V)), n
reg = []
for lab, sub, ycol, xcol in [
        ("all firms: raw post change on raw boom", X, "chg_post_raw_pp", "boom_raw_pp"),
        ("large firms: dev_post on raw boom", X[X.pretrend_pp.notna()], "dev_post_pp", "boom_raw_pp"),
        ("firms with hires data: raw post change on hires ratio", X[X.boom_hires_ratio.notna()], "chg_post_raw_pp", "boom_hires_ratio")]:
    b, se, n = ols(sub[ycol].values, sub[xcol].values)
    reg.append(dict(spec=lab, n=n, intercept=b[0], intercept_se=se[0], slope=b[1], slope_se=se[1],
                    firms=",".join(sub.index)))
reg = pd.DataFrame(reg)
reg.round(3).to_csv(HERE / "design3_regressions.csv", index=False)
print(reg.round(2).to_string())

# ---------------- Infosys job levels (role-based junior: JL3 and below) ----------------
g = W[(W.firm == "infosys") & (W.metric == "headcount_by_grade")].pivot_table(index="fiscal_year", columns="dimension", values="value_num", aggfunc="first")
g["rest"] = g[["grade_middle", "grade_senior"]].sum(axis=1) + g["grade_top"].fillna(0)
g["log_ratio"] = np.log(g.grade_junior / g.rest)
pre = g.loc[2014:2021]
pt = np.polyfit(pre.index, pre.log_ratio, 1)[0]
jl = dict(pretrend_pp=pt * 100,
          chg_post_raw_pp=(g.log_ratio[2026] - g.log_ratio[2023]) / 3 * 100,
          chg_cycle_raw_pp=(g.log_ratio[2026] - g.log_ratio[2021]) / 5 * 100)
jl["dev_post_pp"] = jl["chg_post_raw_pp"] - jl["pretrend_pp"]
jl["dev_cycle_pp"] = jl["chg_cycle_raw_pp"] - jl["pretrend_pp"]
jl["bump_B_pp"] = (g.log_ratio[2023] - g.log_ratio[2021] - 2 * pt) * 100
jl["breakdown_unwind_share"] = -jl["dev_post_pp"] * 3 / jl["bump_B_pp"]
pd.DataFrame([jl]).round(3).to_csv(HERE / "infosys_joblevel_trend.csv", index=False)
print("Infosys JL3-and-below vs rest:", {k: round(v, 2) for k, v in jl.items()})
print(g[["grade_junior", "rest", "log_ratio"]].round(3).to_string())

# ---------------- Design 2b: growth-conditioned counterfactual ----------------
# In a pyramid firm juniors enter through hiring, so the junior share rises with growth and falls when growth
# slows, independent of AI. Fit  d logit(s)_it = a_i + b*gR_it + c*gR_i,t-1  on years <= FY23 (pre + boom),
# predict FY24-latest from actual revenue growth, and read the residual as -(s_J - s_E).
# Six large firms only (consecutive-year shares needed); LTI/Mindtree pre-merger excluded (entity change).
pan = []
for f in ["infosys", "tcs", "hcltech", "wipro", "techm"]:
    b = B[B.firm == f].set_index("fy").sort_index()
    if f == "wipro":
        b = b[b.index >= 2019]
    s = b.sh_lt30
    for t in b.index:
        if t - 1 in s.index and not np.isnan(s.get(t, np.nan)) and not np.isnan(s[t - 1]) and t - 1 in b.index:
            pan.append(dict(firm=f, fy=t, dlogit=(logit(s[t]) - logit(s[t - 1])) * 100, gR=b.gR.get(t, np.nan),
                            gR_l1=b.gR.get(t - 1, np.nan)))
pan = pd.DataFrame(pan).dropna()
est_s = pan[pan.fy <= 2023]; post = pan[pan.fy >= 2024]
firms = sorted(pan.firm.unique())
def design(d):
    Xf = np.column_stack([(d.firm == f).astype(float) for f in firms] + [d.gR, d.gR_l1])
    return Xf
Xe = design(est_s); be, *_ = np.linalg.lstsq(Xe, est_s.dlogit.values, rcond=None)
e = est_s.dlogit.values - Xe @ be
dof = len(e) - Xe.shape[1]
s2 = e @ e / dof
V = s2 * np.linalg.pinv(Xe.T @ Xe)
post = post.copy(); post["pred"] = design(post) @ be; post["resid"] = post.dlogit - post.pred
print("growth coefs b, c:", be[-2:].round(3), "se", np.sqrt(np.diag(V))[-2:].round(3), "n", len(e), "dof", dof, "resid sd", np.sqrt(s2).round(2))
print(post.round(2).to_string())
g2b = post.groupby("firm").resid.mean()
print("mean residual by firm (pp/yr, = -(sJ-sE)):", g2b.round(2).to_dict(), "pooled", round(post.resid.mean(), 2),
      "se of pooled mean (resid sd / sqrt n)", round(np.sqrt(s2 / len(post)), 2))
out = post.assign(sJsE_pp=-post.resid)
out.round(3).to_csv(HERE / "design2b_growth_conditioned.csv", index=False)
pd.DataFrame(dict(term=["gR", "gR_lag1"], coef=be[-2:], se=np.sqrt(np.diag(V))[-2:], n_est=len(e), resid_sd=np.sqrt(s2))).round(4).to_csv(HERE / "design2b_coefs.csv", index=False)
