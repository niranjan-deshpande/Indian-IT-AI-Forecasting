# Audit 1a — spot-check, currency/units, headcount definitions

(Written by the Task 1a audit agent; saved verbatim by the orchestrator because the agent could not write .md files. Row-level evidence: `audit/spotcheck_1a.csv`, `audit/corrections_1a.csv`.)

## 1. Spot-check

**Design.** Seed 20261005 (numpy `default_rng`). 26 cells drawn from the selected vintages in `panel_long.csv` (firm files only, 2015Q2 onward), stratified so each of the 8 firms plus LTI and Mindtree gets 3 of 6 metric groups (revenue USD, headcount, utilization, attrition, vertical share, cc YoY growth); each draw given a target year from a seeded permutation of 2015–2026. 4 more cells from `gfc.csv` (TCS headcount, Infosys revenue, Wipro utilization, Accenture attrition).

**Result: 30 of 30 match.** Values read from the documents themselves (pdftotext for PDFs, openpyxl for the TechM xlsx, HTML parsing for EDGAR, visual read for image-only slides). 18 of 30 checked against freshly downloaded copies — 15 live (EDGAR ×8, wipro.com, hcltech.com, ltm.com, TechM xlsx, investor.accenture.com PDF) and 3 via Wayback (Infosys ×2, TCS GFC). Every downloaded PDF/xlsx was md5-identical to the cache, every EDGAR file text-identical, so the cached files are the genuine primary documents. TCS 2015+ fact sheets could only be checked from the cache (tcs.com 403; Wayback 429 during the audit).

| metric group | n | match | live/Wayback |
|--|--|--|--|
| revenue USD | 6 | 6 | 5 |
| headcount | 7 | 7 | 4 |
| utilization | 7 | 7 | 3 |
| attrition | 5 | 5 | 2 |
| vertical share | 3 | 3 | 0 |
| cc YoY growth | 3 | 3 | 3 |

**Propagation to `core_quarterly.csv`.** 27 sampled cells feed a core column; all arrive unchanged except S21 (Cognizant 2022Q3 attrition: raw 29.0, core 29.2) — intended, because `ATTR_DIM` prefers the Tech Services TTM series.

**Systematic issues found by targeted tests** (rows T01–T08 in `spotcheck_1a.csv`):
1. **Mindtree negative growth stored as positive.** Mindtree prints negatives as "(3.7)%"; all 211 Mindtree growth rows in `ltim.csv` are ≥ 0. Testing every total-growth row against the sign implied by USD levels, and re-parsing all 104 segment-growth rows from the PDFs, found 16 errors: total YoY Q2FY21 (−3.7) and Q3FY21 (−0.4) — both reach core `rev_rep_yoy`; total QoQ Q2FY17 (−3.0), Q3FY17 (−0.4); 12 segment cells in FY22–FY23 releases. LTI and LTIM rows are fine (225 and 78 negatives present). (Task 1b found 6 more for LTI Q1FY18, same parser bug.)
2. **Cognizant attrition definition picked arbitrarily.** For 2020Q1–2021Q4 `panel_long.csv` holds both TTM and quarterly-annualized voluntary attrition under dimension `total`; `pick()` ranks only by dimension with an unstable sort. Core got quarterly-annualized in 2021Q2 (29 vs TTM 18) and 2021Q3 (33 vs TTM 24). No other core column has this ambiguity. Suggested fix: rank `ltm` before `quarter` in `pick()`.
3. **GFC-era non-comparable rows:** TCS 2007Q1 `rev_usd` (convenience translation); Wipro 2007Q1 headcount (old perimeter); TCS/TechM GFC `rev_rep_yoy` is INR growth labelled "reported".

## 2. Currency and units

**How `01_build_tidy.py` chooses.** Fixed unit/basis filters, no fallback: `rev_usd` USD_mn only; `rev_cc_yoy`/`rev_cc_qoq` `basis=cc` only; `rev_rep_yoy` `basis=reported` only; `gR = 100·ln(1+rev_cc_yoy/100)` cc only (quarters without cc stay NaN); `gR_usd` from USD levels. INR crore ×10 → INR mn; TCV USD bn ×1000 → USD mn. `subcon_share` uses a same-currency denominator (INR for all firms except TCS, which uses USD).

**(a) USD revenue.** Every firm-quarter 2015+ is reported USD; none missing or INR-converted. Exceptions:
- Wipro: IT Services segment only (no consolidated USD revenue published). 2007–2012 missing because GFC rows are company totals, dropped by the IT Services dimension filter.
- TCS 2007Q1: INR 51,464 mn translated at Rs 43.47/USD ("INR numbers of Q4 FY07 are converted to USD on convenience translation basis @ Rupees 43.47 per USD", TCS Q4FY07 deck p11/p15). → set_missing.
- Accenture: the latest-vintage rule takes FY18 (2017Q4–2018Q3) from the FY19 releases' ASC 606 restated columns, while FY17 and earlier stay "net revenues" (e.g. Q1FY18 first reported $9,523 mn, restated $9,884 mn). `gR_usd` for those 4 quarters is 13.8–18.7 log points vs reported USD growth of 12/15/16/11% — ~3–4 pp too high. `gR` unaffected. (Corrected at YoY level by Task 1b.)

