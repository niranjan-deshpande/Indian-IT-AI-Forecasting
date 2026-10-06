# India IT pilot: final pass before the write-up

*Date: 2026-10-05. Detailed inputs for the note are in `note_inputs.md`.*

To regenerate the data, tables and figures with one command, run `python3 scripts/final/make_all.py`. Add `--ltim` to re-extract the LTIM raw file with the fixed parser first.

The run includes a reproduction check: the source-fixed pipeline reproduces the previous round's `data/corrected/*_corrected.csv` exactly.

## How the work was split

- **Done directly:** Tasks 1, 3 and 5.
- **Task 2 used two agents.** The first re-scanned the transcripts and coded the statements as coder 1. The second coded the same statements independently, as coder 2.
  - The first agent split the full read across 32 parallel readers, despite the request to limit subagents. The second agent worked alone.
- **Task 4 used one agent,** working alone.
- **Spot checks done by hand:**
  - all six note quotes, verbatim against the transcripts;
  - the Accenture Q4FY26 figures;
  - the TCS subcontracting figures;
  - Persistent FY24 revenue and headcount;
  - both BLS results.

---

## Task 1: Audit decisions and rebuilt data

### Decisions applied

1. **LTI counted once.** LTI + Mindtree are combined through FY22, and LTIMindtree is used from FY23. LTIMindtree's restated history covers FY22, so FY23 growth uses one entity in both years. No period includes both.
2. **HCLTech divestiture: adjust neither revenue nor headcount.**
   - No revenue figure for the divested State Street JV was disclosed. The only number is a forward-looking "80-bps impact" on FY25 guidance (Q1FY25 call); none appears in the investor releases.
   - The 7,398 headcount-base adjustment (D10) is therefore removed. HCLTech's FY25 headcount growth becomes −1.6%, against +1.7% when adjusted. This moves the six-firm simple average by about 0.6 pp.
3. **Wipro.** Growth observations spanning a level break are set to missing; levels are kept.
   - ISRE perimeter change: YoY windows 2017Q2–2018Q1, for headcount growth and USD revenue growth.
   - Alight staff transfer (Q2FY19): headcount growth for 2018Q3–2019Q2.
   - Firm-reported cc growth is kept, because each figure is like-for-like within its own release.
4. **Script bugs fixed at source.**
   - `scripts/extract/ltim_parse_tables.py`: `parse_num` now reads "(3.7)%" as negative.
   - `scripts/01_build_tidy.py`: `pick()` ranks period types in the order listed (trailing-twelve-month before quarterly) and uses a stable sort.
   - `scripts/extract/ltim_build.py`: a `LTIM_OUT` environment variable now lets the output go elsewhere, so `data/raw/` is not overwritten. The default path is unchanged.
   - Checks:
     - The unfixed builder reproduces `data/raw/ltim.csv` byte for byte.
     - The fixed parser changes exactly the 22 audited cells and nothing else.
     - The fixed `pick()` changes exactly the 2 Cognizant attrition cells.
     - The full fixed pipeline reproduces `data/corrected/` exactly.
5. **Accenture Q4FY26 added** from the 1 Oct 2026 8-K (`audit/new_raw_accenture_q4fy26.csv`).
   - Its quarter ends in August, so it maps to calendar 2026Q3, which is Indian Q2FY27. It therefore does not enter Table A.
6. **Acquisitions:** not adjusted.

### Tables and figures

Built by `scripts/final/tables_figures.py`; nothing was hand-computed.

- **Table A** (`output/final/table_A.md`, `.csv`; firm-level inputs in `table_A_firms.csv`).
  - Rows: FY16–FY26, plus FY27 Q1 labelled as one quarter.
  - Columns: revenue growth in USD and in constant currency (cc); headcount growth (average-based, plus a year-end version); revenue per employee (USD and cc); utilization change; residual.
  - Shown for: the Indian simple average, the Indian revenue-weighted average, Accenture and Cognizant.
  - Comparators are aggregated to Indian fiscal years. Accenture's year runs Mar–Feb, so 11 of 12 months overlap.
  - Firm lists are given for each year.
