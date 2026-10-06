# GFC window (2007Q1–2012Q1) — collection notes

Output: `data/raw/gfc.csv` (schema per `data/SCHEMA.md`; 11,336 rows; firms tcs, infosys, hcltech, wipro, techm, cognizant, accenture).
Scope: CORE metrics for calendar quarters 2007Q1–2012Q1: revenue, revenue growth as reported (cc where disclosed), headcount, utilization, attrition. Where the same documents carry them, the file also has revenue shares/levels by vertical, geography and service line, and subcontracting.

**General conventions**
- Every multi-quarter table column is kept as a separate row (vintage) with the source document's `doc_date`. Restatements therefore appear as different values for the same `cal_q`; pick the vintage you need, e.g. the latest `doc_date`.
- Nothing was interpolated or computed. The only transformations are unit scaling of a reported level (USD thousands → USD mn; $bn → $mn), stated in `notes`.
- **Indian firms:** FY ends March; `cal_q` is the quarter containing `period_end`.
  - HCLTech used a **June fiscal year** in this window; `fiscal_q` is HCL's own label (e.g. Q2FY09 = Oct–Dec 2008).
  - **Accenture:** FY ends August. `cal_q` follows SCHEMA (Nov→Q4, Feb→Q1, May→Q2, Aug→Q3), so there is a one-month offset.
- Wayback copies (TCS, HCLTech, Tech Mahindra): `source_url` is the web.archive.org URL; the original company URL is in `notes`.
- Image-only exhibits (Infosys fact sheets, some TCS slides, some TechM results ads) were OCR'd with macOS Vision and cross-checked; rows say "OCR" or "hand-entered" in `notes` / `source_loc`.
- **New metrics / units** (not in SCHEMA vocabulary):
  - `subcontracting_pct_cost_of_sales` (Infosys: cost of technical subcontractors as % of **cost of sales**);
  - `revenue_share_onsite` (TechM);
  - `bookings`, `active_clients`, `clients_bucket` (vocabulary items, collected opportunistically);
  - unit `INR_lakh` (TechM segment revenue and subcontracting, left as reported).
- **Metric mappings to note:**
  - Wipro "gross/net utilization" → incl/excl trainees (judgment call).
  - Accenture "utilization" (no trainee split) → `utilization_incl_trainees`.
  - HCL offshore/onsite utilization → `utilization_offshore` / `utilization_onsite` plus incl/excl trainees; see the HCL section.
- **Blocked sources:** tcs.com returns HTTP 403 to scripts (Wayback used); BSE archive refused access (HCL). No paywalled sources were used. archive.org was briefly offline during collection (retries succeeded).



## TCS (GFC window: Q4FY07–Q4FY12 = cal 2007Q1–2012Q1)

Rows: `data/sources/gfc/tcs/gfc_tcs_rows.csv` (1,905 rows from 37 source documents (39 PDFs downloaded; 2 press releases, Q4FY08 and Q4FY09, yielded no row); all vintages kept, `doc_date` = results-announcement date printed on the document).
Scripts: `scripts/extract/gfc_tcs_download.py` (Wayback download + `_manifest.csv`), `scripts/extract/gfc_tcs_ocr.swift` (macOS Vision OCR of image-only slides), `scripts/extract/gfc_tcs_extract.py` (parsing; re-runnable from local copies in `data/sources/gfc/tcs/{txt,ocr}`).

### 1. Sources
All rows come from TCS's own documents, fetched as **Wayback Machine raw copies of tcs.com PDFs** (`source_url` = `https://web.archive.org/web/<ts>/<original>`, `notes` carry `original URL: ...`). Documents found via the Wayback CDX API over `www.tcs.com/investors/*` and `www.tcs.com/SiteCollectionDocuments/Investors/*`.
- **Quarterly analyst presentations** (`TCS_Analysts_Q#_##.pdf`), all 21 quarters Q4FY07–Q4FY12. Main source: geography / industry ("IP Revenue") / service-line ("SP Revenue") share tables, US GAAP (IFRS from Q1FY12) income statements in INR and USD, HR slide (headcount, utilization, attrition). Several slides are images (US GAAP revenue-growth and USD income-statement slides in FY09–FY11 decks) → OCR'd; those rows carry `[OCR of image slide]` in `source_loc`.
- **Operating Metrics fact sheets** (`TCS_OperatingMetrics_Q#_##.pdf`): only three in-scope copies are archived: Q3FY09, Q1FY10, Q1FY12 (3-column tables: year-ago Q, prior Q, current Q).
- **Press releases** (US GAAP; IFRS from FY12), 16 quarters: used only for USD revenue level / USD growth quoted in the highlights (hand-entered, each value verified by exact-string match in the script; flagged `hand-entered` in notes).

Skipped / blocked:
- **tcs.com direct**: every scripted request (curl, browser UA, GET or HEAD) returns HTTP 403 "Access Denied" (Akamai), even for URLs that are live today. The current tcs.com archive also only goes back to FY2011-12, so Wayback was the only route for FY07–FY11.
- Operating Metrics fact sheets for the other in-scope quarters are not in the Wayback index (the analyst decks carry the same tables, so no metric is lost). Q1–Q3 FY07 fact sheets exist but are out of scope.
- Wayback CDX/playback was intermittently "Temporarily Offline"; retries fixed every download. BSE/NSE archives were not needed and not tried.
- Earnings-call transcripts (archived for several quarters) were not used; nothing core was disclosed only on calls.

