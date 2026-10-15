"""Merge extension rows (Q2FY27 / investor days, BPO firms, pre-AI baseline and contract-structure evidence)
with the corpus rows (m2_statements_corpus.csv) into m2_statements.csv, re-verifying every extension quote
against the downloaded primary text in raw/ (or the local corpus copy for HCL Q1FY23).

Reads downloaded files -> run with:  python3 -I merge_extension.py
Verification: whitespace/ligature/quote-mark normalised substring, '...' = elision, fragments in order,
whole document (page numbers are taken from the agent row or from this round's own reading).
"""
import csv, html, os, re, subprocess

ROOT = "/Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/0. Exploratory Analysis"
OUT = f"{ROOT}/data/explore/round4/price_statements"
RAW = f"{OUT}/raw"
LIG = str.maketrans({"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl",
                     "’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-",
                     "­": "", "…": "...", " ": " "})
F = ["stmt_id", "firm", "segment", "event", "date", "speaker", "speaker_role", "type", "scope", "horizon",
     "tense", "net_of_baseline", "mag_lo", "mag_hi", "mag_unit", "use_in_m2", "quote", "page", "url",
     "confirmed", "source", "note"]


def nrm(s):
    s = re.sub(r"(\w)-\s+(\w)", r"\1-\2", s.translate(LIG))  # re-join words hyphenated across lines
    return re.sub(r"\s+", " ", s).strip().lower()


_cache = {}


def text_of(name):
    if name in _cache:
        return _cache[name]
    cands = []
    for d, _, fs in os.walk(RAW):
        for f in fs:
            if f == name or os.path.splitext(f)[0] == os.path.splitext(name)[0]:
                cands.append(os.path.join(d, f))
    if not cands:
        p = f"{ROOT}/data/sources/hcltech/transcripts_task3/{name}"
        cands = [p] if os.path.exists(p) else []
    t = ""
    for p in sorted(cands, key=lambda x: {".pdf": 0, ".txt": 1}.get(os.path.splitext(x)[1], 2)):
        if p.endswith(".pdf"):
            t = subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True).stdout
        else:
            raw = open(p, encoding="utf-8", errors="ignore").read()
            t = html.unescape(re.sub(r"<[^>]+>", " ", raw))
        if t.strip():
            break
    _cache[name] = nrm(t)
    return _cache[name]


def verify(name, quote):
    t = text_of(name)
    if not t:
        return "NOT CONFIRMED (file not found)"
    pos = 0
    for f in [x.strip() for x in re.split(r"\.\.\.|…", quote) if x.strip()]:
        j = t.find(nrm(f).strip(" \"'"), pos)
        if j < 0:
            return "NOT CONFIRMED"
        pos = j + len(nrm(f))
    return "CONFIRMED"


