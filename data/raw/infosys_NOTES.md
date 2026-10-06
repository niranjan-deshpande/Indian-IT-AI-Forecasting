# Infosys (`infosys`): collection notes

Output: `data/raw/infosys.csv`, 11,934 rows in long format following SCHEMA.md. Every row carries a `source_url`. Coverage runs from Q1FY12 through Q1FY27 (Apr-2011 to Jun-2026). Some Q1FY11–Q4FY11 values also appear, taken from comparative columns in the FY12 documents.

Every multi-quarter table column was kept as its own vintage row. Fact sheets show the current quarter, the prior quarter and the year-ago quarter, and the older sheets' constant-currency block shows 5–6 quarters. To get the as-first-reported value, filter to rows where `fiscal_q` equals the quarter named in `source_doc`. USD revenue is identical in every vintage, so no restatements were found. Segment tables in FY19-format sheets do contain restated history for the FY18 quarters.

## 1. Sources

| Source | URL pattern | Used for |
|---|---|---|
| Quarterly **fact sheet** PDFs (61 of them, Q1FY12–Q1FY27) | `https://www.infosys.com/investors/reports-filings/quarterly-results/<YYYY-YYYY>/q<n>/documents/fact-sheet.pdf` (older sheets use `.../Q<n>/Documents/fact-sheet.pdf`) | revenue USD/INR, QoQ/YoY growth (reported and cc), revenue shares by vertical, geography and service offering, segment growth, Digital/Core, project/contract type, client data (active, added, buckets, top-client shares), effort and utilization, onsite/offshore revenue, person-months, employee metrics (headcount, breakdown, gross/lateral/net additions, attrition). Also some TCV values from the page-1 banner |
| SEC EDGAR 6-K, quarterly results filings (CIK 1067491), one per quarter from Q3FY11 to Q1FY27 | `https://www.sec.gov/Archives/edgar/data/1067491/<accession>/exv99wNN.htm` | Ex 99.1 IFRS USD press release: TCV, net-new %, AI. IFRS USD and INR condensed financial statements or IFRS earnings releases: **Cost of technical sub-contractors**. Earnings-call and press-conference transcript exhibits: TCV for quarters where the press release has none |

- **infosys.com blocks scripts.** It returned HTTP 403 to curl with a browser user-agent and also to WebFetch. The fact sheets were therefore downloaded as archived copies of the original PDFs from the Internet Archive, using `https://web.archive.org/web/<timestamp>id_/<original url>`. `source_url` holds the **original infosys.com URL**. The Wayback timestamp is in `source_doc`, and the full map is in `data/sources/infosys/factsheets/meta.json`.
- The same fact sheet is also filed on EDGAR as Ex 99.4 of each results 6-K. Before Q2FY24 that exhibit is only GIF images, so it was not parsed. From Q2FY24 on it is HTML text and could be a backup URL.
- **Skipped:** the Feb-2026 "Investor AI Day" transcript (6-K 0001067491-26-000006) is image-only (GIFs), so no OCR was attempted. Nothing required a login or payment. The in-app browser was not used.
- Local copies:
  - `data/sources/infosys/factsheets/*.pdf`
  - `data/sources/infosys/edgar/<accession>/` (all exhibits of the 65 results 6-Ks)
  - `edgar_6k_index.json`
  - `wayback_cdx_quarterly_results.txt`
- Scripts, run from the project root in this order:
  1. `scripts/extract/infosys_edgar_index.py`
  2. `infosys_download.py`
  3. `infosys_wayback_factsheets.py`
  4. `infosys_factsheet_parse.py`
  5. `infosys_subcontract_parse.py`
  6. `infosys_manual_tcv_ai.py`
  7. `infosys_combine.py`

  Shared helpers are in `infosys_common.py`.

## 2. Coverage (as-first-reported quarter; vintage rows extend one year earlier)

