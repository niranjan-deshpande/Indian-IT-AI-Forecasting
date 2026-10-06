# HCLTech (firm id `hcltech`): collection notes

Output: `data/raw/hcltech.csv`, 8,006 rows, long format per `data/SCHEMA.md`. Every value comes from a primary HCLTech document. All vintages are kept: each release's 3- and 5-quarter tables give one row per quarter shown, so a quarter usually has several rows that differ in `doc_date`/`source_url`.

Reproduce the file with `python3 scripts/extract/hcltech_parse.py`. It uses `scripts/extract/hcltech_tables.py`, the generic table reader. OCR runs through `scripts/extract/hcltech_ocr.swift` (macOS Vision). Local copies of the documents are in `data/sources/hcltech/`.

## 1. Sources

**Quarterly investor releases (48 documents, Q1FY15 [Sep-2014] to Q1FY27 [Jun-2026]).**
- Index page: https://www.hcltech.com/investor-relations/financial-results
- File pattern: `https://www.hcltech.com/sites/default/files/documents/investor-reports/<file>.pdf`. The full list is in `data/sources/hcltech/investor_release_urls.txt`.
- The Q4FY21 release is published under the name `irdraft_q4_jfm21_23_april_v9.pdf`.
- Tables used:
  - constant-currency reporting (5 quarters of revenue USD and QoQ/YoY growth, reported and CC)
  - geographic / service / segment / vertical / contract-type mix (3 quarters)
  - revenue growth by segment table (current quarter)
  - Mode 1-2-3 and segment-highlight tables
  - client metrics
  - headcount / "People Metrics" (3 or 5 quarters)
  - INR income statement (revenue)
  - cost breakup (Outsourcing costs, Employee benefits; Q2FY23+)
  - HCLSoftware revenue table
- Four releases are image-only PDFs: Q4FY23, Q1FY24, Q2FY24 and Q3FY24. I rendered them with `pdftoppm -r 250` and ran macOS Vision OCR on them (`data/sources/hcltech/ocr/*.txt`). Rows from these files say "(image PDF, OCR)" in `source_doc` and carry an OCR note.
  - I checked 569 OCR values against text vintages of the same quarter. The only differences are the known restatements (Q1FY23 Services-level restatement, Q1FY25 HCLSoftware reclassification).
  - Two OCR header-alignment problems in the client tables were found and fixed in code: a date sitting on its own line was merged back into the header.

**SEBI Reg. 33 consolidated Ind AS financial results (35 quarterly filings used, Q4FY17 to Q1FY27).**
- Same host and folder. The list is in `data/sources/hcltech/sebi_results_urls.txt`.
- Used for `subcontracting_cost` (the "Outsourcing costs" line of the consolidated statement of profit and loss), `employee_cost` and Ind AS `revenue`, in INR crore. Each filing gives the current quarter, the previous quarter and the year-ago quarter. Together they cover Q3FY16 (Mar-2016, as an Ind AS comparative) through Q1FY27 with no quarter missing.
- Most FY17 to FY19 filings and several later ones are scanned. They were OCR'd the same way (`data/sources/hcltech/results_ocr/`) and flagged "(scanned, OCR)".
- Three files are PDF portfolios, and the statements are embedded attachments. I extracted them with `pdfdetach` into `results/detached/`; the source URL is the portfolio and `source_loc` names the embedded file.
  - `financialresults.pdf` = Mar-2020
  - `financialresults-q12020_0.pdf` = Jun-2020
  - `full_financial_results_0.pdf` = Sep-2020

**Skipped or partly used (nothing needed a login or payment; nothing was blocked):**
- SEBI Mar-2019 filing: the OCR of the statement was unusable. The quarter is covered by the Jun-2019 and Mar-2020 filings.
- SEBI Sep-2021, Sep-2022 and Dec-2023 filings: the OCR dropped columns in the cost rows, so I skipped those rows (the code logs "skip partial row"). The quarters are covered by other vintages.
- SEBI Jun-2019 filing: its embedded text layer reads Mar-19 revenue as "13,990". Every other vintage says 15,990, so that one cell is excluded (`RESULTS_SKIP` in the code).
- FY16 (Indian GAAP, in lakhs) and the Jun/Sep/Dec-2016 Ind AS-transition SEBI filings were not used: they are standalone-first layouts and the OCR was incomplete.
- `financial results.pdf` (56-page bundle) and the analyst decks were not needed.
- Earnings-call transcripts were not used. Every metric here is in a release or filing.

