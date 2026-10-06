# Audit Task 1b — fiscal alignment, "missing" 2023, structural breaks, corrected-data pipeline

(Written by the Task 1b audit agent; saved verbatim by the orchestrator because the agent could not write .md files.)

Reproduce from ROOT: `scripts/audit/task3_alignment.py`, `task4_episodes.py`, `task6_breaks.py`, `ltim_sign_scan.py`, `make_corrections_1b.py`, then `build_corrected.py --check-baseline`.

## 3. Fiscal-year alignment

### 3.1 Fiscal calendars (full table with URLs: `audit/fiscal_calendar.csv`)

| firm | FY end | quarter-end months | primary evidence |
|--|--|--|--|
| TCS | 31 Mar | Jun, Sep, Dec, Mar | Q4FY26 press release (IFRS USD) p1: "for the quarter and full year ending March 31, 2026"; Q1FY27 press release p1: "quarter ending June 30, 2026" |
| Infosys | 31 Mar | same | 6-K 0001067491-26-000018 Ex.99.1: "For the year ended March 31, 2026"; 6-K …-000038 Ex.99.1: "For the quarter ended June 30, 2026" |
| HCLTech | 30 Jun to FY15; FY16 = 9 months (Jul-15 to Mar-16); 31 Mar from FY17 | Sep/Dec/Mar/Jun → Sep/Dec/Mar → Jun/Sep/Dec/Mar | Q4FY15 release p2/p12: Fiscal 2015 ends 30-Jun-15; Q3FY16 release p1: "The current financial year of the Company is for 9 months' period from July 01, 2015 to March 31, 2016"; Q1FY27 release p10: "Quarter ended 30-Jun-26" |
| Wipro | 31 Mar | Jun, Sep, Dec, Mar | Q4FY26 press release p1: "Quarter and Year ended March 31, 2026"; Q1FY27 IFRS statements p1: "three months ended June 30, 2026" |
| TechM | 31 Mar | same | Q4FY26 SEBI results p1: "year ended March 31, 2026"; Q1FY27 press release p1: "quarter ended June 30, 2026" |
| LTIM / LTI / Mindtree | 31 Mar | same | Q4FY26 release p1: "Q4 and Full Year FY26"; Q1FY27 release p5: "As of 30th June, 2026" |
| Accenture | 31 Aug | Nov, Feb, May, Aug | 10-K FY25 cover: "fiscal year ended August 31, 2025"; 10-Q covers Nov 30 2025, Feb 28 2026, May 31 2026 |
| Cognizant | 31 Dec | Mar, Jun, Sep, Dec | 10-K FY2025 cover: "fiscal year ended December 31, 2025"; 10-Q: "quarterly period ended June 30, 2026" |

### 3.2 `cal_q` assignment (`calq_mapping_check.csv`)
- Rule: `cal_q` = calendar quarter containing `period_end`, all firms (Accenture Nov→Q4, Feb→Q1, May→Q2, Aug→Q3).
- 0 rows (all 10 raw files) where `cal_q` ≠ quarter of `period_end`; 0 rows where `fiscal_q` conflicts with the firm's calendar; no calendar quarter has more than one `period_end`/`fiscal_q`; no duplicate firm × quarter rows in `core_quarterly`/`yoy_metrics`.
- Gaps are all documented collection gaps: break after 2012Q1 (gfc.csv vs main window); TechM cc YoY not disclosed 2017Q1–2019Q2 and 2019Q3–2020Q2; Mindtree no cc YoY except 2015Q2; LTIM YoY starts Q3FY23.
- HCLTech's transition year leaves no hole: Q3FY16 (Mar-16) is followed by Q1FY17 (Jun-16).

