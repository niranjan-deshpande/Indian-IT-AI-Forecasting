"""Build data/raw/hcltech.csv from HCLTech quarterly investor releases.

Inputs: data/sources/hcltech/*.pdf  (downloaded from hcltech.com/investor-relations/financial-results)
        data/sources/hcltech/txt/*.txt  (pdftotext -layout output)
        data/sources/hcltech/ocr/*.txt  (Vision OCR for the 4 image-only PDFs, see hcltech_ocr.swift)
Run:    python3 scripts/extract/hcltech_parse.py
"""
import os, re, sys, csv, datetime
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
SRC = os.path.join(ROOT, 'data', 'sources', 'hcltech')
OUT = os.path.join(ROOT, 'data', 'raw', 'hcltech.csv')
sys.path.insert(0, HERE)
from hcltech_tables import load_text, extract, split_row, parse_num, is_num, header_info

BASE_URL = 'https://www.hcltech.com/sites/default/files/documents/investor-reports/'

# file stem -> (period_end of the release quarter, doc_date)
DOCS = {
    'hclt-q1-2015-jas14-ir_release': ('2014-09-30', '2014-10-17'),
    'hcl_tech_q2_2015_dec_2014_investor_release': ('2014-12-31', '2015-01-30'),
    'hcl_tech_q3_2015_mar_2015_investor_release_0': ('2015-03-31', '2015-04-21'),
    'hcl-q4_2015-investor_release': ('2015-06-30', '2015-08-03'),
    'hcl_tech_q1_2016_investor_release': ('2015-09-30', '2015-10-19'),
    'hcl_tech_q2_2016_investor_release_0': ('2015-12-31', '2016-01-19'),
    'hcl_tech_q3_2016_investor_release_0_1': ('2016-03-31', '2016-04-28'),
    'hcl_tech_q1_2017_investor_release': ('2016-06-30', '2016-08-03'),
    'hcl_tech_q2_2017_investor_release': ('2016-09-30', '2016-10-21'),
    'hcl_tech_q3_2017_investor_release': ('2016-12-31', '2017-01-24'),
    'hcl_tech_q4_2017_investor_release': ('2017-03-31', '2017-05-11'),
    'hcl_tech_q1_2018_investor_release': ('2017-06-30', '2017-07-27'),
    'hcl_tech_q2_2018_investor_release': ('2017-09-30', '2017-10-25'),
    'hcl_tech_q3_2018_investor_release': ('2017-12-31', '2018-01-19'),
    'hcl_tech_q4_2018_investor_release': ('2018-03-31', '2018-05-02'),
    'hcl_tech_q1_2019_investor_release': ('2018-06-30', '2018-07-27'),
    'hcl_tech_q2_2019_investor_release': ('2018-09-30', '2018-10-23'),
    'hcl_tech_q3_2019_investor_release': ('2018-12-31', '2019-01-29'),
    'hcl_tech_q4_2019_investor_release': ('2019-03-31', '2019-05-09'),
    'hcl_tech_q1_2020_investor_release': ('2019-06-30', '2019-08-07'),
    'hcl_tech_q2_2020_investor_release': ('2019-09-30', '2019-10-23'),
    'hcl_tech_q3_2020_investor_release': ('2019-12-31', '2020-01-17'),
    'hcl_tech_q4_2020_investor_release_0': ('2020-03-31', '2020-05-07'),
    'hcl_tech_q1_2021_investor_release': ('2020-06-30', '2020-07-17'),
    'hcl_tech_q2_2021_investor_release': ('2020-09-30', '2020-10-16'),
    'hcl_tech_q3_2021_investor_release': ('2020-12-31', '2021-01-15'),
    'irdraft_q4_jfm21_23_april_v9': ('2021-03-31', '2021-04-23'),
    'hcl_tech_q1_fy22_investor_release': ('2021-06-30', '2021-07-19'),
    'hcl_tech_q2_fy22_investor_release_0': ('2021-09-30', '2021-10-14'),
    'HCL_Tech_Q3_FY22_Investor_Release': ('2021-12-31', '2022-01-14'),
    'HCL_Tech_Q4_FY22_Investor_Release': ('2022-03-31', '2022-04-21'),
    'HCL_Tech_Q1_FY23_Investor_Release': ('2022-06-30', '2022-07-12'),
    'HCLTech_Q2_FY23_Investor_Release': ('2022-09-30', '2022-10-12'),
    'HCLTech_Q3_FY23_Investor_Release': ('2022-12-31', '2023-01-12'),
    'HCLTech_Q4_FY23_Investor_Release': ('2023-03-31', '2023-04-20'),
    'HCL_Tech_Q1_FY24_Investor_Release': ('2023-06-30', '2023-07-12'),
    'HCLTech_Q2_FY24_Investor_Release': ('2023-09-30', '2023-10-12'),
    'HCLTech_Q3_FY24_Investor_Release_0': ('2023-12-31', '2024-01-12'),
    'HCLTech_Q4_FY24_Investor_Release': ('2024-03-31', '2024-04-26'),
    'HCLTech_Q1_FY25_Investor_Release': ('2024-06-30', '2024-07-12'),
    'hcl-tech-q2-fy25-investor-release': ('2024-09-30', '2024-10-14'),
    'HCL_Tech_Q3_FY25_Investor_Release_0': ('2024-12-31', '2025-01-13'),
    'HCLTech_Q4_FY25_Investor_Release': ('2025-03-31', '2025-04-22'),
    'hcltech-q1-fy26-investor-release': ('2025-06-30', '2025-07-14'),
    'HCLTech_Q2-FY26-Investor': ('2025-09-30', '2025-10-13'),
    'HCLTech_Q3_FY26_Investor_Release': ('2025-12-31', '2026-01-12'),
    'hcltech-q4-fy26-investor-release': ('2026-03-31', '2026-04-21'),
    'HCLTech_Q1_FY27_Investor_Release': ('2026-06-30', '2026-07-13'),
}
OCR_DOCS = {'HCLTech_Q4_FY23_Investor_Release', 'HCL_Tech_Q1_FY24_Investor_Release',
            'HCLTech_Q2_FY24_Investor_Release', 'HCLTech_Q3_FY24_Investor_Release_0'}


def fiscal_q(pe):
    y, m = int(pe[:4]), int(pe[5:7])
    if pe <= '2015-06-30':          # FY ended June (FY15 = Jul-2014..Jun-2015)
        q = {9: 1, 12: 2, 3: 3, 6: 4}[m]
        fy = y + 1 if m >= 7 else y
    elif pe <= '2016-03-31':        # transition FY16 = 9 months Jul-2015..Mar-2016
        q = {9: 1, 12: 2, 3: 3}[m]
        fy = 2016
    else:                           # Apr-Mar FY from FY17
        q = {6: 1, 9: 2, 12: 3, 3: 4}[m]
        fy = y + 1 if m >= 4 else y
    return f'Q{q}FY{fy % 100:02d}'


def cal_q(pe):
    return f'{pe[:4]}Q{(int(pe[5:7]) - 1) // 3 + 1}'


