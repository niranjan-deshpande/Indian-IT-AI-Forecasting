"""Tech Mahindra GFC-window extraction (cal 2007Q1-2012Q1 = Q4FY07..Q4FY12).

Inputs (data/sources/gfc/techm/, downloaded by gfc_techm_download.py from Wayback copies of techmahindra.com):
  1. Consolidated quarterly fact sheets ("Fact Sheet data for N Quarters") -> parsed positionally with pdfplumber.
  2. Quarterly results newspaper advertisements ("*_Consolidated.pdf") -> consolidated segment revenue,
     'Services rendered by Business Associates & Others' and the headline revenue growth.  HAND-ENTERED from
     pdftotext (text PDFs) or from macOS Vision OCR + visual reading of 600-dpi crops (vector-outline PDFs),
     each segment block verified to sum to the reported total (checked below).
  3. Company-published earnings-call transcripts and annual reports -> attrition (hand-entered; verbal figures).
Output: data/sources/gfc/techm/gfc_techm_rows.csv (SCHEMA columns, schema order).
"""
import csv, os, re
import pdfplumber

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'data', 'sources', 'gfc', 'techm')
OUT = os.path.join(SRC, 'gfc_techm_rows.csv')
COLS = ['firm', 'fiscal_q', 'period_end', 'cal_q', 'metric', 'dimension', 'dim_type', 'value', 'unit', 'basis',
        'period_type', 'source_url', 'source_doc', 'source_loc', 'doc_date', 'notes']

MANIFEST = {r['file']: r for r in csv.DictReader(open(os.path.join(SRC, 'manifest.csv')))}

def url(fn):
    return MANIFEST[fn]['wayback_url']

def orig_note(fn):
    return 'original URL: ' + MANIFEST[fn]['original_url']

# results/board-meeting dates (from the results advertisements / call transcripts)
DOC_DATE = {'Q4FY07': '2007-05-07', 'Q1FY08': '2007-07-19', 'Q2FY08': '2007-10-19', 'Q3FY08': '2008-01-22',
            'Q4FY08': '2008-05-19', 'Q1FY09': '2008-07-21', 'Q2FY09': '2008-10-21', 'Q3FY09': '2009-01-23',
            'Q4FY09': '2009-04-27', 'Q1FY10': '2009-07-22', 'Q2FY10': '2009-10-20', 'Q3FY10': '2010-01-22',
            'Q4FY10': '2010-04-30', 'Q1FY11': '2010-07-26', 'Q2FY11': '2010-10-26', 'Q3FY11': '2011-01-21',
            'Q4FY11': '2011-05-26', 'Q1FY12': '2011-08-12', 'Q2FY12': '2011-11-15', 'Q3FY12': '2012-02-08',
            'Q4FY12': '2012-05-23'}

def qinfo(fq):
    """'Q1FY08' -> (period_end, cal_q)"""
    q, fy = int(fq[1]), 2000 + int(fq[4:6])
    y = fy - 1 if q <= 3 else fy
    m = {1: '06-30', 2: '09-30', 3: '12-31', 4: '03-31'}[q]
    cq = {1: 2, 2: 3, 3: 4, 4: 1}[q]
    return f'{y}-{m}', f'{y}Q{cq}'

IN_SCOPE = {f'Q4FY07'} | {f'Q{q}FY{y:02d}' for y in range(8, 13) for q in range(1, 5)}

rows = []
def add(fq, metric, dimension, dim_type, value, unit, basis, period_type, fn, source_doc, source_loc, doc_date, notes=''):
    if fq not in IN_SCOPE:
        return
    pe, cq = qinfo(fq)
    n = (notes + '; ' if notes else '') + orig_note(fn)
    rows.append(dict(firm='techm', fiscal_q=fq, period_end=pe, cal_q=cq, metric=metric, dimension=dimension,
                     dim_type=dim_type, value=value, unit=unit, basis=basis, period_type=period_type,
                     source_url=url(fn), source_doc=source_doc, source_loc=source_loc, doc_date=doc_date, notes=n))

