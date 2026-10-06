"""Hand-entered Tech Mahindra values.

(a) Press releases / earnings presentations: USD revenue growth (reported & constant currency) for quarters where
    the fact sheet has no growth table (FY17-FY20, FY26-FY27), plus 'Digital' revenue share (FY20).
(b) Image-only consolidated-results PDFs (no text layer): values read from macOS Vision OCR output
    (data/sources/techm/ocr/*.ocr.txt, produced by scripts/extract/techm_ocr.swift) and verified visually against
    the rendered page images; IT+BPO segment revenue was checked to sum to reported revenue.
All values are transcribed as printed; Rs lakh values converted to INR mn by /10.
"""
from techm_common import row, BASE_URL, prev_q

DOC_DATE_OVERRIDES = {"Q4FY19": "2019-05-21"}  # Q4FY19 PR is image-only; dateline read from OCR

# ---- (a) growth statements: fiscal_q -> list of (metric, period, basis, value, period_type, source file, loc, note)
PR = "Press release"
GROWTH = {
    "Q1FY17": [("qoq", "reported", 0.9), ("yoy", "reported", 4.3)],
    "Q2FY17": [("qoq", "reported", 4.0), ("yoy", "reported", 6.1), ("qoq", "cc", 5.0), ("yoy", "cc", 7.5)],
    "Q3FY17": [("qoq", "reported", 4.1), ("yoy", "reported", 10.0), ("qoq", "cc", 5.4), ("yoy", "cc", 12.0)],
    "Q4FY17": [("qoq", "reported", 1.3), ("yoy", "reported", 10.6), ("qoq", "cc", 0.9), ("yoy", "cc", 12.1)],
    "Q1FY18": [("qoq", "reported", 0.6), ("yoy", "reported", 10.3)],
    "Q2FY18": [("qoq", "reported", 3.6), ("yoy", "reported", 10.0)],
    "Q3FY18": [("qoq", "reported", 2.5), ("yoy", "reported", 8.3)],
    "Q4FY18": [("qoq", "reported", 2.9), ("yoy", "reported", 10.0)],
    "Q1FY19": [("qoq", "reported", -1.6), ("yoy", "reported", 7.5), ("qoq", "cc", 0.3)],
    "Q2FY19": [("qoq", "reported", -0.5), ("yoy", "reported", 3.3), ("qoq", "cc", 0.4)],
    "Q3FY19": [("qoq", "reported", 3.5), ("yoy", "reported", 4.3), ("qoq", "cc", 4.3)],
    "Q4FY19": [("yoy", "reported", 1.9)],
    "Q1FY20": [("yoy", "reported", 1.9), ("yoy", "cc", 3.7)],
    "Q2FY20": [("qoq", "reported", 3.2), ("qoq", "cc", 4.1)],
    "Q3FY20": [("qoq", "reported", 5.1), ("qoq", "cc", 4.3)],
    "Q4FY20": [("qoq", "reported", -4.3), ("qoq", "cc", -3.3)],
    "Q2FY26": [("qoq", "reported", 1.4), ("yoy", "reported", -0.2), ("qoq", "cc", 1.6), ("yoy", "cc", -0.3)],
    "Q3FY26": [("qoq", "reported", 1.5), ("yoy", "reported", 2.7), ("qoq", "cc", 1.7), ("yoy", "cc", 1.3)],
    "Q4FY26": [("qoq", "reported", 0.9), ("yoy", "reported", 4.9), ("qoq", "cc", 0.6), ("yoy", "cc", 2.4)],
    "Q1FY27": [("qoq", "reported", 2.2), ("yoy", "reported", 6.1), ("qoq", "cc", 2.6), ("yoy", "cc", 6.6)],
}
GROWTH_NOTES = {
    "Q1FY20": "PR: 'Revenue growth at 3.7% in constant currency terms' as sub-bullet under 'up 1.9% YoY' -> recorded as YoY cc (judgment; QoQ reported was negative)",
    "Q2FY20": "PR: 'Revenue growth at 4.1% in constant currency terms' as sub-bullet under 'up 3.2% QoQ' -> recorded as QoQ cc (judgment)",
    "Q3FY20": "PR: 'Revenue growth at 4.3% in constant currency terms' as sub-bullet under 'up 5.1% QoQ' -> recorded as QoQ cc (judgment)",
    "Q4FY20": "PR: 'Revenue degrowth at 3.3% in constant currency terms' as sub-bullet under 'down 4.3% QoQ' -> recorded as QoQ cc (judgment)",
    "Q4FY19": "Q4FY19 PR is an image-only PDF; read via OCR (hand-entered). Quarter cc growth not stated.",
}
PR_FILES = {
    "Q1FY17": "Tech_Mahindra_PressRelease_Q117.pdf", "Q2FY17": "Tech-Mahindra-Press-Release-Q2-FY17.pdf",
    "Q3FY17": "Tech-Mahindra-Press-Release-Q3-FY17.pdf", "Q4FY17": "Tech-Mahindra-Press-Release-Q4-FY17.PDF",
    "Q1FY18": "Tech-Mahindra-Press-Release-Q1-FY18.PDF", "Q2FY18": "Tech-Mahindra-Press-Release-Q2-FY18.pdf",
    "Q3FY18": "Q3-fy18-pr.pdf", "Q4FY18": "Q4-fy18-pr.pdf", "Q1FY19": "Q1-fy19-pr.pdf", "Q2FY19": "Q2-fy19-pr.pdf",
    "Q3FY19": "Q3-FY19-earnings-PR.pdf", "Q4FY19": "Q4-FY19-earnings-PR.pdf", "Q1FY20": "Q1-fy20-pr.pdf",
    "Q2FY20": "Q2-fy20-pr.pdf", "Q3FY20": "TML-Q3-FY-20-Press-Release.pdf", "Q4FY20": "TML-Q4-FY-20-Press-Release.pdf",
    "Q2FY26": "tml-q2-fy-26-press-release.pdf", "Q3FY26": "tml-q3-fy-26-press-release.pdf",
    "Q4FY26": "tml-q4-fy-26-press-release.pdf", "Q1FY27": "tml-q1-fy-27-press-release.pdf",
}
# Q1FY26 press release omits cc growth; the Q1FY26 earnings presentation states it.
PRES_GROWTH = {"Q1FY26": ("tml-q1-fy-26-earnings-presentation.pdf",
                          [("qoq", "reported", 1.0), ("yoy", "reported", 0.4), ("qoq", "cc", -1.4), ("yoy", "cc", -1.0)])}
