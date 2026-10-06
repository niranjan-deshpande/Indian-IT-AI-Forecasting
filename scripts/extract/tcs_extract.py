#!/usr/bin/env python3
"""Extract TCS quarterly metrics from locally saved fact sheets / analyst presentations.

Inputs : data/sources/tcs/*.pdf  (downloaded from tcs.com investor-relations via in-app browser)
         data/sources/tcs/_tcs_pdf_links.txt   (original tcs.com URLs, one per line)
         data/sources/tcs/_transcript_urls.tsv (local transcript name -> URL)
Output : data/raw/tcs.csv

Run    : python3 scripts/extract/tcs_extract.py
"""
import csv, os, re, subprocess, sys, urllib.parse, datetime
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'data', 'sources', 'tcs')
TXT = os.path.join(SRC, 'txt')
OUT = os.path.join(ROOT, 'data', 'raw', 'tcs.csv')
BASE = 'https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/'

FIELDS = ['firm', 'fiscal_q', 'period_end', 'cal_q', 'metric', 'dimension', 'dim_type', 'value', 'unit',
          'basis', 'period_type', 'source_url', 'source_doc', 'source_loc', 'doc_date', 'notes']
rows = []
warnings = []

# ---------------------------------------------------------------- helpers

def pdftotext(pdf, txt):
    if not os.path.exists(txt) or os.path.getmtime(txt) < os.path.getmtime(pdf):
        subprocess.run(['pdftotext', '-layout', pdf, txt], check=True)
    return open(txt, encoding='utf-8', errors='replace').read()


def fq_info(label):
    """'Q1 FY16' / 'Q1FY16' / 'FY16' -> (fiscal_q, period_end, cal_q, period_type)"""
    label = label.replace(' ', '')
    m = re.fullmatch(r'Q([1-4])FY(\d{2})', label)
    if m:
        q, fy = int(m.group(1)), 2000 + int(m.group(2))
        y, md, cq = {1: (fy - 1, '06-30', 2), 2: (fy - 1, '09-30', 3), 3: (fy - 1, '12-31', 4), 4: (fy, '03-31', 1)}[q]
        return f'Q{q}FY{fy % 100:02d}', f'{y}-{md}', f'{y}Q{cq}', 'quarter'
    m = re.fullmatch(r'FY(\d{2})', label)
    if m:
        fy = 2000 + int(m.group(1))
        return f'FY{fy % 100:02d}', f'{fy}-03-31', f'{fy}Q1', 'annual'
    raise ValueError(label)


def num(s):
    """Parse a numeric cell: '1,234', '(0.3)', '- 0.4', '-6,333', '5,09,058', '8.9%'. Returns float or None."""
    if s is None:
        return None
    s = s.strip().replace('%', '').replace('`', '').replace('₹', '').replace('$', '').strip()
    if s in ('', '-', 'NA', 'N.A.', 'na', '--', '–'):
        return None
    neg = False
    if s.startswith('(') and s.endswith(')'):
        neg, s = True, s[1:-1].strip()
    if s.startswith('+'):
        s = s[1:].strip()
    if s.startswith('-') or s.startswith('–'):
        neg, s = True, s[1:].strip()
    s = s.replace(',', '')
    if not re.fullmatch(r'\d+(\.\d+)?', s):
        return None
    v = float(s)
    return -v if neg else v


def fmt(v):
    if v is None:
        return ''
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return repr(round(v, 4))


def add(fiscal_label, metric, dimension, dim_type, value, unit, basis, period_type, doc, loc, notes=''):
    fq, pe, cq, pt = fq_info(fiscal_label)
    if period_type is None:
        period_type = pt
    rows.append(dict(firm='tcs', fiscal_q=fq, period_end=pe, cal_q=cq, metric=metric, dimension=dimension,
                     dim_type=dim_type, value=fmt(value), unit=unit, basis=basis, period_type=period_type,
                     source_url=doc['url'], source_doc=doc['name'], source_loc=loc, doc_date=doc['date'],
                     notes=notes))


MONTHS = {m: i for i, m in enumerate(['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'], 1)}


def doc_date(text):
    head = '\n'.join(text.splitlines()[:15])
    m = re.search(r'(\d{1,2})(?:st|nd|rd|th)?\s+([A-Z][a-z]+)\.?,?\s+(20\d\d)', head)
    if m and m.group(2)[:3].lower() in MONTHS:
        return f'{m.group(3)}-{MONTHS[m.group(2)[:3].lower()]:02d}-{int(m.group(1)):02d}'
    m = re.search(r'([A-Z][a-z]+)\.?\s+(\d{1,2}),?\s+(20\d\d)', head)
    if m and m.group(1)[:3].lower() in MONTHS:
        return f'{m.group(3)}-{MONTHS[m.group(1)[:3].lower()]:02d}-{int(m.group(2)):02d}'
    return ''


# ---------------------------------------------------------------- URL map
links = [l.strip() for l in open(os.path.join(SRC, '_tcs_pdf_links.txt')) if l.strip()]


def find_url(year, q, pred):
    for l in links:
        d = urllib.parse.unquote(l)
        if f'/financial-statements/{year}/{q}/' in d and pred(d.split('/')[-1], d):
            return l
    return None


# ---------------------------------------------------------------- table parser
PERIOD_RE = re.compile(r'Q[1-4]\s?FY\s?\d{2}|(?<![A-Za-z])FY\s?\d{2}(?!\d)')
TABLE_HDR = re.compile(r'^\s*(Geography|IP Revenue|SP Revenue|Vertical|Service Line|Market)\s*\(\s*%\s*\)\s+(.*)$')
DIMTYPE = {'Geography': 'geography', 'Market': 'geography', 'IP Revenue': 'vertical', 'Vertical': 'vertical',
           'SP Revenue': 'service_line', 'Service Line': 'service_line'}


def cells(line):
    parts = [p for p in re.split(r'\s{2,}', line.strip()) if p != '']
    return parts


def growth_basis(tok):
    t = tok.replace(' ', '').lower()
    if t.startswith('cc'):
        return 'cc', ''
    if t.startswith('inr') or t.startswith('`') or t.startswith('₹'):
        return 'reported_inr', 'INR-terms growth'
    if t.startswith('$') or t.startswith('usd'):
        return 'reported', 'USD-terms growth'
    return 'reported_inr', 'growth column labelled only "Growth" (currency not stated; TCS reporting currency is INR)'


