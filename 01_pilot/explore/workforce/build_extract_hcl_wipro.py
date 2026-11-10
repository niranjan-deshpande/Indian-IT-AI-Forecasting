"""Build extract_hcl_wipro.csv: HCLTech + Wipro workforce seniority proxies.

All values hand-transcribed from primary company documents (ESG dashboards,
sustainability reports, integrated annual reports / BRSR, investor releases,
company-hosted earnings-call / AGM transcripts). Page = physical PDF page index.
Run: python3 build_extract_hcl_wipro.py  (writes CSV next to this script)
"""
import csv, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extract_hcl_wipro.csv")
COLS = ["firm", "fiscal_year", "metric", "dimension", "value", "unit", "scope",
        "source_url", "source_doc", "page", "notes"]
rows = []

def add(firm, fy, metric, dim, val, unit, scope, url, doc, page, notes=""):
    rows.append(dict(firm=firm, fiscal_year=fy, metric=metric, dimension=dim, value=val,
                     unit=unit, scope=scope, source_url=url, source_doc=doc, page=page, notes=notes))

# ---------------------------------------------------------------- URLs
HS = "https://www.hcltech.com/sites/default/files"
H = dict(
    sr26=(f"{HS}/documents/resources/pdf-landing-page/files/2026/07/17/sustainability-report-fy26.pdf", "HCLTech Sustainability Report FY26 (ESG Performance Metrics annex)"),
    sr25=(f"{HS}/documents/resources/pdf-landing-page/files/2025/10/15/sustainability-report-fy25.pdf", "HCLTech Sustainability Report FY25 (Oct-2025 version)"),
    sr24=(f"{HS}/documents/resources/pdf-landing-page/files/2024/07/21/hcltech-sustainability-report.pdf", "HCLTech Sustainability Report 2024 (FY24)"),
    sr23=(f"{HS}/document/open/FY2023_HCLTech_Sustainability_Report.pdf", "HCLTech Sustainability Report 2022-23"),
    sr22=(f"{HS}/document/open/FY2022_HCL_Sustainability_Report.pdf", "HCL Sustainability Report 2022 (FY22)"),
    ar26=(f"{HS}/document/open/annual-report/2026-09/annual-report-2025-26.pdf", "HCLTech Integrated Annual Report 2025-26"),
    ar25=(f"{HS}/document/open/annual-report/2025-08/Annual-Report-2024-25_0.pdf", "HCLTech Annual Report 2024-25"),
    ar24=(f"{HS}/document/open/annual-report/2024-08/HCLTech_Annual_Report2023-24.pdf", "HCLTech Annual Report 2023-24"),
    ar23=(f"{HS}/document/open/annual-report/2023-08/Annual_Report_2023.pdf", "HCLTech Annual Report 2022-23"),
    ar22=(f"{HS}/document/open/annual-report/2022-09/FINAL%20HCL%20AR_2022%20%281%29%20%284%29.pdf", "HCL Annual Report 2021-22 (incl. voluntary BRSR)"),
    ir_q4fy22=(f"{HS}/documents/investor-reports/HCL_Tech_Q4_FY22_Investor_Release.pdf", "HCL Q4 FY22 Investor Release"),
    ir_q3fy22=(f"{HS}/documents/investor-reports/HCL_Tech_Q3_FY22_Investor_Release.pdf", "HCL Q3 FY22 Investor Release"),
    tr_q1fy22=(f"{HS}/documents/investor-reports/hcl-earnings_call_transcript_19-7-2021q1fy22.pdf", "HCL Q1 FY22 earnings call transcript (19-Jul-2021)"),
    tr_q2fy25=(f"{HS}/documents/investor-reports/HCLTech-call-earnings-oct14-2024-Transcript.pdf", "HCLTech Q2 FY25 earnings call transcript (14-Oct-2024)"),
    agm23=(f"{HS}/document/open/annual-report/2023-10/AGM-Transcript-2023.pdf", "HCLTech 31st AGM transcript (2023)"),
    agm24=(f"{HS}/document/open/annual-report/2024-09/AGM_Transcript_2024.pdf", "HCLTech AGM transcript (2024)"),
)
WB = "https://www.wipro.com/content/dam/nexus/en"
WQ = f"{WB}/investor/quarterly-results"
W = dict(
    esg21=(f"{WB}/investor/annual-reports/2020-2021/wipro-esg-dashboard-fy-2020-21.pdf", "Wipro ESG Dashboard FY2020-21"),
    esg22=(f"{WB}/investor/annual-reports/2021-2022/wipro-esg-dashboard-fy-2021-22.pdf", "Wipro ESG Dashboard FY2021-22"),
    esg23=(f"{WB}/investor/annual-reports/2022-2023/esg-dashboard-fy-2022-23.pdf", "Wipro ESG Dashboard FY2022-23"),
    esg24=(f"{WB}/investor/annual-reports/2023-2024/wipro-esg-dashboard-fy23-24.pdf", "Wipro ESG Dashboard FY2023-24"),
    esg25=(f"{WB}/investor/annual-reports/2024-2025/esg-wipro-dashboard-fy24-25.pdf", "Wipro ESG Dashboard FY2024-25"),
    esg26=(f"{WB}/investor/annual-reports/2025-2026/esg-wipro-dashboard-fy25-26.pdf", "Wipro ESG Dashboard FY2025-26"),
    ar16=(f"{WB}/investor/annual-reports/2015-2016/11052-Wipro-Annual-Report-2016.pdf", "Wipro Annual Report 2015-16"),
    sr16=(f"{WB}/sustainability/sustainability_reports/Sustainability-Report-15-16.pdf", "Wipro Sustainability Report 2015-16"),
    sr17=(f"{WB}/sustainability/sustainability_reports/wipro-sustainability-report-2016-2017.pdf", "Wipro Sustainability Report 2016-17"),
    ar22=(f"{WB}/investor/annual-reports/2021-2022/integrated-annual-report-2021-22.pdf", "Wipro Integrated Annual Report 2021-22"),
    ar23=(f"{WB}/investor/annual-reports/2022-2023/integrated-annual-report-2022-23.pdf", "Wipro Integrated Annual Report 2022-23 (BRSR)"),
    ar24=(f"{WB}/investor/annual-reports/2023-2024/integrated-annual-report-2023-24.pdf", "Wipro Integrated Annual Report 2023-24 (BRSR)"),
    ar25=(f"{WB}/investor/annual-reports/2024-2025/Integrated-Annual-report-2024-2025.pdf", "Wipro Integrated Annual Report 2024-25 (BRSR)"),
    ar26=(f"{WB}/investor/annual-reports/2025-2026/Integrated-annual-report-2025-26.pdf", "Wipro Integrated Annual Report 2025-26 (BRSR)"),
    tr_q1fy20=(f"{WQ}/2019-2020/q1fy20/wipro-earning-call-transcript-q1-fy20.pdf", "Wipro Q1 FY20 earnings call transcript"),
    tr_q1fy22=(f"{WQ}/2021-2022/q1fy22/wipro-limited-q1-fy22-quarterly-investor-conference-call-transcript.pdf", "Wipro Q1 FY22 earnings call transcript"),
    tr_q2fy22=(f"{WQ}/2021-2022/q2fy22/wipro-limited-q2-fy22-quarterly-investor-conference-call-transcript.pdf", "Wipro Q2 FY22 earnings call transcript"),
    tr_q3fy22=(f"{WQ}/2021-2022/q3fy22/wipro-limited-q3-fy22-quarterly-investor-conference-call-transcript.pdf", "Wipro Q3 FY22 earnings call transcript"),
    tr_q4fy22=(f"{WQ}/2021-2022/q3fy22/wipro-limited-q4-fy22-quarterly-investor-conference-call-transcript.pdf", "Wipro Q4 FY22 earnings call transcript (hosted in q3fy22 folder)"),
    tr_q1fy23=(f"{WQ}/2022-2023/q1fy23/wipro-limited-q1-fy23-quarterly-investor-conference-call-transcript.pdf", "Wipro Q1 FY23 earnings call transcript"),
    tr_q2fy23=(f"{WQ}/2022-2023/q2fy23/wipro-limited-q2-fy23-quarterly-investor-conference-call-transcript.pdf", "Wipro Q2 FY23 earnings call transcript"),
    tr_q4fy23=(f"{WQ}/2022-2023/q4fy23/q4fy23-earnings-transcript.pdf", "Wipro Q4 FY23 earnings call transcript"),
    tr_q3fy25=(f"{WQ}/2024-2025/q3fy25/q3fy25-earnings-transcript.pdf", "Wipro Q3 FY25 earnings call transcript"),
)

