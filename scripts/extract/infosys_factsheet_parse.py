"""Parse Infosys quarterly fact sheets (PDFs from infosys.com; archived copies fetched via the Wayback Machine because
infosys.com returns 403 to scripts) into schema rows.
Run from project root:  python3 scripts/extract/infosys_factsheet_parse.py
Output: data/sources/infosys/parsed_factsheets.csv   (warnings -> stderr)
"""
import re, os, json, subprocess, datetime, csv, sys
sys.path.insert(0, os.path.dirname(__file__))
from infosys_common import *

FS_DIR = f"{BASE}/factsheets"
meta = json.load(open(f"{FS_DIR}/meta.json"))
FIL = filings()

SECTIONS = [
    (r"^Revenues? by (Client )?Geograph", "geo"),
    (r"^Revenues? by Service Offering", "service"),
    (r"^Revenues? by (Client )?Industry|^Revenues? by Business Segment", "vertical"),
    (r"^Revenues? by (Project|Contract) Type", "project"),
    (r"^Revenues? by Offering", "offering"),
    (r"^Client Data", "client"),
    (r"^Effort (and|&) Utili[sz]ation", "effort"),
    (r"^Effort (and|&) Revenues", None),
    (r"^Person Months Data", "pm"),
    (r"^Consolidated IT Services$", None),
    (r"^Employee Metrics\s*[–-]\s*Subsidiaries", None),
    (r"^Employee Metrics$", "emp"),
    (r"^Constant Currency Reporting", "cc"),
    (r"^Revenue Segmentation Growth", "seggrowth"),
    (r"^Revenue Growth(\s*-.*)?$", "rg"),
    (r"[Ss]tatement of Comprehensive Income for three months", "pl3"),
    (r"[Ss]tatement of Comprehensive Income for (six|nine|year|Year)", None),
    (r"^Infrastructure(\s*\(as on.*\))?$", None),
    (r"^(Rupee Dollar Rate|Cash Flow|Revenue per (FTE|Employee)|Subsidiaries Performance|Performance as Against Guidance|Notes:|Basis of computation|Geographical segment\s*[–-]\s*growth|Industry segment\s*[–-]\s*growth|Consolidated Balance Sheet|Refer Note)", None),
]

LINE_RE = re.compile(r"^(\s*)(.*?[A-Za-z%\)\+].*?)\s{2,}((?:" + NUM_TOKEN + r"\s*)+)$")
NUMONLY_RE = re.compile(r"^\s*((?:" + NUM_TOKEN + r"\s+)*" + NUM_TOKEN + r")\s*$")
TOK_RE = re.compile(NUM_TOKEN)
PART_RE = re.compile(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2})\s*,(?!\s*\d{4})")
YEAR_RE = re.compile(r"(?<![\d,])((?:19|20)\d\d)(?![\d,])")


def months_between(a, b):
    return (a.year - b.year) * 12 + a.month - b.month


def header_dates(buf):
    """buf: list of raw header lines. Returns list of quarter-end dates ordered by x position."""
    items, partials, years = [], [], []
    for li, line in enumerate(buf):
        full_spans = []
        for m in DATE_RE.finditer(line):
            mon = MONTHS[m.group(1).lower()[:3]]
            full_spans.append(m.span())
            if mon in QEND:
                items.append(((m.start() + m.end()) / 2, qend_from_date(mon, int(m.group(3)))))
        for m in PART_RE.finditer(line):
            partials.append((li, (m.start() + m.end()) / 2, MONTHS[m.group(1).lower()[:3]]))
        for m in YEAR_RE.finditer(line):
            if not any(a <= m.start() < b for a, b in full_spans):
                years.append((li, (m.start() + m.end()) / 2, int(m.group(1)), m))
    used = set()
    for li, x, mon in partials:
        c = [(abs(x - yx), k) for k, (yl, yx, yv, _) in enumerate(years) if yl != li and k not in used]
        if c:
            _, k = min(c); used.add(k)
            if mon in QEND:
                items.append((x, qend_from_date(mon, years[k][2])))
    items.sort()
    return [d for _, d in items]


