"""Pooled series, validation vs pilot gR, and keyword-in-context check (post-hoc diagnostics; dictionary unchanged)."""
import pandas as pd, numpy as np
ROOT = "/Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/0. Exploratory Analysis"
OUT = f"{ROOT}/data/explore/text_firms/A_text"
F = pd.read_csv(f"{OUT}/family_rates_fq.csv"); D = pd.read_csv(f"{OUT}/term_counts_doc.csv")
FAMS = ["pricing", "productivity", "demand", "gcc"]
D["year"] = D.cal_q.str[:4]
agg = D.groupby("year")[[f"n_{f}" for f in FAMS] + ["words"]].sum()
pooled = pd.DataFrame({f: (agg[f"n_{f}"] / agg.words * 1e4).round(2) for f in FAMS}); pooled["docs"] = D.groupby("year").size()
pooled.to_csv(f"{OUT}/pooled_by_year.csv"); print(pooled)
# validation: within-firm correlation with pilot YoY cc revenue growth (gR) in same quarter and gR 2 quarters later
Y = pd.read_csv(f"{ROOT}/data/tidy/yoy_metrics.csv"); Y["firm"] = Y.firm.str.lower()
m = {"Accenture": "accenture", "HCLTech": "hcltech", "Infosys": "infosys", "TCS": "tcs", "TechM": "techm", "Wipro": "wipro"}
F["f"] = F.firm.map(m)
print(sorted(Y.firm.unique()))
M = F.merge(Y[["firm", "cal_q", "gR"]], left_on=["f", "cal_q"], right_on=["firm", "cal_q"], how="left", suffixes=("", "_y"))
M = M.sort_values(["firm", "cal_q"]); M["gR_lead2"] = M.groupby("firm").gR.shift(-2)
res = []
for f in FAMS:
    for tgt in ["gR", "gR_lead2"]:
        sub = M.dropna(subset=[f, tgt]).copy()
        sub[f + "_dm"] = sub[f] - sub.groupby("firm")[f].transform("mean"); sub["t_dm"] = sub[tgt] - sub.groupby("firm")[tgt].transform("mean")
        res.append(dict(family=f, target=tgt, n=len(sub), within_corr=round(np.corrcoef(sub[f + "_dm"], sub.t_dm)[0, 1], 2)))
R = pd.DataFrame(res); R.to_csv(f"{OUT}/validation_vs_gR.csv", index=False); print(R)
