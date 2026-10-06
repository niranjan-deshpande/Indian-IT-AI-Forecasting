"""Hand-entered Infosys large-deal TCV, net-new share and AI disclosures, each verified against the text of the
primary document (the script asserts the supporting quote is present in the local copy).
Sources: IFRS USD press release (6-K Ex 99.1 = 'pr'), fact sheet PDF page-1 banner ('fs'), or a transcript exhibit
of the same results 6-K (filename given, e.g. 'exv99w06.htm').
Output: data/sources/infosys/parsed_manual.csv
"""
import re, os, sys, csv, json, subprocess
from bs4 import BeautifulSoup
sys.path.insert(0, os.path.dirname(__file__))
from infosys_common import *

FIL = filings()
META = json.load(open(f"{BASE}/factsheets/meta.json"))
TCV_NOTE = "TCV of large deals (Infosys definition: deals with TCV > $50mn); hand-entered from text"
T = []  # (fq, metric, value, unit, period_type, src, quote_regex, note)
tcv = [
    ("Q1FY16", 688, "pr", r"TCV of \$ 688 mn", "6 large deals"),
    ("Q2FY16", 983, "pr", r"TCV of \$ 983 mn", "5 large deals"),
    ("Q3FY16", 362, "exv99w03.htm", r"total TCV of \$ 362 million", "4 large deals; press conference transcript (earnings call says 'nearly $360 mn')"),
    ("Q4FY16", 757, "exv99w06.htm", r"TCV of \$757 mn", "6 large deals; earnings call transcript"),
    ("Q1FY17", 809, "exv99w06.htm", r"\$809 mn of TCV", "earnings call; excludes a frame agreement with a large financial services firm"),
    ("Q2FY17", 1209, "exv99w06.htm", r"large deal wins of \$1\.209 bn", "earnings call; includes committed value $138mn + framework deals $1,071mn"),
    ("Q3FY17", 664, "exv99w06.htm", r"TCV of \$664 mn", "earnings call; 8 large deals, of which $436mn new committed"),
    ("Q4FY17", 806, "exv99w06.htm", r"TCV of \$806 mn", "earnings call; $623mn framework + $183mn committed value"),
    ("Q1FY18", 657, "exv99w07.htm", r"total TCV for this quarter is \$657 ?mn", "earnings call (2nd)"),
    ("Q2FY18", 731, "exv99w06.htm", r"TCV of \$731 mn", "earnings call; 5 large deals"),
    ("Q3FY18", 779, "exv99w06.htm", r"TCV of \$779 mn", "earnings call; 8 large deals"),
    ("Q4FY18", 905, "exv99w06.htm", r"TCV of \$905 mn", "earnings call; 10 large deals"),
    ("Q1FY19", 1100, "exv99w06.htm", r"TCV of US \$1\.1 bn", "earnings call; press release says 'crossed $1 billion'"),
    ("Q2FY19", 2030, "exv99w06.htm", r"TCV of \$2\.03 bn", "earnings call; press release says 'crossed $2 billion'"),
    ("Q3FY19", 1570, "pr", r"large deals at \$1\.57 billion", ""),
    ("Q4FY19", 1570, "fs", r"\$1\.57Bn Q4", "fact sheet banner 'Large deal signings'"),
    ("Q1FY20", 2700, "pr", r"large deal TCV at \$ 2\.7 bn", ""),
    ("Q2FY20", 2800, "pr", r"Large deal wins were \$2\.8 bn", "earnings call cites $2.85bn"),
    ("Q3FY20", 1800, "fs", r"\$1\.8 bn", "fact sheet banner 'Large deal signings'"),
    ("Q4FY20", 1650, "fs", r"\$1\.65bn Q4", "fact sheet banner 'Large deal signings'"),
    ("Q1FY21", 1740, "fs", r"\$1\.74bn", "fact sheet banner 'Large deal signings'"),
    ("Q2FY21", 3150, "pr", r"large deal TCV at \$ 3\.15 bn", ""),
    ("Q3FY21", 7130, "pr", r"Large deal TCV was at all time high of \$7\.13bn", "includes Vanguard mega deal"),
    ("Q4FY21", 2100, "fs", r"\$2\.1 bn Q4", "fact sheet banner 'Large deal signings'"),
    ("Q1FY22", 2600, "pr", r"TCV of \$2\.6 billion in Q1", ""),
    ("Q2FY22", 2150, "pr", r"TCV of \$2\.15 billion in Q2", ""),
    ("Q3FY22", 2530, "pr", r"TCV of \$2\.53 billion in Q3", ""),
    ("Q4FY22", 2300, "pr", r"TCV of large deal wins was \$2\.3 billion in Q4", ""),
    ("Q1FY23", 1690, "exv99w05.htm", r"TCV of \$1\.69 bn", "earnings call; fact sheet banner shows $1.7 bn"),
    ("Q2FY23", 2700, "pr", r"Large deal TCV for the quarter was robust at \$2\.7 bn", ""),
    ("Q3FY23", 3300, "pr", r"strongest in the last 8 quarters at \$3\.3 billion", ""),
    ("Q4FY23", 2100, "exv99w05.htm", r"TCV was \$2\.1 bn with 21% net new", "earnings call; fact sheet banner $2.1 bn Q4"),
    ("Q1FY24", 2300, "pr", r"Large deal TCV for the quarter was at \$2\.3 billion", ""),
    ("Q2FY24", 7700, "pr", r"Large deal TCV for the quarter was \$7\.7 billion", "includes mega deals"),
    ("Q3FY24", 3200, "pr", r"Large deal TCV for the quarter was \$3\.2 billion", ""),
    ("Q4FY24", 4500, "pr", r"Large deal TCV for the quarter was \$4\.5 billion", ""),
    ("Q1FY25", 4100, "pr", r"34 with TCV of \$4\.1 billion", "34 large deals"),
    ("Q2FY25", 2400, "pr", r"TCV of large deal wins was \$2\.4 billion", ""),
    ("Q3FY25", 2500, "pr", r"TCV of large deal wins was \$2\.5 billion", ""),
    ("Q4FY25", 2600, "exv99w05.htm", r"TCV of \$2\.6 bn, 63% of this", "earnings call; fact sheet banner $2.6 Bn Q4"),
    ("Q1FY26", 3800, "pr", r"TCV of large deal wins was \$3\.8 billion", ""),
    ("Q2FY26", 3100, "pr", r"TCV of large deal wins was \$3\.1 billion", ""),
    ("Q3FY26", 4800, "pr", r"TCV of large deal wins was \$4\.8 billion", ""),
    ("Q4FY26", 3200, "exv99w05.htm", r"TCV of \$3\.2 bn", "earnings call; fact sheet banner $3.2 Bn Q4"),
    ("Q1FY27", 3600, "pr", r"TCV of large deal wins was \$3\.6 billion", ""),
]
for fq, v, src, q, n in tcv:
    T.append((fq, "tcv", v, "USD_mn", "quarter", src, q, TCV_NOTE + ("; " + n if n else "")))
