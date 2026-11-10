import csv, sys
out = sys.argv[1]
rows = []
B = ['<30', '30-50', '>50', 'total']
def add(firm, fy, metric, vals, unit, scope, url, doc, page, notes='', bands=B):
    for b, v in zip(bands, vals):
        if v is None: continue
        rows.append(dict(firm=firm, fiscal_year=fy, metric=metric, age_band=b, value=v, unit=unit, scope=scope,
                         source_url=url, source_doc=doc, page=page, status='CONFIRMED', notes=notes))

# ---------------- Persistent ----------------
P26 = 'https://www.persistent.com/wp-content/uploads/2026/07/ESG-Fact-Sheet-FY2025-26.pdf'
P25 = 'https://www.persistent.com/wp-content/uploads/2025/06/ESG-Fact-Sheet-FY2024-25.pdf'
d26 = 'raw/persistent/ESG_FactSheet_FY2025-26.pdf'; d25 = 'raw/persistent/ESG_FactSheet_FY2024-25.pdf'
F = 'Persistent'
sc = 'Global total workforce (Regular/FTE + contract); bands Under 30 / 30-50 / Over 50'
for fy, v in [('FY23', (10904, 11437, 548, 22889)), ('FY24', (9582, 13648, 620, 23850)),
              ('FY25', (7402, 16440, 752, 24594)), ('FY26', (7559, 19023, 920, 27502))]:
    add(F, fy, 'headcount_by_age', v, 'count', sc, P26, d26, 19, 'FY26 total incl. 2,901 contract (24,601 regular)' if fy == 'FY26' else '')
add(F, 'FY22', 'headcount_by_age', (7434, 10638, 527, 18599), 'count', sc, P25, d25, 16, 'older vintage (FY25 fact sheet)')
sc = 'Global new hires; bands Under 30 / 30-50 / Over 50'
for fy, v in [('FY23', (8286, 4658, 238, 13182)), ('FY24', (3014, 4405, 219, 7638)),
              ('FY25', (2720, 4886, 309, 7915)), ('FY26', (3833, 6106, 370, 10309))]:
    add(F, fy, 'hires_by_age', v, 'count', sc, P26, d26, 26)
add(F, 'FY22', 'hires_by_age', (7360, 4438, 209, 12007), 'count', sc, P25, d25, 21,
    'totals only; printed FY22 male column duplicates FY24 male values (doc error), male+female != total')
sc = 'Global FTE turnover rate (section titled Voluntary Turnover Rate, GRI 401-1)'
for fy, v in [('FY23', (21.40, 18.60, 15.20, 19.80)), ('FY24', (13.70, 10.00, 9.60, 11.50)),
              ('FY25', (17.57, 10.94, 10.81, 12.93)), ('FY26', (20.99, 9.88, 9.03, 13.01))]:
    add(F, fy, 'turnover_rate_by_age', v, 'percent', sc, P26, d26, 30,
        'column headers in FY26 fact sheet are shifted one year back (printed FY2021-22..FY2024-25); year assigned by matching totals to the category/region tables and to the FY25 fact sheet')
add(F, 'FY22', 'turnover_rate_by_age', (33.12, 24.10, 12.00, 26.35), 'percent', sc, P25, d25, 24, 'older vintage; FY25 sheet shows FY25 as 17.6/10.9/10.8/12.9')
L = ['junior', 'middle', 'senior', 'total']
for fy, v in [('FY23', (19538, 2926, 425, 22889)), ('FY24', (19557, 3769, 524, 23850)),
              ('FY25', (19812, 4267, 515, 24594)), ('FY26', (21514, 5293, 695, 27502))]:
    add(F, fy, 'headcount_by_level', v, 'count', 'Global workforce by category. Junior=freshers/intern/trainee/contractor; Middle=first-level & middle mgrs; Senior=leadership/delivery heads',
        P26, d26, 17, 'age_band column holds level; FY24 middle printed as "37,69"' if fy == 'FY24' else 'age_band column holds level', bands=L)
