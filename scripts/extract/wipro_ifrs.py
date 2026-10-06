"""Extract consolidated revenue, employee compensation and sub-contracting/technical fees (INR mn)
from Wipro quarterly IFRS consolidated financial statements (pdftotext -layout output).

For each quarterly statement we take the "three months ended" columns, which show
[prior-year same quarter, current quarter] (years printed ascending, verified per file).
Output: data/sources/wipro/parsed_ifrs.csv
"""
import re, os, glob, csv

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
SRC = os.path.join(ROOT, 'data', 'sources', 'wipro')
TXT = os.path.join(SRC, 'txt')

def fy_q_from_name(fn):
    m = re.match(r'(\d{4})-(\d{4})_([A-Za-z0-9]+)_', fn)
    fy = int(m.group(2)) % 100
    q = int(re.search(r'[qQ](\d)', m.group(3)).group(1))
    return fy, q

def nums(s):
    s = re.sub(r'\((refer )?note \d+\)|\(\d\)', ' ', s, flags=re.I)
    out = []
    for m in re.finditer(r'\(?\d[\d,]*\.?\d*\)?', s):
        t = m.group(0)
        neg = t.startswith('(') and t.endswith(')')
        v = float(t.strip('()').replace(',', ''))
        out.append((-v if neg else v, t))
    return out

def main():
    rows, log = [], []
    files = [f for f in sorted(glob.glob(os.path.join(TXT, '*')))
             if re.search(r'ifrs-financials|IFRS-Financials|consolidated-financial|financials-ifrs|ifrs-consolidated|Financials-Results', os.path.basename(f), re.I)]
    for f in files:
        bn = os.path.basename(f)
        if bn.startswith('2014-2015') or 'Financials-Results' in bn or 'Financial-Results' in bn:
            continue
        fy, q = fy_q_from_name(bn)
        lines = open(f, encoding='utf-8', errors='replace').read().replace('\f', '\n').split('\n')
        # --- revenue from income statement: first line starting with Revenues having >=2 big numbers
        rev = None
        for pat in (r'^\s*(Gross )?Revenues\s+\d{1,2}\s', r'^\s*Total revenues'):
            for i, l in enumerate(lines):
                if re.match(pat, l):
                    ns = [v for v, t in nums(l) if (',' in t)]
                    if len(ns) >= 2:
                        rev = (ns[0], ns[1], i + 1, l.strip()[:120])
                        break
            if rev:
                break
        # --- expenses by nature
        emp = sub = None
        years_ok = None
        for i, l in enumerate(lines):
            if re.search(r'Expenses by nature', l):
                # year header within next 5 lines
                for l2 in lines[i + 1:i + 6]:
                    ys = re.findall(r'\b(20\d\d)\b', l2)
                    if len(ys) >= 2:
                        years_ok = int(ys[1]) > int(ys[0])
                        yrs = ys[:2]
                        break
                for j in range(i + 1, min(i + 40, len(lines))):
                    lj = lines[j]
                    if emp is None and re.match(r'^\s*Employee (compensation|benefits? expense)', lj):
                        ns = [v for v, t in nums(lj)]
                        emp = (ns[0], ns[1], j + 1, lj.strip()[:120])
                    if sub is None and re.match(r'^\s*Sub-?\s?contracting', lj, re.I):
                        ns = [v for v, t in nums(lj)]
                        sub = (ns[0], ns[1], j + 1, lj.strip()[:120])
                break
        if years_ok is False:
            log.append(f'YEAR ORDER DESC {bn}')
        for name, rec in (('revenue', rev), ('employee_cost', emp), ('subcontracting_cost', sub)):
            if rec is None:
                log.append(f'MISSING {name} {bn}')
                continue
            prior, cur, ln, txt = rec
            for (tfy, val) in ((fy - 1, prior), (fy, cur)):
                rows.append(dict(fy=fy, q=q, tfy=tfy, tq=q, metric=name, value=val, file=bn, line=ln, text=txt))
    with open(os.path.join(SRC, 'parsed_ifrs.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(len(rows), 'rows'); print('\n'.join(log))

if __name__ == '__main__':
    main()
