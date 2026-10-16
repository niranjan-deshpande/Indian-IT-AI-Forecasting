# Inventory: labour market, hiring, seniority and juniors

Everything below was read only; no files were changed. Paths are relative to `data/explore/`. Figures marked "(my calc)" are ones I computed from the CSVs; everything else is in the files or the FINDINGS.md notes.

## 1. Datasets

| Folder / file | Measures | Source | Entities | Span, frequency, latest |
|--|--|--|--|--|
| `round3/plfs/` (`key_series_grads_21_30.csv`, `employment_levels_long.csv`, `earnings_regular_salaried.csv`, `unemployment_grads.csv`, `occupation_split.csv`, `ict_occ_outside_it_host_industries.csv`, `validation.csv`) | Survey-weighted employment levels, earnings, unemployment and ICT-occupation splits, each with SE, 90% CI and unweighted n | PLFS unit data, aggregated in this repo (MoSPI agreement: cite, aggregate only) | All-India; NIC 62, 63, 62+63, 822, 82; IT+ITeS; cuts by age, graduate, engineering degree, urban/rural, status | Annual: 2017-18 to 2023-24 (July–June rounds), then CY2024 and CY2025. Latest is CY2025 |
| `round3/seniority_sector/nirf_*.csv` | 4-year engineering degree (UG) graduates, number placed, institution median salary, number going to higher studies | NIRF "Data Submitted by Institution" PDFs; 1,313 parsed | 183–239 ranked engineering institutions. Elite = IIT/NIT/IIIT/IISc/BITS. Balanced panel of 147 | Graduating classes 2015-16 to 2023-24, annual. NIRF 2026 is not yet online |
| `round3/seniority_sector/key_numbers.csv` | foundit, JobSpeak GCC tiles, Taggd, Zinnov, AICTE | Portals and press | Mixed | Point values up to Sep 2026 |
| `round3/seniority_firms/under30_panel.csv` | Under-30 share of headcount and of new hires | GRI/ESG annexes | 10 firms: the top 6 plus Persistent, Mphasis, Hexaware, Coforge | FY19–FY26, annual |
| `round3/seniority_firms/` other files | Rule 5 median remuneration (`median_remuneration.csv`), TCS BRSR pay by band, cost per head (`cost_per_head.csv`), Infosys trainee proxy (`infosys_trainees_implied.csv`) | Annual reports and Infosys fact sheets | Firms | Annual to FY26. Trainee proxy is quarterly, Q1 FY11 to Q1 FY27 |
| `workforce/workforce_firm_tidy.csv` | 1,566 rows: headcount, hires and turnover by age; Infosys job levels; fresher counts | Firm ESG, annual reports, earnings calls | Top 6, with LTI and Mindtree separate | FY14–FY26 |
| `workforce/firm_year_junior_metrics.csv`, `fresher_hires_annual_best.csv` | Derived panel: hires by age, hires per $bn revenue, freshers | As above | Top 6 | FY16–FY26 with gaps |
| `workforce/jobspeak_monthly.csv`, `jobspeak_expband_yoy_combined.csv`, `jobspeak_expband_yoy_2025_26_chart.csv`, `jobspeak_vintages_long.csv` | Naukri job-postings indices | Info Edge PDFs | IT-Software and BPO/ITeS indices. Experience bands are all industries, not IT | IT index Jan 2021 to Aug 2026. Band levels Nov 2021 to Dec 2024; 2025–26 YoY read off charts |
| `round4/junior_gap/` | Estimates of junior vs experienced growth (s_J − s_E), Infosys stock-flow, PLFS age gap and relative pay | Built from the above | Firms and sector | Firm data to FY26, PLFS to CY2025 |
| `lca/lca_firm_year_positions.csv`, `lca_firm_quarter_long.csv` | US H-1B Labor Condition Applications (LCAs): certified cases and positions; splits by SOC code, wage level and new vs existing employment | US Department of Labor (DOL OFLC) | 13 firm groups | FY2015 to FY2026 Q3 (to 30 Jun 2026), quarterly |

