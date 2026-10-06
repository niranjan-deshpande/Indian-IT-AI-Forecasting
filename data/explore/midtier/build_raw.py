"""Build midtier_raw.csv from values read by hand from primary filings saved under
data/sources/midtier/<firm>/. Every row = one value read from one document (page = PDF page, 1-based).
`primary`=1 marks the headline value used for the firm-year level in midtier_annual.csv;
primary=0 rows are prior-year comparators / restatements used only for same-basis growth."""
import csv, os

OUT = os.path.join(os.path.dirname(__file__), 'midtier_raw.csv')
SRC = 'data/sources/midtier'

P = 'https://www.persistent.com/wp-content/uploads'
C = 'https://investors.coforge.com/hubfs'
M = 'https://www.mphasis.com/content/dam/mphasis-com/global/en/investors/financial-results'
H = 'https://hexaware.com/wp-content/uploads'

docs = {
 # key: (url, title, date, local file)
 'P20': (f'{P}/2020/05/analyst-presentation-and-factsheet-q4-fy20.pdf', 'Persistent Analyst Presentation & Factsheet Q4FY20', '2020-05-05', 'persistent/q4fy20_factsheet.pdf'),
 'P21': (f'{P}/2021/04/analyst-presentation-and-factsheet-q4fy21.pdf', 'Persistent Analyst Presentation & Factsheet Q4FY21', '2021-04-29', 'persistent/q4fy21_factsheet.pdf'),
 'P22': (f'{P}/2022/04/Analyst-Presentation-and-Factsheet-Q4FY22.pdf', 'Persistent Analyst Presentation & Factsheet Q4FY22', '2022-04-27', 'persistent/q4fy22_factsheet.pdf'),
 'P23pr': (f'{P}/2023/04/Press-Release-Q4FY23.pdf', 'Persistent press release Q4FY23 ("Persistent Crosses $1 Billion in Annual Revenue")', '2023-04-25', 'persistent/q4fy23_press_release.pdf'),
 'P24': (f'{P}/2024/04/analyst-presentation-and-factsheet-q4fy24.pdf', 'Persistent Investor Presentation & Factsheet Q4FY24', '2024-04-21', 'persistent/q4fy24_factsheet.pdf'),
 'P25': (f'{P}/2025/04/analyst-presentation-and-factsheet-q4fy25.pdf', 'Persistent Investor Presentation & Factsheet Q4FY25', '2025-04-24', 'persistent/q4fy25_factsheet.pdf'),
 'P26': (f'{P}/2026/04/analyst-presentation-and-factsheet-q4fy26.pdf', 'Persistent Investor Presentation & Factsheet Q4FY26', '2026-04-21', 'persistent/q4fy26_factsheet.pdf'),
 'C20': (f'{C}/Datasheet-Q4FY20.pdf', 'NIIT Technologies (Coforge) Financial and Operational Metrics (Datasheet) Q4FY20', '2020-05-05', 'coforge/Datasheet-Q4FY20.pdf'),
 'C21': (f'{C}/Datasheet-Q4FY21.pdf', 'Coforge Financial and Operational Metrics (Datasheet) Q4FY21', '2021-05-06', 'coforge/Datasheet-Q4FY21.pdf'),
 'C21p': (f'{C}/Investor-presentation-Q4FY21.pdf', 'Coforge Investor Presentation Q4FY21', '2021-05-06', 'coforge/Investor-presentation-Q4FY21.pdf'),
 'C22': (f'{C}/Factsheet-Q4FY22.pdf', 'Coforge Factsheet Q4FY22', '2022-05-12', 'coforge/Factsheet-Q4FY22.pdf'),
 'C23': (f'{C}/Fact-Sheet-Q4FY23.pdf', 'Coforge Fact Sheet Q4FY23', '2023-04-27', 'coforge/Fact-Sheet-Q4FY23.pdf'),
 'C23p': (f'{C}/Investor-Presentation-Q4FY23.pdf', 'Coforge Investor Presentation Q4FY23', '2023-04-27', 'coforge/Investor-Presentation-Q4FY23.pdf'),
 'C24': (f'{C}/Fact-Sheet-Q4FY24.pdf', 'Coforge Fact Sheet Q4FY24 (period ended 31 Mar 2024)', '2024-05-02', 'coforge/Fact-Sheet-Q4FY24.pdf'),
 'C25': (f'{C}/Q4_FY25_Fact_Sheet.pdf', 'Coforge Fact Sheet Q4FY25', '2025-05-05', 'coforge/Q4_FY25_Fact_Sheet.pdf'),
 'C25p': (f'{C}/Q4_FY25_Presentation.pdf', 'Coforge Investor Presentation Q4FY25', '2025-05-05', 'coforge/Q4_FY25_Presentation.pdf'),
 'C26': (f'{C}/Investor-Presentation-and-Factsheet-Q4FY26.pdf', 'Coforge Investor Presentation & Factsheet Q4FY26', '2026-05-05', 'coforge/q4fy26_factsheet.pdf'),
 'M20t': (f'{M}/2020/q4-transcript-of-earnings-call.pdf', 'Mphasis Q4 & FY2020 earnings call transcript', '2020-05-14', 'mphasis/q4fy20_transcript.pdf'),
 'M21': (f'{M}/2021/q4-group-overview-md-a.pdf', 'Mphasis Group Financial Overview and Trends (MD&A), quarter ending 31 Mar 2021', '2021-05 (PDF created 2021-05-08)', 'mphasis/q4fy21_mda.pdf'),
 'M22': (f'{M}/2022/q4-group-overview-mda.pdf', 'Mphasis Group Financial Overview and Trends (MD&A) Q4FY22', '2022-04-28', 'mphasis/q4fy22_mda.pdf'),
 'M23': (f'{M}/2023/q4-group-overview-mda.pdf', 'Mphasis Group Financial Overview and Trends (MD&A) Q4FY23', '2023-04-27', 'mphasis/q4fy23_mda.pdf'),
 'M24': (f'{M}/2024/q4-group-overview-mda.pdf', 'Mphasis Group Financial Overview and Trends (MD&A) Q4FY24', '2024-04-25', 'mphasis/q4fy24_mda.pdf'),
 'M25': (f'{M}/2025/q4-group-overview-mda.pdf', 'Mphasis Group Financial Overview and Trends (MD&A) Q4FY25', '2025-04-24', 'mphasis/q4fy25_mda.pdf'),
 'M26': (f'{M}/2026/q4-group-overview-mda.pdf', 'Mphasis Group Financial Overview and Trends (MD&A) Q4FY26', '2026-04-29', 'mphasis/q4fy26_mda.pdf'),
 'M22pr': (f'{M}/2022/q4-earnings-press-release.pdf', 'Mphasis earnings press release Q4FY22', '2022-04-28', 'mphasis/q4fy22_press_release.pdf'),
 'M23pr': (f'{M}/2023/q4-earnings-press-release.pdf', 'Mphasis earnings press release Q4FY23', '2023-04-27', 'mphasis/q4fy23_press_release.pdf'),
 'M24pr': (f'{M}/2024/q4-earnings-press-release.pdf', 'Mphasis earnings press release Q4FY24', '2024-04-25', 'mphasis/q4fy24_press_release.pdf'),
 'M25pr': (f'{M}/2025/q4-earnings-press-release.pdf', 'Mphasis earnings press release Q4FY25', '2025-04-24', 'mphasis/q4fy25_press_release.pdf'),
 'M26pr': (f'{M}/2026/q4-earnings-press-release.pdf', 'Mphasis earnings press release Q4FY26', '2026-04-29', 'mphasis/q4fy26_press_release.pdf'),
 'H19': (f'{H}/2019/11/Annual-Report-2019.pdf', 'Hexaware Technologies Annual Report 2019 (FY = CY2019)', '2020 (PDF created 2020-06-11)', 'hexaware/Annual-Report-2019.pdf'),
 'H20': (f'{H}/2019/11/Annual-Report-2020.pdf', 'Hexaware Technologies Annual Report 2020 (FY = CY2020)', '2021 (PDF created 2021-03-30)', 'hexaware/Annual-Report-2020.pdf'),
 'H21': (f'{H}/2019/11/Annual-Report-2021.pdf', 'Hexaware Technologies Annual Report 2021 (FY = CY2021)', '2022 (PDF created 2022-04-04)', 'hexaware/Annual-Report-2021.pdf'),
 'HRHP': (f'{H}/2025/02/Red-Herring-Prospectus.pdf', 'Hexaware Technologies Red Herring Prospectus', '2025-02-05', 'hexaware/Red-Herring-Prospectus_2025-02-05.pdf'),
 'H24': (f'{H}/2025/03/Earnings-Press-Release.pdf', 'Hexaware earnings press release Q4CY24 ("Hexaware Delivers Strong CY24 Performance...")', '2025-03-06', 'hexaware/q4cy24_earnings_press_release.pdf'),
 'H25': (f'{H}/2025/02/Investor-Presentation-Q4_2025.pdf', 'Hexaware Investor Presentation Q4CY25', '2026-02-04', 'hexaware/q4cy25_investor_presentation.pdf'),
}

