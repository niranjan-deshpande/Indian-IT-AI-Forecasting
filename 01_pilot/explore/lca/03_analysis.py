"""LCA probe analysis: exposure merge, contrasts, noise stats, validation, confounds.

PRE-SPECIFICATION (written before any 2023+ LCA numbers were computed or inspected):
 Validation window 2015Q4-2022Q4 (YoY needs FY2015 base; also report excl. 2020Q2-2021Q2).
 V1 (primary): pooled Pearson corr across the 8 firms (LTI and Mindtree kept separate as in the pilot) of
     x = YoY log change x100 of trailing-4-quarter certified LCA positions (decision date), and
     y = pilot gL (YoY log headcount growth x100, data/tidy/yoy_metrics.csv), same calendar quarter.
 V2: same x vs YoY growth of an onsite-staffing proxy built from data/tidy/panel_long.csv:
     Infosys headcount*effort_share_onsite; LTI, Mindtree headcount*(1-effort_share_offshore);
     TechM rev_usd*revenue_share_onsite (2015-2022Q1); Wipro rev_usd*revenue_share_onsite (2013-2020Q2).
 V3 (secondary): x leading y by 2 quarters.
 Decision rule: LCA volume "tracks onsite staffing" if pooled corr >= 0.3 with p < 0.05 in V2 (or V1 where V2 unavailable);
     otherwise LCA is treated as a filing-intensity measure, not a staffing measure.
 Exposure contrast: occupation groups (harmonized across SOC2010/2018, see 02_build_panel.py) with >=0.5% of pooled
     certified positions (8 firms) are split into terciles by Eloundou et al. GPT-4 beta (dv_rating_beta); robustness with
     Felten-Raj-Seamans LM-AIOE. Contrast_ft = YoY dlog(TTM positions, top tercile) - YoY dlog(TTM positions, bottom tercile), x100.
     Also the composition index E_ft = sum_g share_gft * beta_g (YoY change, x100).
 Noise stats per PROBE_BRIEF item 4; 2023-2026 path = mean over 2023Q1-2026Q2 vs 2015-2022 ex-COVID mean.
"""
import os, sys
import numpy as np, pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MAIN8 = ["tcs", "infosys", "hcltech", "wipro", "techm", "ltim", "cognizant", "accenture"]
MID = ["mphasis", "persistent", "coforge", "hexaware", "capgemini"]
cases = pd.read_csv(f"{HERE}/lca_cases_target_firms.csv.gz", low_memory=False)
cases = cases[cases.cal_q.notna()]
C = cases[cases.status_c == "C"].copy()
C["q"] = pd.PeriodIndex(C.cal_q, freq="Q")
QMIN, QMAX = pd.Period("2014Q4", "Q"), pd.Period("2026Q2", "Q")
C = C[(C.q >= QMIN) & (C.q <= QMAX)]
QS = pd.period_range(QMIN, QMAX, freq="Q")

# ------------------------------------------------------------------ exposure
elo = pd.read_csv(f"{HERE}/exposure/eloundou_occ_level.csv")
elo["soc6"] = elo["O*NET-SOC Code"].str[:7]
elo6 = elo.groupby("soc6")[["dv_rating_beta", "human_rating_beta"]].mean()
aioe = pd.read_csv(f"{HERE}/exposure/felten_aioe_soc2010.csv").set_index("SOC Code")
xw = pd.read_csv(f"{HERE}/exposure/bls_soc2010_to_2018_crosswalk.csv")
xw.columns = ["s10", "t10", "s18", "t18"]
s10to18 = xw.groupby("s10").s18.apply(list).to_dict()
s18to10 = xw.groupby("s18").s10.apply(list).to_dict()


def score(s6, s8):
    """Return (eloundou dv beta, eloundou human beta, LM-AIOE, AIOE) for a 6-digit SOC of either vintage."""
    if s8 == "15-1199.01":
        s18s, s10s = ["15-1253"], ["15-1199"]
    elif s6 in s10to18 and s6 not in elo6.index:  # 2010 code
        s18s, s10s = s10to18[s6], [s6]
    else:
        s18s, s10s = [s6], s18to10.get(s6, [s6])
    e = elo6.reindex(s18s).mean()
    a = aioe.reindex(s10s)[["Language Modeling AIOE", "AIOE"]].mean()
    return e.dv_rating_beta, e.human_rating_beta, a["Language Modeling AIOE"], a["AIOE"]


socs = C[["soc6", "soc8"]].drop_duplicates()
sc = pd.DataFrame([(a, b, *score(a, b)) for a, b in socs.itertuples(index=False)],
                  columns=["soc6", "soc8", "beta_gpt4", "beta_human", "lm_aioe", "aioe"])
