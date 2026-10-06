"""Build data/raw/wipro.csv from
  - parsed datasheets (wipro_datasheets.py)
  - parsed IFRS statements (wipro_ifrs.py)
  - hand-entered values from press releases / earnings-call transcripts (below)
"""
import os, re, csv
import pandas as pd

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
SRC = os.path.join(ROOT, 'data', 'sources', 'wipro')
OUT = os.path.join(ROOT, 'data', 'raw', 'wipro.csv')
BASE = 'https://www.wipro.com'

# local filename -> URL
url_of = {}
for p in open(os.path.join(SRC, 'wipro_links_fy15_fy27.txt')).read().split():
    parts = p.split('/')
    url_of[f'{parts[7]}_{parts[8]}_{os.path.basename(p)}'] = BASE + p

def url_for_txt(txtname):
    pdf = re.sub(r'\.txt$', '.pdf', txtname)
    return url_of[pdf]

# results announcement dates (press release dateline); FY15 from earnings-call file names
DOC_DATE = {
    (15, 1): '2014-07-24', (15, 2): '2014-10-22', (15, 3): '2015-01-16', (15, 4): '2015-04-21',
    (16, 1): '2015-07-23', (16, 2): '2015-10-21', (16, 3): '2016-01-18', (16, 4): '2016-04-20',
    (17, 1): '2016-07-19', (17, 2): '2016-10-21', (17, 3): '2017-01-25', (17, 4): '2017-04-25',
    (18, 1): '2017-07-20', (18, 2): '2017-10-17', (18, 3): '2018-01-19', (18, 4): '2018-04-25',
    (19, 1): '2018-07-20', (19, 2): '2018-10-24', (19, 3): '2019-01-18', (19, 4): '2019-04-16',
    (20, 1): '2019-07-17', (20, 2): '2019-10-15', (20, 3): '2020-01-14', (20, 4): '2020-04-15',
    (21, 1): '2020-07-14', (21, 2): '2020-10-13', (21, 3): '2021-01-13', (21, 4): '2021-04-15',
    (22, 1): '2021-07-15', (22, 2): '2021-10-13', (22, 3): '2022-01-12', (22, 4): '2022-04-29',
    (23, 1): '2022-07-20', (23, 2): '2022-10-12', (23, 3): '2023-01-13', (23, 4): '2023-04-27',
    (24, 1): '2023-07-13', (24, 2): '2023-10-18', (24, 3): '2024-01-12', (24, 4): '2024-04-19',
    (25, 1): '2024-07-19', (25, 2): '2024-10-17', (25, 3): '2025-01-17', (25, 4): '2025-04-16',
    (26, 1): '2025-07-17', (26, 2): '2025-10-16', (26, 3): '2026-01-16', (26, 4): '2026-04-16',
    (27, 1): '2026-07-16',
}

def fq(fy, q): return f'Q{q}FY{fy:02d}'
def period_end(fy, q):
    y = 2000 + fy
    return {1: f'{y-1}-06-30', 2: f'{y-1}-09-30', 3: f'{y-1}-12-31', 4: f'{y}-03-31'}[q]
def cal_q(fy, q):
    y = 2000 + fy
    return {1: f'{y-1}Q2', 2: f'{y-1}Q3', 3: f'{y-1}Q4', 4: f'{y}Q1'}[q]

rows = []
def add(tfy, tq, metric, dimension, dim_type, value, unit, basis, period_type, url, doc, loc, doc_date, notes):
    rows.append(dict(firm='wipro', fiscal_q=fq(tfy, tq), period_end=period_end(tfy, tq), cal_q=cal_q(tfy, tq),
                     metric=metric, dimension=dimension, dim_type=dim_type, value=value, unit=unit, basis=basis,
                     period_type=period_type, source_url=url, source_doc=doc, source_loc=loc, doc_date=doc_date,
                     notes=notes))

# ---------------- datasheets
ds = pd.read_csv(os.path.join(SRC, 'parsed_datasheets.csv'), keep_default_na=False)
ds = ds.drop_duplicates(['file', 'tfy', 'tq', 'metric', 'dimension', 'basis', 'period_type', 'value'])
for r in ds.itertuples():
    note = r.note
    if r.metric == 'revenue_share' and r.dim_type == 'service_line' and r.tfy <= 16:
        note += '; FY15-FY16 practice shares as printed sum to ~112% (overlapping practice definitions in source)'
    if (r.fy, r.q) != (r.tfy, r.tq):
        note += f'; prior-period column in {fq(r.fy, r.q)} datasheet (may be restated)'
    add(r.tfy, r.tq, r.metric, r.dimension, r.dim_type, r.value, r.unit, r.basis, r.period_type,
        url_for_txt(r.file), f'Wipro {fq(r.fy, r.q)} analyst datasheet', f'{r.loc}: row "{r.label}"',
        DOC_DATE[(r.fy, r.q)], note)