# ---------------------------------------------------------------- 1. fact sheets
FACTSHEETS = [  # (file, fact-sheet quarter)
    ('TechM_Q1_F08_Factsheet.pdf', 'Q1FY08'),
    ('TML_Consol_Factsheet_data_10_Qtrs_Q2_07_08.pdf', 'Q2FY08'),  # financialchart copy of Q2F08 is a mis-posted duplicate of Q1F08
    ('TechM_Q3_F08_Factsheet.pdf', 'Q3FY08'), ('TechM_Q4_F08_Factsheet.pdf', 'Q4FY08'),
    ('TechM_Q1_F09_Factsheet.pdf', 'Q1FY09'), ('TechM_Q2_F09_Factsheet.pdf', 'Q2FY09'),
    ('TechM_Q3_F09_Factsheet.pdf', 'Q3FY09'), ('TechM_Q4_F09_Factsheet.pdf', 'Q4FY09'),
    ('TechM_Q1_F10_Factsheet.pdf', 'Q1FY10'), ('TechM_Q2_F10_Factsheet.pdf', 'Q2FY10'),
    ('TechM_Q4_F10_Factsheet.pdf', 'Q4FY10'), ('TechM_Q1_F11_Factsheet.pdf', 'Q1FY11'),
    ('TechM_Q2_F11_Factsheet.pdf', 'Q2FY11'), ('TechM_Q3_F11_Factsheet.pdf', 'Q3FY11'),
    ('TechM_Q4_F11_Factsheet.pdf', 'Q4FY11'), ('TechM_Q1_F12_Factsheet.pdf', 'Q1FY12'),
    ('Factsheet_Q2F12.pdf', 'Q2FY12'), ('Factsheet_Q3F12.pdf', 'Q3FY12'), ('Factsheet_Q4F12.pdf', 'Q4FY12'),
]
NUM = re.compile(r'^\(?-?[\d,]+(\.\d+)?\)?%?$')

def parse_num(t):
    neg = t.startswith('(') or t.startswith('-')
    v = float(t.strip('()%-').replace(',', ''))
    return -v if neg else v

def page_lines(page):
    words = page.extract_words()
    words.sort(key=lambda w: (w['top'], w['x0']))
    lines = []
    for w in words:
        for L in lines:
            if abs(L['top'] - w['top']) < 3:
                L['w'].append(w); break
        else:
            lines.append({'top': w['top'], 'w': [w]})
    for L in lines:
        L['w'].sort(key=lambda w: w['x0'])
    return sorted(lines, key=lambda L: L['top'])

def classify(label):
    l = label.lower()
    if l.startswith('revenue from services'): return ('revenue', 'total', 'total')
    if l.startswith('s/w professionals'): return ('headcount', 'S/w Professionals', 'other')
    if l.startswith('bpo professionals'): return ('headcount', 'BPO Professionals', 'other')
    if l.startswith('sales & support'): return ('headcount', 'Sales & Support', 'other')
    if l.startswith('total employees'): return ('headcount', 'total', 'total')
    for g in ('North America', 'Americas', 'Europe', 'Rest of World'):
        if l.startswith(g.lower()): return ('revenue_share', g, 'geography')
    if l.startswith('no. of active clients'): return ('active_clients', 'total', 'total')
    m = re.match(r'≥ \$(\d+) million clients', label)
    if m: return ('clients_bucket', f'USD{m.group(1)}mn+', 'client_bucket')
    if l.startswith('top client'): return ('revenue_share', 'Top client', 'client_bucket')
    if l.startswith('top 5'): return ('revenue_share', 'Top 5 clients', 'client_bucket')
    if l.startswith('top 10'): return ('revenue_share', 'Top 10 clients', 'client_bucket')
    if l.startswith('onsite'): return ('revenue_share_onsite', 'total', 'total')
    if l.startswith('offshore'): return ('revenue_share_offshore', 'total', 'total')
    if 'utilization' in l: return ('utilization_incl_trainees', 'total', 'total')
    return None