def h(key, fy, metric, dim, val, unit, scope, page, notes=""):
    add("HCLTech", fy, metric, dim, val, unit, scope, H[key][0], H[key][1], page, notes)

def w(key, fy, metric, dim, val, unit, scope, page, notes=""):
    add("Wipro", fy, metric, dim, val, unit, scope, W[key][0], W[key][1], page, notes)

AGE3 = ["age_lt30", "age_30_50", "age_gt50"]

# ================================================================ HCLTech
HG = "global group, permanent employees"
# --- Employees by age x gender FY20-FY23 (SR 2022-23 p37; identical in SR2024 p50)
hcl_age_gender = {  # fy: {age: (male, female, other)}
    "FY2020": {"age_lt30": (37307, 22071, 9), "age_30_50": (65648, 15877, 34), "age_gt50": (5651, 1826, 34), "age_na": (1421, 544, 1)},
    "FY2021": {"age_lt30": (38658, 24849, 4), "age_30_50": (76820, 19020, 26), "age_gt50": (6433, 1716, 25), "age_na": (1079, 346, 1)},
    "FY2022": {"age_lt30": (50103, 32239, 12), "age_30_50": (91375, 23910, 36), "age_gt50": (7703, 2002, 23), "age_na": (1100, 374, 0)},
    "FY2023": {"age_lt30": (55717, 36951, 18), "age_30_50": (93972, 26433, 38), "age_gt50": (8995, 2126, 22), "age_na": (1158, 397, 117)},
    "FY2024": {"age_lt30": (52455, 35534, 12), "age_30_50": (95802, 27533, 40), "age_gt50": (10469, 2446, 31), "age_na": (2256, 755, 148)},
}
hcl_perm_total = {"FY2020": 150423, "FY2021": 168977, "FY2022": 208877, "FY2023": 225944}
for fy, d in hcl_age_gender.items():
    key, page = ("sr24", 50) if fy == "FY2024" else ("sr23", 37)
    if fy == "FY2024":
        continue  # FY24 age totals taken from SR FY26 annex below (identical sums); gender split still added
    tot = 0
    for age, (m, f, o) in d.items():
        s = m + f + o
        tot += s
        h(key, fy, "employees_by_age", age, s, "count", HG, page,
          "sum of male+female+other rows in 'Employees by age' table" + ("; age not disclosed" if age == "age_na" else ""))
    assert tot == hcl_perm_total[fy], (fy, tot)