def parse_tables(lines, doc, cur_label):
    """Revenue-mix tables. Columns are located by x-position (Q4 decks interleave FY columns after growth
    columns). Returns dict of total-row growth values found (for cross-checks)."""
    totals = {}
    for i, line in enumerate(lines):
        m = TABLE_HDR.match(line)
        if not m:
            continue
        title = m.group(1)
        pcols = [((mm.start() + mm.end()) / 2, 'p', mm.group(0).replace(' ', ''))
                 for mm in PERIOD_RE.finditer(line) if mm.start() >= m.start(2)]
        if not pcols:
            continue
        top = []
        for j in range(i - 1, max(i - 4, -1), -1):
            t = list(re.finditer(r'Q-o-Q|Y-o-Y|YoY|QoQ', lines[j]))
            if t:
                top = t
                break
        bot = []
        for j in range(i + 1, min(i + 3, len(lines))):
            b = list(re.finditer(r'CC Growth|INR Growth|USD Growth|\$ Growth|` Growth|₹ Growth|Growth', lines[j]))
            if b:
                bot = b
                break
        # merge sub-matches ('CC Growth' also matches 'Growth')
        bot = [b for b in bot if not any(o is not b and o.start() < b.start() < o.end() for o in bot)]
        gcols = []
        for k, t in enumerate(top):
            if bot:
                bb = min(bot, key=lambda b: abs((b.start() + b.end()) / 2 - (t.start() + t.end()) / 2))
                basis, bnote = growth_basis(bb.group(0))
            else:
                basis, bnote = growth_basis('Growth')
            metric = 'segment_growth_qoq' if t.group(0) in ('Q-o-Q', 'QoQ') else 'segment_growth_yoy'
            gcols.append(((t.start() + t.end()) / 2, 'g', (metric, basis, bnote)))
        cols = sorted(pcols + gcols, key=lambda c: c[0])
        # growth column period = nearest period column to its left (FY -> annual growth)
        colspec = []
        last_p = None
        for x, kind, info in cols:
            if kind == 'p':
                last_p = info
                colspec.append((x, 'p', info))
            else:
                per = last_p if (last_p and last_p.startswith('FY')) else cur_label
                colspec.append((x, 'g', info + (per,)))
        ncol = len(colspec)
        if re.search(r'Growth in INR terms|based on actual revenues in INR', '\n'.join(lines[i:i + 30])):
            colspec = [(x, k, (info[0], info[1], 'INR-terms growth (per table footnote)', info[3]) if k == 'g' and info[1] == 'reported_inr' else info)
                       for x, k, info in colspec]
        dim_type = DIMTYPE[title]
        loc = f'{title} (%) table'
        after_total = 0
        for j in range(i + 1, min(i + 45, len(lines))):
            ln = lines[j]
            if not ln.strip():
                continue
            if j <= i + 2 and re.search(r'Growth', ln) and not re.search(r'\d', ln):
                continue
            c = cells(ln)
            k = 0
            while k < len(c) and num(c[k]) is None and c[k] not in ('-', 'NA'):
                k += 1
            label = re.sub(r'\s*\*+$', '', ' '.join(c[:k]).strip())
            if not label or re.match(r'^\d+$', label):
                continue
            if after_total:
                after_total += 1
                if after_total > 3:
                    break
                if not label.startswith('Digital Revenue'):
                    continue
                label = 'Digital'
            # numeric cells with positions
            numcells = []
            for mm in re.finditer(r'\(?[+\-–]?\s?\d[\d,]*(?:\.\d+)?\)?|(?<=\s)(?:NA|-)(?=\s|$)', ln):
                if mm.start() < len(ln) - len(ln.lstrip()) + len(' '.join(c[:k])):
                    continue
                numcells.append(((mm.start() + mm.end()) / 2, num(mm.group(0))))
            if not numcells:
                if label.lower().startswith('total'):
                    break
                continue  # group header e.g. 'Americas'
            note = ''
            if len(numcells) == ncol:
                assign = list(zip(colspec, [v for _, v in numcells]))
            elif len(numcells) < ncol:
                used = set()
                assign = []
                for x, v in numcells:
                    best = min((q for q in range(ncol) if q not in used), key=lambda q: abs(colspec[q][0] - x))
                    used.add(best)
                    assign.append((colspec[best], v))
                warnings.append(f'{doc["name"]}: {title} row "{label}" has {len(numcells)} cells < {ncol}; x-matched')
                note = 'row had fewer cells than header columns; matched to columns by position (check source)'
            else:
                warnings.append(f'{doc["name"]}: {title} row "{label}" has {len(numcells)} cells > {ncol}; skipped')
                continue
            is_total = label.lower().startswith('total')
            dt = 'other' if label == 'Digital' else dim_type
            dnote = 'Digital revenue (TCS-defined) row printed below this table' if label == 'Digital' else ''
            for (x, kind, info), v in assign:
                if v is None:
                    continue
                if kind == 'p':
                    if is_total:
                        continue
                    add(info, 'revenue_share', label, dt, v, 'pct', 'na', None, doc, loc,
                        '; '.join(z for z in [dnote, note, 'full-year share' if info.startswith('FY') else ''] if z))
                else:
                    metric, basis, bnote, per = info
                    if is_total:
                        if title in ('Geography', 'Market'):
                            totals[(metric.replace('segment_', 'revenue_'), basis, per)] = v
                        continue
                    add(per, metric, label, dt, v, 'pct', basis, None, doc, loc, '; '.join(z for z in [dnote, bnote, note] if z))
            if is_total:
                after_total = 1
    return totals


