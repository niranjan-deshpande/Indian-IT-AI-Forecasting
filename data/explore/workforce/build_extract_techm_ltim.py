"""Build extract_techm_ltim.csv from hand-transcribed primary-source tables.

Firms: Tech Mahindra (techm); LTIMindtree / LTM Ltd (ltimindtree, FY23+);
pre-merger L&T Infotech (lti) and Mindtree (mindtree).
All figures transcribed from the PDFs listed below (page = physical PDF page index).
Age components are summed across gender columns in code and checked against
reported grand totals where available.
"""
import csv, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extract_techm_ltim.csv")
rows = []

def add(firm, fy, metric, dim, val, unit, scope, url, doc, page, notes=""):
    rows.append(dict(firm=firm, fiscal_year=fy, metric=metric, dimension=dim, value=val,
                     unit=unit, scope=scope, source_url=url, source_doc=doc, page=page, notes=notes))

def ages(firm, fy, metric, vals, unit, scope, url, doc, page, notes="", dims=("age_lt30", "age_30_50", "age_gt50")):
    for d, v in zip(dims, vals):
        add(firm, fy, metric, d, v, unit, scope, url, doc, page, notes)

# ------------------------------------------------------------------ TECH MAHINDRA
TI = "https://insights.techmahindra.com/investors/"
T = {
    2026: (TI + "tml-integrated-annual-report-fy-2025-26.pdf", "TechM Integrated Annual Report FY2025-26"),
    2025: (TI + "tml-integrated-annual-report-fy-2024-2025.pdf", "TechM Integrated Annual Report FY2024-25"),
    2024: (TI + "tml-integrated-annual-report-fy-2023-2024.pdf", "TechM Integrated Annual Report FY2023-24"),
    2023: (TI + "tml-integrated-annual-report-fy-2022-23.pdf", "TechM Integrated Annual Report FY2022-23"),
    2022: (TI + "tml-integrated-annual-report-fy-2021-22.pdf", "TechM Integrated Annual Report FY2021-22"),
    2021: (TI + "annual-report-20-21.pdf", "TechM Integrated Annual Report FY2020-21"),
    2020: ("https://files.techmahindra.com/static/img/pdf/integrated-report-20.pdf", "TechM Integrated Report FY2019-20"),
    2019: ("https://cache.techmahindra.com/static/img/pdf/Integrated-Report-19.pdf", "TechM Integrated Report FY2018-19"),
    2018: ("https://cache.techmahindra.com/static/img/pdf/Tech-Mahindra-integrated-Report-2017-18.pdf", "TechM Integrated Report FY2017-18"),
}
GL = "global (TechM Ltd + integrated companies; perm+temp full-time incl. fixed-term & third-party contract staff)"
AGE_BANDS_T = "TechM bands: <=30, 31-50, >=51 (FY21-FY23: 18-30, 31-50, 51+)"

# GRI 2-7/102-8 headcount by age: (lt30 components), (30-50), (gt50) as F,M,ND; total; F; M; page; grade dict
techm_hc = {
    2026: ((28396, 37012, 16), (18999, 49429, 11), (1110, 5239, 4), 140216, 48505, 91680, 123,
           {"junior_mgmt": 117276, "middle_mgmt": 12319, "senior_mgmt": 1105, "fixed_term": 5382, "sales": 802, "third_party": 3332}),
    2025: ((28716, 37272, 2), (18308, 49401, 12), (976, 4581, 3), 139271, 48000, 91254, 131,
           {"junior_mgmt": 116770, "middle_mgmt": 12570, "senior_mgmt": 1166, "fixed_term": 4914, "sales": 892, "third_party": 2911, "others": 48}),
    2024: ((25895, 35205, 12), (15750, 46612, 8), (800, 3869, 0), 128151, 42445, 85686, 103,
           {"junior_mgmt": 105489, "middle_mgmt": 12350, "senior_mgmt": 1167, "fixed_term": 4729, "sales": 913, "third_party": 3446, "others": 57}),
    2023: ((26623, 34570, 12), (15332, 45687, 29), (767, 3799, 6), 126825, 42722, 84056, 61,
           {"junior_mgmt": 101552, "middle_mgmt": 12625, "senior_mgmt": 1069, "fixed_term": 6677, "sales": 983, "third_party": 3817, "others": 102}),
    2022: ((28521, 35907, 23), (13512, 43313, 31), (741, 3436, 6), 125490, 42774, 82656, 109,
           {"junior_mgmt": 110771, "middle_mgmt": 13702, "senior_mgmt": 1017}),
    2021: ((21498, 27868, 3), (9662, 37622, 27), (469, 2457, 1), 99607, 31629, 67947, 125,
           {"junior_mgmt": 79212, "middle_mgmt": 11850, "senior_mgmt": 774}),
}
for fy, (a, b, c, tot, f, m, pg, grades) in techm_hc.items():
    url, doc = T[fy]
    v = (sum(a), sum(b), sum(c))
    assert abs(sum(v) - tot) <= 2, (fy, v, tot)
    note = AGE_BANDS_T + ("; FY22 table covers U/P/E bands only (jr/mid/sr mgmt), no FTC/TPC rows" if fy == 2022 else "")
    ages("techm", fy, "employees_by_age", v, "count", GL, url, doc, pg, note)
    add("techm", fy, "employees_total", "total", tot, "count", GL, url, doc, pg, "GRI 2-7/102-8 table grand total; excludes non-employee third-party workers (housekeeping/security)")
    add("techm", fy, "employees_total", "female", f, "count", GL, url, doc, pg)
    add("techm", fy, "employees_total", "male", m, "count", GL, url, doc, pg)
    for g, n in grades.items():
        add("techm", fy, "headcount_by_grade", "grade_" + g, n, "count", GL, url, doc, pg if fy != 2021 else 124,
            "Junior mgmt=U bands, Middle=P bands, Senior=E1+ (per TechM legend); U1/U2 heavily BPO (BSG)")

