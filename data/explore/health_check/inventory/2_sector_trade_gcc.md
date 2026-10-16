# Inventory: sector aggregates, trade, GCCs, listed panel and offshore competitors

All paths below are relative to `/Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/0. Exploratory Analysis/data/explore/`. I did not edit anything.

## 1. Datasets

**Sector aggregates (`round3/sector_aggregates/`)**
- `exports_recomputed.csv` (columns: series, fy, level, yoy_pct, source_url).
  - RBI software-exports survey, FY23–FY26: total, private-limited and public-limited exporters, in USD bn.
  - BoP (RBI data via the IMF API), FY19–FY26, each year the sum of four quarters: computer services, total services, other business services.
- `sector_series_pulled.csv` (series, publisher, fiscal_year, value, unit, vintage, confirmed, notes).
  - RBI survey splits: excluding vs including Mode 3; computer vs ITeS; survey response counts.
  - Nasscom revenue and employment by Strategic Review edition (press figures only).
  - Nasscom–Zinnov GCC headcount and revenue.
  - MeitY exports from software technology park (STP) units.
  - RBI's growth figures for listed IT companies.
  - MoSPI national accounts (gross value added), where IT cannot be separated out.
- `sector_vs_top6_fy23_fy26.csv`: FY23 vs FY26 cumulative and annualised growth for 11 series.

**Trade (`trade/`)**
- `rbi_survey_orgtype.csv`: RBI survey shares by organisation type (private-limited, public-limited, others), the US share, and USD totals. FY12–FY26, with FY18 missing. The method changes several times.
- `affiliated_share_annual.csv`, 2006–2025:
  - BEA ITA US imports from India (all services; computer services);
  - BEA MOFA data on US-owned affiliates in India: services to US parents, services to unaffiliated US buyers, employment. These end in 2023;
  - the affiliated share of all US computer-services imports;
  - India's share of US computer-services imports.
- `bea_ita13_india_quarterly.csv`: BEA Table 1.3, US imports from India, 2003Q1–2026Q2. It has telecom, computer and information services (TCI) and other business services, but no computer-only line.
- `bea_is23_annual.csv`: BEA Table 2.3, 1999–2025.
- `bea_mne_mofa_*`: MOFA services by destination and employment in India, 2009–2023.
- `imf_bop_india_services_quarterly.csv`: India's credits and debits for total services, transport/travel/other (S, SI, SI2, SJ), 2004Q1–2026Q2.
- `noise_stats.csv`, `compare_firm_vs_trade_annual.csv`: noise statistics and correlations with firm revenue.

**GCCs (`round3/gcc/`, `round3/gcc_reconcile/`, `round4/robustness/demand/gcc_*`)**
- `rbi_fla_foreign_subs_ic.csv`: RBI census of foreign-owned firms (FLA, Table 9C). Exports by foreign subsidiaries in "information and communication" (I&C), in ₹ crore with approximate USD. Six rounds covering FY19–FY25, each giving two years. Has within-round growth and the subsidiary count. The FY26 round is not out.
- `top6_headcount_fy.csv`: year-end headcount by firm, FY16–FY26, with three counterfactual trend columns.
- `gcc_estimates_secondary.csv`: 26 rows of mostly secondary figures. Nasscom–Zinnov editions, staffing-firm net hiring, office leasing from Colliers and Vestian, fresher shares, state-government claims.
- `jobspeak_gcc_index.csv`: Naukri GCC job-postings index, monthly, Aug 2023–Oct 2024 only.
- `eurostat_fats_india.csv`: people employed in India by EU-controlled affiliates, 2013–2023, with many cells confidential.
- `gcc_reconcile/reconcile_inputs.csv`, `gcc_scenarios.csv`: GCC change scenarios for FY23–26 and FY24–26 (columns gcc_change_all_functions_k_low/central/high and gcc_tech_change_k_share0.55/0.67/0.80).
- Round 4 files:
  - `gcc_baseline_inputs.csv`: Zinnov levels FY19–FY26;
  - `gcc_baseline_scenarios.csv`: GCC hiring before vs after 2023, as additions per year and as a share of the vendor base;
  - `gcc_rbi_relative_growth.csv`: foreign subsidiaries' growth minus total software-export growth, FY22–25.