def parse_restated(lines, doc):
    """Recast history tables: 'Vertical (%)' alone on a line, next line = quarter labels repeated for
    '% Revenue' block and a growth block (e.g. Q1FY18 deck: FY17 quarters recast to new verticals)."""
    for i, line in enumerate(lines):
        m = re.match(r'^\s*(Vertical|Geography|Service Line)\s*\(%\)\s*$', line)
        if not m:
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        labs = [x.replace(' ', '') for x in PERIOD_RE.findall(lines[j])]
        if len(labs) < 4 or len(labs) % 2:
            continue
        half = len(labs) // 2
        if labs[:half] != labs[half:]:
            continue
        above = ' '.join(lines[max(0, i - 3):i])
        gm = 'segment_growth_qoq' if re.search(r'Q-o-Q', above) else 'segment_growth_yoy'
        gb = 'cc' if re.search(r'CC', above) else 'reported_inr'
        title = m.group(1)
        dim_type = DIMTYPE[title]
        loc = f'{title} (%) recast history table'
        for k in range(j + 1, min(j + 40, len(lines))):
            c = cells(lines[k])
            if not c:
                continue
            q = 0
            while q < len(c) and num(c[q]) is None:
                q += 1
            label = re.sub(r'\s*\*+$', '', ' '.join(c[:q]).strip())
            vals = [num(v) for v in c[q:]]
            if not label or not vals:
                continue
            if len(vals) != len(labs):
                warnings.append(f'{doc["name"]}: recast row {label} {len(vals)} vs {len(labs)}')
                continue
            tot = label.lower().startswith('total')
            for lab, v in zip(labs[:half], vals[:half]):
                if not tot and v is not None:
                    add(lab, 'revenue_share', label, dim_type, v, 'pct', 'na', None, doc, loc,
                        'restated to new segment definitions in this document')
            for lab, v in zip(labs[half:], vals[half:]):
                if v is None:
                    continue
                if tot:
                    add(lab, gm.replace('segment_', 'revenue_'), 'total', 'total', v, 'pct', gb, None, doc, loc,
                        'company total growth, Total row of recast table')
                else:
                    add(lab, gm, label, dim_type, v, 'pct', gb, None, doc, loc, 'restated to new segment definitions in this document')
            if tot:
                break


def parse_digital(lines, doc):
    for i, line in enumerate(lines):
        m = re.match(r'^\s*Digital Revenue\s*\(%\)\s+(.*)$', line)
        if not m:
            continue
        vals = [num(v) for v in cells(m.group(1))]
        # period labels on a line above
        labels, top = [], []
        for j in range(i - 1, max(i - 6, -1), -1):
            ls = [x.replace(' ', '') for x in PERIOD_RE.findall(lines[j])]
            if ls and not labels:
                labels = ls
                tp = re.findall(r'Q-o-Q|Y-o-Y|YoY|QoQ', lines[j])
                if tp:
                    top = tp
            elif not top:
                tp = re.findall(r'Q-o-Q|Y-o-Y|YoY|QoQ', lines[j])
                if tp and labels:
                    top = tp
            if labels and top:
                break
        if not labels:
            warnings.append(f'{doc["name"]}: digital revenue row without labels')
            continue
        # tokens may be on the line just after
        if not top:
            for j in range(i - 3, i):
                top += re.findall(r'Q-o-Q|Y-o-Y|YoY|QoQ', lines[j])
        if len(vals) != len(labels) + len(top):
            warnings.append(f'{doc["name"]}: digital revenue row {len(vals)} vals vs {len(labels)}+{len(top)} cols; skipped')
            continue
        for lab, v in zip(labels, vals):
            add(lab, 'revenue_share', 'Digital', 'other', v, 'pct', 'na', None, doc, 'Digital Revenue (%) row',
                'Digital revenue as % of total (TCS-defined, disclosed FY17-FY20)')
        cur = [l for l in labels if l.startswith('Q')][-1]
        fy = [l for l in labels if l.startswith('FY')]
        for k, (t, v) in enumerate(zip(top, vals[len(labels):])):
            per = fy[-1] if (t == 'YoY' and fy) else cur
            add(per, 'segment_growth_qoq' if t in ('Q-o-Q', 'QoQ') else 'segment_growth_yoy', 'Digital', 'other', v,
                'pct', 'cc', None, doc, 'Digital Revenue (%) row', 'column header not labelled CC in row; assumed CC like adjacent tables')
        break


CLIENT_DIM = {'1': 'USD1mn+', '5': 'USD5mn+', '10': 'USD10mn+', '20': 'USD20mn+', '50': 'USD50mn+', '100': 'USD100mn+'}


def parse_clients(lines, doc, cur_label):
    for i, line in enumerate(lines):
        if 'Clients Contribution' not in line:
            continue
        labels = [x.replace(' ', '') for x in PERIOD_RE.findall(line)]
        if not labels:
            for j in list(range(i + 1, i + 4)) + list(range(i - 1, i - 4, -1)):
                labels = [x.replace(' ', '') for x in PERIOD_RE.findall(lines[j])]
                if labels:
                    break
        if not labels:
            warnings.append(f'{doc["name"]}: clients table without labels')
            continue
        for j in range(i + 1, i + 16):
            m = re.match(r'^\s*US\$\s*(\d+)\s*(?:m|mln|mn|million)\+?\s*Clients?\s+(.*)$', lines[j], re.I)
            if not m:
                continue
            vals = [num(v) for v in cells(m.group(2))]
            if len(vals) != len(labels):
                warnings.append(f'{doc["name"]}: clients row {m.group(1)} {len(vals)} vs {len(labels)}')
                continue
            for lab, v in zip(labels, vals):
                note = 'LTM services revenue'
                if lab.startswith('FY') and ('Q4' + lab) in labels:
                    continue  # quarter column for Q4 already present
                if lab.startswith('FY'):
                    # full-year column: count of clients by FY revenue == LTM at Q4
                    note += f'; column labelled {lab} (full-year), assigned to Q4{lab}'
                    lab = 'Q4' + lab
                if 'Excluding Domestic' in '\n'.join(lines[i:i + 40]):
                    note += '; excluding domestic (India) clients'
                add(lab, 'clients_bucket', CLIENT_DIM[m.group(1)], 'client_bucket', v, 'count', 'na', 'ltm', doc,
                    'Client Parameters table', note)
        break