# earlier TechM vintages (FY18-FY20) - global and India scope
url, doc = T[2020]
ages("techm", 2020, "employees_by_age", (57056, 46217, 3127), "count", GL, url, doc, 129, "bands 18-30/31-50/>50; FY20 Integrated Report")
add("techm", 2020, "employees_total", "total", 106400, "count", GL, url, doc, 129)
for g, n in {"junior_mgmt": 85186, "middle_mgmt": 12844, "senior_mgmt": 834}.items():
    add("techm", 2020, "headcount_by_grade", "grade_" + g, n, "count", GL, url, doc, 129)
ages("techm", 2020, "employees_by_age", (19885 + 28776 + 1, 5573 + 24573, 97 + 797), "count", "Tech Mahindra Ltd India (standalone India employees)", url, doc, 128, "India only; excludes 4,904 third-party")
add("techm", 2020, "employees_total", "total", 79702, "count", "Tech Mahindra Ltd India (standalone India employees)", url, doc, 128)

url, doc = T[2019]
ages("techm", 2019, "employees_by_age", (55575, 41132, 7115), "count", GL, url, doc, 90,
     "bands 18-30/30-50/>50. CONFLICT: same report p99 'Diversity by age' table gives 55,575/45,699/2,548 for same total 103,822")
ages("techm", 2019, "employees_by_age", (55575, 45699, 2548), "count", GL, url, doc, 99,
     "alternate table in same report (GRI 405-1); differs from p90 in 30-50 vs >50 split")
add("techm", 2019, "employees_total", "total", 103822, "count", GL, url, doc, 90)
for g, n in {"junior_mgmt": 83263, "middle_mgmt": 12885, "senior_mgmt": 716}.items():
    add("techm", 2019, "headcount_by_grade", "grade_" + g, n, "count", GL, url, doc, 90)
ages("techm", 2019, "employees_by_age", (19469 + 28458, 4700 + 22222, 946 + 3237), "count", "Tech Mahindra Ltd India", url, doc, 90, "India only")
add("techm", 2019, "employees_total", "total", 79032, "count", "Tech Mahindra Ltd India", url, doc, 90)

url, doc = T[2018]
ages("techm", 2018, "employees_by_age", (51444, 41487, 2063), "count", GL, url, doc, 84, "bands 18-30/30-50/>50; global table by band x age")
add("techm", 2018, "employees_total", "total", 94994, "count", GL, url, doc, 84)
ages("techm", 2018, "employees_by_age", (25240 + 17499, 23524 + 5046, 614 + 81), "count", "Tech Mahindra Ltd India", url, doc, 84, "India only")
add("techm", 2018, "employees_total", "total", 72004, "count", "Tech Mahindra Ltd India", url, doc, 84)

# band-level headcount (global)
bands = {
    2018: (84, {"U1": 26047, "U2": 20419, "U3": 15544, "U4": 16051, "P1": 11156, "P2": 2923, "E1": 566, "E2": 85, "E3": 44, "EVP": 10, "RG1": 585, "RG2": 46, "UJ": 218, "VIS": 1283, "O3": 17},
           "FY18 table is band x age (18-30/30-50/>50); band totals computed F+M"),
    2019: (91, {"U1": 32709, "U2": 20955, "U3": 16970, "U4": 16819, "P1": 10646, "P2": 2877, "E1": 598, "E2": 103, "E3": 50, "EVP": 9, "RG1": 596, "RG2": 44, "VIS1": 75, "VIS2": 37, "VIS3": 1318, "O1": 1, "O3": 15}, ""),
    2020: (129, {"U1": 32712, "U2": 21889, "U3": 18256, "U4": 17157, "P1": 10502, "P2": 2890, "E1": 697, "E2": 109, "E3": 49, "EVP": 8, "RG1": 634, "RG2": 42, "Other": 1455}, ""),
    2021: (125, {"U1": 29104, "U2": 21725, "U3": 17815, "U4": 16599, "P1": 9616, "P2": 2711, "E1": 636, "E2": 101, "E3": 52, "EVP": 7, "RG1": 659, "RG2": 45, "Others": 537}, ""),
    2023: (62, {"U1": 37654, "U2": 28158, "U3": 24251, "U4": 21349, "P1": 10083, "P2": 3069, "E1": 862, "E2": 174, "E3": 57, "RG1": 930, "RG2": 63, "UJ": 12, "VIS": 163}, ""),
    2024: (104, {"U1": 41108, "U2": 26466, "U3": 24204, "U4": 21408, "P1": 9557, "P2": 3099, "E1": 936, "E2": 171, "E3": 60, "RG1": 856, "RG2": 66, "UJ": 2, "VIS": 218}, ""),
}
for fy, (pg, d, note) in bands.items():
    url, doc = T[fy]
    for b, n in d.items():
        add("techm", fy, "headcount_by_grade", "grade_" + b, n, "count", GL, url, doc, pg,
            ("U1 (lowest band) is majority BPO/BSG staff; U=junior, P=middle, E1+=senior, RG=sales, VIS/UJ/O=third-party/others. " + note).strip())

