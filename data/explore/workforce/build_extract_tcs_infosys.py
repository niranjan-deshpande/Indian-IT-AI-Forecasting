"""Build extract_tcs_infosys.csv: TCS & Infosys workforce seniority / age / fresher data.

All values hand-transcribed from primary documents (annual/integrated reports, ESG databooks,
GRI sustainability reports, company press releases, company-hosted earnings-call transcripts).
Page = physical PDF page index (1-based). Region-by-age tables (Infosys FY16-FY22) are summed here
and the sums checked against the reported totals.
Run: python3 build_extract_tcs_infosys.py
"""
import csv, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extract_tcs_infosys.csv")
rows = []

def add(firm, fy, metric, dim, value, unit, scope, url, doc, page, notes=""):
    rows.append(dict(firm=firm, fiscal_year=fy, metric=metric, dimension=dim, value=value, unit=unit,
                     scope=scope, source_url=url, source_doc=doc, page=page, notes=notes))

# ---------------------------------------------------------------- Infosys URLs
IDB = "https://www.infosys.com/sustainability/documents/infosys-esg-databook-{}.pdf"
ISR = "https://www.infosys.com/sustainability/documents/infosys-sustainability-report-{}.pdf"
IESG = "https://www.infosys.com/sustainability/documents/infosys-esg-report-{}.pdf"
IAR = "https://www.infosys.com/investors/reports-filings/annual-report/annual/documents/infosys-ar-{}.pdf"
ICALL = "https://www.infosys.com/investors/reports-filings/quarterly-results/{}/q4/documents/transcripts/earningscall.pdf"
I = "Infosys"
GRP = "Infosys Group (global, permanent employees)"
AGE = {"lt30": "age_lt30", "30_50": "age_30_50", "gt50": "age_gt50"}
AGENOTE = "Infosys age bands: <=30, 31-50, >50 (>=50 label used from FY22 databook)."

# ---- employees by age (as of Mar 31)
emp_age = [  # fy, lt30, 30_50, gt50, total, doc-year, page, doc type, note
    (2014, 111778, 47405, 1222, 160405, "2015-16", 23, "SR", ""),
    (2015, 120697, 53996, 1372, 176187, "2015-16", 23, "SR", "Bands sum to 176,065 not 176,187; restated in SR 2016-17."),
    (2015, 120714, 54086, 1387, 176187, "2016-17", 24, "SR", "Restated vintage (SR 2016-17)."),
    (2016, 122089, 69952, 2003, 194044, "2015-16", 23, "SR", ""),
    (2017, 126777, 71486, 2101, 200364, "2016-17", 24, "SR", ""),
    (2018, 123291, 78312, 2504, 204107, "2017-18", 62, "SR", ""),
    (2019, 133506, 90698, 3919, 228123, "2019-20", 92, "SR", ""),
    (2020, 138941, 97323, 4536, 240800, "2019-20", 92, "SR", "Excludes new acquisitions Simplus and Stater."),
    (2021, 143803, 109632, 6184, 259619, "2020-21", 19, "DB", ""),
    (2022, 187271, 119211, 7533, 314015, "2021-22", 22, "DB", ""),
    (2023, 204647, 129949, 8638, 343234, "2022-23", 21, "DB", ""),
    (2024, 173626, 134543, 9071, 317240, "2023-24", 20, "DB", ""),
    (2025, 169765, 143794, 10019, 323578, "2024-25", 26, "DB", ""),
    (2026, 166636, 150316, 11642, 328594, "2025-26", 27, "DB", ""),
]
for fy, a, b, c, tot, dy, pg, typ, note in emp_age:
    url = (ISR if typ == "SR" else IDB).format(dy)
    doc = f"Infosys {'Sustainability Report' if typ=='SR' else 'ESG Databook'} {dy}"
    for d, v in zip(["lt30", "30_50", "gt50"], [a, b, c]):
        add(I, fy, "employees_by_age", AGE[d], v, "count", GRP, url, doc, pg, (AGENOTE + " " + note).strip())
    add(I, fy, "employees_total", "total", tot, "count", GRP, url, doc, pg, note)

# ---- headcount by role / job level (as of Mar 31)
ROLE_NOTE = ("Associate/Junior = JL3 and below; Middle = JL4-JL5; Senior = JL6-JL8; Top = title holders/UMR "
             "(definitions per ESG Databook 2021-22 training table).")
