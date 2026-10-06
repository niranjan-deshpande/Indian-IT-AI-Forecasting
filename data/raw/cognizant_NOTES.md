# Cognizant (`cognizant`) — data collection notes

Output: `data/raw/cognizant.csv` (5,961 rows, long format per SCHEMA.md). Calendar fiscal year; `fiscal_q` = `cal_q` = `YYYYQn`.
Coverage window: 2013Q4 (earlier, bonus) through 2026Q2 (latest reported, 8-K of 2026-07-29).

Reproduce: `python3 scripts/extract/cognizant_download.py` (downloads from EDGAR into `data/sources/cognizant/edgar/`, writes `manifest.csv`), then `python3 scripts/extract/cognizant_extract.py` (writes the CSV). Text versions of each filing are in `data/sources/cognizant/txt/`; slide images read by hand are in `data/sources/cognizant/slides/`.

## 1. Sources

All rows come from SEC EDGAR filings for CIK 0001058290 (URL pattern `https://www.sec.gov/Archives/edgar/data/1058290/<accession>/<file>`):

| Document | Years | What was taken |
|---|---|---|
| 8-K Ex.99.1 earnings release (Q4 2016: Ex.99.2) | 2014-02 to 2026-07 (Q4 2013 to Q2 2026) | revenue; segment and geography table (USD level, % of total, QoQ growth to 2017, YoY reported, YoY cc from Q4 2018); headcount; net additions; attrition text (from Q4 2022); bookings, book-to-bill, quarterly bookings growth, large-deal count |
| 8-K Ex.99.2/99.3 earnings supplement (slide deck) | 2019-10 to 2026-07 (Q3 2019 to Q2 2026) | revenue-growth tables (total and each segment, reported and cc, multi-quarter history back to Q1 2017); employee metrics (headcount, attrition, utilization); TTM bookings series |
| 10-Q / 10-K | 2014 to 2026 | revenue by service line and contract type (Note 2 disaggregation, 2018+); service-line share and growth text (2015–2018Q3); fixed-price share, active clients, strategic clients, top-5/top-10 client share (2013–2016); 10-K year-end headcount by location (India, North America, Europe/UK/Continental Europe, other) |

Every row has `source_url` pointing to the specific EDGAR document, plus `source_loc` (table or slide number) and `doc_date` (filing date).

**Vintages:** each supplement repeats 5 to 12 quarters of history, and every vintage is kept as its own row (so `doc_date` differs). I cross-checked every (quarter, dimension, basis) group across vintages. Revenue growth, segment growth, headcount, utilization, bookings and book-to-bill agree across all vintages. The only differences:
- Rounding: the Q1 2023 supplement shows Tech-Services attrition as whole numbers (30%) where later decks show 29.8%.
- The genuine Q1 2026 attrition recast (see section 3).

**Skipped or blocked sources:**
- investors.cognizant.com: the brief says it returns 403 to curl, so I did not use it. EDGAR carries the same releases and supplements.
- 8-K 2019-07-31 Ex.99.2 (Q2 2019 supplement): slide images with no usable text layer. Not read, because every value it carries also appears in the Q3 2019 and later decks.
- 8-K Ex.99.2 one-page "fact sheets" (2020Q3 onward): skipped as redundant. Their headcount and attrition figures repeat the release and deck.
- 8-K 2017-02-08 Ex.99.3 (2017 investor-day presentation): not a periodic KPI source.
- 8-K 2020-04-09 (COVID business update) and 8-K 2023-01-12 (CEO appointment with preliminary items): not quarterly results, so skipped.
- Earnings-call transcripts: not used. Utilization is disclosed in the primary supplements, so transcripts were not needed.
- No paywalled or login sources were needed.

**New metric names added (not in SCHEMA vocabulary):**
- `attrition_total`: quarterly-annualized total (voluntary + involuntary) attrition.
- `attrition_involuntary`: quarterly-annualized involuntary attrition.
- `bookings_growth_yoy`: reported % growth in bookings, with period_type quarter, ltm, ytd or annual.
- `large_deals_count`: number of deals with TCV of USD100mn or more signed in the quarter.