def qend(pe):
    """snap a date to its calendar quarter end (tables sometimes say 30-Jun / 31-Mar etc.)"""
    y, m = int(pe[:4]), int(pe[5:7])
    qm = ((m - 1) // 3 + 1) * 3
    d = {3: 31, 6: 30, 9: 30, 12: 31}[qm]
    return f'{y:04d}-{qm:02d}-{d:02d}'


def doc_label(stem):
    return f'HCLTech {fiscal_q(DOCS[stem][0])} investor release' + (' (image PDF, OCR)' if stem in OCR_DOCS else '')


ROWS = []


def add(stem, pe, metric, dimension, dim_type, value, unit, basis, period_type='quarter', loc='', notes=''):
    pe = qend(pe)
    if value is None:
        notes = '; '.join(x for x in [notes, "value printed as '-' (no figure) in source"] if x)
    # disambiguate same-named dimensions whose definition changed (documented in hcltech_NOTES.md)
    if dimension == 'Engineering and R&D Services' and 'NOT comparable' in notes:
        dimension = 'Engineering and R&D Services (service line, pre-FY20 classification)'
    if dim_type == 'geography' and dimension in ('Europe', 'ROW') and DOCS[stem][0] >= '2025-06-30':
        dimension = {'Europe': 'Europe (USA/Europe/ROW/India scheme)', 'ROW': 'ROW (excl. India; USA/Europe/ROW/India scheme)'}[dimension]
    ROWS.append(dict(firm='hcltech', fiscal_q=fiscal_q(pe), period_end=pe, cal_q=cal_q(pe), metric=metric,
                     dimension=dimension, dim_type=dim_type, value=value, unit=unit, basis=basis,
                     period_type=period_type, source_url=BASE_URL + stem + '.pdf', source_doc=doc_label(stem),
                     source_loc=loc, doc_date=DOCS[stem][1],
                     notes=('; '.join(x for x in [notes, 'OCR of image-only PDF (values checked against other vintages where possible)' if stem in OCR_DOCS else ''] if x))))


# ---------------------------------------------------------------- canonical labels
CANON = [
    (r'^(consolidated\s+)?for the company', 'total', 'total'),
    (r'^(geography\s+)?americas', 'geography', 'Americas'),
    (r'^(usa|u\.s\.a?)\b', 'geography', 'USA'),
    (r'^(geography\s+)?europe', 'geography', 'Europe'),
    (r'^(row|rest of the world)', 'geography', 'ROW'),
    (r'^india\b', 'geography', 'India'),
    (r'^it and business', 'service_line', 'IT and Business Services'),
    (r'^engineering and', 'service_line', 'Engineering and R&D Services'),
    (r'^products\s*&', 'service_line', 'Products & Platforms'),
    (r'^hclsoftware', 'service_line', 'HCLSoftware'),
    (r'^(hcltech\s+)?services\s*(\(a\s*\+\s*b\)|$)', 'service_line', 'HCLTech Services'),
    (r'^inter-?segment', 'service_line', 'Inter-segment'),
    (r'^(services\s+)?-?\s*industry application', 'service_line', 'Industry Application Services'),
    (r'^-?\s*enterprise system', 'service_line', 'Enterprise System Integration'),
    (r'^(services\s+)?application services', 'service_line', 'Application Services'),
    (r'^infrastructure services', 'service_line', 'Infrastructure Services'),
    (r'^business services', 'service_line', 'Business Services'),
    (r'^mode\s*([123])', 'service_line', 'Mode {0}'),
    (r'^(verticals\s+)?financial services', 'vertical', 'Financial Services'),
    (r'^manufacturing', 'vertical', 'Manufacturing'),
    (r'^lifesciences', 'vertical', 'Lifesciences & Healthcare'),
    (r'^(verticals\s+)?public services', 'vertical', 'Public Services'),
    (r'^(verticals\s+)?retail', 'vertical', 'Retail & CPG'),
    (r'^(telecom|publishing & entertainment)', 'vertical', 'Telecommunications, Media, Publishing & Entertainment'),
    (r'^technology\s*(&|and)\s*services', 'vertical', 'Technology & Services'),
    (r'^others$', 'vertical', 'Others'),
    (r'^(total|hcltech)\b', 'total', 'total'),
]


def canon(label):
    l = label.strip().lower()
    l = re.sub(r'^(consolidated|geography|segments|verticals|services(?=\s+(application|industry)))\s+', '', l)
    l = l.lstrip('- ').strip()
    for pat, dt, dim in CANON:
        m = re.match(pat, l)
        if m:
            if '{0}' in dim:
                dim = dim.format(m.group(1))
            return dt, dim
    return None, None


SCHEME = {
    'svc': 'classification: pre-FY20 service lines (Application/Infrastructure/Business/ERS)',
    'seg': 'classification: segments from Q1FY20 release (ITBS/ERS/Products & Platforms; P&P renamed HCLSoftware from Q2FY23)',
    'mode': 'classification: Mode 1-2-3 (reported Q1FY19-Q4FY22)',
}


def scheme_note(dim, sec=None, pe_rel=None):
    if dim in ('Application Services', 'Industry Application Services', 'Enterprise System Integration',
               'Infrastructure Services', 'Business Services'):
        return SCHEME['svc']
    if dim.startswith('Mode'):
        return SCHEME['mode']
    if dim in ('IT and Business Services', 'Products & Platforms', 'HCLSoftware', 'HCLTech Services', 'Inter-segment'):
        return SCHEME['seg']
    if dim == 'Engineering and R&D Services':
        if sec == 'svc_mix' or (pe_rel is not None and pe_rel < '2019-06-30'):
            return SCHEME['svc'] + ' -- ERS service line (NOT comparable with the later ERS segment)'
        return SCHEME['seg']
    return ''


def pct_v(raw):
    v = parse_num(raw)
    return v


# ---------------------------------------------------------------- generic tables
def currency_of(pre):
    """decide currency from the nearest preceding line that names one"""
    for ln in reversed(pre.split(' | ')):
        usd = re.search(r'US ?\$|\$ ?M|\$ ?Mn|USD|in \$|\$ for', ln)
        inr = re.search(r'₹|` ?Crore|Crore|INR|in ` ', ln)
        if inr and not usd:
            return 'INR_cr'
        if usd and not inr:
            return 'USD_mn'
    return None


def section(hl, extras):
    H = re.sub(r'\s+', ' ', (hl or '').upper()).strip()
    if 'GEOGRAPHIC' in H or 'GEO GRAPHIC' in H:
        return 'geo_mix'
    if 'SERVICE MIX' in H:
        return 'svc_mix'
    if 'SEGMENT MIX' in H or 'REVENUE MIX' in H:
        return 'seg_mix'
    if 'VERTICAL' in H:
        return 'vert_mix'
    if 'CONTRACT TYPE' in H:
        return 'contract'
    if H == 'DETAILS':
        return None if 'BPS' in extras.upper() else 'details'
    if 'MANPOWER' in H or 'HEADCOUNT' in H or H.startswith('DETAILS (QUARTER') or 'HUMAN CAPITAL' in H:
        return 'people'
    if 'MILLION' in H or '$M CLIENTS' in H or H == 'CLIENT METRICS':
        return 'clients'
    if 'CLIENT CONTRIBUTION' in H:
        return 'topclients'
    if H == 'REPORTED':
        return 'cc_rep'
    if H == 'CONSTANT CURRENCY (QOQ)':
        return 'cc_qoq'
    if H == 'CONSTANT CURRENCY (YOY)':
        return 'cc_yoy'
    if H in ('HCLTECH REVENUE', 'HCLTECH SERVICES REVENUE'):
        return 'cc_new'
    if H == 'INCOME STATEMENT':
        return 'is'
    if H == 'PARTICULARS':
        return 'particulars'
    if H == 'HCLSOFTWARE REVENUE':
        return 'sw_rev'
    return None


def norm_row(r):
    r = (r or '').strip()
    if r in ('900', '20l', 'Q0l', 'QOQ', 'QoQ', '0o0', 'Q00'):
        return 'QoQ'
    return r


def handle_cells(cells):
    skipped = []
    for c in cells:
        stem = c['doc']
        sec = section(c['hlabel'], c['extras'] or '')
        if sec is None or c['col'] == '__short__' or str(c['col']).startswith(('PRIOR:', 'FY:', 'BLK')):
            continue
        col = c['col']
        row = norm_row(c['row'])
        raw = str(c['raw'])
        v = parse_num(raw)
        loc = f"table '{c['hlabel']}' row '{row}'"
        pe_rel = DOCS[stem][0]
        is_extra = col.startswith('X:')
        if is_extra:
            xname = col[2:].upper()
            pe = pe_rel
        else:
            pe = col
        if sec in ('geo_mix', 'svc_mix', 'seg_mix', 'vert_mix', 'details'):
            dt, dim = canon(row)
            if dt is None or dt == 'total':
                continue
            if sec == 'details' and re.match(r'^HCLTech Services\s*$', row):
                continue   # 100% total line of the Services geography/vertical tables
            want = {'geo_mix': 'geography', 'svc_mix': 'service_line', 'seg_mix': 'service_line', 'vert_mix': 'vertical'}.get(sec)
            if want and dt != want:
                continue
            note = scheme_note(dim, sec)
            if dt in ('geography', 'vertical') and pe_rel >= '2022-06-30':
                note = ('HCLTech Services-level mix (excludes Products & Platforms / HCLSoftware); from the Q1FY23 release '
                        'geography & vertical mix is reported at Services level with restated history')
            elif dt in ('geography', 'vertical'):
                note = 'company-level mix'
            if dt == 'geography':
                note += ('; geography scheme USA/Europe/ROW/India (ROW excl. India & non-US Americas split differs), from Q1FY26 release'
                         if dim in ('USA', 'India') or (pe_rel >= '2025-06-30' and dim in ('Europe', 'ROW'))
                         else '; geography scheme Americas/Europe/ROW')
            if is_extra:
                if 'LTM' in xname:
                    continue
                if 'YOY' in xname and 'GROWTH' in xname:
                    add(stem, pe, 'segment_growth_yoy', dim, dt, v, 'pct', 'cc', loc=loc, notes=note)
                elif 'QOQ' in xname and 'GROWTH' in xname:
                    add(stem, pe, 'segment_growth_qoq', dim, dt, v, 'pct', 'cc', loc=loc, notes=note)
                continue
            add(stem, pe, 'revenue_share', dim, dt, v, 'pct', 'na', loc=loc, notes=note)
        elif sec == 'contract':
            if is_extra:
                continue
            if row.lower().startswith('managed services & fixed') or row.lower().startswith('managed services &') and 'time' not in row.lower():
                add(stem, pe, 'revenue_share_fixed_price', 'Managed Services & Fixed Price Projects', 'other', v, 'pct', 'na', loc=loc)
            elif row.lower().startswith('time'):
                add(stem, pe, 'revenue_share', 'Time & Material', 'other', v, 'pct', 'na', loc=loc, notes='contract-type mix')
        elif sec == 'people':
            if is_extra:
                continue
            r = row.lower()
            if r.startswith('total employee count') or r.startswith('total people count'):
                add(stem, pe, 'headcount', 'total', 'total', v, 'count', 'na', 'point', loc,
                    'total employees incl. technical and sales & support; consolidated')
            elif r.startswith('technical'):
                add(stem, pe, 'headcount', 'Technical', 'other', v, 'count', 'na', 'point', loc)
            elif r in ('support', 'sales and support'):
                add(stem, pe, 'headcount', 'Sales and Support', 'other', v, 'count', 'na', 'point', loc,
                    "labelled 'Support' until Q1FY20, 'Sales and Support' thereafter")
            elif r.startswith('gross addition'):
                add(stem, pe, 'gross_additions', 'total', 'total', v, 'count', 'na', 'quarter', loc)
            elif r.startswith('net addition'):
                add(stem, pe, 'net_additions', 'total', 'total', v, 'count', 'na', 'quarter', loc)
            elif r.startswith('freshers added'):
                add(stem, pe, 'fresher_hires', 'total', 'total', v, 'count', 'na', 'quarter', loc, 'freshers added (joined) in the quarter')
            elif r.startswith('attrition - it services'):
                add(stem, pe, 'attrition', 'IT Services', 'other', v, 'pct', 'na', 'ltm', loc,
                    'IT Services attrition, LTM, excludes involuntary attrition (reported until Q4FY19)')
            elif r.startswith('attrition - business services'):
                add(stem, pe, 'attrition', 'Business Services', 'other', v, 'pct', 'na', 'quarter', loc,
                    'Business Services (BPO) attrition, quarterly (not annualised), excludes involuntary (reported until Q4FY19)')
            elif r.startswith('attrition (ltm)'):
                add(stem, pe, 'attrition', 'total', 'total', v, 'pct', 'na', 'ltm', loc,
                    'LTM attrition; excludes involuntary attrition and Digital Process Operations (DPO); company-level series from Q1FY20 release')
            elif r.startswith('blended utilization'):
                add(stem, pe, 'utilization_incl_trainees', 'total', 'total', v, 'pct', 'na', 'quarter', loc,
                    'Blended utilization including trainees (company-wide as labelled); discontinued after Q4FY19')
        elif sec == 'clients':
            if is_extra:
                continue
            m = re.match(r'^\$?(\d+)\s*(million dollar|m)\s*\+', row, re.I)
            if m:
                add(stem, pe, 'clients_bucket', f'USD{m.group(1)}mn+', 'client_bucket', v, 'count', 'na', 'point', loc,
                    'number of clients with LTM revenue above threshold')
        elif sec == 'topclients':
            m = re.match(r'^top\s*(\d+)', row, re.I)
            if m and not is_extra:
                cy = '(CY)' in (c['hlabel'] or '')
                add(stem, pe, 'top_clients_revenue_share', f'Top {m.group(1)} clients', 'client_bucket', v, 'pct', 'na',
                    'annual' if cy else 'ltm', loc, 'calendar-year basis' if cy else 'LTM revenue contribution')
        elif sec == 'cc_rep':
            if row.startswith('Revenue'):
                add(stem, pe, 'revenue', 'total', 'total', v, 'USD_mn', 'reported', loc=loc)
            elif row == 'Growth QoQ':
                add(stem, pe, 'revenue_growth_qoq', 'total', 'total', v, 'pct', 'reported', loc=loc)
            elif row == 'Growth YoY':
                add(stem, pe, 'revenue_growth_yoy', 'total', 'total', v, 'pct', 'reported', loc=loc)
        elif sec == 'cc_qoq':
            if row == 'Growth QoQ':
                add(stem, pe, 'revenue_growth_qoq', 'total', 'total', v, 'pct', 'cc', loc=loc)
        elif sec == 'cc_yoy':
            if row == 'Growth YoY':
                add(stem, pe, 'revenue_growth_yoy', 'total', 'total', v, 'pct', 'cc', loc=loc)
        elif sec == 'cc_new':
            svc = 'SERVICES REVENUE' in (c['hlabel'] or '').upper() or 'Services Revenue' in (c['ctx'] or '')
            if row.startswith('Reported Revenue'):
                if svc:
                    add(stem, pe, 'segment_revenue', 'HCLTech Services', 'service_line', v, 'USD_mn', 'reported', loc=loc,
                        notes='HCLTech Services = ITBS + ERS (excl. HCLSoftware)')
                else:
                    add(stem, pe, 'revenue', 'total', 'total', v, 'USD_mn', 'reported', loc=loc)
            elif row in ('QoQ', 'YoY'):
                if 'CC' not in (c['ctx'] or '').upper():
                    continue
                met = ('segment_growth_' if svc else 'revenue_growth_') + row.lower()
                if svc:
                    add(stem, pe, met, 'HCLTech Services', 'service_line', v, 'pct', 'cc', loc=loc,
                        notes='HCLTech Services = ITBS + ERS (excl. HCLSoftware)')
                else:
                    add(stem, pe, met, 'total', 'total', v, 'pct', 'cc', loc=loc)
        elif sec == 'is':
            cur = currency_of(c['pre'])
            if row in ('Revenues', 'Revenue') and cur == 'INR_cr' and not is_extra:
                add(stem, pe, 'revenue', 'total', 'total', v, 'INR_cr', 'reported', loc=loc + ' (INR income statement)')
        elif sec == 'particulars':
            cur = currency_of(c['pre'])
            r = row.lower()
            if is_extra or cur is None:
                continue
            if r.startswith('outsourcing costs') or r.startswith('(subcontractors'):
                if v is not None and '%' in raw:
                    continue
                add(stem, pe, 'subcontracting_cost', 'total', 'total', v, cur, 'reported', loc=loc,
                    notes="'Outsourcing costs (Subcontractors + Outsourced Work)' from cost breakup")
            elif r.startswith('employee benefits'):
                if '%' in raw:
                    continue
                add(stem, pe, 'employee_cost', 'total', 'total', v, cur, 'reported', loc=loc,
                    notes='Employee benefits expense from cost breakup')
        elif sec == 'sw_rev':
            if row.startswith('Total Revenue') and not is_extra:
                add(stem, pe, 'segment_revenue', 'HCLSoftware', 'service_line', v, 'USD_mn', 'reported', loc=loc,
                    notes='HCLSoftware revenue per HCLSoftware Metrics table')


# ---------------------------------------------------------------- growth tables (pre-Q2FY23)
GROWTH_SPEC = {
    'hclt-q1-2015-jas14-ir_release': ['qoq', 'rep_qoq', 'rep_yoy'],
    'hcl_tech_q2_2015_dec_2014_investor_release': ['qoq', 'rep_qoq', None],
    'hcl_tech_q3_2015_mar_2015_investor_release_0': ['qoq', 'yoy', None],
    'hcl-q4_2015-investor_release': ['qoq', 'yoy', None],
    'hcl_tech_q1_2016_investor_release': ['qoq', 'yoy', None],
    'hcl_tech_q2_2016_investor_release_0': ['qoq', 'yoy', None],
    'hcl_tech_q3_2016_investor_release_0_1': ['qoq', 'yoy', None],
    'hcl_tech_q1_2017_investor_release': ['qoq', 'yoy', None],
    'hcl_tech_q2_2017_investor_release': ['qoq', 'yoy', None],
    'hcl_tech_q3_2017_investor_release': ['qoq', 'yoy', None],
    'hcl_tech_q4_2017_investor_release': ['qoq', 'yoy', None],
    'hcl_tech_q1_2018_investor_release': ['qoq', 'yoy', None],
    'hcl_tech_q2_2018_investor_release': ['qoq', 'yoy', None],
    'hcl_tech_q3_2018_investor_release': ['qoq', 'yoy', None],
    'hcl_tech_q4_2018_investor_release': [None, 'qoq', 'yoy', None],
    'hcl_tech_q1_2019_investor_release': ['qoq', 'yoy', None],
    'hcl_tech_q2_2019_investor_release': ['qoq', 'yoy', None],
    'hcl_tech_q3_2019_investor_release': ['qoq', 'yoy', None],
    'hcl_tech_q4_2019_investor_release': ['qoq', 'yoy', None],
    'hcl_tech_q1_2020_investor_release': ['qoq', 'yoy'],
    'hcl_tech_q2_2020_investor_release': [None, None, 'qoq', 'yoy'],
    'hcl_tech_q3_2020_investor_release': [None, 'qoq', 'yoy'],
    'hcl_tech_q4_2020_investor_release_0': [None, None, 'qoq', 'yoy', None],
    'hcl_tech_q1_2021_investor_release': [None, 'qoq', 'yoy'],
    'hcl_tech_q2_2021_investor_release': ['qoq', 'yoy'],
    'hcl_tech_q3_2021_investor_release': ['qoq', 'yoy'],
    'irdraft_q4_jfm21_23_april_v9': ['qoq', 'yoy', None],
    'hcl_tech_q1_fy22_investor_release': ['qoq', 'yoy'],
    'hcl_tech_q2_fy22_investor_release_0': ['qoq', 'yoy'],
    'HCL_Tech_Q3_FY22_Investor_Release': ['qoq', 'yoy'],
    'HCL_Tech_Q4_FY22_Investor_Release': ['qoq', 'yoy', None],
    'HCL_Tech_Q1_FY23_Investor_Release': ['qoq', 'yoy'],
}
IBM_NOTE = ('Q2FY20-Q1FY21 releases also show growth "per prior methodology" (IBM IP revenue kept in US/Technology & Services); '
            'only the "per actuals" columns are recorded')


def growth_tables(stem, lines):
    spec = GROWTH_SPEC.get(stem)
    if not spec:
        return
    idx = next((i for i, l in enumerate(lines) if 'For the Company' in l), None)
    if idx is None:
        print('no growth table', stem)
        return
    pe = DOCS[stem][0]
    for i in range(idx, min(idx + 32, len(lines))):
        ln = lines[i]
        if re.match(r'^\s*(Note|-\s*\d+\s*-)', ln) and i > idx:
            break
        label, nums = split_row(ln)
        if not nums:
            continue
        prev_label, prev_nums = split_row(lines[i - 1])
        prev_text = not prev_nums
        if not label or label.strip() in ('Services', 'Segments', 'Geography', 'Verticals'):
            parts = [prev_label] if prev_text else []
            nl, nn = split_row(lines[i + 1])
            if not nn:
                parts.append(nl)
            label = ' '.join(parts)
        elif prev_text and re.search(r'(,|&| and)$', prev_label.strip()):
            label = prev_label.strip() + ' ' + label
        dt, dim = canon(label)
        if dt is None:
            if not re.search(r'top\s*\d', label, re.I):
                print('growth: unmatched', stem, repr(label), nums)
            continue
        if len(nums) != len(spec):
            print('growth: count mismatch', stem, label, nums, spec)
            continue
        for tok, what in zip(nums, spec):
            if what is None:
                continue
            v = parse_num(tok)
            basis = 'reported' if what.startswith('rep_') else 'cc'
            kind = what.replace('rep_', '')
            loc = f"Revenue growth table, row '{label.strip()}'"
            note = scheme_note(dim, None, pe)
            if dt in ('geography', 'vertical'):
                note = 'HCLTech Services-level (from Q1FY23 release)' if pe >= '2022-06-30' else 'company-level'
            if stem in ('hcl_tech_q2_2020_investor_release', 'hcl_tech_q3_2020_investor_release',
                        'hcl_tech_q4_2020_investor_release_0', 'hcl_tech_q1_2021_investor_release') and dt in ('geography', 'vertical'):
                note = '; '.join(x for x in [note, IBM_NOTE] if x)
            if dt == 'total':
                continue   # company totals come from the constant-currency reporting table
            else:
                add(stem, pe, f'segment_growth_{kind}', dim, dt, v, 'pct', basis, loc=loc, notes=note)


# ---------------------------------------------------------------- Mode 1-2-3 / segment highlight tables
def highlight_tables(stem, lines):
    pe = DOCS[stem][0]
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]
        if (re.search(r'(Mode 1-2-3 Highlights|Segment Highlights|Segment-wise Highlights|^\s*Segment-wise\s*$|^\s*Mode 1-2-3\s*$)', ln, re.I)
                and not re.search(r'for the Quarter', ln, re.I)) or \
           re.match(r'^\s*(Segment-wise|Mode 1-2-3)\s+Revenue\s*$', ln):
            # header text until first data row
            hdr = []
            j = i
            while j < min(i + 10, n):
                lab, nums = split_row(lines[j])
                d_t, d = canon(lab) if nums else (None, None)
                if nums and d_t == 'service_line':
                    break
                hdr.append(lines[j])
                j += 1
            if any(header_info(h) for h in hdr):
                i = j
                continue
            H = ' '.join(hdr).upper()
            spec = ['rev', 'mix']
            if 'EBIT' in H or 'MARGIN' in H:
                spec.append('ebit')
            if 'QOQ' in H:
                spec.append('qoq')
            if 'YOY' in H:
                spec.append('yoy')
            k = j
            while k < min(j + 8, n):
                lab, nums = split_row(lines[k])
                d_t, d = canon(lab)
                if d_t == 'total' or not nums:
                    break
                if d_t == 'service_line':
                    if len(nums) != len(spec):
                        print('highlight: count mismatch', stem, lab, nums, spec)
                    else:
                        loc = f"{'Mode 1-2-3' if d.startswith('Mode') else 'Segment'} highlights table, row '{lab}'"
                        note = scheme_note(d, 'seg')
                        for tok, what in zip(nums, spec):
                            v = parse_num(tok)
                            if what == 'rev':
                                add(stem, pe, 'segment_revenue', d, 'service_line', v, 'USD_mn', 'reported', loc=loc, notes=note)
                            elif what == 'mix':
                                add(stem, pe, 'revenue_share', d, 'service_line', v, 'pct', 'na', loc=loc, notes=note)
                            elif what in ('qoq', 'yoy'):
                                add(stem, pe, f'segment_growth_{what}', d, 'service_line', v, 'pct', 'cc', loc=loc, notes=note)
                k += 1
            i = k
        i += 1