**(b) cc labelling.** Every core `rev_cc_yoy` comes from a `basis=cc` row (e.g. TechM fact sheet has separate Reported and CC columns; Q1FY20 release: "Revenue growth at 3.7% in constant currency terms"). cc equals reported in only 7 firm-quarters, all genuine (e.g. Accenture Q1FY22 "27% | 27%"). `rev_rep_yoy` mislabelled in the GFC period: TCS 2007Q1–2010Q2 and TechM 2007–2012 are INR growth (TCS Q4FY08 deck p8: "Consolidated US GAAP (INR Million) … Total Revenue … % Growth Y-o-Y 18.43%"; TechM Q3FY09: "Consolidated Revenues at Rs.11,322 million for the quarter, up 17%"); flag_only. Wipro: growth rates as first reported but levels restated (ISRE restatement reaches back only to Q1FY18), so `gR_usd` and `rev_rep_yoy` diverge ~2 pp in 2017Q2–2018Q1; flag_only.

**(c) What `gR` is.** cc YoY only, each firm's own measure:

| firm | definition | source |
|--|--|--|
| Infosys | "comparing current period revenues in respective local currencies converted to US $ using prior period exchange rates" | Q1FY27 fact sheet (6-K Ex.99.4) |
| Wipro (IT Services) | "product of volumes in that period times the average actual exchange rate of the corresponding comparative period" | Q3FY26 datasheet, Note 1 |
| Cognizant | "revenues … restated at the comparative period's foreign currency exchange rates" | Q4 2022 supplement, p17 |
| Accenture | "'in local currency' … restating current period activity into U.S. dollars using the comparable prior year period's foreign currency exchange rates" | 10-Q, quarter to 31 May 2026 |
| TCS, HCLTech, TechM, LTI/LTIM, Mindtree | no definition found in documents checked | — |

Accenture "local currency" = same concept as Indian cc; printed in whole percents in 64 of 68 quarters (up to ±0.5 pp rounding). Coverage gaps stay NaN: TCS before 2015Q2, Cognizant before 2017Q1, TechM 30 of 66 quarters, LTIM from 2022Q4, Mindtree 1 quarter. `03_part2.py` uses `gR_usd` for GFC bars and cc later (labelled in chart).

**(d) Units by series.**

| series | TCS | Infosys | HCLTech | Wipro | TechM | LTI / Mindtree / LTIM | Cognizant | Accenture |
|--|--|--|--|--|--|--|--|--|
| rev_usd | USD mn; **2007Q1 convenience-translated** | USD mn | USD mn | USD mn, **IT Services; missing 2007–12** | USD mn | USD mn | USD mn (from thousands) | USD mn; **net revenues to FY17, ASC 606 from FY18** |
| rev_inr | INR mn | cr→mn | cr→mn | INR mn | INR mn | INR mn | — | — |
| rev_cc_yoy | cc | cc | cc | cc (IT Services) | cc | cc | cc | local currency |
| rev_rep_yoy | USD; **GFC = INR** | USD | USD (to Q1FY23) | USD (as first reported) | USD; **GFC = INR** | USD; **Mindtree sign errors** | USD | USD |
| attrition | LTM, IT Services | mixed definitions (logged) | LTM (IT Services → company) | voluntary TTM | LTM; GFC quarterly-annualized | LTM/TTM | **mixed TTM / quarterly-annualized**, then Tech Services TTM | quarterly-annualized voluntary |
| util0 | excl. trainees (to Q3FY16) | excl. trainees | incl. trainees (to Q4FY19) | net, excl. trainees | incl. trainees | LTI excl. / Mindtree incl. / LTIM excl. | offshore → blended | single figure, mapped to incl. |
| subcon | **USD mn** (COR + SG&A) | cr→mn | cr→mn | INR mn | INR mn | Mindtree INR mn | — | — |
| tcv | bn→mn | USD mn (large deals) | USD mn | USD mn (≥$30mn deals) | USD mn | Mindtree USD mn; LTIM bn→mn | bn→mn, TTM | USD mn bookings |

Apart from bold cells, no unit inconsistencies. TCV definitions differ by firm (already logged).

## 5. Headcount definitions
BRSR figures as of 31 Mar 2025 unless noted (BRSR rows from the research sub-agents; fact-sheet rows verified by 1a).

