"""Extract GFC-period (2007Q1-2012Q1) core metrics from HCL Technologies quarterly
investor releases (Wayback copies of hcltech.com / hcl.in PDFs).

Inputs : data/sources/gfc/hcltech/*.pdf  (+ manifest.tsv: timestamp, original URL, local file)
         text is produced with `pdftotext -layout` into data/sources/gfc/hcltech/txt/
Output : data/sources/gfc/hcltech/gfc_hcltech_rows.csv  (SCHEMA.md columns)

HCL fiscal year in this period ends 30 June (Q1 = Jul-Sep, Q2 = Oct-Dec, Q3 = Jan-Mar,
Q4 = Apr-Jun). Every release shows 3 quarterly columns (year-ago, prior quarter, current),
and from Q3FY09 a 5-6 quarter constant-currency table; all columns are recorded as
separate rows tagged with the doc_date of the release (vintages).
"""
import csv, os, re, subprocess, sys
from collections import OrderedDict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(ROOT, "data", "sources", "gfc", "hcltech")
TXT = os.path.join(SRC, "txt")
OUT = os.path.join(SRC, "gfc_hcltech_rows.csv")

COLS = ["firm", "fiscal_q", "period_end", "cal_q", "metric", "dimension", "dim_type", "value",
        "unit", "basis", "period_type", "source_url", "source_doc", "source_loc", "doc_date", "notes"]

# local file -> (release label, doc_date, doc_date_note)
DOCS = OrderedDict([
    ("HCLT_Q4FY07_hclin_Q4FY07.pdf", ("Q4FY07", "2007-08-13", "")),
    ("HCLT_Q3FY08.pdf", ("Q3FY08", "2008-04-15", "")),
    ("HCLT_Q4FY08.pdf", ("Q4FY08", "2008-08-01", "")),
    ("HCLT_Q1FY09.pdf", ("Q1FY09", "2008-10-15", "")),
    ("HCLT_Q3FY09.pdf", ("Q3FY09", "2009-04-22", "")),
    ("HCLT_Q1FY10.pdf", ("Q1FY10", "2009-10-28", "")),
    ("HCLT_Q2FY10.pdf", ("Q2FY10", "2010-01-25", "")),
    ("HCLT_Q3FY10.pdf", ("Q3FY10", "2010-04-21", "")),
    ("HCLT_Q4FY10.pdf", ("Q4FY10", "2010-07-29", "")),
    ("HCLT_Q1FY11.pdf", ("Q1FY11", "2010-10-19", "doc_date approx = PDF creation date")),
    ("HCLT_Q2FY11.pdf", ("Q2FY11", "2011-01-18", "doc_date approx = PDF creation date")),
    ("HCLT_Q3FY11.pdf", ("Q3FY11", "2011-04-19", "doc_date approx = PDF creation date")),
    ("HCLT_Q4FY11.pdf", ("Q4FY11", "2011-07-26", "doc_date approx = PDF creation date")),
    ("HCLT_Q1FY12.pdf", ("Q1FY12", "2011-10-17", "doc_date approx = PDF creation date")),
    ("HCLT_Q2FY12.pdf", ("Q2FY12", "2012-01-17", "doc_date approx = PDF creation date")),
    ("HCLT_Q3FY12.pdf", ("Q3FY12", "2012-04-18", "doc_date approx = PDF creation date")),
    ("HCLT_Q4FY12.pdf", ("Q4FY12", "2012-07-24", "doc_date approx = PDF creation date")),
])

MON = {m: i for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}
QEND = {"JFM": "03-31", "AMJ": "06-30", "JAS": "09-30", "OND": "12-31"}
DATE_RE = re.compile(r"(\d{1,2})-([A-Z][a-z]{2})-(\d{2})")
NUM_RE = re.compile(r"\(?-?\d[\d,]*(?:\.\d+)?\)?%?")
CAL_START, CAL_END = "2007Q1", "2012Q1"


def fq_from_end(pe):
    y, m = int(pe[:4]), int(pe[5:7])
    fy = y if m <= 6 else y + 1
    q = {9: 1, 12: 2, 3: 3, 6: 4}[m]
    return f"Q{q}FY{fy % 100:02d}"


def calq(pe):
    return f"{pe[:4]}Q{(int(pe[5:7]) - 1) // 3 + 1}"


