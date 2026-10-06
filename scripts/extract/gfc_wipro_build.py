"""Build Wipro GFC-window rows (2007Q1-2012Q1) from EDGAR 6-K presentation exhibits ('Key Operating Metrics' tables,
parsed by gfc_wipro_kom.py -> kom.json), hand-transcribed tables (kom_hand.csv) and hand-entered highlights/MD&A metrics
(wipro_hand_metrics.csv). Output: data/sources/gfc/wipro/gfc_wipro_rows.csv"""
import json, re, datetime, csv
import pandas as pd
B="data/sources/gfc/wipro"
man={m["acc"]:m for m in json.load(open(f"{B}/edgar_manifest.json"))}
kom=json.load(open(f"{B}/kom.json"))
COLS=["firm","fiscal_q","period_end","cal_q","metric","dimension","dim_type","value","unit","basis","period_type","source_url","source_doc","source_loc","doc_date","notes"]
QE=[(3,31),(6,30),(9,30),(12,31)]
def qend_before(d):
    d=datetime.date.fromisoformat(d); c=[datetime.date(y,m,dd) for y in (d.year-1,d.year) for m,dd in QE]; return max(x for x in c if x<d)
def shift(pe,n):
    idx=pe.year*4+(pe.month//3-1)+n; y2,q=divmod(idx,4); m2,d2=QE[q]; return datetime.date(y2,m2,d2)
def fq(pe):
    q={6:1,9:2,12:3,3:4}[pe.month]; fy=pe.year+1 if pe.month>3 else pe.year; return f"Q{q}FY{str(fy)[2:]}"
def calq(pe): return f"{pe.year}Q{(pe.month-1)//3+1}"
rows=[]
def add(pe,metric,dim,dt,v,unit,basis,pt,url,doc,loc,dd,notes):
    if v is None or (isinstance(v,float) and v!=v): return
    if not (datetime.date(2007,1,1)<=pe<=datetime.date(2012,3,31)): return
    rows.append(dict(firm="wipro",fiscal_q=fq(pe),period_end=pe.isoformat(),cal_q=calq(pe),metric=metric,dimension=dim,dim_type=dt,value=v,unit=unit,basis=basis,
        period_type=pt,source_url=url,source_doc=doc,source_loc=loc,doc_date=dd,notes=notes))
GEO={"north america","europe","japan","others","us","india & middle east business","other emerging markets","americas","apac & other emerging markets"}
def seg_note(pe0):
    if pe0<=datetime.date(2008,3,31): return "Global IT business (Global IT Services & BPO; excludes India/ME/AsiaPac IT business)"
    return "IT Services segment (incl. India & Middle East IT services and BPO; segment re-defined from Q1FY09)"
def cleanlab(l):
    l=re.sub(r"^(Revenue Composition|Geography Composition)\s+","",l).strip()
    l=l.replace("Healthcare , Life","Healthcare, Life")
    return l
def ppl(s):
    s=s.replace(",",""); neg=s.startswith("("); s=s.strip("()"); return -float(s) if neg else float(s)
hand=pd.read_csv(f"{B}/kom_hand.csv")
handaccs=set(hand.acc)
for acc,k in kom.items():
    pe0=qend_before(man[acc]["date"]); url=man[acc]["base"]+k["ex"]; dd=man[acc]["date"]
    doc=f"Wipro {fq(pe0)} results presentation (6-K exhibit {k['ex']})"
    cols=[pe0,shift(pe0,-1),shift(pe0,-4)]
    cn=["current quarter","previous quarter","year-ago quarter"]
    if acc in handaccs: continue
    for lab,vals in k["shares"]:
        lab=cleanlab(lab)
        if len(lab)>45 or lab.lower().startswith(("onsite","offshore","off shore","geography composition")): continue
        dt="geography" if lab.lower() in GEO else "vertical"
        for i,v in enumerate(vals):
            add(cols[i],"revenue_share",lab,dt,v,"pct","na","quarter",url,doc,f"Key Operating Metrics table - Revenue break-down, {cn[i]}",dd,seg_note(pe0)+"; parsed from exhibit text")
    seen=set()
    for lab,vals in k["people"]:
        if lab in seen: continue   # first block = headcount; second block = net additions
        seen.add(lab)
        if lab in ("Total","Number of employees","Numberof employees"): dim,dt="total","total"
        else: dim,dt=lab,"other"
        for i,v in enumerate(vals):
            add(cols[i],"headcount",dim,dt,ppl(v),"count","na","point",url,doc,f"Key Operating Metrics table - People related, {cn[i]}",dd,
                seg_note(pe0)+" headcount (not total Wipro Ltd incl. consumer care/infrastructure engineering); parsed from exhibit text")
for x in hand.itertuples():
    pe0=qend_before(man[x.acc]["date"]); ex=kom[x.acc]["ex"]; url=man[x.acc]["base"]+ex; dd=man[x.acc]["date"]
    doc=f"Wipro {fq(pe0)} results presentation (6-K exhibit {ex})"; cols=[pe0,shift(pe0,-1),shift(pe0,-4)]
    cn=["current quarter","previous quarter","year-ago quarter"]
    for i,v in enumerate([x.c0,x.c1,x.c2]):
        if x.kind=="people":
            dim,dt=("total","total") if x.label in ("Total","Number of employees") else (x.label,"other")
            add(cols[i],"headcount",dim,dt,v,"count","na","point",url,doc,f"Key Operating Metrics table - People related, {cn[i]}",dd,seg_note(pe0)+" headcount; hand-entered from exhibit text (column-wise layout)")
        else:
            add(cols[i],"revenue_share",x.label,x.kind,v,"pct","na","quarter",url,doc,f"Key Operating Metrics table - Revenue composition, {cn[i]}",dd,seg_note(pe0)+"; hand-entered from exhibit text (column-wise layout)")
hm=pd.read_csv(f"{B}/wipro_hand_metrics.csv")
for x in hm.itertuples():
    m=man[x.acc]; pe=datetime.date.fromisoformat(x.period_end)
    add(pe,x.metric,x.dimension,"total",x.value,x.unit,x.basis,x.period_type,m["base"]+x.exhibit,x.source_doc,x.source_loc,m["date"],x.notes)
df=pd.DataFrame(rows,columns=COLS); df.to_csv(f"{B}/gfc_wipro_rows.csv",index=False)
print(len(df)); print(df.groupby(["metric","dim_type"]).size())