- **Table B** (`output/final/table_B.md`): mean residual and mean utilization change, FY16–FY23 against FY24–FY26. Variants: excluding FY21, and same firms in both windows.
- **Figure 1** (`figures/final/fig1_india_vs_comparators.png`, `.svg`): the Indian revenue-weighted average against Accenture and Cognizant, FY16–FY26. Three panels (revenue cc, headcount, revenue per employee cc), with FY24 marked.
- **Figure 2** (`figures/final/fig2_subcontracting_share.png`, `.svg`): subcontracting cost as a share of revenue for the six Indian firms, FY20–FY26. LTIMindtree starts at FY22.

### Definitions

- **Growth:** log change × 100.
- **Fiscal-year revenue growth:** quarterly YoY growth aggregated with prior-year revenue weights. For USD revenue, this equals the log change of fiscal-year revenue.
- **Headcount growth:** the mean of the four quarterly YoY changes, which approximates growth of average headcount.
- **Utilization change:** the mean of quarterly YoY changes within each firm's own series.
- **Residual:** revenue-per-employee growth (cc) minus utilization change.
- **Completeness:** a fiscal-year value requires all four quarters.

### Key numbers (`note_numbers.csv`)

| Indian six | FY16–20 mean | FY22 | FY23 | FY24 | FY25 | FY26 |
|---|---|---|---|---|---|---|
| Headcount, simple | +7.4 | +18.5 | +14.3 | **−3.6** | −0.5 | +1.2 |
| Headcount, revenue-weighted | +7.2 | +17.2 | +13.9 | **−2.8** | −0.8 | +0.6 |
| Revenue cc, simple | +8.7 | +16.7 | +12.8 | +0.7 | +2.6 | +1.4 |
| Revenue per employee cc, simple | +2.5 | +0.0 | −0.8 | +4.4 | +3.1 | +0.2 |

**Table B** (mean residual, by window):

| firm set | FY16–23 | FY16–23 excl. FY21 | FY24–26 |
|---|---|---|---|
| All firms with data | +1.1 | +2.1 | +1.3 |
| Same firms (Infosys, Tech Mahindra, Wipro) | +0.5 | +1.7 | +0.9 |

**Subcontracting share fell FY23 → FY24 at all six firms:**

| | TCS | Infosys | HCLTech | Wipro | Tech Mahindra | LTIMindtree |
|---|---|---|---|---|---|---|
| FY23 | 9.5 | 9.6 | 14.7 | 12.7 | 15.0 | 8.5 |
| FY24 | 6.6 | 8.0 | 13.3 | 11.5 | 12.9 | 7.2 |

---

## Task 2: Earnings-call statements

### Extraction

The method is documented in `calls_codebook.md`.

- **Transcripts:** the same 183 transcripts as the pricing pass, listed in `audit/calls_transcripts.csv`. TCS Q4FY23 is still missing.
- **Demand re-scan:**
  - 1,711 statements (`audit/demand_calls_quotes.csv`; dictionary in `audit/calls_demand_dictionary.json`).
  - Every transcript was effectively read in full; about 9.3 statements were kept per call.
  - Rules were the same as the pricing pass: verbatim (machine-checked), management only, speaker confirmed, page re-derived.
- **Merged total:** 389 + 1,711 − 13 cross-pass duplicates = **2,087 statements** (`audit/calls_statements.csv`; duplicates logged in `audit/calls_merge_log.csv`).
- **Scripts:** `scripts/audit/calls_*.py`.

### Codebook and reliability

- **Codebook** (`calls_codebook.md`): categories A–E, 7 decision rules, and one verbatim example per category.
- **Coder 2** was a separate agent. It received only the codebook and a shuffled file of quotes with context notes. It did not see coder 1's codes or which pass each statement came from.
- **Agreement on the primary category:** **92.1%**, Cohen's κ = **0.87** (`output/final/calls_agreement.csv`, `calls_confusion.csv`).

| category | coder 1 count | coder 2 count | coder 1's codes matched by coder 2 | positive agreement | κ |
|---|---|---|---|---|---|
| A | 796 | 743 | 91.0% | 94.1% | 0.91 |
| B | 47 | 54 | 87.2% | 81.2% | 0.81 |
| C | 72 | 83 | 76.4% | 71.0% | 0.70 |
| D | 117 | 91 | 70.1% | 78.8% | 0.78 |
| E | 1,055 | 1,116 | 96.8% | 94.1% | 0.88 |

- **Agreement by pass:** 81.5% on pricing-pass statements, 94.6% on demand-pass statements.
- **Main disagreements:**
  - 71 statements coded A by coder 1 and E by coder 2. These are mostly mixed strength/weakness statements.
  - 22 statements coded D by coder 1 and C by coder 2. In these the AI link is implied but not named.