# GRI 401-1 new hires by age (global)
techm_nh = {
    2026: ((21972, 31343, 23), (6253, 14122, 10), (346, 966, 5), 75040, 28571, 46431, 123,
           {"junior_mgmt": 58227, "middle_mgmt": 1630, "senior_mgmt": 83, "fixed_term": 12175, "third_party": 2797, "sales": 128}),
    2025: ((24307, 31349, 7), (5882, 13234, 12), (285, 905, 5), 75986, 30474, 45488, 130,
           {"junior_mgmt": 60004, "middle_mgmt": 1369, "senior_mgmt": 123, "fixed_term": 11618, "third_party": 2742, "sales": 130}),
    2024: ((18702, 25747, 10), (5838, 12783, 7), (262, 862, 0), 64211, 24802, 39392, 103,
           {"junior_mgmt": 48623, "middle_mgmt": 1076, "senior_mgmt": 96, "fixed_term": 10677, "third_party": 3595, "sales": 144}),
    2023: ((24794, 34819, 0), (8437, 18986, 0), (318, 1074, 0), 88445, 33549, 54879, 60,
           {"junior_mgmt": 59824, "middle_mgmt": 2558, "senior_mgmt": 149, "fixed_term": 21852, "third_party": 3783, "sales": 279}),
    2022: ((18166, 24453, 22), (5760, 15347, 6), (295, 1007, 2), 65058, 24221, 40807, 117,
           {"junior_mgmt": 61464, "middle_mgmt": 3386, "senior_mgmt": 208}),
}
for fy, (a, b, c, tot, f, m, pg, grades) in techm_nh.items():
    url, doc = T[fy]
    v = (sum(a), sum(b), sum(c))
    assert abs(sum(v) - tot) <= 20, (fy, v, tot)
    note = AGE_BANDS_T + "; includes fixed-term & third-party contract hires"
    if fy == 2023:
        note += "; 17 'not disclosed' gender hires not split by age in source (row prints 0/0/0/17)"
    if fy == 2022:
        note += "; FY22 table covers jr/mid/sr mgmt only; text says 'we retained 65,058 new hires'"
    ages("techm", fy, "new_hires_by_age", v, "count", GL, url, doc, pg, note)
    add("techm", fy, "new_hires_total", "total", tot, "count", GL, url, doc, pg)
    add("techm", fy, "new_hires_total", "female", f, "count", GL, url, doc, pg)
    add("techm", fy, "new_hires_total", "male", m, "count", GL, url, doc, pg)
    for g, n in grades.items():
        add("techm", fy, "other", "new_hires_grade_" + g, n, "count", GL, url, doc, pg, "new hires by management category")

url, doc = T[2021]
ages("techm", 2021, "new_hires_by_age", (5877 + 9206 + 1 + 1619 + 1775 + 1, 1027 + 3773 + 836 + 2119, 5 + 82 + 87 + 329), "count", GL, url, doc, 135,
     "sum of offshore (19,971) + onsite (6,766) tables; 18-30/31-50/>50")
add("techm", 2021, "new_hires_total", "total", 26737, "count", GL, url, doc, 134, "text: 'During FY 2020-21, we hired 26,737 associates'")
add("techm", 2021, "new_hires_total", "female", 9451, "count", GL, url, doc, 134)
add("techm", 2021, "new_hires_total", "male", 17284, "count", GL, url, doc, 134)

url, doc = T[2020]
ages("techm", 2020, "new_hires_by_age", (23969, 5839, 69), "count", "Tech Mahindra Ltd India operations", url, doc, 139, "India only; 18-30/31-50/>50")
add("techm", 2020, "new_hires_total", "total", 29877, "count", "Tech Mahindra Ltd India operations", url, doc, 139)
url, doc = T[2019]
add("techm", 2019, "new_hires_total", "total", 33852, "count", "Tech Mahindra Ltd India operations", url, doc, 91, "no age split disclosed for FY19")
url, doc = T[2018]
ages("techm", 2018, "new_hires_by_age", (17589, 4393, 27), "count", "Tech Mahindra Ltd India operations", url, doc, 85, "India only; 18-30/30-50/>50")
add("techm", 2018, "new_hires_total", "total", 22009, "count", "Tech Mahindra Ltd India operations", url, doc, 85)
ages("techm", 2018, "turnover_by_age", (28789, 8106, 268), "count", "Tech Mahindra Ltd India operations", url, doc, 85, "separations (all reasons) India, FY18")
add("techm", 2018, "turnover_total", "total", 37163, "count", "Tech Mahindra Ltd India operations", url, doc, 85, "separations India")
add("techm", 2018, "turnover_total", "it_voluntary_rate", 18.0, "pct", "TechM IT employees", url, doc, 85, "IT attrition rate for the year")

# attrition rates by age/gender/grade (voluntary, IT employees, LTM)
techm_attr = {
    2026: (123, (12.9, 12.2, 6.8), 11.1, 12.5, (12.6, 9.0, 10.9), 12.1, 122),
    2025: (130, (11.5, 22.8, 1.4), 10.8, 12.3, (12.1, 10.1, 9.4), 11.8, 130),
    2024: (103, (9.3, 10.5, 8.2), 9.6, 10.1, (10.0, 9.7, 8.2), 10.0, 102),
    2023: (61, (12.5, 16.6, 11.6), 14.4, 15.0, (14.6, 16.0, 9.8), 14.8, 60),
    2022: (117, (24.4, 23.8, 12.6), 24.6, 23.2, (24.3, 21.2, 15.9), 23.5, 117),
    2021: (135, (15.5, 12.0, 8.7), 13.3, 13.2, (14.3, 9.9, 8.6), 13.3, 135),
}
for fy, (pg, a, f, m, g, tot, pgt) in techm_attr.items():
    url, doc = T[fy]
    note = "voluntary attrition, IT employees only, LTM; age bands <30/30-50/>50"
    if fy == 2025:
        note += "; FLAG: 30-50=22.8% and >50=1.4% look anomalous vs other years/overall 11.8% (as printed)"
    ages("techm", fy, "turnover_rate_by_age", a, "pct", "TechM IT employees (voluntary)", url, doc, pg, note)
    add("techm", fy, "turnover_rate_by_age", "female", f, "pct", "TechM IT employees (voluntary)", url, doc, pg, "by gender")
    add("techm", fy, "turnover_rate_by_age", "male", m, "pct", "TechM IT employees (voluntary)", url, doc, pg, "by gender")
    for gn, gv in zip(("junior_mgmt", "middle_mgmt", "senior_mgmt"), g):
        add("techm", fy, "other", "attrition_rate_grade_" + gn, gv, "pct", "TechM IT employees (voluntary)", url, doc, pg, "voluntary IT attrition by grade")
    add("techm", fy, "turnover_total", "it_voluntary_rate", tot, "pct", "TechM IT employees (voluntary)", url, doc, pgt, "headline LTM voluntary IT attrition")