R, HC, CC, INR = 'revenue_usd_mn', 'headcount', 'cc_growth_pct', 'revenue_inr_mn'
# (firm, fy, period_end, metric, value, unit, basis, doc, loc, notes, primary)
rows = [
 # ---------------- Persistent ----------------
 ('persistent','FY19','2019-03-31',R,480.97,'USD mn','reported_consolidated','P20','p15 Fact Sheet "Revenue from Operations, USD M" FY19 col','prior-year comparator',0),
 ('persistent','FY19','2019-03-31',HC,9962,'persons','total_employees','P20','p19 Fact Sheet People Numbers "Total" FY19 col','prior-year comparator',0),
 ('persistent','FY20','2020-03-31',R,501.61,'USD mn','reported_consolidated','P20','p15 Fact Sheet "Revenue from Operations, USD M" FY20 col','',1),
 ('persistent','FY20','2020-03-31',HC,10632,'persons','total_employees','P20','p19 Fact Sheet People Numbers "Total" (Technical+Sales&BD+Others) Q4FY20','contractors/trainees not stated',1),
 ('persistent','FY21','2021-03-31',R,566.08,'USD mn','reported_consolidated','P21','p29 Fact Sheet "Revenue from Operations, USD M" FY21 col','',1),
 ('persistent','FY21','2021-03-31',HC,13680,'persons','total_employees','P21','p32 Fact Sheet People Numbers "Total" Q4FY21','',1),
 ('persistent','FY22','2022-03-31',R,765.59,'USD mn','reported_consolidated','P22','p29 consolidated P&L "Revenue ($ M)" FY22 (p32 fact sheet shows 765.6)','FY22 acquisitions: Software Corporation International, Data Glove, MediaAgility, Shree Partners & Sureline assets (p23 acquisitions slide)',1),
 ('persistent','FY22','2022-03-31',HC,18599,'persons','total_employees','P22','p34 Fact Sheet People Numbers "Total" Q4FY22','',1),
 ('persistent','FY23','2023-03-31',R,1035.98,'USD mn','reported_consolidated','P23pr','p1 table "Revenue (USD Million)" FY23','',1),
 ('persistent','FY23','2023-03-31',HC,22889,'persons','total_employees','P24','p47 Fact Sheet People Numbers "Total" Q4FY23/FY23 col','FY23 own press release only says "over 22,750 employees" (p5); exact figure from FY24 factsheet comparator',1),
 ('persistent','FY24','2024-03-31',R,1186.05,'USD mn','reported_consolidated','P24','p41 consolidated P&L "Revenue ($ M)" FY24 (p44 fact sheet 1,186.0)','',1),
 ('persistent','FY24','2024-03-31',HC,23850,'persons','total_employees','P24','p47 Fact Sheet People Numbers "Total" Q4FY24','',1),
 ('persistent','FY25','2025-03-31',R,1409.1,'USD mn','reported_consolidated','P25','p47 Fact Sheet "Revenue from Operations, $M" FY25 col','',1),
 ('persistent','FY25','2025-03-31',HC,24594,'persons','total_employees','P25','p50 Fact Sheet People Numbers "Total" Q4FY25','',1),
 ('persistent','FY26','2026-03-31',R,1654.4,'USD mn','reported_consolidated','P26','p46 Fact Sheet "Revenue from Operations, $M" FY26 col','',1),
 ('persistent','FY26','2026-03-31',HC,27502,'persons','total_employees','P26','p49 Fact Sheet People Numbers "Total" Q4FY26','',1),
 # ---------------- Coforge ----------------
 ('coforge','FY19','2019-03-31',HC,10263,'persons','grand_total','C20','p6 People Numbers "Grand Total" Q4FY19 col','includes 89 GIS sales staff (GIS business sold Apr 2019)',0),
 ('coforge','FY20','2020-03-31',INR,41839,'INR mn','continuing_ex_GIS','C20','p5 "Revenue - Continuing Business" FY 2020','USD annual revenue NOT reported in FY20 datasheet/presentation/transcript (only "about $600 million" in call); USD left blank',1),
 ('coforge','FY20','2020-03-31',HC,11156,'persons','grand_total','C20','p6 People Numbers "Grand Total" Q4FY20','billable + S&M + others',1),
 ('coforge','FY21','2021-03-31',R,627.7,'USD mn','reported_consolidated','C22','p6 "Revenue (USD Mn)" FY2021 col','FY21 own docs give only INR 46,628 mn and "+6.0% in $ terms"; USD level from FY22 factsheet comparator',1),
 ('coforge','FY21','2021-03-31',HC,12391,'persons','grand_total','C21','p6 People Numbers "Grand Total" Q4FY21','',1),
 ('coforge','FY21','2021-03-31',CC,6.0,'%','reported_consolidated','C21p','p4 "Up 6.0% in constant currency"','',1),
 ('coforge','FY22','2022-03-31',R,866.5,'USD mn','reported_consolidated','C22','p6 "Revenue (USD Mn)" FY2022 col','',1),
 ('coforge','FY22','2022-03-31',HC,22500,'persons','grand_total','C22','p7 People Data "Grand Total" Q4FY22','LEVEL BREAK: BPS billable 393 (Q4FY21) -> 6,391 (Q4FY22) (p7) = BPS acquisition (SLK Global per general knowledge; name not verified in opened docs)',1),
 ('coforge','FY23','2023-03-31',R,1001.7,'USD mn','reported_consolidated','C23','p6 "Revenue (USD Mn)" FY2023 col','',1),
 ('coforge','FY23','2023-03-31',HC,23224,'persons','grand_total','C23','p7 People Data "Grand Total" Q4FY23','',1),
 ('coforge','FY23','2023-03-31',CC,22.4,'%','reported_consolidated','C23p','p13 "FY23 ... CC revenue growth of 22.4%" (also C24 p6)','',1),
 ('coforge','FY24','2024-03-31',R,1118.7,'USD mn','reported_consolidated','C24','p6 "Revenue (USD Mn)" FY2024 col','',1),
 ('coforge','FY24','2024-03-31',HC,24726,'persons','grand_total','C24','p7 People Data "Grand Total" Q4FY24','',1),
 ('coforge','FY24','2024-03-31',CC,13.3,'%','reported_consolidated','C24','p6 "Q-o-Q CC Revenue Growth" row, FY2024 col (annual CC)','',1),
 ('coforge','FY25','2025-03-31',R,1468,'USD mn','reported_consolidated_incl_AdvantageGo','C25','p2 "Revenue (USD Mn)" FY25 col (C25p p4: "Reported revenue ... $1,468 Mn")','includes Cigniti (54% acquired 2024; balance sheet "Incl Cigniti" at 30 Jun 2024 in Q1FY25 fact sheet); LEVEL BREAK',1),
 ('coforge','FY24','2024-03-31',R,1119,'USD mn','reported_consolidated_incl_AdvantageGo','C25','p2 "Revenue (USD Mn)" FY24 col','prior-year comparator (= FY24 reported 1,118.7)',0),
 ('coforge','FY25','2025-03-31',R,1445.2,'USD mn','continuing_ex_AdvantageGo_FY25pres','C25p','p19 "Gross Revenues" USD FY25 continuing (FY24 continuing 1,099.3)','continuing = Coforge minus AdvantageGo (divested)',0),
 ('coforge','FY25','2025-03-31',R,1448,'USD mn','continuing_ex_AdvantageGo','C26','p45 Factsheet "Revenue (USD Mn)" FY25 col (restated)','restated comparator in FY26 factsheet (continuing ops)',0),
 ('coforge','FY25','2025-03-31',HC,33497,'persons','grand_total','C25','p4 People Data "Grand Total" Q4FY25','includes Cigniti',1),
 ('coforge','FY25','2025-03-31',HC,33023,'persons','grand_total_restated_FY26','C26','p46 People Data "Grand Total" Q4FY25 col (restated)','restated in FY26 factsheet; reason not stated (likely AdvantageGo divestiture)',0),
 ('coforge','FY25','2025-03-31',CC,32.0,'%','continuing_ex_AdvantageGo','C25','p2 "Q-o-Q CC Revenue Growth" row FY25 col; C25p p4 "up by 32.0% on a constant currency basis" (continuing)','',1),
 ('coforge','FY26','2026-03-31',R,1870,'USD mn','continuing_ex_AdvantageGo','C26','p45 Factsheet "Revenue (USD Mn)" FY26 col (p4 headline $1,870.3 Mn; YoY 29.2%)','pre-Encora (Encora consolidated FY27)',1),
 ('coforge','FY26','2026-03-31',HC,35777,'persons','grand_total_restated_FY26','C26','p46 People Data "Grand Total" Q4FY26','',1),
 # ---------------- Mphasis ----------------
 ('mphasis','FY20','2020-03-31',R,1239.6,'USD mn','gross_revenue','M21','p7 KPI "Gross Revenue ($ Mn)" FY20 col','FY20 own MD&A not retrievable (404); value from FY21 MD&A comparator',1),
 ('mphasis','FY20','2020-03-31',HC,26398,'persons','total_incl_billable_contractors','M21','p14 "Total headcount**" Q4FY20 col','**includes billable contractors, S&M and G&A employees',1),
 ('mphasis','FY20','2020-03-31',CC,11.7,'%','gross_revenue','M20t','p3 "FY20 gross revenue grew 12.8% YoY reported and 11.7% in constant currency"','',1),
 ('mphasis','FY21','2021-03-31',R,1308.9,'USD mn','gross_revenue','M21','p7 KPI "Gross Revenue ($ Mn)" FY21 col','',1),
 ('mphasis','FY21','2021-03-31',HC,29473,'persons','total_incl_billable_contractors','M21','p14 "Total headcount**" Q4FY21','',1),
 ('mphasis','FY21','2021-03-31',CC,4.9,'%','gross_revenue','M21','p2 "FY 21 Gross revenue grew 9.8% reported and 4.9% in Constant Currency"','DXC channel revenue -33.0% CC',1),
 ('mphasis','FY22','2022-03-31',R,1593.0,'USD mn','gross_revenue','M22','p7 KPI "Gross Revenue ($ Mn)" FY22 col','includes Blink UX (acq. Q3FY22, per p13 note)',1),
 ('mphasis','FY22','2022-03-31',HC,36534,'persons','total_incl_billable_contractors','M22','p14 "Total headcount**" Q4FY22','',1),
 ('mphasis','FY22','2022-03-31',CC,21.2,'%','gross_revenue','M22pr','p1 "FY22 revenue grew 22.4% reported and 21.2% in Constant Currency"','',1),
 ('mphasis','FY23','2023-03-31',R,1717.7,'USD mn','gross_revenue','M23','p7 KPI "Gross Revenue ($ Mn)" FY23 col','',1),
 ('mphasis','FY23','2023-03-31',HC,34042,'persons','total_incl_billable_contractors','M23','p14 "Total headcount**" Q4FY23','',1),
 ('mphasis','FY23','2023-03-31',CC,9.7,'%','gross_revenue','M23pr','p1 "FY23 revenue grew 16.7% reported and 9.7% in Constant Currency"','',1),
 ('mphasis','FY24','2024-03-31',R,1609.5,'USD mn','gross_revenue','M24','p7 KPI "Gross Revenue ($ Mn)" FY24 col','includes Silverline (acquired FY24; FY24 deck p5/p11 "post acquisition")',1),
 ('mphasis','FY24','2024-03-31',HC,32664,'persons','total_incl_billable_contractors','M24','p14 "Total headcount**" Q4FY24','',1),
 ('mphasis','FY24','2024-03-31',CC,-6.5,'%','gross_revenue','M24pr','p1 "FY 2024 revenue declined 3.7% reported and 6.5% in Constant Currency"','',1),
 ('mphasis','FY25','2025-03-31',R,1680.8,'USD mn','gross_revenue','M25','p7 KPI "Gross Revenue ($ Mn)" FY25 col','',1),
 ('mphasis','FY25','2025-03-31',HC,31442,'persons','total_incl_billable_contractors','M25','p14 "Total headcount**" Q4FY25','FY25 footnote adds "and excludes interns"; Q4FY24 comparator unchanged at 32,664',1),
 ('mphasis','FY25','2025-03-31',CC,4.6,'%','gross_revenue','M25pr','p1 "FY25 revenue grew 6.7% reported and 4.6% in Constant Currency"','',1),
 ('mphasis','FY26','2026-03-31',R,1796.4,'USD mn','gross_revenue','M26','p4 KPI "Revenue ($ Mn)" FY26 col','',1),
 ('mphasis','FY26','2026-03-31',HC,31179,'persons','total_incl_billable_contractors','M26','p7 "Total headcount**" Q4FY26','excludes interns',1),
 ('mphasis','FY26','2026-03-31',CC,6.7,'%','gross_revenue','M26','p4 KPI "Constant Currency (%)" FY26 (also M26pr p1)','',1),
 # ---------------- Hexaware (FY = calendar year) ----------------
 ('hexaware','CY2018','2018-12-31',R,677.67,'USD mn','consolidated','H19','p129 MD&A "to US$ 793.26 million in FY 2019 from US$ 677.67 million"','prior-year comparator',0),
 ('hexaware','CY2018','2018-12-31',HC,16205,'persons','incl_contractors','H19','p129 MD&A "headcount of 16,205 as of December 2018"','prior-year comparator',0),
 ('hexaware','CY2019','2019-12-31',R,793.26,'USD mn','consolidated','H19','p129 MD&A (also p46 table "Income from Operations" US$ mn)','Hexaware FY = Jan-Dec; Mobiquity acquired (all-cash US$182 mn deal "in 2019" per AR2020 p7)',1),
 ('hexaware','CY2019','2019-12-31',HC,19999,'persons','incl_contractors','H19','p129 MD&A "worldwide employee count including subcontractors was 19,999 as of December 2019"','',1),
 ('hexaware','CY2019','2019-12-31',CC,18.2,'%','consolidated','H19','p129 MD&A "revenue in constant currency was US$ 801.30 million, growth of 18.2%"','',1),
 ('hexaware','CY2020','2020-12-31',R,845.04,'USD mn','consolidated','H20','p40 MD&A "Income from Operations" US$ mn 2020 col','delisted from NSE/BSE late 2020; AR still published',1),
 ('hexaware','CY2020','2020-12-31',HC,19833,'persons','incl_contractors','H20','p39 MD&A "worldwide employee count including subcontractors was 19,833"; p60 BRR "19,833 including subsidiaries and contract employees"','',1),
 ('hexaware','CY2020','2020-12-31',HC,18686,'persons','excl_subcontractors','H21','p86 MD&A "headcount of 18,686 as on December 31, 2020" (excl. subcontractors)','alternate basis comparator',0),
 ('hexaware','CY2020','2020-12-31',CC,5.4,'%','consolidated','H20','p40 MD&A "Revenue in constant currency was US$ 844.50 million in 2020, growth of 5.4%"','',1),
 ('hexaware','CY2021','2021-12-31',R,971.2,'USD mn','consolidated','HRHP','PDF p259 (printed p255) KPI table "Revenue from Operations (in $ million)" FY2021 (=CY2021)','AR2021 p86/p88: US$971.16 mn (same basis)',1),
 ('hexaware','CY2021','2021-12-31',R,971.16,'USD mn','consolidated_AR','H21','p88 "Income from Operations" US$ mn 2021 col','alternate (AR2021)',0),
 ('hexaware','CY2021','2021-12-31',HC,24166,'persons','incl_contractors','HRHP','PDF p260 KPI "Total number of employees (headcount)" 31-Dec-2021; p344 (22,659 FTE + 1,507 contractors)','RHP def: full-time employees + contractors',1),
 ('hexaware','CY2021','2021-12-31',HC,22544,'persons','excl_subcontractors','H21','p86 MD&A "employee count excluding subcontractors was 22,544 as on December 31, 2021"','alternate basis',0),
 ('hexaware','CY2021','2021-12-31',CC,15.1,'%','consolidated','H21','p86 MD&A "revenue in constant currency was US$972.93 million, growth of 15.1%"','p89 of same AR says 15.2%',1),
 ('hexaware','CY2022','2022-12-31',R,1165.0,'USD mn','consolidated','HRHP','PDF p259 KPI table "Revenue from Operations (in $ million)" FY2022','',1),
 ('hexaware','CY2022','2022-12-31',HC,28608,'persons','incl_contractors','HRHP','PDF p260 KPI headcount; p344 (26,901 FTE + 1,707 contractors)','',1),
 ('hexaware','CY2023','2023-12-31',R,1256.4,'USD mn','consolidated','HRHP','PDF p259 KPI table FY2023 (also H24 p5)','',1),
 ('hexaware','CY2023','2023-12-31',HC,28292,'persons','incl_contractors','HRHP','PDF p260 KPI headcount; p344 (26,527 FTE + 1,765 contractors)','consistent with H24 p2 "net added 4,017 since Q4CY23"',1),
 ('hexaware','CY2024','2024-12-31',R,1428.9,'USD mn','consolidated','H24','p5 "Revenue (USD Mn)" CY24 col','relisted on NSE/BSE Feb 2025; includes Softcrylic (subsidiary by 30 Sep 2024 per RHP; business-acquisition outflow INR 8,268 mn p7)',1),
 ('hexaware','CY2024','2024-12-31',HC,32309,'persons','incl_contractors','H24','p2 "Closing Headcount: 32,309"','definition not restated in release; assumed same as RHP (FTE+contractors)',1),
 ('hexaware','CY2024','2024-12-31',CC,13.5,'%','consolidated','H24','p1 "Constant Currency Growth ... CY24 YoY 13.5%"','',1),
 ('hexaware','CY2025','2025-12-31',R,1537.4,'USD mn','consolidated','H25','p20 "Revenue (USD Mn)" CY25 col; p4 "CY25: USD 1,537.4 Mn"','CY25 cash flow shows payment for acquisition of business INR 7,452 mn (p30)',1),
 ('hexaware','CY2025','2025-12-31',HC,33844,'persons','incl_contractors','H25','p4 "Closing Headcount: 33,844"; p10 chart','',1),
 ('hexaware','CY2025','2025-12-31',CC,7.1,'%','consolidated','H25','p4 "Constant Currency : +7.1% YoY" (CY25)','',1),
]

with open(OUT, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['firm','fiscal_year','period_end','metric','value','unit','basis','source_url','source_doc','doc_date','source_loc','notes','primary','local_file'])
    for (firm, fy, pe, met, val, unit, basis, d, loc, notes, prim) in rows:
        url, title, date, lf = docs[d]
        assert os.path.exists(os.path.join(os.path.dirname(__file__), '..', '..', 'sources', 'midtier', lf)), lf
        w.writerow([firm, fy, pe, met, val, unit, basis, url, title, date, loc, notes, prim, f'{SRC}/{lf}'])
print('wrote', OUT, len(rows), 'rows')