roles = [  # fy, {grade: v}, total, doc-year, page, type, note
    (2014, dict(junior=80593, middle=57709, senior=21635, top=468), 160405, "2015-16", 23, "SR", "Reported label 'Associate'."),
    (2015, dict(junior=84219, middle=67451, senior=24015, top=502), 176187, "2015-16", 23, "SR", "Reported label 'Associate'."),
    (2016, dict(junior=92552, middle=74225, senior=26634, top=633), 194044, "2015-16", 23, "SR", "Reported label 'Associate'."),
    (2017, dict(junior=91701, middle=80815, senior=27102, top=746), 200364, "2016-17", 23, "SR", "Reported label 'Associate'."),
    (2018, dict(junior=88099, middle=88056, senior=27047, top=905), 204107, "2017-18", 61, "SR", "Reported label 'Associate'."),
    (2019, dict(junior=86558, middle=110502, senior=30092, top=971), 228123, "2018-19", 62, "SR", "Reported label 'Associate'. Middle +22k YoY while Associate flat: check for JL re-mapping."),
    (2020, dict(junior=94584, middle=115277, senior=30013, top=926), 240800, "2019-20", 91, "SR", "Reported label 'Associate'. Excludes Simplus and Stater."),
    (2021, dict(junior=104536, middle=122451, senior=30634, top=965), 258586, "2020-21", 18, "DB", "Reported label 'Associate'. Excludes Stater."),
    (2022, dict(junior=145406, middle=130943, senior=35546, top=1101), 312996, "2021-22", 21, "DB", "Reported label 'Associate'. Excludes Stater."),
    (2022, dict(junior=145406, middle=131962, senior=36647), 314015, "2023-24", 20, "DB", "Restated vintage: Senior includes Top; includes Stater (Middle +1,019)."),
    (2023, dict(junior=157913, middle=141826, senior=42171), 341910, "2022-23", 20, "DB", "Senior includes Top from this databook onward."),
    (2023, dict(junior=157913, middle=143150, senior=42171), 343234, "2023-24", 20, "DB", "Restated vintage (Middle +1,324; total now equals group headcount)."),
    (2024, dict(junior=130304, middle=143709, senior=43227), 317240, "2023-24", 20, "DB", "Senior includes Top."),
    (2025, dict(junior=114735, middle=162064, senior=46779), 323578, "2024-25", 26, "DB", "Senior includes Top."),
    (2026, dict(junior=98703, middle=179657, senior=50234), 328594, "2025-26", 26, "DB", "Senior includes Top."),
]
for fy, g, tot, dy, pg, typ, note in roles:
    url = (ISR if typ == "SR" else IDB).format(dy)
    doc = f"Infosys {'Sustainability Report' if typ=='SR' else 'ESG Databook'} {dy}"
    assert sum(g.values()) == tot, (fy, sum(g.values()), tot)
    for k, v in g.items():
        add(I, fy, "headcount_by_grade", f"grade_{k}", v, "count", GRP, url, doc, pg, ROLE_NOTE + " " + note)