# ---------------------------------------------------------------- hand-entered text disclosures
HAND = [
    # stem, metric, value, unit, basis, period_type, note, loc
    ('irdraft_q4_jfm21_23_april_v9', 'tcv', 3100, 'USD_mn', 'reported', 'quarter', 'New Deal TCV "US $ 3.1 B" (rounded in text), up 49% YoY', 'Key highlights text'),
    ('irdraft_q4_jfm21_23_april_v9', 'tcv', 7300, 'USD_mn', 'reported', 'annual', 'FY21 New Deal TCV "US $ 7.3 B" (rounded), +18% over FY20', 'Key highlights text'),
    ('hcl_tech_q1_fy22_investor_release', 'tcv', 1664, 'USD_mn', 'reported', 'quarter', 'TCV of New Deal wins', 'Key highlights text'),
    ('hcl_tech_q2_fy22_investor_release_0', 'tcv', 2245, 'USD_mn', 'reported', 'quarter', 'TCV of New Deal wins', 'Key highlights text'),
    ('HCL_Tech_Q3_FY22_Investor_Release', 'tcv', 2135, 'USD_mn', 'reported', 'quarter', 'TCV of New Deal wins (Services 1,968 + Products 167)', 'Key highlights text'),
    ('HCL_Tech_Q4_FY22_Investor_Release', 'tcv', 2260, 'USD_mn', 'reported', 'quarter', 'TCV of New Deal wins (Services 2,216 + Products 54 as printed)', 'Key highlights text'),
    ('HCL_Tech_Q4_FY22_Investor_Release', 'tcv', 8308, 'USD_mn', 'reported', 'annual', 'FY22 TCV of New Deal wins', 'Key highlights text'),
    ('HCL_Tech_Q1_FY23_Investor_Release', 'tcv', 2054, 'USD_mn', 'reported', 'quarter', 'TCV of New Deal wins (Services 1,950 + Products 104)', 'Key highlights text'),
    ('HCLTech_Q2_FY23_Investor_Release', 'tcv', 2384, 'USD_mn', 'reported', 'quarter', 'TCV Bookings (New Deal wins)', 'Page 1 highlights'),
    ('HCLTech_Q3_FY23_Investor_Release', 'tcv', 2347, 'USD_mn', 'reported', 'quarter', 'TCV (New Deal wins)', 'Page 1 highlights'),
    ('HCLTech_Q4_FY23_Investor_Release', 'tcv', 2074, 'USD_mn', 'reported', 'quarter', 'TCV (New Deal wins)', 'Page 1 highlights'),
    ('HCLTech_Q4_FY23_Investor_Release', 'tcv', 8853, 'USD_mn', 'reported', 'annual', 'FY23 TCV (New Deal wins), up 6.6%', 'Page 1 highlights'),
    ('HCL_Tech_Q1_FY24_Investor_Release', 'tcv', 1565, 'USD_mn', 'reported', 'quarter', 'TCV (New Deal wins)', 'Page 1 highlights'),
    ('HCLTech_Q2_FY24_Investor_Release', 'tcv', 3969, 'USD_mn', 'reported', 'quarter', 'TCV (New Deal wins)', 'Page 1 highlights'),
    ('HCLTech_Q3_FY24_Investor_Release_0', 'tcv', 1927, 'USD_mn', 'reported', 'quarter', 'TCV (New Deal wins)', 'Page 1 highlights'),
    ('HCLTech_Q4_FY24_Investor_Release', 'tcv', 2290, 'USD_mn', 'reported', 'quarter', 'TCV (New Deal wins)', 'Page 1 highlights'),
    ('HCLTech_Q4_FY24_Investor_Release', 'tcv', 9759, 'USD_mn', 'reported', 'annual', 'FY24 TCV (New Deal wins), up 10.0%', 'Page 1 highlights'),
    ('HCLTech_Q1_FY25_Investor_Release', 'tcv', 1960, 'USD_mn', 'reported', 'quarter', 'TCV (New Deal wins)', 'Page 1 highlights'),
    ('hcl-tech-q2-fy25-investor-release', 'tcv', 2218, 'USD_mn', 'reported', 'quarter', 'TCV (New Deal wins)', 'Page 1 highlights'),
    ('HCL_Tech_Q3_FY25_Investor_Release_0', 'tcv', 2095, 'USD_mn', 'reported', 'quarter', 'TCV (New Deal wins)', 'Page 1 highlights'),
    ('HCLTech_Q4_FY25_Investor_Release', 'tcv', 2995, 'USD_mn', 'reported', 'quarter', 'TCV (New Deal wins)', 'Page 1 highlights'),
    ('HCLTech_Q4_FY25_Investor_Release', 'tcv', 9268, 'USD_mn', 'reported', 'annual', 'FY25 TCV (New Deal wins)', 'Page 1 highlights'),
    ('hcltech-q1-fy26-investor-release', 'tcv', 1812, 'USD_mn', 'reported', 'quarter', 'TCV (New Deal wins)', 'Page 1 highlights'),
    ('HCLTech_Q2-FY26-Investor', 'tcv', 2569, 'USD_mn', 'reported', 'quarter', 'TCV (New Deal wins), up 41.8% QoQ & 15.8% YoY', 'Page 1 highlights'),
    ('HCLTech_Q3_FY26_Investor_Release', 'tcv', 3006, 'USD_mn', 'reported', 'quarter', 'TCV (New Deal wins), up 17.0% QoQ & 43.5% YoY', 'Page 1 highlights'),
    ('hcltech-q4-fy26-investor-release', 'tcv', 1936, 'USD_mn', 'reported', 'quarter', 'TCV (New Deal wins)', 'Page 1 highlights'),
    ('hcltech-q4-fy26-investor-release', 'tcv', 9323, 'USD_mn', 'reported', 'annual', 'FY26 TCV (New Deal wins)', 'Page 1 highlights'),
    ('HCLTech_Q1_FY27_Investor_Release', 'tcv', 2407, 'USD_mn', 'reported', 'quarter', 'Bookings (New Deal Wins); "highest ever Q1 net-new bookings"', 'Page 2 performance dashboard'),
    # people metrics disclosed only in text before the 5-quarter 'People Metrics' table (from Q2FY23)
    ('hcl_tech_q1_2020_investor_release', 'net_additions', 5935, 'count', 'na', 'quarter', '"In Q1, there was a net addition of 5,935 employees"', 'Key highlights text'),
    ('hcl_tech_q2_2020_investor_release', 'net_additions', 3223, 'count', 'na', 'quarter', '"In Q2, there was a net addition of 3,223 employees"', 'Key highlights text'),
    ('hcl_tech_q3_2021_investor_release', 'net_additions', 6597, 'count', 'na', 'quarter', 'Net Additions at 6,597 during the quarter', 'Key highlights text'),
    ('irdraft_q4_jfm21_23_april_v9', 'net_additions', 9295, 'count', 'na', 'quarter', 'Net Additions during the quarter 9295', 'Key highlights text'),
    ('irdraft_q4_jfm21_23_april_v9', 'net_additions', 18554, 'count', 'na', 'annual', 'FY21 Net Addition of 18,554', 'Key highlights text'),
    ('hcl_tech_q1_fy22_investor_release', 'net_additions', 7522, 'count', 'na', 'quarter', 'net Addition of 7,522 during the quarter', 'Key highlights text'),
    ('hcl_tech_q2_fy22_investor_release_0', 'net_additions', 11135, 'count', 'na', 'quarter', 'Net Addition of 11,135 during the quarter', 'Key highlights text'),
    ('HCL_Tech_Q3_FY22_Investor_Release', 'net_additions', 10143, 'count', 'na', 'quarter', 'Net Addition of 10,143 during the quarter', 'Key highlights text'),
    ('HCL_Tech_Q3_FY22_Investor_Release', 'fresher_hires', 16000, 'count', 'na', 'ytd', '"16,000 freshers already hired till Q3" (FY22 Apr-Dec, rounded); plan 20,000-22,000 for FY22', 'People text'),
    ('HCL_Tech_Q4_FY22_Investor_Release', 'net_additions', 11000, 'count', 'na', 'quarter', '"net hiring was 11,000 globally for the quarter" (rounded; later People Metrics table shows 11,100)', 'People text'),
    ('HCL_Tech_Q4_FY22_Investor_Release', 'net_additions', 39900, 'count', 'na', 'annual', 'FY22 Net Addition of 39,900', 'Key highlights text'),
    ('HCL_Tech_Q4_FY22_Investor_Release', 'fresher_hires', 23000, 'count', 'na', 'annual', '"Entry level (fresher) employees hired in FY22 - 23,000"', 'People text'),
    ('HCL_Tech_Q1_FY23_Investor_Release', 'net_additions', 2089, 'count', 'na', 'quarter', 'Net hiring was 2,089 for the quarter', 'People text'),
    ('HCL_Tech_Q1_FY23_Investor_Release', 'fresher_hires', 6023, 'count', 'na', 'quarter', '6,023 freshers were added during the quarter', 'Headcount Details footnote'),
    # AI disclosures
    ('HCLTech_Q2-FY26-Investor', 'ai_disclosure', 100, 'USD_mn', 'reported', 'quarter', 'Advanced AI quarterly revenue "crossed $100M" (lower bound, not exact)', 'Page 1 highlights'),
    ('HCLTech_Q3_FY26_Investor_Release', 'ai_disclosure', 146, 'USD_mn', 'reported', 'quarter', 'Advanced AI Revenue $146M, up 19.9% QoQ CC', 'Page 1 highlights'),
    ('hcltech-q4-fy26-investor-release', 'ai_disclosure', 155, 'USD_mn', 'reported', 'quarter', 'Advanced AI Revenue $155M, up 6.1% QoQ CC; annualized Advanced AI revenue $620M', 'Page 1 highlights'),
    ('HCLTech_Q1_FY27_Investor_Release', 'ai_disclosure', 171, 'USD_mn', 'reported', 'quarter', 'Advanced AI Revenue $171M, up 10.6% QoQ CC and 62.1% YoY CC', 'Page 2 performance dashboard'),
]



