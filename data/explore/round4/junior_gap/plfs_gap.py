"""Designs 4 and 5 (sector scope, NIC 62+63): PLFS age-band employment gap and junior relative pay.

Uses only the AGGREGATE PLFS tables in data/explore/round3/plfs/ (no unit-level data touched).
Junior/experienced definitions:
  main:   21-25 vs 31-40   (as specified in the task)
  robust: 21-30 vs 31-60   (boom-robust: the 2021-23 intake is still under 30 in CY2025)
Gap_t = ln(N_J / N_E) within a round, so the change in the gap is g_J - g_E (the M4 observable).
SE(ln N_J - ln N_E) = sqrt((se_J/N_J)^2 + (se_E/N_E)^2): ignores the (positive) covariance between bands
drawn from the same clusters, so it is conservative.
Round dating (mid-point): 2017-18 -> 2018.0 ... 2023-24 -> 2024.0; CY2024 -> 2024.5; CY2025 -> 2025.5.
Pre-trend: OLS of the gap on time over 2017-18..2020-21 (one survey design) and, as a variant, ..2021-22.
Post: 2022-23 -> CY2025 (crosses the CY2025 redesign) and 2022-23 -> CY2024 (same pre-2025 design family).
Full cycle: 2020-21 -> CY2025 (spans the 2021-23 boom and the bust).
Price check (design 5): ln(mean wage 21-25 / mean wage 31-40) for CWS regular wage workers in NIC 62/63,
differenced against the same ratio for all graduates (all industries).
Outputs: plfs_gap_by_round.csv, plfs_gap_estimates.csv, plfs_relative_pay.csv, plfs_relative_pay_estimates.csv
"""
import pathlib
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[3]
L = pd.read_csv(ROOT / "data/explore/round3/plfs/employment_levels_long.csv")
E = pd.read_csv(ROOT / "data/explore/round3/plfs/earnings_regular_salaried.csv")
T = {"2017-18": 2018.0, "2018-19": 2019.0, "2019-20": 2020.0, "2020-21": 2021.0, "2021-22": 2022.0,
     "2022-23": 2023.0, "2023-24": 2024.0, "cy2024": 2024.5, "cy2025": 2025.5}
Z90 = 1.645

x = L[L.group == "nic62_63"].set_index(["round", "cut"])
rows = []
for r in T:
    def tot(cuts):
        est = sum(x.loc[(r, c), "estimate"] for c in cuts)
        se = np.sqrt(sum(x.loc[(r, c), "se"] ** 2 for c in cuts))  # bands are disjoint; ignores covariance
        n = sum(x.loc[(r, c), "n_unweighted"] for c in cuts)
        return est, se, n
    for lab, jc, ec in [("21-25 vs 31-40", ["age_21_25"], ["age_31_40"]),
                        ("21-30 vs 31-60", ["age_21_25", "age_26_30"], ["age_31_40", "age_41_60"]),
                        ("26-30 vs 31-40", ["age_26_30"], ["age_31_40"])]:
        NJ, sJ, nJ = tot(jc); NE, sE, nE = tot(ec)
        rows.append(dict(round=r, t=T[r], definition=lab, N_J_k=NJ / 1e3, N_E_k=NE / 1e3, n_J=nJ, n_E=nE,
                         gap=np.log(NJ / NE), gap_se=np.sqrt((sJ / NJ) ** 2 + (sE / NE) ** 2),
                         share_J=NJ / (NJ + NE)))
G = pd.DataFrame(rows)
G.round(4).to_csv(HERE / "plfs_gap_by_round.csv", index=False)


def slope(sub):
    t = sub.t.values; y = sub.gap.values; v = sub.gap_se.values ** 2
    c = (t - t.mean()) / ((t - t.mean()) ** 2).sum()
    return (c * y).sum(), np.sqrt((c ** 2 * v).sum())


def change(sub, a, b):
    A = sub[sub["round"] == a].iloc[0]; Bq = sub[sub["round"] == b].iloc[0]
    dt = Bq.t - A.t
    return (Bq.gap - A.gap) / dt, np.sqrt(A.gap_se ** 2 + Bq.gap_se ** 2) / dt, dt


est = []
for d, sub in G.groupby("definition"):
    for pre_lab, pre_rounds in [("pre 2017-18..2020-21", ["2017-18", "2018-19", "2019-20", "2020-21"]),
                                ("pre 2017-18..2021-22", ["2017-18", "2018-19", "2019-20", "2020-21", "2021-22"])]:
        pt, pt_se = slope(sub[sub["round"].isin(pre_rounds)])
        for win, a, b in [("post 2022-23 -> CY2025", "2022-23", "cy2025"),
                          ("post 2022-23 -> CY2024", "2022-23", "cy2024"),
                          ("post 2022-23 -> 2023-24", "2022-23", "2023-24"),
                          ("full cycle 2020-21 -> CY2025", "2020-21", "cy2025"),
                          ("full cycle 2020-21 -> CY2024", "2020-21", "cy2024")]:
            ch, ch_se, dt = change(sub, a, b)
            dev = ch - pt; dev_se = np.sqrt(ch_se ** 2 + pt_se ** 2)
            r = dict(definition=d, pretrend_window=pre_lab, window=win, years=dt, pretrend_pp=pt * 100,
                     pretrend_se_pp=pt_se * 100, change_pp=ch * 100, change_se_pp=ch_se * 100,
                     deviation_pp=dev * 100, deviation_se_pp=dev_se * 100,
                     sJsE_pp=-dev * 100, sJsE_ci90_lo=-(dev + Z90 * dev_se) * 100, sJsE_ci90_hi=-(dev - Z90 * dev_se) * 100)
            if win.startswith("post") and b == "cy2025":
                # boom bump and breakdown, sector scope: bump = gap(2022-23) - [gap(2020-21) + 2*pretrend]
                g = sub.set_index("round").gap
                B_ = g["2022-23"] - (g["2020-21"] + 2 * pt)
                r["bump_B_pp"] = B_ * 100
                r["breakdown_unwind_share"] = (-dev * dt) / B_ if B_ > 0 else np.inf
            est.append(r)
