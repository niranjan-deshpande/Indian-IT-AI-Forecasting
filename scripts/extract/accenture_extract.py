"""Accenture extraction: builds data/raw/accenture.csv from local copies of
SEC EDGAR earnings releases (8-K Ex.99), 10-Q/10-K filings and company-hosted
call transcripts saved under data/sources/accenture/.

Steps (run the download/convert snippets documented in data/raw/accenture_NOTES.md first):
  8k/*.htm  -> txt/*.txt (table rows as '| a | b |') and flat/*.txt (whitespace-collapsed)
  10q/*.htm -> txt/*.txt, flat/*.txt
"""
import re, json, os, glob, calendar, csv
from datetime import date

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'data', 'sources', 'accenture')
OUT = os.path.join(ROOT, 'data', 'raw', 'accenture.csv')

URLS = {}
URLS.update(json.load(open(os.path.join(SRC, '8k_urls.json'))))
URLS.update(json.load(open(os.path.join(SRC, '10q_urls.json'))))

COLS = ['firm', 'fiscal_q', 'period_end', 'cal_q', 'metric', 'dimension', 'dim_type', 'value', 'unit',
        'basis', 'period_type', 'source_url', 'source_doc', 'source_loc', 'doc_date', 'notes']
rows = []

QN = {'first': 1, 'second': 2, 'third': 3, 'fourth': 4}


def qinfo(fy, q):
    """Accenture fiscal quarter -> (fiscal_q, period_end, cal_q)."""
    if q == 1:
        y, m = fy - 1, 11
    else:
        y, m = fy, {2: 2, 3: 5, 4: 8}[q]
    d = calendar.monthrange(y, m)[1]
    pe = date(y, m, d)
    calq = f"{y}Q{(m - 1) // 3 + 1}"
    return f"Q{q}FY{fy % 100:02d}", pe.isoformat(), calq


def filing_q(doc_date):
    """Quarter reported in a filing, from filing date (Dec->Q1, Mar->Q2, Jun->Q3, Sep/Oct->Q4)."""
    y, m = int(doc_date[:4]), int(doc_date[5:7])
    if m == 12:
        return y + 1, 1
    if m in (3, 4):
        return y, 2
    if m in (6, 7):
        return y, 3
    if m in (9, 10, 11):
        return y, 4
    if m in (1,):
        return y, 1
    raise ValueError(doc_date)


def add(fy, q, metric, dimension, dim_type, value, unit, basis, period_type, key, source_doc, source_loc,
        doc_date, notes='', annual=False):
    if annual:
        fq, pe, cq = f"FY{fy % 100:02d}", date(fy, 8, 31).isoformat(), f"{fy}Q3"
    else:
        fq, pe, cq = qinfo(fy, q)
    rows.append(dict(firm='accenture', fiscal_q=fq, period_end=pe, cal_q=cq, metric=metric, dimension=dimension,
                     dim_type=dim_type, value=value, unit=unit, basis=basis, period_type=period_type,
                     source_url=URLS[key], source_doc=source_doc, source_loc=source_loc, doc_date=doc_date,
                     notes=notes))


def num(tok):
    tok = tok.strip()
    if tok in ('—', '-', '–'):
        return 0.0
    if tok.lower() in ('n/m', 'nm'):
        return None
    neg = tok.startswith('-')
    tok = tok.lstrip('-').replace(',', '')
    try:
        v = float(tok)
    except ValueError:
        return 'X'
    return -v if neg else v


SECTION = [(r'OPERATING GROUPS|INDUSTRY GROUPS', 'vertical'),
           (r'GEOGRAPHY|GEOGRAPHIC MARKETS|GEOGRAPHIC REGIONS', 'geography'),
           (r'TYPE OF WORK', 'service_line')]


def parse_release_table(txtfile):
    """Return list of (dim_type, label, footnote_marks, [values]) for the three-months Summary of Revenues."""
    lines = open(txtfile).read().split('\n')
    start = None
    for i, l in enumerate(lines):
        if re.search(r'summary of revenues', l, re.I):
            start = i
            break
    out, foot = [], []
    sec = None
    started = False
    for l in lines[start + 1:]:
        s = l.strip()
        if started and re.search(r'(Nine|Six) Months Ended|Year Ended|Twelve Months Ended|OPERATING INCOME BY|'
                                 r'Operating Income by|CONSOLIDATED BALANCE|Consolidated Balance', s):
            break
        if not s.startswith('|'):
            if started and s:
                foot.append(s)
            continue
        cells = [c.strip() for c in s.strip('|').split('|')]
        cells = [c for c in cells if c != '']
        if not cells:
            continue
        head = re.sub(r'\s*\(\d\)\s*', '', cells[0]).strip()
        matched = False
        for pat, dt in SECTION:
            if len(cells) == 1 and re.fullmatch(pat, head, re.I):
                sec = dt
                started = True
                matched = True
        if matched or sec is None or len(cells) < 3:
            if started and len(cells) == 1 and len(foot) < 40:
                foot.append(cells[0])
            continue
        label = cells[0]
        marks = re.findall(r'\((\d)\)', label)
        label = re.sub(r'\s*\(\d\)\s*', ' ', label).strip().replace("\xa0", " ")
        txt = ' '.join(cells[1:]).replace('$', ' ').replace('%', ' ')
        txt = re.sub(r'\(\s*([\d,.]+)\s*\)', r'-\1', txt)
        txt = re.sub(r'\(\s*([\d,.]+)', r'-\1', txt).replace(')', ' ')
        vals = [num(t) for t in txt.split()]
        vals = [v for v in vals if v != 'X']
        out.append((sec, label, marks, vals))
    return out, ' '.join(foot)


