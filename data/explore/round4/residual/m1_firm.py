"""M1 at firm scope: change in the revenue-per-worker residual (net of utilisation), FY24-26 vs baseline,
with uncertainty, sensitivity variants, and bounds for TCS / HCLTech.

    python3 data/explore/round4/residual/m1_firm.py

Inputs (read only): data/corrected/core_quarterly_final.csv, data/corrected/yoy_metrics_final.csv,
    output/noise_params.json (D27 noise model), data/explore/round3/seniority_firms/infosys_trainees_implied.csv
Definitions replicate scripts/final/tables_figures.py (fy_metrics, LTI group), checked against output/final/table_B.csv.

Outputs (this folder):
  firm_year_panel.csv      firm x FY: rpe (cc, usd, imputed cc), util change (base, Infosys incl.-trainee), residual variants
  replication_check.csv    Table B recomputed vs output/final/table_B.csv
  m1_firm_estimates.csv    Delta residual by variant x estimator, with D27-simulation and pigeonhole-bootstrap CIs
  m1_tcs_hcl_bounds.csv    TCS / HCLTech: observed Delta rpe, peer range of Delta util, implied Delta residual range
  m1_top6_range.csv        top-six (equal and revenue weighted) range combining observed firms and TCS/HCL bounds
  noise_check.csv          D27-implied vs empirical dispersion of annual residuals
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(20261014)

core = pd.read_csv(ROOT / "data/corrected/core_quarterly_final.csv", dtype={"cal_q": str})
yoy = pd.read_csv(ROOT / "data/corrected/yoy_metrics_final.csv", dtype={"cal_q": str})


def qadd(q, k):
    y, n = int(q[:4]), int(q[-1])
    t = y * 4 + n - 1 + k
    return f"{t // 4}Q{t % 4 + 1}"


def fy_quarters(fy):
    return [f"{fy - 1}Q2", f"{fy - 1}Q3", f"{fy - 1}Q4", f"{fy}Q1"]


# ---------------------------------------------------------------- Infosys alternative utilisation / headcount
inf = core[core.firm == "infosys"].set_index("cal_q")
du_incl = 100 * np.log(inf.util_incl / inf.util_incl.shift(4))      # trainee-inclusive utilisation, YoY log x100
# check that shift(4) is a true 4-quarter lag (series is complete and sorted)
assert list(inf.index) == sorted(inf.index)
tr = pd.read_csv(ROOT / "data/explore/round3/seniority_firms/infosys_trainees_implied.csv")
pe = pd.to_datetime(tr.period_end)
tr["cal_q"] = pe.dt.year.astype(str) + "Q" + pe.dt.quarter.astype(str)
tr = tr.set_index("cal_q")
hc_ex = (inf.headcount - tr.implied_trainees_calibrated.reindex(inf.index))
gL_ex = 100 * np.log(hc_ex / hc_ex.shift(4))                        # headcount excluding implied trainees


# ---------------------------------------------------------------- quarterly panel (replicates tables_figures.py)
def lti_group_quarterly():
    rows = []
    c = core.set_index(["firm", "cal_q"])
    y = yoy.set_index(["firm", "cal_q"])
    for q in sorted(set(core.cal_q)):
        if q < "2015Q1":
            continue
        fy = int(q[:4]) + (1 if q[-1] != "1" else 0)
        r = dict(firm="lti_group", cal_q=q)
        if fy <= 2022:
            def lv(f, col, qq):
                return c[col].get((f, qq), np.nan)
            R = lv("lti", "rev_usd", q) + lv("mindtree", "rev_usd", q)
            R0 = lv("lti", "rev_usd", qadd(q, -4)) + lv("mindtree", "rev_usd", qadd(q, -4))
            L = lv("lti", "headcount", q) + lv("mindtree", "headcount", q)
            L0 = lv("lti", "headcount", qadd(q, -4)) + lv("mindtree", "headcount", qadd(q, -4))
            r.update(rev_usd=R, headcount=L, gR_usd=100 * np.log(R / R0), gL=100 * np.log(L / L0), gR=np.nan)
            du = [(y["du"].get((f, q), np.nan), lv(f, "headcount", q)) for f in ("lti", "mindtree")]
            du = [(a, w) for a, w in du if pd.notna(a) and pd.notna(w)]
            r["du"] = np.average([a for a, _ in du], weights=[w for _, w in du]) if len(du) == 2 else np.nan
        else:
            for col in ["rev_usd", "headcount"]:
                r[col] = c[col].get(("ltim", q), np.nan)
            for col in ["gR_usd", "gL", "gR", "du"]:
                r[col] = y[col].get(("ltim", q), np.nan)
        rows.append(r)
    return pd.DataFrame(rows)


ENT = ["tcs", "infosys", "hcltech", "wipro", "techm", "lti_group"]
d = yoy.merge(core[["firm", "cal_q", "rev_usd", "headcount"]], on=["firm", "cal_q"], how="left")
q = pd.concat([d[d.firm.isin(ENT[:5])], lti_group_quarterly()], ignore_index=True)
q = q.set_index(["firm", "cal_q"]).sort_index()
q["du_alt"] = q["du"]
q["gL_alt"] = q["gL"]
for cq in du_incl.index:
    if ("infosys", cq) in q.index:
        q.loc[("infosys", cq), "du_alt"] = du_incl[cq]
        q.loc[("infosys", cq), "gL_alt"] = gL_ex.get(cq, np.nan)


def fy_metrics(firm, quarters):
    out = {}

    def get(col, qq):
        return q[col].get((firm, qq), np.nan)
    base = np.array([get("rev_usd", qadd(qq, -4)) for qq in quarters], dtype=float)
    cur = np.array([get("rev_usd", qq) for qq in quarters], dtype=float)
    for lab, col in [("rev_usd", "gR_usd"), ("rev_cc", "gR")]:
        g = np.array([get(col, qq) for qq in quarters], dtype=float)
        ok = np.isfinite(g).all() and np.isfinite(base).all()
        out[lab] = 100 * np.log((base * np.exp(g / 100)).sum() / base.sum()) if ok else np.nan
    for lab, col in [("headcount", "gL"), ("util_change", "du"), ("util_change_trainee_incl", "du_alt"),
                     ("headcount_ex_trainees", "gL_alt")]:
        g = np.array([get(col, qq) for qq in quarters], dtype=float)
        out[lab] = g.mean() if np.isfinite(g).all() else np.nan
    out["weight_rev_usd"] = cur.sum() if np.isfinite(cur).all() else np.nan
    return out


F = pd.DataFrame([dict(firm=f, fy=fy, **fy_metrics(f, fy_quarters(fy))) for fy in range(2016, 2027) for f in ENT])

# cross-currency effect by FY: mean (USD growth - cc growth) over firms reporting both; used to impute cc where missing
F["fx_gap"] = F.rev_usd - F.rev_cc
fx = F.groupby("fy").fx_gap.mean()
fxn = F.groupby("fy").fx_gap.count()
F["rev_cc_imp"] = F.rev_cc.where(F.rev_cc.notna(), F.rev_usd - F.fy.map(fx))
F["cc_imputed"] = F.rev_cc.isna() & F.rev_cc_imp.notna()

F["rpe_cc"] = F.rev_cc - F.headcount
F["rpe_usd"] = F.rev_usd - F.headcount
F["rpe_cc_imp"] = F.rev_cc_imp - F.headcount
F["residual"] = F.rpe_cc - F.util_change                                  # pilot definition
F["residual_imp"] = F.rpe_cc_imp - F.util_change                          # + imputed cc (TechM FY17-20, LTI FY17-23)
inf_mask = F.firm == "infosys"
# Infosys trainee fix A: trainee-inclusive utilisation (consistent with total headcount)
F["residual_trA"] = F.residual.where(~inf_mask, F.rpe_cc - F.util_change_trainee_incl)
F["residual_imp_trA"] = F.residual_imp.where(~inf_mask, F.rpe_cc_imp - F.util_change_trainee_incl)
# Infosys trainee fix B: headcount excluding implied trainees, utilisation excluding trainees
F["residual_trB"] = F.residual.where(~inf_mask, F.rev_cc - F.headcount_ex_trainees - F.util_change)
F.round(3).to_csv(OUT / "firm_year_panel.csv", index=False)
pd.DataFrame({"fy": fx.index, "fx_gap_mean_usd_minus_cc": fx.values, "n_firms": fxn.values}).round(3).to_csv(
    OUT / "fx_gap_by_fy.csv", index=False)

# ---------------------------------------------------------------- replication of Table B
PRE_ALL = list(range(2016, 2024))
POST = [2024, 2025, 2026]
tb = pd.read_csv(ROOT / "output/final/table_B.csv")
rep = []
for lab, yrs in [("FY16-FY23", PRE_ALL), ("FY16-FY23 excl. FY21 (COVID)", [y for y in PRE_ALL if y != 2021]),
                 ("FY24-FY26", POST)]:
    v = F[F.fy.isin(yrs) & F.residual.notna()]
    orig = tb[(tb.window == lab) & (tb.metric == "residual")].mean_firm_years.iloc[0]
    rep.append(dict(window=lab, recomputed=round(v.residual.mean(), 3), table_B=orig, n_firm_years=len(v)))
rep = pd.DataFrame(rep)
rep.to_csv(OUT / "replication_check.csv", index=False)
print(rep.to_string())
assert (rep.recomputed - rep.table_B).abs().max() < 0.002


# ---------------------------------------------------------------- estimators
MIN_PRE = 2   # a firm enters the within-firm estimator only with >= 2 baseline firm-years


def within_firms(df, col, pre, post):
    x = df[df[col].notna()]
    npre = x[x.fy.isin(pre)].groupby("firm").size()
    npost = x[x.fy.isin(post)].groupby("firm").size()
    return sorted(f for f in npre.index if npre[f] >= MIN_PRE and npost.get(f, 0) >= 1)


def estimators(df, col, pre, post):
    """df: firm, fy, col. Returns pooled (Table B style) and within-firm (equal firm weight) Delta."""
    x = df[df[col].notna()]
    a, b = x[x.fy.isin(pre)], x[x.fy.isin(post)]
    pooled = b[col].mean() - a[col].mean() if len(a) and len(b) else np.nan
    both = within_firms(df, col, pre, post)
    if both:
        dif = [b[b.firm == f][col].mean() - a[a.firm == f][col].mean() for f in both]
        within = float(np.mean(dif))
    else:
        within, dif = np.nan, []
    return pooled, within, both, dict(zip(both, dif))


# ---------------------------------------------------------------- D27 noise simulation
NP = json.load(open(ROOT / "output/noise_params.json"))
mi = [NP["metrics"].index(m) for m in ("gR", "gL", "du")]
RHO = np.array(NP["rho"])[mi]
OMC = np.array(NP["omega_common"])[np.ix_(mi, mi)]
IDIO_KEY = {"tcs": "tcs", "infosys": "infosys", "hcltech": "hcltech", "wipro": "wipro", "techm": "techm",
            "lti_group": "ltim"}
OMI = {f: np.array(NP["omega_idio"][k])[np.ix_(mi, mi)] for f, k in IDIO_KEY.items()}
QS = [f"{y}Q{k}" for y in range(2013, 2027) for k in range(1, 5)]
QS = [x for x in QS if x <= "2026Q1"]
QI = {x: i for i, x in enumerate(QS)}


def simulate_panel(nsim, scale=1.0):
    """Returns array [nsim, firm, fy(2016..2026), 3 metrics] of annual means of quarterly YoY noise."""
    T = len(QS)
    Lc = np.linalg.cholesky(OMC + 1e-9 * np.eye(3))
    Li = {f: np.linalg.cholesky(OMI[f] + 1e-9 * np.eye(3)) for f in ENT}
    common = rng.standard_normal((nsim, T, 3)) @ Lc.T
    out = np.zeros((nsim, len(ENT), 11, 3))
    stat_sd = np.sqrt(np.diag(OMC + np.mean([OMI[f] for f in ENT], axis=0)) / (1 - RHO ** 2))
    for j, f in enumerate(ENT):
        v = common + rng.standard_normal((nsim, T, 3)) @ Li[f].T
        x = np.zeros((nsim, T, 3))
        x[:, 0] = rng.standard_normal((nsim, 3)) * stat_sd
        for t in range(1, T):
            x[:, t] = RHO * x[:, t - 1] + v[:, t]
        for k, fy in enumerate(range(2016, 2027)):
            idx = [QI[z] for z in fy_quarters(fy)]
            out[:, j, k] = x[:, idx].mean(axis=1)
    return out * scale


NSIM = 4000
SIM = simulate_panel(NSIM)
SIM_RES = SIM[..., 0] - SIM[..., 1] - SIM[..., 2]        # residual noise: gR - gL - du
SIM_RPE = SIM[..., 0] - SIM[..., 1]
SIM_DU = SIM[..., 2]
FYI = {fy: k for k, fy in enumerate(range(2016, 2027))}
FI = {f: j for j, f in enumerate(ENT)}

# calibration check: empirical within-firm SD of annual residual (demeaned by firm, pre window) vs simulated
emp = F[F.fy.isin(PRE_ALL) & F.residual_imp.notna()].copy()
emp["dm"] = emp.residual_imp - emp.groupby("firm").residual_imp.transform("mean")
emp_sd = np.sqrt((emp.dm ** 2).sum() / (len(emp) - emp.firm.nunique()))
emp_ex = emp[~emp.fy.isin([2021])].copy()
emp_ex["dm"] = emp_ex.residual_imp - emp_ex.groupby("firm").residual_imp.transform("mean")
emp_sd_ex = np.sqrt((emp_ex.dm ** 2).sum() / (len(emp_ex) - emp_ex.firm.nunique()))
sim_sd = []
for _, r in emp.iterrows():
    pass
mask_fy = [FYI[y] for y in PRE_ALL]
s = SIM_RES[:, :, mask_fy]
s = s - s.mean(axis=2, keepdims=True)
sim_sd = float(np.sqrt((s ** 2).mean() * len(mask_fy) / (len(mask_fy) - 1)))
SCALE = max(1.0, emp_sd / sim_sd)
pd.DataFrame([dict(empirical_sd_annual_residual_within_firm_FY16_23=emp_sd,
                   empirical_sd_excl_FY21=emp_sd_ex, d27_implied_sd=sim_sd, scale_used=SCALE,
                   note="SE from D27 simulation is multiplied by scale_used (>=1) when empirical dispersion exceeds the model's")
              ]).round(3).to_csv(OUT / "noise_check.csv", index=False)
print("noise check: empirical", round(emp_sd, 2), "excl FY21", round(emp_sd_ex, 2), "D27", round(sim_sd, 2))


def d27_se(df, col, pre, post, sim=SIM_RES):
    """SD of the estimators under the D27 noise model, for the observed firm-year pattern of `col`."""
    x = df[df[col].notna() & df.fy.isin(pre + post)]
    pooled, within = [], []
    pre_idx = [(FI[f], FYI[y]) for f, y in zip(x.firm, x.fy) if y in pre]
    post_idx = [(FI[f], FYI[y]) for f, y in zip(x.firm, x.fy) if y in post]
    pa = np.array([sim[:, j, k] for j, k in pre_idx]).T
    pb = np.array([sim[:, j, k] for j, k in post_idx]).T
    pooled = pb.mean(axis=1) - pa.mean(axis=1)
    both = within_firms(df, col, pre, post)
    if both:
        w = []
        for f in both:
            ia = [k for (j, k) in pre_idx if j == FI[f]]
            ib = [k for (j, k) in post_idx if j == FI[f]]
            w.append(sim[:, FI[f], ib].mean(axis=1) - sim[:, FI[f], ia].mean(axis=1))
        within = np.mean(w, axis=0)
    else:
        within = np.full(NSIM, np.nan)
    return np.std(pooled) * SCALE, np.std(within) * SCALE


def pigeonhole(df, col, pre, post, B=4000):
    """Two-way bootstrap: resample firms and (separately within each window) years; common year shocks stay together."""
    x = df[df[col].notna()]
    firms = within_firms(df, col, pre, post)
    piv = x.pivot(index="firm", columns="fy", values=col)
    pooled_b, within_b = [], []
    for _ in range(B):
        fs = rng.choice(firms, len(firms))
        ya = rng.choice(pre, len(pre))
        yb = rng.choice(post, len(post))
        A = np.array([[piv.at[f, y] if (f in piv.index and y in piv.columns) else np.nan for y in ya] for f in fs])
        Bm = np.array([[piv.at[f, y] if (f in piv.index and y in piv.columns) else np.nan for y in yb] for f in fs])
        if np.isfinite(A).sum() and np.isfinite(Bm).sum():
            pooled_b.append(np.nanmean(Bm) - np.nanmean(A))
        ok = np.isfinite(A).any(axis=1) & np.isfinite(Bm).any(axis=1)
        if ok.any():
            with np.errstate(all="ignore"):
                within_b.append(np.mean(np.nanmean(Bm[ok], axis=1) - np.nanmean(A[ok], axis=1)))
    return np.array(pooled_b), np.array(within_b)


from scipy import stats


def yearcluster_t(df, col, pre, post, level=0.95):
    """Within-firm deviations from each firm's own baseline mean, averaged by year (common shocks stay together);
    Delta = mean of post-year means - mean of pre-year means; t interval with year-level variance (df = years - 2)."""
    x = df[df[col].notna()]
    fs = within_firms(df, col, pre, post)
    x = x[x.firm.isin(fs) & x.fy.isin(pre + post)].copy()
    if x.empty:
        return np.nan, np.nan, np.nan, np.nan
    x["dev"] = x[col] - x.firm.map(x[x.fy.isin(pre)].groupby("firm")[col].mean())
    m = x.groupby("fy").dev.mean()
    a, b = m[m.index.isin(pre)], m[m.index.isin(post)]
    delta = b.mean() - a.mean()
    ss = ((a - a.mean()) ** 2).sum() + ((b - b.mean()) ** 2).sum()
    dof = len(a) + len(b) - 2
    se = np.sqrt(ss / dof * (1 / len(a) + 1 / len(b)))
    tq = stats.t.ppf(0.5 + level / 2, dof)
    return delta, se, delta - tq * se, delta + tq * se


# ---------------------------------------------------------------- variants
WINDOWS = {
    "base: FY16-23 vs FY24-26": PRE_ALL,
    "excl. FY21": [y for y in PRE_ALL if y != 2021],
    "excl. FY22-23 (boom)": [y for y in PRE_ALL if y not in (2022, 2023)],
    "baseline FY16-20 only": list(range(2016, 2021)),
}
SERIES = {
    "pilot (cc only)": "residual",
    "cc + imputed cc (TechM FY17-20, LTI FY17-23)": "residual_imp",
    "pilot + Infosys trainee-incl. utilisation": "residual_trA",
    "imputed cc + Infosys trainee-incl. utilisation": "residual_imp_trA",
    "pilot + Infosys headcount ex trainees": "residual_trB",
}
rows = []
for sname, col in SERIES.items():
    for wname, pre in WINDOWS.items():
        pooled, within, both, firmdif = estimators(F, col, pre, POST)
        se_p, se_w = d27_se(F, col, pre, POST)
        bp, bw = pigeonhole(F, col, pre, POST, B=2000)
        yc, yc_se, yc_lo, yc_hi = yearcluster_t(F, col, pre, POST)
        x = F[F[col].notna()]
        rows.append(dict(
            series=sname, window=wname,
            n_firm_years_pre=int(x.fy.isin(pre).sum()), n_firm_years_post=int(x.fy.isin(POST).sum()),
            firms_within=";".join(both),
            pooled=pooled, pooled_d27_se=se_p, pooled_d27_lo95=pooled - 1.96 * se_p, pooled_d27_hi95=pooled + 1.96 * se_p,
            pooled_boot_lo95=np.percentile(bp, 2.5), pooled_boot_hi95=np.percentile(bp, 97.5),
            within=within, within_d27_se=se_w, within_d27_lo95=within - 1.96 * se_w, within_d27_hi95=within + 1.96 * se_w,
            within_boot_lo95=np.nanpercentile(bw, 2.5) if len(bw) else np.nan,
            within_boot_hi95=np.nanpercentile(bw, 97.5) if len(bw) else np.nan,
            yearclust=yc, yearclust_se=yc_se, yearclust_lo95=yc_lo, yearclust_hi95=yc_hi,
            firm_deltas=";".join(f"{k}:{v:+.2f}" for k, v in firmdif.items())))
E = pd.DataFrame(rows)
E.round(3).to_csv(OUT / "m1_firm_estimates.csv", index=False)
pd.set_option("display.width", 250)
print(E[["series", "window", "pooled", "within", "within_d27_se", "within_boot_lo95", "within_boot_hi95",
         "yearclust", "yearclust_lo95", "yearclust_hi95", "firm_deltas"]].round(2).to_string())

# ---------------------------------------------------------------- TCS / HCLTech bounds
brows = []
for wname, pre in WINDOWS.items():
    # peers' Delta util (within firm), any firm with util change in both windows
    peers = {}
    for f in ["infosys", "wipro", "techm", "lti_group", "hcltech"]:
        x = F[(F.firm == f) & F.util_change.notna()]
        a, b = x[x.fy.isin(pre)], x[x.fy.isin(POST)]
        if len(a) and len(b):
            peers[f] = b.util_change.mean() - a.util_change.mean()
    lo, hi = min(peers.values()), max(peers.values())
    # Infosys trainee-incl. alternative also counts as a plausible peer value
    xa = F[(F.firm == "infosys") & F.util_change_trainee_incl.notna()]
    alt = xa[xa.fy.isin(POST)].util_change_trainee_incl.mean() - xa[xa.fy.isin(pre)].util_change_trainee_incl.mean()
    # D27 SE of the peer-mean Delta util is not needed for the range; SE of Delta rpe for TCS/HCL from D27 (gR-gL)
    for f in ["tcs", "hcltech"]:
        x = F[(F.firm == f) & F.rpe_cc.notna()]
        a, b = x[x.fy.isin(pre)], x[x.fy.isin(POST)]
        drpe = b.rpe_cc.mean() - a.rpe_cc.mean()
        ia, ib = [FYI[y] for y in a.fy], [FYI[y] for y in b.fy]
        se = np.std(SIM_RPE[:, FI[f], ib].mean(axis=1) - SIM_RPE[:, FI[f], ia].mean(axis=1)) * SCALE
        brows.append(dict(window=wname, firm=f, delta_rpe_cc=drpe, delta_rpe_d27_se=se,
                          n_pre=len(a), n_post=len(b),
                          peer_delta_util=";".join(f"{k}:{v:+.2f}" for k, v in peers.items()),
                          infosys_delta_util_trainee_incl=alt,
                          peer_delta_util_min=lo, peer_delta_util_max=hi,
                          peer_delta_util_mean=np.mean(list(peers.values())),
                          delta_residual_lo=drpe - hi, delta_residual_mid=drpe - np.mean(list(peers.values())),
                          delta_residual_hi=drpe - lo,
                          delta_residual_lo95=drpe - hi - 1.96 * se, delta_residual_hi95=drpe - lo + 1.96 * se))
BD = pd.DataFrame(brows)
BD.round(3).to_csv(OUT / "m1_tcs_hcl_bounds.csv", index=False)
print(BD[["window", "firm", "delta_rpe_cc", "delta_rpe_d27_se", "peer_delta_util", "delta_residual_lo",
          "delta_residual_mid", "delta_residual_hi"]].round(2).to_string())

# ---------------------------------------------------------------- top-six combination
w26 = F[F.fy == 2026].set_index("firm").weight_rev_usd
trows = []
for sname, col in [("cc + imputed cc", "residual_imp"), ("imputed cc + Infosys trainee-incl.", "residual_imp_trA")]:
    for wname, pre in WINDOWS.items():
        _, _, _, firmdif = estimators(F, col, pre, POST)
        b = BD[BD.window == wname].set_index("firm")
        obs = {k: v for k, v in firmdif.items() if k not in ("tcs", "hcltech")}
        lo = dict(obs, tcs=b.at["tcs", "delta_residual_lo"], hcltech=b.at["hcltech", "delta_residual_lo"])
        mid = dict(obs, tcs=b.at["tcs", "delta_residual_mid"], hcltech=b.at["hcltech", "delta_residual_mid"])
        hi = dict(obs, tcs=b.at["tcs", "delta_residual_hi"], hcltech=b.at["hcltech", "delta_residual_hi"])
        fs = sorted(lo)
        ww = w26.reindex(fs)
        trows.append(dict(series=sname, window=wname, firms=";".join(fs),
                          eq_lo=np.mean([lo[f] for f in fs]), eq_mid=np.mean([mid[f] for f in fs]),
                          eq_hi=np.mean([hi[f] for f in fs]),
                          revw_lo=np.average([lo[f] for f in fs], weights=ww),
                          revw_mid=np.average([mid[f] for f in fs], weights=ww),
                          revw_hi=np.average([hi[f] for f in fs], weights=ww),
                          observed_firms_mean=np.mean(list(obs.values()))))
T6 = pd.DataFrame(trows)
T6.round(3).to_csv(OUT / "m1_top6_range.csv", index=False)
print(T6.round(2).to_string())