fs_values = {}  # (doc fq, metric, dim, unit, target fq) -> value, for checks
for fn, dq in FACTSHEETS:
    pdf = pdfplumber.open(os.path.join(SRC, fn))
    ddate = DOC_DATE[dq]
    for pi, page in enumerate(pdf.pages):
        lines = page_lines(page)
        text = ' '.join(w['text'] for L in lines[:6] for w in L['w'])
        cur = 'INR_mn' if 'Rs in Mn' in text else ('USD_mn' if ('US$ in Mn' in text or 'USD in Mn' in text) else None)
        assert cur, (fn, pi, text[:200])
        # header: first line with >= 8 Qn / Total tokens; FY labels from the nearest line above containing FYxxxx
        hdr_i = next(i for i, L in enumerate(lines) if sum(bool(re.match(r'^(Q[1-4]\*?|Total)$', w['text'])) for w in L['w']) >= 8)
        fy_i = max(i for i in range(hdr_i) if any(re.match(r'^FY\d{4}$', w['text']) for w in lines[i]['w']))
        fys = [w['text'] for w in lines[fy_i]['w'] if re.match(r'^FY\d{4}$', w['text'])]
        cols, k = [], -1
        for w in lines[hdr_i]['w']:
            t = w['text'].rstrip('*')
            if t == 'Q1': k += 1
            if re.match(r'^(Q[1-4]|Total)$', t):
                if t == 'Total':
                    cols.append((w['x1'], None))
                else:
                    fy = fys[k]
                    cols.append((w['x1'], f'{t}FY{fy[-2:]}'))
        section = None
        for L in lines[hdr_i + 1:]:
            ws = L['w']
            lab = ' '.join(w['text'] for w in ws if not NUM.match(w['text']))
            nums = [w for w in ws if NUM.match(w['text']) and w['x0'] > 140]
            if lab.startswith('Revenue by Geography'): section = 'geo'
            if lab.startswith('Revenue On/Off'): section = 'onoff'
            if lab.startswith('Client contribution'): section = 'client'
            if lab.startswith('No. of Active') or lab.startswith('Total Headcount'): section = None
            c = classify(lab)
            if not c or not nums:
                continue
            metric, dim, dtype = c
            if metric == 'revenue_share' and dtype == 'geography' and section != 'geo': continue
            if metric != 'revenue' and pi > 0: continue  # non-currency rows are repeated on the USD page
            if metric == 'revenue': unit, basis, ptype = cur, 'reported', 'quarter'
            elif metric == 'headcount': unit, basis, ptype = 'count', 'na', 'point'
            elif metric in ('active_clients', 'clients_bucket'): unit, basis, ptype = 'count', 'na', 'point'
            else: unit, basis, ptype = 'pct', 'na', 'quarter'
            for w in nums:
                # value right edge sits ~5-12pt right of its header's right edge; take nearest header by x1
                x1, tq = min(cols, key=lambda c: abs((w['x1'] - 8) - c[0]))
                assert abs((w['x1'] - 8) - x1) < 12, (fn, lab, w['text'], w['x1'], x1)
                if tq is None:  # annual / YTD total column -> skipped (quarterly scope)
                    continue
                v = parse_num(w['text'])
                note = ''
                if metric == 'headcount':
                    note = 'Tech Mahindra consolidated (TML + subsidiaries), period-end; excludes Mahindra Satyam (equity-accounted associate from Q1FY10)'
                elif metric == 'utilization_incl_trainees':
                    note = ('row label "' + lab + '"' + ('' if 'Trainees' in lab else
                            '; trainee treatment not stated in this vintage (label dropped "including Trainees" from Q2FY10 fact sheet; historical values unchanged)'))
                elif metric == 'clients_bucket':
                    note = 'row "' + lab + '"; fact sheet does not state whether LTM revenue'
                elif metric == 'revenue_share' and dtype == 'client_bucket':
                    note = 'Client contribution to revenue: ' + lab
                elif metric in ('revenue_share_onsite', 'revenue_share_offshore'):
                    note = 'Revenue On/Off Break-up (in %)'
                elif metric == 'revenue':
                    note = 'Revenue from services, consolidated (TML + subsidiaries; Satyam equity-accounted, not in revenue)'
                    if tq == 'Q2FY11':
                        note += '; Q2FY11 includes Rs 2,989.5 mn pass-through revenue from a customer (fact-sheet note)'
                if dq in ('Q1FY08',) and fn == 'TechM_Q1_F08_Factsheet.pdf':
                    pass
                add(tq, metric, dim, dtype, v, unit, basis, ptype, fn,
                    f'Tech Mahindra {dq} consolidated fact sheet', (f'p{pi + 1} ' + ('P&L Summary (Rs in Mn)' if cur == 'INR_mn' else 'P&L Summary (US$ in Mn)') + f' / {lab}') if metric == 'revenue' else f'p{pi + 1} / {lab}',
                    ddate, note)
                fs_values[(dq, metric, dim, unit, tq)] = v