| metric | first–last | gaps / comments |
|---|---|---|
| revenue (USD_mn, INR_cr) | Q1FY12–Q1FY27 | none |
| revenue_growth_qoq / _yoy (reported, cc) | Q1FY12–Q1FY27 | none. Annual FY growth rows (`period_type=annual`) are included where the fact sheet shows them |
| headcount (point) | Q1FY12–Q1FY27 | none. Consolidated total employees |
| headcount_breakdown | Q1FY12–Q1FY27 | S/W professionals and Sales & Support throughout. Billable, Banking product group and Trainees only through Q4FY18 |
| net_additions, gross_additions, attrition_count | Q1FY12–Q4FY19 | not disclosed from Q1FY20 |
| lateral_additions | Q1FY12–Q4FY17 | not disclosed from Q1FY18 |
| attrition | Q1FY12–Q1FY27 | several definition breaks, see §3 |
| utilization_incl_trainees / _excl_trainees | Q1FY12–Q1FY27 | none |
| effort_share_offshore / _onsite | Q1FY12–Q1FY27 | none |
| revenue_share_offshore / _onsite | Q1FY12–Q4FY18 | not disclosed from Q1FY19 |
| person_months (billed onsite/offshore, non-billable, trainees, sales & support) | Q1FY12–Q4FY18 | not disclosed from Q1FY19 |
| revenue_share, vertical and geography | Q1FY12–Q1FY27 | none. Segment scheme breaks, see §3 |
| revenue_share, service_line | Q1FY12–Q4FY18 (service offerings); Digital share Q1FY19–Q4FY23 | service-offering split ends Q4FY18. Digital/Core stopped after Q4FY23. No service-line split from Q1FY24 |
| segment_revenue (Digital/Core, USD_mn) | Q1FY19–Q4FY23 | – |
| segment_growth_qoq (reported, cc) | Q1FY12–Q4FY19 | Q1FY19 missing (no growth columns in that sheet). FY12–FY17 values come from narrative sentences; Q4FY18 from the "Revenue Segmentation Growth" table; Q2–Q4FY19 from table columns |
| segment_growth_yoy (reported, cc) | Q1FY20–Q1FY27 | Q1FY26 Rest of World reported growth shown as "-" in the sheet, so omitted |
| revenue_share_fixed_price | Q1FY12–Q4FY19 | not disclosed from Q1FY20 |
| active_clients, clients_added, clients_bucket, top_client_share | Q1FY12–Q1FY27 | the set of revenue buckets narrows over time (FY12–FY14 have many; from FY15 only 1/5/10/25/50/75/100/200/300mn; from FY19 only 1/10/50/100mn+) |
| subcontracting_cost (USD_mn quarterly) | Q3FY11–Q1FY27 | USD Q4 quarterly is **not** available FY12–FY20. Q4 USD statements in those years show only year-ended figures, which are recorded as `period_type=annual` (FY14–FY20). Q4FY12 and Q4FY13 have no USD value at all. Q3FY13 USD is present |
| subcontracting_cost (INR_cr quarterly) | Q3FY11–Q1FY27 | Q2FY15 missing. Q4FY11 missing |
| tcv (large deals, USD_mn) | Q1FY16–Q1FY27 quarterly; FY17, FY19–FY26 annual | none quarterly. Q3FY16–Q2FY19 and Q4FY23/25/26 come from call or press-conference transcripts |
| tcv_net_new_share | Q4FY20–Q1FY27 (sparse) | gaps where not stated |
| ai_disclosure | Q1FY24 (80 active GenAI client projects), Q3FY26 (AI services revenue 5.5% of revenue), Q1FY27 (8.2%) | Q4FY26 not disclosed (management declined on the press call) |
| fresher_hires | not collected | not in fact sheets. Appears only ad hoc in calls |

## 3. Definitional breaks

- **Attrition.** The `dimension` column holds the firm's exact label.
  - Q1FY12–Q4FY15: `Attrition % (LTM)`, excluding subsidiaries.
  - Q1FY16–Q4FY20: quarterly annualized, reported twice as `Attrition % (Annualized Standalone)` and `Attrition % (Annualized Consolidated)`. Q1FY16 uses lower-case "standalone/consolidated".
  - Q1FY21–Q4FY21: `Voluntary Attrition % (Annualized - IT Services)`.
  - Q1FY22 onward: `Voluntary Attrition % (LTM - IT Services)`.
  - These series are **not comparable** across the breaks.