**Listed panel (`round3/listed_panel/`)**
- 21 listed firms, FY23–FY26, from primary filings.
  - `listed_panel_firms.csv` (wide): hc_FY23..26, rev_inr_cr_*, rev_usd_mn_*, change and CAGR columns, hc_fell flags.
  - `listed_panel_summary.csv`: by set (all 21, excluding the mid-tier four, the mid-tier four, ER&D 5, IT services excluding the four (7), ITeS/BPM 5, the 12 IT + ER&D firms excluding the four, and the top six). Gives FY23–FY26 levels, aggregate %, median, revenue-weighted mean and number of firms falling.
  - `listed_panel_long.csv`: 367 rows, each with URL and page. `universe.csv` records inclusion and exclusion. `parts/*.csv` are the raw extraction parts.
  - `raw/` holds about 402 MB of PDFs.
  - Minor label issue: `listed_panel_firms.csv` names Cyient "group, incl. DLM", but the notes and FINDINGS say the services segment (DET) is used.

**Offshore competitors (`round3/offshore_competitors/`)**
- `imf_computer_exports_by_country.csv`: computer-services exports, 32 delivery countries, 2012–2025.
- `imf_h1_india_vs_delivery_group.csv`: India vs 24 other countries, H1 2019–2026.
- `india_share_summary.csv` (long: source, metric, year, value), 2014–2025:
  - India's share of world exports on three balanced panels, with and without Ireland;
  - India's share of a group of 30 emerging delivery countries;
  - India's share of US computer imports, and of computer plus other-business imports;
  - the unaffiliated share of US computer imports;
  - US imports from 15 low-cost locations.
- `bea_us_computer_imports_by_country.csv`: about 23 areas, 2010–2025, for computer and other business services. Many cells are suppressed, including the Philippines for computer services.
- `eurostat_eu27_computer_imports_by_partner.csv`, `eurostat_india_share.csv`: 2010–2024.
- `bls_ces_monthly.csv`: US employment in NAICS 5415 (computer systems design) and NAICS 54 (professional and technical services), seasonally adjusted, Jan 2015–Sep 2026.
- `cognizant_headcount_by_location.csv`: from 10-Ks, 2021–2025.
- `raw/`: 11 MB, including the 10-K text.

**Red team (`round3/red_team/`)**
- `rbi_exports_by_activity_type.csv`, FY24–26, in INR and USD: IT services, software products, BPO, engineering, private and public limited, Mode 4, Mode 3.
- `broader_listed_it_growth_fy26.csv`: FY25 and FY26 growth for 14 firms.
- `listed_headcount_absorption.csv`: top six plus the mid-tier four, FY23–26.
- `labour_market_signals.csv`: 23 mostly press-sourced indicators.
- `rbi_fla_foreign_subsidiary_exports.csv`: its FY23 ₹8.5 lakh crore row is a cross-round approximation. Do not use it.

## 2. Headline facts

