import sys, pdfplumber
fn=sys.argv[1]; pages=[int(x) for x in sys.argv[2].split(',')] if len(sys.argv)>2 else None
with pdfplumber.open(fn) as pdf:
    for i,p in enumerate(pdf.pages):
        if pages and i+1 not in pages: continue
        w=p.width
        for name,box in [('L',(0,0,w/2,p.height)),('R',(w/2,0,w,p.height))]:
            t=p.crop(box).extract_text(layout=False) or ''
            print(f'=== page {i+1} {name} ===\n{t}')
