"""Design 1: stock-flow accounting of under-30 headcount (firm scope).

For each firm-year with under-30 (J) and 30+ (E) headcount, hires by age and exits by age:
    J_t = J_{t-1} + hJ_t - xJ_t - A_t       (A_t = net flow of employees crossing age 30)
    E_t = E_{t-1} + hE_t - xE_t + A_t
A_t is the residual from the J equation (A_J) and, as a check, from the E equation (A_E).
Where turnover is reported as a rate, exits = rate x average(stock_{t-1}, stock_t).
Rates are expressed relative to the opening stock J_{t-1}.

Inputs (read-only): data/explore/workforce/workforce_firm_tidy.csv,
                    data/explore/round3/seniority_firms/midtier_age_tables.csv
Output: stockflow_firm_year.csv, stockflow_summary.csv (this folder)
"""
import pathlib, re
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[3]
W = pd.read_csv(ROOT / "data/explore/workforce/workforce_firm_tidy.csv")
M = pd.read_csv(ROOT / "data/explore/round3/seniority_firms/midtier_age_tables.csv")

BANDS = {"age_lt30": "J", "age_30_50": "E1", "age_gt50": "E2"}


def big(firm, metric):
    x = W[(W.firm == firm) & (W.metric == metric) & W.dimension.isin(BANDS)]
    p = x.pivot_table(index="fiscal_year", columns="dimension", values="value_num", aggfunc="first")
    out = pd.DataFrame(index=p.index)
    out["J"] = p.get("age_lt30")
    out["E"] = p.get("age_30_50") + p.get("age_gt50").fillna(0)
    return out


def mid(firm, metric):
    x = M[(M.firm == firm) & (M.metric == metric) & M.age_band.isin(["<30", "30-50", ">50"])]
    x = x[~x.scope.fillna("").str.startswith("Level x age")]
    x = x[~x.scope.fillna("").str.lower().str.startswith("contractual")]
    x = x[~x.fiscal_year.str.contains("as printed")]
    x = x.drop_duplicates(["fiscal_year", "age_band"], keep="last")
    x["fy"] = x.fiscal_year.map(lambda s: 2000 + int(re.findall(r"\d+", s)[0][-2:]))
    p = x.pivot_table(index="fy", columns="age_band", values="value", aggfunc="first")
    out = pd.DataFrame(index=p.index)
    out["J"] = p["<30"]
    out["E"] = p["30-50"] + p[">50"]
    return out


rows = []


def account(firm, hc, hires, exits=None, rates=None, exit_basis="", note=""):
    yrs = sorted(hc.index)
    for t in yrs:
        if t - 1 not in hc.index or t not in hires.index:
            continue
        J0, J1, E0, E1 = hc.loc[t - 1, "J"], hc.loc[t, "J"], hc.loc[t - 1, "E"], hc.loc[t, "E"]
        hJ, hE = hires.loc[t, "J"], hires.loc[t, "E"]
        if exits is not None and t in exits.index:
            xJ, xE = exits.loc[t, "J"], exits.loc[t, "E"]
        elif rates is not None and t in rates.index:
            xJ = rates.loc[t, "J"] / 100 * (J0 + J1) / 2
            xE = rates.loc[t, "E"] / 100 * (E0 + E1) / 2
        else:
            continue
        if np.isnan([J0, J1, E0, E1, hJ, hE, xJ, xE]).any():
            continue
        AJ = J0 + hJ - xJ - J1
        AE = E1 - E0 - hE + xE
        # unaccounted exits u = AJ - AE (exits missing from the reported turnover, e.g. involuntary exits);
        # true ageing A lies in [AE, AJ] when u >= 0. Central: allocate u to J in proportion to reported exits.
        u = AJ - AE
        shJ = xJ / (xJ + xE) if (xJ + xE) > 0 else 0.5
        A_c = AJ - max(u, 0) * shJ if u > 0 else AJ
        rows.append(dict(firm=firm, fy=t, J0=J0, J1=J1, E0=E0, E1=E1, hires_J=hJ, hires_E=hE,
                         exits_J=round(xJ), exits_E=round(xE), ageout_from_J=round(AJ), ageout_from_E=round(AE),
                         unaccounted_exits=round(u), ageout_central=round(A_c),
                         ageout_rate_lo=min(AJ, AE) / J0, ageout_rate_central=A_c / J0, ageout_rate_hi=max(AJ, AE) / J0,
                         exit_rate_J_central=(xJ + (max(u, 0) * shJ)) / J0,
                         gJ_log=np.log(J1 / J0), gE_log=np.log(E1 / E0),
                         gap_log=np.log(J1 / J0) - np.log(E1 / E0),
                         hire_rate_J=hJ / J0, exit_rate_J=xJ / J0, ageout_rate_J=AJ / J0,
                         hire_rate_E=hE / E0, exit_rate_E=xE / E0, agein_rate_E=AJ / E0,
                         closure_gap_pct_of_HC=(AJ - AE) / (J0 + E0) * 100,
                         exit_basis=exit_basis, note=note))


