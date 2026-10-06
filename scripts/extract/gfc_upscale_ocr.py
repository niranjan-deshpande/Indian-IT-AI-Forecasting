"""Upscale fact-sheet images 3x (Lanczos) to PNG and run positional OCR (gfc_ocrj). Usage: python3 gfc_upscale_ocr.py <img_dir>"""
import sys, glob, os, subprocess
from PIL import Image
d=sys.argv[1]
for p in sorted(glob.glob(os.path.join(d,"*.gif"))+glob.glob(os.path.join(d,"*.jpg"))+glob.glob(os.path.join(d,"*.png"))):
    if p.endswith("_x3.png"): continue
    up=p+"_x3.png"; out=up+".ocr.jsonl"
    if os.path.exists(out): continue
    im=Image.open(p).convert("L"); im=im.resize((im.width*3,im.height*3),Image.LANCZOS); im.save(up)
    open(out,"w").write(subprocess.run(["scripts/extract/gfc_ocrj",up],capture_output=True,text=True).stdout)
