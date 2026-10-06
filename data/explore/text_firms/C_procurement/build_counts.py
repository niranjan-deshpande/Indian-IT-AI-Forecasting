import pandas as pd
u=pd.read_csv("usaspending_counts_by_firm_year.csv")
u=u.rename(columns={"n_new_contracts":"n_awards_new","obligations_usd":"value"}).assign(currency="USD",value_definition="prime contract obligations in calendar year (transactions)",
   count_definition="n_awards_new = new prime contract awards (A-D) starting in year; n_active_contracts = contracts with any action in year")
u=u[["source","firm","year","n_awards_new","n_active_contracts","n_new_idvs","value","currency","value_definition","count_definition"]]
k=pd.read_csv("ukcf_counts_by_firm_year.csv")
k=k.rename(columns={"n_awards":"n_awards_new","value_gbp_sole_supplier":"value"}).assign(currency="GBP",value_definition="sum of awardedValue for sole-supplier awards (ceiling/max incl. extensions; NOT spend); multi-supplier framework values excluded",
   count_definition="award notices (published) naming firm as supplier; n_sole_supplier + n_multi_supplier_framework")
k=k[["source","firm","year","n_awards_new","n_sole_supplier","n_multi_supplier_framework","value","value_gbp_all_incl_framework_ceilings","currency","value_definition","count_definition"]]
# fill zero rows for firms/years with no UK hits
idx=pd.MultiIndex.from_product([sorted(set(u.firm)-{"Accenture_AFS_LLP","Accenture_acquired_subs"})|{"Accenture"} if False else ["TCS","Infosys","HCL","Wipro","TechMahindra","LTIMindtree","Cognizant","Accenture"],range(2018,2027)],names=["firm","year"])
k=k.set_index(["firm","year"]).reindex(idx).reset_index(); k["source"]="UK_ContractsFinder"
for c in ["n_awards_new","n_sole_supplier","n_multi_supplier_framework","value","value_gbp_all_incl_framework_ceilings"]: k[c]=k[c].fillna(0)
k[["currency","value_definition","count_definition"]]=k[["currency","value_definition","count_definition"]].ffill().bfill()
out=pd.concat([u,k],ignore_index=True); out.to_csv("counts_by_firm_year.csv",index=False)
p=out.pivot_table(index=["source","firm"],columns="year",values="n_awards_new",aggfunc="sum"); print(p.astype(int).to_string())
v=(out.pivot_table(index=["source","firm"],columns="year",values="value",aggfunc="sum")/1e6).round(1); print(v.to_string())