# Infosys: counts for HC, hires, exits FY16-26 (turnover basis break FY22 noted in round3)
account("infosys", big("infosys", "employees_by_age"), big("infosys", "new_hires_by_age"),
        exits=big("infosys", "turnover_by_age"), exit_basis="count, total exits",
        note="closes exactly with HC totals; turnover basis break FY22")
# Mindtree FY17-22 and LTIM FY24-26: counts
account("mindtree", big("mindtree", "employees_by_age"), big("mindtree", "new_hires_by_age"),
        exits=big("mindtree", "turnover_by_age"), exit_basis="count")
account("ltimindtree", big("ltimindtree", "employees_by_age"), big("ltimindtree", "new_hires_by_age"),
        exits=big("ltimindtree", "turnover_by_age"), exit_basis="count")
# HCL, Wipro, TechM: turnover rates
account("hcltech", big("hcltech", "employees_by_age"), big("hcltech", "new_hires_by_age"),
        rates=big("hcltech", "turnover_rate_by_age"), exit_basis="rate (IT services scope) x avg HC",
        note="turnover rate scope differs from HC scope")
account("wipro", big("wipro", "employees_by_age"), big("wipro", "new_hires_by_age"),
        rates=big("wipro", "turnover_rate_by_age"), exit_basis="rate x avg HC")
account("techm", big("techm", "employees_by_age"), big("techm", "new_hires_by_age"),
        rates=big("techm", "turnover_rate_by_age"), exit_basis="VOLUNTARY rate (IT only) x avg HC",
        note="voluntary-only exits: involuntary exits fall into the ageing residual")
# Mid-tier
account("persistent", mid("Persistent", "headcount_by_age"), mid("Persistent", "hires_by_age"),
        rates=mid("Persistent", "turnover_rate_by_age"), exit_basis="VOLUNTARY rate x avg HC",
        note="incl. contract staff; voluntary-only exits")
account("hexaware", mid("Hexaware", "headcount_by_age"), mid("Hexaware", "hires_by_age"),
        exits=mid("Hexaware", "turnover_count_by_age"), exit_basis="count (CY22+ restated voluntary IT-only)",
        note="calendar years; voluntary-only exits from CY22")

sf = pd.DataFrame(rows).sort_values(["firm", "fy"])
sf.round(4).to_csv(HERE / "stockflow_firm_year.csv", index=False)


# Period summaries: mean annual rates by period, and decomposition of the change in junior growth
def period(fy):
    if fy <= 2021:
        return "pre_FY16_21"
    if fy <= 2023:
        return "boom_FY22_23"
    return "post_FY24_26"


sf["period"] = sf.fy.map(period)
cols = ["gJ_log", "gE_log", "gap_log", "hire_rate_J", "exit_rate_J", "exit_rate_J_central", "ageout_rate_lo",
        "ageout_rate_central", "ageout_rate_hi", "hire_rate_E", "exit_rate_E", "closure_gap_pct_of_HC",
        "hires_J", "hires_E"]
summ = sf.groupby(["firm", "period"])[cols].mean()
summ["n_years"] = sf.groupby(["firm", "period"]).size()
summ = summ.reset_index()
summ.round(4).to_csv(HERE / "stockflow_summary.csv", index=False)

pd.set_option("display.width", 250)
print(sf[["firm", "fy", "J0", "J1", "hires_J", "exits_J", "ageout_from_J", "ageout_from_E", "ageout_central",
          "hire_rate_J", "exit_rate_J_central", "ageout_rate_lo", "ageout_rate_central", "ageout_rate_hi",
          "closure_gap_pct_of_HC"]].round(3).to_string())
print(summ.round(3).to_string())