add("techm", 2020, "turnover_total", "it_voluntary_rate", 19.1, "pct", "TechM IT employees", T[2020][0], T[2020][1], 139)

# fresher hires (TechM)
add("techm", 2021, "fresher_hires", "total", 2404, "count", "TechM (ELEVATE programme)", T[2021][0], T[2021][1], 132, "'2,404 Freshers/Interns were hired in FY21' under ELEVATE - includes interns")
add("techm", 2022, "fresher_hires", "total", 10000, "count", "TechM", T[2022][0], T[2022][1], 95, "CFO: 'hired more than 10,000 freshers throughout the year' (lower bound); CEO letter p21: fresher hiring increased 3X")
add("techm", 2022, "fresher_hires", "total", 10000, "count", "TechM", TI + "tml-q4-fy-22-earnings-transcript.pdf", "TechM Q4 FY22 earnings call transcript", 13, "'we've added more than 10,000 last year' (lower bound)")
add("techm", 2024, "fresher_hires", "9m_apr_dec", 2000, "count", "TechM", TI + "tml-q3-fy-24-earnings-transcript.pdf", "TechM Q3 FY24 earnings call transcript", 8, "'hired over 2,000 freshers up to December' - 9 months only; full-year FY24 not disclosed")
add("techm", 2024, "other", "freshers_added_ltm_jul23_jun24", 5450, "count", "TechM", TI + "tml-q1-fy-25-earnings-transcript.pdf", "TechM Q1 FY25 earnings call transcript", 9, "'added about 5,400-5,500 people in the past four quarters' (Q2FY24-Q1FY25, fresh talent); midpoint recorded")
add("techm", 2025, "fresher_hires", "total", 6000, "count", "TechM", TI + "tml-q4-fy-26-earnings-transcript.pdf", "TechM Q4 FY26 earnings call transcript", 27, "'we did about 6,000 in FY25'; Q1FY26 call p20 says '6,000 plus fresh graduates last year'; quarterly: Q1FY25 ~1,000, Q2FY25 2,000+")
add("techm", 2025, "fresher_hires", "q1", 1000, "count", "TechM", TI + "tml-q1-fy-25-earnings-transcript.pdf", "TechM Q1 FY25 earnings call transcript", 7, "'onboarded close to 1,000 freshers' in quarter")
add("techm", 2025, "fresher_hires", "q2", 2000, "count", "TechM", TI + "tml-q2-fy-25-earnings-transcript.pdf", "TechM Q2 FY25 earnings call transcript", 6, "'2,000 plus freshers that we onboarded for the quarter'")
add("techm", 2026, "fresher_hires", "total", 950, "count", "TechM", TI + "tml-q4-fy-26-earnings-transcript.pdf", "TechM Q4 FY26 earnings call transcript", 27, "'about 950 odd in FY26' (p26: '900 plus'); Q1FY26 only 250")
add("techm", 2026, "fresher_hires", "q1", 250, "count", "TechM", TI + "tml-q1-fy-26-earnings-transcript.pdf", "TechM Q1 FY26 earnings call transcript", 19, "'I think it's 250'")
add("techm", 2017, "fresher_hires", "q2", 2700, "count", "TechM", TI + "Earnings-Call-Transcript-Q2-FY17.pdf", "TechM Q2 FY17 earnings call transcript", 8, "'added about 2,700 trainees' in the quarter (pyramid correction)")

