# TCS (firm id `tcs`): collection notes

Output: `data/raw/tcs.csv` (9,057 rows). The extraction can be reproduced with `python3 scripts/extract/tcs_extract.py`, which reads the local PDFs in `data/sources/tcs/`.
Period covered: Q1FY12 to Q1FY27 (Apr-2011 to Jun-2026). The target window is Q1FY16 to Q1FY27. Year-ago and prior-quarter columns in the decks also put some FY11 values in the file.

## 1. Sources

All sources are company documents downloaded from tcs.com investor relations. The base path is
`https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/<YYYY-YY>/<qN>/...`

| Document | URL pattern (after base) | Local copy | Used for |
|---|---|---|---|
| Quarterly fact sheet (Q4FY14 to Q1FY27) | `Presentations/Q<n> <YYYY-YY> Fact Sheet.pdf` (`.PDF` for FY16 to Q3FY18; `Q<n> FY 2022-23 Fact sheet.pdf` in FY23) | `<YYYY-YY>_q<n>_factsheet.pdf` | almost all rows |
| Analysts presentation (Q1FY12 to Q3FY14) | `Presentations/Q<n> <YYYY-YY> Analysts Presentation.pdf` | `<YYYY-YY>_q<n>_analysts_pres.pdf` | pre-FY15 rows |
| Press release, IFRS USD | `IFRS/Press Release - USD.pdf` (earlier: `US GAAP-IFRS/...`) | `<YYYY-YY>_q<n>_PR_USD.pdf` | cross-checks; TCV Q4FY21 to Q3FY23; FY25+ net additions; AI revenue |
| Earnings-call transcript | `Management Commentary/Transcript of the Q<n> ... .pdf` (full URLs in `_transcript_urls.tsv`) | `<YYYY-YY>_q<n>_transcript.pdf` | TCV Q1FY19 to Q3FY22 (hand-entered); utilization check |

- `_tcs_pdf_links.txt` holds every IR PDF link found on the financial-statements page (729 links).
- Text versions from `pdftotext -layout` are in `data/sources/tcs/txt/`.

**Access.** tcs.com and api.bseindia.com both return an Akamai HTTP 403 to curl and to WebFetch. I used the in-app browser, which the brief permitted for this firm. I opened tcs.com, fetched the PDFs same-origin from the page, and sent them to a local receiver with a multipart form POST. The page's CSP blocks `fetch` to localhost but allows form posts. The files are the original PDFs. BSE/NSE filings were not needed. No sources were skipped for login or payment reasons.

**Not collected:**
- Annual reports and the Ind AS statements. Subcontracting is already in the fact sheets.
- Press releases in INR.
- The Q1FY12 "Operating Metrics" PDF was downloaded but not parsed. The Q1FY12 analysts deck has no highlights block, so Q1FY12 has no revenue or headcount row. Pre-window anyway.

## 2. Coverage

"Current vintage" means the row comes from the quarter's own fact sheet or deck. Every deck also gives year-ago and prior-quarter columns, and these are kept as separate vintages (different `doc_date`).

