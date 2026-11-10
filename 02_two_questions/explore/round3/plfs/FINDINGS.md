# FINDINGS — PLFS: IT/ITeS employment of young graduates, 2017-18 to CY2025

*Saved by the orchestrator from the subagent's report; subagents cannot write report files. Date: 2026-10-14.*

PLFS (MoSPI) unit-level data were downloaded under the user's microdata.gov.in account and Data Access Agreement. Unit-level data stay in `data/sources/plfs/` (gitignored); only aggregate tables are here. Cite PLFS (MoSPI) wherever these are used, and send MoSPI a copy of any publication.

## Summary
- **Validation.** Usual status (ps+ss), age 15+: LFPR, WPR and UR match the published figures exactly in 7 of 9 rounds.
  - 2017-18: UR is 0.1pp off (it matches the all-ages headline).
  - 2020-21: LFPR and WPR are 0.4pp low; the cause is unexplained.
- **Graduates aged 21–30 employed in NIC 62+63 rose from 1.1m (2017-18) to about 2.6–3.0m (2022-23 to 2023-24), and have been flat since.** No significant fall within one survey design.
  - One high-weight FSU (first-stage sampling unit) in Jan–Jun 2024 makes up about 9% of the 2023-24 and CY2024 totals. Without it, both are about 2.6–2.7m.
- **ICT occupations (NCO-2015 251/252/351) employed outside NIC 62–63:** 8.2% (2022-23) → 10.1% → 11.5% → 12.5% (CY2025).
  - Counting NIC 58 (mostly software publishing) as IT gives 5.6% → 8.8%.
  - This suggests modest in-housing, not large-scale relocation.
- **Junior earnings (regular salaried, age 21–25, in 62/63).** The mean rose from ₹20.1k (2017-18) to ₹34.4k (CY2024), then fell to ₹30.9k (CY2025). The median fell from ₹35k to ₹28k.
  - Junior pay relative to ages 31–40 slipped from about 0.58 to about 0.52.
  - All graduates aged 21–25 earned a flat ₹20.6–20.8k.
  - The CY2025 fall is suggestive only (design break; CIs overlap).
- **Unemployment, ps+ss, ages 21–30:**
  - graduates: 31.7% → 24.5% (CY2024) → 20.6% (CY2025);
  - engineering-degree holders: 38.7% → 22.4% → 20.5%.

## 1. Data structure
- **Zip contents.** The zips contain Stata files only: no README, layout or code list. Value labels are corrupt (2017-18) or missing (CY2025).
  - Documentation was taken from the MoSPI NADA catalogue (entries 213, 254, 284).
  - Codes follow the standard PLFS Schedule 10.4 lists and were checked against code distributions in the data.
- **July–June rounds.** Each has 4 files: household and person, first visit (V1) and revisit (RV). The person V1 file is used: rural and urban, all four quarters, about 413–433k persons.
- **CY2024.** Only `chhv1` and `cperv1` (first visit, Q3–Q6 of panel 4). There are no revisit files, which is why the zip is only 13 MB.
  - Its Jan–Jun 2024 records are identical to those in 2023-24: all 104,806 Q3 records match on key, age, sex, education, status, NIC and MULT.
- **CY2025 (revamped design).** `chhv1`/`cperv1` only, 1.15m persons, monthly samples.
  - Variables are renamed. There is no sub-sample or NSS/NO_QTR variable; a `group` stratum and new education items appear.
- **Industry and occupation codes.**
  - Usual-status NIC is 5-digit; current weekly status (CWS) NIC is 2-digit only.
  - NCO is 3-digit: NCO-2004 through 2020-21, NCO-2015 from 2021-22.

## 2. Variable mapping
The full mapping is in `variable_mapping.csv`.

| item | 2017-18 to 2019-20 | 2020-21 to 2023-24 | CY2024 | CY2025 |
|--|--|--|--|--|
| file | hh_per_fv / PerV1 / PERFV | perv1 | cperv1 | cperv12025 |
| age, sex | b4q6, b4q5 | b4q6, b4q5 | Age, Sex | age, sex |
| sector (1 = rural, 2 = urban) | b1q3 | b1q3 | Sector | sec |
| general education (12 = graduate, 13 = postgraduate) | b4q8 | b4q8 | General_Education_Level | gedu_lvl |
| technical education (03 = engineering/technology degree) | b4q9 | b4q9 | Technical_Education_Level | tedu_lvl |
| principal status / NIC / NCO | b5pt1q3 / q5 / q6 | same | Principal_Status_Code / Industry / Occupation | pas / ind_pas / ocu_pas |
| subsidiary status | b5pt2q3 | b5pt2q3 | Subsidiary_Status_Code | sas |
| CWS status / NIC / NCO | b6q5 / b6q6 / b6q7 | same | CWS_* | acws / aind_cws / ocu_cws |
| regular wage earnings | b6q9 | b6q9 | CWS_Earnings_Salaried | ern_reg |
| FSU | fsu_per_fv | b1q1_perv1 | FSU | mfsu |
| weights | NSS, NSC, MULT, No_qtr | NSS, NSC, mult, no_qtr | Ns_Count_Sector_Subsample, Ns_Count_Sector_Substratum, Subsample_Multiplier, State_Sector_Stratum_Substra | nsc, mult |

