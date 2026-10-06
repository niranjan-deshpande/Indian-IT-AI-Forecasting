# Inputs for the research note

*Built 2026-10-05. Every number below comes from a repo file (path given) or from a cited external source. To regenerate everything, run `python3 scripts/final/make_all.py`.*

Conventions used throughout:
- **Growth** is a log change × 100, which is close to a % change.
- **Years** are Indian fiscal years, April–March. "Indian six" means TCS, Infosys, HCLTech, Wipro, Tech Mahindra and the LTI business. The LTI business is counted once: LTI + Mindtree up to FY22, LTIMindtree from FY23.
- **Headcount growth** is the growth of average headcount: the mean of the four quarterly year-on-year changes.

---

## 1. The fact: headcount growth collapsed after FY23

Sources: `output/final/table_A.md` and `table_A.csv`, with summaries in `output/final/note_numbers.csv`. Figure 1: `figures/final/fig1_india_vs_comparators.png` (.svg).

| Indian six | FY16–FY20 mean | FY22 | FY23 | FY24 | FY25 | FY26 | FY27 Q1 (one quarter) |
|---|---|---|---|---|---|---|---|
| Headcount, simple average | +7.4 | +18.5 | +14.3 | **−3.6** | −0.5 | +1.2 | +1.0 |
| Headcount, revenue-weighted | +7.2 | +17.2 | +13.9 | **−2.8** | −0.8 | +0.6 | −0.1 |
| Revenue cc, simple | +8.7 | +16.7 | +12.8 | +0.7 | +2.6 | +1.4 | +3.6 |
| Revenue cc, revenue-weighted | +8.7 | +16.3 | +12.9 | +1.5 | +3.2 | +0.6 | +3.0 |
| Revenue per employee (cc), simple | +2.5 | +0.0 | −0.8 | +4.4 | +3.1 | +0.2 | +2.6 |
| Revenue per employee (cc), revenue-weighted | +2.2 | −0.4 | −0.7 | +4.4 | +4.0 | +0.0 | +3.1 |

- **Breadth of the fall.** Headcount fell in FY24 at 5 of the 6 entities. HCLTech is the exception at +2.1 (`note_numbers.csv`). Year-end headcount (March 2024 vs March 2023) fell 4.7% on the simple average.
- **The comparators slowed too.**
  - Accenture: headcount +1.5 (FY24), +5.7 (FY25), +0.5 (FY26) against a +8.1 FY17–FY20 mean; revenue cc +2.5, +5.4, +5.0.
  - Cognizant: headcount −0.9 (FY24), −2.6 (FY25), +3.9 (FY26) against a +7.1 FY16–FY20 mean; revenue cc −1.0, +4.1, +5.2. Cognizant's FY25–26 revenue includes Belcan; acquisitions are not adjusted.
  - Accenture's year is shifted by one month (its fiscal quarters end Nov/Feb/May/Aug).
- **What FY23 actually shows.** FY23 is the end of the FY22 hiring boom, not a normal year. The collapse is measured against both FY16–FY20 and FY22–23.
- **How many firms are in each average.** The cc revenue average covers 4 firms in FY16–FY20, 5 in FY21–FY23 and 6 from FY24. The LTI group lacks cc revenue before FY24, and Tech Mahindra lacks it before FY21. Firm lists by year are in `table_A.md`.

### 1b. Context: mid-tier firms (kept separate from the main tables)

Source: `data/explore/midtier/midtier_vs_top6.csv`, built from primary filings in `data/explore/midtier/midtier_raw.csv`. The four firms are Persistent, Coforge, Mphasis and Hexaware.

| | FY24 | FY25 | FY26 |
|---|---|---|---|
| Top-six revenue growth (USD, from levels) | +2.0 | +2.7 | +2.2 |
| Mid-tier four revenue growth (USD, from levels) | +5.0 | +14.7 | +13.9 |
| Top-six year-end headcount growth | −4.5 | +1.0 | −0.2 |
| Mid-tier four year-end headcount growth | +0.7 | +10.7 | +5.6 |

- **Share of the combined total (top six plus mid-tier four).** The mid-tier share of revenue rose from 5.1% (FY21) to 7.3% (FY26). Its share of headcount rose from 5.5% to 7.3% over the same years.
- **Acquisitions are included.** Examples: Coforge–Cigniti (FY25), Mphasis–Silverline (FY24), and Hexaware's deals. Excluding Coforge in FY25, the other three still grew revenue +10.9.
- **Hexaware reports calendar years.** Each one is aligned to the Indian fiscal year ending three months later, a 9-month overlap.
- **Headcount definitions differ.** Mphasis and Hexaware include contractors.
- **What it implies.** Demand for Indian-delivered IT services did not fall uniformly. Some work went to smaller Indian vendors. This bears on S1 (demand) versus a vendor-share shift (an S4-like reallocation among vendors). It is not GCC evidence.