### 3.3 YoY computation
- `gR` = firm-reported cc YoY (same fiscal quarter a year earlier). `gL`, `gR_usd`, `du`, `gTCV`, `dsub` use `qadd(q, −4)` (four calendar quarters earlier). These coincide because every fiscal quarter is a fixed 3-month block; HCLTech Q1FY17's base is Q4FY15 (Jun-15 vs Jun-16).
- HCLTech reported vs computed USD YoY agree within 0.05pp in 2015Q2–2017Q1 (`yoy_lag_consistency.csv`). Gaps >1pp occur only for Accenture FY18 (ASC 606 basis), Wipro FY18–19 (perimeter restatements of levels) and Mindtree 2020Q3 (sign error).

### 3.4 How the pilot computes the comparator statistics
- Aggregate: cross-firm **median** per quarter over INDIAN6 + `lti` + `mindtree`, with `ltim` dropped before 2022Q3. So 2022Q3 headcount counts LTI, Mindtree and LTIM together (8 entities).
- Windows: pre = 2016Q1–2022Q4 excl. 2020Q2–2021Q2 (n = 23); post = 2023Q1–2026Q2 (n = 14).
- Reproduced exactly: corr 0.901 / 0.579 (revenue), 0.830 / 0.329 (headcount). Gaps (Indian − Accenture): revenue −1.08 / −1.58; headcount −1.65 / −2.61.
- Firms per quarter in the median: revenue 4–6; headcount 3 in 2016Q1, 6–7 through 2022Q2, 8 in 2022Q3, then 6.

### 3.5 Variants (`comparator_corr_variants.csv`; gaps = Indian − Accenture, pp, pre / post / FY25–27)

| variant | rev pre | rev post | hc pre | hc post | rev 2016Q1–20Q1 | hc 2016Q1–20Q1 | n pre/post | rev gap | hc gap |
|--|--|--|--|--|--|--|--|--|--|
| a pilot | 0.90 | 0.58 | 0.83 | 0.33 | 0.13 | −0.09 | 23/14 | −1.08 / −1.58 / −2.40 | −1.65 / −2.61 / −1.81 |
| a2 no 2022Q3 triple count | 0.90 | 0.58 | 0.83 | 0.33 | 0.13 | −0.09 | 23/14 | −1.08 / −1.58 / −2.40 | −1.68 / −2.61 / −1.81 |
| b Nov→next Q1 (0 months overlap) | 0.87 | 0.60 | 0.79 | 0.41 | 0.49 | −0.09 | 23/14 | −1.20 / −2.37 / −2.08 | −2.10 / −3.18 / −1.76 |
| b2 Nov→Q3 (1 month overlap) | 0.84 | 0.42 | 0.69 | 0.12 | 0.13 | −0.21 | 23/13 | −0.18 / −1.26 / −2.94 | −0.63 / −2.45 / −1.83 |
| f month-weighted Indian (⅔ t + ⅓ t−1) | 0.91 | 0.60 | 0.80 | 0.32 | 0.03 | −0.10 | 23/14 | −1.00 / −1.36 / −2.49 | −1.60 / −2.35 / −1.99 |
| c annual, calendar year | 0.94 | −0.51 | 0.88 | −0.24 | – | – | 5/3 | −0.71 / −1.71 | −1.36 / −3.32 |
| c2 annual, Indian FY | 0.88 | 0.35 | 0.62 | 0.19 | – | – | 5/3 | −0.38 / −1.89 | −0.85 / −3.08 |
| d mean | 0.94 | 0.64 | 0.83 | 0.36 | 0.29 | −0.31 | 23/14 | −0.45 / −2.24 / −2.76 | −1.22 / −2.87 / −2.22 |
| e revenue-weighted mean | 0.90 | 0.54 | 0.79 | 0.44 | 0.18 | −0.29 | 23/14 | −1.40 / −2.11 / −2.94 | −2.02 / −2.97 / −2.75 |
| g one LTI entity, median | 0.90 | 0.58 | 0.80 | 0.33 | 0.13 | −0.27 | 23/14 | −1.08 / −1.58 / −2.40 | −1.94 / −2.61 / −1.81 |
| h clean (a2 + f) | 0.91 | 0.60 | 0.81 | 0.32 | 0.03 | −0.10 | 23/14 | −1.00 / −1.36 / −2.49 | −1.63 / −2.35 / −1.99 |

