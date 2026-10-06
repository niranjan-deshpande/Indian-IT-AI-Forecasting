"""Combine firm extracts -> workforce_firm_tidy.csv; compute junior-share and junior-hiring vs revenue."""
import pandas as pd, numpy as np
W="data/explore/workforce/"
d=pd.concat([pd.read_csv(W+f) for f in ["extract_tcs_infosys.csv","extract_hcl_wipro.csv","extract_techm_ltim.csv"]],ignore_index=True)
d["firm"]=d.firm.str.lower(); d["fiscal_year"]=d.fiscal_year.astype(str).str.extract(r"(\d{4})")[0].astype(int)
d["value_num"]=pd.to_numeric(d.value.astype(str).str.replace(",","").str.strip(),errors="coerce")
d["_india"]=d.scope.astype(str).str.contains("India",case=False)&~d.scope.astype(str).str.contains("global",case=False)
d=d.sort_values(["firm","fiscal_year","metric","_india"])  # prefer global scope when both exist
d.drop(columns="_india").to_csv(W+"workforce_firm_tidy.csv",index=False)
# revenue (USD, reported) by Indian FY from pilot core_quarterly
c=pd.read_csv("data/tidy/core_quarterly.csv")
q=pd.PeriodIndex(c.cal_q,freq="Q"); c["fy"]=np.where(q.quarter==1,q.year,q.year+1)
c["firm"]=c.firm.replace({"ltim":"ltimindtree"})
rv=c.groupby(["firm","fy"]).agg(rev=("rev_usd","sum"),n=("rev_usd","count"),hc=("headcount","last"))
rv=rv[rv.n==4].rev.rename("rev").to_frame().join(rv.hc)
def piv(metric,unit="count"):
    x=d[(d.metric==metric)&(d.unit==unit)&d.dimension.isin(["age_lt30","age_30_50","age_gt50"])]
    return x.pivot_table(index=["firm","fiscal_year"],columns="dimension",values="value_num",aggfunc="first")
E=piv("employees_by_age"); E["sh_lt30"]=100*E.age_lt30/E[["age_lt30","age_30_50","age_gt50"]].sum(1)
Ep=piv("employees_by_age","pct"); Ep["sh_lt30"]=Ep.age_lt30
E=pd.concat([E[["sh_lt30"]],Ep.loc[~Ep.index.isin(E.index),["sh_lt30"]]]).sort_index()
H=piv("new_hires_by_age"); H["hires_lt30"]=H.age_lt30; H["hires_30p"]=H.age_30_50+H.age_gt50
H["sh_hires_lt30"]=100*H.hires_lt30/(H.hires_lt30+H.hires_30p)
X=E.join(H[["hires_lt30","hires_30p","sh_hires_lt30"]],how="outer")
X.index.names=["firm","fy"]; X=X.join(rv,how="left")
X["gR"]=100*np.log(X.rev/X.groupby(level=0).rev.shift(1))
X["hires_lt30_per_bnUSD"]=X.hires_lt30/(X.rev/1000)
X["hires_30p_per_bnUSD"]=X.hires_30p/(X.rev/1000)
X.round(2).to_csv(W+"firm_year_junior_metrics.csv")
print(X.round(1).to_string())
# 1) junior share change FY23 -> latest vs revenue growth
print("\n== <30 share change FY2023->latest vs USD revenue log growth")
for f,g in X.groupby(level=0):
    g=g.droplevel(0)
    if 2023 in g.index and g.sh_lt30.notna().sum()>1:
        last=g.sh_lt30.dropna().index.max()
        if last>2023 and pd.notna(g.sh_lt30.get(2023)):
            r=100*np.log(g.rev.get(last)/g.rev.get(2023)) if pd.notna(g.rev.get(last)) else np.nan
            pre=g.sh_lt30.dropna(); pre=pre[(pre.index>=2016)&(pre.index<=2023)]
            print(f"{f:12s} FY23 {g.sh_lt30[2023]:.1f} -> FY{last%100} {g.sh_lt30[last]:.1f} (d={g.sh_lt30[last]-g.sh_lt30[2023]:+.1f}pp); rev growth {r:+.1f} log pts; pre-period range {pre.min():.1f}-{pre.max():.1f} ({pre.index.min()}-{pre.index.max()})")