## 2. The identity: what the residual says

Source: `output/final/table_B.md` and `table_B.csv`.

The residual is revenue-per-employee growth (cc) minus utilization change. It equals g_p − g_a, and can be computed only for firms that report utilization.

| window | firm set | mean residual | mean utilization change | firm-years | firms |
|---|---|---|---|---|---|
| FY16–FY23 | all with data | +1.1 | +0.8 (33 firm-years) | 18 | HCLTech, Infosys, Tech Mahindra, Wipro |
| FY16–FY23 excl. FY21 | all with data | +2.1 | +0.5 (29) | 15 | same |
| FY24–FY26 | all with data | +1.3 | +1.0 | 12 | Infosys, LTI group, Tech Mahindra, Wipro |
| FY16–FY23 | same firms in both windows | +0.5 | +0.3 | 14 | Infosys, Tech Mahindra, Wipro |
| FY16–FY23 excl. FY21 | same firms | +1.7 | −0.4 | 11 | same |
| FY24–FY26 | same firms | +0.9 | +0.7 | 9 | same |

- **Change in the residual.** After FY23 it moves by between −0.8 and +0.4 pp, depending on the firm set and on whether COVID-hit FY21 is included. S2 predicts a rise equal to the labor-saving effect, e.g. the pilot's prior of about 4 pp a year. No specification shows a rise of more than 0.4 pp.
- **Which firms are not covered.** TCS stopped reporting utilization after Q3FY16 and HCLTech after Q4FY19, so neither is in FY24–26. Wipro is also excluded in FY18–FY20 under decision 3.

## 3. Subcontracting

Sources: Figure 2 `figures/final/fig2_subcontracting_share.png` (.svg); data in `output/final/fig2_data.csv`, from `audit/subcontracting_series.csv`.

Subcontracting cost as a % of revenue, firm-reported, same currency:

| firm | FY23 | FY24 | change | FY26 |
|---|---|---|---|---|
| TCS | 9.5 | 6.6 | −2.9 | 5.5 |
| Infosys | 9.6 | 8.0 | −1.6 | 8.6 |
| HCLTech | 14.7 | 13.3 | −1.5 | 14.2 |
| Wipro | 12.7 | 11.5 | −1.3 | 11.6 |
| Tech Mahindra | 15.0 | 12.9 | −2.2 | 10.7 |
| LTIMindtree | 8.5 | 7.2 | −1.3 | 7.7 |

- **Direction.** The share fell at all 6 firms from FY23 to FY24. In FY26 all 6 remain below their FY23 level, but 5 of 6 rose from FY25 to FY26; Tech Mahindra is the exception.
- **Definitions.**
  - TCS's line is "fees to external consultants" (cost of revenue + SG&A), with a definition break at Q1FY27 (not shown).
  - LTIMindtree's comes from annual reports, from FY22 only.

## 4. S1 vs S4: did the work go to clients' own centres (GCCs)?

Detail and citations: `discriminating_data.md` §(a), rows 1i, 11b and 2a. All three are labelled *measured*.

- **RBI Census on Foreign Liabilities and Assets, Table 9C.**
  - Information-and-communication exports by 22,395 foreign subsidiaries in India: ₹6,53,856 cr (2021-22) and ₹8,45,021 cr (2022-23).
  - Coverage includes foreign-owned vendors as well as captives, and includes telecom and publishing.
  - Source: RBI press release, 12 Sep 2023, https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=56359
- **BEA, employment of US multinationals' majority-owned foreign affiliates (AMNE/MOFA).**
  - India, professional, scientific and technical services, thousands: 598.4 (2019), 877.0 (2022), 893.2 (2023, preliminary).
  - Coverage includes US-headquartered vendors.
  - Source: BEA `mofas-employment.xls`, released 22 Aug 2025; 2024 data due Nov 2026.
