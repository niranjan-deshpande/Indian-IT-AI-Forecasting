# Data audit (follow-up Task 1)

*Date: 2026-10-05. Detailed findings: `audit/findings_1a.md` (items 1, 2, 5) and `audit/findings_1b.md` (items 3, 4, 6, pipeline). Row-level evidence: `audit/*.csv`. No existing file was modified. Corrected data are written to new files in `data/corrected/`.*

## Summary

1. **Spot-check: 30 of 30 values match the primary documents.** 18 were checked against freshly downloaded copies, which were byte- or text-identical to the cached files.
   - Targeted tests outside the sample found **two parser bugs**:
     - Mindtree and LTI negatives printed as "(x.x)%" were stored as positive: 22 cells, 2 of which reach a core column.
     - Cognizant attrition definitions were picked arbitrarily in 2 quarters.
   - None of the errors touch `gR` (cc revenue growth), `gL` or `du` in 2015–2026. **The pilot's Part 2–4 numbers are unchanged by the corrections.**
2. **Currency and units are consistent from 2015 on.** Revenue is reported USD throughout. cc growth is never mixed with reported growth: `gR` has no fallback. Three problems:
   - Accenture FY18 `gR_usd` was inflated by about 3.5 pp by an ASC 606 basis mix. Corrected.
   - Two GFC-era base values were not comparable. Set to missing.
   - Some GFC-era "reported" growth is INR growth. Flagged.
3. **Fiscal-year alignment was not wrong.** Every `cal_q` matches its `period_end`. Mapping Accenture's quarter ending Nov-30 to calendar Q4 is the best alignment available (2 of 3 months overlap).
   - The comparator correlations reproduce exactly (0.90 / 0.58 revenue, 0.83 / 0.33 headcount). Across 11 alignment and aggregation variants they move by about ±0.1–0.2; the cleanest variant gives 0.91 / 0.60 / 0.81 / 0.32.
   - **The bigger issue is interpretation.** Over 2016Q1–2020Q1 the correlations are only 0.13 (revenue) and −0.09 (headcount). The pre-2023 figure comes from the 2021–22 boom. With an effective n of about 5, 0.90 and 0.58 cannot be told apart statistically.
4. **2023 is not missing; it is split across rows and mislabelled.** Q1–Q3FY23 sit in "2015–22" and Q4FY23 in "FY24 slowdown". The labels mix calendar and fiscal years. **"FY25–27" contains 9 quarters: FY25 ×4, FY26 ×4, FY27 ×1 (Q1FY27).**
   - The "2015–22" row also counts the LTI business up to three times (LTI, Mindtree, LTIMindtree). With one LTI entity, baseline headcount growth is 9.9%, not 11.8%.
5. **Headcount excludes contractors at TCS, Infosys, HCLTech and LTIMindtree.** At these four, the fact-sheet figure equals the BRSR "Permanent" row.
   - Tech Mahindra includes directly contracted staff and non-integrated subsidiaries.
   - Wipro's pre-FY18 "Head Count" included contractors and retainers. The repo correctly uses only the later "Employee Count" series. Wipro's current count is not reconciled to its own BRSR.
   - Trainees are explicitly included only at Infosys; at the other firms it is not stated.
6. **Structural-break handling is adequate for headcount but incomplete elsewhere:**
   - The LTI business is counted multiple times in the REPORT's baseline row.
   - Inorganic growth is adjusted nowhere (Belcan, Accenture acquisitions, HCLTech–IBM, Wipro–Alight).
   - The HCLTech divestiture is removed from headcount but not from revenue.
   - Two Wipro breaks were not logged: the ISRE perimeter (FY17 base) and the Alight transfer (Q2FY19, about 9,000 staff).

## 1. Spot-check (`audit/spotcheck_1a.csv`)

**Design.** Seed 20261005. 26 cells were drawn from the vintages actually used (`panel_long.csv`, 2015Q2 onward), stratified across all 8 firms plus LTI and Mindtree, and across six metric groups: revenue USD, headcount, utilization, attrition, vertical share and cc growth. 4 more cells came from the GFC file.

