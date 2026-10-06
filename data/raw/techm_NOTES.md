# Tech Mahindra (`techm`) — collection notes

Output: `data/raw/techm.csv` has 8,089 rows covering Q1FY16 (Jun-2015) to Q1FY27 (Jun-2026), which is 45 quarters. Indian FY (Apr–Mar). `cal_q` is the calendar quarter that contains the period end.
Rebuild: `python3 scripts/extract/techm_extract.py`. It uses `techm_common.py` and `techm_handentered.py`. `techm_ocr.swift` was an OCR aid for the image-only PDFs.
Source copies are in `data/sources/techm/`. Text layers are in `txt/`, OCR dumps in `ocr/` and call transcripts in `transcripts/`. The scraped list of every IR document is `_ir_links_quarterly_earnings.csv`.

## 1. Sources

All sources are on the company IR site: `https://www.techmahindra.com/investors/quarterly-earnings/`. The files themselves are at `https://insights.techmahindra.com/investors/<file>`.

| Document type | Quarters | Metrics used | How extracted |
|---|---|---|---|
| **Fact sheet PDFs**, old format. Each shows the previous FY's 4 quarters plus the current FY's quarters to date. | Q1FY17–Q3FY20. This gives FY16 comparatives. | Revenue (INR and USD), headcount (software / BPO / sales & support / total), IT attrition LTM, IT utilization (incl. and excl. trainees), vertical and geography mix, active clients, % repeat business, $-client buckets, top 5/10/20 client share, onsite/offshore IT revenue split, average USD/INR rate | Parsed from the PDF text layer |
| **Fact sheet PDFs**, new format. Each shows 3 columns: current quarter, previous quarter, same quarter last year. | Q1FY21–Q4FY25 | Same as above, plus the "Revenue Growth (USD)" table (QoQ/YoY, reported and cc). From FY21–FY22 that table is also split by Communications/CME vs Enterprise. Also segment QoQ/YoY growth next to the mix tables, and net new deal wins (TCV). | Parsed from the PDF text layer |
| **Data sheet xlsx** (full history back to FY16) | Q3FY24–Q1FY27 (10 files) | Same operating metrics, with unrounded values; percentages are stored as fractions and were multiplied by 100 | The Q1FY27 data sheet is loaded in full, FY17–FY27. From the other 9 data sheets only the latest 5 quarters are kept, as vintages. FY16 columns are skipped in every data sheet (see judgment calls). |
| **Consolidated results, SEBI format** | Every quarter Q1FY17–Q1FY27; each shows the quarter, the previous quarter and the same quarter last year | `subcontracting_cost` (the "Subcontracting Expense(s)" line), `employee_cost`, revenue, and `segment_revenue` for IT and BPO/BPS | Parsed. Ten image-only PDFs were hand-entered (see below). |
| **Press releases** | FY17–FY20 and FY26–FY27 | USD revenue growth, reported and cc; "Digital" revenue share (FY20 only) | Hand-entered |
| **Earnings presentations** | FY26–FY27 | Geography and vertical mix plus QoQ/YoY growth. The Q1FY26 cc growth also comes from here, because the Q1FY26 press release leaves it out. Also the AI workforce statements. | Mix and growth parsed; cc growth and AI statements hand-entered |
| **Earnings-call transcripts** (company-published) | Q2FY18, Q4FY18, Q2FY20 | cc growth that was only disclosed on the call | Hand-entered |

**Hand-entered from image-only PDFs.** There is no text layer in these files:
- Consolidated results for Q1FY17, Q2FY17, Q3FY18, Q4FY18, Q1FY19, Q2FY19, Q3FY19, Q4FY19, Q2FY20 and Q1FY26
- The Q4FY19 press release

The pages were OCR'd with macOS Vision. Each value was then checked visually against the rendered page, and IT + BPO segment revenue was confirmed to equal total revenue. These rows are flagged `hand-entered` in `notes`.

**Skipped or blocked:**
- **Image-only fact sheets** (Q2FY17, Q3FY18, Q4FY18, Q1FY19, Q3FY19, Q4FY19, Q4FY20) were not parsed. Each of those quarters is still covered by at least one text-based fact sheet or data sheet vintage.
- **Q2FY24 press release** is image-only. It was not needed because the Q2FY24 fact sheet covers the same data.
- **BSE API** (`api.bseindia.com`) returned "Access Denied" (Akamai), so it was not used.
- **FY14–FY16 quarterly documents** are not on the IR site: its FY filter jumps from FY2012-13 to FY2016-17. FY16 is covered through the FY17 comparatives.
- Nothing needed a login or payment.