Cognizant (quarters align exactly; cc starts 2017 so pre n = 19): pilot 0.35 / −0.02 (rev), 0.52 / 0.52 (hc); mean 0.42 / 0.16, 0.47 / 0.53; revenue-weighted 0.35 / −0.03, 0.63 / 0.47. Cognizant 2024Q4–2025Q2 includes ~4pp from Belcan.

### 3.6 Verdict
- The Accenture mapping is not wrong (Nov→Q4 gives the maximum 2-of-3-month overlap); no `cal_q` correction needed. Headline direction holds; magnitudes move ±0.1–0.2.
- Interpretation caveats: the pre-2023 correlation is a one-episode artefact (2016Q1–2020Q1: 0.13 revenue, −0.09 headcount). Bartlett effective n ≈ 4–5; 95% CI roughly [0.0, 0.99] for 0.90 and [−0.55, 0.96] for 0.58 — statistically indistinguishable. Within FY25–27 alone the correlations are 0.05 and −0.10.
- The FY25–27 gap of −2.4 to −2.9pp coincides with Accenture's FY25 inorganic guidance ("a bit more than 3%", ~4% H1 / ~2% H2, Q4FY24 and Q1FY25 calls; ~1.5% for FY26, Q4FY25 call). Guidance, not realized; growth is never adjusted for acquisitions (D12).

## 4. Is 2023 missing?
Files: `episode_row_quarter_map.csv`, `episode_row_fy_counts.csv`, `episodes_relabelled.csv`, `episodes_fiscal.csv`, `latest_quarter_by_firm.csv`.

### 4.1 Coverage of each REPORT row

| REPORT row | calendar | Indian FY quarters | quarters per FY | Accenture's own labels |
|--|--|--|--|--|
| 2015–22 ex-COVID | 2015Q2–2022Q4 excl. 2020Q2–21Q2 | Q1FY16–Q3FY23 | FY16–20: 4 each; FY22: 3; **FY23: 3** | Q3FY15–Q1FY23 |
| pre-COVID "2015–19" | 2015Q2–**2020Q1** | Q1FY16–Q4FY20 | 4 each | Q3FY15–Q2FY20 |
| COVID | 2020Q2–Q4 | Q1–Q3FY21 | 3 | Q3FY20–Q1FY21 |
| "FY24 slowdown" | 2023Q1–2024Q1 | **Q4FY23**–Q4FY24 | **FY23: 1**, FY24: 4 | Q2FY23–Q2FY24 |
| "FY25–27" | 2024Q2–2026Q2 | Q1FY25–Q1FY27 | FY25: 4, FY26: 4, **FY27: 1** | Q3FY24–Q3FY26 |

- FY23 is split 3 + 1 between the baseline row and the FY24 row; no row shows it alone. Labels mix calendar and fiscal years (`common.py`: "FY2023-24 slowdown"; REPORT: "FY24"). 2021Q1–Q2 fall in no row. Only overlap: pre-COVID inside 2015–22.
- Every firm's latest quarter is 2026Q2 (Indian Q1FY27, Accenture Q3FY26, Cognizant 2026Q2). Accenture Q4FY26 (released 1 Oct 2026) is not in the data.

### 4.2 How the 2015–22 and pre-COVID rows were made
No saved script produces them. They reproduce only as a mean of firm-means over all 8 Indian entities, including LTIM (whose window is only its 2022Q2–Q4 boom quarters; gR has one quarter), LTI, and Mindtree (one gR quarter). Consequence: published rev/employee (0.9) ≠ revenue − headcount (12.2 − 11.8 = 0.4).

### 4.3 Recomputed rows: pilot set vs clean 6-entity set (LTI group as one entity)

