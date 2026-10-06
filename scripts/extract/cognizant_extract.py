"""Extract Cognizant (CIK 1058290) KPIs from local copies of EDGAR filings into data/raw/cognizant.csv.

Inputs (created by cognizant_download.py):
  data/sources/cognizant/manifest.csv       list of downloaded filings (form, dates, url, local file)
  data/sources/cognizant/edgar/*.htm        raw EDGAR documents
  data/sources/cognizant/txt/*.txt          text versions (tables flattened to 'a | b | c' lines), built below if missing

Sources parsed:
  1. Earnings releases (8-K Ex.99.1; Q4 2016 = Ex.99.2): revenue, segment/geography tables, headcount,
     net additions, attrition, bookings, book-to-bill, large deals.
  2. Earnings supplements (8-K Ex.99.2/99.3 slide decks, 2019Q3+): revenue-growth tables (total & segment,
     reported & cc), employee-metrics tables (2022Q1+), TTM bookings series (2022Q1+).
     Chart-only slides (2019Q3-2021Q4 employee metrics; 2021Q4 bookings) were read from the slide images
     (data/sources/cognizant/slides/*.jpg) and are HAND-ENTERED below (see HAND_* dicts).
  3. 10-Q / 10-K: revenue by service line and contract type (2018+), service-line share/growth text (2014-2017),
     fixed-price share, active/strategic clients, top-5/top-10 client share (2014-2016), 10-K headcount by location.
"""
import csv, glob, os, re, datetime as dt
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'data', 'sources', 'cognizant')
OUT = os.path.join(ROOT, 'data', 'raw', 'cognizant.csv')
FIRM = 'cognizant'

# ---------------------------------------------------------------- helpers
QEND = {1: (3, 31), 2: (6, 30), 3: (9, 30), 4: (12, 31)}
MONTHS = {m: i for i, m in enumerate(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                      'September', 'October', 'November', 'December'], 1)}


def qlabel(y, q):
    return f'{y}Q{q}'


def qend(y, q):
    m, d = QEND[q]
    return f'{y}-{m:02d}-{d:02d}'


def q_of_date(d):  # d: date -> (y,q)
    return d.year, (d.month - 1) // 3 + 1


def prior_qend(filing_date):
    d = dt.date.fromisoformat(filing_date)
    y, q = q_of_date(d)
    # quarter strictly before the one containing the filing date
    q -= 1
    if q == 0:
        y, q = y - 1, 4
    return y, q


def parse_date(s):
    s = s.replace(',', ' ').split()
    return dt.date(int(s[2]), MONTHS[s[0]], int(s[1]))


def parse_qtoken(tok):
    """"Q1 '25", "Q1' 18", "Q1 2021", "Q4 '221" (footnote) -> (y,q)"""
    m = re.match(r"Q([1-4])\s*['’‘]?\s*(\d{4}|\d{2})", tok)
    q = int(m.group(1)); ys = m.group(2)
    y = int(ys) if len(ys) == 4 else 2000 + int(ys)
    return y, q


QTOK = r"Q[1-4](?:\s?['’‘]\s?\d{2}(?!\d{2})\d?|\s\d{4})"
PCT = r"(?:\(\d+\.?\d*%\)|\(\d+\.?\d*\)%|[+-]?\d+\.?\d*%|—%)"


def pct_val(tok):
    tok = tok.strip()
    if tok.startswith('—'):
        return 0.0
    neg = tok.startswith('(')
    v = float(re.sub(r'[^\d.]', '', tok))
    return -v if neg else v


def num(s):
    return float(s.replace(',', ''))


rows = []


def add(y, q, metric, dimension, dim_type, value, unit, basis, period_type, src, loc, notes=''):
    rows.append(dict(firm=FIRM, fiscal_q=qlabel(y, q), period_end=qend(y, q), cal_q=qlabel(y, q), metric=metric,
                     dimension=dimension, dim_type=dim_type,
                     value='' if value is None else (round(value, 4) if isinstance(value, float) else value),
                     unit=unit, basis=basis, period_type=period_type, source_url=src['url'], source_doc=src['doc'],
                     source_loc=loc, doc_date=src['date'], notes=notes))


# ---------------------------------------------------------------- text conversion
def to_text(path):
    s = BeautifulSoup(open(path, 'rb').read(), 'lxml')
    for t in s(['script', 'style']):
        t.decompose()
    for tr in s.find_all('tr'):
        cells = [c.get_text(' ', strip=True) for c in tr.find_all(['td', 'th'])]
        cells = [c for c in cells if c]
        tr.replace_with(s.new_string('\n' + ' | '.join(cells) + '\n'))
    txt = s.get_text('\n')
    return re.sub(r'\n\s*\n+', '\n', txt)


def get_text(local):
    p = os.path.join(SRC, 'txt', local + '.txt')
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w').write(to_text(os.path.join(SRC, 'edgar', local)))
    return open(p).read().replace('\xa0', ' ')


def flat(t):
    t = re.sub(r'\s+', ' ', t)
    t = t.replace('V oluntary', 'Voluntary')
    return t


man = list(csv.DictReader(open(os.path.join(SRC, 'manifest.csv'))))

# ---------------------------------------------------------------- 1. earnings releases
SKIP_8K = {'2020-04-09', '2023-01-12'}  # COVID business update / CEO appointment (not quarterly results)
NAME_FIX = {'Products & Resources': 'Products and Resources',
            'Communications, Media & Technology': 'Communications, Media and Technology'}
WORDQ = {'first': 1, 'second': 2, 'third': 3, 'fourth': 4}
NUMWORD = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
           'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15}

releases = []
for m in man:
    if m['form'] != '8-K' or m['filing_date'] in SKIP_8K:
        continue
    t = get_text(m['local'])
    if not re.search(r'Revenues? by Segment', t):
        continue
    if 'FOR IMMEDIATE RELEASE' not in flat(t) and 'REPORTS' not in t.upper()[:3000]:
        continue
    releases.append((m, t))

