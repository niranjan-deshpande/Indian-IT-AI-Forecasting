# Discriminating data: a screen of sources that could separate S1–S4

*Screened 2026-10-05. Scenarios and identity as in `NEXT_STEPS.md` §3: R = pQ, L = aQ/u, so g_{R/L} = g_u + (g_p − g_a).*
- S1: client demand fell.
- S2: labour per unit fell and prices held.
- S3: labour per unit fell and the savings were passed through as lower prices.
- S4: the work moved to client GCCs or to subcontractors.

Effort and rate data measure a·Q and p/a, so they cannot separate S1 from S3.

**Verification key.**
- **V** = re-checked in this pass by me against the primary document; the quote or number was matched.
- **A** = checked in this pass by a research sub-agent that fetched the source; not independently re-checked.
- **R** = repo data inspected.
- **N** = not verified (source blocked, or claim second-hand).

**Figure labels.**
- *measured* = official or company-reported.
- *estimated* = consultancy or model estimate.
- *commentary* = qualitative or survey opinion.

**Corrections to earlier repo claims found in this pass:**
1. **The RBI software-exports survey has FY2017-18; the repo's `rbi_survey_orgtype.csv` and trade `FINDINGS.md` ("FY18 missing") omit it.** Values: Private Ltd 51.7%, Public Ltd 47.5%, Others 0.8%, total US$108.4bn. Source: [RBI PR prid=48664](https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=48664), 18 Nov 2019, "Survey on Computer Software and ITES Exports: 2018-19", Table 4 (**V**).
   - All other CSV rows match their cited releases (**A**; FY09–13 and FY2017-19 re-checked **V**).
   - Two minor vintage notes:
     - FY2020-21 was first published as 52.9/44.8/2.3 (prid 52258, 20 Sep 2021). The CSV's 53.0/2.2 is the revised vintage in prid 54338.
     - FY2024-25 was first released in prid 61562 (4 Nov 2025). The CSV cites the Sep-2026 release, which repeats the same values.
2. **`core_quarterly.csv` `subcon` is not INR for TCS.** It is USD mn (COR + SG&A), divided by `rev_usd`. The other firms are INR / `rev_inr`. The share is unaffected; the new series uses INR throughout (**R**).
3. **LTIMindtree does disclose sub-contracting, annually.** `ltim_NOTES.md` says it is not reported, which holds for quarterly results only. The consolidated figure appears in each annual report's Board's Report "Financial Results" table (**V**; see (b)).
4. **The Nasscom-Zinnov GCC headcount series cannot be chained across editions.** Nasscom "restated the GCC industry revenues and headcount in September 2024" (Strategic Review 2025 press release, 24 Feb 2025) (**A**). Implied growth rates across the 2023, 2024 and 2026 editions are mutually inconsistent (details in row 1a). The repo's "2.36m in FY26" figure is correct (**V**) but is not comparable with the FY23 1.66m.
5. **The JobSpeak URL pattern `Naukri-Jobspeak-<Mon>-<YYYY>.pdf` no longer works for every month** (`workforce/FINDINGS.md`). `Sep-2026` and `Aug-2026` return 404; `September-2026` and `August-2026` return 200; `Mar-2026` works (**V**, curl status codes).
6. **The repo LCA extract (`lca_cases_target_firms.csv.gz`) dropped `SECONDARY_ENTITY` / `SECONDARY_ENTITY_BUSINESS_NAME`.** These are the client-site fields (**R**; existence of the field in the DOL record layout: **A**).

**Bottom line.**
- **Most promising free sources for S1 vs S4:**
  - RBI FLA census Table 9C (exports of foreign subsidiaries in I&C, annual);
  - BEA MOFA India employment by industry (annual; 2024 due Nov 2026);
  - the Naukri JobSpeak GCC vs IT-services split (monthly postings; YoY only in 2026);
  - MCA filings of named GCC entities (₹100 per company).
- **S1 vs S3:** nothing public. Output prices, renewal re-pricing and service-line incidence are not published (see (c)). The best public partial measures are firm client-band counts and the US OEWS occupation mix within NAICS 5415.
- **S2 vs S4 (subcontractors):** the firm subcontracting series in (b) is the direct test. **It fell in FY24–25 and rebounded modestly in FY26.** There was no shift of work from employees to subcontractors when headcount slowed.

## (a) Source screen

Columns follow the brief. "Pair" = the scenario pair the source can help separate. Access URLs are as fetched on 2026-10-05.

### GCCs and where the work went (S4)