### 2. Coverage (calendar quarters; all 21 in-scope quarters exist for most metrics)
| metric | dimension | first–last | gaps / remarks |
|---|---|---|---|
| revenue INR_mn | total | 2007Q1–2012Q1 | none; 2–3 vintages per quarter (US GAAP INR mn; IFRS from Q1FY12 decks) |
| revenue USD_mn | total | 2007Q1–2012Q1 | **2007Q1–2007Q4 (Q4FY07–Q3FY08): only convenience translation** (current quarter only, at period-end rate, e.g. Rs 43.47/USD for Q4FY07). Average-rate USD revenue starts in the Q1FY09 deck, which also restates FY08 quarters (Q1FY08 1,262; Q2FY08 1,372; Q3FY08 1,484; Q4FY08 1,517). No average-rate USD figure for Q4FY07. |
| revenue_growth_qoq / _yoy | total | 2007Q1–2012Q1 | INR-terms growth (deck table) Q4FY07–Q1FY11; USD-terms growth (press releases) for 13 quarters, some rounded (e.g. "up 12%"); no growth figure for Q2–Q3 FY12 other than cc. `notes` say "INR terms" vs "USD terms". |
| revenue_growth_qoq basis cc | total | 2011Q4–2012Q1 | constant-currency Q-o-Q growth first disclosed in Q3FY12 (4.5%) and Q4FY12 (2.3%) decks; not disclosed earlier. |
| headcount | total | 2007Q1–2012Q1 | none (definition breaks below) |
| headcount | TCS excl. subsidiaries | 2007Q1–2011Q2 | missing Q2FY08 (deck gives only consolidated + Indian subs); Q4FY11/Q1FY12 only from the Q1FY12 fact sheet ("TCS Limited"); not given for Q2–Q4 FY12. |
| utilization_excl/incl_trainees | total | 2007Q1–2012Q1 | none |
| attrition (LTM, incl. BPO) | total | 2007Q1–2011Q4 | **Q4FY12 missing**: deck gives only IT Services (11.05%) and BPO (21.64%). |
| attrition | IT Services / BPO | 2007Q1–2012Q1 | none |
| revenue_share | geography, vertical, service_line | 2007Q1–2012Q1 | none; each quarter appears in 2–4 vintages; all 158 doc×quarter×dimension groups sum to 100.0 |
| segment_growth_qoq / _yoy | all three | 2011Q3–2012Q1 | only FY12 Q2–Q4 decks report segment growth (INR terms); Q4FY12 Y-o-Y column is FY12 annual (period_type annual, fiscal_q FY12). |
| subcontracting_cost | Fees to external consultants (COR) / (SG&A) | 2010Q2–2012Q1 | only the IFRS decks (Q1FY12+) break out "Fees to external consultants" (with year-ago columns back to Q1FY11); COR and SG&A lines recorded separately (INR mn and USD mn), not summed. US GAAP decks (FY07–FY11) bury it in "Other costs"/"Professional fees" → not collected. |

### 3. Definitional breaks
- **Headcount – e-Serve / Diligenta (2009Q1, Q4FY09).** Through Q3FY09 the headline "Total employees" = TCS (incl. overseas branches/subsidiaries, GDCs) + Indian subsidiaries (CMC, WTI) and explicitly **excludes TCS e-Serve** (Citigroup captive, acquired 31-Dec-2008; 12,459 employees per Q3FY09 deck). From Q4FY09 the total = TCS Ltd + "Subsidiaries" (CMC, WTI, TCS e-Serve, Diligenta & others). The Q3FY09→Q4FY09 jump (130,343 → 143,761) is mostly this consolidation, not hiring (TCS Ltd went 126,613 → 126,150; Diligenta moved from "TCS" to subsidiaries, prior quarters restated only in a chart, which was not collected). The "TCS excl." dimension name changes accordingly: `TCS excl. Indian subsidiaries (CMC, WTI)` (to Q3FY09) vs `TCS excl. subsidiaries (CMC, WTI, e-Serve, Diligenta & others)` (from Q4FY09). The Q1FY10 fact sheet's Q1FY09 column repeats the old unadjusted numbers under the new labels.
- Q3FY08: 439 employees of a divested non-core business removed (deck footnote).
- **Utilization and attrition**: from Q4FY11 (2011Q1) the decks state they **exclude subsidiaries (CMC, e-Serve, Diligenta)**; earlier the basis is not stated. Attrition is LTM throughout; total = "including BPO".
- **Accounting basis**: US GAAP through Q4FY11; **IFRS from Q1FY12** (Q1FY12 deck restates FY11 quarters: e.g. Q4FY11 USD 2,244 → 2,245, Q3FY11 INR 96,634 → 96,633). Indian GAAP figures (also in decks) not collected.
- **INR revenue restatement of FY08 quarters** in FY09 decks (Q1FY08 52,028 → 51,572; Q2FY08 56,398 → 55,497; Q3FY08 59,241 → 58,637; Q4FY08 60,947 → 60,469); no reason given in the decks.
- **Industry verticals**: (a) Q1FY08 deck restates Q4FY07 (Manufacturing 15.1 → 13.6, Life Sciences & Healthcare 4.7 → 6.2); (b) **Q1FY09 (2008Q2) reorg**: Hi-Tech and Media & Entertainment carved out (Manufacturing, Telecom, Others restated, e.g. Q4FY08 Manufacturing 13.0 → 9.8), "Transportation" relabelled "Travel & Hospitality" in decks (fact sheets keep "Transportation"; same segment, identical values); (c) **Q1FY11 (2010Q2) restatement** (Q4FY10 BFSI 44.4 → 45.6, Others 2.8 → 5.9, Retail 12.3 → 10.9, Hi-Tech 5.1 → 4.4).
- **Geography**: "Ibero America" renamed "Latin America" from the Q4FY10 deck; Q4FY08 shares restated in the Q1FY09 deck (e.g. North America 50.4 → 50.0); Q2FY10 restated in the Q3FY10 deck (North America 53.4 → 52.5, India 7.3 → 8.1, Asia Pacific 5.3 → 5.4).
- **Service lines**: stable (9 lines throughout); fact sheets spell "Application Development & Maintenance", decks "Application Development & Maint.".

### 4. Judgment calls
- Annual (FY) share columns in Q4 decks were not collected. The FY12 annual Y-o-Y segment growth was collected (period_type annual).
- `revenue` USD for Q4FY07–Q3FY08 = the deck's convenience-translated USD column (flagged in notes). It is not comparable with the later average-rate USD series; use the restated FY08 values from the Q1FY09/Q4FY09 decks instead.
- `revenue_growth_*` basis `reported` covers both INR-terms (deck) and USD-terms (press release) growth; which one is which is in `notes`. Press-release growth values are often rounded ("up 3 %", "up 12%").
- Headline headcount = the largest employee count quoted on the HR slide (a smaller "Total Employees: 7,196" on the Q1FY08 BPO slide is a unit count, excluded).
- The Q4FY12 press release's "Q4 Revenues at $ 2.64 billion up 2.4%" was recorded as Q-o-Q (it matches 2,648/2,586).
- 11 table rows garbled by `pdftotext -layout` (values printed on separate lines: Q4FY07, Q1FY08, Q2FY08, Q4FY08 decks) are hand-entered in the script's `HAND` dict, and each is asserted to appear as "label v1 v2 ..." in `pdftotext -raw` output. One header (Q2FY08 geography, "Q1 FY08" printed a line above) was set manually. In the Q2FY10 service table a trailing commentary number ("15%") was dropped.
- Every table/regex value is asserted to appear verbatim in the source text; OCR'd USD revenue matches the press-release figures wherever both exist (Q3FY09 1,483; Q4FY10 1,686; Q1FY11 1,794).
- Spot check: 12 random rows re-read against the source text (all matched), plus two OCR slides (Q2FY09, Q2FY10 USD income statements) checked visually against the page images.