# ---------------------------------------------------------------- 2. results advertisements (hand-entered)
AD_FILE = {'Q4FY07': 'TechM_Q4_F07_Consolidated.pdf', 'Q1FY08': 'TechM_Q1_F08_Consolidated.pdf',
           'Q2FY08': 'TechM_Q2_F08_Consolidated.pdf', 'Q3FY08': 'TechM_Q3_F08_Consolidated.pdf',
           'Q4FY08': 'TechM_Q4_F08_Consolidated.pdf', 'Q1FY09': 'TechM_Q1_F09_Consolidated.pdf',
           'Q2FY09': 'TechM_Q2_F09_Consolidated.pdf', 'Q3FY09': 'TechM_Q3_F09_Consolidated.pdf',
           'Q4FY09': 'TechM_Q4_F09_Consolidated.pdf', 'Q1FY10': 'TechM_Q1_F10_Consolidated.pdf',
           'Q2FY10': 'TechM_Q2_F10_Consolidated.pdf', 'Q3FY10': 'TechM_Q3_F10_Consolidated.pdf',
           'Q4FY10': 'TechM_Q4_F10_Consolidated.pdf', 'Q1FY11': 'TechM_Q1_F11_Consolidated.pdf',
           'Q2FY11': 'TechM_Q2_F11_Consolidated.pdf', 'Q3FY11': 'TechM_Q3_F11_Consolidated.pdf',
           'Q4FY11': 'TechM_Q4_F11_Consolidated.pdf', 'Q1FY12': 'TechM_Q1_F12_Consolidated.pdf',
           'Q2FY12': 'Consolidated_Q2F12.pdf', 'Q3FY12': 'Consolidated_Q3F12.pdf', 'Q4FY12': 'Consolidated_Q4F12.pdf'}
SCANNED = {'Q4FY09', 'Q1FY10', 'Q3FY10', 'Q4FY10', 'Q1FY11', 'Q2FY11', 'Q3FY11', 'Q2FY12', 'Q3FY12', 'Q4FY12'}