Status codes: workers are 11–51; regular salaried is 31; unemployed is 81. Earnings are recorded for CWS status 31, 71 and 72.

## 3. Weighting
- **July–June rounds:** MULT/100 if NSS = NSC, else MULT/200; then divide by NO_QTR for annual estimates. This is the 2023-24 README rule, applied to all July–June rounds.
- **CY2024:** MULT/(NO_QTR×100) if NSS = NSC, else MULT/(NO_QTR×200). This is numerically identical to the rule above.
- **CY2025:** MULT/100.
- Annual usual-status estimates use the first-visit file, rural and urban together.

## 4. Validation (ps+ss, age 15+, persons, all-India; estimate / published, %)

| round | LFPR | WPR | UR |
|--|--|--|--|
| 2017-18 | 49.8 / 49.8 | 46.8 / 46.8 | 6.0 / 6.1 (all ages 6.1) |
| 2018-19 | 50.2 / 50.2 | 47.3 / 47.3 | 5.8 / 5.8 |
| 2019-20 | 53.5 / 53.5 | 50.9 / 50.9 | 4.8 / 4.8 |
| 2020-21 | 54.5 / 54.9 | 52.2 / 52.6 | 4.2 / 4.2 |
| 2021-22 | 55.2 / 55.2 | 52.9 / 52.9 | 4.1 / 4.1 |
| 2022-23 | 57.9 / 57.9 | 56.0 / 56.0 | 3.2 / 3.2 |
| 2023-24 | 60.1 / 60.1 | 58.2 / 58.2 | 3.2 / 3.2 |
| CY2024 | 59.6 / 59.6 | 57.7 / 57.7 | 3.2 / 3.2 |
| CY2025 | 59.3 / 59.3 | 57.4 / 57.4 | 3.1 / 3.1 |

The 2020-21 gap is 0.4pp in both rural and urban areas and does not come from the NO_QTR divisor. It may reflect the COVID-era survey or a different data release.

## 5. Definitions
- **Employment:** usual principal status (UPS) worker; industry is the UPS NIC.
- **Industry groups:** 62; 63; 62+63; 822; 82; IT+ITeS = 62+63+822.
- **Graduate:** general education code 12 or 13.
- **Engineering degree:** technical education code 03. A broader variant that adds code 13 (graduate-level diploma) is in the levels file.
- **ICT occupations:**
  - NCO-2015 251, 252, 351.
  - For NCO-2004 rounds, 213 + 312 as an approximate concordance (312 is broader).
- **Earnings:** CWS regular wage workers (status 31/71/72) in CWS NIC 62/63 with earnings above zero; nominal INR, previous month.
- **Precision:**
  - Method: Taylor linearisation with the ultimate-cluster variance estimator.
  - Clusters: FSU×quarter (FSU×month in CY2025).
  - Strata: state × sector × stratum × sub-stratum (plus `group` in CY2025).
  - Ratios are linearised. No finite-population correction; the one singleton stratum (CY2025) contributes 0.
  - CI = estimate ± 1.645 SE. Cells with fewer than 100 respondents are flagged.

## 6. Results

### Key series: employed graduates aged 21–30, thousands, 90% CI

| round | 62+63 | CI | n | IT+ITeS | CI | all employed grads 21–30 | share 62+63 (%) | CI | share IT+ITeS (%) |
|--|--|--|--|--|--|--|--|--|--|
| 2017-18 | 1,121 | 998–1,243 | 439 | 1,206 | 1,076–1,335 | 14,919 | 7.5 | 6.7–8.3 | 8.1 |
| 2018-19 | 1,247 | 1,073–1,422 | 455 | 1,313 | 1,136–1,490 | 16,137 | 7.7 | 6.7–8.8 | 8.1 |
| 2019-20 | 1,388 | 1,215–1,561 | 459 | 1,490 | 1,313–1,668 | 18,362 | 7.6 | 6.6–8.5 | 8.1 |
| 2020-21 | 1,688 | 1,507–1,868 | 625 | 1,818 | 1,632–2,003 | 18,897 | 8.9 | 8.0–9.8 | 9.6 |
| 2021-22 | 2,429 | 2,204–2,653 | 862 | 2,527 | 2,299–2,755 | 20,599 | 11.8 | 10.8–12.8 | 12.3 |
| 2022-23 | 2,606 | 2,350–2,863 | 872 | 2,729 | 2,469–2,988 | 20,424 | 12.8 | 11.6–13.9 | 13.4 |
| 2023-24 | 2,994 | 2,436–3,553 | 844 | 3,075 | 2,516–3,635 | 24,089 | 12.4 | 10.4–14.5 | 12.8 |
| CY2024 | 2,884 | 2,362–3,405 | 857 | 3,017 | 2,493–3,542 | 24,810 | 11.6 | 9.7–13.5 | 12.2 |
| CY2025 | 2,822 | 2,565–3,079 | 2,103 | 2,941 | 2,681–3,202 | 28,446 | 9.9 | 9.1–10.7 | 10.3 |

