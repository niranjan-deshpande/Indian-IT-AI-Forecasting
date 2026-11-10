"""Check Analytics India Magazine (21 Aug 2026) / Unearthinsight revenue-per-employee figures against our canonical panel.
Claim (as extracted from the article via WebFetch, 2026-10-15; page text not saveable - JS challenge):
  RPE FY19 -> FY26 (USD): Infosys 51,722 -> 61,346 (2.47%/yr); TCS 49,290 -> 51,353 (0.59%); HCLTech 62,567 -> 64,548 (0.45%);
  TechM 41,051 -> 43,252 (0.75%); Wipro 45,144 -> 40,763 (-1.45%). Gaurav Vasu: ~60% of the improvement from workforce
  rationalisation, ~40% from AI efficiency (no method given).
Input: data/corrected/core_quarterly_final.csv (rev_usd in USD mn; Wipro = IT Services segment; headcount company-wide).
Output: aim_rpe_check.csv, aim_rpe_decomposition.csv. Run: python3 -I aim_rpe_check.py
"""
import os, numpy as np, pandas as pd
OUT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(OUT, "..", "..", "..", "..", ".."))
d = pd.read_csv(os.path.join(REPO, "data", "corrected", "core_quarterly_final.csv"))
d["q"] = pd.PeriodIndex(d.cal_q, freq="Q")
d["fy"] = [p.year + 1 if p.quarter >= 2 else p.year for p in d.q]  # FY t = Apr(t-1)..Mar(t)
CLAIM = {"infosys": (51722, 61346, 2.47), "tcs": (49290, 51353, 0.59), "hcltech": (62567, 64548, 0.45),
         "techm": (41051, 43252, 0.75), "wipro": (45144, 40763, -1.45)}

def fy_metrics(firms, fy):
    x = d[d.firm.isin(firms) & (d.fy == fy)].groupby("q").agg(rev=("rev_usd", "sum"), hc=("headcount", "sum"),
                                                                n_rev=("rev_usd", "count"), n_hc=("headcount", "count"))
    if len(x) != 4 or (x.n_rev < len(firms)).any() or (x.n_hc < len(firms)).any(): return None
    rev = x.rev.sum() * 1e6
    return dict(rev_usd_bn=rev / 1e9, hc_end=x.hc.iloc[-1], hc_avg=x.hc.mean(),
                rpe_end=rev / x.hc.iloc[-1], rpe_avg=rev / x.hc.mean(), rpe_q4_annualised=x.rev.iloc[-1] * 4e6 / x.hc.iloc[-1])

ENT = {"tcs": ["tcs"], "infosys": ["infosys"], "hcltech": ["hcltech"], "wipro": ["wipro"], "techm": ["techm"],
       "ltim (LTI+Mindtree pre-FY23)": None, "top6": None}
rows = []
for name in ENT:
    for fy in [19, 23, 26]:
        Y = 2000 + fy
        if name.startswith("ltim"): firms = ["lti", "mindtree"] if Y <= 2022 else ["ltim"]
        elif name == "top6": firms = ["tcs", "infosys", "hcltech", "wipro", "techm"] + (["lti", "mindtree"] if Y <= 2022 else ["ltim"])
        else: firms = ENT[name]
        m = fy_metrics(firms, Y)
        if m: rows.append(dict(entity=name, fy=f"FY{fy}", **{k: round(v, 3 if k == "rev_usd_bn" else 0) for k, v in m.items()}))
t = pd.DataFrame(rows)
out = []
for name, g in t.groupby("entity", sort=False):
    g = g.set_index("fy"); r = dict(entity=name)
    for c in ["rpe_end", "rpe_avg", "rpe_q4_annualised"]:
        for a, b, yrs in [("FY19", "FY26", 7), ("FY23", "FY26", 3)]:
            if a in g.index and b in g.index:
                r[f"{c}_{a}"] = g.loc[a, c]; r[f"{c}_{b}"] = g.loc[b, c]
                r[f"{c}_cagr_{a}_{b}_pct"] = round(((g.loc[b, c] / g.loc[a, c]) ** (1 / yrs) - 1) * 100, 2)
    if name in CLAIM:
        r["unearth_FY19"], r["unearth_FY26"], r["unearth_cagr_pct"] = CLAIM[name]
    out.append(r)
o = pd.DataFrame(out); o.to_csv(os.path.join(OUT, "aim_rpe_check.csv"), index=False)
cols = ["entity", "rpe_end_FY19", "unearth_FY19", "rpe_end_FY26", "unearth_FY26", "rpe_end_cagr_FY19_FY26_pct", "unearth_cagr_pct",
        "rpe_avg_cagr_FY19_FY26_pct", "rpe_end_cagr_FY23_FY26_pct", "rpe_avg_cagr_FY23_FY26_pct"]
print(o[cols].to_string(index=False))

# accounting decomposition of RPE growth (log points): dln(RPE) = dln(revenue) - dln(headcount)
dec = []
for name, g in t.groupby("entity", sort=False):
    g = g.set_index("fy")
    for a, b in [("FY19", "FY26"), ("FY23", "FY26")]:
        if a in g.index and b in g.index:
            dr = np.log(g.loc[b, "rev_usd_bn"] / g.loc[a, "rev_usd_bn"]) * 100
            dl = np.log(g.loc[b, "hc_avg"] / g.loc[a, "hc_avg"]) * 100
            drpe = dr - dl
            dec.append(dict(entity=name, window=f"{a}-{b}", dlog_revenue=round(dr, 1), dlog_avg_headcount=round(dl, 1), dlog_rpe=round(drpe, 1),
                            share_from_headcount_cut_pct=round(-dl / drpe * 100, 0) if drpe > 0 and dl < 0 else None))
dd = pd.DataFrame(dec); dd.to_csv(os.path.join(OUT, "aim_rpe_decomposition.csv"), index=False); print(dd.to_string(index=False))