# ------------------------------------------------------------------ LTIMindtree / LTM (FY23+)
LR = "https://www.ltm.com/content/dam/ltimcorporatewebsite/uploads/report/"
L = {
    2026: (LR + "2026/sustainability-report-fy26.pdf", "LTM Sustainability Report FY2025-26"),
    2025: (LR + "2025/ltimindtree-sustainability-report-fy2024-25.pdf", "LTIMindtree Sustainability Report FY2024-25"),
    2024: (LR + "2024/ltimindtree-sustainability-report-fy2023-24.pdf", "LTIMindtree Sustainability Report FY2023-24"),
    2023: (LR + "2023/ltimindtree-sustainability-report-fy2022-23.pdf", "LTIMindtree Sustainability Report FY2022-23"),
}
LS = "LTIMindtree/LTM global, permanent employees"
ltim = {
    # hc_age, hc_tot, hcF, hcM, pg_hc, grades, nh_age, nh_tot, nhF, nhM, pg_nh, at_age, at_tot, atF, atM, pg_at, rate_age, rate_tot, rateF, rateM
    2026: ((30814, 54613, 2523), 87950, 27151, 60756, 57, {"associates": 76447, "middle_mgmt": 10593, "senior_mgmt": 791, "top_mgmt": 119},
           (13002, 9543, 359), 22905, 7346, 15539, 58, (5035, 6173, 190), 11399, 3420, 7976, 59, (16.56, 11.59, 8.06), 13.25, 12.95, 13.39),
    2025: ((30132, 52031, 2144), 84307, 25606, 58661, 62, {"associates": 72596, "middle_mgmt": 10703, "senior_mgmt": 866, "top_mgmt": 142},
           (11810, 11087, 304), 23201, 6812, 16363, 63, (5714, 6195, 134), 12043, 3850, 8190, 64, (18.37, 12.21, 6.54), None, None, None),
    2024: ((31859, 47910, 1881), 81650, 25061, 56566, 61, {"associates": 71038, "middle_mgmt": 9611, "senior_mgmt": 852, "top_mgmt": 149},
           (7736, 7619, 238), 15593, 4672, 10903, 62, (5872, 5886, 126), 11884, 3795, 8087, 63, (18.32, 12.14, 6.62), 14.45, 14.98, 14.21),
    2023: ((37469, 44777, 1988), 84546, 25998, 58528, 40, {"associates": 74442, "middle_mgmt": 8855, "senior_mgmt": 841, "top_mgmt": 96, "subsidiary": 312},
           (15261, 15508, 528), 31297, 8889, 22391, 41, (8066, 8759, 232), 17057, 5348, 11708, 42, (21.4, 19.4, 11.6), None, None, None),
}
for fy, r in ltim.items():
    url, doc = L[fy]
    (hca, hct, hcf, hcm, pgh, gr, nha, nht, nhf, nhm, pgn, ata, att, atf, atm, pga, rta, rtt, rtf, rtm) = r
    n23 = "; FY23 = first post-merger year (merger effective 14 Nov 2022; figures are combined entity at 31 Mar 2023)" if fy == 2023 else ""
    ages("ltimindtree", fy, "employees_by_age", hca, "count", LS, url, doc, pgh,
         "Talent Pool by age <30/30-50/>50" + ("; age sum 84,234 vs permanent total 84,546 (312 subsidiary employees?)" if fy == 2023 else "") + n23)
    add("ltimindtree", fy, "employees_total", "total", hct, "count", LS, url, doc, pgh, "permanent employees (contract staff reported separately)")
    add("ltimindtree", fy, "employees_total", "female", hcf, "count", LS, url, doc, pgh)
    add("ltimindtree", fy, "employees_total", "male", hcm, "count", LS, url, doc, pgh)
    for g, n in gr.items():
        add("ltimindtree", fy, "headcount_by_grade", "grade_" + g, n, "count", LS, url, doc, pgh, "employee category (Associates / Middle / Senior / Top management)")
    ages("ltimindtree", fy, "new_hires_by_age", nha, "count", LS, url, doc, pgn, "New hires by age" + n23)
    add("ltimindtree", fy, "new_hires_total", "total", nht, "count", LS, url, doc, pgn, "FY23 total computed from category rows (not printed)" if fy == 2023 else "")
    add("ltimindtree", fy, "new_hires_total", "female", nhf, "count", LS, url, doc, pgn)
    add("ltimindtree", fy, "new_hires_total", "male", nhm, "count", LS, url, doc, pgn)
    ages("ltimindtree", fy, "turnover_by_age", ata, "count", LS, url, doc, pga, "Attrition (all exits: voluntary, dismissal, retirement, death)")
    add("ltimindtree", fy, "turnover_total", "total", att, "count", LS, url, doc, pga)
    add("ltimindtree", fy, "turnover_total", "female", atf, "count", LS, url, doc, pga)
    add("ltimindtree", fy, "turnover_total", "male", atm, "count", LS, url, doc, pga)
    ages("ltimindtree", fy, "turnover_rate_by_age", rta, "pct", LS, url, doc, pga,
         "rate = exits / headcount at END of period (company formula), all exits")
    if rtt is not None:
        add("ltimindtree", fy, "turnover_rate_by_age", "total", rtt, "pct", LS, url, doc, pga, "all exits / end-period headcount")
        add("ltimindtree", fy, "turnover_rate_by_age", "female", rtf, "pct", LS, url, doc, pga)
        add("ltimindtree", fy, "turnover_rate_by_age", "male", rtm, "pct", LS, url, doc, pga)

# LTIM fresher data
L26AR = "https://www.ltm.com/annual-report-2026/ltm-limited-ir-2025-26.pdf"
L25AR = "https://www.ltm.com/annual-report-2025/pdfs/integrated-annual-report-fy-2024-25.pdf"
BSE = "https://www.bseindia.com/xml-data/corpfiling/AttachHis/"
add("ltimindtree", 2026, "fresher_hires", "total", 6700, "count", "LTM global", L[2026][0], L[2026][1], 29, "'Total Freshers Hired 6,700' (vs 22,905 total hires)")
add("ltimindtree", 2026, "fresher_hires", "total", 6700, "count", "LTM global", L26AR, "LTM Integrated Annual Report FY2025-26", 7, "'welcomed over 6,700 freshers during the year, a 40% jump over FY25' (also p63)")
add("ltimindtree", 2026, "fresher_hires", "q1", 1600, "count", "LTM global", BSE + "0c36ef61-c324-46a6-8d2b-bff48c9267a0.pdf", "LTIMindtree Q1 FY26 earnings call transcript (BSE filing)", 5, "'1,600 plus freshers this quarter'")
add("ltimindtree", 2026, "fresher_hires", "q2", 2604, "count", "LTM global", BSE + "60a18a9e-72c5-46db-b9bb-181056722d54.pdf", "LTIMindtree Q2 FY26 earnings call transcript (BSE filing)", 5, "'net addition of 2,558 employees ... including 2,604 freshers'")
add("ltimindtree", 2025, "fresher_hires", "total", 4700, "count", "LTIMindtree global", BSE + "35d78302-d45a-4dec-b9ad-0fc7c093795e.pdf", "LTIMindtree Q4 FY25 earnings call transcript (BSE filing)", 8, "'onboarded over 4,700 freshers during the year' (consistent with FY26 '40% jump' to 6,700)")
add("ltimindtree", 2025, "fresher_hires", "q2", 1100, "count", "LTIMindtree global", BSE + "c7ad0bac-0e7d-4b11-b33b-6b7182a6b744.pdf", "LTIMindtree Q2 FY25 earnings call transcript (BSE filing)", 8, "'1,100-plus freshers this quarter'")
add("ltimindtree", 2025, "fresher_hires", "q3", 1400, "count", "LTIMindtree global", BSE + "8e2e9fe2-3869-4e1c-b8a3-dd76a79dd5ef.pdf", "LTIMindtree Q3 FY25 earnings call transcript (BSE filing)", 9, "'over 1,400 freshers this quarter'")
add("ltimindtree", 2025, "other", "fresh_grads_onboarded_annually_generic", 9500, "count", "LTIMindtree", L25AR, "LTIMindtree Integrated Annual Report FY2024-25", 79, "generic claim 'onboard 9,000-10,000 fresh graduates annually' (p45: 'new recruits onboarded every year'); NOT a FY25 actual - conflicts with 4,700 actual")
add("ltimindtree", 2025, "employees_total", "total", 84307, "count", LS, L25AR, "LTIMindtree Integrated Annual Report FY2024-25", 79, "Key Employee Metrics table; FY24 81,650")
add("ltimindtree", 2025, "turnover_total", "ttm_rate", 14.4, "pct", "LTIMindtree global (TTM attrition, company KPI)", L25AR, "LTIMindtree Integrated Annual Report FY2024-25", 79, "TTM attrition FY25 14.4%, FY24 14.4% (voluntary-basis KPI, differs from SR all-exit turnover)")
add("ltimindtree", 2024, "turnover_total", "ttm_rate", 14.4, "pct", "LTIMindtree global (TTM attrition, company KPI)", L25AR, "LTIMindtree Integrated Annual Report FY2024-25", 79, "prior-year column")
add("ltimindtree", 2024, "fresher_hires", "q2", 1400, "count", "LTIMindtree global", BSE + "05c977ac-349f-4d9f-bc92-699d657d12ec.pdf", "LTIMindtree Q2 FY24 earnings call transcript (BSE filing)", 8, "'onboarded 1,400+ freshers this quarter'; FY24 annual total not found")
add("ltimindtree", 2024, "fresher_hires", "q4", 500, "count", "LTIMindtree global", BSE + "952743dd-2300-4b9b-b8cb-a8638f7e0b00.pdf", "LTIMindtree Q4 FY24 earnings call transcript (BSE filing)", 8, "'onboarded another 500+ freshers this quarter'")
add("ltimindtree", 2023, "other", "campus_hires_onboarded_via_LBJ", 2512, "count", "LTIMindtree", L[2023][0], L[2023][1], 21, "'2512 campus hires cleared LBJ (Learning Before Joining) and onboarded' - subset of FY23 fresher joins, not full count")
add("ltimindtree", 2023, "fresher_offers", "total", 7638, "count", "LTIMindtree", L[2023][0], L[2023][1], 21, "'IGNITE (LBJ) program launched for 2023 campus hires in Feb with 7638 campus hires' - pre-joining offer holders, not joined")

