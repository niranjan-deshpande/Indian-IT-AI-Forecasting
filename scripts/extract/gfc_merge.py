"""Merge per-firm GFC-window row files (data/sources/gfc/<firm>/gfc_<firm>_rows.csv) into data/raw/gfc.csv,
validate schema, restrict to cal_q 2007Q1..2012Q1, drop exact duplicate rows."""
import pandas as pd, os
COLS=["firm","fiscal_q","period_end","cal_q","metric","dimension","dim_type","value","unit","basis","period_type","source_url","source_doc","source_loc","doc_date","notes"]
FIRMS=["tcs","infosys","hcltech","wipro","techm","cognizant","accenture"]
parts=[]
for f in FIRMS:
    p=f"data/sources/gfc/{f}/gfc_{f}_rows.csv"
    if not os.path.exists(p): print("MISSING",f); continue
    d=pd.read_csv(p,dtype={"value":float})
    assert list(d.columns)==COLS, (f,list(d.columns))
    assert (d.firm==f).all(), f
    assert d.source_url.notna().all(), f
    n0=len(d); d=d[(d.cal_q>="2007Q1")&(d.cal_q<="2012Q1")]
    parts.append(d); print(f,n0,len(d))
df=pd.concat(parts,ignore_index=True).drop_duplicates()
df.to_csv("data/raw/gfc.csv",index=False)
print("total",len(df))
print(df.groupby("firm").size())