def dates_in(line):
    """quarter-end dates in a header line; truncated at the first non-increasing date so that
    the 'Year Ended' columns of Q4 releases are not mistaken for quarters."""
    out = []
    for d, mo, y in DATE_RE.findall(line):
        if mo in MON:
            x = f"20{y}-{MON[mo]:02d}-{int(d):02d}"
            if out and x <= out[-1]:
                break
            out.append(x)
    return out


def num(tok):
    t = tok.strip()
    neg = t.startswith("(") and t.rstrip("%").endswith(")")
    t = t.strip("()%").replace(",", "")
    try:
        v = float(t)
    except ValueError:
        return None
    return -v if neg else v


def nums_after(text):
    text = re.sub(r"\[[^\]]*\]", " ", text)
    return [(m.group(0), num(m.group(0))) for m in NUM_RE.finditer(text)]


def load(fn):
    t = os.path.join(TXT, fn.replace(".pdf", ".txt"))
    if not os.path.exists(t):
        os.makedirs(TXT, exist_ok=True)
        subprocess.run(["pdftotext", "-layout", os.path.join(SRC, fn), t], check=True,
                       stderr=subprocess.DEVNULL)
    return open(t, encoding="utf-8", errors="replace").read().split("\n")


def page_of(lines, i):
    # pages are separated by form feeds in pdftotext output
    return sum(l.count("\f") for l in lines[: i + 1]) + 1


class Doc:
    def __init__(self, fn, url, label, doc_date, dnote):
        self.fn, self.url, self.label, self.doc_date, self.dnote = fn, url, label, doc_date, dnote
        self.lines = load(fn)
        self.rows = OrderedDict()
        self.conflicts = []

    def add(self, pe, metric, dim, dim_type, value, unit, basis, ptype, loc, notes=""):
        if value is None:
            return
        cq = calq(pe)
        if not (CAL_START <= cq <= CAL_END):
            return
        key = (pe, metric, dim, basis)
        if key in self.rows:
            if abs(self.rows[key]["value"] - value) > 1e-9:
                self.conflicts.append((key, self.rows[key]["value"], value, loc))
                self.rows[key]["notes"] += f"; same document shows {value:g} at {loc}"
            return
        n = "; ".join(x for x in [notes, self.dnote] if x)
        self.rows[key] = dict(firm="hcltech", fiscal_q=fq_from_end(pe), period_end=pe, cal_q=cq,
                              metric=metric, dimension=dim, dim_type=dim_type, value=value,
                              unit=unit, basis=basis, period_type=ptype, source_url=self.url,
                              source_doc=f"HCL Technologies {self.label} investor release",
                              source_loc=loc, doc_date=self.doc_date, notes=n)

    # --- helpers -------------------------------------------------------------
    def find(self, pat, start=0, end=None, flags=0):
        rx = re.compile(pat, flags)
        end = len(self.lines) if end is None else end
        for i in range(start, end):
            if rx.search(self.lines[i]):
                return i
        return None

    def section(self, pat, need_dates=True, start=0):
        """first match of pat whose following ~8 lines contain a date header (skips TOC)."""
        i = start
        while True:
            i = self.find(pat, i)
            if i is None:
                return None
            if not need_dates or any(len(dates_in(l)) >= 2 for l in self.lines[i:i + 8]):
                return i
            i += 1

    def header_dates(self, i, lo):
        for j in range(i, lo - 1, -1):
            d = dates_in(self.lines[j])
            if len(d) >= 2:
                return d, j
        return None, None

    def row(self, label_pat, lo, hi, cont=True):
        """return (line_idx, dates, values) for first line in [lo,hi) starting with label_pat"""
        rx = re.compile(r"^\s*" + label_pat)
        for i in range(lo, min(hi, len(self.lines))):
            m = rx.search(self.lines[i])
            if not m:
                continue
            dates, _ = self.header_dates(i, lo if lo > 0 else 0)
            if dates is None:
                dates, _ = self.header_dates(i, max(0, lo - 60))
            if dates is None:
                continue
            vals = nums_after(self.lines[i][m.end():])
            if len(vals) < len(dates) and cont and i + 1 < len(self.lines):
                nxt = self.lines[i + 1]
                # continuation line: label text followed by the numbers
                vals = vals + nums_after(re.sub(r"^\s*\([^)]*\)", " ", nxt))
            return i, dates, vals
        return None, None, None