def structure_note(dt, fy, q):
    """Segment-structure context, taken from the release footnotes (see NOTES)."""
    k = fy * 10 + q
    if dt == 'geography':
        if fy <= 2017:
            return 'Geographic regions pre-FY18 composition.'
        if fy <= 2019:
            return ('Effective Sep 1 2017 regions revised: North America (US & Canada), Europe, Growth Markets '
                    '(Asia Pacific, Latin America, Africa, Middle East, Turkey).')
        if fy <= 2023:
            return 'Effective Sep 1 2019 one country moved from Growth Markets to Europe (prior periods reclassified).'
        if fy == 2024:
            return ('Effective Sep 1 2023 Middle East & Africa moved from Growth Markets to Europe; Europe renamed EMEA '
                    '(prior periods reclassified).')
        return ('Q1FY25: Latin America moved from Growth Markets to North America -> "Americas"; Growth Markets -> '
                '"Asia Pacific" (prior periods reclassified).')
    if dt == 'vertical':
        n = 'Operating groups incl. "Other" line (pre-FY21).' if fy <= 2020 else \
            'Effective Sep 1 2020 "Other" folded into industry groups (prior periods reclassified).'
        if k >= 20224:
            n += ' Effective Jun 1 2022 Aerospace & Defense moved from CMT to Products (prior periods reclassified).'
        return n
    if dt == 'service_line':
        return 'Managed Services = previously "Outsourcing" (renamed Q1FY23).' if fy >= 2023 else ''
    return ''


def release_docname(fy, q):
    return f"Accenture Q{q}FY{fy % 100:02d} earnings release (8-K Ex.99)"


