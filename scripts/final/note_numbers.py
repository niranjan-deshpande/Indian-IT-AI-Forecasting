"""Summary numbers quoted in note_inputs.md, computed from the final tables (so every number traces to a file).

    python3 scripts/final/note_numbers.py   -> output/final/note_numbers.csv
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "final"
A = pd.read_csv(OUT / "table_A.csv")
F = pd.read_csv(OUT / "table_A_firms.csv")
S = pd.read_csv(OUT / "fig2_data.csv", index_col=0)
rows = []
PRE = [f"FY{y}" for y in range(16, 21)]        # FY16-FY20 (pre-COVID)
for grp in ["Indian simple average", "Indian revenue-weighted average", "Accenture", "Cognizant"]:
    for m in ["rev_cc", "rev_usd", "headcount", "headcount_yearend", "rpe_cc", "rpe_usd"]:
        x = A[(A.group == grp) & (A.metric == m)].set_index("period").value
        pre = x.reindex(PRE).dropna()
        rows.append(dict(item=f"{grp} | {m} | mean FY16-FY20", value=pre.mean(), n=len(pre), source="output/final/table_A.csv"))
        for p in ["FY22", "FY23", "FY24", "FY25", "FY26", "FY27 Q1 (one quarter)"]:
            rows.append(dict(item=f"{grp} | {m} | {p}", value=x.get(p), n=1, source="output/final/table_A.csv"))
        post = x.reindex(["FY24", "FY25", "FY26"]).dropna()
        rows.append(dict(item=f"{grp} | {m} | mean FY24-FY26", value=post.mean(), n=len(post), source="output/final/table_A.csv"))
# firms with negative avg-based headcount growth in FY24
fy24 = F[(F.period == "FY24") & F.firm.isin(["tcs", "infosys", "hcltech", "wipro", "techm", "lti_group"])]
rows.append(dict(item="Indian entities with negative headcount growth in FY24 (count of 6)", value=int((fy24.headcount < 0).sum()),
                 n=int(fy24.headcount.notna().sum()), source="output/final/table_A_firms.csv"))
for _, r in fy24.iterrows():
    rows.append(dict(item=f"{r.firm} | headcount | FY24", value=r.headcount, n=1, source="output/final/table_A_firms.csv"))
# subcontracting
for f in S.columns:
    v = S[f]
    rows.append(dict(item=f"subcontracting % rev | {f} | FY23", value=v.get("FY23"), n=1, source="output/final/fig2_data.csv"))
    rows.append(dict(item=f"subcontracting % rev | {f} | FY24", value=v.get("FY24"), n=1, source="output/final/fig2_data.csv"))
    rows.append(dict(item=f"subcontracting % rev | {f} | FY26", value=v.get("FY26"), n=1, source="output/final/fig2_data.csv"))
    rows.append(dict(item=f"subcontracting % rev | {f} | change FY23->FY24 (pp)", value=v.get("FY24") - v.get("FY23"), n=1, source="output/final/fig2_data.csv"))
d = S.loc["FY24"] - S.loc["FY23"]
rows.append(dict(item="subcontracting: firms whose share fell FY23->FY24", value=int((d < 0).sum()), n=int(d.notna().sum()), source="output/final/fig2_data.csv"))
rows.append(dict(item="subcontracting: firms with FY26 share below FY23", value=int((S.loc["FY26"] < S.loc["FY23"]).sum()), n=int(S.loc["FY26"].notna().sum()), source="output/final/fig2_data.csv"))
pd.DataFrame(rows).round(3).to_csv(OUT / "note_numbers.csv", index=False)
print(pd.DataFrame(rows).round(2).to_string())