# classification of agent rows by index: (type, scope, horizon, tense, net, lo, hi, unit, use, note)
BPO_CLS = {
    0: ("portfolio_deflation_rate", "portfolio", "per_year", "current", "N", 1.5, 2.0, "% of revenue per year lost to efficiency ('cannibalisation')", "core_bpo", "Gross: includes pre-AI automation and offshoring (rows 9, 12)."),
    1: ("portfolio_deflation_rate", "portfolio", "per_year", "expectation", "N", 4.0, 5.0, "% of revenue per year in 2-3 years", "core_bpo", "Prediction from May 2025 for ~FY27-FY28; gross."),
    2: ("timing_or_bound", "portfolio", "n/a", "current", "unclear", "", "", "mechanism: lower transaction rate", "context", ""),
    3: ("price_same_scope", "single_deal", "one_off_level", "expectation", "unclear", 80, 80, "% lower price per bot-handled transaction (illustrative)", "outlier", "Illustration only."),
    4: ("timing_or_bound", "portfolio", "n/a", "expectation", "unclear", "", "", "'large part of the benefit' to clients (phi high)", "context", ""),
    5: ("timing_or_bound", "renewals", "n/a", "past", "unclear", "", "", "no price increases; renewal pressure", "context", ""),
    6: ("renewal_structure", "portfolio", "n/a", "past", "n/a", 3, 3, "typical contract term, years", "conversion", ""),
    7: ("renewal_structure", "portfolio", "n/a", "past", "n/a", 90, 90, "% recurring revenue; FTE or transaction pricing", "conversion", ""),
    8: ("baseline_pre_AI", "portfolio", "per_year", "past", "N", "", "", "standing efficiency give-back (no %)", "baseline", ""),
    9: ("portfolio_deflation_rate", "portfolio", "per_year", "current", "N", 1.5, 2.0, "% of revenue per year ('150, 200 basis points')", "core_bpo", "Gross; includes onshore-offshore migration."),
    10: ("timing_or_bound", "portfolio", "n/a", "expectation", "unclear", "", "", "more efficiency commitments expected", "context", ""),
    11: ("baseline_pre_AI", "portfolio", "per_year", "past", "N", "", "", "year-on-year productivity offsets price reductions", "context", ""),
    12: ("baseline_pre_AI", "portfolio", "per_year", "past", "N", 1.0, 1.5, "% of revenue per year BEFORE AI ('100 to 150 bps'); rising to 2.0 near term", "core_bpo", "Key: pre-AI baseline (incl. offshoring and older automation)."),
    13: ("timing_or_bound", "portfolio", "n/a", "current", "unclear", "", "", "pricing pressure > increases", "context", ""),
    14: ("renewal_structure", "industry", "n/a", "current", "n/a", 75, 75, "% of IT services and BPO industry on T&M (CEO's estimate)", "conversion", ""),
    15: ("renewal_structure", "portfolio", "n/a", "current", "n/a", "", "", "Firstsource: 'meaningful number' non-linear", "context", ""),
    16: ("renewal_structure", "portfolio", "n/a", "current", "n/a", "", "", "'large part' non-headcount", "context", ""),
    17: ("delivery_productivity", "single_deal", "n/a", "past", "unclear", 20, 20, "% effort reduction, chat pilot (100 -> 80)", "s_only", "Aug 2023; CEO declines to extrapolate."),
    18: ("timing_or_bound", "single_deal", "n/a", "current", "unclear", "", "", "platform fee + per-interaction pricing", "context", ""),
    19: ("renewal_structure", "portfolio", "n/a", "current", "n/a", 80, 80, "% of eClerx work FTE-priced", "conversion", ""),
    20: ("delivery_productivity", "service_line", "n/a", "current", "unclear", 15, 15, "% minimum productivity gate for AI pilots", "s_only", ""),
    21: ("timing_or_bound", "portfolio", "n/a", "past", "unclear", 0, 0, "no annual productivity pass-back asked by top clients", "core_bpo", "Lower bound evidence (KPO)."),
    22: ("delivery_productivity", "single_deal", "n/a", "past", "unclear", 87, 87, "% time per case (4h -> 30min)", "s_only", ""),
}
BASE_CLS = {
    0: ("baseline_pre_AI", "portfolio", "per_year", "past", "N", "", "", "productivity commitments dip Q1 revenue (no %)", "baseline", "Pre-2023."),
    1: ("baseline_pre_AI", "portfolio", "per_year", "past", "N", "", "", "commitments 'for several years' (no %)", "baseline", "Pre-2023."),
    2: ("baseline_pre_AI", "service_line", "per_year", "past", "N", "", "", "year-on-year productivity benefit in managed services (no %)", "baseline", "Offset by COLA clauses."),
    3: ("baseline_pre_AI", "single_deal", "per_year", "past", "N", "", "", "contract charge declines yearly; % REDACTED", "baseline", "Client 10-K exhibit (Health Net/Cognizant, 2010)."),
    4: ("baseline_pre_AI", "single_deal", "per_year", "past", "N", "", "", "annual productivity improvement; % REDACTED", "baseline", ""),
    5: ("baseline_pre_AI", "single_deal", "n/a", "past", "N", "", "", "TCS MSA productivity commitments (no %)", "baseline", "Client 10-K exhibit (Nielsen/TCS, 2018)."),
    6: ("renewal_structure", "portfolio", "n/a", "past", "n/a", 49.6, 49.6, "% of Accenture FY25 revenue from managed services", "conversion", "Computed from table."),
    7: ("renewal_structure", "service_line", "n/a", "current", "n/a", "", "", "managed services 'several years'", "conversion", ""),
    8: ("renewal_structure", "service_line", "n/a", "current", "n/a", "", "", "consulting <12 months", "conversion", ""),
    9: ("renewal_structure", "portfolio", "n/a", "past", "n/a", "", "", "RPO ~$34bn", "conversion", ""),
    10: ("renewal_structure", "portfolio", "n/a", "past", "n/a", 35.9, 47.4, "% outsourcing (35.9) / fixed-price (47.4) of Cognizant 2025 revenue; T&M 43.3", "conversion", "Computed from table."),
    11: ("renewal_structure", "portfolio", "n/a", "past", "n/a", 35, 55, "% of FP RPO recognised within 1 yr (35) / 2 yrs (55)", "conversion", ""),
    12: ("renewal_structure", "portfolio", "n/a", "past", "n/a", 54, 54, "% Infosys revenue fixed-price FY26", "conversion", ""),
    13: ("renewal_structure", "portfolio", "n/a", "past", "n/a", 49.7, 49.7, "% of Infosys RPO recognised within 1 yr", "conversion", ""),
    14: ("renewal_structure", "portfolio", "n/a", "current", "n/a", "", "", "short-term engagements (risk factor)", "context", ""),
    15: ("renewal_structure", "portfolio", "n/a", "past", "n/a", 63, 63, "% of Wipro RPO within 2 yrs (FY26)", "conversion", ""),
    16: ("renewal_structure", "portfolio", "n/a", "past", "n/a", 52.4, 52.4, "% Wipro IT services revenue fixed-price & volume-based FY26", "conversion", "Computed from table."),
}
IT_CLS = {
    0: ("single_deal_commitment", "single_deal", "one_off_level", "past", "unclear", 20, 20, "% 'benefit' on an incumbent app-dev portfolio (aerospace OEM)", "outlier", "Showcase; 'cannibalizing our own revenue'; not defined as price."),
    1: ("delivery_productivity", "single_deal", "n/a", "past", "unclear", 25, 25, "% productivity, one client", "s_only", ""),
    2: ("delivery_productivity", "single_deal", "n/a", "past", "unclear", 30, 30, "% productivity, one client", "s_only", ""),
}