| row | Indian FY | set | rev cc | heads | rev/emp | Δutil | resid |
|--|--|--|--|--|--|--|--|
| 2015–22 ex-COVID | Q1FY16–Q3FY23 | pilot | 12.2 | 11.8 | 0.9 | 0.2 | 2.0 |
| 2015–22 ex-COVID | Q1FY16–Q3FY23 | clean6 | 11.7 | 9.9 | 1.0 | 0.3 | 2.1 |
| pre-COVID | Q1FY16–Q4FY20 | pilot | 9.9 | 7.0 | 1.7 | 1.1 | 1.6 |
| pre-COVID | Q1FY16–Q4FY20 | clean6 | 9.5 | 6.7 | 1.8 | 0.9 | 1.8 |
| COVID | Q1–Q3FY21 | pilot | 0.6 | 2.5 | −1.8 | 2.2 | −2.2 |
| COVID | Q1–Q3FY21 | clean6 | 0.6 | 2.2 | −1.6 | 2.0 | −1.9 |
| FY24 slowdown | Q4FY23–Q4FY24 | both | 2.4 | −1.8 | 4.2 | 1.5 | 2.9 |
| FY25–27 | Q1FY25–Q1FY27 | both | 2.2 | 0.7 | 1.5 | 0.1 | 1.0 |

### 4.4 Indian fiscal-year windows (clean6)

| window | rev | heads | rev/emp | Δutil | resid | Accenture rev / heads | Cognizant rev / heads |
|--|--|--|--|--|--|--|--|
| FY16–FY22 ex-COVID | 11.1 | 8.8 | 1.4 | 0.8 | 1.9 | 10.6 / 11.1 | 8.0 / 7.9 |
| **FY23** | **13.7** | **14.3** | −0.6 | −4.0 | 2.8 | 16.6 / 12.8 | 5.0 / 8.1 |
| FY24 | 0.7 | **−3.6** | **4.4** | 2.5 | 2.3 | 2.4 / 1.5 | −1.0 / −0.9 |
| FY25 | 2.6 | 0.1 | 2.6 | 1.1 | 1.1 | 5.4 / 5.7 | 4.1 / −2.5 |
| FY26 | 1.4 | 1.2 | 0.2 | −0.7 | 0.6 | 5.0 / 0.5 | 5.2 / 3.9 |
| Q1FY27 | 3.6 | 1.0 | 2.6 | −0.4 | 2.1 | 3.0 / 1.0 | 4.0 / 3.7 |

FY23 is the end of the boom (firm headcount growth fell from 18–28% in Q1FY23 to 1–9% in Q4FY23). FY24 alone is sharper than the REPORT row (headcount −3.6% vs −1.8%). The baseline FY25–27 is compared against shrinks (revenue gap ≈ 9.5pp, not ≈ 10).

## 6. Structural breaks
Files: `structural_breaks_jumps.csv`, `ltim_switch_check.csv`, `hcl_divestiture_check.csv`.