# ---------------------------------------------------------------- SEBI (Reg. 33) consolidated Ind AS results
# (file stem under data/sources/hcltech/results[/detached], text source, published file name, quarter end)
RESULTS = [
    ('full_financial_results-_qtr._and_year_ended_march_31_2017', 'ocr', 'full_financial_results-_qtr._and_year_ended_march_31_2017.pdf', '2017-03-31', ''),
    ('full_financial_results_-_qtr._ended_june_30_2017', 'ocr', 'full_financial_results_-_qtr._ended_june_30_2017.pdf', '2017-06-30', ''),
    ('full_financial_results-_qtr._ended_sep_30_2017_0', 'ocr', 'full_financial_results-_qtr._ended_sep_30_2017_0.pdf', '2017-09-30', ''),
    ('full_financial_results_-_qtr._ended_dec_31_2017_0', 'ocr', 'full_financial_results_-_qtr._ended_dec_31_2017_0.pdf', '2017-12-31', ''),
    ('full_financial_results-_year_ended_march_31_2018', 'ocr', 'full_financial_results-_year_ended_march_31_2018.pdf', '2018-03-31', ''),
    ('full_financial_results_-_qtr._ended_june_30_2018', 'ocr', 'full_financial_results_-_qtr._ended_june_30_2018.pdf', '2018-06-30', ''),
    ('full_financial_results', 'ocr', 'full_financial_results.pdf', '2018-09-30', ''),
    ('full_financial_results_-_qtr._ended_december_31_2018', 'ocr', 'full_financial_results_-_qtr._ended_december_31_2018.pdf', '2018-12-31', ''),
    ('full_financial_results_qtr_ended_june_30_2019', 'txt', 'full_financial_results_qtr_ended_june_30_2019.pdf', '2019-06-30', ''),
    ('full_financial_results_qtr._ended_september_30_2019', 'txt', 'full_financial_results_qtr._ended_september_30_2019.pdf', '2019-09-30', ''),
    ('full_financial_results_qtr._ended_december_31_2019_1', 'txt', 'full_financial_results_qtr._ended_december_31_2019_1.pdf', '2019-12-31', ''),
    ('detached/Reg33_Mar20_Main', 'txt', 'financialresults.pdf', '2020-03-31', "embedded file '2. Reg 33 Financials Mar'20 - Main.pdf' in PDF portfolio"),
    ('detached/q12021_1', 'txt', 'financialresults-q12020_0.pdf', '2020-06-30', "embedded file '1.pdf' in PDF portfolio"),
    ('detached/Reg33_JAS20_Main', 'txt', 'full_financial_results_0.pdf', '2020-09-30', "embedded file '4. Regulation 33 - JAS'20 - Main.pdf' in PDF portfolio"),
    ('FinancialResults_0', 'txt', 'FinancialResults_0.pdf', '2020-12-31', ''),
    ('financialresultsmarch2021', 'txt', 'financialresultsmarch2021.pdf', '2021-03-31', ''),
    ('financial_resultsq12021', 'ocr', 'financial_resultsq12021.pdf', '2021-06-30', ''),
    ('financialresultsnew_0', 'ocr', 'financialresultsnew_0.pdf', '2021-09-30', ''),
    ('fullfinanicalResultsec2021', 'txt', 'fullfinanicalResultsec2021.pdf', '2021-12-31', ''),
    ('Financial_Results', 'ocr', 'Financial%20Results.pdf', '2022-03-31', ''),
    ('Financial_Results_0', 'ocr', 'Financial%20Results_0.pdf', '2022-09-30', ''),
    ('FinancialResults_1', 'ocr', 'FinancialResults_1.pdf', '2023-03-31', ''),
    ('Financial-Results_0', 'txt', 'Financial-Results_0.pdf', '2023-06-30', ''),
    ('FinancialResults_2', 'txt', 'FinancialResults_2.pdf', '2023-09-30', ''),
    ('FinancialResults_3', 'ocr', 'FinancialResults_3.pdf', '2023-12-31', ''),
    ('Audited-Financial-Results-for-the-quarter-and-year-ended-March-31-2024', 'ocr', 'Audited-Financial-Results-for-the-quarter-and-year-ended-March-31-2024.pdf', '2024-03-31', ''),
    ('Audited-Financial-Results-for-the-quarter-ended-June-30-2024', 'ocr', 'Audited-Financial-Results-for-the-quarter-ended-June-30-2024.pdf', '2024-06-30', ''),
    ('audited-financial-results-for-the-quarter-ended-september-30-2024', 'txt', 'audited-financial-results-for-the-quarter-ended-september-30-2024.pdf', '2024-09-30', ''),
    ('Audited-Financial-Results-for-the-quarter-ended-December-31-2024_0', 'txt', 'Audited-Financial-Results-for-the-quarter-ended-December-31-2024_0.pdf', '2024-12-31', ''),
    ('Audited-Financial-Results-for-the-quarter-and-year-ended-March-31-2025', 'txt', 'Audited-Financial-Results-for-the-quarter-and-year-ended-March-31-2025.pdf', '2025-03-31', ''),
    ('audited-financial-results-for-the-quarter-ended-June-30-2025', 'txt', 'audited-financial-results-for-the-quarter-ended-June-30-2025.pdf', '2025-06-30', ''),
    ('Audited-Financial-Results-for-the-quarter-ended-September-30-2025_0', 'txt', 'Audited-Financial-Results-for-the-quarter-ended-September-30-2025_0.pdf', '2025-09-30', ''),
    ('Audited-Financial-Results-for-the-quarter-ended-December-31-2025', 'txt', 'Audited-Financial-Results-for-the-quarter-ended-December-31-2025.pdf', '2025-12-31', ''),
    ('audited-financial-results-for-the-quarter-ended-march-31-2026', 'txt', 'audited-financial-results-for-the-quarter-ended-march-31-2026.pdf', '2026-03-31', ''),
    ('Un-audited-Financial-Results-for-the-quarter-ended-June-30-2026', 'txt', 'Un-audited-Financial-Results-for-the-quarter-ended-June-30-2026.pdf', '2026-06-30', ''),
]