| firm | trainees | contractors | BPO / subsidiaries / support | definition changes (verified) |
|--|--|--|--|--|
| TCS | not stated | excluded: fact sheet 607,979 = BRSR permanent; other-than-permanent 28,854, "individuals on direct TCS contracts or through third party" (IAR 2024-25, PDF p.131) | includes subsidiaries (IAR 10-year table, p.95) | **2009Q1 (Q4FY09):** e-Serve and Diligenta added (Q3FY09 deck p16: "TCS : 126,613 (Excluding 12,459 TCS e-Serve employees)"; Q4FY09 deck p19: "* CMC, WTI, TCS e-Serve, Diligenta & others"). None 2015–26. |
| Infosys | **included** (20-F FY2016: "182,329 are software professionals, including trainees"; 20-F FY2026: "…including trainees"; Q4FY18 fact sheet p5 lists "Trainees 5,252") | excluded: 31 Mar 2024 BRSR permanent 317,240; other-than-permanent 23,447, "'Other than permanent' employees includes contractors" (IAR 2023-24, p.159) | consolidated incl. BPM/subsidiaries | none in definition; trainee breakdown dropped after Q4FY18 |
| HCLTech | not stated | excluded: 223,420 = 167,316 company + 56,104 subsidiaries (Directors' report p.130; BRSR p.187); other-than-permanent 11,076 | Technical + Sales & Support; subsidiaries included | **Q1FY25:** divestiture 7,398 (Q1FY25 release p3: "Reduction in headcount due to divestiture (7,398)") — `DIVEST` adjustment correct. Label changes only (Q2FY20, Q2FY23). |
| Wipro | not stated | pre-FY18 "Head Count" included contractors & retainers (AR 2016-17 p.52: "Employee count for IT Services as on March 31, 2017 is 165,481. In addition, contractors and retainers augment our employees."). Current 233,346 sits between BRSR permanent 225,306 and BRSR total 235,415 (IAR 2024-25 p.482): not reconciled | "Closing Employee Count – IT Services" | **Q4FY17:** both series shown (181,482 vs 165,481); repo series starts Q4FY16 on the new basis — correct. **Unlogged:** Q3FY19 ISRE restatement reaches back only to Q1FY18, so FY17 is old perimeter and `gL` 2017Q2–2018Q1 biased ≈−3 pp. **Unlogged step Q2FY19 (+6.6% QoQ):** "About 9000 employees come for the large deal which we had won from Alight" (Q2FY19 call p15). **Q2FY25 Note 6** corrections (Q3'24 239,655; Q4'24 232,614; Q1'25 232,911; Q4FY23 258,570): core uses corrected values. **GFC:** 2007Q1 (67,818) old Global IT perimeter. |
| TechM | not stated | **included (direct contractors):** fact sheet 148,731 = BRSR 139,271 (131,444 permanent + 7,827 directly contracted) + 9,460 non-integrated subsidiaries (IAR FY25 p.125) | Software + BPO/BPS + Sales & support | BPO→BPS label only; GFC excludes Satyam |
| LTIMindtree | not stated | excluded: 84,307 permanent + 3,782 "Non-FTE Subcontractors" = 88,089 (FY25 BRSR p.3; MD&A p.153) | Software professionals + Sales & Support | **Merger:** Q1FY22 restated 63,696 vs LTI 38,298 + Mindtree 27,256 = 65,554 (−1,858); verified LTIM Q3FY23 fact sheet p16, LTI Q1FY22 p10, Mindtree Q1FY23 p13. No splice. |
| LTI / Mindtree | not stated | not stated | Development + Sales & Support / Software + S&M + G&A | none found |
| Cognizant | not stated | excluded implicitly (10-K FY2025: "Historically, subcontractor usage has been immaterial relative to our overall headcount") | company-wide; 2014Q4 "includes approximately 3,770 employees from the acquisition of TriZetto" (10-K FY2014); Belcan from Q3 2024 | 2009Q3 "more than 68,000" is a lower bound |
| Accenture | not stated | not stated | "Represents the total number of Accenture employees" (Q3FY26 deck p17) | none found |

All BRSRs report zero "workers".

**YoY headcount outliers >|15%| outside 2021–22 (2015–2026):** Accenture 2015Q4–2016Q1 consistent across three sources, no break; Cognizant 2015Q1–Q2 partly TriZetto, 2016Q3–Q4 no break found; HCLTech 2015Q2 and 2019Q2–Q3 (IBM products deal closed 30 Jun 2019, no headcount effect stated); LTI 2017–2019 and Mindtree 2018Q4 organic. GFC outliers explained by TCS e-Serve, HCL Axon, Wipro perimeter (in `gfc_NOTES`); TechM 2009Q4–2011 surge unexplained.

## Proposed corrections (`audit/corrections_1a.csv`, 28 rows)
1. replace — Mindtree sign errors (16 raw rows).
2. replace — core `rev_rep_yoy` Mindtree 2020Q3 3.7→−3.7, 2020Q4 0.4→−0.4.
3. replace — core attrition Cognizant 2021Q2 29→18, 2021Q3 33→24.
4. set_missing — TCS 2007Q1 `rev_usd`.
5. set_missing — Wipro 2007Q1 headcount.
6. flag_only — Accenture `rev_usd` 2017Q4–2018Q3 (ASC 606 mix); Wipro headcount and `rev_usd` 2017Q2–2018Q1 (ISRE perimeter); Wipro 2018Q3 headcount (Alight); TCS 2009Q1 headcount (e-Serve/Diligenta); TCS 2007Q1–2010Q2 and TechM 2007–2012 `rev_rep_yoy` (INR labelled reported).

Not added (unverified): Cognizant 2019Q1–Q4 attrition is quarterly-annualized per repo notes, while 2020+ is TTM.