# ---------------------------------------------------------------------------------------------
# Design-1 estimate: gap net of abnormal ageing, relative to the firm's own pre-period gap.
#   adjusted_gap_post = gap_post + (a_post - a_pre) * (1 + J/E)   [move abnormal crossings back]
#   -(s_J - s_E) = adjusted_gap_post - gap_pre
# Only firms with a pre-period stock-flow (Infosys FY16-21, Wipro FY20-21, Mindtree FY17-21 -> LTIM).
# ---------------------------------------------------------------------------------------------
est = []
pairs = [("infosys", "infosys", "infosys"), ("wipro", "wipro", "wipro"), ("ltimindtree", "mindtree", "LTIM post vs Mindtree pre (entity change)")]
for post_f, pre_f, lab in pairs:
    po = sf[(sf.firm == post_f) & (sf.period == "post_FY24_26")]
    pr = sf[(sf.firm == pre_f) & (sf.period == "pre_FY16_21")]
    je = (po.J0 / po.E0).mean()
    gap_pre, gap_post = pr.gap_log.mean(), po.gap_log.mean()
    for k in ["lo", "central", "hi"]:
        exc = po[f"ageout_rate_{k}"].mean() - pr[f"ageout_rate_{k}"].mean()
        adj = gap_post + exc * (1 + je)
        est.append(dict(firm=lab, ageing_case=k, pre_years=f"{int(pr.fy.min())}-{int(pr.fy.max())}",
                        post_years=f"{int(po.fy.min())}-{int(po.fy.max())}", gap_pre=gap_pre, gap_post=gap_post,
                        excess_ageout_rate=exc, adjusted_gap_post=adj,
                        sJ_minus_sE_pp_no_ageing_adj=-(gap_post - gap_pre) * 100,
                        sJ_minus_sE_pp=-(adj - gap_pre) * 100))
est = pd.DataFrame(est)
est.round(4).to_csv(HERE / "design1_estimates.csv", index=False)
print(est.round(3).to_string())

# ---------------------------------------------------------------------------------------------
# Cohort check (Infosys): how many EXTRA crossings of age 30 can the FY22-23 hiring boom have produced by FY26?
# Assumptions (explicit, not data): freshers are 22 at hire -> cross 30 eight years later;
# non-fresher under-30 hires are spread evenly over ages 23-29 -> cross 1..7 years later (1/7 each);
# annual exit probability 0.20 (Infosys pre-period junior exit rate 0.22; post central 0.23).
# Excess = FY22-23 hires above the FY16-21 average, split into fresher and non-fresher parts.
# ---------------------------------------------------------------------------------------------
fr = pd.read_csv(ROOT / "data/explore/workforce/fresher_hires_annual_best.csv")
fr = fr[fr.firm == "infosys"].set_index("fy").fresher
inf = sf[sf.firm == "infosys"].set_index("fy")
pre_years = [2016, 2017, 2018, 2019, 2021]  # FY20 fresher count missing
pre_J = inf.loc[pre_years, "hires_J"].mean(); pre_fr = fr.loc[pre_years].mean(); pre_lat = pre_J - pre_fr
coh = []
for exit_p in [0.15, 0.20, 0.25]:
    surv = 1 - exit_p
    cross = {}
    for y in [2022, 2023]:
        ex_fr = fr.loc[y] - pre_fr
        ex_lat = (inf.loc[y, "hires_J"] - fr.loc[y]) - pre_lat
        for k in range(1, 8):
            cross[y + k] = cross.get(y + k, 0) + ex_lat / 7 * surv ** k
        cross[y + 8] = cross.get(y + 8, 0) + ex_fr * surv ** 8
    for t in range(2023, 2032):
        coh.append(dict(exit_prob=exit_p, fy=t, excess_crossings=round(cross.get(t, 0)),
                        pct_of_FY23_under30=round(100 * cross.get(t, 0) / inf.loc[2023, "J1"], 2)))
coh = pd.DataFrame(coh)
coh.to_csv(HERE / "infosys_boom_cohort_ageing.csv", index=False)
print("pre avg: under-30 hires %.0f, freshers %.0f, non-fresher <30 %.0f" % (pre_J, pre_fr, pre_lat))
print("FY22-23 excess freshers:", [fr.loc[y] - pre_fr for y in (2022, 2023)],
      "excess non-fresher <30:", [inf.loc[y, "hires_J"] - fr.loc[y] - pre_lat for y in (2022, 2023)])
print(coh.pivot(index="fy", columns="exit_prob", values="excess_crossings").to_string())