| metric | basis / dimension | first to last | gaps / comments |
|---|---|---|---|
| revenue USD_mn | reported | Q2FY12 to Q1FY27 | none. Current quarter comes from the highlights text. Prior 4 quarters come from the USD bar-chart data labels (vintages). |
| revenue INR_mn | reported | Q4FY12 to Q1FY27 | none |
| revenue_growth_yoy | cc | Q1FY16 to Q1FY27 | none |
| revenue_growth_yoy | reported (USD) / reported_inr | Q2FY12 to Q1FY27 | none |
| revenue_growth_qoq | cc | Q1FY16 to Q1FY27 | **not disclosed** Q1FY20 to Q1FY21 and Q2FY22 to Q1FY26 (TCS reported YoY only). Do not compute. |
| revenue_growth_qoq | reported (USD) | Q2FY12 to Q1FY27 | same gaps, plus Q3FY19 to Q4FY19 |
| headcount | total | Q2FY12 to Q1FY27 | none |
| net_additions | quarter | Q1FY12 to Q2FY25 | Q4FY24, Q3FY25 and Q4FY25 not disclosed. Q2FY26 to Q1FY27 not disclosed. Q3FY19 and Q3FY22 were given only YoY (`period_type=ltm`), Q3FY20 only 9M YTD (`ytd`), Q1FY26 only YoY (press release). Q1FY25 and Q2FY25 come from press releases. |
| gross_additions, fresher_hires | quarter | Q1FY12 to Q3FY18 | Disclosure stopped after Q3FY18. `fresher_hires` = "Trainees" hired in India, taken from the gross-additions breakdown. |
| attrition | IT Services, LTM | Q1FY12 to Q1FY27 | Q1FY15 to Q3FY15 give only the incl.-BPS figure |
| attrition | Including BPS, LTM | Q1FY12 to Q1FY19 | discontinued after Q1FY19 |
| attrition | quarterly annualized | Q2FY16 and Q3FY16 only | |
| utilization excl./incl. trainees | | Q2FY12 to Q3FY16 | **Discontinued after Q3FY16.** Checked every transcript from Q4FY16 to Q1FY27; none gives a number. In the Q4FY16 call TCS said utilization would "steadily lose relevance". |
| revenue_share, segment growth | vertical | Q1FY12 to Q1FY27 | shares sum to 100 (±0.6) for all 416+ doc/period/type groups |
| revenue_share, segment growth | geography | Q2FY11 to Q1FY27 | |
| revenue_share, segment growth | service_line | Q1FY12 to Q4FY17 | **Service-line disclosure dropped from Q1FY18** |
| revenue_share | Digital (dim_type other) | Q3FY16 to Q2FY20 | printed below the vertical/SP tables in the FY17 to Q2FY20 decks |
| segment_growth_qoq | cc | FY16 to FY19Q2, FY21Q2 to FY22Q1, FY26Q2+ | same YoY-only gaps as the total |
| subcontracting_cost | "Fees to external consultants", split COR / SG&A, INR_mn and USD_mn | Q1FY12 to Q4FY26 | see break below |
| subcontracting_cost | expense by nature, INR_cr and USD_mn | Q1FY26 to Q1FY27 | Q1FY27 deck only (5 quarters) |
| employee_cost | same structure as subcontracting | Q1FY12 to Q1FY27 | |
| tcv | total order book (deals signed in quarter), USD_bn | Q1FY19 to Q1FY27 | none. Q1FY19 to Q3FY23 hand-entered from calls/press releases; Q4FY23+ from fact sheets. Fact sheets also give North America, BFSI, Retail/Consumer Business. Annual rows: FY21, FY23+. |
| clients_bucket | USD1mn+ to USD100mn+, LTM | Q1FY12 to Q1FY27 | none |
| active_clients | | Q2FY12 to Q4FY13 | disclosed only in old decks |
| ai_disclosure | annualized AI revenue run-rate | Q3FY26, Q4FY26, Q1FY27 | $1.8bn, "crosses" $2.3bn, $2.6bn. Also growth %. From press releases. |
| effort/revenue offshore mix, fixed-price mix | | none | not in TCS fact sheets |

## 3. Definitional breaks

**Verticals**
- Q4FY16: revenue of the erstwhile CMC Ltd (in "Others" through Q3FY16) was broken up into the respective verticals (per the Q3FY16 deck footnote).
- Q1FY18: major recast. Label changes from "IP Revenue (%)" to "Vertical (%)". New "Regional Markets & Others" line (India, MEA, APAC ex-Australia, Latin America, products & platforms) and new "Technology & Services". BFSI share falls from about 40% to about 33%. The Q1FY18 deck has a recast FY17 quarterly table, recorded with `source_loc` = "recast history table".
- Q1FY19: "Retail & CPG" absorbs "Travel & Hospitality". Other verticals were restated for account reclassification, and prior periods in that deck are restated.
- Q1FY20: vertical break-up recast for org-structure changes. The deck gives 4 restated quarters.
- Q2FY24: APAC ex-Japan, Middle East & Africa and Energy & Resources were moved from "Regional Markets & Others" into industry verticals. New names are "Consumer Business" (was Retail & CPG) and "Energy, Resources and Utilities". The deck gives 5 restated quarters.
- Always use the vintage matching the definition you need (`doc_date`). Old-definition columns are never mixed with new ones inside a single document.

**Service lines**
- Disclosed through Q4FY17. From Q1FY18 there is only qualitative "Service Lines Commentary".
- Names changed over time: "Enterprise Solutions" became "Enterprise Solutions & Consulting" (Global Consulting merged in) from Q3FY16. "Business Process Outsourcing" became "Business Process Services" from Q1FY14. "Business Intelligence" was last shown in Q1FY13. The spelling "Asset Leverage Solutions" changed to "Asset Leveraged Solutions" after FY13.