def do_releases():
    for fn in sorted(glob.glob(os.path.join(SRC, '8k', '*.htm'))):
        base = os.path.basename(fn)
        key = f"8k/{base}"
        doc_date = base[:10]
        fy, q = filing_q(doc_date)
        docname = release_docname(fy, q)
        txt = os.path.join(SRC, 'txt', base.replace('.htm', '.txt'))
        flat = open(os.path.join(SRC, 'flat', base.replace('.htm', '.txt'))).read()
        table, foot = parse_release_table(txt)
        foot = re.sub(r'\s+', ' ', foot)[:600]
        pre606 = fy < 2019
        loc = 'Summary of Revenues (three months)'
        first_total_done = False
        for sec, label, marks, vals in table:
            is_total = label.lower().startswith('total')
            fnote = (' Footnote in table: ' + foot) if (marks and foot) else ''
            if is_total:
                if label.upper() == 'TOTAL REVENUES' and pre606:
                    # gross revenues incl. reimbursements (pre ASC 606)
                    add(fy, q, 'revenue', 'Revenues incl. reimbursements', 'other', vals[0] / 1000, 'USD_mn',
                        'reported', 'quarter', key, docname, loc, doc_date,
                        'Pre-ASC 606 gross revenues including reimbursements; headline "revenue" row uses net revenues.')
                    continue
                if first_total_done:
                    continue
                first_total_done = True
                note = ('Net revenues (revenues before reimbursements), the pre-FY19 headline measure.' if pre606
                        else 'Revenues (post ASC 606; includes reimbursements).')
                add(fy, q, 'revenue', 'total', 'total', vals[0] / 1000, 'USD_mn', 'reported', 'quarter', key,
                    docname, loc, doc_date, note)
                pfy = fy - 1
                add(pfy, q, 'revenue', 'total', 'total', vals[1] / 1000, 'USD_mn', 'reported', 'quarter', key,
                    docname, loc + ' prior-year column', doc_date,
                    'Prior-year comparative as presented in this later release (may be revised). ' + note)
                if len(vals) >= 4:
                    add(fy, q, 'revenue_growth_yoy', 'total', 'total', vals[2], 'pct', 'reported', 'quarter', key,
                        docname, loc, doc_date, 'USD growth vs prior-year quarter as reported in table (rounded).')
                    add(fy, q, 'revenue_growth_yoy', 'total', 'total', vals[3], 'pct', 'cc', 'quarter', key,
                        docname, loc, doc_date,
                        'Local-currency growth (restating current period at prior-year FX rates), as reported in table.')
                continue
            if label.lower() == 'reimbursements':
                add(fy, q, 'segment_revenue', 'Reimbursements', 'other', vals[0] / 1000, 'USD_mn', 'reported',
                    'quarter', key, docname, loc, doc_date, 'Pre-ASC 606 reimbursements line.')
                continue
            notes = ('Segment of net revenues (pre-ASC 606). ' if pre606 else '') + structure_note(sec, fy, q)
            add(fy, q, 'segment_revenue', label, sec, vals[0] / 1000, 'USD_mn', 'reported', 'quarter', key, docname,
                loc, doc_date, notes.strip())
            add(fy - 1, q, 'segment_revenue', label, sec, vals[1] / 1000, 'USD_mn', 'reported', 'quarter', key,
                docname, loc + ' prior-year column', doc_date,
                ('Prior-year comparative as presented in this later release (restated/reclassified to current '
                 'structure where applicable). ' + notes).strip())
            if len(vals) >= 4 and vals[2] is not None:
                add(fy, q, 'segment_growth_yoy', label, sec, vals[2], 'pct', 'reported', 'quarter', key, docname,
                    loc, doc_date, notes.strip())
            if len(vals) >= 4 and vals[3] is not None:
                add(fy, q, 'segment_growth_yoy', label, sec, vals[3], 'pct', 'cc', 'quarter', key, docname, loc,
                    doc_date, ('Local currency. ' + notes).strip())

        # ---- bookings (quarter) ----
        qword = [k for k, v in QN.items() if v == q][0]
        m = re.search(r'New bookings (?:for the (?:%s )?quarter[^$]{0,40}?|in the (?:%s )?quarter[^$]{0,40}?)'
                      r'(?:were|was|of) (?:a )?(?:record )?\$\s?([\d.]+) billion([^.]*(?:\.\d[^.]*)*)' % (qword, qword), flat, re.I)
        if m:
            val = float(m.group(1))
            add(fy, q, 'bookings', 'total', 'total', val * 1000, 'USD_mn', 'reported', 'quarter', key, docname,
                'Financial review: New Bookings', doc_date,
                'Total new bookings; reported in $ billions (' + m.group(1) + ').')
            tail = flat[m.end(1):m.end(1) + 300]
            tail = re.split(r'\.\s+[A-Z\u2022\u25aa]', tail)[0]
            if not re.search(r'in (?:both )?U\.?S\.? dollars|in local currency', tail):
                hb = re.search(r'New bookings (?:are|of|were) (?:a )?(?:record )?\$\s?[\d.]+ billion', flat)
                if hb:
                    tail = re.split(r'\u2022|\u25aa|--|\u2014|Generative AI|\.\s+[A-Z]', flat[hb.end():hb.end() + 250])[0]
            sign = -1 if re.search(r'\bdecrease', tail, re.I) else 1
            both = re.search(r'([\d.]+)\s?(?:%|percent) (?:increase |decrease )?in both U\.?S\.? dollars and local currency', tail, re.I)
            usd = re.search(r'([\d.]+)\s?(?:%|percent) (?:increase |decrease )?in U\.?S\.? dollars', tail, re.I)
            lc = re.search(r'(?:([\d.]+)\s?(?:%|percent)|(flat)) in local currency', tail, re.I)
            gr = {}
            if both:
                gr = {'reported': float(both.group(1)), 'cc': float(both.group(1))}
            else:
                if usd:
                    gr['reported'] = float(usd.group(1))
                if lc:
                    gr['cc'] = 0.0 if lc.group(2) else float(lc.group(1))
            for b_, v in gr.items():
                add(fy, q, 'bookings_growth_yoy', 'total', 'total', sign * v if v else 0.0, 'pct', b_, 'quarter', key,
                    docname, 'Financial review: New Bookings', doc_date,
                    'YoY growth of total new bookings as stated: "' + tail.strip()[:160] + '"')
        for lab, pat in [('Consulting', r'Consulting (?:and outsourcing )?(?:new )?bookings (?:for the quarter )?were (?:each )?(?:a )?(?:record )?\$\s?([\d.]+) billion'),
                         ('Outsourcing / Managed Services',
                          r'(Outsourcing|Managed [Ss]ervices|[Cc]onsulting and outsourcing) (?:new )?bookings (?:for the quarter )?were (?:each )?(?:a )?(?:record )?\$\s?([\d.]+) billion')]:
            mm = re.search(pat, flat)
            if mm:
                v = float(mm.group(mm.lastindex))
                dim = lab if lab == 'Consulting' else mm.group(1).replace('services', 'Services')
                if dim.lower().startswith('consulting and'):
                    dim = 'Outsourcing'
                add(fy, q, 'bookings', dim, 'service_line', v * 1000, 'USD_mn', 'reported', 'quarter', key, docname,
                    'Financial review: New Bookings', doc_date,
                    f'New bookings by type of work; reported in $ billions ({mm.group(mm.lastindex)}). '
                    'First match in release = quarterly figure.')

        # ---- utilization / attrition in releases (FY15-FY16 only) ----
        mu = re.search(r'Utilization for (?:the (?:fourth )?quarter|the fourth quarter of fiscal \d{4})[^.]*? was (\d+) percent', flat)
        if mu:
            add(fy, q, 'utilization_incl_trainees', 'total', 'total', float(mu.group(1)), 'pct', 'na', 'quarter',
                key, docname, 'Financial review text', doc_date,
                'Accenture "utilization" (company-wide; Accenture does not state trainee treatment). Mapped to '
                'utilization_incl_trainees by convention.')
        ma = re.search(r'Attrition for (?:the (?:first|second|third|fourth) quarter of fiscal \d{4}|the quarter) was (\d+) percent', flat)
        if ma:
            add(fy, q, 'attrition', 'total', 'total', float(ma.group(1)), 'pct', 'na', 'quarter', key, docname,
                'Financial review text', doc_date, 'Quarterly attrition as stated in release (annualized voluntary, '
                'excl. involuntary terminations per 10-Q definition).')
        # ---- boilerplate headcount ----
        mh = re.search(r'(approximately|more than|nearly|over) ([\d,]{6,7}) (?:people|employees)', flat)
        if mh:
            add(fy, q, 'headcount', 'total (press-release boilerplate, rounded)', 'other',
                float(mh.group(2).replace(',', '')), 'count', 'na', 'point', key, docname,
                'About Accenture boilerplate', doc_date,
                f'Boilerplate says "{mh.group(1)} {mh.group(2)} people"; rounded and possibly not as of quarter end. '
                'Prefer 10-Q/10-K headcount (dimension total).')


