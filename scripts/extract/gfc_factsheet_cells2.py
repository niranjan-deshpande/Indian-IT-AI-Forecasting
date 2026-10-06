"""Cluster-based column assignment for OCR'd fact sheet tables (Infosys-style: 5 numeric columns = 3 quarters + 2 LTM/YE).
For each page & section: numeric tokens' right edges (x1) are clustered; columns are ordered left->right.
Writes data/sources/gfc/<firm>/factsheet_cells2.csv with col index within section."""
import json, glob, re, sys, csv, os
firm=sys.argv[1]
SECTIONS=["EMPLOYEE METRICS - SUBSIDIARIES","EMPLOYEE METRICS-SUBSIDIARIES","EMPLOYEE METRICS -SUBSIDIARIES","REVENUE BY GEOGRAPHICAL SEGMENT","REVENUE BY SERVICE OFFERING","REVENUE BY PROJECT TYPE","REVENUE BY INDUSTRY",
          "CLIENT DATA","EFFORT AND UTILIZATION","PERSON MONTHS","EMPLOYEE METRICS","CONSOLIDATED IT SERVICE","SUBSIDIARIES PERFORMANCE",
          "RUPEE","PERFORMANCE AS AGAINST","CONSTANT CURRENCY","INFRASTRUCTURE","GROSS PROFIT","US DOLLAR RATE"]
num=re.compile(r"^\(?-?\d[\d,. ]*\)?%?$")
dre=re.compile(r"(jan|feb|mar|apr|may|jun|jul|aug|sep|sop|oct|nov|dec|doc)[a-z]*\.?\s*\d{1,2}",re.I)
def pnum(t):
    s=t.strip().rstrip("%").strip()
    neg=s.startswith("(") and s.endswith(")"); s=s.strip("()").strip()
    if re.fullmatch(r"\d{1,3}\.\d{3}",s) or re.fullmatch(r"\d{1,2}(\.\d{2})+\.\d{3}",s): s=s.replace(".",",")
    if re.fullmatch(r"\d+ \d",s): s=s.replace(" ",".")
    if re.fullmatch(r"\d{1,2}\.\d{2},\d{3}",s) or re.fullmatch(r"\d{1,2},\d{2}\.\d{3}",s): s=s.replace(".",",")
    s=s.replace(" ","")
    if not re.fullmatch(r"\d[\d,]*(\.\d+)?",s): return None
    v=float(s.replace(",",""))
    return -v if neg else v
out=[]
for f in sorted(glob.glob(f"data/sources/gfc/{firm}/img/*.merged.jsonl")):
    acc=os.path.basename(f).split("_")[0]; page=os.path.basename(f)[len(acc)+1:].split(".")[0]
    T=sorted([json.loads(l) for l in open(f)],key=lambda d:d["y"])
    rows=[]
    for t in T:
        if rows and abs(rows[-1][0]["y"]-t["y"])<0.0065: rows[-1].append(t)
        else: rows.append([t])
    # split into sections
    secs=[]; cur=None
    for r in rows:
        r.sort(key=lambda d:d["x0"])
        hit=[s for s in SECTIONS for d in r if d["t"].upper().strip().startswith(s)]
        if hit and len(r)<=3: cur=dict(sec=hit[0],rows=[]); secs.append(cur); continue
        if cur: cur["rows"].append(r)
    for s in secs:
        cells=[]
        for r in s["rows"]:
            if sum(1 for d in r if dre.search(d["t"]))>=2: continue  # header row
            numt=[d for d in r if num.match(d["t"].strip()) and d["x0"]>0.3 and pnum(d["t"]) is not None]
            if not numt: continue
            lab=" ".join(d["t"] for d in r if d["x1"]<=min(x["x0"] for x in numt)+0.001 and d not in numt).strip()
            for d in numt: cells.append((lab,d,round(r[0]["y"],4)))
        if not cells: continue
        xs=sorted(d["x1"] for _,d,_ in cells)
        cl=[[xs[0]]]
        for x in xs[1:]:
            if x-cl[-1][-1]>0.025: cl.append([x])
            else: cl[-1].append(x)
        cl=[c for c in cl if len(c)>=2] or cl
        cent=[sum(c)/len(c) for c in cl]
        for lab,d,y in cells:
            ci=min(range(len(cent)),key=lambda i:abs(cent[i]-d["x1"]))
            if abs(cent[ci]-d["x1"])>0.03: continue
            out.append(dict(acc=acc,page=page,section=s["sec"],label=lab,col=ci,ncols=len(cent),raw=d["t"],value=pnum(d["t"]),n=d.get("n",1),y=y))
with open(f"data/sources/gfc/{firm}/factsheet_cells2.csv","w",newline="") as fh:
    w=csv.DictWriter(fh,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print(len(out))
