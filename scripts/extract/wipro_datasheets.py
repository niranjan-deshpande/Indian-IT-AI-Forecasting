"""Parse Wipro quarterly analyst datasheets (pdftotext -layout output) into schema rows.

Input : data/sources/wipro/txt/*data*sheet*.txt  (created with `pdftotext -layout`)
Output: data/sources/wipro/parsed_datasheets.csv  (merged into data/raw/wipro.csv by wipro_build.py)

Approach: every datasheet table has a column header line made only of Q1..Q4/FY tokens
(current FY quarters descending, prior FY total, prior-year quarters descending). Numbers are
assigned to the nearest header column by character position. Annual (FY) columns are skipped.
The "Growth Metrics" table (Reported QoQ, Reported YoY, CC QoQ, CC YoY) is parsed separately.
"""
import re, os, csv, glob, sys

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
SRC = os.path.join(ROOT, 'data', 'sources', 'wipro')
TXT = os.path.join(SRC, 'txt')

NUM = re.compile(r'^\(?[-−–]?\$?\d[\d,]*\.?\d*%?\)?$')

def fy_q_from_name(fn):
    # e.g. 2015-2016_q1_11322-Data-Sheet-Q1-FY-16.txt ; 2020-2021_q1fy20_analyst-data-sheet-q1-fy21.txt
    m = re.match(r'(\d{4})-(\d{4})_([A-Za-z0-9]+)_', fn)
    fy = int(m.group(2)) % 100
    q = int(re.search(r'[qQ](\d)', m.group(3)).group(1))
    return fy, q

def period_end(fy, q):
    y = 2000 + fy
    return {1: f'{y-1}-06-30', 2: f'{y-1}-09-30', 3: f'{y-1}-12-31', 4: f'{y}-03-31'}[q]

def cal_q(fy, q):
    y = 2000 + fy
    return {1: f'{y-1}Q2', 2: f'{y-1}Q3', 3: f'{y-1}Q4', 4: f'{y}Q1'}[q]

def chunks(line):
    """split on 2+ spaces, return list of (start, end, text)"""
    out = []
    for m in re.finditer(r'\S+(?: \S+)*', line):
        out.append((m.start(), m.end(), m.group(0)))
    return out

def split_line(line):
    """returns label_chunks [(s,e,text)], value_tokens [(center, text)]"""
    labels, vals = [], []
    for s, e, t in chunks(line):
        parts = t.split(' ')
        if all(NUM.match(p) or p in ('-', '—') for p in parts):
            pos = s
            for p in parts:
                c = pos + len(p) / 2.0
                vals.append((c, p))
                pos += len(p) + 1
        else:
            labels.append((s, e, t))
    return labels, vals

def to_num(t):
    if t in ('-', '—'):
        return None
    neg = t.startswith('(') and t.endswith(')')
    t2 = t.strip('()').replace('$', '').replace(',', '').replace('%', '').replace('−', '-').replace('–', '-')
    try:
        v = float(t2)
    except ValueError:
        return None
    return -v if neg else v

HEADER = re.compile(r'^\s*((Q[1-4]|FY)\s+){4,}(Q[1-4]|FY)\s*$')

def parse_header(line, cur_fy):
    toks = [(m.start() + len(m.group(0)) / 2.0, m.group(0)) for m in re.finditer(r'Q[1-4]|FY', line)]
    cols = []
    year = cur_fy
    last_q = None
    first = True
    for c, t in toks:
        if t == 'FY':
            if first:
                fyear = cur_fy
            else:
                fyear = year - 1
            year = fyear
            last_q = 5
            cols.append((c, None, f'FY{fyear}'))
        else:
            n = int(t[1])
            if last_q is not None and n >= last_q:
                year -= 1
            last_q = n
            cols.append((c, (year, n), f'Q{n}FY{year:02d}'))
        first = False
    return cols

