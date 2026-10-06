"""Generic layout-text table parser for LTI / Mindtree / LTIMindtree fact sheets.

Reads pdftotext -layout outputs listed in a doc index and emits raw table cells:
(doc_id, section, subsec, label, column, raw_value, value, is_pct, line_no)

Column alignment uses character positions of the header tokens (quarter labels,
QoQ / YoY growth labels) in the layout text.
"""
import re, json, sys, os, csv

QTOK = re.compile(r"Q\s*([1-4])\s*[\'’]?\s*F?Y\s*[\'’]?\s*(?:20)?(\d{2})(?!\d)", re.I)
GROWTH_TOK = re.compile(r"(Q-o-Q|QoQ|Y-o-Y|YoY)", re.I)
NUM_CHUNK = re.compile(r"^\(?[-–]?\s*[₹$]?\s*[\d,]*\.?\d+\s*%?\)?\s*%?\*?$|^\(?[-–]?[\d,]*\.?\d+\)?\s*bps$|^[-–]$|^NA$", re.I)
TRAIL_NUM = re.compile(r"^(.*?[A-Za-z&\)\+%\.:][^\d]*?)\s+(\(?[-–]?[\d,]*\.\d+%?\)?|\(?[-–]?\d[\d,]*\.?\d*%\)?)$")


def parse_num(s):
    s0 = s.strip().replace('₹', '').replace('$', '').replace('*', '').strip()
    if s0 in ('-', '–', 'NA', ''):
        return None, False
    # negatives are printed as "(3.7)", "(3.7%)" or "(3.7)%"; the last form was previously read as positive (audit 2026-10)
    neg = s0.startswith('(') and (s0.endswith(')') or s0.endswith('%)') or s0.endswith(')%'))
    bps = s0.lower().endswith('bps')
    t = s0.strip('()').replace('bps', '').replace('%', '').replace(',', '').replace('–', '-').replace(' ', '').strip('()')
    try:
        v = float(t)
    except ValueError:
        return None, False
    if neg:
        v = -abs(v)
    return v, ('%' in s0 or bps)


def chunks_with_pos(line):
    out = []
    for m in re.finditer(r"\S+(?: \S+)*", line):
        out.append((m.start(), m.end(), m.group(0)))
    return out


def split_chunks(line):
    """Split on 2+ spaces, keep positions. Also split single-space runs of numbers."""
    res = []
    for m in re.finditer(r"\S(?:.*?\S)?(?=\s{2,}|\s*$)", line):
        s, e, txt = m.start(), m.end(), m.group(0)
        # break chunks that are sequences of numbers separated by single spaces
        parts = txt.split(' ')
        if len(parts) > 1 and all(NUM_CHUNK.match(p) for p in parts if p) and not txt.lower().endswith('bps'):
            pos = s
            for p in parts:
                res.append((pos, pos + len(p), p))
                pos += len(p) + 1
            continue
        # peel trailing numbers from a label chunk (label and value separated by 1 space)
        if not NUM_CHUNK.match(txt):
            mm = TRAIL_NUM.match(txt)
            if mm and re.search(r"[A-Za-z]", mm.group(1)):
                lab = mm.group(1)
                res.append((s, s + len(lab), lab))
                num = mm.group(2)
                res.append((e - len(num), e, num))
                continue
        res.append((s, e, txt))
    return res


def is_num(txt):
    return bool(NUM_CHUNK.match(txt.strip()))


def classify(line):
    ch = split_chunks(line)
    if not ch:
        return 'blank', ch
    q = list(QTOK.finditer(line))
    nums = [c for c in ch if is_num(c[2])]
    if len(q) >= 2 and len(nums) <= 1:
        return 'header', ch
    if not q and len(FYTOK.findall(line)) >= 2 and len(nums) <= 1:
        return 'fyheader', ch
    g = GROWTH_TOK.findall(line)
    if not q and len(g) >= 2 and not nums:
        return 'gheader', ch
    if nums and any(not is_num(c[2]) for c in ch[:1]):
        return 'data', ch
    if nums and all(is_num(c[2]) for c in ch):
        return 'data', ch
    return 'text', ch


FYTOK = re.compile(r"(?<![Q\dA-Za-z])(?:9M\s*)?FY\s*[\'’]?\s*(?:20)?(\d{2})(?!\d)", re.I)


def normalize(line):
    return (line.replace('\ufffd', 'ti').replace('ﬁ', 'fi').replace('ﬀ', 'ff').replace('ﬂ', 'fl')
            .replace('\u200b', '').replace('\xa0', ' '))



UNIT_PAT = re.compile(r"(Amount in (INR|USD)|\((₹|\$) ?million\)|In (INR|USD) Mn|INR ₹|USD \$)", re.I)


def unit_tag(txt):
    m = UNIT_PAT.search(txt)
    if not m:
        return ''
    t = m.group(0).upper()
    return ' [INR]' if ('INR' in t or '₹' in t) else ' [USD]'


