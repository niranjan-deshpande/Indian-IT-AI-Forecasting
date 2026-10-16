# Inventory: firm-level quarterly panel (top-6 Indian IT firms, Accenture, Cognizant, GFC backfill)

All figures below were computed with pandas from the repo files. Nothing in the repo was modified. Scratch scripts are in the session scratchpad only.

## 1. Which file is canonical

**Use `data/corrected/core_quarterly_final.csv` (levels) and `data/corrected/yoy_metrics_final.csv` (log YoY × 100).** Each has 591 rows and covers 10 entities: tcs, infosys, hcltech, wipro, techm, ltim, lti, mindtree, accenture, cognizant. The calendar runs 2007Q1–2026Q3, with a gap between roughly 2012Q2 and 2015Q1.
- They are built by `scripts/final/build_final_data.py`, described in `FINAL_PASS_SUMMARY.md` and dated 5 Oct 2026.
- Inputs are `data/raw/*.csv` and `gfc.csv`, except LTIM, which comes from `data/rebuilt/raw/ltim.csv` (re-extracted after fixing the "(x.x)%" sign-loss parser bug). Accenture Q4FY26 is added from `audit/new_raw_accenture_q4fy26.csv`.
- On top of that it applies the audit corrections and the final-pass decisions:
  - HCLTech divestiture: no adjustment to either revenue or headcount.
  - Wipro growth that spans a perimeter break is set to missing.
- Every change is logged in `data/corrected/CHANGELOG.csv`: 105 audit-round rows and 88 final-pass rows.

**Superseded files:**
- `data/tidy/core_quarterly.csv` and `yoy_metrics.csv`: the pilot versions, from before the audit.
- `data/corrected/*_corrected.csv`: the audit round. It still applies the HCL 7,398-person headcount add-back and lacks Accenture Q4FY26.
- `yoy_metrics_corrected_alt_ltimchain.csv`: an alternative with a chained LTI group. It is not canonical.

**Segment, people and deal detail exists only in `data/tidy/panel_long.csv`.** It has 36,654 rows: verticals, geographies, service lines, fresher hires, client buckets and so on, keeping the latest vintage. There is no "final" version of it. The audit fixes that would touch it are Mindtree and LTI segment-growth signs from 2017–22, which do not affect the recent window.

**Most of `output/` was built from the pre-audit tidy files by `scripts/03_part2.py`.** That includes the `cross_section_*`, `episode_*` and `india_vs_comparators` files. The fiscal-year tables in `output/final/table_A*.csv` and `table_B` are built from the final files.

`output/key_table_*`, `sim_*` and `voi_*` are simulation and detection-power outputs. They are not descriptive data and are not useful for a health check.

## 2. Variables and coverage

The table below covers `core_quarterly_final`, calendar quarters. Gaps of the form "2012Q2–2015Q1" are uncollected windows between the GFC file and the main collection. All Indian series end at **2026Q2 (Q1FY27)**. Accenture ends at **2026Q3 (its Q4FY26)**.

| variable | TCS | Infosys | HCLTech | Wipro | TechM | LTIM | Accenture | Cognizant |
|---|---|---|---|---|---|---|---|---|
| `rev_usd` | 07Q2– | 07Q1– | 07Q1– | **13Q2–** (IT Services segment only) | 07Q1–; gap 12Q2–15Q1 | 21Q2– | 07Q1–26Q3 | 07Q1– |
| `rev_cc_yoy` | **15Q2–** | 07Q2– | 07Q4– | 14Q2– | 16Q3–; gaps 17Q2–19Q1, 19Q4–20Q1 | **22Q4–** | 07Q1– (whole %) | **17Q1–** |
| `headcount` | 07Q1– | 07Q1– | 07Q1– | 07Q2–; gap 12Q2–15Q4 (new definition from 16Q1) | gap 12Q2–15Q1 | 21Q2– | 07Q3– | 07Q4– |
| `attrition` | 07Q1– | 10Q2– | 07Q1– | 13Q2– | patchy before 2015 | 21Q2– | 07Q1–26Q2 | 07Q1–; gap 12Q2–18Q4 |
| utilization (`util0`/`util1`) | **ends 15Q4** | 07Q1– (excl. trainees) | **13Q3–19Q1 only** | 07Q2– (excl. trainees; gap 07Q4–13Q1) | incl. trainees (excl. ends 25Q1) | 21Q2– (excl. trainees) | 08Q1– | offshore 17Q1–23Q4, then blended 23Q1– |
| `subcon_share` (% of revenue) | 11Q1–**26Q1** (break at Q1FY27) | 10Q2– | 16Q1– | 14Q2– | 15Q2– | **not in core** (FY22+ in `output/final/fig2_data.csv`) | — | — |
| `tcv_q` / `tcv_ttm` | 18Q2– | 15Q2– (large deals) | 21Q1– | 20Q4– (≥$30m large deals) | 18Q2– | 22Q4– | bookings 08Q3– | TTM bookings 20Q4– |