for m, t in releases:
    y, q = prior_qend(m['filing_date'])
    exh = re.search(r'EX-99\.(\d)', t).group(1)
    src = dict(url=m['url'], doc=f'Cognizant Q{q} {y} earnings release (8-K Ex.99.{exh})', date=m['filing_date'])
    lines = t.split('\n')
    # --- segment / geography table (first = three-month block)
    i0 = next(i for i, l in enumerate(lines) if re.match(r'\s*Revenues? by Segment', l))
    header = re.sub(r'\s+', ' ', ' '.join(lines[max(0, i0 - 6):i0]))
    assert 'Three Months Ended' in header, (m['local'], header)
    hq = re.search(r"Three Months Ended\s*(\w+ \d{1,2}, ?\d{4})", header)
    if not hq: print("HDR", m["local"], header[-400:])
    hy, hqq = q_of_date(parse_date(hq.group(1)))
    assert (hy, hqq) == (y, q), (m['local'], hy, hqq, y, q)
    typ = 'A' if 'Sequential' in header else ('C' if 'Constant Currency' in header else 'B')
    thousands = 'thousands' in header.lower()
    section = 'vertical'
    done_tot = 0
    for l in lines[i0 + 1:i0 + 30]:
        if re.match(r'\s*Revenues? by Geography', l):
            section = 'geography'; continue
        if '|' not in l:
            continue
        cells = l.split('|')
        name = re.sub(r'\s*(\([a-z]\))+\s*$', '', cells[0].strip()).strip()
        name = re.sub(r'\s*\([a-z]\)', '', name).strip()
        rest = ' '.join(cells[1:]).replace('$', ' ').replace('%', ' ')
        rest = rest.replace('—', ' 0 ')
        rest = re.sub(r'\(\s*([\d.,]+)\s*\)', r'-\1', rest)
        vals = [num(x) for x in re.findall(r'-?[\d,]*\.?\d+', rest)]
        loc = 'Revenue by Business Segment and Geography table (three months)' if typ != 'A' else 'Schedule of Supplemental Information - revenue by segment/geography (three months)'
        note_k = 'converted from USD thousands as reported' if thousands else ''
        if name.startswith('Total Revenue'):
            if done_tot == 0:
                exp = {'A': 3, 'B': 2, 'C': 3}[typ]
                assert len(vals) == exp, (m['local'], l, vals)
                rev = vals[0] / 1000 if thousands else vals[0]
                add(y, q, 'revenue', 'total', 'total', rev, 'USD_mn', 'reported', 'quarter', src, loc, note_k)
                if typ == 'A':
                    add(y, q, 'revenue_growth_qoq', 'total', 'total', vals[1], 'pct', 'reported', 'quarter', src, loc)
                    add(y, q, 'revenue_growth_yoy', 'total', 'total', vals[2], 'pct', 'reported', 'quarter', src, loc)
                else:
                    add(y, q, 'revenue_growth_yoy', 'total', 'total', vals[1], 'pct', 'reported', 'quarter', src, loc)
                if typ == 'C':
                    add(y, q, 'revenue_growth_yoy', 'total', 'total', vals[2], 'pct', 'cc', 'quarter', src, loc)
            done_tot += 1
            if done_tot == 2:
                break
            continue
        if section == 'geography' and done_tot < 1:
            continue
        exp = {'A': 4, 'B': 3, 'C': 4}[typ]
        if len(vals) != exp:
            print('WARN row', m['local'], l, vals); continue
        dim = name
        dtp = section
        seg_note = note_k
        if dim == 'Rest of Europe':
            seg_note = (seg_note + '; ' if seg_note else '') + 'Renamed "Continental Europe" from Q2 2019'
        if dim == 'Products and Resources' and (y, q) <= (2018, 4) and (y, q) >= (2017, 1):
            seg_note = (seg_note + '; ' if seg_note else '') + 'Previously referred to as Manufacturing/Retail/Logistics'
        if dim == 'Communications, Media and Technology' and (2017, 1) <= (y, q) <= (2018, 4):
            seg_note = (seg_note + '; ' if seg_note else '') + 'Previously referred to as Other'
        add(y, q, 'segment_revenue', dim, dtp, vals[0] / 1000 if thousands else vals[0], 'USD_mn', 'reported', 'quarter', src, loc, seg_note)
        add(y, q, 'revenue_share', dim, dtp, vals[1], 'pct', 'reported', 'quarter', src, loc, seg_note if 'Renamed' in seg_note or 'Previously' in seg_note else '')
        if typ == 'A':
            add(y, q, 'segment_growth_qoq', dim, dtp, vals[2], 'pct', 'reported', 'quarter', src, loc)
            add(y, q, 'segment_growth_yoy', dim, dtp, vals[3], 'pct', 'reported', 'quarter', src, loc)
        else:
            add(y, q, 'segment_growth_yoy', dim, dtp, vals[2], 'pct', 'reported', 'quarter', src, loc)
        if typ == 'C':
            add(y, q, 'segment_growth_yoy', dim, dtp, vals[3], 'pct', 'cc', 'quarter', src, loc)

    f = flat(t)
    # --- headcount (a) "approximately N employees as of <date>"
    for mm in re.finditer(r'approximately ([\d,]+) employees as of (\w+ \d{1,2}, \d{4})', f):
        d = parse_date(mm.group(2)); hy, hq = q_of_date(d)
        add(hy, hq, 'headcount', 'total', 'total', num(mm.group(1)), 'count', 'na', 'point', src, 'About Cognizant paragraph',
            'approximate; total employees (company-wide)')
    mm = re.search(r'year-end headcount was approximately ([\d,]+)', f)
    if mm:
        add(y, q, 'headcount', 'total', 'total', num(mm.group(1)), 'count', 'na', 'point', src, 'Highlights',
            'approximate; year-end headcount')
    mm = re.search(r'Net headcount addition for the quarter was approximately ([\d,]+)', f)
    if mm:
        add(y, q, 'net_additions', 'total', 'total', num(mm.group(1)), 'count', 'na', 'quarter', src, 'Highlights', 'approximate')
    # (b) Employee Metrics table
    for i, l in enumerate(lines):
        if l.strip().startswith('Employee Metrics:'):
            dates = [parse_date(x.strip()) for x in l.split('|')[1:] if x.strip()]
            nl = lines[i + 1]
            assert nl.startswith('Number of employees'), nl
            ns = [num(x) for x in re.findall(r'[\d,]{5,}', nl)]
            assert len(ns) == len(dates)
            for d, n in zip(dates, ns):
                hy, hq = q_of_date(d)
                add(hy, hq, 'headcount', 'total', 'total', n, 'count', 'na', 'point', src, 'Employee Metrics table',
                    'Number of employees (company-wide)' + ('' if (hy, hq) == (y, q) else '; comparative period shown in later release'))
    # (c) "Total headcount ... was N"
    mm = re.search(r'Total headcount (?:at the end of the (\w+) quarter|as of (\w+ \d{1,2}, \d{4})) was\s+([\d,]+)([^.]*?)\.(?=\s)', f)
    if mm:
        n = num(mm.group(3)); tail = mm.group(4)
        note = 'Total headcount (company-wide)' + ('; includes Belcan (acquired Aug 2024)' if 'Belcan' in tail else '')
        add(y, q, 'headcount', 'total', 'total', n, 'count', 'na', 'point', src, 'Employee Metrics paragraph', note)
        sign = 1
        for c in re.finditer(r'(?:(an increase|a decrease|increase|decrease)\s+of\s+)?([\d,]+)\s+from\s+(both\s+)?(Q[1-4] \d{4}|\w+ \d{1,2}, \d{4})(?:\s+and\s+(Q[1-4] \d{4}|\w+ \d{1,2}, \d{4}))?', tail):
            if c.group(1):
                sign = 1 if 'increase' in c.group(1) else -1
            refs = [c.group(4)] + ([c.group(5)] if c.group(5) else [])
            for r in refs:
                ry, rq = parse_qtoken(r) if r.startswith('Q') else q_of_date(parse_date(r))
                lag = (y - ry) * 4 + (q - rq)
                if lag == 1:
                    add(y, q, 'net_additions', 'total', 'total', sign * num(c.group(2)), 'count', 'na', 'quarter', src,
                        'Employee Metrics paragraph', 'change in total headcount vs prior quarter end, as reported')
                elif lag == 4:
                    add(y, q, 'net_additions', 'total', 'total', sign * num(c.group(2)), 'count', 'na', 'ltm', src,
                        'Employee Metrics paragraph', 'change in total headcount vs year-ago quarter end, as reported')
    # --- attrition text
    mm = re.search(r'Voluntary attrition, on a quarterly annualized basis, declined to (\d+\.?\d*)%', f)
    if mm:
        add(y, q, 'attrition', 'total', 'total', float(mm.group(1)), 'pct', 'na', 'quarter', src, 'Employee Metrics paragraph',
            'Voluntary attrition, quarterly annualized, company-wide')
    mm = re.search(r'Voluntary attrition, on a trailing-twelve-month basis, declined to (\d+\.?\d*)%', f)
    if mm:
        add(y, q, 'attrition', 'total', 'total', float(mm.group(1)), 'pct', 'na', 'ltm', src, 'Employee Metrics paragraph',
            'Voluntary attrition, trailing twelve months, company-wide')
    mm = re.search(r'Voluntary attrition\s*[-–]\s*Tech Services[^%]{0,120}?(?:was|to)\s+(\d+\.?\d*)\s*%', f, re.I)
    if mm:
        note = 'Voluntary Attrition - Tech Services, trailing twelve months (excludes Intuitive Operations and Automation practice)'
        if (y, q) >= (2026, 1):
            note += '; definition modified Q1 2026 to exclude certain categories of negotiated separations'
        add(y, q, 'attrition', 'total', 'total', float(mm.group(1)), 'pct', 'na', 'ltm', src, 'Employee Metrics paragraph', note)
    # --- bookings
    loc = 'Bookings paragraph / highlights'
    ttm = None
    for pat in [r'trailing[- ]12-month bookings of \$(\d+\.\d) billion',
                r'trailing-twelve-month basis, bookings (?:grew|increased|declined|decreased)(?: \d+%)?(?: year-over-year)? to \$(\d+\.\d) billion']:
        mm = re.search(pat, f, re.I)
        if mm:
            ttm = float(mm.group(1)); break
    if ttm is not None:
        add(y, q, 'bookings', 'total', 'total', ttm, 'USD_bn', 'reported', 'ltm', src, loc,
            'Trailing-twelve-month bookings (TCV of new contracts incl. renewals and expansions)')
    mm = re.search(r'trailing-twelve-month basis, bookings (grew|increased|declined|decreased) (\d+)%', f, re.I)
    if mm:
        v = float(mm.group(2)) * (-1 if mm.group(1) in ('declined', 'decreased') else 1)
        add(y, q, 'bookings_growth_yoy', 'total', 'total', v, 'pct', 'reported', 'ltm', src, loc, 'growth in TTM bookings, as reported')
    mm = re.search(r'full-year (\d{4}) bookings of \$(\d+\.\d) billion', f) or re.search(r'For the full[- ]year, bookings grew (?:\d+)% (?:year-over-year )?to \$(\d+\.\d) billion', f)
    if mm and ttm is None:
        add(y, q, 'bookings', 'total', 'total', float(mm.groups()[-1]), 'USD_bn', 'reported', 'annual', src, loc, 'Full-year bookings')
    mm = re.search(r'For the full[- ]year, bookings grew (\d+)%', f)
    if mm:
        add(y, q, 'bookings_growth_yoy', 'total', 'total', float(mm.group(1)), 'pct', 'reported', 'annual', src, loc, 'growth in full-year bookings, as reported')
    for mm in re.finditer(r'book-to-bill of (?:approximately )?(\d+\.\d+)', f):
        ctx = f[max(0, mm.start() - 120):mm.start()]
        if 'in-period' in ctx:
            pt, nt = 'quarter', 'in-period (quarterly) book-to-bill'
        elif re.search(r'full[- ]year', ctx, re.I) and 'trailing' not in ctx.lower():
            pt, nt = 'annual', 'full-year bookings / full-year revenue'
        else:
            pt, nt = 'ltm', 'TTM bookings / TTM revenue'
        key = (y, q, pt)
        if any(r['metric'] == 'book_to_bill' and r['fiscal_q'] == qlabel(y, q) and r['period_type'] == pt and r['source_url'] == src['url'] for r in rows):
            continue
        add(y, q, 'book_to_bill', 'total', 'total', float(mm.group(1)), 'ratio', 'reported', pt, src, loc, nt + ' (approximate, as reported)')
    qb = None
    mm = re.search(r'Bookings in the (first|second|third|fourth)? ?quarter (grew|increased|declined|decreased|were flat)(?: (\d+)%)?(?: year-over-year)?', f)
    if mm:
        qb = 0.0 if mm.group(2) == 'were flat' else float(mm.group(3)) * (-1 if mm.group(2) in ('declined', 'decreased') else 1)
    else:
        mm = re.search(r'Q[1-4] bookings(?: \d)? (grew|increased|declined|decreased) (\d+)% year-over-year', f)
        if mm:
            qb = float(mm.group(2)) * (-1 if mm.group(1) in ('declined', 'decreased') else 1)
    if qb is not None:
        add(y, q, 'bookings_growth_yoy', 'total', 'total', qb, 'pct', 'reported', 'quarter', src, loc, 'growth in quarterly bookings, as reported')
    mm = re.search(r'(?:First half|Year-to-date) \d{0,4} ?bookings(?: 1)? increased (\d+)%', f)
    if mm:
        add(y, q, 'bookings_growth_yoy', 'total', 'total', float(mm.group(1)), 'pct', 'reported', 'ytd', src, loc, 'growth in year-to-date bookings, as reported')
    mm = re.search(r'year-to-date bookings growth to (\d+)%', f)
    if mm:
        add(y, q, 'bookings_growth_yoy', 'total', 'total', float(mm.group(1)), 'pct', 'reported', 'ytd', src, loc, 'growth in year-to-date bookings, as reported')
    mm = re.search(r'quarter bookings included (\w+) large deals', f)
    if mm:
        add(y, q, 'large_deals_count', 'total', 'total', float(NUMWORD[mm.group(1).lower()]), 'count', 'na', 'quarter', src, loc,
            'number of large deals (TCV >= USD100mn) signed in quarter')