**Conventions:**
- `bookings` is in USD_bn and is TTM (`ltm`) unless marked `annual` (full-year).
- `book_to_bill` is TTM unless marked `annual` or `quarter` (the single "in-period" value, Q3 2022).
- Contract-type revenue (Time and materials / Fixed-price / Transaction or volume-based) is stored as `segment_revenue` with `dim_type=other`.

## 2. Coverage (rows per metric group; first and last quarter; quarters with no row)

| metric | dimension scope | basis | period_type | rows | first | last | gaps (no row for quarter) |
|---|---|---|---|---|---|---|---|
| active_clients | total: total | na | point | 4 | 2013Q4 | 2014Q3 | none |
| ai_disclosure | total: total | na | annual | 1 | 2025Q4 | 2025Q4 | none |
| ai_disclosure | total: total | na | point | 4 | 2023Q2 | 2026Q1 | 2023Q3, 2023Q4, 2024Q1, 2024Q2, 2024Q3, 2024Q4, 2025Q1, 2025Q2, 2025Q3 |
| attrition | other: Tech Services | na | ltm | 104 | 2022Q1 | 2026Q2 | none |
| attrition | total: total | na | ltm | 43 | 2020Q1 | 2022Q4 | none |
| attrition | total: total | na | quarter | 106 | 2019Q1 | 2022Q4 | none |
| attrition_involuntary | total: total | na | quarter | 42 | 2020Q1 | 2022Q4 | none |
| attrition_total | total: total | na | quarter | 107 | 2017Q1 | 2021Q4 | none |
| book_to_bill | total: total | reported | annual | 4 | 2021Q4 | 2023Q4 | 2022Q1, 2022Q2, 2022Q3, 2023Q1, 2023Q2, 2023Q3 |
| book_to_bill | total: total | reported | ltm | 16 | 2022Q1 | 2026Q2 | 2022Q4, 2023Q4 |
| book_to_bill | total: total | reported | quarter | 1 | 2022Q3 | 2022Q3 | none |
| bookings | total: total | reported | annual | 2 | 2021Q4 | 2022Q4 | 2022Q1, 2022Q2, 2022Q3 |
| bookings | total: total | reported | ltm | 112 | 2020Q4 | 2026Q2 | none |
| bookings_growth_yoy | total: total | reported | annual | 2 | 2022Q4 | 2023Q4 | 2023Q1, 2023Q2, 2023Q3 |
| bookings_growth_yoy | total: total | reported | ltm | 13 | 2023Q1 | 2026Q2 | 2023Q4 |
| bookings_growth_yoy | total: total | reported | quarter | 20 | 2021Q3 | 2026Q2 | none |
| bookings_growth_yoy | total: total | reported | ytd | 3 | 2020Q2 | 2021Q3 | 2020Q4, 2021Q1, 2021Q2 |
| clients_bucket | client_bucket: strategic clients | na | point | 12 | 2013Q4 | 2016Q3 | none |
| headcount | geography: Continental Europe, Europe, India, North America, Rest of World (other locations), United Kingdom | na | point | 54 | 2014Q4 | 2025Q4 | 33 quarters without a value (sparse series) |
| headcount | total: total | na | point | 314 | 2013Q4 | 2026Q2 | none |
| large_deals_count | total: total | na | quarter | 6 | 2025Q1 | 2026Q2 | none |
| net_additions | total: total | na | ltm | 13 | 2022Q4 | 2026Q2 | 2024Q4, 2025Q1 |
| net_additions | total: total | na | quarter | 23 | 2013Q4 | 2026Q2 | 28 quarters without a value (sparse series) |
| revenue | total: total | reported | quarter | 51 | 2013Q4 | 2026Q2 | none |
| revenue_growth_qoq | total: total | reported | quarter | 17 | 2013Q4 | 2017Q4 | none |
| revenue_growth_yoy | total: total | cc | quarter | 269 | 2017Q1 | 2026Q2 | none |
| revenue_growth_yoy | total: total | reported | quarter | 289 | 2013Q4 | 2026Q2 | none |
| revenue_share | client_bucket: Top 10 clients, Top 5 clients | reported | quarter | 14 | 2014Q2 | 2016Q3 | 2014Q4, 2015Q4 |
| revenue_share | geography: Continental Europe, Europe - Total, North America, Rest of Europe, Rest of World, United Kingdom | reported | quarter | 255 | 2013Q4 | 2026Q2 | none |
| revenue_share | service_line: Consulting and technology services, Outsourcing services | reported | quarter | 24 | 2015Q1 | 2018Q3 | 2015Q4, 2016Q4, 2017Q4 |
| revenue_share | vertical: 7 dims | reported | quarter | 204 | 2013Q4 | 2026Q2 | none |
| revenue_share_fixed_price | total: total | reported | annual | 4 | 2013Q4 | 2016Q4 | 2014Q1, 2014Q2, 2014Q3, 2015Q1, 2015Q2, 2015Q3, 2016Q1, 2016Q2, 2016Q3 |
| revenue_share_fixed_price | total: total | reported | quarter | 1 | 2014Q1 | 2014Q1 | none |
| revenue_share_fixed_price | total: total | reported | ytd | 2 | 2014Q2 | 2014Q3 | none |
| segment_growth_qoq | geography: Europe - Total, North America, Rest of Europe, Rest of World, United Kingdom | reported | quarter | 85 | 2013Q4 | 2017Q4 | none |
| segment_growth_qoq | vertical: Communications, Media and Technology, Financial Services, Healthcare, Manufacturing/Retail/Logistics, Other, Products and Resources | reported | quarter | 68 | 2013Q4 | 2017Q4 | none |
| segment_growth_yoy | geography: Continental Europe, Europe - Total, North America, Rest of Europe, Rest of World, United Kingdom | cc | quarter | 155 | 2018Q4 | 2026Q2 | none |
| segment_growth_yoy | geography: Continental Europe, Europe - Total, North America, Rest of Europe, Rest of World, United Kingdom | reported | quarter | 255 | 2013Q4 | 2026Q2 | none |
| segment_growth_yoy | service_line: Consulting and technology services, Outsourcing services | reported | quarter | 24 | 2015Q1 | 2018Q3 | 2015Q4, 2016Q4, 2017Q4 |
| segment_growth_yoy | vertical: Communications, Media and Technology, Financial Services, Health Sciences, Healthcare, Products and Resources | cc | quarter | 1058 | 2017Q1 | 2026Q2 | none |
| segment_growth_yoy | vertical: 7 dims | reported | quarter | 1138 | 2013Q4 | 2026Q2 | none |
| segment_revenue | geography: Continental Europe, Europe - Total, North America, Rest of Europe, Rest of World, United Kingdom | reported | quarter | 255 | 2013Q4 | 2026Q2 | none |
| segment_revenue | other: Fixed-price, Time and materials, Transaction or volume-based | reported | annual | 24 | 2018Q4 | 2025Q4 | 21 quarters without a value (sparse series) |
| segment_revenue | other: Fixed-price, Time and materials, Transaction or volume-based | reported | quarter | 78 | 2018Q1 | 2026Q2 | 2018Q4, 2019Q4, 2020Q4, 2021Q4, 2022Q4, 2023Q4, 2024Q4, 2025Q4 |
| segment_revenue | service_line: Consulting and technology services, Outsourcing services | reported | annual | 16 | 2018Q4 | 2025Q4 | 21 quarters without a value (sparse series) |
| segment_revenue | service_line: Consulting and technology services, Outsourcing services | reported | quarter | 52 | 2018Q1 | 2026Q2 | 2018Q4, 2019Q4, 2020Q4, 2021Q4, 2022Q4, 2023Q4, 2024Q4, 2025Q4 |
| segment_revenue | vertical: 7 dims | reported | quarter | 204 | 2013Q4 | 2026Q2 | none |
| utilization_excl_trainees | total: total | na | quarter | 63 | 2023Q1 | 2026Q2 | none |
| utilization_offshore | total: total | na | quarter | 175 | 2017Q1 | 2023Q4 | none |
| utilization_onsite | total: total | na | quarter | 175 | 2017Q1 | 2023Q4 | none |