# ---- hires & turnover by age x region x gender (FY16-FY22), summed here
# each entry: {age: [(men, women) for Americas, APAC, EMEA, India]}
reg = {
 ("hires", 2016): ("2015-16", 24, "SR", 52545, {
    "lt30": [(1041, 608), (1533, 1190), (466, 544), (22074, 15639)],
    "30_50": [(1558, 610), (899, 378), (683, 274), (3536, 931)],
    "gt50": [(319, 71), (24, 14), (101, 37), (13, 2)]}),
 ("turn", 2016): ("2015-16", "24-25", "SR", 34688, {
    "lt30": [(405, 275), (919, 866), (376, 414), (13410, 9260)],
    "30_50": [(849, 316), (661, 334), (553, 276), (4032, 1393)],
    "gt50": [(191, 49), (17, 8), (49, 13), (20, 2)]}),
 ("hires", 2017): ("2016-17", 24, "SR", 44235, {
    "lt30": [(689, 441), (1573, 1184), (604, 551), (18068, 13485)],
    "30_50": [(1052, 590), (807, 367), (641, 282), (2687, 752)],
    "gt50": [(239, 55), (40, 13), (91, 16), (8, 0)]}),
 ("turn", 2017): ("2016-17", "24-25", "SR", 37915, {
    "lt30": [(479, 338), (1084, 969), (367, 362), (13863, 9998)],
    "30_50": [(981, 492), (756, 363), (656, 322), (4748, 1639)],
    "gt50": [(254, 75), (24, 18), (79, 25), (20, 3)]}),
 ("hires", 2018): ("2017-18", 62, "SR", 44110, {
    "lt30": [(1170, 521), (548, 730), (516, 501), (18465, 12684)],
    "30_50": [(1525, 836), (483, 263), (625, 281), (3344, 880)],
    "gt50": [(522, 97), (19, 8), (66, 11), (13, 2)]}),
 ("turn", 2018): ("2017-18", 63, "SR", 40367, {
    "lt30": [(523, 347), (1088, 877), (401, 452), (14528, 10364)],
    "30_50": [(1157, 536), (965, 442), (672, 332), (5165, 1895)],
    "gt50": [(359, 61), (28, 12), (96, 34), (29, 4)]}),
 ("hires", 2019): ("2019-20", 92, "SR", None, {
    "lt30": [(1907, 1008), (1094, 1001), (736, 536), (27681, 20324)],
    "30_50": [(2932, 1784), (1096, 586), (1107, 499), (4946, 1434)],
    "gt50": [(1117, 274), (63, 19), (173, 57), (25, 2)]}),
 ("turn", 2019): ("2019-20", 92, "SR", None, {
    "lt30": [(780, 361), (764, 794), (367, 393), (17498, 12288)],
    "30_50": [(1476, 731), (798, 512), (605, 376), (5849, 2040)],
    "gt50": [(441, 88), (38, 10), (119, 25), (31, 2)]}),
 ("hires", 2020): ("2019-20", 92, "SR", None, {
    "lt30": [(2349, 1029), (776, 801), (1405, 1241), (23749, 19287)],
    "30_50": [(1952, 1360), (784, 432), (1099, 674), (3679, 1232)],
    "gt50": [(641, 167), (74, 33), (152, 69), (22, 2)]}),
 ("turn", 2020): ("2019-20", 92, "SR", None, {
    "lt30": [(1161, 615), (505, 569), (618, 528), (17209, 12556)],
    "30_50": [(1976, 1122), (776, 396), (737, 459), (7462, 2501)],
    "gt50": [(691, 146), (46, 9), (126, 35), (77, 12)]}),
 ("hires", 2021): ("2020-21", 19, "DB", None, {
    "lt30": [(2228, 1255), (580, 487), (1116, 1014), (18048, 14283)],
    "30_50": [(2701, 2046), (891, 471), (1047, 654), (2949, 917)],
    "gt50": [(765, 395), (56, 15), (149, 52), (15, 3)]}),
 ("turn", 2021): ("2020-21", 19, "DB", None, {
    "lt30": [(1207, 590), (582, 491), (831, 727), (10473, 7023)],
    "30_50": [(1536, 1166), (774, 436), (689, 480), (5096, 1815)],
    "gt50": [(567, 146), (47, 16), (92, 46), (52, 7)]}),
 ("hires", 2022): ("2021-22", 22, "DB", 141556, {
    "lt30": [(3745, 1880), (1565, 1394), (1892, 1548), (58278, 41463)],
    "30_50": [(4161, 3598), (2116, 1386), (1524, 1206), (9872, 4111)],
    "gt50": [(865, 267), (149, 46), (277, 125), (75, 13)]}),
 ("turn", 2022): ("2021-22", 22, "DB", None, {
    "lt30": [(2161, 1127), (732, 743), (1550, 1404), (27883, 19568)],
    "30_50": [(2963, 2200), (1371, 797), (1317, 1042), (15245, 5659)],
    "gt50": [(690, 234), (64, 28), (194, 106), (76, 6)]}),
}
for (kind, fy), (dy, pg, typ, chk, tab) in reg.items():
    url = (ISR if typ == "SR" else IDB).format(dy)
    doc = f"Infosys {'Sustainability Report' if typ=='SR' else 'ESG Databook'} {dy}"
    metric = "new_hires_by_age" if kind == "hires" else "turnover_by_age"
    tmetric = "new_hires_total" if kind == "hires" else "turnover_total"
    base = ("Computed: sum of reported age x region (Americas/APAC/EMEA/India) x gender cells. "
            + ("Reported 'rate' columns in source are shares of total hires/turnover, not rates; not recorded. "))
    if kind == "turn":
        base += ("Total (voluntary+involuntary presumably) turnover - NOT the voluntary IT-services series used from FY22 onward in later databooks. ")
    if fy == 2021:
        base += "ESG Databook 2021-22 repeats FY21 with >=50 men/women hire cells swapped (totals unchanged). "
    grand = 0
    for age, cells in tab.items():
        m = sum(c[0] for c in cells); w = sum(c[1] for c in cells); t = m + w; grand += t
        add(I, fy, metric, AGE[age], t, "count", GRP, url, doc, pg, base + AGENOTE)
        add(I, fy, metric, AGE[age] + "_male", m, "count", GRP, url, doc, pg, base)
        add(I, fy, metric, AGE[age] + "_female", w, "count", GRP, url, doc, pg, base)
    if chk is not None:
        assert grand == chk, (kind, fy, grand, chk)
    add(I, fy, tmetric, "total", grand, "count", GRP, url, doc, pg,
        base + (f"Matches reported total {chk:,}." if chk else "Reported total not printed; sum of cells."))

# ---- hires by age FY22-FY26 (direct age totals in databook)
hires = [  # fy, lt30, 30_50, gt50, total, men, women, dy, page
    (2022, 111765, 27974, 1817, 141556, 84519, 57037, "2022-23", 21),
    (2023, 84085, 29179, 1588, 114852, 70919, 43933, "2022-23", 21),
    (2024, 22304, 13831, 947, 37082, 23699, 13383, "2023-24", 21),
    (2025, 50606, 20445, 1162, 72213, 45018, 27195, "2024-25", 27),
    (2026, 53937, 17983, 1592, 73512, 44004, 29508, "2025-26", 31),
]
for fy, a, b, c, tot, m, w, dy, pg in hires:
    url, doc = IDB.format(dy), f"Infosys ESG Databook {dy}"
    assert a + b + c == tot and m + w == tot
    n = "Permanent employees. " + AGENOTE
    for d, v in zip(["lt30", "30_50", "gt50"], [a, b, c]):
        add(I, fy, "new_hires_by_age", AGE[d], v, "count", GRP, url, doc, pg, n)
    add(I, fy, "new_hires_total", "total", tot, "count", GRP, url, doc, pg, n)
    add(I, fy, "new_hires_total", "male", m, "count", GRP, url, doc, pg, n)
    add(I, fy, "new_hires_total", "female", w, "count", GRP, url, doc, pg, n)

