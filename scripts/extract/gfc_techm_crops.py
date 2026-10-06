"""Render crops of the segment table and expenditure rows of the scanned TechM results ads,
located via the Vision OCR boxes (600 dpi coordinates), for human reading / verification."""
import os, subprocess, sys
D = sys.argv[1]; OUT = sys.argv[2]
DOCS = ['TechM_Q4_F09_Consolidated','TechM_Q1_F10_Consolidated','TechM_Q3_F10_Consolidated','TechM_Q4_F10_Consolidated',
        'TechM_Q1_F11_Consolidated','TechM_Q2_F11_Consolidated','TechM_Q3_F11_Consolidated','Consolidated_Q2F12','Consolidated_Q3F12','Consolidated_Q4F12']
def boxes(p):
    for l in open(p):
        b, t = l.rstrip('\n').split('\t', 1)
        yield list(map(float, b.split())), t
for d in DOCS:
    bx = list(boxes(os.path.join(D, 'ocr', d + '_full.ocr')))
    def find(key, after=0):
        c = [b for b, t in bx if key.lower() in t.lower() and b[1] > after]
        return min(c, key=lambda b: b[1]) if c else None
    seg = find('Segment Revenue'); net = find('Income from operations', seg[1] if seg else 0) or find('Net Sales', seg[1] if seg else 0)
    inc = find('Income from Operations'); sub = find('Business Associates')
    crops = []
    if seg and net:
        crops.append(('seg', seg[0] - 80, seg[1] - 700, 99999, net[3] - seg[1] + 800))
    if inc and sub:
        crops.append(('exp', inc[0] - 80, inc[1] - 600, 4200, sub[3] - inc[1] + 700))
    for name, x, y, w, h in crops:
        x, y = max(0, int(x)), max(0, int(y))
        subprocess.run(['pdftoppm', '-r', '600', '-x', str(x), '-y', str(y), '-W', str(int(w) if w < 99999 else 20000), '-H', str(int(h)),
                        '-png', '-singlefile', os.path.join(D, d + '.pdf'), os.path.join(OUT, f'{d}_{name}')])
    print(d, [c[0] for c in crops])