def parse_usd_chart(lines, doc, cur_label):
    """5-quarter USD revenue bar chart ('Growth Summary (USD)'): map values to quarter labels by x-position."""
    for i, line in enumerate(lines):
        if 'Growth Summary (USD)' not in line:
            continue
        # x where the second (growth) chart starts, from the chart-title line
        split = None
        for j in range(i + 1, min(i + 4, len(lines))):
            mm = re.search(r'(Y-o-Y|Q-o-Q|Y-0-Y|Q-0-Q)\s*Growth', lines[j])
            if mm:
                split = mm.start() - 5
                break
        if split is None:
            continue
        labs = None
        for j in range(i + 1, min(i + 30, len(lines))):
            cand = [mm for mm in re.finditer(r'Q[1-4] ?FY ?\d{2}', lines[j]) if mm.start() < split]
            if len(cand) >= 4:
                labs = cand
                break
        if not labs:
            continue  # e.g. full-year chart in Q4 decks (FY labels only)
        centers = [((mm.start() + mm.end()) / 2, mm.group(0).replace(' ', '')) for mm in labs]
        found = {}
        for k in range(i + 1, j):
            for mm in re.finditer(r'(?<![\d.,])(\d{1,2},\d{3})(?![\d.,%])', lines[k]):
                if mm.start() > split:
                    continue
                c = (mm.start() + mm.end()) / 2
                lab = min(centers, key=lambda t: abs(t[0] - c))[1]
                v = num(mm.group(1))
                if lab in found and found[lab] != v:
                    warnings.append(f'{doc["name"]}: USD chart conflict {lab}')
                    found[lab] = None
                    continue
                found.setdefault(lab, v)
        for lab, v in found.items():
            if lab == cur_label.replace(' ', '') or v is None:
                continue  # current quarter recorded from highlights text
            add(lab, 'revenue', 'total', 'total', v, 'USD_mn', 'reported', None, doc,
                'Growth Summary (USD) revenue chart', 'chart data label; prior-quarter vintage from this document')


def growth_tokens(s):
    """Return list of (value, 'qoq'/'yoy'/None) from a highlight phrase."""
    out = []
    s = s.replace('|', ',')
    for m in re.finditer(r'(up|down|de-growth of|growth of)?\s*(\(?[+\-–]?\s*\d+(?:\.\d+)?\)?)\s*%\s*(QoQ|YoY|QOQ|Q-o-Q|Y-o-Y)?|(flat|Flat)\s*(QoQ|YoY)', s):
        if m.group(4):
            out.append((0.0, m.group(5).lower(), 'reported as "flat"'))
            continue
        v = num(m.group(2))
        if v is None:
            continue
        w = (m.group(1) or '').lower()
        if w in ('down', 'de-growth of') and v > 0:
            v = -v
        per = m.group(3).lower().replace('-', '') if m.group(3) else None
        out.append((v, per, ''))
    return out


def block(lines, heading_re):
    for i, l in enumerate(lines):
        if re.search(heading_re, l):
            end = i + 1
            while end < len(lines) and end < i + 40 and not re.search(r'Performance Highlights|Growth Summary|Financial Performance|Disclaimer', lines[end]):
                end += 1
            return lines[i:end]
    return None