# ---------------------------------------------------------------- 2. earnings supplements (decks)
SEGS = [('Financial Services', 'Financial Services'), ('Health Sciences', 'Health Sciences'), ('Healthcare', 'Healthcare'),
        ('Products & Resources', 'Products and Resources'), ('Communications, Media & Technology', 'Communications, Media and Technology')]


def slides_of(local):
    s = open(os.path.join(SRC, 'edgar', local), errors='ignore').read()
    parts = re.split(r'<IMG[^>]*>', s, flags=re.I)
    return [flat(BeautifulSoup(p, 'lxml').get_text(' ')) for p in parts[1:]]


def qruns(t):
    """list of (end_pos, [(y,q),...]) runs of >=4 consecutive quarter labels"""
    out = []
    for mm in re.finditer(rf"(?:{QTOK}\s*){{4,}}", t):
        toks = [(x.start(), x.end(), parse_qtoken(x.group(0))) for x in re.finditer(QTOK, mm.group(0))]
        cur = [toks[0]]
        for tk in toks[1:]:
            if tk[2] > cur[-1][2]:
                cur.append(tk)
            else:
                out.append((mm.start() + cur[0][0], mm.start() + cur[-1][1], [c[2] for c in cur])); cur = [tk]
        out.append((mm.start() + cur[0][0], mm.start() + cur[-1][1], [c[2] for c in cur]))
    return [o for o in out if len(o[2]) >= 4]