# ---------------- IFRS statements
fi = pd.read_csv(os.path.join(SRC, 'parsed_ifrs.csv'), keep_default_na=False)
for r in fi.itertuples():
    lab = re.sub(r'[.…`₹]+', ' ', r.text).split('  ')[0].strip()
    if r.metric == 'revenue':
        dim, dt, note = 'total', 'total', f'Consolidated revenues (IFRS, INR mn), row "{lab}"'
        loc = 'Consolidated statement of income / revenue note'
    elif r.metric == 'subcontracting_cost':
        dim, dt, note = 'total', 'total', f'Consolidated; IFRS note "Expenses by nature", row "{lab}" (three months ended)'
        loc = 'Notes: Expenses by nature'
    else:
        dim, dt, note = 'total', 'total', f'Consolidated employee compensation; IFRS "Expenses by nature", row "{lab}"'
        loc = 'Notes: Expenses by nature'
    if (r.fy, r.q) != (r.tfy, r.tq):
        note += f'; prior-year comparative column in {fq(r.fy, r.q)} statements'
    add(r.tfy, r.tq, r.metric, dim, dt, r.value, 'INR_mn', 'reported', 'quarter', url_for_txt(r.file),
        f'Wipro {fq(r.fy, r.q)} IFRS interim consolidated financial statements', f'{loc} (line {r.line} of pdftotext output)',
        DOC_DATE[(r.fy, r.q)], note)

# ---------------- hand-entered (press releases / transcripts)
T = {
    (21, 3): '2020-2021_q3fy21_wipro-limited-q3-fy21-quarterly-investor-conference-call.pdf',
    (21, 4): '2020-2021_q4fy21_wipro-limited-q4-fy21-quarterly-investor-conference-call-transcript.pdf',
    (22, 1): '2021-2022_q1fy22_wipro-limited-q1-fy22-quarterly-investor-conference-call-transcript.pdf',
    (22, 2): '2021-2022_q2fy22_wipro-limited-q2-fy22-quarterly-investor-conference-call-transcript.pdf',
    (23, 1): '2022-2023_q1fy23_wipro-limited-q1-fy23-quarterly-investor-conference-call-transcript.pdf',
    (23, 4): '2022-2023_q4fy23_q4fy23-earnings-transcript.pdf',
    (24, 1): '2023-2024_q1fy24_q1fy24-earnings-transcript.pdf',
    (24, 2): '2023-2024_q2fy24_q2fy24-earnings-transcript.pdf',
    (24, 3): '2023-2024_q3fy24_q3fy24-earnings-transcript.pdf',
    (25, 1): '2024-2025_q1fy25_q1fy25-earnings-transcript.pdf',
    (25, 2): '2024-2025_q2fy25_q2fy25-earnings-transcript.pdf',
    (25, 3): '2024-2025_q3fy25_q3fy25-earnings-transcript.pdf',
    (26, 1): '2025-2026_q1fy26_q1fy26-earnings-transcript.pdf',
}
PR = {
    (23, 1): '2022-2023_q1fy23_press-release-q1-fy23.pdf',
    (23, 2): '2022-2023_q2fy23_press-release-q2fy23.pdf',
    (23, 3): '2022-2023_q3fy23_press-release-q3fy23.pdf',
}
HE = 'hand-entered; '
def tr(fy, q, metric, dim, dt, val, unit, ptype, note, pr=False):
    f = PR[(fy, q)] if pr else T[(fy, q)]
    doc = f'Wipro {fq(fy, q)} press release' if pr else f'Wipro {fq(fy, q)} earnings call transcript (company-published)'
    add(fy, q, metric, dim, dt, val, unit, 'reported' if unit.startswith('USD') or unit == 'pct' else 'na', ptype,
        url_of[f], doc, 'text (management remarks)' if not pr else 'text', DOC_DATE[(fy, q)], HE + note)

