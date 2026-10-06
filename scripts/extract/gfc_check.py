"""Consistency checks on a gfc rows csv: cross-vintage disagreements, share sums, coverage table."""
import pandas as pd, sys
d=pd.read_csv(sys.argv[1])
key=["metric","dim_type","dimension","basis","period_type","cal_q"]
g=d.groupby(key).value.agg(["min","max","count"])
dis=g[(g["max"]-g["min"]).abs()>0.051]
print("cross-vintage disagreements:",len(dis))
print(dis.head(80).to_string())
sh=d[(d.metric=="revenue_share")&(d.dim_type=="geography")]
s=sh.groupby(["source_doc","cal_q"]).value.sum()
print("geo share sums off:",s[(s-100).abs()>0.25].to_string())
cov=d[d.dimension.isin(["total"])].groupby(["metric","basis"]).cal_q.agg(["min","max","nunique"])
print(cov.to_string())