# Consolidated segment revenue, Rs lakhs: {ad quarter: {column quarter: (TSP, TEM, BPO, Others, Total)}}
SEG = {
    'Q1FY09': {'Q1FY09': (97868, 5140, 6540, 2090, 111638), 'Q1FY08': (78256, 5399, 1535, 2443, 87633)},
    'Q2FY09': {'Q2FY09': (102263, 5524, 6358, 2337, 116482), 'Q2FY08': (80561, 4414, 2649, 2130, 89753)},
    'Q3FY09': {'Q3FY09': (98071, 6235, 6756, 2158, 113220), 'Q3FY08': (86087, 5214, 3975, 1764, 97040)},
    'Q4FY09': {'Q4FY09': (89280, 7198, 5372, 3280, 105130), 'Q4FY08': (91213, 4342, 4804, 1821, 102180)},
    'Q1FY10': {'Q1FY10': (95142, 6617, 6767, 2776, 111302), 'Q1FY09': (97870, 5140, 6540, 2090, 111640)},
    'Q2FY10': {'Q2FY10': (97789, 6991, 6740, 2660, 114180), 'Q2FY09': (102261, 5524, 6358, 2337, 116480)},
    'Q3FY10': {'Q3FY10': (102582, 5794, 6270, 4083, 118729), 'Q3FY09': (98071, 6235, 6756, 2158, 113220)},
    'Q4FY10': {'Q4FY10': (101896, 7033, 6824, 2576, 118329), 'Q4FY09': (89276, 7198, 5372, 3280, 105126)},
    'Q1FY11': {'Q1FY11': (98963, 5836, 6686, 1883, 113368), 'Q1FY10': (95142, 6617, 6767, 2776, 111302)},
    'Q2FY11': {'Q2FY11': (136912, 6843, 7710, 1925, 153390), 'Q2FY10': (97789, 6991, 6740, 2660, 114180)},
    'Q3FY11': {'Q3FY11': (105671, 5830, 7666, 1947, 121114), 'Q3FY10': (102583, 5794, 6270, 4083, 118730)},
    'Q4FY11': {'Q4FY11': (105675, 7792, 10073, 2613, 126153), 'Q4FY10': (101896, 7034, 6824, 2576, 118330)},
    'Q1FY12': {'Q1FY12': (106465, 8287, 12211, 2285, 129248), 'Q1FY11': (98963, 5836, 6686, 1883, 113368)},
    'Q2FY12': {'Q2FY12': (108663, 8064, 12396, 4206, 133329), 'Q1FY12': (106465, 8287, 12211, 2285, 129248),
               'Q2FY11': (136912, 6843, 7710, 1925, 153390)},
    'Q3FY12': {'Q3FY12': (113508, 10607, 13888, 6484, 144487), 'Q2FY12': (108663, 8064, 12396, 4206, 133329),
               'Q3FY11': (105671, 5830, 7666, 1947, 121114)},
    'Q4FY12': {'Q4FY12': (114262, 9035, 14725, 3883, 141905), 'Q3FY12': (113508, 10607, 13888, 6484, 144487),
               'Q4FY11': (105674, 7793, 10073, 2613, 126153)},
}
SEG_NAMES = ['Telecom Service Provider', 'Telecom Equipment Manufacturer', 'BPO', 'Others']
# Consolidated 'Services rendered by Business Associates & Others', Rs lakhs
SUBCON = {
    'Q3FY09': {'Q3FY09': 8980, 'Q3FY08': 9590},
    'Q4FY09': {'Q4FY09': 11690, 'Q4FY08': 11910},
    'Q1FY10': {'Q1FY10': 11267, 'Q1FY09': 11267},
    'Q2FY10': {'Q2FY10': 10535, 'Q2FY09': 13224},
    'Q3FY10': {'Q3FY10': 11161, 'Q3FY09': 9500},
    'Q4FY10': {'Q4FY10': 14585, 'Q4FY09': 10675},
    'Q1FY11': {'Q1FY11': 12235, 'Q1FY10': 11546},
    'Q2FY11': {'Q2FY11': 12452, 'Q2FY10': 10535},
    'Q3FY11': {'Q3FY11': 11380, 'Q3FY10': 11161},
    'Q4FY11': {'Q4FY11': 13400, 'Q4FY10': 14590},
    'Q1FY12': {'Q1FY12': 13652, 'Q1FY11': 12230},
    'Q2FY12': {'Q2FY12': 13966, 'Q1FY12': 13652, 'Q2FY11': 12447},
    'Q3FY12': {'Q3FY12': 15370, 'Q2FY12': 13966, 'Q3FY11': 11380},
    'Q4FY12': {'Q4FY12': 15035, 'Q3FY12': 15370, 'Q4FY11': 13403},
}
# Headline revenue growth (consolidated INR) printed at top of the advertisement
# (ad quarter, metric, period_type, value, headline text)
HEAD = [
    ('Q4FY07', 'revenue_growth_yoy', 'quarter', 108, "Consolidated Revenues for Q4'07 at Rs. 8,745 million. Up 108% YoY"),
    ('Q4FY07', 'revenue_growth_yoy', 'annual', 136, "Consolidated Revenues for FY'07 at Rs. 29,290 million. Up 136% YoY"),
    ('Q1FY08', 'revenue_growth_yoy', 'quarter', 49, 'Consolidated Revenues at Rs 8,763 million for the Quarter, up 49% over previous year'),
    ('Q2FY08', 'revenue_growth_yoy', 'quarter', 29, 'Consolidated Revenues at Rs 8,975 million for the Quarter, up 29% over previous year'),
    ('Q2FY08', 'revenue_growth_yoy', 'ytd', 38, 'Consolidated Revenues at Rs 17,739 million for the Half Year, up 38% over previous year'),
    ('Q3FY08', 'revenue_growth_yoy', 'quarter', 26, 'Consolidated Revenues at Rs 9,704 million for the Quarter, up 26% over previous year'),
    ('Q3FY08', 'revenue_growth_yoy', 'ytd', 34, 'Consolidated Revenues at Rs 27,443 million for the nine months, up 34% over previous year'),
    ('Q4FY08', 'revenue_growth_yoy', 'annual', 29, 'Consolidated Revenues at Rs 37,661 million for the year, up 29% over previous year'),
    ('Q1FY09', 'revenue_growth_yoy', 'quarter', 27, 'Consolidated Revenues at Rs 11,164 million for the quarter, up 27% over previous year and 9% sequentially'),
    ('Q1FY09', 'revenue_growth_qoq', 'quarter', 9, 'Consolidated Revenues at Rs 11,164 million for the quarter, up 27% over previous year and 9% sequentially'),
    ('Q2FY09', 'revenue_growth_yoy', 'quarter', 30, 'Consolidated Revenues at Rs.11,648 million for the quarter, up 30% over previous year'),
    ('Q3FY09', 'revenue_growth_yoy', 'quarter', 17, 'Consolidated Revenues at Rs.11,322 million for the quarter, up 17% over previous year'),
    ('Q3FY09', 'revenue_growth_yoy', 'ytd', 24, 'Consolidated Revenues at Rs.34,134 million for the nine months, up 24% over previous year'),
    ('Q4FY09', 'revenue_growth_yoy', 'annual', 19, 'Consolidated Revenues at Rs. 44,647 million for the year, up 19% over previous year'),
    ('Q1FY10', 'revenue_growth_qoq', 'quarter', 6, 'Consolidated Revenues at Rs.11,130 million for the quarter, up 6% over previous quarter'),
    ('Q2FY10', 'revenue_growth_qoq', 'quarter', 3, 'Consolidated Revenues at Rs. 11,418 million for the quarter, up 3% over previous quarter'),
    ('Q3FY10', 'revenue_growth_qoq', 'quarter', 4, 'Consolidated Revenues at Rs. 11,873 million for the quarter, up 4% over previous quarter'),
    ('Q4FY10', 'revenue_growth_yoy', 'quarter', 13, 'Consolidated Revenues at Rs. 11,833 million for the quarter, up 13% over previous year'),
    ('Q1FY11', 'revenue_growth_yoy', 'quarter', 2, 'Consolidated Revenues at Rs. 11,337 million for the quarter, up 2% over previous year'),
    ('Q2FY11', 'revenue_growth_qoq', 'quarter', 35, 'Consolidated Revenues at Rs. 15,339 million for the quarter, up 35% over previous quarter'),
    ('Q4FY11', 'revenue_growth_yoy', 'annual', 11, 'Consolidated Revenues at Rs. 51,402 million for the year, up 11% over previous year'),
    ('Q1FY12', 'revenue_growth_yoy', 'quarter', 14, 'Consolidated Revenues at Rs. 12,925 million for the quarter, up 14% over previous year'),
    ('Q3FY12', 'revenue_growth_qoq', 'quarter', 8, 'Revenue for the quarter at Rs.14,449 Mn, up 8% sequentially and 19% over previous year'),
    ('Q3FY12', 'revenue_growth_yoy', 'quarter', 19, 'Revenue for the quarter at Rs.14,449 Mn, up 8% sequentially and 19% over previous year'),
    ('Q4FY12', 'revenue_growth_yoy', 'quarter', 12, 'Revenue for the quarter at Rs.14,190 Mn, up 12% over previous year'),
]