def do_filings():
    for fn in sorted(glob.glob(os.path.join(SRC, '10q', '*.htm'))):
        base = os.path.basename(fn)
        key = f"10q/{base}"
        doc_date = base[:10]
        form = base[11:15]
        fy, q = filing_q(doc_date)
        docname = f"Accenture {form} Q{q}FY{fy % 100:02d}" if form == '10-Q' else f"Accenture 10-K FY{fy % 100:02d}"
        t = open(os.path.join(SRC, 'flat', base.replace('.htm', '.txt'))).read()
        t = re.sub(r'\d+ Table of Contents ', '', t)
        loc = 'MD&A - Overview / People metrics'
        # headcount
        m = re.search(r'(?:headcount|workforce), the majority of which serves? our clients,[^.]*? (?:to|was) '
                      r'(approximately|more than) ([\d,]+) as of ([A-Z][a-z]+ \d+, \d{4})', t)
        if not m:
            m = re.search(r'we employed (approximately) ([\d,]+) people', t) or \
                re.search(r'(approximately) ([\d,]+) employees worldwide', t)
        if m:
            add(fy, q, 'headcount', 'total', 'total', float(m.group(2).replace(',', '')), 'count', 'na', 'point', key,
                docname, loc, doc_date,
                f'"{m.group(1)} {m.group(2)}" - total workforce ("the majority of which serve our clients"); '
                'includes all employees (client-facing and support).')
        # utilization quarterly
        qword = [k for k, v in QN.items() if v == q][0]
        m = re.search(r'Utilization for the %s quarter of fiscal \d{4} was (\d+)%%' % qword, t)
        if m:
            add(fy, q, 'utilization_incl_trainees', 'total', 'total', float(m.group(1)), 'pct', 'na', 'quarter', key,
                docname, loc, doc_date,
                'Accenture company-wide "utilization"; trainee treatment not specified - mapped to '
                'utilization_incl_trainees by convention.')
        m = re.search(r'Utilization for fiscal (\d{4}) was (\d+)%', t)
        if m and form == '10-K':
            add(int(m.group(1)), 4, 'utilization_incl_trainees', 'total', 'total', float(m.group(2)), 'pct', 'na',
                'annual', key, docname, loc, doc_date,
                'Full fiscal-year utilization (Q4-only figure not disclosed in this 10-K).', annual=True)
        # attrition quarterly
        m = re.search(r'(?:Annualized attrition, excluding involuntary terminations, for the %s quarter of fiscal \d{4} was'
                      r'|Attrition, excluding involuntary terminations, for the %s quarter of fiscal \d{4} was'
                      r'|For the %s quarter of fiscal \d{4}, (?:annualized )?attrition, excluding involuntary terminations, was)'
                      r' (\d+)%%' % (qword, qword, qword), t)
        if m:
            add(fy, q, 'attrition', 'total', 'total', float(m.group(1)), 'pct', 'na', 'quarter', key, docname, loc,
                doc_date, 'Voluntary attrition (excluding involuntary terminations); ' +
                ('stated as "annualized".' if 'nnualized' in m.group(0) else
                 'wording omits "annualized" but it is a quarterly rate on the same basis (10-Q people metrics).'))
        m = re.search(r'(?:Attrition|attrition), excluding involuntary terminations, for fiscal (\d{4}) was (\d+)%|'
                      r'For fiscal (\d{4}), attrition, excluding involuntary terminations, was (\d+)%', t)
        if m and form == '10-K':
            y = int(m.group(1) or m.group(3)); v = float(m.group(2) or m.group(4))
            add(y, 4, 'attrition', 'total', 'total', v, 'pct', 'na', 'annual', key, docname, loc, doc_date,
                'Full fiscal-year voluntary attrition (excl. involuntary terminations).', annual=True)