- **Disagreements:** all 164 are in **`calls_disagreements.csv`**, unresolved, with a `resolved_primary` column to fill in.
- **Spot-check:** 30 statements drawn with seed 20261006, showing both codings, in `calls_spotcheck.csv`.

### Figure 3

- **Files:** `figures/final/fig3_call_categories.png` and `.svg` (coder 1 codes); `fig3_call_categories_coder2.png` (coder 2 codes); data in `output/final/fig3_data.csv`.
- **What it shows:** statements per transcript by category and half-year, 2021H1–2026H2. Transcript counts appear under the axis. Panels are split by scale.

Statements per transcript (coder 1):

| category | 2021–22 | 2023 | 2024H2–2026H1 | 2026H2 |
|---|---|---|---|---|
| A, demand weakness | 0.4–1.4 (3.0 in 2022H2) | 7.5–7.9 | 4.7–5.7 | 5.9 |
| D, AI pass-through | 0–0.1 | 0.3 | 0.6–1.6 | 3.0 (8 transcripts) |

- **Robustness:** coder 2's codes give the same pattern.
- **Caveat:** A comes mostly from the broader demand pass (about 9 statements per call), and D from the pricing pass (about 2). Compare trends within a category, not levels across categories.

### Quotes (`note_quotes.md`)

All six were re-verified verbatim on the cited page (`scripts/final/verify_note_quotes.py` → `output/final/note_quotes_check.csv`). Both coders agree on every one.

| # | category | firm, call, date | speaker | quote |
|---|---|---|---|---|
| 1 | A | Infosys Q2FY24, 12 Oct 2023 | Salil Parekh | "We continue to see the overall environment where digital transformation program and discretionary spends are low and decision-making is slow. This is impacting our volumes." |
| 2 | A | TCS Q2FY24, 11 Oct 2023 | K Krithivasan | "Our growth was affected by the holding back of discretionary spends by clients." |
| 3 | B | TCS Q3FY24, 11 Jan 2024 | Samir Seksaria | "…Pricing environment is stable…" |
| 4 | D | TCS Q4FY25, 10 Apr 2025 | K Krithivasan | "…we will try to share those gains with our customers… what we did with $100 if we are able to do with $95 or $90." |
| 5 | D | HCLTech Q4FY26, 21 Apr 2026 | C. Vijayakumar | "…would translate to 2% to 3% for our portfolio." |
| 6 | D | HCLTech Q4FY26, 21 Apr 2026 | C. Vijayakumar | "$100 million deal would be much lesser today - maybe 80 million…" |

The full quotes, URLs and page numbers are in `note_quotes.md`.

---

## Task 3: Price index check

Added to `price_data.md` §A2b; files are in `data/explore/prices/final_bls/`.

- **NAICS 5415 / 541511 / 541512: no BLS producer price index exists.**
  - The BLS API returns "Series does not exist" for PCU5415--5415--, PCU541511541511 and PCU541512541512.
  - The current and discontinued industry lists have no 5415 code.
  - BLS's [Areas of Noncoverage](https://www.bls.gov/ppi/fd-id/areas-of-noncoverage-in-the-ppi-system.htm) page (last modified March 4, 2026) lists 541511, 541512, 541513 and 541519 as not covered.