for fy, v in [('FY23', (12021, 1031, 130, 13182)), ('FY24', (6509, 990, 139, 7638)),
              ('FY25', (6809, 981, 125, 7915)), ('FY26', (8745, 1359, 205, 10309))]:
    add(F, fy, 'hires_by_level', v, 'count', 'Global new hires by management category (Junior/Middle/Senior)', P26, d26, 24, 'extra metric; age_band column holds level', bands=L)
for fy, v in [('FY23', (20.5, 15.6, 17.4, 19.8)), ('FY24', (12.2, 8.0, 9.7, 11.5)),
              ('FY25', (13.3, 10.9, 15.2, 12.9)), ('FY26', (14.23, 8.12, 15.21, 13.01))]:
    add(F, fy, 'turnover_rate_by_level', v, 'percent', 'Global turnover rate by category', P26, d26, 28, 'extra metric; age_band column holds level', bands=L)

# ---------------- Mphasis ----------------
F = 'Mphasis'
M21 = 'https://www.mphasis.com/content/dam/mphasis-com/global/en/home/esg/mphasis-esg-report-20-21.pdf'
M22 = 'https://www.mphasis.com/content/dam/mphasis-com/global/en/home/esg/mphasis-esg-databook-2021-2022.pdf'
M23 = 'https://www.mphasis.com/content/dam/mphasis-com/global/en/home/esg/mphasis-esg-databook-2022-2023.pdf'
M24 = 'https://www.mphasis.com/content/dam/mphasis-com/global/en/home/esg/mphasis-esg-databook-2023-2024.pdf'
M25 = 'https://marketingable.mphasis.com/content/dam/mphasis-com/global/en/home/esg/our-esg-databook-2024-2025.pdf'
m21, m22, m23, m24, m25 = ('raw/mphasis/esg_report_20-21.pdf', 'raw/mphasis/databook_2021-22.pdf', 'raw/mphasis/databook_2022-23.pdf',
                           'raw/mphasis/databook_2023-24.pdf', 'raw/mphasis/databook_2024-25.pdf')
sc = 'Workforce global (employees, excl. contractual workers); bands <30 / 30-50 / >50'
add(F, 'FY22', 'headcount_by_age', (16819, 18440, 1650), 'count', sc, M22, m22, 7, 'M+F=36,910; level x age rows sum to less (34,424)')
add(F, 'FY23', 'headcount_by_age', (15514, 17388, 1481), 'count', sc, M23, m23, 4)
add(F, 'FY24', 'headcount_by_age', (14009, 15796, 1425), 'count', sc, M25, m25, 5, 'same values in 2023-24 databook p5')
add(F, 'FY25', 'headcount_by_age', (11959, 18098, 2026), 'count', sc, M25, m25, 5)
lv = {'SM': 'Senior management (L11-L12)', 'MM': 'Middle management (L9-L10)', 'JM': 'Junior management (L7-L8)', 'OE': 'Other employees non-executive (L1-L6)'}
hc = {('FY21', M21, m21, 44): {'SM': (0, 42, 26), 'MM': (0, 472, 137), 'JM': (5, 1777, 296), 'OE': (10492, 12633, 925)},
      ('FY22', M22, m22, 6): {'SM': (0, 48, 27), 'MM': (0, 519, 181), 'JM': (12, 1949, 309), 'OE': (16205, 14234, 940)},
      ('FY23', M23, m23, 4): {'SM': (0, 60, 53), 'MM': (1, 451, 176), 'JM': (7, 1802, 314), 'OE': (14969, 13755, 775)},
      ('FY24', M25, m25, 5): {'SM': (None, 38, 42), 'MM': (None, 461, 237), 'JM': (11, 1806, 367), 'OE': (13998, 13490, 779)},
      ('FY25', M25, m25, 5): {'SM': (0, 36, 39), 'MM': (0, 463, 269), 'JM': (10, 1804, 418), 'OE': (12989, 15039, 1036)}}
for (fy, u, d, pg), dd in hc.items():
    for k, v in dd.items():
        add(F, fy, 'headcount_by_age', v, 'count', 'Level x age: ' + lv[k], u, d, pg,
            'FY21: Mphasis Ltd, no global age total printed' if fy == 'FY21' else ('<30 printed as "-"' if v[0] is None else ''))
