"""Download a PDF (curl w/ browser UA) and extract text with pdfplumber.
Usage: python fetch_extract.py <name> <url> [sec]
Writes text to scratch dir; raw PDF deleted afterwards."""
import sys, subprocess, os, pdfplumber
SCR = os.environ.get("SCR", "/tmp")
name, url = sys.argv[1], sys.argv[2]
ua = ("ndeshpande research ndeshpande@college.harvard.edu" if len(sys.argv) > 3
      else "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36")
from urllib.parse import urlparse
u=urlparse(url); referer=f"{u.scheme}://{u.netloc}/"
pdf = os.path.join(SCR, name + ".pdf")
subprocess.run(["curl", "-sL", "-A", ua, "-e", referer, "-o", pdf, url], check=True)
txt = os.path.join(SCR, name + ".txt")
try:
    with pdfplumber.open(pdf) as p:
        out = [f"=== page {i+1} ===\n" + (pg.extract_text() or "") for i, pg in enumerate(p.pages)]
    open(txt, "w").write("\n".join(out))
    print(name, len(out), "pages ->", txt)
except Exception as e:
    print("FAIL", name, e, open(pdf, 'rb').read(200))
finally:
    if os.path.exists(pdf): os.remove(pdf)