- **One cluster drives the 2023-24 peak.** A single FSU (Jan–Jun 2024) contributes 9.3% of 2023-24 and 9.6% of CY2024. Without it, the totals are 2.72m and 2.61m.
- **Engineering-degree holders aged 21–30 in 62+63:** 0.39m (2017-18), 1.09m (2021-22), 1.30m (2022-23), 1.56m (2023-24), 1.64m (CY2024), 1.39m (CY2025). From 2021-22 on, this is 45–53% of all employed engineering graduates aged 21–30.

### Employment levels, all ages, thousands
Breakdowns by age, education, sector and status are in `employment_levels_long.csv`.

| round | 62 | 63 | 62+63 | 822 | 82 | IT+ITeS |
|--|--|--|--|--|--|--|
| 2017-18 | 1,798 | 553 | 2,352 | 188* | 1,731 | 2,539 |
| 2018-19 | 1,990 | 550 | 2,540 | 149* | 1,532 | 2,689 |
| 2019-20 | 2,351 | 632 | 2,982 | 223* | 1,614 | 3,206 |
| 2020-21 | 2,664 | 554 | 3,218 | 281* | 1,474 | 3,499 |
| 2021-22 | 3,818 | 766 | 4,583 | 214* | 1,730 | 4,797 |
| 2022-23 | 4,703 | 772 | 5,475 | 231* | 1,720 | 5,706 |
| 2023-24 | 5,179 | 797 | 5,976 | 180* | 1,440 | 6,156 |
| CY2024 | 4,901 | 844 | 5,745 | 260* | 1,588 | 6,006 |
| CY2025 | 4,720 | 982 | 5,702 | 259 | 1,930 | 5,962 |

\* Fewer than 100 respondents; relative SE 14–19%.

**62+63 by age band, thousands:**

| round | 21–25 | 26–30 |
|--|--|--|
| 2017-18 | 461 | 858 |
| 2020-21 | 760 | 1,126 |
| 2022-23 | 1,066 | 1,705 |
| 2023-24 | 1,295 | 1,897 |
| CY2024 | 1,250 | 1,859 |
| CY2025 | 1,169 | 1,921 |

In 62+63, about 91% of workers are graduates, about 90% are urban, and 88–92% are regular salaried.

### ICT-occupation workers outside NIC 62–63 (all ages)

| round | ICT-occupation total (k) | outside IT (k) | share outside (90% CI) | n outside | classification |
|--|--|--|--|--|--|
| 2017-18 | 2,259 | 753 | 33.4% (29.6–37.1) | 350 | NCO-2004 |
| 2018-19 | 2,363 | 785 | 33.2% (29.1–37.4) | 318 | NCO-2004 |
| 2019-20 | 2,394 | 788 | 32.9% (28.8–37.1) | 334 | NCO-2004 |
| 2020-21 | 2,524 | 735 | 29.1% (25.1–33.2) | 304 | NCO-2004 |
| 2021-22 | 3,549 | 732 | 20.6% (15.5–25.8) | 229 | NCO-2015 (first year, anomalous) |
| 2022-23 | 3,975 | 326 | 8.2% (6.4–10.1) | 139 | NCO-2015 |
| 2023-24 | 4,451 | 451 | 10.1% (7.5–12.7) | 159 | NCO-2015 |
| CY2024 | 4,235 | 487 | 11.5% (8.4–14.6) | 159 | NCO-2015 |
| CY2025 | 4,108 | 515 | 12.5% (10.6–14.5) | 429 | NCO-2015 |

- **Graduates aged 21–30 in ICT occupations outside IT:** 127k (2022-23), 185k, 269k, 223k (CY2025). Fewer than 100 respondents in every round except CY2025.
- **Host industries.** The largest is NIC 58 (88–99% software publishing, 582), at 23–32%. Then 61, 82, 84, 64 and 71.
- **Treating 58 as IT,** the share outside IT is 5.6% (2022-23) → 7.8% → 8.4% → 8.8% (CY2025).

### Earnings: regular salaried workers in 62/63 (CWS industry), mean / median, INR per month