def parse_highlights(lines, doc, cur_label, totals, is_q4):
    q = cur_label  # e.g. 'Q1 FY16'
    qn = q.replace(' ', '')
    blk = block(lines, r'^\s*' + q.replace(' ', r'\s*') + r'\s+Performance Highlights')
    if blk is None:
        # older decks: single highlights block
        blk = block(lines, r'Performance Highlights') or lines[:80]
        warnings.append(f'{doc["name"]}: used generic highlights block')
    text = '\n'.join(blk)
    loc = f'{qn} Performance Highlights'
    got = set()
    m = re.search(r'USD Revenue of \$\s*([\d,]+)\s*Mn,?(.*)', text)
    if m:
        add(q, 'revenue', 'total', 'total', num(m.group(1)), 'USD_mn', 'reported', None, doc, loc)
        for v, per, n in growth_tokens(m.group(2)):
            if per:
                add(q, f'revenue_growth_{per}', 'total', 'total', v, 'pct', 'reported', None, doc, loc,
                    '; '.join(x for x in ['USD-terms growth', n] if x))
    else:
        warnings.append(f'{doc["name"]}: no USD revenue in highlights')
    m = re.search(r'INR Revenue of\s*[`₹]?\s*([\d,]+)\s*Mn,?(.*)', text)
    if m:
        add(q, 'revenue', 'total', 'total', num(m.group(1)), 'INR_mn', 'reported', None, doc, loc)
        for v, per, n in growth_tokens(m.group(2)):
            if per:
                add(q, f'revenue_growth_{per}', 'total', 'total', v, 'pct', 'reported_inr', None, doc, loc,
                    '; '.join(x for x in ['INR-terms growth', n] if x))
    m = re.search(r'(?:Constant currency|CC) revenue\s*(.*)', text, re.I)
    if m:
        phrase = re.split(r'[;,]?\s*Volume growth', m.group(1), flags=re.I)[0]
        for v, per, n in growth_tokens(phrase):
            note = n
            if per is None:
                # unlabeled: resolve against geography-table Total row
                if totals.get(('revenue_growth_qoq', 'cc', qn)) == v:
                    per, note = 'qoq', 'period (QoQ) not labelled in highlight; matched Geography table Total QoQ CC'
                elif totals.get(('revenue_growth_yoy', 'cc', qn)) == v:
                    per, note = 'yoy', 'period (YoY) not labelled in highlight; matched Geography table Total YoY CC'
                else:
                    warnings.append(f'{doc["name"]}: unlabeled CC growth {v} unresolved')
                    continue
            add(q, f'revenue_growth_{per}', 'total', 'total', v, 'pct', 'cc', None, doc, loc, note)
            got.add((f'revenue_growth_{per}', 'cc', qn))
    # table totals not already covered by highlight
    for (mt, basis, per), v in totals.items():
        if basis != 'cc':
            continue
        if (mt, basis, per) in got:
            continue
        add(per, mt, 'total', 'total', v, 'pct', basis, None, doc, 'Geography (%) table, Total row',
            'company total growth from Total row of geography table')
    # headcount
    m = re.search(r'[Cc]losing headcount\s*:?\s*([\d,]+)', text)
    hc = num(m.group(1)) if m else None
    if hc is None:
        m = re.search(r'Total Employees\s*:\s*([\d,]+)', '\n'.join(lines))
        hc = num(m.group(1)) if m else None
        loc_hc = 'Total Employee Base slide'
    else:
        loc_hc = loc
    if hc is None:
        # FY22+ decks: chart only; take the last chart label (current quarter) in Total Employee Base slide
        for i, l in enumerate(lines):
            if 'Total Employee Base' in l:
                seg = lines[i:i + 25]
                labs_line = [s for s in seg if re.search(r'Q[1-4]-\d\d\s+Q[1-4]-\d\d', s)]
                nums = [(k, mm) for k, s in enumerate(seg) for mm in re.finditer(r'(?<![\d,])(\d{1,2},?\d{2},\d{3}|\d{3},\d{3})(?![\d,])', s)]
                if labs_line and nums:
                    lastlab = list(re.finditer(r'Q[1-4]-\d\d', labs_line[0]))[-1]
                    c0 = (lastlab.start() + lastlab.end()) / 2
                    best = min(nums, key=lambda t: abs((t[1].start() + t[1].end()) / 2 - c0))
                    hc = num(best[1].group(1))
                    loc_hc = 'Total Employee Base chart (rightmost bar)'
                break
    if hc is not None:
        add(q, 'headcount', 'total', 'total', hc, 'count', 'na', 'point', doc, loc_hc,
            'consolidated closing headcount (TCS incl. subsidiaries)')
    else:
        warnings.append(f'{doc["name"]}: no headcount')
    # net / gross additions (quarterly only)
    m = re.search(r'(9M FY\d\d |FY\d\d )?[Nn]et addition of\s*(\(?-?[\d,]+\)?)\s*(associates)?\s*(YoY)?', text)
    if m and not m.group(1) and not m.group(4):
        add(q, 'net_additions', 'total', 'total', num(m.group(2)), 'count', 'na', 'quarter', doc, loc)
    else:
        m2 = re.search(r'Net [Aa]dditions:?\s*(\(?-?[\d,]+\)?)', '\n'.join(lines))
        if m2 and not (m and (m.group(1) or m.group(4))):
            add(q, 'net_additions', 'total', 'total', num(m2.group(1)), 'count', 'na', 'quarter', doc,
                'Human Resources / Employee Addition slide')
        elif m:
            pt = 'ytd' if m.group(1) and m.group(1).startswith('9M') else 'other'
            add(q, 'net_additions', 'total', 'total', num(m.group(2)), 'count', 'na',
                'ytd' if pt == 'ytd' else 'ltm', doc, loc,
                '9M YTD net additions' if pt == 'ytd' else 'YoY (trailing 4-quarter) net additions as stated')
    m = re.search(r'Gross addition of\s*([\d,]+)', text)
    if m:
        add(q, 'gross_additions', 'total', 'total', num(m.group(1)), 'count', 'na', 'quarter', doc, loc)
    else:
        m = re.search(r'Gross [Aa]dditions:?\s*([\d,]+)', '\n'.join(lines))
        if m:
            add(q, 'gross_additions', 'total', 'total', num(m.group(1)), 'count', 'na', 'quarter', doc,
                'Human Resources / Employee Addition slide')
    alltext = '\n'.join(lines)
    m = re.search(r'([\d,]+)\s*Trainees\s*(?:&|and)\s*([\d,]+)\s*Laterals', alltext)
    if m:
        add(q, 'fresher_hires', 'total', 'total', num(m.group(1)), 'count', 'na', 'quarter', doc,
            'Gross Additions breakdown', 'trainees (freshers) hired in India during the quarter; laterals in India = ' + m.group(2))
    else:
        m = re.search(r'•\s*([\d,]+)\s*Trainees', alltext)
        if m:
            add(q, 'fresher_hires', 'total', 'total', num(m.group(1)), 'count', 'na', 'quarter', doc,
                'Employee Addition slide', 'trainees (freshers) hired in India during the quarter (first/quarter column)')
    # attrition
    att = {}
    pats = [(r'([\d.]+)\s*%?\s*\(LTM\),?\s*(IT Services|including BPS|Including BPS|including BPO|Consolidated)', 'Human Resources slide'),
            (r'IT Services:\s*([\d.]+)\s*%\s*\(LTM\)()', 'Human Resources slide'),
            (r'([\d.]+)\s*%\s*LTM Attrition\*?\s*[–-]\s*(IT Services)', 'Human Resources slide'),
            (r'LTM [Aa]ttrition[^\n%]*?([\d.]+)%\s*in (IT Services)', loc),
            (r'LTM Attrition \((IT Services)\)[^\d\n]{0,40}\n?[^\d\n]{0,40}([\d.]+)\s*%', 'Performance Highlights (swap)'),
            (r'([\d.]+)\s*%\s*\(LTM\),\s*(including)\s*\n[^\n]*\bBPS\b', 'Human Resources slide')]
    for pat, where in pats:
        for m in re.finditer(pat, alltext):
            if where.endswith('(swap)'):
                att.setdefault('IT Services', (num(m.group(2)), loc, 'IT Services'))
                continue
            g2 = m.group(2) or 'IT Services'
            if g2 == 'including':
                g2 = 'including BPS'
            dim = 'IT Services' if 'IT' in g2 else ('Including BPS' if ('BPS' in g2 or 'BPO' in g2) else 'Consolidated')
            att.setdefault(dim, (num(m.group(1)), where, g2))
    vol = 'voluntary ' if re.search(r'Voluntary Attrition', alltext) else ''
    sub = 'excluding subsidiaries' if re.search(r'Excluding Subsidiaries', alltext, re.I) else ''
    if re.search(r'Excluding CMC', alltext):
        sub = 'excluding CMC & Diligenta (per footnote)'
    for dim, (v, where, g2) in att.items():
        add(q, 'attrition', dim, 'other', v, 'pct', 'na', 'ltm', doc, where,
            '; '.join(x for x in [f'LTM {vol}attrition, {dim}' + (' (labelled "including BPO")' if 'BPO' in g2 else ''), sub] if x))
    m = re.search(r'Quarterly Annualized Attrition[^\n]*?([\d.]+)%', text)
    if m:
        add(q, 'attrition', 'IT Services (quarterly annualized)', 'other', num(m.group(1)), 'pct', 'na', 'quarter',
            doc, loc, 'quarterly annualized attrition as stated in highlights')
    # utilization
    m = re.search(r'Utili[sz]ation at\s*([\d.]+)%\s*\(ex-trainees\)\s*and\s*([\d.]+)%\s*\(including trainees\)', text)
    if m:
        foot = 'excluding CMC & Diligenta' if re.search(r'Excluding CMC', alltext) else ''
        add(q, 'utilization_excl_trainees', 'total', 'total', num(m.group(1)), 'pct', 'na', 'quarter', doc, loc,
            '; '.join(x for x in ['TCS utilization excl. trainees', foot] if x))
        add(q, 'utilization_incl_trainees', 'total', 'total', num(m.group(2)), 'pct', 'na', 'quarter', doc, loc,
            '; '.join(x for x in ['TCS utilization incl. trainees', foot] if x))
    # TCV
    m = re.search(r'Order book TCV at \$\s*([\d.]+)\s*Bn(.*)', text)
    if m:
        add(q, 'tcv', 'total', 'total', num(m.group(1)), 'USD_bn', 'reported', 'quarter', doc, loc,
            'order book TCV of deals signed in the quarter')
        for mm in re.finditer(r'([A-Z][A-Za-z ]+?) TCV at \$\s*([\d.]+)\s*Bn', m.group(2)):
            nm = mm.group(1).strip()
            dt = 'geography' if nm in ('North America', 'UK', 'Europe') else 'vertical'
            add(q, 'tcv', nm, dt, num(mm.group(2)), 'USD_bn', 'reported', 'quarter', doc, loc,
                'order book TCV of deals signed in the quarter')
    m = re.search(r'Active clients:?\s*([\d,]+)', text, re.I)
    if m:
        add(q, 'active_clients', 'total', 'total', num(m.group(1)), 'count', 'na', 'point', doc, loc)
    # full-year block (Q4 decks)
    if is_q4:
        fy = 'FY' + qn[-2:]
        fb = block(lines, r'^\s*FY\s?' + qn[-2:] + r'\s+Performance Highlights')
        if fb:
            ft = '\n'.join(fb)
            floc = f'{fy} Performance Highlights'
            m = re.search(r'USD Revenue of \$\s*([\d,]+)\s*Mn', ft)
            if m:
                add(fy, 'revenue', 'total', 'total', num(m.group(1)), 'USD_mn', 'reported', 'annual', doc, floc)
            m = re.search(r'Order book TCV at \$\s*([\d.]+)\s*Bn', ft)
            if m:
                add(fy, 'tcv', 'total', 'total', num(m.group(1)), 'USD_bn', 'reported', 'annual', doc, floc,
                    'full-year order book TCV')
            m = re.search(r'Net addition of\s*(\(?-?[\d,]+\)?)', ft)
            if m:
                add(fy, 'net_additions', 'total', 'total', num(m.group(1)), 'count', 'na', 'annual', doc, floc)