- **LTI–Mindtree merger.** No splice. LTI and Mindtree run to 2022Q3; LTIM restated series starts 2021Q2, its `gL` 2022Q2, `gR` 2022Q4. In 2022Q3 the comparator headcount median counts all three (median 17.1 → 17.8; correlation unchanged). No jump at the switch (LTIM restated YoY 21.5% vs LTI+Mindtree 21.3%); LTIM level is 2.5–2.8% below the standalone sum, but YoY is within series. Part 3/4 calibration drops `ltim` up to 2022Q4 — no double count there. The problem is the triple count in the REPORT's 2015–22 row.
- **HCLTech FY change.** Handled correctly via `period_end`.
- **HCLTech divestiture (D10).** 7,398 subtracted from the base for exactly 2024Q2–2025Q1 (adjusted `gL` 1.5 / 2.3 / 1.6 / 1.5 vs −1.8 / −1.1 / −1.8 / −1.8 unadjusted). Revenue not adjusted (Q4FY25 release p15: "Financial Services includes the impact of a divestiture in Q2 FY25"), so `gRPE` is biased down 2024Q3–2025Q2. Flagged.
- **Wipro.** Q4FY17 definition change: only the new series used, no YoY spans it — OK. Q2FY19 Alight deal: ~9,000 employees transferred ("no inorganic component … About 9000 employees come for the large deal", Q2FY19 call p15), adding ~5pp to `gL` for 4 quarters — flagged. Capco (Q1FY22) not adjusted (D12).
- **Inorganic growth not adjusted (D12):** HCLTech IBM products deal (`gR` 15.7–18.6 in 2019Q2–Q4; Q1FY20 release p3/p7, Q2FY20 release p6); Cognizant Belcan (~4pp; 8-K Ex.99.2 Q2 2025 fn 1); Cognizant TriZetto ($169.0m in Q1 2015, 10-Q; affects only `gR_usd`, `gL`); TechM Q2FY22 +14,930 heads in the quarter (acquired headcount not quantified).
- **Other.** TCS: no breaks. Infosys: no level jumps outside 2021–22. Accenture ASC 606: `gR` (cc) fine; `gR_usd` FY18 overstated by 3.3–3.7pp — corrected. Accenture 2015 `gL` 15.6%: organic per 10-Q MD&A. LTI 2017–20: smooth, organic. Mindtree 2015Q3 jump: unverified (scanned filings unreadable).
- **Verdict.** Adequate: headcount-side handling and HCLTech FY change. Weak: LTI business counted multiple times in the REPORT baseline row; inorganic growth adjusted nowhere (biases the comparator gap and the pre-COVID baseline); HCLTech divestiture removed from headcount but not revenue.

## 7. Corrected-data pipeline (`scripts/audit/build_corrected.py`)
- Imports `01_build_tidy` via importlib (no edits to pilot code). Reads `audit/corrections_*.csv`.
- Levels (optional `level` column overrides auto choice): **raw** (`column` is a raw metric; changes every matching vintage before vintage selection; optional filters `fiscal_q`, `unit`, `basis`, `period_type`, `doc_date`); **core** (`column` is a `core_quarterly` column; sets value and `_src`, recomputes `subcon_share` and YoY); **yoy** (column only in `yoy_metrics`; applied last; recomputes `gRPE`, `resid`).
- `old_value` must match the data to its written precision, else `AssertionError` and nothing is written. Duplicates across files applied once, logged `duplicate`. Accepts 1a notation (`metric (raw, basis=…)`, `cal_q` ranges `A..B`, `;`-lists for flag-only rows).
- Outputs: `core_quarterly_corrected.csv`, `yoy_metrics_corrected.csv`, `CHANGELOG.csv`, and an alternative (not a correction) `yoy_metrics_corrected_alt_ltimchain.csv`. No alternative-alignment file (the pilot mapping is already the best available).
- Checks: with no corrections both outputs are byte-identical to `data/tidy` (573,820 and 77,903 bytes). Tested all three levels and a deliberately wrong `old_value`.

### Corrections in `corrections_1b.csv` (generated by `make_corrections_1b.py`)
- Accenture `gR_usd` 2017Q4–2018Q3: 14.91 / 17.51 / 18.74 / 13.80 → 11.18 / 14.19 / 15.13 / 10.37 (log change in net revenues, current vs prior-year column of the same FY18 8-K Ex.99; the pilot divided an ASC 606 "revenues" level by a pre-606 "net revenues" level).
- 22 sign errors (16 Mindtree, 6 LTI Q1FY18) from a `(x.x)%` parser bug in `scripts/extract/ltim_parse_tables.py`, found by `ltim_sign_scan.py` checking 1,980 positive growth rows against the local PDFs (16 also found by 1a).
- 8 flag-only rows: Wipro Alight, HCLTech divestiture revenue, Cognizant Belcan.
