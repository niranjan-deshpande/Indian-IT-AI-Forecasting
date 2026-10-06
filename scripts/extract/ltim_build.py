"""Build data/raw/ltim.csv from LTI / Mindtree / LTIMindtree fact sheets.

Usage: python3 scripts/extract/ltim_build.py
Reads layout-text copies of PDFs (pdftotext -layout) in data/sources/ltim/{txt,mindtree/nse/txt}.
Rows for firm 'lti' / 'mindtree' come from pre-merger standalone documents; rows for firm 'ltim'
come from LTIMindtree documents (including restated combined figures for pre-merger quarters).
Hand-entered rows (scanned documents) are appended from scripts/extract/ltim_hand_entered.csv.
"""
import os, re, sys, csv, collections
sys.path.insert(0, os.path.dirname(__file__))
from ltim_docs import docs, ROOT
from ltim_parse_tables import parse_text, normalize

OUT = os.environ.get('LTIM_OUT', os.path.join(ROOT, 'data', 'raw', 'ltim.csv'))  # LTIM_OUT: write elsewhere (e.g. data/rebuilt/raw) without touching data/raw
HAND = os.path.join(os.path.dirname(__file__), 'ltim_hand_entered.csv')
COLS = ['firm', 'fiscal_q', 'period_end', 'cal_q', 'metric', 'dimension', 'dim_type', 'value', 'unit', 'basis',
        'period_type', 'source_url', 'source_doc', 'source_loc', 'doc_date', 'notes']


def qinfo(fq):
    m = re.match(r"Q([1-4])FY(\d{2})$", fq)
    q, fy = int(m.group(1)), 2000 + int(m.group(2))
    if q == 1: return f"{fy-1}-06-30", f"{fy-1}Q2"
    if q == 2: return f"{fy-1}-09-30", f"{fy-1}Q3"
    if q == 3: return f"{fy-1}-12-31", f"{fy-1}Q4"
    return f"{fy}-03-31", f"{fy}Q1"


def clean(s):
    s = normalize(s)
    s = re.sub(r"\s+", " ", s).strip().strip('*').strip()
    s = s.replace(' .', '.').replace('( ', '(')
    return s


SHARE_SEC = [
    (r"revenue by (vertical|industry)|industry segments|revenue by industr", 'vertical'),
    (r"revenue by service|service offering|service line", 'service_line'),
    (r"revenue by geo|^geography$", 'geography'),
]

FIRM_NOTE = {
    'lti': 'Pre-merger L&T Infotech (LTI) standalone consolidated figures.',
    'mindtree': 'Pre-merger Mindtree standalone consolidated figures.',
    'ltim': 'LTIMindtree combined entity.',
}


def bucket(label):
    m = re.search(r"\$?\s*(\d+)\s*(?:mn|Million)", label, re.I)
    return f"USD{m.group(1)}mn+" if m else None


GLOBAL_DIMS = {}
ORD = []
# trivial label variants of the same segment (typos / wording in an addendum table)
ALIAS = {'Rest of World': 'Rest of the World', 'High-Tech, Media &': 'High-Tech, Media & Entertainment',
         'Platiorm Based Solutions': 'Platform Based Solutions'}