# ---- hand-entered AI disclosures (releases & company-hosted transcripts) ----
TR = {l.split()[0]: l.split()[1] for l in open(os.path.join(SRC, 'transcripts', 'urls.txt')) if l.strip()}


def do_ai():
    rel = {os.path.basename(k)[:10]: k for k in URLS if k.startswith('8k/')}
    items = [
        # (fy,q, dimension, value USD_mn, period_type, src_type, src_key, doc_date, note)
        (2023, 4, 'GenAI new bookings', 200, 'quarter', 'tr', 'Q4FY23', '2023-09-28',
         'Transcript: "another approximately $200 million in gen AI sales" in Q4 FY23. Hand-entered.'),
        (2023, 4, 'GenAI new bookings', 300, 'annual', 'tr', 'Q4FY23', '2023-09-28',
         'Transcript: "total to over $300 million for the year" (FY23 gen AI sales); release says $300M in last six months. Hand-entered.'),
        (2024, 1, 'GenAI new bookings', 450, 'quarter', 'rel', '2023-12-19', '2023-12-19',
         'Release CEO quote: "over $450 million in new bookings" in Gen AI. Value is a floor ("over"). Hand-entered.'),
        (2024, 2, 'GenAI new bookings', 600, 'quarter', 'rel', '2024-03-21', '2024-03-21',
         'Release: "Generative AI new bookings of over $600 million in the quarter for a total of $1.1 billion through the first half". Floor. Hand-entered.'),
        (2024, 2, 'GenAI new bookings', 1100, 'ytd', 'rel', '2024-03-21', '2024-03-21',
         'Release: $1.1 billion H1 FY24 GenAI new bookings. Hand-entered.'),
        (2024, 3, 'GenAI new bookings', 900, 'quarter', 'rel', '2024-06-20', '2024-06-20',
         'Release: "Generative AI new bookings of over $900 million for a total of $2 billion fiscal year-to-date". Floor. Hand-entered.'),
        (2024, 3, 'GenAI new bookings', 2000, 'ytd', 'rel', '2024-06-20', '2024-06-20',
         'Release: $2 billion FY24 YTD GenAI new bookings. Hand-entered.'),
        (2024, 3, 'GenAI revenue', 500, 'ytd', 'rel', '2024-06-20', '2024-06-20',
         'Release CEO quote: "$500 million in revenue year-to-date" from Generative AI (9M FY24). Hand-entered.'),
        (2023, 4, 'GenAI revenue', 100, 'annual', 'tr', 'Q3FY24', '2024-06-20',
         'Q3FY24 transcript: "roughly $100 million in revenue from GenAI in FY23". Hand-entered.'),
        (2024, 4, 'GenAI new bookings', 1000, 'quarter', 'rel', '2024-09-26', '2024-09-26',
         'Release: "Generative AI new bookings of $1 billion for the quarter and $3 billion for the full year". Hand-entered.'),
        (2024, 4, 'GenAI new bookings', 3000, 'annual', 'rel', '2024-09-26', '2024-09-26',
         'Release: $3 billion FY24 GenAI new bookings. Hand-entered.'),
        (2024, 4, 'GenAI revenue', 900, 'annual', 'tr', 'Q4FY24', '2024-09-26',
         'Transcript: "for the full fiscal year, we had nearly $900 million in revenue" (GenAI). Approximate ("nearly"). Hand-entered.'),
        (2025, 1, 'GenAI new bookings', 1200, 'quarter', 'rel', '2024-12-19', '2024-12-19',
         'Release: "Generative AI new bookings of $1.2 billion". Hand-entered.'),
        (2025, 1, 'GenAI revenue', 500, 'quarter', 'tr', 'Q1FY25', '2024-12-19',
         'Transcript: "$1.2 billion in new bookings and approximately $500 million in revenue" (GenAI). Approximate. Hand-entered.'),
        (2025, 2, 'GenAI new bookings', 1400, 'quarter', 'rel', '2025-03-20', '2025-03-20',
         'Release: "Generative AI new bookings of $1.4 billion". Hand-entered.'),
        (2025, 2, 'GenAI revenue', 600, 'quarter', 'tr', 'Q2FY25', '2025-03-20',
         'Transcript: "$1.4 billion in new bookings and approximately $600 million in revenue" (Gen AI). Approximate. Hand-entered.'),
        (2025, 2, 'GenAI revenue', 1100, 'ytd', 'tr', 'Q2FY25', '2025-03-20',
         'Transcript (Q&A, CEO): "in H1, we did $1.1 billion in revenue" (Gen AI). Hand-entered.'),
        (2025, 3, 'GenAI new bookings', 1500, 'quarter', 'rel', '2025-06-20', '2025-06-20',
         'Release: "Generative AI new bookings of $1.5 billion". Hand-entered.'),
        (2025, 3, 'GenAI new bookings', 4100, 'ytd', 'tr', 'Q3FY25', '2025-06-20',
         'Transcript: "Q3 year-to-date GenAI bookings to a total of $4.1 billion". Hand-entered.'),
        (2025, 3, 'GenAI revenue', 700, 'quarter', 'tr', 'Q3FY25', '2025-06-20',
         'Transcript: "$1.5 billion in bookings and over $700 million in revenues" (GenAI). Floor ("over"). Hand-entered.'),
        (2025, 3, 'GenAI revenue', 1800, 'ytd', 'tr', 'Q3FY25', '2025-06-20',
         'Transcript: "revenue to $1.8 billion" (GenAI, 9M FY25). Hand-entered.'),
        (2025, 4, 'GenAI new bookings', 1800, 'quarter', 'rel', '2025-09-25', '2025-09-25',
         'Release: "Generative AI new bookings of $1.8 billion for the quarter and $5.9 billion for the year". Hand-entered.'),
        (2025, 4, 'GenAI new bookings', 5900, 'annual', 'rel', '2025-09-25', '2025-09-25',
         'Release: $5.9 billion FY25 GenAI new bookings. Transcript clarifies scope = "advanced AI" (Gen AI, agentic AI, physical AI; excludes data, classical AI, AI used in delivery). Hand-entered.'),
        (2025, 4, 'GenAI revenue', 2700, 'annual', 'tr', 'Q4FY25', '2025-09-25',
         'Transcript: "In FY25, we tripled our revenue over FY24 from Gen AI and increasingly agentic AI to $2.7 billion". Hand-entered.'),
        (2026, 1, 'Advanced AI new bookings', 2200, 'quarter', 'rel', '2025-12-18', '2025-12-18',
         'Release: "Advanced AI new bookings of $2.2 billion". Label changed from Generative AI to Advanced AI (Gen AI, agentic AI, physical AI; excludes data, classical AI, RPA). Hand-entered.'),
        (2026, 1, 'Advanced AI revenue', 1100, 'quarter', 'tr', 'Q1FY26', '2025-12-18',
         'Transcript: "Revenue reached another milestone this quarter at approximately $1.1 billion" (advanced AI). Approximate. Hand-entered.'),
        (2026, 1, 'Advanced AI new bookings (cumulative since Q3FY23)', 11500, 'ytd', 'tr', 'Q1FY26', '2025-12-18',
         'Transcript: "To date, we have now delivered approximately $11.5 billion in bookings across 11,000 projects, with revenue of $4.8 billion." Cumulative since metric introduced in Q3 FY23 (period_type ytd used loosely = cumulative). Hand-entered.'),
        (2026, 1, 'Advanced AI revenue (cumulative since Q3FY23)', 4800, 'ytd', 'tr', 'Q1FY26', '2025-12-18',
         'Transcript: cumulative advanced AI revenue of $4.8 billion since Q3 FY23 (period_type ytd used loosely = cumulative). Company said Q1FY26 is "the last quarter in which we share these specific metrics". Hand-entered.'),
    ]
    for fy, q, dim, val, pt, st, sk, dd, note in items:
        annual = pt == 'annual'
        if st == 'rel':
            key = rel[sk]
            doc = release_docname(*filing_q(sk))
            loc = 'Headline key metrics / CEO quote'
        else:
            URLS['tr:' + sk] = TR[sk]
            key = 'tr:' + sk
            tfy, tq = int('20' + sk[-2:]), int(sk[1])
            doc = f"Accenture Q{tq}FY{sk[-2:]} earnings call transcript (company-hosted)"
            loc = 'Prepared remarks / Q&A'
        add(fy, q, 'ai_disclosure', dim, 'other', val, 'USD_mn', 'reported', pt, key, doc, loc, dd, note,
            annual=annual)