## Infosys

**Sources (all SEC EDGAR, CIK 0001067491; local copies in `data/sources/gfc/infosys/edgar/<accession>/`)**
- Results-day 6-K, Ex.99.1: the US GAAP press release (through Q1FY09) or the IFRS USD press release (from Q2FY09). Gives revenue (USD mn), YoY/QoQ growth as stated, and total employees. Only the first (results-day) filing of each release is used.
- Results-week 6-K "Fact Sheet" exhibit (Ex.99.5; Ex.99.4 in 2012). This exhibit is image-only (GIF pages).
  - Pages were downloaded to `img/` and OCR'd with macOS Vision: `scripts/extract/gfc_ocrj.swift`, then `gfc_multiocr.py`, a multi-scale OCR run with position-based voting.
  - Tables were extracted by column clustering (`gfc_factsheet_cells2.py`).
  - The fact sheet gives utilization with and without trainees, LTM attrition, total employees, revenue shares by geography, industry and service offering, and the 'Constant Currency Reporting' table (reported and cc growth, QoQ and YoY).
  - Three fact sheets were OCR-unreadable (JPEG-like artefacts on shaded columns) and were **hand-entered** from the images: Q3FY11 (0001067491-11-000006), Q2FY12 (-11-000088) and Q4FY12 (-12-000011). Those rows carry "hand-entered" in `notes`.
- Quarterly 6-K report (MD&A, the Form-10-Q equivalent), Q1–Q3 of each FY:
  - Utilization for "total services excluding BPO" (later "services and software application products"), recorded under the separate dimension `IT services excl. BPO (6-K MD&A)`.
  - Cost of technical subcontractors as % of cost of sales, three-month and fiscal-year figures, under the **new metric `subcontracting_pct_cost_of_sales`**. It is not a % of revenue.
- Scripts: `gfc_edgar_index.py`, `gfc_edgar_download.py`, `gfc_html2txt.py`, `gfc_infosys_factsheet_ocr.py`, `gfc_upscale_ocr.py`, `gfc_multiocr.py`, `gfc_factsheet_cells2.py`, `gfc_infosys_build.py`.

**Vintages:** every fact sheet shows three quarter columns: current, previous and year-ago. All three are kept as separate rows with that fact sheet's `doc_date`. The two LTM/year-ended columns are not recorded, except that attrition is itself an LTM measure.

**Coverage (cal quarters):** all 21 quarters 2007Q1–2012Q1 have:
- revenue (USD) and reported YoY growth;
- reported and cc QoQ growth, and cc YoY growth, from 2007Q2 (fact-sheet cc table);
- headcount, utilization with and without trainees (fact-sheet definition), and LTM attrition;
- revenue shares by geography, industry and service offering.

subcontracting_pct_cost_of_sales covers 2008Q1–2012Q1: three-month values for June quarters, YTD otherwise, plus fiscal-year values. MD&A utilization has no March quarters (Q4 is reported only in the 20-F).

**Definitional breaks and cautions**
- **Accounting basis:** US GAAP through Q1FY09 (Jun-2008), IFRS from Q2FY09. The press-release `notes` say which.
- **Infosys BPO:** headcount (and revenue) are Infosys and subsidiaries, including Infosys BPO, throughout. Fact-sheet attrition explicitly *excludes subsidiaries*. The Philips shared-services centres (Infosys BPO, FY08) and McCamish (Dec-2009) are included from their consolidation.
- **Two utilization definitions:** the fact-sheet figures (dimension `total`) and the MD&A figures (dimension `IT services excl. BPO (6-K MD&A)`) differ by up to ~2pp. For example, Jun-2008 is 68.9/72.2 in the fact sheet and 69.8/72.3 in the MD&A.
- **Industry taxonomy:**
  - FY07–FY11: Insurance, banking & financial services (subtotal = Insurance + Banking & financial services), Manufacturing, Retail, Telecom, Energy & Utilities, Transportation & logistics, Services, Others.
  - From Q1FY12 (Jun-2011): four top-level groups (Insurance, Banking & Financial Services; Manufacturing; Retail & Life Sciences; Energy, Utilities, Communications & Services), with sub-rows, Healthcare and Life Sciences split out, and prior quarters restated.
  - Subtotal rows are flagged "subtotal row" in `notes`.
- **Service-offering taxonomy:**
  - FY07: Development / Maintenance / Re-engineering / Package implementation / Consulting / Testing / Engineering services / BPM / Other services / Products.
  - FY08–FY11: ADM (subtotal) = AD + AM; BPM; Consulting & Package Implementation; Infrastructure Mgmt; PES; SI; Testing; Others; Products.
  - FY12: Business IT Services / Consulting & System Integration / Products, Platforms and Solutions with sub-rows. These were reshuffled again in Q3FY12 and Q4FY12 (BPM Platform, PES moved), with restatements.
  - 'Total services' subtotal rows are not recorded.
- **QA drop rule:** a fact-sheet share block (document × quarter × dim_type) whose non-subtotal shares do not sum to 100±0.5 was dropped as an OCR/label failure. 17 blocks were dropped, mostly service offering; they are listed in `data/sources/gfc/infosys/dropped_share_blocks.json`. Every quarter still has at least one vintage for each share type.
- **Growth figures:** the fact-sheet cc table is Infosys's own computation, with rates per FEDAI from Apr-2008. Headline growth is rounded in some releases (e.g. "up 8%").