- **NAICS 518210, PCU518210518210** (data processing, hosting and related services; base Dec 2000 = 100).
  - According to the [BLS fact sheet](https://www.bls.gov/ppi/factsheets/producer-price-index-for-the-data-processing-and-related-services-industry-naics-518210.htm) (last modified Nov 7, 2008), it was introduced in January 2002 with history from December 2000. It is priced by repricing actual contracts with fixed characteristics.
  - Annual-average growth:

| 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (Jan–Aug YoY) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| +0.3 | +1.2 | +1.5 | +0.3 | +0.5 | +2.9 | +1.0 | +1.0 | +1.5 | +1.3 | +3.3 | +0.5 |

  - May–Aug 2026 values are preliminary.
  - **Label:** a US domestic producer price, used as a proxy for offshore Indian vendors' prices, not as a measure of them.

---

## Task 4 (optional): Mid-tier Indian firms

Files are in `data/explore/midtier/` (raw rows with citations, annual file, comparison file); source documents are in `data/sources/midtier/`. These firms are not in the main tables.

**Coverage, FY20–FY26:**
- **Persistent:** complete.
- **Mphasis:** complete. FY20 comes from the FY21 report, because the FY20 report link returns 404.
- **Coforge:** complete, except FY20 USD revenue (INR only).
- **Hexaware:** reports calendar years (CY2019–CY2025). Each is aligned to the Indian fiscal year ending three months later.

| | FY24 | FY25 | FY26 |
|---|---|---|---|
| Top-six revenue growth (USD) | +2.0 | +2.7 | +2.2 |
| Mid-tier four revenue growth (USD) | +5.0 | +14.7 | +13.9 |
| Top-six year-end headcount growth | −4.5 | +1.0 | −0.2 |
| Mid-tier four year-end headcount growth | +0.7 | +10.7 | +5.6 |

- **Share gain.** The mid-tier share of combined revenue rose from 5.1% (FY21) to 7.3% (FY26); its share of headcount rose from 5.5% to 7.3%. The mid-tier firms gained share while the top six stalled.
- **Acquisitions are included:** Coforge–Cigniti (FY25), Mphasis–Silverline (FY24), Persistent (FY22) and Hexaware's deals. Excluding Coforge, FY25 revenue growth for the other three is still +10.9.
- **Headcount definitions differ:** Mphasis and Hexaware include contractors.

---

## Task 5: Note inputs

Written to `note_inputs.md`, organised by the note's eight sections plus a 1b subsection on the mid-tier firms. Every number traces to a repo file (mostly `output/final/note_numbers.csv`, `table_A.*`, `table_B.*`, `fig2_data.csv`, `fig3_data.csv`, `calls_agreement.csv`) or to a cited external source. There are 16 limitations, one line each.

---

## Every data change in this pass

All are logged in `data/corrected/CHANGELOG.csv`, which now has 193 rows: 105 from the audit round (also kept in `CHANGELOG_v1_audit.csv`) and 88 from this pass. The final files are `data/corrected/core_quarterly_final.csv` and `yoy_metrics_final.csv`; the previous `*_corrected.csv` files are untouched.

1. **Source fixes (decision 4).**
   - The 22 LTI/Mindtree sign cells and the 2 Cognizant attrition cells (2021Q2: 29 → 18; 2021Q3: 33 → 24) are now produced by the fixed code instead of applied as corrections. Values are the same as before.
   - The fixed LTIM raw file is `data/rebuilt/raw/ltim.csv`; `data/raw/ltim.csv` is unchanged.
2. **HCLTech (decision 2).** The divestiture adjustment is removed. Headcount growth for 2024Q2 / Q3 / Q4 / 2025Q1:

| | 2024Q2 | 2024Q3 | 2024Q4 | 2025Q1 |
|---|---|---|---|---|
| Before | +1.54 | +2.26 | +1.55 | +1.50 |
| After | −1.82 | −1.15 | −1.80 | −1.80 |

   Revenue-per-employee growth for those quarters changes accordingly.
3. **Wipro (decision 3).**
   - Headcount growth set to missing for 2017Q2–2018Q1 (ISRE) and 2018Q3–2019Q2 (Alight).
   - USD revenue growth set to missing for 2017Q2–2018Q1.
   - The derived revenue-per-employee growth and residual are missing for the same quarters.
4. **Accenture Q4FY26 (decision 5).** New raw rows, all from the 1 Oct 2026 8-K Ex.99:
   - revenue $18,679.11M;
   - growth +6% in USD, +7% in local currency;
   - new bookings $22,170M;
   - headcount 814,000. This is a rounded figure: the release says "approximately 814,000 people".
   - Utilization and attrition are not available: the presentation returns 403 and is not archived, and the 10-K is not yet filed.
   - Derived 2026Q3 values: cc revenue growth +6.77, USD revenue growth +5.97, headcount growth +4.36.
5. **LTI counted once (decision 1):** done at aggregation in the tables script; no data change.

**Files modified in place:** the three scripts in decision 4 (as instructed) and `price_data.md` (Task 3). No original data file, simulation code or existing write-up was modified.

---

## What contradicts or qualifies the note's five claims

1. **"Headcount growth collapsed after FY23": supported, with qualifiers.**
   - The six-firm average fell from +14.3% (FY23) to −3.6% (FY24), against a +7.4% FY16–20 mean. Headcount fell at 5 of 6 entities in FY24; HCLTech was the exception at +2.1%.
   - The comparators slowed too: Accenture +1.5% (FY24); Cognizant −0.9% (FY24) and −2.6% (FY25).
   - The mid-tier Indian firms grew strongly, so this is not a sector-wide collapse.
   - FY23 itself is the end of the FY22 hiring boom, not a normal year.
2. **"The identity rules out S2": weaker than stated.**
   - After FY23 the residual changes by −0.8 to +0.4 pp, depending on the firm set and on whether FY21 is included. S2 predicts a rise of several points.
   - But the test covers only Infosys, Wipro, Tech Mahindra and the LTI group. TCS and HCLTech, the two largest, report no utilization.
   - TCS's revenue per employee accelerated in FY24–25 (+4.2 and +3.9, against +1.7 in FY16–20) and cannot be decomposed.
   - Infosys's residual reached +6.6 in FY24. That may be mechanical: utilization excludes trainees while headcount includes them, and fresher intake collapsed.
   - So the data rule out a large S2 effect at those four firms, not at all six. The second half of the claim (S1 and S3 are equivalent under full pass-through) follows from the identity and is unaffected.
3. **"Subcontracting share fell in FY24, ruling out the subcontractor version of S4": holds for FY24–25.**
   - The share fell at all six firms in FY24.
   - It rose again at 5 of 6 in FY26, though all six remain below FY23.
   - It is a cost ratio, not contractor FTEs.
4. **"No public source measures output prices for Indian IT services": holds for Indian vendors specifically.**
   - ISG publishes measured unit-price declines for a narrow slice of managed-services contracts, across all vendors.
   - The BLS 518210 index is a contract output price for US domestic firms.
5. **"Explanations shifted from demand weakness to AI pass-through": partly.**
   - Pass-through (D) statements rose from about 0.1–0.3 per transcript before mid-2024 to 0.6–1.6 from 2024H2 to 2026H1.
   - Demand-weakness (A) statements stayed high: 4.7–5.9 per transcript in 2024H2–2026H2, down from 7.5–7.9 in 2023.
   - Pass-through talk was added to demand talk, not substituted for it. The pattern holds under both coders.

---

## Judgment calls you may want to revisit

- **HCLTech:** I treated the "80-bps" guidance remark as not a disclosure of divested revenue. If you count it as disclosed, adjusting both revenue and headcount takes one small change.
- **Wipro:** firm-reported cc revenue growth is kept across the ISRE and Alight windows, because each figure is like-for-like within its own release. Only level-based growth is excluded.
- **Accenture Q4FY26 headcount:** a rounded boilerplate figure. Replace it with the exact count when the 10-K or presentation is available.

---

## New files in this pass

**Note documents:** `note_inputs.md`, `note_quotes.md`, `calls_codebook.md`, `calls_disagreements.csv`, `calls_spotcheck.csv`, `FINAL_PASS_SUMMARY.md`.

**Data:**
- `data/corrected/core_quarterly_final.csv`, `yoy_metrics_final.csv`, `CHANGELOG.csv`, `CHANGELOG_v1_audit.csv`
- `data/rebuilt/raw/ltim.csv`
- `data/explore/midtier/`
- `data/explore/prices/final_bls/`
- `data/sources/accenture/final_q4fy26/`, `data/sources/midtier/`

**Tables:** `output/final/` — `table_A.*`, `table_B.*`, `table_A_firms.csv`, `note_numbers.csv`, `calls_agreement.csv`, `calls_confusion.csv`, `fig2_data.csv`, `fig3_data*.csv`, `note_quotes_check.csv`.

**Figures:** `figures/final/` — `fig1_india_vs_comparators`, `fig2_subcontracting_share`, `fig3_call_categories`, `fig3_call_categories_coder2` (PNG and SVG each).

**Audit files:** `audit/calls_transcripts.csv`, `calls_statements.csv`, `calls_statements_for_coder2.csv`, `demand_calls_quotes.csv`, `calls_demand_dictionary.json`, `calls_merge_log.csv`, `calls_coding_coder1.csv`, `calls_coding_coder2.csv`, `new_raw_accenture_q4fy26.csv`.

**Scripts:** `scripts/final/` — `make_all.py`, `build_final_data.py`, `tables_figures.py`, `calls_analysis.py`, `verify_note_quotes.py`, `note_numbers.py`; and `scripts/audit/calls_*.py`.