def row_after(t, label_regex, n, start=0):
    mm = re.compile(label_regex + rf"\s+((?:{PCT}\s*){{{n}}})").search(t, start)
    if not mm:
        return None, None
    toks = re.findall(PCT, mm.group(1))
    return [pct_val(x) for x in toks], mm.end()


decks = []
for m in man:
    if m['form'] != '8-K' or not re.search(r'exhibit99[23]', m['doc']):
        continue
    if m['filing_date'] < '2019-10-01':
        continue  # 2019-07-31 deck has no text layer; 2017-02-08 is an investor-day deck
    sl = slides_of(m['local'])
    if len(sl) < 10:
        continue  # one-page fact sheet
    decks.append((m, sl))

for m, sl in decks:
    y, q = prior_qend(m['filing_date'])
    exh = re.search(r'exhibit99(\d)', m['doc']).group(1)
    src = dict(url=m['url'], doc=f'Cognizant Q{q} {y} earnings supplement (8-K Ex.99.{exh})', date=m['filing_date'])
    for si, t in enumerate(sl, 1):
        if 'Revenue Performance' in t or 'Guidance' in t[:120]:
            continue
        # --- revenue growth tables
        if 'Y/Y CC' in t:
            seg = None
            if 'Adjusted Diluted EPS' in t:
                seg = 'total'
            else:
                found = [(t.find(k), v) for k, v in SEGS if k in t]
                if found:
                    seg = min(found)[1]
            if seg:
                for (a, b, qs) in qruns(t):
                    n = len(qs)
                    yy, e1 = row_after(t[b:b + 400], r"(?:Revenue )?Y/Y1?", n)
                    if yy is None:
                        continue
                    cc, e2 = row_after(t[b:b + 800], r"(?:Revenue )?Y/Y CC1?", n)
                    loc = f'slide {si}: revenue growth table'
                    for (qy, qq), v in zip(qs, yy):
                        if seg == 'total':
                            add(qy, qq, 'revenue_growth_yoy', 'total', 'total', v, 'pct', 'reported', 'quarter', src, loc)
                        else:
                            add(qy, qq, 'segment_growth_yoy', seg, 'vertical', v, 'pct', 'reported', 'quarter', src, loc)
                    if cc:
                        for (qy, qq), v in zip(qs, cc):
                            if seg == 'total':
                                add(qy, qq, 'revenue_growth_yoy', 'total', 'total', v, 'pct', 'cc', 'quarter', src, loc)
                            else:
                                add(qy, qq, 'segment_growth_yoy', seg, 'vertical', v, 'pct', 'cc', 'quarter', src, loc)
                    break
        # --- TTM bookings series (text decks 2022Q1+)
        mm = re.search(r"((?:\$\d+\.\d\s*){5})((?:\d{1,2}/\d{1,2}/\d{4}\s*|" + QTOK + r"\s*){5})\s*Trailing Twelve Month Bookings", t)
        if mm:
            vals = [float(x) for x in re.findall(r'\d+\.\d', mm.group(1))]
            labs = re.findall(r"\d{1,2}/\d{1,2}/\d{4}|" + QTOK, mm.group(2))
            for v, lab in zip(vals, labs):
                if '/' in lab:
                    mo, dd, yyyy = lab.split('/'); by, bq = q_of_date(dt.date(int(yyyy), int(mo), int(dd)))
                else:
                    by, bq = parse_qtoken(lab)
                note = 'Trailing-twelve-month bookings'
                if (by, bq) >= (2021, 3) and (by, bq) <= (2022, 1) and m['filing_date'] < '2022-11-01':
                    note += '; definition modified Q4 2021 (excl. early-renewal overlap, incl. unintegrated acquisitions); TTM to 6/30/2021 and earlier not restated'
                elif (by, bq) <= (2021, 2):
                    note += '; old definition (pre-Q4 2021), not restated'
                add(by, bq, 'bookings', 'total', 'total', v, 'USD_bn', 'reported', 'ltm', src, f'slide {si}: Trailing Twelve Month Bookings chart', note)
        # --- employee metrics tables (2022Q1+ text layout)
        if t.find('Employee Metrics') >= 0 and ('Onsite Utilization' in t or 'Blended Utilization' in t):
            runs = qruns(t)
            if not runs:
                continue
            a, b, qs = runs[0]
            n = len(qs)
            head = t[t.find('Employee Metrics') + len('Employee Metrics'):a]
            head = re.sub(r'(\d+) \.(\d)', r'\1.\2', head)
            hcs = [float(x) for x in re.findall(r'\d{3}\.\d', head)]
            loc = f'slide {si}: Employee Metrics'
            if len(hcs) == n:
                for (qy, qq), v in zip(qs, hcs):
                    add(qy, qq, 'headcount', 'total', 'total', round(v * 1000), 'count', 'na', 'point', src, loc,
                        'total headcount, reported in thousands (one decimal) in supplement chart')
            else:
                print('WARN hc', m['local'], head, n)
            specs = [(r'Trailing 12-Month Voluntary Attrition - Tech Services1?', 'attrition', 'ltm',
                      'Voluntary Attrition - Tech Services, trailing twelve months (excludes Intuitive Operations and Automation practice)'),
                     (r'Trailing 12-Month Voluntary Attrition(?! -)', 'attrition', 'ltm', 'Voluntary attrition, trailing twelve months, company-wide'),
                     (r'Quarterly Annualized Voluntary Attrition', 'attrition', 'quarter', 'Voluntary attrition, quarterly annualized, company-wide'),
                     (r'Quarterly Annualized Involuntary Attrition', 'attrition_involuntary', 'quarter', 'Involuntary attrition, quarterly annualized, company-wide'),
                     (r'Offshore Utilization, Excluding Trainees', 'utilization_offshore', 'quarter', 'Offshore utilization excluding trainees'),
                     (r'Onsite Utilization', 'utilization_onsite', 'quarter', 'Onsite utilization'),
                     (r'Blended Utilization, Excluding Trainees1?', 'utilization_excl_trainees', 'quarter',
                      'Blended Utilization, Excluding Trainees (new metric from Q1 2024; blended onsite+offshore, replaces separate onsite/offshore disclosure)')]
            for lab, met, pt, note in specs:
                vals, _ = row_after(t, lab, n)
                if vals is None:
                    continue
                # Tech-services attrition label also contains the generic label; avoid double capture
                if met == 'attrition' and 'Tech Services' not in lab and 'Tech Services' in t[t.find('Trailing 12-Month'):t.find('Trailing 12-Month') + 60]:
                    continue
                for (qy, qq), v in zip(qs, vals):
                    nn = note
                    if met == 'attrition' and 'Tech Services' in lab and (qy, qq) >= (2026, 1):
                        nn += '; definition modified Q1 2026 to exclude certain categories of negotiated separations'
                    if met == 'attrition' and 'Tech Services' in lab and m['filing_date'] >= '2026-04-01' and (qy, qq) < (2026, 1):
                        nn += '; RECAST to the Q1 2026 definition (excl. certain negotiated separations) - differs from earlier vintages'
                    add(qy, qq, met, 'total', 'total', v, 'pct', 'na', pt, src, loc, nn)

