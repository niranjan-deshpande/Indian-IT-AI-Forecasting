"""Multi-variant OCR for small table images: runs macOS Vision (gfc_ocrj) on 1x, 2x, 3x, 4x and horizontal strips of 2x,
merges tokens by position, majority vote on text. Output <img>.merged.jsonl. Usage: gfc_multiocr.py <img files...>"""
import sys, os, subprocess, json, collections, tempfile
from PIL import Image, ImageFilter
OCR="scripts/extract/gfc_ocrj"
def ocr(im):
    f=tempfile.NamedTemporaryFile(suffix=".png",delete=False); im.save(f.name)
    r=[json.loads(l) for l in subprocess.run([OCR,f.name],capture_output=True,text=True).stdout.splitlines() if l.startswith("{")]
    os.unlink(f.name); return r
def run(p):
    out=p+".merged.jsonl"
    if os.path.exists(out): return
    base=Image.open(p).convert("L")
    toks=[]
    for k in (1,2,3,4):
        im=base.resize((base.width*k,base.height*k),Image.LANCZOS)
        if k==2: im=im.filter(ImageFilter.SHARPEN)
        toks+= [dict(t,v=f"x{k}") for t in ocr(im)]
    # strips of 2x image, height 12% with 50% overlap
    im=base.resize((base.width*2,base.height*2),Image.LANCZOS); H=im.height
    s=0.0
    while s<1.0:
        e=min(1.0,s+0.12); c=im.crop((0,int(s*H),im.width,int(e*H)))
        for t in ocr(c):
            t=dict(t); t["y"]=s+t["y"]*(e-s); t["h"]=t["h"]*(e-s); t["v"]="strip"; toks.append(t)
        s+=0.06
    # cluster tokens: same if y within 0.006 and x-overlap > 50%
    cl=[]
    for t in toks:
        for c in cl:
            r=c[0]
            ov=min(r["x1"],t["x1"])-max(r["x0"],t["x0"]); w=min(r["x1"]-r["x0"],t["x1"]-t["x0"])
            if abs(r["y"]-t["y"])<0.006 and w>0 and ov/w>0.5: c.append(t); break
        else: cl.append([t])
    with open(out,"w") as f:
        for c in cl:
            cnt=collections.Counter(x["t"] for x in c); txt,n=cnt.most_common(1)[0]
            r=[x for x in c if x["t"]==txt][0]
            f.write(json.dumps(dict(y=r["y"],x0=r["x0"],x1=r["x1"],t=txt,n=len(c),alts=dict(cnt)))+"\n")
for p in sys.argv[1:]: run(p)