| # | source | scenario pair(s) | mechanism | frequency | coverage | free / paid | access | verification + citation | notes |
|--|--|--|--|--|--|--|--|--|--|
| 1a | **Nasscom-Zinnov India GCC Landscape** (GCC 4.0, 2023; "5-Year Journey", 2024; "GCC Value Orbit", 2026) | S1 vs S4 | Total GCC headcount rising while vendor headcount stalls means work exists elsewhere (S4); under S1 both should slow | ~biennial, plus half-yearly/quarterly "trends" notes (no quarterly note found after Q4 CY2023) | FY19–FY26 reference years, by edition | 2026 edition **free with business email**; 2023/2024 reports ₹20,000 each | [Zinnov 2026 page](https://zinnov.com/centers-of-excellence/zinnov-nasscom-india-gcc-landscape-2026-report/); nasscom.in knowledge-center publication pages | **Exists, but differs: estimated, not measured; series breaks.** Figures by edition (all *estimated*):<br>• FY23: 1,580+ GCCs, 1.66M+ (GCC 4.0, 1 Jun 2023) (A)<br>• FY24: 1,700+ GCCs / 2,975+ units, 1.9M+, $64.6bn (Sep 2024) (A)<br>• FY26: 2,117 GCCs / 3,728 units, 2.36M talent, $98.4bn, "32% growth since FY2021" (V, Zinnov page) | Method: "200+ primary interviews… 1M+ GCC job postings" plus Zinnov's tracking database (V). Breakdowns by city, industry, function and maturity; **not by parent company** in the free material (A). Editions are inconsistent (A, agent arithmetic):<br>• the FY23→FY24 revenue jump of +40% reflects the restatement<br>• 6.2%/yr since FY21 implies ~1.75M in FY21, above the FY23 1.66M<br>Treat as a level indicator only. |
| 1b | **Nasscom Strategic Review** (annual, Feb) | S1 vs S4 (weak) | Industry totals **include** GCCs; vendor share = total − GCC | annual | FY24 restated onward | ₹50,000 (2026) / ₹40,000 (2025); free executive summary | nasscom.in | **Exists, but differs.** FY26E revenue $315bn; employment ~6.0M, +2.3% (+135k) (*estimated*). Export revenue split 50/50 between "Global MNCs (including GCCs)" and Indian providers (A) | No GCC vs vendor headcount split; the MNC bucket also holds Accenture, Cognizant and Capgemini. |
| 1c | **Economic Survey 2024-25 (ch. 8, para 8.30) and 2025-26 (para 7.33, Chart VII.12)** | — | — | annual | FY19–FY24 | free | indiabudget.gov.in | **Exists, but not an independent statistic.** It reprints NASSCOM: 1,430→1,700 GCCs; 14→19 lakh staff (FY19–FY24E) (A) | The government publishes no measured GCC employment statistic. The FY19 GCC count is 1,430 here vs 1,285 in Nasscom-Zinnov 2024 (A). |
| 1d | **EY GCC Pulse Survey 2025** (23 Nov 2025) | S2 vs S4 (subcontractor variant) | Shows whether GCCs themselves outsource back to vendors | annual | 2024–2025 | free PDF | ey.com | **Exists** (A). *Commentary* (n≈65 GCC leaders): in-house delivery 84%; GCC outsourcing 8%→12% | If GCCs re-outsource, S4 to GCCs is partly offset. |
| 1e | **ANSR "Talent Trends in GCCs in India"** (24 Sep 2026) | S1 vs S4 | GCC hiring vs vendor hiring | ad hoc | H1 2026 | press release free | GlobeNewswire | **Exists** (A). *Estimated*: 1,900+ GCCs, 2.1M+ staff; GCC hiring +12–15% YoY in H1 2026 | Conflicts with Nasscom-Zinnov (2,117 / 2.36M) for the same period. |
| 1f | Deloitte (Jul 2025), Everest, Bain (2017) GCC reports | — | — | ad hoc | — | Everest paid; others free | — | **Exists** (A). No new independent counts: Deloitte reuses Nasscom figures; Bain's last is 2017 (~1,100 centres, 800k+, *estimated*) | Context only. |
| 1g | **MCA21 filings of GCC entities** (AOC-4 financial statements; board reports) | S1 vs S4; S2 vs S4 (GCC subcontracting line) | Per-entity employee-benefit expense (and, from FY25 board reports, employee counts by gender) for named captives, e.g. JPMorgan, Goldman or Walmart India entities. Sum across a panel of large GCCs and compare with vendor headcount | annual | ~FY15– (electronic filings) | **Paid per document**: electronic inspection ₹100 per company per inspection; certified copies ₹25/page (Companies (Registration Offices and Fees) Rules 2014, fee table §IV) (A) | mca.gov.in (returned HTTP 403 to the agent) | **Exists; partly unverified.** The fee rules were read (A). The employee-count requirement in board reports (from 14 Jul 2025, Companies (Accounts) Amendment Rules 2025) is per Khaitan & Co commentary only (**N** for primary text) | The only free/cheap entity-level route to GCC employment. Needs a curated list of GCC CINs. Cost is roughly ₹100 × entities × years. |
| 1h | **data.gov.in Company Master Data** | (sampling frame for 1g) | CIN, class, activity code, ROC; possibly a foreign-company / subsidiary flag | periodic | — | free | data.gov.in | **Exists per search; site returned 503** (N) | No employees or financials. |
| 1i | **RBI Census on Foreign Liabilities and Assets (FLA)**: Table 9C "Activity-wise Export of Foreign subsidiary companies in India" | **S1 vs S4** (best official proxy found) | Exports by foreign-owned subsidiaries in "Information and communication", compared with total software exports and with the large vendors' revenue. Captive exports rising while vendor exports stall = S4 | annual (provisional release ~September) | 2022-23 round verified (with 2021-22 comparative); other rounds not located (search budget exhausted) | free (HTML press release) | [RBI PR prid=56359](https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=56359), 12 Sep 2023 | **Verified (V).** *Measured*: I&C exports of 22,395 foreign subsidiaries were ₹6,53,856 cr (2021-22) and ₹8,45,021 cr (2022-23). That is 51.6% of all foreign-subsidiary exports and 71.3% of those firms' I&C sales | Caveats:<br>• "I&C" includes telecom and publishing.<br>• "Foreign subsidiary" includes foreign-owned **vendors** (Accenture, Cognizant, Capgemini India), not only captives.<br>• No employment.<br>Next step: locate the 2016-17 to 2025-26 rounds on the RBI press-release archive. |
| 1j | **RBI "Finances of FDI Companies" 2024-25** (prid 62601, 22 Apr 2026) | S1 vs S4 (possible) | Financial statements of ~3,100 FDI companies by industry; possibly an exports line | annual | — | free (data.rbi.org.in) | RBI DBIE | **Exists** (A); exports and industry detail **not verified** (N) | Check for an NIC 62 cut and an export-earnings item. |
| 1k | **Karnataka GCC Policy 2024–29** | — | — | one-off | 2024 | free | state govt (read via a mirror PDF) | **Exists** (A). 875+ GCC units and 0.6M+ talent in Karnataka (*estimated*; sources: Nasscom-Zinnov, ANSR, JLL, EY) | Not independent. |

### Trade statistics (S1 vs S4, aggregate demand)

| # | source | scenario pair(s) | mechanism | frequency | coverage | free / paid | access | verification + citation | notes |
|--|--|--|--|--|--|--|--|--|--|
| 4a | **RBI Survey on Computer Software & ITES Exports**, organisation-type table | S1 vs S4 (weak proxy) | Private-limited share (GCCs + foreign vendors + small domestic firms) vs public-limited share (includes all six large vendors); total exports vs vendor revenue | annual (release ~Sep–Nov, ~6-month lag) | FY09–FY26 (FY09–13 earlier method) | free | RBI press releases (HTML; PDFs/xlsx on rbidocs sit behind a CAPTCHA) | **Exists as described; categories confirmed.** The exact labels are "Private Limited Company", "Public Limited Company" and "Others" ("Others include mostly LLPs/proprietor firms", from 2019-20) (A; FY2017-19 table V). **No foreign-owned, affiliate or GCC category in any release checked** (A). *Measured*: FY26 total $221.4bn; private 60.8%, public 36.9% ([prid 63625](https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63625), 18 Sep 2026) (A) | The questionnaire collects **employee numbers (Q16)** and **billing to subsidiaries/associates abroad**, but neither is published (RBI survey FAQ, updated 1 Jun 2026) (A). |
| 4b | Same survey: "Software Business by Foreign Affiliates of Indian Companies" (Mode 3) | S1 vs S4 (vendor-internal shift) | Indian firms' overseas subsidiaries delivering locally; shows work moving onsite-abroad within the vendor, not to GCCs | annual | — | free | as 4a | **Exists** (A). *Measured*: Mode 3 "locally" $13.9bn (FY25), $17.9bn (FY26) (A, not re-checked) | Does not concern GCCs. |
| 4c | **RBI quarterly BoP / "Data on India's Invisibles"** (BPM6) software services | S1 (aggregate India-delivered demand) vs firm-specific shocks | India-wide software receipts vs the six firms' revenue | quarterly (~3-month lag) | 2004Q1–2026Q2 (repo has the IMF-API version) | free (xlsx behind CAPTCHA; repo used IMF API) | rbi.org.in; IMF API | **Exists, but current table not opened** (blocked). A "software services receipts" line is evidenced in RBI Bulletin Oct 2010 (Id=11605) (A) | Repo: `trade/imf_bop_india_services_quarterly.csv`. |
| 4d | RBI monthly services trade | — | — | monthly (~30-day lag) | — | free | RBI PR (e.g. prid 63699, 30 Sep 2026) | **Exists; total services only, no software split** (A) | Not useful. |
| 11a | **BEA Table 2.3**, US trade in services by country and affiliation (India) | S1 vs S4 (weak) | US imports of computer services from India | annual (Jul) | 1999–2025 | free | apps.bea.gov iTable / CSV | **Exists, but differs: no India × affiliation split for computer services.** For India, affiliation is split only for IP charges (A). *Measured*: computer services from India $13,643m (2023), $15,888m (2024), $18,020m (2025) (A). Affiliated computer-services imports all-countries only ($47,337m, 2025) | Confirms the repo trade finding (BEA C&M §31.8). |
| 11b | **BEA AMNE/MOFA**: employment of majority-owned foreign affiliates, country × industry | S1 vs S4 | US-parent captives' India employment (includes US-HQ vendors such as Cognizant, IBM, Accenture's US parent) | annual, ~2-year lag | 2009–2023 (2023 preliminary, released 22 Aug 2025); 2024 due Nov 2026 | free (xls) | bea.gov `mofas-employment.xls` | **Verified as described** (A). *Measured*, India, thousands: total 1,792.6 (2023); professional, scientific & technical 191.8 (2009) → 598.4 (2019) → 877.0 (2022) → 893.2 (2023); information 194.3 (2023) | No finer industry split; vendor affiliates sit inside it. **Most useful official S4 series, with FLA 9C.** Growth slowed to +1.8% in 2023. |
| 11c | **BEA BE-125 / BE-10/11 microdata** (country × affiliation × service type) | S4 | Affiliated computer imports from India | quarterly/annual | — | **restricted** (special sworn employee) | BEA | Collected, not published by country (repo trade FINDINGS, BEA C&M §31.8) | Months of access lead time. |