**Results.**

| metric group | n | match | checked against live or Wayback copy |
|--|--|--|--|
| revenue USD | 6 | 6 | 5 |
| headcount | 7 | 7 | 4 |
| utilization | 7 | 7 | 3 |
| attrition | 5 | 5 | 2 |
| vertical share | 3 | 3 | 0 |
| cc YoY growth | 3 | 3 | 3 |
| **total** | **30** | **30** | **18** |

- Each value was read from the document itself, not from the CSV. The table with value in repo, value in source, source location and result is `audit/spotcheck_1a.csv`.
- **Propagation:** 27 of the cells feed `core_quarterly.csv`, and all arrive unchanged. The one exception is a deliberate preference for Cognizant's Tech Services attrition series.
- **Coverage gap:** TCS 2015+ fact sheets could be checked only against the local cache, because tcs.com returns 403 and Wayback rate-limited.

**Systematic problems found by targeted tests** (rows T01–T08):
- **Sign loss for negatives printed as "(x.x)%".**
  - Mindtree: 16 cells. Two of them are total YoY growth in Q2FY21 and Q3FY21, which feed core `rev_rep_yoy`.
  - LTI: 6 cells (Q1FY18 segment growth), found by Task 1b's scan of 1,980 positive rows against the PDFs.
  - Cause: `parse_num` in `scripts/extract/ltim_parse_tables.py`. LTIM rows are unaffected.
  - Because Mindtree has only one cc-growth quarter, `gR` is unaffected.
- **Cognizant attrition 2021Q2–Q3.** `pick()` chose quarterly-annualized rates (29, 33) where the neighbouring quarters use TTM (18, 24). It is the only ambiguous pick in any core column.

## 2. Currency and units (`audit/findings_1a.md` §2)

- **Revenue USD:**
  - Reported USD for every firm-quarter from 2015.
  - Wipro is the IT Services segment only, and 2007–12 is missing.
  - TCS 2007Q1 is an INR convenience translation at Rs 43.47 per USD: set to missing.
  - Accenture FY18 quarters come from the ASC 606 restated vintage, while FY17 is on the old net-revenue basis. That inflates `gR_usd` for 2017Q4–2018Q3 by 3.3–3.7 pp. Corrected using the like-for-like growth printed in the FY18 releases.
- **Constant currency:**
  - Every `rev_cc_yoy` value comes from a `basis=cc` row. `gR` is cc only and missing elsewhere: it never falls back to USD growth (DECISIONS D18).
  - Infosys, Wipro, Cognizant and Accenture all define cc as current-period revenue at prior-period FX rates. Accenture calls it "local currency" and prints whole percents, so there is ±0.5 pp of rounding.
  - TCS, HCLTech, TechM and LTIM print no definition in the documents checked.
- **Mislabelled basis:** GFC-era `rev_rep_yoy` for TCS (2007Q1–2010Q2) and TechM (2007–12) is INR growth. Flagged; it is not used in Parts 2–4.
- **Units:**
  - Revenue, headcount, utilization and TCV are consistent once the build script's conversions are applied (INR crore→mn, USD bn→mn).
  - TCS `subcon` is USD, unlike the other firms (INR). Its share uses a USD denominator, so the ratio is still correct.
- **Utilization definitions differ by firm** (including vs excluding trainees, offshore vs blended). The audit confirms that only within-firm changes (`du`) are used.

## 3. Fiscal-year alignment (`audit/findings_1b.md` §3; `audit/fiscal_calendar.csv`, `comparator_corr_variants.csv`)

| firm | FY end | quarter ends |
|--|--|--|
| TCS, Infosys, Wipro, TechM, LTIM/LTI/Mindtree | 31 Mar | Jun, Sep, Dec, Mar |
| HCLTech | 30 Jun to FY15; FY16 = 9 months (Jul-15 to Mar-16); 31 Mar from FY17 | — |
| Accenture | 31 Aug | Nov, Feb, May, Aug |
| Cognizant | 31 Dec | Mar, Jun, Sep, Dec |

Each row is cited to a primary filing in `fiscal_calendar.csv`.