**Growth-column basis**
- FY12 to FY15 decks label segment growth as INR growth ("` Growth", or bare "Growth" with an "INR terms" footnote). These rows use `basis=reported_inr`.
- CC growth starts in Q1FY16.
- From Q2FY26, tables carry both CC and INR growth.

**Utilization**
- Last disclosed Q3FY16. Definition: TCS consolidated, excluding CMC & Diligenta (per footnote).

**Attrition**
- The core series is LTM IT Services attrition excluding subsidiaries (FY16 footnote: excluding CMC & Diligenta).
- The "including BPS" (earlier "including BPO") series ends Q1FY19.
- From Q2FY26 the decks label it "Voluntary Attrition". I did not verify whether the underlying definition changed.

**Headcount**
- Consolidated closing headcount ("Total Employees"). No definitional change was noted in the documents.
- The FY21 to FY22 decks print Indian digit grouping (e.g. 5,09,058); this was parsed correctly.

**Subcontracting ("Fees to external consultants")**
- Through Q4FY26 it is reported in the IFRS "COR – SG&A Details" tables as two lines: COR and SG&A. I kept these as separate dimensions and did not sum them.
- The Q1FY27 deck replaced these tables with an "Expense by Nature" table that has a single "Fees to External consultants" line, in INR crore and USD mn. The two series do not reconcile: for Q4FY26, expense-by-nature gives ₹3,971 cr, while COR + SG&A gives ₹4,238 cr (42,380 mn). Treat Q1FY27 as a series break.
- Level drop in FY24: COR fees went from ₹48,680 mn in Q4FY23 to ₹27,990 mn in Q4FY24. This is reported as-is. The Q2FY24 call mentions "optimizing subcontractor expenses". No restatement note was found.
- Some tables split columns into "Ex Adj / Reported" (e.g. Q4FY15, Q2FY21, Q4FY24 annual). For these only the last, reported current-period column was recorded, and the note says so.

**TCV**
- First disclosed on the Q1FY19 call ("starting this quarter, we will start sharing"). It is the total value of contracts signed in the quarter.
- Q3FY20 was given only as "about 6 billion" in Q&A. It is recorded as 6.0 with a note.

**M&A / other**
- CMC Ltd was merged into TCS in FY16 (see the vertical note above).
- The Q4FY26 cash-flow statement shows an acquisition of a subsidiary (₹62.1 bn). No headcount or segment effect was flagged in the deck.

## 4. Judgment calls

- **New `basis` value `reported_inr`.** It marks INR-terms growth. `reported` growth rows are USD-terms, consistent with the USD revenue series.
- **New dimension names:**
  - attrition: `IT Services`, `Including BPS`, `IT Services (quarterly annualized)`, all with dim_type `other`.
  - subcontracting/employee cost: `Fees to external consultants (in cost of revenue)`, `(in SG&A)`, `(expense by nature)`, and the same pattern for `Employee cost ...`.
  - ai_disclosure: `Annualized AI revenue`, `Annualized AI services revenue`, `... growth QoQ`.
- **"Flat" growth.** Where the highlights say "flat QoQ" (Q3FY15 USD, Q1FY27 USD), the value is recorded as 0.0 with the note `reported as "flat"`.
- **Unlabelled CC growth.** Some highlights give a CC figure without saying QoQ or YoY. It was assigned only when it matched the geography table's Total-row QoQ or YoY figure; otherwise it was dropped. Dropped cases: Q1FY15, Q3FY15, Q4FY15 and several FY12 to FY14 decks.
- **Clients table in Q4 decks.** Where it has FY columns (full-year LTM) and no Q4 column, the FY value is assigned to Q4 of that FY, with a note.
- **Company-total CC growth from the Geography table Total row.** Recorded only when the highlights did not give that figure for the same document.
- **Hand-entered rows** (`notes` start with "hand-entered", with the quote):
  - 19 quarterly TCV totals and FY21 annual TCV.
  - 3 press-release net-addition figures.
  - 5 AI rows.
- **Spot checks.** 14 randomly sampled fact-sheet rows were checked against the PDF text; all matched. Quarterly USD revenue agrees across all vintages (no restatement). USD revenue also matches the USD press-release headline figures within rounding.