# cells whose embedded text layer is a known OCR misread (value contradicts all other vintages)
RESULTS_SKIP = {('full_financial_results_qtr_ended_june_30_2019', 'revenue', 1)}   # prints 13,990 for Mar-19 (IR & other vintages: 15,990)


def prev_q(pe, k):
    y, m = int(pe[:4]), int(pe[5:7])
    m -= 3 * k
    while m <= 0:
        m += 12
        y -= 1
    return qend(f'{y:04d}-{m:02d}-01')


def clean_tok(t):
    t = re.sub(r'^[^\d(]+', '', t)
    if re.match(r'^\d\.\d{3}$', t):      # OCR read a thousands comma as a period
        t = t.replace('.', ',')
    return t


def sebi_results():
    rel_doc = {v[0]: v[1] for v in DOCS.values()}
    for stem, kind, fname, pe, loc_extra in RESULTS:
        base = os.path.join(SRC, 'results_ocr' if kind == 'ocr' else 'results', stem + '.txt')
        if kind == 'txt':
            base = os.path.join(SRC, 'results', stem + '.txt')
        lines = load_text(base)
        start = next((i for i, l in enumerate(lines) if re.search(r'Consolidated Statement of (Financial Results|Profit and Loss)', l)), None)
        if start is None:
            print('results: no consolidated statement', stem)
            continue
        end = next((i for i in range(start + 1, len(lines)) if re.search(r'Standalone Statement|Segment Information|Consolidated Balance|Reconciliation', lines[i])), len(lines))
        doc_date = rel_doc.get(pe, '')
        url = BASE_URL + fname
        src_doc = f'HCLTech {fiscal_q(pe)} SEBI Reg.33 consolidated Ind AS financial results' + (' (scanned, OCR)' if kind == 'ocr' else '')
        for ln in lines[start:end]:
            m = re.match(r'^\s*(Revenue from operations|Employee benefits? expenses?|Outsourcing costs?)\b(.*)$', ln, re.I)
            if not m:
                continue
            toks = [clean_tok(t) for t in m.group(2).split()]
            vals = [parse_num(t) for t in toks[:3]]
            if len(toks) < 3 or any(v is None or v < 100 for v in vals):
                print('results: skip partial row', stem, ln.strip()[:90])
                continue
            name = m.group(1).lower()
            met = 'revenue' if name.startswith('revenue') else ('employee_cost' if name.startswith('employee') else 'subcontracting_cost')
            for k, v in enumerate(vals):
                if (stem, met, k) in RESULTS_SKIP:
                    print('results: skipped known text-layer OCR error', stem, met, k, v)
                    continue
                q = prev_q(pe, [0, 1, 4][k])
                note = {'revenue': 'Ind AS consolidated revenue from operations (SEBI results)',
                        'employee_cost': 'Employee benefits expense, Ind AS consolidated (SEBI results)',
                        'subcontracting_cost': "'Outsourcing costs' line, Ind AS consolidated statement of profit and loss (SEBI results)"}[met]
                if kind == 'ocr':
                    note += '; OCR of scanned PDF'
                if pe == '2017-03-31' and k == 2:
                    note += '; Q4FY16 comparative restated under Ind AS'
                pe_q = qend(q)
                ROWS.append(dict(firm='hcltech', fiscal_q=fiscal_q(pe_q), period_end=pe_q, cal_q=cal_q(pe_q), metric=met,
                                 dimension='total', dim_type='total', value=v, unit='INR_cr', basis='reported',
                                 period_type='quarter', source_url=url, source_doc=src_doc,
                                 source_loc=('Consolidated statement of financial results, row ' + m.group(1) +
                                             (f'; {loc_extra}' if loc_extra else '')),
                                 doc_date=doc_date, notes=note))