def parse_cost_lines(lines, doc, cur_label, is_q4):
    """'Fees to external consultants' and 'Employee cost' lines in COR/SG&A detail tables; Expense by Nature."""
    for i, line in enumerate(lines):
        m = re.match(r'^\s*(Fees to [Ee]xternal consultants|Employee [Cc]ost)\s+(.*)$', line)
        if not m:
            continue
        item = 'subcontracting_cost' if m.group(1).lower().startswith('fees') else 'employee_cost'
        vals = [num(v) for v in cells(m.group(2))]
        if any(v is None for v in vals) or len(vals) < 2:
            continue
        # context above
        ctx_lines = []
        for j in range(i - 1, max(i - 12, -1), -1):
            ctx_lines.append(lines[j])
            if re.search(r'Million|Crore|Mn\b', lines[j]):
                break
        ctx = '\n'.join(reversed(ctx_lines))
        if re.search(r'Income Statement', ctx):
            continue
        cur_unit = 'USD_mn' if re.search(r'\$\s*M', ctx) else ('INR_cr' if re.search(r'Crore', ctx) else 'INR_mn')
        section = 'Expense by nature'
        for j in range(i - 1, max(i - 14, -1), -1):
            if re.search(r'^\s*(COR|Cost of [Rr]evenue)\b', lines[j]) or re.search(r'COR\s+(Q\d|FY)', lines[j]) or re.match(r'^\s*COR\s*$', lines[j].strip()):
                section = 'COR'; break
            if re.match(r'^(SGA|SG&A)', re.sub(r'\s', '', lines[j])):
                section = 'SG&A'; break
            if re.search(r'Expense by Nature', lines[j], re.I):
                section = 'Expense by nature'; break
        if section == 'Expense by nature' and not re.search(r'Expense by Nature', '\n'.join(lines[max(0, i - 25):i]), re.I):
            # unknown table
            continue
        labels = []
        for l in reversed(ctx_lines):
            labels += [x.replace(' ', '') for x in PERIOD_RE.findall(l)]
        # de-duplicate while keeping order of first appearance
        uniq = []
        for l in labels:
            if l not in uniq:
                uniq.append(l)
        n = len(vals) // 2 if len(vals) % 2 == 0 else None
        if n is None:
            warnings.append(f'{doc["name"]}: odd value count for {item} line')
            continue
        cur_vals = vals[:n]
        split = re.search(r'Ex Adj|Reported', ctx)
        dim = {'COR': 'Fees to external consultants (in cost of revenue)',
               'SG&A': 'Fees to external consultants (in SG&A)',
               'Expense by nature': 'Fees to external consultants (expense by nature)'}[section]
        if item == 'employee_cost':
            dim = {'COR': 'Employee cost (in cost of revenue)', 'SG&A': 'Employee cost (in SG&A)',
                   'Expense by nature': 'Employee cost (expense by nature)'}[section]
        loc = {'COR': 'COR - SG&A Details (COR table)', 'SG&A': 'COR - SG&A Details (SG&A table)',
               'Expense by nature': 'Expense by Nature table'}[section]
        if cur_unit == 'USD_mn':
            loc += ' - USD'
        dt = 'other'
        # ordered labels (drop duplicates from 2-line headers) -- only trust mapping when counts match exactly
        per_labels = uniq[:n] if len(uniq) >= n else None
        # 2-line header with split current/prior columns (Ex Adj / Reported) -> only take last value
        if split or per_labels is None or len(uniq) != n:
            anyfy = [l for l in uniq if l.startswith('FY')]
            anyq = [l for l in uniq if l.startswith('Q')]
            per = ('FY' + cur_label[-2:]) if (anyfy and not anyq) else cur_label
            add(per, item, dim, dt, cur_vals[-1], cur_unit, 'reported', None, doc, loc,
                'last (current-period, reported) column only; header has Ex Adj/Reported split or ambiguous labels')
            continue
        for lab, v in zip(per_labels, cur_vals):
            add(lab, item, dim, dt, v, cur_unit, 'reported', None, doc, loc)