for fy, d in hcl_age_gender.items():
    key, page = ("sr24", 50) if fy == "FY2024" else ("sr23", 37)
    for age, (m, f, o) in d.items():
        if age == "age_na":
            continue
        h(key, fy, "employees_by_age", f"{age}_male", m, "count", HG, page)
        h(key, fy, "employees_by_age", f"{age}_female", f, "count", HG, page)
for fy, v in hcl_perm_total.items():
    h("sr23", fy, "employees_total", "permanent", v, "count", HG, 36, "'Global Total' in employees by geography & gender table")

# --- SR FY26 ESG annex (FY24-FY26)
sr26_age = {"FY2026": (77219, 132588, 15321, 2053), "FY2025": (78602, 127867, 14251, 2700), "FY2024": (88001, 123375, 12946, 3159)}
sr26_perm = {"FY2026": 227181, "FY2025": 223420, "FY2024": 227481}
sr26_total = {"FY2026": 237098, "FY2025": 234496, "FY2024": 237248}
for fy, (a, b, c, na) in sr26_age.items():
    assert a + b + c + na == sr26_perm[fy]
    note = "HEADCOUNT - AGE DISTRIBUTION; sums to permanent headcount"
    if fy == "FY2025":
        note += "; differs from SR FY25 p49 (81,530/134,755/15,450/2,761) which is on total-employee base 234,496 (incl. non-permanent)"
    for dim, v in zip(AGE3 + ["age_na"], (a, b, c, na)):
        h("sr26", fy, "employees_by_age", dim, v, "count", HG, 84, note)
    h("sr26", fy, "employees_total", "permanent", sr26_perm[fy], "count", HG, 84)
    h("sr26", fy, "employees_total", "total_incl_nonpermanent", sr26_total[fy], "count", "global group, permanent + other-than-permanent", 84)
