"""UK Contracts Finder probe: v2 search API (POST /api/rest/2/search_notices/json, no key).
Full-text keyword search of awarded notices 2018-01..2026-09; classify whether firm is the awarded supplier."""
import requests, pandas as pd, re, time, html
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36","Content-Type":"application/json"}
EP="https://www.contractsfinder.service.gov.uk/api/rest/2/search_notices/json"
FIRMS={"TCS":(['"Tata Consultancy"'],r"tata consult"),
 "Infosys":(["Infosys"],r"infosys"),
 "HCL":(['"HCL Technologies"','"HCL America"','HCL'],r"\bhcl\b"),
 "Wipro":(["Wipro"],r"wipro"),
 "TechMahindra":(['"Tech Mahindra"'],r"tech ?mahindra"),
 "LTIMindtree":(["Mindtree","LTIMindtree",'"Larsen & Toubro Infotech"'],r"mindtree|larsen.*infotech|\blti\b"),
 "Cognizant":(["Cognizant"],r"cognizant"),
 "Accenture":(["Accenture"],r"accenture")}
rows=[]
for f,(kws,rx) in FIRMS.items():
    for kw in kws:
        # split by year windows to stay under result caps
        for y in range(2018,2027):
            body={"searchCriteria":{"keyword":kw,"statuses":["Awarded"],"publishedFrom":f"{y}-01-01","publishedTo":f"{y}-12-31"},"size":1000}
            for i in range(3):
                try: r=requests.post(EP,json=body,headers=UA,timeout=60).json(); break
                except Exception: time.sleep(3); r={}
            hits=r.get("hitCount",0); lst=r.get("noticeList",[])
            if hits>len(lst): print("TRUNCATED",f,kw,y,hits,len(lst))
            for n in lst:
                it=n["item"]; it["firm"]=f; it["kw"]=kw; rows.append(it)
            time.sleep(0.5)
d=pd.DataFrame(rows).drop_duplicates(["firm","id"])
d["supplier_match"]=d["awardedSupplier"].fillna("").str.lower().str.contains("|".join([FIRMS[f][1] for f in FIRMS]),regex=True)
d["supplier_is_firm"]=[bool(re.search(FIRMS[f][1],str(s).lower())) for f,s in zip(d.firm,d.awardedSupplier)]
d["description"]=d["description"].fillna("").map(html.unescape).str.slice(0,600)
d["url"]="https://www.contractsfinder.service.gov.uk/Notice/"+d["id"]
d["year"]=pd.to_datetime(d["awardedDate"].fillna(d["publishedDate"]),errors="coerce",utc=True).dt.year
keep=["firm","supplier_is_firm","year","awardedDate","publishedDate","organisationName","title","awardedSupplier","awardedValue","valueLow","valueHigh","start","end","cpvCodes","noticeIdentifier","description","url"]
keep=[c for c in keep if c in d]
d[keep].to_csv("ukcf_notices_mentioning_firms.csv",index=False)
d["n_suppliers"]=d["awardedSupplier"].fillna("").str.count(",")+1
d=d[(d.year>=2018)&(d.year<=2026)]
d[keep+["n_suppliers"]].to_csv("ukcf_notices_mentioning_firms.csv",index=False)
s=d[d.supplier_is_firm].copy(); s["sole"]=s.n_suppliers==1
s["value_sole"]=s.awardedValue.where(s.sole,0)
g=s.groupby(["firm","year"]).agg(n_awards=("id","count"),n_sole_supplier=("sole","sum"),n_multi_supplier_framework=("sole",lambda x:(~x).sum()),value_gbp_all_incl_framework_ceilings=("awardedValue","sum"),value_gbp_sole_supplier=("value_sole","sum")).reset_index()
g.insert(0,"source","UK_ContractsFinder"); g.to_csv("ukcf_counts_by_firm_year.csv",index=False)
m=d[~d.supplier_is_firm].groupby("firm").size(); print("mentions-not-supplier:",m.to_dict())
print(g.pivot(index="firm",columns="year",values="n_awards"))
print((g.pivot(index="firm",columns="year",values="value_gbp_sole_supplier")/1e6).round(1))
