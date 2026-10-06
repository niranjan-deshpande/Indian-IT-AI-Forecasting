"""Extract TCS GFC-window (Q4FY07..Q4FY12) core metrics from local copies of TCS analyst presentations,
operating-metrics fact sheets and press releases (Wayback copies of tcs.com PDFs).

Inputs : data/sources/gfc/tcs/txt/*.txt (pdftotext -layout), data/sources/gfc/tcs/ocr/*.ocr.txt
         (macOS Vision OCR of image-only slides, via scripts/extract/gfc_tcs_ocr.swift),
         data/sources/gfc/tcs/_manifest.csv (archive/original URLs)
Output : data/sources/gfc/tcs/gfc_tcs_rows.csv (SCHEMA.md columns)

Parsing approach
- Segment share tables (Geography / IP Revenue = industry vertical / SP Revenue = service line) are
  parsed from the table header (period labels) + label rows.
- Revenue (INR, USD), growth, headcount, utilization, attrition are parsed by regex from the text and
  every value is asserted to appear verbatim in the source text.
- A few values that pdftotext garbled are hand-entered (HAND dict) and checked against the text.
"""
import csv, os, re, sys
from collections import OrderedDict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'data', 'sources', 'gfc', 'tcs')
OUT = os.path.join(SRC, 'gfc_tcs_rows.csv')
COLS = ['firm','fiscal_q','period_end','cal_q','metric','dimension','dim_type','value','unit','basis',
        'period_type','source_url','source_doc','source_loc','doc_date','notes']

QEND = {1: ('06-30', 2), 2: ('09-30', 3), 3: ('12-31', 4), 4: ('03-31', 1)}

def fq_info(q, fy):
    """q in 1..4, fy two-digit int -> (fiscal_q, period_end, cal_q)"""
    fy = int(fy)
    year = 2000 + fy if q == 4 else 2000 + fy - 1
    md, cq = QEND[q]
    return f"Q{q}FY{fy:02d}", f"{year}-{md}", f"{year}Q{cq}"

IN_SCOPE = lambda pe: '2007-01-01' <= pe <= '2012-03-31'

# ---------------------------------------------------------------- documents
manifest = {r['local']: r for r in csv.DictReader(open(os.path.join(SRC, '_manifest.csv')))}

DOC_DATES = {  # publication (results) dates as printed on the documents
 'Q4FY07': '2007-04-16', 'Q1FY08': '2007-07-16', 'Q2FY08': '2007-10-15', 'Q3FY08': '2008-01-16',
 'Q4FY08': '2008-04-21', 'Q1FY09': '2008-07-16', 'Q2FY09': '2008-10-22', 'Q3FY09': '2009-01-15',
 'Q4FY09': '2009-04-20', 'Q1FY10': '2009-07-17', 'Q2FY10': '2009-10-16', 'Q3FY10': '2010-01-15',
 'Q4FY10': '2010-04-19', 'Q1FY11': '2010-07-15', 'Q2FY11': '2010-10-21', 'Q3FY11': '2011-01-17',
 'Q4FY11': '2011-04-21', 'Q1FY12': '2011-07-14', 'Q2FY12': '2011-10-17', 'Q3FY12': '2012-01-17',
 'Q4FY12': '2012-04-23',
}

def load(local):
    b = local[:-4]
    t = open(os.path.join(SRC, 'txt', b + '.txt'), encoding='utf-8', errors='replace').read()
    o = os.path.join(SRC, 'ocr', b + '.ocr.txt')
    ocr = ''
    if os.path.exists(o):
        ocr = open(o, encoding='utf-8', errors='replace').read().replace(' | ', '    ')
    return t, ocr

rows = []
def add(docq, local, fq, pe, cq, metric, dim, dim_type, value, unit, basis, ptype, loc, notes='', doc_label=None):
    m = manifest[local]
    notes = (notes + '; ' if notes else '') + 'original URL: ' + m['original_url']
    rows.append(OrderedDict(zip(COLS, ['tcs', fq, pe, cq, metric, dim, dim_type, value, unit, basis, ptype,
        m['archive_url'], doc_label or DOCLABEL(local, docq), loc, DOC_DATES[docq], notes])))

def DOCLABEL(local, docq):
    if local.startswith('TCS_Analysts'): return f'TCS {docq} analyst presentation'
    if local.startswith('TCS_OperatingMetrics'): return f'TCS {docq} operating metrics (fact sheet)'
    if local.startswith('TCS_PR'): return f'TCS {docq} press release ({"US GAAP" if "USGAAP" in local else "IFRS"})'
    return local

def num(s):
    s = s.strip().replace(',', '').replace('%', '').replace(' ', '')
    neg = s.startswith('(') and s.endswith(')')
    s = s.strip('()')
    v = float(s)
    return -v if neg else v