**Mapping checks.**
- `cal_q` is the calendar quarter containing `period_end` for every firm. Checks found 0 inconsistencies, 0 duplicates, and no holes at HCLTech's transition year.
- The pilot uses the firm-reported same-fiscal-quarter cc growth, and computes other growth as 4 calendar quarters back. The two coincide.

**Comparator correlations, Indian aggregate vs Accenture** (pre = 2016Q1–2022Q4 excluding COVID quarters; post = 2023Q1–2026Q2).

| variant | revenue pre | revenue post | headcount pre | headcount post |
|--|--|--|--|--|
| pilot (median; Nov→Q4) | 0.90 | 0.58 | 0.83 | 0.33 |
| Accenture Nov→next Q1 (0 months overlap) | 0.87 | 0.60 | 0.79 | 0.41 |
| Accenture Nov→Q3 (1 month overlap) | 0.84 | 0.42 | 0.69 | 0.12 |
| month-weighted Indian (⅔ t + ⅓ t−1) | 0.91 | 0.60 | 0.80 | 0.32 |
| mean instead of median | 0.94 | 0.64 | 0.83 | 0.36 |
| revenue-weighted mean | 0.90 | 0.54 | 0.79 | 0.44 |
| annual, calendar year (n = 5 / 3) | 0.94 | −0.51 | 0.88 | −0.24 |
| clean (no triple count, month-weighted) | 0.91 | 0.60 | 0.81 | 0.32 |
| *pilot set, 2016Q1–2020Q1 only* | *0.13* | — | *−0.09* | — |

**Verdict.**
- The periods were **not misaligned**, so the headline figures do not need to change.
- They are fragile, however:
  - The pre-2023 correlation is driven by the single 2021–22 boom-and-bust.
  - Within FY25–27 alone the correlations are 0.05 (revenue) and −0.10 (headcount).
  - The 95% confidence intervals overlap almost completely.
  - Task 2's 8-quarter rolling correlation shows the same thing: it is high only in windows that span 2020–24 (−0.08 in 2019Q4, 0.96 in 2022Q4, −0.05 in 2026Q2 for revenue).
- **The FY25–27 growth gap** (Indian minus Accenture, −2.4 to −2.9 pp for revenue) overlaps with Accenture's guided inorganic growth of "a bit more than 3%" in FY25 and about 1.5% in FY26. That is guidance, not realized growth; it comes from the Q4FY24, Q1FY25 and Q4FY25 calls. Growth is not adjusted for acquisitions in any series.

## 4. The "missing" 2023 (`audit/findings_1b.md` §4; `episodes_relabelled.csv`, `episodes_fiscal.csv`)

| REPORT row | calendar quarters | Indian FY quarters | quarters per FY |
|--|--|--|--|
| 2015–22 (ex-COVID) | 2015Q2–2022Q4, excl. 2020Q2–21Q2 | Q1FY16–Q3FY23 | FY23: 3 |
| pre-COVID "2015–19" | 2015Q2–**2020Q1** | Q1FY16–Q4FY20 | — |
| COVID | 2020Q2–Q4 | Q1–Q3FY21 | — |
| "FY24 slowdown" | 2023Q1–2024Q1 | **Q4FY23**–Q4FY24 | FY23: 1, FY24: 4 |
| "FY25–27" | 2024Q2–2026Q2 | Q1FY25–Q1FY27 | FY25: 4, FY26: 4, **FY27: 1** |

- **FY23 is split 3 + 1.** Calendar-year labels ("2015–22") and fiscal-year labels ("FY24") are mixed in one table.
- **Gaps and labels:** 2021Q1–Q2 fall in no row. The "2015–19" row actually runs to 2020Q1.
- **Latest quarter:** every firm ends at 2026Q2. Accenture's Q4FY26, released 1 Oct 2026, is not yet in the data.
- **Indian fiscal-year windows** (one LTI entity):
  - **FY23 on its own is the tail of the boom:** revenue +13.7%, headcount +14.3%.
  - **FY24 is sharper than the REPORT row:** headcount −3.6% against −1.8%, and revenue per employee +4.4%.
  - **Later years:** FY25 revenue +2.6% and headcount +0.1%; FY26 +1.4% and +1.2%.