# 2) junior hiring intensity vs pre-period, conditional on revenue: log(hires_lt30) = firm FE + b*gR, fit FY<=2023, predict FY24-26
Y=X.dropna(subset=["hires_lt30","gR"]).copy(); Y["ly"]=np.log(Y.hires_lt30); Y["ly30"]=np.log(Y.hires_30p)
Y=Y.reset_index()
for dep in ["ly","ly30"]:
    tr=Y[Y.fy<=2023]
    D=pd.get_dummies(tr.firm).astype(float); Xm=np.column_stack([D.values,tr.gR.values])
    b,*_=np.linalg.lstsq(Xm,tr[dep].values,rcond=None); fe=dict(zip(D.columns,b[:-1])); slope=b[-1]
    res_tr=tr[dep].values-Xm@b
    te=Y[(Y.fy>=2024)&Y.firm.isin(fe)].copy(); te["pred"]=te.firm.map(fe)+slope*te.gR; te["resid_logpts"]=100*(te[dep]-te.pred)
    print(f"\n== {dep}: slope on gR={slope:.3f}, in-sample resid sd={100*res_tr.std(ddof=len(b)):.1f} log pts, n={len(tr)}")
    print(te[["firm","fy","gR","resid_logpts"]].round(1).to_string(index=False)); print("mean FY24-26 resid:",round(te.resid_logpts.mean(),1))

# 3) trend-adjusted junior share: pre-2022 linear trend (pp/yr) vs FY23->latest pace
print("\n== <30 share: pre-FY22 trend vs FY23->latest pace (pp/yr)")
for f,g in X.groupby(level=0):
    s=g.droplevel(0).sh_lt30.dropna(); pre=s[s.index<=2021]
    if len(pre)>=3 and 2023 in s.index and s.index.max()>2023:
        b=np.polyfit(pre.index,pre.values,1)[0]; last=s.index.max()
        print(f"{f:10s} pre FY{pre.index.min()%100}-FY{pre.index.max()%100}: {b:+.2f} pp/yr | FY23-FY{last%100}: {(s[last]-s[2023])/(last-2023):+.2f} pp/yr")