# ---- hand-entered values read from slide images (chart decks). Each tuple: quarter -> value
Q = lambda s: (int(s[:4]), int(s[-1]))
HAND_SERIES = {
    'hc': {'2017Q1': 261.2, '2017Q2': 256.8, '2017Q3': 256.1, '2017Q4': 260.0, '2018Q1': 261.4, '2018Q2': 268.9, '2018Q3': 274.2,
           '2018Q4': 281.6, '2019Q1': 285.8, '2019Q2': 288.2, '2019Q3': 289.9, '2019Q4': 292.5, '2020Q1': 291.7, '2020Q2': 281.2,
           '2020Q3': 283.1, '2020Q4': 289.5, '2021Q1': 296.5, '2021Q2': 301.2, '2021Q3': 318.4, '2021Q4': 330.6},
    'attr_tot': {'2017Q1': 15, '2017Q2': 24, '2017Q3': 23, '2017Q4': 18, '2018Q1': 20, '2018Q2': 23, '2018Q3': 22, '2018Q4': 19,
                 '2019Q1': 19, '2019Q2': 23, '2019Q3': 24, '2019Q4': 21, '2020Q1': 22, '2020Q2': 24, '2020Q3': 18, '2020Q4': 19,
                 '2021Q1': 21, '2021Q2': 31, '2021Q3': 37, '2021Q4': 35},
    'attr_vol': {'2019Q1': 16, '2019Q2': 19, '2019Q3': 18, '2019Q4': 16, '2020Q1': 13, '2020Q2': 11, '2020Q3': 10, '2020Q4': 16,
                 '2021Q1': 18, '2021Q2': 29, '2021Q3': 33, '2021Q4': 31},
    'onsite': {'2017Q1': 91, '2017Q2': 93, '2017Q3': 93, '2017Q4': 92, '2018Q1': 92, '2018Q2': 93, '2018Q3': 93, '2018Q4': 92,
               '2019Q1': 91, '2019Q2': 92, '2019Q3': 92, '2019Q4': 92, '2020Q1': 91, '2020Q2': 91, '2020Q3': 93, '2020Q4': 91,
               '2021Q1': 92, '2021Q2': 92, '2021Q3': 91, '2021Q4': 90},
    'offshore': {'2017Q1': 79, '2017Q2': 80, '2017Q3': 82, '2017Q4': 83, '2018Q1': 83, '2018Q2': 83, '2018Q3': 83, '2018Q4': 83,
                 '2019Q1': 83, '2019Q2': 83, '2019Q3': 84, '2019Q4': 85, '2020Q1': 83, '2020Q2': 80, '2020Q3': 85, '2020Q4': 87,
                 '2021Q1': 85, '2021Q2': 84, '2021Q3': 84, '2021Q4': 83},
}
# deck filing date -> (slide no, first quarter shown, last quarter shown, series present)
HAND_DECKS = {
    '2019-10-30': (11, '2017Q1', '2019Q3', ['hc', 'attr_tot', 'onsite', 'offshore']),
    '2020-02-05': (12, '2017Q1', '2019Q4', ['hc', 'attr_tot', 'onsite', 'offshore']),
    '2020-05-07': (12, '2018Q1', '2020Q1', ['hc', 'attr_tot', 'onsite', 'offshore']),
    '2020-07-29': (11, '2018Q1', '2020Q2', ['hc', 'attr_tot', 'attr_vol', 'onsite', 'offshore']),
    '2020-10-28': (11, '2018Q1', '2020Q3', ['hc', 'attr_tot', 'attr_vol', 'onsite', 'offshore']),
    '2021-02-03': (13, '2018Q1', '2020Q4', ['hc', 'attr_tot', 'attr_vol', 'onsite', 'offshore']),
    '2021-05-05': (10, '2019Q1', '2021Q1', ['hc', 'attr_tot', 'attr_vol', 'onsite', 'offshore']),
    '2021-07-28': (10, '2019Q1', '2021Q2', ['hc', 'attr_tot', 'attr_vol', 'onsite', 'offshore']),
    '2021-10-27': (10, '2019Q1', '2021Q3', ['hc', 'attr_tot', 'attr_vol', 'onsite', 'offshore']),
    '2022-02-02': (13, '2019Q1', '2021Q4', ['hc', 'attr_tot', 'attr_vol', 'onsite', 'offshore']),
}
SERIES_META = {
    'hc': ('headcount', 'count', 'point', 'total headcount, reported in thousands (one decimal) in supplement chart'),
    'attr_tot': ('attrition_total', 'pct', 'quarter', 'Total attrition (voluntary + involuntary), quarterly annualized, company-wide'),
    'attr_vol': ('attrition', 'pct', 'quarter', 'Voluntary attrition, quarterly annualized, company-wide'),
    'onsite': ('utilization_onsite', 'pct', 'quarter', 'Onsite utilization'),
    'offshore': ('utilization_offshore', 'pct', 'quarter', 'Offshore utilization excluding trainees'),
}
deck_by_date = {m['filing_date']: m for m, sl in decks}
for fd, (slide, q0, q1, series) in HAND_DECKS.items():
    m = deck_by_date[fd]
    y, q = prior_qend(fd)
    exh = re.search(r'exhibit99(\d)', m['doc']).group(1)
    src = dict(url=m['url'], doc=f'Cognizant Q{q} {y} earnings supplement (8-K Ex.99.{exh})', date=fd)
    for s in series:
        met, unit, pt, note = SERIES_META[s]
        for ql, v in HAND_SERIES[s].items():
            if Q(ql) < Q(q0) or Q(ql) > Q(q1):
                continue
            val = round(v * 1000) if s == 'hc' else float(v)
            extra = ''
            if s == 'attr_tot' and ql == '2020Q2':
                extra = '; increase driven by involuntary attrition from Fit for Growth plan (slide footnote)'
            add(*Q(ql), met, 'total', 'total', val, unit, 'na', pt, src, f'slide {slide}: Employee Metrics chart',
                note + extra + '; hand-entered from slide image')