Pre-merger LTI and Mindtree run 2015Q2–2022Q3. Mindtree has almost no cc growth.

**In `panel_long` only:**

- **Mix shares by vertical and geography:** every firm through 2026Q2, including Cognizant from 2013Q4. Accenture reports segment levels and growth, not shares.
- **Service-line mix in the recent window:** only HCLTech (ITBS / ER&D / HCLSoftware), TechM (IT/BPS, INR segment revenue), Accenture (Consulting / Managed Services) and Cognizant (2 lines). TCS stops at 17Q1, Infosys at 23Q1, Wipro at 23Q1; LTIM never reported one.
- **Fresher hires:** effectively HCLTech only, quarterly 2021Q3–2026Q2. TCS has 2011–17.
- **Net additions:** TCS to 2025Q2, HCLTech 2019Q2–, Cognizant.
- **Other metrics:** client buckets (all Indian firms), offshore effort share (Infosys, LTIM), fixed-price share (Wipro), employee cost (TCS, HCL, TechM, Wipro), AI disclosures (1–10 quarters per firm).
- **Revenue per employee:** not stored. It has to be derived (`gRPE` = gR − gL in the yoy file).

## 3. Headline current-state facts

**Revenue (USD, sum of levels; LTI group = LTIM).**
- Top-6 quarterly revenue was **$21.85bn in 2026Q2, +3.0% YoY**. 2026Q1 was +4.2%.
- By firm, 2026Q2 YoY in USD:

| LTIM | TechM | HCL | Infosys | TCS | Wipro IT Services |
|---|---|---|---|---|---|
| +6.1% | +6.1% | +3.0% | +2.9% | +2.7% | +1.1% |

- **Fiscal-year top-6 revenue:**

| FY | revenue | growth |
|---|---|---|
| FY23 | $80.67bn | +10.0% |
| FY24 | $82.28bn | +2.0% |
| FY25 | $84.56bn | +2.8% |
| FY26 | $86.46bn | +2.2% |

- FY26 USD growth by firm: HCL +6.0%, LTIM +6.0%, Infosys +4.6%, TechM +1.9%, Wipro −0.3%, **TCS −0.5%**.

**Constant currency** (`output/final/table_A.md`, log growth):
- FY26 cc growth was **+0.6 revenue-weighted** (+1.4 simple). FY25 was +3.2 and FY24 +1.5.
- Q1FY27 alone: +3.0 weighted.
- FY26 cc by firm:

| LTIM | HCL | Infosys | TechM | Wipro | TCS |
|---|---|---|---|---|---|
| +5.1 | +3.8 | +3.1 | +0.6 | −1.6 | −2.4 |

- Latest quarter (2026Q2), firm-reported cc YoY:

| TechM | LTIM | TCS | HCL | Infosys | Wipro |
|---|---|---|---|---|---|
| 6.6 | 6.4 | 3.2 | 2.6 | 2.4 | 0.9 |

- TCS was negative for 2025Q2–2026Q1, at −3.1, −3.3, −2.6 and −0.6.

**Headcount.**
- Top-6 headcount was **1,623,439 at 2026Q2, against a peak of 1,694,188 at 2022Q3** (−70,749, −4.2%). YoY it is −0.1%.
- Change from each firm's peak:

| firm | peak | change from peak |
|---|---|---|
| TechM | 2022Q3 | −10.5% |
| Wipro | 2022Q3 | −7.5% |
| Infosys | 2022Q4 | −5.4% |
| TCS | 2022Q3 | −3.6% (−22,373) |
| HCL | 2024Q1 | −1.6% |
| LTIM | 2025Q4 | −0.1% (at peak) |

- TCS is down 3.1% YoY at 2026Q2.
- March fiscal-year-end totals (`data/explore/round3/gcc/top6_headcount_fy.csv`):

| FY23 | FY24 | FY25 | FY26 |
|---|---|---|---|
| 1,679,489 | 1,605,986 | 1,621,361 | 1,618,023 |