C = C.merge(sc, on=["soc6", "soc8"], how="left")
m8 = C.firm_group.isin(MAIN8)
w = C[m8]
grp = w.groupby("occ_group").apply(lambda g: pd.Series({
    "positions": g.total_workers.sum(),
    **{k: np.average(g[k].dropna(), weights=g.loc[g[k].notna(), "total_workers"]) if g[k].notna().any() else np.nan
       for k in ["beta_gpt4", "beta_human", "lm_aioe", "aioe"]}}), include_groups=False)
grp["share"] = grp.positions / grp.positions.sum()
elig = grp[(grp.share >= 0.005) & grp.beta_gpt4.notna()].copy()
for k in ["beta_gpt4", "lm_aioe"]:
    elig[f"terc_{k}"] = pd.qcut(elig[k].rank(method="first"), 3, labels=["low", "mid", "high"])
grp = grp.join(elig[["terc_beta_gpt4", "terc_lm_aioe"]])
grp.sort_values("beta_gpt4", ascending=False).round(3).to_csv(f"{HERE}/occ_group_exposure.csv")
C["tw_orig"] = C.total_workers
print("Occupation-group exposure (8 firms, certified positions, all years):\n", grp.sort_values("beta_gpt4", ascending=False).round(3).to_string())


# ------------------------------------------------------------------ measure switch (terciles above fixed on positions)
MEAS = sys.argv[1] if len(sys.argv) > 1 else "positions"
SUF = "" if MEAS == "positions" else "_cases"
if MEAS == "cases":
    frac = 1 / C.total_workers
    C["pos_new"] = C.pos_new * frac; C["pos_existing"] = C.pos_existing * frac
    C["total_workers"] = 1.0
print("\n=========== MEASURE:", MEAS, "===========")
# ------------------------------------------------------------------ series helpers
def qseries(df, firmcol="firm_group"):
    s = df.groupby([firmcol, "q"]).total_workers.sum().unstack(firmcol).reindex(QS).fillna(0)
    return s


def yoy(level, ttm=True):
    x = level.rolling(4).sum() if ttm else level
    with np.errstate(divide="ignore", invalid="ignore"):
        r = 100 * np.log(x / x.shift(4))
    return r.replace([np.inf, -np.inf], np.nan)


def add_pooled(df, firms):
    df = df.copy(); df["pooled8"] = df[firms].sum(axis=1) if df is not None else np.nan
    return df


ex = lambda idx: ~((idx >= pd.Period("2020Q2", "Q")) & (idx <= pd.Period("2021Q2", "Q")))
PRE = lambda idx: (idx >= pd.Period("2015Q1", "Q")) & (idx <= pd.Period("2022Q4", "Q")) & ex(idx)
POST = lambda idx: (idx >= pd.Period("2023Q1", "Q")) & (idx <= pd.Period("2026Q2", "Q"))


def noise(ser):
    s = ser.dropna()
    pre = s[PRE(s.index)]
    post = s[POST(s.index)]
    if len(pre) < 6:
        return dict(n_pre=len(pre))
    r = pre - pre.mean()
    # AR(1) on consecutive quarters only
    rr = r.reindex(pd.period_range(r.index.min(), r.index.max(), freq="Q"))
    pair = pd.concat([rr, rr.shift(1)], axis=1).dropna()
    ar1 = np.polyfit(pair.iloc[:, 1], pair.iloc[:, 0], 1)[0] if len(pair) > 4 else np.nan
    return dict(n_pre=len(pre), mean_pre=pre.mean(), sd_resid=r.std(ddof=1), ar1=ar1,
                n_post=len(post), mean_post=post.mean(), diff=post.mean() - pre.mean(),
                t_naive=(post.mean() - pre.mean()) / (r.std(ddof=1) * np.sqrt(1 / len(pre) + 1 / max(len(post), 1))) if len(post) else np.nan)


out_series = {}
tot = qseries(C[C.firm_group.isin(MAIN8 + MID)])
tot["pooled8"] = tot[MAIN8].sum(axis=1); tot["pooled_mid"] = tot[MID].sum(axis=1)
out_series["total_ttm"] = yoy(tot)
out_series["total_q"] = yoy(tot, ttm=False)


def contrast(mask_hi, mask_lo, ttm=True):
    hi = qseries(C[mask_hi & C.firm_group.isin(MAIN8 + MID)]).reindex(columns=tot.columns[:-2], fill_value=0)
    lo = qseries(C[mask_lo & C.firm_group.isin(MAIN8 + MID)]).reindex(columns=tot.columns[:-2], fill_value=0)
    for d_ in (hi, lo):
        d_["pooled8"] = d_[MAIN8].sum(axis=1); d_["pooled_mid"] = d_[MID].sum(axis=1)
    return yoy(hi, ttm) - yoy(lo, ttm), hi, lo