def fmt(v):
    return ('%.4f' % v).rstrip('0').rstrip('.')

def verify(text, token):
    if token not in text:
        raise AssertionError(f'value token {token!r} not found in source text')

# ---------------------------------------------------------------- period tokens
PER = re.compile(r'(Q([1-4])\s*[- ]?\s*FY\s*(?:20)?(\d{2})(?!\d))|((?<![Q\d] )FY\s*(?:20)?(\d{2})(?!\d))')
def periods(s):
    out = []
    for m in PER.finditer(s):
        if m.group(1):
            out.append(('Q', int(m.group(2)), int(m.group(3))))
        else:
            out.append(('FY', None, int(m.group(5))))
    return out

NUMTOK = re.compile(r'^\(?-?[\d,]*\.?\d+\)?%?$')

# ---------------------------------------------------------------- segment tables
TABLES = [  # (keyword regex, dim_type, stop regex)
    (r'Geography \(%|Revenue by Geography', 'geography'),
    (r'IP Revenue \(%|Customer.s Industry', 'vertical'),
    (r'SP Revenue \(%|Service Offerings', 'service_line'),
]
GROUP_HDRS = {'Americas', 'Europe', 'IT Solutions and Services', 'Vertical / Domain'}
STOP = re.compile(r'^\s*(Total|Customer.s Industry|Contract Type|Client|Utili[sz]ation Rate|Employees|Growth in INR|Note:|\* For|Onsite)')

HEADER_OVERRIDE = {('TCS_Analysts_Q2FY08.pdf', 'geography'): [('Q', 2, 8), ('Q', 1, 8)]}  # 'Q1 FY08' printed one line above header

HAND = {}   # (doc local, dim_type, label) -> list of values  (pdftotext garbled rows; verified visually)
HAND[('TCS_Analysts_Q4FY07.pdf', 'service_line', 'Business Intelligence')] = [9.8, 9.5, 9.5, 8.5]
HAND[('TCS_Analysts_Q4FY07.pdf', 'service_line', 'Engineering & Industrial Services')] = [5.4, 5.4, 5.8, 6.6]
HAND[('TCS_Analysts_Q1FY08.pdf', 'vertical', 'Life Sciences & Healthcare')] = [6.1, 6.2]
HAND[('TCS_Analysts_Q2FY08.pdf', 'vertical', 'Manufacturing')] = [12.7, 12.4]
HAND[('TCS_Analysts_Q2FY08.pdf', 'vertical', 'Retail & Distribution')] = [7.6, 8.0]
HAND[('TCS_Analysts_Q2FY08.pdf', 'service_line', 'Enterprise Solutions')] = [12.8, 12.4]
HAND[('TCS_Analysts_Q2FY08.pdf', 'service_line', 'Assurance Services')] = [3.8, 3.3]
HAND[('TCS_Analysts_Q4FY08.pdf', 'service_line', 'Enterprise Solutions')] = [13.7, 13.2, 13.1, 12.2]
HAND[('TCS_Analysts_Q4FY08.pdf', 'service_line', 'Assurance Services')] = [4.2, 4.0, 3.8, 2.3]
HAND[('TCS_Analysts_Q4FY08.pdf', 'service_line', 'Engineering & Industrial Services')] = [5.3, 5.3, 5.4, 5.8]
HAND[('TCS_Analysts_Q4FY08.pdf', 'service_line', 'Infrastructure Services')] = [6.7, 6.7, 6.5, 6.0]

import subprocess
_RAW = {}
def verify_hand(local, label, vals):
    """HAND rows: check 'label v1 v2 ..' appears in pdftotext -raw output (column order preserved there)."""
    if local not in _RAW:
        _RAW[local] = subprocess.run(['pdftotext', '-raw', os.path.join(SRC, local), '-'], capture_output=True, text=True).stdout
    raw = ' '.join(_RAW[local].split())
    tok = label + ' ' + ' '.join(('%.1f' % v) for v in vals)
    if tok not in raw:
        raise AssertionError('HAND row not found in -raw text: ' + tok)