## 2. Headline current-state facts

**Sector employment (PLFS, NIC 62+63, all ages, usual principal status)**
- 2.35m in 2017-18, then 2.98m (2019-20), 4.58m (2021-22), 5.48m (2022-23), 5.98m (2023-24), 5.75m (CY2024) and 5.70m (CY2025; 90% CI 5.33–6.07m).
- Employment roughly doubled 2019-20 → 2022-23 and has been flat since. The 2023-24 peak is partly one high-weight sampling cluster.
- About 91% of these workers are graduates, about 90% urban and 88–92% regular salaried.

**Young graduates aged 21–30 in IT (62+63)**
- 1.12m (2017-18), 1.69m (2020-21), 2.61m (2022-23), 2.99m (2023-24), 2.88m (CY2024), 2.82m (CY2025; CI 2.57–3.08m).
- As a share of all employed graduates aged 21–30: 7.5% → 12.8% (2022-23) → 9.9% (CY2025). Part of that drop is the denominator jumping 15% at the CY2025 redesign.
- Engineering-degree holders aged 21–30 in IT: 0.39m → 1.64m (CY2024) → 1.39m (CY2025). That is 45–53% of all employed young engineering graduates.

**Graduate unemployment (ps+ss)**

| Group | 2017-18 | CY2024 | CY2025 |
|--|--|--|--|
| Graduates 21–30 | 31.7% | 24.5% | 20.6% |
| Graduates 21–25 | 45.0% | 35.0% | 28.3% |
| Engineering degree, 21–30 | 38.7% | 22.4% | 20.5% |

Unemployment has fallen steadily; there is no sign yet of distress among new graduates.

**Earnings (CWS regular wage workers in 62/63, nominal ₹ per month)**
- Age 21–25 mean: ₹20.1k (2017-18) → ₹34.4k (CY2024) → ₹30.9k (CY2025). Median: ₹35k → ₹28k over the last step.
- Age 31–40 mean is flat at about ₹59k from 2023-24 to CY2025.
- The IT premium for young graduates over all graduates aged 21–25 (my calc): 1.57× (2017-18), 1.74× (CY2024), 1.53× (CY2025). For comparison, all graduates aged 21–25 earn ₹20.8k.

**Junior relative pay (mean pay at 21–25 ÷ mean pay at 31–40)**
- IT: 0.643 (2020-21), 0.587 (2022-23), 0.583 (CY2024), 0.523 (CY2025).
- All graduates: flat at 0.53–0.58.
- Difference-in-differences, 2020-21 → CY2025: −5.4 log points a year (SE 1.85).
- The median ratio does not confirm it: 0.553 → 0.560.

**Age mix (PLFS 62+63; my calc)**
- Under-30 share of workers: 56.8% (2017-18), 59.1% (2020-21), 51.2% (2022-23), 53.7% (2023-24), 54.7% (CY2025). Noisy, with no clear trend.
- Share aged 21–25: about 20–24%.

**Firm under-30 share of headcount, FY23 → latest**

| Firm | FY23 | Latest |
|--|--|--|
| Infosys | 59.6% | 50.7% |
| TCS (India only, to FY25) | 52.9% | 47.7% |
| HCL | 41.3% | 34.3% |
| Wipro | 53.3% | 48.4% |
| TechM | 48.3% | 46.7% |
| LTIM | 44.5% | 35.0% |
| Persistent | 47.6% | 27.5% |
| Mphasis (to FY25) | 45.1% | 37.3% |

- The under-30 share of headcount fell at 8 of 10 firms; Hexaware and Coforge were flat.
- The under-30 share of new hires has recovered at Infosys (60.2% FY24 → 73.4% FY26) and LTIM (49.6% → 56.8%). Persistent is about 37%.

