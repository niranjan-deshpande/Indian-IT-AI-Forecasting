"""Download all htm/txt documents of relevant GFC-window EDGAR filings into data/sources/gfc/<firm>/edgar/<acc>/"""
import json, time, requests, os, sys
UA={"User-Agent":"ndeshpande research ndeshpande@college.harvard.edu"}
def want(firm,r):
    if firm in("infosys","wipro"): return r["form"] in("6-K","20-F","20-F/A")
    return r["form"] in("10-K","10-Q") or (r["form"]=="8-K" and "2.02" in r["items"])
for firm in sys.argv[1:]:
    rows=json.load(open(f"data/sources/gfc/{firm}/edgar_filings.json"))
    man=[]
    for r in rows:
        if not want(firm,r): continue
        cik=str(int(r["cik"])); a=r["acc"].replace("-","")
        d=f"data/sources/gfc/{firm}/edgar/{r['acc']}"; os.makedirs(d,exist_ok=True)
        base=f"https://www.sec.gov/Archives/edgar/data/{cik}/{a}/"
        try:
            idx=requests.get(base+"index.json",headers=UA,timeout=60).json(); time.sleep(0.15)
        except Exception as e: print("ERR idx",r["acc"],e); continue
        docs=[]
        for it in idx["directory"]["item"]:
            n=it["name"]
            if n.lower().endswith((".htm",".html",".txt",".pdf")) and not n.endswith("-index.htm") and not n.endswith("-index-headers.html") and n!=r["acc"]+".txt":
                if r["form"] in("10-K","20-F","20-F/A","10-Q") and n!=r["doc"] and not n.lower().startswith(("ex99","dex99")): continue
                p=os.path.join(d,n)
                if not os.path.exists(p):
                    c=requests.get(base+n,headers=UA,timeout=120).content; time.sleep(0.15)
                    open(p,"wb").write(c)
                docs.append(dict(name=n,url=base+n))
        man.append(dict(r,base=base,docs=docs)); print(firm,r["form"],r["date"],len(docs))
    json.dump(man,open(f"data/sources/gfc/{firm}/edgar_manifest.json","w"),indent=0)