## 2. Coverage (quarterly, point or LTM series; first to last quarter)

| metric | coverage | comments |
|---|---|---|
| revenue USD_mn | Q1FY14 (Sep-13) to Q1FY27 (Jun-26), all 52 qtrs | 5-quarter CC table in every release. Also the HCLTech Services segment. |
| revenue INR_cr | Q1FY14 to Q1FY27 | IR income statement (US GAAP until Q3FY22, Ind AS after). Also Ind AS from SEBI filings, from Jun-18. |
| revenue_growth_qoq / _yoy, cc | Q1FY14 to Q1FY27, all quarters | Reported-basis growth only until Q1FY23. |
| headcount (total) | Q1FY14 to Q1FY27, all quarters | Technical / (Sales and) Support split available until Q4FY26. |
| attrition | IT Services LTM and Business Services quarterly: Q1FY14 to Q4FY19. Company LTM (excl. involuntary and DPO): Q1FY19 to Q1FY27 | See breaks below. |
| utilization_incl_trainees | Q1FY14 to Q4FY19 | Discontinued from the Q1FY20 release. |
| gross_additions | Q1FY14 to Q4FY21 | Not reported afterwards. |
| net_additions | Tables: Q2FY22 to Q1FY27. Text: Q1FY20, Q2FY20, Q3FY21, Q4FY21, Q1FY22 to Q4FY22 | Gaps: Q3FY20 to Q2FY21. I did not compute net additions from headcount. |
| fresher_hires | Q2FY22 to Q1FY27 quarterly; FY22 annual (23,000) and FY22 YTD Q3 (16,000) from text | None before FY22. |
| subcontracting_cost | INR: Q3FY16 to Q1FY27 (SEBI "Outsourcing costs", and IR cost breakup from Q4FY22). USD: Q2FY22 to Q1FY27 (IR cost breakup) | |
| employee_cost | INR: Q3FY16 to Q1FY27. USD: Q2FY22 to Q1FY27 | |
| tcv | Q4FY21 to Q1FY27 quarterly (New Deal wins TCV), plus FY21 to FY26 annual | Before FY21 only qualitative text ("in excess of $1bn"); no values recorded. Q4FY21 ($3.1bn) and FY21 ($7.3bn) are rounded. |
| clients_bucket (LTM) | USD1/5/10/20/50/100mn+: Q1FY14 to Q1FY27. USD30/40mn+: to Q1FY19 | |
| top_clients_revenue_share | Top 5/10/20 (LTM): Q1FY14 to Q1FY27 | |
| revenue_share_fixed_price | Q1FY14 to Q4FY22 | "Managed Services & Fixed Price Projects"; T&M is a separate `revenue_share` row with dim_type `other`. Not reported after Q4FY22. |
| revenue_share / segment growth: geography | Americas/Europe/ROW: Q1FY14 to Q4FY25. USA/Europe/ROW/India: Q1FY25 to Q1FY27 (restated) | Geography QoQ growth stops after Q4FY24; YoY only from then. |
| revenue_share / growth: verticals | Q1FY14 to Q1FY27 | QoQ growth stops after Q4FY24. |
| service lines (pre-FY20) | Application / Infrastructure / Business Services / ERS service line: Q1FY14 to Q4FY19. IAS/ESI sub-lines: Q1FY14 to Q4FY15 | |
| segments | ITBS, ERS: shares Q1FY19 (restated) to Q1FY27; CC growth Q1FY20 to Q1FY27; USD levels only Q1FY21 to Q1FY23. Products & Platforms: Q1FY19 to Q2FY23. HCLSoftware: Q3FY22 (restated) to Q1FY27, with USD revenue Q4FY22 to Q1FY27. HCLTech Services (ITBS+ERS): share Q3FY21+, USD revenue and CC growth Q2FY22+ | |
| Mode 1/2/3 | Revenue USD, share, QoQ CC growth: Q1FY19 to Q4FY22. YoY CC growth: Q2FY21 to Q4FY22 | FY18 releases give only narrative or annual Mode shares, not recorded. |
| ai_disclosure | Q2FY26 (">$100M", lower bound) to Q1FY27 | Advanced AI revenue $146M, $155M, $171M. |
| headcount_divested (new metric) | Q1FY25: 7,398 | Also an FY25 annual row for the same event. |