**Fresher hiring at the big firms (`fresher_hires_annual_best.csv`)**
- TCS: 110k (FY22; 100–118k depending on source), 44k (FY23), 42k (FY25), 44k (FY26).
- Infosys: 84.8k (FY22), 50k, 11.9k (FY24), 15.3k, 20k (FY26). Pre-COVID about 9–21k.
- HCL: 23k, 26.7k (FY23), 12.1k, 7.8k, 11.7k.
- TechM: 10k (FY22), 6k (FY25), 950 (FY26).
- LTIM: 4.7k (FY25), 6.7k (FY26).
- TCS + Infosys + HCL combined (my calc): about 218k (FY22) → 121k (FY23) → 65k (FY25) → 76k (FY26). That is about −65% from the peak, and roughly back to pre-boom levels.
- Definitions vary (trained vs hired vs onboarded; lower bounds), and TCS FY24 and Wipro after FY23 are missing.

**Infosys job levels and trainees**
- Junior band (JL3 and below): 157.9k (FY23) → 98.7k (FY26). As a share of headcount: 50% (FY14), about 40% (FY21), 46% (FY23), 30% (FY26) (my calc from `workforce_firm_tidy.csv`).
- Middle grew 141.8k → 179.7k; Senior 42.2k → 50.2k.
- Implied trainees (annual mean): about 15.5k (FY23), 4.2k (FY24, the lowest since FY11), 5.6k (FY25), 8.7k (FY26), 7.5k (Q1 FY27).
- Under-30 hires: 111.8k (FY22) → 22.3k (FY24) → 53.9k (FY26).

**Naukri/JobSpeak**
- IT-Software index, annual mean: 4,567 (2021), 4,914 (2022), 3,535 (2023), 3,445 (2024), 3,443 (2025), 3,514 (2026, Jan–Aug).
  - Peak is 5,872 (Jul 2022). The 2026 level is about 28% below the 2022 mean and has been flat for three years.
  - YoY in 2026 ranges from −7.6 to +10.3.
- Experience-band levels (all industries), 2022 → 2024: 0–3 years fell from 3,120 to 2,731 (−12%), while 16+ years rose from 1,823 to 2,752 (+51%).
- YoY gap, 0–3 years minus 16+ years: −35 (2023), −20 (2024), about −4 (2025), about +4 (2026). The junior penalty has reversed.
- Latest months, all industries:
  - Sep 2026: 0–3 years +1%, senior bands +5% to +7%.
  - Aug 2026: 0–3 years +15%.

**NIRF engineering placements (UG 4-year, all employers, GCCs included)**
- Placement rate for all institutions (unbalanced sample): 70.4% (2015-16), 72.5% (2021-22), 74.1% (2022-23), 70.1% (2023-24).
- Elite tier: 85.3% → 83.8% → 76.6%.
- Same-edition comparison for the class of 2023-24: number placed fell 1.8 log points while graduates rose 3.3. This is the first fall in the series; earlier years grew +2.5 to +10.5.
- Median of institution median salaries: all institutions ₹3.5L (2015-16), ₹6.5L (2021-22), ₹7.5L (2022-23), ₹7.5L (2023-24). Elite ₹15L → ₹12L for 2023-24; within-edition change −11 log points.
- Students going to higher studies rose about 20% for 2023-24 (balanced panel: 16.2k → 19.9k).

**H-1B LCA (certified cases, six Indian firms: TCS, Infosys, Wipro, HCL, TechM, LTIM; my calc)**
- 76.6k (FY15), 50.6k (FY19), 26.9k (FY23), 26.1k (FY24), 22.4k (FY25), 11.9k (FY26, Oct–Jun only).
- Positions are distorted by bulk filing; for example, Infosys positions were 93–105k in FY21–22.
- New-employment positions (all 13 firms) in the Apr–Jun cap quarter: 17.7k (2023), 17.6k (2024), 14.3k (2025), 2.1k (2026). This follows the September 2025 $100k proclamation.

## 3. Caveats

