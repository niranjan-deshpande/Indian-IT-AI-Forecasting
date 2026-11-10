import sys
from pypdf import PdfReader, PdfWriter
src, out = sys.argv[1], sys.argv[2]; keys = sys.argv[3:]
r = PdfReader(src); w = PdfWriter(); hits = []
for i, p in enumerate(r.pages):
    t = p.extract_text() or ''
    if any(k in t for k in keys):
        hits.append(i + 1); w.add_page(p)
w.write(out); print('pages', hits)