tg = grp.terc_beta_gpt4.to_dict(); ta = grp.terc_lm_aioe.to_dict()
C["terc"] = C.occ_group.map(tg); C["terc_aioe"] = C.occ_group.map(ta)
out_series["contrast_gpt4"], HI, LO = contrast(C.terc == "high", C.terc == "low")
out_series["contrast_lmaioe"], _, _ = contrast(C.terc_aioe == "high", C.terc_aioe == "low")
# DEV+QA vs SUPPORT+NETWORK: simple named contrast
out_series["contrast_devqa_vs_supnet"], _, _ = contrast(C.occ_group.isin(["DEV", "QA"]), C.occ_group.isin(["SUPPORT", "NETWORK"]))
# wage level I-II vs III-IV
out_series["contrast_L12_vs_L34"], _, _ = contrast(C.wage_level.isin(["I", "II"]), C.wage_level.isin(["III", "IV"]))
# exposure contrast within wage level II only (removes wage-level composition shocks)
out_series["contrast_gpt4_withinL2"], _, _ = contrast((C.terc == "high") & (C.wage_level == "II"), (C.terc == "low") & (C.wage_level == "II"))

# composition index (TTM shares)
C["bw"] = C.beta_gpt4 * C.total_workers
num_ = C[C.beta_gpt4.notna()].groupby(["firm_group", "q"]).bw.sum().unstack(0).reindex(QS).fillna(0)
den_ = C[C.beta_gpt4.notna()].groupby(["firm_group", "q"]).total_workers.sum().unstack(0).reindex(QS).fillna(0)
num_["pooled8"] = num_[MAIN8].sum(axis=1); den_["pooled8"] = den_[MAIN8].sum(axis=1)
E = num_.rolling(4).sum() / den_.rolling(4).sum()
out_series["comp_index_gpt4_dYoY_x100"] = 100 * (E - E.shift(4))

# new vs existing (FY2017+ only)
Cn = C[C.pos_new.notna()]
newq = Cn.groupby(["firm_group", "q"]).pos_new.sum().unstack(0).reindex(QS)
exq = Cn.groupby(["firm_group", "q"]).pos_existing.sum().unstack(0).reindex(QS)
newq.loc[newq.index < pd.Period("2016Q4", "Q")] = np.nan; exq.loc[exq.index < pd.Period("2016Q4", "Q")] = np.nan
for d_ in (newq, exq):
    d_["pooled8"] = d_[MAIN8].sum(axis=1, min_count=1)
out_series["new_ttm"] = yoy(newq); out_series["existing_ttm"] = yoy(exq)

# save series
long = []
for k, df in out_series.items():
    t = df.copy(); t.index = t.index.astype(str); t = t.stack(dropna=True).rename("value").reset_index()
    t.columns = ["cal_q", "firm", "value"]; t["series"] = k; long.append(t)
long = pd.concat(long)
long["source"] = "DOL OFLC LCA disclosure data; https://www.dol.gov/agencies/eta/foreign-labor/performance"
long.to_csv(f"{HERE}/lca_yoy_series{SUF}.csv", index=False)

# noise table
rows = []
for k, df in out_series.items():
    for f in [c for c in df.columns if c in MAIN8 + ["pooled8", "pooled_mid"]]:
        rows.append(dict(series=k, firm=f, **noise(df[f])))
nt = pd.DataFrame(rows)
nt.round(2).to_csv(f"{HERE}/lca_noise_stats{SUF}.csv", index=False)
pd.set_option("display.width", 250)
print("\nNOISE / PATH (pooled):\n", nt[nt.firm.isin(["pooled8", "pooled_mid"])].round(2).to_string(index=False))
print("\nNOISE / PATH per firm (contrast_gpt4, total_ttm):\n", nt[nt.series.isin(["contrast_gpt4", "total_ttm"]) & nt.firm.isin(MAIN8)].round(2).to_string(index=False))