**Doc dates.** These come from the press-release datelines. Two are approximate:
- Q2FY24 is set to the 28th of the month after quarter end, because its press release is image-only.
- Q4FY19 was read from the OCR text.

## 2. Coverage (all metrics are quarterly unless stated)

| metric | first–last | gaps / comments |
|---|---|---|
| `revenue` USD_mn and INR_mn | Q1FY16–Q1FY27 | none |
| `revenue_growth_qoq` cc | Q2FY17–Q1FY27 | Missing in FY16, Q1FY17, Q1FY18, Q3FY18, Q4FY19, Q1FY20. Q2FY18 and Q4FY18 come only from call transcripts. |
| `revenue_growth_yoy` cc | Q2FY17–Q1FY27 | Missing in FY16, Q1FY17, FY18, FY19 (only the FY19 annual figure exists), Q3FY20, Q4FY20. The Q1FY20 value is a judgment call (see §4). |
| `revenue_growth_*` reported | Q1FY17–Q1FY27 | QoQ missing Q4FY19 and Q1FY20; YoY missing Q2FY20–Q4FY20. The company also reports levels, but no growth rate was computed from them. |
| `headcount` (total plus components) | Q1FY16–Q1FY27 | none. The label is "BPO professionals" up to Q1FY25 in fact sheets and "BPS professionals" after that; data sheets use BPS throughout. |
| `attrition` | Q1FY16–Q1FY27 | none |
| `utilization_incl_trainees` | Q1FY16–Q1FY27 | none |
| `utilization_excl_trainees` | Q1FY16–Q4FY25 | Discontinued from FY26 |
| `subcontracting_cost` INR_mn | Q1FY16–Q1FY27 | **none.** Q1FY16–Q3FY16 and Q1FY27 have a single vintage; every other quarter has at least 2. |
| `employee_cost` INR_mn | Q1FY16–Q1FY27 | none |
| `segment_revenue` IT and BPO/BPS | Q1FY16–Q1FY27 | The label changes from BPO to BPS in the Q1FY25 filing (Q4FY24 and earlier quarters shown as comparatives) |
| `revenue_share` geography (Americas / Europe / Rest of world) | Q1FY16–Q1FY27 | none |
| `revenue_share` vertical | Q1FY16–Q1FY27 | Three classifications (see §3) |
| `segment_growth_qoq/yoy` | Q1FY21–Q1FY27 | Fact sheets and FY26+ presentations only |
| `tcv` (net new deal wins) | Q1FY19–Q1FY27 | Not disclosed before FY19 |
| `clients_bucket` ($1/5/10/20/50mn+), `client_concentration` | Q1FY16–Q1FY27 | none |
| `active_clients` | Q1FY16–Q4FY25 | Discontinued from FY26 |
| `repeat_business_pct` | Q1FY16–Q4FY24 | Discontinued afterwards |
| `revenue_share_offshore/onsite` (IT revenue) | Q1FY16–Q4FY22 | Replaced by the IT headcount split |
| `headcount_share_offshore/onsite` (IT headcount) | Q1FY22–Q1FY27 | Restated back to Q1FY22 |
| `fx_usdinr_avg` | Q1FY16–Q1FY27 | none |
| `revenue_share` "Digital" | Q1FY20–Q4FY20 | Press releases only |
| `ai_disclosure` | Q3FY26, Q4FY26 | Workforce AI-enablement percentages only. No AI revenue or bookings were found. |

**New metric names** added to the vocabulary: `repeat_business_pct`, `client_concentration`, `revenue_share_onsite`, `headcount_share_offshore`, `headcount_share_onsite`, `fx_usdinr_avg`.

**Subcontracting % of revenue is not published.** No Tech Mahindra fact sheet, data sheet or presentation reports `subcontracting_pct_rev`. Only the INR level from the results filings is recorded. No ratio was computed.

## 3. Definitional breaks