# ---- People-metrics tables in company-hosted supporting materials / earnings presentations ----
PRES = {l.split()[0]: l.split()[1] for l in open(os.path.join(SRC, 'presentations', 'urls.txt')) if l.strip()}
PRES_DOCS = {  # file stem -> (doc label, doc_date)
    'Q2FY2015_opmetrics': ('Accenture Q2FY15 Operational Metrics (IR supporting PDF)', '2015-03-26'),
    'Q3FY16_supporting': ('Accenture Q3FY16 Supporting Materials (IR PDF)', '2016-06-23'),
    'Q4FY17_supporting': ('Accenture Q4FY17 Supporting Materials (IR PDF)', '2017-09-28'),
    'Q4FY19_supporting': ('Accenture Q4FY19 Supporting Materials (IR PDF)', '2019-09-26'),
    'Q2FY21_supporting': ('Accenture Q2FY21 Supporting Materials (IR PDF)', '2021-03-18'),
    'Q4FY21_supporting': ('Accenture Q4FY21 Supporting Materials (IR PDF)', '2021-09-23'),
    'Q4FY22_supporting': ('Accenture Q4FY22 Supporting Materials (IR PDF)', '2022-09-22'),
    'Q4FY23_supporting': ('Accenture Q4FY23 Supporting Materials (IR PDF)', '2023-09-28'),
    'Q4FY24_supporting': ('Accenture Q4FY24 Supporting Materials (IR PDF)', '2024-09-26'),
    'Q4FY25_pres': ('Accenture Q4FY25 Earnings Presentation (IR PDF)', '2025-09-25'),
    'Q3FY26': ('Accenture Q3FY26 Earnings Presentation (IR PDF)', '2026-06-18'),
}
ROWMAP = [
    (r'^Billable$', 'headcount', 'Billable', 'other'),
    (r'^Non-Billable$', 'headcount', 'Non-Billable', 'other'),
    (r'^Total Accenture Employees$', 'headcount', 'total', 'total'),
    (r"^Accenture's Global Delivery Network$", 'headcount', 'Global Delivery Network', 'other'),
    (r"^(Accenture's )?Utilization$", 'utilization_incl_trainees', 'total', 'total'),
    (r"^(Quarterly Voluntary Attrition - Annualized|Accenture's Attrition)$", 'attrition', 'total', 'total'),
    (r'^Annual Voluntary Attrition$', 'attrition_annual', 'total', 'total'),
]