### Indian labour-market sources

| # | source | scenario pair(s) | mechanism | frequency | coverage | free / paid | access | verification + citation | notes |
|--|--|--|--|--|--|--|--|--|--|
| 2a | **Naukri JobSpeak** (Info Edge) | **S1 vs S4** (IT-services vs GCC postings); S1 vs S2/S3 (weak; experience bands, all industries) | Postings plus recruiter résumé searches. Under S4, GCC demand holds while IT-services demand falls; under S1 both fall | monthly, ~1-week lag | Index base Jul 2008 = 1000; PDFs online from ~Mar 2023; repo parsed Jan 2021–Aug 2026 | free PDF | infoedge.in/InvestorRelations/NaukriJobSpeak; files `Naukri-Jobspeak-<Month>-2026.pdf` (full month name in 2026) | **Exists, but differs.** Sep-2026 PDF (11 pp.), p.4 tiles: IT/Software Services −4%, **GCC +4%**, AI/ML +20%, BPO/ITES +4% ("GCC hiring in the sector grew by +59%"). Annex: IT-Software/Software Services 3432 (Sep'26) vs 3585 (Sep'25); overall index 3053 (V, *measured* index). In 2026 the GCC series appears **only as a YoY tile, not as an index level** (V for Sep-2026; per the agent it was a full annex row in Sep-2024: A). No "foreign MNC"/"unicorn" cut in 2025–26 (A) | Breaks: Sep'23 rebasing for the BFSI/Tech/GCC reclassification (overall 2835→2573); free job listings included from Jan 2026, a "transient uplift" (A). Postings, not hires. **The repo has not parsed the GCC series**; it is cheap to add. Experience bands are all-industry. |
| 2b | **foundit Insights Tracker** | S1 vs S4 | GCC vs IT-services postings | monthly | — | free PDF | foundit.in | **Exists** (A). *Commentary/estimated*: June 2026 GCC jobs +11% YoY, IT-Software & Services −6% | A second postings source to cross-check 2a. |
| 2c | **Xpheno active-openings counts** | S1 vs S4 | Open roles in IT services vs GCCs | monthly (press) | — | free (press) | PeopleMatters and other press | **Exists** (A). *Commentary*: Sep 2026 ~57k IT services, ~13k GCC openings | Press only; method opaque. |
| 3a | **EPFO payroll data** | S1 vs rest (weak); juniors via age 18–25 | Net new EPF payroll in the computer-related establishment category | monthly (~2-month lag) | from Sep 2017 (since Apr 2018 release) | free PDF | epfindia.gov.in → epfo.gov.in (**403 to all fetches**; Wayback copy read) | **Exists, but differs.** The industry table is "Net New Payroll in **Top 10** Industries & Age Buckets"; the category is "ESTABLISHMENT ENGAGED IN MANUFACTURE, MARKETING SERVICING, USAGE OF COMPUTERS" and appears only when in the top 10 (A; Aug-2025 PDF pp.18–20). *Measured*, age 22–25: FY24 118,118; FY25 152,037 (A). "Expert services" = manpower suppliers, contractors and security (~40% of additions) (A) | No ownership split (GCCs and vendors pooled), so it **cannot separate S4**. Contractor payroll hides the end-employer. **No release after Jul-2025 data found** (A). A Dataful mirror claims an industry × age dataset (N). Establishment-level search: secondary source only (N). |
| 3b | **PLFS unit-level data** (MoSPI) | S1 vs S4 (sector employment vs the vendors) | NIC 62/63 employment (all employers). If sector employment holds while the six vendors stall, work moved elsewhere (S4 or other vendors) | annual from 2017-18; calendar-year from 2021; quarterly/monthly from 2025 | 2017-18 – 2026 | free (registration) | microdata.gov.in | **Verified** (A): NIC industry code and enterprise-type code in the 2025 data dictionary. No foreign-ownership code | Small samples in NIC 62; published bulletins give broad sectors only. |
| 3c | **ASISSE** (Annual Survey of Incorporated Service Sector Enterprises; the "ASSSE") | S1 vs S4 (future) | Employees by enterprise, NIC 2025, from the GST registry | annual | first full survey launched 6 Apr 2026, reference FY2024-25; **no results yet** | free (when published) | mospi.gov.in | **Exists, but differs** (pilot 2024-25; full round in the field) (A). No foreign-ownership item in the user guide (A) | Watch: if published with an ownership flag or microdata, it becomes a key S4 source. |
| 3d | ASUSE | — | — | annual | — | free | MoSPI | Exists; **unincorporated sector only**, so irrelevant (A) | — |
| 3e | **BRSR** (SEBI format) | S1 vs S2/S3 (turnover, gender) | Firm-level employees and turnover | annual | FY22– (mandatory for top 1,000 from FY23) | free | firm annual reports, SEBI | **Verified as described, with correction** (A): SEBI/HO/CFD/CMD-2/P/CIR/2021/562 (10 May 2021); BRSR Core circular SEBI/HO/CFD/CFD-SEC-2/P/CIR/2023/122 (12 Jul 2023). Q20 employees by gender/permanent; Q22 turnover. **No age bands or new-hire counts required**; those are voluntary GRI 401-1/405-1 items | Repo already uses the GRI age tables (`workforce/`). |
| 2d | **Indeed Hiring Lab** postings | — | — | daily/weekly | — | free (GitHub) | github.com/hiring-lab/job_postings_tracker | **Exists, but India not covered**: 11 countries, no IN folder (A; last commit 29 Sep 2026) | India appears only in blog commentary. |
| 2e | LinkedIn Economic Graph India / Revelio Labs (role-level) | S1 vs S3; S2 vs S3 (role incidence) | Role × firm headcount by AI exposure | monthly | ~2015– | **paid** (Revelio; price not public); LinkedIn research access by application | — | Not re-checked in this pass; see NEXT_STEPS C7 | The plan's Gate-2 candidate. |
| 11d | **STPI / SEZ export statistics** | S1 (aggregate) | Exports by STP or SEZ units | annual | — | free | stpi.in; sezindia.nic.in | **Exists, but differs**: SEZ fact sheet (31 Mar 2026): employment 32,61,147, FY26 exports ₹16,36,192 cr, **no sector or owner split**; STPI state-wise exports only (A) | Not useful for S4. |
| 11e | GST / income-tax data by sector | — | — | — | — | — | — | **Not found** as a public sector-level dataset (one search; the GSTN publishes no sectoral export-of-services series that I found) | — |
| 11f | ESIC | — | — | monthly | — | free | — | Exists; no industry split (A) | — |