def parse_tables(local, docq, text):
    lines = text.split('\n')
    for kw, dtype in TABLES:
        for i, ln in enumerate(lines):
            mk = re.search(kw, ln)
            if not mk: continue
            # header: this line (from keyword on) or one of next 2 lines with >=2 period tokens
            hdr_idx, per = None, []
            for j in range(i, min(i + 3, len(lines))):
                seg = lines[j][mk.start():] if j == i else lines[j]
                p = periods(seg)
                if len(p) >= 2:
                    hdr_idx, per = j, p; break
            if hdr_idx is None and (local, dtype) in HEADER_OVERRIDE:
                hdr_idx, per = i, HEADER_OVERRIDE[(local, dtype)]
            if hdr_idx is None:
                print('WARN no header', local, dtype, ln.strip()[:60]); continue
            growth_fmt = any('Q-o-Q' in lines[k] for k in range(max(0, hdr_idx - 2), hdr_idx + 1))
            col_x = mk.start()
            k = hdr_idx + 1; blank = 0; seen = 0
            while k < len(lines) and blank < 4:
                raw = lines[k]; k += 1
                s = raw.strip()
                if not s: blank += 1; continue
                blank = 0
                if STOP.match(s) and seen: break
                if 'Growth' == s or s.startswith('Growth '): continue
                # restrict to table columns: drop text left of the table start if pie labels precede it
                cut = raw[max(0, col_x - 25):] if col_x > 40 else raw
                tk = [(mm.group(0), mm.start(), mm.end()) for mm in re.finditer(r'\S+', cut)]
                toks = [t[0] for t in tk]
                t0 = 0
                while t0 < len(toks) and NUMTOK.match(toks[t0]): t0 += 1   # pie-chart labels left of table
                t1 = t0
                while t1 < len(toks) and not NUMTOK.match(toks[t1]): t1 += 1
                if t1 == t0 or t1 >= len(toks) and False: continue
                # label = words immediately left of the first number, separated by single spaces (drops legend text)
                l0 = t1 - 1
                while l0 - 1 >= t0 and tk[l0][1] - tk[l0 - 1][2] == 1: l0 -= 1
                if l0 < t0 or not re.match(r'[A-Za-z]', toks[l0]): continue
                label = ' '.join(toks[l0:t1])
                if label == 'Total': break
                if label in GROUP_HDRS: continue
                vals = []
                for t in toks[t1:]:
                    if NUMTOK.match(t): vals.append(t)
                    else: break
                key = (local, dtype, label)
                if key in HAND:
                    verify_hand(local, label, HAND[key])
                    vals = [str(v) for v in HAND[key]]
                if not vals: continue
                seen += 1
                emit_row(local, docq, dtype, label, per, vals, growth_fmt, text, lines[hdr_idx].strip())
            break  # only first occurrence of each table

def emit_row(local, docq, dtype, label, per, vals, growth_fmt, text, hdr):
    n, kper = len(vals), len(per)
    if growth_fmt:
        # layout: P0 P1 QoQ P2 [P3] YoY
        if n != kper + 2:
            print('WARN growth-format mismatch', local, dtype, label, per, vals); return
        seq = [per[0], per[1], 'QOQ'] + per[2:] + ['YOY']
    else:
        if n > kper and n <= kper + 2 and not any(x[0] == 'FY' for x in per):
            print('NOTE truncating trailing commentary numbers', local, dtype, label, vals[kper:])
            vals = vals[:kper]; n = kper
        if n != kper:
            print('WARN col mismatch', local, dtype, label, per, vals); return
        seq = per
    loc = {'geography': 'Growth by Market / Geography table', 'vertical': 'Growth by Domain / IP Revenue (%) table',
           'service_line': 'Growth by Service Line / SP Revenue (%) table'}[dtype]
    if local.startswith('TCS_OperatingMetrics'):
        loc = {'geography': 'Revenue by Geography', 'vertical': "Customer's Industry", 'service_line': 'Service Offerings'}[dtype]
    for p, v in zip(seq, vals):
        if (local, dtype, label) not in HAND:
            verify(text, v)
        if p == 'QOQ' or p == 'YOY':
            q0 = per[0]
            fq, pe, cq = fq_info(q0[1], q0[2])
            if not IN_SCOPE(pe): continue
            annual = (p == 'YOY' and any(x[0] == 'FY' for x in per))
            if annual:
                fyl = [x for x in per if x[0] == 'FY'][0]
                fq, pe, cq = f'FY{fyl[2]:02d}', f'20{fyl[2]:02d}-03-31', f'20{fyl[2]:02d}Q1'
            add(docq, local, fq, pe, cq, 'segment_growth_qoq' if p == 'QOQ' else 'segment_growth_yoy', label, dtype,
                fmt(num(v)), 'pct', 'reported', 'annual' if annual else 'quarter', loc,
                'growth in INR terms as reported' + ('; FY (annual) Y-o-Y growth' if annual else ''))
            continue
        if p[0] == 'FY':
            continue  # annual shares not collected
        fq, pe, cq = fq_info(p[1], p[2])
        if not IN_SCOPE(pe): continue
        note = ''
        if dtype == 'vertical' and local.startswith('TCS_Analysts'): note = 'IP = industry practice'
        if dtype == 'service_line' and local.startswith('TCS_Analysts'): note = 'SP = service practice'
        add(docq, local, fq, pe, cq, 'revenue_share', label, dtype, fmt(num(v)), 'pct', 'reported', 'quarter', loc, note)

