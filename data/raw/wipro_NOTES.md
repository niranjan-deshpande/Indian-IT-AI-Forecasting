# Wipro (firm id `wipro`) — collection notes

Output: `data/raw/wipro.csv`, 12,565 rows, 110 distinct source documents. Fiscal year runs Apr–Mar (FY27 = Apr-2026..Mar-2027). Coverage: Q1FY14 (from prior-year columns in FY15 datasheets) through Q1FY27 (quarter ended 2026-06-30, released 2026-07-16).

Reproducible pipeline (run in order):
1. `scripts/extract/wipro_datasheets.py`: parses every quarterly analyst datasheet (`data/sources/wipro/txt/*data*sheet*.txt`, made with `pdftotext -layout`) into `data/sources/wipro/parsed_datasheets.csv`. Parse issues are logged to `data/sources/wipro/parse_datasheets.log`. The only leftover unmatched lines are guidance ranges, wrapped prior-year fragments and page footers, all skipped on purpose.
2. `scripts/extract/wipro_ifrs.py`: reads the quarterly IFRS interim consolidated statements into `parsed_ifrs.csv`. It extracts revenue, employee compensation and sub-contracting.
3. `scripts/extract/wipro_build.py`: merges the two parsed files, adds the hand-entered rows (press releases and transcripts, flagged `hand-entered` in notes), and writes `data/raw/wipro.csv`.

## 1. Sources

All source documents are on wipro.com's quarterly results page (`https://www.wipro.com/investors/quarterly-results/`). They are fetched with curl and saved in `data/sources/wipro/`. Local filenames use the form `<FY folder>_<quarter folder>_<original name>`.
- **Analyst datasheet**, one per quarter, Q1FY15–Q1FY27 (49 files). URL pattern: `https://www.wipro.com/content/dam/nexus/en/investor/quarterly-results/<YYYY-YYYY>/<qNfyNN>/...data-sheet...pdf` or `datasheet-qNfyNN.pdf`. Each covers the current quarter, the prior full year, and prior-year quarters (6–8 columns). **Every column is kept as a separate vintage row.** `doc_date` is the results date, and prior-period columns carry a note saying so.
- **IFRS interim consolidated financial statements**, Q1FY16–Q1FY27 (e.g. `consolidated-financial-statement-q1fy27.pdf`, `IFRS-Financials-Jun-2015.pdf`). Used for consolidated revenue (INR mn), employee compensation and "Sub-contracting and technical fees" (note "Expenses by nature"). Only the three-month columns are used: the current quarter plus the prior-year comparative, which gives two vintages.
- **Press releases**, used for the results dates (`doc_date`) and a few bookings figures. **Company-published earnings-call transcripts**, used for large-deal TCV before datasheet disclosure (Q3FY21–Q1FY23) and for AI disclosures.
- EDGAR (CIK 0001123799) 6-K and 20-F filings carry the same press releases and IFRS statements. I checked the submissions JSON (`data/sources/wipro/edgar_submissions.json`) but cite the wipro.com PDFs, because they are the same documents and have stable direct URLs.
- **Nothing was paywalled or blocked.** No login was needed anywhere.
- **Missing extraction:** the Q1FY19 IFRS statement's income-statement revenue line is not in the PDF text layer, so no current-vintage consolidated revenue row exists for Q1FY19. The Q1FY20 comparative column (139,777) does cover it.

## 2. Coverage (target quarters, all vintages combined)