**Revenue per employee** (annualised quarterly USD revenue ÷ end-of-quarter headcount).
- Top-6: $48.6k (2022Q4) → $51.4k (2024Q1) → **$53.8k (2026Q2)**. The pre-COVID level was $52.0k in 2019Q1.
- By firm at 2026Q2: HCL 65.2, Infosys 62.0, LTIM 55.7, TCS 51.4, TechM 45.3, Wipro 43.0. Wipro is understated because its numerator is IT Services revenue and its denominator is company-wide headcount.
- Revenue per employee in cc, revenue-weighted (log growth): FY24 +4.4, FY25 +4.0, FY26 +0.0.

**Utilization** (only within-firm comparisons are valid):

| firm | 2026Q2 | 2016–19 mean | peak |
|---|---|---|---|
| Infosys | 84.9 | 83.4 | 89.2 (21Q3) |
| Wipro | 83.6 | 82.7 | 89.2 (21Q3) |
| TechM (incl. trainees) | 87.0 | 80.3 | 88.0 |
| LTIM | 86.4 | — | 88.3 (24Q2) |
| Accenture | 93 | 91.2 | — |
| Cognizant (blended) | 85 | — | — |

TCS and HCL have no recent utilization data.

**Attrition (LTM; definitions differ).**
- At 2026Q2 the Indian firms sit at **11.8–13.9%**: TechM 11.8, HCL 12.7, Infosys 13.0, LTIM 13.3, TCS 13.6, Wipro 13.9.
- 2022Q2–Q3 peaks were 21.5–28.4.
- Most firms are below their 2016–19 means: Infosys 20.3, TechM 19.1, HCL 16.9, Wipro 16.7. TCS is the exception, above its 11.6 mean.

**Comparators.**
- Indian fiscal-year aligned, FY26: Accenture cc +5.0 with headcount +0.5; Cognizant cc +5.2 with headcount +3.9. The Indian weighted average was cc +0.6 with headcount +0.6.
- Accenture's latest quarter (Q4FY26) was cc +7%, with headcount of 814,000.
- At 2026Q2, Cognizant cc was +4.1%, and USD revenue growth was Accenture +5.6% and Cognizant +4.5%, against +3.0% for the top-6.
- `output/india_vs_comparators.csv`: the correlation of Indian and Accenture cc growth was 0.90 before 2023 (2016–22 ex-COVID) and 0.58 for 2023Q1–2026Q2. The mean gap over 2023Q1–2026Q2 is −1.6 pp (revenue) and −2.6 pp (headcount). The audit calls these correlations fragile, driven by the 2021–22 boom, and notes the gap is partly Accenture's inorganic growth.

**Mid-tier** (`data/explore/midtier/midtier_vs_top6.csv`: Persistent, Coforge, Mphasis, plus Hexaware on a calendar year).

| | FY24 | FY25 | FY26 |
|---|---|---|---|
| Mid-4 revenue growth (log) | 4.96 | 14.65 | 13.92 |
| Top-6 revenue growth (log) | 1.98 | 2.74 | 2.22 |

- The mid-4 share of combined revenue rose from 4.0% (FY20) to 7.3% (FY26).
- Caveats: Coforge's figures include acquisitions (Cigniti in FY25, then an AdvantageGo carve-out), and Mphasis headcount includes contractors.
- `vertical_mix_midtier.csv` gives FY26 financial-services shares: Mphasis about 67% (BFS + Insurance), Persistent 34.6% BFSI, Coforge 41.5% (BFS + Insurance).

**Verticals and geographies** (`output/cross_section_*`: mean segment YoY for 2024Q2–2026Q2 against 2017Q1–2019Q4; cc where reported).
- **Financial services:** recent growth of TCS 1.0, Infosys 4.6, HCL 3.3, Wipro −0.6, TechM 4.5, LTIM 3.4. That is a slowdown of 4.7–12 pp, while Accenture (6.1, +0.4) and Cognizant (5.7, +2.3) accelerated.
- **North America vs Europe:**

| | TCS | Infosys | HCL | Wipro | TechM | LTIM | Accenture | Cognizant |
|---|---|---|---|---|---|---|---|---|
| North America | −0.5 | 1.0 | 3.8 | 0.3 | −0.4 | 5.5 | 5.7 | 5.9 |
| Europe | 0.6 | 9.4 | 5.9 | −5.4 | 5.4 | 5.0 | 3.7 | 0.8 |