# ---------------------------------------------------------------- revenue
def parse_revenue(local, docq, text, ocr):
    full = text + '\n' + ocr
    lines = full.split('\n')
    # (a) INR revenue + INR growth from "US GAAP Revenue Growth" / "Total Revenue" table (3 quarterly cols)
    for i, ln in enumerate(lines):
        m = re.match(r'^\s*Total Revenue\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s*$', ln)
        if not m: continue
        # find header above
        per = None
        for j in range(i - 1, max(0, i - 12), -1):
            p = periods(lines[j])
            if len(p) >= 3 and all(x[0] == 'Q' for x in p[:3]) and ('INR' in lines[j] or 'Rs' in lines[j]):
                per = p[:3]; break
        if not per: continue
        for p, v in zip(per, m.groups()):
            fq, pe, cq = fq_info(p[1], p[2])
            if IN_SCOPE(pe):
                add(docq, local, fq, pe, cq, 'revenue', 'total', 'total', fmt(num(v)), 'INR_mn', 'reported', 'quarter',
                    'US GAAP Revenue Growth (quarterly) table - Total Revenue' + (' [OCR of image slide]' if ln in ocr else ''), 'consolidated US GAAP, INR million')
        # growth lines follow Total Revenue
        for j in range(i + 1, min(i + 4, len(lines))):
            g = re.match(r'^\s*% Growth (Q-[o0]-Q|Y-[o0]-Y)\s+(-?[\d.]+)%', lines[j])
            if g:
                fq, pe, cq = fq_info(per[0][1], per[0][2])
                if IN_SCOPE(pe):
                    add(docq, local, fq, pe, cq, 'revenue_growth_qoq' if g.group(1).startswith('Q') else 'revenue_growth_yoy',
                        'total', 'total', g.group(2), 'pct', 'reported', 'quarter',
                        'US GAAP Revenue Growth (quarterly) table' + (' [OCR of image slide]' if ln in ocr else ''), 'INR terms: revenue growth of consolidated US GAAP INR revenue')
        break
    # (b) quarterly income statement "Revenue" rows: [USD_conv] INR/USD cur, prev-Q, year-ago-Q, then 100.00 x3
    done = set()
    have_inr = {r['fiscal_q'] for r in rows if r['metric'] == 'revenue' and r['unit'] == 'INR_mn'
                and r['source_url'] == manifest[local]['archive_url']}
    for i, ln in enumerate(lines):
        m = re.match(r'^\s*Revenue\s+(.*)$', ln)
        if not m: continue
        toks = [t for t in m.group(1).split()]
        if not toks or not all(NUMTOK.match(t) for t in toks): continue
        if len(toks) == 7 and toks[4:] == ['100.00'] * 3: layout = 'conv'
        elif len(toks) == 6 and toks[3:] == ['100.00'] * 3: layout = 'q3'
        else: continue
        per, ctx = None, ''
        for j in range(i - 1, max(0, i - 6), -1):
            ctx = lines[j] + '\n' + ctx
            p = [x for x in periods(lines[j]) if x[0] == 'Q']
            if len(p) >= 3 and per is None: per = p[:3]
        if not per: continue
        ctx_wide = '\n'.join(lines[max(0, i - 8):i])
        gaap = 'IFRS' if 'IFRS' in ctx_wide else 'US GAAP'
        from_ocr = ln in ocr
        if layout == 'conv':
            fq, pe, cq = fq_info(per[0][1], per[0][2])
            tail = full[full.find(ln): full.find(ln) + 4000]
            rate = re.search(r'convenience translation basis @ Rupees ([\d.]+)', tail)
            if IN_SCOPE(pe) and ('conv', fq) not in done:
                done.add(('conv', fq))
                add(docq, local, fq, pe, cq, 'revenue', 'total', 'total', fmt(num(toks[0])), 'USD_mn', 'reported', 'quarter',
                    'US GAAP Income Statement - Quarterly (USD Millions column)',
                    'USD is a convenience translation of INR revenue at the period-end rate Rs %s/USD stated in the document, not average-rate USD revenue' % (rate.group(1) if rate else '?'))
            vals, usd = toks[1:4], False
        else:
            vals = toks[:3]
            usd = bool(re.search(r'USD|\$ Million', ctx))
        kind = 'USD' if usd else 'INR'
        if kind in done: continue
        done.add(kind)
        for p, v in zip(per, vals):
            fq, pe, cq = fq_info(p[1], p[2])
            if not IN_SCOPE(pe): continue
            if kind == 'INR' and fq in have_inr: continue
            add(docq, local, fq, pe, cq, 'revenue', 'total', 'total', fmt(num(v)), 'USD_mn' if usd else 'INR_mn', 'reported', 'quarter',
                f'{gaap} Income Statement - Quarterly' + (' in USD' if usd else ' (INR million)') + (' [OCR of image slide]' if from_ocr else ''),
                f'consolidated {gaap}' + ('; USD revenue as reported by TCS' if usd else ', INR million'))