sc = 'Global new hires (all levels); bands <30 / 30-50 / >50'
add(F, 'FY22', 'hires_by_age', (13556, 9991, 811), 'count', sc, M22, m22, 8, 'age rows sum 24,358 but headline new hires = 15,040 (p8/9); inconsistent')
add(F, 'FY23', 'hires_by_age', (8063, 6048, 373, 14484), 'count', sc, M23, m23, 5)
add(F, 'FY24', 'hires_by_age', (6218, 3480, 299, 11264), 'count', sc, M25, m25, 6, 'age rows sum 9,997 vs headline 11,264')
add(F, 'FY25', 'hires_by_age', (4663, 3985, 336, 9916), 'count', sc, M25, m25, 6, 'age rows sum 8,984 vs headline 9,916')
hh = {('FY21', M21, m21, 45): {'SM': (0, 3, 1), 'MM': (0, 42, 27), 'JM': (5, 250, 108), 'OE': (4471, 3742, 693)},
      ('FY22', M22, m22, 8): {'SM': (0, 2, 2), 'MM': (0, 68, 37), 'JM': (8, 580, 126), 'OE': (13548, 9341, 646)},
      ('FY23', M23, m23, 5): {'SM': (1, 63, 19), 'MM': (8, 364, 50), 'JM': (7398, 4532, 189), 'OE': (0, 0, 0)},
      ('FY24', M25, m25, 6): {'SM': (0, 4, 5), 'MM': (0, 71, 21), 'JM': (11, 365, 60), 'OE': (6208, 3040, 213)},
      ('FY25', M25, m25, 6): {'SM': (0, 8, 6), 'MM': (0, 69, 29), 'JM': (3, 254, 39), 'OE': (4356, 3034, 158)}}
for (fy, u, d, pg), dd in hh.items():
    for k, v in dd.items():
        add(F, fy, 'hires_by_age', v, 'count', 'Level x age: ' + lv[k], u, d, pg,
            {'FY21': 'FY21 also lists contractual hires 279/633/125; headline FY21 hires elsewhere = 5,207', 'FY23': 'FY23 Other-employee hires reported as 0, all non-mgmt hires booked under Junior mgmt'}.get(fy, ''))
add(F, 'FY21', 'hires_by_age', (279, 633, 125), 'count', 'Contractual employees new hires', M21, m21, 45)
tr = {('FY21', M21, m21, 46): {'SM': (0.0, 2.5, 11.1), 'MM': (0.0, 10.7, 10.5), 'JM': (70.6, 18.9, 24.8), 'OE': (31.7, 31.3, 63.1)},
      ('FY22', M22, m22, 10): {'SM': (0, 0.03, 0.02), 'MM': (0, 0.75, 0.39), 'JM': (0.05, 7.1, 2.11), 'OE': (87.11, 91.29, 11.11)},
      ('FY23', M23, m23, 6): {'SM': (0, 19.61, 7.06), 'MM': (0, 19.37, 16.45), 'JM': (66.67, 26.37, 23.57), 'OE': (47.73, 43.66, 44.53)},
      ('FY24', M25, m25, 7): {'SM': (None, 27, 23), 'MM': (100, 13, 9), 'JM': (13, 18, 19), 'OE': (40, 33, 36)},
      ('FY25', M25, m25, 7): {'SM': (0, 15.2, 16.2), 'MM': (0, 13.8, 16.0), 'JM': (35, 19, 18.7), 'OE': (47.6, 31.7, 35.2)}}
for (fy, u, d, pg), dd in tr.items():
    for k, v in dd.items():
        add(F, fy, 'turnover_rate_by_age', v, 'percent', 'Total (vol+invol) turnover rate, level x age: ' + lv[k], u, d, pg,
            'FY22 values do not behave like rates (look like shares; sum >100 for OE); treat as unreliable' if fy == 'FY22' else '')