def clean_label(t):
    t = re.sub(r'\s*Note\s*[\d&,\s]*$', '', t)
    t = re.sub(r'Note\s*\d(\s*&\s*\d)?', '', t)
    t = t.replace('—', '-').replace('—', '-').strip(' *^@#')
    t = re.sub(r'\*+$', '', t).strip()
    return t

SEC_PATTERNS = [
    (re.compile(r'Practices|Service Line|Global Business Lines', re.I), 'service_line'),
    (re.compile(r'Strategic Business Units|SBU Mix|^Verticals|^Sectors|Industry Verticals', re.I), 'vertical'),
    (re.compile(r'^Geograph|Strategic Market Units', re.I), 'geography'),
]
SIDE = {'mix', 'service line', 'service', 'sbu mix', 'geography', 'geograph', 'y mix', 'revenue &',
        'revenue & om %', 'revenue & om', 'om%', 'om %', 'delivery', 'customer', 'relationships',
        'customer metrics', 'employee metrics', 'currency mix', 'guidance', 'service line mix',
        'service delivery', 'customer relationships'}

# (regex on label, metric, dimension, dim_type, unit, basis, period_type, note)
TABLE_METRICS = [
    (r'^IT Serv\s?ices Revenues.*Earlier Segment', 'revenue', 'IT Services (earlier segment definition)', 'other', 'USD_mn', 'reported', 'quarter', 'IT Services revenue per segment definition before ISRE carve-out (shown for continuity in Q3FY19-era datasheets)'),
    (r'^IT Serv\s?ices Revenues', 'revenue', 'IT Services', 'other', 'USD_mn', 'reported', 'quarter', 'IT Services segment revenue (USD mn)'),
    (r'^Sequential Growth in Constant Currency', 'revenue_growth_qoq', 'IT Services', 'other', 'pct', 'cc', 'quarter', 'IT Services sequential growth, constant currency'),
    (r'^Sequential Growth$', 'revenue_growth_qoq', 'IT Services', 'other', 'pct', 'reported', 'quarter', 'IT Services sequential growth, reported USD'),
    (r'^> ?\$', 'clients_bucket', None, 'client_bucket', 'count', 'na', 'ltm', 'Number of customers by TTM revenue bucket (IT Services)'),
    (r'Total Number of active customers|^customers$', 'active_clients', 'total', 'total', 'count', 'na', 'point', 'Total number of active customers (IT Services)'),
    (r'Number of new customers', 'new_clients', 'total', 'total', 'count', 'na', 'quarter', 'Number of new customers in quarter (IT Services); new metric'),
    (r'Closing Head ?Count|Closing Employee Count', 'headcount', 'total', 'total', 'count', 'na', 'point', None),
    (r'Sales & Support Staff', 'headcount', 'Sales & Support Staff - IT Services', 'other', 'count', 'na', 'point', None),
    (r'^Gross Utilization', 'utilization_gross', 'total', 'total', 'pct', 'na', 'quarter', None),
    (r'Net Utilization \((excl|Excluding) Support\)', 'utilization_net_excl_support', 'total', 'total', 'pct', 'na', 'quarter', None),
    (r'Net Utilization \(Excluding Trainees\)', 'utilization_excl_trainees', 'total', 'total', 'pct', 'na', 'quarter', None),
    (r'^Voluntary TTM', 'attrition', 'Voluntary TTM', 'other', 'pct', 'na', 'ltm', None),
    (r'^Voluntary Quarterly Annualized', 'attrition', 'Voluntary Quarterly Annualized', 'other', 'pct', 'na', 'quarter', None),
    (r'^(BPO|BPS|DOP|DO&P) ?%? ?[-—]? ?\(?Post Training Quarterly', 'attrition', 'BPS/DOP post-training quarterly', 'other', 'pct', 'na', 'quarter', None),
    (r'^(BPO|BPS|DOP|DO&P) ?%? ?[-—]? ?Quarterly', 'attrition', 'BPS/DOP quarterly', 'other', 'pct', 'na', 'quarter', None),
    (r'Revenue from FPP', 'revenue_share_fixed_price', 'total', 'total', 'pct', 'na', 'quarter', None),
    (r'Onsite revenue', 'revenue_share_onsite', 'total', 'total', 'pct', 'na', 'quarter', None),
    (r'Off ?shore revenue', 'revenue_share_offshore', 'total', 'total', 'pct', 'na', 'quarter', None),
    (r'Total Bookings TCV', 'bookings', 'total', 'total', 'USD_mn', 'reported', 'quarter', 'Total bookings TCV: all orders booked incl. new orders, renewals and changes to existing contracts (datasheet note)'),
    (r'Large deal TCV', 'tcv', 'Large deals (>=USD30mn TCV)', 'other', 'USD_mn', 'reported', 'quarter', 'Large deal bookings = deals >= $30mn TCV (datasheet note)'),
]
TABLE_METRICS = [(re.compile(p, re.I),) + tuple(rest) for p, *rest in TABLE_METRICS]
SKIP_LABEL = re.compile(r'Guidance|actual currency|Revenues performance|Operating Margin|Top customer|^Top \d|^Top$|Revenue from Existing|^(USD|GBP|EUR|INR|AUD|CAD|Others)$|Currency|^\$$', re.I)
END_SECTION = re.compile(r'Guidance|Customer size|Total Bookings|% of Revenue|Currency|Closing|Utilization|Attrition|Revenue Mix|Revenue from FPP|Customer Concentration|Growth Metrics|Annexure', re.I)