ANNUAL_GROWTH = [  # (fiscal_q of Q4, basis, value, file)
    ("Q4FY19", "reported", 4.2, "Q4-FY19-earnings-PR.pdf"), ("Q4FY19", "cc", 5.8, "Q4-FY19-earnings-PR.pdf"),
    ("Q4FY20", "reported", 4.3, "TML-Q4-FY-20-Press-Release.pdf"), ("Q4FY20", "cc", 5.6, "TML-Q4-FY-20-Press-Release.pdf"),
    ("Q4FY26", "reported", 1.9, "tml-q4-fy-26-press-release.pdf"), ("Q4FY26", "cc", 0.6, "tml-q4-fy-26-press-release.pdf"),
]
# Company-published earnings-call transcripts (cc growth disclosed only on the call)
TRANSCRIPT = [  # (fiscal_q, metric, dimension, dim_type, basis, value, period_type, file, quote-note)
    ("Q2FY18", "revenue_growth_qoq", "total", "total", "cc", 2.3, "quarter", "Earnings-Call-Transcript-Q2-FY18.pdf",
     "CFO: 'sequential revenue growth in constant currency was 2.3%'"),
    ("Q4FY18", "revenue_growth_qoq", "total", "total", "cc", 1.7, "quarter", "Q4-FY18-call-transcript.pdf",
     "CFO: 'Q4 revenue growth in constant currency term was 1.7% QoQ'"),
    ("Q4FY18", "revenue_growth_yoy", "total", "total", "cc", 7.8, "annual", "Q4-FY18-call-transcript.pdf",
     "FY18 full year: 'constant currency growth was about 7.8%'"),
    ("Q2FY20", "revenue_growth_yoy", "total", "total", "cc", 7.3, "quarter", "Q2-FY20-call-transcript.pdf",
     "CFO: revenues grew 'about 7.3% YoY on a constant currency basis'"),
    ("Q2FY20", "segment_growth_qoq", "Enterprise", "vertical", "cc", 5.6, "quarter", "Q2-FY20-call-transcript.pdf",
     "CFO: 'Enterprise business had a very strong quarter of 5.6% growth in CC terms' (sequential)"),
    ("Q2FY20", "segment_growth_qoq", "Communications", "vertical", "cc", 2.0, "quarter", "Q2-FY20-call-transcript.pdf",
     "CFO: 'Communications grew about 2% in CC terms sequentially' (approximate)"),
]
# Quantitative AI statements (workforce enablement only; no AI revenue/bookings disclosed in collected docs)
AI = [  # (fiscal_q, dimension, value, file, quote)
    ("Q3FY26", "Sales & support workforce AI-enabled", 80.0, "tml-q3-fy-26-earnings-presentation.pdf", "'80%+ Sales & support workforce enabled with AI' (lower bound)"),
    ("Q4FY26", "Global workforce AI-enabled", 80.0, "tml-q4-fy-26-earnings-presentation.pdf", "'80% of our global workforce is now AI-enabled'"),
    ("Q4FY26", "Employees with advanced AI training & certification", 76.0, "tml-q4-fy-26-earnings-presentation.pdf", "'76% of employees have completed advanced AI training and achieved AI certification'"),
    ("Q4FY26", "Customer-facing employees AI-enabled", 84.0, "tml-q4-fy-26-earnings-presentation.pdf", "'84% of customer-facing employees are AI-enabled'"),
]
DIGITAL = {"Q1FY20": 36.0, "Q2FY20": 39.0, "Q3FY20": 41.0, "Q4FY20": 44.0}