def is_year_line(s, allow_single=False):
    toks = s.split()
    return len(toks) >= (1 if allow_single else 2) and all(re.fullmatch(r"(19|20)\d\d", t) for t in toks)


def clean(label):
    return re.sub(r"\s*\(\d\)$", "", re.sub(r"\s+", " ", label.replace("*", "").replace("^", "").replace("#", "")).strip())


def parse_doc(fq):
    m = meta[fq]
    txt = subprocess.run(["pdftotext", "-layout", m["file"], "-"], capture_output=True, text=True).stdout
    lines = txt.split("\n")
    doc_pe = fq_to_pe(fq)
    doc_date = FIL.get(fq, {}).get("announce_date", "")
    src = dict(source_url=m["url"], source_doc=f"Infosys {fq} fact sheet (archived copy web.archive.org/web/{m['ts']})",
               doc_date=doc_date)
    rows = []
    st = dict(page=1)
    contract_note = ("Revenues by contract type, including products" if re.search(r"Including products", txt)
                     else "Revenues by project type, excluding products")

    def add(pe, metric, dim, dim_type, value, unit, basis="na", ptype="quarter", loc="", notes=""):
        if value is None:
            return
        fqq, pes, calq = period_info(pe)
        rows.append(dict(firm="infosys", fiscal_q=fqq, period_end=pes, cal_q=calq, metric=metric, dimension=dim,
                         dim_type=dim_type, value=value, unit=unit, basis=basis, period_type=ptype,
                         source_loc=f"p{st['page']} {loc}".strip(), notes=notes, **src))

    def reset(name, title):
        st["tbl"] = st.get("tbl", 0) + 1
        st.update(section=name, secname=title, qdates=[], ndates=0, gtype=None, subhdr="", top=None, parent="",
                  hbuf=[], cc_cols=[], cc_block="", pl_ccy=None, pmtot=0, offer_pct=False, rgfmt="", rg_fy=False,
                  last_label="")
    reset(None, "")
    pl_done = set()
    for i, raw in enumerate(lines):
        if "\f" in raw:
            st["page"] += raw.count("\f"); raw = raw.replace("\f", "")
        s = raw.strip()
        if not s:
            continue
        s_nounit = re.sub(r"\s*\((in %|In %|Nos\.|in \$ mn|In US \$ K)\)\s*$", "", s).strip()
        hit = None
        for pat, name in SECTIONS:
            if re.search(pat, s_nounit) and not LINE_RE.match(raw):
                hit = name; break
        if hit is not None or any(re.search(p, s_nounit) and not LINE_RE.match(raw) for p, n in SECTIONS if n is None):
            reset(hit, s_nounit)
            continue
        sec = st["section"]
        if sec is None:
            continue
        if sec == "pl3":
            if re.search(r"US ?\$ ?million", s): st["pl_ccy"] = "USD_mn"
            elif re.search(r"crore", s): st["pl_ccy"] = "INR_cr"
        if sec == "cc":
            qs = re.findall(r"Q([1-4])\s?(\d{2})\b", s)
            if len(qs) >= 2:
                st["cc_cols"] = [fq_to_pe(f"Q{a}FY{b}") for a, b in qs]
                low = s.lower()
                st["cc_block"] = "rep" if "reported" in low else ("ccqoq" if re.search(r"q\s*o\s*q", low) else ("ccyoy" if re.search(r"y\s*o\s*y", low) else "other"))
                continue
        # header lines (dates / partial dates / years / column captions)
        single_ok = bool(st["hbuf"]) and not st.get("hbuf_done") and any(PART_RE.search(x) for x in st["hbuf"])
        if (DATE_RE.search(raw) or PART_RE.search(raw) or is_year_line(s, single_ok) or not (LINE_RE.match(raw) or NUMONLY_RE.match(raw))) \
                and sec not in ("pl3",):
            if DATE_RE.search(raw) or PART_RE.search(raw) or is_year_line(s, single_ok) or re.search(r"Quarter ended|Growth|Reported|LTM|Year [Ee]nded|CC", s):
                if st["hbuf"] and st.get("hbuf_done"):
                    st["hbuf"] = []
                st["hbuf"].append(raw); st["hbuf_done"] = False
                # constant currency / segmentation-growth column captions like "Q2 15  Q1 15"
                qs = re.findall(r"Q([1-4])\s?(\d{2})\b", s)
                if sec in ("cc",) and len(qs) >= 2:
                    st["cc_cols"] = [fq_to_pe(f"Q{a}FY{b}") for a, b in qs]
                    low = s.lower()
                    st["cc_block"] = "rep" if "reported" in low else ("ccqoq" if re.search(r"q\s*o\s*q", low) else ("ccyoy" if re.search(r"y\s*o\s*y", low) else st["cc_block"]))
                if sec == "rg" and "CC QoQ" in s:
                    st["rgfmt"] = "3col"
                if sec == "seggrowth":
                    st["seg_cols"] = re.findall(r"(Q[1-4] ?\d\d(?: CC)?|FY ?\d\d(?: CC)?)", s) or st.get("seg_cols", [])
                    if re.search(r"Geographical", s): st["seg_dt"] = "geography"
                    if re.search(r"Industry|Business", s): st["seg_dt"] = "vertical"
                continue
            # other label-only line (sub header or wrapped label)
            if st.get("pend_label") and re.search(r"[,&]$|Financial$", st["pend_label"]):
                full = st["pend_label"] + " " + s
                for r in rows:
                    if r.get("_li") == st["pend_idx"]:
                        r["dimension"] = clean(full) if r["dimension"] == clean(st["pend_label"]) else r["dimension"]
                        if st["parent"] == clean(st["pend_label"]): st["parent"] = clean(full)
                st["pend_label"] = ""
                continue
            st["last_label"] = s; st["subhdr"] = s
            continue
        # data line
        if not (LINE_RE.match(raw) or NUMONLY_RE.match(raw)):
            continue
        if st["hbuf"] and not st.get("hbuf_done"):
            ds = header_dates(st["hbuf"])
            htxt = " ".join(x.strip() for x in st["hbuf"])
            if ds:
                qd = [ds[0]]
                for d in ds[1:]:
                    if d in qd or months_between(qd[0], d) not in (3, 12) or len(qd) == 3:
                        break
                    qd.append(d)
                if qd[0] != doc_pe:
                    print(f"WARN {fq} p{st['page']} {sec}: first header date {qd[0]} != {doc_pe}", file=sys.stderr)
                if len(qd) < 3:
                    print(f"NOTE {fq} p{st['page']} {sec}: {len(qd)} quarter cols {qd} from {htxt[:100]}", file=sys.stderr)
                st["qdates"] = qd; st["ndates"] = len(ds)
                st["gtype"] = ("yoy" if re.search(r"YoY Growth", htxt) else "qoq" if re.search(r"QoQ Growth", htxt) else None) \
                    if re.search(r"Reported", htxt) else None
                if sec == "offering" and st.get("offer_seen"):
                    st["offer_pct"] = True
                if sec == "offering":
                    st["offer_seen"] = True
            st["hbuf_done"] = True
        lm = LINE_RE.match(raw)
        if lm:
            indent = len(lm.group(1)); label = lm.group(2).strip(); toks = TOK_RE.findall(lm.group(3))
        else:
            nm = NUMONLY_RE.match(raw)
            indent = len(raw) - len(raw.lstrip()); toks = TOK_RE.findall(nm.group(1)); label = st["last_label"]
            if label:
                j = i + 1
                while j < len(lines) and not lines[j].strip(): j += 1
                nxt = lines[j].strip() if j < len(lines) else ""
                if nxt and not LINE_RE.match(lines[j]) and not NUMONLY_RE.match(lines[j]) and not DATE_RE.search(nxt) \
                        and not any(re.search(p_, nxt) for p_, _ in SECTIONS) and not re.search(r"www\.infosys|Page \d|^\*|^\(|Refer Note|Total", nxt) \
                        and len(nxt) < 45:
                    label = label + " " + nxt; lines[j] = ""
        vals = [to_num(t) for t in toks]
        n0 = len(rows)
        handle(st, label, indent, vals, doc_pe, add, pl_done, contract_note, fq)
        for r in rows[n0:]:
            r["_li"] = i; r["_tbl"] = st["tbl"]
        st["pend_label"] = label; st["pend_idx"] = i; st["last_label"] = ""
    # narrative segment growth sentences (older fact sheets)
    for line in lines:
        s = re.sub(r"\s+", " ", line.strip())
        mm = re.match(r"^([A-Z][A-Za-z &,\-]+?) (grew|declined) by ([\d.]+) ?%(.*)$", s)
        if not mm or "sequentially" not in s:
            continue
        seg, v1verb, v1, rest = mm.group(1).strip(), mm.group(2), float(mm.group(3)), mm.group(4)
        s1 = -1 if v1verb == "declined" else 1
        if re.search(r"both sequentially and in constant currency|and also in constant currency|^ sequentially and in constant currency", rest):
            v2, s2 = v1, s1
        elif re.search(r"was flat in constant currency", rest):
            v2, s2 = 0.0, 1
        elif re.fullmatch(r" sequentially\.?", rest):
            v2 = None
        else:
            m2 = re.search(r"(?:(grew|declined) by )?([\d.]+) ?% in constant currency", rest)
            if not m2:
                print(f"WARN {fq} unparsed growth sentence: {s}", file=sys.stderr); continue
            v2 = float(m2.group(2)); s2 = -1 if (m2.group(1) or v1verb) == "declined" else 1
        dt = "geography" if seg.lower() in ("north america", "europe", "india", "rest of the world") else "vertical"
        note = "from narrative sentence in fact sheet ('grew'/'declined'); declines recorded as negative"
        add(doc_pe, "segment_growth_qoq", seg, dt, s1 * v1, "pct", "reported", loc="segment growth text", notes=note)
        if v2 is not None:
            add(doc_pe, "segment_growth_qoq", seg, dt, s2 * v2, "pct", "cc", loc="segment growth text", notes=note)
    assign_hierarchy(rows, doc_pe)
    for r in rows:
        r.pop("_li", None); r.pop("_tbl", None)
    return rows