# ---------------------------------------------------------------- main per-document loop
def process_deck(fn):
    y, q = fn.split('_')[0], fn.split('_')[1]
    qn = int(q[1])
    fy = int(y[:4]) + 1
    cur_label = f'Q{qn} FY{fy % 100:02d}'
    pdf = os.path.join(SRC, fn)
    text = pdftotext(pdf, os.path.join(TXT, fn[:-4] + '.txt'))
    lines = text.splitlines()
    kind = 'fact sheet' if 'factsheet' in fn else 'analysts presentation'
    url = find_url(y, q, lambda f, d: ('Fact' in f) if kind == 'fact sheet' else ('Analysts Presentation' in f))
    doc = dict(url=url, name=f'TCS Q{qn}FY{fy % 100:02d} {kind}', date=doc_date(text))
    totals = parse_tables(lines, doc, cur_label.replace(' ', ''))
    parse_restated(lines, doc)
    parse_clients(lines, doc, cur_label)
    parse_usd_chart(lines, doc, cur_label)
    parse_highlights(lines, doc, cur_label, totals, qn == 4)
    parse_cost_lines(lines, doc, cur_label.replace(' ', ''), qn == 4)


def hand_entered():
    """TCV totals disclosed only on earnings calls / press releases before fact sheets carried TCV (Q4FY23+)."""
    tmap = dict(l.rstrip('\n').split('\t') for l in open(os.path.join(SRC, '_transcript_urls.tsv')) if '\t' in l)
    H = [  # (fiscal label, value USD bn, local file stem, quote/locator, source kind)
        ('Q1FY19', 4.9, '2018-19_q1', 'CEO remarks: "The total value of contracts signed in Q1 is $4.9 billion"', 'transcript'),
        ('Q2FY19', 4.9, '2018-19_q2', 'CEO remarks: "total value of contracts signed in this quarter is $4.9 billion"', 'transcript'),
        ('Q3FY19', 5.9, '2018-19_q3', 'CEO remarks: "total value of contracts signed in Q3 was US$5.9 billion"', 'transcript'),
        ('Q4FY19', 6.2, '2018-19_q4', 'CEO remarks: "total TCV of contracts signed in Q4 was $6.2 billion"', 'transcript'),
        ('Q1FY20', 5.7, '2019-20_q1', 'CEO remarks: "total value of contracts signed in Q1 of FY 20 is $5.7 billion"', 'transcript'),
        ('Q2FY20', 6.4, '2019-20_q2', 'CEO remarks: "TCV in Q2 was $6.4 billion"', 'transcript'),
        ('Q3FY20', 6.0, '2019-20_q3', 'Q&A: "overall order book for the quarter ... was at about 6 billion" (approximate)', 'transcript'),
        ('Q4FY20', 8.9, '2019-20_q4', 'CEO remarks: "order book signed in the quarter was at $8.9 billion"', 'transcript'),
        ('Q1FY21', 6.9, '2020-21_q1', 'CEO remarks: "total contract value of deals signed in the quarter was $6.9 billion"', 'transcript'),
        ('Q2FY21', 8.6, '2020-21_q2', 'CEO remarks: "total contract value of deals signed in Q2 was $8.6 billion"', 'transcript'),
        ('Q3FY21', 6.8, '2020-21_q3', 'CEO remarks: "total contract value signed this quarter is $6.8 billion"', 'transcript'),
        ('Q4FY21', 9.2, '2020-21_q4', 'Press release: "Order Book: $9.2 Bn"', 'pr'),
        ('Q1FY22', 8.1, '2021-22_q1', 'Press release: "Order Book at $8.1 Bn"', 'pr'),
        ('Q2FY22', 7.6, '2021-22_q2', 'CEO remarks: "Our TCV in Q2 was $7.6 billion"', 'transcript'),
        ('Q3FY22', 7.6, '2021-22_q3', 'CEO remarks: "overall order book in Q3, our total TCV was $7.6 billion"', 'transcript'),
        ('Q4FY22', 11.3, '2021-22_q4', 'Press release: "Highest Ever Order Book TCV: $11.3 billion"', 'pr'),
        ('Q1FY23', 8.2, '2022-23_q1', 'Press release: "Order Book at $8.2 billion"', 'pr'),
        ('Q2FY23', 8.1, '2022-23_q2', 'Press release: "Order Book at $8.1 billion"', 'pr'),
        ('Q3FY23', 7.8, '2022-23_q3', 'Press release: "Order Book at $7.8 billion"', 'pr'),
    ]
    for lab, v, stem, quote, kind in H:
        y, q = stem.split('_')
        if kind == 'transcript':
            url = tmap.get(f'{stem}_transcript.pdf')
            txt = open(os.path.join(TXT, f'{stem}_transcript.txt'), errors='replace').read()
            name = f'TCS {lab} earnings call transcript'
        else:
            url = find_url(y, q, lambda f, d: 'Press Release - USD' in f)
            txt = open(os.path.join(TXT, f'{stem}_PR_USD.txt'), errors='replace').read()
            name = f'TCS {lab} press release (IFRS, USD)'
        doc = dict(url=url, name=name, date=doc_date(txt) or '')
        add(lab, 'tcv', 'total', 'total', v, 'USD_bn', 'reported', 'quarter', doc, quote.split(':')[0],
            'hand-entered; total contract value of deals signed in the quarter (order book); ' + quote)
    # press-release-only items (FY25+): net additions and AI revenue run-rate
    PR = [
        ('Q1FY25', '2024-25', 'q1', 'net_additions', 'total', 'total', 5452, 'count', 'na', 'quarter',
         'Press release highlights', 'hand-entered; "Net Headcount addition of 5,452"'),
        ('Q2FY25', '2024-25', 'q2', 'net_additions', 'total', 'total', 5726, 'count', 'na', 'quarter',
         'Press release highlights', 'hand-entered; "Net Headcount addition of 5,726" (headline also: H1FY25 net addition of more than 11,000)'),
        ('Q1FY26', '2025-26', 'q1', 'net_additions', 'total', 'total', 6071, 'count', 'na', 'ltm',
         'Press release highlights', 'hand-entered; "Net Headcount addition of 6,071 YoY" (year-on-year change, not quarterly)'),
        ('Q3FY26', '2025-26', 'q3', 'ai_disclosure', 'Annualized AI services revenue', 'other', 1.8, 'USD_bn', 'reported', 'point',
         'Press release highlights', 'hand-entered; "Annualized AI Services Revenue at $1.8 billion; up 17.3% QoQ in Constant Currency" (run-rate)'),
        ('Q3FY26', '2025-26', 'q3', 'ai_disclosure', 'Annualized AI services revenue growth QoQ', 'other', 17.3, 'pct', 'cc', 'quarter',
         'Press release highlights', 'hand-entered; QoQ CC growth of annualized AI services revenue'),
        ('Q4FY26', '2025-26', 'q4', 'ai_disclosure', 'Annualized AI revenue', 'other', 2.3, 'USD_bn', 'reported', 'point',
         'Press release highlights', 'hand-entered; "Annualized AI Revenue crosses US$ 2.3 billion in Q4FY26" (lower bound: "crosses"/"surpassed")'),
        ('Q1FY27', '2026-27', 'q1', 'ai_disclosure', 'Annualized AI revenue', 'other', 2.6, 'USD_bn', 'reported', 'point',
         'Press release highlights', 'hand-entered; "Annualized AI Revenue at US$ 2.6 billion in Q1FY27, up 13.6% QoQ" (run-rate)'),
        ('Q1FY27', '2026-27', 'q1', 'ai_disclosure', 'Annualized AI revenue growth QoQ', 'other', 13.6, 'pct', 'reported', 'quarter',
         'Press release highlights', 'hand-entered; QoQ growth of annualized AI revenue (currency basis not stated)'),
    ]
    for lab, y, q, metric, dim, dt, v, unit, basis, pt, loc, note in PR:
        url = find_url(y, q, lambda f, d: 'Press Release - USD' in f)
        txt = open(os.path.join(TXT, f'{y}_{q}_PR_USD.txt'), errors='replace').read()
        doc = dict(url=url, name=f'TCS {lab} press release (IFRS, USD)', date=doc_date(txt) or '')
        add(lab, metric, dim, dt, v, unit, basis, pt, doc, loc, note)
    # full-year order book in FY21 press release
    url = find_url('2020-21', 'q4', lambda f, d: 'Press Release - USD' in f)
    doc = dict(url=url, name='TCS Q4FY21 press release (IFRS, USD)',
               date=doc_date(open(os.path.join(TXT, '2020-21_q4_PR_USD.txt'), errors='replace').read()))
    add('FY21', 'tcv', 'total', 'total', 31.6, 'USD_bn', 'reported', 'annual', doc, 'Press release headline',
        'hand-entered; FY21 full-year order book TCV "Order Book: $31.6 Bn"')