# rows read this round from downloaded files
OWN = [
    dict(stmt_id="EXT-TCS-Q2FY27-a", firm="TCS", segment="IT", event="Q2FY27 earnings call (transcript filed with BSE 14 Oct 2026)", date="2026-10-08",
         speaker="Samir Seksaria, CFO", quote="See, there would be some frontloading of productivity benefits that could happen. But at the same time, we are seeing better pricing on the AI revenues we are generating.",
         file="TCS_Q2FY27_transcript_BSE.pdf", page="PDF p.20", url="BSE filing (local raw/it_q2fy27/TCS_Q2FY27_transcript_BSE.pdf)",
         cls=("timing_or_bound", "portfolio", "n/a", "current", "unclear", "", "", "front-loaded productivity benefits; better AI pricing", "core", "Call date = board meeting date stated in the filing cover letter.")),
    dict(stmt_id="EXT-TCS-Q2FY27-b", firm="TCS", segment="IT", event="Q2FY27 earnings call (transcript filed with BSE 14 Oct 2026)", date="2026-10-08",
         speaker="Samir Seksaria, CFO", quote="And if you take the revenue per employee, you will see there's a slight reduction, not a significant one. So, at an overall portfolio level, the pricing is broadly stable.",
         file="TCS_Q2FY27_transcript_BSE.pdf", page="PDF p.20", url="BSE filing (local raw/it_q2fy27/TCS_Q2FY27_transcript_BSE.pdf)",
         cls=("timing_or_bound", "portfolio", "n/a", "current", "unclear", 0, 1, "portfolio pricing 'broadly stable' H1 FY27 (read as <~1%)", "core", "Includes mix (better AI pricing), so same-scope price can still fall; used to cap TCS FY27.")),
    dict(stmt_id="EXT-CTSH-JEF-2026", firm="Cognizant", segment="IT", event="Jefferies Nasdaq investor conference", date="2026-06-10",
         speaker="Jatin Dalal, CFO (attribution from transcript layout)", quote="Although there is very little deflation at a aggregate industry and company level because even with that deflation at individual project level, we are seeing that the last year we grew 6%-plus.",
         file="CTSH_Jefferies_2026-06-10_transcript.pdf", page="PDF p.3", url="Cognizant IR (local raw/it_q2fy27/CTSH_Jefferies_2026-06-10_transcript.pdf; FactSet CallStreet corrected transcript)",
         cls=("timing_or_bound", "portfolio", "n/a", "past", "unclear", "", "", "'very little deflation' at company level", "context", "Comparator firm.")),
]