# 2021Q4 deck, slide 12 (image): TTM bookings
m = deck_by_date['2022-02-02']
src = dict(url=m['url'], doc='Cognizant Q4 2021 earnings supplement (8-K Ex.99.3)', date='2022-02-02')
for ql, v in {'2020Q4': 19.8, '2021Q1': 20.0, '2021Q2': 20.5, '2021Q3': 21.7, '2021Q4': 23.1}.items():
    note = 'Trailing-twelve-month bookings; hand-entered from slide image'
    note += ('; new definition (Q4 2021: excl. early-renewal overlap, incl. unintegrated acquisitions)' if Q(ql) >= (2021, 3)
             else '; old definition, not restated (data for unintegrated acquired entities unavailable)')
    add(*Q(ql), 'bookings', 'total', 'total', v, 'USD_bn', 'reported', 'ltm', src, 'slide 12: Trailing Twelve Month Bookings chart', note)
add(2021, 4, 'book_to_bill', 'total', 'total', 1.2, 'ratio', 'reported', 'annual', src, 'slide 12', 'FY2021 book-to-bill ratio; hand-entered from slide image')

# ---- Q1 2026 Tech Services attrition under the PREVIOUS definition (bridge value stated in footnote)
m = next(x for x in man if x['filing_date'] == '2026-04-29' and x['doc'] == 'exhibit9933312026.htm')
src = dict(url=m['url'], doc='Cognizant Q1 2026 earnings supplement (8-K Ex.99.3)', date='2026-04-29')
add(2026, 1, 'attrition', 'total', 'total', 14.0, 'pct', 'na', 'ltm', src, 'slide 13 footnote',
    'Voluntary Attrition - Tech Services, trailing twelve months, under PREVIOUS (pre-Q1 2026) definition; bridge value from footnote; hand-entered')

