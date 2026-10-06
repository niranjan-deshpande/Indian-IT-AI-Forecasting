"""Build monthly JobSpeak series (latest vintage per month) + YoY log x100 and compare with firm headcount (pilot)."""
import pandas as pd, numpy as np
W="data/explore/workforce/"
d=pd.read_csv(W+"jobspeak_vintages_long.csv")
d=d.sort_values("report_month").groupby(["series","month"]).tail(1)   # latest vintage
w=d.pivot(index="month",columns="series",values="value").sort_index()
w.index=pd.PeriodIndex(w.index,freq="M")
y=100*np.log(w/w.shift(12))
out=w.add_prefix("idx_").join(y.add_prefix("yoy_"))
out["rel_0_3_vs_16plus_log"]=100*np.log(w.exp_0_3/w.exp_16plus)
out.index=out.index.astype(str); out.index.name="month"
src=d.pivot(index="month",columns="series",values="source_url")["it_software"]
out["source_url_it"]=src
out.round(2).to_csv(W+"jobspeak_monthly.csv")
print(out[["idx_it_software","yoy_it_software","yoy_exp_0_3","yoy_exp_4_7","yoy_exp_16plus","rel_0_3_vs_16plus_log"]].round(1).to_string())
# quarterly
q=w.copy(); q.index=q.index.asfreq("Q"); q=q.groupby(level=0).mean()
qy=100*np.log(q/q.shift(4))
print(qy.round(1).dropna(how="all").to_string())
# compare with pilot headcount of 6 Indian firms
p=pd.read_csv("data/tidy/yoy_metrics.csv")
ind=p[p.firm.isin(["tcs","infosys","hcltech","wipro","techm","ltimindtree","ltim"])]
print(ind.firm.unique())
g=ind.groupby("cal_q")[["gL","gR"]].mean(); g.index=pd.PeriodIndex(g.index,freq="Q")
m=qy[["it_software","exp_0_3","exp_16plus"]].join(g,how="inner").dropna(subset=["it_software","gL"])
print(m.round(1).to_string()); print(m.corr().round(2))
# noise stats on monthly YoY for what exists pre-2023 (2022 only)
s=y.it_software.dropna(); pre=s[(s.index.year<=2022)]
r=pre-pre.mean(); ar=np.corrcoef(r[1:],r[:-1])[0,1]
print("pre-2023 IT YoY: n=",len(pre),"sd",round(r.std(),1),"AR1",round(ar,2),"mean",round(pre.mean(),1),"| 2023-26 mean",round(s[s.index.year>=2023].mean(),1))
for yr in [2022,2023,2024,2025,2026]: print(yr, round(s[s.index.year==yr].mean(),1))
# --- experience bands: annex levels (2021-11..2024-12) + chart YoY (2025-01..2026-08) -> relative 0-3 vs 16+ YoY gap
c=pd.read_csv(W+"jobspeak_expband_yoy_2025_26_chart.csv")
c["yoy_log"]=100*np.log1p(c.yoy_pct/100)
cc=c.pivot(index="month",columns="series",values="yoy_log")
a=y[["exp_0_3","exp_4_7","exp_8_12","exp_16plus"]].dropna(); a.index=a.index.astype(str)
band=pd.concat([a,cc[["exp_0_3","exp_4_7","exp_8_12","exp_16plus"]]])
band["gap_0_3_minus_16plus"]=band.exp_0_3-band.exp_16plus
band.round(2).to_csv(W+"jobspeak_expband_yoy_combined.csv")
band["yr"]=band.index.str[:4]
print(band.groupby("yr")[["exp_0_3","exp_4_7","exp_16plus","gap_0_3_minus_16plus"]].mean().round(1))
