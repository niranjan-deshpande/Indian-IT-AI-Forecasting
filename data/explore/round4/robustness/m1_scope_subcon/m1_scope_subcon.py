"""Robustness check R2 for M1 = (1-phi)s_bar: (1) top-six scope with proper uncertainty propagation,
(2) subcontracting (in-/out-sourcing) correction built firm-year by firm-year, (3) recombination with M2.

    python3 data/explore/round4/robustness/m1_scope_subcon/m1_scope_subcon.py

Inputs (read only):
  data/explore/round4/residual/firm_year_panel.csv     residual / rpe series (built by residual/m1_firm.py)
  data/explore/round4/residual/m1_tcs_hcl_bounds.csv   peer range of Delta utilisation, per baseline window
  data/explore/round4/residual/m1_firm_estimates.csv   4-firm year-cluster estimates (replication check)
  data/explore/round4/price_statements/m2_firm_year.csv, m2_aggregate.csv   M2 (phi s_bar)
  audit/subcontracting_series.csv                       subcontracting cost % of revenue, fiscal years
  data/raw/{tcs,hcltech,wipro,techm,ltim}.csv           employee cost and revenue (employee cost share)
  data/explore/round4/price_statements/raw/baseline/infy_20f_fy2026.txt   Infosys employee cost (FY25-26)

Outputs (this folder):
  replication_4firm.csv          4-firm year-cluster estimates recomputed vs residual/m1_firm_estimates.csv
  employee_cost_share.csv        employee cost / revenue by firm-year, and the fixed c_e used per firm
  subcon_corrections_firm_year.csv   per firm-year: subcon share, its change, correction under k_lo/k_mid/k_hi
  subcon_correction_summary.csv  per firm x window: mean correction post, pre, and Delta (enters M1)
  m1_top6.csv                    M1 at top-six scope by window x weighting x subcon variant, with ranges
  sbar_phi_ai_share.csv          s_bar = M1 + M2, phi = M2/s_bar, AI share of the 8.3 pp slowdown
"""
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
R4 = ROOT / "data/explore/round4"
rng = np.random.default_rng(20261015)

F = pd.read_csv(R4 / "residual/firm_year_panel.csv")
BD = pd.read_csv(R4 / "residual/m1_tcs_hcl_bounds.csv")
E1 = pd.read_csv(R4 / "residual/m1_firm_estimates.csv")

PRE_ALL = list(range(2016, 2024))
POST = [2024, 2025, 2026]
WINDOWS = {
    "base: FY16-23 vs FY24-26": PRE_ALL,
    "excl. FY21": [y for y in PRE_ALL if y != 2021],
    "excl. FY22-23 (boom)": [y for y in PRE_ALL if y not in (2022, 2023)],
    "baseline FY16-20 only": list(range(2016, 2021)),
}
MEASURED = ["infosys", "wipro", "techm", "lti_group"]
BOUNDED = ["tcs", "hcltech"]
TOP6 = MEASURED + BOUNDED
MIN_PRE = 2
W26 = F[F.fy == 2026].set_index("firm").weight_rev_usd           # FY26 USD revenue weights (as residual/)


# ------------------------------------------------------------------ estimator
def yearcluster(vals, pre, post, weights=None, level=0.95):
    """vals: DataFrame firm, fy, v. Same estimator as residual/m1_firm.py::yearcluster_t, with optional
    firm weights in the year averages (renormalised over firms present in each year)."""
    x = vals.dropna(subset=["v"])
    npre = x[x.fy.isin(pre)].groupby("firm").size()
    npost = x[x.fy.isin(post)].groupby("firm").size()
    fs = sorted(f for f in npre.index if npre[f] >= MIN_PRE and npost.get(f, 0) >= 1)
    x = x[x.firm.isin(fs) & x.fy.isin(pre + post)].copy()
    x["dev"] = x.v - x.firm.map(x[x.fy.isin(pre)].groupby("firm").v.mean())
    x["w"] = 1.0 if weights is None else x.firm.map(weights)
    m = x.groupby("fy").apply(lambda g: np.average(g.dev, weights=g.w), include_groups=False)
    a, b = m[m.index.isin(pre)], m[m.index.isin(post)]
    delta = b.mean() - a.mean()
    ss = ((a - a.mean()) ** 2).sum() + ((b - b.mean()) ** 2).sum()
    dof = len(a) + len(b) - 2
    se = np.sqrt(ss / dof * (1 / len(a) + 1 / len(b)))
    tq = stats.t.ppf(0.5 + level / 2, dof)
    return dict(est=delta, se=se, dof=dof, lo95=delta - tq * se, hi95=delta + tq * se, firms=";".join(fs))