# ---- voluntary turnover by age x gender FY22-FY26 (count + rate)
turn = [  # fy, {age: (m, m_rate, w, w_rate, total)}, total tuple, dy, page
    (2022, {"lt30": (23043, 32.4, 15489, 26.5, 38532), "30_50": (15414, 25.0, 6197, 25.5, 21611),
            "gt50": (627, 16.9, 133, 16.9, 760)}, (39084, 28.7, 21819, 26.1, 60903), "2022-23", 22),
    (2023, {"lt30": (18803, 21.8, 14008, 20.7, 32811), "30_50": (13433, 20.6, 5762, 20.4, 19195),
            "gt50": (646, 14.5, 137, 14.9, 783)}, (32882, 21.1, 19907, 20.6, 52789), "2022-23", 22),
    (2024, {"lt30": (11586, 14.1, 8330, 13.2, 19916), "30_50": (7589, 11.2, 3438, 11.2, 11027),
            "gt50": (443, 9.1, 95, 9.7, 538)}, (19618, 12.6, 11863, 12.5, 31481), "2023-24", 22),
    (2025, {"lt30": (12902, 17.6, 8429, 14.9, 21331), "30_50": (8263, 11.7, 3779, 11.4, 12042),
            "gt50": (456, 8.7, 105, 10.4, 561)}, (21621, 14.5, 12313, 13.6, 33934), "2024-25", 28),
    (2026, {"lt30": (12657, 17.6, 7394, 13.4, 20051), "30_50": (6978, 9.3, 3258, 9.0, 10236),
            "gt50": (473, 7.8, 86, 7.6, 559)}, (20108, 13.2, 10738, 11.6, 30846), "2025-26", 32),
]
for fy, tab, (tm, tmr, tw, twr, tt), dy, pg in turn:
    url, doc = IDB.format(dy), f"Infosys ESG Databook {dy}"
    n = ("Voluntary attrition, LTM, IT services (per table note); permanent employees. Rates reported only by "
         "gender within age band (denominator not stated). " + AGENOTE)
    if fy == 2022:
        n += " ESG Databook 2021-22 reports a different (larger, total-turnover) FY22 series; see those rows."
    for age, (m, mr, w, wr, t) in tab.items():
        assert m + w == t
        add(I, fy, "turnover_by_age", AGE[age], t, "count", GRP, url, doc, pg, n)
        add(I, fy, "turnover_by_age", AGE[age] + "_male", m, "count", GRP, url, doc, pg, n)
        add(I, fy, "turnover_by_age", AGE[age] + "_female", w, "count", GRP, url, doc, pg, n)
        add(I, fy, "turnover_rate_by_age", AGE[age] + "_male", mr, "pct", GRP, url, doc, pg, n)
        add(I, fy, "turnover_rate_by_age", AGE[age] + "_female", wr, "pct", GRP, url, doc, pg, n)
    add(I, fy, "turnover_total", "total", tt, "count", GRP, url, doc, pg, n)
    add(I, fy, "turnover_total", "male_rate", tmr, "pct", GRP, url, doc, pg, n)
    add(I, fy, "turnover_total", "female_rate", twr, "pct", GRP, url, doc, pg, n)

# role-wise share of turnover FY21/FY22
for fy, vals in [(2022, dict(junior=40.74, middle=52.20, senior=6.89, top=0.11)),
                 (2021, dict(junior=44.20, middle=47.58, senior=7.99, top=0.17))]:
    for k, v in vals.items():
        add(I, fy, "other", f"turnover_share_grade_{k}", v, "pct", GRP + ", excl. Stater", IDB.format("2021-22"),
            "Infosys ESG Databook 2021-22", 23,
            "Reported as 'Role wise employee turnover rate' but values sum to ~100%: share of total turnover by role (Associate=junior).")

# ---- BRSR turnover rates (permanent employees)
brsr = [  # fy, male, female, total, AR yy, page, note
    (2020, 17.6, 17.0, 17.4, "22", 301, "Prior-year column in BRSR FY22 (voluntary BRSR year)."),
    (2021, 11.3, 10.2, 10.9, "22", 301, "Prior-year column in BRSR FY22."),
    (2022, 28.7, 26.1, 27.7, "22", 301, ""),
    (2023, 21.1, 20.6, 20.9, "23", 137, ""),
    (2024, 12.6, 12.5, 12.6, "24", 133, ""),
    (2025, 14.5, 13.6, 14.1, "25", 135, "BRSR Core basis (per footnote)."),
    (2026, 13.2, 11.6, 12.6, "26", 144, ""),
]
for fy, m, w, t, yy, pg, note in brsr:
    for d, v in [("male_rate", m), ("female_rate", w), ("total_rate", t)]:
        add(I, fy, "turnover_total", d, v, "pct", "Infosys Group permanent employees (BRSR)", IAR.format(yy),
            f"Infosys Integrated Annual Report FY20{yy} - BRSR Q22/Q20", pg,
            ("BRSR turnover rate; matches databook voluntary IT-services LTM series where overlapping. " + note).strip())