Not disclosed by HCLTech in these documents: utilization after Q4FY19, onsite/offshore effort or revenue mix, fixed-price mix after FY22, bookings before FY21.

New metrics I added (not in the SCHEMA vocabulary):
- `top_clients_revenue_share`: Top 5/10/20 clients' share of LTM revenue.
- `headcount_divested`: reduction in headcount due to divestiture.

## 3. Definitional breaks

**Fiscal year.**
- Until FY15 the FY ended in June: Q1FY15 = Jul–Sep 2014 and Q4FY15 = Apr–Jun 2015.
- FY16 was a 9-month transition year, Jul 2015 to Mar 2016, with only Q1FY16 to Q3FY16. Confirmed by the "nine months ended March 31, 2016" results and by the Q3FY16 release's "12 months ended 31-Mar-16".
- From FY17 the FY runs Apr–Mar.
- `fiscal_q` follows these labels. `period_end` and `cal_q` are the actual quarter-end dates, and quarter ends are continuous.

**Accounting basis.**
- IR financials were US GAAP up to the Q3FY22 release.
- From Q4FY22 the USD financials are IFRS and the INR financials are Ind AS.
- SEBI filings are Ind AS throughout (from FY17).

**Service lines, segments and Mode classification.**
- **Application Services split (effective Q1FY15, Jul 2014).** Application Services was split into Industry Application Services and Enterprise System Integration. These sub-lines are shown until the Q4FY15 release.
- **Service lines, up to Q4FY19.** Application Services, Infrastructure Services, Business Services and Engineering and R&D Services, from Q1FY14 to Q4FY19 (Mar-2019).
- **Segments, from the Q1FY20 release (Jun-2019).** Three segments, with history restated back to Jun-18:
  - IT and Business Services
  - Engineering and R&D Services
  - Products & Platforms
- **Renamed old ERS series.** The old ERS *service line* included IP-partnership / product revenue that later went into Products & Platforms. Example for Jun-18: 24.5% as a service line against 17.3% as a segment. The pre-FY20 series is therefore stored under the dimension `Engineering and R&D Services (service line, pre-FY20 classification)`. This is the one place where a dimension name departs from the firm's exact label, and I did it deliberately for disambiguation.
- **Mode 1-2-3.** Mode 1 (core), Mode 2 (next-gen) and Mode 3 (products & platforms) were reported quarterly from the Q1FY19 to the Q4FY22 release. Growth is QoQ CC only until Q1FY21, then QoQ and YoY.
- **Q1FY23 reorganisation.** Internally developed software products were moved from ITBS to Products & Platforms, with prior periods restated. From the same release the geography and vertical mix and growth are reported at **HCLTech Services level**, excluding P&P/HCLSoftware ("Revenue analysis at Services level"), with restated history. As a result the same quarter has company-level values in older vintages and Services-level values in newer ones. Example for Technology & Services, Jun-21: 17.3% company-level against 13.3% Services-level. The `notes` column says which is which.
- **Q2FY23.** Products & Platforms was renamed HCLSoftware. The "Services (A+B)" subtotal is kept as dimension `HCLTech Services`.
- **Q1FY25.** Services tied to certain software products moved from HCLSoftware to ITBS and ERS, with prior periods restated ("immaterial"). This produces small restatements in FY24 segment shares, for example ERS Jun-23 at 15.4 against 15.5.
- **Q1FY26 geography change.** Geography moved from Americas/Europe/ROW to USA/Europe/ROW/India, restated back to Jun-24. The new Europe and ROW are not comparable with the old ones (Dec-24: Europe 26.2 against 28.2; ROW 11.0 against 6.3). They are stored as `Europe (USA/Europe/ROW/India scheme)` and `ROW (excl. India; USA/Europe/ROW/India scheme)`.

