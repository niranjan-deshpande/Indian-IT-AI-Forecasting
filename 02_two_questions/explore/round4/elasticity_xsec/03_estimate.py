"""M6 step 3: implied epsilon from cross-line variation in AI exposure.
Model (annual growth, %): g_R,j = (eps-1)*c_j + (1-eps)*pi + d_j, with c_j = phi*s_j the AI price cut.
Outcome y_j = mean g_R (recent) - mean g_R (pre-2023 baseline). Within-firm differences remove firm d and FX.
Price cut: c_j = PHI_S_BAR * e_j / mean(e)  (s_j proportional to exposure; PHI_S_BAR illustrative, 2-3 %/yr, M2 pending).
Slope b = eps-1 through the origin in within-firm differences (two lines per firm => identical to firm-FE OLS).
Inference: sign-flip randomisation over firms (2^4 = 16 assignments), leave-one-firm-out, and a noise band
assuming each within-firm contrast carries SIGMA = 3 pp/yr of line-specific drift (DECISIONS D4: uncorrected s.d. of
firm-relative drift changes 3.0 %/yr) plus its own sampling error.
RBI baselines: FY20-23; FY20-23 ex FY21 (COVID); FY20-22 (drops FY23, when the survey frame/grossing and BPO
sub-line classification changed and every activity jumped 20%+).
Outputs: firm_contrasts.csv, eps_firm_estimates.csv, rbi_segment_growth.csv, eps_rbi_estimates.csv"""
from itertools import product
from pathlib import Path
import numpy as np, pandas as pd
HERE = Path(__file__).resolve().parent
PHI_S_BAR = {"low": 2.0, "mid": 2.5, "high": 3.0}
SIGMA = 3.0
lg = pd.read_csv(HERE / "line_growth_firms.csv")
ex = pd.read_csv(HERE / "line_exposure.csv")

PAIRS = {  # firm: (line counted as 'k' = baseline-D2 low, line 'j' = baseline-D2 high); contrast = j - k
    "accenture": ("ACN_Consulting", "ACN_ManagedSvcs"), "cognizant": ("CTSH_ConsultTech", "CTSH_Outsourcing"),
    "hcltech": ("HCL_ERD", "HCL_ITBS"), "techm": ("TECHM_IT", "TECHM_BPS")}
FIRM_LINES = [l for pr in PAIRS.values() for l in pr]

def contrasts(base_window):
    w = lg.pivot_table(index="line", columns="window", values=["mean_g", "sd_g", "n_q"])
    rows = []
    for f, (k, j) in PAIRS.items():
        yj = w.loc[j, ("mean_g", "recent_2024Q2_2026Q2")] - w.loc[j, ("mean_g", base_window)]
        yk = w.loc[k, ("mean_g", "recent_2024Q2_2026Q2")] - w.loc[k, ("mean_g", base_window)]
        # sampling s.e. of a mean of overlapping YoY quarters: treat n_q/4 as effective independent obs
        se2 = 0
        for l in (j, k):
            for win in ("recent_2024Q2_2026Q2", base_window):
                se2 += w.loc[l, ("sd_g", win)] ** 2 / max(w.loc[l, ("n_q", win)] / 4, 1)
        rows.append(dict(firm=f, line_k=k, line_j=j, y_j=yj, y_k=yk, dy=yj - yk, se_sampling=np.sqrt(se2)))
    return pd.DataFrame(rows)

def slope(dc, dy):
    return float(np.sum(dc * dy) / np.sum(dc ** 2))

def infer(dc, dy, se):
    b = slope(dc, dy)
    flips = [slope(dc, dy * np.array(s)) for s in product([1, -1], repeat=len(dy))]
    p_perm = np.mean(np.abs(flips) >= abs(b) - 1e-12)
    loo = [slope(np.delete(dc, i), np.delete(dy, i)) for i in range(len(dy))]
    var_e = SIGMA ** 2 + se ** 2
    se_b = float(np.sqrt(np.sum(dc ** 2 * var_e)) / np.sum(dc ** 2))
    return b, p_perm, min(loo), max(loo), se_b

out, crow = [], []
for base in ("pre_2016_2022", "pre_2016_2019"):
    C = contrasts(base)
    C["baseline_window"] = base
    crow.append(C)
    dy, se = C.dy.values, C.se_sampling.values
    # continuous exposure mappings
    for comp in ("compA", "compB"):
        E = ex[ex.composition == comp].set_index("line")
        for m in ("E_gpt_raw", "E_human_raw", "E_gpt", "E_human", "F_lm"):
            e = E.loc[FIRM_LINES, m]
            for lvl, ps in PHI_S_BAR.items():
                c = ps * E[m] / e.mean()
                dc = np.array([c[j] - c[k] for k, j in PAIRS.values()])
                b, p, lo, hi, seb = infer(dc, dy, se)
                out.append(dict(design="firm_lines", baseline_window=base, mapping=f"{comp}:{m}", phi_s_bar=ps,
                                dc_by_firm=";".join(f"{x:+.2f}" for x in dc), mean_abs_dc=np.abs(dc).mean(),
                                eps_minus_1=b, eps=1 + b, se_noise=seb, ci95_lo=1 + b - 1.96 * seb,
                                ci95_hi=1 + b + 1.96 * seb, p_signflip=p, loo_eps_min=1 + lo, loo_eps_max=1 + hi))
    # binary D2 mappings: high-minus-low price-cut gap G (pp/yr), sign +1 if j is 'high', -1 if 'low', 0 dropped
    BIN = {"D2_baseline": [1, 1, 1, 1], "D2_altA_ERD_high": [1, 1, 0, 1],
           "D2_altB_consulting_high": [-1, -1, 1, 1], "D2_altC_BPS_neutral": [1, 1, 1, 0]}
    for name, sgn in BIN.items():
        sgn = np.array(sgn, float)
        keep = sgn != 0
        for G in (1.0, 2.5):
            dc = (sgn * G)[keep]
            b, p, lo, hi, seb = infer(dc, dy[keep], se[keep])
            out.append(dict(design="firm_lines", baseline_window=base, mapping=name, phi_s_bar=np.nan,
                            gap_G=G, dc_by_firm=";".join(f"{x:+.2f}" for x in sgn * G), mean_abs_dc=G,
                            eps_minus_1=b, eps=1 + b, se_noise=seb, ci95_lo=1 + b - 1.96 * seb,
                            ci95_hi=1 + b + 1.96 * seb, p_signflip=p, loo_eps_min=1 + lo, loo_eps_max=1 + hi))
