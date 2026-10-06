"""Build Infosys GFC-window rows (2007Q1-2012Q1) from EDGAR 6-K exhibits:
 - press releases (exv99w01): revenue USD, YoY/QoQ growth, headcount
 - fact sheets (image exhibits, OCR'd -> factsheet_cells2.csv + hand-transcribed factsheet_hand.csv): utilization, attrition,
   headcount, revenue shares (geography, industry, service offering)
 - fact sheet 'Constant Currency Reporting' table: reported and cc growth
 - quarterly 6-K MD&A: utilization (alt definition), subcontractor cost % of cost of sales
Output: data/sources/gfc/infosys/gfc_infosys_rows.csv"""
import json, re, csv, os, datetime, collections
import pandas as pd
B="data/sources/gfc/infosys"
man={m["acc"]:m for m in json.load(open(f"{B}/edgar_manifest.json"))}
fs=json.load(open(f"{B}/factsheets.json"))
COLS=["firm","fiscal_q","period_end","cal_q","metric","dimension","dim_type","value","unit","basis","period_type","source_url","source_doc","source_loc","doc_date","notes"]
rows=[]
QE=[(3,31),(6,30),(9,30),(12,31)]
def qend_before(d):
    d=datetime.date.fromisoformat(d)
    cands=[datetime.date(y,m,dd) for y in (d.year-1,d.year) for m,dd in QE]
    return max(c for c in cands if c<d)