def assign_hierarchy(rows, doc_pe):
    """Mark sub-segments in revenue_share tables: a row is a parent if its current-quarter value equals the
    sum of the immediately following >=2 rows (tolerance 0.25pp). Children get a note; parents keep none."""
    from collections import OrderedDict
    tbls = OrderedDict()
    for r in rows:
        if r["metric"] in ("revenue_share", "segment_growth_yoy", "segment_growth_qoq") and r.get("_tbl") and r["source_loc"].find("segment growth text") < 0:
            tbls.setdefault(r["_tbl"], []).append(r)
    for t, rs in tbls.items():
        order = []
        for r in rs:
            if r["metric"] == "revenue_share" and r["period_end"] == doc_pe.isoformat() and (r["dimension"], r["_li"]) not in [(o[0], o[2]) for o in order]:
                order.append((r["dimension"], r["value"], r["_li"]))
        if not order or rs[0]["dim_type"] not in ("vertical", "geography", "service_line"):
            continue
        if re.search(r"Revenues? by Offering", rs[0]["source_loc"]):
            continue  # FY19 Digital/Core table: children already named 'Parent - Child
        parent_of = {}
        if abs(sum(o[1] for o in order) - 100) <= 0.6:
            order = []
        i = 0
        while i < len(order):
            found = False
            for k in range(2, 12):
                if i + k >= len(order) + 0 and i + k > len(order):
                    break
                ch = order[i + 1:i + 1 + k]
                if len(ch) < k:
                    break
                if abs(sum(c[1] for c in ch) - order[i][1]) <= 0.15 and not all(c[1] == 0 for c in ch):
                    for c in ch:
                        parent_of[c[2]] = order[i][0]
                    i = i + 1 + k; found = True
                    break
            if not found:
                i += 1
        for r in rs:
            if r["_li"] in parent_of:
                r["notes"] = (f"sub-segment of '{parent_of[r['_li']]}' (dimension prefixed with parent to disambiguate)" + ("; " + r["notes"] if r["notes"] and not r["notes"].startswith("sub-segment") else "")).strip()
                r["dimension"] = f"{parent_of[r['_li']]} > {r['dimension']}"
            elif r["notes"].startswith("sub-segment"):
                r["notes"] = ""
    return rows