def map_row(firm, sec, subsec, label, col, is_pct, doc_dims):
    """Return (metric, dimension, dim_type, unit, basis, period_type, note) or None."""
    s = sec.lower(); ss = subsec.lower(); l = label.lower()
    isq = col.startswith('Q')
    isg = col in ('qoq', 'yoy', 'qoq_usd', 'yoy_usd', 'qoq_cc', 'yoy_cc')
    if col.startswith('FY'):
        return None
    if re.search(r"(\bat|\bis|\bwas|\bof)$", l) or re.match(r"^(o |• |- |\d+\. )", l):
        return None  # narrative bullet text, not a table row
    if re.search(r"\((inr|usd) mn\)$", l) and s == '':
        return None  # chart titles
    # ---------------- Revenue (company level)
    if '[inr]' in s:
        usd_ctx, inr_ctx = False, True
    elif '[usd]' in s:
        usd_ctx, inr_ctx = True, False
    else:
        usd_ctx = bool(re.search(r"usd|\$ ?m|\$ million|in usd", s)) and not re.search(r"inr|₹", s)
        inr_ctx = bool(re.search(r"inr|₹|financials|income statement", s))
    if re.match(r"^revenue\s*(\(usd million\)|usd mn|\$ ?mn|- ?usd mn|- ?\$ ?mn)$", l) or (l in ('revenue', 'revenues') and usd_ctx):
        if isq and not is_pct:
            return ('revenue', 'total', 'total', 'USD_mn', 'reported', 'quarter', '')
        if isg:
            return (f"revenue_growth_{col[:3]}", 'total', 'total', 'pct', 'reported', 'quarter', 'USD revenue growth')
        return None
    if re.match(r"^revenue\s*(₹ ?millions|- ?₹ ?millions|₹ ?mn)$", l) or (l in ('revenue', 'revenues') and inr_ctx):
        if isq and not is_pct:
            return ('revenue', 'total', 'total', 'INR_mn', 'reported', 'quarter', '')
        return None
    if re.search(r"constant currency|\(cc\)|revenue cc", l) and not re.search(r"reporting", s):
        if isg:
            return (f"revenue_growth_{col[:3]}", 'total', 'total', 'pct', 'cc', 'quarter', '')
        if isq:
            g = 'qoq' if 'qoq' in l else ('yoy' if 'yoy' in l else None)
            if g:
                return (f"revenue_growth_{g}", 'total', 'total', 'pct', 'cc', 'quarter', '')
        return None
    if re.match(r"^(qoq|yoy) growth( %)?$", l) and isq and re.search(r"in usd mn|^revenue$", s):
        return (f"revenue_growth_{l[:3]}", 'total', 'total', 'pct', 'reported', 'quarter', 'USD revenue growth')
    # LTI constant-currency reporting table
    if 'constant currency reporting' in s and isg:
        lab = re.sub(r"^(qoq growth yoy growth\s*)", '', label, flags=re.I).strip()
        if re.search(r"company$", lab, re.I):
            return (f"revenue_growth_{col[:3]}", 'total', 'total', 'pct', 'cc', 'quarter', 'from Constant Currency Reporting table')
        lab = re.sub(r"^(vertical|service offering|geography)\s+", '', lab, flags=re.I).strip()
        dt = doc_dims.get(lab.lower()) or GLOBAL_DIMS.get((firm, lab.lower()))
        if dt:
            return (f"segment_growth_{col[:3]}", lab, dt, 'pct', 'cc', 'quarter', 'from Constant Currency Reporting table')
        return ('__unmapped_cc__', lab, 'other', 'pct', 'cc', 'quarter', '')
    # ---------------- Segment shares
    for pat, dt in SHARE_SEC:
        if re.search(pat, s):
            if l in ('total',):
                return None
            if re.match(r"^digital", l):
                if isq:
                    return ('revenue_share', 'Digital', 'other', 'pct', 'na', 'quarter', 'Digital revenue share (overlaps service lines)')
                if isg:
                    return (f"segment_growth_{col[:3]}", 'Digital', 'other', 'pct', 'cc' if col.endswith('_cc') else 'reported', 'quarter', 'Digital revenue growth')
                return None
            if isq:
                return ('revenue_share', label, dt, 'pct', 'na', 'quarter', '')
            if isg:
                return (f"segment_growth_{col[:3]}", label, dt, 'pct', 'cc' if col.endswith('_cc') else 'reported', 'quarter', 'USD growth' if not col.endswith('_cc') else '')
            return None
    if re.search(r"revenue by project type", s) and isq:
        if re.search(r"fixed", l):
            return ('revenue_share_fixed_price', 'total', 'total', 'pct', 'na', 'quarter', f'Mindtree label: {label}')
        return None
    # ---------------- Onsite / offshore mix
    if isq and re.search(r"offshore", l):
        if re.search(r"fee|billed|\$", ss) or re.search(r"billed|person months", s):
            return None
        if 'effort' in l or ss.startswith('effort') or re.search(r"effort mix|effort (&|and) utili", s):
            return ('effort_share_offshore', 'total', 'total', 'pct', 'na', 'quarter', '')
        if ss == 'revenue' or re.search(r"revenue mix", s):
            return ('revenue_share_offshore', 'total', 'total', 'pct', 'na', 'quarter', '')
        return None
    # ---------------- Utilization
    if isq and ('utili' in l or 'utili' in s or 'utili' in ss):
        if re.search(r"incl(uding|\.)? ?trainees", l):
            return ('utilization_incl_trainees', 'total', 'total', 'pct', 'na', 'quarter', '')
        if re.search(r"excl(uding|\.)? ?trainees", l):
            return ('utilization_excl_trainees', 'total', 'total', 'pct', 'na', 'quarter', '')
        if l == 'utilization' and firm == 'mindtree':
            return ('utilization_incl_trainees', 'total', 'total', 'pct', 'na', 'quarter',
                    "Mindtree row labelled just 'Utilization' (from Q4FY21 doc on); equals the earlier 'Including Trainees' series (e.g. Q4FY20 76.5% in both Q4FY20 and Q4FY21 docs).")
    # ---------------- People
    if isq and re.search(r"attrition", l):
        return ('attrition', 'total', 'total', 'pct', 'na', 'ltm', f'label: {label}')
    if isq and re.search(r"^(total headcount|total mindtree minds|total employees)$", l):
        return ('headcount', 'total', 'total', 'count', 'na', 'point', f'label: {label}')
    if isq and re.search(r"employee|headcount|mindtree minds", s) and re.match(r"^(development|software professionals|sales & support|sales|support)$", l):
        return ('headcount', label, 'other', 'count', 'na', 'point', 'headcount sub-category')
    if isq and l == 'gross additions':
        return ('gross_additions', 'total', 'total', 'count', 'na', 'quarter', '')
    if isq and l == 'net additions':
        return ('net_additions', 'total', 'total', 'count', 'na', 'quarter', '')
    # ---------------- Clients
    if isq and re.search(r"(million dollar|mn\+? ?\+?clients|mn\+ clients|mn clients)", l):
        b = bucket(label)
        if b:
            return ('clients_bucket', b, 'client_bucket', 'count', 'na', 'ltm', f'label: {label}')
    if isq and re.search(r"^(number of active clients|active clients)$", l):
        return ('active_clients', 'total', 'total', 'count', 'na', 'quarter', f'label: {label}')
    if isq and re.search(r"^new clients added", l):
        return ('new_clients', 'total', 'total', 'count', 'na', 'quarter', f'label: {label}')
    if isq and re.match(r"^top (client|\d+ clients)$", l):
        n = re.search(r"\d+", l)
        return ('top_client_share', f"Top {n.group(0) if n else 1}", 'client_bucket', 'pct', 'na', 'quarter', 'share of quarterly revenue')
    # ---------------- Deals
    if isq and re.search(r"order inflow", l):
        return ('tcv', 'total', 'total', 'USD_bn', 'na', 'quarter', 'Order inflow (all deals) as reported')
    if isq and re.search(r"total contract value|tcv", s + ' ' + l):
        if l in ('total', 'overall tcv'):
            return ('tcv', 'total', 'total', 'USD_mn', 'na', 'quarter', 'Mindtree total contract value signed in quarter (renewals + new)')
        if l in ('renewals', 'new'):
            return ('tcv', label, 'other', 'USD_mn', 'na', 'quarter', 'Mindtree TCV component')
        return None
    return None