# ---- fresher / campus hires
fr = [  # fy, metric, dim, value, url, doc, page, scope, note
    (2016, "fresher_hires", "total", 16000, ISR.format("2015-16"), "Infosys Sustainability Report 2015-16", 28, "Infosys Ltd (Foundation Program, Mysuru)",
     "'about 16,000 freshers were trained' in FY16 Foundation Program; proxy for campus joiners (trained, not hired, count)."),
    (2017, "fresher_hires", "total", 12430, ISR.format("2016-17"), "Infosys Sustainability Report 2016-17", 27, "Infosys Ltd (Foundation Program, Mysuru)",
     "'about 12,430 freshers were trained'; proxy for campus joiners."),
    (2018, "fresher_hires", "total", 8934, ISR.format("2017-18"), "Infosys Sustainability Report 2017-18", 28, "Infosys Ltd (Foundation Program)",
     "'8,934 freshers were trained'; proxy for campus joiners."),
    (2019, "fresher_hires", "total", 18435, ISR.format("2018-19"), "Infosys Sustainability Report 2018-19", 26, "Infosys Ltd (Foundation Program)",
     "'About 18,435 freshers were trained in fiscal 2019'; proxy for campus joiners."),
    (2019, "fresher_hires", "total", 21500, IAR.format("19"), "Infosys Annual Report 2018-19 (CEO letter)", 17, "Infosys Group, global",
     "'over 1,500 college graduates outside India and more than 20,000 college graduates in India'; lower bound, sum of the two."),
    (2021, "fresher_hires", "total", 20000, ICALL.format("2020-2021"), "Infosys Q4 FY21 earnings call transcript", 9, "Infosys, global",
     "'recruited over 20,000 people from campus in FY21'; lower bound."),
    (2022, "fresher_hires", "total", 84782, IAR.format("22"), "Infosys Integrated Annual Report 2021-22 (Business highlights)", 21, "Infosys Group, global",
     "'Fresh college graduates hired globally 84,782'. Q4 FY22 call says 'recruited 85,000 college graduates' (p4)."),
    (2023, "fresher_hires", "total", 50000, IAR.format("23"), "Infosys Integrated Annual Report 2022-23", 22, "Infosys Group, global",
     "'~50,000 Fresh graduates hired globally'; CEO letter p17 'over 50,000'; ESG Report 2022-23 p26 'hired 50,000 freshers'. Approximate."),
    (2024, "fresher_hires", "total", 11900, IAR.format("24"), "Infosys Integrated Annual Report 2023-24", 21, "Infosys Group, global",
     "'11,900+ Fresh graduates hired globally'; CEO letter p17 'nearly 11,900'. Approximate."),
    (2025, "fresher_hires", "total", 15288, IAR.format("25"), "Infosys Integrated Annual Report 2024-25", 22, "Infosys Group, global",
     "'15,288 Fresh graduates hired globally'; Q4 FY25 call p6 'hired 15,000 freshers'."),
    (2026, "fresher_hires", "total", 20000, IAR.format("26"), "Infosys Integrated Annual Report 2025-26", 25, "Infosys Group, global",
     "'20,000+ Fresh graduates hired globally'; Q4 FY26 call p5 'onboarded more than 20,000 freshers'. Lower bound."),
    (2026, "other", "fresh_grads_completed_GEC_training", 10766, IAR.format("26"), "Infosys Integrated Annual Report 2025-26", 85, "Infosys, GEC Mysuru",
     "'10,766 fresh graduates completed the training at GEC Mysuru and were released to delivery units' in FY26."),
    # fresh graduates hired locally outside India
    (2020, "fresher_hires", "outside_india_local", 2035, IAR.format("20"), "Infosys Annual Report 2019-20", 72, "Infosys, local hires in overseas markets",
     "'recruited 6,932 employees locally in our markets, of which 2,035 were fresh graduates'."),
    (2021, "fresher_hires", "outside_india_local", 1941, IAR.format("21"), "Infosys Integrated Annual Report 2020-21", 57, "Infosys, local hires in overseas markets",
     "'over 7,280 employees locally ... of which 1,941 were fresh graduates'."),
    (2022, "fresher_hires", "outside_india_local", 3650, IAR.format("22"), "Infosys Integrated Annual Report 2021-22", 20, "Infosys, local hires in overseas markets",
     "'over 14,805 employees locally ... of which 3,650 were fresh graduates'."),
    (2023, "fresher_hires", "outside_india_local", 2216, IAR.format("23"), "Infosys Integrated Annual Report 2022-23", 21, "Infosys, local hires in overseas markets",
     "'over 10,169 employees locally ... of which 2,216 were fresh graduates'."),
    # POSH onboarding coverage (proxy only)
    (2021, "other", "freshers_covered_onboarding_POSH", 19000, IAR.format("21"), "Infosys Integrated Annual Report 2020-21 (BRR)", 279, "Infosys Ltd (India)",
     "'Mandatory onboarding sessions for new hires covering approximately 20,000+ laterals and 19,000+ freshers'; proxy for fresher joiners."),
    (2023, "other", "freshers_covered_onboarding_POSH", 29640, IDB.format("2022-23"), "Infosys ESG Databook 2022-23", 23, "Infosys Ltd (India)",
     "'approx. 50116 laterals and 29640 freshers covered through the year' in mandatory onboarding sessions; much lower than ~50,000 freshers hired claim."),
]
for fy, metric, dim, v, url, doc, pg, scope, note in fr:
    add(I, fy, metric, dim, v, "count", scope, url, doc, pg, note)