**PLFS**
- The CY2025 design changed: monthly sampling, new strata, and about 2.5× the sample size (n for 62+63 is about 4,470 vs about 1,750 before).
- 2023-24 and CY2024 share their Jan–Jun 2024 records, so they are not independent. One sampling cluster accounts for about 9% of both totals; without it they are 2.72m and 2.61m.
- The number of strata changes in 2021-22, so the +44% jump that year is partly artefact.
- Occupation codes switch from NCO-2004 to NCO-2015 in 2021-22. Read the ICT-outside-IT share only from 2022-23 (8.2% → 12.5%; 5.6% → 8.8% if NIC 58 counts as IT).
- Earnings use the 2-digit CWS industry code and are nominal; I found no CPI deflation in the files.
- The age 21–25 earnings cells have n = 183–866, with mean SE ₹0.8–1.7k.
- GCC staff cannot be identified (they may sit in NIC 62 or the parent's industry). Age is not experience.
- 2020-21 LFPR and WPR are 0.4pp off the published figures, cause unexplained.

**Firm data**
- Voluntary GRI disclosures with varying scope: TCS is India-only and read off charts; Persistent, Coforge and Hexaware include contract staff; Hexaware uses calendar years; LTIM is stitched from LTI and Mindtree.
- Turnover became voluntary-only around FY23, which breaks the stock-flow reconciliation.
- Infosys "Senior" absorbs "Top" from FY23. Fresher definitions vary.
- **Boom-cohort ageing:** the FY22–23 intake inflates the junior bump, and its promotion out of JL3 inflates the junior-level decline.
- Infosys stock-flow shows no excess ageing out yet (7.2% a year vs 8.5% pre-period). The fresher bulge crosses age 30 in FY30–31, when it will add about 7–19k crossings.

**Other sources**
- JobSpeak: postings only, with no campus hiring. Experience bands cover all industries. Values from 2025 on are read visually as simple %, while earlier values are log×100, so the combined file mixes the two.
- NIRF: upper-tier sample (about 175k of 1.2m+ B.Tech graduates). 35% of overlapping cells are revised in later editions, so prefer within-edition comparisons. No IT/GCC split.
- LCA: requests, not hires. Bulk filing, recoding of SOC codes, the 2017 scrutiny and the 2025 proclamation dominate. Validation against onsite headcount is weak (r = 0.32 for cases, 0.13 for positions).
- foundit: one portal with rounded shares; implied growth rates are ±5 points.

## 4. Conclusions the folders reached

1. **PLFS:** young-graduate IT employment rose about 2.5× to roughly 2.6–3.0m and has been flat since 2022-23, with no significant fall within one survey design. ICT occupations outside IT are rising modestly, which suggests some in-housing.
2. **Junior gap (`round4/junior_gap/FINDINGS.md`):**
   - Firm-scope s_J − s_E is about 0 to +1 pp a year (range −2 to +3). It is not distinguishable from zero once the FY22–23 boom is netted out.
   - Sector-scope is about +2 (21–25 vs 31–40: +1.4, CI −2.2 to 5.0; 21–30 vs 31–60: +1.9, CI −0.7 to 4.4). Suggestive, but the CI includes 0.
   - The boom unwound through a shift in the hiring mix toward over-30 hires (Infosys 30+ hires up 65%), not through ageing out.
   - Relative junior pay falling in IT points directionally to weaker demand for juniors.
   - All of this predates the summer-2026 jump in coding agents.
3. **Seniority firms:** under-30 shares fell from FY23 at 8 of 10 firms, and mid-tier growth (Persistent, Mphasis) came without a junior ladder. Junior hiring at Infosys and LTIM has partly recovered since FY24.
4. **Seniority sector:** entry-level hiring is falling sector-wide, but the evidence is modest and recent (NIRF 2023-24, foundit fresher postings −10%). GCCs hire freshers less intensively and offset only about a fifth of the IT loss.
5. **Workforce:** the JobSpeak junior gap was cyclical and has reversed. Infosys fresher hires are below the level its revenue would predict but the shortfall is narrowing (−59 → −31 log points, FY24–26).
6. **LCA:** no concentration of declines in AI-exposed occupations, and the sign flips with the exposure measure. Judged not worth pursuing ("conditional, leaning no").

## 5. Candidate charts

1. **Young graduates in IT, levels with CI:** `round3/plfs/key_series_grads_21_30.csv`, series `nic62_63`; columns `round`, `estimate`, `ci90_lo`, `ci90_hi`, with `share` for a second panel. A PNG already exists: `plfs_it_young_graduates.png`.
2. **Sector employment by age band (stacked):** `round3/plfs/employment_levels_long.csv`, `group=='nic62_63'`, `cut` in `age_15_20`, `age_21_25`, `age_26_30`, `age_31_40`, `age_41_60`; column `estimate`.
3. **Graduate unemployment:** `round3/plfs/unemployment_grads.csv`; `population` in `grads_21_30`, `grads_21_25`, `engdeg_21_30`; columns `ur_upss`, `ur_upss_se`.
4. **Earnings by age, IT vs all graduates:** `round3/plfs/earnings_regular_salaried.csv`; `sample` in `cws_regular_nic62_63_grads`, `cws_regular_all_grads`; columns `age_band`, `mean_inr`, `mean_se`, `median_inr`.
5. **Junior/senior pay ratio, IT vs all graduates:** `round4/junior_gap/plfs_relative_pay.csv`; columns `round`, `sample`, `ratio_mean`, `ratio_median`, `lnratio_se`.
6. **Fresher hires by firm, FY16–26 (bars, marking the FY22 peak):** `workforce/fresher_hires_annual_best.csv`; columns `firm`, `fy`, `fresher`, with `per_bn` as an alternative.
7. **Under-30 share of headcount and of hires, 10 firms (small multiples):** `round3/seniority_firms/under30_panel.csv`; columns `firm`, `fy`, `hc_share_lt30`, `hires_share_lt30`.
8. **Infosys job-level pyramid, FY14–26:** `workforce/workforce_firm_tidy.csv`, `firm=='infosys'`, `metric=='headcount_by_grade'`; columns `dimension` (`grade_junior`, `grade_middle`, `grade_senior`, `grade_top`) and `value_num`.
9. **Infosys trainee proxy, quarterly from FY11:** `round3/seniority_firms/infosys_trainees_implied.csv`; columns `period_end`, `trainee_effort_share_pct`, `implied_trainees_calibrated`.
10. **Under-30 vs 30+ hires per $bn of revenue:** `workforce/firm_year_junior_metrics.csv`; columns `hires_lt30_per_bnUSD`, `hires_30p_per_bnUSD`.
11. **JobSpeak IT-Software index, 2021–26:** `workforce/jobspeak_monthly.csv`; columns `month`, `idx_it_software`, with `idx_bpo_ites` as a comparison.
12. **JobSpeak experience gap:** `workforce/jobspeak_expband_yoy_combined.csv`, column `gap_0_3_minus_16plus`. For band levels to Dec 2024, use `idx_exp_0_3` and `idx_exp_16plus` in `jobspeak_monthly.csv`.
13. **NIRF placement rate and median salary by graduating class, elite vs other:** `round3/seniority_sector/nirf_ug4_placement_by_gradyear.csv`, `sample=='balanced'`; columns `tier`, `grad_year`, `placement_rate`, `median_of_inst_median_salary`, `higher_studies`.
14. **NIRF same-edition YoY change in placements:** `round3/seniority_sector/nirf_within_edition_yoy.csv`; columns `edition`, `tier`, `dlog_placed_x100`, `dlog_graduates_x100`.
15. **H-1B LCA cases, Indian firms, FY15–26:** `lca/lca_firm_year_positions.csv`, `measure=='certified_cases'`, year columns `2015`–`2026` (FY26 is partial). For the new-employment collapse, use `lca/lca_firm_quarter_long.csv`, `split=='emp_type'`, column `positions`.

A dot plot of the estimates (`round4/junior_gap/estimates_summary.csv`, columns `estimate`, `lo`, `hi`) suits an appendix better than the main text.