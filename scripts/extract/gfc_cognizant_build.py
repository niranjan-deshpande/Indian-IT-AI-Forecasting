"""Build Cognizant GFC-window rows (2007Q1-2012Q1) from EDGAR: 8-K earnings releases (revenue growth, headcount),
10-Q (quarterly revenue, segment & geography revenue, attrition), 10-K (quarterly revenue table, annual attrition).
Output: data/sources/gfc/cognizant/gfc_cognizant_rows.csv"""
import json, re, datetime
import pandas as pd
B="data/sources/gfc/cognizant"
man=json.load(open(f"{B}/edgar_manifest.json"))
COLS=["firm","fiscal_q","period_end","cal_q","metric","dimension","dim_type","value","unit","basis","period_type","source_url","source_doc","source_loc","doc_date","notes"]
QE={1:(3,31),2:(6,30),3:(9,30),4:(12,31)}
QN={"first":1,"second":2,"third":3,"fourth":4}
MON={"March":1,"June":2,"September":3,"December":4}
rows=[]
def pe_of(y,q): m,d=QE[q]; return datetime.date(y,m,d)
def add(pe,metric,dim,dt,v,unit,basis,pt,url,doc,loc,dd,notes=""):
    if v is None or not (datetime.date(2007,1,1)<=pe<=datetime.date(2012,3,31)): return
    q=(pe.month-1)//3+1
    rows.append(dict(firm="cognizant",fiscal_q=f"{pe.year}Q{q}",period_end=pe.isoformat(),cal_q=f"{pe.year}Q{q}",metric=metric,dimension=dim,dim_type=dt,value=v,unit=unit,
        basis=basis,period_type=pt,source_url=url,source_doc=doc,source_loc=loc,doc_date=dd,notes=notes))
