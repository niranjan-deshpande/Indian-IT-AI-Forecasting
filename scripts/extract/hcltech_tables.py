"""Generic table extractor for HCLTech investor releases (text from pdftotext -layout,
or macOS Vision OCR output for image-only PDFs).

Produces "raw cells": (doc, line_no, header_label, header_extras, subctx, row_label, col, value_str).
Used by hcltech_parse.py.

Text generation (reproducible):
  pdftotext -layout <pdf> txt/<name>.txt
  OCR for image-only PDFs (Q4FY23, Q1FY24, Q2FY24, Q3FY24):
     pdftoppm -r 250 -png <pdf> img/p ; swiftc -O hcltech_ocr.swift -o hcl_ocr ; ./hcl_ocr img/p-XX.png >> ocr/<name>.txt
"""
import re, os, subprocess

CYR = str.maketrans({'М': 'M', 'а': 'a', 'г': 'r', 'о': 'o', 'е': 'e', 'с': 'c', 'р': 'p', 'А': 'A', 'С': 'C', 'Е': 'E', 'О': 'O', 'Т': 'T', 'Н': 'H', 'В': 'B', 'К': 'K', 'х': 'x', 'у': 'y'})
MON = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*'
DATE_RE = re.compile(r'\b(\d{1,2})-(' + MON + r')-(\d{2,4})\b', re.I)
NUM_RE = re.compile(r'^\(?[-–−]?[$₹]?\d[\d,]*(?:\.\d+)?\.?%?\)?\*?#?$')
NIL = {'-', '–', '—', 'NA', 'N/A', 'na', '−'}
MONTHS = {m: i for i, m in enumerate(['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'], 1)}


def norm_date(d, m, y):
    import calendar
    y = int(y)
    if y < 100:
        y += 2000
    mi = MONTHS[m[:3].lower()]
    return f"{y:04d}-{mi:02d}-{int(d):02d}"