def cc_text(firm, text):
    """Headline constant-currency growth from press-release text (Mindtree mainly)."""
    out = []
    t = re.sub(r"\s+", " ", normalize(text))
    m = re.search(r"constant currency growth of\s*\(?(-?[\d.]+)%\)?\s*q-o-q", t, re.I)
    if m:
        out.append(('qoq', float(m.group(1)), m.group(0)))
    m = re.search(r"(-?[\d.]+)%\s*QoQ CC growth", t, re.I)
    if m and not out:
        out.append(('qoq', float(m.group(1)), m.group(0)))
    m = re.search(r"CC growth of\s*(-?[\d.]+)%\s*q-o-q", t, re.I)
    if m and not out:
        out.append(('qoq', float(m.group(1)), m.group(0)))
    m = re.search(r"(-?[\d.]+)%\s*(?:YoY|y-o-y) (?:CC|constant currency)", t, re.I)
    if m:
        out.append(('yoy', float(m.group(1)), m.group(0)))
    return out


def main():
    rows = []
    conflicts = []
    for d in docs():
        text = open(d['txt'], encoding='utf-8', errors='replace').read()
        lines = text.split('\n')
        recs = parse_text(lines)
        # page lookup: count form feeds before line
        ff = [0]
        for ln in lines:
            ff.append(ff[-1] + ln.count('\f'))
        # doc-level label -> dim_type from share tables
        doc_dims = {}
        for r in recs:
            for pat, dt in SHARE_SEC:
                if re.search(pat, r['section'].lower()) and r['column'].startswith('Q'):
                    doc_dims.setdefault(clean(r['label']).lower(), dt)
        for k, v in doc_dims.items():
            GLOBAL_DIMS.setdefault((d['firm'], k), v)
        seen = {}
        for r in recs:
            lab = clean(r['label']); sec = clean(r['section']); sub = clean(r['subsec'])
            if r['value'] is None:
                continue
            m = map_row(d['firm'], sec, sub, lab, r['column'], r['is_pct'], doc_dims)
            if not m:
                continue
            metric, dim, dt, unit, basis, ptype, note = m
            if r['how'] == 'ordinal':
                ORD.append((d['doc_id'], metric, lab, r['column'], r['raw'], r['line']))
            dim = ALIAS.get(dim, dim)
            if metric.startswith('__'):
                conflicts.append(('UNMAPPED_CC', d['doc_id'], lab, r['column'], r['raw']))
                continue
            if r['column'].startswith('Q'):
                fq = r['column']
            else:
                fq = d['doc_q']
            key = (fq, metric, dim, basis, unit)
            if key in seen:
                if abs(seen[key] - r['value']) > 1e-9:
                    conflicts.append(('DUP_DIFF', d['doc_id'], key, seen[key], r['value'], r['line']))
                continue
            seen[key] = r['value']
            firm = d['firm']
            pe, cq = qinfo(fq)
            notes = [FIRM_NOTE[firm]]
            if firm == 'ltim' and fq < 'Q3FY23' and fq[-2:] <= '23' and (int(fq[-2:]), int(fq[1])) < (23, 3):
                notes.append('Pre-merger quarter restated on combined LTI+Mindtree basis in LTIMindtree document (merger accounted as common-control combination; comparatives restated).')
            if fq != d['doc_q']:
                notes.append(f'Comparative column in {d["doc_q"]} document.')
            if note:
                notes.append(note)
            if d['doc_id'] == 'lti_Q1FY18_fs' and dt in ('vertical', 'service_line', 'geography'):
                notes.append('LTI reorganised verticals/service lines in Q1FY18; this document re-presents FY16-FY17 mix under the new classification (differs from earlier vintages).')
            if firm == 'ltim' and d['doc_q'] == 'Q1FY27' and dt == 'vertical':
                notes.append('Q1FY27 segment reorganisation (Financial Services / Consumer / Technology & Services / Production); prior periods restated in this document.')
            if metric == 'utilization_excl_trainees' and firm == 'ltim' and fq == 'Q1FY24':
                notes.append('Fact-sheet footnote: 1.6% increase in utilization on account of reclassification of people from delivery to sales and support in Q1FY24.')
            if metric == 'utilization_excl_trainees' and firm == 'mindtree' or (metric.startswith('utilization') and firm == 'mindtree'):
                notes.append('Mindtree: Billed Hours / Available Hours; available hours do NOT exclude leave (per fact sheet).')
            loc = d['loc_prefix'] + f"p{ff[r['line']] + 1}; table '{sec[:60]}'; row '{lab[:60]}'; col {r['column']}"
            rows.append(dict(firm=firm, fiscal_q=fq, period_end=pe, cal_q=cq, metric=metric, dimension=dim,
                             dim_type=dt, value=r['value'], unit=unit, basis=basis, period_type=ptype,
                             source_url=d['url'], source_doc=d['source_doc'], source_loc=loc,
                             doc_date=d['doc_date'], notes=' '.join(notes)))
        # LTIMindtree order inflow from press-release text where not in a table
        if d['firm'] == 'ltim':
            t = re.sub(r"\s+", " ", normalize(text))
            mm = None
            for m_ in re.finditer(r"order inflow[a-z ]{0,45}?(?:at|of|was|reached|stood at)\s*(?:USD|US\$|\$)\s*([\d.]+)\s*(billion|bn)", t, re.I):
                ctx = t[max(0, m_.start() - 90):m_.end()].lower()
                if re.search(r"full[- ]year|fy\d\d full|for the year|annual", ctx):
                    continue
                mm = m_
                break
            key = (d['doc_q'], 'tcv', 'total', 'na', 'USD_bn')
            if mm and key not in seen:
                seen[key] = float(mm.group(1))
                pe, cq = qinfo(d['doc_q'])
                rows.append(dict(firm='ltim', fiscal_q=d['doc_q'], period_end=pe, cal_q=cq, metric='tcv', dimension='total',
                                 dim_type='total', value=float(mm.group(1)), unit='USD_bn', basis='na', period_type='quarter',
                                 source_url=d['url'], source_doc=d['source_doc'], source_loc=f'press release text: "{mm.group(0)[:80]}"',
                                 doc_date=d['doc_date'], notes=FIRM_NOTE['ltim'] + ' Order inflow (all deals) from press-release text.'))
        # headline cc growth from text for Mindtree (not in tables)
        if d['firm'] == 'mindtree':
            for g, v, snip in cc_text(d['firm'], text):
                key = (d['doc_q'], f'revenue_growth_{g}', 'total', 'cc', 'pct')
                if key in seen:
                    continue
                seen[key] = v
                pe, cq = qinfo(d['doc_q'])
                rows.append(dict(firm='mindtree', fiscal_q=d['doc_q'], period_end=pe, cal_q=cq,
                                 metric=f'revenue_growth_{g}', dimension='total', dim_type='total', value=v,
                                 unit='pct', basis='cc', period_type='quarter', source_url=d['url'],
                                 source_doc=d['source_doc'], source_loc=d['loc_prefix'] + f'press release text: "{snip[:80]}"',
                                 doc_date=d['doc_date'], notes=FIRM_NOTE['mindtree'] + ' Headline constant-currency growth from press-release text.'))
    # hand-entered rows
    if os.path.exists(HAND):
        for r in csv.DictReader(open(HAND)):
            rows.append({k: r.get(k, '') for k in COLS})
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for r in sorted(rows, key=lambda r: (r['firm'], r['period_end'], r['metric'], r['dimension'], r['doc_date'])):
            v = r['value']
            if isinstance(v, float):
                r['value'] = ('%.4f' % v).rstrip('0').rstrip('.')
            w.writerow(r)
    with open('/tmp/ltim_conflicts.txt', 'w') as f:
        for c in conflicts:
            f.write(repr(c) + '\n')
    print('rows', len(rows), 'conflicts', len(conflicts))
    with open('/tmp/ltim_ordinal.txt', 'w') as f:
        for o in ORD:
            f.write(repr(o) + '\n')


if __name__ == '__main__':
    main()