# ------------------------------------------------------------------ calendar-year tables
C["cy"] = C.q.dt.year
cy = C[m8].pivot_table(index="cy", columns="occ_group", values="total_workers", aggfunc="sum").fillna(0)
print("\nPooled 8 certified positions by calendar year x occ group:\n", cy.astype(int).to_string())
wl = C[m8].pivot_table(index="cy", columns="wage_level", values="total_workers", aggfunc="sum").fillna(0)
print("\nwage level by CY (8 firms):\n", wl.astype(int).to_string())
# Level-I+II share by exposure tercile, pre vs post (confound check)
C["junior"] = C.wage_level.isin(["I", "II"])
j = C[m8 & (C.wage_level != "NA")].groupby(["terc", C.cy >= 2023]).apply(lambda g: np.average(g.junior, weights=g.total_workers), include_groups=False)
print("\nLevel I+II share of positions by exposure tercile (pre-2023 False / 2023+ True):\n", j.round(3).to_string())
jl1 = C[m8 & (C.wage_level != "NA")].groupby(["occ_group"]).apply(lambda g: np.average(g.wage_level == "I", weights=g.total_workers), include_groups=False)
print("\nLevel I share by occ group (all years):\n", jl1.round(3).to_string())
nq = C[m8].groupby("q")[["pos_new", "pos_existing", "total_workers"]].sum()
print("\npooled8 new vs existing by quarter (2024Q1+):\n", nq[nq.index >= pd.Period("2024Q1", "Q")].to_string())

# ------------------------------------------------------------------ validation (2015-2022 only)
yo = pd.read_csv(f"{ROOT}/data/tidy/yoy_metrics.csv"); yo["q"] = pd.PeriodIndex(yo.cal_q, freq="Q")
core = pd.read_csv(f"{ROOT}/data/tidy/core_quarterly.csv"); core["q"] = pd.PeriodIndex(core.cal_q, freq="Q")
pl = pd.read_csv(f"{ROOT}/data/tidy/panel_long.csv", low_memory=False); pl["q"] = pd.PeriodIndex(pl.cal_q, freq="Q")
totf = qseries(C, "firm")  # LTI & Mindtree separate
lca_g = yoy(totf)
V = []
for f in ["tcs", "infosys", "hcltech", "wipro", "techm", "lti", "mindtree", "cognizant", "accenture"]:
    if f not in lca_g: continue
    g = yo[yo.firm == f].set_index("q").gL
    hc = core[core.firm == f].set_index("q")
    onsite = None
    def share(metric, dim=None):
        s = pl[(pl.firm == f) & (pl.metric == metric)]
        if dim: s = s[s.dimension == dim]
        return s.groupby("q").value.mean()
    if f == "infosys": onsite = hc.headcount * share("effort_share_onsite") / 100
    if f in ("lti", "mindtree"): onsite = hc.headcount * (1 - share("effort_share_offshore") / 100)
    if f == "techm": onsite = hc.rev_usd * share("revenue_share_onsite", "Onsite") / 100
    if f == "wipro": onsite = hc.rev_usd * share("revenue_share_onsite") / 100
    go = 100 * np.log(onsite / onsite.shift(4)) if onsite is not None else None
    if go is not None:
        go = go.reindex(pd.period_range(go.index.min(), go.index.max(), freq="Q"))
        o2 = onsite.reindex(pd.period_range(onsite.index.min(), onsite.index.max(), freq="Q"))
        go = 100 * np.log(o2 / o2.shift(4))
    df = pd.DataFrame({"lca": lca_g[f], "gL": g.reindex(QS), "g_onsite": go.reindex(QS) if go is not None else np.nan})
    df["lca_lead2"] = df.lca.shift(2)
    df["firm"] = f
    V.append(df)
V = pd.concat(V); V.index.name = "q"; V = V.reset_index()
win = (V.q >= pd.Period("2015Q4", "Q")) & (V.q <= pd.Period("2022Q4", "Q"))
res = []
for lab, mk in [("2015Q4-2022Q4", win), ("ex-COVID", win & ex(pd.PeriodIndex(V.q)))]:
    for xv in ["lca", "lca_lead2"]:
        for yv in ["gL", "g_onsite"]:
            s = V[mk][[xv, yv, "firm"]].dropna()
            if len(s) > 5:
                r, p = stats.pearsonr(s[xv], s[yv])
                # within-firm (demeaned)
                sd = s.copy(); sd[[xv, yv]] = sd.groupby("firm")[[xv, yv]].transform(lambda z: z - z.mean())
                rw, pw = stats.pearsonr(sd[xv], sd[yv])
                res.append(dict(window=lab, x=xv, y=yv, n=len(s), firms=s.firm.nunique(), r=r, p=p, r_within=rw, p_within=pw))
    for f in V.firm.unique():
        s = V[mk & (V.firm == f)][["lca", "gL", "g_onsite"]]
        for yv in ["gL", "g_onsite"]:
            ss = s[["lca", yv]].dropna()
            if len(ss) > 5:
                r, p = stats.pearsonr(ss.lca, ss[yv]); res.append(dict(window=lab, x="lca", y=yv, firm=f, n=len(ss), r=r, p=p))
res = pd.DataFrame(res)
res.round(3).to_csv(f"{HERE}/lca_validation{SUF}.csv", index=False)
print("\nVALIDATION:\n", res.round(3).to_string(index=False))