# ------------------------------------------------------------------ MINDTREE (pre-merger)
M = {
    2017: (LR + "2017/mindtree-sustainability-report-fy2016-17.pdf", "Mindtree Sustainability Report FY2016-17"),
    2020: (LR + "2020/mindtree-sustainability-report-fy2019-20.pdf", "Mindtree Sustainability Report FY2019-20"),
    2021: (LR + "2021/mindtree-sustainability-report-fy2020-21.pdf", "Mindtree Sustainability Report FY2020-21"),
    2022: (LR + "2022/mindtree-sustainability-report-fy2021-22.pdf", "Mindtree Sustainability Report FY2021-22"),
}
MS = "Mindtree Ltd global, permanent employees"
# (vintage, fy): hc_age, hc_tot, F, M, pg, nh_age, nh_tot, pg, at_age, at_tot, pg, rate_age, rate_tot, rateF, rateM, pg, grades
mt = [
    (2017, 2016, (8588, 7533, 176), 16297, 4564, 11733, 80, (3831, 1846, 107), 5784, 81, (2039, 1529, 37), 3605, 82, (23.74, 20.30, 21.02), 22.12, 22.33, 22.04, 82,
     {"associates_T4_C4": 13275, "middle_mgmt_C5_C7": 2783, "senior_mgmt_C8_C9": 148, "top_mgmt_C10_C12": 17, "subsidiary": 74}),
    (2017, 2017, (7910, 7976, 195), 16081, 4668, 11413, 80, (2212, 1246, 55), 3513, 81, (1888, 1783, 58), 3729, 82, (23.87, 22.35, 29.74), 21.85, 23.50, 21.17, 82,
     {"associates_T4_C4": 12822, "middle_mgmt_C5_C7": 3046, "senior_mgmt_C8_C9": 185, "top_mgmt_C10_C12": 18, "subsidiary": 10}),
    (2020, 2018, (8561, 8740, 264), 17565, 5187, 12378, 64, (3043, 1535, 115), 4693, 65, (1442, 1684, 84), 3210, 66, (16.8, 19.3, 31.8), 18.3, 16.6, 19.0, 67,
     {"associates_T4_C4": 14029, "middle_mgmt_C5_C7": 3123, "senior_mgmt_C8_C9": 213, "top_mgmt_C10_C12": 20, "subsidiary": 180}),
    (2020, 2019, (9793, 10070, 341), 20204, 6272, 13932, 64, (4442, 2378, 119), 6939, 65, (2262, 2093, 105), 4460, 66, (23.1, 20.8, 30.8), 22.1, 19.7, 23.1, 67,
     {"associates_T4_C4": 16245, "middle_mgmt_C5_C7": 3682, "senior_mgmt_C8_C9": 251, "top_mgmt_C10_C12": 26}),
    (2020, 2020, (10753, 10904, 334), 21991, 7124, 14867, 64, (4792, 2314, 103), 7209, 65, (2418, 2827, 178), 5423, 66, (22.5, 25.9, 53.3), 24.7, 23.4, 25.3, 67,
     {"associates_T4_C4": 17990, "middle_mgmt_C5_C7": 3736, "senior_mgmt_C8_C9": 249, "top_mgmt_C10_C12": 16}),
    (2021, 2021, (10909, 12542, 363), 23814, 7663, 16151, 51, (3433, 2436, 70), 5939, 52, (1288, 1453, 41), 2782, 53, (12.5, 11.8, 11.4), 12.1, 10.7, 12.8, 54,
     {}),
    (2022, 2022, (18182, 16379, 504), 35065, 11415, 23650, 40, (12728, 7276, 190), 20194, 41, (3578, 4263, 120), 7961, 42, (21.08, 26.62, 24.39), 23.78, 22.72, 24.29, 43,
     {"associates_C_C4": 29383, "middle_mgmt_C5_C7": 5193, "senior_mgmt_C8_C9": 472, "top_mgmt_C10_C12": 17}),
]
for (vin, fy, hca, hct, hcf, hcm, pgh, nha, nht, pgn, ata, att, pga, rta, rtt, rtf, rtm, pgr, gr) in mt:
    url, doc = M[vin]
    ages("mindtree", fy, "employees_by_age", hca, "count", MS, url, doc, pgh, "<30/30-50/>50")
    add("mindtree", fy, "employees_total", "total", hct, "count", MS, url, doc, pgh)
    add("mindtree", fy, "employees_total", "female", hcf, "count", MS, url, doc, pgh)
    add("mindtree", fy, "employees_total", "male", hcm, "count", MS, url, doc, pgh)
    nnote = ""
    if fy == 2021:
        nnote = "RESTATED: FY22 report (p41) restates FY21 new hires as 10,298 (<30 5,370; 30-50 4,737; >50 191)"
    ages("mindtree", fy, "new_hires_by_age", nha, "count", MS, url, doc, pgn, nnote)
    add("mindtree", fy, "new_hires_total", "total", nht, "count", MS, url, doc, pgn, nnote)
    ages("mindtree", fy, "turnover_by_age", ata, "count", MS, url, doc, pga, "total employee attrition (all exits)")
    add("mindtree", fy, "turnover_total", "total", att, "count", MS, url, doc, pga)
    ages("mindtree", fy, "turnover_rate_by_age", rta, "pct", MS, url, doc, pgr, "rate of employee turnover")
    add("mindtree", fy, "turnover_rate_by_age", "total", rtt, "pct", MS, url, doc, pgr)
    add("mindtree", fy, "turnover_rate_by_age", "female", rtf, "pct", MS, url, doc, pgr)
    add("mindtree", fy, "turnover_rate_by_age", "male", rtm, "pct", MS, url, doc, pgr)
    for g, n in gr.items():
        add("mindtree", fy, "headcount_by_grade", "grade_" + g, n, "count", MS, url, doc, pgh - 1 if vin in (2020, 2022) else pgh,
            "Mindtree grade bands (T4/C-C4 associates, C5-C7 middle, C8-C9 senior, C10-C12 top)")