# ---- (b) image-only consolidated results: file -> (doc fiscal_q, scale, {metric/dim: [cur, prev q, yoy q]})
OCR_RESULTS = {
    "Tech_Mahindra_Consolidated_Q117.pdf": ("Q1FY17", 0.1, {
        ("revenue", "total"): [692093, 688373, 629382],
        ("employee_cost", "total"): [362740, 362306, 335425],
        ("subcontracting_cost", "total"): [87192, 83947, 91356],
        ("segment_revenue", "IT"): [643212, 639973, 584323],
        ("segment_revenue", "BPO"): [48881, 48400, 45059]}),
    "Tech-Mahindra-Consolidated-Q2-FY17.pdf": ("Q2FY17", 0.1, {
        ("revenue", "total"): [716741, 692093, 661554],
        ("employee_cost", "total"): [390217, 362740, 348063],
        ("subcontracting_cost", "total"): [87436, 87192, 90519],
        ("segment_revenue", "IT"): [668461, 643212, 610951],
        ("segment_revenue", "BPO"): [48280, 48881, 50603]}),
    "Q3-FY18-Consol-Results.pdf": ("Q3FY18", 0.1, {
        ("revenue", "total"): [777596, 760638, 755750],
        ("employee_cost", "total"): [421288, 420500, 393202],
        ("subcontracting_cost", "total"): [97794, 93718, 89464],
        ("segment_revenue", "IT"): [715710, 708752, 703116],
        ("segment_revenue", "BPO"): [61886, 51886, 52634]}),
    "Q4-FY18-Consol-Results.pdf": ("Q4FY18", 0.1, {
        ("revenue", "total"): [805450, 777596, 749500],
        ("employee_cost", "total"): [414530, 421288, 399235],
        ("subcontracting_cost", "total"): [106390, 97794, 97025],
        ("segment_revenue", "IT"): [746367, 715710, 697576],
        ("segment_revenue", "BPO"): [59083, 61886, 51924]}),
    "Q1-FY19-Consol-Results.pdf": ("Q1FY19", 0.1, {
        ("revenue", "total"): [827628, 805450, 733610],
        ("employee_cost", "total"): [437946, 414530, 406079],
        ("subcontracting_cost", "total"): [97041, 106390, 90894],
        ("segment_revenue", "IT"): [766151, 746367, 686320],
        ("segment_revenue", "BPO"): [61477, None, 47290]}),
    "Q2-F19-Consolidated-Results.pdf": ("Q2FY19", 0.1, {
        ("revenue", "total"): [862985, 827628, 760638],
        ("employee_cost", "total"): [430311, 437946, 420500],
        ("subcontracting_cost", "total"): [111541, 97041, 93718],
        ("segment_revenue", "IT"): [796487, 766151, 708752],
        ("segment_revenue", "BPO"): [66498, 61477, 51886]}),
    "Q3-Fy19-Consolidated-Results.pdf": ("Q3FY19", 1.0, {
        ("revenue", "total"): [89437, 86298, 77760],
        ("employee_cost", "total"): [45182, 43031, 42129],
        ("subcontracting_cost", "total"): [10900, 11154, 9779],
        ("segment_revenue", "IT"): [81895, 79648, 71571],
        ("segment_revenue", "BPO"): [7542, 6650, 6189]}),
    "Q4-Fy19-Consolidated-Results.pdf": ("Q4FY19", 1.0, {
        ("revenue", "total"): [88923, 89437, 80545],
        ("employee_cost", "total"): [43071, 45182, 41453],
        ("subcontracting_cost", "total"): [11739, 10900, 10639],
        ("segment_revenue", "IT"): [81077, 81895, 74637],
        ("segment_revenue", "BPO"): [7846, 7542, 5908]}),
    "Q2-FY20-Consol-Results.pdf": ("Q2FY20", 1.0, {
        ("revenue", "total"): [90699, 86530, 86298],
        ("employee_cost", "total"): [47057, 45009, 43031],
        ("subcontracting_cost", "total"): [13687, 12197, 11154],
        ("segment_revenue", "IT"): [82245, 78572, 79648],
        ("segment_revenue", "BPO"): [8454, 7958, 6650]}),
    "tml-q1-fy-26-consolidated-results.pdf": ("Q1FY26", 1.0, {
        ("revenue", "total"): [133512, 133840, 130055],
        ("employee_cost", "total"): [74989, 73623, 73315],
        ("subcontracting_cost", "total"): [13108, 13539, 15065],
        ("segment_revenue", "IT"): [112637, 113276, 108780],
        ("segment_revenue", "BPS"): [20875, 20564, 21275]}),
}
MET_NOTE = {
    "revenue": "Revenue from operations (consolidated)",
    "employee_cost": "Employee benefits expense (consolidated)",
    "subcontracting_cost": "Consolidated subcontracting expense line",
    "segment_revenue": "Primary business segment revenue",
}