tcv_annual = [
    ("Q4FY17", 3500, "exv99w04.htm", r"Pravin Rao \$3\.5 bn", "FY17 total, press conference answer"),
    ("Q4FY19", 6280, "fs", r"\$6\.28Bn FY", "FY19 total, fact sheet banner"),
    ("Q4FY20", 9000, "fs", r"\$9\.0bn FY", "FY20 total, fact sheet banner"),
    ("Q4FY21", 14100, "pr", r"\$14\.1 billion with 66% being net new", "FY21 total"),
    ("Q4FY22", 9500, "pr", r"large deal wins with TCV of \$9\.5 billion", "FY22 total"),
    ("Q4FY23", 9800, "fs", r"\$9\.8 bn FY", "FY23 total, fact sheet banner"),
    ("Q4FY24", 17700, "pr", r"Large deal TCV for FY24 was highest ever at \$17\.7 billion", "FY24 total"),
    ("Q4FY25", 11600, "pr", r"TCV of large deal wins was \$11\.6 billion for the year", "FY25 total"),
    ("Q4FY26", 14900, "pr", r"TCV of large deal wins was \$14\.9 billion", "FY26 total"),
]
for fq, v, src, q, n in tcv_annual:
    T.append((fq, "tcv", v, "USD_mn", "annual", src, q, TCV_NOTE + "; " + n))