def shift(pe,n):
    y,m=pe.year,pe.month; idx=y*4+(m//3-1)+n; y2,q=divmod(idx,4); m2,d2=QE[q]; return datetime.date(y2,m2,d2)
def fq(pe):  # Indian FY
    q={6:1,9:2,12:3,3:4}[pe.month]; fy=pe.year+1 if pe.month>3 else pe.year
    return f"Q{q}FY{str(fy)[2:]}"
def calq(pe): return f"{pe.year}Q{(pe.month-1)//3+1}"
def inrange(pe): return datetime.date(2007,1,1)<=pe<=datetime.date(2012,3,31)
def add(pe,metric,dim,dim_type,value,unit,basis,ptype,url,doc,loc,docdate,notes=""):
    if value is None or not inrange(pe): return
    rows.append(dict(firm="infosys",fiscal_q=fq(pe),period_end=pe.isoformat(),cal_q=calq(pe),metric=metric,dimension=dim,dim_type=dim_type,
        value=value,unit=unit,basis=basis,period_type=ptype,source_url=url,source_doc=doc,source_loc=loc,doc_date=docdate,notes=notes))
def num(s): return float(s.replace(",",""))

# ---------- 1. press releases ----------
seen=set()
for acc,m in sorted(man.items(),key=lambda x:x[1]["date"]):
    for d in m["docs"]:
        if d["name"] not in ("exv99w01.htm","evx99w01.htm"): continue
        t=open(f"{B}/edgar/{acc}/{d['name']}.txtc").read()
        if "announces results" not in t[:2500].lower(): continue
        t2=re.sub(r"\s+"," ",t)
        pe=qend_before(m["date"])
        if pe in seen: continue  # only the first (results-day) filing of each release
        seen.add(pe)
        gaap="US GAAP" if "US GAAP" in t2[:300].upper().replace(".","") or "USGAAP" in t2[:300].upper() else "IFRS"
        doc=f"Infosys {fq(pe)} {gaap} press release (6-K Ex.99.1)"
        base=f"{gaap} consolidated; Infosys and subsidiaries"
        hi=t2[:6000]
        mrev=re.search(r"(?:quarter )?revenues (?:at|were) \$ ?([\d,]+) million",hi,re.I)
        if mrev:
            add(pe,"revenue","total","total",num(mrev.group(1)),"USD_mn","reported","quarter",d["url"],doc,"Highlights",m["date"],base)
        seg=hi[mrev.start():mrev.start()+400] if mrev else ""
        my=re.search(r"up (?:by )?([\d.]+)% from the corresponding quarter",seg) or re.search(r"YoY (growth|decline) was ([\d.]+)%",seg)
        if my:
            if my.re.pattern.startswith("up"): v=float(my.group(1))
            else: v=float(my.group(2))*(-1 if my.group(1)=="decline" else 1)
            add(pe,"revenue_growth_yoy","total","total",v,"pct","reported","quarter",d["url"],doc,"Highlights",m["date"],base)
        mq=re.search(r"QoQ (growth|decline) was ([\d.]+)%",seg)
        qv=None
        if mq: qv=float(mq.group(2))*(-1 if mq.group(1)=="decline" else 1)
        else:
            h=hi[:800]
            m1=re.search(r"sequential growth (?:of )?([\d.]+)%",h,re.I) or re.search(r"sequentially grew by ([\d.]+)%",h,re.I) or re.search(r"grew by ([\d.]+)% sequentially",h,re.I)
            m2=re.search(r"sequential(?:ly)? decline(?:d)? (?:of |by )?([\d.]+)%",h,re.I) or re.search(r"declined by ([\d.]+)% sequentially",h,re.I)
            if m1: qv=float(m1.group(1))
            elif m2: qv=-float(m2.group(1))
        if qv is not None:
            add(pe,"revenue_growth_qoq","total","total",qv,"pct","reported","quarter",d["url"],doc,"Highlights/headline",m["date"],base)
        me=re.search(r"([\d,]+) employees as (?:on|of) [A-Za-z]+ \d+, ?\d{4}",t2)
        if me:
            add(pe,"headcount","total","total",num(me.group(1)),"count","na","point",d["url"],doc,"Highlights",m["date"],"Infosys and its subsidiaries (incl. Infosys BPO)")
        mc=re.search(r"in constant currency (?:terms )?(?:was |of )?([\d.]+)%",hi[:1500],re.I)
        if mc and "corresponding quarter" in hi[max(0,mc.start()-200):mc.start()]:
            add(pe,"revenue_growth_yoy","total","total",float(mc.group(1)),"pct","cc","quarter",d["url"],doc,"Highlights",m["date"],base)

# ---------- 2. fact sheet cells ----------
cells=pd.read_csv(f"{B}/factsheet_cells2.csv")
hand=pd.read_csv(f"{B}/factsheet_hand.csv")
handaccs=set(hand.acc)
GEO={"north america":"North America","europe":"Europe","india":"India","rest of the world":"Rest of the world"}
def clean(l): return re.sub(r"[*#]","",str(l)).strip()
def fs_meta(acc):
    f=fs[acc]; pe0=qend_before(man[acc]["date"])
    return f,pe0
def fsadd(acc,col,metric,dim,dim_type,value,unit,ptype,section,notes,hand_flag=False):
    f,pe0=fs_meta(acc); pe=[pe0,shift(pe0,-1),shift(pe0,-4)][col]
    loc=f"Fact Sheet (image exhibit), table '{section}', column {['current quarter','previous quarter','year-ago quarter'][col]} ({pe.isoformat()})"
    n=(notes+"; " if notes else "")+("hand-entered from fact-sheet image" if hand_flag else "OCR of fact-sheet image (macOS Vision), cross-checked against other vintages")
    add(pe,metric,dim,dim_type,value,unit,"na" if unit!="USD_mn" else "reported",ptype,f["url"],f"Infosys {fq(pe0)} Fact Sheet (6-K Ex.99.5/99.4)",loc,man[acc]["date"],n)
def has_appdev_parent(labels):
    return any(clean(l).lower() in ("maintenance","application development and","application development and maintenance") for l in labels)
def service_canon(labels):
    """map raw service-offering labels (ordered top->bottom) to canonical as-reported names"""
    out=[]; parent=None; has_appdev=any(re.match(r"application development$",clean(l),re.I) for l in labels)
    for i,l in enumerate(labels):
        c=clean(l); lc=c.lower()
        prev=clean(labels[i-1]).lower() if i>0 else ""
        if lc in ("business it services","business operations"): parent="Business IT Services"; out.append(("Business IT Services",True)); continue
        if lc.startswith("consulting & system") : parent="Consulting & System Integration"; out.append(("Consulting & System Integration",True)); continue
        if lc.startswith("products, platforms"): parent="Products, Platforms and Solutions"; out.append(("Products, Platforms and Solutions",True)); continue
        if lc.startswith("consulting, package"): parent=None; out.append(("Consulting, Package Implementation & Others",True)); continue
        if lc in ("maintenance","application development and","application development and maintenance") and has_appdev:
            out.append(("Application Development and Maintenance",True)); continue
        if lc in ("implementation","consulting services and package","consulting services and package implementation"):
            out.append(("Consulting Services and Package Implementation",False)); continue
        if lc=="services" and parent: 
            out.append(("Infrastructure Management Services" if "maintenance" in prev else "Business Process Management Services",False)); continue
        if lc in ("others","other services") and parent: out.append((f"{parent} - Others",False)); continue
        if lc in ("total services",): out.append((None,True)); continue
        if lc in ("","nan"):
            nxt=clean(labels[i+1]).lower() if i+1<len(labels) else ""
            if nxt.startswith("application development") and not has_appdev_parent(labels): out.append(("Application Development and Maintenance",True)); continue
            if prev.startswith("business process management") or nxt.startswith("infrastructure management"): out.append(("Consulting Services and Package Implementation",False)); continue
            out.append((None,False)); continue
        if lc in ("total","total revenues"): out.append((None,False)); continue
        out.append((c[:1].upper()+c[1:],False))
    return out
def industry_canon(c):
    lc=c.lower()
    if lc.startswith("insurance, banking & financial") or lc.startswith("insurance, banking &"): return "Insurance, Banking & Financial Services",True
    if lc.startswith("energy, utilities"): return "Energy, Utilities, Communications & Services",True
    if lc.startswith("retail & life") : return "Retail & Life Sciences",True
    if lc in ("total","totall",""): return None,False
    return c,False
IND_OK=re.compile(r"^(insurance|banking & financial services|manufacturing|retail|telecom|energy & utilities|transportation & logistics|transport & logistics|services|others|retail & cpg|life sciences|healthcare|communication and services|insurance, banking & financial.*|energy, utilities.*|retail & life.*|financial services)$",re.I)
SVC_OK=re.compile(r"^(development|maintenance|re-engineering|package implementation|consulting|testing|engineering services|business process management|other services|total services|products|application development and|application development|application maintenance|consulting services and package|consulting services and package implementation|implementation|infrastructure management|product engineering services|system integration|systems integration|testing services|others|business it services|business operations|services|consulting & system integration|consulting & package|products, platforms and solutions|business process management services|infrastructure management services|consulting, package implementation & others|bpm platform|total|total revenues)$",re.I)
issues=[]
for acc in sorted(fs):
    if acc in handaccs: continue
    c=cells[(cells.acc==acc)&(cells.col<=2)]
    for sec,g in c.groupby("section"):
        # restrict to rows: one value per (y,col)
        g=g.sort_values("y")
        ys=list(dict.fromkeys(g.y))
        if sec=="REVENUE BY GEOGRAPHICAL SEGMENT":
            for y in ys:
                r=g[g.y==y]; lab=clean(r.label.iloc[0]).lower()
                if lab in GEO:
                    for x in r.itertuples(): fsadd(acc,int(x.col),"revenue_share",GEO[lab],"geography",x.value,"pct","quarter",sec,"")
        elif sec=="REVENUE BY INDUSTRY":
            prevlab=""
            for y in ys:
                r=g[g.y==y]; lab=clean(r.label.iloc[0])
                FIX={"MANUFACTURING":"Manufacturing","RETAIL & LIFESCIENCES":"Retail & Life Sciences","COMMUNICATIONS & SERVICES":"Energy, Utilities, Communications & Services",
                     "Heaithcore":"Healthcare","Heaithcare":"Healthcare","Energy, Utilities, Communications":"Energy, Utilities, Communications & Services",
                     "Energy, Utilities, Communications &":"Energy, Utilities, Communications & Services"}
                lab=FIX.get(lab,lab)
                if lab=="Services" and prevlab.lower().startswith("insurance, banking & financial"): lab=prevlab
                prevlab=lab
                if not IND_OK.match(lab): 
                    if lab.lower() not in ("total","totall"): issues.append((acc,sec,lab))
                    continue
                name,sub=industry_canon(lab)
                if lab.lower().startswith("insurance, banking & financial") and name is None: pass
                if lab.lower()=="insurance, banking & financial": name,sub="Insurance, banking & financial services",True
                if name is None: continue
                for x in r.itertuples(): fsadd(acc,int(x.col),"revenue_share",name,"vertical",x.value,"pct","quarter",sec,"subtotal row" if sub else "")
        elif sec=="REVENUE BY SERVICE OFFERING":
            labs=[clean(g[g.y==y].label.iloc[0]) for y in ys]
            bad=[l for l in labs if not SVC_OK.match(l)]
            if bad: issues.append((acc,sec,"|".join(bad)))
            canon=service_canon(labs)
            for y,(name,sub),l in zip(ys,canon,labs):
                if name is None or not SVC_OK.match(l): continue
                for x in g[g.y==y].itertuples(): fsadd(acc,int(x.col),"revenue_share",name,"service_line",x.value,"pct","quarter",sec,"subtotal row" if sub else "")
        elif sec=="EFFORT AND UTILIZATION":
            for y in ys:
                r=g[g.y==y]; lab=clean(r.label.iloc[0]).lower()
                met={"including trainees":"utilization_incl_trainees","excluding trainees":"utilization_excl_trainees"}.get(lab)
                if met:
                    for x in r.itertuples(): fsadd(acc,int(x.col),met,"total","total",x.value,"pct","quarter",sec,"fact-sheet definition (consolidated); see MD&A rows for alternative definition")
        elif sec=="EMPLOYEE METRICS":
            for y in ys:
                r=g[g.y==y]; lab=clean(r.label.iloc[0]).lower()
                if lab.startswith("total employees"):
                    for x in r.itertuples(): fsadd(acc,int(x.col),"headcount","total","total",x.value,"count","point",sec,"Total employees, Infosys and subsidiaries")
                elif lab.startswith("attrition %") or lab.startswith("attrition (ltm)"):
                    for x in r.itertuples(): fsadd(acc,int(x.col),"attrition","total","total",x.value,"pct","ltm",sec,"LTM attrition, excluding subsidiaries (per fact-sheet footnote)")
for x in hand.itertuples():
    sec=x.section; lab=x.label
    for col,v in enumerate([x.c0,x.c1,x.c2]):
        if sec=="REVENUE BY GEOGRAPHICAL SEGMENT": fsadd(x.acc,col,"revenue_share",lab,"geography",v,"pct","quarter",sec,"",True)
        elif sec=="REVENUE BY INDUSTRY":
            sub=lab.startswith(("Insurance, banking","Insurance, Banking","Retail & Life","Energy, Utilities"))
            fsadd(x.acc,col,"revenue_share",lab,"vertical",v,"pct","quarter",sec,"subtotal row" if sub else "",True)
        elif sec=="REVENUE BY SERVICE OFFERING":
            sub=lab in ("Business IT Services","Consulting & System Integration","Products, Platforms and Solutions","Application development and maintenance","Total services")
            fsadd(x.acc,col,"revenue_share",lab,"service_line",v,"pct","quarter",sec,"subtotal row" if sub else "",True)
        elif lab=="Including trainees": fsadd(x.acc,col,"utilization_incl_trainees","total","total",v,"pct","quarter",sec,"fact-sheet definition (consolidated); see MD&A rows for alternative definition",True)
        elif lab=="Excluding trainees": fsadd(x.acc,col,"utilization_excl_trainees","total","total",v,"pct","quarter",sec,"fact-sheet definition (consolidated); see MD&A rows for alternative definition",True)
        elif lab=="Total employees": fsadd(x.acc,col,"headcount","total","total",v,"count","point",sec,"Total employees, Infosys and subsidiaries",True)
        elif lab.startswith("Attrition %"): fsadd(x.acc,col,"attrition","total","total",v,"pct","ltm",sec,"LTM attrition, excluding subsidiaries (per fact-sheet footnote)",True)

# ---------- 3. constant currency table ----------
qre=re.compile(r"^[QO0]\s?([1-4])\s?[' ]?(\d{2})$")
for acc in sorted(fs):
    import glob
    pages=sorted(glob.glob(f"{B}/img/{acc}_*.merged.jsonl"))
    for p in pages:
        T=sorted([json.loads(l) for l in open(p)],key=lambda d:d["y"])
        R=[]
        for t in T:
            if R and abs(R[-1][0]["y"]-t["y"])<0.0065: R[-1].append(t)
            else: R.append([t])
        mode=None; hdr=None
        for r in R:
            r.sort(key=lambda d:d["x0"]); s=" ".join(d["t"] for d in r)
            qs=[d for d in r if qre.match(d["t"].strip().replace("S","5"))]
            if len(qs)>=4:
                low=s.lower()
                if "reported revenues" in low: mode=("reported",None)
                elif "q-o-q" in low or "q o q" in low or "qoq" in low: mode=("cc","qoq")
                elif "yoy" in low or "y o y" in low: mode=("cc","yoy")
                else: mode=None
                hdr=[]
                for d in qs:
                    mm=qre.match(d["t"].strip()); hdr.append((d["x1"],int(mm.group(1)),int(mm.group(2))))
                continue
            if not mode or not hdr: continue
            low=s.lower()
            which=None
            if low.startswith("sequential growth"): which="qoq"
            elif low.startswith("yoy growth"): which="yoy"
            else: continue
            if mode[0]=="cc" and mode[1]!=which: continue
            vals=[d for d in r if re.fullmatch(r"\(?-?\d+\.\d\)?",d["t"].strip())]
            for d in vals:
                h=min(hdr,key=lambda h:abs(h[0]-d["x1"]))
                if abs(h[0]-d["x1"])>0.04: continue
                q,yy=h[1],h[2]; fyv=2000+yy
                pe=datetime.date(fyv-1,[6,9,12][q-1],[30,30,31][q-1]) if q<4 else datetime.date(fyv,3,31)
                v=float(d["t"].strip("()"))*(-1 if d["t"].strip().startswith("(") else 1)
                f=fs[acc]
                add(pe,f"revenue_growth_{which}","total","total",v,"pct",mode[0],"quarter",f["url"],f"Infosys {fq(qend_before(man[acc]['date']))} Fact Sheet (6-K Ex.99.5/99.4)",
                    f"Fact Sheet 'Constant Currency Reporting' table, column Q{q} {yy:02d}",man[acc]["date"],
                    ("reported-currency growth" if mode[0]=="reported" else "constant-currency growth as computed by Infosys")+"; OCR of fact-sheet image")

# ---------- 4. MD&A (quarterly 6-K) ----------
for acc,m in man.items():
    p=f"{B}/edgar/{acc}/index.htm.txtc"
    if not os.path.exists(p) or os.path.getsize(p)<150000: continue
    t=open(p).read(); t2=re.sub(r"\s+"," ",t)
    mm=re.search(r"table sets forth the utilization rates of billable employees for ([^:]{0,160}):? ?Three months ended ([A-Za-z]+ \d+),? ?(\d{4}) \| (\d{4}) Including trainees \| ([\d.]+)% \| ([\d.]+)% Excluding trainees \| ([\d.]+)% \| ([\d.]+)%",t2)
    if not mm:
        mm2=re.search(r"table sets forth the utilization rates of billable employees for ([^:]{0,200}):? ?Three months ended ?([A-Za-z]+ \d+),? (\d{4}) \| [A-Za-z]* ?\d*,? ?(\d{4}) Including trainees \| ([\d.]+)% \| ([\d.]+)% Excluding trainees \| ([\d.]+)% \| ([\d.]+)%",t2)
        mm=mm2
    if mm:
        mon={"March":3,"June":6,"September":9,"December":12}[mm.group(2).split()[0]]
        for yr,inc,exc in ((int(mm.group(3)),mm.group(5),mm.group(7)),(int(mm.group(4)),mm.group(6),mm.group(8))):
            pe=datetime.date(yr,mon,{3:31,6:30,9:30,12:31}[mon])
            dim="IT services excl. BPO (6-K MD&A)"
            note=f"6-K MD&A definition: utilization of billable employees for {mm.group(1).strip()}"
            doc=f"Infosys 6-K quarterly report (MD&A) for quarter ended {qend_before(m['date'])}"
            url=m["base"]+"index.htm"
            add(pe,"utilization_incl_trainees",dim,"other",float(inc),"pct","na","quarter",url,doc,"MD&A - Results of operations, utilization table",m["date"],note)
            add(pe,"utilization_excl_trainees",dim,"other",float(exc),"pct","na","quarter",url,doc,"MD&A - Results of operations, utilization table",m["date"],note)
    for ms in re.finditer(r"(?:For|for) the (three|six|nine) months ended ([A-Za-z]+ \d+, \d{4}) and fiscal (\d{4}),? approximately ([\d.]+)% and ([\d.]+)%,?(?: respectively,)? of our cost of (?:sales|revenues) (?:was|were) attributable to cost of technical subcontractors",t2):
        pe=datetime.datetime.strptime(ms.group(2),"%B %d, %Y").date()
        per={"three":"quarter","six":"ytd","nine":"ytd"}[ms.group(1)]
        url=m["base"]+"index.htm"; doc=f"Infosys 6-K quarterly report (MD&A) for quarter ended {qend_before(m['date'])}"
        note=f"cost of technical subcontractors as % of cost of sales (NOT % of revenue), {ms.group(1)} months ended {pe}; new metric"
        add(pe,"subcontracting_pct_cost_of_sales","total","total",float(ms.group(4)),"pct","reported",per,url,doc,"MD&A - Overview (cost of technical subcontractors)",m["date"],note)
        fy=int(ms.group(3)); pa=datetime.date(fy,3,31)
        add(pa,"subcontracting_pct_cost_of_sales","total","total",float(ms.group(5)),"pct","reported","annual",url,doc,"MD&A - Overview (cost of technical subcontractors)",m["date"],f"fiscal {fy} (Apr-Mar) cost of technical subcontractors as % of cost of sales; new metric")
        break
df=pd.DataFrame(rows,columns=COLS)
# drop hand/ocr 'Total services' subtotal and any fact-sheet share block whose leaf shares do not sum to 100+-0.5 (OCR/label failure)
df=df[~((df.metric=="revenue_share")&(df.dimension=="Total services"))]
sh=df[(df.metric=="revenue_share")&(~df.notes.fillna("").str.contains("subtotal"))]
sums=sh.groupby(["source_doc","dim_type","cal_q"]).value.sum()
bad=sums[(sums-100).abs()>0.5]
dropped=[]
for (doc,dt,cq),v in bad.items():
    m=(df.metric=="revenue_share")&(df.source_doc==doc)&(df.dim_type==dt)&(df.cal_q==cq)
    dropped.append((doc,dt,cq,round(v,1),int(m.sum()))); df=df[~m]
json.dump(dropped,open(f"{B}/dropped_share_blocks.json","w"),indent=0)
print("dropped share blocks:",dropped)
df.to_csv(f"{B}/gfc_infosys_rows.csv",index=False)
print(len(df)); print(df.groupby("metric").size())
print("label issues:",len(issues)); [print(i) for i in issues[:40]]
