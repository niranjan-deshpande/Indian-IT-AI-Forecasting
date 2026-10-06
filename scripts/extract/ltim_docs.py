"""Document index for LTI / Mindtree / LTIMindtree sources (local copies in data/sources/ltim)."""
import os, re, csv, datetime as dt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'data', 'sources', 'ltim')
NSE_BASE = 'https://nsearchives.nseindia.com/corporate/'

MONTHS = {m: i + 1 for i, m in enumerate(['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])}


def find_date(text):
    head = text[:6000]
    m = re.search(r"(?:Mumbai|Bengaluru|Bangalore)[^:\n]{0,40}:\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(20\d{2})", text[:20000])
    if m:
        return dt.date(int(m.group(3)), MONTHS[m.group(1).lower()[:3]], int(m.group(2))).isoformat()
    m = re.search(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(20\d{2})", head)
    if m:
        return dt.date(int(m.group(3)), MONTHS[m.group(1).lower()[:3]], int(m.group(2))).isoformat()
    m = re.search(r"(\d{1,2})(?:st|nd|rd|th)?\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*,?\s+(20\d{2})", head)
    if m:
        return dt.date(int(m.group(3)), MONTHS[m.group(2).lower()[:3]], int(m.group(1))).isoformat()
    return ''


# Mindtree: one earnings-release document per quarter (the NSE results filing that embeds the
# "Earnings release" with Key Revenue / Client / Employee metrics). (doc_q, local pdf/zip name)
MINDTREE_DOCS = [
    ('Q2FY17', '2016-10-21_118LettertoSEsonQtr2resultsintimationasperRegulation33ofLODR_21102016163303'),
    ('Q3FY17', '2017-01-19_164reg33Q3_19012017160733'),
    ('Q4FY17', '2017-04-20_14LettertoSEsonQtr4results_20042017160001'),
    ('Q1FY18', '2017-07-19_71_ResultQ1_19072017162541'),
    ('Q2FY18', '2017-10-25_121LettertoSEQtr2results_25102017160302'),
    ('Q3FY18', '2018-01-17_157LetteronSEsQtr3resultsRegulation33_17012018153601'),
    ('Q4FY18', '2018-04-24_13LetterQtr4resultsRegulation33_24042018095335'),
    ('Q1FY19', '2018-07-18_75Qtr1resultsintimationRegulation33LODR_18072018160344'),
    ('Q2FY19', '2018-10-17_127Q2resultsSept302018_17102018153750'),
    ('Q3FY19', '2019-01-16_167Reg33onQtr3results_16012019161641'),
    ('Q4FY19', '2019-04-17_12LetterSEsQtr4resultsReg33_17042019134402'),
    ('Q1FY20', '2019-07-17_84LetteronQtr1results_17072019164624'),
    ('Q2FY20', '2019-10-16_157Q2LetterReg33Financialresults_16102019154659'),
    ('Q3FY20', '2020-01-14_206LetterQ3results_14012020161650'),
    ('Q4FY20', '2020-04-24_8LetterQtr4resultsRegulation33LODR_24042020165708'),
    ('Q2FY21', '2020-10-15_201LetteronQtr2resultsOct152020_15102020163206'),
    ('Q3FY21', '2021-01-18_247LettertoSEsonQtr3resultsintimationasperRegulatio33ofLODR_18012021154325'),
    ('Q4FY21', '2021-04-16_9LetterQtr4resultsRegulation33LODR'),
    ('Q1FY22', '2021-07-13_59LetterQ1Results_13072021153603'),
    ('Q2FY22', '2021-10-13_98LetterQ2Results_13102021154757'),
    ('Q3FY22', '2022-01-13_129LetterQ3Results_13012022155113'),
    ('Q4FY22', '2022-04-18_10LetterQ4Results_18042022163758'),
    ('Q1FY23', '2022-07-13_MINDTREE_13072022155715_50LetterQ1Results'),
    ('Q2FY23', '2022-10-13_MINDTREE_13102022161548_98LetterQ2results'),
]


def docs():
    out = []
    # LTI / LTIM fact sheets
    idx = {}
    for line in open(os.path.join(SRC, 'download_index.tsv')):
        fn, url = line.rstrip('\n').split('\t')
        idx[fn] = url
    for fn, url in sorted(idx.items()):
        if not fn.endswith('_fs.pdf'):
            continue
        firm, q, _ = fn[:-4].split('_')
        txt = os.path.join(SRC, 'txt', fn[:-4] + '.txt')
        text = open(txt, encoding='utf-8', errors='replace').read()
        if len(text) < 2000 or len(text) > 500000:
            continue  # image-only or garbled-font PDF (logged in notes)
        name = 'LTI' if firm == 'lti' else 'LTIMindtree'
        out.append(dict(doc_id=fn[:-4], firm=firm, doc_q=q, url=url, txt=txt,
                        source_doc=f"{name} {q} Earnings Release & Fact Sheet", doc_date=find_date(text),
                        loc_prefix=''))
    # LTI quarters whose ltm.com fact-sheet PDF is image-only / garbled: NSE copies of the
    # results filing (embedding the Earnings Release & Fact Sheet)
    for q, rel, url, dd, loc in [
        ('Q4FY17', 'LTI_Results_04052017164048/LTI_Results.txt', NSE_BASE + 'LTI_Results_04052017164048.zip', '2017-05-04', 'PDF inside NSE zip; '),
        ('Q1FY20', 'listcontract3_18072019191541_larsen_outcome_387.txt', NSE_BASE + 'listcontract3_18072019191541_larsen_outcome_387.pdf', '2019-07-18', ''),
        ('Q1FY23', 'LTI_14072022152621_OutcomeofBoardmeeting.txt', NSE_BASE + 'LTI_14072022152621_OutcomeofBoardmeeting.pdf', '2022-07-14', ''),
    ]:
        out.append(dict(doc_id=f'lti_{q}_nse', firm='lti', doc_q=q, url=url, txt=os.path.join(SRC, 'lti_nse', rel),
                        source_doc=f"LTI {q} results filing to NSE (incl. Earnings Release & Fact Sheet)",
                        doc_date=dd, loc_prefix=loc))
    # Mindtree NSE filings
    nse_idx = {}
    p = os.path.join(SRC, 'mindtree', 'nse', 'index.tsv')
    for line in open(p):
        parts = line.rstrip('\n').split('\t')
        nse_idx[parts[0]] = parts[1]
    for q, stem in MINDTREE_DOCS:
        fn_zip, fn_pdf = stem + '.zip', stem + '.pdf'
        if fn_zip in nse_idx:
            url = nse_idx[fn_zip]; loc = 'PDF inside NSE zip; '
        elif fn_pdf in nse_idx:
            url = nse_idx[fn_pdf]; loc = ''
        else:
            url = NSE_BASE + stem.split('_', 1)[1] + '.pdf'; loc = ''
        txt = os.path.join(SRC, 'mindtree', 'nse', 'txt', stem + '.txt')
        out.append(dict(doc_id='mindtree_' + q, firm='mindtree', doc_q=q, url=url, txt=txt,
                        source_doc=f"Mindtree {q} earnings release (NSE results filing)",
                        doc_date=stem[:10], loc_prefix=loc))
    return out


if __name__ == '__main__':
    for d in docs():
        print(d['doc_id'], d['doc_q'], d['doc_date'], d['url'][:90], os.path.exists(d['txt']))