def set_header(i, qcols, title, lines, kinds, chs, last_text, section):
    n = len(lines)
    cols = list(qcols)
    gcols = []
    for j in range(max(0, i - 3), min(n, i + 4)):
        for m in GROWTH_TOK.finditer(lines[j]):
            c = (m.start() + m.end()) / 2
            if c > cols[-1][1] + 3:
                g = 'qoq' if m.group(1).lower().startswith('q') else 'yoy'
                qual = ''
                for jj in range(max(0, j - 2), min(n, j + 3)):
                    seg = lines[jj][max(0, int(m.start()) - 3):int(m.end()) + 3]
                    if re.search(r"\bCC\b", seg):
                        qual = '_cc'
                    elif re.search(r"\bUSD\b", seg):
                        qual = qual or '_usd'
                gcols.append((g + qual, c))
    gcols.sort(key=lambda x: x[1])
    ded = []
    for g in gcols:
        if not ded or abs(ded[-1][1] - g[1]) > 4:
            ded.append(g)
    if not any(g[0].endswith('_cc') for g in ded):
        ded = [(g[0].split('_')[0], g[1]) for g in ded]
    cols = cols + ded
    prev = [t for (idx, t) in last_text if i - idx <= 4]
    tag = ''
    for t in prev + [title]:
        tag = unit_tag(t) or tag
    if title and not QTOK.search(title) and not re.match(r"^(\(|Metrics$|Particulars$)", title):
        sec = title
    else:
        below = None
        j = i + 1
        while j < n and kinds[j] == 'blank':
            j += 1
        k = j + 1
        while k < n and kinds[k] == 'blank':
            k += 1
        if j < n and kinds[j] == 'text' and k < n and kinds[k] == 'data' and not NUM_CHUNK.match(chs[k][0][2]) \
                and len(lines[j].strip()) < 60 and not re.search(r"growth|qoq|yoy|q-o-q|y-o-y", lines[j], re.I):
            below = ' '.join(c[2] for c in chs[j])
        cand = [t for t in prev if not re.match(r"^(Growth|QoQ|Q-o-Q|YoY|Amount in|USD Growth|\(|Particulars)", t.strip(), re.I)]
        if below and (not cand or re.match(r"^(Revenue by|Revenue Mix|Client|Total Contract|Mindtree Minds|Key)", below, re.I)):
            sec = below
        elif cand:
            sec = cand[-1].strip()
        elif title:
            sec = title
        else:
            sec = section
    return cols, sec + tag, ''


