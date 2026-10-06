"""Sub-probe A: pre-specified dictionary counts in earnings-call transcripts, 2019-2026.
Dictionary: dictionary.json (written before counting). Output: term_counts_doc.csv, family_rates_fq.csv, onsets.csv.
Transcripts: project data/sources/* (TCS, Infosys 6-K Ex.99.5, Wipro, Accenture Q4s + FY24-26) plus
company-IR PDFs fetched to scratchpad (Accenture FY20-23 quarters, TechM FY19-27, HCLTech 2018-27).
"""
import json, re, os, glob, subprocess, html, datetime as dt
import pandas as pd, numpy as np

ROOT = "/Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/0. Exploratory Analysis"
SRC = f"{ROOT}/data/sources"
OUT = f"{ROOT}/data/explore/text_firms/A_text"
SCR = "/private/tmp/claude-501/-Users-ndeshpande-Documents-2-misc-1-AI-SPAR---Andrei-0--Exploratory-Analysis/9cc3a03a-6131-4e75-9f79-142cb203a8ae/scratchpad"

DIC = json.load(open(f"{OUT}/dictionary.json"))
FAMS = ["pricing", "productivity", "demand", "gcc"]


def term_regex(t):
    """whole-word, case-insensitive; tokens joined by space/hyphen; '(s)' = optional plural."""
    if t == "GCC":
        return re.compile(r"\bGCCs?\b")  # case-sensitive
    special = {
        "discretionary spend": r"discretionary[\s\-]+spend(?:ing|s)?",
        "global capability center(s)": r"global[\s\-]+capability[\s\-]+cent(?:er|re)s?",
        "productivity pass": r"productivity[\s\-]+pass",  # pass-through / pass on / passed
        "give-back": r"give[\s\-]*backs?",
    }
    if t in special:
        body = special[t]
    else:
        toks = re.split(r"[\s\-]+", t)
        body = r"[\s\-]+".join(re.escape(x.replace("(s)", "")) + ("s?" if x.endswith("(s)") else "") for x in toks)
    tail = "" if t == "productivity pass" else r"\b"
    return re.compile(r"\b" + body + tail, re.I)


TERMS = {f: [(t, term_regex(t)) for t in DIC[f]] for f in FAMS}

# ---------------- manifest ----------------
docs = []  # firm, path, url, kind
# TCS
tcs_urls = dict(l.rstrip("\n").split("\t") for l in open(f"{SRC}/tcs/_transcript_urls.tsv") if "\t" in l)
for p in sorted(glob.glob(f"{SRC}/tcs/*_transcript.pdf")):
    b = os.path.basename(p)
    if int(b[:4]) >= 2018:
        docs.append(("TCS", p, tcs_urls.get(b, "https://www.tcs.com/investor-relations"), "pdf"))
# Infosys: 6-K exhibit descriptions 'EARNINGS CALL'
for l in open(f"{SRC}/infosys/exhibit_desc.txt"):
    p, d = l.rstrip("\n").split("|", 1)
    if "EARNINGS CALL" in d.upper() and "PRESS" not in d.upper():
        acc = p.split("/")[0]
        if int(acc.split("-")[1]) >= 18:
            url = f"https://www.sec.gov/Archives/edgar/data/1067491/{acc.replace('-', '')}/{p.split('/')[1]}"
            docs.append(("Infosys", f"{SRC}/infosys/edgar/{p}", url, "html"))
# Wipro
wl = {os.path.basename(x.strip()): "https://www.wipro.com" + x.strip() for x in open(f"{SRC}/wipro/wipro_links_fy15_fy27.txt")}
for p in sorted(glob.glob(f"{SRC}/wipro/*.pdf")):
    b = os.path.basename(p)
    if re.search(r"transcript|earnings-call|conference-call", b, re.I) and int(b[:4]) >= 2017:
        key = b.split("_", 2)[-1]
        docs.append(("Wipro", p, wl.get(key, "https://www.wipro.com/investors/"), "pdf"))
# Accenture local + scratch
au = {}
for l in open(f"{SRC}/accenture/transcripts/urls.txt"):
    q, u = l.split()
    au[q] = u
for p in sorted(glob.glob(f"{SRC}/accenture/transcripts/*.pdf")):
    q = os.path.basename(p)[:-4]
    if q != "Q4FY17":
        docs.append(("Accenture", p, au.get(q, ""), "pdf"))
for l in open(f"{SCR}/acn/got.txt"):
    q, u = l.split()
    docs.append(("Accenture", f"{SCR}/acn/{q}.pdf", u, "pdf"))
# TechM
tmu = {os.path.basename(u.strip()): u.strip() for u in open(f"{SCR}/tm_urls.txt")}
for b, u in tmu.items():
    docs.append(("TechM", f"{SCR}/tm/{b}", u, "pdf"))
# HCLTech
for u in open(f"{SCR}/hcl_urls.txt"):
    u = u.strip()
    b = os.path.basename(u)
    p = f"{SCR}/hcl/{b}"
    if os.path.exists(p):
        docs.append(("HCLTech", p, u, "pdf"))
