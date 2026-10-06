"""Build Accenture GFC-window rows (fiscal Q2FY07 [Feb-2007] .. Q2FY12 [Feb-2012]) from EDGAR 8-K earnings releases
(net revenues, USD/local-currency growth, consulting/outsourcing, operating group & geography revenue and growth, bookings,
utilization, attrition) and 10-Q/10-K MD&A (headcount, utilization, attrition). Output data/sources/gfc/accenture/gfc_accenture_rows.csv"""
import json, re, datetime
import pandas as pd
B="data/sources/gfc/accenture"
man=json.load(open(f"{B}/edgar_manifest.json"))
COLS=["firm","fiscal_q","period_end","cal_q","metric","dimension","dim_type","value","unit","basis","period_type","source_url","source_doc","source_loc","doc_date","notes"]
QN={"first":1,"second":2,"third":3,"fourth":4}
def pe_of(fy,q):
    return {1:datetime.date(fy-1,11,30),2:(datetime.date(fy,2,29) if fy%4==0 else datetime.date(fy,2,28)),3:datetime.date(fy,5,31),4:datetime.date(fy,8,31)}[q]
def calq(pe): return f"{pe.year}Q{ {11:4,2:1,5:2,8:3}[pe.month] }"
rows=[]
def add(fy,q,metric,dim,dt,v,unit,basis,pt,url,doc,loc,dd,notes=""):
    if v is None: return
    pe=pe_of(fy,q)
    if not (datetime.date(2007,1,1)<=pe<=datetime.date(2012,3,31)): return
    rows.append(dict(firm="accenture",fiscal_q=f"Q{q}FY{str(fy)[2:]}",period_end=pe.isoformat(),cal_q=calq(pe),metric=metric,dimension=dim,dim_type=dt,value=v,unit=unit,
        basis=basis,period_type=pt,source_url=url,source_doc=doc,source_loc=loc,doc_date=dd,notes=notes))
def amt(x,u): v=float(x.replace(",","")); return v*1000 if u=="billion" else v
def growth(s):
    """parse USD and LC growth from phrases like 'an increase of 16 percent in U.S. dollars and 10 percent in local currency'"""
    s=s.replace("U.S. dollars","USD").replace("local currency","LC")
    m=re.match(r"\s*(?:an? )?(increase|decrease) of (\d+) percent in both USD and LC",s)
    if m: v=int(m.group(2))*(1 if m.group(1)=="increase" else -1); return v,v
    m=re.match(r"\s*flat in both USD and LC",s)
    if m: return 0,0
    m=re.match(r"\s*(?:(?:an? )?(increase|decrease) of (\d+) percent|(flat)) in USD and (?:(?:an? )?(increase|decrease) of )?(?:(\d+) percent|(flat)) in LC",s)
    if not m: return None,None
    usd=0 if m.group(3) else int(m.group(2))*(1 if m.group(1)=="increase" else -1)
    if m.group(6): lc=0
    else:
        sign=m.group(4) or m.group(1) or "increase"
        lc=int(m.group(5))*(1 if sign=="increase" else -1)
    return usd,lc