- `cross_section_variance_shares.csv`: firm effects explain about 41% / 39% of the cross-firm variance in recent vertical / geography growth. Vertical or region groups explain only 2% / 6%. **The weakness is firm-specific, not concentrated in particular verticals or regions.**
- Latest North America share: TCS 48.3, Infosys 56.4, HCL (USA) 56.0, Wipro (Americas 1+2) 60.6, TechM 48.6, LTIM 73.9, Cognizant 75.3. Latest BFSI share: TCS 32.1, Infosys 27.9, HCL 22.1, Wipro 34.1, TechM 16.7, LTIM 34.0.

**Subcontracting share of revenue** (`output/final/fig2_data.csv`).
- It fell at all six firms from FY23 to FY24–25 (TCS 9.5 → 4.6; TechM 15.0 → 11.0). It **rose again in FY26 at 5 of 6**: TCS 5.5, Infosys 8.6, HCL 14.2, Wipro 11.6, LTIM 7.65. TechM went to 10.7.
- HCL reached 14.8 in 2026Q2.

**Fresher hiring (HCL only).** Quarterly hires were 10,339 in 2022Q3 and **1,056 in 2026Q2**, the lowest in the series.

**Deal value, trailing 12 months.** These cannot be compared across firms.
- 2026Q2 against 2025Q2: TCS $40.8bn vs $40.4bn; Infosys large deals $14.7bn vs $11.3bn; HCL $9.9bn vs $9.1bn; TechM $4.1bn vs $3.0bn; LTIM $6.65bn vs $6.21bn; Wipro large deals $6.8bn vs $6.9bn.
- Comparators: Accenture bookings $84.5bn, Cognizant $29.1bn.

**GFC backfill.**
- USD YoY troughs: Infosys −5.2 (2009Q3), TCS −5.7 (2009Q1), TechM −19.8, Accenture −17.1. HCL stayed positive and Cognizant stayed above +12.
- Headcount growth never went negative at TCS, Infosys or HCL; Accenture fell to −6.1.
- Data are in `core_quarterly_final` 2007Q1–2012Q1 and `output/episode_summary.csv`.

## 4. Data quality issues

- **LTI group.** LTIM's restated history starts in Q1FY22. Its headcount is 2.6–2.8% below LTI + Mindtree, which is unexplained (`audit/ltim_switch_check.csv`). There is no level splice. The final tables use LTI + Mindtree through FY22 and LTIM after. LTIM cc YoY starts only in 2022Q4. The older pilot and REPORT baseline counted the LTI business up to three times; that has been corrected.
- **HCLTech.**
  - Its fiscal year ended in June until FY15, and FY16 was a 9-month year. The data are mapped by `period_end`, which is correct.
  - The Q1FY25 divestiture removed 7,398 staff. The final files do **not** adjust for it, so FY25 HCL headcount growth is −1.6 rather than +1.7. Revenue is not adjusted either, because the divested revenue was not disclosed.
  - Utilization stops after 2019Q1. HCL also has software products (HCLSoftware) inside its revenue.
- **Wipro.**
  - Revenue is the IT Services segment while headcount is company-wide. The headcount definition changed at Q4FY17, and only the new series from 2016Q1 is used.
  - Growth windows that span the ISRE perimeter change (2017Q2–18Q1) and the Alight transfer (about 9,000 staff, Q2FY19) are set to missing.
  - The current headcount is not reconciled to Wipro's own BRSR.
- **TCS.**
  - No utilization after 2015Q4. The subcontracting line moves to an expense-by-nature definition at Q1FY27, so 2026Q2 is missing.
  - TCS's subcontracting figure is in USD, while the other firms' are in INR.
  - In the GFC window, TCS "reported" growth is INR growth, and its 2007Q1 USD figure was removed as a convenience translation.
- **Cognizant.**
  - Utilization switches from offshore to blended in 2023–24. Attrition definitions change. The 2021Q2–Q3 attrition values were fixed.
  - Belcan adds about 4 pp to growth in 2024Q4–2025Q2 and is not adjusted.
- **Accenture.**
  - Its quarter ending in November maps to calendar Q4, so there is a 1-month offset; Indian-FY tables cover Mar–Feb. cc growth is printed in whole percents.
  - ASC 606 inflated FY18 USD growth; this is corrected. Acquisitions (guided at about 3% in FY25) are not adjusted.