| metric | dimension | first | last | gaps / comments |
|---|---|---|---|---|
| revenue (USD_mn) | IT Services | Q1FY14 | Q1FY27 | none. IT Services segment revenue from datasheets. |
| revenue (INR_mn) | total (consolidated) | Q1FY15 | Q1FY27 | none (Q1FY19 only from the Q1FY20 comparative) |
| revenue | IT Services (earlier segment definition) | Q1FY18 | Q2FY19 | Q3FY19 datasheet only (pre-ISRE-carve-out continuity) |
| revenue_growth_qoq | IT Services, reported and cc | Q1FY14 (rep) / Q1FY15 (cc) | Q1FY27 | none |
| revenue_growth_yoy | IT Services, reported and cc | Q1FY15 | Q1FY27 | current quarter only (Growth Metrics table) |
| headcount | total (= "Closing Employee Count") | Q4FY16 | Q1FY27 | starts Q4FY16 only through the Q4FY17 datasheet's restated columns (see breaks) |
| headcount | IT Services head count (pre-FY18 definition) | Q1FY14 | Q4FY17 | old definition, not comparable with total |
| headcount | Sales & Support Staff - IT Services | Q1FY14 | Q1FY27 | an average in older sheets ("avg"), a closing count later (see source_loc) |
| utilization_excl_trainees | total | Q1FY14 | Q1FY27 | none. Net utilization excluding trainees, IT Services excl. BPS/DOP and non-integrated acquisitions. |
| utilization_gross (new) | total | Q1FY14 | Q4FY23 | discontinued after Q4FY23 |
| utilization_net_excl_support (new) | total | Q1FY14 | Q1FY21 | discontinued |
| attrition | Voluntary TTM | Q1FY14 | Q1FY27 | none. IT Services excl. BPO/BPS/DOP (scope in notes). |
| attrition | Voluntary Quarterly Annualized; BPS/DOP quarterly | Q1FY14 | Q1FY21 | discontinued |
| attrition | BPS/DOP post-training quarterly | Q1FY14 | Q1FY27 | none |
| revenue_share | vertical | Q1FY14 | Q1FY27 | none (taxonomy changes, see breaks) |
| revenue_share | geography | Q1FY14 | Q1FY27 | none |
| revenue_share | service_line | Q1FY14 | Q4FY23 | **no service-line or practice mix from Q1FY24 onward** |
| segment_growth_qoq/yoy | vertical, geography (reported and cc) | Q1FY15 | Q1FY27 | current quarter only |
| segment_growth_qoq/yoy | service_line | Q1FY15 | Q4FY23 | QoQ missing Q1FY17. YoY missing Q1–Q4FY17 (not disclosed; practices reclassified). FY15–FY16 practices: reported growth only, no cc. |
| clients_bucket | USD1/3/5/10/20/50/75/100mn+ (TTM revenue) | Q1FY14 | Q1FY27 | none |
| active_clients, new_clients (new) | total | Q1FY14 | Q1FY27 | none |
| revenue_share_fixed_price | total | Q1FY14 | Q1FY27 | none (IT Services subset, scope in notes) |
| revenue_share_offshore | total | Q1FY14 | Q1FY27 | none |
| revenue_share_onsite (new) | total | Q1FY14 | Q1FY21 | discontinued |
| subcontracting_cost (INR_mn) | total (consolidated) | Q1FY15 | Q1FY27 | none |
| employee_cost (INR_mn) | total | Q1FY15 | Q1FY27 | none |
| bookings (total TCV, USD_mn) | total | Q3FY23 | Q1FY27 | datasheets from Q3FY23 (via Q4FY23+ sheets). Q3–Q4FY23 also hand-entered from PR/call. |
| bookings_growth_yoy (new) | total | Q1FY23 | Q2FY23 | PR text only, hand-entered |
| tcv (large deals ≥$30mn TCV) | Large deals | Q3FY21 | Q1FY27 | Q3FY21–Q2FY22 and Q1FY23 from call transcripts (hand-entered). **No figure for Q3FY22 or Q4FY22.** Datasheet figures from Q1FY23. |
| ai_disclosure | various (training counts, $1bn AI investment, AI agents) | Q1FY24 | Q1FY26 | transcripts, hand-entered. No AI revenue or bookings figure is disclosed. |

Not collected (disclosed but out of scope): operating margin, revenue guidance, currency mix, top-1/5/10 client concentration, % revenue from existing customers, and the annual (FY) columns and FY growth columns in datasheets. The annual columns could be added if needed.

## 3. Definitional breaks

- **Headcount definition (Q4FY17).** Through Q3FY17, datasheets report "Closing Head Count – IT Services". The Q4FY17 datasheet shows both that and "Closing Employee Count – IT Services": 181,482 vs 165,481 for Q4FY17, a gap of about 16k that persists back to Q4FY16. From Q1FY18 only "Closing Employee Count" is shown. No explanatory footnote was found in the datasheet or on the call.
  - The old series is stored as dimension `IT Services head count (pre-FY18 definition)`. The `total` series starts Q4FY16.
- **Other headcount restatements.**
  - Q3FY19 restated earlier quarters for the ISRE carve-out: Q2FY19 went from 175,346 to 171,451.
  - Q2FY25 datasheet (Note 6): "corrected the previously reported headcount for Q3'24, Q4'24 and Q1'25". Both vintages are kept.
  - Q1FY18 was later restated from 166,790 to 161,439.
  - Q2FY19 shows a +10.6k jump as originally reported (164,659 → 175,346). It is recorded as reported, with no cause asserted.
- **IT Services segment.**
  - Q3FY19: India State Run Enterprise (ISRE) business carved out of IT Services, with prior quarters restated. That sheet also shows "earlier segment" revenue.
  - Q4FY21: prior-period revenue restated "due to change in revenue segment policy".
  - Q1FY25: ISRE re-included in IT Services and prior quarters restated, except FY24 guidance and utilization.
