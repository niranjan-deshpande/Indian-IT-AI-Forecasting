# FINDINGS — H-1B LCA firm × occupation panel

*Saved by the orchestrator from the probe's report; the probe could not write files. The value-of-information result at the end was added by the orchestrator.*

## 1. Access
- **Source:** DOL OFLC, https://www.dol.gov/agencies/eta/foreign-labor/performance. Free, no login.
- **Format:** xlsx at case level; one file per fiscal year, and one per quarter from FY2020.
- **Coverage pulled:** Oct 2014 – 30 Jun 2026 (FY2026 Q3), 30 files, about 4 GB. Only the filtered extract is kept.
- **Lag:** about one quarter.
- **Download quirk:** Akamai blocks browser user-agents; a plain user-agent works.

## 2. Level
- **Unit:** employer × case, with SOC code, job title, wage level and worksite.
- **Firms:** all 8, plus Mphasis, Persistent, Coforge, Hexaware and Capgemini. LTIMindtree is LTI + Mindtree.
- **Volume:** the 8 firms file 36–89k certified cases a year.
- **Certified positions per fiscal year:**

| FY | positions |
|--|--|
| 2015 | 252k |
| 2016 | 218k |
| 2017 | 170k |
| 2018 | 152k |
| 2019 | 104k |
| 2020 | 92k |
| 2021 | 155k |
| 2022 | 152k |
| 2023 | 84k |
| 2024 | 56k |
| 2025 | 52k |
| 2026 (Q1–Q3) | 24k |

- **Per-firm counts:** `lca_firm_year_positions.csv`.

## 3. Measurement
- **Definition:** positions are the "Total number of foreign workers requested by the Employer". These are requests, not hires.
- **Mapping to the identity:** they measure the task mix and a·Q for the US-onsite H-1B slice. They say nothing about p.

## 4. Noise
Pooled 8 firms; trailing-4-quarter YoY log ×100 of case counts; 2015–22 excluding 2020Q2–2021Q2 (n=21).

| series | s.d. | AR(1) | pre mean | post (2023–26Q2) mean |
|--|--|--|--|--|
| total cases | 21.3 | 0.62 | −5.4 | −9.9 |
| total positions | 33.0 | 0.84 | −9.8 | −34.4 |
| high−low exposure, Eloundou GPT-4 terciles | 14.5 | 0.75 | −13.4 | −4.8 |
| high−low exposure, Felten LM-AIOE terciles | 28.4 | 0.79 | +8.6 | −28.1 |
| Eloundou contrast, 5 stable-coding firms | 13.5 | — | −4.3 | −4.8 |
| job-title contrast, same 5 firms | 16.7 | — | −19.7 | −23.9 |

- **Per-firm noise (Eloundou contrast):** s.d. ranges from 14.7 (HCLTech) and 18.6 (TechM) to 111.8 (Cognizant); the median is about 55.
- **No concentration in AI-exposed occupations:** 2023–26 declines are not concentrated there, and the sign flips with the exposure score used.
- **Why the sign flips:** firms recode all their filings at once (Cognizant 15-1211 → 15-1299 in 2023–24; Infosys 15-1121 → 15-1199 in 2020).

## Validation (pre-specified, 2015–22)
- **Against onsite headcount or effort** (Infosys, Wipro, TechM, LTI, Mindtree; n=106):
  - case counts: r=0.32 (p=0.001), just over the 0.3 bar
  - positions: r=0.13 (p=0.20), fails
- **Against total headcount growth gL:** r=0.13–0.16. Accenture: r=−0.79.

## 5. Predicted signs (high−low exposure contrast)
S1 ≈0; S2 and S3 <0 (indistinguishable); S4 ≈0.

**Confounds:**
- **Bulk filing:** Cognizant averaged about 30 positions per case to FY2017, Mphasis about 20 to FY2018, Infosys 5–35 in FY2020–23.
- **2017 scrutiny:** Level I share fell from about 20% to under 1%.
- **Sept 2025 $100k proclamation and wage-weighted lottery:** new-employment LCAs fell 128–181 log points in every exposure tercile, while continuing employment moved −20 to +6. This swamps totals from 2025Q4.

## 6. Verdict
**Conditional, leaning no.** Only worth it with case counts, stable-coding firms, a job-title classifier and USCIS Employer Data Hub approvals (4–6 RA-days).

## Value of information (orchestrator)
S1-vs-S3 accuracy at 12 quarters, observed from quarter 6 after onset (`scripts/07_voi.py`):

| scenario | accuracy |
|--|--|
| baseline (no LCA) | 0.74 |
| measured per-firm noise | 0.76 |
| measured noise, signal attenuated to 0.3 (validation r) | 0.74 |
| HCLTech + TechM only | 0.76 |

**Fails AC1.** The occupation channel needs a contrast noise of 8pp or less per firm to reach 0.90.

## Files
- Scripts: `01_download_filter.py`, `02_build_panel.py`, `03_analysis.py`, `04_robustness.py`
- Data: `lca_cases_target_firms.csv.gz`, `lca_firm_quarter_long.csv`, `lca_firm_year_positions.csv`, `employer_name_map.csv`
- Results: `occ_group_exposure.csv`, `lca_yoy_series[_cases].csv`, `lca_noise_stats[_cases].csv`, `lca_validation[_cases].csv`, `lca_robustness_series.csv`
- `exposure/`: Eloundou (github.com/openai/GPTs-are-GPTs), Felten AIOE and LM-AIOE (github.com/AIOE-Data/AIOE), BLS SOC crosswalk