# Infosys job-level (grade) junior share
gI=d[(d.firm=="infosys")&(d.metric=="headcount_by_grade")].pivot_table(index="fiscal_year",columns="dimension",values="value_num",aggfunc="first")
gI["jr_share"]=100*gI.grade_junior/gI[[c for c in gI.columns if c.startswith("grade_")]].sum(1)
gI=gI.join(rv.loc["infosys"].rev)
print("\n== Infosys job-level: junior (JL3 and below) share and levels"); print(gI[["grade_junior","grade_middle","grade_senior","jr_share","rev"]].round(1).to_string())
pre=gI.jr_share[(gI.index>=2014)&(gI.index<=2021)]; print("pre FY14-21 trend pp/yr:",round(np.polyfit(pre.index,pre.values,1)[0],2),"| FY23-26 pp/yr:",round((gI.jr_share[2026]-gI.jr_share[2023])/3,2))
print("junior log change FY23-26:",round(100*np.log(gI.grade_junior[2026]/gI.grade_junior[2023]),1),"; middle+senior:",round(100*np.log((gI.grade_middle[2026]+gI.grade_senior[2026])/(gI.grade_middle[2023]+gI.grade_senior[2023])),1),"; revenue:",round(100*np.log(gI.rev[2026]/gI.rev[2023]),1))
# 4) annual fresher hires vs revenue: log(fresher per $bn) = firm FE + b*gR, fit FY<=2023, predict FY24-26
F=d[(d.metric=="fresher_hires")&(d.dimension=="total")].copy()
F=F[~((F.firm=="tcs")&(F.fiscal_year==2020))]            # H1 lower bound only
F=F[~((F.firm=="infosys")&(F.fiscal_year==2019)&F.scope.str.contains("Foundation"))]  # keep group figure for FY19
F=F[~((F.firm=="tcs")&(F.fiscal_year==2022)&(F.value_num!=110000))]  # middle of 100k/110k/118k
F=F.groupby(["firm","fiscal_year"]).value_num.first().rename("fresher").reset_index().rename(columns={"fiscal_year":"fy"})
R=rv.copy(); R["gR"]=100*np.log(R.rev/R.groupby(level=0).rev.shift(1)); R.index.names=["firm","fy"]
F=F.merge(R.reset_index()[["firm","fy","rev","gR"]],on=["firm","fy"],how="left")
F["per_bn"]=F.fresher/(F.rev/1000); F["lp"]=np.log(F.per_bn)
print("\n== annual fresher hires (best series)"); print(F.round(1).to_string(index=False)); F.round(2).to_csv(W+"fresher_hires_annual_best.csv",index=False)
tr=F[(F.fy<=2023)&F.gR.notna()]; tr=tr[tr.firm.map(tr.firm.value_counts())>=2]
D=pd.get_dummies(tr.firm).astype(float); M=np.column_stack([D.values,tr.gR.values]); b,*_=np.linalg.lstsq(M,tr.lp.values,rcond=None)
fe=dict(zip(D.columns,b[:-1])); res=tr.lp.values-M@b
te=F[(F.fy>=2024)&F.firm.isin(fe)&F.gR.notna()].copy(); te["pred_per_bn"]=np.exp(te.firm.map(fe)+b[-1]*te.gR); te["resid_logpts"]=100*(te.lp-np.log(te.pred_per_bn))
print(f"fit FY<=2023: n={len(tr)} firms={list(fe)} slope per 1pt gR={100*b[-1]:.1f}% ; resid sd={100*res.std(ddof=len(b)):.0f} log pts")
print(te[["firm","fy","gR","per_bn","pred_per_bn","resid_logpts"]].round(0).to_string(index=False)); print("mean resid FY24-26:",round(te.resid_logpts.mean(),0))
# 5) hiring intensity by age: FY25-26 avg vs pre-COVID avg (per $bn revenue)
print("\n== hires per $bn revenue: pre-COVID (<=FY20) avg vs FY25-26 avg, log change x100")
Z=X.reset_index()
Z.loc[Z.firm.isin(["lti","mindtree"]),"firm"]="ltim_pre"
for f,g in Z[Z.firm!="techm"].groupby("firm"):  # techm pre-FY21 hires are India-only -> not comparable
    if f=="ltim_pre":
        g=g[g.fy<=2020].groupby("fy")[["hires_lt30","hires_30p","rev"]].sum(min_count=1)
    pre=g[(g.index if f=="ltim_pre" else g.fy)<=2020] if f=="ltim_pre" else g[g.fy<=2020]
    if f=="ltim_pre": continue
    post=g[g.fy>=2025]
    if f=="ltimindtree":
        L=Z[(Z.firm=="ltim_pre")&(Z.fy<=2020)].groupby("fy")[["hires_lt30","hires_30p","rev"]].sum(min_count=1).dropna()
        pre=L.reset_index()
    pre=pre.dropna(subset=["hires_lt30"]); post=post.dropna(subset=["hires_lt30"])
    if len(pre) and len(post):
        a=lambda h,G:(G[h]/(G.rev/1000)).mean()
        j=100*np.log(a("hires_lt30",post)/a("hires_lt30",pre)); s=100*np.log(a("hires_30p",post)/a("hires_30p",pre))
        print(f"{f:12s} pre FY{int(pre.fy.min())%100}-{int(pre.fy.max())%100}: <30 {j:+.0f}, 30+ {s:+.0f}, relative junior {j-s:+.0f}")