- **No saved script produces the REPORT's 2015–22 and pre-COVID rows.** They reproduce only as a mean of firm-means over 8 Indian entities, which counts the LTI business up to three times. That is why revenue per employee (0.9) ≠ revenue − headcount (12.2 − 11.8).
- **Rows recomputed with one LTI entity:**
  - 2015–22: revenue 11.7, headcount 9.9, revenue per employee 1.0, Δutilization 0.3, residual 2.1.
  - pre-COVID: 9.5 / 6.7 / 1.8 / 0.9 / 1.8.
  - The FY24 and FY25–27 rows are unchanged.

## 5. Headcount definitions (`audit/findings_1a.md` §5)

| firm | trainees | contractors / subcontractors | changes over sample |
|--|--|--|--|
| TCS | not stated | **excluded**. Fact sheet 607,979 = BRSR permanent; 28,854 "other than permanent" (IAR 2024-25, p.131) | 2009Q1: e-Serve and Diligenta added (GFC window). None 2015–26 |
| Infosys | **included**. 20-F FY2016 and FY2026: "…including trainees" | **excluded**. 317,240 = BRSR permanent; 23,447 contractors excluded (IAR 2023-24, p.159) | wording only; trainee sub-line dropped after Q4FY18 |
| HCLTech | not stated | **excluded**. 223,420 = BRSR permanent = 167,316 company + 56,104 subsidiaries (AR 2024-25, pp.130, 187) | Q1FY25 divestiture of 7,398, correctly adjusted in `gL` |
| Wipro | not stated | pre-FY18 "Head Count" **included** contractors and retainers (181,482 vs 165,481 employees at Q4FY17; AR 2016-17, p.52). Current employee count 233,346 lies between BRSR permanent 225,306 and BRSR total 235,415: **unreconciled** | Q4FY17 switch (handled: the repo uses the employee count from Q4FY16). **Unlogged:** ISRE perimeter restated only back to Q1FY18 (biases `gL` 2017Q2–18Q1 by about −3 pp); Alight transfer of about 9,000 staff in Q2FY19. Q2FY25 restatement of Q3'24–Q1'25 (corrected values are in use) |
| TechM | not stated | **included** if contracted directly. 148,731 = BRSR 139,271 (incl. 7,827 contractors) + 9,460 non-integrated subsidiaries (IAR FY25, p.125) | label changes only |
| LTIMindtree | not stated | **excluded**. 84,307 permanent; 3,782 "Non-FTE Subcontractors" excluded (FY25 BRSR p.3) | merger restatement 1,858–2,335 below LTI + Mindtree, unexplained (no splice used) |
| Cognizant | not stated | excluded implicitly: "subcontractor usage has been immaterial" (10-K FY2025) | TriZetto (2014Q4), Belcan (2024Q3) |
| Accenture | not stated | not stated | none found |

**Implication.** The Indian headcount series measure permanent employees, so a shift from employees to contractors would show up as falling L. Task 4's subcontracting-cost series rules that out for FY24–FY26: subcontracting as a share of revenue *fell* at all six firms in FY24 (`discriminating_data.md` §b).

## 6. Structural breaks (`audit/findings_1b.md` §6)

| break | handling in pilot | verdict |
|--|--|--|
| LTI–Mindtree merger | no splice; LTI and Mindtree until 2022Q3, LTIM after; Parts 3–4 drop LTIM before 2022Q4 | correct in the model. **REPORT baseline row counts the LTI business up to three times.** The comparator median includes all three in 2022Q3 (no material effect) |
| HCLTech FY change | mapped through `period_end` | correct |
| HCLTech divestiture (Q1FY25) | headcount base reduced by 7,398 for 4 quarters | correct for `gL`. **Revenue not adjusted**, so `gRPE` is biased down 2024Q3–2025Q2 |
| Wipro Q4FY17 definition | new series only | correct |
| Wipro ISRE perimeter; Alight transfer | not logged | flagged |
| Inorganic growth (Belcan ~4 pp; Accenture acquisitions; HCLTech–IBM 2019; Capco; TriZetto) | not adjusted (D12) | biases the comparator gap and the baseline. Flagged, not corrected |
| Accenture ASC 606 | cc growth as reported | `gR` fine; `gR_usd` FY18 corrected |