OG=["Communications & High Tech","Financial Services","Health & Public Service","Products","Public Service","Resources"]
GEO={"Americas":"Americas","Europe, Middle East and Africa (EMEA)":"EMEA","EMEA":"EMEA","Asia Pacific":"Asia Pacific"}
for m in man:
    for d in m["docs"]:
        if d["name"].endswith("index.html"): continue
        t=re.sub(r"\s+"," ",open(f"{B}/edgar/{m['acc']}/{d['name']}.txtc").read()); url=d["url"]; dd=m["date"]
        if m["form"]=="8-K" and ("99" in d["name"] or "exhibit" in d["name"].lower()):
            i0=t.find("Accenture Reports")
            if i0<0: continue
            hd=t[i0:i0+200]
            h=re.search(r"(First|Second|Third|Fourth)-Quarter.{0,40}?Fiscal (\d{4})",hd)
            if h: q=QN[h.group(1).lower()]; fy=int(h.group(2))
            else:
                h=re.search(r"for Fiscal (\d{4})",hd)
                if not h: continue
                q=4; fy=int(h.group(1))
            doc=f"Accenture Q{q}FY{str(fy)[2:]} earnings release (8-K Ex.99.1)"; doc=f"Accenture Q{q}FY{str(fy)[2:]} earnings release (8-K Ex.99.1)"
            def cell(x):
                x=x.replace(" ",""); neg=x.startswith("("); v=int(x.strip("()%")); return -v if neg else v
            PC=r"(\(?-?\d+ ?%?\)?%?|n/m)(?: \| %\))?"
            TBL=r" ?(?:\(\d\))?\*? \| ([\d,]+) \| ([\d,]+) \|(?: \(\d\) \|)? "+PC+r" \| "+PC
            tr=re.search(r"TOTAL Net Revenues"+TBL,t)
            if tr:
                add(fy,q,"revenue","total","total",int(tr.group(1).replace(",",""))/1000,"USD_mn","reported","quarter",url,doc,"Financial table - TOTAL Net Revenues (three months)",dd,"net revenues (revenues before reimbursements); US GAAP; USD thousands /1000")
                add(fy,q,"revenue_growth_yoy","total","total",cell(tr.group(3)),"pct","reported","quarter",url,doc,"Financial table - % increase (decrease) U.S. dollars",dd,"growth in U.S. dollars vs same quarter prior fiscal year")
                add(fy,q,"revenue_growth_yoy","total","total",cell(tr.group(4)),"pct","cc","quarter",url,doc,"Financial table - % increase (decrease) local currency",dd,"growth in local currency (Accenture's constant-currency measure)")
            else: print("no total table",dd)
            LABS=[(l,"vertical",l) for l in ["Communications & High Tech","Communications, Media & Technology","Financial Services","Health & Public Service","Government","Public Service","Products","Resources"]]+\
                 [("Americas","geography","Americas"),("EMEA","geography","EMEA"),("Asia Pacific","geography","Asia Pacific"),("Consulting","service_line","Consulting"),("Outsourcing","service_line","Outsourcing")]
            for lab,dt,dim in LABS:
                sm=re.search(r"(?<!& )"+re.escape(lab)+TBL,t)
                if not sm: continue
                note={"vertical":"operating group","geography":"geographic region","service_line":"type of work"}[dt]
                add(fy,q,"segment_revenue",dim,dt,int(sm.group(1).replace(",",""))/1000,"USD_mn","reported","quarter",url,doc,"Financial table (three months)",dd,note+"; USD thousands /1000")
                if sm.group(3)!="n/m":
                    add(fy,q,"segment_growth_yoy",dim,dt,cell(sm.group(3)),"pct","reported","quarter",url,doc,"Financial table (three months)",dd,note+"; USD growth yoy")
                    add(fy,q,"segment_growth_yoy",dim,dt,cell(sm.group(4)),"pct","cc","quarter",url,doc,"Financial table (three months)",dd,note+"; local-currency growth yoy")
            b=re.search(r"New bookings for the (?:\w+ )?quarter were (?:a record )?\$([\d.,]+) (billion|million)",t)
            if b: add(fy,q,"bookings","total","total",amt(b.group(1),b.group(2)),"USD_mn","reported","quarter",url,doc,"New Bookings",dd,"new bookings (consulting + outsourcing)")
            u=re.search(r"Utilization for the (?:quarter|\w+ quarter(?: of fiscal \d{4})?) was (\d+) percent",t)
            if u: add(fy,q,"utilization_incl_trainees","total","total",float(u.group(1)),"pct","na","quarter",url,doc,"Financial Review",dd,"Accenture 'utilization' (client-service personnel; no trainee split disclosed) - mapped to incl_trainees by convention")
            a=re.search(r"Attrition (?:for the (?:quarter|\w+ quarter(?: of fiscal \d{4})?) )?was (\d+) percent",t)
            if a: add(fy,q,"attrition","total","total",float(a.group(1)),"pct","na","quarter",url,doc,"Financial Review",dd,"annualized attrition, excluding involuntary terminations (per 10-Q definition)")
        if m["form"] in ("10-Q","10-K"):
            doc=f"Accenture {m['form']} filed {dd}"
            for a in re.finditer(r"Annualized attrition(?:,)? (?:excluding involuntary terminations,? )?(?:in|for) the (\w+) quarter of fiscal (\d{4}) was (\d+)%",t):
                add(int(a.group(2)),QN[a.group(1)],"attrition","total","total",float(a.group(3)),"pct","na","quarter",url,doc,"MD&A - Overview (attrition)",dd,"annualized attrition, excluding involuntary terminations")
                break
            a=re.search(r"Annualized attrition for the three months and year ended August 31, (\d{4}) was (\d+)%",t)
            if a: add(int(a.group(1)),4,"attrition","total","total",float(a.group(2)),"pct","na","quarter",url,doc,"MD&A - Overview (attrition)",dd,"annualized attrition excl. involuntary terminations; three months (same as full year)")
            a=re.search(r"Annualized attrition, excluding involuntary terminations, for the three months and year ended August 31, (\d{4}) was (\d+)% and (\d+)%",t)
            if a: add(int(a.group(1)),4,"attrition","total","total",float(a.group(2)),"pct","na","quarter",url,doc,"MD&A - Overview (attrition)",dd,"annualized attrition excl. involuntary terminations; three months")
            u=re.search(r"Utilization for the (\w+) quarter of fiscal (\d{4}) was approximately (\d+)%",t)
            if u: add(int(u.group(2)),QN[u.group(1)],"utilization_incl_trainees","total","total",float(u.group(3)),"pct","na","quarter",url,doc,"MD&A - Cost of services (utilization)",dd,"Accenture 'utilization' (no trainee split disclosed) - mapped to incl_trainees by convention; 'approximately'")
            u=re.search(r"Utilization for the three months ended (February|May) (\d+), (\d{4}) was approximately (\d+)%",t)
            if u:
                fy=int(u.group(3)); q=2 if u.group(1)=="February" else 3
                add(fy,q,"utilization_incl_trainees","total","total",float(u.group(4)),"pct","na","quarter",url,doc,"MD&A - Cost of services (utilization)",dd,"Accenture 'utilization'; 'approximately'")
            h=re.search(r"headcount[^.]{0,80}? (?:to|at) (approximately|more than) ([\d,]+) as of ([A-Za-z]+) (\d+), (\d{4})",t)
            if h:
                mon=h.group(3); yr=int(h.group(5)); q={"November":1,"February":2,"May":3,"August":4}[mon]; fy=yr+1 if mon=="November" else yr
                add(fy,q,"headcount","total","total",float(h.group(2).replace(",","")),"count","na","point",url,doc,"MD&A - Overview (headcount)",dd,f"'{h.group(1)}' (rounded as stated)")
df=pd.DataFrame(rows,columns=COLS); df.to_csv(f"{B}/gfc_accenture_rows.csv",index=False)
print(len(df)); print(df.groupby(["metric","dim_type","basis"]).size())