- **Naukri JobSpeak, Sep 2026.**
  - Year-on-year hiring index: IT/Software Services −4%, GCC +4% (p.4 tiles).
  - IT-software index 3,432 (Sep 2026) vs 3,585 (Sep 2025).
  - These are job postings, not hires. The GCC series is shown only as a year-on-year change.
  - Source: Info Edge, `Naukri-Jobspeak-September-2026.pdf`, infoedge.in/InvestorRelations/NaukriJobSpeak

## 5. Earnings calls

**Material.** 2,087 verbatim management statements from 183 transcripts, Jan 2021–Oct 2026, eight firms (`audit/calls_statements.csv`). Codebook, extraction methods and reliability: `calls_codebook.md`.

**Agreement between the two coders.**
- Primary category: **92.1%**, κ = 0.87 (`output/final/calls_agreement.csv`).
- By category (share of coder 1's codes matched by coder 2):

| A | B | C | D | E |
|---|---|---|---|---|
| 91.0% | 87.2% | 76.4% | 70.1% | 96.8% |

- 164 disagreements are listed in `calls_disagreements.csv`, unresolved. A 30-statement spot-check sample is in `calls_spotcheck.csv`.

**Figure 3.** `figures/final/fig3_call_categories.png` (coder 1). The coder-2 version is `fig3_call_categories_coder2.png`; data in `output/final/fig3_data.csv`.

Statements per transcript (coder 1):

| category | 2021–22 | 2023 | 2024H2–2026H1 | 2026H2 |
|---|---|---|---|---|
| A, demand weakness | 0.4–1.4 (3.0 in 2022H2) | 7.5–7.9 | 4.7–5.7 | 5.9 |
| D, AI productivity passed to clients | 0–0.1 | 0.3 | 0.6–1.6 | 3.0 (8 transcripts) |

- Coder 2's codes give the same pattern.
- **Caveat on levels.** A comes mainly from a broader extraction pass than D: about 9 vs 2 statements per call. Compare trends within a category, not levels across categories.

**Quotes.** Six, all re-verified verbatim: `note_quotes.md`.
- Two are A (TCS and Infosys, Oct 2023).
- One is B (TCS, Jan 2024).
- Three are D (TCS, Apr 2025; HCLTech ×2, Apr 2026).

## 6. Price data

**What was searched and found.** Searched:
- official producer and services price indices: US BLS/BEA, UK ONS, Eurostat, Bank of Japan, India's WPI and new Services PPI, India's national-accounts deflators;
- the firms' own disclosures, 2003–2026;
- sourcing advisors: ISG, Everest, Gartner, HfS;
- broker research;
- 183 earnings calls.

What was found:
- **No public source measures output prices for Indian IT services in any period.**
- Official indices cover domestic producers and mostly price hourly or person-month rates, which measure price per unit of labor (p/a), not per unit of work.
- India has no IT services price index.
- Firm disclosures measure p/a and stopped by FY2020.
- Analysts' 2025–28 "deflation" estimates assume pass-through rather than measure it.
- The only measured output price found is ISG's contracted resource-unit prices in managed-services deals. It covers all vendors and a narrow, mostly infrastructure, slice.

Details: `price_data.md`.

**Infosys person-month bound.**
- Infosys's 20-F reported revenue per billed person-month (p/a) every year FY2003–FY2020. Growth, USD reported: FY15 −2.8%, FY16 −4.7%, FY17 −2.7%, FY18 +1.5%, FY19 −0.8%, FY20 −1.5% (`price_data.md` §A3; values in `audit/price_firm_disclosures.csv`).
- Adjusted to constant currency, this is about −1% to −2% a year in FY15–FY17 and about 0% in FY18–FY20. The adjustment is our own calculation, labelled derived (`price_data.md` §b).
- Since g_p = g_{p/a} + g_a, this is an *upper* bound on Infosys's g_p **only if labor per unit (a) did not rise**. That is an assumption, not an observation.
- It is a single firm, not the sector, and it ends in FY20.

**BLS check (Task 3; `price_data.md` §A2b).**
- **NAICS 5415 / 541511 / 541512:** BLS publishes no producer price index for these. The BLS API returns "Series does not exist" for PCU5415--5415--, PCU541511541511 and PCU541512541512. BLS lists 541511–541519 as non-covered industries (https://www.bls.gov/ppi/fd-id/areas-of-noncoverage-in-the-ppi-system.htm, last modified March 4, 2026).
- **NAICS 518210, data processing and hosting (PCU518210518210):** introduced January 2002 with history from December 2000. It is priced by repricing actual contracts with fixed characteristics (BLS fact sheet, last modified Nov 7, 2008).
  - Annual-average growth: 2015 +0.3, 2016 +1.2, 2017 +1.5, 2018 +0.3, 2019 +0.5, 2020 +2.9, 2021 +1.0, 2022 +1.0, 2023 +1.5, 2024 +1.3, 2025 +3.3; 2026 Jan–Aug +0.5 year-on-year.
  - Files: `data/explore/prices/final_bls/`.
  - This is a US domestic producer price: a proxy for offshore Indian vendors' prices, not a measure of them.

## 7. What would settle it

From `discriminating_data.md` §(c), condensed.

| data item | who could collect it | pair it separates | exists publicly? |
|---|---|---|---|
| Price per unit of output in managed-service and fixed-price contracts; renewal value vs prior value for the same scope | Vendors, client procurement teams, sourcing advisors (ISG, Everest, Avasant) | **S1 vs S3** | No. Held in contracts and paid advisory benchmarks |
| Revenue and headcount by service line, split by AI exposure (testing, application maintenance, infrastructure, BPO vs consulting/engineering) | The six firms (disclosure choice) | S1 vs S3 | Discontinued: TCS after FY17, Infosys after FY18, Wipro after FY23 |
| Headcount by role or job level | The firms. Paid proxy: Revelio Labs / LinkedIn | S1 vs S3 | Infosys job bands only; otherwise paid |
| GCC headcount by parent company and function, measured | MCA filings compiled per entity (₹100 per company inspection); Nasscom | **S1 vs S4** | No. Industry estimates only, with no parent detail |
| Affiliated vs unaffiliated computer-services imports from India | BEA (BE-125 survey) | S1 vs S4 | Collected, not published by country |
| RBI software-exports survey: employees and billing to subsidiaries abroad | RBI | S1 vs S4 | Collected, not published |
| Subcontractor headcount (FTEs) | The firms | S2 vs S4 (subcontractor version) | No. Cost lines only |
| Utilization for all six firms on a consistent definition | The firms | S1 vs S2 (the utilization term) | Discontinued at TCS (FY16) and HCLTech (FY19) |

## 8. Limitations

1. The S2 test rests on 4 of 6 firms. TCS and HCLTech, the two largest, report no utilization in FY24–26.
2. TCS's revenue per employee rose faster in FY24–25 (+4.2, +3.9 vs +1.7 in FY16–20), but without utilization data it cannot be decomposed (`output/final/table_A_firms.csv`).
3. Infosys's residual jumped to +6.6 in FY24. Its utilization excludes trainees but its headcount includes them, so the collapse in fresher intake can raise the residual mechanically.
4. Before FY24, constant-currency revenue covers only 4–5 of the six entities. The averages change composition over time.
5. The HCLTech divestiture is not adjusted (decision 2). HCLTech's FY25 headcount growth is −1.6% unadjusted against +1.7% adjusted (`data/corrected/CHANGELOG.csv`), which moves the six-firm simple average by about 0.6 pp.
6. Acquisitions are not adjusted: Cognizant–Belcan, Wipro–Capco, Accenture's programme, HCLTech–IBM products.
7. Accenture's fiscal year is offset from the Indian year by one month. Its Q4FY26 (added in this pass) falls outside Table A.
8. Accenture Q4FY26 headcount is a rounded "approximately 814,000". Its utilization and attrition were not available on 2026-10-05.
9. Wipro growth observations spanning the ISRE perimeter change (FY18) and the Alight transfer (FY19–FY20) are excluded, so Wipro is missing from several FY18–FY20 averages.
10. Fiscal-year cc growth aggregates quarterly firm-reported cc growth using prior-year revenue weights. Accenture's cc is printed in whole percents (±0.5 pp).
11. Headcount excludes contractors at TCS, Infosys, HCLTech and LTIMindtree but includes direct contractors at Tech Mahindra. Trainee treatment is stated only by Infosys.
12. Subcontracting share is a cost ratio: it mixes contractor rates with volume. Contractor FTEs are not reported.
13. The S4 evidence (RBI FLA, BEA affiliates, Naukri) includes foreign-owned vendors, is annual or postings-based, and lags 1–3 years.
14. Call statements are management commentary (cheap talk), selected through keyword screens. The two passes differ in intensity, coder agreement on D is 70–79%, and 164 disagreements are unresolved.
15. The pilot's S1-vs-S3 argument relies on the full pass-through assumption, under which revenue, headcount and utilization can't separate the two.
16. The demand re-scan used 32 parallel readers. Their per-call yields may differ somewhat.