# SR FY25 vintage (different base)
for dim, v in zip(AGE3 + ["age_na"], (81530, 134755, 15450, 2761)):
    h("sr25", "FY2025", "employees_by_age", dim, v, "count", "global group, total employees incl. other-than-permanent (234,496)", 49,
      "pie chart 'Total employee by age in FY25'; base differs from SR FY26 restated permanent-only figures")
# BRSR totals incl. non-permanent FY22, FY23
h("ar22", "FY2022", "employees_total", "total_incl_nonpermanent", 224834, "count", "global group (BRSR, voluntary)", 196, "BRSR Q18: permanent 208,877 + other-than-permanent")
h("ar23", "FY2023", "employees_total", "total_incl_nonpermanent", 241352, "count", "global group (BRSR)", 182, "permanent 225,944 + other-than-permanent 15,408")

# --- New hires by age
hcl_hires = {  # fy: (lt30, 30_50, gt50, inorganic, age_na, total, key, page, band_note)
    "FY2021": (25170, 17514, 1508, 470, 33, 44695, "sr22", 34, "bands <30 / 30-50 / >50"),
    "FY2022": (53993, 40257, 2476, 767, 2, 97495, "sr22", 34, "bands <30 / 30-50 / >50"),
    "FY2024": (27728, 17163, 2180, 674, None, 47745, "sr26", 85, "bands reported as 18-30 / 31-50 / 51+; 'inorganic' = 'Others (including Inorganic)'"),
    "FY2025": (26703, 21344, 1869, 519, None, 50435, "sr26", 85, "bands reported as 18-30 / 31-50 / 51+; 'inorganic' = 'Others (including Inorganic)'"),
    "FY2026": (29346, 19392, 1598, 567, None, 50903, "sr26", 85, "bands reported as 18-30 / 31-50 / 51+; 'inorganic' = 'Others (including Inorganic)'"),
}
for fy, (a, b, c, inorg, na, tot, key, page, bn) in hcl_hires.items():
    assert a + b + c + inorg + (na or 0) == tot, fy
    for dim, v in zip(AGE3 + ["inorganic_or_other"], (a, b, c, inorg)):
        h(key, fy, "new_hires_by_age", dim, v, "count", "global group, new permanent hires", page, bn)
    if na:
        h(key, fy, "new_hires_by_age", "age_na", na, "count", "global group, new permanent hires", page, "row with age '-'")
    h(key, fy, "new_hires_total", "total", tot, "count", "global group, new permanent hires", page)
# new hires by management level FY21/FY22 (SR22 p34)
for fy, (sen, mid, jun) in {"FY2021": (28, 1749, 42448), "FY2022": (48, 2978, 93702)}.items():
    for dim, v in (("new_hires_mgmt_senior_top", sen), ("new_hires_mgmt_middle", mid), ("new_hires_mgmt_junior", jun)):
        h("sr22", fy, "other", dim, v, "count", "global group, new hires", 34, "New hires by management level (GRI 401-1 table); sums to total excl. inorganic/unassigned")
# new hires by gender FY24-26
for fy, (m, f, o) in {"FY2026": (34114, 16647, 142), "FY2025": (35420, 14977, 38), "FY2024": (33058, 14616, 71)}.items():
    h("sr26", fy, "new_hires_total", "male", m, "count", "global group", 85)
    h("sr26", fy, "new_hires_total", "female", f, "count", "global group", 85)
h("sr25", "FY2025", "other", "new_hire_rate", 22.4, "pct", "global group", 42, "'22.4% rate of new employee hire'")