for fy, u, d, pg, v in [('FY21', M21, m21, 46, (25.0, 22.5, 38.5)), ('FY23', M23, m23, 6, (34.61, 31.33, 12.10)),
                        ('FY24', M25, m25, 7, (28, 23, 10)), ('FY25', M25, m25, 7, (35, 23.3, 14.6))]:
    add(F, fy, 'turnover_rate_by_age', v, 'percent', 'Voluntary turnover rate, level x age: ' + lv['OE'], u, d, pg)
for fy, v, u, d, pg in [('FY20', 27.10, M23, m23, 6), ('FY21', 28.88, M23, m23, 6), ('FY22', 44.17, M25, m25, 7),
                        ('FY23', 43.78, M25, m25, 7), ('FY24', 34.5, M25, m25, 7), ('FY25', 36.7, M25, m25, 7)]:
    add(F, fy, 'turnover_rate_by_age', (v,), 'percent', 'Total employee turnover rate, global (no age split)', u, d, pg, bands=['total'])

# ---------------- Hexaware (calendar year) ----------------
F = 'Hexaware'
H25 = 'https://cdn.hexaware.com/wp-content/uploads/2024/02/Sustainability-Report-2025-Tech-for-People-Planet-and-Progress.pdf'
H23 = 'https://hexaware.com/wp-content/uploads/2024/02/Databook-2023.pdf'
H22 = 'https://hexaware.com/wp-content/uploads/2024/01/Sustainability-Databook-V3-1.pdf'
h25, h23, h22 = 'raw/hexaware/SR_2025.pdf', 'raw/hexaware/Databook-2023.pdf', 'raw/hexaware/databook_v3_1.pdf'
sc = 'Global employee count incl. contract employees (Hexaware IT, BPS, Mobiquity); bands <30 / 30-50 / >50'
add(F, 'CY2021', 'headcount_by_age', (10319, 13090, 757, 24166), 'count', sc, H22, h22, 6)
for fy, v in [('CY2022', (13428, 14230, 950, 28608)), ('CY2023', (11886, 15303, 1103, 28292)),
              ('CY2024', (14312, 17051, 946, 32309)), ('CY2025', (14396, 18098, 1350, 33844))]:
    add(F, fy, 'headcount_by_age', v, 'count', sc, H25, h25, 89, 'calendar-year FY; latest vintage (SR 2025)')
sc = 'Global new hires incl. contract employees'
add(F, 'CY2021', 'hires_by_age', (8972, 6617, 376, 15965), 'count', sc, H22, h22, 5)
for fy, v in [('CY2022', (12448, 6867, 443, 19758)), ('CY2023', (7591, 5067, 258, 12916)),
              ('CY2024', (11492, 6219, 304, 18015)), ('CY2025', (7035, 4490, 281, 11806))]:
    add(F, fy, 'hires_by_age', v, 'count', sc, H25, h25, 90,
        'CY2024 restated: 30-50 and >50 were interchanged in prior disclosure (SR 2025 p6)' if fy == 'CY2024' else '')
sc = 'Voluntary exits of IT employees only (restated basis, SR 2025)'
for fy, v, r in [('CY2022', (1237, 2430, 81, 3748), 24.3), ('CY2023', (940, 1655, 52, 2647), 15.7),
                 ('CY2024', (805, 1221, 58, 2084), 11.9), ('CY2025', (1009, 1253, 60, 2322), 11.7)]:
    add(F, fy, 'turnover_count_by_age', v, 'count', sc, H25, h25, 92, 'restated; earlier databooks reported all exits incl. contract')
    add(F, fy, 'turnover_rate_by_age', (r,), 'percent', sc, H25, h25, 92, 'total rate only', bands=['total'])