# ---------------------------------------------------------------- HR
def parse_hr(local, docq, text, ocr):
    full = text + '\n' + ocr
    q = re.match(r'Q(\d)FY(\d\d)', docq)
    fq, pe, cq = fq_info(int(q.group(1)), int(q.group(2)))
    loc = 'Human Resources slides'
    # headcount (consolidated / headline)
    hc = None
    cands = []
    for pat in [r'Largest (?:IT|Private) Employer in India\s*:\s*([\d,]+)\s*employees',
                r'Total Employee Base\s*:\s*([\d,]+)', r'Total Employees\s*:\s*([\d, ]+\d)',
                r'TCS Employees\s*:\s*([\d,]+)\s*\(consolidated\)', r'Employee Base\s*:\s*([\d,]+)',
                r'TCS Consolidated\s*:\s*([\d,]+)']:
        for m in re.finditer(pat, full):
            cands.append(m.group(1))
    if cands:  # headline = largest employee count quoted on the HR slides (smaller ones are e.g. BPO-unit counts)
        hc = max(cands, key=lambda x: int(x.replace(',', '').replace(' ', '')))
    if hc:
        verify(full, hc)
        v = hc.replace(' ', '')
        if pe < '2009-03-31':
            note = 'Total employees = TCS (incl. overseas branches & subsidiaries, GDCs) + Indian subsidiaries (CMC, WTI); excludes TCS e-Serve (acquired Dec-2008)'
        elif pe < '2011-03-31':
            note = 'Total employee base = TCS Ltd + subsidiaries (CMC, WTI, TCS e-Serve, Diligenta & others); from Q4FY09 e-Serve and Diligenta shown under subsidiaries'
        else:
            note = 'Consolidated headcount (incl. subsidiaries CMC, e-Serve & Diligenta)'
        add(docq, local, fq, pe, cq, 'headcount', 'total', 'total', v.replace(',', ''), 'count', 'na', 'point', loc, note)
    # excl subsidiaries
    m = re.search(r'TCS Employees\s*:\s*([\d,]+)\s*(?!\s*\(consolidated)', full)
    m_old = re.search(r'^\s*\S?\s*TCS\s*:\s*([\d,]+)', full, re.M) or re.search(r'No\. of TCS Employees\s*:\s*([\d,]+)', full)
    if pe >= '2009-03-31' and m and '(consolidated)' not in full[m.start():m.end() + 20]:
        add(docq, local, fq, pe, cq, 'headcount', 'TCS excl. subsidiaries (CMC, WTI, e-Serve, Diligenta & others)', 'other',
            m.group(1).replace(',', ''), 'count', 'na', 'point', loc, 'TCS Ltd employees incl. overseas branches & GDCs; excludes listed subsidiaries')
    elif pe < '2009-03-31' and m_old:
        add(docq, local, fq, pe, cq, 'headcount', 'TCS excl. Indian subsidiaries (CMC, WTI)', 'other',
            m_old.group(1).replace(',', ''), 'count', 'na', 'point', loc,
            'TCS incl. overseas subsidiaries & branches and GDCs; excludes Indian subsidiaries' + ('; excludes 12,459 TCS e-Serve employees' if 'e-Serve employees' in full else ''))
    # utilization
    ex = inc = None
    mu = re.search(r'Utili[sz]ation Rate', full)
    if mu:
        win = full[mu.start(): mu.start() + 700]
        m1 = re.search(r'([\d.]+)\s*%\s*\(excluding trainees\)', win, re.I)
        m2 = re.search(r'([\d.]+)\s*%\s*\(including trainees\)', win, re.I)
        if m1 and m2: ex, inc = m1.group(1), m2.group(1)
    if ex:
        note = 'TCS excluding subsidiaries (CMC, e-Serve & Diligenta)' if pe >= '2011-03-31' else 'as reported in HR slide (TCS; basis not further specified)'
        add(docq, local, fq, pe, cq, 'utilization_excl_trainees', 'total', 'total', ex, 'pct', 'na', 'quarter', loc, note)
        add(docq, local, fq, pe, cq, 'utilization_incl_trainees', 'total', 'total', inc, 'pct', 'na', 'quarter', loc, note)
    else:
        print('WARN no utilization', local)
    # attrition
    sub = ' (excluding subsidiaries CMC, e-Serve & Diligenta)' if pe >= '2011-03-31' else ''
    tot = None
    for ma in re.finditer(r'Attrition', full):
        win = full[ma.start(): ma.start() + 400]
        mt = re.search(r'(?:was\s*)?([\d.]+)\s*%\s*(?:\(LTM\))?,?\s*including\s*BPO', win) or \
             re.search(r'Last Twelve Months \(LTM\) was\s*([\d.]+)%', win)
        if mt:
            tot = mt.group(1); break
    if tot:
        add(docq, local, fq, pe, cq, 'attrition', 'total', 'total', tot, 'pct', 'na', 'ltm', loc, 'LTM attrition including BPO' + sub)
    else:
        print('WARN no total attrition', local)
    m = re.search(r'IT (?:Services|Attrition)(?: was)?\s*:?\s*([\d.]+)\s*%\s*\(LTM\)', full)
    if m:
        add(docq, local, fq, pe, cq, 'attrition', 'IT Services', 'other', m.group(1), 'pct', 'na', 'ltm', loc, 'LTM attrition, IT services' + sub)
    m = re.search(r'BPO(?: Attrition was)?\s*:?\s*([\d.]+)\s*%\s*\(LTM\)', full)
    if m:
        add(docq, local, fq, pe, cq, 'attrition', 'BPO', 'other', m.group(1), 'pct', 'na', 'ltm', loc, 'LTM attrition, BPO' + sub)