| round | age 21–25 | age 26–30 | age 31–40 |
|--|--|--|--|
| 2017-18 | 20,076 / 19,000 | 29,411 / 25,000 | 34,380 / 30,000 |
| 2019-20 | 21,475 / 20,000 | 32,207 / 30,000 | 44,851 / 35,000 |
| 2021-22 | 27,264 / 25,000 | 39,385 / 35,000 | 44,947 / 40,000 |
| 2022-23 | 30,168 / 26,800 | 39,228 / 38,000 | 51,351 / 48,500 |
| 2023-24 | 33,120 / 30,000 | 45,046 / 45,000 | 58,777 / 50,000 |
| CY2024 | 34,430 / 35,000 | 46,928 / 45,000 | 59,024 / 52,000 |
| CY2025 | 30,904 / 28,000 | 45,778 / 40,000 | 59,095 / 50,000 |

- SE of the age 21–25 mean: ₹0.8–1.7k; n = 183–866 per cell.
- For comparison, the mean for all employed graduates aged 21–25 was ₹20.6k (CY2024) and ₹20.8k (CY2025).

### Unemployment, ps+ss (%)

| round | graduates aged 21–30 | engineering degree, aged 21–30 |
|--|--|--|
| 2017-18 | 31.7 | 38.7 |
| 2018-19 | 30.9 | 38.5 |
| 2019-20 | 30.8 | 33.8 |
| 2020-21 | 27.2 | 35.1 |
| 2021-22 | 26.6 | 28.1 |
| 2022-23 | 25.9 | 26.2 |
| 2023-24 | 24.6 | 23.0 |
| CY2024 | 24.5 | 22.4 |
| CY2025 | 20.6 | 20.5 |

SEs: about 0.4–1.0pp for graduates and 1.5–3pp for engineering-degree holders. Principal-status rates and the age 21–25 group are in the CSV.

## 7. Caveats
1. **CY2025 design break.** CY2025 uses a monthly design with new strata and multipliers. Employed graduates aged 21–30 jump 15% in one year. Compare it with earlier rounds cautiously, especially shares.
2. **2023-24 and CY2024 share their Jan–Jun 2024 records.** Their difference is effectively H2 2023 vs H2 2024. One high-weight FSU in that overlap inflates both.
3. **The stratum count changes.** It was 1,115 through 2020-21, then 985 (2021-22 and 2022-23), then 910 (2023-24 and CY2024). The +44% jump in 2021-22 is not all real growth.
4. **Occupation codes changed from NCO-2004 to NCO-2015 in 2021-22.** 2021-22 looks anomalous, so read the occupation split only from 2022-23.
5. **The CWS industry code is 2-digit.** Earnings can't isolate 822, and they relate to current weekly status, not usual status.
6. **2020-21 validation gap.** 0.4pp on LFPR and WPR, unexplained.
7. **Industry is self-reported.** GCC staff may appear under NIC 62 or under the parent firm's industry.
8. **Disclosure control.** Host-industry cells with fewer than 3 respondents are suppressed. No unit-level data left `data/sources/`.

## 8. Files
Scripts:
- `build_mapping.py`
- `extract_std.py`
- `analyze.py`
- `make_chart.py`
- diagnostics: `check_*.py`, `diag_*.py`
- helpers: `inspect_dta.py`, `peek.py`, `value_labels.py`, `docx_text.py`

Outputs:
- `variable_mapping.csv`
- `validation.csv`
- `key_series_grads_21_30.csv`
- `results_compact.csv`
- `employment_levels_long.csv`
- `occupation_split.csv`
- `ict_occ_outside_it_host_industries.csv`
- `earnings_regular_salaried.csv`
- `unemployment_grads.csv`
- `plfs_it_young_graduates.png`

To rerun, from this folder:
```
python3 -I extract_std.py ../../../sources/plfs/extracted variable_mapping.csv ../../../sources/plfs/work
python3 -I analyze.py ../../../sources/plfs/work .
python3 -I make_chart.py .
```

## Sources
- MoSPI NADA catalogue entries [213](https://microdata.gov.in/NADA/index.php/catalog/213/related-materials), [254](https://microdata.gov.in/NADA/index.php/catalog/254/related-materials) and [284](https://microdata.gov.in/NADA/index.php/catalog/284/related-materials).
- [Key Employment-Unemployment Indicators, PLFS 2024](https://www.mospi.gov.in/sites/default/files/publication_reports/Key_employment_unemployment_indicators_PLFS_2024_final.pdf).
- [PLFS Annual Report 2025 press note](https://www.mospi.gov.in/uploads/latestReleases/latest_release_1774607827733_3e8964a9-268b-4cc9-ad65-cfc8a9e32f08_Press_note_AR_PLFS_2025_23032025_V2.1_26032026_final.pdf).
- PLFS annual reports for the July–June rounds.