def panel(corr=None, du=None):
    """Firm-year values: measured firms -> residual_imp_trA; TCS/HCL -> rpe_cc_imp minus assumed Delta util
    in the post years only (a constant shift = the bound in m1_tcs_hcl_bounds.csv). corr: Series indexed
    (firm, fy) added to every firm's value (subcontracting correction)."""
    rows = []
    for _, r in F[F.firm.isin(TOP6)].iterrows():
        if r.firm in MEASURED:
            v = r.residual_imp_trA
        else:
            v = r.rpe_cc_imp - (du[r.firm] if (du is not None and r.fy in POST) else 0.0)
        if corr is not None:
            v = v + corr.get((r.firm, r.fy), 0.0)
        rows.append(dict(firm=r.firm, fy=r.fy, v=v))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ 0. replication of the 4-firm estimate
rep = []
for wn, pre in WINDOWS.items():
    p = panel()
    est = yearcluster(p[p.firm.isin(MEASURED)], pre, POST)
    ref = E1[(E1.series == "imputed cc + Infosys trainee-incl. utilisation") & (E1.window == wn)].iloc[0]
    rep.append(dict(window=wn, recomputed=est["est"], residual_folder=ref.yearclust, lo95=est["lo95"],
                    hi95=est["hi95"], ref_lo95=ref.yearclust_lo95, ref_hi95=ref.yearclust_hi95, firms=est["firms"]))
rep = pd.DataFrame(rep)
rep.round(3).to_csv(OUT / "replication_4firm.csv", index=False)
assert (rep.recomputed - rep.residual_folder).abs().max() < 0.002, rep
print(rep.round(3).to_string())

# ------------------------------------------------------------------ 1. employee cost share c_e
ce_rows = []
for f, unit, dims, sub in [("tcs", "INR_mn", ["Employee cost (in SG&A)", "Employee cost (in cost of revenue)"], "tcs"),
                           ("hcltech", "INR_cr", ["total"], "hcltech"), ("wipro", "INR_mn", ["total"], "wipro"),
                           ("techm", "INR_mn", ["total"], "techm"), ("ltim", "INR_mn", ["total"], "mindtree")]:
    d = pd.read_csv(ROOT / f"data/raw/{f}.csv").sort_values("doc_date")
    d = d[d.firm == sub]
    e = d[(d.metric == "employee_cost") & (d.unit == unit) & (d.period_type == "quarter") & d.dimension.isin(dims)]
    e = e.drop_duplicates(["fiscal_q", "dimension"], keep="last").groupby("fiscal_q").value.sum()
    r = d[(d.metric == "revenue") & (d.unit == unit) & (d.period_type == "quarter") & (d.dimension == "total")]
    r = r.drop_duplicates("fiscal_q", keep="last").set_index("fiscal_q").value
    x = pd.DataFrame({"e": e, "r": r}).dropna()
    x["fy"] = [2000 + int(q[-2:]) for q in x.index]
    g = x.groupby("fy").agg(e=("e", "sum"), r=("r", "sum"), n=("e", "count"))
    g = g[g.n == 4]
    for fy, gg in g.iterrows():
        ce_rows.append(dict(firm="lti_group" if f == "ltim" else f, fy=fy, c_e=gg.e / gg.r,
                            source=f"data/raw/{f}.csv ({sub}) employee_cost / revenue, {unit}, 4 quarters"))