# ---- hand-entered AI disclosures
AI = [
    ('2023-08-02', 'exhibit9916302023.htm', 'earnings release (8-K Ex.99.1)', 'CEO quote', 100, 'count',
     'Cognizant Neuro AI platform "has helped drive more than 100 early engagements as clients embrace generative AI" (lower bound)'),
    ('2026-02-04', 'exhibit99312312025.htm', 'earnings supplement (8-K Ex.99.3)', 'slide 4: 2025 strategic objectives', 30, 'pct',
     '"Over 30% of code AI assisted" (2025; lower bound; company sampling estimate)'),
    ('2026-02-04', 'exhibit99312312025.htm', 'earnings supplement (8-K Ex.99.3)', 'slides 4-5: 2025 results', 260000, 'count',
     '"~260K employees skilled in gen AI" / "260K Employees AI trained" (2025, approximate)'),
    ('2026-04-29', 'exhibit9933312026.htm', 'earnings supplement (8-K Ex.99.3)', 'slide 3: Q1 2026 highlights', 5000, 'count',
     '"Over 5,000 AI engagements" (lower bound)'),
    ('2026-04-29', 'exhibit9933312026.htm', 'earnings supplement (8-K Ex.99.3)', 'slide 3: Q1 2026 highlights', 40, 'pct',
     '"Nearly 40% of code is AI assisted" (estimated based on company sampling methodology; upper bound approx.)'),
]
for fd, doc, desc, loc, v, unit, note in AI:
    m = next(x for x in man if x['filing_date'] == fd and x['doc'] == doc)
    y, q = prior_qend(fd)
    src = dict(url=m['url'], doc=f'Cognizant Q{q} {y} {desc}', date=fd)
    add(y, q, 'ai_disclosure', 'total', 'total', float(v), unit, 'na', 'point' if unit == 'count' and v > 1000 and 'employees' in note else ('annual' if '2025' in note else 'point'),
        src, loc, note + '; hand-entered')