- **Headcount definitions.** TCS, Infosys, HCL and LTIM report permanent employees only, excluding contractors. TechM includes direct contractors.
- **`panel_long` artefacts.**
  - TechM has duplicate vertical rows under different label spellings from different vintages, for example "BFSI" and "Banking, Financial services & Insurance" in the same quarter. This creates a double-count risk.
  - Infosys has hierarchical "Parent > Child" sub-segments.
  - HCL has two overlapping geography schemes in 2024Q2–2025Q1.
  - LTIM has a junk dimension "©LTM | Q1 FY27 Investor Release" in its geography rows.
  - **Shares must be mapped carefully across reorganizations.** My own naive mapping double-counted in several of these cases.
- `output/coverage_matrix.csv` lists Wipro revenue from 2007, but the core USD series (IT Services) starts in 2013Q2.
- No firm reports price or volume separately, and quantitative AI revenue covers only 1–4 quarters per firm.

## 5. Candidate charts

1. **Top-6 USD revenue and headcount levels, 2015–2026Q2,** with the 2022Q3 headcount peak marked. Source: `core_quarterly_final.csv` `rev_usd` and `headcount`, summed with the LTI-group rule.
2. **Fiscal-year cc revenue growth FY16–FY26 plus Q1FY27,** Indian weighted vs Accenture vs Cognizant. Source: `output/final/table_A.csv`, column "Revenue, constant currency".
3. **Firm small multiples of quarterly cc YoY, 2022–2026Q2,** which would show TCS turning negative and LTIM and TechM recovering. Source: `yoy_metrics_final.csv` `gR`, or `figures/task2/plotted_series_02_revenue_cc.csv`.
4. **Headcount change from each firm's peak (bar chart).** Source: `core_quarterly_final.csv` `headcount`.
5. **FY-end top-6 headcount FY16–FY26.** Source: `data/explore/round3/gcc/top6_headcount_fy.csv`, columns `top6` and the per-firm columns.
6. **Revenue per employee (USD k), top-6 and by firm.** Derived as `rev_usd`×4/`headcount`. Alternatively use the growth form in `figures/task2/plotted_series_04_revenue_per_employee.csv` (`gRPE_usd`).
7. **Utilization by firm, 2016–2026,** shaded against each firm's 2016–19 mean. Source: `core_quarterly_final.csv` `util0` (and `util1` for Cognizant); within-firm only.
8. **Attrition 2016–2026 by firm,** showing the 2022 spike and today's normalisation. Source: `core_quarterly_final.csv` `attrition`.
9. **Indian average minus Accenture gap,** revenue cc and headcount. Source: `figures/task2/plotted_series_07_gap_vs_accenture.csv` (`gap`, `metric`, `freq`, `avg`).
10. **Mid-tier vs top-6 revenue growth FY20–FY26** plus the mid-tier revenue share. Source: `data/explore/midtier/midtier_vs_top6.csv`, columns `top6_rev_growth_logx100`, `mid4_rev_growth_logx100`, `mid4_rev_share_pct`.
11. **Financial-services growth, recent vs 2017–19, by firm** (dumbbell chart). Source: `output/cross_section_verticals.csv` (`recent`, `base`, `grp`=='FS').
12. **North America vs Europe recent growth by firm.** Source: `output/cross_section_geographies.csv`. Note that the NA label reads as NaN in pandas; use `keep_default_na=False`.
13. **Subcontracting share of revenue FY20–FY26.** Source: `output/final/fig2_data.csv`.
14. **HCL fresher hires per quarter, 2021Q3–2026Q2.** Source: `panel_long.csv` `metric=='fresher_hires'`, `firm=='hcltech'`, `period_type=='quarter'`.
15. **GFC vs now** (USD revenue YoY and headcount YoY, 2008–10 vs 2023–26). Source: `yoy_metrics_final.csv` `gR_usd` and `gL`, or `output/episode_summary.csv`.

`data/sources/` is about 6.9 GB, untracked and git-ignored. It holds per-firm folders (accenture, cognizant, hcltech, infosys, ltim, tcs, techm, wipro), plus `gfc/` (3,714 files: Wayback HTML/PDF copies, OCR text, jsonl), `midtier/` (factsheet PDFs) and `plfs/` (.dta/parquet microdata). The document types are IR fact sheets and earnings releases (PDF), the `.txt` extracted from them, SEC EDGAR filings (htm), NSE/SEBI results PDFs, TechM xlsx datasheets, and Cognizant slide images (jpg).