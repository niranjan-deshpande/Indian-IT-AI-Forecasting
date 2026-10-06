"""Noise stats, 2023-26 path, affiliated shares, and comparison with pilot firm revenue growth."""
import numpy as np, pandas as pd
ROOT = "../../tidy/"
out = []

def qstats(s, name, note=""):
    """s: pd.Series indexed by 'YYYYQn' of YoY log x100."""
    s = s.dropna()
    yr = s.index.str[:4].astype(int); q = s.index
    excl = (q >= "2020Q2") & (q <= "2021Q2")
    w = s[(yr >= 2015) & (yr <= 2022) & ~excl]
    resid = w - w.mean()
    # AR(1) on consecutive quarters within window (skip across excluded gap)
    pairs = [(w[q0], w[q1]) for q0, q1 in zip(w.index[:-1], w.index[1:]) if pd.Period(q1, "Q") - pd.Period(q0, "Q") == pd.offsets.QuarterEnd(1) or (pd.Period(q1,'Q').ordinal-pd.Period(q0,'Q').ordinal)==1]
    x, y = np.array(pairs).T
    ar1 = np.corrcoef(x - w.mean(), y - w.mean())[0, 1]
    post = s[yr >= 2023]
    pre = s[(yr >= 2015) & (yr <= 2022) & ~excl]
    out.append(dict(series=name, freq="Q", n=len(w), mean_2015_22=w.mean(), sd_resid=resid.std(ddof=1), ar1=ar1,
                    n_post=len(post), mean_2023_on=post.mean(), post_minus_pre=post.mean() - pre.mean(),
                    last=f"{post.index[-1]}={post.iloc[-1]:.1f}" if len(post) else "", note=note))

def astats(s, name, note=""):
    s = s.dropna()
    w = s[(s.index >= 2015) & (s.index <= 2022) & ~s.index.isin([2020, 2021])]
    w_all = s[(s.index >= 2015) & (s.index <= 2022)]
    post = s[s.index >= 2023]
    x = w_all.values
    ar1 = np.corrcoef(x[:-1], x[1:])[0, 1] if len(x) > 3 else np.nan
    out.append(dict(series=name, freq="A", n=len(w), mean_2015_22=w.mean(), sd_resid=w.std(ddof=1), ar1=ar1,
                    n_post=len(post), mean_2023_on=post.mean(), post_minus_pre=post.mean() - w.mean(),
                    last=f"{post.index[-1]}={post.iloc[-1]:.1f}" if len(post) else "", note=note + " (annual; excl. 2020-21; AR1 on 2015-22 incl.)"))

def yoy_q(v):  # v indexed YYYYQn
    v = v.sort_index(); idx = pd.PeriodIndex(v.index, freq="Q")
    s = pd.Series(v.values, index=idx)
    g = 100 * np.log(s / s.shift(4, freq="Q")).reindex(idx)
    g.index = g.index.astype(str); return g

# ---------- BEA quarterly (ITA 1.3, India, NSA)
q = pd.read_csv("bea_ita13_india_quarterly.csv")
q["period"] = q.period.str.replace(" ", "")
series = {}
for (d, lab), g in q.groupby(["direction", "label"]):
    v = g.set_index("period").value
    series[f"BEA US {'imports from' if d=='imports' else 'exports to'} India: {lab} (Q, NSA)"] = v
for k in [k for k in series if "imports" in k]:
    qstats(yoy_q(series[k]), k)

# ---------- IMF/RBI India quarterly BoP credits
m = pd.read_csv("imf_bop_india_services_quarterly.csv")
m["period"] = m.TIME_PERIOD.str.replace("-", "")
lab = {"SI2": "computer services", "SI": "telecom, computer & information", "SJ": "other business services", "S": "total services"}
for ind in ["SI2", "SJ", "S"]:
    v = m[(m.BOP_ACCOUNTING_ENTRY == "CD_T") & (m.INDICATOR == ind)].set_index("period").OBS_VALUE
    qstats(yoy_q(v), f"India BoP exports (RBI via IMF): {lab[ind]} (Q, all destinations)")

# ---------- BEA annual Table 2.3 India
a = pd.read_csv("bea_is23_annual.csv")
a["year"] = a.year.astype(str).str.strip().astype(int)
ind = a[(a.area == "India") & (a.direction == "imports")]
piv = ind.pivot_table(index="year", columns="label", values="value")
for col in ["Computer services", "Other computer services", "Computer software, including end-user licenses and customization",
            "Telecommunications, computer, and information services", "Other business services", "Professional and management consulting services",
            "Research and development services", "Imports of services"]:
    s = 100 * np.log(piv[col] / piv[col].shift(1))
    astats(s, f"BEA US imports from India: {col} (A)")

# ---------- MOFA (US-owned affiliates in India) services supplied to US parents
mo = pd.read_csv("bea_mne_mofa_services_by_destination.csv")
mo_i = mo[mo.row == "India"].pivot_table(index="year", columns="column", values="value")
to_par = mo_i["To the United States | To U.S. parents"]
astats(100 * np.log(to_par / to_par.shift(1)), "BEA MNE: India MOFAs' services supplied to US parents (A, fiscal yr) = affiliated proxy")
emp = pd.read_csv("bea_mne_mofa_employment_india.csv")
emp_i = emp[emp.row == "India"].set_index("year").value
astats(100 * np.log(emp_i / emp_i.shift(1)), "BEA MNE: employment of US MOFAs in India (A)")