## Corrections

Applied by `scripts/audit/build_corrected.py`. Every row is logged in `data/corrected/CHANGELOG.csv`, and every change was verified against a primary document.

| # | firm | quarters | field | old → new | reason |
|--|--|--|--|--|--|
| 1 | Mindtree | 16 cells: Q2–Q3FY17 QoQ, Q2–Q3FY21 YoY, 12 segment cells FY22–23 | raw growth rates | +x → −x | parser lost "(x.x)%" sign |
| 2 | Mindtree | 2020Q3, 2020Q4 | core `rev_rep_yoy` | 3.7 → −3.7; 0.4 → −0.4 | same bug, propagated to core |
| 3 | LTI | Q1FY18, 6 segment cells | raw growth rates | +x → −x | same bug |
| 4 | Cognizant | 2021Q2, 2021Q3 | core `attrition` | 29 → 18; 33 → 24 | definition mix (quarterly-annualized vs TTM) |
| 5 | TCS | 2007Q1 | core `rev_usd` | 1,183.9 → missing | INR convenience translation; removes the 2008Q1 `gR_usd` (24.8) |
| 6 | Wipro | 2007Q1 | core `headcount` | 67,818 → missing | old perimeter; removes the 2008Q1 `gL` (+34.3) |
| 7 | Accenture | 2017Q4–2018Q3 | yoy `gR_usd` | 14.91 / 17.51 / 18.74 / 13.80 → 11.18 / 14.19 / 15.13 / 10.37 | ASC 606 vintage mix; like-for-like net revenue growth from the FY18 releases |

**Flagged, not changed (57 rows):**
- Wipro ISRE perimeter (2017Q2–2018Q1)
- Wipro Alight (2018Q3)
- TCS e-Serve (2009Q1)
- GFC-era INR growth labelled "reported" (TCS, TechM)
- HCLTech divestiture effect on revenue
- Cognizant Belcan
- Accenture `rev_usd` FY18 levels

There are 18 duplicate rows, where 1a and 1b found the same error.

**Effect on pilot outputs.**
- Corrected `yoy_metrics` differs from the original in only 6 cells: 5 `gR_usd`, 1 `gL`. No `gR`, `du` or `resid` value changes.
- The Part 2 episode table and the comparator correlations are unchanged. The simulation inputs (`gR`, `gL`, `du`, `gTCV`, `dsub`) are also unchanged; the simulation was not re-run.

**Alternative, not a correction.** `data/corrected/yoy_metrics_corrected_alt_ltimchain.csv` adds a single LTI-group entity (`ltim_chain`), built from growth rates with no level splice.

## Files

- `data/corrected/core_quarterly_corrected.csv`, `yoy_metrics_corrected.csv`, `CHANGELOG.csv`, `yoy_metrics_corrected_alt_ltimchain.csv`
- Regenerate: `python scripts/audit/build_corrected.py`. It asserts each `old_value` before changing it. With no corrections, its output is byte-identical to `data/tidy`.
- Evidence: `audit/spotcheck_1a.csv`, `corrections_1a.csv`, `corrections_1b.csv`, `fiscal_calendar.csv`, `calq_mapping_check.csv`, `comparator_corr_variants.csv`, `episode_row_quarter_map.csv`, `episodes_relabelled.csv`, `episodes_fiscal.csv`, `structural_breaks_jumps.csv`, `ltim_sign_scan.csv`, `hcl_divestiture_check.csv`
- Scripts: `scripts/audit/*.py`

## Not fixed at source (outside the brief)

The parser bug in `scripts/extract/ltim_parse_tables.py` (`parse_num`) and the attrition ranking in `scripts/01_build_tidy.py` (`pick()`) are both corrected downstream here. The original scripts were left unchanged.
