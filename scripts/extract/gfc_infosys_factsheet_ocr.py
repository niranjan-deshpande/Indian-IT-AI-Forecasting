"""Find Infosys 'Fact Sheet' exhibits (image-only) in EDGAR 6-Ks, download page GIF/JPGs, OCR via macOS Vision (gfc_ocr)."""
import json, re, os, time, requests, subprocess, glob
UA={"User-Agent":"ndeshpande research ndeshpande@college.harvard.edu"}
B="data/sources/gfc/infosys"
man=json.load(open(f"{B}/edgar_manifest.json"))
out={}
for m in man:
    for d in m["docs"]:
        p=f"{B}/edgar/{m['acc']}/{d['name']}"
        if not p.endswith(".htm"): continue
        h=open(p,errors="ignore").read()
        if not re.search(r"<(?:title|DESCRIPTION)>[^<\n]*fact\s*sheet",h,re.I): continue
        imgs=re.findall(r'src="([^"]+\.(?:gif|jpg|png))"',h,re.I)
        txts=[]
        for im in imgs:
            lp=f"{B}/img/{m['acc']}_{im}"
            if not os.path.exists(lp):
                c=requests.get(m["base"]+im,headers=UA,timeout=60).content; time.sleep(0.15); open(lp,"wb").write(c)
            op=lp+".ocr.txt"
            if not os.path.exists(op):
                o=subprocess.run(["scripts/extract/gfc_ocr",lp],capture_output=True,text=True).stdout; open(op,"w").write(o)
            txts.append(open(op).read())
        out[m["acc"]]=dict(date=m["date"],url=m["base"]+d["name"],imgs=[m["base"]+i for i in imgs])
        open(f"{B}/img/{m['acc']}_factsheet.ocr.txt","w").write("\n\n=====PAGE=====\n".join(txts))
        print(m["date"],m["acc"],len(imgs))
json.dump(out,open(f"{B}/factsheets.json","w"),indent=1)