def bucket_dim(label):
    m = re.search(r'\$\s*(\d+)', label)
    return f'USD{m.group(1)}mn+'

def parse_file(fn, rows, log):
    fy, q = fy_q_from_name(os.path.basename(fn))
    lines = open(fn, encoding='utf-8', errors='replace').read().split('\n')
    mode = None  # 'table', 'growth', 'skip'
    cols = None
    section = None
    gcols = None
    prev_text = ''
    scope = ''
    scope_open = False
    for ln_i, line in enumerate(lines):
        line = line.replace('\f', '')
        line = re.sub(r'(?<=[\d%])(Note ?\d+|\*+|\^+|#+)', lambda m: ' ' * len(m.group(0)), line)
        if HEADER.match(line):
            cols = calibrate(lines, ln_i, parse_header(line, fy))
            mode = 'table'
            prev_text = ''
            continue
        if re.search(r'Growth Metrics', line, re.I):
            mode = 'growth'; section = None; gcols = None; prev_text = ''
            continue
        if re.search(r'Annexure|Segment-wise breakup|Reconciliation|Break-up of', line, re.I):
            mode = 'skip'
            continue
        st = line.strip()
        if re.match(r'^(\(IT Serv|\(Excluding|B\. IT Services|IT Services excl|\(IT Services)', st) or scope_open:
            if not scope_open:
                scope = ''
            scope = (scope + ' ' + re.sub(r'\s{2,}.*$', '', st)).strip()
            scope_open = scope.count('(') > scope.count(')')
        labels, vals = split_line(line)
        ltexts = [clean_label(t) for _, _, t in labels]
        ltexts = [t for t in ltexts if t]
        # section headings
        for t in ltexts:
            for pat, dt in SEC_PATTERNS:
                if pat.search(t):
                    section = dt
        if mode not in ('table', 'growth'):
            continue
        if not vals:
            if ltexts and ltexts[-1].lower() not in SIDE:
                prev_text = ltexts[-1]
                if END_SECTION.search(' '.join(ltexts)) and not any(p.search(t) for t in ltexts for p, _ in SEC_PATTERNS):
                    section = None
            continue
        label = ltexts[-1] if ltexts else ''
        if label.lower() in SIDE:
            label = ''
        full = (prev_text + ' ' + label).strip() if prev_text else label
        # guidance ranges and other skip rows
        if SKIP_LABEL.search(label) or (not label and SKIP_LABEL.search(prev_text)):
            prev_text = ''
            if re.search(r'Guidance|Currency|Top', label + prev_text, re.I):
                section = None
            continue
        if any(re.search(r'\d-\d', v) for _, v in vals):
            prev_text = ''
            continue
        if mode == 'table':
            if cols is None:
                continue
            matched = None
            for rx, metric, dim, dt, unit, basis, ptype, note in TABLE_METRICS:
                if rx.search(label) or (not label and rx.search(prev_text)) or (label and len(label) < 25 and rx.search(full)):
                    matched = (metric, dim, dt, unit, basis, ptype, note, rx)
                    break
            if matched:
                metric, dim, dt, unit, basis, ptype, note, rx = matched
                if metric not in ('revenue', 'revenue_growth_qoq'):
                    section = None
                if metric == 'clients_bucket':
                    dim = bucket_dim(label)
                if metric == 'headcount' and dim == 'total':
                    lab = label or full
                    note = f'Datasheet row "{lab}"'
                    if re.search('Head Count', lab, re.I):
                        dim, dt = 'IT Services head count (pre-FY18 definition)', 'other'
                        note += '; older "Head Count" definition, ~16k above "Employee Count" where both shown (Q4FY17 datasheet); not comparable with total'
                    else:
                        note += '; closing employee count (datasheet titled Operating Metrics pertaining to IT Services Segment)'
                if metric == 'headcount' and dim != 'total':
                    note = f'Datasheet row "{label or full}"'
                if metric in ('attrition',) or metric.startswith('utilization') or metric.startswith('revenue_share_o') or metric == 'revenue_share_fixed_price':
                    note = f'Datasheet row "{label or full}"; scope sub-heading: "{scope}"'
                emit(rows, log, fn, fy, q, cols, vals, metric, dim, dt, unit, basis, ptype, note, label or full, line)
            elif section and label and all(v.endswith('%') for _, v in vals):
                seg = label
                emit(rows, log, fn, fy, q, cols, vals, 'revenue_share', seg, section, 'pct', 'na', 'quarter',
                     'Share of IT Services revenue', seg, line)
            else:
                log.append(f'UNMATCHED table {os.path.basename(fn)}:{ln_i+1}: [{full}] {line.strip()[:140]}')
            prev_text = ''
        elif mode == 'growth':
            numeric = [(c, v) for c, v in vals if v not in ('-', '—')]
            if gcols is None and len(vals) >= 4:
                gcols = [c for c, _ in vals]
            if gcols is None:
                log.append(f'NOGCOLS {os.path.basename(fn)}:{ln_i+1}: {line.strip()[:120]}')
                continue
            if not label:
                label = prev_text
            if not label:
                log.append(f'UNLABELED growth {os.path.basename(fn)}:{ln_i+1}: {line.strip()[:120]}')
                continue
            names = [('segment_growth_qoq', 'reported'), ('segment_growth_yoy', 'reported'),
                     ('segment_growth_qoq', 'cc'), ('segment_growth_yoy', 'cc')]
            is_total = re.match(r'^IT Services$', label, re.I) is not None
            idx = align([c for c, _ in vals], gcols)
            if idx is None:
                log.append(f'TOOMANY growth {os.path.basename(fn)}:{ln_i+1}: {line.strip()[:120]}')
                continue
            for (c, v), j in zip(vals, idx):
                if len(vals) < len(gcols) and abs(gcols[j] - c) > 8:
                    log.append(f'FAR growth {os.path.basename(fn)}:{ln_i+1}: {v} {line.strip()[:120]}')
                if j >= 4:
                    continue  # FY growth columns in Q4 datasheets: skipped (annual)
                val = to_num(v)
                if val is None:
                    continue
                metric, basis = names[j]
                if is_total:
                    metric = metric.replace('segment_', 'revenue_')
                    dim, dt = 'IT Services', 'other'
                else:
                    if section is None:
                        log.append(f'NOSECTION growth {os.path.basename(fn)}:{ln_i+1}: {line.strip()[:120]}')
                        continue
                    dim, dt = label, section
                rows.append(dict(fy=fy, q=q, tfy=fy, tq=q, metric=metric, dimension=dim, dim_type=dt, value=val,
                                 unit='pct', basis=basis, period_type='quarter', file=os.path.basename(fn),
                                 loc='Growth Metrics table', note='Growth as reported in datasheet Growth Metrics table', label=label))
            prev_text = ''

