"""Generic positional table extractor for OCR'd fact-sheet images (merged jsonl from gfc_multiocr.py).
Finds section titles, header date columns (by right edge x1), assigns numeric tokens in each labelled row to nearest column.
Usage: gfc_factsheet_tables.py <firm> <acc_prefix_glob>  -> writes data/sources/gfc/<firm>/factsheet_cells.csv"""
import json, glob, re, sys, csv, os
firm=sys.argv[1]
SECTIONS=["REVENUE BY GEOGRAPHICAL SEGMENT","REVENUE BY SERVICE OFFERING","REVENUE BY PROJECT TYPE","REVENUE BY INDUSTRY",
          "CLIENT DATA","EFFORT AND UTILIZATION","PERSON MONTHS","EMPLOYEE METRICS","CONSOLIDATED IT SERVICE","SUBSIDIARIES PERFORMANCE",
          "RUPEE","PERFORMANCE AS AGAINST","CONSTANT CURRENCY","INFRASTRUCTURE","GROSS PROFIT"]
MON={"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,"jul":7,"aug":8,"sep":9,"sop":9,"oct":10,"nov":11,"dec":12,"doc":12,"dac":12,"mat":3,"juns":6}
dre=re.compile(r"^\s*(jan|feb|mar|mat|apr|may|jun|june|jul|aug|sep|sop|sept|oct|nov|dec|doc|dac)[a-z]*\.?\s*(\d{1,2})\s*[,.]?\s*(\d{4})?\s*$",re.I)
num=re.compile(r"^\(?-?[\d,. ]+\)?%?$")
def pnum(t):
    s=t.strip().rstrip("%").replace(" ",".")
    neg=s.startswith("(") and s.endswith(")"); s=s.strip("()")
    if s.count(".")>1 or ("," in s and "." in s and s.rfind(".")<s.rfind(",")):  # e.g. 103.078 as thousands
        pass
    # Indian/Intl thousands: remove commas; if pattern like 103.078 (3 decimals, >=100) treat '.' as thousands sep
    if re.fullmatch(r"\d{1,3}(\.\d{3})+",s) and len(s)>5: s=s.replace(".","")
    s=s.replace(",","")
    try: v=float(s)
    except: return None
    return -v if neg else v
out=[]
files=sorted(glob.glob(f"data/sources/gfc/{firm}/img/*.merged.jsonl"))
for f in files:
    acc=os.path.basename(f).split("_")[0]; page=os.path.basename(f)[len(acc)+1:].split(".")[0]
    T=[json.loads(l) for l in open(f)]
    T.sort(key=lambda d:d["y"])
    rows=[]
    for t in T:
        if rows and abs(rows[-1][0]["y"]-t["y"])<0.0065: rows[-1].append(t)
        else: rows.append([t])
    sec=None; cols=None; year_hint=None
    for r in rows:
        r.sort(key=lambda d:d["x0"])
        txt=" ".join(d["t"] for d in r).upper()
        for s in SECTIONS:
            if r[0]["t"].upper().startswith(s) or (s in txt and r[0]["x0"]<0.3 and len(r)<=2):
                sec=s; cols=None; break
        # header date row: >=2 date tokens
        ds=[]
        for d in r:
            m=dre.match(d["t"].replace("’","'"))
            if m: ds.append((d,m))
        if len(ds)>=2:
            cols=[]
            for d,m in ds:
                mo=MON.get(m.group(1).lower()[:3],None) or MON.get(m.group(1).lower(),None)
                cols.append(dict(x1=d["x1"],mon=mo,day=int(m.group(2)),year=m.group(3),raw=d["t"]))
            continue
        # year-only row just below a header lacking years
        if cols and all(re.fullmatch(r"\d{4}",d["t"].strip()) for d in r if d["x0"]>0.3) and any(re.fullmatch(r"\d{4}",d["t"].strip()) for d in r):
            for d in r:
                if re.fullmatch(r"\d{4}",d["t"].strip()):
                    c=min(cols,key=lambda c:abs(c["x1"]-d["x1"]))
                    if c["year"] is None and abs(c["x1"]-d["x1"])<0.04: c["year"]=d["t"].strip()
            continue
        if not cols or sec is None: continue
        lab=" ".join(d["t"] for d in r if d["x1"]<min(c["x1"] for c in cols)-0.07 and not num.match(d["t"])).strip()
        nums=[d for d in r if num.match(d["t"]) and d["x1"]>min(c["x1"] for c in cols)-0.07 and pnum(d["t"]) is not None]
        for d in nums:
            ci=min(range(len(cols)),key=lambda i:abs(cols[i]["x1"]-d["x1"]))
            if abs(cols[ci]["x1"]-d["x1"])>0.035: continue
            c=cols[ci]
            out.append(dict(acc=acc,page=page,section=sec,label=lab,col=ci,ncols=len(cols),colhdr=c["raw"],mon=c["mon"],day=c["day"],year=c["year"],
                            raw=d["t"],value=pnum(d["t"]),n=d.get("n",1),y=round(d["y"],4)))
with open(f"data/sources/gfc/{firm}/factsheet_cells.csv","w",newline="") as fh:
    w=csv.DictWriter(fh,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print(len(out))