### US sources

| # | source | scenario pair(s) | mechanism | frequency | coverage | free / paid | access | verification + citation | notes |
|--|--|--|--|--|--|--|--|--|--|
| 9a | **USCIS H-1B Employer Data Hub** | S1 vs S4 (vendor vs client-firm filings); onsite slice only | Approvals by employer: vendors' new-employment H-1Bs vs clients' (GCC parents') own H-1Bs | quarterly updates | **FY2009 – FY2026 Q3** | free (Tableau → CSV crosstab; archived per-year CSVs FY2009–23) | [uscis.gov H-1B Employer Data Hub](https://www.uscis.gov/tools/reports-and-studies/h-1b-employer-data-hub) | **Verified** (V: "fiscal year 2009 through fiscal year 2026 (quarter 3)"). **Fields changed** (A, "Understanding" page updated 7 Jul 2025): New Employment, Continuation, Change with Same Employer, New Concurrent, Change of Employer, Amended (approvals and denials). The old Initial/Continuing columns survive in archived CSVs. First decision only; 2-digit NAICS; employer name = most common spelling per tax ID; mailing address, not worksite | The Sept-2025 $100k fee dominates from FY2026 (repo LCA finding). |
| 9b | **USCIS "Approved L-1 Petitions by Employer"** | S1 vs S4 (intra-company transfers) | Vendors' L-1 inflow | annual | **FY2015–FY2019 only** | free PDF/CSV | uscis.gov reports and studies | **Exists, but differs: stops at FY2019** (A). *Measured* example: Tata Consultancy Svcs Ltd, initial L-1A total 1,542 (FY2019 file). No FY2020+ employer file found; probably FOIA only (N) | Excludes blanket-L consular cases; cells under 10 masked. |
| 9c | **DOL OFLC LCA disclosure** | S2/S3 vs S1 (occupation incidence; failed in the repo probe); **S4 via `SECONDARY_ENTITY_BUSINESS_NAME`** (client-site placements) | Which clients vendors place H-1B workers at, and whether those clients begin filing LCAs themselves | quarterly (cumulative within FY) | FY2015 – FY2026 Q3 (latest file `LCA_Disclosure_Data_FY2026_Q3.xlsx`) | free xlsx | dol.gov/agencies/eta/foreign-labor/performance | **Verified** (A; repo probe R). Secondary-entity fields present in the record layout (A); **not kept in the repo extract** (R) | Requests, not hires. A client-name panel needs a re-download of ~4 GB. |
| 9d | State Dept NIV issuances by nationality and class | S1 (onsite demand, aggregate) | India × H-1B/L-1 issuances | monthly | to ~2025 per search | free PDF | travel.state.gov (**403**) | **Unverified** (N) | Not firm-level. |
| 10a | **BLS CES 5415** (computer systems design) | S1 vs S4 (US-side substitution); context | US employment in the competing/complementary industry | monthly | 1990– | free API | `CES6054150001` | **Verified (V).** *Measured*: Sep 2026 2,355.4k (preliminary) vs Sep 2025 2,387.6k (−1.3%), Sep 2024 2,437.6k | US domestic employment falling too counts against S4-to-US-onshore; consistent with S1 or S3 industry-wide. |
| 10b | **BLS QCEW 5415 / 541511 / 541512** | as 10a, plus establishment counts | Jobs vs establishments | quarterly, ~2-quarter lag | to 2026Q1 | free API/CSV | data.bls.gov/cew | **Verified** (A). *Measured* 2026Q1: 5415 March employment 2,343,383 (−1.8% YoY); 425,715 establishments (+2.7%); 541512 −3.5%, 541511 −0.7% | — |
| 10c | **BLS OEWS**, occupations within NAICS 5415 | **S1 vs S3 / S2 vs S1** (task incidence, US side) | Whether US 5415 cuts concentrate in AI-exposed occupations (programmers, QA) vs others | annual (May) | 2003 – May 2025 | free | bls.gov/oes (`oesm25in4.zip`) | **Verified** (A). *Measured* May 2025, NAICS 541500: all 2,445,140; software developers 515,410; QA analysts/testers 57,200; programmers 27,660. No 6-digit split | A US analogue of the role-incidence test, with no firm split. |
| 10d | JOLTS | — | — | monthly | — | free | — | **No 5415 detail**; closest is professional & business services (A) | — |
| 10e | **Census QSS**, NAICS 5415 revenue | S2 vs S3 (industry level) | Revenue ÷ employment for US 5415 = p/a·u (the same identity), so it **cannot** separate S1 from S3; it shows whether p/a is rising (S2) | quarterly | — | free | census.gov/services/qss | **Verified** (A). *Measured*: 2Q2026 5415 revenue $194,939m SA (preliminary), +3.3% on 2Q2025 | US industry, not the Indian vendors. |
| 10f | **Census AIES** (successor to SAS): purchased computer/professional services and contract labour by **client** industry | **S1 vs S4** (client side) | Clients' purchases of IT services vs their in-house IT; if purchases fall while clients' own tech employment holds, that is S4 | annual | reference years 2023–2024 | free (API key now required) | api.census.gov (`aiesexp02`) | **Exists** (A); **values not pulled** (key required) (N) | Promising client-side volume measure (US clients only). SAS NAPCS product lines for 5415 not re-verified. |
| 11g | **Client-side 10-Ks** (banks) | S1 vs S4 | India headcount or India footprint of large clients | annual | — | free (EDGAR) | sec.gov | **Exists, but differs: no India headcount** at JPM, Citi, BofA, GS, MS or WFC. Proxies (*measured*): JPMorgan Properties table, India 6.6M sq ft (FY2025 10-K); Goldman "In India… approximately 2.0 million square feet" (A) | India floor space over time is a crude S4 proxy; collecting several years is cheap. |
| 11h | **Cognizant 10-K**: headcount by country | S1 vs S4 (comparator) | India vs North America headcount | annual | — | free | [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1058290/000105829026000008/ctsh-20251231.htm), "Our People and Culture" | **Verified (V).** *Measured*: "approximately 351,600 employees, with 256,900 in India, 41,600 in North America…" (31 Dec 2025); FY2024 336,800 / 241,500 (A). Risk factors: "competition from clients' in-house technology resources, such as GCCs, which may provide a lower cost alternative" (V, commentary) | — |

### Firm-reported metrics (repo)

| # | source | scenario pair(s) | mechanism | frequency | coverage | free / paid | access | verification + citation | notes |
|--|--|--|--|--|--|--|--|--|--|
| 5 | **Subcontracting cost** (firm P&L) | **S2 vs S4-subcontractor** | If work moves from employees to contractors, subcon/revenue rises while headcount slows; under S2/S3 both fall | quarterly (TCS, Infosys, HCL, Wipro, TechM); annual (LTIM) | see (b) | free | `audit/subcontracting_series.csv` | **Verified** (V, spot checks in (b)) | **Cognizant: no amount.** 10-K: "Historically, subcontractor usage has been immaterial relative to our overall headcount" (V). **Accenture: mixed line only.** FY2025 10-K segment table "Non-payroll costs including subcontractor costs" $11,627,175k (16.7% of revenue; FY2024 $10,841,173k, 16.7%); footnote: "primarily include subcontractor costs and other non-payroll such as facilities, technology and travel costs" (V). The same table gives payroll costs: $45.68bn = 65.6% of revenue (FY2024 65.6%) (V; my arithmetic). |
| 6a | **TCV / bookings** | S1 vs S3 (only with renewal detail); S1 vs ramp timing | Bookings ÷ revenue (book-to-bill) falls under S1. Under S3, renewals are re-signed at lower annual value, so TCV need not fall but revenue does. **High TCV with weak revenue is ambiguous** (longer tenures, slow ramps, front-loaded productivity give-backs) | quarterly | TCS Q1FY19+ (total order book); Infosys Q1FY16+ (large deals ≥$50m) and net-new share Q4FY20+ (sparse); HCL Q4FY21+ (new deal wins); TechM Q1FY19+ (net new deal wins); Wipro large deals ≥$30m Q3FY21+, total bookings Q3FY23+; LTIM order inflow Q3FY23+; Mindtree new/renewal split FY16–FY23; Cognizant TTM bookings 2020Q4+; Accenture bookings by Consulting / Managed Services FY08+ | free | `data/tidy/panel_long.csv` (`tcv`, `bookings`, `book_to_bill`, `tcv_net_new_share`) | **R** (definitions per `data/raw/*_NOTES.md`) | **Definitions differ across firms; not comparable.** Only Infosys net-new share and the Mindtree new/renewal split can show renewal re-pricing, and neither gives the renewal's annual value vs the prior contract. |
| 6b | **Large-deal counts** | as 6a | Count of deals ≥$100m | quarterly | Cognizant 2025Q1–2026Q2 only (4–12 a quarter) | free | `panel_long` `large_deals_count` | **R** | TCS and Infosys counts appear in press releases but are not collected in the repo. Accenture: "clients with quarterly bookings >$100m" (Q3FY23+) is bookings-based. |
| 6c | **Client counts by revenue band** ($1m+, $10m+, $50m+, $100m+; TTM revenue) | **S1/S4 (client exit) vs S3/S2** | Full client exits (S4 insourcing, or S1 project cancellation) lower counts across bands. S3 deflation moves clients down bands but rarely to zero. Rising counts with flat headcount count against broad client loss | quarterly | TCS 2011Q1+; Infosys 2010Q2+; HCL 2013Q3+; Wipro 2013Q2+; TechM 2007Q1+ (no $100m+); LTIM 2021Q2+; LTI/Mindtree to 2022Q3 | free | `panel_long` `clients_bucket`, `active_clients`, `new_clients` | **R.** 2023Q1 → 2026Q2, *measured*:<br>• $1m+ clients: TCS 1241→1401; Infosys 922→1026; HCL 939→987; LTIM 383→407; Wipro 766→714; TechM 582→499<br>• $100m+: TCS 60→66; Infosys 40→41; HCL 19→23; Wipro 19→16 | Nominal-USD thresholds drift upward with inflation. Counts cannot distinguish S1 from S4: a lost client looks the same either way. Falling counts at Wipro and TechM coincide with their revenue declines. |
| 7 | **Onsite/offshore mix** | S1 vs S4 / S3 (weak) | S1 tends to cut discretionary onsite consulting first, so the offshore share rises. GCC insourcing (S4) and automation of offshore run/test work (S3) take offshore work, so the offshore share falls | quarterly | Infosys effort 2010Q2+; Wipro revenue 2013Q2+; TechM revenue 2007–2022Q1, then IT headcount 2021Q2+; LTIM effort 2021Q2+; TCS, HCL: not disclosed | free | `panel_long` `effort_share_offshore`, `revenue_share_offshore`, `headcount_share_offshore` | **R.** 2023Q1 → 2026Q1, *measured*:<br>• Infosys offshore effort 75.4→77.2<br>• Wipro offshore revenue 59.9→62.8 (59.7 in 2026Q2; possible definition change, unverified)<br>• TechM offshore headcount 72.8→77.8<br>• LTIM 85.1→85.8 | The offshore share is **rising**, which leans against S4-to-GCC and S3-on-offshore-work as the dominant force, or reflects visa costs (Sept 2025 fee). Weak. |
| 8 | **Fresher hiring** | S1 vs S2/S3 (persistence) | Under S1, junior hiring falls with revenue and recovers; under S2/S3 it stays low conditional on revenue | annual (quarterly for HCL) | `workforce/fresher_hires_annual_best.csv`: TCS, Infosys, HCL, TechM, LTIM, Wipro (sparse); panel_long quarterly only for HCL 2021Q3+ and TCS 2011Q2–2017Q4 | free | repo | **R.** *Measured* (repo, from firm statements): Infosys 50,000 (FY23) → 11,900 (FY24) → 20,000 (FY26); TCS 44,000 (FY23) → 44,000 (FY26); HCL 26,734 (FY23) → 11,744 (FY26); TechM 950 (FY26) | Values are often rounded verbal statements ("~20,000"). Confounded by the FY22 over-hiring hangover (workforce FINDINGS). |
| 6d | Fixed-price revenue share | S1 vs S3 (mechanism) | Pass-through is automatic under T&M and contractual under fixed price; a rising fixed-price share changes how AI savings reach p | quarterly | Wipro 2013Q2–2026Q2; Infosys to 2019Q1; HCL to 2022Q1 | free | `panel_long` `revenue_share_fixed_price` | **R** | Only Wipro still discloses it. |

## (b) Subcontracting cost as % of revenue (measured; computed from the firms' own filings)

Files: `audit/subcontracting_series.csv` (462 rows: quarterly + fiscal-year, per firm × definition series, with source URL per row); regenerate with `python3 scripts/audit/subcontracting_series.py` (reads `data/tidy/panel_long.csv` only, plus 5 hand-entered LTIMindtree annual rows defined in the script).

**Units and definitions (verified).**
- Numerator and denominator are both consolidated and both INR, converted to INR million (crore ×10, lakh ×0.1). Annual = sum of the 4 fiscal quarters (Apr–Mar); a year is left blank unless all 4 quarters of both series exist. YoY is computed within one definition series only.
- **The task brief's "subcon [INR]" is not right for TCS.** In `core_quarterly.csv` TCS `subcon` is **USD mn**, and its `subcon_share` uses `rev_usd`. The other firms' values are INR with `rev_inr`. The new file uses INR for TCS too (COR + SG&A INR lines). It reproduces the USD-based share to within 0.04 pp (61 quarters).
- Lines used:
  - TCS: "Fees to external consultants", COR + SG&A.
  - Infosys: "Cost of technical sub-contractors".
  - HCLTech: "Outsourcing costs (Subcontractors + Outsourced Work)". The SEBI and IR versions are identical in all 20 overlapping quarters.
  - Wipro: "Sub-contracting and technical fees".
  - TechM: "Subcontracting Expense(s)"; before Q4FY17, "Services rendered by Business Associates & Others".
  - LTIMindtree: "Sub-contracting expenses", annual only.
- Spot-checked against the PDFs/HTML:
  - Wipro Q4FY26: 27,925 / 242,363 INR mn (consolidated-financial-statement-q4fy26.pdf).
  - Infosys Q1FY26: ₹3,497 cr (6-K Ex.99.8).
  - TCS Q4FY23: COR ₹48,680 mn (8.23%) + SG&A ₹1,950 mn (0.33%) (Q4 FY24 fact sheet).
  - TCS Q1FY27: expense-by-nature ₹4,293 cr, printed as 5.9% (Q1FY27 fact sheet).
- **TCS Q1FY27 definition break.**
  - The Q1FY27 fact sheet replaced the COR/SG&A tables with a single "Expense by Nature" line, back-filled for Q1FY26–Q1FY27 only.
  - In Q4FY26 that line is ₹3,971 cr, against ₹4,238 cr for COR+SG&A (FY26: 5.13% vs 5.50% of revenue).
  - In the CSV, Q1FY27 (cal 2026Q2) is flagged `series=expense_by_nature`. Its YoY (+1.21 pp) is taken against Q1FY26 on the same definition.
- **LTIMindtree.** The company was renamed LTM Limited in FY26. Quarterly results do not break the line out, but each annual report does: Board's Report, "Financial Results" table, consolidated.
  - FY22: 23,591 / 261,087
  - FY23: 28,286 / 331,830
  - FY24: 25,599 / 355,170
  - FY25: 26,312 / 380,081
  - FY26: 32,369 / 423,076 (INR mn)
  - Sources: [FY23 Board's Report](https://www.ltm.com/content/dam/ltimcorporatewebsite/annual-reports-2023/pdfs/board-report-ar.pdf), [FY25 Board's Report](https://www.ltm.com/annual-report-2025/pdfs/ltm-ir-2024-25-board-report.pdf), [FY26 Board's Report](https://www.ltm.com/annual-report-2026/ltm-limited-iar-2025-26-boards-report.pdf).
  - These rows are hand-entered and are **not** in `data/tidy`.
  - A web-search summary attributed ₹23,591 mn to FY23. It is the FY22 comparative.
  - Standalone sub-contracting exceeds consolidated (e.g. FY26: 42,148 vs 32,369), because standalone includes payments to group subsidiaries. Use consolidated.
- **Mindtree** (pre-merger): FY22 only (10.2%).
- **Cognizant and Accenture:** see the table in (a).

**Annual subcontracting cost, % of revenue (primary definition per firm)**

| FY | TCS | Infosys | HCLTech | Wipro | TechM | LTIM |
|:--|--:|--:|--:|--:|--:|--:|
| FY16 | 7.7 | 5.7 | – | 13.2 | 13.5 | – |
| FY17 | 7.5 | 5.6 | 18.5 | 15.0 | 12.4 | – |
| FY18 | 7.3 | 6.1 | 17.0 | 15.5 | 12.6 | – |
| FY19 | 7.7 | 7.3 | 16.2 | 16.2 | 12.5 | – |
| FY20 | 8.2 | 7.4 | 15.1 | 14.8 | 14.8 | – |
| FY21 | 8.0 | 7.0 | 13.5 | 13.5 | 13.1 | – |
| FY22 | 9.1 | 10.4 | 14.6 | 13.7 | 15.6 | 9.0 |
| FY23 | 9.5 | 9.6 | 14.7 | 12.7 | 15.0 | 8.5 |
| FY24 | 6.6 | 8.0 | 13.3 | 11.5 | 12.9 | 7.2 |
| FY25 | 4.6 | 7.9 | 13.0 | 11.2 | 11.0 | 6.9 |
| FY26 | 5.5 | 8.6 | 14.2 | 11.6 | 10.7 | 7.7 |
| FY27 Q1 (quarter) | 5.9 (EBN) | 8.7 | 14.8 | 11.8 | 11.4 | n/a |

Notes on the table:
- TCS COR-only: 9.2 (FY23) → 6.2 → 4.3 → 5.2 (FY26).
- HCLTech FY17 starts at Q1FY17. HCLTech and Wipro revenue includes software/products. TechM includes BPS.
- Tech Mahindra had no complete FY13–FY15 years in the repo.

**YoY change (pp), fiscal year**

| firm | FY24 | FY25 | FY26 |
|:--|--:|--:|--:|
| TCS | −2.9 | −2.0 | +0.9 |
| Infosys | −1.6 | 0.0 | +0.7 |
| HCLTech | −1.5 | −0.3 | +1.2 |
| Wipro | −1.3 | −0.2 | +0.4 |
| TechM | −2.2 | −1.9 | −0.3 |
| LTIM | −1.3 | −0.3 | +0.7 |

Quarterly YoY was positive at all five quarterly-reporting firms in 2026Q1–Q2 (Q4FY26–Q1FY27): +0.2 to +1.9 pp.

**Reading (descriptive only).**
- **Subcontracting did not rise after 2023; it fell.** FY24 dropped at all six firms (−1.3 to −2.9 pp), and FY25 was flat to down.
- The FY22–23 peak coincided with the post-COVID demand and attrition spike.
- **A modest rebound began in FY26** (+0.4 to +1.2 pp at 5 of 6 firms; TechM −0.3) and continued into Q1FY27.
- FY26 levels are still below the FY22–23 levels at every firm (HCLTech is closest: 14.2 vs 14.7).
- TCS's FY24 drop (COR fees ₹48,680 mn in Q4FY23 → ₹27,990 mn in Q4FY24) coincides with the Q2FY24 call language on "optimizing subcontractor expenses" (repo `tcs_NOTES.md`).
- So the FY24–25 headcount slowdown was not accompanied by a shift of work from employees to subcontractors. Subcontracting fell along with headcount. That is not the subcontractor version of S4.
- The FY26 rebound is too short and small to read.


## (c) Data that would separate the scenarios but are not publicly available

Two kinds: **collected but unpublished**, and **not collected by anyone publicly**.

| # | data | status | pair | why it would separate them |
|--|--|--|--|--|
| 1 | **Price per unit of output in managed-service / fixed-price contracts** (per ticket, per application supported, per test case, per transaction), and the change in annual contract value when a renewal covers the same scope | not collected publicly (inside contracts and sourcing-advisor benchmarks) | **S1 vs S3**; S2 vs S3 | S3 is defined by falling p. Only an output price observes p without the p/a contamination (NEXT_STEPS §3). Renewal ACV versus prior ACV for the same scope is the cleanest version. |
| 2 | **Vendor revenue and headcount by service line split by AI exposure** (testing, application maintenance, infra/IMS, BPO vs consulting/engineering) | mostly *discontinued* by the six firms (repo `*_NOTES.md`: service-line splits ended or were redefined) | **S1 vs S3**, S2 vs S3 | Under S1, cuts are spread across lines in proportion to discretionary spend. Under S3, cuts concentrate in exposed lines, and revenue in those lines falls with headcount. |
| 3 | **Vendor headcount by role/job level** (beyond Infosys JL bands) | not collected publicly (Infosys only); paid proxy = Revelio/LinkedIn | S1 vs S3/S2 | Incidence of cuts across AI-exposed roles (NEXT_STEPS design D). |
| 4 | **GCC headcount by parent company and function, measured** | not collected officially. Nasscom-Zinnov are estimates without parent detail; MCA filings exist per entity but are not compiled | **S1 vs S4** | S4 needs the same clients' captive headcount rising while their vendor spend falls. Only parent-level data link the two. |
| 5 | **Client IT spend split vendor / in-house (GCC) / subcontractor, by client** | not collected publicly (Census AIES has purchased services by client *industry*, US only, no in-house IT) | **S1 vs S4** | S1: total client spend falls. S4: total spend holds and the vendor share falls. |
| 6 | **Affiliated vs unaffiliated computer-services imports from India** | **collected, unpublished** (BEA BE-125, published only for all countries) | **S1 vs S4** | Affiliated imports from India rising while unaffiliated stall is the S4 signature in trade data. |
| 7 | **RBI software survey: employees (Q16) and billing to subsidiaries/associates abroad** | **collected, unpublished** (RBI survey FAQ, 1 Jun 2026) | S1 vs S4; S2 vs S1 (exports per employee by company type) | Employees by company type would give the GCC-type sector's labour directly. Intra-group billing identifies captives. |
| 8 | **Foreign-owned vs domestic split in official Indian employment data** (EPFO by establishment ownership; PLFS/ASISSE ownership flag) | not collected (EPFO, PLFS); ASISSE has none found yet | **S1 vs S4** | Formal IT employment at foreign-owned captives vs Indian vendors, monthly (EPFO), would be the most direct S4 test. |
| 9 | **Subcontractor / contractor headcount (FTEs)** and the share of work passed to sub-vendors | not collected (only cost lines; Cognizant calls it "immaterial", Accenture mixes it with other costs) | **S2 vs S4-subcontractor** | The cost ratio mixes the contractor rate with volume. FTEs would show whether work moved to contractors. |
| 10 | **Utilization (all six firms, consistent definition)** | discontinued at HCL (after FY19) and partly at TechM (excl-trainees ended FY26) | S2 vs S1 (g_u term) | Under S1, u falls first. Under S2/S3, u can hold while a falls. |
| 11 | **Hours per unit of output / AI-assisted share of delivery** | not collected | S2/S3 vs S1 | It measures a directly. Combined with an output price it identifies S2 vs S3. |
| 12 | **Naukri GCC index levels** (2026 PDFs show YoY only) and an IT × experience-band cross-tab | collected by Info Edge, **not published** as a series | S1 vs S4; S1 vs S3 (junior IT roles) | Without levels or IT-specific experience bands, the postings data can't be chained or split by seniority within IT. |

## (d) Search log (2026-10-05)

**Repo read:**
- `NEXT_STEPS.md`
- `data/explore/PROBE_BRIEF.md`
- `data/explore/{trade,workforce,lca,prices}/FINDINGS.md`
- `trade/rbi_survey_orgtype.csv`
- `workforce/jobspeak_*.csv`, `fresher_hires_annual_best.csv`
- `lca_cases_target_firms.csv.gz` (header)
- `data/raw/*_NOTES.md` (subcontracting, TCV, client and offshore definitions)
- `scripts/01_build_tidy.py` (how `subcon`/`subcon_share` are built)
- `data/tidy/{core_quarterly,panel_long}.csv`

**Primary documents fetched and checked by me (curl / pdftotext / WebFetch):**
- Wipro `consolidated-financial-statement-q4fy26.pdf` (Sub-contracting and technical fees, Revenues): match.
- Infosys 6-K Ex.99.8 (`000106749126000038/exv99w08.htm`), cost of technical sub-contractors: match.
- TCS Q4 FY2023-24 and Q1 FY2026-27 fact sheets (repo copies in `data/sources/tcs/`; tcs.com returned HTML to curl): match.
- LTIMindtree / LTM Board's Reports FY23, FY25, FY26 (ltm.com PDFs). The ltimindtree.com 2023-24 financial-statements URL returned HTML, not a PDF.
- SEC EDGAR: Cognizant FY2025 10-K and Accenture FY2025 10-K (quotes in row 5 and 11h).
- USCIS H-1B Employer Data Hub page (coverage sentence).
- Naukri JobSpeak September-2026 PDF (text layer and p.4 image).
- JobSpeak URL variants (Sep/September/Aug/August/Mar-2026), via curl status codes.
- RBI PR prid 48664 (FY2017-18/2018-19 org-type table) and prid 56359 (FLA census Table 9C).
- BLS API v1, CES6054150001.
- Zinnov 2026 GCC report page.

**Web searches by me:**
- "EPFO payroll data industry-wise net subscribers expert services computer software"
- "LTIMindtree annual report 2024-25 sub-contracting expenses" (the snippet's FY23 attribution was wrong, corrected from the PDF)
- "LTIMindtree Integrated Annual Report 2022-23 Board's Report … Sub-contracting expenses"
- "GST collection sector-wise data IT services export of services" (no sectoral dataset found)
- "RBI Census on Foreign Liabilities and Assets 2024-25 …": **not run**, because the session web-search budget (200) was exhausted by then. Later FLA rounds were therefore not located.

**Sub-agent searches** (four agents; each was told to cite URL, date and section and to log failures):
- **GCC agent:**
  - Searched Nasscom-Zinnov 2023 / 2024 / 2026 editions, the mid-market report, Strategic Review 2025 / 2026, Economic Survey GCC chapters, Union Budget and MeitY GCC framework, MCA fee rules and Accounts Amendment Rules 2025, data.gov.in company master, the Karnataka policy, EY, ANSR, Deloitte, Everest, Bain and a Zinnov tracker.
  - Failures: data.gov.in (503), mca.gov.in (403), indiankanoon (403).
- **Labour agent:**
  - Searched Info Edge PDFs (short and long month names) and the IR page; EPFO industry tables and 2026 releases; data.gov.in EPFO; the EPFO establishment search; PLFS microdata; ASISSE/ASSSE; ASUSE; Indeed India; the SEZ fact sheet; STPI; foundit; LinkedIn; Xpheno; ESIC; MCA master.
  - Failures: epfo.gov.in and pib.gov.in (403), Business Standard (403), Wayback copies of 2026 EPFO PDFs (404).
- **Trade agent:**
  - Fetched all CSV-cited RBI press releases plus prids 48664, 52258 and 56542; the RBI survey FAQ; BEA iTable JSON and CSV (Tables 2.3, 3.3, 4.2; MOFA employment xls).
  - Failures: rbidocs PDFs/xlsx (CAPTCHA, not attempted); RBI rate-limiting (HTTP 429) during a press-release ID scan, which was stopped; the agent's web-search cap was reached.
- **US agent:**
  - Searched the USCIS hub, Understanding and archive pages; USCIS L-1 by-employer files FY2015–19 (FY2020+ not found); DOL performance page (via WebFetch; curl got 403) and record layout.
  - Also BLS API, `ce.series`, the QCEW API, the OEWS zip and JOLTS series lists; Census QSS PDF, SAS/AIES pages and the API catalog (values need a key); EDGAR full-text search ("employees in India", "India", "Bengaluru", "subcontractor") for six bank CIKs, Cognizant and Accenture.
  - Failures: travel.state.gov (403).

**Not attempted:**
- paid reports (Nasscom, Zinnov gated download, Everest, Revelio)
- CAPTCHA-gated RBI files
- MCA document purchases