def ad_note(aq):
    how = ('hand-entered from Vision OCR of the vector-outline PDF, verified visually on 600-dpi crops'
           if aq in SCANNED else 'hand-entered from pdftotext')
    return how

for aq, cols in SEG.items():
    fn = AD_FILE[aq]
    for cq, vals in cols.items():
        assert abs(sum(vals[:4]) - vals[4]) <= 2, (aq, cq, vals, sum(vals[:4]))  # source rounding (Q2FY08 col of Q2FY09 ad sums to +1)
        rel = 'current quarter' if cq == aq else 'comparative column'
        for name, v in zip(SEG_NAMES + ['total'], vals):
            add(cq, 'segment_revenue', name, 'vertical' if name != 'total' else 'total', v, 'INR_lakh', 'reported', 'quarter', fn,
                f'Tech Mahindra {aq} consolidated audited results (newspaper advertisement)',
                f'Segmentwise Revenue, Results and Capital Employed / Segment Revenue ({rel})', DOC_DATE[aq],
                f'{ad_note(aq)}; consolidated; primary segments = category of customer; Rs lakhs (1 lakh = 0.1 mn); segments verified to sum to total (within 2 lakh rounding)'
                + ('; includes Rs 2,989.5 mn pass-through revenue (fact-sheet note)' if cq == 'Q2FY11' else ''))

for aq, cols in SUBCON.items():
    fn = AD_FILE[aq]
    for cq, v in cols.items():
        rel = 'current quarter' if cq == aq else 'comparative column'
        add(cq, 'subcontracting_cost', 'total', 'total', v, 'INR_lakh', 'reported', 'quarter', fn,
            f'Tech Mahindra {aq} consolidated audited results (newspaper advertisement)',
            f'Consolidated results / 2 Expenditure / Services rendered by Business Associates & Others ({rel})', DOC_DATE[aq],
            f'{ad_note(aq)}; line item "Services rendered by Business Associates & Others" (business associates = subcontractors; the Others component is not broken out); consolidated; Rs lakhs'
            + ('; value printed identically in both quarter columns of this ad (Q1FY11 ad restates Q1FY10 as 11546)' if aq == 'Q1FY10' else ''))