def handle(st, label, indent, vals, doc_pe, add, pl_done, contract_note, fq):
    sec = st["section"]
    lab = clean(label)
    loc = clean(st["secname"])[:80]
    if sec == "cc":
        if not st["cc_cols"]:
            return
        met = None; b = st["cc_block"]
        if b == "rep":
            if re.match(r"Revenues? \(\$ ?mn\)", lab): met, basis, unit = "revenue", "reported", "USD_mn"
            elif "Sequential" in lab: met, basis, unit = "revenue_growth_qoq", "reported", "pct"
            elif "YoY" in lab: met, basis, unit = "revenue_growth_yoy", "reported", "pct"
        elif b == "ccqoq" and "Sequential" in lab: met, basis, unit = "revenue_growth_qoq", "cc", "pct"
        elif b == "ccyoy" and "YoY" in lab: met, basis, unit = "revenue_growth_yoy", "cc", "pct"
        if met:
            if len(vals) != len(st["cc_cols"]):
                print(f"WARN {fq} cc block col mismatch {lab} {vals} {st['cc_cols']}", file=sys.stderr)
            for pe, v in zip(st["cc_cols"], vals):
                add(pe, met, "total", "total", v, unit, basis, loc=f"{loc} ({b})")
        return
    if sec == "rg":
        if re.match(r"Revenues \(\$ mn\)\s*-\s*FY", lab):
            st["rg_fy"] = True
            return
        if lab.startswith("FY growth") and len(vals) == 2:
            add(doc_pe, "revenue_growth_yoy", "total", "total", vals[0], "pct", "reported", "annual", loc=loc, notes="fiscal-year growth")
            add(doc_pe, "revenue_growth_yoy", "total", "total", vals[1], "pct", "cc", "annual", loc=loc, notes="fiscal-year growth")
            return
        if st.get("rg_fy"):
            if lab.startswith("YoY growth") and len(vals) == 3:
                add(doc_pe, "revenue_growth_yoy", "total", "total", vals[0], "pct", "reported", "annual", loc=loc, notes="fiscal-year growth")
                add(doc_pe, "revenue_growth_yoy", "total", "total", vals[2], "pct", "cc", "annual", loc=loc, notes="fiscal-year growth")
            return
        if st["rgfmt"] == "3col":   # columns: Reported | CC QoQ | CC YoY
            if lab.startswith("QoQ growth") and len(vals) == 3:
                add(doc_pe, "revenue_growth_qoq", "total", "total", vals[0], "pct", "reported", loc=loc)
                add(doc_pe, "revenue_growth_qoq", "total", "total", vals[1], "pct", "cc", loc=loc)
            elif lab.startswith("YoY growth") and len(vals) == 3:
                add(doc_pe, "revenue_growth_yoy", "total", "total", vals[0], "pct", "reported", loc=loc)
                add(doc_pe, "revenue_growth_yoy", "total", "total", vals[2], "pct", "cc", loc=loc)
        else:
            if re.match(r"(QoQ|YoY) growth", lab) and len(vals) == 2:
                met = "revenue_growth_qoq" if lab.startswith("QoQ") else "revenue_growth_yoy"
                add(doc_pe, met, "total", "total", vals[0], "pct", "reported", loc=loc)
                add(doc_pe, met, "total", "total", vals[1], "pct", "cc", loc=loc)
        return
    if sec == "seggrowth":
        cols = st.get("seg_cols", [])
        if lab.lower().startswith("total") or not cols:
            return
        dt = st.get("seg_dt", "vertical")
        for c, v in zip(cols, vals):
            if c.startswith("Q"):
                basis = "cc" if c.endswith("CC") else "reported"
                add(doc_pe, "segment_growth_qoq", lab, dt, v, "pct", basis, loc=loc,
                    notes=f"column '{c}' in Revenue Segmentation Growth table (sequential growth)")
        return
    if sec == "pl3":
        ccy = st["pl_ccy"]
        if lab == "Revenues" and ccy and ccy not in pl_done and len(vals) >= 4:
            pl_done.add(ccy)
            add(doc_pe, "revenue", "total", "total", vals[0], ccy, "reported", loc=loc)
            add(doc_pe.replace(year=doc_pe.year - 1), "revenue", "total", "total", vals[1], ccy, "reported", loc=loc,
                notes="prior-year comparative column")
            pq = {3: datetime.date(doc_pe.year - 1, 12, 31), 6: datetime.date(doc_pe.year, 3, 31),
                  9: datetime.date(doc_pe.year, 6, 30), 12: datetime.date(doc_pe.year, 9, 30)}[doc_pe.month]
            add(pq, "revenue", "total", "total", vals[3], ccy, "reported", loc=loc, notes="prior-quarter comparative column")
        return
    qd = st["qdates"]
    if not qd:
        return
    nq = len(qd)
    if len(vals) < nq:
        print(f"WARN {fq} {sec} '{lab}' fewer values {vals} than cols {nq}", file=sys.stderr)
        return
    qv = vals[:nq]
    extra = []
    if st["gtype"] and len(vals) >= st["ndates"] + 2:
        extra = vals[st["ndates"]:st["ndates"] + 2]

    def put(metric, dim, dim_type, unit, basis="na", ptype="quarter", notes=""):
        for pe, v in zip(qd, qv):
            add(pe, metric, dim, dim_type, v, unit, basis, ptype, loc=loc, notes=notes)

    def put_growth(dim, dt, note=""):
        if extra:
            met = "segment_growth_yoy" if st["gtype"] == "yoy" else "segment_growth_qoq"
            add(qd[0], met, dim, dt, extra[0], "pct", "reported", loc=loc, notes=note)
            add(qd[0], met, dim, dt, extra[1], "pct", "cc", loc=loc, notes=note)

    if sec in ("geo", "vertical", "service"):
        if lab.lower().startswith("total"):
            return
        dt = {"geo": "geography", "vertical": "vertical", "service": "service_line"}[sec]
        if st["top"] is None or indent <= st["top"]:
            st["top"] = indent if st["top"] is None else min(st["top"], indent)
            st["parent"] = lab; note = ""
        else:
            note = f"sub-segment of '{st['parent']}'"
        if re.match(r"New (Services|Software)", lab):
            note = "memo item: revenues from new services/software launched since Apr 1, 2015; already included in rows above"
        put("revenue_share", lab, dt, "pct", notes=note)
        put_growth(lab, dt, note)
        return
    if sec == "project":
        if lab.lower().startswith("fixed price"):
            put("revenue_share_fixed_price", "total", "total", "pct", notes=contract_note)
            put_growth("Fixed Price", "other", contract_note)
        return
    if sec == "offering":
        if not st["offer_pct"]:
            if lab in ("Digital", "Core"):
                put("segment_revenue", lab, "service_line", "USD_mn", "reported")
                put_growth(lab, "service_line")
            elif re.match(r"Digital Revenues? as %", lab):
                put("revenue_share", "Digital", "service_line", "pct")
        else:  # FY19-style % table: Services/Products and Platforms/Total each split into Digital/Core
            if st["top"] is None or indent <= st["top"]:
                st["top"] = indent if st["top"] is None else min(st["top"], indent)
                st["parent"] = lab
                if lab.lower().startswith("total"):
                    return
                dim = lab
            else:
                dim = lab if st["parent"].lower().startswith("total") else f"{st['parent']} - {lab}"
            nt = "Digital/Core split of total revenue (alternative breakdown to Services / Products and Platforms)" if st["parent"].lower().startswith("total") else ""
            put("revenue_share", dim, "service_line", "pct", notes=nt)
            put_growth(dim, "service_line", nt)
            return
            put("revenue_share", dim, "service_line", "pct")
            put_growth(dim, "service_line")
        return
    if sec == "client":
        if lab == "Active":
            put("active_clients", "total", "total", "count")
        elif lab.startswith("Added during the period"):
            put("clients_added", "total", "total", "count", notes="gross client additions in the quarter")
        else:
            mm = re.match(r"(\d+) Million dollar \+", lab, re.I)
            if mm:
                put("clients_bucket", f"USD{mm.group(1)}mn+", "client_bucket", "count", notes="number of clients by LTM revenue")
            elif re.match(r"Top (client|\d+ clients)", lab):
                put("top_client_share", lab, "client_bucket", "pct", notes="share of quarterly revenue")
        return
    scope = "Consolidated IT services" if "Consolidated IT Services" in st["secname"] else "table titled '%s' (scope not stated in title)" % clean(st["secname"])
    if sec == "effort":
        l2 = lab
        mm = re.match(r"(Effort|Revenues?|Utili[sz]ation)\s*-\s*(.*)", lab)
        sh = st["subhdr"].lower()
        if mm:
            sh = mm.group(1).lower(); l2 = mm.group(2).strip()
        if l2 in ("Onsite", "Offshore"):
            if sh.startswith("effort"):
                put(f"effort_share_{l2.lower()}", "total", "total", "pct", notes=scope + "; share of effort (person-months)")
            elif sh.startswith("revenue"):
                put(f"revenue_share_{l2.lower()}", "total", "total", "pct", notes=scope)
        elif l2.startswith("Including trainees"):
            put("utilization_incl_trainees", "total", "total", "pct", notes=scope)
        elif l2.startswith("Excluding trainees"):
            put("utilization_excl_trainees", "total", "total", "pct", notes=scope)
        return
    if sec == "pm":
        l2 = lab.replace("–", "").replace("-", " ").strip()
        if lab.startswith("Billed"):
            dim = "Billed - " + l2.replace("Billed", "").strip()
        elif lab.startswith(("–", "-")):
            dim = "Billed - " + l2
        elif lab.upper() == "TOTAL":
            st["pmtot"] += 1
            dim = "Billed - Total" if st["pmtot"] == 1 else "Total"
        else:
            dim = l2
        put("person_months", dim, "other", "count", notes="Person months; " + scope)
        return
    if sec == "emp":
        if lab == "Total employees":
            put("headcount", "total", "total", "count", ptype="point", notes="Consolidated total employees (Infosys group incl. subsidiaries)")
        elif lab in ("S/W professionals", "Billable", "Banking product group", "Trainees", "Sales & Support"):
            put("headcount_breakdown", lab, "other", "count", ptype="point",
                notes="Billable/Banking product group/Trainees are sub-components of S/W professionals" if lab in ("Billable", "Banking product group", "Trainees") else "")
        elif lab == "Gross addition":
            put("gross_additions", "total", "total", "count")
        elif lab.startswith("Of which lateral"):
            put("lateral_additions", "total", "total", "count")
        elif lab == "Attrition":
            put("attrition_count", "total", "total", "count", notes="number of employee exits in the quarter")
        elif lab == "Net addition":
            put("net_additions", "total", "total", "count")
        elif lab.startswith("Attrition %") or lab.startswith("Voluntary Attrition"):
            put("attrition", lab, "other", "pct", notes="definition as in dimension label (firm's own label)")
        return


if __name__ == "__main__":
    allrows = []
    for fq in sorted(meta, key=lambda k: fq_to_pe(k)):
        if not os.path.exists(meta[fq]["file"]) or os.path.getsize(meta[fq]["file"]) < 10000:
            print("MISSING", fq, file=sys.stderr); continue
        r = parse_doc(fq)
        print(fq, len(r), file=sys.stderr)
        allrows += r
    with open(f"{BASE}/parsed_factsheets.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader()
        for r in allrows:
            w.writerow({k: r.get(k, "") for k in COLS})
    print("rows", len(allrows), file=sys.stderr)