# ---------- Affiliated share table
tot = piv["Imports of services"]; comp = piv["Computer services"]
share = pd.DataFrame({"US_imports_services_from_India_ITA": tot, "US_imports_computer_services_from_India_ITA": comp,
                      "MOFA_India_services_to_US_parents": to_par, "MOFA_India_services_to_unaffiliated_US": mo_i["To the United States | To unaffiliated U.S. persons"],
                      "MOFA_India_services_total_all_dest": mo_i["To all destinations | Total"], "MOFA_India_employment_thous": emp_i})
share["MOFA_to_parents_share_of_ITA_total_pct"] = 100 * share.MOFA_India_services_to_US_parents / share.US_imports_services_from_India_ITA
share["residual_nonMOFA_ITA_total"] = share.US_imports_services_from_India_ITA - share.MOFA_India_services_to_US_parents
# world-level affiliated share of US computer-services imports (Table 2.3 'All countries, affiliated' / 'All countries')
w = a[(a.direction == "imports") & (a.label == "Computer services")].pivot_table(index="year", columns="area", values="value")
share["WORLD_US_computer_services_imports_affiliated_share_pct"] = 100 * w["All countries, affiliated"] / w["All countries"]
share["India_share_of_US_computer_services_imports_pct"] = 100 * comp / w["All countries"]
share = share.loc[2006:]
share.round(1).to_csv("affiliated_share_annual.csv")
print(share.round(1).to_string())

# ---------- comparison with pilot Indian-firm revenue growth (annualized: mean of quarterly YoY USD within calendar year)
y = pd.read_csv(ROOT + "yoy_metrics.csv")
y["yr"] = y.cal_q.str[:4].astype(int)
y["g"] = y.gR_usd.fillna(y.gR)
indian = ["tcs", "infosys", "wipro", "hcltech", "techm", "ltim", "lti", "mindtree"]
fi = y[y.firm.isin(indian)].groupby(["yr"]).g.mean()
cog = y[y.firm == "cognizant"].groupby("yr").g.mean()
cmp = pd.DataFrame({"indian_firms_rev_usd_yoy": fi, "cognizant_rev_usd_yoy": cog,
                    "BEA_computer_services_imports_India_yoy": 100 * np.log(comp / comp.shift(1)),
                    "BEA_total_services_imports_India_yoy": 100 * np.log(tot / tot.shift(1)),
                    "MOFA_to_US_parents_yoy": 100 * np.log(to_par / to_par.shift(1)),
                    "nonMOFA_residual_yoy": 100 * np.log(share.residual_nonMOFA_ITA_total / share.residual_nonMOFA_ITA_total.shift(1))})
# India BoP computer services exports, calendar-year sum
bq = m[(m.BOP_ACCOUNTING_ENTRY == "CD_T") & (m.INDICATOR == "SI2")].copy(); bq["yr"] = bq.TIME_PERIOD.str[:4].astype(int)
bs = bq.groupby("yr").OBS_VALUE.agg(["sum", "count"]); bs = bs[bs["count"] == 4]["sum"]
cmp["India_BoP_computer_exports_yoy"] = 100 * np.log(bs / bs.shift(1))
cmp = cmp.loc[2010:2025]
cmp.round(1).to_csv("compare_firm_vs_trade_annual.csv")
print(cmp.round(1).to_string())
win = cmp.loc[2015:2022]
for c in cmp.columns[2:]:
    ww = win[["indian_firms_rev_usd_yoy", c]].dropna()
    out.append(dict(series=f"CORR 2015-22: indian_firms_rev_usd_yoy vs {c}", freq="A", n=len(ww), mean_2015_22=ww[c].mean(),
                    sd_resid=np.nan, ar1=ww.corr().iloc[0, 1], note="ar1 column holds Pearson corr"))
# quarterly: BEA TCI imports YoY vs Indian firms quarterly mean YoY
fq = y[y.firm.isin(indian)].groupby("cal_q").g.mean()
bt = yoy_q(series["BEA US imports from India: Telecommunications, computer, and information services (Q, NSA)"])
jj = pd.concat([fq.rename("f"), bt.rename("b")], axis=1).dropna()
jj = jj[(jj.index >= "2015Q1") & (jj.index <= "2022Q4")]
out.append(dict(series="CORR 2015Q1-2022Q4 quarterly: Indian firms mean rev YoY vs BEA TCI imports from India YoY", freq="Q", n=len(jj),
                ar1=jj.corr().iloc[0, 1], note="ar1 column holds Pearson corr (incl. COVID quarters)"))
bi = yoy_q(m[(m.BOP_ACCOUNTING_ENTRY == "CD_T") & (m.INDICATOR == "SI2")].set_index("period").OBS_VALUE)
jj = pd.concat([fq.rename("f"), bi.rename("b")], axis=1).dropna(); jj = jj[(jj.index >= "2015Q1") & (jj.index <= "2022Q4")]
out.append(dict(series="CORR 2015Q1-2022Q4 quarterly: Indian firms mean rev YoY vs India BoP computer-services exports YoY", freq="Q", n=len(jj),
                ar1=jj.corr().iloc[0, 1], note="ar1 column holds Pearson corr (incl. COVID quarters)"))
res = pd.DataFrame(out)
res.round(3).to_csv("noise_stats.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 95)
print(res.round(2).to_string())
