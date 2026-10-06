"""Rebuild text lines from Vision OCR box output (gfc_techm_ocr.swift) -> <name>.txt next to it.
Used only to let a human read the scanned results advertisements; values were then hand-entered
into gfc_techm_extract.py and checked (segment sums, cross-check vs fact sheets)."""
import glob, os, sys
def lines(path):
    rows = []
    for l in open(path):
        if '\t' not in l: continue
        b, t = l.rstrip('\n').split('\t', 1)
        x0, y0, x1, y1 = map(float, b.split())
        rows.append((y0, y1, x0, t))
    rows.sort()
    out = []
    for y0, y1, x0, t in rows:
        c = (y0 + y1) / 2
        for L in out:
            if abs(L['c'] - c) < (y1 - y0) * 0.45:
                L['w'].append((x0, t)); break
        else:
            out.append({'c': c, 'w': [(x0, t)]})
    res = []
    for L in sorted(out, key=lambda L: L['c']):
        res.append(f"{int(L['c']):6d}  " + ' | '.join(f"{t}" for x, t in sorted(L['w'])))
    return res
if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else '.'
    for p in glob.glob(os.path.join(d, '*.ocr')):
        open(p[:-4] + '.txt', 'w').write('\n'.join(lines(p)) + '\n')
