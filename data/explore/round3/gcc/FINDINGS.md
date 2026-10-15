# FINDINGS — GCCs in India: size, and did they absorb the top six's slowdown?

*Saved by the orchestrator from the subagent's report; subagents cannot write report files. Probed 2026-10-14. Builds on `data/explore/trade/FINDINGS.md` and `discriminating_data.md` §(a), rows 1a–1k and 4a, without repeating them.*

## 1. Headline

- **No official statistic measures GCC employment.** Every GCC headcount figure comes from Nasscom–Zinnov estimates, including those quoted by ministers in Parliament and in the Economic Survey.
  - Nasscom–Zinnov restated the series in September 2024, so its editions cannot be chained.
  - On the restated basis: **1.90m (FY24) → 2.36m (FY26), about +460k.**
  - Staffing-firm estimates of net hiring for FY24–26 are about 60k, 110–140k and 200k: **about +370–400k** in total.
- **Top-six headcount shortfall at FY26** (year-end basis; the average basis is almost identical, see §4):

  | benchmark | shortfall |
  |--|--|
  | flat at the FY23 level | 61k |
  | 7%/yr from FY23 | 439k |
  | actual FY16–20 trend (6.0%/yr) from FY23 | 384k |
  | 7%/yr from FY20 (skipping the FY22 boom) | 187k |

  - **The estimated GCC additions (about 0.4–0.46m) are as large as even the steepest shortfall.**
  - Read this as the same order of magnitude only. The GCC figures are estimates and include non-IT functions: finance, HR, analytics and engineering R&D.
- **Best official proxy: RBI's census of foreign-owned companies (FLA census), Table 9C.** It reports exports by foreign subsidiaries in "Information and communication" (I&C). It has no employment data.
  - Within-round USD growth was about 9.6% in FY24 and 9.2% in FY25.
  - That beats total software exports (+2.8%, +7.3%) and public-limited exporters (−1%, +1%).
  - It does not beat the subsidiaries' own pre-COVID growth (FY20 12.6%, FY21 5.9%).
  - The level is about **$137bn in FY25, roughly two-thirds of India's software exports.** It includes foreign-owned vendors such as Accenture, Cognizant, Capgemini and IBM.
- **GCCs hire few freshers.**
  - Entry-level staff are about 20–22% of the GCC workforce (TeamLease).
  - GCCs' share of all fresher hiring rose only from 8% to 11% (foundit, July 2026).
  - Flows of workers from IT services to GCCs appear only as unsourced staffing-firm claims (Xpheno: "nearly half" of displaced IT-services staff found GCC roles).
- **Surprise: Nasscom's own numbers conflict.**
  - The GCC gain over FY25–26 (+460k) is larger than Nasscom's net additions for the *whole* tech industry over the same years: +133k and +135k, about +268k (press figures).
  - One explanation is that non-GCC tech employment fell by about 190k. That fits poorly with a flat top six (+12k over FY24–26) and a growing mid-tier.
  - More likely, the GCC count includes non-tech functions and newly tracked centres, which would overstate the IT jobs that were reallocated.

## 2. Sources