# Infosys: 20-F FY2026 (USD mn). Employee benefit costs (expenses by nature): FY26 10,882, FY25 10,165.
# Revenue = cost of sales / its % of revenue (14,079 / 69.8%; 13,405 / 69.5%) -- parsed from the text below.
t = re.sub(r"\s+", " ", (R4 / "price_statements/raw/baseline/infy_20f_fy2026.txt").read_text(errors="ignore"))
m_cos = re.search(r"Cost of sales ([\d,]+) ([\d,]+) [\d,]+ [\d.]+ % As a percentage of revenues ([\d.]+) % ([\d.]+) %", t)
m_ebc = re.search(r"Expenses by nature \(Dollars in millions\) Year ended March 31, 2026 2025 2024 "
                  r"Employee benefit costs ([\d,]+) ([\d,]+) ([\d,]+)", t)
num = lambda s: float(s.replace(",", ""))
for i, fy in enumerate([2026, 2025]):
    rev = num(m_cos.group(1 + i)) / (float(m_cos.group(3 + i)) / 100)
    ce_rows.append(dict(firm="infosys", fy=fy, c_e=num(m_ebc.group(1 + i)) / rev,
                        source="Infosys 20-F FY2026: employee benefit costs / (cost of sales / cost-of-sales % of revenue)"))
CE = pd.DataFrame(ce_rows)
ce_fixed = CE[CE.fy.between(2016, 2026)].groupby("firm").c_e.mean()
CE["c_e_fixed_used"] = CE.firm.map(ce_fixed)
CE.round(4).to_csv(OUT / "employee_cost_share.csv", index=False)
print("\nfixed employee cost share used:", ce_fixed.round(3).to_dict())

# ------------------------------------------------------------------ 2. subcontracting correction
S = pd.read_csv(ROOT / "audit/subcontracting_series.csv")
S = S[(S.period_type == "fiscal_year") & S.primary & S.subcon_pct_rev.notna()]
S = S[S.firm.isin(["tcs", "infosys", "hcltech", "wipro", "techm", "ltim"])].copy()
S["firm"] = S.firm.replace({"ltim": "lti_group"})
S["fy"] = S.fiscal_year.str[2:].astype(int) + 2000
S = S[S.n_q.isna() | (S.n_q == 4)]           # LTIM annual-report rows have n_q NaN (full-year by construction)
cs = S.set_index(["firm", "fy"]).subcon_pct_rev / 100

# conversion factor k = 1 / (c_e * m), m = cost of subcontracted capacity relative to own staff, for the same revenue
#   m_lo = 1.0 (subcontractors cost no less than own staff: Wipro Q1FY23 "about 30% higher", TechM Q2FY22 "higher")
#   m_mid = 1.3 (Wipro Q1FY23)
#   m_hi = 1 / c_e (subcontracted work delivered at zero gross margin, i.e. subcon cost = the revenue it delivers)
M_SCEN = {"k_hi (m=1.0)": lambda ce: 1.0, "k_mid (m=1.3)": lambda ce: 1.3, "k_lo (m=1/c_e)": lambda ce: 1 / ce}
crow = []
CORR = {}
for scen, mf in M_SCEN.items():
    corr = {}
    for f in TOP6:
        ce = ce_fixed[f]
        m = mf(ce)
        for fy in range(2016, 2027):
            c1, c0 = cs.get((f, fy), np.nan), cs.get((f, fy - 1), np.nan)
            # own-staff share of delivered revenue: 1 - sh = 1 / (1 + c_s / (c_e m)); correction = Delta ln(1 - sh)
            val = -100 * (np.log1p(c1 / (ce * m)) - np.log1p(c0 / (ce * m)))
            corr[(f, fy)] = val
            crow.append(dict(variant=scen, firm=f, fy=fy, c_e=ce, m=m, k=1 / (ce * m), subcon_share=c1,
                             d_subcon_pp=100 * (c1 - c0), correction_pp=val))
    CORR[scen] = pd.Series(corr)