for aq, metric, ptype, v, text in HEAD:
    fn = AD_FILE[aq]
    add(aq, metric, 'total', 'total', v, 'pct', 'reported', ptype, fn,
        f'Tech Mahindra {aq} consolidated audited results (newspaper advertisement)', 'headline',
        DOC_DATE[aq], f'{ad_note(aq)}; INR consolidated revenue growth; headline text: "{text}"')

# ---------------------------------------------------------------- 3. attrition (transcripts / annual reports)
ATTR = [  # (fq, value, period_type, file, source_doc, loc, note)
    ('Q1FY08', 18, 'quarter', 'TechM_Q1_F08_Calltranscripts.pdf', 'Tech Mahindra Q1FY08 earnings call transcript (company-published)', 'Q&A',
     'verbal: "It is 18% like to like" in reply to attrition rate this quarter; definition not stated'),
    ('Q2FY08', 31, 'quarter', 'TechM_Q2_F08_Calltranscripts.pdf', 'Tech Mahindra Q2FY08 earnings call transcript (company-published)', 'Q&A (Sujit Baksi)',
     'verbal: "Total attrition is about 31%", of which ~400 people asked to leave (certificate verification); "effective was about 21%"; basis not stated'),
    ('Q3FY08', 20, 'quarter', 'TechM_Q3_F08_Calltranscripts.pdf', 'Tech Mahindra Q3FY08 earnings call transcript (company-published)', 'Q&A (Sonjoy Anand)',
     'verbal: "around 20%, 21%" and later "on an annualized basis around 20%"'),
    ('Q4FY08', 18, 'quarter', 'TechM_Q4_F08_Calltranscripts.pdf', 'Tech Mahindra Q4FY08 earnings call transcript (company-published)', 'Q&A (Vineet Nayyar)',
     'verbal: "I think it was about 18%" (attrition for the quarter); basis not stated'),
    ('Q4FY09', 11, 'quarter', 'TechM_Q4_F09_Calltranscripts.pdf', 'Tech Mahindra Q4FY09 earnings call transcript (company-published)', 'Q&A (Sujit Baksi)',
     'verbal: "voluntary attrition was at about 11%" (performance-based releases additional, not quantified); period/basis not stated'),
    ('Q4FY10', 22, 'quarter', 'TechM_Q4_F10_Calltranscripts.pdf', 'Tech Mahindra Q4FY10 earnings call transcript (company-published)', 'Q&A (Sujit Baksi)',
     'verbal: "attrition this quarter was 22% annualized"'),
    ('Q4FY10', 17, 'annual', 'TechM_Q4_F10_Calltranscripts.pdf', 'Tech Mahindra Q4FY10 earnings call transcript (company-published)', 'Q&A (Sujit Baksi)',
     'verbal: "For the last whole year ... annual attrition was at 17%" (FY10); conflicts with AR FY10 IT attrition 20.0%'),
    ('Q1FY11', 27, 'quarter', 'TechM_Q1_F11_Calltranscripts.pdf', 'Tech Mahindra Q1FY11 earnings call transcript (company-published)', 'Q&A (Sonjoy Anand)',
     'verbal: "Attrition during the quarter on the IT side was 27%, annualized" (IT services)'),
    ('Q2FY11', 30, 'quarter', 'TechM_Q2_F11_Calltranscripts.pdf', 'Tech Mahindra Q2FY11 earnings call transcript (company-published)', 'Q&A (Sonjoy Anand)',
     'verbal: "Our attrition was around 30%"; Q3FY11 call clarifies the 30% is IT services, quarterly annualized (not TTM)'),
    ('Q4FY11', 25, 'quarter', 'TechM_Q4_F11_Calltranscripts.pdf', 'Tech Mahindra Q4FY11 earnings call transcript (company-published)', 'Q&A (Sonjoy Anand)',
     'verbal: analyst asked "around 25% for this quarter?" - management: "That is correct"; AR FY11 also says IT attrition ~25% for the last quarter'),
    ('Q3FY12', 20, 'quarter', 'Calltranscripts_Q3F12.pdf', 'Tech Mahindra Q3FY12 earnings call transcript (company-published)', 'opening remarks',
     'verbal: "attrition was stable at 20%"; basis not stated'),
    ('Q4FY12', 19, 'quarter', 'Calltranscripts_Q4F12.pdf', 'Tech Mahindra Q4FY12 earnings call transcript (company-published)', 'opening remarks',
     'verbal: "Our attrition levels ... are at 19% in Q4 FY12"; basis not stated'),
    ('Q4FY07', 20.7, 'annual', 'annual_report_0708.pdf', 'Tech Mahindra Annual Report 2007-08', "Management Discussion & Analysis / E. Material developments in human resources",
     'AR: "The attrition rate for the year 2008 and 2007 was 29.6% and 20.7%" (company-wide incl. BPO; FY07)'),
    ('Q4FY08', 29.6, 'annual', 'annual_report_0708.pdf', 'Tech Mahindra Annual Report 2007-08', "Management Discussion & Analysis / E. Material developments in human resources",
     'AR: attrition rate for year 2008 = 29.6%, "primarily due to high attrition in the BPO business" (company-wide incl. BPO)'),
    ('Q4FY08', 24.7, 'annual', 'TML_AR_2009_final.pdf', 'Tech Mahindra Annual Report 2008-09', "Management Discussion & Analysis / E. Material developments in human resources",
     'AR: "The IT attrition rate for the year 2009 and 2008 was 18.7% and 24.7%" (IT only; FY08; differs from 29.6% company-wide in AR 2007-08)'),
    ('Q4FY09', 18.7, 'annual', 'TML_AR_2009_final.pdf', 'Tech Mahindra Annual Report 2008-09', "Management Discussion & Analysis / E. Material developments in human resources",
     'AR: IT attrition rate for the year 2009 = 18.7% (IT only)'),
    ('Q4FY09', 18.7, 'annual', 'AR_2010.pdf', 'Tech Mahindra Annual Report 2009-10', "Management Discussion & Analysis / E. Material developments in human resources",
     'AR: "The IT attrition rate for the year 2010 and 2009 was 20.0% and 18.7%" (IT only; FY09)'),
    ('Q4FY10', 20.0, 'annual', 'AR_2010.pdf', 'Tech Mahindra Annual Report 2009-10', "Management Discussion & Analysis / E. Material developments in human resources",
     'AR: IT attrition rate for the year 2010 = 20.0% (IT only; FY10); call transcript Q4FY10 said 17% for the year'),
    ('Q4FY11', 25, 'quarter', 'TML_Annual_Report_2010_2011.pdf', 'Tech Mahindra Annual Report 2010-11', "Management Discussion & Analysis / E. Material developments in human resources",
     'AR: "The IT attrition was around 25% for the last quarter of year" (IT only)'),
]
for fq, v, ptype, fn, sd, loc, note in ATTR:
    dd = DOC_DATE[fq] if 'Calltranscripts' in fn else {'annual_report_0708.pdf': '2008-06-30', 'TML_AR_2009_final.pdf': '2009-06-30', 'AR_2010.pdf': '2010-06-30',
                                                        'TML_Annual_Report_2010_2011.pdf': '2011-06-30'}[fn]
    add(fq, 'attrition', 'total', 'total', v, 'pct', 'na', ptype, fn, sd, loc, dd, 'hand-entered; ' + note)

