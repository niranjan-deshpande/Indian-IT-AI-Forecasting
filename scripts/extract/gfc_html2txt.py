"""Convert downloaded EDGAR htm files to text (.txtc) preserving table rows as ' | '-joined lines."""
import glob, os, sys
from bs4 import BeautifulSoup
for p in glob.glob("data/sources/gfc/*/edgar/*/*.htm*"):
    out=p+".txtc"
    if os.path.exists(out): continue
    s=BeautifulSoup(open(p,"rb").read(),"lxml")
    for tr in s.find_all("tr"):
        cells=[c.get_text(" ",strip=True) for c in tr.find_all(["td","th"])]
        cells=[c for c in cells if c not in("","$","%",")")]
        tr.replace_with(s.new_string("\n"+" | ".join(cells)+"\n"))
    t=s.get_text("\n")
    t="\n".join(l.strip() for l in t.splitlines() if l.strip())
    open(out,"w").write(t)