def extract(d):
    L = d.lines
    conv = d.find(r"Financials in INR as per convenience translation", 40) or len(L)
    # guard: first real occurrence after TOC
    c2 = d.section(r"Financials in INR as per convenience translation", need_dates=False, start=45)
    if c2:
        conv = c2
    # ---------------- Consolidated income statement (US$) -------------------
    is0 = d.section(r"Consolidated Income Statement")
    bs = d.find(r"Consolidated Balance Sheet", is0 or 0)
    if is0 is not None and is0 < conv:
        i, dates, vals = d.row(r"Revenues\b", is0, bs or is0 + 30)
        if i is not None:
            n = len(dates)
            loc = f"p.{page_of(L, i)} Consolidated Income Statement (US$ mn, US GAAP)"
            for k in range(n):
                d.add(dates[k], "revenue", "total", "total", vals[k][1], "USD_mn", "reported", "quarter", loc)
            pct = [v for t, v in vals[n:] if t.endswith("%")]
            if len(pct) >= 2:
                d.add(dates[n - 1], "revenue_growth_yoy", "total", "total", pct[0], "pct", "reported", "quarter", loc)
                d.add(dates[n - 1], "revenue_growth_qoq", "total", "total", pct[1], "pct", "reported", "quarter", loc)
    # ---------------- Constant currency table ------------------------------
    r0 = d.find(r"^\s*Reported\s+(OND|JFM|AMJ|JAS)")
    if r0 is not None:
        loc = f"p.{page_of(L, r0)} Constant Currency Reporting table"
        def qs(line):
            return [f"20{y}-{QEND[q]}" for q, y in re.findall(r"(OND|JFM|AMJ|JAS)\s*['’]?\s*(\d{2})", line)]
        qrep = qs(L[r0])
        block = "rep"
        for j in range(r0 + 1, r0 + 14):
            s = L[j].strip()
            if s.startswith("Constant Currency (QoQ)"):
                block = "ccq"; continue
            if s.startswith("Constant Currency (YoY)"):
                block = "ccy"; continue
            if s.startswith("Average Rates"):
                break
            m = re.match(r"(Revenue \(\$ ?mn\)|Growth QoQ|Growth YoY)\s+(.*)$", s, re.I)
            if not m:
                continue
            vals = [v for _, v in nums_after(m.group(2))]
            if len(vals) != len(qrep):
                print("CC table length mismatch", d.fn, s, file=sys.stderr); continue
            lab = m.group(1).lower()
            for pe, v in zip(qrep, vals):
                if block == "rep" and lab.startswith("revenue"):
                    d.add(pe, "revenue", "total", "total", v, "USD_mn", "reported", "quarter", loc)
                elif block == "rep" and lab == "growth qoq":
                    d.add(pe, "revenue_growth_qoq", "total", "total", v, "pct", "reported", "quarter", loc)
                elif block == "rep" and lab == "growth yoy":
                    d.add(pe, "revenue_growth_yoy", "total", "total", v, "pct", "reported", "quarter", loc)
                elif block == "ccq" and lab == "growth qoq":
                    d.add(pe, "revenue_growth_qoq", "total", "total", v, "pct", "cc", "quarter", loc)
                elif block == "ccy" and lab in ("growth yoy", "growth qoq"):
                    d.add(pe, "revenue_growth_yoy", "total", "total", v, "pct", "cc", "quarter", loc,
                          "" if lab == "growth yoy" else "row mislabelled 'Growth QoQ' in the Constant Currency (YoY) block of the release; it is the YoY cc growth")
    # highlights text: "Revenue on constant currency basis, up 19.2% YoY and 2.4% sequentially"
    cur_pe = None
    if is0 is not None:
        dd, _ = d.header_dates(min(is0 + 12, len(L) - 1), is0)
        cur_pe = dd[-1] if dd else None
    for j in range(0, 120):
        m = re.search(r"Revenue on constant currency basis, up ([\d.]+)% YoY and (?:up )?([\d.]+)% sequentially", L[j])
        if m and cur_pe:
            loc = f"p.{page_of(L, j)} Results Highlights (text)"
            d.add(cur_pe, "revenue_growth_yoy", "total", "total", float(m.group(1)), "pct", "cc", "quarter", loc)
            d.add(cur_pe, "revenue_growth_qoq", "total", "total", float(m.group(2)), "pct", "cc", "quarter", loc)
            break
    # ---------------- Revenue mix -------------------------------------------
    ra = d.section(r"^\s*Revenue Analysis")
    if ra is None:
        ra = d.section(r"^\s*Geographic Mix")
    if ra is not None:
        for hdr, dtype in [(r"Geographic Mix", "geography"), (r"Service Offering Mix", "service_line"),
                           (r"Revenue by Vertical", "vertical")]:
            h = d.find(r"^\s*" + hdr, ra, ra + 80)
            if h is None:
                continue
            dates = dates_in(L[h]); n = len(dates)
            loc = f"p.{page_of(L, h)} Revenue Analysis - {hdr}"
            for j in range(h + 1, h + 20):
                s = L[j].strip()
                if not s:
                    continue
                if re.match(r"(Geographic Mix|Service Offering Mix|Revenue by|Rupee|IT Services|“LTM”|\"LTM\")", s) or dates_in(s):
                    break
                parts = re.split(r"\s{2,}", s)
                label = parts[0]
                vals = [(t, num(t)) for t in parts[1:] if re.fullmatch(r"-?\d+(\.\d+)?%", t)]
                if len(vals) < n:
                    continue
                for k in range(n):
                    d.add(dates[k], "revenue_share", label, dtype, vals[k][1], "pct", "reported", "quarter", loc,
                          "share of consolidated revenue")
    # ---------------- Utilization (Core Software / Software Services) -------
    om = d.section(r"^\s*Operational Metrics")
    if om is None:
        om = d.section(r"^\s*(Core )?Software Services \(Quarter Ended\)")
    if om is not None:
        u = d.find(r"^\s*Utili[sz]ation", om, om + 30)
        seg = "Core Software Services" if re.search(r"Core Software", " ".join(L[om:om + 3])) else "Software Services"
        if u is not None:
            loc = f"p.{page_of(L, u)} Operational Metrics - {seg}"
            for pat, metric, dim, note in [
                (r"Offshore\s*-\s*Including trainees", "utilization_incl_trainees", f"{seg} - Offshore", "offshore utilization incl. trainees"),
                (r"Offshore\s*-\s*Excluding trainees", "utilization_excl_trainees", f"{seg} - Offshore", "offshore utilization excl. trainees"),
                (r"Onsite\b", "utilization_onsite", seg, "onsite utilization"),
                (r"Blended Utili[sz]ation \(Excl\. Trainees\)", "utilization_excl_trainees", f"{seg} - Blended", "blended (offshore+onsite) utilization excl. trainees"),
            ]:
                i, dates, vals = d.row(pat, u, u + 7)
                if i is None:
                    continue
                for k in range(len(dates)):
                    d.add(dates[k], metric, dim, "service_line", vals[k][1], "pct", "na", "quarter", loc,
                          note + f"; HCL {seg} only (excludes Infrastructure Services and BPO)")
    # ---------------- Employee metrics -------------------------------------
    em = d.section(r"^\s*Manpower Details")
    if em is not None:
        fac = d.find(r"^\s*Facilit(y|ies)", em) or em + 120
        loc = f"p.{page_of(L, em)} Employee Metrics"
        def put(pat, metric, dim, dtype, unit, ptype, note, lo=em, hi=fac):
            i, dates, vals = d.row(pat, lo, hi)
            if i is None:
                return None
            if len(vals) < len(dates):
                print("short row", d.fn, pat, vals, file=sys.stderr)
            nt = note
            m = re.search(r"Attrition\s*\((FY'?\d\d)\)", L[i])
            if m:
                nt += f"; row labelled 'Attrition ({m.group(1)})' in this release (trailing-12-month / fiscal-year basis)"
            if metric == "attrition" and dim.startswith("BPO") and "Offshore" not in L[i]:
                nt += "; row labelled 'Attrition - Quarterly' (BPO block) in this release, same series later labelled 'Offshore Attrition - Quarterly'"
            for k in range(min(len(dates), len(vals))):
                d.add(dates[k], metric, dim, dtype, vals[k][1], unit, "na", ptype,
                      f"p.{page_of(L, i)} Employee Metrics", nt)
            return i
        put(r"Total Employee Count", "headcount", "total", "total", "count", "point",
            "total employees incl. IT services (software + infrastructure), BPO and support staff")
        put(r"IT Services \((Core )?Software", "headcount", "IT Services", "service_line", "count", "point",
            "IT Services = Core Software/Software Services + Infrastructure Services, incl. support staff")
        put(r"Attrition \((?:LTM|FY'?\d\d)\s*\)\s*\*?\s*-\s*IT Services", "attrition", "IT Services", "service_line", "pct", "ltm",
            "LTM attrition, IT Services (software + infrastructure); excludes involuntary attrition")
        put(r"BPO Services\s*-\s*Total", "headcount", "BPO Services", "service_line", "count", "point",
            "BPO Services headcount incl. support")
        put(r"(Offshore )?Attrition\s*[–-]\s*Quarterly\**\s*\d?\s*$|(Offshore )?Attrition\s*[–-]\s*Quarterly\**\s{2,}",
            "attrition", "BPO Services - Offshore", "service_line", "pct", "quarter",
            "BPO offshore attrition, quarterly (not annualised); excludes UK BPO where footnoted")
        csi = d.find(r"^\s*(Core Software|Software Services)\s*[–-]\s*Total", em, fac)
        csname = "Core Software" if (csi is not None and "Core Software" in L[csi]) else "Software Services"
        cs = put(r"(Core Software|Software Services)\s*[–-]\s*Total", "headcount",
                 csname, "service_line", "count", "point",
                 "Core Software (renamed 'Software Services' from Q1FY10 release) headcount incl. support")
        inf = d.find(r"^\s*Infrastructure Services\s*-\s*Total", em, fac)
        if cs is not None:
            put(r"Attrition\s*\((?:LTM|FY'?\d\d)\s*\)\s*\*?(?!\s*-)", "attrition", csname, "service_line", "pct", "ltm",
                "LTM attrition, Core Software/Software Services; excludes involuntary attrition",
                lo=cs, hi=inf if (inf and inf > cs) else cs + 16)
        if inf is not None:
            put(r"Infrastructure Services\s*-\s*Total", "headcount", "Infrastructure Services", "service_line",
                "count", "point", "Infrastructure Services headcount incl. support", lo=inf, hi=fac)
            put(r"Attrition\s*\((?:LTM|FY'?\d\d)\s*\)\s*\*?(?!\s*-)", "attrition", "Infrastructure Services", "service_line", "pct", "ltm",
                "LTM attrition, Infrastructure Services; excludes involuntary attrition", lo=inf, hi=inf + 16)
    # ---------------- subcontracting (search only) --------------------------
    for j, l in enumerate(L):
        if re.search(r"sub-?contract", l, re.I):
            print("SUBCONTRACT mention", d.fn, j, l.strip()[:120], file=sys.stderr)