# ---------------------------------------------------------------- op-metrics fact sheets: HR block
def parse_opm_hr(local, docq, text):
    lines = text.split('\n')
    hdr = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith('Utilization Rate') or ln.strip().startswith('Employees'):
            per = periods(ln)
            if len(per) == 3: hdr = per
        def grab(prefix):
            return re.match(r'^\s*' + prefix + r'\s+([\d.,]+%?)\s+([\d.,]+%?)\s+([\d.,]+%?)\s*$', ln)
        spec = [('Including Trainees', 'utilization_incl_trainees', 'total', 'total', 'pct', 'quarter', 'Utilization Rate', ''),
                ('Excluding Trainees', 'utilization_excl_trainees', 'total', 'total', 'pct', 'quarter', 'Utilization Rate', ''),
                ('Attrition Rate', 'attrition', 'total', 'total', 'pct', 'ltm', 'Employees', 'attrition rate as reported (LTM, including BPO per analyst presentation)')]
        for pre, met, dim, dt, unit, pt, sloc, note in spec:
            m = grab(pre)
            if m and hdr:
                for p, v in zip(hdr, m.groups()):
                    fq, pe, cq = fq_info(p[1], p[2])
                    if IN_SCOPE(pe):
                        add(docq, local, fq, pe, cq, met, dim, dt, v.rstrip('%'), unit, 'na', pt, sloc, note)
        m = re.match(r'^\s*\(End of the Period\)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)', ln)
        if m and hdr:
            prev = lines[i - 1]
            if 'including' in prev:
                met_dim, dt, note = 'total', 'total', prev.strip().rstrip('^') + ' (End of the Period)' + ('; subsidiaries = CMC, WTI, TCS eServe, Diligenta and Others' if 'Indian' not in prev else '')
            else:
                if 'Indian' in prev:
                    met_dim, dt, note = 'TCS excl. Indian subsidiaries (CMC, WTI)', 'other', 'Total Number of Employees excluding Indian Subsidiaries (End of the Period)'
                else:
                    met_dim, dt = 'TCS excl. subsidiaries (CMC, WTI, e-Serve, Diligenta & others)', 'other'
                    note = prev.strip().rstrip('^') + ' (End of the Period)' + ('; subsidiaries = CMC, WTI, TCS eServe, Diligenta and Others; Q1FY09 column equals the earlier figure that excluded only Indian subsidiaries' if docq == 'Q1FY10' else '')
            for p, v in zip(hdr, m.groups()):
                fq, pe, cq = fq_info(p[1], p[2])
                if IN_SCOPE(pe):
                    add(docq, local, fq, pe, cq, 'headcount', met_dim, dt, v.replace(',', ''), 'count', 'na', 'point', 'Employees', note)

# ---------------------------------------------------------------- subcontracting (IFRS FY12 decks)
def parse_subcon(local, docq, text, ocr):
    full = text + '\n' + ocr
    lines = full.split('\n')
    seen = set()
    for i, ln in enumerate(lines):
        m = re.match(r'^\s*Fees to external cons\s?ultants\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+[\d.]+', ln)
        if not m: continue
        per, unit_line, block = None, '', ''
        for j in range(i - 1, max(0, i - 6), -1):
            p = periods(lines[j])
            if len(p) >= 3 and not per: per = p[:3]
            if re.search(r'COR|S\s?G\s?&\s?A', lines[j]) and not block: block = 'COR' if re.search(r'\bCOR\b', lines[j]) and not re.search(r'S\s?G\s?&\s?A', lines[j]) else 'SG&A'
            unit_line += lines[j]
        # determine unit: look further up for "In USD"/"$ Million"
        ctx = '\n'.join(lines[max(0, i - 16):i])
        usd = bool(re.search(r'In USD|\$ Million|USD Million', ctx))
        if not per or not block: continue
        key = (block, usd)
        if key in seen: continue
        seen.add(key)
        for p, v in zip(per, m.groups()):
            fq, pe, cq = fq_info(p[1], p[2])
            if IN_SCOPE(pe):
                add(docq, local, fq, pe, cq, 'subcontracting_cost', f'Fees to external consultants ({block})', 'other',
                    v.replace(',', ''), 'USD_mn' if usd else 'INR_mn', 'reported', 'quarter',
                    f'COR - SG&A Details{" - In USD" if usd else ""} (IFRS)',
                    'IFRS line "Fees to external consultants" (subcontractor proxy); COR and SG&A components recorded separately, not summed')