def row(sid, firm, seg, event, date, speaker, role, cls, quote, page, url, conf, source, extra_note=""):
    typ, scope, hor, tense, net, lo, hi, unit, use, note = cls
    return dict(stmt_id=sid, firm=firm, segment=seg, event=event, date=date, speaker=speaker, speaker_role=role,
                type=typ, scope=scope, horizon=hor, tense=tense, net_of_baseline=net, mag_lo=lo, mag_hi=hi,
                mag_unit=unit, use_in_m2=use, quote=quote, page=page, url=url, confirmed=conf, source=source,
                note="; ".join(x for x in (note, extra_note) if x))


def main():
    rows = list(csv.DictReader(open(f"{OUT}/m2_statements_corpus.csv")))
    for i, r in enumerate(csv.DictReader(open(f"{RAW}/bpo/agent_rows.csv"))):
        conf = verify(r["local_file"], r["quote"])
        seg = "BPO"
        rows.append(row(f"EXT-BPO-{i:02d}", r["firm"], seg, r["event"], r["date"], r["speaker_title"],
                        "management", BPO_CLS[i], r["quote"], f"PDF p.{r['page']}", r["url"], conf,
                        "raw/bpo/agent_rows.csv", r.get("note", "")))
    for i, r in enumerate(csv.DictReader(open(f"{RAW}/baseline/agent_rows.csv"))):
        conf = verify(r["local_file"], r["quote"])
        role = "management" if "Contract" not in r["speaker_title"] and "Filing" not in r["speaker_title"] else "filing/contract text"
        pg = r["page"] if r["page"] == "HTML" else f"PDF p.{r['page']}"
        rows.append(row(f"EXT-BASE-{i:02d}", r["firm"], r["segment"], r["event"], r["date"], r["speaker_title"],
                        role, BASE_CLS[i], r["quote"], pg, r["url"], conf, "raw/baseline/agent_rows.csv",
                        r.get("disclosed_figure", "")))
    for i, r in enumerate(csv.DictReader(open(f"{RAW}/it_q2fy27/agent_rows.csv"))):
        conf = verify("TCS_AnalystDay_2025-12-17_transcript_BSE.pdf", r["quote_verbatim"])
        rows.append(row(f"EXT-IT-{i:02d}", r["firm"], "IT", r["event"], r["date"], r["speaker_title"], "management",
                        IT_CLS[i], r["quote_verbatim"], r["page"], r["url"], conf, "raw/it_q2fy27/agent_rows.csv"))
    for o in OWN:
        conf = verify(o["file"], o["quote"])
        rows.append(row(o["stmt_id"], o["firm"], o["segment"], o["event"], o["date"], o["speaker"], "management",
                        o["cls"], o["quote"], o["page"], o["url"], conf, "raw/it_q2fy27 (read this round)"))
    with open(f"{OUT}/m2_statements.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=F); w.writeheader(); w.writerows(rows)
    bad = [(r["stmt_id"], r["confirmed"]) for r in rows if r["confirmed"] != "CONFIRMED"]
    print(len(rows), "rows;", len(rows) - len(bad), "CONFIRMED; not:", bad)


if __name__ == "__main__":
    main()