# ---------------------------------------------------------------- 3. 10-Q / 10-K
for m in man:
    if m['form'] not in ('10-Q', '10-K'):
        continue
    t = get_text(m['local'])
    f = flat(t)
    rd = dt.date.fromisoformat(m['report_date'])
    y, q = q_of_date(rd)
    is10k = m['form'] == '10-K'
    src = dict(url=m['url'], doc=f'Cognizant {m["form"]} ' + (f'FY{y}' if is10k else f'Q{q} {y}'), date=m['filing_date'])
    lines = t.split('\n')
    # --- disaggregation table (2018+): take first table after 'Disaggregation of Revenues'
    i0 = next((i for i, l in enumerate(lines) if 'Disaggregation of Revenues' in l), None)
    if i0 is not None and y >= 2018:
        # find first 'Service line:' after i0
        blk_hdr = None
        for i in range(i0, min(i0 + 80, len(lines))):
            if re.search(r'(Three Months|Year) Ended|^\s*20\d\d\s*$|\(in millions\)', lines[i]) and blk_hdr is None:
                blk_hdr = i
            if lines[i].startswith('Service line'):
                svc = i; break
        hdr = ' '.join(lines[i0:svc])
        ok = True
        if not is10k and not re.search(rf'Three Months Ended \w+ \d+, {y}', hdr):
            print('WARN disagg hdr', m['local'], hdr[-300:]); ok = False
        if ok:
            pt = 'annual' if is10k else 'quarter'
            loc = 'Note 2 - Disaggregation of Revenues (total column)'
            for l in lines[svc + 1:svc + 12]:
                nm = re.sub(r'\s*\(\d\)\s*$', '', l.split('|')[0].strip())
                if nm in ('Consulting and technology services', 'Outsourcing services', 'Time and materials', 'Fixed-price', 'Transaction or volume-based'):
                    vals = [num(x) for x in re.findall(r'[\d,]+(?:\.\d+)?', ' '.join(l.split('|')[1:]))]
                    if len(vals) < 5:
                        print('WARN disagg', m['local'], l); continue
                    tot = vals[4]
                    if nm in ('Consulting and technology services', 'Outsourcing services'):
                        add(y, q, 'segment_revenue', nm, 'service_line', tot, 'USD_mn', 'reported', pt, src, loc)
                    else:
                        add(y, q, 'segment_revenue', nm, 'other', tot, 'USD_mn', 'reported', pt, src, loc, 'revenue by contract type')
                if l.startswith('Costs to') or l.startswith('Cognizant'):
                    break
    # --- service-line text (pre-2018)
    for mm in re.finditer(r'Our (consulting and technology services|outsourcing services) revenues? for the (three|six|nine|twelve) months ended (\w+ \d{1,2}, \d{4}) (?:increased|grew) by (?:approximately )?(\d+\.\d)%(?: compared to the (?:three|six|nine|twelve) months ended \w+ \d{1,2}, \d{4})? and (?:represented|constituted) (?:approximately )?(\d+\.\d)% of total revenues', f):
        per = mm.group(2)
        if per in ('six', 'nine'):
            continue
        pt = 'quarter' if per == 'three' else 'annual'
        nm = 'Consulting and technology services' if mm.group(1).startswith('consulting') else 'Outsourcing services'
        d = parse_date(mm.group(3)); py, pq = q_of_date(d)
        add(py, pq, 'revenue_share', nm, 'service_line', float(mm.group(5)), 'pct', 'reported', pt, src, 'MD&A - Revenues', 'approximate')
        add(py, pq, 'segment_growth_yoy', nm, 'service_line', float(mm.group(4)), 'pct', 'reported', pt, src, 'MD&A - Revenues', 'approximate')
    for mm in re.finditer(r'Our (consulting and technology services|outsourcing services) revenues? (?:for|in) (\d{4}) (?:increased|grew) by (?:approximately )?(\d+\.\d)%[^.]*?(?:represented|constituted) (?:approximately )?(\d+\.\d)% of', f):
        nm = 'Consulting and technology services' if mm.group(1).startswith('consulting') else 'Outsourcing services'
        py = int(mm.group(2))
        if not is10k or py != y:
            continue
        add(py, 4, 'revenue_share', nm, 'service_line', float(mm.group(4)), 'pct', 'reported', 'annual', src, 'MD&A - Revenues', 'approximate')
        add(py, 4, 'segment_growth_yoy', nm, 'service_line', float(mm.group(3)), 'pct', 'reported', 'annual', src, 'MD&A - Revenues', 'approximate')
    # --- fixed-price share
    for mm in re.finditer(r'Fixed-price contracts accounted for approximately (\d+\.\d)% of our revenues for the (three|six|nine|twelve|12) months ended (\w+ \d{1,2}, \d{4})|Fixed-price contracts accounted for approximately (\d+\.\d)% of our revenues for the year ended (\w+ \d{1,2}, \d{4})', f):
        if mm.group(1):
            v, per, d = float(mm.group(1)), mm.group(2), parse_date(mm.group(3))
        else:
            v, per, d = float(mm.group(4)), 'twelve', parse_date(mm.group(5))
        pt = {'three': 'quarter', 'six': 'ytd', 'nine': 'ytd', 'twelve': 'annual', '12': 'annual'}[per]
        py, pq = q_of_date(d)
        add(py, pq, 'revenue_share_fixed_price', 'total', 'total', v, 'pct', 'reported', pt, src, 'MD&A / Risk factors', 'approximate')
    # --- active & strategic clients
    mm = re.search(r'We had approximately ([\d,]+) active clients as of,? (\w+ ?,? \d{1,2}, \d{4})', f.replace('March,', 'March'))
    if mm:
        d = parse_date(mm.group(2).replace(' ,', ','))
        py, pq = q_of_date(d)
        add(py, pq, 'active_clients', 'total', 'total', num(mm.group(1)), 'count', 'na', 'point', src, 'MD&A - Overview', 'approximate')
    mm = re.search(r'total number of our strategic clients to (\d+)', f)
    if mm:
        add(y, q, 'clients_bucket', 'strategic clients', 'client_bucket', float(mm.group(1)), 'count', 'na', 'point', src, 'MD&A - Overview',
            'Cognizant-defined "strategic client": potential to generate at least $5mn to $50mn or more in annual revenues at maturity')
    # --- top 5 / top 10 client share (current period only)
    for mm in re.finditer(r'Revenues from our top (five|ten) customers as a percentage of total revenues were (\d+\.\d)% and (\d+\.\d)% for the (three months|quarters|nine months|six months|years) ended (\w+ \d{1,2},? \d{4}|\w+ \d{1,2})', f):
        per = mm.group(4)
        if per in ('nine months', 'six months'):
            continue
        pt = 'annual' if per == 'years' else 'quarter'
        add(y, q, 'revenue_share', f'Top {"5" if mm.group(1) == "five" else "10"} clients', 'client_bucket', float(mm.group(2)), 'pct',
            'reported', pt, src, 'MD&A - Revenues', '')
    # --- 10-K headcount by location
    if is10k:
        mm = re.search(r'(?:We had approximately|As of December 31, \d{4}, we had approximately) ([\d,]+) employees(?: at the end of (\d{4}))?\s*,?\s*with ([^.]*?)(?:\.\s)', f)
        if mm:
            tot = num(mm.group(1)); body = mm.group(3)
            add(y, 4, 'headcount', 'total', 'total', tot, 'count', 'na', 'point', src, 'Item 1 - Employees/Workforce', 'approximate; 10-K year-end')
            for part in re.finditer(r'(?:approximately )?([\d,]+) (?:persons |employees )?in (?:the )?([A-Z][A-Za-z ]+?)(?: region)?(?=,| and |$)', body):
                loc_name = part.group(2).strip()
                loc_name = {'North American': 'North America', 'European': 'Europe'}.get(loc_name, loc_name)
                if loc_name.startswith('various other locations'):
                    continue
                add(y, 4, 'headcount', loc_name, 'geography', num(part.group(1)), 'count', 'na', 'point', src,
                    'Item 1 - Employees/Workforce', 'employees by location (as reported, approximate)')
            mm2 = re.search(r'([\d,]+) (?:persons )?in various other locations throughout the rest of (?:the )?world', body)
            if mm2:
                add(y, 4, 'headcount', 'Rest of World (other locations)', 'geography', num(mm2.group(1)), 'count', 'na', 'point', src,
                    'Item 1 - Employees/Workforce', 'employees in "various other locations throughout the rest of the world"' +
                    (' (includes India)' if y < 2022 else ' (excludes India, reported separately)'))

# ---------------------------------------------------------------- write
cols = ['firm', 'fiscal_q', 'period_end', 'cal_q', 'metric', 'dimension', 'dim_type', 'value', 'unit', 'basis', 'period_type',
        'source_url', 'source_doc', 'source_loc', 'doc_date', 'notes']
for r in rows:  # keep the Tech-Services-scoped attrition series separate from company-wide series
    if r['metric'] == 'attrition' and 'Tech Services' in r['notes']:
        r['dimension'], r['dim_type'] = 'Tech Services', 'other'
rows.sort(key=lambda r: (r['fiscal_q'], r['metric'], r['dim_type'], r['dimension'], r['basis'], r['period_type'], r['doc_date']))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=cols, quoting=csv.QUOTE_MINIMAL)
    w.writeheader(); w.writerows(rows)
print('rows', len(rows))