def main():
    decks = sorted(f for f in os.listdir(SRC) if f.endswith('.pdf') and ('factsheet' in f or 'analysts_pres' in f))
    for fn in decks:
        process_deck(fn)
    hand_entered()
    # doc_date fallback: results-day date parsed from the same quarter's transcript URL (results are released
    # the same day as the call); press releases/decks/transcripts of a quarter share that date.
    tdates = {}
    for l in open(os.path.join(SRC, '_transcript_urls.tsv')):
        if '\t' not in l:
            continue
        nm, u = l.rstrip('\n').split('\t')
        mm = re.search(r'on ([A-Z][a-z]+)\.? (\d{1,2}),? (20\d\d)', urllib.parse.unquote(u))
        if mm:
            y, q = nm.split('_')[:2]
            lab = f'Q{q[1]}FY{(int(y[:4]) + 1) % 100:02d}'
            tdates[lab] = f'{mm.group(3)}-{MONTHS[mm.group(1)[:3].lower()]:02d}-{int(mm.group(2)):02d}'
    for r in rows:
        if not r['doc_date']:
            mm = re.search(r'(Q\dFY\d\d)', r['source_doc'])
            if mm and mm.group(1) in tdates:
                r['doc_date'] = tdates[mm.group(1)]
    for r in rows:
        if not r['doc_date'] and r['source_url']:
            d = urllib.parse.unquote(r['source_url'])
            m = re.search(r'on ([A-Z][a-z]+) (\d{1,2}), (20\d\d)', d)
            if m:
                r['doc_date'] = f'{m.group(3)}-{MONTHS[m.group(1)[:3].lower()]:02d}-{int(m.group(2)):02d}'
        if not r['source_url']:
            warnings.append(f'missing url: {r["source_doc"]}')
    # de-duplicate: same (period, metric, dimension, unit, basis, period_type, document) reported in two tables of
    # one document (e.g. Q1FY18 main vertical table and its recast-history table) -> keep first if values agree
    seen, out = {}, []
    for r in rows:
        k = tuple(r[f] for f in ['fiscal_q', 'metric', 'dimension', 'unit', 'basis', 'period_type', 'source_doc'])
        if k in seen:
            if seen[k]['value'] == r['value']:
                continue
            warnings.append(f'conflicting duplicate within doc: {k} {seen[k]["value"]} vs {r["value"]} ({r["source_loc"]})')
        seen.setdefault(k, r)
        out.append(r)
    out.sort(key=lambda r: (r['period_end'], r['period_type'], r['metric'], r['dim_type'], r['dimension'], r['doc_date'], r['unit']))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows(out)
    print(f'wrote {len(out)} rows to {OUT}')
    for wmsg in warnings:
        print('WARN', wmsg, file=sys.stderr)


if __name__ == '__main__':
    main()