def rows(links, doc_date):
    out = []
    url = lambda fn: links[fn][2] if fn in links else BASE_URL + fn
    for q, items in GROWTH.items():
        fn = PR_FILES[q]
        for per, basis, v in items:
            note = "USD revenue growth as stated in press release; hand-entered"
            if q in GROWTH_NOTES and (basis == "cc" or q == "Q4FY19"):
                note += "; " + GROWTH_NOTES[q]
            out.append(row(q, f"revenue_growth_{per}", "total", "total", v, "pct", basis, "quarter", url(fn),
                           f"TechM {q} press release", "Financial highlights for the quarter (USD)", doc_date(q), note))
    for q, (fn, items) in PRES_GROWTH.items():
        for per, basis, v in items:
            out.append(row(q, f"revenue_growth_{per}", "total", "total", v, "pct", basis, "quarter", url(fn),
                           f"TechM {q} earnings presentation", "Financial Highlights slide", doc_date(q),
                           "USD revenue growth as stated in presentation (press release omits cc); hand-entered"))
    for q, basis, v, fn in ANNUAL_GROWTH:
        out.append(row(q, "revenue_growth_yoy", "total", "total", v, "pct", basis, "annual", url(fn),
                       f"TechM {q} press release", "Financial highlights for the year (USD)", doc_date(q),
                       "Full fiscal-year USD revenue growth; hand-entered" + ("; image-only PDF read via OCR" if "FY19" in q else "")))
    for q, metric, dim, dt_, basis, v, pt, fn, qn in TRANSCRIPT:
        out.append(row(q, metric, dim, dt_, v, "pct", basis, pt, url(fn), f"TechM {q} earnings call transcript",
                       "Management remarks (CFO)", doc_date(q), "Disclosed only on earnings call; hand-entered; " + qn))
    for q, dim, v, fn, qn in AI:
        out.append(row(q, "ai_disclosure", dim, "other", v, "pct", "na", "point", url(fn), f"TechM {q} earnings presentation",
                       "Strategic/people highlights slide", doc_date(q),
                       "Workforce AI-enablement statement (not AI revenue/bookings); hand-entered; " + qn))
    for q, v in DIGITAL.items():
        fn = PR_FILES[q]
        out.append(row(q, "revenue_share", "Digital", "service_line", v, "pct", "na", "quarter", url(fn),
                       f"TechM {q} press release", "Financial highlights for the quarter (USD)", doc_date(q),
                       "'Digital revenues ... at X% of Revenues' (company-defined digital; overlaps other segments; disclosed only FY20); hand-entered"))
    for fn, (dq, scale, d) in OCR_RESULTS.items():
        cols = [dq, prev_q(dq), prev_q(dq, 4)]
        for (metric, dim), vals in d.items():
            for c, v in zip(cols, vals):
                if v is None:
                    continue
                note = MET_NOTE[metric]
                if metric == "subcontracting_cost" and dq in ("Q1FY17", "Q2FY17"):
                    note += " (labelled 'Services rendered by Business Associates and Others')"
                if scale != 1.0:
                    note += f"; reported Rs lakh {v:,}; converted to INR mn (/10)"
                note += "; hand-entered from OCR of image-only PDF, visually verified"
                dim_type = "total" if dim == "total" else "service_line"
                out.append(row(c, metric, dim, dim_type, round(v * scale, 1), "INR_mn", "reported", "quarter", url(fn),
                               f"TechM {dq} consolidated financial results (SEBI format)",
                               "Statement of consolidated results / segment information, quarter-ended columns (image PDF)",
                               doc_date(dq), note))
    return out