def merge_split_headers(lines):
    """OCR sometimes puts one header date on its own line just above the header row; merge it back."""
    from hcltech_tables import DATE_RE, norm_date
    out = list(lines)
    for i in range(len(out) - 1):
        d1 = list(DATE_RE.finditer(out[i]))
        d2 = list(DATE_RE.finditer(out[i + 1]))
        if len(d1) == 1 and len(d2) >= 2:
            label = out[i + 1][:d2[0].start()].rstrip()
            toks = [m.group(0) for m in d2] + [d1[0].group(0)]
            toks.sort(key=lambda t: norm_date(*DATE_RE.match(t).groups()))
            extra = out[i + 1][d2[-1].end():].strip()
            extra1 = (out[i][:d1[0].start()] + '  ' + out[i][d1[0].end():]).strip()
            out[i + 1] = label + '  ' + '  '.join(toks) + ('  ' + extra if extra else '') + ('  ' + extra1 if extra1 else '')
            out[i] = ''
            print('merged OCR header:', out[i + 1].strip()[:100])
        elif len(d1) >= 2 and len(d2) == 1 and not split_row(out[i + 1])[1]:
            label = (out[i][:d1[0].start()].strip() or out[i + 1][:d2[0].start()].strip())
            toks = [m.group(0) for m in d1] + [d2[0].group(0)]
            toks.sort(key=lambda t: norm_date(*DATE_RE.match(t).groups()))
            extra = out[i][d1[-1].end():].strip()
            out[i] = label + '  ' + '  '.join(toks) + ('  ' + extra if extra else '')
            out[i + 1] = ''
            print('merged OCR header (below):', out[i].strip()[:100])
    return [l for l in out if l.strip()]