C = pd.concat(crow)
C.round(3).to_csv(HERE / "firm_contrasts.csv", index=False)
R = pd.DataFrame(out)
R.round(3).to_csv(HERE / "eps_firm_estimates.csv", index=False)
print(C.round(2).to_string())
pd.set_option("display.width", 250)
print(R[R.phi_s_bar.isin([2.5]) | R.mapping.str.startswith("D2")].round(2).drop(columns=["design"]).to_string())

# ------------------------------------------------------------------ RBI activity segments (sector scope)
r = pd.read_csv(HERE / "rbi_activity_exports.csv")
r = r.sort_values(["activity", "fy"])
r["g_inr"] = 100 * np.log(r.inr_crore / r.groupby("activity").inr_crore.shift())
r["g_usd"] = 100 * np.log(r.usd_bn / r.groupby("activity").usd_bn.shift())
W = {"base_FY20_23": ["2019-20", "2020-21", "2021-22", "2022-23"], "base_FY20_22": ["2019-20", "2020-21", "2021-22"], "base_FY20_23_exFY21": ["2019-20", "2021-22", "2022-23"],
     "FY24": ["2023-24"], "recent_FY25_26": ["2024-25", "2025-26"]}
seg = []
for a, s in r.groupby("activity"):
    row = dict(activity=a)
    for w, yrs in W.items():
        row[f"g_inr_{w}"] = s[s.fy.isin(yrs)].g_inr.mean()
        row[f"g_usd_{w}"] = s[s.fy.isin(yrs)].g_usd.mean()
    seg.append(row)
S = pd.DataFrame(seg).set_index("activity")
for b in ("base_FY20_23", "base_FY20_23_exFY21", "base_FY20_22"):
    S[f"dy_{b}"] = S["g_inr_recent_FY25_26"] - S[f"g_inr_{b}"]
S.round(2).to_csv(HERE / "rbi_segment_growth.csv")
print(S.round(1).to_string())
RB = {"it_services": "RBI_IT_services", "bpo": "RBI_BPO", "engineering": "RBI_Engineering"}
w_exp = r[(r.fy == "2023-24") & r.activity.isin(RB)].set_index("activity").inr_crore
rows = []
for b in ("base_FY20_23", "base_FY20_23_exFY21", "base_FY20_22"):
    for comp in ("compA", "compB"):
        E = ex[ex.composition == comp].set_index("line")
        for m in ("E_gpt_raw", "E_human_raw", "E_gpt", "E_human", "F_lm"):
            e = pd.Series({a: E.loc[l, m] for a, l in RB.items()})
            ebar = (e * w_exp).sum() / w_exp.sum()
            c = PHI_S_BAR["mid"] * e / ebar
            for a in ("bpo", "engineering"):
                dc = c[a] - c["it_services"]
                dy = S.loc[a, f"dy_{b}"] - S.loc["it_services", f"dy_{b}"]
                rows.append(dict(design="rbi_segments", baseline=b, mapping=f"{comp}:{m}", phi_s_bar=2.5,
                                 contrast=f"{a}-it_services", dc=dc, dy=dy, eps_minus_1=dy / dc, eps=1 + dy / dc,
                                 se_noise_if_sigma3=SIGMA / abs(dc)))
            # 3-segment OLS with intercept (1 df)
            X = np.column_stack([np.ones(3), c[["it_services", "bpo", "engineering"]].values])
            yv = S.loc[["it_services", "bpo", "engineering"], f"dy_{b}"].values
            bb = np.linalg.lstsq(X, yv, rcond=None)[0]
            rows.append(dict(design="rbi_segments", baseline=b, mapping=f"{comp}:{m}", phi_s_bar=2.5,
                             contrast="OLS 3 segments w/ intercept", dc=c.max() - c.min(), dy=np.nan,
                             eps_minus_1=bb[1], eps=1 + bb[1], se_noise_if_sigma3=np.nan))
    for G in (1.0, 2.5):  # binary: BPO 'high', IT and engineering 'low'
        dy = S.loc["bpo", f"dy_{b}"] - S.loc["it_services", f"dy_{b}"]
        rows.append(dict(design="rbi_segments", baseline=b, mapping="binary_BPO_high", phi_s_bar=np.nan,
                         contrast="bpo-it_services", dc=G, dy=dy, eps_minus_1=dy / G, eps=1 + dy / G,
                         se_noise_if_sigma3=SIGMA / G))
RR = pd.DataFrame(rows)
RR.round(3).to_csv(HERE / "eps_rbi_estimates.csv", index=False)
print(RR.round(2).to_string())
