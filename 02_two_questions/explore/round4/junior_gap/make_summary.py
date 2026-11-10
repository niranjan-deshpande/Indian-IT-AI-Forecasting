"""Collect s_J - s_E estimates (pp/yr; positive = AI hits juniors harder) from the design outputs into one table.
Run after stockflow.py, trend_xfirm.py and plfs_gap.py. Output: estimates_summary.csv
"""
import pathlib
import numpy as np
import pandas as pd

H = pathlib.Path(__file__).parent
rows = []
add = lambda **k: rows.append(k)

d1 = pd.read_csv(H / "design1_estimates.csv")
for _, r in d1[d1.ageing_case == "central"].iterrows():
    add(scope="firm", design="1 stock-flow (ageing channel netted, vs own FY16-21)", unit=r.firm,
        estimate=r.sJ_minus_sE_pp, lo=min(r.sJ_minus_sE_pp_no_ageing_adj, r.sJ_minus_sE_pp),
        hi=max(r.sJ_minus_sE_pp_no_ageing_adj, r.sJ_minus_sE_pp), interval="no-adjustment vs central ageing")

pool = pd.read_csv(H / "design2_pooled_large.csv").set_index("metric")
for m, lab in [("sJsE_post_noboom_pp", "2 trend, FY23->latest, no boom correction"),
               ("sJsE_passive_d20_pp", "2 trend, boom bump decays passively (d=0.20)"),
               ("sJsE_passive_d30_pp", "2 trend, boom bump decays passively (d=0.30)"),
               ("sJsE_fullcycle_pp", "2 trend, full cycle FY21->latest (bump fully unwound)")]:
    r = pool.loc[m]
    add(scope="firm", design=lab, unit="large six (mean; hc-weighted in estimate_alt)", estimate=r["mean"],
        estimate_alt=r.hc_weighted, lo=r["min"], hi=r["max"], interval="firm min-max")

g2b = pd.read_csv(H / "design2b_growth_conditioned.csv")
c2b = pd.read_csv(H / "design2b_coefs.csv")
se = c2b.resid_sd.iloc[0] / np.sqrt(len(g2b))
add(scope="firm", design="2b growth-conditioned trend (FE panel, est. <=FY23)", unit="large five (no LTIM)",
    estimate=g2b.sJsE_pp.mean(), lo=g2b.sJsE_pp.mean() - 1.645 * se, hi=g2b.sJsE_pp.mean() + 1.645 * se,
    interval="90% CI from residual sd")

reg = pd.read_csv(H / "design3_regressions.csv").iloc[0]
pt = pool.loc["pretrend_pp"]
for lab, p in [("mean", pt["mean"]), ("hc-weighted", pt.hc_weighted)]:
    est = -(reg.intercept - p)
    add(scope="firm", design=f"3 cross-firm intercept minus pooled pre-trend ({lab})", unit="9 firms",
        estimate=est, lo=est - 1.645 * reg.intercept_se, hi=est + 1.645 * reg.intercept_se,
        interval="90% CI from intercept SE only")

jl = pd.read_csv(H / "infosys_joblevel_trend.csv").iloc[0]
add(scope="firm", design="2 trend on Infosys job levels (JL3- vs rest), full cycle FY21->26", unit="infosys",
    estimate=-jl.dev_cycle_pp, lo=np.nan, hi=-jl.dev_post_pp, interval="hi = FY23->26 window (inflated by promotion of boom cohort)")

mr = pd.read_csv(H / "plfs_gap_multiround.csv")
for _, r in mr[mr.definition != "26-30 vs 31-40"].iterrows():
    add(scope="sector", design="4 PLFS, mean 2023-24 & CY2025 vs mean 2017-18..2020-21, no trend", unit=r.definition,
        estimate=r.sJsE_no_trend_pp, lo=r.ci90_lo, hi=r.ci90_hi, interval="90% CI")
pe = pd.read_csv(H / "plfs_gap_estimates.csv")
for _, r in pe[(pe.definition != "26-30 vs 31-40") & (pe.pretrend_window == "pre 2017-18..2020-21") &
               pe.window.isin(["full cycle 2020-21 -> CY2025", "post 2022-23 -> CY2025"])].iterrows():
    add(scope="sector", design=f"4 PLFS, {r.window}, net of 2017-21 pre-trend", unit=r.definition,
        estimate=r.sJsE_pp, lo=r.sJsE_ci90_lo, hi=r.sJsE_ci90_hi, interval="90% CI")
    add(scope="sector", design=f"4 PLFS, {r.window}, no trend", unit=r.definition,
        estimate=-r.change_pp, lo=-r.change_pp - 1.645 * r.change_se_pp, hi=-r.change_pp + 1.645 * r.change_se_pp,
        interval="90% CI")
S = pd.DataFrame(rows)
S.round(2).to_csv(H / "estimates_summary.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 80)
print(S.round(2).to_string())