# --- Turnover (voluntary attrition, LTM, IT services)
TN = "voluntary attrition % (LTM - IT Services)"
for fy, (a, b, c, oth) in {"FY2024": (14.04, 11.68, 5.65, 16.73), "FY2025": (15.53, 11.90, 5.72, 14.87), "FY2026": (16.23, 10.75, 5.44, 17.94)}.items():
    for dim, v in zip(AGE3 + ["age_other"], (a, b, c, oth)):
        h("sr26", fy, "turnover_rate_by_age", dim, v, "pct", "global group, IT services", 86, TN + "; bands 18-30 / 31-50 / 51+")
hcl_turn = {  # fy: (total, male, female, key, page)
    "FY2020": (16.27, 15.79, 17.11, "ar22", 196),
    "FY2021": (9.90, 9.81, 10.16, "ar23", 183),
    "FY2022": (21.92, 21.87, 22.05, "ar23", 183),
    "FY2023": (19.50, 19.83, 18.60, "ar23", 183),
    "FY2024": (12.42, 12.32, 12.72, "sr26", 85),
    "FY2025": (12.99, 13.06, 12.81, "sr26", 85),
    "FY2026": (12.51, 12.61, 12.28, "sr26", 85),
}
for fy, (t, m, f, key, page) in hcl_turn.items():
    pg_f = 86 if key == "sr26" else page
    h(key, fy, "turnover_total", "total", t, "pct", "global group, IT services, permanent", page, TN + "; same values in BRSR")
    h(key, fy, "turnover_total", "male", m, "pct", "global group, IT services, permanent", page, TN)
    h(key, fy, "turnover_total", "female", f, "pct", "global group, IT services, permanent", pg_f, TN)

# --- Freshers
h("ir_q4fy22", "FY2022", "fresher_hires", "total", 23000, "count", "global group", 10, "'Entry level (fresher) employees hired in FY'22 - 23,000'")
h("ir_q3fy22", "FY2022", "fresher_hires", "ytd_Q1_Q3", 16000, "count", "global group", 11, "'16,000 freshers already hired till Q3'; plan 20,000-22,000 for FY22")
h("tr_q1fy22", "FY2022", "fresher_hires", "quarter_Q1", 3500, "count", "global group", 6, "CEO: 'We hired 3,500 freshers during the same period'")
h("ar23", "FY2023", "fresher_hires", "total", 26734, "count", "global group", 52, "'Freshers added in FY23'; AGM-2023 transcript p6 says 'over 26,700'; AR 2025-26 p13 repeats 26,734")
h("ar24", "FY2024", "fresher_hires", "total", 12141, "count", "global group", 124, "Directors' report; also AR24 p7, AGM-2024 p6, AR 2025-26 p13; Q2FY25 call p13 says 'about 12,000'")
h("ar25", "FY2025", "fresher_hires", "total", 7829, "count", "global group", 126, "'7,829 freshers were onboarded'; also SR FY25 p43 ('fresh graduates') and AR 2025-26 p13")
h("ar25", "FY2025", "other", "freshers_hired_infographic", "1800+", "count", "global group", 65, "People-section infographic says '1,800+ Freshers hired' - conflicts with 7,829 on p126; possibly a sub-programme figure; treat as unreliable")
h("ar25", "FY2025", "other", "new_vistas_fresh_graduates_hired", "1900+", "count", "India Tier-2/3 New Vistas centres", 69, "of >4,400 New Vistas hires in FY25")
h("ar26", "FY2026", "fresher_hires", "total", 11744, "count", "global group", 135, "Directors' report 'onboarded 11,744 freshers, including through TechBee'; also p13 and p57")
# --- Gen Z share (age proxy)
h("agm23", "FY2023", "other", "genz_share_of_employees", 24, "pct", "global group", 6, "Gen Z = born ~1997+; 'represent 24% of our total employees today' (Aug-2023)")
h("ar24", "FY2024", "other", "genz_share_of_employees", 27.2, "pct", "global group", 80)
h("ar25", "FY2025", "other", "genz_share_of_employees", 28, "pct", "global group", 69, "AGM-2025 transcript says 'over 25%'")
h("ar26", "FY2026", "other", "genz_share_of_employees", 31, "pct", "global group", 13, "also p57")
h("sr26", "FY2026", "other", "campus_hires_female_share", 46, "pct", "global group", 87, "FY25 50%, FY24 43% on same page")

