"""M1 at sector scope (exports per PLFS worker) and evidence on pi (non-AI price drift).

    python3 data/explore/round4/residual/m1_sector_pi.py

Inputs (read only):
  data/explore/trade/imf_bop_india_services_quarterly.csv      BoP computer services (SI2) and ICT (SI) exports, quarterly
  data/explore/trade/rbi_survey_orgtype.csv                    RBI software & ITeS exports survey, FY totals (FY18 missing)
  data/explore/round3/plfs/employment_levels_long.csv          PLFS employment levels with SEs
  data/explore/round3/plfs/earnings_regular_salaried.csv       PLFS earnings, regular salaried, NIC 62/63, by age band
  data/corrected/core_quarterly_final.csv                      INR/USD implied by Infosys revenue (INR / USD)
  data/explore/round3/seniority_firms/cost_per_head.csv        firm employee cost per head (INR)
  data/explore/prices/price_indices_quarterly.csv              UK SPPI / US PPI / ECI (charge-out rates, wages)
Outputs (this folder): sector_rpw_by_round.csv, sector_m1_changes.csv, pi_wage_evidence.csv, pi_price_index_evidence.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent

# ---------------------------------------------------------------- PLFS rounds: quarters covered and time midpoints
ROUNDS = {f"{y}-{(y + 1) % 100:02d}": ([f"{y}-Q3", f"{y}-Q4", f"{y + 1}-Q1", f"{y + 1}-Q2"], y + 1.0)
          for y in range(2017, 2024)}
ROUNDS["cy2024"] = (["2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4"], 2024.5)
ROUNDS["cy2025"] = (["2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4"], 2025.5)
DESIGN = {"2017-18": "A (1,115 strata)", "2018-19": "A (1,115 strata)", "2019-20": "A (1,115 strata)",
          "2020-21": "A (1,115 strata)", "2021-22": "B (985 strata)", "2022-23": "B (985 strata)",
          "2023-24": "C (910 strata)", "cy2024": "C (910 strata; shares Jan-Jun 2024 with 2023-24)",
          "cy2025": "D (revamped monthly design)"}

bop = pd.read_csv(ROOT / "data/explore/trade/imf_bop_india_services_quarterly.csv")
bop = bop[(bop.BOP_ACCOUNTING_ENTRY == "CD_T")]
bopq = bop.pivot(index="TIME_PERIOD", columns="INDICATOR", values="OBS_VALUE") / 1e9

rbi = pd.read_csv(ROOT / "data/explore/trade/rbi_survey_orgtype.csv").set_index("fy").total_usd_bn


def rbi_for_round(r):
    """RBI FY (Apr-Mar) totals mapped to PLFS windows by months of overlap. FY2017-18 is not in the repo."""
    def fy(y):   # FY ending March y
        return rbi.get(f"{y - 1}-{y % 100:02d}", np.nan)
    if r.startswith("cy"):
        y = int(r[2:])
        return 0.25 * fy(y) + 0.75 * fy(y + 1)
    y = int(r[:4])
    return 0.75 * fy(y + 1) + 0.25 * fy(y + 2)     # Jul y - Jun y+1: 9 months of FY(y+1), 3 of FY(y+2)


plfs = pd.read_csv(ROOT / "data/explore/round3/plfs/employment_levels_long.csv")
plfs = plfs[plfs.cut == "all"].set_index(["round", "group"])

rows = []
for r, (qs, mid) in ROUNDS.items():
    ok = all(q in bopq.index for q in qs)
    rows.append(dict(round=r, midpoint=mid, design=DESIGN[r],
                     bop_computer_usd_bn=bopq.loc[qs, "SI2"].sum() if ok else np.nan,
                     bop_ict_usd_bn=bopq.loc[qs, "SI"].sum() if ok else np.nan,
                     rbi_total_usd_bn=rbi_for_round(r),
                     plfs_nic62_63=plfs.loc[(r, "nic62_63"), "estimate"],
                     plfs_nic62_63_se=plfs.loc[(r, "nic62_63"), "se"],
                     plfs_it_ites=plfs.loc[(r, "it_ites"), "estimate"],
                     plfs_it_ites_se=plfs.loc[(r, "it_ites"), "se"]))
S = pd.DataFrame(rows)
S["rpw_bop_computer_usd_k"] = S.bop_computer_usd_bn * 1e6 / S.plfs_nic62_63
S["rpw_rbi_total_usd_k"] = S.rbi_total_usd_bn * 1e6 / S.plfs_it_ites            # matched: IT + ITeS both sides
S["rpw_rbi_total_over_nic62_63_usd_k"] = S.rbi_total_usd_bn * 1e6 / S.plfs_nic62_63
S.round(3).to_csv(OUT / "sector_rpw_by_round.csv", index=False)
print(S.round(2).to_string())
S = S.set_index("round")

PAIRS = {   # name: (pre start, pre end, post start, post end)
    "main: 2017-18->2022-23 vs 2022-23->CY2025": ("2017-18", "2022-23", "2022-23", "cy2025"),
    "avoid 2025 design break: post 2022-23->CY2024": ("2017-18", "2022-23", "2022-23", "cy2024"),
    "within-design only: pre 2017-18->2020-21 (A), post 2023-24->CY2024 (C)": ("2017-18", "2020-21", "2023-24", "cy2024"),
    "pre within design A, post 2022-23->CY2025": ("2017-18", "2020-21", "2022-23", "cy2025"),
    "RBI-compatible: 2018-19->2022-23 vs 2022-23->CY2025": ("2018-19", "2022-23", "2022-23", "cy2025"),
}
SERIES = {"BoP computer services / PLFS NIC 62+63": ("bop_computer_usd_bn", "plfs_nic62_63"),
          "RBI survey total / PLFS NIC 62+63+822": ("rbi_total_usd_bn", "plfs_it_ites"),
          "RBI survey total / PLFS NIC 62+63": ("rbi_total_usd_bn", "plfs_nic62_63")}
out = []
for sname, (num, den) in SERIES.items():
    for pname, (a, b, c, d) in PAIRS.items():
        if S.loc[[a, b, c, d], num].isna().any():
            continue
        T1, T2 = S.at[b, "midpoint"] - S.at[a, "midpoint"], S.at[d, "midpoint"] - S.at[c, "midpoint"]

        def g(x, y, col, T):
            return 100 * np.log(S.at[y, col] / S.at[x, col]) / T
        pre_rpw = g(a, b, num, T1) - g(a, b, den, T1)
        post_rpw = g(c, d, num, T2) - g(c, d, den, T2)
        # sampling variance from PLFS only (exports treated as fixed); rounds treated as independent samples
        rse = {k: S.at[k, den + "_se"] / S.at[k, den] for k in {a, b, c, d}}
        coef = {k: 0.0 for k in rse}
        coef[d] += 1 / T2; coef[c] -= 1 / T2; coef[b] += 1 / T1; coef[a] -= 1 / T1   # on log L, with sign flipped
        se = 100 * np.sqrt(sum((coef[k] * rse[k]) ** 2 for k in rse))
        out.append(dict(series=sname, windows=pname, pre_years=T1, post_years=T2,
                        pre_exports_growth=g(a, b, num, T1), pre_employment_growth=g(a, b, den, T1),
                        pre_rpw_growth=pre_rpw,
                        post_exports_growth=g(c, d, num, T2), post_employment_growth=g(c, d, den, T2),
                        post_rpw_growth=post_rpw, delta=post_rpw - pre_rpw, delta_se_plfs=se,
                        delta_lo95=post_rpw - pre_rpw - 1.96 * se, delta_hi95=post_rpw - pre_rpw + 1.96 * se))
SC = pd.DataFrame(out)
SC.round(2).to_csv(OUT / "sector_m1_changes.csv", index=False)
pd.set_option("display.width", 250)
print(SC.drop(columns=["pre_years", "post_years"]).round(1).to_string())

# ---------------------------------------------------------------- pi: wage evidence
core = pd.read_csv(ROOT / "data/corrected/core_quarterly_final.csv", dtype={"cal_q": str})
inf = core[core.firm == "infosys"].set_index("cal_q")
inr_per_usd = (inf.rev_inr / inf.rev_usd)          # INR mn / USD mn; check units by level
inr_per_usd = inr_per_usd * (83 / inr_per_usd.loc["2024Q1"]) if inr_per_usd.loc["2024Q1"] > 1000 else inr_per_usd


def fx_round(r):
    qs = [q.replace("-", "") for q in ROUNDS[r][0]]
    return inr_per_usd.reindex(qs).mean()


fxr = {r: fx_round(r) for r in ROUNDS}
earn = pd.read_csv(ROOT / "data/explore/round3/plfs/earnings_regular_salaried.csv")
earn = earn[earn["sample"] == "cws_regular_nic62_63"].set_index(["round", "age_band"])
wrows = []
for band in ["21-25", "26-30", "31-40"]:
    for pname, (a, b, c, d) in PAIRS.items():
        T1, T2 = S.at[b, "midpoint"] - S.at[a, "midpoint"], S.at[d, "midpoint"] - S.at[c, "midpoint"]

        def gw(x, y, T, usd):
            w0, w1 = earn.at[(x, band), "mean_inr"], earn.at[(y, band), "mean_inr"]
            fxadj = np.log(fxr[y] / fxr[x]) if usd else 0.0
            return 100 * (np.log(w1 / w0) - fxadj) / T
        for usd in (False, True):
            pre, post = gw(a, b, T1, usd), gw(c, d, T2, usd)
            rse = {k: earn.at[(k, band), "mean_se"] / earn.at[(k, band), "mean_inr"] for k in {a, b, c, d}}
            coef = {k: 0.0 for k in rse}
            coef[d] += 1 / T2; coef[c] -= 1 / T2; coef[b] -= 1 / T1; coef[a] += 1 / T1
            se = 100 * np.sqrt(sum((coef[k] * rse[k]) ** 2 for k in rse))
            wrows.append(dict(source="PLFS mean earnings, regular salaried, NIC 62/63", age_band=band, windows=pname,
                              currency="USD" if usd else "INR", pre_growth=pre, post_growth=post,
                              delta=post - pre, delta_se=se))
cph = pd.read_csv(ROOT / "data/explore/round3/seniority_firms/cost_per_head.csv")
cph["fyn"] = cph.fy.str[2:].astype(int) + 2000
fxfy = {fy: inr_per_usd.reindex([f"{fy - 1}Q2", f"{fy - 1}Q3", f"{fy - 1}Q4", f"{fy}Q1"]).mean() for fy in range(2012, 2027)}
for f, x in cph.groupby("firm"):
    x = x.set_index("fyn").sort_index()
    x["usd_yoy"] = x.yoy_log_x100 - 100 * np.log(pd.Series(fxfy).reindex(x.index) / pd.Series(fxfy).reindex(x.index - 1).values)
    for wname, pre in [("FY17-23 vs FY24-26", range(2017, 2024)), ("FY17-20 vs FY24-26", range(2017, 2021))]:
        for cur, col in [("INR", "yoy_log_x100"), ("USD", "usd_yoy")]:
            a = x.loc[x.index.isin(pre), col].dropna()
            b = x.loc[x.index.isin([2024, 2025, 2026]), col].dropna()
            wrows.append(dict(source=f"firm employee cost per head ({f}); composition-affected", age_band="all",
                              windows=wname, currency=cur, pre_growth=a.mean(), post_growth=b.mean(),
                              delta=b.mean() - a.mean(), delta_se=np.nan))
W = pd.DataFrame(wrows)
W.round(2).to_csv(OUT / "pi_wage_evidence.csv", index=False)
print(W[W.windows.str.startswith(("main", "avoid", "FY"))].round(2).to_string())
print("INR/USD by round:", {k: round(v, 1) for k, v in fxr.items()})

# ---------------------------------------------------------------- pi: price indices (charge-out rates, wages)
P = pd.read_csv(ROOT / "data/explore/prices/price_indices_quarterly.csv", dtype={"cal_q": str})
P["year"] = P.cal_q.str[:4].astype(int)
covid = ["2020Q2", "2020Q3", "2020Q4", "2021Q1", "2021Q2"]
prow = []
for s, x in P.groupby("series"):
    x = x[x.yoy_log100.notna() & ~x.cal_q.isin(covid)]
    for wname, pre in [("2016-22 vs 2023-26", range(2016, 2023)), ("2016-19 vs 2023-26", range(2016, 2020))]:
        a = x[x.year.isin(pre)].yoy_log100
        b = x[x.year >= 2023].yoy_log100
        prow.append(dict(series=s, windows=wname, pre_mean_yoy=a.mean(), post_mean_yoy=b.mean(),
                         delta=b.mean() - a.mean(), n_pre_q=len(a), n_post_q=len(b),
                         last_q=x.cal_q.max()))
PI = pd.DataFrame(prow)
PI.round(2).to_csv(OUT / "pi_price_index_evidence.csv", index=False)
print(PI.round(2).to_string())