Notes on the gaps:
- **Q4 service-line and contract-type revenue:** only the 10-K annual total is disclosed, and Q4 was not derived.
- **net_additions:** stated only in 2013–2016 highlights ("Net headcount addition for the quarter") and in releases from Q4 2022. Not computed from headcount for other quarters.
- **Utilization:**
  - Onsite and offshore-excl-trainees: 2017Q1–2023Q4.
  - "Blended Utilization, Excluding Trainees": introduced in Q1 2024 with history back to 2023Q1, and replaces the onsite/offshore split.
  - Nothing before 2017Q1.
- **Attrition:**
  - Quarterly-annualized total: 2017Q1–2021Q4.
  - Quarterly-annualized voluntary: 2019Q1–2022Q4.
  - Quarterly-annualized involuntary: 2020Q1–2022Q4.
  - TTM voluntary, company-wide: 2020Q1–2022Q4.
  - TTM voluntary, Tech Services (`dimension=Tech Services`): 2022Q1–2026Q2.
  - Nothing before 2017.
- **Bookings:**
  - TTM levels from 2020Q4. The Q4 2021 deck chart goes back to 12/31/2020.
  - Before that, only YTD growth (H1 2020 +14%, 9M 2020 +15%, 9M 2021 +13%).
- **Constant-currency growth:**
  - In releases from Q4 2018.
  - Total and segment cc growth for 2017Q1–2018Q3 comes only from the history tables in the 2019 and 2020 supplements.
  - Geography cc growth only from Q4 2018.