- **Utilization and effort.** FY12–FY14 tables are titled only "Effort and Utilization", with scope not stated. From Q1FY15 they say "Consolidated IT Services" (IT services, excluding BPM). The notes column records which applies.
- **Headcount.** Consolidated group total employees throughout, including subsidiaries such as Infosys BPM/BPO and acquired entities. Acquisitions add step changes. Examples, with quarters approximate: Panaya (Q4FY15), Kallidus/Skava (Q1FY16), Noah (Q3FY16), Fluido and WongDoody (FY19), Stater (Q1FY20), Simplus, GuideVision, Kaleidoscope and Blue Acorn (FY21), BASE life science (FY23), InSemi and in-tech (Q4FY24–Q1FY25), MRE Consulting and Versent (FY26). The Q1FY27 call says acquisitions added about 1.1% QoQ to revenue.
- **Verticals.**
  - FY12–FY18 used a 4-group scheme: Banking & Financial Services + Insurance; Manufacturing; Retail & Life Sciences (Retail & CPG, Transport & Logistics, Life Sciences, Healthcare); Energy, Utilities, Communications & Services (Energy & Utilities, Telecom, Others). Labels changed along the way: all caps in Q1FY12, "Insurance, Banking & Financial Services" through Q2FY14, then "Banking & Financial Services, Insurance" from Q3FY14.
  - "Manufacturing" became **"Manufacturing & Hi-Tech"** from Q4FY16 to Q4FY18.
  - **Q1FY19 reorganization** to 8 business segments: Financial services, Retail, Communication, Energy/Utilities/Resources & Services, Manufacturing, Hi Tech, Life Sciences, Others. The Q1FY19–Q4FY19 sheets restate FY18 comparatives. "Hi Tech" is spelled "Hi-Tech" from Q1FY21 (label change only). No further vertical reorganization is visible through Q1FY27.
  - Sub-segments are named `Parent > Child` (for example `Retail & Life Sciences > Life Sciences`) and flagged in `notes`. Only top-level rows sum to 100.
- **Service lines.**
  - Q1FY12: Business Operations / Consulting & System Integration / Products, Platforms & Solutions.
  - Q2FY12–Q4FY12 transition, then Business IT Services / Consulting, Package Implementation & Others / Products, Platforms and Solutions through Q4FY16.
  - "Products, Platforms and Others" in FY17. "Products and Platforms" in FY18.
  - Q4FY18 adds memo rows "New Services" and "New Software", which are already included in the rows above and flagged.
  - From Q1FY19, Digital/Core replaces service offerings. In FY19 it is split further by Services vs Products & Platforms.
  - Digital is no longer reported from Q1FY24.
- **Fixed-price share.** FY12–FY18 is "Revenues by Project Type, excluding products". FY19 is "Revenues by Contract Type, including products". Not reported after Q4FY19.
- **Segment growth dimension names.** FY12–FY17 narrative sentences use abbreviations (`FSI`, `MFG`, `MFG & Hi-Tech`, `RCL`, `ECS`), recorded as written.
- **TCV.** This is Infosys "large deals" (TCV above $50mn). FY17 values mix committed and "framework" deals (see notes). Q3FY21 ($7.13bn) and Q2FY24 ($7.7bn) include mega deals.
- **Subcontracting cost.** "Cost of technical sub-contractors" from the IFRS cost-of-sales break-up note, consolidated. The USD and INR versions come from separate IFRS statements.

## 4. Judgment calls

- Parsing is automated with `pdftotext -layout` plus the rules in the parser. Sub-segment hierarchy is found by checking whether a parent row equals the sum of the rows beneath it. Parent/child checks passed: top-level shares sum to 100 ±0.6 in every table.
- Narrative growth sentences ("declined by X% sequentially") are recorded as negative numbers. "Both sequentially and in constant currency" and "and also in constant currency" give the same value for both bases. "Was flat in constant currency" is recorded as 0.
- Revenue rows come from the three-month IFRS P&L extract (current, prior-year and prior-quarter columns) and from the older constant-currency block. Exact within-document duplicates were dropped. No conflicting values were found within any document.
- TCV, net-new %, and AI figures were **hand-entered**. `infosys_manual_tcv_ai.py` checks each one against a quote in the local copy of the document, and all quotes matched.
  - Q2FY20 uses the press-release $2.8bn. The call said $2.85bn.
  - Q3FY16 uses $362mn from the press conference. The call said "nearly $360mn".
  - Q3FY26 AI share (5.5%) is taken from the Q1FY27 earnings-call transcript, because the Investor AI Day deck is images only.
- Fact-sheet rows (11,620 of them) were parsed from the Wayback copy, but `source_url` gives the original infosys.com URL, which should open in a normal browser. The remaining 314 rows point to sec.gov.
- Spot check: 15 randomly sampled fact-sheet values were compared with the PDF text, including column position, and all 15 matched. USD revenue matches the press-release figures (for example Q1FY16 $2,256mn and Q1FY27 $5,082mn). Headcount net additions equal the first differences of headcount wherever both are reported.
- New metric names added beyond the SCHEMA vocabulary: `clients_added`, `top_client_share`, `effort_share_onsite`, `revenue_share_onsite`, `person_months`, `headcount_breakdown`, `lateral_additions`, `attrition_count`, `tcv_net_new_share`, `tcv_net_new`.