def load_text(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        txt = f.read().translate(CYR)
    lines = []
    for ln in txt.splitlines():
        if not ln.strip():
            continue
        lines.append(re.sub(r'\s{3,}', '  ', ln.rstrip()))
    return lines


def is_num(tok):
    return bool(NUM_RE.match(tok)) or tok in NIL


def parse_num(tok):
    if tok in NIL:
        return None
    t = tok.rstrip('*#')
    neg = t.startswith('(') and t.endswith(')')
    t = t.strip('()').replace(',', '').replace('$', '').replace('₹', '')
    t = t.replace('–', '-').replace('−', '-')
    pct = t.endswith('%')
    t = t.rstrip('%')
    try:
        v = float(t)
    except ValueError:
        return None
    if neg:
        v = -v
    return v


def split_row(line):
    """return (label, [numeric tokens]) by consuming numeric fields from the right."""
    fields = [f for f in re.split(r'\s{2,}', line.strip()) if f]
    nums = []
    while fields:
        sub = fields[-1].split()
        if sub and all(is_num(s) for s in sub):
            nums = sub + nums
            fields.pop()
        else:
            # a field like "Label 12.3%" (single space) -> peel numeric tail tokens
            tail = []
            while sub and is_num(sub[-1]):
                tail.insert(0, sub.pop())
            # keep short integers that belong to the label ('Mode 1', 'Top 5')
            if tail and sub and re.match(r'^\d{1,2}$', tail[0]) and re.search(r'[A-Za-z]$', sub[-1]):
                sub.append(tail.pop(0))
            if tail and sub:
                nums = tail + nums
                fields[-1] = ' '.join(sub)
            break
    label = '  '.join(fields).strip()
    return label, nums


def header_info(line):
    """Return (label, cols, extras) or None. cols: ordered list of column ids, one per numeric
    token expected in a row: a date 'YYYY-MM-DD', 'PRIOR:date', 'FY:date' / 'FY:X:name' (annual block), or 'X:name'."""
    ds = list(DATE_RE.finditer(line))
    if len(ds) < 2:
        return None
    label = line[:ds[0].start()].strip()
    def xsplit(txt):
        out = []
        for e in re.split(r'\s{2,}', txt):
            if e:
                out += [x for x in re.split(r'\s(?=(?:YoY|QoQ|QOQ|YOY)\b)', e) if x and x not in ('YoY', 'QoQ', 'QOQ', 'YOY') or x]
        return [x for x in out if x]
    toks = []
    pos = ds[0].start()
    for k, m in enumerate(ds):
        between = line[pos:m.start()].strip()
        if between and k > 0:
            toks += [('x', e) for e in xsplit(between)]
        toks.append(('d', norm_date(*m.groups())))
        pos = m.end()
    tail = line[pos:].strip()
    toks += [('x', e) for e in xsplit(tail)]
    dseq = [v for t, v in toks if t == 'd']
    if all(t == 'd' for t, _ in toks[:len(dseq)]):
        for h in range(2, len(dseq) // 2 + 1):
            if len(dseq) % h == 0 and all(dseq[k] == dseq[k % h] for k in range(len(dseq))):
                # amount block followed by repeated blocks ('% of revenue', or $ block) with the same dates
                cols = [dseq[k] if k < h else f'BLK{k // h}:' + dseq[k] for k in range(len(dseq))]
                cols += ['X:' + v for t, v in toks[len(dseq):]]
                return label, cols, [v for t, v in toks if t == 'x']
    cols = []
    seen = {}
    annual = False
    last = None
    for idx, (t, v) in enumerate(toks):
        if t == 'd':
            if not annual and last is not None and v < last and v not in seen:
                # typo in a quarter header (e.g. '31-Mar-16' for '31-Mar-17' in Q2FY18): fix year if that restores order
                v2 = f"{int(v[:4]) + 1:04d}" + v[4:]
                if v2 > last:
                    print(f'header date fix: {v} -> {v2} in: {line.strip()[:90]}')
                    v = v2
            if v in seen and not annual:
                first = seen[v]
                if any(tt == 'x' for tt, _ in toks[first + 1:idx]) or (last is not None and last > v):
                    annual = True     # a second (year-ended) block starts
                else:
                    cols[first] = 'PRIOR:' + v   # adjacent duplicate: 'prior methodology' vs 'actuals'
            seen.setdefault(v, idx)
            cols.append(('FY:' if annual else '') + v)
            last = v
        else:
            cols.append(('FY:' if annual else '') + 'X:' + v)
    extras = [v for t, v in toks if t == 'x']
    return label, cols, extras


def extract(lines, doc):
    """Walk lines; every line with >=2 dates starts a table. Rows = label + numeric tokens."""
    cells = []
    n = len(lines)
    cur = None
    ctx = []          # all no-number lines since header (sub-headers such as 'Growth % (CC)')
    for i, ln in enumerate(lines):
        h = header_info(ln)
        if h:
            label, cols, extras = h
            if not label and i > 0 and not DATE_RE.search(lines[i - 1]):
                pf = [f for f in re.split(r'\s{2,}', lines[i - 1].strip()) if f]
                if pf:
                    label = pf[0]
                    if not extras:
                        extras = pf[1:]
                        cols = cols + ['X:' + e for e in extras]
            pre = ' | '.join(lines[max(0, i - 4):i])
            if re.search(r'Year Ended', pre, re.I) and not re.search(r'Quarter Ended', pre, re.I):
                cols = ['FY:' + c for c in cols]
            cur = dict(label=label, dates=cols, extras=extras, start=i, pre=pre)
            ctx = []
            continue
        if cur is None:
            continue
        if i - cur['start'] > 45 or re.match(r'^\s*-\s*\d+\s*-\s*$', ln) or ln.strip().startswith('#### PAGE'):
            cur = None
            continue
        label, nums = split_row(ln)
        if not nums:
            ctx.append(label)
            continue
        prev_label, prev_nums = split_row(lines[i - 1])
        prev_is_text = (not prev_nums) and not header_info(lines[i - 1])
        if not label or label in ('Services', 'Segments', 'Geography', 'Verticals'):
            parts = []
            if prev_is_text:
                parts.append(prev_label)
            if i + 1 < n:
                nl, nn = split_row(lines[i + 1])
                if not nn and len(nl) < 60 and not header_info(lines[i + 1]):
                    parts.append(nl)
            label = ' '.join(parts)
        elif prev_is_text and re.search(r'(,|&| and)$', prev_label.strip()):
            label = prev_label.strip() + ' ' + label
        nd = len([c for c in cur['dates'] if not c.startswith('X:') and not c.startswith('FY:X:')])
        base = dict(doc=doc, line=i + 1, hlabel=cur['label'], extras='|'.join(cur['extras']),
                    ctx='|'.join(ctx), pre=cur['pre'], row=label)
        if len(nums) < nd:
            cells.append(dict(base, col='__short__', raw=' '.join(nums)))
            continue
        allc = cur['dates']
        for j, tok in enumerate(nums):
            col = allc[j] if j < len(allc) else f'X:extra{j}'
            cells.append(dict(base, col=col, raw=tok))
    return cells


if __name__ == '__main__':
    import sys, csv
    base = sys.argv[1]
    out = []
    for sub in ('cond', 'ocr'):
        pass