| name | publisher | measures | unit / disaggregation | period, frequency | lag | access | confirmed? | URL |
|--|--|--|--|--|--|--|--|--|
| Top-six headcount | firm filings (repo) | headcount | persons, by firm | FY16–26, quarterly | ~1 month | repo | **CONFIRMED**, computed | `data/corrected/core_quarterly_final.csv` |
| FLA census, Tables 9A/9C | RBI (official) | foreign subsidiaries' sales and exports by activity | ₹ crore by activity; I&C includes telecom and publishing; no employment, no parent country | FY19–25 (6 rounds of 2 years), annual | ~7 months; FY26 round expected Oct 2026 | free HTML | **CONFIRMED**, all 6 releases parsed | rbi.org.in BS_PressReleaseDisplay.aspx?prid= 51367, 52719, 54408, 56359, 58874, 61524 |
| India GCC Landscape | Nasscom–Zinnov (industry body / consultancy) | GCC count, units, headcount, revenue | by city, industry and function (full report) | FY23, FY24 (restated), FY26; about every 2 years | — | 2026 edition behind a business-email form; older editions ₹20k | FY26 **CONFIRMED** (landing page); FY23/24 secondary | https://media.zinnov.com/wp-content/uploads/2026/05/zinnov-nasscom-india-gcc-landscape-2026-report.pdf |
| Parliament replies | MeitY (Jul 2024, Aug 2025), Labour (Mar 2025); reprint Nasscom figures | GCC count, headcount, revenue | — | FY23, FY24 | — | free | secondary; PDFs not opened | https://dge.gov.in/dge/sites/default/files/2025-05/3757_e.pdf ; https://ianslive.in/over-1700-gccs-are-in-operation-in-india-minister--20250806142159 |
| JobSpeak GCC index | Info Edge / Naukri (job portal) | postings index | monthly | levels Aug 2023–Oct 2024 (text layer); GCC first appears in the Jul-2024 report; 2025+ reports give YoY only, as images | ~1 week | free PDF | **CONFIRMED** | https://www.infoedge.in/pdfs/News_Events_pdfs/Naukri-Jobspeak-October-2024.pdf |
| Outward FATS (`fats_out2_r2`, `fats_out_activ`) | Eurostat (official) | persons employed in EU-controlled affiliates in India | NACE J and J62_J63; many cells confidential | 2013–2023, annual | ~27 months | free API | **CONFIRMED**, pulled | URLs in CSV |
| US multinationals' foreign affiliates (MOFA) | BEA (official) | employment by industry | — | 2009–2023; 2024 due Nov 2026 | ~2 years | free | prior work (`note_inputs.md`) | — |
| Software exports survey | RBI | exports by organisation type | no foreign-owned category; employee counts collected but not published | FY09–26 | ~6 months | free | prior work | — |
| GCC hiring estimates | UnearthInsight, Xpheno, TeamLease Digital (consultancies / staffing firms) | GCC hiring, persons per year | gross vs net often unclear | FY24–26 | — | press only | secondary | in CSV |
| GCC office leasing | Colliers, Vestian, CBRE, JLL, ANAROCK (real-estate consultancies) | million sq ft leased, by city | — | 2021–H1 2026, half-yearly | ~1 month | free press releases | secondary | in CSV |
| State figures | Karnataka policy, Telangana minister, FICCI-ANAROCK | GCC counts and jobs | — | ad hoc | — | free | secondary | in CSV |
| Parent-company disclosures | JPMorgan, Goldman, Walmart, Target, Lowe's | India headcount | — | — | — | — | press only (JPMorgan ~55k; Goldman 5k+, undated); no India split found in 10-K or ESG reports | in CSV |
| Company master data and filings | MCA (official) | foreign-subsidiary flag, industry code; per-entity filings (employee counts from FY25) | per entity | — | — | data.gov.in returned 503; filings ₹100 per company | not confirmed | data.gov.in/catalog/company-master-data |
| Job postings tracker | Indeed Hiring Lab | postings index | — | — | — | — | **CONFIRMED absent**: no India folder in the public repo | github.com/hiring-lab/job_postings_tracker |
| Economic Graph | LinkedIn | flows from IT services to GCCs | — | — | — | — | nothing public found | — |

## 3. What each source can tell us

**RBI census of foreign-owned companies (official; the best source)**
- Bears on S4a (work moving to GCCs) against S1, S3 and S4d.
- Supports S4a if foreign subsidiaries' exports grow while the vendors stall, which is what FY24–25 shows.
- Undermines S4a if their exports stall too, as they would under S1 or S4d. Under S3, cost-plus captive exports would also slow.
- Caveats:
  - no employment data;
  - includes foreign-owned vendors;
  - I&C includes telecom;
  - the respondent set grew from 18.5k to 26.3k, so only within-round growth is used;
  - USD figures use exchange rates implied by Infosys's figures, so they are approximate;
  - the tables are labelled "at market value", a carry-over label since exports are flows.

**Nasscom–Zinnov (consultancy estimate)**
- Bears on the size of the move to GCCs (S4a).
- Supports S4a if GCC gains are on the scale of the vendor shortfall, which they are. Undermines it if gains are much smaller.
- Caveats:
  - method is "200+ interviews, 1M+ job postings" plus Zinnov's own database;
  - the restatement breaks the series;
  - includes non-tech functions;
  - conflicts with Nasscom's own industry totals.
- Treat it as an upper bound.

**JobSpeak (job portal)**
- Bears on the timing of S4a, using postings rather than hires.
- GCC postings were up 17% y/y in October 2024, 18% in October–November 2025, and 4% in September 2026 (when IT-services postings fell 4%).
- Caveats:
  - no pre-2023 baseline, so it cannot show acceleration;
  - in September 2023 Naukri reclassified "sub-industries intersecting with BFSI, Tech, and GCC".