# ================================================================ TCS
T = "TCS"
TAR = "https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/{}/ar/annual-report-{}.pdf"
TAR26 = "https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2025-26/ar/annual-report-2025-2026.pdf"
TSR = "https://www.tcs.com/content/dam/global-tcs/en/pdfs/who-we-are/sustainability-reports/{}.pdf"
TPR = "https://www.tcs.com/who-we-are/newsroom/press-release/tcs-financial-results-q4-fy-{}"
def tar(fy):
    a, b = fy - 1, fy
    return TAR.format(f"{a}-{str(b)[2:]}", f"{a}-{b}")

CHART = "Read from infographic labels (male+female summed); values are % of India employees."
# ---- employees by age, % (TCS)
tcs_age = [  # fy, {dim: pct}, url, doc, page, scope, note
    (2016, dict(age_lt30=59.5, age_30_50=38.8, age_30_40=32.7, age_40_50=6.1, age_gt50=1.7), TSR.format("GRI-2016-Sustainability-Report"),
     "TCS Corporate Sustainability Report 2015-16 (Exhibit 15)", 39, "TCS incl. subsidiaries, global (353,843)", "Pie chart labels by age x gender, summed."),
    (2017, dict(age_lt30=65.7, age_30_50=33.7, age_gt50=0.6), TSR.format("GRI-Sustainability-Report-2016-2017"),
     "TCS Corporate Sustainability Report 2016-17 (Exhibit 5)", 23, "TCS, India region only", CHART + " Other regions charted separately."),
    (2020, dict(age_lt30=52.0, age_30_50=47.0, age_30_40=39.0, age_40_50=8.0, age_gt50=1.0), tar(2020),
     "TCS Annual Report 2019-20 (MD&A)", 86, "TCS, India region only", CHART + " Whole-% labels; M/F label placement ambiguous but band sums robust."),
    (2021, dict(age_lt30=56.0, age_30_50=43.0, age_30_40=36.0, age_40_50=7.0, age_gt50=1.1), tar(2021),
     "TCS Integrated Annual Report 2020-21 (MD&A)", 108, "TCS, India region only", CHART),
    (2022, dict(age_lt30=59.0, age_30_50=40.0, age_30_40=33.0, age_40_50=7.0, age_gt50=1.1), tar(2022),
     "TCS Integrated Annual Report 2021-22 (Human Capital)", 22, "TCS, India region only", CHART),
    (2023, dict(age_lt30=52.9, age_30_50=46.0, age_30_40=37.3, age_40_50=8.7, age_gt50=1.1), tar(2023),
     "TCS Integrated Annual Report 2022-23 (Human Capital)", 18, "TCS, India region only", CHART),
    (2024, dict(age_lt30=50.3, age_30_50=48.4, age_30_40=35.8, age_40_50=12.6, age_gt50=1.3), tar(2024),
     "TCS Integrated Annual Report 2023-24 (Human Capital)", 18, "TCS, India region only", CHART),
    (2025, dict(age_lt30=47.7, age_30_50=50.8, age_30_40=38.9, age_40_50=11.9, age_gt50=1.5), tar(2025),
     "TCS Integrated Annual Report 2024-25 (MD&A)", 85, "TCS, India region only", CHART),
]
for fy, d, url, doc, pg, scope, note in tcs_age:
    for k, v in d.items():
        add(T, fy, "employees_by_age", k, v, "pct", scope, url, doc, pg, note + " TCS bands: <30, 30-40, 40-50, >50.")

# ---- new hires & turnover by age, % (TCS)
add(T, 2016, "new_hires_by_age", "age_lt30", 81.7, "pct", "TCS incl. subsidiaries, global", TSR.format("GRI-2016-Sustainability-Report"),
    "TCS Corporate Sustainability Report 2015-16 (Exhibit 19)", 42, "Share of FY16 gross hires (90,182); pie labels summed (M49.2+F32.5).")
add(T, 2016, "new_hires_by_age", "age_30_50", 17.1, "pct", "TCS incl. subsidiaries, global", TSR.format("GRI-2016-Sustainability-Report"),
    "TCS Corporate Sustainability Report 2015-16 (Exhibit 19)", 42, "30-40: 14.6, 40-50: 2.5.")
add(T, 2016, "new_hires_by_age", "age_gt50", 1.2, "pct", "TCS incl. subsidiaries, global", TSR.format("GRI-2016-Sustainability-Report"),
    "TCS Corporate Sustainability Report 2015-16 (Exhibit 19)", 42, "")
for k, v in dict(age_lt30=65.0, age_30_40=29.0, age_40_50=4.0, age_gt50=2.0).items():
    add(T, 2016, "turnover_by_age", k, v, "pct", "TCS incl. subsidiaries, global", TSR.format("GRI-2016-Sustainability-Report"),
        "TCS Corporate Sustainability Report 2015-16 (Exhibit 24A)", 45,
        "Chart subtitled '(out of employee base in age group)' but values sum to 100%: most likely share of departures by age.")