**Vertical reclassifications.** The classification version is written in `notes`, and in `source_loc` for data-sheet rows.
- **v1** (up to FY21): Communication(s); Manufacturing; Technology, Media & Entertainment; BFSI; Retail, Transport & Logistics; Others.
- **v2** (from Q1FY22; FY21 restated): Communications, Media & Entertainment (CME); Manufacturing; Technology; BFSI; RTL; Others. Deal wins are split CME/Enterprise.
- **v3** (from Q1FY24; the data sheet carries v3 from FY24 and v2 up to FY24, so FY24 has both): Communications; Manufacturing; Hi-Tech and Media; BFSI; RTL; Healthcare & Life Sciences; Others. "Others" drops from about 10.7% to about 4%.
- **Q4FY25:** customer groups that span several businesses were re-aligned to one vertical, and the prior-year comparative was restated.
- **Earlier restatements:** vintages differ in small ways. For example, Q1FY16 TME is 7.3% in the Q1FY17 sheet but 6.7% in the Q3FY17 sheet, which is normal regrouping.
- **Presentations (FY26+)** use different labels ("Technology, Media and Entertainment", "ROW", "BFSI") for the same v3 segments.

**Onsite/offshore.** From Q1FY23 the fact sheet replaced the IT revenue on/off split with the IT headcount split, restated back to Q1FY22.

**Accounting.** FY16 figures were restated to Ind AS (note in the Q1FY17 fact sheet). Q1FY17–Q3FY17 results use the older SEBI format, where subcontracting is labelled "Services rendered by Business Associates and Others". From Q4FY17 the line is "Subcontracting Expenses", and the Q3FY16 and Q4FY16 figures in that filing are nearly identical to the earlier ones. Results were in Rs lakh until Q2FY19 and in Rs million from Q3FY19.

**Attrition and utilization.** Both are IT only and cover the "organic business" (marked #). Attrition is LTM. Fact sheets round to whole %; data sheets hold unrounded values. From FY24 utilization is shown to 2 decimals. Utilization excluding trainees was discontinued in FY26.

**Headcount.** Total = software (IT) professionals + BPO/BPS professionals + sales & support, consolidated, at period end. There is a restatement: the Q3FY20 data sheet shows BPO 50,886 and sales & support 6,874, while the Q3FY20 fact sheet shows 51,096 and 6,664.

**Acquisitions** noted in the primary documents:
- Pininfarina (subsidiary from 30-May-2016, Q1FY17)
- BIO Agency (1-Jul-2016) and Target Group (17-Aug-2016), both Q2FY17
- HCI / CJS Solutions (4-May-2017, Q1FY18)
- Objectwise (Oct-2019) and BORN Group (Nov-2019), both Q3FY20; Cerium, 70% stake announced in Q3FY20
- Tenzing and Momenton (Q2FY21 press release)
- Lodestone (Q4FY21 press release)
- Eventus Solutions (Q2FY22 press release)
- Avant Techno Solutions (Q1FY27 press release)

The sharp Q2FY22–Q1FY23 headcount jump (126k to 158k) is consistent with acquisitions plus hiring. The collected documents do not quantify acquired headcount. Com Tec Co, Allyis and similar acquisitions were not mentioned in the documents collected, so they are not verified here.

## 4. Judgment calls

- **Vintages.** Every document's figures are kept as separate rows; `doc_date` identifies the vintage. The Q1FY27 data sheet is the latest restated full history.
- **FY16 columns in the data sheets were skipped.** In the xlsx, the FY2015-16 columns are shifted up one row relative to the labels from the "Revenue by Industry – Restated" block down. The restated-classification rows for FY16 actually hold v1 data. FY16 is taken from the text fact sheets instead.
- **Rs lakh to INR mn.** Values reported in Rs lakh were divided by 10; the original lakh figure is kept in `notes` for the hand-entered rows.
- **Ambiguous press-release wording on cc growth.** The Q1FY20 figure (3.7%) was recorded as YoY. The Q2FY20–Q4FY20 figures were recorded as QoQ, based on which reported-growth bullet each sits under and whether the numbers are consistent. For Q2FY20 the call transcript separately gives about 7.3% YoY cc. These rows carry notes.
- **Segment growth currency.** The fact sheet does not label the currency of the segment QoQ/YoY columns. They are recorded as `basis=reported`, assumed USD, with a note.
- **Client buckets** are TechM's "No. of Million $ Clients". The documents do not state whether this is on LTM revenue.
- **"Digital" share (FY20)** is company-defined and overlaps other segments. Its `dim_type` is `service_line`.
- **Annual figures.** A few annual cc/reported growth rates (FY18, FY19, FY20, FY26) are included with `period_type=annual` on the Q4 row.
- **Spot checks.** 14 randomly sampled parsed values were checked against the PDF text and all matched. Cross-document consistency was also checked: revenue, subcontracting, employee cost, segment revenue and total headcount agree within 0.6% across all vintages apart from the Q3FY20 restatement above. Mix shares sum to 100 ±1 within each document and classification. Headcount components sum to the total in every document.