**Verticals.**
- Q1FY19: "Manufacturing (including Hitech)" was split into Manufacturing and Technology & Services, restated back to Jun-17. Pre-FY19 Manufacturing (about 35%) is not comparable with the later series (about 20%).
- Vertical "Others" is shown until Q4FY18.
- The Public Services definition included Oil & Gas until the Q1FY23 release. From Q2FY23 the description lists only Energy & Utilities, Travel-Transport-Logistics and Government.
- Q4FY25 release: "Financial Services includes the impact of a divestiture in Q2 FY25."

**IBM select-products acquisition ($1.8bn).**
- Closed on June 30, 2019; revenue is included from Q2FY20. This is a large Products & Platforms / Mode 3 step-up.
- Until Q1FY20, IBM IP-deal revenue sat in US geography, the Technology & Services vertical and a single client. From Q2FY20 it is classified by the end customer.
- The Q2FY20 to Q1FY21 releases also show growth "per prior methodology". Only the "per actuals" columns are recorded; the prior-methodology columns (and a duplicate 30-Sep-19 mix column) are dropped.

**Other M&A mentioned in releases.** These are not quantified in headcount or revenue except where noted:
- Geometric and Butler Aerospace (announced FY17)
- C3i and Actian (FY19)
- H&D (FY19)
- Strong-Bridge Envision and Sankalp (FY20)
- DWS (FY21)
- Starschema, Confinale, 51% of Gesellschaft für Banksysteme (gbs) (FY22–FY23)
- HPE CTG assets (FY25 guidance mentions it)
- Divested business in P&P/HCLSoftware (Q1FY23: YoY CC excluding divested business given in a footnote)
- **Q1FY25 divestiture that cut headcount by 7,398.** This is included in that quarter's net addition of −8,080 and is recorded as `headcount_divested`.

**Headcount.**
- Always total consolidated employees: Technical plus (Sales and) Support.
- Labels changed over time: "Total Employee Count" became "Total People Count" (Q2FY23), and "Support" became "Sales and Support" (Q2FY20).
- No change in scope is stated.

**Attrition.**
- Until the Q4FY19 release: "Attrition - IT Services (LTM)" and "Attrition - Business Services (Quarterly)", both excluding involuntary attrition.
- From the Q1FY20 release: a single "Attrition (LTM)" excluding involuntary attrition and Digital Process Operations. The restated history (Jun-18 to Mar-19) equals the old IT Services figures.

**Utilization.** "Blended Utilization (Including Trainees)", last reported for Mar-2019.

**Client buckets.** The $30M+ and $40M+ buckets were dropped after the Q1FY19 release.

## 4. Judgment calls

- **Company totals.** Total revenue and growth come from the constant-currency reporting table, not from the segment-growth table (the values are identical). USD revenue is taken from that table, not from the USD income statement, to avoid duplicates.
- **Blank cells.** Cells printed as "-" are kept with an empty value and the note "value printed as '-'". There are 6 such rows.
- **Annual columns.** "Year ended" columns in Q4 releases, "LTM Mix" columns and "% of revenue" blocks are not recorded. Exceptions are the annual TCV / net-addition / fresher text figures, which carry `period_type=annual/ytd`.
- **Header typo.** The Q2FY18 release prints the header "31-Mar-16" where it should read 31-Mar-17, in its 5-quarter tables. The code fixes this automatically and logs it.
- **SEBI filings.** I took only the first three numeric columns (current, previous and year-ago quarter) of the consolidated statement. Rows with fewer than three readable numbers are skipped.
- **Hand-entered text values.** These are flagged "hand-entered" in `notes`: all TCV, AI disclosures, pre-FY23 net additions and fresher text figures, and the divestiture headcount.
- **Share checks.** Segment / geography / vertical shares sum to about 100 per quarter and vintage, except for the documented sub-line / subtotal rows (IAS/ESI, HCLTech Services, Inter-segment).
- **Spot checks.** More than 25 random values were checked against the PDF text or OCR. Cross-vintage comparisons show differences only where HCLTech restated.