def parse_text(lines):
    lines = [normalize(l) for l in lines]
    recs = []
    cols = None  # list of (name, center)
    section = ''
    subsec = ''
    last_text = []  # recent text lines (idx, text)
    n = len(lines)
    i = 0
    kinds = [None] * n
    chs = [None] * n
    for k in range(n):
        kinds[k], chs[k] = classify(lines[k])
    consumed = set()
    for i in range(n):
        kind, ch = kinds[i], chs[i]
        line = lines[i]
        if kind == 'blank':
            continue
        if kind == 'fyheader':
            fys = list(FYTOK.finditer(line))
            # split header: 'Q1   Q4   Q1' on previous non-blank line + 'FY2017 FY2017 FY2018' here
            j = i - 1
            while j >= 0 and kinds[j] == 'blank':
                j -= 1
            qonly = list(re.finditer(r"\bQ([1-4])\b", lines[j])) if j >= 0 else []
            if len(qonly) == len(fys) and not re.search(r"\d{2,}", re.sub(r"\bQ[1-4]\b", "", lines[j])):
                qcols = []
                for qm, fm in zip(qonly, fys):
                    qcols.append((f"Q{qm.group(1)}FY{fm.group(1)}", (fm.start() + fm.end()) / 2))
                title = line[:fys[0].start()].strip()
                cols, section, subsec = set_header(i, qcols, title, lines, kinds, chs, last_text, section)
                last_text = []
                continue
            cols = [('FY' + m.group(1), (m.start() + m.end()) / 2) for m in fys]
            subsec = ''
            continue
        if kind == 'gheader':
            # growth-only header (e.g. LTI 'Constant Currency Reporting' table); ignore if a
            # quarter header follows within 3 non-blank lines
            nxt = [k for k in range(i + 1, min(n, i + 6)) if kinds[k] != 'blank'][:3]
            prv = [k for k in range(max(0, i - 6), i) if kinds[k] != 'blank'][-3:]
            if any(kinds[k] in ('header', 'fyheader') for k in nxt + prv):
                continue
            cols = []
            for m in GROWTH_TOK.finditer(line):
                g = 'qoq' if m.group(1).lower().startswith('q') else 'yoy'
                cols.append((g, (m.start() + m.end()) / 2))
            cand = [t for (idx, t) in last_text if i - idx <= 4]
            section = cand[-1].strip() if cand else section
            subsec = ''
            last_text = []
            continue
        if kind == 'header':
            qs = list(QTOK.finditer(line))
            qcols = [(f"Q{m.group(1)}FY{m.group(2)}", (m.start() + m.end()) / 2) for m in qs]
            title = line[:qs[0].start()].strip()
            # split header: a lone quarter label on the adjacent line (e.g. 'Q4FY18' above 'Q3FY19 Q4FY19')
            for dj in (-1, 1):
                j = i + dj
                while 0 <= j < n and kinds[j] == 'blank':
                    j += dj
                if 0 <= j < n and kinds[j] != 'header':
                    extra = list(QTOK.finditer(lines[j]))
                    if len(extra) == 1 and not re.search(r"\d[\d,]*\.\d|%", lines[j]):
                        m = extra[0]
                        c = (m.start() + m.end()) / 2
                        if all(abs(c - q[1]) > 4 for q in qcols):
                            qcols.append((f"Q{m.group(1)}FY{m.group(2)}", c))
                            if dj == -1:
                                title = lines[j][:m.start()].strip() or title
            qcols.sort(key=lambda x: x[1])
            cols, section, subsec = set_header(i, qcols, title, lines, kinds, chs, last_text, section)
            last_text = []
            continue
        if kind == 'text':
            if i in consumed:
                continue
            txt = ' '.join(c[2] for c in ch)
            last_text.append((i, txt))
            # decide if it's a label prefix (next nonblank line is data with empty label)
            j = i + 1
            while j < n and kinds[j] == 'blank':
                j += 1
            if j < n and kinds[j] == 'data' and is_num(chs[j][0][2]) and len(txt) < 60:
                continue  # prefix; handled by data row
            if len(txt) < 60 and cols:
                subsec = txt
            continue
        if kind == 'data' and cols:
            label_parts = [c for c in ch if not is_num(c[2])]
            vals = [c for c in ch if is_num(c[2])]
            # label = non-numeric chunks that appear before first value
            first_val_pos = vals[0][0] if vals else 10**6
            label = ' '.join(c[2] for c in label_parts if c[0] < first_val_pos).strip()
            if not label:
                # prefix from previous text line(s), suffix from next text line
                pre = ''
                j = i - 1
                while j >= 0 and kinds[j] == 'blank':
                    j -= 1
                if j >= 0 and kinds[j] == 'text' and len(lines[j].strip()) < 60:
                    pre = ' '.join(c[2] for c in chs[j])
                    if subsec == pre:
                        subsec = ''
                suf = ''
                j = i + 1
                while j < n and kinds[j] == 'blank':
                    j += 1
                if j < n and kinds[j] == 'text' and len(lines[j].strip()) < 45 and not QTOK.search(lines[j]):
                    nxt = ' '.join(c[2] for c in chs[j])
                    if not re.search(r"P a g e|Page \d|Investor Release|^\*|^Note", nxt):
                        suf = nxt
                        consumed.add(j)
                label = (pre + ' ' + suf).strip()
                if len(vals) == 1 and len(cols) > 1:
                    continue  # lone number under a text line (page numbers etc.)
            else:
                # three-line label with the values on the middle line, e.g.
                # 'Application' / 'Development   41.5% ...' / 'Maintenance'
                j = i - 1
                while j >= 0 and kinds[j] == 'blank':
                    j -= 1
                k = i + 1
                while k < n and kinds[k] == 'blank':
                    k += 1
                if (j >= 0 and kinds[j] == 'text' and j not in consumed and k < n and kinds[k] == 'text'
                        and len(lines[j].strip()) < 40 and len(lines[k].strip()) < 40
                        and not QTOK.search(lines[j]) and not QTOK.search(lines[k])
                        and not re.match(r"^(Revenue|Utili|Effort|Billed|Client|Total|Key|Metrics|Fee|Onsite|Offshore|Headcount|Employee|Attrition|Growth|\*|Note|\d)", lines[j].strip(), re.I)
                        and not re.search(r"P a g e|Page \d|Investor Release|^\*|^Note|\d", lines[k])
                        and (re.search(r"[,&]$", lines[j].strip()) or re.search(r"[,&]$", label) or kinds[k + 1 if k + 1 < n else k] in ('data', 'blank'))):
                    label = (' '.join(c[2] for c in chs[j]) + ' ' + label + ' ' + ' '.join(c[2] for c in chs[k])).strip()
                    consumed.add(k)
                    if subsec == ' '.join(c[2] for c in chs[j]):
                        subsec = ''
            # assign values to columns by position
            assign = {}
            ok = True
            for (s, e, t) in vals:
                c = (s + e) / 2
                best = min(cols, key=lambda cc: abs(cc[1] - c))
                if best[0] in assign:
                    ok = False
                assign.setdefault(best[0], t)
            if not ok:
                # fallback: ordinal
                assign = {}
                for (name, _), (s, e, t) in zip(cols, vals):
                    assign[name] = t
                how = 'ordinal'
            else:
                how = 'pos'
            if not label or re.match(r'^\d+$', label):
                continue
            for colname, t in assign.items():
                v, ispct = parse_num(t)
                recs.append(dict(section=section, subsec=subsec, label=label, column=colname,
                                 raw=t, value=v, is_pct=ispct, line=i + 1, how=how,
                                 ncols=len([c for c in cols if c[0].startswith('Q')])))
    return recs


if __name__ == '__main__':
    path = sys.argv[1]
    lines = open(path, encoding='utf-8', errors='replace').read().split('\n')
    for r in parse_text(lines):
        print(r)