**Exports, RBI survey (USD, excluding Mode 3)**
- Levels: FY23 $185.5bn, FY24 $190.7bn (+2.8%), FY25 $204.7bn (+7.3%), FY26 $221.4bn (+8.2%). That is +19.4% over FY23–26, or 6.1% a year.
- In INR: FY25 +9.7%, FY26 +13.0%.
- Including Mode 3 (Indian firms' affiliates abroad), FY26 is $239.3bn.
- Mix in FY26: computer services $153.4bn, of which IT services $147.0bn and software products $6.4bn. ITeS $68.0bn, of which BPO $56.0bn and engineering $12.0bn.
- The source of growth flips between years:
  - FY25: IT services +4.6%, BPO +11.4%.
  - FY26: IT services +12%, BPO +0.4%.
- Delivery modes: Mode 3 rose from $13.9bn to $17.9bn. Mode 4 (on-site) fell from $19.1bn to $18.4bn.
- The US takes 54.1% of exports. Weights for FY24–26 from round 4: North America 55%, Europe 31.8% (UK 15%).

**Exports, BoP computer services (excludes ITeS)**
- FY23 $146.8bn → FY26 $203.7bn, +38.8%. Growth was 9.2%, 12.7% and 12.8% in FY24–26.
- Latest quarter: 2026Q2 $51.4bn, +8.6% y/y, down from 12–14% in the preceding quarters.
- Calendar 2025, IMF annual: $197.3bn.
- BoP other business services: $124.2bn in FY26 (+15.8%).

**Sector size (Nasscom, press figures only)**
- FY26 revenue $315bn (+6.1%), of which exports $246bn (+5.6%) and core IT services $149bn.
- FY25 revenue was revised from $282.6bn to $297bn.
- Employment 5.95m in FY26 (+135k, +2.3%), 5.815m in FY25.
- FY23→FY26 chained within each edition: revenue +16.6%, employment +6.1% (about 2% a year).

**Top six's share of exports**
- I computed this; no file in the repo does.
- Top-six global USD revenue divided by RBI survey exports: $80.7bn / $185.5bn = 43.5% in FY23, and $86.5bn / $221.4bn = 39.1% in FY26.
- This is only indicative: the top six's revenue includes on-site, domestic and overseas-subsidiary revenue.
- The cleaner official proxy is the public-limited exporters' share in `rbi_survey_orgtype.csv`:
  - 64.6% (FY13), 46.6% (FY20), 41.5% (FY23), 36.9% (FY26).
  - The private-limited share rose from 35.3% to 60.8% over the same years.
- The shift continued after 2023 but did not speed up: +3.0 pp a year over FY14–22, +1.6 pp a year over FY23–26, with a probable method break at FY22→23.
- Public-limited exports: $77.0bn (FY23) → $81.7bn (FY26), +6%. Private-limited: $104.1bn → $134.6bn, +29%.
- Top six themselves, FY23→FY26: USD revenue +7.2%, headcount 1,679,489 → 1,618,023 (−3.7%).

**GCCs**
- No official headcount exists. Nasscom–Zinnov levels:

  | year | headcount | basis | GCC count |
  |--|--|--|--|
  | FY19 | ~1.0m | old | — |
  | FY21 | 1.38m | old | — |
  | FY23 | 1.66m | old | 1,580 |
  | FY24 | 1.90m | restated Sep 2024 | 1,700+ |
  | FY26 | 2.36m | 2026 edition, coverage probably wider | 2,117 |

- GCC revenue: $64.6bn (FY24) and $98.4bn (FY26).
- The reconciled change over FY23–26 (`gcc_scenarios.csv`):
  - all functions: central about +385k, range +240k to +570k;
  - tech roles: central about +260k, range +155k to +430k.
- The +460k figure for FY24–26 (2026 edition) is judged overstated. It mixes editions and adds newly counted GCCs.
- Staffing-firm estimates of net hiring: about 60k (FY24), 110–140k (FY25) and 200k (FY26).
- Best official proxy, the RBI census, foreign subsidiaries' I&C exports:
  - within-round growth in INR: 12.6% (FY24) and 11.5% (FY25);
  - in USD: 9.6% and 9.2%;
  - level about $137bn in FY25.
  - This proxy includes foreign vendors such as Accenture, Cognizant and Capgemini, and includes telecom.
- BEA MOFA (US-owned affiliates in India):
  - employment 1.79m in 2023, but only +1.6% that year, against +12.6% in 2022;
  - services sold to US parents: 72% of US services imports from India in 2023, up from 24% in 2009.
- Eurostat: EU-owned affiliates in India in computer services (J62–63) employed about 270k (2021), 300k (2022) and 291k (2023).
- Office leasing: GCCs took 38% of 2025 leasing and 41.7% of H1 2026 leasing.

**Other listed firms, FY23→FY26 (headcount is global)**

| set | headcount | excl. known acquired staff | USD revenue |
|--|--|--|--|
| all 21 | 337k → 400k (+18.6%) | +13.9% | +32.8% |
| mid-tier four | +18.0% | +14.1% | +39.4% |
| ER&D (5) | +4.0% | +0.2% | +25.0% |
| IT services excl. four (7) | +7.3% | +4.9% | +13.7% |
| ITeS/BPM (5) | +36.2% | +28.7% | +47.7% |
| IT + ER&D excl. four (12) | +5.5% | +2.3% | +20.3% |

- The 12 IT and ER&D firms outside the four: FY26 headcount −1.2%, USD revenue +2.6%. Five of the 12 shrank over the three years.
- Firms that shrank: HGS −17%, Mastek −16%, Mphasis −8%, Birlasoft −7%, Cyient DET −6%, Tata Elxsi −3%, Sonata −2%.
- Top six plus the 21 combined: 2,016,758 → 2,017,997, essentially flat.
- The 21 firms' gain covers about 16% of the top six's 384k shortfall against their pre-COVID trend.
- Red team, FY26 revenue growth at 11 broader firms: about 5% revenue-weighted, median 3.1%, about 2.2% excluding eClerx and Firstsource.

**India vs competitors**
- India's share of world computer-services exports (84 reporters): 27.3% (2015), 20.4% (2022), 19.5% (2025). Excluding Ireland: 34.6%, 29.3%, 30.1%.
- Share of the 30-country delivery group: 75.2% (2015), 65.9% (2022), 65.2% (2025).
- H1 share among 25 countries: 67.0% (2023), 66.5%, 66.6%, 66.6% (2026). India grew +11.1% in H1 2026, the same as the others.
- Computer-export CAGR 2022–25 and 2025 levels:

  | country | CAGR | 2025 level |
  |--|--|--|
  | India | 11.8% | $197bn |
  | Poland | 18.3% | $20.3bn |
  | Romania | 11.5% | $10.2bn |
  | Philippines | 10.1% | $8.4bn |
  | Brazil | 19.3% | — |
  | Serbia | 22.6% | — |
  | Ukraine | −3.2% | — |

- India's share of US computer-services imports: 46.6% (2015), 24.4% (2022), 25.1% (2025). US imports from India were $18.0bn in 2025, and from 15 low-cost locations $3.9bn.
- US other-business-services imports from the Philippines fell from $4.5bn to $3.8bn over 2022–25.
- India's share of EU computer imports from outside the EU: 10.0% (2022), 9.4% (2024). Excluding the US, UK and Switzerland, it rose from 30.3% to 31.2%.
- Cognizant's India share of headcount: 72.6–73.1% across 2021–25.

**US BLS, NAICS 5415**
- Jan–Sep averages: 2,475k (2023), 2,442k, 2,406k, 2,368k (2026).
- The monthly peak was 2,483.5k in March 2023. September 2026 was 2,355.4k, which is −5.2% from peak (my calculation).

**Affiliated vs unaffiliated**
- The affiliated share of all US computer-services imports fell from 85.6% (2015) to 62.2% (2023), then rose to 66.0% (2025). The unaffiliated share is 34.0% in 2025.
- There is no India × affiliation split. Proxies: the MOFA share (72%, 2023) and the RBI private-limited share (60.8%, FY26).

## 3. Conflicts and caveats

- **RBI survey vs BoP.**
  - BoP computer services in FY26 ($203.7bn) is about $50bn above the survey's computer-services figure ($153.4bn), and the gap is unexplained.
  - BoP grew +38.8% over FY23–26 against +19.4% in the survey. Use BoP for timing only.
- **Survey method.**
  - Figures are grossed up for non-respondents, and the survey frame grew 12% in one round.
  - FY23 comes from a different release vintage, and there is a probable break at FY23 (public-limited +31.8% that year).
  - FY25 was first reported at $183.4bn before grossing up.
- **BEA coverage.** US computer imports from India were $13.6bn in 2023, against $103bn of RBI software exports to the US.
  - Over 2019–22, BEA's India series fell while India's BoP rose about 55%. BEA levels are a poor guide to India's sales to the US.
- **RBI census of foreign-owned firms across rounds.**
  - Use within-round growth only. The respondent set grew from 18.5k to 26.3k firms.
  - The red team's "about +22% in FY24" and the note's §5b (₹6.5 → 8.5 lakh crore) both compare across rounds and are wrong.
- **Nasscom.**
  - Levels are revised every year.
  - The industry total includes GCCs (confirmed): the FY24 restatement from 5.43m to 5.67m equals the GCC revision of +0.24m.
  - The Strategic Review (Feb 2026) and the GCC report (Jul 2026) are on different vintages.
  - The GCC count is for all functions. For mega-GCCs the mix is about 43% ER&D, 24% IT and 33% BPM.
  - Treat the 2026 GCC edition as an upper bound.
- **GCC export values are cost-plus.** They track wages, not volume. Net of about 9% GCC pay growth (Aon), volume growth is about 2–5% a year.
  - The safe-harbour margin changes to a single 15.5% from FY27, which will create a series break.
- **Headcount.** Listed and top-six headcounts are global, not India-only. This matters especially for the BPM firms.
  - Acquisition adjustments are lower bounds.
- **IMF shares.**
  - They are in USD, so a strong euro and zloty in 2025 flatter Central and Eastern Europe.
  - Vietnam, China, the UK and Chile are missing.
  - They measure values, not jobs, so a shift of only junior work abroad would be invisible.
- **Job postings.** Naukri's one-month "GCC +4% vs IT −4%" is noise: the monthly year-on-year standard deviation is about 23 points.

## 4. Conclusions, and what round 4 changed

**Round 3's conclusions**
- Output is not shrinking: exports grow 7–8% a year in USD, and the growth is real IT work, not BPO.
- Growth is concentrated in private-limited exporters (GCCs, multinational vendors, unlisted firms).
- Work is not leaving India in aggregate (S4d ruled out). There is no onshoring.
- Jobs are the weak link. Industry employment grows about 2% a year against revenue growth of 5–6%.
- GCCs added about 260k tech jobs (central). That more than offsets the top six's −61k against FY23 and covers about two-thirds of their −384k against trend.
- The rest of the industry is roughly flat.
- The broad IT and ER&D mid-tier did not absorb the slack (S4b weak). Persistent is the exception.
- The red team concluded: "reallocation of output, but stalled job creation for young graduates".

**What round 4 superseded** (`round4/robustness/demand/FINDINGS.md`, dated 2026-10-15)
- Net of GCCs' pre-2023 hiring pace, the GCC term in the demand decomposition becomes +0.5 pp, range −2.2 to +1.6. Before, it was −1.0.
- Pre-2023 additions were about 100–165k a year; post-2023 about 94–180k a year (central, staffing-firm basis, 128k).
- The RBI census gap between foreign subsidiaries and total exports was +5.3 pp in FY20–23 and +4.3 pp in FY24–25.
- So GCCs gained share no faster after 2023 than before, and "GCCs drop out" of explaining the post-2023 slowdown.
- This undercuts round 3's framing that GCC hiring "absorbed" the top-six shortfall. GCC growth is real, but it is a continuing trend, not a new shift.
- This fits the trade folder's result that the private-limited share did not accelerate.
- `round4/SYNTHESIS.md` (first pass) still says "GCCs about −1". The robustness file is the later word.
- The robustness file also confirms the US NAICS 5415 decline with CES data: −0.6% a year over 2023–25, against +3.6% over 2016–22.

## 5. Candidate charts

1. **Exports in USD, FY23–26, total vs public-limited vs private-limited.** `round3/sector_aggregates/exports_recomputed.csv`, rows "RBI survey *_usd_bn", columns fy and level.
2. **Long-run organisation-type shares, FY12–26.** `trade/rbi_survey_orgtype.csv`, columns private_ltd_share_pct and public_ltd_share_pct. Mark the FY23 break.
3. **Export mix by activity, FY24–26.** `round3/red_team/rbi_exports_by_activity_type.csv`, series it_services, bpo, engineering and software_products, column usd_bn.
4. **Quarterly BoP computer exports, level and y/y, through 2026Q2.** `trade/imf_bop_india_services_quarterly.csv`, filtered to INDICATOR=SI2, BOP_ACCOUNTING_ENTRY=CD_T, columns TIME_PERIOD and OBS_VALUE.
5. **Revenue vs employment growth, indexed FY23=100.** `round3/sector_aggregates/sector_vs_top6_fy23_fy26.csv`, columns fy23, fy26 and cum_growth_pct for the Nasscom, RBI, BoP and top-six rows.
6. **Top-six headcount vs counterfactual trends, FY16–26.** `round3/gcc/top6_headcount_fy.csv`, columns top6, trendpre_from_FY23 and trend7_from_FY20.
7. **GCC headcount scenarios as a range plot.** `round3/gcc_reconcile/gcc_scenarios.csv`, columns gcc_change_all_functions_k_low/central/high and gcc_tech_change_k_share0.67, for the FY23-26 window.
8. **GCC hiring before vs after 2023.** `round4/robustness/demand/gcc_baseline_scenarios.csv`, columns pre_adds_k_per_yr and post_adds_k_per_yr. Alternatively `gcc_rbi_relative_growth.csv`, column foreign_subs_minus_total.
9. **RBI census of foreign subsidiaries, within-round growth vs total software exports.** `round3/gcc/rbi_fla_foreign_subs_ic.csv`, columns within_round_growth_inr_pct and the USD equivalent, alongside RBI total growth.
10. **Listed-firm headcount change by segment, FY23–26.** `round3/listed_panel/listed_panel_summary.csv`, metric=hc, columns agg_pct_change_FY23_26, with the excluding-acquisitions values from FINDINGS. A firm-level dot plot can use `listed_panel_firms.csv`, column hc_chg_pct_FY23_26 by group.
11. **India's share of world and delivery-group computer exports, 2015–25.** `round3/offshore_competitors/india_share_summary.csv`, metrics "India share excl. Ireland, balanced panel 2015-2025, %" and "India share of emerging delivery-country group, balanced 2015-2025, %".
12. **H1 growth, India vs 24 others, 2020–26.** `imf_h1_india_vs_delivery_group.csv`, columns india_yoy_pct, others_yoy_pct and india_share_pct.
13. **Competitor export levels and CAGR.** `imf_computer_exports_by_country.csv`, columns 2019–2025 for IND, POL, PHL, ROU, BRA, SRB and UKR. Use a log scale or a CAGR bar chart.
14. **India's share of US computer imports and the affiliated share, 2006–25.** `trade/affiliated_share_annual.csv`, columns India_share_of_US_computer_services_imports_pct and WORLD_US_computer_services_imports_affiliated_share_pct. MOFA_to_parents_share_of_ITA_total_pct can be added.
15. **US NAICS 5415 employment, monthly 2015–Sep 2026.** `bls_ces_monthly.csv`, column CES6054150001. A small companion chart can use `cognizant_headcount_by_location.csv`, column india_share_pct.