# ================================================================ Wipro
WS = "Wipro Ltd group, permanent employees, excl. Capco & other acquisitions"
w_emp = {  # fy: (lt30, 30_50, gt50, total, key, page)
    "FY2019": (96063, 74167, 5460, 175690, "esg21", 7),
    "FY2020": (100663, 81107, 6500, 188270, "esg22", 8),
    "FY2021": (102964, 90522, 8179, 201665, "esg23", 6),
    "FY2022": (124856, 105535, 9433, 239824, "esg24", 12),
    "FY2023": (132720, 107617, 8758, 249095, "esg26", 18),
    "FY2024": (111756, 104833, 8793, 225382, "esg26", 18),
    "FY2025": (109726, 106817, 8763, 225306, "esg26", 18),
    "FY2026": (110489, 109791, 7867, 228147, "esg26", 18),
}
for fy, (a, b, c, t, key, page) in w_emp.items():
    assert a + b + c == t, fy
    note = "same figure in all later dashboard vintages checked (no restatement)"
    if fy == "FY2019":
        note = "FY2019 total from p8; Capco not yet acquired"
    if fy == "FY2022":
        note += "; FY22 dashboard excludes Ampion & Edgile"
    for dim, v in zip(AGE3, (a, b, c)):
        w(key, fy, "employees_by_age", dim, v, "count", WS, page, note)
    w(key, fy, "employees_total", "permanent_excl_capco", t, "count", WS, page if fy != "FY2019" else 8)
w_con = {
    "FY2020": (10125, 4046, 3409, 17580, "esg22", 9),
    "FY2021": (8519, 4563, 3419, 16501, "esg23", 6),
    "FY2022": (26656, 6587, 3126, 36369, "esg23", 6),
    "FY2023": (5950, 5299, 1983, 13232, "esg26", 19),
    "FY2024": (4239, 5140, 1170, 10549, "esg26", 19),
    "FY2025": (3925, 5595, 589, 10109, "esg26", 19),
    "FY2026": (3733, 5284, 897, 9914, "esg26", 19),
}
for fy, (a, b, c, t, key, page) in w_con.items():
    assert a + b + c == t, fy
    for dim, v in zip(AGE3, (a, b, c)):
        w(key, fy, "employees_by_age", dim, v, "count", "Wipro group, contractual (other-than-permanent) employees", page, "Employee Count (Contractual) age-wise")
    w(key, fy, "employees_total", "contractual", t, "count", "Wipro group, contractual employees", page)
# Capco FY22
for dim, v in zip(AGE3, (1810, 3782, 553)):
    w("esg22", "FY2022", "employees_by_age", dim, v, "count", "Capco only (acquired Apr-2021)", 16, "age not captured for some; age-known total 6,145 of 7,249")
w("esg22", "FY2022", "employees_total", "capco", 7249, "count", "Capco only", 16)

w_hire = {
    "FY2019": (43478, 19906, 1903, 65323, "esg21", 9),
    "FY2020": (46518, 19070, 2559, 68147, "esg22", 10),
    "FY2021": (34343, 16436, 3134, 53913, "esg23", 7),
    "FY2022": (77028, 41000, 3290, 121318, "esg24", 13),
    "FY2023": (66395, 29126, 1896, 97417, "esg25", 20),
    "FY2024": (27711, 11540, 931, 40182, "esg25", 20),
    "FY2025": (41881, 17262, 1029, 60172, "esg25", 20),
}
for fy, (a, b, c, t, key, page) in w_hire.items():
    gap = t - (a + b + c)
    assert gap == 0 or fy == "FY2019", fy
    for dim, v in zip(AGE3, (a, b, c)):
        w(key, fy, "new_hires_by_age", dim, v, "count", WS, page, "GRI 401-1 new hires age-wise; FY26 dashboard dropped this table")
    w(key, fy, "new_hires_total", "total", t, "count", WS, page,
      f"age rows sum to {a+b+c:,}, {gap} short of region/gender total" if gap else "")