def date_to_fq(ds):
    m, d, y = [int(x) for x in ds.split('/')]
    y += 2000
    q = {11: 1, 2: 2, 5: 3, 8: 4}[m]
    fy = y + 1 if m == 11 else y
    return fy, q


def do_people_tables():
    for stem, (docname, doc_date) in PRES_DOCS.items():
        URLS['pres:' + stem] = PRES[stem]
        key = 'pres:' + stem
        lines = open(os.path.join(SRC, 'presentations', stem + '.txt')).read().split('\n')
        i0 = [i for i, l in enumerate(lines) if re.search(r'HEADCOUNT TREND|PEOPLE METRICS|^People Metrics', l.strip())][0]
        block = lines[i0:i0 + 45]
        dates = None
        notes_txt = ' '.join(l.strip() for l in block if l.strip())
        notes_txt = notes_txt[notes_txt.find('Notes:'):][:500] if 'Notes:' in notes_txt else ''
        for l in block:
            ds = re.findall(r'\b\d{1,2}/\d{2}/\d{2}\b', l)
            if len(ds) >= 6 and dates is None:
                dates = ds
                continue
            if dates is None:
                continue
            mm = re.match(r'\s*([A-Za-z\' -]+?)\s{2,}(.*)$', l)
            if not mm:
                continue
            label, rest = mm.group(1).strip(), mm.group(2)
            vals = re.findall(r'-?[\d,]+(?:\.\d+)?', rest.replace('%', ' ').replace('(1)', '').replace('(2)', ''))
            for pat, metric, dim, dt in ROWMAP:
                if not re.match(pat, label):
                    continue
                if metric == 'attrition_annual':
                    augs = [d for d in dates if d.startswith('8/31')]
                    for d, v in zip(augs[-len(vals):] if vals else [], vals):
                        fy, q = date_to_fq(d)
                        add(fy, 4, 'attrition', 'total', 'total', float(v), 'pct', 'na', 'annual', key, docname,
                            'People Metrics table', doc_date, 'Annual voluntary attrition (fiscal year).', annual=True)
                    continue
                if len(vals) != len(dates):
                    print('WARN length mismatch', stem, label, vals, dates)
                    continue
                for d, v in zip(dates, vals):
                    fy, q = date_to_fq(d)
                    v = float(v.replace(',', ''))
                    if metric == 'headcount':
                        n = ('Exact employee count at quarter end from People Metrics/Headcount Trend table. ' +
                             {'total': 'Total Accenture employees.',
                              'Billable': 'Billable employees (classification discontinued in FY22 materials).',
                              'Non-Billable': 'Non-billable employees (classification discontinued in FY22 materials).',
                              'Global Delivery Network': 'Memo: employees in Accenture Global Delivery Network (delivery centers, largely offshore); Feb-28-2015 reflects reclassification of ~3,300 personnel into GDN, prior periods not restated.'}[dim])
                        if dim in ('Billable', 'Non-Billable'):
                            n += ' FY15 realignment of ~2% of employees from billable to non-billable (FY14 restated).'
                        if d == '8/31/25':
                            n += ' Includes exits from FY25 Q4 business optimization program.'
                        add(fy, q, 'headcount', dim, dt, v, 'count', 'na', 'point', key, docname,
                            'People Metrics table', doc_date, n)
                    elif metric == 'utilization_incl_trainees':
                        add(fy, q, metric, 'total', 'total', v, 'pct', 'na', 'quarter', key, docname,
                            'People Metrics table', doc_date,
                            'Accenture company-wide utilization; trainee treatment not specified - mapped to '
                            'utilization_incl_trainees by convention.')
                    else:
                        add(fy, q, 'attrition', 'total', 'total', v, 'pct', 'na', 'quarter', key, docname,
                            'People Metrics table', doc_date,
                            'Quarterly voluntary attrition, annualized (label "' + label + '").')