def n(s): return float(s.replace(",",""))
def txt(m,d): return re.sub(r"\s+"," ",open(f"{B}/edgar/{m['acc']}/{d['name']}.txtc").read())
for m in man:
    for d in m["docs"]:
        if d["name"].endswith("index.html") or re.search(r"d8k\.htm$|\dd8k\.htm$",d["name"]): continue
        t=txt(m,d); url=d["url"]; dd=m["date"]
        if m["form"]=="8-K" and "dex991" in d["name"]:
            s=re.search(r"Revenue for the (?:(first|second|third|fourth) )?quarter(?: of (\d{4}))? (?:rose|increased|grew|was|declined)(?: to)? \$([\d.,]+) (million|billion)(.{0,400})",t)
            if not s: 
                print("no rev sentence",dd); continue
            fd0=datetime.date.fromisoformat(dd); qb=((fd0.month-1)//3) or 4
            q=QN[s.group(1)] if s.group(1) else qb
            fd=datetime.date.fromisoformat(dd); y=int(s.group(2)) if s.group(2) else (fd.year if q<4 else fd.year-1); pe=pe_of(y,q)
            hl=re.search(r"Revenue Up ([\d.]+)% Year-[Oo]ver-[Yy]ear and ([\d.]+)% Sequentially",t[:1500])
            if not hl: hl=re.search(r"()revenue up ([\d.]+)% sequentially",t[:1500],re.I)
            if hl: add(pe,"revenue_growth_qoq","total","total",float(hl.group(2)),"pct","reported","quarter",url,f"Cognizant {y}Q{q} earnings release (8-K Ex.99.1)","Headline",dd,"GAAP revenue, as reported (headline)")
            doc=f"Cognizant {y}Q{q} earnings release (8-K Ex.99.1)"
            for g in re.finditer(r"(up|down) ([\d.]+)%(?: sequentially)? from \$[\d.,]+ (?:million|billion) in the (\w+) quarter of (\d{4})",s.group(5)):
                q2=QN.get(g.group(3)); y2=int(g.group(4)); v=float(g.group(2))*(1 if g.group(1)=="up" else -1)
                if q2==q and y2==y-1: add(pe,"revenue_growth_yoy","total","total",v,"pct","reported","quarter",url,doc,"Body text (revenue paragraph)",dd,"GAAP revenue, as reported")
                elif (y2==y and q2==q-1) or (q==1 and q2==4 and y2==y-1): add(pe,"revenue_growth_qoq","total","total",v,"pct","reported","quarter",url,doc,"Body text (revenue paragraph)",dd,"GAAP revenue, as reported")
            h=re.search(r"(approximately |over |more than |)([\d,]+) employees as of ([A-Za-z]+) (\d+), (\d{4})",t)
            if h:
                ph=pe_of(int(h.group(5)),MON[h.group(3)])
                add(ph,"headcount","total","total",n(h.group(2)),"count","na","point",url,doc,"'About Cognizant' boilerplate",dd,f"'{h.group(1)}{h.group(2)} employees' (as stated in boilerplate; rounded)")
            a=re.search(r"(\w+) quarter annualized attrition rate of ([\d.]+)%, including our BPO/KPO practice",t)
            if a: add(pe,"attrition","total","total",float(a.group(2)),"pct","na","quarter",url,doc,"CEO/President quote",dd,"quarter annualized attrition incl. BPO/KPO (as stated in release)")
        if m["form"]=="10-Q":
            mm=re.search(r"(?:three|Three) [Mm]onths [Ee]nded (March|June|September) 30|(?:three|Three) [Mm]onths [Ee]nded (March) 31",t)
            per=re.search(r"(?:QUARTERLY PERIOD ENDED|quarterly period ended) ([A-Za-z]+) (\d+), (\d{4})",t)
            if not per: print("no period",dd); continue
            pe=pe_of(int(per.group(3)),MON[per.group(1).capitalize()]); y=pe.year
            doc=f"Cognizant 10-Q {y}Q{(pe.month-1)//3+1}"
            r=re.search(r"Revenues \| (\d{1,3}(?:,\d{3})+) \| (\d{1,3}(?:,\d{3})+)",t)
            if r:
                add(pe,"revenue","total","total",n(r.group(1))/1000,"USD_mn","reported","quarter",url,doc,"Condensed consolidated statements of operations",dd,"US GAAP; converted from USD thousands (÷1000)")
                add(pe.replace(year=pe.year-1),"revenue","total","total",n(r.group(2))/1000,"USD_mn","reported","quarter",url,doc,"Condensed consolidated statements of operations (prior-year column)",dd,"US GAAP; converted from USD thousands (÷1000)")
            i=t.find("Revenues: Financial Services")
            if i>0:
                seg=t[i:i+600]
                for lab in ["Financial Services","Healthcare","Manufacturing/Retail/Logistics","Other"]:
                    s2=re.search(re.escape(lab)+r" \| ([\d,]+) \| ([\d,]+)",seg)
                    if s2:
                        add(pe,"segment_revenue",lab,"vertical",n(s2.group(1))/1000,"USD_mn","reported","quarter",url,doc,"Notes - Segment information, revenues (three months)",dd,"reportable segment revenue; USD thousands ÷1000")
                        add(pe.replace(year=pe.year-1),"segment_revenue",lab,"vertical",n(s2.group(2))/1000,"USD_mn","reported","quarter",url,doc,"Notes - Segment information, revenues (three months, prior-year column)",dd,"reportable segment revenue; USD thousands ÷1000")
            jm=re.search(r"Revenues:? ?(?:\( ?\d ?\) )?North America",t)
            j=jm.start() if jm else -1
            if j>0:
                seg=t[j:j+500]
                for lab,pat in [("North America",r"North America(?: \(\d\))? \| ([\d,]+) \| ([\d,]+)"),("Europe",r"Europe(?: \(\d\))? \| ([\d,]+) \| ([\d,]+)"),("Other",r"Other(?: \(\d\))? \| ([\d,]+) \| ([\d,]+)"),("Asia",r"Asia(?: \(\d\))? \| ([\d,]+) \| ([\d,]+)")]:
                    s3=re.search(pat,seg)
                    if s3:
                        add(pe,"segment_revenue",lab,"geography",n(s3.group(1))/1000,"USD_mn","reported","quarter",url,doc,"Notes - Geographic area information (three months)",dd,"revenue by customer location; USD thousands ÷1000")
                        add(pe.replace(year=pe.year-1),"segment_revenue",lab,"geography",n(s3.group(2))/1000,"USD_mn","reported","quarter",url,doc,"Notes - Geographic area information (three months, prior-year column)",dd,"revenue by customer location; USD thousands ÷1000")
            at=re.search(r"[Aa]nnualized (?:turnover|attrition rate),? including both voluntary and (?:\d+ Table of Contents )?involuntary,? was approximately ([\d.]+)% during the three months ended ([A-Za-z]+) (\d+), (\d{4})",t)
            if at: add(pe_of(int(at.group(4)),MON[at.group(2)]),"attrition","total","total",float(at.group(1)),"pct","na","quarter",url,doc,"Risk factors (attrition)",dd,"annualized turnover (attrition) incl. voluntary and involuntary, three months (10-Q risk factors)")
        if m["form"]=="10-K":
            fy=re.search(r"(?:FISCAL YEAR ENDED|fiscal year ended) December 31, (\d{4})",t); fy=int(fy.group(1))
            doc=f"Cognizant 10-K FY{fy}"
            for qq in re.finditer(r"Three Months Ended \| Full Year (\d{4}) \| March 31 \| June 30 \| September 30 \| December 31 Revenues? \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \| ([\d,]+)",t):
                yy=int(qq.group(1))
                for k in range(4):
                    add(pe_of(yy,k+1),"revenue","total","total",n(qq.group(k+2))/1000,"USD_mn","reported","quarter",url,doc,"Selected quarterly financial data (unaudited)",dd,"US GAAP; USD thousands ÷1000")
            at=re.search(r"[Aa]nnualized (?:turnover|attrition rate),? including both voluntary and (?:\d+ Table of Contents )?involuntary,? was approximately ([\d.]+)% for (\d{4})",t)
            if at: add(pe_of(int(at.group(2)),4),"attrition","total","total",float(at.group(1)),"pct","na","annual",url,doc,"Risk factors (attrition)",dd,f"annualized attrition incl. voluntary and involuntary, full year {at.group(2)}")
            h=re.search(r"As of December 31, (\d{4}), we employed approximately ([\d,]+) persons",t)
            if h: add(pe_of(int(h.group(1)),4),"headcount","total","total",n(h.group(2)),"count","na","point",url,doc,"Item 1 - Employees",dd,"'approximately' (rounded as stated)")
df=pd.DataFrame(rows,columns=COLS); df.to_csv(f"{B}/gfc_cognizant_rows.csv",index=False)
print(len(df)); print(df.groupby(["metric","dim_type"]).size())