def axon(d):
    """flag the Axon Group plc acquisition (consolidated from 16 Dec 2008) on affected rows"""
    for r in d.rows.values():
        pe, m = r["period_end"], r["metric"]
        add = ""
        if m in ("revenue", "revenue_share") and pe == "2008-12-31":
            add = "BREAK: includes HCL Axon (Axon Group plc, consolidated from 16-Dec-2008) for ~2 weeks"
        elif m in ("revenue", "revenue_share") and pe >= "2009-03-31":
            add = "BREAK: includes HCL Axon (acquired Dec-2008) for the full quarter"
        elif m in ("revenue_growth_qoq",) and r["basis"] in ("reported", "cc") and pe in ("2008-12-31", "2009-03-31"):
            add = "BREAK: growth inflated by Axon acquisition (consolidated from 16-Dec-2008); inorganic"
        elif m == "revenue_growth_yoy" and "2008-12-31" <= pe <= "2009-12-31":
            add = "BREAK: YoY growth includes inorganic contribution of Axon (consolidated from 16-Dec-2008)"
        elif m == "headcount" and pe >= "2008-12-31" and r["dimension"] in ("total", "IT Services", "Core Software", "Software Services"):
            add = "BREAK: includes HCL Axon employees from OND'08 (Dec-2008) onwards"
        elif m.startswith("utilization") and pe >= "2009-03-31":
            add = "includes HCL Axon from JFM'09 quarter (per release footnote)"
        if add:
            r["notes"] = add + ("; " + r["notes"] if r["notes"] else "")


def main():
    man = {}
    for line in open(os.path.join(SRC, "manifest.tsv")):
        ts, orig, fn = line.rstrip("\n").split("\t")
        man[fn] = (f"https://web.archive.org/web/{ts}/{orig}", orig)
    allrows = []
    for fn, (label, dd, dn) in DOCS.items():
        url, orig = man[fn]
        d = Doc(fn, url, label, dd, (dn + "; " if dn else "") + f"original URL: {orig}")
        extract(d)
        axon(d)
        for c in d.conflicts:
            print("CONFLICT", fn, c, file=sys.stderr)
        print(fn, len(d.rows), file=sys.stderr)
        allrows.extend(d.rows.values())
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for r in allrows:
            r = dict(r)
            v = r["value"]
            r["value"] = int(v) if r["unit"] == "count" and float(v).is_integer() else v
            w.writerow(r)
    print("wrote", len(allrows), "rows to", OUT, file=sys.stderr)


if __name__ == "__main__":
    main()