for k, v in dict(age_lt30=91.2, age_30_50=8.7, age_gt50=0.0).items():
    add(T, 2017, "new_hires_by_age", k, v, "pct", "TCS, India region only (67,328 India hires)", TSR.format("GRI-Sustainability-Report-2016-2017"),
        "TCS Corporate Sustainability Report 2016-17 (Exhibit 6)", 24, "Share of India new hires; chart labels M+F summed.")
for k, v in dict(age_lt30=69.4, age_30_50=30.1, age_gt50=0.5).items():
    add(T, 2017, "turnover_by_age", k, v, "pct", "TCS, India region only", TSR.format("GRI-Sustainability-Report-2016-2017"),
        "TCS Corporate Sustainability Report 2016-17 (Exhibit 8)", 28, "Share of India separations; chart labels M+F summed.")

# ---- totals
add(T, 2016, "new_hires_total", "total", 90182, "count", "TCS incl. subsidiaries, global", TSR.format("GRI-2016-Sustainability-Report"),
    "TCS Corporate Sustainability Report 2015-16", 41, "Gross recruits FY16 (FY15: 67,123).")
add(T, 2017, "new_hires_total", "total", 78912, "count", "TCS, global", TSR.format("GRI-Sustainability-Report-2016-2017"),
    "TCS Corporate Sustainability Report 2016-17", 24, "'hired and integrated 78,912 employees - 67,328 in India and 11,584 outside'.")
add(T, 2018, "new_hires_total", "total", 52746, "count", "TCS, global", TSR.format("GRI-Sustainability-Report-2017-2018"),
    "TCS Corporate Sustainability Report 2017-18", 8, "'New hires for the year / Gross Headcount Addition'.")
emp = [(2016, 353843, TSR.format("GRI-2016-Sustainability-Report"), "TCS Corporate Sustainability Report 2015-16", 39),
       (2017, 387223, TSR.format("GRI-Sustainability-Report-2016-2017"), "TCS Corporate Sustainability Report 2016-17", 22),
       (2018, 394998, TSR.format("GRI-Sustainability-Report-2017-2018"), "TCS Corporate Sustainability Report 2017-18", 27)]
emp += [(fy, v, TPR.format(fy), f"TCS Q4 FY{fy} results press release", "html")
        for fy, v in [(2019, 424285), (2020, 448464), (2021, 488649), (2022, 592195), (2023, 614795),
                      (2024, 601546), (2025, 607979), (2026, 584519)]]
for fy, v, url, doc, pg in emp:
    add(T, fy, "employees_total", "total", v, "count", "TCS consolidated, global", url, doc, pg, "Headcount as of Mar 31.")

add(T, 2016, "headcount_by_grade", "grade_junior", 52.2, "pct", "TCS incl. subsidiaries, global", TSR.format("GRI-2016-Sustainability-Report"),
    "TCS Corporate Sustainability Report 2015-16 (Exhibit 14)", 39, "Pie labels: Junior M30.6 + F21.6. Only year TCS gives workforce split by category.")
add(T, 2016, "headcount_by_grade", "grade_middle", 43.2, "pct", "TCS incl. subsidiaries, global", TSR.format("GRI-2016-Sustainability-Report"),
    "TCS Corporate Sustainability Report 2015-16 (Exhibit 14)", 39, "Mid-level M31.6 + F11.6.")
add(T, 2016, "headcount_by_grade", "grade_senior", 4.6, "pct", "TCS incl. subsidiaries, global", TSR.format("GRI-2016-Sustainability-Report"),
    "TCS Corporate Sustainability Report 2015-16 (Exhibit 14)", 39, "Senior M4.1 + F0.5.")
add(T, 2016, "other", "attrition_rate_junior_level", 16.4, "pct", "TCS, global", TSR.format("GRI-2016-Sustainability-Report"),
    "TCS Corporate Sustainability Report 2015-16", 45, "'attrition rate is higher at junior levels - 16.4%' vs IT services 14.7%, overall 15.5%.")

for fy, v, url, doc, pg in [
        (2016, 29.5, TSR.format("GRI-2016-Sustainability-Report"), "TCS Corporate Sustainability Report 2015-16", 39),
        (2017, 29.7, TSR.format("GRI-Sustainability-Report-2016-2017"), "TCS Corporate Sustainability Report 2016-17", 22),
        (2018, 30.2, TSR.format("GRI-Sustainability-Report-2017-2018"), "TCS Corporate Sustainability Report 2017-18", 27),
        (2019, 30.7, TSR.format("GRI-Sustainability-Report-2018-2019"), "TCS Corporate Sustainability Report 2018-19", 24),
        (2020, 31.0, tar(2020), "TCS Annual Report 2019-20 (MD&A infographic)", 85)]:
    add(T, fy, "avg_age", "total", v, "count", "TCS incl. subsidiaries, global", url, doc, pg, "Unit = years. Not disclosed after FY20.")
for fy, v, pg in [(2022, 88, 22), (2023, 88, 18), (2024, 89, 18)]:
    add(T, fy, "other", "millennials_share", v, "pct", "TCS, global", tar(fy), f"TCS Integrated Annual Report {fy-1}-{str(fy)[2:]}", pg,
        "'3 Generations, X% Millennials' infographic.")