EST = pd.DataFrame(est)
EST.round(3).to_csv(HERE / "plfs_gap_estimates.csv", index=False)
pd.set_option("display.width", 260); pd.set_option("display.max_columns", 30)
print(G.round(3).to_string())
print(EST.round(2).to_string())

# ---------------- Design 5: junior relative pay ----------------
pr = []
for r in T:
    for samp in ["cws_regular_nic62_63", "cws_regular_nic62_63_grads", "cws_regular_all_grads"]:
        s = E[(E["round"] == r) & (E["sample"] == samp)].set_index("age_band")
        if not {"21-25", "31-40"} <= set(s.index):
            continue
        a, b = s.loc["21-25"], s.loc["31-40"]
        pr.append(dict(round=r, t=T[r], sample=samp, ratio_mean=a.mean_inr / b.mean_inr,
                       lnratio=np.log(a.mean_inr / b.mean_inr),
                       lnratio_se=np.sqrt((a.mean_se / a.mean_inr) ** 2 + (b.mean_se / b.mean_inr) ** 2),
                       ratio_median=a.median_inr / b.median_inr, n_21_25=a.n_unweighted, n_31_40=b.n_unweighted))
PR = pd.DataFrame(pr)
PR.round(4).to_csv(HERE / "plfs_relative_pay.csv", index=False)
print(PR.pivot(index="round", columns="sample", values="ratio_mean").round(3).to_string())
print(PR.pivot(index="round", columns="sample", values="ratio_median").round(3).to_string())
pe = []
for samp, sub in PR.groupby("sample"):
    sub = sub.rename(columns={"lnratio": "gap", "lnratio_se": "gap_se"})
    pt, pt_se = slope(sub[sub["round"].isin(["2017-18", "2018-19", "2019-20", "2020-21"])])
    for win, a, b in [("post 2022-23 -> CY2025", "2022-23", "cy2025"), ("post 2022-23 -> CY2024", "2022-23", "cy2024"),
                      ("full cycle 2020-21 -> CY2025", "2020-21", "cy2025")]:
        ch, ch_se, dt = change(sub, a, b)
        pe.append(dict(sample=samp, window=win, pretrend_pp=pt * 100, pretrend_se_pp=pt_se * 100,
                       change_pp=ch * 100, change_se_pp=ch_se * 100,
                       deviation_pp=(ch - pt) * 100, deviation_se_pp=np.sqrt(ch_se ** 2 + pt_se ** 2) * 100))
PE = pd.DataFrame(pe)
# difference-in-differences of relative pay: IT minus all graduates (independent samples assumed; conservative)
for win in PE.window.unique():
    it = PE[(PE["sample"] == "cws_regular_nic62_63") & (PE.window == win)].iloc[0]
    ag = PE[(PE["sample"] == "cws_regular_all_grads") & (PE.window == win)].iloc[0]
    pe_row = dict(sample="DiD: nic62_63 minus all_grads", window=win,
                  change_pp=it.change_pp - ag.change_pp, change_se_pp=np.hypot(it.change_se_pp, ag.change_se_pp),
                  deviation_pp=it.deviation_pp - ag.deviation_pp,
                  deviation_se_pp=np.hypot(it.deviation_se_pp, ag.deviation_se_pp))
    PE = pd.concat([PE, pd.DataFrame([pe_row])], ignore_index=True)
PE.round(3).to_csv(HERE / "plfs_relative_pay_estimates.csv", index=False)
print(PE.round(2).to_string())

# ---------------- Multi-round level comparison (less sensitive to single-round noise) ----------------
# pre = mean of 2017-18..2020-21; post = mean of 2023-24 and CY2025 (non-overlapping samples; CY2024 is
# excluded because it shares Jan-Jun 2024 with 2023-24). Rounds treated as independent.
# Annualised over the distance between period mid-points. No trend netting (assumes a stable J/E ratio
# absent AI) -- reported alongside the pre-trend-netted version.
mr = []
for d, sub in G.groupby("definition"):
    s = sub.set_index("round")
    pre_r = ["2017-18", "2018-19", "2019-20", "2020-21"]; post_r = ["2023-24", "cy2025"]
    m_pre, v_pre = s.loc[pre_r, "gap"].mean(), (s.loc[pre_r, "gap_se"] ** 2).sum() / len(pre_r) ** 2
    m_post, v_post = s.loc[post_r, "gap"].mean(), (s.loc[post_r, "gap_se"] ** 2).sum() / len(post_r) ** 2
    dt = s.loc[post_r, "t"].mean() - s.loc[pre_r, "t"].mean()
    ch = (m_post - m_pre) / dt; se = np.sqrt(v_pre + v_post) / dt
    mr.append(dict(definition=d, pre_mean_gap=m_pre, post_mean_gap=m_post, years=dt, change_pp=ch * 100,
                   change_se_pp=se * 100, sJsE_no_trend_pp=-ch * 100,
                   ci90_lo=-(ch + Z90 * se) * 100, ci90_hi=-(ch - Z90 * se) * 100))
MR = pd.DataFrame(mr)
MR.round(3).to_csv(HERE / "plfs_gap_multiround.csv", index=False)
print(MR.round(2).to_string())