C = pd.DataFrame(crow)
C.round(4).to_csv(OUT / "subcon_corrections_firm_year.csv", index=False)
print("\nper-year change in subcontracting share (pp of revenue):")
print(C[C.variant == "k_mid (m=1.3)"].pivot(index="fy", columns="firm", values="d_subcon_pp").round(2).to_string())
print("correction to residual, k_mid (pp):")
print(C[C.variant == "k_mid (m=1.3)"].pivot(index="fy", columns="firm", values="correction_pp").round(2).to_string())

# correction summary per firm and window: post mean - pre mean, using the firm-years that enter the M1 estimator
srows = []
for scen in M_SCEN:
    cc = C[C.variant == scen]
    for wn, pre in WINDOWS.items():
        for f in TOP6:
            x = cc[cc.firm == f].set_index("fy").correction_pp
            # only years where the firm's M1 value exists
            pv = panel()
            have = set(pv[(pv.firm == f) & pv.v.notna()].fy)
            pre_y = [y for y in pre if y in have]
            pre_ok = [y for y in pre_y if np.isfinite(x.get(y, np.nan))]
            xf = x.reindex(range(2016, 2027)).fillna(0.0)      # same 0-fill as the estimator (missing -> no correction)
            srows.append(dict(variant=scen, window=wn, firm=f, post_mean=xf[POST].mean(),
                              pre_mean=xf[pre_y].mean(),
                              delta=xf[POST].mean() - xf[pre_y].mean(),
                              pre_years_with_corr=f"{len(pre_ok)}/{len(pre_y)}",
                              fy26_corr=x.get(2026, np.nan)))
SC = pd.DataFrame(srows)
SC.round(3).to_csv(OUT / "subcon_correction_summary.csv", index=False)

# ------------------------------------------------------------------ 3. top-six M1 with uncertainty
def du_scen(wn):
    b = BD[BD.window == wn].set_index("firm")
    lo, hi, mid = b.peer_delta_util_min.iloc[0], b.peer_delta_util_max.iloc[0], b.peer_delta_util_mean.iloc[0]
    return lo, mid, hi


NMC = 20000
rows = []
for variant in ["uncorrected"] + list(M_SCEN):
    corr = None if variant == "uncorrected" else CORR[variant].fillna(0.0)   # missing years -> no correction
    for wn, pre in WINDOWS.items():
        dlo, dmid, dhi = du_scen(wn)
        for wlab, wts in [("equal", None), ("revenue", W26)]:
            est = {}
            for lab, du in [("mid", dmid), ("util_hi", dhi), ("util_lo", dlo)]:
                est[lab] = yearcluster(panel(corr, {f: du for f in BOUNDED}), pre, POST, wts)
            c, a, b = est["mid"], est["util_hi"], est["util_lo"]          # util_hi -> lowest residual
            # 4 measured firms only, same correction and weighting
            m4 = yearcluster(panel(corr)[lambda d: d.firm.isin(MEASURED)], pre, POST,
                             None if wts is None else W26)
            # Monte Carlo: TCS and HCL Delta util independently U[lo, hi]; sampling error t(dof)*se
            # estimate is linear in each firm's Delta util -> evaluate slope by finite difference
            e_tcs = yearcluster(panel(corr, {"tcs": dhi, "hcltech": dmid}), pre, POST, wts)["est"]
            e_hcl = yearcluster(panel(corr, {"tcs": dmid, "hcltech": dhi}), pre, POST, wts)["est"]
            s_tcs = (e_tcs - c["est"]) / (dhi - dmid)
            s_hcl = (e_hcl - c["est"]) / (dhi - dmid)
            ut, uh = rng.uniform(dlo, dhi, NMC), rng.uniform(dlo, dhi, NMC)
            draws = c["est"] + s_tcs * (ut - dmid) + s_hcl * (uh - dmid) + c["se"] * rng.standard_t(c["dof"], NMC)
            rows.append(dict(
                variant=variant, window=wn, weighting=wlab, firms=c["firms"],
                tcs_hcl_delta_util_lo=dlo, tcs_hcl_delta_util_mid=dmid, tcs_hcl_delta_util_hi=dhi,
                m1_central=c["est"], se=c["se"], dof=c["dof"], ci95_at_central_lo=c["lo95"], ci95_at_central_hi=c["hi95"],
                bound_lo=a["est"], bound_hi=b["est"],
                union95_lo=a["lo95"], union95_hi=b["hi95"],
                mc95_lo=np.percentile(draws, 2.5), mc95_hi=np.percentile(draws, 97.5),
                m1_4firm=m4["est"], m1_4firm_lo95=m4["lo95"], m1_4firm_hi95=m4["hi95"]))