**Eurostat (official)**
- Employment in EU-owned I&C affiliates in India: 243k (2018), 270k (2020), 304k (2021), 330k (2022, estimated), 327k (2023).
- Likely dominated by vendors such as Capgemini. Context only, not a GCC measure.

**Office leasing**
- GCC leasing rose from about 15 million sq ft (2021) to 28–35 million (2025).
- GCCs' share of all leasing was 40–45% in 2025, after dipping below about 35% in 2022.
- Gross leasing only, and definitions and city sets differ across firms.

**Hiring composition (TeamLease, foundit, Xpheno)**
- Bears on the entry-level ladder: even if work moves to GCCs, they absorb few entry-level hires.
- No published methodology.

## 4. Numbers pulled

**Headcount definition.** The shortfall figures in §1 sum **year-end (March) headcount across the six firms**; LTIMindtree before FY22 is LTI plus Mindtree. The note uses the average of the four quarterly year-on-year changes, which approximates growth of average headcount and gives its +14% for FY23.

| FY | year-end (March) headcount | YoY | average of 4 quarter-ends | YoY |
|--|--|--|--|--|
| FY20 | 1,202,808 | 6.3% | 1,193,322 | 8.6% |
| FY21 | 1,295,816 | 7.7% | 1,236,230 | 3.6% |
| FY22 | 1,588,982 | 22.6% | 1,467,193 | 18.7% |
| FY23 | 1,679,489 | 5.7% | 1,679,750 | **14.5%** |
| FY24 | 1,605,986 | −4.4% | 1,629,665 | −3.0% |
| FY25 | 1,621,361 | 1.0% | 1,617,199 | −0.8% |
| FY26 | 1,618,023 | −0.2% | 1,623,859 | 0.4% |

Year-end series also: FY16 951,741; FY19 1,131,253.

**FY26 shortfall on the two bases**

| benchmark | year-end | average |
|--|--|--|
| flat at FY23 | 61k | 56k |
| 7%/yr from FY23 | 439k | 434k |
| pre-COVID trend from FY23 | 384k (6.0%, FY16–20) | 386k (6.16%, FY17–20) |
| 7%/yr from FY20 | 187k | 167k |

- The year-end series is saved in `top6_headcount_fy.csv` (built by `top6_headcount.py`, with source URLs per firm).
- The average-basis figures were computed inline by the subagent and are not saved.

**RBI census of foreign-owned companies: I&C exports by foreign subsidiaries** (`rbi_fla_foreign_subs_ic.csv`, `build_fla_csv.py`)

| FY | ₹ crore | ≈ USD bn | within-round growth, INR | within-round growth, ≈ USD | subsidiaries | release |
|--|--|--|--|--|--|--|
| FY20 | 5,00,461 | 70.4 | 14.1% | 12.6% | 18,468 | prid 51367 |
| FY21 | 5,52,554 | 74.6 | 10.4% | 5.9% | 20,023 | prid 52719 |
| FY22 | 6,44,837 | 86.5 | 27.4% | 26.5% | 20,505 | prid 54408 |
| FY23 | 8,45,021 | 104.9 | 29.2% | 19.6% | 22,395 | prid 56359 |
| FY24 | 10,14,742 | 122.6 | 12.6% | 9.6% | 25,249 | prid 58874 |
| FY25 | 11,59,637 | 137.2 | 11.5% | 9.2% | 26,269 | prid 61524 |

Release URL pattern: https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=NNNNN

**Other extracts**
- `jobspeak_gcc_index.csv`: monthly GCC index, Aug 2023–Oct 2024, roughly 860–1,140.
- `eurostat_fats_india.csv`
- `gcc_estimates_secondary.csv`: Nasscom–Zinnov editions, hiring estimates, leasing, state and parent figures. Each row has a URL and a confirmed-or-secondary flag.

## 5. Could not check
- Full Nasscom–Zinnov 2026 report (form-gated), so there is no FY21–26 series from a single edition.
- Nasscom Strategic Review PDF (HTTP 406); FY25–26 industry totals come from the press.
- The Parliament reply PDFs (not opened).
- RBI census round for 2025-26 and BEA's 2024 data (not yet released).
- data.gov.in (503); MCA per-entity filings are paid.
- Parent companies' 10-K and ESG reports (not opened). Large US filers rarely split headcount by country; MCA filings for their Indian entities are the practical route.
- Any public primary data from LinkedIn, Xpheno or UnearthInsight on worker flows.
- JobSpeak GCC figures for 2025–26 (images, not transcribed).
- The yearly Colliers series is built from half-year figures in the press.