**QA:**
- Cross-vintage agreement (3 OCR'd images per quarter) holds for all core metrics, apart from small restatements (e.g. cc YoY 2008Q3: 19.5 in the release vs 19.3 in the table).
- 12 random text-sourced rows matched their source text.
- One full OCR'd table (Q2FY10 service offering, 11 values) was checked visually against the image, with 0 errors.


## HCLTech

GFC-period collection (calendar 2007Q1–2012Q1), core metrics only. Output: `data/sources/gfc/hcltech/gfc_hcltech_rows.csv` (1,713 rows, 17 source documents, all vintages kept). Scripts: `scripts/extract/gfc_hcltech_wayback.py` (polite Wayback CDX/download helper, with retry/backoff) and `scripts/extract/gfc_hcltech_extract.py` (parses `pdftotext -layout` output of the local PDFs; reproducible from `data/sources/gfc/hcltech/*.pdf` + `manifest.tsv`).

### Fiscal calendar (important)
- In this period HCL's fiscal year ended **30 June**. Q1 = Jul–Sep, Q2 = Oct–Dec, Q3 = Jan–Mar, Q4 = Apr–Jun. So FY2009 ("FY 2008-09") = Jul-2008..Jun-2009, e.g. `Q2FY09` = Oct–Dec 2008 (period_end 2008-12-31, cal_q 2008Q4), `Q3FY09` = Jan–Mar 2009. Verified from the releases (e.g. the "Third Quarter FY 2008-09" release covers the quarter ended 31-Mar-2009; the Q4FY07 release covers "the quarter and year ended 30th June, 2007").
- `fiscal_q` uses HCL's own June-FY labels (`Q3FY07` … `Q3FY12`); `cal_q` = calendar quarter containing period_end.
- HCL's later move to a March fiscal year (a 9-month transition period Jul-2014..Mar-2015) is outside this window; no transition quarter occurs in 2007Q1–2012Q1.

### Sources used
All are HCL Technologies' own quarterly **Investor Releases** (US GAAP, US$; each includes an INR convenience translation which was not used). Every one was retrieved from Wayback Machine copies of HCL's own PDFs; `source_url` is the archive URL `https://web.archive.org/web/<timestamp>/<original>` and each row's notes carry `original URL: …`.
- `hcl.in/attachment/Q4FY07.pdf` (HCL Enterprise site hosting the HCLT Q4 FY2006-07 release, 13-Aug-2007).
- `www.hcltech.com/investors/Downloads/FR/…`: `Q3_FY08.pdf`, `Q4%20FY08.pdf`, `Q1%20FY09.pdf`, `Q3-FY09.pdf`, `Q1_FY10.pdf`, `Q2_FY10.pdf`, `Q3_FY10.pdf`, `HCLT-Q4-2010-AMJ'10_&_FY'09-10-IR_Release.pdf`, `HCLT-Q1-2011-JAS'10-IR_Release.pdf`, `HCLT-Q2-2011-OND'10-…`, `HCLT-Q3-2011-JFM'11-…`, `HCLT-Q4-2011-AMJ%2711-…`, `HCLT-Q1-2012-JAS'11-…`, `HCLT-Q2-2012-OND'11-…`.
- `www.hcltech.com/sites/default/files/hclt-q3-2012-jfm12-ir_release.pdf` and `hclt-q4-2012-amj12-ir_release.pdf` (Q4FY12, used only for its in-window columns 2011Q2 and 2012Q1, as a later vintage).
- Each release has 3 quarterly columns (year-ago, prior, current quarter) in the income statement, revenue-mix, utilization and employee tables. From Q3FY09 on, a "Constant Currency Reporting" table gives 5–6 quarters of reported revenue, reported QoQ/YoY growth and CC QoQ/YoY growth. All columns were recorded as separate vintages (doc_date = release date).
- doc_date: taken from the release dateline where printed; for the FY11–FY12 releases (no dateline) it is the PDF creation date (flagged "doc_date approx" in notes; within ~1 day of the results date per HCL's call-invite PDFs).

### Skipped / blocked / not found
- Individual releases for **Q3FY07 (Jan–Mar 2007), Q1FY08 (Jul–Sep 2007), Q2FY08 (Oct–Dec 2007), Q2FY09 (Oct–Dec 2008) and Q4FY09 (Apr–Jun 2009)** were not found in the Wayback Machine. The 2007–08 releases were linked from `hcltech.com/pdf/<name with spaces>.pdf` (e.g. `Invester ReleaseQ1-V5.pdf`, `Q3 FY07.pdf`, `Press Release Aug 13 - version 1.pdf`) and were never archived. `investors/Downloads/FR/IR_Release_Annual_&_Q4_08-09.pdf` is archived only as a 404. **Every one of these quarters is still covered** as a prior-quarter/year-ago column in adjacent releases (e.g. Q2FY09 from the Q3FY09 and Q2FY10 releases; Q4FY09 from Q1FY10, Q2FY10, Q3FY10 and Q4FY10). What is lost is the first-print (same-quarter) vintage, and reported growth for 2007Q1 and 2007Q3 (only in those releases).
- `hcl.in/attachment/InvestorsFRQ3.pdf` turned out to be the Q3 **FY06** release (Jan–Mar 2006), which is out of window, so it was discarded.
- Today's hcltech.com hosts some legacy files under `/sites/default/files/documents/investor-reports/` (`q3_fy07.pdf`, `q4_fy07.pdf`, `q1_fy08.pdf`, `q2_fy08.pdf`, `q1_fy09.pdf`), but these are **earnings-call transcripts**, not releases. They were not used because every metric collected is in the releases. No live copy was found for the Q2FY09/Q4FY09 releases (name guesses returned 404).
- BSE corporate-announcement API (scrip 532281): "Access Denied" (Akamai block), so it was skipped. NSE was not tried.
- The Wayback CDX/download endpoints were intermittently "Temporarily Offline" (503/504) or refused connections. The helper retries with backoff.
- **Subcontracting cost:** not disclosed in any of these releases. A text search for "subcontract" found no hits. No rows.

### Coverage (cal_q, all vintages combined; no interpolation)
- `revenue` (US$ mn, total): 2007Q1–2012Q1, no gaps (76 rows).
- `revenue_growth_qoq` / `revenue_growth_yoy`, reported: 2007Q2–2012Q1, **gap 2007Q3**, and 2007Q1 is missing too (both were only in the missing releases). Taken from the income-statement growth columns (current quarter) and the CC table's reported-growth rows.
- `revenue_growth_qoq` / `revenue_growth_yoy`, **cc**: 2007Q4–2012Q1, no gaps. The first CC table (Q3FY09 release) goes back to OND'07. The Q1FY09 release gives CC growth only in text ("Revenue on constant currency basis, up 19.2% YoY and 2.4% sequentially"), and that was recorded too. CC is not disclosed before 2007Q4.
- `headcount` total: 2007Q1–2012Q1, no gaps. By service line: `Core Software` (label used through the Q3FY09 release) / `Software Services` (same series, renamed from the Q1FY10 release), `Infrastructure Services`, `BPO Services`: 2007Q1–2012Q1. `IT Services` (software + infrastructure): 2007Q3–2012Q1, gap 2007Q4 (that line is not in the Q4FY07/Q3FY08/Q4FY08 releases).
- `attrition`: IT Services, Core Software/Software Services and Infrastructure Services are LTM and exclude involuntary attrition, 2007Q1–2012Q1. `BPO Services - Offshore` is **quarterly, not annualised**, excludes UK BPO, 2007Q1–2012Q1. The Q4FY12 release labels the LTM rows "Attrition (FY'12)", which is noted on those rows.
- Utilization (Core Software/Software Services only; excludes Infrastructure Services and BPO): `utilization_incl_trainees` = "Offshore – Including trainees", `utilization_excl_trainees` = "Offshore – Excluding trainees" (dimension `… - Offshore`), `utilization_onsite` = "Onsite": 2007Q1–2012Q1, no gaps. `utilization_excl_trainees` with dimension `Software Services - Blended` ("Blended Utilization (Excl. Trainees)"): 2010Q2–2012Q1 only (first shown in the Q4FY11 release).
- `revenue_share` by geography, service line and vertical: 2007Q1–2012Q1, no gaps. Shares sum to 99.8–100.1 in every doc/quarter. Only quarter columns were recorded. The LTM / "Last Year" / FY'12 columns were skipped.

### Definitional breaks
- **Axon acquisition:** Axon Group plc (UK SAP consultancy) was consolidated from **16-Dec-2008**, so Q2FY09 (2008Q4) holds about 2 weeks of Axon and Q3FY09 (2009Q1) is the first full quarter. The Q3FY09 release shows EAS revenue up 117.8% QoQ, and Europe and Energy-Utilities-Public Sector shares jump. Headcount is "inclusive of HCL Axon" from OND'08. Utilization and client metrics include Axon "w.e.f JFM'09". These rows carry a `BREAK:` note. Axon also inflates QoQ growth in 2008Q4–2009Q1 and YoY growth through 2009Q4.
- **Revenue restatement between vintages:** the Q3FY08/Q4FY08/Q1FY09 releases show Dec-07 461.0, Mar-08 484.9, Jun-08 504.0 and Sep-08 504.7. The Q3FY09 and later releases show 453.9, 477.5, 501.7 and 500.9. Reported growth changed with them (e.g. Q4FY08 QoQ 3.9% at first print, 5.1% later). No reconciliation note was found in the available releases. The missing Q2FY09 release likely explained it. Both vintages are kept, and the analyst should prefer the later one for a consistent series.
- **Vertical reclassification** (from the Q3FY09 release, Apr-2009, with restated history back to Mar-08): `Hi-tech` / `Hi-tech - Manufacturing` became `Manufacturing`, `Retail` became `Retail & CPG`, and `Energy-Utilities-Public Sector` was carved out, mainly from Others. `Life Sciences` became `Healthcare` (from the Q4FY10 release, restated to 2009Q2). `Media & Entertainment` / `Media Publishing & Entertainment (MPE)` / `Media, Publishing & Entertainment (MPE)` are label variants.
- **Geography labels:** `US` / `Europe` / `Asia Pacific` through the Q4FY10 release. `Americas` / `Europe` / `Rest of World` from Q1FY11 (restated to 2009Q3), and `ROW` in the Q2–Q3FY12 releases. The Q4FY12 release goes back to `US` / `Europe` / `Asia Pacific` for its 2011Q2 and 2012Q1 columns, which differ from the Q3FY12 release's Americas/ROW values for 2012Q1. These are recorded as reported, not mapped.
- **Service-line labels:** `Custom Application (Industry Solutions)` became `Custom Application Services` (from the Q2FY11 release). `Core Software` became `Software Services` (from the Q1FY10 release) in the headcount, attrition and utilization tables.
- **BPO attrition label:** "Attrition – Quarterly" in the BPO block (through the Q4FY08 release) became "Offshore Attrition – Quarterly" later. The overlapping values are identical (e.g. Jun-08 12.3%), so it is treated as one series.

### Judgment calls
- Revenue is US$ (HCL's reporting currency then). INR convenience-translation figures were ignored.
- If a quarter appears in both the income statement and the CC table of the same release, only one row is kept (values matched in every case). One same-document discrepancy was found: Q3FY09 release, CC YoY growth for Q3FY09 is **27.5%** in the CC table but **27.4%** in the highlights text. The table value is kept, and the text value is noted on the row.
- From the Q4FY10 release onward, the CC (YoY) block's growth row is mislabelled "Growth QoQ". It is recorded as `revenue_growth_yoy` basis `cc`, with a note.
- Headcount rows by segment use dim_type `service_line`. Totals include support staff, as HCL reports them.
- `page` in source_loc is the PDF page index from pdftotext, which matches the page number printed in the release footer ±1.
- Spot-checked 17 values against the PDF text (revenue, headcount, attrition, utilization, revenue shares, CC growth), all correct. A programmatic check also found all 1,713 values in the text of their source document.


## Wipro

**Sources (SEC EDGAR, CIK 0001123799)**
- Results 6-K presentation exhibit (Ex.99.3 through FY10Q3, Ex.3.1 for Q3FY09, Ex.99.2 from Q4FY10). Its "Key Operating Metrics in (Global IT business | IT Services)" table gives revenue shares by vertical and geography and headcount for the current, previous and year-ago quarter.
  - Parsed from the exhibit text by `gfc_wipro_kom.py`.
  - Column-wise layouts were **hand-entered** in `kom_hand.csv`: Q2FY08 and Q3FY08 people rows, Q3FY10, Q4FY11, Q1FY12, Q4FY12 and Q1FY13.
- The "Highlights" slide of the same exhibits gives IT-services revenue (USD mn), sequential/YoY growth (reported and cc when stated), and gross utilization and attrition when stated. These were **hand-entered** in `wipro_hand_metrics.csv` with the exhibit named for each row.
- Quarterly 6-K reports (MD&A, through Q3FY10) and the 20-Fs give "average utilization of billable employees" (hand-entered).
- A few metrics are disclosed only in company-filed transcripts of calls and media interviews (6-K exhibits). `source_doc` says so for each:
  - Q4FY07 attrition (analyst call);
  - Q2FY08 utilization excluding trainees 79.3% (NDTV interview);
  - Q3FY08 attrition 18.1% (wire-agency interview).
- Build script: `gfc_wipro_build.py`.

**Coverage:**
- **Full (21 quarters):** revenue (USD), headcount (total), and vertical and geography shares.
- **reported QoQ growth:** 17 quarters.
- **cc QoQ growth:** 9 quarters (FY09–FY12, where stated).
- **reported YoY growth:** 2007Q1–2008Q4.
- **cc YoY growth:** 2008Q4 and 2009Q1.
- **Utilization:** gross utilization / MD&A "average utilization" for 14 quarters, plus annual FY09–FY12. Net utilization / utilization excluding trainees only for 2007Q2–Q3. Gaps are 2008Q1 and 2010Q2–2011Q4, apart from 2011Q2.
- **Attrition:** 6 quarters only (2007Q1, 2007Q3, 2007Q4, 2011Q3, 2011Q4, 2012Q1), with **inconsistent definitions** (quarter-annualised total; 'attrition in IT services'; voluntary quarter-annualised). Wipro's data sheets on wipro.com, which carried utilization and attrition, are not in EDGAR and were not recovered.

**Definitional breaks**
- **Revenue and headcount perimeter:**
  - FY07–FY08 figures are the **Global IT business** (Global IT Services + BPO), which excludes India/Middle East/AsiaPac IT.
  - From **Q1FY09 (Jun-2008)** the **IT Services segment** includes India & Middle East IT services and BPO. Q1FY09-vintage tables restate the FY08 year-ago columns on the new basis, which is why the 2007Q2–2007Q4 year-ago values differ from the earlier vintages.
  - Wipro total (IT Products, Consumer Care & Lighting) is never used.
- **Headcount:** FY07–FY09Q4 give IT Services / BPO / (India-ME IT) / Total. From Q1FY10 there is a single "Number of employees" (IT Services).
- **Vertical taxonomy:**
  - FY07–FY08: Tech. Services, Financial Solutions, Enterprise Solutions.
  - FY09: TMT, Financial Services, Manufacturing & Healthcare, Retail & Transportation, E&U.
  - FY10: Manufacturing and Healthcare & Services split.
  - FY12 (Q1FY12): Global Media & Telecom, Finance Solutions, Manufacturing & Hitech, Healthcare, Life Sciences & Services, Retail & Transportation, Energy & Utilities.
- **Geography:** North America/Europe/Japan/Others (FY07–08) → US/Europe/Japan/India & ME/Other Emerging Markets (FY09) → "Americas" from Q4FY10 → "APAC & Other Emerging Markets" from Q1FY11.
- **Acquisitions:** Infocrossing (consolidated from 20-Sep-2007; Q2FY08 growth is stated organic) and Citi Technology Services (from Q4FY09).
- **Accounting basis:** US GAAP → IFRS from FY10.
- **Utilization mapping:** Wipro "gross utilization" is mapped to `utilization_incl_trainees` and "net utilization" to `utilization_excl_trainees`. This is a judgment call; Wipro does not use the trainee wording. The MD&A "average utilization of billable employees" equals the gross figures where both exist.


## Tech Mahindra (techm) — GFC window, cal 2007Q1–2012Q1 (Q4FY07–Q4FY12)

Rows: `data/sources/gfc/techm/gfc_techm_rows.csv` (3,746 rows, 54 source documents, all vintages kept as separate rows).
Scripts: `scripts/extract/gfc_techm_download.py` (Wayback download + `manifest.csv`), `gfc_techm_extract.py` (parse + hand-entered values + checks), `gfc_techm_ocr.swift` / `gfc_techm_ocrlines.py` / `gfc_techm_crops.py` (OCR helpers for the scanned results ads). OCR output is in `data/sources/gfc/techm/ocr/`.

### Sources
All documents are Tech Mahindra's own, taken from **Wayback Machine copies of techmahindra.com**. The current techmahindra.com no longer hosts pre-2013 investor files. Every row has `source_url` = `https://web.archive.org/web/<ts>/<original>`, and `notes` ends with `original URL: ...`. Captures were found with the Wayback CDX API (`url=techmahindra.com/*`, mimetype pdf, 2007–2013, plus prefix queries on `content/investor/` and `content/investors/`).
- **Consolidated quarterly fact sheets** ("Fact Sheet data for N Quarters"), `.../Documents/Financials/financialchart/<yr>/TechM_Qn_Fyy_Factsheet.pdf`, `.../2011-2012/Factsheet_QnF12.pdf`, and older copies under `.../content/investor/TML_Consol_Factsheet_data_*.pdf`. There is one for every quarter Q1FY08–Q4FY12 **except Q3FY10**, which is not archived. Q3FY10 values still come from later vintages (Q4FY10 onward). Each sheet shows 9–13 quarters, so most quarters have 5–12 vintages.
  - The financialchart copy `08_q2/TechM_Q2_F08_Factsheet.pdf` is byte-identical to the Q1FY08 sheet (mis-posted by the company). For Q2FY08 I used `content/investor/TML_Consol_Factsheet_data_10_Qtrs_in_Rs_&_$_Q2_07_08.pdf` instead.
  - The Q1FY08 sheet has INR figures only (no USD page).
- **Quarterly results newspaper advertisements** (`TechM_Qn_Fyy_Consolidated.pdf`, `Consolidated_QnF12.pdf`), used for consolidated segment revenue, "Services rendered by Business Associates & Others", and the headline growth. Ten of them (Q4FY09, Q1FY10, Q3FY10, Q4FY10, Q1FY11–Q3FY11, Q2FY12–Q4FY12) are vector-outline PDFs with no text layer. I OCR'd those with macOS Vision and checked every value used visually on 600-dpi crops or through segment-sum checks.
- **Earnings-call transcripts** (company-published, `..._Calltranscripts.pdf`) for attrition, which is not in the fact sheets.
- **Annual reports**: 2007-08 (`content/investor/annual_report_0708.pdf`), 2008-09 (`TML_AR_2009_final.pdf`), 2009-10 (`financialchart/2010.pdf`) and 2010-11 (`AnnualReports/TML_Annual_Report_2010_2011.pdf`), for annual attrition.
- **Not found / skipped**: the Q3FY10 fact sheet (no capture); the FY2011-12 annual report (only the subsidiaries volume `TechMahindra_Subsidiary_2011_12.pdf` is archived); a standalone Q4FY07 fact sheet (Q4FY07 is covered by the 13-quarter Q1FY08 sheet). BSE/NSE archives were not needed. Nothing was paywalled. archive.org was briefly "Temporarily Offline" and a few downloads needed retries, but all eventually succeeded.
- **Mahindra Satyam**: none of its figures were collected. Mahindra Satyam published its own results separately (mahindrasatyam.com); I did not check that site.

### What the reported numbers include (key break: Satyam)
- All fact-sheet and results-ad figures are **Tech Mahindra Limited consolidated**, meaning TML plus its subsidiaries (e.g., Tech Mahindra Americas, BPO subsidiary).
- Tech Mahindra took control of Satyam Computer Services through its subsidiary Venturbay in April–June 2009 (Q1FY10). Satyam is **not consolidated line by line**:
  - The Q1FY10–Q4FY10 ads state that the "results do not include the results of SCSL and its subsidiaries", because SCSL was restating its accounts (CLB/SEBI permission).
  - From Q2FY11 (Oct 2010) Satyam is equity-accounted as an associate (AS 23). Only "Share of profit/(loss) ... in Associate: Satyam Computer Services" appears below PAT.
  - Revenue, headcount, utilization, client and segment data therefore **exclude Satyam** throughout 2007Q1–2012Q1. There is no level break in these series from the acquisition.
  - Indirect effects: acquisition-financing interest rises from Q1FY10 (not collected), and the fact sheets add a Satyam associate line from Q2FY11.
- **Q2FY11 (2010Q3) revenue is inflated.** It includes Rs 2,989.5 mn of **pass-through revenue** from one customer's end-to-end implementation (fact-sheet note). This drives the USD 328.2 mn quarter and the jumps in RoW share, onsite/offshore mix and top-client share. Flagged in notes on the revenue and segment rows.
- **Q4FY10 (2010Q1)**: a customer (not named in the ad) restructured long-term contracts from 1 Apr 2009, paying Rs 96,819 lakh of restructuring fees. These are amortised as revenue over the contract term, with Rs 5,012 lakh recognised in Q4FY10 and Rs 20,049 lakh in FY10 (ad note 4). The effect is embedded in reported revenue.
- **Q4FY12 (2012Q1)**: an exceptional provision of Rs 678.7 mn for dues from two Indian telecom operators. This is below operating profit and does not affect revenue.

### Metrics and coverage (cal_q; "vint" = number of vintages)
| metric | dimension(s) | first–last | gaps / remarks |
|---|---|---|---|
| revenue (INR_mn, USD_mn) | total | 2007Q1–2012Q1 | none (Q3FY10 only from later vintages). USD for Q4FY07/Q1FY08 first appears in the Q2FY08 sheet. Small restatements, e.g., Q4FY07 INR 8,745 vs 8,753 in the Q3FY08 sheet; Q1FY09 11,164 → 11,163 |
| revenue_growth_yoy / _qoq | total, INR, reported | 2007Q1–2012Q1 | Only the one or two growth figures in each ad's headline (quarter, ytd or annual). Many quarters have none (e.g., 2009Q1–Q4 yoy, 2011Q3). No USD or cc growth is reported in these documents. I did not compute any |
| headcount | total + S/w Professionals, BPO Professionals, Sales & Support | 2007Q1–2012Q1 | period-end; consolidated TML incl. BPO and support staff; excludes Satyam. Components sum to total (checked) |
| utilization_incl_trainees | total | 2007Q1–2012Q1 | "IT Utilization % including Trainees" up to the Q1FY10 sheet. From the Q2FY10 sheet the label is just "IT Utilization %", with identical historical values (same series). Trainee treatment for quarters first reported after Q1FY10 is not stated (flagged in notes). IT only, excludes BPO |
| attrition | total | 2007Q1–2012Q1 (sparse) | **Not in fact sheets.** Quarterly values are verbal figures from call transcripts: Q1FY08 18, Q2FY08 31 (effective ~21), Q3FY08 ~20, Q4FY08 ~18, Q4FY09 11 (voluntary), Q4FY10 22 (annualised), Q1FY11 27 (IT, annualised), Q2FY11 ~30 (IT, quarterly annualised), Q4FY11 ~25, Q3FY12 20, Q4FY12 19. Annual values from annual reports: FY07 20.7 and FY08 29.6 (company-wide incl. BPO), FY08 24.7, FY09 18.7 and FY10 20.0 (IT only); FY10 17 (call). Definitions are inconsistent (see notes column). Missing: 2008Q2–Q4, 2009Q2–Q4, 2010Q4, 2011Q2–Q3 |
| revenue_share (geography) | North America (to Q4FY11 sheet) / Americas (from Q1FY12 sheet), Europe, Rest of World | 2007Q1–2012Q1 | shares sum to 100 (checked). The label change from "North America" to "Americas" is a relabel, with identical historical values. Dimension kept exactly as printed |
| revenue_share (client_bucket) | Top client, Top 5 clients, Top 10 clients | 2007Q1–2012Q1 | The top client is not named in the fact sheets (commonly known to be BT). Falls from 65% (Q4FY07) to 37% (Q4FY12) |
| clients_bucket | USD1/2/5/10/15/20/25/50mn+ | 2007Q1–2012Q1 | "No. of Million $ Clients"; the LTM basis is not stated |
| active_clients | total | 2007Q1–2012Q1 | |
| revenue_share_offshore / revenue_share_onsite (new metric) | total | 2007Q1–2012Q1 | "Revenue On/Off Break-up (in %)" |
| segment_revenue (INR_lakh) | Telecom Service Provider, Telecom Equipment Manufacturer, BPO, Others, total | 2007Q2–2012Q1 | Consolidated segment tables from the Q1FY09 ad onward; the comparative columns reach back to Q1FY08. Ads for Q4FY07–Q4FY08 show only **standalone** segments, which I did not collect, so 2007Q1 is missing. Segments sum to total within 2 lakh (source rounding). Totals match the fact-sheet INR revenue |
| subcontracting_cost (INR_lakh) | total | 2007Q4–2012Q1 | Line "Services rendered by Business Associates & Others", printed in consolidated results from the Q3FY09 ad (comparative back to Q3FY08). Ads before Q3FY09 do not break this line out. The Q1FY10 ad prints 11,267 in both the Q1FY10 and Q1FY09 columns; the Q1FY11 ad restates Q1FY10 as 11,546. Recorded as printed |

New units/metrics: `INR_lakh` (1 lakh = 0.1 INR mn; the ads report in Rs lakhs and I did not convert) and `revenue_share_onsite`.

### Judgment calls
- Fact sheets were parsed by position with pdfplumber: each value is matched to the nearest column header by right edge, and annual/YTD "Total" columns are dropped. Checks run: geography sums to 100, headcount components sum to total, and ad segment totals match fact-sheet revenue to within Rs 1 mn. 12 random fact-sheet values were spot-checked against pdftotext lines, all correct. Ad values were checked visually on crops: Q4FY09, Q1FY10 and Q1FY11 segment/expenditure tables, and the Q2FY12 and Q3FY12 subcontracting rows.
- Utilization: every vintage goes into `utilization_incl_trainees`, with the label caveat in notes (see the table above).
- Attrition figures are verbal and approximate ("about", "around"). I recorded each as stated, with a quote in notes; basis (LTM vs annualised quarterly, IT-only vs total) differs by quarter. Q3FY11 is not recorded because management only restated the previous quarter's 30%.
- Headline growth rows are INR consolidated growth printed in the ad headline (rounded to whole %). Annual and nine-month headline growth rates are kept with `period_type` annual/ytd.
- `doc_date` = board-meeting / results date printed in the ad or transcript. For annual reports I used an approximate 30 June.
- Duplicate downloads (identical md5 between `content/investor/` and `financialchart/` copies) are kept locally, but rows cite only one copy per document.


## Cognizant

**Sources (SEC EDGAR, CIK 0001058290)**
- 8-K Ex.99.1 earnings releases: YoY and QoQ growth as stated (body text or headline) and headcount from the "About Cognizant" boilerplate, which is rounded ("approximately/over X employees as of ...").
- 10-Q:
  - quarterly revenue (USD thousands ÷1000);
  - segment revenue for Financial Services, Healthcare, Manufacturing/Retail/Logistics and Other, as `segment_revenue` levels (USD mn), current and prior-year three-month columns;
  - revenue by customer location (North America / Europe / Asia→"Other");
  - "annualized turnover/attrition, including both voluntary and involuntary" for the three months.
- 10-K: the "Selected quarterly financial data" table (quarterly revenues, used for Q4s), full-year attrition, and Item 1 headcount (FY06–FY07 only).
- Build script: `gfc_cognizant_build.py`.

**Coverage:**
- **All 21 quarters:** revenue, reported YoY growth, and attrition. Attrition is three-month annualized for Q1–Q3; for Q4 the 10-K gives full-year values (period_type annual), and 2011Q4 has the quarterly 10% from the release.
- **Headcount:** 2007Q4–2012Q1.
- **QoQ growth:** 16 quarters (not stated in the 2009Q1–2010Q1 releases).
- **Segment and geography revenue:** Q1–Q3 only, because the 10-K gives annual figures only. No Q4 segment data.
- **Utilization:** not disclosed in filings (only on calls; not collected).
- **Subcontracting:** not disclosed.

**Breaks:** geography label "Asia" (2007–2008) became "Other". Revenue from growth sentences is not used; revenue comes from the 10-Q/10-K statements.


## Accenture

**Sources (SEC EDGAR):** Accenture Ltd (CIK 0001134538) through Q3FY09, then Accenture plc (CIK 0001467373).
- 8-K Ex.99.1 earnings releases, from the financial table in each release (three-month columns, USD thousands):
  - net revenues (revenues before reimbursements) with % change in USD and in local currency (`basis`=`cc`);
  - net revenues and growth by operating group (dim_type vertical), geographic region, and type of work (Consulting/Outsourcing → service_line), as `segment_revenue` and `segment_growth_yoy`;
  - new bookings (`bookings`, from FY08Q4) and utilization/attrition sentences where present.
- 10-Q/10-K MD&A: "Annualized attrition, excluding involuntary terminations", "Utilization ... approximately X%", and headcount ("headcount ... to approximately/more than X as of ...").
- Build script: `gfc_accenture_build.py`.

**Fiscal calendar:** FY ends 31-Aug. Q2FY07 (period_end 2007-02-28) → 2007Q1, through Q2FY12 (2012-02-29) → 2012Q1. The calendar mapping follows SCHEMA (Nov→Q4, Feb→Q1, May→Q2, Aug→Q3).

**Coverage:**
- **All 21 quarters:** revenue with USD and local-currency YoY growth, attrition, and operating-group, geography and type-of-work revenue and growth.
- **Utilization:** 2008Q1–2012Q1 (Q2FY08 onward).
- **Headcount:** 2007Q3 and 2008Q3–2012Q1; missing FY07Q2–Q3 and FY08Q1–Q3 (10-Qs then did not state it).
- **Bookings:** 2008Q3–2012Q1, missing 2011Q3.
- **QoQ growth:** not reported by Accenture.

**Breaks:**
- **Operating groups:** 'Government' (FY07) became 'Public Service'. From 1-Sep-2009 (FY10) **'Health & Public Service'** was formed from Public Service plus the healthcare parts of Products, with prior periods reclassified in FY10 releases. 'Communications & High Tech' was renamed **'Communications, Media & Technology'** from FY12.
- **Utilization and attrition:** Accenture "utilization" has no trainee split; it is recorded under `utilization_incl_trainees` by convention. Attrition excludes involuntary terminations.
- **Operating-group sums:** the groups sum to net revenues less a small 'Other' line, which is not recorded.