for dim, v in zip(AGE3, (1517, 2798, 274)):
    w("esg22", "FY2022", "new_hires_by_age", dim, v, "count", "Capco only", 17)
w("esg22", "FY2022", "new_hires_total", "total", 4589, "count", "Capco only", 17)

w_att = {
    "FY2019": (17.6, 15.9, 12.0, "esg21", 17, "read from bar-chart data labels (FY19/FY20/FY21 series); FY20/FY21 values match FY22 table"),
    "FY2020": (13.40, 12.10, 9.90, "esg22", 11, ""),
    "FY2021": (13.0, 11.6, 8.2, "esg23", 7, ""),
    "FY2022": (23.8, 22.8, 14.4, "esg24", 13, ""),
    "FY2023": (20.3, 21.1, 13.5, "esg25", 21, ""),
    "FY2024": (14.4, 14.0, 9.8, "esg25", 21, ""),
    "FY2025": (14.4, 15.7, 8.3, "esg25", 21, "FY26 dashboard dropped attrition-by-age table"),
}
for fy, (a, b, c, key, page, n) in w_att.items():
    for dim, v in zip(AGE3, (a, b, c)):
        w(key, fy, "turnover_rate_by_age", dim, v, "pct", WS, page, ("voluntary attrition %; " + n).strip("; "))
for dim, v in zip(AGE3, (50.2, 27.0, 13.9)):
    w("esg22", "FY2022", "turnover_rate_by_age", dim, v, "pct", "Capco only", 17, "voluntary attrition %")
w_att_g = {"FY2019": (15.2, 17.3, "esg21", 17), "FY2020": (11.90, 13.00, "esg22", 11), "FY2021": (11.2, 12.5, "esg23", 7),
           "FY2022": (21.5, 23.9, "esg23", 7), "FY2023": (20.2, 20.5, "esg25", 21), "FY2024": (12.8, 14.5, "esg25", 21), "FY2025": (13.5, 15.4, "esg25", 21)}
for fy, (f, m, key, page) in w_att_g.items():
    w(key, fy, "turnover_total", "female", f, "pct", WS, page, "ESG dashboard voluntary attrition by gender")
    w(key, fy, "turnover_total", "male", m, "pct", WS, page, "ESG dashboard voluntary attrition by gender")
# BRSR turnover (voluntary, IT services) incl. restatements
BN = "BRSR turnover = voluntary attrition of IT Services; excludes acquired businesses"
w("ar23", "FY2021", "turnover_total", "total", 12, "pct", "Wipro Ltd IT services (BRSR)", 412, BN)
w("ar23", "FY2022", "turnover_total", "total", 22.9, "pct", "Wipro Ltd IT services (BRSR)", 412, BN + "; RESTATED to 23.71 in FY24 BRSR")
w("ar24", "FY2022", "turnover_total", "total", 23.71, "pct", "Wipro Ltd IT services (BRSR)", 434, BN + "; restatement of 22.9 in FY23 BRSR")
w("ar23", "FY2023", "turnover_total", "total", 20.4, "pct", "Wipro Ltd IT services (BRSR)", 412, BN + "; RESTATED to 19.21 in FY24/FY25 BRSR")
w("ar24", "FY2023", "turnover_total", "total", 19.21, "pct", "Wipro Ltd IT services (BRSR)", 434, BN + "; restatement of 20.4 in FY23 BRSR (M 19.97, F 17.63)")
for fy, (t, m, f) in {"FY2024": (13.95, 14.50, 12.83), "FY2025": (14.81, 15.43, 13.52), "FY2026": (14.09, 14.36, 13.54)}.items():
    w("ar26", fy, "turnover_total", "total", t, "pct", "Wipro Ltd IT services (BRSR)", 491, BN)
    w("ar26", fy, "turnover_total", "male", m, "pct", "Wipro Ltd IT services (BRSR)", 491, BN)
    w("ar26", fy, "turnover_total", "female", f, "pct", "Wipro Ltd IT services (BRSR)", 491, BN)