# ---------------------------------------------------------------- checks
# (a) fact-sheet INR revenue (mn) vs advertisement segment total (lakhs) for the same quarter & vintage
for aq, cols in SEG.items():
    fs = fs_values.get((aq, 'revenue', 'total', 'INR_mn', aq))
    if fs is not None:
        assert abs(fs - cols[aq][4] / 10) <= 1, (aq, fs, cols[aq][4])
# (b) geography shares ~100
from collections import defaultdict
g = defaultdict(float)
for r in rows:
    if r['metric'] == 'revenue_share' and r['dim_type'] == 'geography':
        g[(r['source_doc'], r['fiscal_q'])] += r['value']
bad = {k: v for k, v in g.items() if abs(v - 100) > 1.5}
assert not bad, bad
# (c) headcount components sum to total
h = defaultdict(dict)
for r in rows:
    if r['metric'] == 'headcount':
        h[(r['source_doc'], r['fiscal_q'])][r['dimension']] = r['value']
for k, d in h.items():
    comp = sum(v for kk, v in d.items() if kk != 'total')
    assert abs(comp - d['total']) < 1, (k, d)

rows.sort(key=lambda r: (r['metric'], r['dimension'], r['period_end'], r['doc_date'], r['source_doc']))
with open(OUT, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    for r in rows:
        r['value'] = ('%g' % r['value']) if isinstance(r['value'], float) else r['value']
        w.writerow(r)
print(len(rows), 'rows ->', OUT)
