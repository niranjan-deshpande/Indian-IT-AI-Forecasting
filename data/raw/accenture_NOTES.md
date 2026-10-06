# Accenture (firm id `accenture`) – collection notes

Output: `data/raw/accenture.csv` (2,848 rows). Script: `scripts/extract/accenture_extract.py`. It rebuilds the CSV from the local copies in `data/sources/accenture/`.
Period: Q1FY15 (quarter ended 2014-11-30) to Q3FY26 (quarter ended 2026-05-31).
**Q4FY26 (quarter ending 2026-08-31) is not yet reported.** Accenture announced that it will release results on 2026-10-01. As of 2026-09-27, EDGAR shows no filing after 2026-07-10.

Fiscal year ends Aug 31. `cal_q` follows SCHEMA: Nov-30 maps to calendar Q4, Feb-end to Q1, May-31 to Q2, Aug-31 to Q3.
Annual rows (`period_type=annual`) use `fiscal_q=FYxx`, `period_end=Aug 31`, `cal_q=YYYYQ3`.

## 1. Sources used

- **SEC EDGAR earnings releases** (8-K Item 2.02, Ex.99), 47 quarters. URL pattern: `https://www.sec.gov/Archives/edgar/data/1467373/<acc>/<fyXXqYearnings8-kexhibit.htm>`. Local copies are in `sources/accenture/8k/`.
  - Revenues come from the "Summary of Revenues" table (three-month block, in USD thousands). The table gives the current quarter, the prior-year comparative, USD growth and local-currency growth for:
    - operating/industry groups
    - geographic markets
    - type of work
  - New bookings (total, consulting, outsourcing/managed services) come from the text.
  - FY15–FY16 releases also state utilization and attrition.
  - The "About Accenture" boilerplate gives headcount.
- **SEC EDGAR 10-Q/10-K** (47 filings), in `sources/accenture/10q/`. The MD&A gives:
  - workforce ("approximately N as of date")
  - quarterly utilization
  - quarterly annualized voluntary attrition
  - annual utilization and attrition in the 10-K
- **Company-hosted IR PDFs** on investor.accenture.com, in `sources/accenture/presentations/` (URLs in `urls.txt`). These are "Supporting Materials", "Operational Metrics" and earnings presentations. Each contains a **People Metrics / Headcount Trend table** covering 8 quarters, with:
  - exact employee counts
  - billable / non-billable split (FY14–FY21)
  - Global Delivery Network (GDN) headcount (FY14–FY17)
  - quarterly utilization and annualized quarterly voluntary attrition
  - Vintages used: Q2FY15, Q3FY16, Q4FY17, Q4FY19, Q2FY21, Q4FY21, Q4FY22, Q4FY23, Q4FY24, Q4FY25, Q3FY26. Together they give full quarterly coverage from FY14 onward.
- **Company-hosted earnings-call transcripts** (investor.accenture.com PDFs, in `sources/accenture/transcripts/`, URLs in `urls.txt`) for Q4FY18–Q4FY23 and Q1FY24–Q3FY26. These are used only for:
  - GenAI / advanced-AI revenue, which is disclosed only on calls
  - a few counts of clients with more than $100M in quarterly bookings

**Skipped or blocked sources**
- The Q4FY17 transcript URL (`Accenture-IR/quaterly-earnings/2017/q4fy17/...`) returned 403. It was not needed.
- The IR "earnings reports" listing page is a JS app, and its async endpoint returned an error page. I found the PDF URLs through web search instead.
- No paywalled sources were used. Seeking Alpha, Motley Fool and MarketScreener transcripts were not used.
- Some supporting-materials PDFs (e.g. Q4FY21) carry a footer reading "Material, Non-Public - Not To Be Distributed Further". They are nonetheless publicly posted on the IR site. Treat this as a curiosity, not a restriction.

## 2. Coverage (quarterly unless noted)