def main():
    for stem in DOCS:
        path = os.path.join(SRC, 'ocr' if stem in OCR_DOCS else 'txt', stem + '.txt')
        lines = load_text(path)
        if stem in OCR_DOCS:   # common OCR misreads of the row label 'QoQ'
            lines = [re.sub(r'^(\s*)(900|20l|Q0l|0o0|Q00|QOQ|Q0Q|QoO)(\s{2,})', r'\1QoQ\3', l) for l in lines]
            lines = merge_split_headers(lines)
        handle_cells(extract(lines, stem))
        growth_tables(stem, lines)
        highlight_tables(stem, lines)
    sebi_results()
    for stem, met, val, unit, basis, pt, note, loc in HAND:
        add(stem, DOCS[stem][0], met, 'total', 'total', val, unit, basis, pt, loc, note + '; hand-entered from text')
    add('HCLTech_Q1_FY25_Investor_Release', '2024-06-30', 'headcount_divested', 'total', 'total', 7398, 'count', 'na', 'quarter',
        'Page 1 highlights (People)', '"Reduction in headcount due to divestiture (7,398)"; included in Q1FY25 net addition of (8,080); hand-entered from text')
    add('HCLTech_Q4_FY25_Investor_Release', '2025-03-31', 'headcount_divested', 'total', 'total', 7398, 'count', 'na', 'annual',
        'Page 1 highlights (People)', 'FY25: "Reduction in headcount due to divestiture: 7,398" (same Q1FY25 event); FY25 net addition (4,061); hand-entered from text')
    df = pd.DataFrame(ROWS)
    # annual TCV rows: period_end = FY end (same as Q4) is fine; mark
    df = df.drop_duplicates(['fiscal_q', 'period_end', 'metric', 'dimension', 'dim_type', 'value', 'unit', 'basis',
                             'period_type', 'source_url'])
    cols = ['firm', 'fiscal_q', 'period_end', 'cal_q', 'metric', 'dimension', 'dim_type', 'value', 'unit', 'basis',
            'period_type', 'source_url', 'source_doc', 'source_loc', 'doc_date', 'notes']
    df = df[cols].sort_values(['period_end', 'metric', 'dim_type', 'dimension', 'doc_date']).reset_index(drop=True)
    df.to_csv(OUT, index=False, quoting=csv.QUOTE_MINIMAL)
    print('rows', len(df))
    return df


if __name__ == '__main__':
    main()