# FY21 restated new hires (FY22 vintage)
url, doc = M[2022]
ages("mindtree", 2021, "new_hires_by_age", (5370, 4737, 191), "count", MS, url, doc, 41, "RESTATEMENT of FY21 (FY21 report said 5,939 total); keep both")
add("mindtree", 2021, "new_hires_total", "total", 10298, "count", MS, url, doc, 41, "RESTATEMENT of FY21 (FY21 report: 5,939)")
for g, n in {"associates_C_C4": 19500, "middle_mgmt_C5_C7": 4006, "senior_mgmt_C8_C9": 290, "top_mgmt_C10_C12": 18}.items():
    add("mindtree", 2021, "headcount_by_grade", "grade_" + g, n, "count", MS, url, doc, 39, "from FY22 report prior-year column")
add("mindtree", 2022, "turnover_total", "female", 2470, "count", MS, url, doc, 42)
add("mindtree", 2022, "turnover_total", "male", 5491, "count", MS, url, doc, 42)
# Mindtree fresher data
add("mindtree", 2019, "fresher_hires", "total", 1733, "count", "Mindtree Ltd", "https://www.bseindia.com/bseplus/AnnualReport/532819/5328190319.pdf", "Mindtree Integrated Annual Report FY2018-19 (BSE)", 23,
    "'number of Campus Minds trained at Mindtree Kalinga during FY19 was 1,733' (campus-hire induction; proxy for fresher joins)")
add("mindtree", 2021, "fresher_hires", "total", 1340, "count", "Mindtree Ltd", M[2021][0], M[2021][1], 9, "'1,340 Campus Mindtree Minds joined'")
add("mindtree", 2022, "fresher_hires", "total", 5000, "count", "Mindtree Ltd", M[2022][0], M[2022][1], 21, "'fresher onboarding (Orchard) went up by three times with about 5,000+ Campus Minds trained' (lower bound)")
add("mindtree", 2020, "other", "orchard_cumulative_since_2015", 6328, "count", "Mindtree Ltd", "https://www.bseindia.com/bseplus/AnnualReport/532819/5328190320.pdf", "Mindtree Integrated Annual Report FY2019-20 (BSE)", 82,
    "cumulative campus recruits through 90-day Orchard onboarding since 2015 (FY16-FY20)")