- **Geography.**
  - FY14–Q2FY19: Americas / Europe / India & Middle East / APAC & Other Emerging Markets.
  - Q3FY19–Q3FY21: Americas / Europe / Rest of the World.
  - Q4FY21 onward: Strategic Market Units Americas 1 / Americas 2 / Europe / APMEA (CEO Delaporte's reorg effective Jan 2021; the Q4FY21 sheet restates Q4FY20–Q3FY21).
  - Q1FY27: LatAm and Canada customers realigned into Americas 1/2 sectors, and hi-tech and airports folded into Americas 1 sectors. Prior periods readjusted in that sheet.
- **Verticals.**
  - FY14–FY16: Global Media & Telecom, Finance Solutions, Manufacturing & Hitech, Healthcare/Life Sciences & Services, Retail/Consumer Goods & Transportation, Energy/Natural Resources & Utilities.
  - Q1FY17 realignment: Communications, Consumer (Business Unit), Manufacturing & Technology, etc.
  - Q1FY18: BFSI naming, Healthcare and Lifesciences.
  - Q1FY19: seven verticals, with Manufacturing and Technology split and a Health Business Unit.
  - Q4FY21: sectors under the SMU model (BFSI, Consumer, Health, ENU, Manufacturing, Technology, Communications).
  - Q2FY25: Technology and Communications merged.
  - Q3FY25: Manufacturing and ENU merged into "Energy, Manufacturing and Resources".
- **Service lines.**
  - FY15: ADM, BAS, GIS, ATS, BPO, Product Engineering, R&D, Consulting.
  - Q1FY16 "practices" realigned. **FY15–FY16 practice shares sum to about 112% as printed**, suggesting overlapping definitions. Recorded as reported and flagged in notes.
  - FY17–FY18: five practices.
  - Q1FY19: new practices (DOP, Cloud & Infrastructure, Data/Analytics & AI, Modern Application Services, Industrial & Engineering Services).
  - Q4FY21–Q4FY23: two Global Business Lines, iDEAS and iCORE.
  - From Q1FY24: no service-line disclosure.
- **Attrition and utilization scope.** Both follow a datasheet sub-heading that excludes BPO/BPS (called DOP / DO&P in FY19–FY24), India & Middle East in early years, and a changing list of acquisitions (Designit, cellent, HPS, Appirio, Cooper, Infoserver, Topcoder, Capco, Rizing, …) until they are integrated.
  - The exact sub-heading is copied into each row's `notes`.
  - Voluntary quarterly annualized attrition, net utilization excluding support, and onsite revenue share were all discontinued after Q1FY21. Gross utilization was discontinued after Q4FY23.
- **Growth-rate adjustments.** Some growth rates are adjusted for divestments per datasheet notes: Q2FY19–Q4FY19 for the hosted data-centre divestment, and FY21 sheets "adjusted for the impact of divestments".
  - Acquisitions to keep in mind: Capco, closed Q1FY22 (IT Services +12.0% QoQ cc in Q1FY22); also Appirio (FY17), HPS (FY16), Designit and cellent (FY16), Ampion, Edgile, LeanSwift, CAS and Rizing (FY22–FY23).
- **Bookings definitions** (datasheet notes): Total Bookings = TCV of all orders booked in the period, including renewals and changes to existing contracts. Large deals = TCV ≥ $30mn.
  - The Q1FY23 call said large deals were "nearly $1.5 billion", but later datasheets show 1,123 for Q1FY23. Both are kept.
- **Subcontracting row label:** "Sub-contracting/technical fees/third party application" in FY16, then "Sub-contracting/technical fees", then "Sub-contracting and technical fees". Consolidated, INR mn, quarterly. The Q1FY17 comparative was restated slightly (20,304 → 20,360).

## 4. Judgment calls

- **New metric names:** `utilization_gross` and `utilization_net_excl_support`, because Wipro's gross and net-excl-support definitions do not map cleanly to "incl trainees". Also `revenue_share_onsite`, `new_clients` and `bookings_growth_yoy`.
- **IT Services series:** IT Services revenue and growth use dimension `IT Services` (dim_type other). Consolidated INR revenue uses `total`. Wipro does not report consolidated USD revenue other than as a convenience translation, which was not recorded.
- **Attrition series** are separated by dimension: `Voluntary TTM` (headline), `Voluntary Quarterly Annualized`, `BPS/DOP quarterly`, `BPS/DOP post-training quarterly`.
- **Parsing method:** columns are assigned by character position, using monotonic alignment to header columns calibrated on complete rows. When a row has every column it is mapped in order.
  - I spot-checked 15 random values against the PDF text, including column position; all matched.
  - Automatic checks: vertical and geography shares sum to 98.5–101.5 in every vintage and quarter; headcount and revenue move smoothly apart from the documented breaks.
- **Hand-entered "over $X" and "nearly $X" figures** are recorded at X, with the qualifier quoted in notes. Q2FY22 "nine deals with a TCV of $580 million" is assumed to be large deals, which is flagged. The half-year H2FY21 total TCV of $7.1bn was not recorded.
- **Deduplication:** identical duplicate rows within one document are dropped. This happens for the repeated IT Services revenue row in older sheets and for QoQ growth that appears in both the operating table and the Growth Metrics table.