# ---------------------------------------------------------------- press releases (hand-verified tokens)
# (doc local, fiscal quarter of statement, metric, value, unit, basis, exact source token)
PR = [
 ('TCS_PR_USGAAP_Q4FY07.pdf', 'Q4FY07', 'revenue_growth_qoq', '8', 'pct', 'reported', 'Total Revenues at US $ 1.2 billion; up 8% Q-on-Q', 'USD terms (convenience-translated USD); rounded'),
 ('TCS_PR_USGAAP_Q2FY08.pdf', 'Q2FY08', 'revenue_growth_yoy', '45.2', 'pct', 'reported', 'Q2 Revenues at $ 1.42b; up 45.2% Y-o-Y, up 10.8% Q-o-Q', 'USD terms'),
 ('TCS_PR_USGAAP_Q2FY08.pdf', 'Q2FY08', 'revenue_growth_qoq', '10.8', 'pct', 'reported', 'Q2 Revenues at $ 1.42b; up 45.2% Y-o-Y, up 10.8% Q-o-Q', 'USD terms'),
 ('TCS_PR_USGAAP_Q3FY09.pdf', 'Q3FY09', 'revenue', '1483', 'USD_mn', 'reported', 'Revenues at $1,483 million flat Y-o-Y; (5.8%) Q-o-Q', 'US GAAP'),
 ('TCS_PR_USGAAP_Q3FY09.pdf', 'Q3FY09', 'revenue_growth_qoq', '-5.8', 'pct', 'reported', 'Revenues at $1,483 million flat Y-o-Y; (5.8%) Q-o-Q', 'USD terms; Y-o-Y described as "flat"'),
 ('TCS_PR_USGAAP_Q1FY10.pdf', 'Q1FY10', 'revenue_growth_qoq', '3', 'pct', 'reported', 'Q1 Revenues at $1.48 billion, up 3 % Q-o-Q', 'USD terms; rounded'),
 ('TCS_PR_USGAAP_Q3FY10.pdf', 'Q3FY10', 'revenue_growth_yoy', '10.3', 'pct', 'reported', 'Q3 Revenues at $1.64 billion; up 10.3% Y-o-Y; up 6.3% Q-o-Q', 'USD terms'),
 ('TCS_PR_USGAAP_Q3FY10.pdf', 'Q3FY10', 'revenue_growth_qoq', '6.3', 'pct', 'reported', 'Q3 Revenues at $1.64 billion; up 10.3% Y-o-Y; up 6.3% Q-o-Q', 'USD terms'),
 ('TCS_PR_USGAAP_Q4FY10.pdf', 'Q4FY10', 'revenue', '1686', 'USD_mn', 'reported', 'Q4 Revenues at $1,686 m', 'US GAAP'),
 ('TCS_PR_USGAAP_Q4FY10.pdf', 'Q4FY10', 'revenue_growth_yoy', '17.61', 'pct', 'reported', 'up 17.61% Y-on-Y and 3.07% Q-on-Q', 'USD terms'),
 ('TCS_PR_USGAAP_Q4FY10.pdf', 'Q4FY10', 'revenue_growth_qoq', '3.07', 'pct', 'reported', 'up 17.61% Y-on-Y and 3.07% Q-on-Q', 'USD terms'),
 ('TCS_PR_USGAAP_Q1FY11.pdf', 'Q1FY11', 'revenue', '1794', 'USD_mn', 'reported', 'Revenues at $1,794 million up 6.4% sequentially;', 'US GAAP'),
 ('TCS_PR_USGAAP_Q1FY11.pdf', 'Q1FY11', 'revenue_growth_qoq', '6.4', 'pct', 'reported', 'Revenues at $1,794 million up 6.4% sequentially;', 'USD terms'),
 ('TCS_PR_USGAAP_Q1FY11.pdf', 'Q1FY11', 'revenue_growth_yoy', '21.2', 'pct', 'reported', 'up 21.2% Y-o-Y', 'USD terms'),
 ('TCS_PR_USGAAP_Q2FY11.pdf', 'Q2FY11', 'revenue_growth_qoq', '12', 'pct', 'reported', 'up 12% Q-o-Q, 30% Y-o-Y', 'USD terms; rounded'),
 ('TCS_PR_USGAAP_Q2FY11.pdf', 'Q2FY11', 'revenue_growth_yoy', '30', 'pct', 'reported', 'up 12% Q-o-Q, 30% Y-o-Y', 'USD terms; rounded'),
 ('TCS_PR_USGAAP_Q3FY11.pdf', 'Q3FY11', 'revenue_growth_qoq', '7', 'pct', 'reported', 'up 7% Q-o-Q, 31.1% Y-o-Y', 'USD terms; rounded'),
 ('TCS_PR_USGAAP_Q3FY11.pdf', 'Q3FY11', 'revenue_growth_yoy', '31.1', 'pct', 'reported', 'up 7% Q-o-Q, 31.1% Y-o-Y', 'USD terms'),
 ('TCS_PR_USGAAP_Q4FY11.pdf', 'Q4FY11', 'revenue_growth_yoy', '33.2', 'pct', 'reported', 'Q4 Revenues at $2.2 billion up 33.2% Y-o-Y & 4.7% Q-o-Q', 'USD terms'),
 ('TCS_PR_USGAAP_Q4FY11.pdf', 'Q4FY11', 'revenue_growth_qoq', '4.7', 'pct', 'reported', 'Q4 Revenues at $2.2 billion up 33.2% Y-o-Y & 4.7% Q-o-Q', 'USD terms'),
 ('TCS_PR_IFRS_Q1FY12.pdf', 'Q1FY12', 'revenue_growth_yoy', '34.4', 'pct', 'reported', 'Revenues at $ 2.41 billion up 34.4% Y-o-Y', 'USD terms (IFRS)'),
 ('TCS_PR_IFRS_Q2FY12.pdf', 'Q2FY12', 'revenue_growth_yoy', '26', 'pct', 'reported', 'Q2 Revenues to $2.52 b up 26% Y-o-Y', 'USD terms (IFRS); rounded'),
 ('TCS_PR_IFRS_USD_Q4FY12.pdf', 'Q4FY12', 'revenue_growth_qoq', '2.4', 'pct', 'reported', 'Q4 Revenues at $ 2.64 billion up 2.4%', 'USD terms (IFRS); stated as "up 2.4%" alongside Q4 revenue, sequential per analyst deck'),
]
# constant-currency growth (analyst presentations, highlights slide)
CC = [
 ('TCS_Analysts_Q3FY12.pdf', 'Q3FY12', 'revenue_growth_qoq', '4.5', 'Constant currency revenue growth of 4.5%, volume growth of 3.2% QoQ'),
 ('TCS_Analysts_Q4FY12.pdf', 'Q4FY12', 'revenue_growth_qoq', '2.3', 'Constant currency revenue growth of 2.3%, volume growth of 3.3% Q-o-Q'),
]