# ---- hand-entered counts of clients with >$100M quarterly bookings (releases / transcripts) ----
def do_bigclients():
    rel = {os.path.basename(k)[:10]: k for k in URLS if k.startswith('8k/')}
    DIM = 'Clients with quarterly bookings >USD100mn'
    items = [
        (2023, 3, DIM, 26, 'quarter', 'rel', '2023-06-22', 'Release CEO quote: "26 clients with quarterly bookings of $100 million or more".'),
        (2023, 4, DIM, 21, 'quarter', 'tr', 'Q4FY23', 'Transcript (CFO, Q&A): "the 21 clients that we had with over $100 million" in Q4.'),
        (2023, 4, DIM, 106, 'annual', 'rel', '2023-09-28', 'Release CEO quote: "106 clients with quarterly bookings of more than $100 million" in FY23 (sum of quarterly counts).'),
        (2024, 1, DIM, 30, 'quarter', 'rel', '2023-12-19', 'Release CEO quote: "30 clients with quarterly bookings of more than $100 million".'),
        (2024, 2, DIM, 39, 'quarter', 'rel', '2024-03-21', 'Release CEO quote: "a record 39 clients with quarterly bookings of over $100 million".'),
        (2024, 3, DIM, 23, 'quarter', 'rel', '2024-06-20', 'Release CEO quote: "another 23 clients with quarterly bookings of over $100 million" (92 YTD per release).'),
        (2024, 4, DIM, 33, 'quarter', 'tr', 'Q4FY24', 'Transcript: "33 clients with quarterly bookings greater than $100 million in the fourth quarter, bringing the total of such bookings to 125 for the year".'),
        (2024, 4, DIM, 125, 'annual', 'rel', '2024-09-26', 'Release: "a record 125 quarterly client bookings of more than $100 million" in FY24.'),
        (2025, 1, DIM, 30, 'quarter', 'rel', '2024-12-19', 'Release: "30 quarterly client bookings of more than $100 million".'),
        (2025, 2, DIM, 32, 'quarter', 'rel', '2025-03-20', 'Release: "32 clients with quarterly bookings greater than $100 million".'),
        (2025, 3, DIM, 30, 'quarter', 'rel', '2025-06-20', 'Release: "30 clients with quarterly bookings greater than $100 million".'),
        (2025, 4, DIM, 37, 'quarter', 'tr', 'Q4FY25', 'Transcript: "We added 37 clients with quarterly bookings greater than $100 million in Q4 alone, bringing us to a record of 129 such bookings for the year".'),
        (2025, 4, DIM, 129, 'annual', 'tr', 'Q4FY25', 'Transcript: record 129 quarterly client bookings over $100 million in FY25.'),
        (2026, 1, DIM, 33, 'quarter', 'rel', '2025-12-18', 'Release: "33 clients with quarterly bookings greater than $100 million".'),
        (2026, 2, DIM, 41, 'quarter', 'rel', '2026-03-19', 'Release: "a record 41 clients with quarterly bookings greater than $100 million".'),
        (2026, 3, DIM, 104, 'ytd', 'rel', '2026-06-18', 'Release: "104 quarterly client bookings of $100 million or more year-to-date, up 13%" (9M FY26; Q3-alone count not stated in release).'),
    ]
    for fy, q, dim, val, pt, st, sk, note in items:
        if st == 'rel':
            key, doc, loc, dd = rel[sk], release_docname(*filing_q(sk)), 'Headline / CEO quote', sk
        else:
            URLS['tr:' + sk] = TR[sk]
            key, doc, loc = 'tr:' + sk, f"Accenture {sk} earnings call transcript (company-hosted)", 'Prepared remarks / Q&A'
            dd = {'Q4FY23': '2023-09-28', 'Q4FY24': '2024-09-26', 'Q4FY25': '2025-09-25'}[sk]
        add(fy, q, 'clients_bucket', dim, 'client_bucket', val, 'count', 'na', pt, key, doc, loc, dd,
            'Bookings-based (not revenue-based) bucket: number of clients with >$100M new bookings in the quarter. ' + note + ' Hand-entered.',
            annual=(pt == 'annual'))


do_releases()
do_filings()
do_people_tables()
do_ai()
do_bigclients()

with open(OUT, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    rows = [r for r in rows if r['period_end'] >= '2014-09-01']  # study period starts Q1FY15
    for r in rows:
        if isinstance(r['value'], float):
            r['value'] = ('%.4f' % r['value']).rstrip('0').rstrip('.')
        w.writerow(r)
print(len(rows), 'rows ->', OUT)