sc = 'All exits incl. contract employees (original basis)'
add(F, 'CY2021', 'turnover_count_by_age', (6100, 5268, 264, 11632), 'count', sc, H22, h22, 7, 'superseded basis')
add(F, 'CY2022', 'turnover_count_by_age', (8094, 6844, 378, 15316), 'count', sc, H23, h23, 8, 'superseded basis; same in V3.1 databook p7')
add(F, 'CY2023', 'turnover_count_by_age', (7010, 5845, 378, 13233), 'count', sc, H23, h23, 8, 'superseded basis')
L4 = ['senior', 'middle', 'junior', 'contract', 'total']
lvsc = 'Global; Junior=Trainees,G2-G4 (IT)/Band1-2 (BPS); Middle=SMT,G5-G7/Band3; Senior=G8+/Band4'
add(F, 'CY2021', 'headcount_by_level', (1499, 7868, 13228, 1571, 24166), 'count', lvsc, H22, h22, 6, 'age_band column holds level', bands=L4)
for fy, v in [('CY2022', (1803, 7533, 17565, 1707, 28608)), ('CY2023', (1989, 7862, 16576, 1865, 28292)),
              ('CY2024', (2344, 8992, 18650, 2323, 32309)), ('CY2025', (2641, 10510, 18290, 2403, 33844))]:
    add(F, fy, 'headcount_by_level', v, 'count', lvsc, H25, h25, 89, 'age_band column holds level', bands=L4)
add(F, 'CY2021', 'hires_by_level', (383, 3683, 10449, 1450, 15965), 'count', lvsc, H22, h22, 5, 'extra metric; age_band holds level', bands=L4)
for fy, v in [('CY2022', (372, 2838, 14992, 1556, 19758)), ('CY2023', (240, 1932, 9255, 1489, 12916)),
              ('CY2024', (413, 2567, 12971, 2064, 18015)), ('CY2025', (393, 2820, 7251, 1342, 11806))]:
    add(F, fy, 'hires_by_level', v, 'count', lvsc, H25, h25, 91,
        'extra metric; age_band holds level' + ('; junior printed "1,2971"' if fy == 'CY2024' else ''), bands=L4)

# ---------------- Coforge ----------------
F = 'Coforge'
C25 = 'https://nsearchives.nseindia.com/corporate/COFORGE_07092025222746_SR_Intimation.pdf'
C26 = 'https://esg.coforge.com/hubfs/FY26_Sustainability_Report.pdf?hsLang=en'
c25, c26 = 'raw/coforge/SR_intimation_FY25.pdf', 'raw/coforge/FY26_SR_workforce_pages.pdf (subset of 300MB original)'
sc = 'Total workforce incl. workers, India operations; bands Below 30 / 30-50 incl. / >50'
add(F, 'FY25', 'headcount_by_age', (10051, 16910, 462, 27423), 'count', sc, C26, c26, 79, 'FY26 SR restatement of FY25; page = original page (subset p2)')
add(F, 'FY26', 'headcount_by_age', (10546, 17733, 543, 28822), 'count', sc, C26, c26, 79, 'page = original page (subset p2)')
sc = 'Workforce profile as printed in FY25 SR (scope unstated; standalone)'
add(F, 'FY25 (as printed)', 'headcount_by_age', (5233, 8801, 284, 14318), 'count', sc, C25, c25, 55,
    'column headers likely swapped: text says female rose 3,412 (FY24) -> 7,520 (FY25) but table prints 3,412 under FY25; superseded by FY26 SR')
add(F, 'FY24 (as printed)', 'headcount_by_age', (10659, 15740, 500, 26899), 'count', sc, C25, c25, 55, 'see swap note on FY25 row')
sc = 'Exits of permanent employees, India (regions N/E/W/S)'
add(F, 'FY24', 'turnover_count_by_age', (1345, 2275, 55, 3675), 'count', sc, C25, c25, 70)
add(F, 'FY25', 'turnover_count_by_age', (1322, 2252, 40, 3614), 'count', sc, C25, c25, 70)
sc = 'Voluntary attrition rate, permanent employees, India excl. BPO'
add(F, 'FY25', 'turnover_rate_by_age', (11.5, 10.6, 7.4, 10.8), 'percent', sc, C26, c26, 85, 'page = original (subset p4); FY25 SR headline said 19%, different basis')
add(F, 'FY26', 'turnover_rate_by_age', (11.7, 10.4, 8.8, 10.8), 'percent', sc, C26, c26, 85, 'page = original (subset p4)')

cols = 'firm,fiscal_year,metric,age_band,value,unit,scope,source_url,source_doc,page,status,notes'.split(',')
with open(out, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
print(len(rows), 'rows')