NN = "share of large-deal TCV that is net new (vs renewals), as stated"
netnew = [
    ("Q4FY20", 56, "exv99w05.htm", r"56% of it was net new", "quarter", "earnings call"),
    ("Q1FY21", 19, "exv99w05.htm", r"19% was net new", "quarter", "earnings call"),
    ("Q3FY21", 73, "pr", r"73% being net new", "quarter", ""),
    ("Q4FY21", 66, "pr", r"66% being net new", "annual", "FY21"),
    ("Q1FY23", 50, "exv99w03.htm", r"50% of these were net new", "quarter", "press conference"),
    ("Q4FY23", 21, "exv99w05.htm", r"TCV was \$2\.1 bn with 21% net new", "quarter", "earnings call"),
    ("Q4FY23", 40, "exv99w05.htm", r"\$9\.8 bn for the year, with 40% net new", "annual", "FY23; earnings call"),
    ("Q1FY24", 56.1, "pr", r"net new of 56\.1%", "quarter", ""),
    ("Q2FY24", 48, "pr", r"net new of 48%", "quarter", ""),
    ("Q3FY24", 71, "pr", r"71% being net new", "quarter", ""),
    ("Q4FY24", 44, "pr", r"44% being net new", "quarter", ""),
    ("Q4FY24", 52, "pr", r"52% being net new", "annual", "FY24"),
    ("Q1FY25", 57.6, "pr", r"57\.6% being net new", "quarter", ""),
    ("Q2FY25", 41, "pr", r"41% being net new", "quarter", ""),
    ("Q3FY25", 63, "pr", r"63% net new", "quarter", ""),
    ("Q4FY25", 63, "exv99w05.htm", r"TCV of \$2\.6 bn, 63% of this", "quarter", "earnings call"),
    ("Q4FY25", 56, "pr", r"\$11\.6 billion for the year, with 56% net new", "annual", "FY25"),
    ("Q1FY26", 55, "pr", r"55% net new", "quarter", ""),
    ("Q2FY26", 67, "pr", r"net new of 67%", "quarter", ""),
    ("Q3FY26", 57, "pr", r"net new of 57%", "quarter", ""),
    ("Q4FY26", 55, "pr", r"\$14\.9 billion, with net new of 55%", "annual", "FY26"),
    ("Q1FY27", 61, "pr", r"61% net new", "quarter", ""),
]
for fq, v, src, q, pt, n in netnew:
    T.append((fq, "tcv_net_new_share", v, "pct", pt, src, q, NN + ("; " + n if n else "")))
T.append(("Q2FY18", "tcv_net_new", 495, "USD_mn", "quarter", "exv99w06.htm", r"TCV of \$731 mn",
          "net new portion of large-deal TCV ($495mn of $731mn) stated in press conference/TV call (exv99w03/04); quote check on TCV only"))
# AI
T.append(("Q1FY24", "ai_disclosure", 80, "count", "point", "pr", r"80 active client projects",
          "generative AI: number of active client projects (press release quote: 'Our generative AI capabilities are expanding well, with 80 active client projects')"))
T.append(("Q3FY26", "ai_disclosure", 5.5, "pct", "quarter", "Q1FY27:exv99w05.htm", r"our AI revenue, which was 5\.5% for Q3",
          "AI services revenue as % of total revenue for Q3FY26 (first disclosed at Feb-2026 Investor AI Day; figure taken from Q1FY27 earnings call transcript)"))
T.append(("Q1FY27", "ai_disclosure", 8.2, "pct", "quarter", "pr", r"AI Revenues at 8\.2% in Q1",
          "AI services revenue as % of total revenue ('primary AI revenue' from Infosys AI strategy value pools; excludes AI-infused work per call); also on fact sheet banner 'AI as a % of Revenue'"))

_cache = {}


def text_of(path):
    if path not in _cache:
        if path.endswith(".pdf"):
            _cache[path] = re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", "-l", "1", path, "-"], capture_output=True, text=True).stdout)
        else:
            _cache[path] = re.sub(r"\s+", " ", BeautifulSoup(open(path, encoding="latin-1").read(), "html.parser").get_text(" ", strip=True))
    return _cache[path]


rows = []
for fq, metric, v, unit, pt, src, q, note in T:
    sfq = fq
    if ":" in src:
        sfq, src = src.split(":")
    f = FIL[sfq]
    if src == "fs":
        path = META[sfq]["file"]; url = META[sfq]["url"]
        sdoc = f"Infosys {sfq} fact sheet (archived copy web.archive.org/web/{META[sfq]['ts']})"; loc = "p1 headline banner"
    else:
        exf = "exv99w01.htm" if src == "pr" else src
        path = f"{BASE}/edgar/{f['acc']}/{exf}"; url = f["base"] + exf
        raw = open(path, encoding="latin-1").read(3000)
        desc = (re.search(r"<DESCRIPTION>(.*)", raw) or [0, ""])[1].strip().title()
        sdoc = f"Infosys {sfq} {desc} (6-K exhibit)"; loc = "text"
    assert re.search(q, text_of(path)), (fq, metric, q, path)
    pe = fq_to_pe(fq)
    fqq, pes, calq = period_info(pe)
    rows.append(dict(firm="infosys", fiscal_q=fqq, period_end=pes, cal_q=calq, metric=metric, dimension="total", dim_type="total",
                     value=v, unit=unit, basis="na", period_type=pt, source_url=url, source_doc=sdoc, source_loc=loc,
                     doc_date=f["announce_date"], notes=note + "; hand-entered"))
with open(f"{BASE}/parsed_manual.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=COLS); w.writeheader(); w.writerows(rows)
print(len(rows), "rows; all quotes verified")