tr(21, 3, 'tcv', 'Large deals (>=USD30mn TCV)', 'other', 1200, 'USD_mn', 'quarter', 'CEO: "closed 12 deals with more than 30 million TCV each and the TCV booked of this was over $1.2 billion" (lower bound)')
tr(21, 4, 'tcv', 'Large deals (>=USD30mn TCV)', 'other', 1400, 'USD_mn', 'quarter', '"closed 12 large deals, resulting in a TCV of USD1.4 billion", includes one mega deal (Americas). CFO: H2FY21 total TCV $7.1bn of which $2.6bn large deals (half-year, not recorded)')
tr(22, 1, 'tcv', 'Large deals (>=USD30mn TCV)', 'other', 715, 'USD_mn', 'quarter', '"closed eight large deals, resulting in a TCV of over $715 million" (lower bound)')
tr(22, 2, 'tcv', 'Large deals (>=USD30mn TCV)', 'other', 580, 'USD_mn', 'quarter', 'CFO: "signed in Q2 nine deals with a TCV of $580 million" (large deals implied, not explicitly labelled)')
tr(23, 1, 'tcv', 'Large deals (>=USD30mn TCV)', 'other', 1500, 'USD_mn', 'quarter', 'CEO: "large deals bookings were nearly $1.5 billion", 18 large deals. NB later datasheets (Q4FY23+) show Q1FY23 large deal TCV = 1,123 (different definition/vintage)')
tr(23, 1, 'bookings_growth_yoy', 'total', 'total', 32, 'pct', 'quarter', 'Press release: "order bookings grew 32% YoY in Total Contract Value terms"; new metric', pr=True)
tr(23, 2, 'bookings_growth_yoy', 'total', 'total', 23.8, 'pct', 'quarter', 'Press release: "Order bookings (Total Contract Value) grew by 23.8% YoY"; new metric', pr=True)
tr(23, 3, 'bookings', 'total', 'total', 4300, 'USD_mn', 'quarter', 'Press release: "Total Bookings were over $4.3 billion" (lower bound; datasheets show 4,333)', pr=True)
tr(23, 4, 'bookings', 'total', 'total', 4100, 'USD_mn', 'quarter', 'CEO: "Total bookings for the quarter were US$4.1 billion" (datasheets show 4,172)')
tr(24, 1, 'ai_disclosure', 'AI investment commitment (USD bn, 3 years)', 'other', 1, 'USD_bn', 'point', 'Announced USD 1 billion investment in AI over three years and Wipro ai360 ecosystem (July 2023)')
tr(24, 1, 'ai_disclosure', 'Employees to be trained in AI (target)', 'other', 250000, 'count', 'point', '"Over the next 12 months, we will train our entire workforce, nearly 250,000 employees, in AI" (target, not achieved figure)')
tr(24, 2, 'ai_disclosure', 'Employees trained - basic/foundational GenAI', 'other', 180000, 'count', 'point', '"trained as many as 180,000 employees in basic Gen AI general principles"')
tr(24, 3, 'ai_disclosure', 'Employees trained - basic/foundational GenAI', 'other', 210000, 'count', 'point', '"210,000 Wiproites who have been trained on AI 101 skills"')
tr(25, 1, 'ai_disclosure', 'Employees trained - basic/foundational GenAI', 'other', 225000, 'count', 'point', '"foundational training to over 225,000 of our employees"')
tr(25, 1, 'ai_disclosure', 'Employees - advanced AI trained/certified', 'other', 30000, 'count', 'point', '"an additional 30,000 employees have received advanced AI training"')
tr(25, 2, 'ai_disclosure', 'Employees - advanced AI trained/certified', 'other', 44000, 'count', 'point', '"trained and certified over 44,000 employees on Advanced AI"; ~230,000 trained on GenAI basics')
tr(25, 2, 'ai_disclosure', 'Employees trained - basic/foundational GenAI', 'other', 230000, 'count', 'point', '"the initial 230,000 people who got trained on the basics of Gen AI"')
tr(25, 3, 'ai_disclosure', 'Employees - advanced AI trained/certified', 'other', 50000, 'count', 'point', '"50,000 of our employees now hold advanced AI Certification"')
tr(26, 1, 'ai_disclosure', 'AI agents deployed', 'other', 200, 'count', 'point', '"deployed over 200 AI power agents" (lower bound)')

df = pd.DataFrame(rows)
df = df.sort_values(['metric', 'dimension', 'fiscal_q', 'doc_date']).reset_index(drop=True)
# order by period
df['_k'] = df.period_end
df = df.sort_values(['metric', 'dim_type', 'dimension', '_k', 'doc_date', 'basis']).drop(columns='_k')
os.makedirs(os.path.dirname(OUT), exist_ok=True)
df.to_csv(OUT, index=False, quoting=csv.QUOTE_MINIMAL)
print(len(df), 'rows written to', OUT)