# ------------------------------------------------------------------ L&T INFOTECH (pre-merger)
LT = {
    2018: (LR + "2018/lti-sustainability-report-fy2017-18.pdf", "LTI Sustainability Report FY2017-18"),
    2019: (LR + "2019/lti-sustainability-report-fy2018-19.pdf", "LTI Sustainability Report FY2018-19"),
    2020: (LR + "2020/lti-sustainability-report-fy2019-20.pdf", "LTI Sustainability Report FY2019-20"),
    2021: (LR + "2021/lti-sustainability-report-fy2020-21.pdf", "LTI Sustainability Report FY2020-21"),
}
LTS = "LTI on-roll employees (excl. subsidiaries)"
url, doc = LT[2018]
ages("lti", 2018, "employees_by_age", (11004, 11527, 395), "count", LTS, url, doc, 41, "read from bar chart; on-roll only (sum 22,926 vs 24,139 incl. Syncordis)")
add("lti", 2018, "employees_total", "total", 24139, "count", "LTI incl. Syncordis subsidiary", url, doc, 42)
ages("lti", 2018, "new_hires_by_age", (4839, 2919, 150), "count", LTS, url, doc, 42, "read from bar chart; on-roll only")
ages("lti", 2018, "turnover_by_age", (1878, 1306, 31), "count", LTS, url, doc, 43, "read from bar chart; employee attrition by age")
add("lti", 2018, "turnover_total", "voluntary_rate", 14.8, "pct", "LTI", url, doc, 43, "voluntary resignations only; FY17 = 16.9%")
add("lti", 2017, "turnover_total", "voluntary_rate", 16.9, "pct", "LTI", url, doc, 43, "prior-year figure in FY18 report")
add("lti", 2018, "fresher_hires", "total", 1050 + 987, "count", LTS, url, doc, 42, "new hires in 'Trainee' category (987 M + 1,050 F; bar chart) - LTI trainee = graduate engineer trainees/freshers (proxy)")
for g, n in {"trainee": 1898, "jr_mgmt": 3113, "sr_mgmt": 1016, "consultant": 16899, "lt_depute": 101, "retainer": 972, "syncordis": 140}.items():
    add("lti", 2018, "headcount_by_grade", "grade_" + g, n, "count", "LTI incl. Syncordis", url, doc, 41, "employee category (bar chart); Trainee = freshers in training")
url, doc = LT[2019]
ages("lti", 2019, "employees_by_age", (48.63, 49.49), "pct", "LTI", url, doc, 37, "text: 48.63% below 30, 49.49% 30-50 (>50 implied ~1.88%)", dims=("age_lt30", "age_30_50"))
add("lti", 2019, "employees_total", "total", 28169, "count", "LTI", url, doc, 36)
add("lti", 2019, "new_hires_total", "total", 10063, "count", "LTI", url, doc, 37)
add("lti", 2019, "turnover_total", "voluntary_rate", 17.5, "pct", "LTI", url, doc, 37)
for g, n in {"trainee": 2948, "jr_mgmt": 3421, "sr_mgmt": 1200, "consultant": 18849, "lt_depute": 138, "retainer": 1209, "acquired": 404}.items():
    add("lti", 2019, "headcount_by_grade", "grade_" + g, n, "count", "LTI", url, doc, 36, "employee category")
url, doc = LT[2020]
ages("lti", 2020, "employees_by_age", (13671, 15258, 518), "count", LTS, url, doc, 55, "Below 30 / 30-50 / Above 50; on-roll only (29,447 vs 31,437 total)")
add("lti", 2020, "employees_total", "total", 31437, "count", "LTI incl. deputes/retainers/acquired", url, doc, 55)
ages("lti", 2020, "new_hires_by_age", (6111, 3204, 139), "count", "LTI", url, doc, 56)
add("lti", 2020, "new_hires_total", "total", 9454, "count", "LTI", url, doc, 56)
add("lti", 2020, "turnover_total", "voluntary_rate", 16.5, "pct", "LTI", url, doc, 56, "FY19 = 17.5%")
for g, n in {"trainee": 2723, "jr_mgmt": 4415, "sr_mgmt": 1490, "consultant": 20819, "lt_depute": 160, "retainer": 1165, "acquired": 664}.items():
    add("lti", 2020, "headcount_by_grade", "grade_" + g, n, "count", "LTI", url, doc, 55, "employee category")
url, doc = LT[2021]
ages("lti", 2021, "new_hires_by_age", (6413, 4184, 254), "count", "LTI (DOB-available employees)", url, doc, 29, "total 10,851 by age vs 11,241 by region (DOB missing for some onsite)")
add("lti", 2021, "new_hires_total", "total", 11241, "count", "LTI", url, doc, 28, "by-region total")
ages("lti", 2021, "turnover_by_age", (2125, 1813, 59), "count", "LTI", url, doc, 29, "separations by age")
ages("lti", 2021, "turnover_rate_by_age", (14.93, 10.98, 9.92), "pct", "LTI", url, doc, 29, "separations / AVERAGE headcount")
ages("lti", 2021, "other", (14238, 16506, 595), "count", "LTI", url, doc, 29, "average headcount by age (denominator for turnover rate)", dims=("avg_headcount_age_lt30", "avg_headcount_age_30_50", "avg_headcount_age_gt50"))
add("lti", 2021, "turnover_rate_by_age", "female", 13.02, "pct", "LTI", url, doc, 29)
add("lti", 2021, "turnover_rate_by_age", "male", 12.65, "pct", "LTI", url, doc, 29)
add("lti", 2021, "turnover_total", "total", 4000, "count", "LTI", url, doc, 29, "sum of gender separations 2,730 M + 1,270 F")
add("lti", 2021, "employees_total", "total", 35991, "count", "LTI", url, doc, 28)
for g, n in {"trainee": 3062, "jr_mgmt": 4746, "sr_mgmt": 1724, "consultant": 24267, "others": 2192}.items():
    add("lti", 2021, "headcount_by_grade", "grade_" + g, n, "count", "LTI", url, doc, 28, "employee category (GRI 405-1)")
add("lti", 2022, "fresher_hires", "total", 5200, "count", "LTI", BSE + "127349f5-965d-450d-b6ef-313fc0d8a8d2.pdf", "LTI Q4 FY22 earnings call transcript (BSE filing)", 5, "'started FY22 with a plan of hiring 4,500 freshers and ended up with 5,200'; FY23 floor plan >=6,500")
add("lti", 2020, "other", "planned_fresher_additions", 3800, "count", "LTI", "https://www.bseindia.com/bseplus/AnnualReport/540005/5400050319.pdf", "LTI Annual Report FY2018-19 (BSE)", 28, "plan: 'we plan to add 3,800 freshers during this year' (written in FY19 AR, refers to FY20) - plan, not actual")

with open(OUT, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["firm", "fiscal_year", "metric", "dimension", "value", "unit", "scope", "source_url", "source_doc", "page", "notes"])
    w.writeheader(); w.writerows(rows)
print(len(rows), "rows ->", OUT)