def align(centers, cols_c):
    """monotonic assignment of tokens to columns minimising total distance (DP)."""
    n, m = len(centers), len(cols_c)
    if n > m:
        return None
    if n == m:
        return list(range(n))
    INF = float('inf')
    D = [[INF] * (m + 1) for _ in range(n + 1)]
    B = [[None] * (m + 1) for _ in range(n + 1)]
    for j in range(m + 1):
        D[0][j] = 0
    for i in range(1, n + 1):
        for j in range(i, m + 1):
            # token i-1 at column j-1, or column j-1 skipped
            a = D[i - 1][j - 1] + abs(centers[i - 1] - cols_c[j - 1])
            b = D[i][j - 1]
            if a <= b:
                D[i][j], B[i][j] = a, 'take'
            else:
                D[i][j], B[i][j] = b, 'skip'
    res = []
    i, j = n, m
    while i > 0:
        if B[i][j] == 'take':
            res.append(j - 1); i -= 1; j -= 1
        else:
            j -= 1
    return res[::-1]

def calibrate(lines, start, cols):
    offs = [[] for _ in cols]
    for line in lines[start + 1:]:
        if HEADER.match(line) or re.search(r'Growth Metrics', line, re.I):
            break
        _, vals = split_line(line.replace('\f', ''))
        if len(vals) == len(cols):
            for k, (c, v) in enumerate(vals):
                offs[k].append(c - cols[k][0])
    out = []
    for k, col in enumerate(cols):
        o = sorted(offs[k])
        med = o[len(o) // 2] if o else 0
        out.append((col[0] + med,) + tuple(col[1:]))
    return out

def emit(rows, log, fn, fy, q, cols, vals, metric, dim, dt, unit, basis, ptype, note, label, line):
    idx = align([c for c, _ in vals], [c[0] for c in cols])
    if idx is None:
        log.append(f'TOOMANY table {os.path.basename(fn)}: {label}: {line.strip()[:140]}')
        return
    for (c, v), j in zip(vals, idx):
        if len(vals) < len(cols) and abs(cols[j][0] - c) > 8:
            log.append(f'FAR {os.path.basename(fn)}: {label}: token {v} at {c} col {cols[j][2]} at {cols[j][0]:.1f}')
        tq = cols[j][1]
        if tq is None:
            continue  # annual column
        val = to_num(v)
        if val is None:
            continue
        rows.append(dict(fy=fy, q=q, tfy=tq[0], tq=tq[1], metric=metric, dimension=dim, dim_type=dt, value=val,
                         unit=unit, basis=basis, period_type=ptype, file=os.path.basename(fn),
                         loc='Operating metrics table', note=note, label=label))

def main():
    files = sorted(glob.glob(os.path.join(TXT, '*')))
    files = [f for f in files if re.search(r'data-?sheet', os.path.basename(f), re.I)]
    rows, log = [], []
    for f in files:
        parse_file(f, rows, log)
    out = os.path.join(SRC, 'parsed_datasheets.csv')
    with open(out, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    with open(os.path.join(SRC, 'parse_datasheets.log'), 'w') as fh:
        fh.write('\n'.join(log))
    print(len(rows), 'rows;', len(log), 'log lines')

if __name__ == '__main__':
    main()