T = pd.DataFrame(rows)
T.round(3).to_csv(OUT / "m1_top6.csv", index=False)
pd.set_option("display.width", 250)
print("\n", T[["variant", "window", "weighting", "m1_central", "bound_lo", "bound_hi", "union95_lo", "union95_hi",
               "mc95_lo", "mc95_hi", "m1_4firm"]].round(2).to_string())

# ------------------------------------------------------------------ 4. recombination with M2
M2F = pd.read_csv(R4 / "price_statements/m2_firm_year.csv")
M2F = M2F[(M2F.segment == "IT") & M2F.fy.isin(["FY24", "FY25", "FY26"])].copy()
M2F["firm"] = M2F.firm.replace({"TCS": "tcs", "HCLTech": "hcltech", "LTIMindtree": "lti_group", "Infosys": "infosys",
                                "Wipro": "wipro", "TechM": "techm"})
M2A = pd.read_csv(R4 / "price_statements/m2_aggregate.csv")
M2A = M2A[(M2A.segment == "IT top-6") & M2A.fy.isin(["FY24", "FY25", "FY26"])]
m2 = {"revenue": dict(lo=M2A.low.mean(), mid=M2A.central.mean(), hi=M2A.high.mean(),
                      hi_bias=M2A.high_bias_widened.mean())}
eq = M2F.groupby("fy")[["low", "central", "high"]].mean().mean()
m2["equal"] = dict(lo=eq.low, mid=eq.central, hi=eq.high, hi_bias=2 * eq.high)
print("\nM2 FY24-26 average:", {k: {kk: round(vv, 3) for kk, vv in v.items()} for k, v in m2.items()})
SLOW = 8.3       # top-six employment-growth slowdown, FY24-26 vs FY16-20 (SYNTHESIS.md; note_numbers.csv)
rec = []
for _, r in T.iterrows():
    mm = m2[r.weighting]
    s_mid = r.m1_central + mm["mid"]
    s_blo, s_bhi = r.bound_lo + mm["lo"], r.bound_hi + mm["hi"]
    s_ulo, s_uhi = r.union95_lo + mm["lo"], r.union95_hi + mm["hi_bias"]
    rec.append(dict(variant=r.variant, window=r.window, weighting=r.weighting,
                    m1_central=r.m1_central, m2_central=mm["mid"],
                    sbar_central=s_mid, sbar_bound_lo=s_blo, sbar_bound_hi=s_bhi,
                    sbar_wide_lo=s_ulo, sbar_wide_hi=s_uhi,
                    phi_central=mm["mid"] / s_mid if s_mid > 0 else np.nan,
                    phi_at_bounds=(f"{mm['lo'] / s_bhi:.2f}-{mm['hi'] / s_blo:.2f}" if s_blo > 0 else "unbounded (s_bar lo <= 0)"),
                    ai_share_central=s_mid / SLOW, ai_share_bound_lo=s_blo / SLOW, ai_share_bound_hi=s_bhi / SLOW,
                    ai_share_wide_lo=s_ulo / SLOW, ai_share_wide_hi=s_uhi / SLOW))
REC = pd.DataFrame(rec)
REC.round(3).to_csv(OUT / "sbar_phi_ai_share.csv", index=False)
print("\n", REC.round(2).to_string())