| metric | dimension / type | first–last | gaps / notes |
|---|---|---|---|
| revenue | total, USD_mn | Q1FY15–Q3FY26 | none. Every release also carries a prior-year comparative row (vintage). |
| revenue | "Revenues incl. reimbursements" (other) | Q1FY15–Q4FY18 | pre-ASC 606 gross revenue |
| revenue_growth_yoy | reported + cc | Q1FY15–Q3FY26 | none (from the table's Total row) |
| segment_revenue / segment_growth_yoy (reported + cc) | vertical, geography, service_line | Q1FY15–Q3FY26 | none. Segment sums match the total in every quarter (checked). "Other" has no growth rows (n/m). |
| headcount | total | Q1FY15–Q3FY26 | none. There are three vintages/sources per quarter: exact count from the IR People Metrics tables, "approximately N" from 10-Q/10-K, and a press-release boilerplate row (dimension `total (press-release boilerplate, rounded)`, dim_type other). |
| headcount | Billable / Non-Billable | Q1FY15–Q4FY21 | classification discontinued in FY22 materials |
| headcount | Global Delivery Network | Q1FY15–Q4FY17 | not shown after the Q4FY17 materials |
| utilization_incl_trainees | total | Q1FY15–Q3FY26 | none. Q4 values come only from the IR tables, because the 10-K gives only the annual figure. Annual values are also included. |
| attrition | total | Q1FY15–Q3FY26 | none, plus annual rows FY15–FY25 |
| bookings | total, Consulting, Outsourcing / Managed Services | Q1FY15–Q3FY26 | none. Reported in $bn with 1–2 decimals, converted to USD_mn. |
| bookings_growth_yoy | reported / cc | Q3FY20–Q3FY26, partial | only where the release states it; missing Q1FY15–Q2FY20, Q1–Q2FY21, Q2FY22, Q1–Q2FY23, Q2FY24. Q3FY21 has USD only. |
| clients_bucket | "Clients with quarterly bookings >USD100mn" | Q3FY23–Q2FY26 (+ Q3FY26 YTD 104; FY23/24/25 annual) | hand-entered. This is bookings-based, not a revenue bucket. |
| ai_disclosure | GenAI / Advanced AI new bookings and revenue | Q4FY23–Q1FY26 | discontinued after Q1FY26 (see §3) |

**Not disclosed by Accenture, so absent:**
- subcontracting cost
- onsite/offshore effort or revenue mix (the GDN headcount memo, FY15–FY17, is the closest proxy)
- fixed-price mix
- fresher hires
- active clients by revenue bucket
- revenue_share. Accenture reports segment levels, not shares, and no shares were computed.
- Q4-only GenAI revenue for FY24 and FY25. Only annual or YTD figures were stated, and no differences were computed.

## 3. Definitional breaks

- **ASC 606 (Q1FY19, effective 2018-09-01).** Before FY19 the headline measure was "net revenues", i.e. before reimbursements. The `revenue`/`total` rows and all segment rows for Q1FY15–Q4FY18 are **net revenues**.
  - From FY19 on, revenue includes reimbursements.
  - FY19 releases restate the FY18 prior-year columns on the new basis. Those comparative rows are therefore gross and will not match the FY18 original rows.
  - Pre-FY19 gross revenue is kept separately under dimension "Revenues incl. reimbursements".
- **Geography:**
  - FY15–FY17: North America / Europe / Growth Markets (original composition).
  - Q1FY18 (effective 2017-09-01): regions revised. North America = US & Canada; Growth Markets = Asia Pacific, Latin America, Africa, Middle East, Turkey.
  - Q1FY20: one country moved from Growth Markets to Europe.
  - Q1FY24: Middle East & Africa moved from Growth Markets to Europe, and Europe was renamed **EMEA**.
  - Q1FY25: Latin America moved from Growth Markets to North America, which became **Americas**; Growth Markets became **Asia Pacific**.
  - Prior-year comparatives in each release are reclassified to the current structure. They are kept as separate rows (source_loc "prior-year column").
- **Industry groups:**
  - "Operating groups" included an "Other" line through FY20. From Q1FY21, "Other" is folded into the five groups (prior periods reclassified).
  - Effective 2022-06-01 (Q4FY22), Aerospace & Defense moved from CMT to Products.
- **Type of work:** "Outsourcing" was renamed **"Managed Services"** in Q1FY23. The release footnote says "previously referred to as our outsourcing business".
- **Headcount:**
  - Feb-28-2015: ~3,300 personnel reclassified into the GDN, prior periods not restated.
  - FY15: ~2% of employees realigned from billable to non-billable (FY14 restated).
  - Q4FY25 headcount includes exits from the business-optimization program.
  - Totals include all employees, client-facing and support. Accenture Federal Services and Avanade are included (consolidated).
- **Attrition:** the definition is voluntary attrition excluding involuntary terminations, annualized quarterly rate. 10-Q wording drops "annualized" in FY18–FY21 but the basis looks unchanged.
- **AI metric:**
  - Accenture began disclosing GenAI "sales"/new bookings in Q3FY23 (about $100M over roughly 4 months, per the Q4FY23 call).
  - In Q1FY26 the label became **"Advanced AI"**: Gen AI, agentic AI and physical AI; excludes data, classical AI and RPA.
  - The company stated that Q1FY26 was the last quarter it would share these metrics.

## 4. Judgment calls

- **Utilization mapping.** Accenture's single "utilization" is mapped to `utilization_incl_trainees` by convention. Accenture does not say how trainees are treated.
- **"Over/nearly/approximately" AI figures.** These are recorded at the stated number, and the qualifier (floor or approximate) is in the notes.
- **YTD and cumulative AI figures.**
  - YTD figures use `period_type=ytd`.
  - The cumulative-since-Q3FY23 figures ($11.5bn bookings, $4.8bn revenue) also use `ytd`, with a note.
- **Bookings rounding.** Bookings in older releases are rounded to $0.1bn. Consulting/outsourcing may not sum exactly to the total.
- **Boilerplate headcount.** Kept under a separate dimension so it never competes with the exact or 10-Q counts in vintage selection.
- **Hand-entered rows.** AI rows and clients_bucket rows were hand-entered from release and transcript text, with verbatim wording quoted in notes. Everything else is parsed by the script.
- **Spot-checks.** 14 random rows plus several growth rows were checked against the source text, and all matched. Headcount, utilization and attrition are identical across all overlapping vintages of the IR tables and agree with the 10-Q/10-K ("approximately") figures.

## 5. Reproduction

1. **Download filings.** EDGAR submissions JSON (CIK 0001467373) gives `filings_index.json`, filtered to 8-K Item 2.02 plus 10-Q/10-K from 2014-12 onward. Download each 8-K's exhibit (`*exhib*.htm`) into `8k/`, and each 10-Q/10-K primary document into `10q/`. The URL maps are in `8k_urls.json` and `10q_urls.json`.
2. **Convert to text.** Use BeautifulSoup (lxml) twice:
   - into `txt/`, with each table row rendered as `| cell | cell |`
   - into `flat/`, with `get_text(' ')` and whitespace collapsed
3. **Convert IR PDFs.** Transcripts and presentations (URLs in `transcripts/urls.txt` and `presentations/urls.txt`) are converted with `pdftotext -layout` into same-name `.txt` files.
4. **Build the CSV.** Run `python3 scripts/extract/accenture_extract.py`.