- **Not disclosed by Cognizant (no rows):**
  - subcontracting cost
  - employee cost (not broken out)
  - fresher hires
  - revenue by client bucket (only top-5/top-10 share, 2014–2016)
  - onsite/offshore effort or revenue mix (only 10-K headcount by location)
- **Top-5/top-10 client share and strategic/active clients:** stop after 2016 (the disclosure was discontinued).

## 3. Definitional breaks

**Segments (verticals):**
- Through Q4 2016: Financial Services / Healthcare / Manufacturing/Retail/Logistics / Other.
- From Q1 2017: "Manufacturing/Retail/Logistics" was renamed "Products and Resources" and "Other" was renamed "Communications, Media and Technology". Release footnotes call both renames ("previously referred to as"). QoQ growth columns were dropped after Q4 2017.
- Q2 2022: "Healthcare" was renamed "Health Sciences". Supplements from Q2 2022 relabel history back to 2020Q1 as Health Sciences, so both names appear for 2020Q1–2022Q1.
- From Q4 2024 the releases list Health Sciences first. This is ordering only.
- I found no statement of a client re-mapping between segments, and no "recast" note, in 2015–2026 releases or 10-Ks. Deck history matches the original release values, so there was no 2020/2021 regrouping with restated segment history.

**Geography:** "Rest of Europe" was renamed "Continental Europe" from Q2 2019. Europe - Total, UK and Rest of World are consistent throughout.

**Revenue recognition:**
- ASC 606 adopted 1 Jan 2018 using the modified retrospective method. Prior periods are not restated, so YoY growth for 2018 compares ASC 606 to ASC 605.
- Contract-type and service-line disaggregation starts 2018Q1 under ASC 606. Earlier service-line data are MD&A percentages.

**M&A and one-offs affecting growth (flagged in release footnotes):**
- 2019–2021: exit of certain content-moderation services (drag on CMT).
- Q4 2020: exit from a large Continental Europe Financial Services engagement (-$107mn revenue).
- Samlink sale, 1 Feb 2022 (Financial Services / Continental Europe drag through Q4 2022).
- Belcan acquired Aug 2024: adds about 400bp to total growth in Q4 2024 to Q2 2025, and 1,500–1,600bp to Products and Resources. The Q3 2024 headcount statement notes it "includ[es] Belcan".
- Thirdera (2024), 3Cloud (Q1 2026) and Astreya (Q2 2026) acquisitions.
- Q1–Q2 2026: third-party product resale ("integrated offerings") adds 140–170bp to growth.