def main():
    for local in sorted(manifest):
        if manifest[local]['ok'] != 'True': continue
        docq = re.search(r'(Q\dFY\d\d)', local).group(1)
        text, ocr = load(local)
        if local.startswith('TCS_Analysts'):
            parse_tables(local, docq, text)
            parse_revenue(local, docq, text, ocr)
            parse_hr(local, docq, text, ocr)
            parse_subcon(local, docq, text, ocr)
        elif local.startswith('TCS_OperatingMetrics'):
            parse_tables(local, docq, text)
            parse_opm_hr(local, docq, text)
    for local, docq, met, v, unit, basis, tok, note in PR:
        text, _ = load(local)
        verify(' '.join(text.split()), ' '.join(tok.split()))
        q = re.match(r'Q(\d)FY(\d\d)', docq); fq, pe, cq = fq_info(int(q.group(1)), int(q.group(2)))
        add(docq, local, fq, pe, cq, met, 'total', 'total', v, unit, basis, 'quarter', 'Highlights (first page)',
            note + '; hand-entered from press release text (verified by exact-string match); quoted: "' + ' '.join(tok.split()) + '"')
    for local, docq, met, v, tok in CC:
        text, _ = load(local)
        verify(' '.join(text.split()), tok)
        q = re.match(r'Q(\d)FY(\d\d)', docq); fq, pe, cq = fq_info(int(q.group(1)), int(q.group(2)))
        add(docq, local, fq, pe, cq, met, 'total', 'total', v, 'pct', 'cc', 'quarter', 'Quarter highlights slide',
            'constant currency Q-o-Q revenue growth as stated')
    # de-duplicate identical rows
    seen, out = set(), []
    for r in rows:
        k = tuple(r[c] for c in COLS if c != 'notes')
        if k in seen: continue
        seen.add(k); out.append(r)
    out.sort(key=lambda r: (r['period_end'], r['metric'], r['dim_type'], r['dimension'], r['doc_date']))
    with open(OUT, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(out)
    print('rows', len(out))

if __name__ == '__main__':
    main()