for p in glob.glob(f"{SCR}/hcl/hcltech-earnings-oct14-2021_0.pdf"):
    docs.append(("HCLTech", p, "https://www.hcltech.com/sites/default/files/documents/investor-reports/hcltech-earnings-oct14-2021_0.pdf", "pdf"))


# ---------------- text + date ----------------
def get_text(p, kind):
    if kind == "pdf":
        return subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True).stdout
    raw = open(p, encoding="utf-8", errors="ignore").read()
    raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
    return html.unescape(re.sub(r"<[^>]+>", " ", raw))


MON = "january|february|march|april|may|june|july|august|september|october|november|december"
MI = {m: i + 1 for i, m in enumerate(MON.split("|"))}
PATS = [re.compile(rf"\b({MON})\s+(\d{{1,2}})(?:st|nd|rd|th)?,?\s+(20\d\d)", re.I),
        re.compile(rf"\b(\d{{1,2}})(?:st|nd|rd|th)?\s+({MON}),?\s+(20\d\d)", re.I)]


def call_date(text):
    head = text[:4000]
    best = None
    for i, pat in enumerate(PATS):
        for m in pat.finditer(head):
            g = m.groups()
            mo, d, y = (MI[g[0].lower()], int(g[1]), int(g[2])) if i == 0 else (MI[g[1].lower()], int(g[0]), int(g[2]))
            try:
                dd = dt.date(y, mo, d)
            except ValueError:
                continue
            if best is None or m.start() < best[0]:
                best = (m.start(), dd)
    return best[1] if best else None


# manual fallback dates (no parsable date on first page): from filename quarter / 6-K filing date
FALLBACK = {"tml-q2-fy-22-earnings-transcript.pdf": dt.date(2021, 10, 25),  # Q2 FY22 (Jul-Sep 2021)
            "tml-q4-fy-26-earnings-transcript.pdf": dt.date(2026, 4, 22),   # Q4 FY26 call 22 Apr 2026 (per IR)
            "0001067491-22-000046": dt.date(2022, 10, 13)}                  # Infosys Q2 FY23 6-K
rows = []
for firm, p, url, kind in docs:
    if not os.path.exists(p) or os.path.getsize(p) < 5000:
        continue
    t = get_text(p, kind)
    t = re.sub(r"\s+", " ", t)
    nw = len(re.findall(r"[A-Za-z][A-Za-z'\-]*", t))
    if nw < 2000:
        print("SHORT", firm, p, nw)
        continue
    d = call_date(t) or FALLBACK.get(os.path.basename(p) if kind == "pdf" else p.split("/")[-2])
    if d is None:
        print("NODATE", firm, p)
        continue
    ref = d - dt.timedelta(days=60)  # reported quarter = quarter containing call date - 60d
    cq = f"{ref.year}Q{(ref.month - 1) // 3 + 1}"
    r = dict(firm=firm, cal_q=cq, call_date=d.isoformat(), words=nw, file=os.path.basename(p), url=url)
    for f in FAMS:
        tot = 0
        for term, rx in TERMS[f]:
            n = len(rx.findall(t))
            r[f"n::{f}::{term}"] = n
            tot += n
        r[f"n_{f}"] = tot
    rows.append(r)

D = pd.DataFrame(rows)
D = D[(D.cal_q >= "2018Q1")]
# one doc per firm-quarter (keep longest; duplicates are re-uploads)
D = D.sort_values("words", ascending=False).drop_duplicates(["firm", "cal_q"]).sort_values(["firm", "cal_q"])
D.to_csv(f"{OUT}/term_counts_doc.csv", index=False)

F = D[["firm", "cal_q", "call_date", "words", "url"]].copy()
for f in FAMS:
    F[f] = (D[f"n_{f}"] / D.words * 1e4).round(3)
F.to_csv(f"{OUT}/family_rates_fq.csv", index=False)

# ---------------- onsets ----------------
out = []
for firm, g in F.groupby("firm"):
    base = g[(g.cal_q >= "2019Q1") & (g.cal_q <= "2022Q4")]
    post = g[g.cal_q >= "2023Q1"]
    for f in FAMS:
        mu, sd = base[f].mean(), base[f].std()
        thr = mu + 2 * sd
        hit = post[post[f] > thr]
        out.append(dict(firm=firm, family=f, n_base=len(base), base_mean=round(mu, 2), base_sd=round(sd, 2),
                        threshold=round(thr, 2), first_onset=hit.cal_q.iloc[0] if len(hit) else "none",
                        n_post_above=len(hit), n_post=len(post), post_mean=round(post[f].mean(), 2),
                        quarters_above=";".join(hit.cal_q)))
O = pd.DataFrame(out)
O.to_csv(f"{OUT}/onsets.csv", index=False)
print(D.groupby("firm").cal_q.agg(["count", "min", "max"]))
print(O.to_string())
