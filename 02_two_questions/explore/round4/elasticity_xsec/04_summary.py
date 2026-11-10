"""M6 step 4: summary tables.
 rbi_growth_by_year.csv  YoY log growth (INR, %) by RBI activity, FY20-FY26 (FX cancels in cross-activity contrasts)
 listed_segment_growth.csv  FY23-26 listed-panel growth by segment (copied from round3/listed_panel; no pre-2023 baseline)
 m6_summary.csv  one row per design x mapping at phi*s_bar = 2.5 (or G = 2.5 for binary maps): eps, band, sign of
                 exposure ordering, and whether the implied eps lies in a plausible [0, 4] range."""
from pathlib import Path
import numpy as np, pandas as pd
HERE = Path(__file__).resolve().parent
r = pd.read_csv(HERE / "rbi_activity_exports.csv").sort_values(["activity", "fy"])
r["g_inr"] = 100 * np.log(r.inr_crore / r.groupby("activity").inr_crore.shift())
gy = r.pivot(index="fy", columns="activity", values="g_inr").round(1)
gy.to_csv(HERE / "rbi_growth_by_year.csv")
print(gy.to_string())
lp = pd.read_csv(HERE.parents[1] / "round3/listed_panel/listed_panel_summary.csv")
lp = lp[lp.set.isin(["mid4", "ITservices_ex_mid4_7", "ERD_5", "ITeS_BPM_5"]) & lp.metric.isin(["rev_inr_cr", "rev_usd_mn", "hc"])]
lp = lp[["set", "metric", "n_firms", "agg_cagr_FY23_26", "agg_pct_change_FY23_26", "note"]]
lp.to_csv(HERE / "listed_segment_growth.csv", index=False)
print(lp.to_string())
F = pd.read_csv(HERE / "eps_firm_estimates.csv")
F = F[((F.phi_s_bar == 2.5) | (F.gap_G == 2.5))]
F = F[["design", "baseline_window", "mapping", "mean_abs_dc", "eps", "ci95_lo", "ci95_hi", "p_signflip", "loo_eps_min", "loo_eps_max"]]
B = pd.read_csv(HERE / "eps_rbi_estimates.csv")
B = B[(B.phi_s_bar == 2.5) | ((B.mapping == "binary_BPO_high") & (B.dc == 2.5))]
B = B.rename(columns={"baseline": "baseline_window"})
B["ci95_lo"] = B.eps - 1.96 * B.se_noise_if_sigma3
B["ci95_hi"] = B.eps + 1.96 * B.se_noise_if_sigma3
B["mean_abs_dc"] = B.dc.abs()
B["mapping"] = B.mapping + " [" + B.contrast + "]"
S = pd.concat([F, B[["design", "baseline_window", "mapping", "mean_abs_dc", "eps", "ci95_lo", "ci95_hi"]]])
S["eps_in_0_4"] = S.eps.between(0, 4)
S.round(2).to_csv(HERE / "m6_summary.csv", index=False)
print(S.round(2).to_string())