# ------------------------------------------------------------------ 5. FY26 reversal and breakdown points
# (a) per firm: post-period mean correction using per-year changes (FY24, FY25, FY26) vs ignoring FY26's reversal
cm = C[C.variant == "k_mid (m=1.3)"].set_index(["firm", "fy"]).correction_pp
brow = []
for f in TOP6:
    brow.append(dict(item="per-firm correction, k_mid", firm=f,
                     d_subcon_FY24=C[(C.variant == "k_mid (m=1.3)") & (C.firm == f) & (C.fy == 2024)].d_subcon_pp.iloc[0],
                     d_subcon_FY25=C[(C.variant == "k_mid (m=1.3)") & (C.firm == f) & (C.fy == 2025)].d_subcon_pp.iloc[0],
                     d_subcon_FY26=C[(C.variant == "k_mid (m=1.3)") & (C.firm == f) & (C.fy == 2026)].d_subcon_pp.iloc[0],
                     corr_FY24=cm[(f, 2024)], corr_FY25=cm[(f, 2025)], corr_FY26=cm[(f, 2026)],
                     post_mean_per_year=np.mean([cm[(f, y)] for y in POST]),
                     post_mean_ignoring_FY26=np.mean([cm[(f, 2024)], cm[(f, 2025)]]),
                     delta_vs_FY16_23=SC[(SC.variant == "k_mid (m=1.3)") & (SC.window == "base: FY16-23 vs FY24-26") & (SC.firm == f)].delta.iloc[0],
                     delta_vs_FY16_20=SC[(SC.variant == "k_mid (m=1.3)") & (SC.window == "baseline FY16-20 only") & (SC.firm == f)].delta.iloc[0]))
B1 = pd.DataFrame(brow)
# (b) top-six M1 if FY26 had been treated like FY24-25 (correction for FY26 replaced by the FY24-25 mean) -> shows
#     how much the FY26 reversal offsets
alt = CORR["k_mid (m=1.3)"].fillna(0.0).copy()
for f in TOP6:
    alt[(f, 2026)] = np.mean([alt[(f, 2024)], alt[(f, 2025)]])
b2 = []
for wn, pre in WINDOWS.items():
    dlo, dmid, dhi = du_scen(wn)
    for wlab, wts in [("equal", None), ("revenue", W26)]:
        un = T[(T.variant == "uncorrected") & (T.window == wn) & (T.weighting == wlab)].m1_central.iloc[0]
        co = T[(T.variant == "k_mid (m=1.3)") & (T.window == wn) & (T.weighting == wlab)].m1_central.iloc[0]
        nofy26 = yearcluster(panel(alt, {f: dmid for f in BOUNDED}), pre, POST, wts)["est"]
        mm = m2[wlab]["mid"]
        corr_size = co - un
        # share of the measured subcontracting-cost fall that would have to be price (not volume) for s_bar to stay
        # below thresholds; correction scales ~linearly in k
        need = {}
        for thr_lab, thr in [("sbar<1.66 (AI share<20%)", 1.66), ("sbar<2.49 (AI share<30%)", 2.49)]:
            x = 1 - (thr - mm - un) / corr_size
            need[thr_lab] = float(np.clip(x, 0, 1)) if co + mm > thr else 0.0
        b2.append(dict(item="top-six M1, k_mid", window=wn, weighting=wlab, m1_uncorrected=un, m1_corrected=co,
                       correction=corr_size, m1_if_FY26_reversal_ignored=nofy26,
                       fy26_reversal_effect=co - nofy26,
                       price_share_of_subcon_fall_needed_for_AI_share_below_20pct=need["sbar<1.66 (AI share<20%)"],
                       price_share_of_subcon_fall_needed_for_AI_share_below_30pct=need["sbar<2.49 (AI share<30%)"]))
B2 = pd.DataFrame(b2)
pd.concat([B1, B2], ignore_index=True).round(3).to_csv(OUT / "subcon_fy26_and_breakdown.csv", index=False)
print("\n", B1.round(2).to_string())
print("\n", B2.round(2).to_string())