# ---- TCS fresher hires
tf = [
    (2016, "fresher_hires", "total", 34365, TSR.format("GRI-2016-Sustainability-Report"), "TCS Corporate Sustainability Report 2015-16", 41,
     "TCS incl. subsidiaries, global", "'Of this [90,182 gross recruits], 34,365 (38%) were graduates fresh out of college'."),
    (2020, "fresher_hires", "total", 30000, tar(2020), "TCS Annual Report 2019-20 (MD&A)", 88, "TCS, campus recruits (India)",
     "'onboarded all campus recruits, adding up to over 30,000 trainees, in just the first two quarters' of FY20; lower bound for FY20."),
    (2021, "other", "freshers_onboarded_FY20_FY21_cumulative", 60000, tar(2021), "TCS Integrated Annual Report 2020-21 (Chairman letter)", 13,
     "TCS", "'onboarding over 60,000 freshers over the last couple of years' (approx. FY20+FY21 cumulative)."),
    (2022, "fresher_hires", "total", 100000, tar(2022), "TCS Integrated Annual Report 2021-22 (MD&A)", 114, "TCS, India",
     "'India Freshers Training: Over 100,000 trainees were onboarded during the year'; also p23 '100,000+ trainees onboarded'; Q4FY22 call p16 'about 100,000 people who were freshers'."),
    (2022, "fresher_hires", "total", 118000, tar(2022), "TCS Integrated Annual Report 2021-22 (Chairman Q&A)", 42, "TCS",
     "'training and onboarding 118,000 fresh engineers in FY 2022' - inconsistent with 100,000+ elsewhere in same report and 110,000 in FY23 report."),
    (2022, "fresher_hires", "total", 110000, tar(2023), "TCS Integrated Annual Report 2022-23 (Letter to Shareholders)", 9, "TCS",
     "Later vintage: 'over 110,000 in FY 2022'."),
    (2023, "fresher_hires", "total", 44000, tar(2023), "TCS Integrated Annual Report 2022-23 (MD&A)", 89, "TCS",
     "'about 44,000 fresh engineers'; letter p9 'over 44,000 in FY 2023'; Q4FY23 press release 'onboarded over 44K freshers'."),
    (2025, "fresher_hires", "total", 42000, TPR.format(2025), "TCS Q4 FY2025 results press release (CHRO quote)", "html", "TCS",
     "'Our trainee onboarding in FY25 was 42,000 as planned'."),
    (2026, "fresher_hires", "total", 44000, TAR26, "TCS Integrated Annual Report 2025-26 (MD&A)", 55, "TCS",
     "'In FY 2026, the Company hired over 44,000 freshers' (lower bound). FY26 also had a 'reskilling and restructuring program'."),
]
for fy, metric, dim, v, url, doc, pg, scope, note in tf:
    add(T, fy, metric, dim, v, "count", scope, url, doc, pg, note)

# ---- TCS BRSR turnover rates
tb = [  # fy, m, f, t, url, doc, page, note
    (2020, 12.8, 14.2, 13.3, tar(2022), "TCS Integrated Annual Report 2021-22 - BRSR Q20", 189, "Global headcount incl. IT and business services, excl. non-wholly-owned subs (prior-year column)."),
    (2021, 7.5, 7.5, 7.5, tar(2022), "TCS Integrated Annual Report 2021-22 - BRSR Q20", 189, "Same basis as above (prior-year column)."),
    (2022, 17.3, 17.8, 17.5, tar(2022), "TCS Integrated Annual Report 2021-22 - BRSR Q20", 189, "Global incl. IT & BS, excl. non-wholly-owned subs."),
    (2022, 17.3, 17.7, 17.4, tar(2024), "TCS Integrated Annual Report 2023-24 - BRSR Q22", 129, "Restated vintage: LTM IT services basis."),
    (2023, 20.9, 21.9, 21.3, tar(2023), "TCS Integrated Annual Report 2022-23 - BRSR Q20", 148, "Global headcount excl. non-wholly-owned subs."),
    (2023, 20.2, 20.1, 20.2, tar(2024), "TCS Integrated Annual Report 2023-24 - BRSR Q22", 129, "Restated vintage: LTM IT services basis."),
    (2024, 12.5, 12.5, 12.5, tar(2024), "TCS Integrated Annual Report 2023-24 - BRSR Q22", 129, "LTM IT services."),
    (2025, 13.2, 13.6, 13.3, tar(2025), "TCS Integrated Annual Report 2024-25 - BRSR Q22", 131, "LTM IT services."),
    (2026, 13.8, 13.4, 13.7, TAR26, "TCS Integrated Annual Report 2025-26 - BRSR Q22", 108, "Basis changed to LTM VOLUNTARY IT services attrition."),
]
for fy, m, f, t, url, doc, pg, note in tb:
    for d, v in [("male_rate", m), ("female_rate", f), ("total_rate", t)]:
        add(T, fy, "turnover_total", d, v, "pct", "TCS global permanent employees (BRSR)", url, doc, pg, note)

with open(OUT, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(f"wrote {len(rows)} rows -> {OUT}")