**Headcount:**
- Source changes over time: "approximately N employees" (About Cognizant paragraph, 2013–2016), then the release "Number of employees" table (2017Q1–2020Q3), then the supplement charts (thousands, one decimal, 2019Q3+), then the release "Total headcount" text (Q4 2022+).
- Values agree exactly across sources for every quarter. All are company-wide totals.
- 10-K location split: "Rest of World (other locations)" includes India up to FY2021. From FY2022 India is reported separately and excluded from that bucket. The 10-K labels "North American region" and "European region" (FY2014–2016) were normalized to "North America" and "Europe". Europe was split into UK and Continental Europe from FY2020.

**Attrition (several breaks; do not splice series without care):**
- Through 2021: quarterly-annualized total and voluntary, company-wide.
- 2022: adds TTM voluntary, company-wide.
- Q1 2023: new "Voluntary Attrition - Tech Services" (TTM; excludes the Intuitive Operations and Automation (BPO) practice) replaces the company-wide voluntary and involuntary series. History was shown back to Q1 2022.
- Q1 2026: the Tech Services definition was modified to exclude certain categories of negotiated separations, and prior periods were **recast**. For example, Q1 2025 was 15.8% in 2025 vintages and 12.0% in 2026 vintages. Q1 2026 under the old definition was 14.0%; this is stored as a separate row with a note. Pick vintages by `doc_date`.

**Utilization:** onsite, and offshore excluding trainees, until Q4 2023. "Blended Utilization, Excluding Trainees" from Q1 2024 (history to Q1 2023); it includes other methodology changes and is not comparable with the offshore series.

**Bookings:**
- Q4 2021 definition change: excludes early-renewal overlap and includes unintegrated acquired entities. TTM to 6/30/2021 and earlier cannot be restated. Rows carry notes.
- Bookings are TCV of new contracts, renewals and expansions, and are not updated for later terminations.
- The deck footnote says the definition impact was "$0.2 million" and "$0.3 million". This is recorded as reported and is probably a typo for billion.

## 4. Judgment calls

- **Values hand-entered from slide images (supplements whose charts have no reliable text order):**
  - Employee-metrics charts in the Q3 2019 through Q4 2021 decks: headcount, total and voluntary attrition, onsite and offshore utilization.
  - The Q4 2021 TTM-bookings chart.
  - All such rows carry `hand-entered from slide image` in `notes`, and the values are in `HAND_SERIES` in the extract script.
  - Every hand value was checked against the other chart vintages and against the text-table decks from 2022 onward, where they overlap. All agree.
- **2014 releases (Q4 2013 to Q4 2014) report in USD thousands.** These were converted to USD_mn (divide by 1,000), and the notes say so. This is the only transformation of a reported number.
- **"—%" in growth columns** was recorded as 0.0.
- **Headcount in supplements** is reported in thousands with one decimal. It is stored as a count (x1,000), and the notes say so.
- **Net additions:** the stated change vs the prior quarter end is recorded as `net_additions` (quarter). The stated change vs the year-ago quarter is recorded as `net_additions` with period_type `ltm`. Both are as reported, not computed.
- **AI disclosures** (`ai_disclosure`) are qualitative-to-quantitative statements with bounds, all hand-entered:
  - More than 100 GenAI engagements (Q2 2023).
  - Over 30% of code AI-assisted, and about 260K employees skilled in or trained on gen AI (FY2025).
  - Over 5,000 AI engagements, and nearly 40% of code AI-assisted (Q1 2026; a company sampling estimate).
  - No AI revenue or bookings figure is disclosed.
- **Segment names** are used exactly as each document prints them: release names use "and"; deck names using "&" were mapped to the release spelling.
- **Supplement revenue-growth history for segments** is stored as `dim_type=vertical`. Geography growth history in decks was not parsed; geography comes from releases only.
- **Quarter assignment:** each 8-K is assigned to the quarter ending before its filing date. For each release this was checked against the "Three Months Ended" header.