# BRSR headcount
for key, fy, perm, tot, page, sc in (("ar23", "FY2023", 249095, 262325, 411, "excl. acquisitions"),
                                      ("ar24", "FY2024", 225381, 235930, 434, "excl. acquisitions"),
                                      ("ar25", "FY2025", 225306, 235415, 468, "excl. acquisitions"),
                                      ("ar26", "FY2026", 236322, 246990, 491, "INCLUDES Capco (dashboard excl. Capco = 228,147)")):
    w(key, fy, "employees_total", "permanent_brsr", perm, "count", f"Wipro group BRSR, {sc}", page)
    w(key, fy, "employees_total", "total_incl_nonpermanent_brsr", tot, "count", f"Wipro group BRSR, {sc}", page)

# --- Age / tenure style
w("ar16", "FY2016", "avg_age", "total", 30.6, "count", "Wipro group", 48, "unit = years; 'average age of 30.6 years' (Management Discussion); SR 2015-16 p59 same")
w("ar16", "FY2016", "employees_by_age", "age_lt30", 60, "pct", "Wipro group", 48, "'60% of our employees under the age of 30 years'")
w("sr17", "FY2017", "employees_by_age", "age_lt30", 60, "pct", "Wipro group", 83, "'a significant portion (60%) is under the age of 30'; average age stated only as '30+ years'")

# --- Freshers (Wipro)
w("tr_q1fy20", "FY2020", "fresher_hires", "quarter_Q1", 6000, "count", "Wipro group (global)", 3, "'In Q1, we have hired 6,000 freshers and onboard with them globally'")
w("tr_q1fy22", "FY2022", "other", "fresher_growth_plan_vs_FY21", 33, "pct", "Wipro group", 6, "plan: 'onboard 33% more freshers in FY22 versus the previous year'; also 'intend to onboard 6,000 freshers in Q2'")
w("tr_q2fy22", "FY2022", "fresher_hires", "quarter_Q2", 8150, "count", "Wipro group", 6, "'8,150 young colleagues joining us from campus in Q2'")
w("tr_q2fy22", "FY2023", "other", "fresher_plan", 25000, "count", "Wipro group", 6, "plan (Oct-2021): 'well positioned to add over 25,000 freshers in the next financial year'")
w("tr_q3fy22", "FY2022", "other", "fresher_growth_vs_FY21", 70, "pct", "Wipro group", 6, "'on course to onboard over 70% more fresh talent from the campus in FY22 versus the previous year'")
w("tr_q4fy22", "FY2022", "other", "fresher_growth_vs_FY21", 100, "pct", "Wipro group", 7, "'We doubled our fresher intake for FY22 when compared to the previous year'; Q1FY23 call p8: FY22 'more than double' FY21")
w("ar22", "FY2022", "other", "campus_hires_completed_induction_program", 17464, "count", "Wipro group", 45, "'30-day virtual learning program was completed by 17,464 campus hires' - lower bound proxy for FY22 campus intake")
w("tr_q2fy23", "FY2022", "other", "fresher_hires_implied_derived", 18700, "count", "Wipro group", 6, "DERIVED not stated: H1FY23 >14,000 = '75% of what we added in the whole of last year' => FY22 ~18,700")
w("tr_q1fy23", "FY2023", "fresher_hires", "quarter_Q1", 10000, "count", "Wipro group", 6, "'onboarded more than 10,000 freshers in Q1' (lower bound)")
w("tr_q2fy23", "FY2023", "fresher_hires", "H1", 14000, "count", "Wipro group", 6, "'on-boarded over 14,000 freshers in H1' (lower bound)")
w("ar23", "FY2023", "fresher_hires", "total", 22000, "count", "Wipro group", 10, "'hired 22,000 Next-Gen Associates (or freshers)'; Q4FY23 call p6 says 'over 22,000'")
w("tr_q3fy25", "FY2026", "other", "fresher_plan_per_year", "10000-12000", "count", "Wipro group", 12, "plan (Jan-2025): 'for the next fiscal ... hiring about 10,000 to 12,000 people' from campus; outcome not stated in Wipro-hosted FY26 transcripts")

with open(OUT, "w", newline="") as fh:
    wr = csv.DictWriter(fh, fieldnames=COLS)
    wr.writeheader()
    wr.writerows(rows)
print(f"wrote {len(rows)} rows -> {OUT}")
