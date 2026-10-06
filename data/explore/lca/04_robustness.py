"""Robustness of the exposure contrast to firm-level SOC recoding breaks (e.g. Cognizant 15-1211 -> 15-1299 in 2023-24,
Infosys 15-1121 -> 15-1199 in 2020). Case counts (certified), TTM, YoY log x100.
 R1: Eloundou-tercile contrast on 'stable-coding' firms only (TCS, Wipro, HCLTech, Accenture, TechM).
 R2: job-title contrast: titles with TEST/QA/QUALITY/DEVELOPER/PROGRAMMER (high exposure) vs
     ARCHITECT/MANAGER/CONSULTANT/LEAD/ANALYST-BUSINESS (low exposure); all 8 firms.
 R3: SOC-2018-only fine contrast (15-1252+15-1253 vs 15-1211+15-1232+15-1241+15-1244+13-1111), YoY available from 2023Q2.
"""
import os, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(f"{HERE}/03_analysis.py").read().split("# ------------------------------------------------------------------ measure switch")[0])  # reuse exposure/terciles
MAIN8 = ["tcs", "infosys", "hcltech", "wipro", "techm", "ltim", "cognizant", "accenture"]
STABLE = ["tcs", "wipro", "hcltech", "accenture", "techm"]
C["n"] = 1.0
ex = lambda idx: ~((idx >= pd.Period("2020Q2", "Q")) & (idx <= pd.Period("2021Q2", "Q")))
PRE = lambda idx: (idx >= pd.Period("2015Q1", "Q")) & (idx <= pd.Period("2022Q4", "Q")) & ex(idx)
POST = lambda idx: (idx >= pd.Period("2023Q1", "Q")) & (idx <= pd.Period("2026Q2", "Q"))
tg = grp.terc_beta_gpt4.to_dict(); C["terc"] = C.occ_group.map(tg)


def ttm_yoy(mask, firms):
    s = C[mask & C.firm_group.isin(firms)].groupby("q").n.sum().reindex(QS).fillna(0).rolling(4).sum()
    return 100 * np.log(s / s.shift(4)).replace([np.inf, -np.inf], np.nan)


def summarize(name, ser):
    ser = ser.dropna(); pre = ser[PRE(ser.index)]; post = ser[POST(ser.index)]
    r = pre - pre.mean()
    ar = np.corrcoef(r.values[1:], r.values[:-1])[0, 1] if len(r) > 4 else np.nan
    print(f"{name:55s} n_pre={len(pre):2d} mean_pre={pre.mean():7.1f} sd={r.std():6.1f} ar1={ar:5.2f} | n_post={len(post):2d} mean_post={post.mean():7.1f} diff={post.mean()-pre.mean() if len(pre) else np.nan:7.1f}")
    return ser


out = {}
out["R1_gpt4_terc_stablefirms"] = summarize("R1 Eloundou tercile hi-lo, stable firms", ttm_yoy(C.terc == "high", STABLE) - ttm_yoy(C.terc == "low", STABLE))
out["R1b_devqa_vs_supnet_stable"] = summarize("R1b DEV+QA vs SUPPORT+NETWORK, stable firms", ttm_yoy(C.occ_group.isin(["DEV", "QA"]), STABLE) - ttm_yoy(C.occ_group.isin(["SUPPORT", "NETWORK"]), STABLE))
jt = C.job_title.fillna("").str.upper()
hi = jt.str.contains(r"TEST|\bQA\b|QUALITY|DEVELOPER|PROGRAMMER")
lo = jt.str.contains(r"ARCHITECT|MANAGER|CONSULTANT|\bLEAD\b|BUSINESS ANALYST") & ~hi
print(f"R2 title coverage (8 firms): high {C[hi & C.firm_group.isin(MAIN8)].shape[0]}, low {C[lo & C.firm_group.isin(MAIN8)].shape[0]}, all {C[C.firm_group.isin(MAIN8)].shape[0]}")
out["R2_title_hi_lo_8firms"] = summarize("R2 job-title hi-lo, 8 firms", ttm_yoy(hi, MAIN8) - ttm_yoy(lo, MAIN8))
out["R2_title_hi_lo_stable"] = summarize("R2 job-title hi-lo, stable firms", ttm_yoy(hi, STABLE) - ttm_yoy(lo, STABLE))
out["R2_title_hi_8firms"] = summarize("R2 job-title hi only (level), 8 firms", ttm_yoy(hi, MAIN8))
out["R2_title_lo_8firms"] = summarize("R2 job-title lo only (level), 8 firms", ttm_yoy(lo, MAIN8))
h18 = C.soc6.isin(["15-1252", "15-1253"]); l18 = C.soc6.isin(["15-1211", "15-1232", "15-1241", "15-1244", "13-1111"])
r3 = ttm_yoy(h18, MAIN8) - ttm_yoy(l18, MAIN8)
r3s = ttm_yoy(h18, STABLE) - ttm_yoy(l18, STABLE)
print("R3 SOC2018 fine contrast (8 firms / stable), 2023Q2+:\n", pd.DataFrame({"8firms": r3, "stable": r3s})[QS >= pd.Period("2023Q2", "Q")].round(1).T.to_string())
out["R3_soc2018_fine_8firms"] = r3; out["R3_soc2018_fine_stable"] = r3s
# annual path of hi-lo title contrast
L = pd.DataFrame(out); L.index = L.index.astype(str); L.index.name = "cal_q"
L.round(2).to_csv(f"{HERE}/lca_robustness_series.csv")
print("\nQ4 values by year:\n", L[L.index.str.endswith("Q4") | (L.index == "2026Q2")].round(1).to_string())
