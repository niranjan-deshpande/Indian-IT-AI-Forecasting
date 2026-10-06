"""Random spot-check: for text-sourced EDGAR rows, confirm the reported value string occurs in the local copy of the source document."""
import pandas as pd, re, sys, glob, os, random
random.seed(int(sys.argv[2]) if len(sys.argv)>2 else 1)
firm=sys.argv[1]
d=pd.read_csv(f"data/sources/gfc/{firm}/gfc_{firm}_rows.csv")
d=d[~d.notes.fillna("").str.contains("OCR|hand-entered")]
S=d.sample(min(12,len(d)),random_state=random.randint(0,999))
for r in S.itertuples():
    acc=r.source_url.split("/")[-2]; name=r.source_url.split("/")[-1]
    # map accession-without-dashes to local folder
    cand=[p for p in glob.glob(f"data/sources/gfc/{firm}/edgar/*/{name}.txtc") if p.split("/")[-2].replace("-","")==acc]
    t=re.sub(r"\s+"," ",open(cand[0]).read()) if cand else ""
    v=r.value
    forms=set()
    if r.unit=="USD_mn" and "thousands" in str(r.notes): forms.add(f"{int(round(v*1000)):,}")
    elif r.unit=="USD_mn": forms|={f"{v:,.0f}",f"{v/1000:.2f}",f"{v/1000:.3f}",f"{v:,.1f}",f"{v/1000:.1f}"}
    elif r.unit=="count": forms|={f"{int(v):,}"}
    else: forms|={f"{v:g}",f"{abs(v):g}",f"{v:.1f}",f"{abs(v):.1f}"}
    ok=any(f in t for f in forms)
    print("OK " if ok else "?? ",r.cal_q,r.metric,r.dimension,v,"|",name,"|",sorted(forms)[:3])
